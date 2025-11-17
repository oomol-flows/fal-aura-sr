#region generated meta
import typing
class Inputs(typing.TypedDict):
    task_id: str
    enable_polling: bool | None
    max_attempts: float | None
    interval_seconds: float | None
class Outputs(typing.TypedDict):
    status: typing.NotRequired[str]
    image_url: typing.NotRequired[str]
    result: typing.NotRequired[dict]
    is_completed: typing.NotRequired[bool]
#endregion

from oocana import Context
import requests
import asyncio

async def main(params: Inputs, context: Context) -> Outputs:
    """
    Query the conversion result status from fal-aura-sr API using OOMOL token.
    Supports optional polling to wait for task completion.

    Args:
        params: Input parameters containing task_id and polling options
        context: OOMOL execution context

    Returns:
        Dictionary containing status, result data, and completion flag
    """
    task_id = params["task_id"]

    # Get polling parameters with null-safe defaults
    enable_polling_param = params.get("enable_polling")
    enable_polling = enable_polling_param if enable_polling_param is not None else True

    max_attempts_param = params.get("max_attempts")
    max_attempts = int(max_attempts_param) if max_attempts_param is not None else 120

    interval_seconds_param = params.get("interval_seconds")
    interval_seconds = int(interval_seconds_param) if interval_seconds_param is not None else 2

    # Get OOMOL token
    oomol_token = await context.oomol_token()

    # Construct the API endpoint
    url = f"https://fusion-api.oomol.com/v1/fal-aura-sr/result/{task_id}"

    # Set up headers with OOMOL token
    headers = {
        "Authorization": oomol_token
    }

    if enable_polling:
        print(f"Polling task {task_id}...")
        print(f"Max attempts: {max_attempts}, Interval: {interval_seconds}s")

    attempts = 1 if not enable_polling else max_attempts

    for attempt in range(1, attempts + 1):
        try:
            # Update progress
            if enable_polling:
                progress = int((attempt / attempts) * 100)
                context.report_progress(progress)
                if attempt > 1:
                    print(f"\nAttempt {attempt}/{attempts}...")

            # Make GET request to query the result
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()

            # Parse the response
            result_data = response.json()

            # Print the API response for debugging (only on first attempt or when polling)
            if attempt == 1 or enable_polling:
                print("=" * 60)
                print("API Response:")
                print("=" * 60)
                print(result_data)
                print("=" * 60)

            # Extract state from response
            state = result_data.get("state", "unknown")

            # Extract image URL from nested structure: data.image.url
            image_url = ""
            if "data" in result_data and isinstance(result_data["data"], dict):
                image_data = result_data["data"].get("image", {})
                if isinstance(image_data, dict):
                    image_url = image_data.get("url", "")

            # Use state as status (processing, completed, failed, etc.)
            status = state

            # Determine if the task is completed (only when we have image_url)
            is_completed = bool(image_url) and state not in ["processing", "pending", "queued"]

            if enable_polling:
                print(f"Current state: {state}")
                if image_url:
                    print(f"Image URL: {image_url}")

            # If completed or failed, return immediately
            if is_completed:
                if enable_polling:
                    print(f"\n✓ Task completed successfully after {attempt} attempts!")
                    context.report_progress(100)
                return {
                    "status": status,
                    "image_url": image_url,
                    "result": result_data,
                    "is_completed": True
                }

            # Check if failed
            if state in ["failed", "error"]:
                if enable_polling:
                    print(f"\n✗ Task failed with state: {state}")
                return {
                    "status": status,
                    "image_url": "",
                    "result": result_data,
                    "is_completed": False
                }

            # If not polling, return current state
            if not enable_polling:
                return {
                    "status": status,
                    "image_url": image_url,
                    "result": result_data,
                    "is_completed": is_completed
                }

            # Still processing, wait before next attempt
            if attempt < attempts:
                print(f"Still {state}... waiting {interval_seconds}s before next check")
                await asyncio.sleep(interval_seconds)

        except requests.exceptions.RequestException as e:
            error_message = f"Failed to query result: {str(e)}"
            print(f"Request error on attempt {attempt}: {error_message}")

            if not enable_polling or attempt >= attempts:
                return {
                    "status": "error",
                    "image_url": "",
                    "result": {"error": error_message},
                    "is_completed": False
                }

            # Wait before retry
            if attempt < attempts:
                await asyncio.sleep(interval_seconds)

    # Timeout reached (only when polling is enabled)
    print(f"\n⚠ Timeout: Max attempts ({attempts}) reached")
    return {
        "status": "timeout",
        "image_url": "",
        "result": {"error": f"Polling timeout after {attempts} attempts"},
        "is_completed": False
    }
