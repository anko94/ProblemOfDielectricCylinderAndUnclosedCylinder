from data.arc import Arc
from data.dielectricRectangle import DielectricRectangle
from data.source import Source
from visualization import Visualization

if __name__ == "__main__":
    #all angles in degrees
    #lower left point, width, height, rotateAngle
    dielectricRectangle = DielectricRectangle([0, 0], 1, 2, 30)
    #point
    source = Source([2, 2])
    #center, radius, angle, rotateAngle
    arc = Arc([-2, -2], 1, 30, -90)
    visualization = Visualization()
    visualization.drawTask(dielectricRectangle, source, arc)