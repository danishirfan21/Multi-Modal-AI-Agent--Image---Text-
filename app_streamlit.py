"""
Streamlit Web Interface for Multi-Modal AI Agent
Alternative to Gradio with different UI capabilities
"""
import streamlit as st
from PIL import Image
import os
from pathlib import Path
from agent.multimodal_agent import MultiModalAgent
from models.image_captioner import MultiModalAnalyzer
from config import Config


# Page config
st.set_page_config(
    page_title=Config.APP_TITLE,
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)


@st.cache_resource
def load_models():
    """Load models with caching"""
    analyzer = MultiModalAnalyzer()
    agent = MultiModalAgent()
    return analyzer, agent


def main():
    """Main Streamlit app"""

    # Header
    st.title("🤖 Multi-Modal AI Agent")
    st.markdown(Config.APP_DESCRIPTION)

    # Sidebar
    with st.sidebar:
        st.header("⚙️ Settings")
        analysis_depth = st.selectbox(
            "Analysis Depth",
            ["Quick Caption", "Detailed Analysis", "Full Analysis"],
            index=2
        )

        show_classification = st.checkbox("Show Classification", value=True)
        show_tools = st.checkbox("Show Available Tools", value=False)

        st.markdown("---")
        st.markdown("""
        ### About
        Multi-modal AI agent using:
        - 🖼️ CLIP (visual-text matching)
        - 📝 BLIP (image captioning)
        - 🔗 LangChain (agent reasoning)
        """)

    # Main content
    col1, col2 = st.columns([1, 1])

    with col1:
        st.header("📤 Upload Image")
        uploaded_file = st.file_uploader(
            "Choose an image...",
            type=["jpg", "jpeg", "png", "bmp"],
            help="Upload an image to analyze"
        )

        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Image", use_column_width=True)

            st.markdown("---")
            query = st.text_area(
                "Ask a question about the image (optional):",
                placeholder="e.g., What's happening in this image?",
                height=100
            )

            analyze_button = st.button("🔍 Analyze Image", type="primary", use_container_width=True)

    with col2:
        st.header("📊 Results")

        if uploaded_file is not None and analyze_button:
            with st.spinner("Loading models..."):
                analyzer, agent = load_models()

            # Save temp image
            temp_dir = Path("temp_uploads")
            temp_dir.mkdir(exist_ok=True)
            image_path = temp_dir / "current_image.jpg"
            image.save(image_path)

            try:
                # Caption
                if analysis_depth in ["Quick Caption", "Detailed Analysis", "Full Analysis"]:
                    with st.spinner("Generating caption..."):
                        caption = analyzer.captioner.generate_caption(str(image_path))
                        st.success("**Caption:**")
                        st.write(f"📸 {caption}")

                # Detailed analysis
                if analysis_depth in ["Detailed Analysis", "Full Analysis"]:
                    with st.spinner("Performing detailed analysis..."):
                        with st.expander("📋 Detailed Descriptions", expanded=True):
                            detailed = analyzer.captioner.generate_detailed_description(str(image_path))
                            for question, answer in detailed["descriptions"].items():
                                st.markdown(f"**{question}**")
                                st.write(f"→ {answer}")

                # Answer question
                if query and query.strip():
                    with st.spinner("Answering your question..."):
                        st.info("**Your Question:**")
                        st.write(query)

                        if "?" in query:
                            answer = analyzer.captioner.answer_question(str(image_path), query)
                            st.success("**Answer:**")
                            st.write(answer)
                        else:
                            result = agent.run(query, str(image_path))
                            if result["success"]:
                                st.success("**Agent Response:**")
                                st.write(result['response'])
                            else:
                                st.error(f"Error: {result.get('error', 'Unknown error')}")

                # Classification
                if show_classification:
                    with st.spinner("Classifying image..."):
                        st.markdown("---")
                        st.subheader("🏷️ Image Classification")

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

                        best_match, score, all_scores = analyzer.embedder.find_best_match(
                            str(image_path), common_labels
                        )

                        st.metric("Most Likely Category", best_match, f"{score:.1%} confidence")

                        # Show bar chart
                        import pandas as pd
                        df = pd.DataFrame({
                            'Category': common_labels,
                            'Confidence': all_scores
                        }).sort_values('Confidence', ascending=False)

                        st.bar_chart(df.set_index('Category'))

            except Exception as e:
                st.error(f"Error: {str(e)}")

        elif uploaded_file is None:
            st.info("👆 Upload an image to get started!")

    # Show tools section
    if show_tools:
        st.markdown("---")
        st.header("🛠️ Available Tools")

        with st.expander("View All Tools", expanded=True):
            analyzer, agent = load_models()
            tools = agent.get_available_tools()

            for tool in tools:
                st.markdown(f"**{tool['name']}**")
                st.write(tool['description'])
                st.markdown("---")


if __name__ == "__main__":
    main()
