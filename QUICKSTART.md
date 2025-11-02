# ⚡ Quick Start Guide

Get your Multi-Modal AI Agent running in 5 minutes!

## 🚀 Fast Setup

### Step 1: Install Dependencies (2 min)

```bash
# Create virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install packages
pip install -r requirements.txt
```

### Step 2: Configure (30 sec)

```bash
# Copy environment file
cp .env.example .env

# Optional: Add OpenAI key for advanced features
# Edit .env and add: OPENAI_API_KEY=your-key-here
```

### Step 3: Test (1 min)

```bash
python test_agent.py
```

Expected output: All tests pass ✅

### Step 4: Launch (30 sec)

```bash
python app_gradio.py
```

Open browser at **http://localhost:7860**

## 🎯 First Steps

1. **Upload an image** - Click the upload area
2. **Ask a question** - Try "What's in this image?"
3. **Click Analyze** - See the magic happen!

## 📝 Example Queries

Start with these:

### Basic
- "What's in this image?"
- "Describe this scene"
- "What colors are present?"

### Specific
- "How many people are visible?"
- "Is this indoors or outdoors?"
- "What's the main object?"

### Advanced
- "Describe the mood and atmosphere"
- "What activity is happening here?"
- "What makes this image interesting?"

## 🎨 Interface Overview

### Gradio (Default)
- **Main Analysis**: Full multi-modal analysis
- **Quick Caption**: Fast image description
- **Examples**: Sample queries and use cases
- **About**: Technical information

### Streamlit (Alternative)
```bash
streamlit run app_streamlit.py
```
- Interactive sidebar
- Real-time updates
- Data visualizations

## 🔧 Common Commands

```bash
# Run tests
python test_agent.py

# Run examples
python example_usage.py

# Launch Gradio (default)
python run.py

# Launch Streamlit
python run.py --ui streamlit

# Custom port
python run.py --port 8080

# With sharing link
python run.py --share
```

## 💡 Tips

### First Run
- Models will download (~1.5GB)
- Takes 2-5 minutes depending on connection
- Subsequent runs are instant

### Performance
- **CPU Mode** (default): 1-2 seconds per image
- **GPU Mode**: 100-200ms per image
  - Enable: Set `USE_GPU=true` in `.env`

### Memory
- Requires ~4GB RAM
- Close other apps if low on memory
- Use smaller models if needed

## 🐛 Troubleshooting

### Models won't load
```bash
# Check internet connection
# Verify disk space (need 2GB free)
pip install --upgrade transformers torch
```

### Out of memory
```bash
# In .env file:
USE_GPU=false
# Use smaller models:
CLIP_MODEL=openai/clip-vit-base-patch32
```

### Port already in use
```bash
python run.py --port 8080
```

### Import errors
```bash
pip install --upgrade -r requirements.txt
```

## 📚 Next Steps

After getting it running:

1. **Read README.md** - Full documentation
2. **Try example_usage.py** - Code examples
3. **Check SETUP_GUIDE.md** - Detailed setup
4. **Read PROJECT_OVERVIEW.md** - Architecture

## 🎯 Quick Architecture

```
You → Web UI → Agent → Tools → Models → Results
                 ↓        ↓       ↓
            LangChain  Caption  CLIP
                      VQA      BLIP
                      Classify
```

## 🌟 Key Features

✅ Image captioning (describe images)
✅ Visual Q&A (answer questions)
✅ Zero-shot classification (categorize)
✅ Multi-modal reasoning (combine info)
✅ Web interface (easy to use)

## 📊 What You Can Do

- **Content Creation**: Auto-generate image descriptions
- **Accessibility**: Alt text for images
- **E-commerce**: Product categorization
- **Research**: Image analysis
- **Education**: Visual learning tools

## 🎉 You're Ready!

Your multi-modal AI agent is now running.

Try uploading different types of images:
- Photos
- Screenshots
- Artwork
- Diagrams
- Product images

Ask various questions:
- Descriptive ("What's this?")
- Specific ("What color?")
- Analytical ("What's the mood?")

Have fun exploring multi-modal AI! 🚀

---

**Questions?** Check the full README.md or open an issue on GitHub.
