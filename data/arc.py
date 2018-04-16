import math


class Arc:

    def getBorderVertices(self):
        return self.getTwoVertices(self.angle)

    def getTwoVertices(self, angle):
        rotateAngleRadians = (self.rotateAngle+90) % 360 * math.pi/180
        x1 = self.center[0] + self.radius * math.sin(rotateAngleRadians)
        y1 = self.center[1] - self.radius * math.cos(rotateAngleRadians)
        b = (180 - angle)/2
        c = 90 - b
        bRadians = b * math.pi/180
        cRadians = c * math.pi/180
        side1 = 2*self.radius * math.cos(bRadians)
        return [[x1 + side1 * math.cos(rotateAngleRadians + cRadians),
                 y1 + side1 * math.sin(rotateAngleRadians + cRadians)],
                [x1 - side1 * math.cos(cRadians - rotateAngleRadians),
                 y1 + side1 * math.sin(cRadians - rotateAngleRadians)]]

    def breakUpArcByNPoints(self, n):
        n+=1
        result = []
        exitFlag = 0
        angle = self.angle
        dl = 2 * math.pi * self.radius/(n-1) * angle * 2/360
        while exitFlag != 1:
            d = self.getTwoVertices(angle)
            if math.sqrt((d[0][0] - d[1][0])**2 + (d[0][1] - d[1][1])**2) < self.accuracy:
                result.append(d[0])
            else:
                result.append(d[0])
                result.append(d[1])
            angle = angle - dl/(2*math.pi*self.radius) * 360
            if angle < 0:
                exitFlag = 1
        result = self.putVerticesInCorrectOrder(result)
        result1 = []
        for i in range(1, len(result)):
            result1.append([(result[i-1][0]+result[i][0])/2, (result[i-1][1]+result[i][1])/2])
        return result1

    #rewrite this method for another case of arc
    def putVerticesInCorrectOrder(self, array):
        resultArray = []
        i = 1
        while i<len(array):
            resultArray.append(array[i])
            i+=2
        i = len(array)-2 if len(array)%2==0 else len(array) - 1
        while i>=0:
            resultArray.append(array[i])
            i-=2
        return resultArray

    def __init__(self, center, radius, angle, rotateAngle):
        self.center = center
        self.radius = radius
        self.angle = angle
        self.rotateAngle = rotateAngle % 360
        self.accuracy = 0.0000001
