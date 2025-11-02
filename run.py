#!/usr/bin/env python3
"""
Quick launcher for Multi-Modal AI Agent
"""
import sys
import argparse


def main():
    parser = argparse.ArgumentParser(description="Launch Multi-Modal AI Agent")
    parser.add_argument(
        "--ui",
        choices=["gradio", "streamlit"],
        default="gradio",
        help="UI framework to use (default: gradio)"
    )
    parser.add_argument(
        "--share",
        action="store_true",
        help="Create public sharing link (Gradio only)"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=7860,
        help="Port number (default: 7860)"
    )
    parser.add_argument(
        "--test",
        action="store_true",
        help="Run tests instead of launching app"
    )

    args = parser.parse_args()

    if args.test:
        print("Running tests...")
        from test_agent import run_all_tests
        success = run_all_tests()
        sys.exit(0 if success else 1)

    if args.ui == "gradio":
        print("Launching Gradio interface...")
        from app_gradio import main as gradio_main
        gradio_main()

    elif args.ui == "streamlit":
        print("Launching Streamlit interface...")
        import subprocess
        cmd = ["streamlit", "run", "app_streamlit.py", "--server.port", str(args.port)]
        subprocess.run(cmd)


if __name__ == "__main__":
    main()
