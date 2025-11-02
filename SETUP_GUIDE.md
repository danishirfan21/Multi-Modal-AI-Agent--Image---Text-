# 🛠️ Setup Guide - Multi-Modal AI Agent

Complete step-by-step setup guide for all platforms.

## 📋 Table of Contents

1. [System Requirements](#system-requirements)
2. [Windows Setup](#windows-setup)
3. [macOS Setup](#macos-setup)
4. [Linux Setup](#linux-setup)
5. [Docker Setup](#docker-setup)
6. [Configuration](#configuration)
7. [Verification](#verification)

---

## System Requirements

### Minimum Requirements
- **OS**: Windows 10+, macOS 10.15+, or Linux (Ubuntu 20.04+)
- **Python**: 3.8 or higher
- **RAM**: 4GB minimum, 8GB recommended
- **Disk Space**: 5GB free (for models and dependencies)
- **Internet**: Required for initial model download

### Optional (for better performance)
- **GPU**: NVIDIA GPU with CUDA support (4GB+ VRAM)
- **CUDA**: 11.8 or higher
- **OpenAI API Key**: For advanced agent reasoning

---

## Windows Setup

### Step 1: Install Python

1. Download Python from [python.org](https://www.python.org/downloads/)
2. **Important**: Check "Add Python to PATH" during installation
3. Verify installation:
```cmd
python --version
pip --version
```

### Step 2: Set Up Project

1. Open Command Prompt or PowerShell
2. Navigate to project directory:
```cmd
cd "D:\Multi-Modal AI Agent (Image + Text)"
```

3. Create virtual environment:
```cmd
python -m venv venv
venv\Scripts\activate
```

4. Install dependencies:
```cmd
pip install --upgrade pip
pip install -r requirements.txt
```

### Step 3: Configure

1. Copy environment template:
```cmd
copy .env.example .env
```

2. Edit `.env` (optional):
```cmd
notepad .env
```

### Step 4: Run

```cmd
python test_agent.py
python app_gradio.py
```

---

## macOS Setup

### Step 1: Install Python

Python 3 is usually pre-installed on macOS. Verify:
```bash
python3 --version
```

If not installed or version < 3.8:
```bash
# Install Homebrew if needed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python
brew install python@3.10
```

### Step 2: Set Up Project

```bash
cd "/path/to/Multi-Modal AI Agent (Image + Text)"

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

### Step 3: Configure

```bash
cp .env.example .env
nano .env  # or use your preferred editor
```

### Step 4: Run

```bash
python test_agent.py
python app_gradio.py
```

---

## Linux Setup

### Step 1: Install Python

Ubuntu/Debian:
```bash
sudo apt update
sudo apt install python3.10 python3.10-venv python3-pip
```

Fedora/RHEL:
```bash
sudo dnf install python3.10 python3-pip
```

### Step 2: Set Up Project

```bash
cd "/path/to/Multi-Modal AI Agent (Image + Text)"

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

### Step 3: Configure

```bash
cp .env.example .env
nano .env
```

### Step 4: Run

```bash
python test_agent.py
python app_gradio.py
```

---

## Docker Setup

### Dockerfile

Create `Dockerfile`:
```dockerfile
FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Expose ports
EXPOSE 7860 8501

# Run app
CMD ["python", "app_gradio.py"]
```

### Build and Run

```bash
# Build image
docker build -t multimodal-agent .

# Run container (Gradio)
docker run -p 7860:7860 multimodal-agent

# Run container (Streamlit)
docker run -p 8501:8501 multimodal-agent streamlit run app_streamlit.py

# With GPU support
docker run --gpus all -p 7860:7860 multimodal-agent
```

---

## Configuration

### Basic Configuration

Edit `.env` file:

```bash
# Required: Set to false if using OpenAI
USE_LOCAL_MODELS=true

# Optional: OpenAI API key for advanced reasoning
OPENAI_API_KEY=sk-...

# Model selection
CLIP_MODEL=openai/clip-vit-large-patch14
BLIP_MODEL=Salesforce/blip-image-captioning-large

# Agent settings
MAX_ITERATIONS=5
VERBOSE=true

# GPU support (if available)
USE_GPU=false
```

### GPU Configuration

If you have NVIDIA GPU:

1. Install CUDA Toolkit from [NVIDIA](https://developer.nvidia.com/cuda-downloads)

2. Install PyTorch with CUDA:
```bash
# CUDA 11.8
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118

# CUDA 12.1
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu121
```

3. Update `.env`:
```bash
USE_GPU=true
```

4. Verify:
```python
import torch
print(torch.cuda.is_available())  # Should print True
```

### OpenAI Configuration

To use GPT-4 for advanced reasoning:

1. Get API key from [OpenAI Platform](https://platform.openai.com/api-keys)

2. Update `.env`:
```bash
OPENAI_API_KEY=sk-your-key-here
USE_LOCAL_MODELS=false
```

---

## Verification

### Run Test Suite

```bash
python test_agent.py
```

Expected output:
```
============================================================
Test: Imports
============================================================
✓ Config module
✓ CLIP Embedder
✓ Image Captioner & Analyzer
✓ LangChain Tools
✓ Multi-Modal Agent
✅ All imports successful!

[... more tests ...]

============================================================
TEST SUMMARY
============================================================
Imports......................................... ✅ PASSED
Configuration................................... ✅ PASSED
Tools........................................... ✅ PASSED
Model Loading................................... ✅ PASSED
Agent........................................... ✅ PASSED

🎉 All tests passed! Your agent is ready to use.
```

### Manual Verification

Test individual components:

```python
# Test CLIP
python -c "from models.clip_embedder import CLIPEmbedder; e = CLIPEmbedder(); print('CLIP OK')"

# Test BLIP
python -c "from models.image_captioner import ImageCaptioner; c = ImageCaptioner(); print('BLIP OK')"

# Test Agent
python -c "from agent.multimodal_agent import MultiModalAgent; a = MultiModalAgent(); print('Agent OK')"
```

---

## Common Issues

### Issue: "ModuleNotFoundError"

**Solution**:
```bash
pip install --upgrade -r requirements.txt
```

### Issue: "CUDA out of memory"

**Solution**:
```bash
# In .env
USE_GPU=false
```

### Issue: "Port already in use"

**Solution**:
```bash
python run.py --port 8080
```

### Issue: Models won't download

**Solution**:
1. Check internet connection
2. Verify HuggingFace is accessible
3. Set HF_HOME to custom directory:
```bash
export HF_HOME=/path/to/large/storage
```

### Issue: Slow first run

**Expected**: First run downloads ~1.5GB of models. Subsequent runs are fast.

---

## Performance Optimization

### For CPU-only systems

1. Use smaller models:
```bash
CLIP_MODEL=openai/clip-vit-base-patch32
BLIP_MODEL=Salesforce/blip-image-captioning-base
```

2. Reduce batch size in code if needed

### For GPU systems

1. Enable GPU in `.env`:
```bash
USE_GPU=true
```

2. Monitor GPU usage:
```bash
nvidia-smi
```

### For low-memory systems

1. Close other applications
2. Use swap space (Linux):
```bash
sudo fallocate -l 4G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

---

## Next Steps

After successful setup:

1. **Launch the app**:
   ```bash
   python app_gradio.py
   ```

2. **Try example queries** (see README.md)

3. **Customize tools** (see agent/tools.py)

4. **Deploy to production** (see deployment guide)

---

## Getting Help

- **GitHub Issues**: Report bugs and request features
- **Documentation**: See README.md for usage examples
- **Community**: Join discussions on GitHub

---

**Setup complete!** You're ready to use the Multi-Modal AI Agent. 🎉
