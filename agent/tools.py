"""
LangChain Tools for Multi-Modal Agent
"""
from langchain.tools import BaseTool
from typing import Optional, Type
from pydantic import BaseModel, Field
from PIL import Image
import requests
from io import BytesIO
import json


class ImageCaptionInput(BaseModel):
    """Input schema for image captioning tool"""
    image_path: str = Field(description="Path to the image file or URL")


class ImageCaptionTool(BaseTool):
    """Tool for generating image captions using BLIP"""

    name: str = "image_captioner"
    description: str = """Useful for describing what's in an image.
    Input should be a file path to an image.
    Returns a natural language description of the image content."""
    args_schema: Type[BaseModel] = ImageCaptionInput

    def __init__(self):
        super().__init__()
        from models.image_captioner import ImageCaptioner
        self.captioner = ImageCaptioner()

    def _run(self, image_path: str) -> str:
        """Execute the image captioning"""
        try:
            caption = self.captioner.generate_caption(image_path)
            return f"Image description: {caption}"
        except Exception as e:
            return f"Error generating caption: {str(e)}"

    async def _arun(self, image_path: str) -> str:
        """Async version"""
        return self._run(image_path)


class ImageQuestionInput(BaseModel):
    """Input schema for visual question answering"""
    image_path: str = Field(description="Path to the image file")
    question: str = Field(description="Question about the image")


class ImageQuestionTool(BaseTool):
    """Tool for answering questions about images (VQA)"""

    name: str = "image_qa"
    description: str = """Useful for answering specific questions about an image.
    Input should be a JSON with 'image_path' and 'question' fields.
    Returns an answer to the question based on the image content."""
    args_schema: Type[BaseModel] = ImageQuestionInput

    def __init__(self):
        super().__init__()
        from models.image_captioner import ImageCaptioner
        self.captioner = ImageCaptioner()

    def _run(self, image_path: str, question: str) -> str:
        """Execute visual question answering"""
        try:
            answer = self.captioner.answer_question(image_path, question)
            return f"Answer: {answer}"
        except Exception as e:
            return f"Error answering question: {str(e)}"

    async def _arun(self, image_path: str, question: str) -> str:
        """Async version"""
        return self._run(image_path, question)


class ImageClassificationInput(BaseModel):
    """Input schema for image classification"""
    image_path: str = Field(description="Path to the image file")
    labels: str = Field(description="Comma-separated list of possible labels")


class ImageClassificationTool(BaseTool):
    """Tool for classifying images using CLIP"""

    name: str = "image_classifier"
    description: str = """Useful for classifying an image into predefined categories.
    Input should be a JSON with 'image_path' and 'labels' (comma-separated) fields.
    Returns the most likely category and confidence scores."""
    args_schema: Type[BaseModel] = ImageClassificationInput

    def __init__(self):
        super().__init__()
        from models.clip_embedder import CLIPEmbedder
        self.embedder = CLIPEmbedder()

    def _run(self, image_path: str, labels: str) -> str:
        """Execute image classification"""
        try:
            label_list = [label.strip() for label in labels.split(",")]
            best_match, score, all_scores = self.embedder.find_best_match(image_path, label_list)

            result = f"Classification: {best_match} (confidence: {score:.2%})\n"
            result += "All scores:\n"
            for label, s in zip(label_list, all_scores):
                result += f"  - {label}: {s:.2%}\n"

            return result
        except Exception as e:
            return f"Error classifying image: {str(e)}"

    async def _arun(self, image_path: str, labels: str) -> str:
        """Async version"""
        return self._run(image_path, labels)


class CalculatorInput(BaseModel):
    """Input schema for calculator"""
    expression: str = Field(description="Mathematical expression to evaluate")


class CalculatorTool(BaseTool):
    """Tool for performing calculations"""

    name: str = "calculator"
    description: str = """Useful for performing mathematical calculations.
    Input should be a mathematical expression as a string.
    Returns the result of the calculation."""
    args_schema: Type[BaseModel] = CalculatorInput

    def _run(self, expression: str) -> str:
        """Execute calculation"""
        try:
            # Safely evaluate mathematical expressions
            allowed_chars = set("0123456789+-*/.() ")
            if not all(c in allowed_chars for c in expression):
                return "Error: Invalid characters in expression"

            result = eval(expression, {"__builtins__": {}}, {})
            return f"Result: {result}"
        except Exception as e:
            return f"Error calculating: {str(e)}"

    async def _arun(self, expression: str) -> str:
        """Async version"""
        return self._run(expression)


class WebSearchInput(BaseModel):
    """Input schema for web search"""
    query: str = Field(description="Search query")


class WebSearchTool(BaseTool):
    """Tool for searching the web (mock implementation)"""

    name: str = "web_search"
    description: str = """Useful for finding information on the internet.
    Input should be a search query string.
    Returns relevant information found online."""
    args_schema: Type[BaseModel] = WebSearchInput

    def _run(self, query: str) -> str:
        """Execute web search (mock)"""
        # Note: In production, integrate with actual search API (Google, Bing, etc.)
        return f"""Web search results for '{query}':

This is a mock web search tool. To enable real web search, integrate with:
- Google Custom Search API
- Bing Search API
- DuckDuckGo API
- Or use LangChain's built-in web search tools

For now, returning mock results based on query analysis."""

    async def _arun(self, query: str) -> str:
        """Async version"""
        return self._run(query)


def get_all_tools():
    """Get all available tools for the agent"""
    return [
        ImageCaptionTool(),
        ImageQuestionTool(),
        ImageClassificationTool(),
        CalculatorTool(),
        WebSearchTool(),
    ]


if __name__ == "__main__":
    # Test tools
    print("Available Tools:")
    tools = get_all_tools()
    for tool in tools:
        print(f"\n{tool.name}:")
        print(f"  {tool.description}")
