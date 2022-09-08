from PIL import Image
from IPython.display import display
import random
import json
import os
import re
import shutil
from utility.nftstorage import NftStorage


def create_image(attributes, images_attributes):
    new_image = {}

    for i in attributes:
        new_image[i] = re.sub(".png", "", (random.choices(attributes[i])[0]))

    if new_image in images_attributes:
        return create_image(attributes, images_attributes)
    else:
        return new_image
    
    # Returns true if all images are unique


def all_images_unique(all_images):
    seen = list()
    return not any(i in seen or seen.append(i) for i in all_images)


def create_attributes(nb_images):
    attributes = {}
    images_attributes = []
    # liste tous les attributs dans un dictionnaire
    for i in files:
        if not (re.search("\.", i)):
            attributes[i] = os.listdir("./assets/" + str(i))

    #gênère toutes les images dans un dictionnaire 
    
    for i in range(int(nb_images)):
        images_attributes.append(create_image(attributes, images_attributes))
        
    #on test si toutes les images sont uniques
    if not (all_images_unique(images_attributes)):
        print("all images are not uniques")
        create_attributes()
    else : 
        print("toutes les images sont uniques")
        
    return images_attributes


def create_images(all_images):
    print("création des images")
    tokenId = 0

    # création du fichier image
    shutil.rmtree(f'./images')
    os.mkdir(f'./images')
    
    for item in all_images:
        attribute_img = []
        com = []

        for i in item:
            attribute_img.append(Image.open(
                f'./assets/' + str(i) + '/' + str(item[i]) + '.png').convert('RGBA'))
            # print('./assets/' + str(i) + '/' + str(item[i]) + '.png')
            # print(Image.open(f'./assets/' + str(i) + '/' + str(item[i]) + '.png').convert('RGBA'))

        for i in range(len(attribute_img)-1):
            # #Create each composite
            if (i == 0):
                com.append((Image.alpha_composite(
                    attribute_img[0], attribute_img[1])))
            else:
                com.append(Image.alpha_composite(com[i-1], attribute_img[i+1]))
        # #Convert to RGB
        rgb_im = com[-1].convert('RGB')
        file_name = str(tokenId) + ".png"
        rgb_im.save("./images/" + file_name)
        print("./images/" + file_name)
        tokenId += 1

def upload_images():
    print("upload des images")
    imagePathList = []

    for i in os.listdir("./images/"):
        imagePathList.append("./images/" + i)

    cid = c.upload(imagePathList, 'image/' + IMAGE_TYPE)
    return cid

def metadatas_create():
    
    shutil.rmtree(f'./metadata')
    os.mkdir(f'./metadata')
    
    PROJECT_NAME = input ("entrez le titre de la collection : \n")
    ROYALTIES_AMOUNT = 10
    DESCRIPTION = input("entrez la description de la collection : \n")
    IMAGES_BASE_URL = "ipfs://" + str(upload_images()) + "/"
    
    print("images link : " + IMAGES_BASE_URL)

    # création des attributs puis des métadatas
    # upload des fichiers metadatas
    print("créations des métadatas")
    for i in range(int(nb_images)):
        ATTRIBUTES = []
        for j in all_images[i]:
            ATTRIBUTES.append({"trait_type": j, "value": all_images[i][j]})

        token = {
            "image": IMAGES_BASE_URL + str(i),
            "tokenId": i,
            "name": PROJECT_NAME + ' #' + str(i) + "/" + str(nb_images),
            "description": DESCRIPTION,
            "attributes": ATTRIBUTES,
            "edition_total": nb_images,
            "royalty_amount": ROYALTIES_AMOUNT,
        }

        jsonfile = str("./metadata/" + str(i) + ".json")
        with open(jsonfile, "w") as outfile:
            json.dump(token, outfile, indent=4)

        meta_file_list.append(jsonfile)

def upload_metadata():
    #metadata upload
    print("upload des metadatas")
        
    cid = c.upload(meta_file_list, 'application/json')
    print("images link : " + "ipfs://" + cid + "/")
        
        
    with open("metapath.json", "w") as metapath:
        for i in range(len(meta_file_list)):
            
            json.dump("ipfs://" + cid + "/" + meta_file_list[i].split('/')[2], metapath, indent=4)





files = os.listdir("./assets/")

meta_file_list = []
IMAGE_TYPE = "png"
NFTSTORAGE_API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJkaWQ6ZXRocjoweGUzZGU2RjRjZTdlYTdEZERiOWJFMGVCMTIzMjNDOENDODViNDQxNzUiLCJpc3MiOiJuZnQtc3RvcmFnZSIsImlhdCI6MTY0Njg1OTM0ODg3MywibmFtZSI6InRlc3QifQ.oqGDpxt1uHvOcFKCUXaYhxuRUEG6VJDLjuFtt77C90I"
c = NftStorage(NFTSTORAGE_API_KEY)
nstorage = {} 

# calcul du nombre d'images a générer
nb_max = 1

for i in files:
    if not (re.search("\.", i)):
        tab = os.listdir("./assets/" + str(i))
        nb_max *= len(tab)
print("nombre maximum de fichier pouvant être généré : " + str(nb_max))
# nft metadatas:

nb_images = input("nombre d'images a générer:\n")

all_images = create_attributes(nb_images)

create_images(all_images)

if(input("voulez vous créer les metadatas: \n-oui : y\n-no : n\n") == "y"):

    metadatas_create()
    upload_metadata()

