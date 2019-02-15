import matplotlib
import matplotlib.pyplot as plt
from pylab import rcParams
import matplotlib.patches as patches
import numpy as np

#created classes
from .paper_space import PaperSpace
from .choord_change import ChoordChange

class PlotWindMap(ChoordChange):
    '''
    assumed text height = 82 units  for 22000
    150 units for 3500

    length 500 for 656

    '''
    IMAGE_PATH = "WINDMAP.JPG"

    MF = 1.8 #MULTIPLICATION FACTOR
    def __init__(self, wind_values, app_data):
        super().__init__()
        plt.axis('off')
        self.app_data = app_data
        plt.figure(figsize=(16,16), dpi=100)
        self.paper_space = PaperSpace()
        self.start_point = (80 * PlotWindMap.MF, 80 * PlotWindMap.MF)
        self.container = {
            "length": 900 * PlotWindMap.MF,
            "height": 127.5 * PlotWindMap.MF
        }
        self.setFont()
        self.wind_values = wind_values
        pass

    def setFont(self):
        font = {
            'family' : 'calibri',
            'weight': 'normal',
            'size'   : 12
        }
        matplotlib.rc('font', **font)
        # rcParams['figure.figsize'] = 50, 100
        pass

    def plotMap(self):
        print("Creating wind map image . . .")
        axes = plt.gca()
        axes.set_xlim(self.paper_space.x_limit)
        axes.set_ylim(self.paper_space.x_limit)
        self.drawContainers()
        # self.drawLines()
        #save test image
        plt.axis('off')
        plt.savefig(self.app_data.getWindMapImagePath(), bbox_inches='tight')
        # plt.show()
        pass

    def drawContainers(self):
        start_point = list(self.start_point)
        length = self.container["length"]
        
        for i, text in enumerate(self.wind_values):
            height = self.container["height"] * len(text)
            # print(len(text), height, start_point)
            rect = self.getRect(start_point, length, height)
            plt.gca().add_patch(rect)
            self.addTexts(start_point, text)
            start_point[1] += height/4
            if i%5 == 4:
                #for third value, reset x and y and change x
                start_point[1] = self.start_point[1]
                start_point[0]+= length + 100 * PlotWindMap.MF

    def drawLines(self): 
        '''
        not being used at the time
        '''
        start_point = list(self.start_point)
        length = self.container["length"]
        height = self.container["height"] 
        for i, text in enumerate(self.wind_values):
            self.drawRectPoints(start_point, length, height)
            self.addTexts(start_point, text)
            start_point[1] += height/4
            if i%4 == 3:
                #for third value, reset x and y and change x
                start_point[1] = self.start_point[1]
                start_point[0]+= length + 100 * PlotWindMap.MF

    def drawRectPoints(self, start_point, length, height):
        '''
           2 ___________ 3
            |           |
            |           |
            |           |
            |           |
            |___________|
           1             4

           not being used at the time
        '''
        pt1 = start_point
        pt2 = self.changeY(pt1, height)
        pt3 = self.changeX(pt2, length)
        pt4 = self.changeX(pt1, length)
        # for each line you two lists
        # line1
        line1x, line1y = [pt1[0], pt2[0]], [pt1[1], pt2[1]]
        line2x, line2y = [pt2[0], pt3[0]], [pt2[1], pt3[1]]
        line3x, line3y = [pt3[0], pt4[0]], [pt3[1], pt4[1]]
        line4x, line4y = [pt4[0], pt1[0]], [pt4[1], pt1[1]]

        plt.plot(line1x, line1y, line2x, line2y, line3x, line3y, line4x, line4y)

    def plotRectData(self, start_point, length, height):
        rect = self.getRect(start_point, length, height)
        plt.gca().add_patch(rect)

    def addTexts(self, start_point, texts):
        step = 120 * PlotWindMap.MF
        pt = start_point
        # pt = [i + (40 * PlotWindMap.MF) for i in start_point]
        pt[0] = start_point[0] + (40 * PlotWindMap.MF)
        pt[1] = start_point[1] + (80 * PlotWindMap.MF)
        y = pt[1]
        for i, text in enumerate(reversed(texts)):
            pt[1] = y + step * i
            self.addText(text, pt)

    def getRect(self, start_point, length, height, 
        linewidth=0.5, edgecolor='black', facecolor='none'):

        return plt.Rectangle(start_point,length,height,
            linewidth=linewidth, edgecolor=edgecolor, facecolor=facecolor)

    def addText(self, text, start_point):
        plt.text(start_point[0], start_point[1], text)






# plt.plot((1,2,3), (5,7,4))

# fig, ax = plt.subplots(1)
# plt.savefig("test.png", bbox_inches='tight')

# ax.add_patch(rect)
# ax.axis('off')

