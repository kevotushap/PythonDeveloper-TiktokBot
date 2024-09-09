import requests
import time


def solve_captcha(captcha_image_url):
    # Your 2Captcha API key
    api_key = '6342c84f0de54f8717c3afbfa2d9845f'

    try:
        # Step 1: Submit the CAPTCHA for solving
        api_submit_url = "http://2captcha.com/in.php"
        print(f"Fetching CAPTCHA image from: {captcha_image_url}")
        image_response = requests.get(captcha_image_url)

        if image_response.status_code != 200:
            raise Exception(f"Failed to fetch CAPTCHA image: HTTP {image_response.status_code}")

        print("CAPTCHA image fetched successfully.")
        files = {'file': ('captcha.jpg', image_response.content, 'image/jpeg')}
        data = {
            'key': api_key,
            'method': 'post',
            'json': 1
        }

        submit_response = requests.post(api_submit_url, files=files, data=data)
        submit_result = submit_response.json()

        if submit_result['status'] == 1:
            request_id = submit_result['request']
            result_url = f"https://2captcha.com/res.php?key={api_key}&action=get&id={request_id}&json=1"

            # Step 2: Poll for the solution
            for _ in range(10):  # Try for up to 10 times
                result_response = requests.get(result_url)
                result_data = result_response.json()

                if result_data['status'] == 1:
                    print("CAPTCHA solved successfully.")
                    return result_data['request']

                print("CAPTCHA not yet solved. Retrying...")
                time.sleep(5)  # Wait for 5 seconds before trying again

            raise Exception("Failed to solve CAPTCHA within the timeout period")
        else:
            raise Exception(f"Failed to submit CAPTCHA: {submit_result.get('request', 'No request ID')}")

    except requests.RequestException as e:
        raise Exception(f"Network or HTTP error: {e}")
    except Exception as e:
        raise Exception(f"Error during CAPTCHA solving: {e}")

