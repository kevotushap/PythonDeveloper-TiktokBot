import requests


def solve_captcha(captcha_image_url):
    # Replace with your actual API call to sadcaptcha
    api_url = "https://www.sadcaptcha.com/api/solve"
    data = {
        'image_url': captcha_image_url,
        'ref': 'angell'  # Replace with actual reference if needed
    }
    response = requests.post(api_url, data=data)

    if response.status_code == 200:
        return response.json().get('solution')
    else:
        raise Exception("Failed to solve CAPTCHA")
