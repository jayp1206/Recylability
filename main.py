import nyckel
import cv2
import requests
import json
import serial
import urllib.request
import base64

# Imgur Client ID
IMGUR_CLIENT_ID = 'ec59d37ddd7bd5a'

# Get Nyckel API Credentials
NYCKEL_USER_ID = "ef685j8v6rle35viejvu0kw6kmpm0fsy"
NYCKEL_USER_SECRET = "49d85yrdqz2x9g7m5je0olauizniulvqzm9trndgsi41hzx4f2hg1sajzjp5a8i4"

credentials = nyckel.Credentials(NYCKEL_USER_ID, NYCKEL_USER_SECRET)


def upload_to_imgur(image_path):
    # Open the image and convert it to base64
    with open(image_path, "rb") as image:
        image_data = image.read()
        b64_image = base64.standard_b64encode(image_data).decode('utf-8')  # Ensure it's a string for the data

    headers = {'Authorization': 'Client-ID ' + IMGUR_CLIENT_ID}
    
    # Prepare the data dictionary
    data = {
        'image': b64_image,
        'title': 'test'
    }

    # URL-encode the data and make sure it's in bytes
    encoded_data = urllib.parse.urlencode(data).encode('utf-8')

    # Send the request
    request = urllib.request.Request(url="https://api.imgur.com/3/upload.json", data=encoded_data, headers=headers)

    try:
        response = urllib.request.urlopen(request).read()
        parse = json.loads(response)
        return parse['data']['link']
    except Exception as e:
        print(f"Error uploading image: {e}")
        return None





# Take photo and pass to nyckel
def analyze():
    cam = cv2.VideoCapture(0)
    result, image = cam.read()
    if result:
        cv2.imwrite("image.png", image)
    else:
        print("Image capture failed")
        quit()

    link = upload_to_imgur("image.png")
    print(link)
    print(nyckel.invoke("recycling-identifier", link, credentials))



input("Analyze? ")
analyze()

#input("Delete?")
#delete_from_gofile()


# Listen for button press
'''
serial_port = serial.Serial( port='/dev/ttyUSB1', baudrate=115200 )
while ( True ):
    command = serial_port.read( 2 )  # read 2 bytes from the Arduino
    if ( len( command ) == 2 ):
        if ( command == b'GO' ):
            analyze()

'''
