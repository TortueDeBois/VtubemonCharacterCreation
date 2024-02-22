from js import File, Uint8Array, window, navigator
import js
from io import BytesIO
import random
import json
import sys
import os
from pathlib import Path
from pyodide.http import pyfetch
import asyncio
from PIL import Image
from PIL.PngImagePlugin import PngInfo

width, height = 400, 200

is_selecting = False
init_sx, init_sy = None, None
sx, sy = None, None

projectName = "/VtubemonCharacterCreation"
data = ['body/Body_32x32_01.png', 'body/Body_32x32_02.png', 'hair/Hair_01.png', 'hair/Hair_02.png', 'hair/Hair_03.png', 'hair/Hair_04.png']
order = ["body","hair"]

indexDict = {}
dictionary = {}

previewImage = None

def initDict(path):
    dictTemp = {}
    i = 0

    for f in os.listdir(path):
        dictTemp[str(i)] = path + "/" + f
        i = i + 1
    return dictTemp

async def draw_image():
    global previewImage

    img_html = js.document.getElementById("preview")

    metadata = set_metadata()
     
    # Get images
    images = await get_images()
    image_name = images[0].name
    images = await convert_to_python_image(images)
    
    js.console.log("1",images[0].size)
    images = resize(images)
    js.console.log("4",images[0].size)

    my_image = images[0]
    for x in range(1,len(images)):
        my_image.paste(images[x], (0,0), mask = images[x])

    # store the final image
    my_stream = BytesIO()
    my_image.save(my_stream, format="PNG", pnginfo=metadata)
    previewImage = my_image

    # convert it in js png file
    image_file = File.new([Uint8Array.new(my_stream.getvalue())], image_name, {type: "image/png"})
    
    # only useful with the first loading
    img_html.classList.remove("loading")
    img_html.classList.add("ready")
    
    # change html image src
    img_html.src = window.URL.createObjectURL(image_file)

async def get_images():
    images = []

    for value in order:
        image = get_image(value)
        images.append(image)

    return images

async def convert_to_python_image(images):
    for x in range(len(images)):
        images[x] = await js_image_to_python_image(images[x])
    
    return images

def set_metadata():
    metadata = PngInfo()
    metadata.add_itxt("Copyright", "Réalisé à partir des tiles de Limezu (https://limezu.itch.io/)")
    metadata.add_itxt("Seed", get_seed())
    return metadata

# Get image from pyodide to an png file used by js
def get_image(shape):
    image_file = get_image_from_pyodide(dictionary[str(shape)][str(indexDict[str(shape)])], str(shape) + ".png")
    return image_file

def get_image_from_pyodide(path, name):
    f = open(path, 'rb')
    image_file = File.new([Uint8Array.new(f.read())], name, {"type": "image/png"})
    return image_file

# Transform a png file (js) to an Image from Pil
async def js_image_to_python_image(jsImage):
    array_buf = Uint8Array.new(await jsImage.arrayBuffer())
    bytes_list = bytearray(array_buf)
    my_bytes = BytesIO(bytes_list) 
    return Image.open(my_bytes)

def resize(images):
    js.console.log("2",images[0].size)
    for image in images :
        image = image.crop((0, 0, 110, 72))
    js.console.log("3",images[0].size)
    return images

def get_seed():
    seed = ""
    for value in order :
        seed += '{}-{};'.format(str(value), dictionary[str(value)][str(indexDict[str(value)])].replace("/assets/"+value+"/","").replace(".png",""))

    return seed

def change_seed_in_seed_area():
    seed = get_seed()
    textElement = js.document.getElementById("seedArea") 
    textElement.innerText = seed

# Buttons
async def plus(event):
    shape = list(set(event.target.className.split(' ')) & set(order))[0]
    indexDict.update({str(shape): await index_change_operation(dictionary[str(shape)], indexDict[str(shape)], 1)})
    await after_index_change(str(shape))

async def minus(event):
    shape = list(set(event.target.className.split(' ')) & set(order))[0]
    indexDict.update({str(shape): await index_change_operation(dictionary[str(shape)], indexDict[str(shape)], -1)})
    await after_index_change(str(shape))

async def index_change_operation(dictionary, index, operation):
    index += operation
    if operation < 0 and index < 0 :
        index = len(dictionary) - 1

    elif operation > 0 and index >= len(dictionary) :
        index = 0
    
    return index

async def after_index_change(nameIndex):
    displayIndex(nameIndex)
    await draw_image()
    change_seed_in_seed_area()

def copy_seed(ev):
    seed = get_seed()

    navigator.clipboard.writeText(seed)

def dl_preview(ev):
    global previewImage

    metadata = set_metadata()
    previewImage = previewImage.resize((200,100), Image.NEAREST)

    my_stream = BytesIO()
    previewImage.save(my_stream, format="PNG", pnginfo=metadata)
    image_file = File.new([Uint8Array.new(my_stream.getvalue())], "unused_file_name.png", {type: "image/png"})
    url = js.URL.createObjectURL(image_file)

    hidden_a = js.document.createElement('a')
    hidden_a.setAttribute('href', url)
    hidden_a.setAttribute('download', "new_image.png")
    hidden_a.click()

async def randomize(ev):
    for value in order:
        indexDict.update({str(value): random.randrange(len(dictionary[str(value)]))})
        await after_index_change(value)

# display index
def displayIndex(shape):
    textIndexes = js.document.querySelectorAll(".index."+shape) 
    for element in textIndexes:
        element.innerText = dictionary[str(shape)][str(indexDict[str(shape)])].replace("/assets/"+str(shape)+"/","").replace(".png","")

async def init_assets():
    global data
    path = "/assets"
    os.mkdir(path) 

    for info in data:
        path = "/assets/" + info.split('/')[0]

        if not os.path.exists(path):
            os.mkdir(path) 

        url = "https://tortuedebois.github.io" + projectName + "/assets/" + info
        response = await pyfetch(url)

        with open("/assets/" + info, mode="wb") as f:
            f.write(await response.bytes())


    # files = os.listdir('/assets')
    # for file in files:
    #     js.console.log(file)

    #     for f in os.listdir('/assets/' + file):
    #         js.console.log("\t" + f)

def init_data():
    """
    Récupérer toutes les imgs. Selon la nomenclature:
    $path/<folder>/<file>
    """
    # data = []
    # for f in os.listdir(str(Path.cwd()) + "/assets/"):
    #     for file in os.listdir(str(Path.cwd()) + "/assets/" + f + "/"):
    #         data.append(f + "/" + file) #Trouver une alternativeà "append" car risque d'explosion en compléxité (temps ET mémoire)
    # print(data)

    global dictionary, indexDict

    files = os.listdir('/assets')
    for file in files:
        if file not in dictionary :
            dictionary[str(file)] = initDict("/assets/" + file)
            indexDict[str(file)] = 0

async def main():
    await init_assets()
    init_data()
    for value in order :
        displayIndex(value)
    await draw_image()
    change_seed_in_seed_area()

loop = asyncio.get_event_loop()
loop.run_until_complete(main())