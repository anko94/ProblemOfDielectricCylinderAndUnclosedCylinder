import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.lines import Line2D
import math


class Visualization:

    def fillLine(self, line, n):
        br = line.breakUpByNPoints(n)
        x = br[0]
        y = br[1]
        nx = 0
        if type(x) is list:
            nx = 1
        d = x if nx==1 else y
        for i in range(len(d)):
            if nx ==1:
                self.axes.add_patch(mpatches.Circle([d[i], y], 0.03, color=(0, 0, 0)))
            else:
                self.axes.add_patch(mpatches.Circle([x, d[i]], 0.03, color=(0, 0, 0)))
            plt.draw()

    def fillCircle(self, circle, n):
        c = circle.breakUpByNPoints(n)
        for i in range(len(c)):
            self.axes.add_patch(mpatches.Circle(c[i], 0.03, color=(0, 0, 0)))
            plt.draw()
            plt.pause(self.arcPeriod)

    def fillDielectricRectangle(self, dielectricRectangle, n, m):
        rectangles = dielectricRectangle.breakUpRectangleByNMPoints(n, m)
        for i in range(len(rectangles)):
            vertices = rectangles[i].getListOfVertices()
            self.axes.add_patch(mpatches.Circle(vertices[0], 0.003, color=(0, 0, 0)))
            plt.draw()
            plt.pause(self.rectanglePeriod)
            self.axes.add_patch(mpatches.Circle(vertices[1], 0.003, color=(0, 0, 0)))
            plt.draw()
            plt.pause(self.rectanglePeriod)
            self.axes.add_patch(mpatches.Circle(vertices[2], 0.003, color=(0, 0, 0)))
            plt.draw()
            plt.pause(self.rectanglePeriod)
            self.axes.add_patch(mpatches.Circle(vertices[3], 0.003, color=(0, 0, 0)))
            plt.draw()
            self.axes.add_patch(mpatches.Circle([vertices[1][0]-math.fabs(vertices[1][0]-vertices[2][0])/2,
                     vertices[1][1]-math.fabs(vertices[1][1]-vertices[2][1])/2], 0.003, color=(0, 0, 0)))
            plt.draw()
            plt.pause(self.dielectricPeriod)

    def fillArc(self, arc, n):
        c = arc.breakUpArcByNPoints(n)
        for i in range(len(c)):
            self.axes.add_patch(mpatches.Circle(c[i], 0.03, color=(0, 0, 0)))
            plt.draw()
            plt.pause(self.arcPeriod)

    def drawTask(self, dielectricRectangle, source, arc, figure, figureObj):
        self.axes.add_patch(mpatches.Rectangle(dielectricRectangle[0].lowerLeft, dielectricRectangle[0].width,
                                               dielectricRectangle[0].height, dielectricRectangle[0].rotateAngle, fill=False))
        if len(dielectricRectangle)==2:
            self.axes.add_patch(mpatches.Rectangle(dielectricRectangle[1].lowerLeft, dielectricRectangle[1].width,
                                                   dielectricRectangle[1].height, dielectricRectangle[1].rotateAngle,
                                                   fill=False))
        self.axes.add_patch(mpatches.Circle(source.point, 0.1, color=(0, 0, 0)))
        self.axes.add_patch(mpatches.Arc(arc.center, arc.radius * 2, arc.radius * 2, arc.rotateAngle, -arc.angle, arc.angle))
        if figure == "circle":
            self.axes.add_patch(mpatches.Circle(figureObj.center, figureObj.radius, color=(0, 0, 0), fill=False))
        else:
            self.axes.add_line(Line2D(figureObj.x, figureObj.y, color="black"))
        plt.draw()
        plt.pause(self.taskPeriod)

    def blockPlot(self):
        plt.ioff()
        plt.show()

    def __init__(self, taskPeriod, arcPeriod, rectanglePeriod, dielectricPeriod):
        self.figure = plt.figure()
        self.axes = self.figure.add_subplot(111, aspect='equal')
        self.axes.set_xbound([-4, 4])
        self.axes.set_ybound([-4, 4])
        self.taskPeriod = taskPeriod
        self.arcPeriod = arcPeriod
        self.rectanglePeriod = rectanglePeriod
        self.dielectricPeriod = dielectricPeriod
        plt.ion()
