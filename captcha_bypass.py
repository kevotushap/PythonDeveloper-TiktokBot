import requests

def solve_captcha(captcha_image_url):
    """
    Solve CAPTCHA using the sadcaptcha API.

    :param captcha_image_url: URL of the CAPTCHA image to solve.
    :return: The CAPTCHA solution if successful, otherwise raises an exception.
    """
    # Define the API endpoint
    api_url = "https://www.sadcaptcha.com/api/solve"

    # Prepare the data payload for the POST request
    data = {
        'image_url': captcha_image_url,
        'ref': 'angell'  # Replace with actual reference if needed
    }

    # Send the POST request to the API
    response = requests.post(api_url, data=data)

    # Check if the response is successful
    if response.status_code == 200:
        return response.json().get('solution')  # Return the CAPTCHA solution
    else:
        raise Exception("Failed to solve CAPTCHA")  # Raise an exception if the request fails
