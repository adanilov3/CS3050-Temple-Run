import arcade

UPDATES_PER_FRAME_RUNNING = 3
UPDATES_PER_FRAME_JUMPING = 6
UPDATES_PER_FRAME_SLIDING = 5
UPDATES_PER_FRAME_DYING = 5
class Character(arcade.Sprite):
    def __init__(self):

        # Set up parent class
        super().__init__()

        # Default to face-right
        self.character_face_direction = 0

        # Used for flipping between image sequences
        self.cur_texture = 0

        self.scale = 1.0

        # Adjust the collision box. Default includes too much empty space
        # side-to-side. Box is centered at sprite center, (0, 0)
        self.points = [[-22, -64], [22, -64], [22, 28], [-22, 28]]

        # --- Load Textures ---

        # Load textures for walking
        self.walk_textures = []
        for i in range(8):
            texture = arcade.load_texture("images/Adventurer Sprite Sheet v1.5.png", x=i * 32, y=352, width=32, height=32)
            self.walk_textures.append(texture)

        # Load textures for walking
        self.jump_textures = []
        for i in range(6):
            texture = arcade.load_texture("images/Adventurer Sprite Sheet v1.5.png", x=i * 32, y=160, width=32, height=32)
            self.jump_textures.append(texture)

        self.is_jumping = False

        # Load textures for sliding
        self.slide_textures = []
        for i in range(6):
            texture = arcade.load_texture("images/Adventurer Sprite Sheet v1.5.png", x=i * 32, y=384, width=32, height=32)
            self.slide_textures.append(texture)

        self.is_sliding = False

        # Load textures for death
        self.death_textures = []
        for i in range(6):
            texture = arcade.load_texture("images/Adventurer Sprite Sheet v1.5.png", x=i * 32, y=224, width=32, height=32)
            self.death_textures.append(texture)

        # Load textures for death
        self.fall_textures = []
        for i in range(9):
            texture = arcade.load_texture("images/Adventurer Sprite Sheet v1.5.png", x=i * 32, y=448, width=32,
                                              height=32)
            self.fall_textures.append(texture)

        self.is_dead_splat = False
        self.is_dead_fall = False
        self.go_to_menu = False

    def update_animation(self, delta_time: float = 1 / 60):

        if self.is_jumping:
            # Update jump animation
            self.cur_texture += 1
            if self.cur_texture > 5 * UPDATES_PER_FRAME_JUMPING:
                self.is_jumping = False
                self.cur_texture = 0
            frame = self.cur_texture // UPDATES_PER_FRAME_JUMPING
            self.texture = self.jump_textures[frame]

        elif self.is_sliding:
            # Update slide animation
            self.cur_texture += 1
            if self.cur_texture > 5 * UPDATES_PER_FRAME_SLIDING:
                self.is_sliding = False
                self.cur_texture = 0
            frame = self.cur_texture // UPDATES_PER_FRAME_SLIDING
            self.texture = self.slide_textures[frame]

        elif self.is_dead_fall or self.is_dead_splat:
            # Update death animation and set go_to_menu as true
            self.cur_texture += 1
            if self.is_dead_splat:
                if self.cur_texture > len(self.death_textures) * UPDATES_PER_FRAME_DYING:
                    self.is_dead_splat = False
                    self.cur_texture = 0
                    self.go_to_menu = True

                frame = self.cur_texture // UPDATES_PER_FRAME_DYING
                if frame < len(self.death_textures):
                    self.texture = self.death_textures[frame]
            else:
                if self.cur_texture > len(self.fall_textures) * UPDATES_PER_FRAME_DYING:
                    self.is_dead_fall = False
                    self.cur_texture = 0
                    self.go_to_menu = True

                frame = self.cur_texture // UPDATES_PER_FRAME_DYING
                if frame < len(self.fall_textures):
                    self.texture = self.fall_textures[frame]


        else:
            # Walking animation
            self.cur_texture += 1
            if self.cur_texture > 7 * UPDATES_PER_FRAME_RUNNING:
                self.cur_texture = 0
            frame = self.cur_texture // UPDATES_PER_FRAME_RUNNING
            self.texture = self.walk_textures[frame]

    def start_jump_animation(self):
        # Play the jump animation when the player presses the up arrow key
        if not self.is_jumping:
            self.is_jumping = True
            self.cur_texture = 0  # Reset the texture frame
            self.texture = self.jump_textures[0]  # Use the first frame of the jump animation

    def start_slide_animation(self):
        # Play the slide animation when the player presses the down arrow key
        if not self.is_sliding:
            self.is_sliding = True
            self.cur_texture = 0  # Reset the texture frame
            self.texture = self.slide_textures[0]  # Use the first frame of the slide animation

    def start_death_animation(self):
        # Play the death animation when the player collides with the obstacle
        if not self.is_dead_splat:
            self.is_dead_splat = True
            self.cur_texture = 0  # Reset the texture frame
            self.texture = self.death_textures[0]  # Use the first frame of the death animation

    def start_fall_animation(self):
        # Play the death animation when the player collides with the obstacle
        if not self.is_dead_fall:
            self.is_dead_fall = True
            self.cur_texture = 0  # Reset the texture frame
            self.texture = self.fall_textures[0]  # Use the first frame of the death animation






