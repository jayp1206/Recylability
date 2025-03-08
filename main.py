import nyckel
import cv2
import serial
import requests

# Get API Credentials
user_id = "ef685j8v6rle35viejvu0kw6kmpm0fsy"
user_secret = "49d85yrdqz2x9g7m5je0olauizniulvqzm9trndgsi41hzx4f2hg1sajzjp5a8i4"
credentials = nyckel.Credentials(user_id, user_secret)

# Test Images
soda = "https://images.pexels.com/photos/1292294/pexels-photo-1292294.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2"
bag = "https://images.pexels.com/photos/3746335/pexels-photo-3746335.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2"
styrofoam = "https://images.pexels.com/photos/5768314/pexels-photo-5768314.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2"

# Print Result
print(nyckel.invoke("recycling-identifier", styrofoam, credentials)['labelName'])

def img_url(image_path):
    url = 'https://file.io'
    files = {'file': open(image_path, 'rb')}
    
    # Upload the image
    response = requests.post(url, files=files)
    
    # Check for successful upload
    if response.status_code == 200:
        file_url = response.json().get('link')
        return file_url
    else:
        print("Failed to upload image.")
        return None
    
def analyze():
    cam = cv2.VideoCapture(0)
    result, image = cam.read()
    if result:
        cv2.imwrite("image.png", image)
        print(img_url("image.png"))
    else:
        print("Image capture failed")



analyze()
# Listen for button press
'''serial_port = serial.Serial( port='/dev/ttyUSB1', baudrate=115200 )
while ( True ):
    command = serial_port.read( 2 )  # read 2 bytes from the Arduino
    if ( len( command ) == 2 ):
        if ( command == b'GO' ):
            analyze()

'''