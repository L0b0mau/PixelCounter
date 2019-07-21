import numpy as np
import cv2
import glob
import csv


# This script automatically measures how much of an image was colorized by test subjects
# written by Silvio de Carvalho:)

def translate(value, leftMin, leftMax, rightMin, rightMax):
    # mapping percentage values to the right values.
    # Taken from stackoverflow due to lazines :D written by Adam Luchjenbroers
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)


# img = cv2.imread('test.jpg',0)
img = cv2.imread('empty.jpg', 0)  # empty image
full = cv2.imread('full.jpg', 0)  # full image



filenames = glob.glob("images/*.jpg")  # enter the path to your samples and the corresponding file extension
filenames.sort()  # sorting them alphabetically
images = [cv2.imread(img, 0) for img in filenames]

print("\n\nWelcome to our image processing skript")
print(f"Today we are testing {len(filenames)} sample files\n")

height, width = img.shape

print("Image Height: ", height)
print("Image Width: ", width)
print("Image Shape: ", img.shape)
# print("example: ", img[100,100])



#defining the part of the image we are interested in
topX = 350
topY = 0
bottomX = 951
bottomY = 1098

selection = img[topX:bottomX, topY:bottomY]  # The part of the image we are interested in
selectionfull = full[topX:bottomX, topY:bottomY]


height2, width2 = selection.shape

print("\nSelection Height: ", selection.shape[0])
print("Selection Width: ", selection.shape[1])
print("Selection Shape: ", selection.shape)
print("Selection Pixels: ", selection.shape[0] * selection.shape[0])

ret, thresh1 = cv2.threshold(selection, 200, 255, cv2.THRESH_BINARY)
ret, threshfull = cv2.threshold(selectionfull, 200, 255, cv2.THRESH_BINARY)


# empty standard image
whitepixel = cv2.countNonZero(thresh1)
totalpixel = (height2 * width2)
darkpixel = totalpixel - whitepixel  # this are our 0%
print("\nDark Pixels in a non colored image: ", darkpixel)

# Completely filled out
whitepixelfull = cv2.countNonZero(threshfull)
darkpixelfull = totalpixel - whitepixelfull  # this are our 100%
print("\nDark Pixels in a fully colored image: ", darkpixelfull)

with open('Colorizingdata.csv', mode='w') as colorizeInfo:
    colorizeInfo_writer = csv.writer(colorizeInfo, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    colorizeInfo_writer.writerow(['SubjectNr', 'Percentage', 'Colored Pixel', 'Filepath'])

# Calculations for each individual test sample
counter = 0
for myimg in images:
    counter += 1
    subjectselection = myimg[topX:bottomX, topY:bottomY]
    subjectcode = myimg[0:150, 0:480]  # If there is a subject code written somewhere on the page

    ret, threshprob = cv2.threshold(subjectselection, 200, 255,
                                    cv2.THRESH_BINARY)  # threshold needs to be defined manually to see what fits best
    whitepixelprob = cv2.countNonZero(threshprob)
    darkpixelprob = totalpixel - whitepixelprob
    pixeldif = darkpixelprob - darkpixel

    coloredpercentage = round(translate(darkpixelprob, darkpixel, darkpixelfull, 0, 100), 1)
    print("Image", counter)
    print("Path", filenames[counter - 1])
    print("Colored Pixel:", pixeldif)
    print("Color Percentage: ", coloredpercentage, "%")

    # storing the data in an csv file
    with open('Colorizingdata.csv', mode='a') as colorizeInfo:
        colorizeInfo_writer = csv.writer(colorizeInfo, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        colorizeInfo_writer.writerow([counter, coloredpercentage, darkpixelprob, filenames[counter - 1]])

    # writing the data together with the subject code in new images

    message1 = f"colored pixels: {pixeldif}"
    message2 = f"colored percentage: {coloredpercentage}%"

    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(subjectcode, message1, (10, 110), font, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
    cv2.putText(subjectcode, message2, (10, 130), font, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
    myfilename = f"results/participant{counter}.png"
    cv2.imwrite(myfilename, subjectcode)

    #Show images if wanted
    # cv2.imshow('Subjectcode with info', subjectcode)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()





