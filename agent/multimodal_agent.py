"""
Multi-Modal LangChain Agent
Orchestrates tools for visual and textual reasoning
"""
from typing import Optional, Dict, Any
from langchain_classic.agents import create_react_agent, AgentExecutor
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_community.llms import HuggingFacePipeline
from agent.tools import get_all_tools
from config import Config
import os


class MultiModalAgent:
    """
    Multi-modal agent that can reason about images and text
    using various tools including CLIP, BLIP, and web search
    """

    def __init__(self, use_openai: bool = None, temperature: float = 0.7):
        """
        Initialize the multi-modal agent

        Args:
            use_openai: Whether to use OpenAI API (default from config)
            temperature: Model temperature for generation
        """
        self.use_openai = use_openai if use_openai is not None else not Config.USE_LOCAL_MODELS
        self.temperature = temperature
        self.tools = get_all_tools()

        # Initialize LLM
        self.llm = self._initialize_llm()

        # Create agent
        self.agent = self._create_agent()

    def _initialize_llm(self):
        """Initialize the language model"""
        if self.use_openai and Config.OPENAI_API_KEY:
            print("Initializing OpenAI ChatGPT...")
            return ChatOpenAI(
                model="gpt-4o-mini",
                temperature=self.temperature,
                openai_api_key=Config.OPENAI_API_KEY
            )
        else:
            print("Using local reasoning mode (tool-only)...")
            # For local setup without OpenAI, use a simple reasoning wrapper
            return None

    def _create_agent(self):
        """Create the ReAct agent with tools"""
        if self.llm is None:
            # Simple tool executor without complex reasoning
            return None

        # ReAct prompt template
        template = """You are a multi-modal AI agent that can understand both images and text.
You have access to tools that can analyze images, answer questions about them, and perform other tasks.

TOOLS:
{tools}

Use the following format:

Question: the input question or task
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

When working with images:
1. First use image_captioner to understand what's in the image
2. Use image_qa for specific questions about the image
3. Use image_classifier when you need to categorize the image

Begin!

Question: {input}
Thought: {agent_scratchpad}"""

        prompt = PromptTemplate.from_template(template)

        agent = create_react_agent(
            llm=self.llm,
            tools=self.tools,
            prompt=prompt
        )

        return AgentExecutor(
            agent=agent,
            tools=self.tools,
            verbose=Config.VERBOSE,
            max_iterations=Config.MAX_ITERATIONS,
            handle_parsing_errors=True
        )

    def run(self, query: str, image_path: Optional[str] = None) -> Dict[str, Any]:
        """
        Run the agent with a query and optional image

        Args:
            query: Text query or question
            image_path: Optional path to image file

        Returns:
            Dictionary with response and metadata
        """
        # Prepare input
        full_query = query
        if image_path:
            full_query = f"Analyze the image at '{image_path}' and answer: {query}"

        try:
            if self.agent is not None:
                # Use LangChain agent
                result = self.agent.invoke({"input": full_query})
                return {
                    "success": True,
                    "response": result.get("output", ""),
                    "query": query,
                    "image_path": image_path
                }
            else:
                # Fallback: direct tool usage without agent reasoning
                return self._direct_tool_execution(query, image_path)

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "query": query,
                "image_path": image_path
            }

    def _direct_tool_execution(self, query: str, image_path: Optional[str]) -> Dict[str, Any]:
        """
        Execute tools directly without LLM reasoning
        Used when no OpenAI API key is available
        """
        from models.image_captioner import MultiModalAnalyzer

        response_parts = []

        if image_path:
            # Use multi-modal analyzer
            analyzer = MultiModalAnalyzer()

            # Generate caption
            response_parts.append(f"Image Analysis:")
            response_parts.append(f"Caption: {analyzer.captioner.generate_caption(image_path)}")

            # Answer specific question if provided
            if "?" in query:
                answer = analyzer.captioner.answer_question(image_path, query)
                response_parts.append(f"\nAnswer to '{query}': {answer}")

            # Detailed analysis
            detailed = analyzer.captioner.generate_detailed_description(image_path)
            response_parts.append(f"\nDetailed descriptions:")
            for q, a in detailed["descriptions"].items():
                response_parts.append(f"  - {q}: {a}")

        else:
            response_parts.append("No image provided. Please provide an image for analysis.")

        return {
            "success": True,
            "response": "\n".join(response_parts),
            "query": query,
            "image_path": image_path,
            "mode": "direct_execution"
        }

    def get_available_tools(self) -> list:
        """Get list of available tools"""
        return [{"name": tool.name, "description": tool.description} for tool in self.tools]


if __name__ == "__main__":
    # Test the agent
    agent = MultiModalAgent()

    print(f"\n{'='*60}")
    print("Multi-Modal Agent Initialized!")
    print(f"{'='*60}\n")

    print("Available Tools:")
    for tool_info in agent.get_available_tools():
        print(f"\n  - {tool_info['name']}")
        print(f"    {tool_info['description']}")

    print(f"\n{'='*60}")
    print("Agent ready for multi-modal reasoning!")
    print(f"{'='*60}\n")
