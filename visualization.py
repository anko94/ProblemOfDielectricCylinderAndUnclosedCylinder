import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


class Visualization:

    def drawTask(self, dielectricRectangle, source, arc):
        self.axes.add_patch(mpatches.Rectangle(dielectricRectangle.lowerLeft, dielectricRectangle.width,
                                               dielectricRectangle.height,dielectricRectangle.rotateAngle, fill=False))
        self.axes.add_patch(mpatches.Circle(source.point, 0.1, color=(0, 0, 0)))
        self.axes.add_patch(mpatches.Arc(arc.center, arc.radius*2, arc.radius*2, arc.rotateAngle, -arc.angle, arc.angle))

        d = dielectricRectangle.getListOfVertices()
        self.axes.add_patch(mpatches.Circle(d[0], 0.1, color=(0, 0, 0)))
        self.axes.add_patch(mpatches.Circle(d[1], 0.1, color=(0, 0, 0)))
        self.axes.add_patch(mpatches.Circle(d[2], 0.1, color=(0, 0, 0)))
        self.axes.add_patch(mpatches.Circle(d[3], 0.1, color=(0, 0, 0)))

        plt.show()

    def __init__(self):
        self.figure = plt.figure()
        self.axes = self.figure.add_subplot(111, aspect='equal')
        self.axes.set_xbound([-4, 4])
        self.axes.set_ybound([-4, 4])
