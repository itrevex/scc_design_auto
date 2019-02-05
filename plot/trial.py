import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

#created classes
from paper_space import PaperSpace

class PlotWindMap:
    def __init__(self):
        plt.axis('off')
        self.paper_space = PaperSpace()
        pass
    
    def plotMap(self):
        axes = plt.gca()
        axes.set_xlim(self.paper_space.x_limit)
        axes.set_ylim(self.paper_space.x_limit)
        rect = self.getRect((10,30), 300, 150, 0.5)
        self.addText("Fig. 27.4-4, ≤ 0.5L", 150)
        self.addText("θ", 100)
        self.addText("0˚", 50)
        plt.gca().add_patch(rect)
        plt.show()
        pass

    def getRect(self, start_point, length, width, 
        linewidth=1, edgecolor='black', facecolor='none'):

        return plt.Rectangle(start_point,length,width,
            linewidth=linewidth, edgecolor=edgecolor, facecolor=facecolor)

    def addText(self, text, y):
        return plt.text(20, y, text)

plot_map = PlotWindMap()
plot_map.plotMap()





# plt.plot((1,2,3), (5,7,4))

# fig, ax = plt.subplots(1)
# plt.savefig("test.png", bbox_inches='tight')

# ax.add_patch(rect)
# ax.axis('off')

