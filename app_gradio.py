"""
Gradio Web Interface for Multi-Modal AI Agent
Interactive demo with image upload and text queries
"""
import gradio as gr
from PIL import Image
import os
from pathlib import Path
from agent.multimodal_agent import MultiModalAgent
from models.image_captioner import MultiModalAnalyzer
from config import Config


class MultiModalApp:
    """Gradio application for multi-modal agent"""

    def __init__(self):
        """Initialize the application"""
        self.agent = None
        self.analyzer = None
        self.temp_dir = Path("temp_uploads")
        self.temp_dir.mkdir(exist_ok=True)

    def initialize_models(self):
        """Lazy load models when needed"""
        if self.analyzer is None:
            print("Loading models...")
            self.analyzer = MultiModalAnalyzer()
            self.agent = MultiModalAgent()
            print("Models loaded!")

    def process_image_query(self, image, query, analysis_type):
        """
        Process image and query through the multi-modal agent

        Args:
            image: PIL Image from Gradio
            query: User's text query
            analysis_type: Type of analysis to perform

        Returns:
            Tuple of (result_text, classification_text)
        """
        if image is None:
            return "Please upload an image first.", ""

        try:
            # Initialize models if needed
            self.initialize_models()

            # Save uploaded image temporarily
            image_path = self.temp_dir / "current_image.jpg"
            image.save(image_path)

            response = ""
            classification = ""

            # Basic caption
            if analysis_type in ["caption", "full"]:
                caption = self.analyzer.captioner.generate_caption(str(image_path))
                response += f"**Caption:** {caption}\n\n"

            # Detailed analysis
            if analysis_type in ["detailed", "full"]:
                detailed = self.analyzer.captioner.generate_detailed_description(str(image_path))
                response += "**Detailed Analysis:**\n"
                for question, answer in detailed["descriptions"].items():
                    response += f"- {question}\n  → {answer}\n"
                response += "\n"

            # Answer specific question
            if query and query.strip():
                if "?" in query:
                    answer = self.analyzer.captioner.answer_question(str(image_path), query)
                    response += f"**Your Question:** {query}\n**Answer:** {answer}\n\n"
                else:
                    # Use agent for complex queries
                    result = self.agent.run(query, str(image_path))
                    if result["success"]:
                        response += f"**Agent Response:**\n{result['response']}\n\n"
                    else:
                        response += f"**Error:** {result.get('error', 'Unknown error')}\n\n"

            # Classification with common categories
            common_labels = [
                "a photo of a person",
                "a photo of an animal",
                "a landscape or nature scene",
                "a cityscape or urban scene",
                "food or dining",
                "a vehicle or transportation",
                "indoor scene",
                "outdoor scene",
                "an object or product",
                "art or creative work"
            ]

            best_match, score, all_scores = self.analyzer.embedder.find_best_match(
                str(image_path), common_labels
            )

            classification = f"**Most likely category:** {best_match} ({score:.1%} confidence)\n\n"
            classification += "**All categories:**\n"
            sorted_results = sorted(zip(common_labels, all_scores), key=lambda x: x[1], reverse=True)
            for label, s in sorted_results:
                bar = "█" * int(s * 20)
                classification += f"{label:.<40} {bar} {s:.1%}\n"

            return response.strip(), classification

        except Exception as e:
            return f"Error: {str(e)}", ""

    def quick_caption(self, image):
        """Quick caption generation"""
        if image is None:
            return "Please upload an image first."

        try:
            self.initialize_models()
            image_path = self.temp_dir / "current_image.jpg"
            image.save(image_path)
            caption = self.analyzer.captioner.generate_caption(str(image_path))
            return f"📸 {caption}"
        except Exception as e:
            return f"Error: {str(e)}"

    def build_interface(self):
        """Build Gradio interface"""

        with gr.Blocks(title=Config.APP_TITLE, theme=gr.themes.Soft()) as demo:
            gr.Markdown(f"# {Config.APP_TITLE}")
            gr.Markdown(Config.APP_DESCRIPTION)

            with gr.Tab("🎯 Main Analysis"):
                with gr.Row():
                    with gr.Column(scale=1):
                        image_input = gr.Image(type="pil", label="Upload Image")
                        query_input = gr.Textbox(
                            label="Your Question (optional)",
                            placeholder="e.g., What's happening in this image? What colors are present?",
                            lines=2
                        )
                        analysis_type = gr.Radio(
                            choices=["caption", "detailed", "full"],
                            value="full",
                            label="Analysis Depth"
                        )
                        analyze_btn = gr.Button("🔍 Analyze", variant="primary")

                    with gr.Column(scale=1):
                        result_output = gr.Markdown(label="Analysis Results")
                        classification_output = gr.Textbox(
                            label="Classification Results",
                            lines=15,
                            max_lines=20
                        )

                analyze_btn.click(
                    fn=self.process_image_query,
                    inputs=[image_input, query_input, analysis_type],
                    outputs=[result_output, classification_output]
                )

            with gr.Tab("⚡ Quick Caption"):
                with gr.Row():
                    with gr.Column():
                        quick_image = gr.Image(type="pil", label="Upload Image")
                        quick_btn = gr.Button("Generate Caption", variant="primary")
                    with gr.Column():
                        quick_output = gr.Textbox(label="Caption", lines=3)

                quick_btn.click(
                    fn=self.quick_caption,
                    inputs=[quick_image],
                    outputs=[quick_output]
                )

            with gr.Tab("📋 Examples"):
                gr.Markdown("""
                ## Try these example queries:

                **Basic Questions:**
                - What's in this image?
                - Describe the scene
                - What colors are dominant?
                - Is this indoors or outdoors?

                **Specific Questions:**
                - How many people are in the image?
                - What is the main object?
                - What's the weather like?
                - What time of day is it?

                **Complex Analysis:**
                - Describe the mood of this image
                - What activity is taking place?
                - What's unusual about this image?
                """)

            with gr.Tab("ℹ️ About"):
                gr.Markdown("""
                ## Multi-Modal AI Agent

                This application demonstrates multi-modal reasoning combining:

                ### 🧠 Models Used:
                - **CLIP** (OpenAI): Visual-text matching and zero-shot classification
                - **BLIP** (Salesforce): Image captioning and visual question answering
                - **LangChain**: Agentic reasoning and tool orchestration

                ### 🛠️ Capabilities:
                1. **Image Captioning**: Generate natural language descriptions
                2. **Visual Q&A**: Answer specific questions about images
                3. **Classification**: Zero-shot categorization into custom labels
                4. **Multi-tool Agent**: Complex reasoning using multiple tools

                ### 🚀 Technical Stack:
                - PyTorch + Transformers
                - LangChain Agents
                - Gradio UI
                - CLIP + BLIP models

                ---
                Built with ❤️ using cutting-edge multi-modal AI
                """)

        return demo

    def launch(self, share=False, server_port=7860):
        """Launch the Gradio app"""
        print("\n" + "="*60)
        print("Initializing Multi-Modal AI Agent...")
        print("="*60 + "\n")

        demo = self.build_interface()

        print("\n" + "="*60)
        print("🚀 Launching Gradio Interface...")
        print("="*60 + "\n")

        demo.launch(
            share=share,
            server_port=server_port,
            server_name="0.0.0.0"
        )


def main():
    """Main entry point"""
    app = MultiModalApp()
    app.launch(share=False, server_port=7860)


if __name__ == "__main__":
    main()
