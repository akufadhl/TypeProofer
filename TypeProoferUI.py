#from collections import OrderedDict
from drawBot import *
from fontTools import ttLib
import os
import random
from datetime import datetime
import re

#add your font Path here
fontPath = "Fonts"

now = datetime.now()
dateNow = now.strftime("%d/%m/%Y %H:%M:%S")

words = '/Users/fadhlschriftlabor/Repositories/TypeProofer/Words.txt'

Uppercase = "ABCDEFGHIJKL\nMNOPQRSTUVWXYZ"

with open("article.txt", "r", encoding="utf-8") as article:
    #articles = article.read()
    article = re.sub(r'\[\d+\]', ' ', article.read())

#Get Random Words
def RandWord(words, amounts):
    RandomWords = " "
    with open(words) as word_file:
        words = word_file.read().split()
        random_word = random.sample(words, amounts)
    return (RandomWords.join(random_word))

randomWord = str(RandWord(words, 700))

#Get font "name" table
def getName(font, ID, platformID=3, platEncID=1):
    name = str(font['name'].getName(ID, platformID,platEncID))
    return name
    
#Read for font files in folder
def fontName(folder):
    names = []    
    for name in os.listdir(folder):
        if os.path.isfile(os.path.join(folder, name)):
            if (".otf" in name) and ("Original" not in name):
                names.append(fontPath + "/" +name)
    #print(names)  
    return names


#batch calling font = ttLib.TTFont(fontPath)
def TTObject(fontList):
    fontAvail = []
    for fonta in fontList:
        fontAvail.append(ttLib.TTFont(fonta))
                
    return fontAvail

path = fontName(fontPath)  
fonts = TTObject(path)
#print(fonts)

def sortFont(fonts):
    uprights = []
    italics = []
    
    weightClass = {}
    for font in fonts:
        name = getName(font, 6)
        weight = font['OS/2'].usWeightClass
        width = font['OS/2'].usWidthClass
        italic = int(font['post'].italicAngle)
    
        weightClass[name] = width, weight, italic
    
    weights = sorted(weightClass.items(), key=lambda x:(x[1],x[1][0]))
    
    for x in weights:
        #print(x[0],int(x[1][2]))
        if x[1][2] >= 0:
            #print(x[0])
            uprights.append(fontPath + "/" + x[0] + ".otf")
        else:
            #print(x[0])
            italics.append(fontPath + "/" + x[0] + ".otf")
    #res = "\n".join("{} {}".format(x, y) for x, y in zip(uprights, italics))   
    #print(res)    
    weight = []
    for a in weights:
        weight.append(fontPath + "/" + a[0] + ".otf")
    
    #print(weight)
    return weight, uprights, italics

fontList = sortFont(fonts)
weight = fontList[0]
upright = fontList[1]
italic = fontList[2]

#Font style Names using TTFont "name" Table
designerName = getName(fonts[0], 9)
familyName = getName(fonts[0], 16) #Basic Family Name
manufacturer = getName(fonts[0], 8)
    
regular = weight[0]
slanted = weight[2]

#Font Feature

notFeature = ['aalt', 'case', 'ccmp', 'dnom', 'kern', 'mark', 'mkmk', 'numr', 'ordn', 'pnum', 'sinf', 'subs', 'sups']
#Feat = listOpenTypeFeatures(regular)
#Feature = list(filter(lambda a: a not in notFeature, Feat))

def compareNewOld(FontNames, PageSize, Fontsize, Letters): 

    for pages in FontNames:
        path = pages
        OriginalFont = re.sub(r'(-)', r'Original\1', path)

        fonta = ttLib.TTFont(pages)
        name = getName(fonta, 6)
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
        path = pages
        fonta = ttLib.TTFont(pages)
        name = getName(fonta, 6)
        #New Page
        newPage(PageSize)

        #FontName
        text(name, (50, 30))

        #DateTime
        text(dateNow, (width()-50, 30), align = "right")
        text(f"{str(Fontsize)} point", (width()-50, height()-30), align = "right")


        #Old/New
        if Letters == Uppercase:
            text("Uppercase Preview", (50, height()-30))
        elif Letters == Lowercase:
            text("Lowercase Preview", (50, height()-30))

        #Old(top)
        font(path)
        fontSize(Fontsize)
        textBox(Letters,(x, y, w, h), align="center")

def showRandomWords(FontNames, PageSize, Fontsize, RandomWord):
    x, y, w, h = 65, 90, 710, 450

    for pages in FontNames: 
        path = pages
        fonta = ttLib.TTFont(pages)
        name = getName(fonta, 6)
        
        newPage(PageSize)

        text(dateNow, (width()-50, 30), align = "right")
        text(f"{str(Fontsize)} point", (width()-50, height()-30), align = "right")
    
        text("Random Words", (50, height()-30))

        #font(path)
        text(name, (50, 30))

        font(path)
        fontSize(Fontsize)
        textBox(RandomWord,

                (x, y, w, h), align="left")

def showRandomArticle(italic=None, upright, PageSize, Fontsize, article):
    x, y, w, h = 65, 90, 710/2.3, 450
    
    for pages, pages2 in zip(upright, italic):
        uprights = pages
        italics = pages2
        print(uprights, italics)
        fonta = ttLib.TTFont(pages)
        name = getName(fonta, 6)
        
        newPage(PageSize)

        text(dateNow, (width()-50, 30), align = "right")
        text(f"{str(Fontsize)} point", (width()-50, height()-30), align = "right")
    
        text("Random Article", (50, height()-30))

        #font(uprights) #standardFont
        text(name, (50, 30))
        
        #txt = FormattedString()
        #print(txt)
        font(uprights)
        fontSize(Fontsize)
        #txt.append(article)
        textBox(article,
                (x, y, w, h), align="left")
        translate(x=(w*2)-w/1.3, y=0)
        font(italics)                
        textBox(article,
                (x, y, w, h), align="left")
                    
showGlyphs(weight, 'A4Landscape', 75, Uppercase)
showRandomWords(weight, 'A4Landscape', 15, randomWord)
showRandomArticle(italic, upright, 'A4Landscape', 12, article)
#save Image
#saveImage("~/Desktop/PDFSpecimen.pdf")