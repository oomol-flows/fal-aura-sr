#region generated meta
import typing
class Inputs(typing.TypedDict):
    image_url: str
class Outputs(typing.TypedDict):
    session_id: typing.NotRequired[str]
    success: typing.NotRequired[bool]
#endregion

from oocana import Context
import requests

async def main(params: Inputs, context: Context) -> Outputs:
    """
    Submit an image to the clarity enhancement API and return the session ID.

    This task only submits the request and returns the session ID for polling.
    """
    image_url = params["image_url"]

    # Get OOMOL token for authentication
    token = await context.oomol_token()

    # Submit the enhancement request
    submit_url = "https://fusion-api.oomol.com/v1/fal-aura-sr/submit"
    headers = {
        "Authorization": token,
        "Content-Type": "application/json"
    }

    submit_payload = {
        "imageURL": image_url
    }

    context.report_progress(50)

    # Submit the request
    submit_response = requests.post(
        submit_url,
        json=submit_payload,
        headers=headers,
        timeout=30.0
    )

    if submit_response.status_code == 502:
        raise Exception("The image enhancement API is temporarily unavailable (502 Bad Gateway). Please try again later.")

    if submit_response.status_code != 200:
        # Try to parse error message from JSON response
        try:
            error_data = submit_response.json()
            error_msg = error_data.get("error", error_data.get("message", str(error_data)))
            raise Exception(f"API request failed ({submit_response.status_code}): {error_msg}")
        except:
            raise Exception(f"API request failed with status {submit_response.status_code}")

    submit_result = submit_response.json()

    # Get session ID from response
    session_id = submit_result.get("sessionID")
    success = submit_result.get("success", False)

    if not session_id:
        raise Exception(f"No sessionID returned from submit endpoint. Response: {submit_result}")

    context.report_progress(100)

    return {
        "session_id": session_id,
        "success": success
    }
