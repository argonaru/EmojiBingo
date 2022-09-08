import numpy
import cv2
import tkinter 
from PIL import Image, ImageTk
import math
import json
from random import randint
from os import remove,rmdir,mkdir,chmod
from uuid import uuid4
from shutil import rmtree
import random

imgSheet = cv2.imread("resources/tilesheet.png", cv2.IMREAD_UNCHANGED)
iconSpoiler = cv2.imread("resources/emojiDEFAULT.png", cv2.IMREAD_UNCHANGED)
definitionList = json.load(open('resources/definitions.json'))
#for i in definitionList['0']:
#    print(i['name'])
class GameConstruct:

    def __init__(self, master):


        self.EmojiListState = [True for x in range(75)]
        self.CurrentEmoji = -99
        self.RoundNumber = 0

        self.master = master
        master.title("BINGO")
        master.geometry("440x688")
        master.resizable(False, False)

        self.Header = tkinter.Canvas(master, borderwidth=5, highlightthickness=0, height=10, width=220, bg='#36393f')
        self.Header.pack(side="top", anchor="nw")

        
        self.Button3Image = ImageTk.PhotoImage(Image.open("resources/sprite3.png").resize((40, 40),Image.Resampling.LANCZOS))
        self.PrintButton = tkinter.Button(self.Header,  image=self.Button3Image, command=lambda: self.PrintNewCards(), width=40, height=40, default=tkinter.ACTIVE, borderwidth=0)
        self.PrintButton.pack(side="top", anchor="ne", padx=(390,8), pady=(5, 5))
        
        self.MainContainer = tkinter.Frame(master, borderwidth=5, highlightthickness=0, height=600, width=220, bg='#36393f')
        self.MainContainer.pack(side="top", anchor="nw")

        

        self.MainLeftFrame = tkinter.Frame(self.MainContainer, borderwidth=0, highlightthickness=0, height=600, width=100, bg='#36393f')
        self.MainLeftFrame.pack(side="left", anchor="nw", padx=(15,0))

        self.MainRightFrame = tkinter.Frame(self.MainContainer, borderwidth=0, highlightthickness=0, height=600, width=100, bg='#36393f')
        self.MainRightFrame.pack(side="left", anchor="nw", padx = (50,13))

        self.EmojiListFrame = tkinter.Frame(self.MainLeftFrame, borderwidth=0, highlightthickness=0, height=600, width=100, bg='#36393f')
        self.EmojiListFrame.pack(side="top", anchor="nw")

        self.RowFrame = [] 
        
        self.ImageList = [[] for i in range(5)]
        self.EmojiLabelList = [[] for i in range(5)]
        

        for i in range(5):
            self.RowFrame.append(tkinter.Frame(self.EmojiListFrame, width=30, height=500))
            self.RowFrame[i].pack(side="left", anchor="nw")
            for j in range(15):
                num = i * 15 + j
                newYOrigin = (num%10) * 75
                newXOrigin = math.floor(num/10) * 75
                imgh = imgSheet[newXOrigin:newXOrigin+75, newYOrigin:newYOrigin+75]
                bg = numpy.zeros((75, 75, 4), numpy.uint8)
                bg[:] = (63,57,54,255)
                imgh = self.MergeImages(imgh, bg)
                b,g,r,a = cv2.split(cv2.resize(imgh, (30,30)))
                image= ImageTk.PhotoImage(image=Image.fromarray(cv2.merge((r,g,b))))
    
                label = tkinter.Label(self.RowFrame[i], image=image)
                label.pack(side="top", anchor="nw", fill='both')
                label.bind('<Button-1>', lambda event, number = num : self.UpdateIconByNumber(number), add='+')
                label.bind('<Motion>', lambda event, number = num : self.ReplaceMainImage(number), add='+')
                label.bind('<Leave>', lambda event, number = num : self.ResetMainImage(), add='+')
                self.ImageList[i].append(image)
                self.EmojiLabelList[i].append(label)

        self.EmojiLabelLeft = tkinter.Label(self.MainLeftFrame, text="Round 0")
        self.EmojiLabelLeft.pack(side="top", anchor="nw", ipadx=30, ipady=2, pady=5)


        self.MainImageResource = ImageTk.PhotoImage(Image.open("resources/emojiDEFAULT.png").resize((176, 176),Image.Resampling.LANCZOS))
        self.MainImageLabel = tkinter.Label(self.MainRightFrame, image=self.MainImageResource)
        self.MainImageLabel.pack(side="top", anchor="nw", pady= (50, 10))

        self.EmojiLabelRight = tkinter.Label(self.MainRightFrame, text="", bg='#2f3136', fg='#ffffff')
        self.EmojiLabelRight.pack(side="top", anchor="center", ipadx=30, ipady=2, fill= 'x')
        self.Button0Image = ImageTk.PhotoImage(Image.open("resources/sprite0.png").resize((180, 40),Image.Resampling.LANCZOS))
        self.Button0 = tkinter.Button(self.MainRightFrame,command=lambda: self.ResetAll(), text="", width=180, height=40, default=tkinter.ACTIVE, borderwidth=0)
        self.Button0.config(image=self.Button0Image)
        self.Button0.pack(side="top", anchor="nw", pady=(175,10))
        

        

        self.Button1Image = ImageTk.PhotoImage(Image.open("resources/sprite1.png").resize((180, 50),Image.Resampling.LANCZOS))
        self.Button1 = tkinter.Button(self.MainRightFrame, image=self.Button1Image , command=lambda: self.ChooseNewRandomNumber(), text="", width=180, height=50, default=tkinter.ACTIVE, borderwidth=0)
        self.Button1.pack(side="top", anchor="nw")

        self.Footer = tkinter.Label(master, text = "\n-------------------------------------------------------------------------------\nFree for any use,\n @aru#8982 or at https://github.com/argonaru\nOr argonaru@gmail.com\n\n", bg='#36393f', fg='#ffffff', width=62, height=5)
        self.Footer.pack(side="top", anchor="nw")
        self.ResetMainImage()
        
    def UpdateIconByNumber(self, num, event=None):
        newYOrigin = (num%15)
        newXOrigin = math.floor(num/15)
        newYOrigin0 = (num%10) * 75
        newXOrigin0 = math.floor(num/10) * 75
        newimage = imgSheet[newXOrigin0:newXOrigin0+75, newYOrigin0:newYOrigin0+75]
        imgh = cv2.resize(imgSheet[newXOrigin0:newXOrigin0+75, newYOrigin0:newYOrigin0+75], (30,30))
        bg = numpy.zeros((30, 30, 4), numpy.uint8)
        bg[:] = (63,57,54,255)
        imgh = self.MergeImages(imgh, bg)
        if(self.EmojiListState[num]): 
            overlay = cv2.resize(iconSpoiler, (30,30))
            imgh = self.MergeImages(overlay, imgh)

        b,g,r,a = cv2.split(imgh)
        imgg = ImageTk.PhotoImage(image=Image.fromarray(cv2.merge((r,g,b))))
        self.ImageList[newXOrigin][newYOrigin] = imgg
        self.EmojiLabelList[newXOrigin][newYOrigin].configure(image = self.ImageList[newXOrigin][newYOrigin])

        self.EmojiListState[num] = not self.EmojiListState[num]
        

    def ReplaceMainImage(self, num, event=None):
        self.EmojiLabelRight.config(text=definitionList['0'][num]['name'])
        newYOrigin0 = (num%10) * 75
        newXOrigin0 = math.floor(num/10) * 75
        newimage = imgSheet[newXOrigin0:newXOrigin0+75, newYOrigin0:newYOrigin0+75]
        imgh = cv2.resize(imgSheet[newXOrigin0:newXOrigin0+75, newYOrigin0:newYOrigin0+75], (176,176))
        bg = numpy.zeros((176, 176, 4), numpy.uint8)
        bg[:] = (63,57,54,255)
        imgh = self.MergeImages(imgh, bg)
        b,g,r,a = cv2.split(imgh)
        imgg = ImageTk.PhotoImage(image=Image.fromarray(cv2.merge((r,g,b))))
        self.MainImageResource = imgg
        self.MainImageLabel.config(image=self.MainImageResource)

    def ResetMainImage(self, event=None):
        if(self.CurrentEmoji != -99):
            self.EmojiLabelRight.config(text=self.CurrentEmoji)
            num = self.CurrentEmoji
            newYOrigin0 = (num%10) * 75
            newXOrigin0 = math.floor(num/10) * 75
            newimage = imgSheet[newXOrigin0:newXOrigin0+75, newYOrigin0:newYOrigin0+75]
            imgh = cv2.resize(imgSheet[newXOrigin0:newXOrigin0+75, newYOrigin0:newYOrigin0+75], (176,176))
            bg = numpy.zeros((176, 176, 4), numpy.uint8)
            bg[:] = (63,57,54,255)
            imgh = self.MergeImages(imgh, bg)
            b,g,r,a = cv2.split(imgh)
            self.EmojiLabelRight.config(text=definitionList['0'][num]['name'])
        else:
            #imgh = self.MergeImages()
            self.EmojiLabelRight.config(text="New Game")
            imgh = cv2.resize(cv2.imread("resources/sprite4.png", cv2.IMREAD_UNCHANGED),(176,176))
            b,g,r = cv2.split(imgh)
        imgg = ImageTk.PhotoImage(image=Image.fromarray(cv2.merge((r,g,b))))
        self.MainImageResource = imgg
        self.MainImageLabel.config(image=self.MainImageResource)

    def ResetAll(self, event=None):
        self.EmojiListState = [False for x in range(len(self.EmojiListState))]
        self.UpdateAllIcons()
        self.CurrentEmoji = -99
        self.RoundNumber = 0
        self.ResetMainImage()
        self.EmojiLabelLeft.config(text="Round 0")
            

    def ChooseNewRandomNumber(self, event=None):
        newListAvailable = []
        for x in range(len(self.EmojiListState)):
            if(self.EmojiListState[x]):
                newListAvailable.append(x)

        if(len(newListAvailable) != 0):
            newNum = newListAvailable[randint(0, len(newListAvailable) - 1)]
            self.EmojiListState[newNum] = True
            self.CurrentEmoji = newNum
            self.UpdateIconByNumber(newNum)
            self.ResetMainImage()
            self.RoundNumber+=1
            self.EmojiLabelLeft.config(text="Round "+str(self.RoundNumber))
            

    def UpdateAllIcons(self, event=None):
        for i in range(75):
            self.UpdateIconByNumber(i)

    def ExitApp(self, event=None):
        num = 1

    def MergeImages(self, image0, image1, event=None): #image 0 above image1
        alpha_bg = image1[:,:,3] / 255.0
        alpha_fg = image0[:,:,3] / 255.0
        for color in range(0,3):
            image1[:,:,color] = alpha_fg * image0[:,:,color] + \
                                alpha_bg * image1[:,:,color] * ( 1 - alpha_fg )
        image1[:,:,3] = (1 - (1 - alpha_fg) * (1 - alpha_bg)) * 255

        return image1

    def PrintNewCards(self, event=None):
        cardheight = 5
        cardwidth = 5
        sheetIndex = 10
        spacing = 25

        
        imgSheet = cv2.imread("resources/tilesheet.png", cv2.IMREAD_UNCHANGED)

        chmod('generatedCards', 0o777)
        rmtree('generatedCards', ignore_errors=True)
        mkdir('generatedCards')
        
        for c in range(30):
            BingoArray = []
            renderSheet = cv2.imread("resources/card.png", cv2.IMREAD_UNCHANGED)
            for i in range(cardwidth):
                BingoColumn = [-99 for x in range(cardheight)]
                for Val in range(cardheight):
                    newRandom = random.randrange( i * 15 + 1, ( i + 1 ) * 15) - 1
                    while newRandom in BingoColumn:
                        newRandom = random.randrange( i * 15 + 1, ( i + 1 ) * 15) - 1
                    BingoColumn[Val] = newRandom
                BingoArray.append(BingoColumn)
            BingoArray[math.floor(cardwidth/2)][math.floor(cardheight/2)] = -99

            FinalImage = numpy.zeros(shape=[(cardheight*75)+(cardheight*spacing), spacing, 4], dtype=numpy.uint8)

            for i in range(len(BingoArray)):

                newVal = BingoArray[i][0]
                newYOrigin = (newVal%10) * 75
                newXOrigin = math.floor(newVal/10) * 75
                image = imgSheet[newXOrigin:newXOrigin+75, newYOrigin:newYOrigin+75]
                spacer = numpy.zeros(shape=[spacing, 75, 4], dtype=numpy.uint8)
                newImage = cv2.vconcat([image, spacer])
                for j in range(len(BingoArray[0]) - 1):
                    if( BingoArray[i][j + 1] == -99):
                        newYOrigin = 9 * 75
                        newXOrigin = 7 * 75
                        image = numpy.zeros(shape=[75, 75, 4], dtype=numpy.uint8)
                        
                        newImage = cv2.vconcat([newImage, image])
                    else:
                        newVal = BingoArray[i][j + 1]
                        newYOrigin = (newVal%10) * 75
                        newXOrigin = math.floor(newVal/10) * 75
                        image = imgSheet[newXOrigin:newXOrigin+75, newYOrigin:newYOrigin+75]
                        newImage = cv2.vconcat([newImage, image])
                    newImage = cv2.vconcat([newImage, numpy.zeros(shape=[spacing, 75, 4], dtype=numpy.uint8)])
                newspacing = numpy.zeros(shape=[cardheight*75+(cardwidth*spacing), spacing, 4], dtype=numpy.uint8)
                FinalImage = cv2.hconcat([FinalImage,newImage])
                FinalImage = cv2.hconcat([FinalImage,newspacing])
            FinalImage = cv2.vconcat([ numpy.zeros(shape=[spacing, cardheight*75+(cardwidth*spacing) + spacing, 4], dtype=numpy.uint8), FinalImage])
            x_offset, y_offset = 150, 30

            maskSheet = renderSheet[x_offset:x_offset+FinalImage.shape[0],y_offset:y_offset+FinalImage.shape[1]]
            alpha_background = maskSheet[:,:,3] / 255.0
            alpha_foreground = FinalImage[:,:,3] / 255.0

            for color in range(0, 3):
                maskSheet[:,:,color] = alpha_foreground * FinalImage[:,:,color] + \
                    alpha_background * maskSheet[:,:,color] * (1 - alpha_foreground)
            maskSheet[:,:,3] = (1 - (1 - alpha_foreground) * (1 - alpha_background)) * 255

            renderSheet[x_offset:x_offset+FinalImage.shape[0],y_offset:y_offset+FinalImage.shape[1]] = maskSheet
            cv2.imwrite('generatedCards/gen_'+str(c)+'.png', renderSheet)
        print("cards generated successfully!")
        
def main():
    root = tkinter.Tk()
    GUI = GameConstruct(root)
    root.mainloop()

if __name__ == '__main__':
    main()
