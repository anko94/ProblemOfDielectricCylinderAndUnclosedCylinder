class Line:
    def breakUpByNPoints(self, n):
        nx = 0
        d = self.y
        if self.y[0]==self.y[1]:
            nx=1
            d=self.x
        k = (d[1]-d[0])/(n-1)
        d1 = d[0]
        result = []
        for i in range(n):
            result.append(d1+k*i)
        return [result, self.y[0]] if nx==1 else [self.x[0], result]

    def __init__(self, x, y):
        self.x = x
        self.y = y