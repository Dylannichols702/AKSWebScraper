# This script scrapes a specified product image from the AKS website
# and copies it to a specified file destination
# Author: Dylan Nichols

# Imports necessary modules
from urllib.request import FancyURLopener
from urllib.request import urlopen
from bs4 import BeautifulSoup
from termcolor import colored
from tkinter import messagebox
from tkinter import filedialog
import requests
import shutil
import os
import tkinter

# Defines default settings
products = []
fileDest = ""
userAgentName = "New User-Agent"

# Initializes colored terminal text
os.system('color')

# Creates a user agent to authorize access to the page
class MyOpener(FancyURLopener):
    version = userAgentName

# Inserts a piece of text into a read-only text box
def writeToTextBox(tb, text):
    tb.configure(state = "normal")
    tb.insert(tkinter.INSERT, text)
    tb.configure(state = "disabled")

# Clears a read-only text box
def clearTextBox(tb):
    tb.configure(state = "normal")
    tb.delete("1.0", "end")
    tb.configure(state = "disabled")

# Defines template for creating a new window
def createWindow(root, title):    
    w = tkinter.Toplevel(root)
    w.resizable(False, False)
    w.title(title)
    
    return w
  
# Scrapes the images from the internet and drops them into
# the specified file location
def scrapeImages(np, p, fp):
    # Initializes the list of products the scraper was unable to find
    productsWithFindErr = []
    statusString = ""
    global statusText
    global root

    clearTextBox(statusText)
    
    for product in range(np): 
        # Derives the product ID and URL from the page
        currProduct = p[product]
        productID = str(currProduct)[3:8]
        url = "https://www.americankeysupply.com/product/" + productID

        # Writes the current product to the status text box
        productString = str(currProduct) + ": "
        writeToTextBox(statusText, productString)
        root.update()

        # Attempts to open the specified page
        myOpener = MyOpener()
        page = myOpener.open(url)

        # Prints the ID of the product
        statusString = statusString + str(currProduct) + ": "

        # Searches the page for the link to the product image,
        # goes to the next product if there was an issue
        # decoding the page.
        if page.closed == False:
            html = page.read().decode("utf-8")
            soup = BeautifulSoup(html, "html.parser")
            img = soup.main.img
            imgLink = img["data-src"]
        else:
            writeToTextBox(statusText, "Error\n")
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
        writeToTextBox(statusText, "Success\n")
        statusText.yview_pickplace("end")
        root.update()

    # Find unfound images if there are any
    unfoundProductsString = "There were errors finding the images for these products:\n\n"
    for product in range(len(productsWithFindErr)):
        unfoundProductsString = unfoundProductsString + str(productsWithFindErr[product]) + "\n"
    
    # Determines whether there were issues finding any of requested item images
    if(len(productsWithFindErr) > 0):
        tkinter.messagebox.showinfo(title = "Search Errors",
                                    message = unfoundProductsString)
    else:
        tkinter.messagebox.showinfo(title = "Search Success",
                                    message = "All images have been successfully downloaded! Yay!")
        
# Returns a string of the list of products
def getProductList():
    ans = ""
    for product in range(len(products)):
        ans = ans + str(products[product]) + "\n"
    return ans

# Clears the product list
def clearProductList():
    products.clear()

# Behavior for when the user presses the done button on the edit products window
def onAddWindowDoneButtonClick(topLevel, textBox):
    textFromBox = textBox.get("1.0", tkinter.END).rstrip("\n")
    clearProductList()
    for line in textFromBox.splitlines():
        if line.isnumeric():
            products.append(int(line));
    topLevel.destroy()

# Behavior for when the user presses the save button on the options window
def onOptionsWindowDoneButtonClick(topLevel, textBox):
    textFromBox = textBox.get("1.0", tkinter.END).rstrip("\n")
    global userAgentName
    userAgentName = textFromBox
    topLevel.destroy()

# Scrapes images from the site when the scrape button is clicked
def onScrapeButtonClick(filePath):
    global fileDest
    fileDest = filePath.get("1.0", tkinter.END).rstrip("\n")
    if not os.path.exists(fileDest):
        messagebox.showerror(title = "Error", message = "Please input a valid file path.")
        return
    scrapeImages(len(products), products, fileDest)

def onSetPathButtonClick(textBox):
    textFromBox = textBox.get("1.0", tkinter.END).rstrip("\n")
    global fileDest
    fileDest = textFromBox

# Defines behavior for opening a new instance of the options window
def openOptionsWindow():
    optionsWindow = createWindow(root, "Options")
    tkinter.Label(optionsWindow,
                  text = "User-Agent:",
                  justify = tkinter.RIGHT).grid(row = 0, column = 0)
    userAgentTextBox = tkinter.Text(optionsWindow,
                                    height = 1,
                                    wrap = "none")
    userAgentTextBox.insert(tkinter.INSERT,
                            userAgentName)
    userAgentTextBox.grid(row = 0,
                          column = 1,
                          padx = 10,
                          pady = 10)
    tkinter.Button(optionsWindow,
                   text = "Save",
                   command = lambda: onOptionsWindowDoneButtonClick(optionsWindow, userAgentTextBox)).grid(row = 1,
                                                                                                           column = 1,
                                                                                                           pady = (0,10))

# Defines behavior for openning a new instance of the adding products window
def openAddWindow():
    addWindow = createWindow(root, "Edit Products")
    tkinter.Label(addWindow,
                  text = "Edit Products:",
                  height = 1).grid(row = 0, column = 0)
    productText = tkinter.Text(addWindow,
                               height = 10)
    productText.insert(tkinter.INSERT,
                       getProductList())
    productText.grid(row = 1,
                     column = 0,
                     padx = 10,
                     pady = 10)
    tkinter.Button(addWindow,
                   text = "Done",
                   command = lambda: onAddWindowDoneButtonClick(addWindow, productText)).grid(row = 2,
                                                                                              column = 0,
                                                                                              pady = (0,10))

# Defines behavior for when the select path button is clicked
def onSelectPathButtonClick(text):
    chosenPath = tkinter.filedialog.askdirectory()
    clearTextBox(text)
    writeToTextBox(text, chosenPath)

# Declares the window the program will live in
root = tkinter.Tk()
# Fixes the dimensions of the window
root.resizable(False, False)
# Changes the title of the window
root.title("AKS Image Scraping Tool")

# Places all of the elements in the main window
tkinter.Label(root,
              text = "Path:",
              justify = tkinter.RIGHT,
              wrap = None).grid(row = 0, column = 0, pady = (10,0))
tkinter.Label(root,
              text = "Status:").grid(row = 1, column = 1, pady = (10,0))
filePathText = tkinter.Text(root,
                            height = 1,
                            state = "disabled")
filePathText.insert(tkinter.INSERT,
                    fileDest)
filePathText.grid(row = 0,
                  column = 1,
                  padx = 10,
                  pady = (10,0))
statusText = tkinter.Text(root,
                          height = 10,
                          state = "disabled")
statusText.grid(row = 2,
                column = 1,
                padx = 10,
                pady = 10,
                rowspan = 3)
tkinter.Button(root,
               text = "Options",
               width = 15,
               command = lambda: openOptionsWindow()).grid(row = 2,
                                                           column = 0,
                                                           padx = (10, 0),
                                                           pady = 10)
tkinter.Button(root,
               text = "Edit Products",
               width = 15,
               command = lambda: openAddWindow()).grid(row = 3,
                                                       column = 0,
                                                       padx = (10, 0),
                                                       pady = 10)
tkinter.Button(root,
               text = "Scrape",
               width = 15,
               command = lambda: onScrapeButtonClick(filePathText)).grid(row = 4,
                                                                         column = 0,
                                                                         padx = (10, 0),
                                                                         pady = 10)
tkinter.Button(root,
               text = "Select Path",
               width = 10,
               command = lambda: onSelectPathButtonClick(filePathText)).grid(row = 0, column = 2, padx = (0, 10), pady = (10, 0))

# Instantiates the window
root.mainloop()
