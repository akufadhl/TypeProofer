import AppKit
from drawBot import *
from vanilla import *
import os
import random
import re
from datetime import datetime

Variable([
    dict(name="folder", ui="EditText", args=dict(text='/Users/fadhlschriftlabor/Repositories/TypeProofer/Fonts')),
    dict(name="CompareUC", ui="CheckBox", args=dict(value=False)),
    dict(name="CompareLC", ui="CheckBox", args=dict(value=False)),
    dict(name="fontsize", ui="Slider", args=dict(value=45, minValue=6, maxValue=200)),
    dict(name="ShowUC", ui="CheckBox", args=dict(value=True)),
    dict(name="ShowLC", ui="CheckBox", args=dict(value=True)),
    dict(name="save", ui="Button"),
], globals())
    
now = datetime.now()
dateNow = now.strftime("%d/%m/%Y %H:%M:%S")

    #you can just use the Masters exports (delete other fonts), and export the original file and add 'Original' after the name eg, MFFlapperOriginal. Then check the regex for original fonts list creation.
    #folder = '/Users/fadhlschriftlabor/Repositories/TypeProofer/Fonts'
    #WordLists are courtesy of https://github.com/dwyl/english-words
    
words = '/Users/fadhlschriftlabor/Repositories/TypeProofer/Words.txt'
Uppercase = "ABCDEFGHIJKL\nMNOPQRSTUVWXYZ"
Lowercase = Uppercase.lower()
Figures = "0123456789"
Symbols = "ƒ☺@&¶§©®℗™°|¦†‡℮℠¤£+−×÷=<≤±~¬^∞∅∫∏∑√∂"
Puncts = """.,:;…!¡?¿·•*⁂․//\⁑‥#-­–—_(){}[]‚„“”‘’«»‹›"'"""

def fontName(folder):
    names = []    
    for name in os.listdir(folder):
        if os.path.isfile(os.path.join(folder, name)):
            if (".otf" in name) and ("Original" not in name):
                names.append(name)  
    return names

def RandWord(words, amounts):
    RandomWords = " "
    with open(words) as word_file:
        words = word_file.read().split()
        random_word = random.sample(words, amounts)
    return (RandomWords.join(random_word))


#Change the number value for numbers lists,    
RandomWord = str(RandWord(words, 700))
FontNames = fontName(folder)


    #Generating The Old and New Comparison
    #Should be a separate function that takes a predifined param, such as lowercase, uppercase, figures, symbols.
def CompareNewOld(FontNames, PageSize, Fontsize, Letters): 

    for pages in FontNames:
        path = folder + '/{f}'.format(f = pages)
        OriginalFont = re.sub(r'(-)', r'Original\1', path)

        #New Page
        newPage(PageSize)

        #FontName
        text(pages, (50, height()-50))

        #DateTime
        text(dateNow, (50, 50))

        #Old/New
        text("Old(top), New(bottom)", (width()-50, 50), align = "right")

        #New(Bottom)
        font(path)
        fontSize(Fontsize)
        textBox(Letters,
                (80, height()-550, 700, 250), align="center")

        #Old(top)
        font(OriginalFont)
        fontSize(Fontsize)
        textBox(Letters,
                (80, height()-350, 700, 250), align="center")

def showGlyphs(FontNames, PageSize, Fontsize, Letters): 
    x, y, w, h = 65, 100, 710, 400

    for pages in FontNames:
        path = folder + '/{f}'.format(f = pages)
        OriginalFont = re.sub(r'(-)', r'Original\1', path)

        #New Page
        newPage(PageSize)

        #FontName
        text(pages, (50, height()-50))

        #DateTime
        text(dateNow, (50, 50))

        #Old/New
        text("Old(top), New(bottom)", (width()-50, 50), align = "right")

        #Old(top)
        font(path)
        fontSize(Fontsize)
        textBox(Letters,(x, y, w, h), align="center")
                    
#Generating random words, should also be a separate function that takes a parameter like uppercase, fontSize, howMuch words (currently using a predefined var 'RandomWords')   
def RandomWords(FontNames, PageSize, FontSize, RandomWord):
    for pages in FontNames: 
        path = folder +'/{f}'.format(f = pages)
   
        newPage(PageSize)

        text(dateNow, (width()-50, 30), align = "right")

        font(path)
        text(pages, (50, 30))

        font(path)
        fontSize(FontSize)
        textBox(RandomWord,

                (150, 150, width()-250, height()-250), align="left")

class PDFSpecimen:
    if CompareUC:   
        CompareNewOld(FontNames, 'A4Landscape', 45, Uppercase)
    if CompareLC:
        CompareNewOld(FontNames, 'A4Landscape', 45, Lowercase)
    if fontsize:
        if ShowUC:
            showGlyphs(FontNames, 'A4Landscape', fontsize, Uppercase)
        if ShowLC:
            showGlyphs(FontNames, 'A4Landscape', fontsize, Lowercase)
    #RandomWords(FontNames, 'A4Landscape', 20, RandomWord.lower())
    #RandomWords(FontNames, 'A4Landscape', 20, RandomWord.upper())
    if save:
        fontname = "MFSansPlomb"
        saveImage(f"~/Desktop/{fontname}.pdf")

PDFSpecimen()