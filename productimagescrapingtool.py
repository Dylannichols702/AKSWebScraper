# This script scrapes a specified product image from the AKS website
# and copies it to a specified file destination
# Author: Dylan Nichols

from urllib.request import FancyURLopener
from urllib.request import urlopen
from bs4 import BeautifulSoup
from termcolor import colored
import requests
import shutil
import os

# Initializes colored terminal text
os.system('color')

# Creates a user agent to authorize access to the page
class MyOpener(FancyURLopener):
    version = 'New User-Agent'

# Gets bulk number and file path information from the user
numProducts = input("Enter the number of products to get images for: ")
while not numProducts.isnumeric() or int(numProducts) <= 0:
    numProducts = input("Please enter a  positive whole number of products to get images for: ")
numProducts = int(numProducts)
products = []
print("Enter the Generic(Bulk) product number(s): ")
for product in range(numProducts):
    productNum = input()
    while not productNum.isnumeric():
        print("Please enter the 8 - digit bulk product number.")
        productNum = input()
    products.append(int(productNum))
fileDest = ""
while not os.path.exists(fileDest):
    fileDest = input("Enter the file path of where the image(s) should be saved: ")
    if not os.path.exists(fileDest):
        print("Please input a valid file path.")

# Initializes the list of products the scraper was unable to find
productsWithFindErr = []

for product in range(numProducts): 
    # Derives the product ID and URL from the page
    currProduct = products[product]
    productID = str(currProduct)[3:8]
    url = "https://www.americankeysupply.com/product/" + productID

    # Attempts to open the specified page
    myOpener = MyOpener()
    page = myOpener.open(url)

    # Prints the ID of the product
    print(str(currProduct) + ": ", end = " ")

    # Searches the page for the link to the product image,
    # goes to the next product if there was an issue
    # decoding the page.
    if page.closed == False:
        html = page.read().decode("utf-8")
        soup = BeautifulSoup(html, "html.parser")
        img = soup.main.img
        imgLink = img["data-src"]
    else:
        print(colored("Error","red"))
        productsWithFindErr.append(currProduct)
        continue

    # Prepares the file to be placed at the correct destination
    # with the correct name
    fileName = imgLink.split("/")[-1]
    bulkNumberName = str(currProduct) + ".jpg"
    bulkNumberDest = fileDest + "/" + bulkNumberName

    # Gets the image content from the supplied URL
    r = requests.get(imgLink, stream = True)
    r.raw.decode_content = True

    # Copies the file to the correct destination
    with open(bulkNumberDest,'wb') as f:
        shutil.copyfileobj(r.raw, f)

    # Prints if the file copy was a success to the user
    print(colored("Success", "green"))

# Determines whether there were issues finding any of requested item images
if(len(productsWithFindErr) > 0):
    print("\nThere were errors finding the images for these products:")
else:
    print("\nAll images have been successfully downloaded! Yay!")
        
# Prints unfound images if there are any
for product in range(len(productsWithFindErr)):
    print(productsWithFindErr[product])

# Ensures window won't close immediately upon finishing the task
input()
