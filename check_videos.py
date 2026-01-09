"""
Check Z.AI video generation status and retrieve completed videos
"""

import os
import requests
from dotenv import load_dotenv
from zai import ZaiClient

# Load environment variables
load_dotenv()


class ZAIVideoChecker:
    """Check and retrieve Z.AI video generation status"""

    def __init__(self, api_key=None):
        """Initialize the Z.AI video checker

        Args:
            api_key (str): Z.AI API key. If None, reads from ZAI_API_KEY env var
        """
        self.api_key = api_key or os.getenv("ZAI_API_KEY")
        if not self.api_key:
            raise ValueError("Z.AI API key is required")

        self.base_url = "https://api.z.ai/api/paas/v4"

    def retrieve_result(self, task_id):
        """Retrieve the result of a video generation task

        Args:
            task_id (str): The task ID to check

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

        print(f"Checking task: {task_id}")
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()

        result = response.json()
        return result

    def check_task_ids(self, task_ids):
        """Check multiple task IDs

        Args:
            task_ids (list): List of task IDs to check

        Returns:
            dict: Results keyed by task ID
        """
        results = {}

        for task_id in task_ids:
            try:
                result = self.retrieve_result(task_id)
                results[task_id] = result

                status = result.get("task_status")
                print(f"\n✓ Task ID: {task_id}")
                print(f"  Status: {status}")

                if status == "SUCCESS":
                    if "video_result" in result:
                        video_url = result["video_result"].get("url")
                        print(f"  Video URL: {video_url}")
                elif status == "PROCESSING":
                    print(f"  Still processing...")
                elif status == "FAIL":
                    print(f"  Generation failed")

            except Exception as e:
                print(f"\n✗ Error checking task {task_id}: {str(e)}")
                results[task_id] = {"error": str(e)}

        return results


def main():
    """Main function to check video generation status"""

    print("Z.AI Video Generation Status Checker")
    print("="*60)

    # Check for saved task IDs
    task_files = ["plus_video_url.txt", "minus_video_url.txt"]
    found_task_ids = []

    print("\n1. Checking for saved task IDs...")
    for filename in task_files:
        if os.path.exists(filename):
            print(f"\n  Found: {filename}")
            with open(filename, "r") as f:
                content = f.read()
                print(f"  Content:\n{content}")
                # Extract task ID if present
                for line in content.split("\n"):
                    if line.startswith("Task ID:"):
                        task_id = line.split(": ")[1].strip()
                        found_task_ids.append(task_id)
                        print(f"  → Extracted Task ID: {task_id}")

    if found_task_ids:
        print(f"\n2. Found {len(found_task_ids)} task(s), checking status...")

        try:
            checker = ZAIVideoChecker()
            results = checker.check_task_ids(found_task_ids)

            print("\n" + "="*60)
            print("SUMMARY")
            print("="*60)

            for task_id, result in results.items():
                if "error" in result:
                    print(f"\n{task_id}: ERROR - {result['error']}")
                else:
                    status = result.get("task_status")
                    if status == "SUCCESS" and "video_result" in result:
                        url = result["video_result"].get("url")
                        print(f"\n{task_id}: SUCCESS")
                        print(f"  Video URL: {url}")
                    else:
                        print(f"\n{task_id}: {status}")

        except Exception as e:
            print(f"\nError: {str(e)}")

    else:
        print("\n  No saved task IDs found.")

    # Instructions
    print("\n" + "="*60)
    print("HOW TO CHECK YOUR VIDEO GENERATIONS")
    print("="*60)
    print("""
To see your video generation history:

1. **Via Web Dashboard (Recommended)**:
   - Go to: https://api.z.ai/ or https://bigmodel.cn/
   - Log in with your account
   - Look for sections like:
     * "My Generations"
     * "Task History"
     * "Video Gallery"
     * "Usage/Records"

2. **If you have specific Task IDs**:
   - Add them to this script or run:
     python check_specific_task.py <task_id>

3. **Check your email**:
   - Z.AI may have sent completion notifications
   - Look for emails with video links

4. **API Quota/Billing**:
   - Check your account dashboard for:
     * Current balance
     * Usage history
     * Pending tasks
    """)

    # Ask if user wants to check a specific task ID
    print("\n" + "="*60)
    task_id = input("Do you have a specific Task ID to check? (paste it or press Enter): ").strip()

    if task_id:
        try:
            print(f"\nChecking task: {task_id}")
            checker = ZAIVideoChecker()
            result = checker.retrieve_result(task_id)

            print(f"\nStatus: {result.get('task_status')}")
            if result.get("task_status") == "SUCCESS":
                if "video_result" in result:
                    url = result["video_result"].get("url")
                    print(f"\n✓ VIDEO READY!")
                    print(f"Download URL: {url}")
            elif result.get("task_status") == "PROCESSING":
                print(f"\n⏳ Still processing, check again in a few minutes")
            elif result.get("task_status") == "FAIL":
                print(f"\n✗ Video generation failed")
        except Exception as e:
            print(f"\nError: {str(e)}")


if __name__ == "__main__":
    main()
