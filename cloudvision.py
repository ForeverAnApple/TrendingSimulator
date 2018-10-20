import requests


class VisionApi():
    # images will be a list of tuples, with tuple being (image_id, image_url)
    def __init__(self, images):
        # [START vision_quickstart]

        # Instantiates a client
        # [START vision_python_migration_client]

        api_f = open('cloud-vision.key', 'r')
        api_token = api_f.read()
        print("token: " + api_token)
        self.images = images
        self.DISCOVERY_URL = 'https://vision.googleapis.com/v1/images:annotate?key=' + api_token
        print("url: " + self.DISCOVERY_URL)

    def getlabels(self):
        # Created a massive request for all the images
        request = {'requests': []}
        for image in self.images:
            request['requests'].append({
                "image": {
                    "source": {
                        "imageUri":
                            image[1]
                    }
                },
                "features": [
                    {
                        "type": "LABEL_DETECTION",
                        "maxResults": 3
                    }
                ]
            })

        # HTTP POST the request with json body
        response = requests.post(self.DISCOVERY_URL, json=request)
        print(response.status_code, response.reason)

        # Parse into json dictionary
        jres = response.json()

        # construct label
        labels = []

        # This goes through each response, and for every single description of the big image requests sent, create a
        # list of lists of image ids and a list of their tags received from Google Cloud Vision
        for label_i, response in enumerate(jres['responses']):
            innertags = []
            for annotations in response['labelAnnotations']:
                innertags.append(annotations['description'])

            print('assigning label', label_i)
            print('images at', label_i, 'is', self.images[label_i])
            print('inner tags for label', label_i, 'is', innertags)
            labels.append([self.images[label_i][0], innertags])

        print(labels)
        # labels = [annotations['description'] for annotations in jres['responses'][0]['labelAnnotations']]
        # print("Descriptions for " + self.img_url + ":", labels)
        # labels = response.label_annotations
        # print('Labels for ' + self.img_url + ':')
        # for label in labels:
        #     print(label.description)
        return labels


def main():
    images = ((2, 'https://i.imgur.com/BBcy6Wc.jpg'),
              (1, 'https://www.petmd.com/sites/default/files/salmonella-infection-dogs.jpg'),
              (0, 'https://media.gettyimages.com/photos/fish-shape-made-up-of-fish-picture-id182108931'),
              (3, 'https://i.imgur.com/PT3Nh7B.jpg'))
    test_img = VisionApi(images)
    test_img.getlabels()


if __name__ == '__main__':
    main()