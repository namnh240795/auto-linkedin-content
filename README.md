# Z.AI Video Generator - Plus and Minus Teaching Videos

This project uses the Z.AI SDK and CogVideoX model to generate educational videos teaching children about addition (plus) and subtraction (minus) operators.

## Features

- Generate animated educational videos using AI
- Text-to-video generation with CogVideoX-3 model
- Automatic polling for video completion
- Generates two separate videos:
  - **Plus Operator Video**: Teaches addition with colorful animations
  - **Minus Operator Video**: Teaches subtraction with visual demonstrations

## Prerequisites

- Python 3.8 or higher
- Z.AI API key (get one at [https://api.z.ai/](https://api.z.ai/))

## Installation

1. **Clone or download this project**

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your API key:**

   Create a `.env` file in the project root:
   ```bash
   cp .env.example .env
   ```

   Edit `.env` and add your Z.AI API key:
   ```
   ZAI_API_KEY=your_actual_api_key_here
   ```

## Usage

### Generate Videos

Run the main script to generate both plus and minus operator videos:

```bash
python generate_video.py
```

The script will:
1. Submit video generation tasks to Z.AI
2. Poll for completion (checks every 10 seconds)
3. Display the video URLs when ready

### Expected Output

```
Z.AI Video Generator - Plus and Minus Operator Teaching Videos
============================================================

Generating video for: PLUS operator
============================================================

Generating video with prompt: An educational cartoon animation...
Parameters: cogvideox-3, speed, 1920x1080, 30fps, 5s
Video generation task submitted successfully!
Task ID: 1234567890
Request ID: req_abc123
Status: PROCESSING

Polling for completion...
Current status: PROCESSING
Waiting 10 seconds...
Current status: SUCCESS
Video generation completed successfully!

✓ PLUS video ready!
Video URL: https://...

Generating video for: MINUS operator
...
```

## Customization

You can modify the `generate_math_videos()` function in `generate_video.py` to:

- **Change prompts**: Edit the prompts dictionary to customize video content
- **Adjust quality**: Change `quality="speed"` to `quality="quality"` for higher quality
- **Enable audio**: Set `with_audio=True` to add AI sound effects
- **Change resolution**: Modify `size` (options: "1280x720", "1920x1080", "3840x2160", etc.)
- **Adjust duration**: Change `duration` (options: 5 or 10 seconds)
- **Change frame rate**: Modify `fps` (options: 30 or 60)

Example:
```python
task_result = generator.generate_video(
    prompt=prompt,
    quality="quality",     # Higher quality mode
    with_audio=True,        # Enable sound effects
    size="3840x2160",      # 4K resolution
    fps=60,                # 60 FPS
    duration=10            # 10 seconds
)
```

## API Reference

### ZAIVideoGenerator Class

#### `generate_video(prompt, model, quality, with_audio, size, fps, duration)`

Generate a video from text prompt.

**Parameters:**
- `prompt` (str): Text description (max 512 characters)
- `model` (str): Model name (default: "cogvideox-3")
- `quality` (str): "speed" or "quality" mode
- `with_audio` (bool): Generate AI sound effects
- `size` (str): Resolution (e.g., "1920x1080")
- `fps` (int): Frame rate - 30 or 60
- `duration` (int): Duration in seconds - 5 or 10

#### `retrieve_result(task_id)`

Retrieve the result of a video generation task.

#### `poll_until_complete(task_id, check_interval, timeout)`

Poll task status until completion or timeout.

## Project Structure

```
videogenerator/
├── generate_video.py      # Main script
├── requirements.txt        # Python dependencies
├── .env.example           # Environment variables template
├── .env                   # Your API key (create this)
└── README.md              # This file
```

## Troubleshooting

### "Z.AI API key is required"
Make sure you've created a `.env` file with your API key.

### "Video generation failed"
- Check your API key is valid
- Ensure you have sufficient credits/quota on your Z.AI account
- Try with `quality="speed"` instead of `quality="quality"`

### Timeout errors
Video generation can take several minutes. Increase the timeout in `poll_until_complete()`:
```python
final_result = generator.poll_until_complete(
    task_id=task_id,
    check_interval=10,
    timeout=600  # 10 minutes instead of 5
)
```

## Resources

- [Z.AI Documentation](https://docs.z.ai/)
- [Video Generation API Reference](https://docs.z.ai/api-reference/video/generate-video)
- [Quick Start Guide](https://docs.z.ai/guides/overview/quick-start)
- [Python SDK GitHub](https://github.com/zai-org/z-ai-sdk-python)

## License

This project is provided as-is for educational purposes.

## Support

For issues related to:
- **Z.AI API**: Contact Z.AI support
- **This script**: Check the code comments or modify as needed

---

**Note**: Video generation uses API credits. Check your Z.AI pricing plan for details.
# auto-linkedin-content
