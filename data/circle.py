import math


class Circle:
    def fromDegreesToRadians(self, angle):
        return angle * math.pi/180

    def breakUpByNPoints(self, n):
        dAngle = 360/n
        angle = 0
        result = []
        while math.fabs(360 - angle) >= self.accuracy:
            if angle >= 0 and angle < 90:
                result.append([self.center[0]+self.radius*math.sin(self.fromDegreesToRadians(angle)),
                               self.center[1]+self.radius*math.cos(self.fromDegreesToRadians(angle))])
            elif angle >= 90 and angle < 180:
                result.append([self.center[0] + self.radius * math.cos(self.fromDegreesToRadians(angle-90)),
                               self.center[1] - self.radius * math.sin(self.fromDegreesToRadians(angle-90))])
            elif angle >= 180 and angle < 270:
                result.append([self.center[0] - self.radius * math.sin(self.fromDegreesToRadians(angle-180)),
                               self.center[1] - self.radius * math.cos(self.fromDegreesToRadians(angle-180))])
            elif angle >= 270 and angle < 360:
                result.append([self.center[0] - self.radius * math.cos(self.fromDegreesToRadians(angle-270)),
                               self.center[1] + self.radius * math.sin(self.fromDegreesToRadians(angle-270))])
            angle+=dAngle
        return result

    def __init__(self, center, radius):
        self.center = center
        self.radius = radius
        self.accuracy = 0.0000001