"""
Generate a single video using Z.AI SDK
Use this to generate one video at a time to avoid concurrency limits
"""

import sys
import time
from generate_video import ZAIVideoGenerator


def generate_single(operation):
    """Generate a single video for the specified operation

    Args:
        operation (str): 'plus' or 'minus'
    """

    generator = ZAIVideoGenerator()

    prompts = {
        "plus": (
            "An educational cartoon animation teaching young children about addition "
            "(plus operator). The video shows friendly animated objects like apples "
            "or stars combining together to demonstrate addition. Visual equation "
            "2 + 3 = 5 appears with colorful animations. Bright, cheerful colors, "
            "playful style suitable for elementary school students learning math."
        ),
        "minus": (
            "An educational cartoon animation teaching young children about subtraction "
            "(minus operator). The video shows friendly animated objects being taken "
            "away to demonstrate subtraction. Visual equation 5 - 2 = 3 appears with "
            "clear animations showing objects leaving. Bright, cheerful colors, "
            "playful style suitable for elementary school students learning math."
        )
    }

    if operation not in prompts:
        print(f"Error: Operation must be 'plus' or 'minus'. Got: {operation}")
        sys.exit(1)

    prompt = prompts[operation]

    print(f"\n{'='*60}")
    print(f"Generating video for: {operation.upper()} operator")
    print(f"{'='*60}\n")

    try:
        # Submit video generation task
        task_result = generator.generate_video(
            prompt=prompt,
            quality="speed",
            with_audio=False,
            size="1920x1080",
            fps=30,
            duration=5
        )

        task_id = task_result.get("id")
        print(f"\n✓ Task submitted successfully!")
        print(f"Task ID: {task_id}")
        print(f"\nNow waiting for video generation to complete...")
        print("This typically takes 2-5 minutes.\n")

        # Poll for completion
        final_result = generator.poll_until_complete(
            task_id=task_id,
            check_interval=15,
            timeout=600
        )

        # Check result
        if final_result.get("task_status") == "SUCCESS":
            print(f"\n{'='*60}")
            print(f"✓ {operation.upper()} VIDEO COMPLETED SUCCESSFULLY!")
            print(f"{'='*60}\n")

            if "video_result" in final_result:
                video_url = final_result["video_result"].get("url")
                print(f"Video URL: {video_url}")
                print(f"\nYou can download the video from the URL above.")

                # Also save to a file
                with open(f"{operation}_video_url.txt", "w") as f:
                    f.write(f"Task ID: {task_id}\n")
                    f.write(f"Video URL: {video_url}\n")
                    f.write(f"Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                print(f"\nVideo URL also saved to: {operation}_video_url.txt")
            else:
                print("\nNote: Video completed but URL not in expected format.")
                print(f"Full result: {final_result}")

        elif final_result.get("task_status") == "FAIL":
            print(f"\n✗ Video generation failed!")
            print(f"Result: {final_result}")
        else:
            print(f"\n⚠ Video generation status: {final_result.get('task_status')}")
            print(f"Result: {final_result}")

    except Exception as e:
        print(f"\n✗ Error generating video: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python generate_one_video.py <plus|minus>")
        print("\nExamples:")
        print("  python generate_one_video.py plus")
        print("  python generate_one_video.py minus")
        sys.exit(1)

    operation = sys.argv[1].lower()
    generate_single(operation)
