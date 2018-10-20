import requests
# from google.cloud.vision import types

class VisionApi():
    def __init__(self, img_url):
        # [START vision_quickstart]

        # Instantiates a client
        # [START vision_python_migration_client]

        api_f = open('cloud-vision.key', 'r')
        api_token = api_f.read()
        print("token: " + api_token)
        self.img_url = img_url
        self.request = {}
        self.DISCOVERY_URL = 'https://vision.googleapis.com/v1/images:annotate?key=' + api_token
        print("url: " + self.DISCOVERY_URL)

    def getLabels(self):
        self.request = {
            "requests": [
                {
                    "image": {
                        "source": {
                            "imageUri":
                                self.img_url
                        }
                    },
                    "features": [
                        {
                            "type": "LABEL_DETECTION",
                            "maxResults": 3
                        }
                    ]
                }
            ]
        }

        response = requests.post(self.DISCOVERY_URL, json=self.request)
        print(response.status_code, response.reason)
        jres = response.json()
        labels = [annotations['description'] for annotations in jres['responses'][0]['labelAnnotations']]
        print("Descriptions for " + self.img_url + ":", labels)
        # labels = response.label_annotations
        # print('Labels for ' + self.img_url + ':')
        # for label in labels:
        #     print(label.description)
        return labels


def main():
    test_img = VisionApi('https://i.imgur.com/BBcy6Wc.jpg')
    test_img.getLabels()


if __name__ == '__main__':
    main()