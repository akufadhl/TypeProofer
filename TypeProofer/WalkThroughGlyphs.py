import os
import random
import re
from datetime import datetime

now = datetime.now()
dateNow = now.strftime("%d/%m/%Y %H:%M:%S")

#you can just use the Masters exports (delete other fonts), and export the original file and add 'Original' after the name eg, MFFlapperOriginal. Then check the regex for original fonts list creation.
folder = '/Users/fadhlschriftlabor/Documents/TypeProofer/Fonts'
#WordLists are courtesy of https://github.com/dwyl/english-words
words = '/Users/fadhlschriftlabor/Documents/TypeProofer/Words.txt'
AllGlyphs = """AÁĂÂÄÀĀĄÅÃÆBCĆČÇĊDÐĎĐEÉĚÊËĖÈĒĘFGĞĢĠHĦIĲÍÎÏİÌĪĮJKĶLĹĽĻĿŁMNŃŇŅÑŊOÓÔÖÒŐŌØÕŒPÞQRŔŘŖSŚŠŞȘẞƏTŦŤŢȚUÚÛÜÙŰŪŲŮVWẂŴẄẀXYÝŶŸỲZŹŽŻaáăâäàāąåãæbcćčçċdðďđeéěêëėèēęəfgğģġhħiıíîïìĳīįjȷkķlĺľļŀłmnńňņñŋoóôöòőōøõœpþqrŕřŗsśšşșßtŧťţțuúûüùűūųůvwẃŵẅẁxyýŷÿỳzźžżªºΔΩμπ0123456789⓿❶❷❸❹❺❻❼❽❾⓪①②③④⑤⑥⑦⑧⑨ ⁰¹²³⁴⁵⁶⁷⁸⁹⁄½⅓⅔¼¾⅛⅜⅝⅞.,:;…!¡?¿·•*⁂#․//\⁑-­–—_ (){}[] ‚„“”‘’«»‹›"'ƒ☺@&¶§©®℗™°|¦†‡℮№℠₿¢¤$€£¥+−×÷=≠><≥≤±≈~¬^∞∅∫∏∑√µ∂%‰↑↗→↘↓↙←↖↔↕↰↱↲↳●○◊■□▲△"""
Letters = "AÆBCDÐEFGHIJKLMNOŒ\nPÞQRSẞƏTUVWXYZ"
Figures = "0123456789"
Symbols = "ƒ☺@&¶§©®℗™°|¦†‡℮℠¤£+−×÷=<≤±~¬^∞∅∫∏∑√∂"
        
def fontName(folder):
    names = []    
    for name in os.listdir(folder):
        if os.path.isfile(os.path.join(folder, name)):
            if (".otf" in name) and ("Original" not in name):
                names.append(name)  
    return names

FontNames = fontName(folder)
OriginalFonts = []

#Make a list of Original Fonts
for a in FontNames:
    #print(a[:9])
    OriginalFonts.append(a[:9]+'Original'+a[9:])

#Generating The Old and New Comparison
#Should be a separate function that takes a predifined param, such as lowercase, uppercase, figures, symbols.    
for pages in FontNames:
    for glyphs in AllGlyphs:
        path = '/Users/fadhlschriftlabor/Documents/TypeProofer/Fonts/{f}'.format(f = pages)
    
        newPage(500, 500)
        print(glyphs)
    
        #FontName
        text(pages, (50, height()-50))
    
        #DateTime
        text(dateNow, (50, 50))
    
    
        #New(Bottom)
        font(path)
        fontSize(200)
        textBox(glyphs,
                (100, 100, 300, 300), align="center")

saveImage("~/Desktop/MFFlapper Upright.gif")