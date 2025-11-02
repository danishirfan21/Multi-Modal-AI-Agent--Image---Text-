"""
Example usage scripts for Multi-Modal AI Agent
Demonstrates various capabilities
"""
from pathlib import Path


def example_1_image_caption():
    """Example: Generate image caption"""
    print("\n" + "="*60)
    print("Example 1: Image Captioning")
    print("="*60 + "\n")

    from models.image_captioner import ImageCaptioner

    captioner = ImageCaptioner()

    # Note: Replace with actual image path
    image_path = "path/to/your/image.jpg"

    if Path(image_path).exists():
        caption = captioner.generate_caption(image_path)
        print(f"Image: {image_path}")
        print(f"Caption: {caption}")
    else:
        print(f"Please provide a valid image path.")
        print("Example caption: 'a person walking on a beach during sunset'")


def example_2_visual_qa():
    """Example: Visual Question Answering"""
    print("\n" + "="*60)
    print("Example 2: Visual Question Answering")
    print("="*60 + "\n")

    from models.image_captioner import ImageCaptioner

    captioner = ImageCaptioner()
    image_path = "path/to/your/image.jpg"

    questions = [
        "What is in this image?",
        "What colors are dominant?",
        "Is this indoors or outdoors?",
    ]

    if Path(image_path).exists():
        print(f"Image: {image_path}\n")
        for question in questions:
            answer = captioner.answer_question(image_path, question)
            print(f"Q: {question}")
            print(f"A: {answer}\n")
    else:
        print("Please provide a valid image path.")
        print("\nExample Q&A:")
        print("Q: What is in this image?")
        print("A: a person standing on a beach with ocean waves\n")


def example_3_classification():
    """Example: Zero-shot image classification"""
    print("\n" + "="*60)
    print("Example 3: Zero-Shot Classification (CLIP)")
    print("="*60 + "\n")

    from models.clip_embedder import CLIPEmbedder

    embedder = CLIPEmbedder()
    image_path = "path/to/your/image.jpg"

    # Define possible categories
    categories = [
        "a photo of a cat",
        "a photo of a dog",
        "a photo of a bird",
        "a photo of nature",
        "a photo of food",
        "a photo of a person",
    ]

    if Path(image_path).exists():
        print(f"Image: {image_path}")
        print(f"Categories: {', '.join(categories)}\n")

        best_match, confidence, all_scores = embedder.find_best_match(
            image_path, categories
        )

        print(f"Best match: {best_match}")
        print(f"Confidence: {confidence:.2%}\n")

        print("All scores:")
        for category, score in zip(categories, all_scores):
            bar = "█" * int(score * 20)
            print(f"  {category:.<30} {bar} {score:.1%}")
    else:
        print("Please provide a valid image path.")
        print("\nExample classification:")
        print("Best match: a photo of a cat")
        print("Confidence: 87.3%")


def example_4_multimodal_analysis():
    """Example: Comprehensive multi-modal analysis"""
    print("\n" + "="*60)
    print("Example 4: Comprehensive Multi-Modal Analysis")
    print("="*60 + "\n")

    from models.image_captioner import MultiModalAnalyzer

    analyzer = MultiModalAnalyzer()
    image_path = "path/to/your/image.jpg"

    if Path(image_path).exists():
        print(f"Analyzing: {image_path}\n")

        # Basic caption
        caption = analyzer.captioner.generate_caption(image_path)
        print(f"Caption: {caption}\n")

        # Detailed descriptions
        detailed = analyzer.captioner.generate_detailed_description(image_path)
        print("Detailed Analysis:")
        for question, answer in detailed["descriptions"].items():
            print(f"  Q: {question}")
            print(f"  A: {answer}\n")

        # Classification
        labels = [
            "outdoor scene",
            "indoor scene",
            "nature photography",
            "urban environment",
            "portrait"
        ]
        best, score, _ = analyzer.embedder.find_best_match(image_path, labels)
        print(f"Category: {best} ({score:.1%})")
    else:
        print("Please provide a valid image path for analysis.")


def example_5_agent():
    """Example: Using the full agent"""
    print("\n" + "="*60)
    print("Example 5: Multi-Modal Agent")
    print("="*60 + "\n")

    from agent.multimodal_agent import MultiModalAgent

    agent = MultiModalAgent()
    image_path = "path/to/your/image.jpg"

    queries = [
        "What's happening in this image?",
        "Describe the colors and atmosphere",
        "Is there any text visible?",
    ]

    if Path(image_path).exists():
        print(f"Image: {image_path}\n")

        for query in queries:
            print(f"Query: {query}")
            result = agent.run(query, image_path)

            if result["success"]:
                print(f"Response: {result['response']}\n")
            else:
                print(f"Error: {result['error']}\n")
    else:
        print("Please provide a valid image path.")
        print("\nThe agent can:")
        print("  - Analyze images using multiple tools")
        print("  - Answer complex questions")
        print("  - Reason about visual content")
        print("  - Combine multiple analysis methods")


def example_6_custom_classification():
    """Example: Custom zero-shot classification"""
    print("\n" + "="*60)
    print("Example 6: Custom Classification Categories")
    print("="*60 + "\n")

    from models.clip_embedder import CLIPEmbedder

    embedder = CLIPEmbedder()
    image_path = "path/to/your/image.jpg"

    # Define your own custom categories
    custom_categories = [
        "professional photography",
        "casual snapshot",
        "artistic composition",
        "product photo",
        "selfie",
        "screenshot",
    ]

    if Path(image_path).exists():
        print(f"Classifying: {image_path}")
        print(f"Into custom categories...\n")

        best, score, all_scores = embedder.find_best_match(
            image_path, custom_categories
        )

        print(f"Classification: {best} ({score:.1%})\n")
        print("Detailed scores:")
        sorted_results = sorted(
            zip(custom_categories, all_scores),
            key=lambda x: x[1],
            reverse=True
        )
        for cat, s in sorted_results:
            print(f"  {cat:.<30} {s:.1%}")
    else:
        print("Custom classification allows you to define any categories!")
        print("Examples: emotions, styles, quality levels, etc.")


def print_menu():
    """Print example menu"""
    print("\n" + "="*60)
    print("Multi-Modal AI Agent - Example Usage")
    print("="*60)
    print("\nAvailable Examples:")
    print("  1. Image Captioning")
    print("  2. Visual Question Answering")
    print("  3. Zero-Shot Classification")
    print("  4. Comprehensive Analysis")
    print("  5. Agent Usage")
    print("  6. Custom Classification")
    print("  7. Run All Examples")
    print("  0. Exit")
    print("="*60)


def main():
    """Main function"""
    examples = {
        "1": example_1_image_caption,
        "2": example_2_visual_qa,
        "3": example_3_classification,
        "4": example_4_multimodal_analysis,
        "5": example_5_agent,
        "6": example_6_custom_classification,
    }

    while True:
        print_menu()
        choice = input("\nSelect an example (0-7): ").strip()

        if choice == "0":
            print("\nGoodbye!")
            break
        elif choice == "7":
            for func in examples.values():
                func()
            input("\nPress Enter to continue...")
        elif choice in examples:
            examples[choice]()
            input("\nPress Enter to continue...")
        else:
            print("\nInvalid choice. Please try again.")


if __name__ == "__main__":
    print("\n" + "="*60)
    print("🤖 Multi-Modal AI Agent - Examples")
    print("="*60)
    print("\nNote: These examples require actual image files.")
    print("Replace 'path/to/your/image.jpg' with real image paths.")
    print("\nFor testing without images, the examples will show")
    print("what output you can expect.")
    print("="*60)

    main()
