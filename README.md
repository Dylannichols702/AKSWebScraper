# AKSWebScraper

## Introduction
The purpose of this program is to make finding and downloading AKS product images more 
efficient.

This program will:
- Find the correct image or set of images for products given a search criteria.
- Download the correct image and place in the folder you choose.
- Show which products the tool couldn't find on the site.

## How to Use

### Setting a File Path
To select which path you'd like the images to be saved in, click the "Select Path" button in the top right corner of the program window. From here, select the folder you'd like to store the images in and click "Select Folder".

### Adding and Removing Products to be Searched
To add or remove products to the search, click the "Edit Products" button on the left side of the program window. In the text box of the pop-up window, add the 8-digit generic bulk product number (e.g. 19301234) of your first product and hit "Enter". Continue this process for the rest of the products you'd like to search for. Your product list should look like the following:

```
19301234
19305546
19313514
...
```

You can also search for products by product number by selecting "Product Number" in the "Product Identifier Type" dropdown of the "Options" menu. For example, if you wanted to look for the aforementioned elements via search, your product list should like this sample:

```
1234
5546
13514
...
```

Once you've entered the identifier for each product, click the "Done" button at the bottom of the pop-up window.

### Scanning for Products
At this point, press the "Scrape" button on the bottom of the program window to start the search. During this process, each product's number will appear in the text window in the center of the screen, as well as whether or not the search yielded an image download. When the search is complete, a pop-up window will appear either stating complete success in every download or, more likely, listing all of the products the search couldn't find. Click the "OK" button to dismiss this window.
