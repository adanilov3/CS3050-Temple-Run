import math

import shapes


class Renderer:
    """
    Function: Renderer constructor
    initializes screen dimensions and the players initial position
    """
    def __init__(self, screen_height, screen_width, player_y_pos):
        self.screen_height = screen_height
        self.screen_width = screen_width
        self.player_x_pos = screen_width/2
        self.player_y_pos = player_y_pos

    """
    Function: scale_object
    @param object shape 
    Scales shape based off of distance from the player
    """
    def scale_object(self, shape):
        scale_rate = .997
        base_size = shape.getSize()

        shape.setScale((scale_rate ** shape.y) * base_size + 1)

    def scale_object_sprite(self, shape, base_scale):
        scale_rate = .997
        if base_scale <= .4:
            shape.scale = ((scale_rate ** shape.center_y))
        if (base_scale <= .6) and (base_scale > .4):
            shape.scale = ((scale_rate ** shape.center_y) + .5)
        if (base_scale <= 1.0) and (base_scale > .7):
            shape.scale = ((scale_rate ** shape.center_y) + 0.8)


    """
    Function: getAngle
    @param object shape
    @returns float angle
    gets the angle formed by the object's x and y movement vectors, scaled by the max_angle_scaler
    """
    def getAngle(self, shape):
        max_angle_scaler = 180/180
        # if object is to right of player the angle will be negative, otherwise positive
        # (an angle of 0 is straight down)
        if shape.getX() > self.player_x_pos:
            angle = -math.atan((self.player_x_pos - (shape.getX() - 2*(shape.getX() - self.player_x_pos)))
                               / shape.getY())
        else:
            angle = math.atan((self.player_x_pos - shape.getX())
                              / shape.getY())

        return angle * max_angle_scaler

    def getAngleSprite(self, sprite):
        max_angle_scaler = 180/180
        # if object is to right of player the angle will be negative, otherwise positive
        # (an angle of 0 is straight down)
        if sprite.center_x > self.player_x_pos:
            angle = -math.atan((self.player_x_pos - (sprite.center_x - 2*(sprite.center_x - self.player_x_pos)))
                               / sprite.center_y)
        else:
            angle = math.atan((self.player_x_pos - sprite.center_x)
                              / sprite.center_y)

        return angle * max_angle_scaler

    """
    Function: translate_object
    @param object shape, float x, float y
    translates the given shapes coords by given x, y values and gets the 
    new angle the object will travel at
    """
    def translate_object(self, shape, x, y):
        y_move = shape.getY() - y
        x_move = shape.getX() - x

        shape.setY(y_move)
        shape.setX(x_move)

        shape.setAngle(self.getAngle(shape))

    def translate_object_sprite(self, shape, x, y):
        y_move = shape.center_y - y
        x_move = shape.center_x - x

        shape.center_x = y_move
        shape.center_y = x_move

        shape.setAngleSprite(self.getAngle(shape))

    """
    Function: move_object
    @param object shape, delta time
    moves shape based on an objects scale and delta time
    """
    def move_object(self, shape, delta_time):
        angle = shape.getAngle()
        # universal speed scales the speed of everything moving
        if type(shape) is shapes.Cloud:
            universal_speed = 200
        else:
            universal_speed = 300

        # set speed (length of whole velocity vector)
        speed = delta_time * universal_speed * (self.screen_height - shape.getY()) / self.screen_height

        # get the x and y coord the object will travel to
        y_move = shape.getY() - speed
        x_move = shape.getX() - math.tan(angle) * speed

        shape.setY(y_move)
        shape.setX(x_move)

    def move_object_sprite(self, shape, delta_time):
        angle = shape.angle
        # universal speed scales the speed of everything moving
        universal_speed = 200

        # set speed (length of whole velocity vector)
        speed = delta_time * universal_speed * (self.screen_height - shape.center_y) / self.screen_height

        # get the x and y coord the object will travel to
        y_move = shape.center_y - speed
        x_move = shape.center_x - math.tan(angle) * speed

        shape.center_y = y_move
        shape.center_x = x_move
