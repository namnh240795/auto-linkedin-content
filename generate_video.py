"""
Video Generator using Z.AI SDK
Generates educational videos about plus and minus operators
"""

import os
import time
import requests
from dotenv import load_dotenv
from zai import ZaiClient

# Load environment variables
load_dotenv()


class ZAIVideoGenerator:
    """Generate videos using Z.AI CogVideoX model"""

    def __init__(self, api_key=None):
        """Initialize the Z.AI video generator

        Args:
            api_key (str): Z.AI API key. If None, reads from ZAI_API_KEY env var
        """
        self.api_key = api_key or os.getenv("ZAI_API_KEY")
        if not self.api_key:
            raise ValueError(
                "Z.AI API key is required. Set ZAI_API_KEY environment variable "
                "or pass api_key parameter."
            )

        self.client = ZaiClient(api_key=self.api_key)
        self.base_url = "https://api.z.ai/api/paas/v4"

    def generate_video(
        self,
        prompt,
        model="cogvideox-3",
        quality="speed",
        with_audio=False,
        size="1920x1080",
        fps=30,
        duration=5
    ):
        """Generate a video from text prompt

        Args:
            prompt (str): Text description of the video (max 512 characters)
            model (str): Model to use (default: cogvideox-3)
            quality (str): 'speed' or 'quality' mode
            with_audio (bool): Whether to generate AI sound effects
            size (str): Video resolution (e.g., '1920x1080')
            fps (int): Frame rate (30 or 60)
            duration (int): Video duration in seconds (5 or 10)

        Returns:
            dict: Response with task ID for video generation
        """
        url = f"{self.base_url}/videos/generations"

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Accept-Language": "en-US,en"
        }

        payload = {
            "model": model,
            "prompt": prompt,
            "quality": quality,
            "with_audio": with_audio,
            "size": size,
            "fps": fps,
            "duration": duration
        }

        print(f"Generating video with prompt: {prompt[:100]}...")
        print(f"Parameters: {model}, {quality}, {size}, {fps}fps, {duration}s")

        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()

        result = response.json()
        print(f"Video generation task submitted successfully!")
        print(f"Task ID: {result.get('id')}")
        print(f"Request ID: {result.get('request_id')}")
        print(f"Status: {result.get('task_status')}")

        return result

    def retrieve_result(self, task_id):
        """Retrieve the result of a video generation task

        Args:
            task_id (str): The task ID returned from generate_video

        Returns:
            dict: Task result with video URL if available
        """
        url = f"{self.base_url}/videos/retrievals"

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "id": task_id
        }

        print(f"Retrieving result for task: {task_id}")
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()

        result = response.json()
        return result

    def poll_until_complete(self, task_id, check_interval=10, timeout=300):
        """Poll the task status until completion or timeout

        Args:
            task_id (str): Task ID to poll
            check_interval (int): Seconds between status checks
            timeout (int): Maximum seconds to wait

        Returns:
            dict: Final task result
        """
        start_time = time.time()

        while time.time() - start_time < timeout:
            result = self.retrieve_result(task_id)
            status = result.get("task_status")

            print(f"Current status: {status}")

            if status == "SUCCESS":
                print("Video generation completed successfully!")
                return result
            elif status == "FAIL":
                print("Video generation failed!")
                return result

            print(f"Waiting {check_interval} seconds...")
            time.sleep(check_interval)

        print("Timeout reached while waiting for video generation")
        return result


def generate_single_video(generator, operation, prompt):
    """Generate a single video and wait for completion

    Args:
        generator: ZAIVideoGenerator instance
        operation: str - Operation name (plus/minus)
        prompt: str - Video generation prompt

    Returns:
        dict with results
    """
    print(f"\n{'='*60}")
    print(f"Generating video for: {operation.upper()} operator")
    print(f"{'='*60}\n")

    try:
        # Submit video generation task
        task_result = generator.generate_video(
            prompt=prompt,
            quality="speed",  # Use 'quality' for higher quality
            with_audio=False,
            size="1920x1080",
            fps=30,
            duration=5
        )

        task_id = task_result.get("id")

        # Poll for completion
        print(f"\nPolling for completion...")
        final_result = generator.poll_until_complete(
            task_id=task_id,
            check_interval=15,  # Check every 15 seconds
            timeout=600  # Wait up to 10 minutes
        )

        # Check if video URL is available
        if final_result.get("task_status") == "SUCCESS":
            print(f"\n✓ {operation.upper()} video ready!")
            if "video_result" in final_result:
                video_url = final_result["video_result"].get("url")
                print(f"Video URL: {video_url}")
            return {"status": "success", "result": final_result}
        else:
            print(f"\n✗ {operation.upper()} video generation failed or incomplete")
            return {"status": "failed", "result": final_result}

    except Exception as e:
        print(f"\nError generating {operation} video: {str(e)}")
        return {"status": "error", "error": str(e)}


def generate_math_videos():
    """Generate videos teaching plus and minus operators - ONE AT A TIME"""

    generator = ZAIVideoGenerator()

    # Define prompts for plus and minus videos
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

    results = {}

    # Generate videos ONE AT A TIME to avoid concurrency limits
    for operation, prompt in prompts.items():
        result = generate_single_video(generator, operation, prompt)
        results[operation] = result

        # If we just completed a video successfully, wait before starting the next
        if result.get("status") == "success":
            print(f"\n✓ {operation.upper()} video completed successfully!")
            # Check if there are more videos to generate
            remaining = [op for op in prompts.keys() if op not in results]
            if remaining:
                print(f"\nWaiting 30 seconds before generating next video...")
                print("This ensures we don't hit the concurrency limit.")
                time.sleep(30)

    return results


if __name__ == "__main__":
    print("Z.AI Video Generator - Plus and Minus Operator Teaching Videos")
    print("="*60)
    print("\nThis script will generate educational videos teaching addition "
          "and subtraction using the Z.AI CogVideoX model.\n")

    try:
        results = generate_math_videos()

        print("\n" + "="*60)
        print("SUMMARY")
        print("="*60)

        for key, value in results.items():
            print(f"\n{key}: {value}")

        print("\n" + "="*60)
        print("All done! Check the results above for video URLs and task IDs.")
        print("="*60)

    except Exception as e:
        print(f"\nError: {str(e)}")
        print("\nMake sure you have set up your ZAI_API_KEY in a .env file.")
        print("Create a .env file with: ZAI_API_KEY=your_api_key_here")
