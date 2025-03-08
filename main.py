import nyckel
import cv2
from imgurpython import ImgurClient
import serial

# Imgur Client ID
IMGUR_CLIENT_ID = "ec59d37ddd7bd5a"
IMGUR_CLIENT_SECRET = "ad56d86a085615d8f3af5ea711d3c9b5a504f152"
IMGUR_ACCESS_TOKEN = "29d36f0417313a44195c0557503c1613408ccc9f"
IMGUR_REFRESH_TOKEN = "c6ec821353f112d6a393ee9107e50ab08cf3c0e5"
IMGUR_ALBUM_ID = "DESK267"

# Nyckel API Credentials
NYCKEL_USER_ID = "ef685j8v6rle35viejvu0kw6kmpm0fsy"
NYCKEL_USER_SECRET = "49d85yrdqz2x9g7m5je0olauizniulvqzm9trndgsi41hzx4f2hg1sajzjp5a8i4"

def upload_to_imgur(image_path):
    client = ImgurClient(IMGUR_CLIENT_ID, IMGUR_CLIENT_SECRET, IMGUR_REFRESH_TOKEN)
    client.set_user_auth(IMGUR_ACCESS_TOKEN, IMGUR_REFRESH_TOKEN)
    config = {
	    'album': IMGUR_ALBUM_ID,
	}
    upload_results = client.upload_from_path(image_path, config=config, anon=False)
    url = upload_results['link']
    id = upload_results['id']
    return url, id

def delete_from_imgur(image_id):
    client = ImgurClient(IMGUR_CLIENT_ID, IMGUR_CLIENT_SECRET, IMGUR_REFRESH_TOKEN)
    client.set_user_auth(IMGUR_ACCESS_TOKEN, IMGUR_REFRESH_TOKEN)
    client.delete_image(image_id)

# Take photo and pass to nyckel
def analyze():
    cam = cv2.VideoCapture(0)
    result, image = cam.read()
    cam.release()
    if result:
        cv2.imwrite("image.png", image)
    else:
        print("Image capture failed")
        quit()

    link, img_id = upload_to_imgur("image.png")
    print(link)

    credentials = nyckel.Credentials(NYCKEL_USER_ID, NYCKEL_USER_SECRET)

    try:
        result = nyckel.invoke("recycling-identifier", link, credentials)['labelName']
    except KeyError:
        print("Error")

    else:
        for char in ['#', '/', '(', ')', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
            result = result.replace(char, "")

    print(result)

    delete_from_imgur(img_id)



input("Analyze? ")
analyze()

# Listen for button press
'''
serial_port = serial.Serial( port='/dev/ttyUSB1', baudrate=115200 )
while ( True ):
    command = serial_port.read( 2 )  # read 2 bytes from the Arduino
    if ( len( command ) == 2 ):
        if ( command == b'GO' ):
            analyze()

'''
