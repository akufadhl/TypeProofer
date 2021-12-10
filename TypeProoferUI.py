#from collections import OrderedDict
from drawBot import *
from fontTools import ttLib
import os
import random
from datetime import datetime
import re

Variable([
    #Hamburgefonts
    dict(name="fontsize", ui="Slider",
            args=dict(
                # some vanilla specific
                # setting for a slider
                value=45,
                minValue=8,
                maxValue=100)),
    dict(name="hamburg", ui="CheckBox", args=dict(title="Hamburgefonts", value=True)),

    #Show All Glyphs
    dict(name="fontsize2", ui="Slider",
            args=dict(
                # some vanilla specific
                # setting for a slider
                value=20,
                minValue=8,
                maxValue=100)),
    dict(name="allGlyphs", ui="CheckBox", args=dict(title="ShowAllGlyphs", value=False)),
    #Show Glyphs
    dict(name="fontsize3", ui="Slider",
            args=dict(
                # some vanilla specific
                # setting for a slider
                value=75,
                minValue=8,
                maxValue=120)),
    dict(name="Uppercase", ui="CheckBox"),
    dict(name="Lowercase", ui="CheckBox"),

    #Random Words
    dict(name="fontsize4", ui="Slider",
            args=dict(
                # some vanilla specific
                # setting for a slider
                value=15,
                minValue=8,
                maxValue=120)),
    dict(name="wordCount", ui="EditText", args=dict(text='200')),
    dict(name="RandomWord", ui="CheckBox"),
    
    #Show Random Article
    dict(name="fontsize5", ui="Slider",
            args=dict(
                # some vanilla specific
                # setting for a slider
                value=12,
                minValue=8,
                maxValue=120)),
    dict(name="RandomArticle", ui="CheckBox"),

    dict(name="filename", ui="EditText", args=dict(text='filename')),
    dict(name="savePDF", ui="CheckBox", continuous=False),
], globals())

#Export your fonts to the /Fonts folder
fontPath = "Fonts"
defaultFont = "lib/Fonts/Modal-Regular.otf"

now = datetime.now()
dateNow = now.strftime("%d/%m/%Y %H:%M:%S")

words = 'Words.txt'

uppercase = "ABCDEFGHIJKL\nMNOPQRSTUVWXYZ"
lowercase = uppercase.lower()
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
        elif x[1][2] == None:
            pass
        else:
            #print(x[0])
            italics.append(fontPath + "/" + x[0] + ".otf")
    #res = "\n".join("{} {}".format(x, y) for x, y in zip(uprights, italics))   
    #print(res)    
    weight = []
    for a in weights:
        weight.append(fontPath + "/" + a[0] + ".otf")
    
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
        font(defaultFont)

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

def hamburgefont(FontNames, PageSize, Fontsize, upright, italic=0): 
    x, y, w, h = 65, 100, 710, 430
    if italic != 0:
        path = upright[0]
        fonta = ttLib.TTFont(path)
        name = getName(fonta, 6)

        newPage(PageSize)
        font(defaultFont)
        #FontName
        text(name, (50, 30))
        text("Hamburgefont", (50, height()-30))

        #DateTime
        text(dateNow, (width()-50, 30), align = "right")
        text(f"{str(Fontsize)} point", (width()-50, height()-30), align = "right")

        for fonts in upright:
            paths = fonts
            #Old(top)
            font(paths)
            fontSize(Fontsize)
            textBox("Hamburgefonts1234567890",(x, y, w, h))
            translate(x=0, y=-fontLineHeight())
        
    elif italic != 0:       
        newPage(PageSize)
        font(defaultFont)
        #FontName
        text(name, (50, 30))
        text("Hamburgefont", (50, height()-30))

        #DateTime
        text(dateNow, (width()-50, 30), align = "right")
        text(f"{str(Fontsize)} point", (width()-50, height()-30), align = "right")
        
        for fonts in italic:
            paths = fonts
            #Old(top)
            font(paths)
            fontSize(Fontsize)
            textBox("Hamburgefonts1234567890",(x, y, w, h))
            translate(x=0, y=-fontLineHeight())
            
def showGlyphs(FontNames, PageSize, Fontsize, Letters): 
    x, y, w, h = 65, 100, 710, 430

    for pages in FontNames:
        path = pages
        fonta = ttLib.TTFont(pages)
        name = getName(fonta, 6)
        #New Page
        newPage(PageSize)
        font(defaultFont)

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

def showAllGlyphs(FontNames, PageSize, Fontsize): 
    x, y, w, h = 65, 100, 710, 430

    for pages in FontNames:
        path = pages
        fonta = ttLib.TTFont(pages)
        cmap = fonta['cmap'].getBestCmap().items()
        name = getName(fonta, 6)
        #New Page
        newPage(PageSize)
        font(defaultFont)

        #FontName
        text(name, (50, 30))
        text("All Chars", (50, height()-30))

        #DateTime
        text(dateNow, (width()-50, 30), align = "right")
        text(f"{str(Fontsize)} point", (width()-50, height()-30), align = "right")
        
        txt = FormattedString()
        txt.font(path)
        txt.fontSize(Fontsize)
        for key, values in cmap:
            #print(name)
            txt.append(chr(key) + " ")
        textBox(txt,
                (x, y, w, h), align="left")
                
def showRandomWords(FontNames, PageSize, Fontsize, RandomWord):
    x, y, w, h = 65, 90, 710, 450

    for pages in FontNames: 
        path = pages
        fonta = ttLib.TTFont(pages)
        name = getName(fonta, 6)
        
        newPage(PageSize)
        font(defaultFont)

        text(dateNow, (width()-50, 30), align = "right")
        text(f"{str(Fontsize)} point", (width()-50, height()-30), align = "right")
    
        text("Random Words", (50, height()-30))

        #font(path)
        text(name, (50, 30))

        font(path)
        fontSize(Fontsize)
        textBox(RandomWord,
                (x, y, w, h), align="left")

def showRandomArticle(PageSize, Fontsize, article,upright, italic=0):
    x, y, w, h = 65,75, 710/2.3, 450
    
    if len(italic) != 0:
        for pages, pages2 in zip(upright, italic):
            uprights = pages
            italics = pages2
            print(uprights, italics)
            fonta = ttLib.TTFont(pages)
            name = getName(fonta, 6)
        
            newPage(PageSize)
            font(defaultFont)

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
    else:
        for pages in upright:
            uprights = pages
            #print(uprights)
            fonta = ttLib.TTFont(pages)
            name = getName(fonta, 6)
        
            newPage(PageSize)
            font(defaultFont)

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
                    (x, y, w*2.3, h), align="left")
#save Image   
if hamburg: 
    if fontsize:
        hamburgefont(weight, 'A4Landscape', fontsize, upright, italic)

if allGlyphs:
    if fontsize2:         
        showAllGlyphs(weight, 'A4Landscape', fontsize2)

if fontsize3:
    if Uppercase:
            showGlyphs(weight, 'A4Landscape', fontsize3, uppercase)
    if Lowercase:
        showGlyphs(weight, 'A4Landscape', fontsize3, lowercase)

if RandomWord:
    if fontsize4:
        if wordCount:
                showRandomWords(weight, 'A4Landscape', fontsize4, RandWord(words, int(wordCount)))
            
if fontsize5:
    if RandomArticle:
        showRandomArticle('A4Landscape', fontsize5, article, upright, italic)

if savePDF:
    saveImage(f"{filename}.pdf")
