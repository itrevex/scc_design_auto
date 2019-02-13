class PaperSpace:
    '''
    x_limit shows extents from minimum to 
    maximum x. (0, 1000) means from x = 0 to x = 1000
    y_limit is similar to x limit but in y
    '''
    def __init__(self):
        self.x_limit = (0, 10000)
        self.y_limit = (0, 10000)
        pass


    def setXLimit(self, limit):
        self.x_limit = tuple(limit)

    def setYLimit(self, limit):
        self.y_limit = tuple(limit)