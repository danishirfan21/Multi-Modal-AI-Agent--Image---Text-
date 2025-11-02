"""
Test script for Multi-Modal AI Agent
Run this to verify all components are working
"""
import sys
from pathlib import Path


def test_imports():
    """Test that all modules can be imported"""
    print("Testing imports...")

    try:
        from config import Config
        print("✓ Config module")

        from models.clip_embedder import CLIPEmbedder
        print("✓ CLIP Embedder")

        from models.image_captioner import ImageCaptioner, MultiModalAnalyzer
        print("✓ Image Captioner & Analyzer")

        from agent.tools import get_all_tools
        print("✓ LangChain Tools")

        from agent.multimodal_agent import MultiModalAgent
        print("✓ Multi-Modal Agent")

        print("\n✅ All imports successful!\n")
        return True

    except Exception as e:
        print(f"\n❌ Import failed: {str(e)}\n")
        return False


def test_config():
    """Test configuration"""
    print("Testing configuration...")

    try:
        from config import Config

        print(f"  - USE_LOCAL_MODELS: {Config.USE_LOCAL_MODELS}")
        print(f"  - CLIP_MODEL: {Config.CLIP_MODEL}")
        print(f"  - BLIP_MODEL: {Config.BLIP_MODEL}")
        print(f"  - DEVICE: {Config.DEVICE}")

        if not Config.USE_LOCAL_MODELS and not Config.OPENAI_API_KEY:
            print("\n⚠️  Warning: No OpenAI API key set. Agent will use local-only mode.")
            print("   Set OPENAI_API_KEY in .env for full agent capabilities.\n")
        else:
            print("\n✅ Configuration valid!\n")

        return True

    except Exception as e:
        print(f"\n❌ Configuration test failed: {str(e)}\n")
        return False


def test_tools():
    """Test that tools can be initialized"""
    print("Testing tools initialization...")

    try:
        from agent.tools import get_all_tools

        tools = get_all_tools()
        print(f"\n  Found {len(tools)} tools:")

        for tool in tools:
            print(f"    ✓ {tool.name}")

        print("\n✅ All tools initialized!\n")
        return True

    except Exception as e:
        print(f"\n❌ Tools test failed: {str(e)}\n")
        return False


def test_model_loading():
    """Test loading AI models (may take a while on first run)"""
    print("Testing model loading (this may take a few minutes on first run)...")
    print("Models will be downloaded from HuggingFace if not cached.\n")

    try:
        # Test CLIP
        print("Loading CLIP model...")
        from models.clip_embedder import CLIPEmbedder
        clip = CLIPEmbedder()
        print("✓ CLIP loaded successfully")

        # Test text encoding
        test_text = "a photo of a cat"
        embedding = clip.encode_text(test_text)
        print(f"✓ Text encoding works (embedding shape: {embedding.shape})")

        # Test BLIP
        print("\nLoading BLIP model...")
        from models.image_captioner import ImageCaptioner
        captioner = ImageCaptioner()
        print("✓ BLIP loaded successfully")

        print("\n✅ All models loaded successfully!\n")
        return True

    except Exception as e:
        print(f"\n❌ Model loading failed: {str(e)}")
        print("\nThis might be due to:")
        print("  - Missing dependencies (run: pip install -r requirements.txt)")
        print("  - Insufficient memory (models require ~4GB RAM)")
        print("  - Network issues (models need to be downloaded from HuggingFace)")
        print("\n")
        return False


def test_agent():
    """Test agent initialization"""
    print("Testing agent initialization...")

    try:
        from agent.multimodal_agent import MultiModalAgent

        agent = MultiModalAgent()
        print("✓ Agent initialized")

        tools = agent.get_available_tools()
        print(f"✓ Agent has {len(tools)} tools available")

        print("\n✅ Agent ready!\n")
        return True

    except Exception as e:
        print(f"\n❌ Agent test failed: {str(e)}\n")
        return False


def run_all_tests():
    """Run all tests"""
    print("\n" + "="*60)
    print("Multi-Modal AI Agent - Test Suite")
    print("="*60 + "\n")

    tests = [
        ("Imports", test_imports),
        ("Configuration", test_config),
        ("Tools", test_tools),
        ("Model Loading", test_model_loading),
        ("Agent", test_agent),
    ]

    results = {}

    for name, test_func in tests:
        print(f"\n{'='*60}")
        print(f"Test: {name}")
        print('='*60 + "\n")

        results[name] = test_func()

    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60 + "\n")

    for name, passed in results.items():
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{name:.<40} {status}")

    all_passed = all(results.values())

    print("\n" + "="*60)
    if all_passed:
        print("🎉 All tests passed! Your agent is ready to use.")
        print("\nRun the app with:")
        print("  python app_gradio.py    # For Gradio interface")
        print("  streamlit run app_streamlit.py  # For Streamlit interface")
    else:
        print("⚠️  Some tests failed. Please fix the issues above.")
    print("="*60 + "\n")

    return all_passed


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
