import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

#created classes
from paper_space import PaperSpace

class PlotWindMap:
    '''
    assumed text height = 82 units  for 22000
    150 units for 3500

    length 500 for 656

    '''
    def __init__(self):
        plt.axis('off')
        self.paper_space = PaperSpace()
        self.start_point = (80,80)
        self.container = {
            "length": 1300,
            "height": 1400
        }
        self.setFont()
        pass

    def setFont(self):
        font = {
            'family' : 'normal',
            'weight': 'normal',
            'size'   : 11
        }
        matplotlib.rc('font', **font)
        pass

    def plotMap(self):
        axes = plt.gca()
        axes.set_xlim(self.paper_space.x_limit)
        axes.set_ylim(self.paper_space.x_limit)
        self.drawContainers()
        plt.show()
        pass

    def drawContainers(self):
        start_point = list(self.start_point)
        length = self.container["length"]
        height = self.container["height"]
        for i in range(4):
            rect = self.getRect(start_point, length, height)
            plt.gca().add_patch(rect)
            self.addTexts(start_point)
            start_point[1] += height + 200
            if i == 1:
                #for third value, reset x and y and change x
                start_point = list(self.start_point)
                start_point[0]+= length + 300
            
            
    def plotRectData(self, start_point, length, height):
        rect = self.getRect(start_point, length, height)
        plt.gca().add_patch(rect)

    def addTexts(self, start_point):
        texts = ["Fig. 27.4-4, ≤ 0.5L", "θ = 0˚", 
            "CASE A: CN = -0.8", "P = -0.6005 kN/sq.m", "Zone: 804",
            "", "CASE B: CN = 0.8", "Zone: 805"]
        step = 160
        pt = [i + 80 for i in start_point]
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


plot_map = PlotWindMap()
plot_map.plotMap()





# plt.plot((1,2,3), (5,7,4))

# fig, ax = plt.subplots(1)
# plt.savefig("test.png", bbox_inches='tight')

# ax.add_patch(rect)
# ax.axis('off')

