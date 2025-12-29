import requests
import json
import base64
import os

class HFBiometric:
    def __init__(self, biometric_device):
        self.password = biometric_device['DevicePassword']
        self.base_url = f"http://{biometric_device['DeviceIP']}:{biometric_device['DevicePort']}"
        self.session = requests.Session()

    def reset_device(self):
        url = f"{self.base_url}/device/reset"
        data = {'pass': self.password}
        response = self.session.post(url, data=data)
        response.raise_for_status()
        return response.text

    def get_device_serial_number(self):
        url = f"{self.base_url}/getDeviceKey"
        response = self.session.post(url)
        response.raise_for_status()
        return response.text

    def restart_device(self):
        url = f"{self.base_url}/restartDevice?pass={self.password}"
        response = self.session.post(url)
        response.raise_for_status()
        return response.text

    def create_person(self, persons):
        try:
            url = f"{self.base_url}/api/v2/person/create"
            data = {
                'pass': self.password,
                'persons': json.dumps(persons)
            }
            response = self.session.post(url, data=data)
            response.raise_for_status()
            print(response.text)
            return True
        except Exception as e:
            print(f"Error: {str(e)}")
            return False

    def register_photo_with_response(self, photo_registration):
        try:
            url = f"{self.base_url}/face/create"
            data = {
                'faceId': photo_registration['FaceId'],
                'imgBase64': photo_registration['ImgBase64'],
                'personId': photo_registration['PersonId'],
                'pass': photo_registration['Pass']
            }
            response = self.session.post(url, data=data)
            response.raise_for_status()
            print(response.text)
            self.display_uploaded_picture(photo_registration['ImgBase64'])
            return True
        except Exception as e:
            print(f"Error: {str(e)}")
            return False

    def register_photo_with_http_response(self, photo_registration):
        try:
            url = f"{self.base_url}/face/create"
            data = {
                'faceId': photo_registration['FaceId'],
                'imgBase64': photo_registration['ImgBase64'],
                'personId': photo_registration['PersonId'],
                'pass': photo_registration['Pass']
            }
            response = self.session.post(url, data=data)
            response.raise_for_status()
            self.display_uploaded_picture(photo_registration['ImgBase64'])
            return response
        except Exception as e:
            print(f"Error: {str(e)}")
            return None

    def set_device_config(self, config_data):
        url = f"{self.base_url}/setConfig"
        data = {
            'pass': self.password,
            'config': json.dumps(config_data)
        }
        response = self.session.post(url, data=data)
        response.raise_for_status()
        return response.text

    def delete_person(self, request_model):
        url = f"{self.base_url}/person/delete"
        data = {
            'pass': self.password,
            'id': str(request_model['Id'])
        }
        response = self.session.post(url, data=data)
        response.raise_for_status()
        return response.text

    def modify_logo(self):
        url = f"{self.base_url}/changeLogo"
        image_path = "images/logo1.png"  # adjust path as necessary
        base64_img = self.convert_image_to_base64(image_path)
        if base64_img is None:
            return "Image not found"

        data = {
            'pass': self.password,
            'imgBase64': base64_img
        }

        response = self.session.post(url, data=data)
        response.raise_for_status()
        return response.text

    def convert_image_to_base64(self, image_path):
        full_path = os.path.join(os.getcwd(), image_path)
        if os.path.exists(full_path):
            with open(full_path, 'rb') as image_file:
                return base64.b64encode(image_file.read()).decode('utf-8')
        else:
            print(f"Image not found at path: {full_path}")
            return None

    def display_uploaded_picture(self, img_base64):
        url = f"{self.base_url}/api/v2/device/showImage"
        data = {
            'pass': self.password,
            'imgBase64': img_base64,
            'showTime': '2'
        }
        response = self.session.post(url, data=data)
        response.raise_for_status()
        return response.text
