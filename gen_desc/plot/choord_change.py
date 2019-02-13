class ChoordChange(object):
    X = 0
    Y = 1
    def __init__(self, scale_factor=1):
        self.scale_factor = float(scale_factor)
        pass

    def changeY(self, coord, value):
    
        '''
        change y coordinate of coord by the value sent in.
        A scale factor is applied if it is a user preference
        '''

        new_coord = list(coord)
        new_coord[ChoordChange.Y] += (value * self.scale_factor)

        return new_coord

    def changeX(self, coord, value):

        '''
        change x coordinate of coord by the value sent in.
        A scale factor is applied if it is a user preference
        '''

        new_coord = list(coord)
        new_coord[ChoordChange.X] += (value * self.scale_factor)

        return new_coord

    def changeXY(self, coord, value_x, value_y):
        new_coord_1 = self.changeX(coord, value_x)
        new_coord_2 = self.changeY(new_coord_1, value_y)

        return new_coord_2


