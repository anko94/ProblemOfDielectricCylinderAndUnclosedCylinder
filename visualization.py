import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


class Visualization:

    def fillDielectricRectangle(self, dielectricRectangle, n, m):
        rectangles = dielectricRectangle.breakUpRectangleByNMPoints(n, m)
        for i in range(len(rectangles)):
            vertices = rectangles[i].getListOfVertices()
            self.axes.add_patch(mpatches.Circle(vertices[0], 0.03, color=(0, 0, 0)))
            self.axes.add_patch(mpatches.Circle(vertices[1], 0.03, color=(0, 0, 0)))
            self.axes.add_patch(mpatches.Circle(vertices[2], 0.03, color=(0, 0, 0)))
            self.axes.add_patch(mpatches.Circle(vertices[3], 0.03, color=(0, 0, 0)))
        plt.show()

    def fillArc(self, arc, n):
        c = arc.breakUpArcByNPoints(n)
        print(len(c))
        for i in range(len(c)):
            self.axes.add_patch(mpatches.Circle(c[i], 0.03, color=(0, 0, 0)))
        plt.show()

    def drawTask(self, dielectricRectangle, source, arc):
        self.axes.add_patch(mpatches.Rectangle(dielectricRectangle.lowerLeft, dielectricRectangle.width,
                                               dielectricRectangle.height,dielectricRectangle.rotateAngle, fill=False))
        self.axes.add_patch(mpatches.Circle(source.point, 0.1, color=(0, 0, 0)))
        self.axes.add_patch(mpatches.Arc(arc.center, arc.radius*2, arc.radius*2, arc.rotateAngle, -arc.angle, arc.angle))

        plt.show()

    def __init__(self):
        self.figure = plt.figure()
        self.axes = self.figure.add_subplot(111, aspect='equal')
        self.axes.set_xbound([-4, 4])
        self.axes.set_ybound([-4, 4])
