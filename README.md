# 🤖 Multi-Modal AI Agent

> A powerful multi-modal AI system that combines visual and textual understanding using CLIP, BLIP, and LangChain agents.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![PyTorch](https://img.shields.io/badge/PyTorch-2.0%2B-red)
![License](https://img.shields.io/badge/License-MIT-green)

## 🌟 Features

- **🖼️ Image Understanding**: Analyze images using state-of-the-art CLIP and BLIP models
- **💬 Visual Question Answering**: Ask questions about images in natural language
- **🏷️ Zero-Shot Classification**: Classify images without training data
- **🔗 Agentic Workflow**: LangChain-powered agent with multiple tools
- **🎨 Beautiful UI**: Choose between Gradio or Streamlit interfaces
- **⚡ Fast Inference**: Optimized for quick responses
- **🔌 Extensible**: Easy to add new tools and capabilities

## 🏗️ Architecture

```
┌─────────────────────────────────────────┐
│         User Interface Layer            │
│    (Gradio / Streamlit Web App)        │
└──────────────┬──────────────────────────┘
               │
┌──────────────▼──────────────────────────┐
│      Multi-Modal Agent Layer            │
│    (LangChain Agent Orchestration)      │
└──────────────┬──────────────────────────┘
               │
       ┌───────┴───────┐
       │               │
┌──────▼─────┐  ┌─────▼──────┐
│   Tools    │  │   Models   │
├────────────┤  ├────────────┤
│ • Caption  │  │ • CLIP     │
│ • VQA      │  │ • BLIP     │
│ • Classify │  │ • LLM      │
│ • Search   │  │            │
│ • Calc     │  │            │
└────────────┘  └────────────┘
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- 4GB+ RAM (for loading models)
- Optional: CUDA-capable GPU for faster inference
- Optional: OpenAI API key for advanced reasoning

### Installation

1. **Clone the repository**
```bash
cd "Multi-Modal AI Agent (Image + Text)"
```

2. **Create virtual environment** (recommended)
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**
```bash
# Copy example env file
cp .env.example .env

# Edit .env and add your OpenAI API key (optional)
# OPENAI_API_KEY=your_key_here
```

5. **Run tests** (optional but recommended)
```bash
python test_agent.py
```

### Launch the App

**Option 1: Gradio (Recommended)**
```bash
python app_gradio.py
```

**Option 2: Streamlit**
```bash
streamlit run app_streamlit.py
```

**Option 3: Quick launcher**
```bash
# Gradio
python run.py --ui gradio

# Streamlit
python run.py --ui streamlit

# With public sharing link (Gradio only)
python run.py --ui gradio --share

# Custom port
python run.py --port 8080
```

The app will open in your browser at `http://localhost:7860` (Gradio) or `http://localhost:8501` (Streamlit).

## 📖 Usage

### Basic Usage

1. **Upload an image** using the file uploader
2. **Ask a question** (optional) like:
   - "What's happening in this image?"
   - "What colors are present?"
   - "How many people are in the photo?"
3. **Click Analyze** to get results

### Advanced Features

#### Image Captioning
```python
from models.image_captioner import ImageCaptioner

captioner = ImageCaptioner()
caption = captioner.generate_caption("path/to/image.jpg")
print(caption)
```

#### Visual Question Answering
```python
from models.image_captioner import ImageCaptioner

captioner = ImageCaptioner()
answer = captioner.answer_question(
    "path/to/image.jpg",
    "What color is the sky?"
)
print(answer)
```

#### Image Classification (CLIP)
```python
from models.clip_embedder import CLIPEmbedder

embedder = CLIPEmbedder()
labels = ["a photo of a cat", "a photo of a dog", "a bird"]
best_match, score, all_scores = embedder.find_best_match(
    "path/to/image.jpg",
    labels
)
print(f"Best match: {best_match} ({score:.2%})")
```

#### Using the Agent
```python
from agent.multimodal_agent import MultiModalAgent

agent = MultiModalAgent()
result = agent.run(
    query="What's in this image and is it indoors or outdoors?",
    image_path="path/to/image.jpg"
)
print(result["response"])
```

## 🛠️ Project Structure

```
Multi-Modal AI Agent/
├── models/
│   ├── __init__.py
│   ├── clip_embedder.py      # CLIP-based visual-text matching
│   └── image_captioner.py    # BLIP-based captioning & VQA
├── agent/
│   ├── __init__.py
│   ├── tools.py              # LangChain tools
│   └── multimodal_agent.py   # Main agent logic
├── app_gradio.py             # Gradio web interface
├── app_streamlit.py          # Streamlit web interface
├── config.py                 # Configuration management
├── test_agent.py             # Test suite
├── run.py                    # Quick launcher
├── requirements.txt          # Dependencies
├── .env.example              # Environment template
├── .gitignore
└── README.md
```

## 🧰 Available Tools

The agent has access to these tools:

| Tool | Description |
|------|-------------|
| `image_captioner` | Generates natural language descriptions of images |
| `image_qa` | Answers specific questions about image content |
| `image_classifier` | Classifies images into provided categories (zero-shot) |
| `calculator` | Performs mathematical calculations |
| `web_search` | Searches for information online (mock/extendable) |

## 🎯 Example Queries

### Basic Questions
- "What's in this image?"
- "Describe the scene"
- "What objects can you see?"

### Specific Questions
- "What color is the car?"
- "How many people are visible?"
- "Is this indoors or outdoors?"
- "What's the weather like?"

### Complex Analysis
- "Describe the mood and atmosphere of this scene"
- "What activity is taking place and what objects are involved?"
- "Compare the foreground and background"

## 🔧 Configuration

Edit `.env` file or `config.py` to customize:

```python
# Use local models only (no API needed)
USE_LOCAL_MODELS=true

# Model selections
CLIP_MODEL=openai/clip-vit-large-patch14
BLIP_MODEL=Salesforce/blip-image-captioning-large

# OpenAI API (optional, for advanced reasoning)
OPENAI_API_KEY=your_key_here

# Agent settings
MAX_ITERATIONS=5
VERBOSE=true
```

## 📊 Model Information

### CLIP (Contrastive Language-Image Pre-training)
- **Publisher**: OpenAI
- **Purpose**: Visual-text matching, zero-shot classification
- **Size**: ~600MB
- **Use case**: Finding similarities between images and text

### BLIP (Bootstrapping Language-Image Pre-training)
- **Publisher**: Salesforce
- **Purpose**: Image captioning, visual question answering
- **Size**: ~990MB
- **Use case**: Generating descriptions and answering questions

## 🚀 Performance Tips

1. **First run**: Models will download (~1.5GB total) - this may take time
2. **GPU acceleration**: Set `USE_GPU=true` in `.env` if you have CUDA
3. **Memory**: Close other applications if you encounter memory issues
4. **Batch processing**: Process multiple images in a loop for efficiency

## 🔌 Extending the Agent

### Adding a New Tool

```python
# In agent/tools.py

from langchain.tools import BaseTool
from pydantic import BaseModel, Field

class MyToolInput(BaseModel):
    param: str = Field(description="Parameter description")

class MyCustomTool(BaseTool):
    name: str = "my_tool"
    description: str = "What this tool does"
    args_schema: Type[BaseModel] = MyToolInput

    def _run(self, param: str) -> str:
        # Your logic here
        return f"Result: {param}"

# Add to get_all_tools()
def get_all_tools():
    return [
        # ... existing tools ...
        MyCustomTool(),
    ]
```

### Using a Different LLM

```python
# In agent/multimodal_agent.py

def _initialize_llm(self):
    # Use local model
    from langchain_community.llms import HuggingFacePipeline
    return HuggingFacePipeline.from_model_id(
        model_id="facebook/opt-1.3b",
        task="text-generation"
    )
```

## 🐛 Troubleshooting

### Models won't download
- Check your internet connection
- Verify you have ~2GB free disk space
- Try manually downloading from HuggingFace

### Out of memory errors
- Reduce batch size
- Close other applications
- Use CPU instead of GPU
- Try smaller model variants

### Import errors
```bash
pip install --upgrade -r requirements.txt
```

### Port already in use
```bash
python run.py --port 8080
```

## 📝 Example Output

```
Image Analysis:
Caption: a person standing on a beach during sunset

Detailed Analysis:
- What is in this image?
  → a person standing on a sandy beach with ocean waves
- What are the main objects?
  → person, beach, ocean, sunset, sky
- What is happening?
  → a person is enjoying a sunset view at the beach

Classification: outdoor scene (87.3% confidence)
```

## 🤝 Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Add tests for new features
4. Submit a pull request

## 📄 License

MIT License - feel free to use this project for any purpose.

## 🙏 Acknowledgments

- **OpenAI** for CLIP
- **Salesforce** for BLIP
- **LangChain** for the agent framework
- **HuggingFace** for model hosting and transformers library
- **Gradio** and **Streamlit** for UI frameworks

## 📧 Contact

For questions or feedback, please open an issue on GitHub.

---

## 🎓 Learn More

- [CLIP Paper](https://arxiv.org/abs/2103.00020)
- [BLIP Paper](https://arxiv.org/abs/2201.12086)
- [LangChain Documentation](https://python.langchain.com/)
- [Transformers Documentation](https://huggingface.co/docs/transformers)

---

**Built with ❤️ using cutting-edge multi-modal AI**

⭐ Star this repo if you find it useful!
