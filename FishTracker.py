try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract
import cv2
import keyboard
import time

inventorySpace = 0
fishDB = {}
inventory = {}
pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'
print('Start')

def run():
    init()
    active = True
    while True:
        if active:
            if keyboard.is_pressed('x'):
                checkFish()
            elif keyboard.is_pressed('alt + z'):
                active = False
                print('Not active')
                time.sleep(1)
            elif keyboard.is_pressed('c'):
                print(inventory)
            elif keyboard.is_pressed('c'):
                print(f'Inventory value: {inventoryValue()} bells')
            elif keyboard.is_pressed('v'):
                for key, val in fishDB:
                    print(f'{key}: {val}')
        if keyboard.is_pressed('alt + z'):
            active = True
            print('Active')
            time.sleep(1)
        time.sleep(0.05)

def init():
    global inventorySpace
    db = open('database.txt', 'r')
    for line in db:
        entry = line.split(';')
        fishDB[entry[0].strip().lower()] = int(entry[1].strip().lower())
    while True:
        item = input('Fish in inventory (type 0 if none): ').lower()
        if item == '0':
            break
        elif item not in inventory:
            inventory[item] = 1
        else:
            inventory[item] += 1

    inventorySpace = int(input('Total slots for fish: '))


def testImage():
    camera = cv2.VideoCapture('https://192.168.1.9:8080/video')
    r, img = camera.read()
    cv2.imwrite('testImage.jpg', img)
    imgText = pytesseract.image_to_string(Image.open('testImage.jpg')).lower()
    print(imgText)

def checkFish():
    imgText = getImageText()
    for fString in fishDB.keys():
        if fString in imgText:
            print(f'Fish found: {fString}')
            print(f'Inventory space: {inventorySpace - sum(inventory.values())}')
            if sum(inventory.values()) < inventorySpace:
                addFish(fString)
            else: 
                fMin = lowestFish()
                if fMin[1] < fishDB[fString]:
                    input(f'Remove {fMin[0]} for an additional {fishDB[fString]-fMin[1]} bells')
                    removeFish(fMin[0])
                    addFish(fString)
                else: 
                    input(f'Toss is, unless you want {fMin[1]-fishDB[fString]} less bells')
        else:
            print('No fish detected')

def addFish(fString):
    if fishString not in inventory:
        inventory[fString] = 1
    else:
        inventory[fString] += 1
    print(f'Added {fString} to inventory')

def removeFish(fString):
    inventory[fString] -= 1
    if inventory[fString] == 0:
        inventory.pop(fString, None)

def lowestFish():
    minValFish = ''
    minVal = 20000
    for entry in inventory.keys():
        if fishDB[entry] < minVal:
            minVal = fishDB[entry]
            minValFish = entry
    return [minValFish, minVal]

def inventoryValue():
    val = 0
    for item, amount in inventory:
        val += (fishDB[item])*amount
    return val

def getImageText():
    camera = cv2.VideoCapture('https://192.168.1.9:8080/video')
    r, img = camera.read()
    cv2.imwrite('fish.jpg', img)
    return pytesseract.image_to_string(Image.open('fish.jpg')).lower()
        
