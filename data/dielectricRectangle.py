import math


class DielectricRectangle:

    def breakUpRectangleByNMPoints(self, n, m):
        dw = self.width/m
        dh = self.height/n
        rotateAngleRadians = self.rotateAngle * math.pi/180
        result = []
        for i in range(m):
            for j in range(n):
                x1 = self.lowerLeft[0] + i * dw * math.cos(rotateAngleRadians) - j * dh * math.sin(rotateAngleRadians)
                y1 = self.lowerLeft[1] + i * dw * math.sin(rotateAngleRadians) + j * dh * math.cos(rotateAngleRadians)
                result.append(DielectricRectangle([x1, y1], dw, dh, self.rotateAngle))

        return result

    def getListOfVertices(self):
        rotateAngleRadians = self.rotateAngle * math.pi/180
        x1 = self.lowerLeft[0] - self.height * math.sin(rotateAngleRadians)
        y1 = self.lowerLeft[1] + self.height * math.cos(rotateAngleRadians)
        return [self.lowerLeft,
                [x1, y1],
                [self.lowerLeft[0] + self.width * math.cos(rotateAngleRadians),
                 self.lowerLeft[1] + self.width * math.sin(rotateAngleRadians)],
                [x1 + self.width * math.cos(rotateAngleRadians), y1 + self.width * math.sin(rotateAngleRadians)]]

    # rotateAngle to OX
    def __init__(self, lowerLeft, width, height, rotateAngle):
        self.lowerLeft = lowerLeft
        self.width = width
        self.height = height
        self.rotateAngle = rotateAngle % 360
