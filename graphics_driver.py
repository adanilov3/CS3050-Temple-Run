import math
import arcade
import arcade.gui
import random
import shapes
from arcade import shape_list
from renderer import Renderer
from obstacles import Rock, Coin, StaticTree, TurnTree, Gap
import collision_system
from object_randomizer import Object_Randomizer
from char_animation import Character
from menu import MenuView, MenuViewDeath
from highscores import HighScores

# Set universal variables
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 775
SCREEN_TITLE = "Temple Run!"

# sets the x units off the center of the screen for the sides of the path
PATH_WIDTH = 100

# animation speeds
MOVEMENT_SPEED = 5
MOVEMENT_SPEED2 = 5
JUMP_HEIGHT = 125  # The height of the jump
JUMP_PERIOD = 1.3  # The period of the jump motion
SLIDE_PERIOD = 0.5 # The period of the jump anim


# function used to load textures for animations
def load_texture_pair(filename):
    """
    Load a texture pair, with the second being a mirror image.
    """
    return [
        arcade.load_texture(filename),
        arcade.load_texture(filename)
    ]


class MyGame(arcade.View):
    """ Main application class. """

    def __init__(self):
        # Call the parent __init__
        super().__init__()

        self.jump_sound = arcade.Sound("sounds/gruntJump.wav")
        self.splat_sound = arcade.Sound("sounds/splat.wav")
        self.played_splat = False
        self.scream_sound = arcade.Sound("sounds/scream.wav")
        self.played_scream = False
        self.slide_sound = arcade.Sound("sounds/slide.wav")
        self.coin_sound = arcade.Sound("sounds/coin.wav")
        self.highscore_sound = arcade.Sound("sounds/woohoo.wav")
        self.played = False

        self.muted = False

        # define variables used to make path and boundaries for player movement
        self.line_start = None
        self.line_end = None
        self.bound = None
        self.bound_list = None

        # place-holder number, can change without breaking anything (probably)
        self.o_tree = None
        player_y_pos = 75

        # make an instance of the renderer
        self.engine = Renderer(SCREEN_HEIGHT, SCREEN_WIDTH, player_y_pos)

        # make an instance of the randomizer system
        self.o_list = [Rock, StaticTree]
        self.randomizer = Object_Randomizer(self.o_list, Coin, Gap, TurnTree, 2.5, 0.5, 20.0, 10.0, -80, 80)

        # initialization for the menu widgets
        self.manager = arcade.gui.UIManager()

        switch_menu_button = arcade.gui.UITextureButton(texture=arcade.load_texture(
            ":resources:onscreen_controls/shaded_light/pause_square.png"
        ))

        # Initialise the button with an on_click event.
        @switch_menu_button.event("on_click")
        def on_click_switch_button(event):
            # Passing the main view into menu view as an argument.
            menu_view = MenuView(self)
            self.window.show_view(menu_view)

        # Use the anchor to position the button on the screen.
        self.anchor = self.manager.add(arcade.gui.UIAnchorLayout())

        self.anchor.add(
            anchor_x="right",
            anchor_y="top",
            child=switch_menu_button,
        )

        # define sprites and sprite lists for character, shapes, obstacles, and graphitcs.
        self.shape_list = None
        self.player_list = None
        self.rock_list = None
        self.player = None
        self.rock = None
        self.base_scale_rock = None
        self.fade_rect = None
        self.path = None
        self.walls_list = None
        self.wall = None
        self.base_scale_wall = None
        self.initial_wall = None
        self.initial_walls = None
        self.coins_list = None
        self.coin = None
        self.base_scale_coin = None
        self.coin_score = 0
        self.tree = None
        self.trees_list = None
        self.base_scale_tree = None
        self.score = 0

        # define line segments for drawing and outline on the path
        self.line_segments = [
            ((320, 0), (400, 700)),
            ((680, 0), (600, 700)),
        ]

        self.sky_fade = shape_list.ShapeElementList()

        # sets height of sky and fade in area
        sky_height = SCREEN_HEIGHT * .7
        fade_height = SCREEN_HEIGHT * .6

        # color is sky_blue 255 is solid, 0 transparent
        background_color_solid = (125, 206, 235, 255)
        background_color_transparent = (125, 206, 235, 0)

        # points for transparent sky
        points = (
            (0, sky_height),
            (SCREEN_WIDTH, sky_height),
            (SCREEN_WIDTH, SCREEN_HEIGHT),
            (0, SCREEN_HEIGHT)
        )

        # solid color to cover up path and objects not yet visible to player
        colors = (
            background_color_solid, background_color_solid,
            background_color_solid, background_color_solid
        )

        sky = shape_list.create_rectangle_filled_with_colors(points, colors)
        self.sky_fade.append(sky)

        # points for the fade in area below sky
        points = (
            (0, fade_height),
            (SCREEN_WIDTH, fade_height),
            (SCREEN_WIDTH, sky_height),
            (0, sky_height)
        )

        # colors vec from transparent -> solid
        colors = (
            background_color_transparent, background_color_transparent,
            background_color_solid, background_color_solid
        )

        # list of sky, fade is printed in on_draw
        fade_rect = shape_list.create_rectangle_filled_with_colors(points, colors)
        self.sky_fade.append(fade_rect)

        # define more variables for animation states
        self.physics_engine = None
        self.jump_start_y = None
        self.is_jumping = False
        self.slide_start_y = None
        self.is_sliding = False
        self.jump_time = 0.0
        self.slide_time = 0.0
        self.draw_interval = 2.0
        self.is_dead_splat = False
        self.is_dead_fall = False

        # displaying highscores
        self.highscores = HighScores()
        self.score_added_to_highscores = False
        self.show_highscore_message = False
        self.highscore_shown = False
        self.high_score_message_timer = 0

        self.setup()

    def setup(self):
        # def the sprite lists
        self.shape_list = []
        self.bound_list = arcade.SpriteList()
        self.walls_list = arcade.SpriteList()
        self.rock_list = arcade.SpriteList()
        self.initial_walls = arcade.SpriteList()
        self.player_list = arcade.SpriteList()
        self.coins_list = arcade.SpriteList()
        self.trees_list = arcade.SpriteList()

        for shape in self.shape_list:
            shape.setAngle(self.engine.getAngle(shape))

        # define sprite for a player character
        self.player = Character()
        self.player.center_x = 500
        self.player.center_y = 100
        self.player.scale = 3.0
        self.player_list.append(self.player)

        y_coordinates = []

        for i in range(0, 669, 31):
            y_coordinates.append(i)

        # Put up some wood walls
        # using a coordinate list to place sprites
        coordinate_list = [[400, 700], [600, 700]]

        for coordinate in coordinate_list:
            # Add a wall on the ground
            self.wall = arcade.Sprite(
                "images/woodWallCorner_N.png", .2
            )
            self.wall.center_x = coordinate[0]
            self.wall.center_y = coordinate[1]
            self.wall.height = 10
            self.wall.width = 10
            self.wall.angle = self.engine.getAngleSprite(self.wall)
            self.base_scale_wall = .3
            self.walls_list.append(self.wall)

        # define boundary sprites
        bound_coords = [[340, 100], [660, 100]]
        for coord in bound_coords:
            self.bound = arcade.Sprite(":resources:images/topdown_tanks/tankGreen_barrel1_outline.png", .2)
            self.bound.center_x = coord[0]
            self.bound.center_y = coord[1]
            self.bound_list.append(self.bound)

        # Create the 'physics engine' that will make sure the player does not go past the bounds
        self.physics_engine = arcade.PhysicsEngineSimple(
            self.player, self.bound_list
        )

        # define the rock sprites
        self.rock = arcade.Sprite(arcade.load_texture(":resources:images/space_shooter/meteorGrey_big1.png"))
        self.rock.center_x = 430
        self.rock.center_y = 550
        self.rock.height = 10
        self.rock.width = 10
        self.rock.angle = self.engine.getAngleSprite(self.rock)
        self.rock.scale = .5
        self.base_scale_rock = .5
        #self.rock_list.append(self.rock)

        self.coin = arcade.Sprite(arcade.load_texture(":resources:images/items/coinGold.png"))
        self.coin.center_x = 570
        self.coin.center_y = 550
        self.coin.height = 5
        self.coin.width = 5
        self.coin.scale = .3
        self.base_scale_coin = .3
        self.coin.angle = self.engine.getAngleSprite(self.coin)
        self.coin.is_collected = False

        self.tree = arcade.Sprite(arcade.load_texture("images/tree.png"))
        self.tree.center_x = 500
        self.tree.center_y = 550
        self.tree.height = 10
        self.tree.width = 10
        self.tree.scale = 0.3
        self.base_scale_tree = 0.3
        self.tree.angle = self.engine.getAngleSprite(self.tree)

        # define variables to check player state and help with the jump movement
        self.jump_start_y = self.player.center_y  # Starting y-coordinate of the jump
        self.is_jumping = False  # Flag to indicate if the player is currently jumping
        self.jump_time = 0  # Time elapsed during the jump

        # this function will call the given function every 2 seconds so that the walls are continuously
        # being drawn
        arcade.schedule(self.draw_repetitive_wall, self.draw_interval)

    def on_update(self, dt):

        #Add new objects as needed
        self.randomizer.tick(dt, self.engine)

        if len(self.shape_list) < 10:
            l_or_r = random.randint(0, 1)

            if l_or_r == 0:
                self.shape_list.append(shapes.Cloud(SCREEN_WIDTH, SCREEN_HEIGHT, random.randint(100, 300)))
            else:
                self.shape_list.append(shapes.Cloud(SCREEN_WIDTH, SCREEN_HEIGHT, random.randint(700, 900)))

            self.shape_list[-1].setAngle(self.engine.getAngle(self.shape_list[-1]))

        # Move the player and update animation
        self.player_list.update()
        self.player_list.update_animation()
        self.physics_engine.update()

        """ Move everything """
        for shape in self.shape_list:
            # remove objects off-screen
            if shape.getX() > SCREEN_WIDTH + 100 or shape.getX() < -100 or shape.getY() < -100:
                self.shape_list.remove(shape)

            # do scaling and movement operations
            self.engine.scale_object(shape)
            self.engine.move_object(shape, dt)
            if type(shape) is shapes.ObstacleTree:
                shape.rotate()

        # move all objects instantiated by randomizer
        for obst in self.randomizer.active_obstacles:
            if (obst.sprite.center_y + (obst.sprite.height / 3) < 0 or
                    obst.sprite.center_x + obst.sprite.width < 0 or
                    obst.sprite.center_y - obst.sprite.width > SCREEN_WIDTH):
                obst.sprite.kill()
                self.randomizer.active_obstacles.remove(obst)
            # do scaling and movement operations
            self.engine.scale_object_sprite(obst.sprite, self.base_scale_rock)
            self.engine.move_object_sprite(obst.sprite, dt)

        for coin in self.randomizer.active_coins:
            if (coin.sprite.center_y + (coin.sprite.height / 2) < 0 or
                    coin.sprite.center_x + coin.sprite.width < 0 or
                    coin.sprite.center_y - coin.sprite.width > SCREEN_WIDTH):
                coin.sprite.kill()
                self.randomizer.active_coins.remove(coin)
            # do scaling and movement operations
            self.engine.scale_object_sprite(coin.sprite, self.base_scale_coin)
            self.engine.move_object_sprite(coin.sprite, dt)

        for tree in self.randomizer.active_trees:
            if(tree.y < 0):
                self.randomizer.active_trees.remove(tree)
            self.engine.scale_object(tree)
            self.engine.move_object(tree, dt)

        for gap in self.randomizer.active_gaps:
            if(gap.y < 0):
                self.randomizer.active_gaps.remove(gap)
            self.engine.scale_object(gap)
            self.engine.move_object(gap, dt)

        # update all sprite lists so that they are removed from the lists when they are moved off the screen
        # also pass the sprites in the list to the renderer to be moved and scaled
        for wall in self.walls_list:
            if wall.top < 0:
                wall.kill()

            # do scaling and movement operations
            self.engine.scale_object_sprite(wall, self.base_scale_wall)
            self.engine.move_object_sprite(wall, dt)

        for coin in self.randomizer.active_coins:
            if collision_system.runner_collision(self.player, coin, self.is_jumping, self.is_sliding):
                if not coin.is_collected:
                    if not self.muted:
                        self.coin_sound.play()
                    coin.is_collected = True
                    self.coin_score += 1
                    coin.sprite.kill()
                    self.randomizer.active_coins.remove(coin)
            # for obst in self.randomizer.active_obstacles:
            #     if collision_system.runner_collision(obst, coin, self.is_jumping, self.is_sliding):
            #         self.randomizer.active_obstacles.remove(obst)

        for obst in self.randomizer.active_obstacles:
            if collision_system.runner_collision(self.player, obst, self.is_jumping, self.is_sliding):
                self.is_dead_splat = True
                self.player.start_death_animation()
                if not self.played_splat and not self.muted:
                    self.splat_sound.play()
                    self.played_splat = True

        for gap in self.randomizer.active_gaps:
            if (collision_system.prim_collision_gap(self.player, gap, self.is_jumping)):
                self.is_dead_fall = True
                self.player.start_fall_animation()
                if not self.played_scream and not self.muted:
                    self.scream_sound.play()
                    self.played_scream = True

        for tree in self.randomizer.active_trees:
            if(collision_system.prim_collision_tree(self.player, tree, self.is_jumping)):
                self.is_dead_splat = True
                self.player.start_death_animation()
                if not self.played_splat and not self.muted:
                    self.splat_sound.play()
                    self.played_splat = True



        self.score += dt * 100
        # jump motion update
        if self.is_jumping:
            self.jump_time += dt
            if self.jump_time >= JUMP_PERIOD:
                self.is_jumping = False  # End the jump
                self.jump_time = 0
                self.player.center_y = self.jump_start_y  # Reset the player's y-coordinate
            else:
                # Calculate the new y-coordinate based on the sine wave
                self.player.center_y = self.jump_start_y + JUMP_HEIGHT * math.sin(
                    (math.pi / JUMP_PERIOD) * self.jump_time)

        if self.is_sliding:
            self.slide_time += dt
            if self.slide_time >= SLIDE_PERIOD:
                self.is_sliding = False
                self.slide_time = 0

        # check player collision with rock obstacle and start death animation if it collides
        # if self.player.collides_with_sprite(self.rock):
        #     self.player.start_death_animation()
        #     if not self.played_splat and not self.muted:
        #         self.splat_sound.play()
        #         self.played_splat = True

        # after death animation the view will switch to a menu
        menu_view = MenuViewDeath(self)
        go_to_menu = self.player.go_to_menu
        if go_to_menu:
            self.window.show_view(menu_view)

        if self.show_highscore_message:
            self.high_score_message_timer += dt
            if self.high_score_message_timer > 3:
                self.show_highscore_message = False
                self.highscore_shown = True


    def on_hide_view(self):
        # Disable the UIManager when the view is hidden.
        self.manager.disable()

    def on_show_view(self):
        """ This is run once when we switch to this view """
        arcade.set_background_color(arcade.color.SKY_BLUE)
        # Enable the UIManager when the view is shown.
        self.manager.enable()

    def on_draw(self):
        """ Render the screen. """
        # Clear the screen
        self.clear()
        # draw the bound sprites
        self.bound_list.draw()

        # draw a polygon and outlines to represent the path
        point_list = ((320, 0),
                      (680, 0),
                      (600, 700),
                      (400, 700))
        arcade.draw_polygon_filled(point_list, arcade.color.DIRT)
        for line_start, line_end in self.line_segments:
            arcade.draw_line(line_start[0], line_start[1], line_end[0], line_end[1], arcade.color.FOREST_GREEN, 4)

        if self.is_dead_splat:
            self.player_list.draw()

        for shape in self.shape_list:
            shape.draw()

        for gap in self.randomizer.active_gaps:
            gap.draw()

        # draw the other sprite lists.
        #self.o_tree.draw()
        self.walls_list.draw()
        self.rock_list.draw()
        self.coins_list.draw()
        self.trees_list.draw()

        for obst in self.randomizer.active_obstacles:
            obst.sprite.draw()

        for coin in self.randomizer.active_coins:
            coin.sprite.draw()

        for tree in self.randomizer.active_trees:
            tree.draw()

        # checking player layers
        if not self.is_dead_splat:
            self.player.draw()

        # draws the sky box and fade in area
        self.sky_fade.draw()


        coin_count_text = "Coins: " + str(self.coin_score)
        display_coins = arcade.Text(coin_count_text, 10, 50, arcade.color.BURNT_ORANGE, 25, font_name='Impact')
        display_coins.draw()

        # draws the score
        score_text = f"Score: {int(self.score)}"
        display_score = arcade.Text(score_text, 10, 10, arcade.color.BURNT_ORANGE, 25, font_name='Impact')
        display_score.draw()
        # Draw the manager.
        self.manager.draw()


        score = int(self.score)
        if score > self.highscores.get_high_score():
            self.show_highscore_message = True

        if self.show_highscore_message and not self.highscore_shown:
            if not self.played and not self.muted:
                self.highscore_sound.play()
                self.played = True

            high_score_message = "New High Score!"
            display_highscore = arcade.Text(high_score_message, 350, 600, arcade.color.BURNT_ORANGE, 40, font_name='Impact')
            display_highscore.draw()

    def on_key_press(self, key, modifiers):
        """
        Called whenever a key is pressed.
        """

        # Handle jump animation
        if key == arcade.key.UP:
            if not self.is_jumping and not self.is_sliding:  # check if the player is already jumping
                self.is_jumping = True
                self.jump_start_y = self.player.center_y  # set the starting y-coordinate of the jump
                self.player.start_jump_animation()
                if not self.muted:
                    self.jump_sound.play()

        # handle slide animation
        elif key == arcade.key.DOWN:
            if not self.is_sliding and not self.is_jumping:  # check if the player is already jumping
                self.is_sliding = True
                self.slide_start_y = self.player.center_y  # set the starting y-coordinate of the jump
                self.player.start_slide_animation()
                if not self.muted:
                    self.slide_sound.play()

        # handle running left
        if key == arcade.key.LEFT:
            self.player.change_x = -MOVEMENT_SPEED


        # handle running right
        elif key == arcade.key.RIGHT:
            self.player.change_x = MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
        """
        Called when the user releases a key.
        """
        if key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player.change_x = 0
        elif key == arcade.key.UP:
            self.player.change_y = 0

    def restart(self):
        # restart the game when called
        new_game = MyGame()
        self.window.show_view(new_game)

    def draw_repetitive_wall(self, dt):
        # this is called every 2 seconds to redraw all the walls so that they are constantly sliding
        # down the screen
        coordinate_list = [[400, 700], [600, 700]]

        for coordinate in coordinate_list:
            # Add a wall on the ground
            self.wall = arcade.Sprite(
                "images/woodWallCorner_N.png", .2
            )
            self.wall.center_x = coordinate[0]
            self.wall.center_y = coordinate[1]
            self.wall.height = 10
            self.wall.width = 10
            self.wall.angle = self.engine.getAngleSprite(self.wall)
            self.base_scale_wall = .3
            self.walls_list.append(self.wall)


def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, resizable=True)
    main_view = MyGame()
    window.show_view(main_view)
    arcade.run()


if __name__ == "__main__":
    main()
