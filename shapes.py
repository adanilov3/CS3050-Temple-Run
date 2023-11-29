import arcade
import math
import random

"""
Class path is the parent class of all primitive objects, provides attributes and 
allows uniform scaling, movement within the renderer
"""
class Shape:
    def __init__(self, x, y, width, height, color, size, object_type=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.scale = 1
        self.size = size
        self.type = object_type
        self.angle = None

    # Getters
    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def getScale(self):
        return self.scale

    def getSize(self):
        return self.size

    def getWidth(self):
        return self.width

    def getHeight(self):
        return self.height

    def getAngle(self):
        return self.angle

    def getType(self):
        return self.type

    # Setters
    def setX(self, x):
        self.x = x

    def setY(self, y):
        self.y = y

    def setScale(self, scale):
        self.scale = scale

    def setSize(self, size):
        self.size = size

    def setAngle(self, angle):
        self.angle = angle


# rotates a point around another point and returns the outcome
def rotate_point(point, pivot_point, angle):
    # point to rotate
    x, y = point

    # point to rotate about
    px, py = pivot_point

    new_x = px + math.cos(angle) * (x - px) - math.sin(angle) * (y - py)
    new_y = py + math.sin(angle) * (x - px) + math.cos(angle) * (y - py)
    return new_x, new_y


"""
Path objects appear in the game as a hole in the ground that the player has to avoid
"""
class Path(Shape):
    def __init__(self, screen_width, screen_height, color, side_of_path):
        # seg height is the total vertical distance of the segment of the hole
        self.seg_height = 10

        # hole width is the width of the top of the hole
        self.hole_width = 30

        # creates values for the points based on which side of the path it on
        # -1 is left, 0 is middle, 1 is right  (of the path)
        if side_of_path == -1:
            self.c_x = screen_width / 2 - self.hole_width * 2
            self.l_slope = 8 / 70
            self.r_slope = 8 / 90
        elif side_of_path == 1:
            self.c_x = screen_width / 2 + self.hole_width * 2
            self.l_slope = 8 / 90
            self.r_slope = 8 / 70
        else:
            self.c_x = screen_width / 2
            self.l_slope = 8 / 90
            self.r_slope = 8 / 90

        super().__init__(self.c_x, screen_height - 100, screen_width/3, 30, color, 1, 1)

    def draw(self):
        # top left x, bottom y etc, for the point list
        t_l_x = (self.x - self.hole_width * self.scale)
        t_r_x = (self.x + self.hole_width * self.scale)
        b_r_x = ((self.x + self.hole_width * self.scale) + self.seg_height * self.r_slope)
        b_l_x = ((self.x - self.hole_width * self.scale) - self.seg_height * self.l_slope)
        t_y = (self.y + self.seg_height * self.scale / 2)
        b_y = (self.y - self.seg_height * self.scale / 2)

        point_list = ((t_l_x, t_y), (t_r_x, t_y), (b_r_x, b_y), (b_l_x, b_y))
        arcade.draw_polygon_filled(point_list, self.color)


"""
Randomly generated Clouds appear on side of screen as a decoration
"""
class Cloud(Shape):
    def __init__(self, screen_width, screen_height, x):
        super().__init__(x, screen_height - 100, screen_width/3, 30, arcade.color.WHITE, 1, 1)
        # the number of circles that will make up the cloud
        self.num_parts = 8
        # make a list of all the random values being plugged into the cloud for the duration of its instantiation
        # x, y offset from the origin of the cloud and radius
        self.x_off = []
        self.y_off = []
        self.rads = []
        # populate lists with random values
        for i in range(self.num_parts):
            self.x_off.append(random.randint(-30, 30))
            self.y_off.append(random.randint(-30, 30))
            self.rads.append(random.randint(15, 45))

    def draw(self):
        for i in range(self.num_parts):
            arcade.draw_circle_filled(self.x + self.x_off[i], self.y + self.y_off[i], self.rads[i], self.color)


"""
Trees fall over to give player something else to avoid
"""
class ObstacleTree(Shape):
    def __init__(self, x, y, width, height, color, size, rotation_rate, side_of_path):
        super().__init__(x, y, width, height, color, size)
        # stores current rotation
        self.visual_rotation = 0
        # rotation rate is in radians
        self.rotation_rate = rotation_rate * -side_of_path
        # holds state of not rotated/rotating/rotated -> 0/1/2
        self.rotating = 0
        # gets which direction to rotate 1 = left side, -1 = right side
        self.side_of_path = side_of_path
        self.py = self.y - (self.height / 2) * self.scale

        # num parts is the number of circles that make up the foliage
        self.num_parts = 6
        self.x_off = []
        self.y_off = []
        self.rads = []

        # populate lists of x offset, y offset, and radius of each of the circles in the foliage
        for i in range(self.num_parts):
            self.x_off.append(random.randint(-20, 20))
            self.y_off.append(random.randint(-20, 20))
            self.rads.append(random.randint(15, 35))

    def draw(self):
        # gets width and height / 2
        w2 = self.width / 2
        h2 = self.height / 2

        # x and y coord to rotate about
        c_x = self.x + w2 * self.side_of_path  * self.scale
        c_y = self.y - h2 * self.scale
        self.py = c_y

        # gets top, bottom, left, right y and x values
        l_x = self.x - w2 * self.scale
        r_x = self.x + w2 * self.scale
        b_y = c_y
        t_y = self.y + h2 * self.scale

        # gets the points, rotated about the bottom left or right corner of the tree
        # by self.visual_rotation radians

        # draw the trunk

        points = (
            rotate_point((l_x, b_y), (c_x, c_y), self.visual_rotation),
            rotate_point((r_x, b_y), (c_x, c_y), self.visual_rotation),
            rotate_point((r_x, t_y), (c_x, c_y), self.visual_rotation),
            rotate_point((l_x, t_y), (c_x, c_y), self.visual_rotation)
        )
        arcade.draw_polygon_filled(points, self.color)

        # draw the foliage
        for i in range(self.num_parts):
            coords = rotate_point((self.x + self.x_off[i] * self.scale,
                                   self.y + self.height/2 + self.y_off[i] * self.scale),
                                  (c_x, c_y), self.visual_rotation)
            arcade.draw_circle_filled(coords[0], coords[1],
                                      self.rads[i] * self.scale, arcade.color.FOREST_GREEN)

    # increments the rotation from origin the tree is at,
    def start_rotating(self):
        self.rotating = 1

    # if currently rotating self.rotating will = 1, if finished rotating, 2
    def rotate(self):
        if self.rotating == 1:
            self.visual_rotation -= self.rotation_rate

        # only allows 90 degrees of rotation
        if abs(self.visual_rotation) >= (math.pi / 2):
            self.rotating = 2
