import arcade
import arcade.gui


class MenuView(arcade.View):
    """Main menu view class."""

    def __init__(self, main_view):
        super().__init__()

        self.manager = arcade.gui.UIManager()

        # place buttons
        resume_button = arcade.gui.UIFlatButton(text="Resume", width=150, height=75)
        start_new_game_button = arcade.gui.UIFlatButton(text="Restart", width=150, height=75)
        settings_button = arcade.gui.UIFlatButton(text="Settings", width=150, height=75)
        exit_button = arcade.gui.UIFlatButton(text="Exit", width=150, height=75)

        # Initialise a grid in which widgets can be arranged.
        self.grid = arcade.gui.UIGridLayout(column_count=2, row_count=2, horizontal_spacing=20, vertical_spacing=20)

        # Adding the buttons to the layout.
        self.grid.add(resume_button, col_num=0, row_num=0)
        self.grid.add(settings_button, col_num=1, row_num=0)
        self.grid.add(start_new_game_button, col_num=0, row_num=1)
        self.grid.add(exit_button, col_num=1, row_num=1)

        self.anchor = self.manager.add(arcade.gui.UIAnchorLayout())

        self.anchor.add(
            anchor_x="center_x",
            anchor_y="center_y",
            child=self.grid,
        )

        self.title = arcade.gui.UILabel(
            text="Menu",
            font_size=80,
            font_name="Impact",
            text_color=arcade.color.BURNT_ORANGE

        )
        self.anchor.with_padding(all=40)
        self.anchor.add(
            anchor_x="center_x",
            anchor_y="top",
            child=self.title,
        )

        self.main_view = main_view

        @resume_button.event("on_click")
        def on_click_resume_button(event):
            # Pass already created view because we are resuming.
            self.window.show_view(self.main_view)

        @start_new_game_button.event("on_click")
        def on_click_start_new_game_button(event):
            # Create a new view because we are starting a new game.
            score = int(self.main_view.score)
            if not self.main_view.score_added_to_highscores:
                self.main_view.highscores.add_score(score)
                self.main_view.score_added_to_highscores = True
            main_view.restart()

        @exit_button.event("on_click")
        def on_click_exit_button(event):
            score = int(self.main_view.score)
            if not self.main_view.score_added_to_highscores:
                self.main_view.highscores.add_score(score)
                self.main_view.score_added_to_highscores = True
            arcade.exit()

        @settings_button.event("on_click")
        def on_click_volume_button(event):
            volume_menu = SubMenu(
                "Settings", "Sound Effects", "Music", main_view
            )
            self.manager.add(
                volume_menu,
                layer=1
            )

    def on_hide_view(self):
        # Disable the UIManager when the view is hidden.
        self.manager.disable()

    def on_show_view(self):
        """ This is run once when we switch to this view """

        # Makes the background darker
        # self.menu_background = arcade.load_texture("background.png")
        arcade.set_background_color(arcade.color.DARK_GOLDENROD)

        # Enable the UIManager when the view is showm.
        self.manager.enable()

    def on_draw(self):
        """ Render the screen. """
        # Clear the screen
        self.clear()

        # display current high score and score
        score = int(self.main_view.score)
        highscore = int(self.main_view.highscores.get_high_score())

        if score > highscore:
            highscore_text = "High Score: " + str(score)
        else:
            highscore_text = "High Score: " + str(highscore)

        highscore_display = arcade.Text(highscore_text, 330, 200,
                         arcade.color.BURNT_ORANGE, 40, 80, 'left', "Impact")
        highscore_display.draw()

        score_text = "Score: " + str(score)
        score_display = arcade.Text(score_text, 330, 100,
                                    arcade.color.BURNT_ORANGE, 40, 80, 'left', "Impact")
        score_display.draw()

        self.manager.draw()


class MenuViewDeath(arcade.View):
    """Main menu view class."""

    def __init__(self, main_view):
        super().__init__()

        self.manager = arcade.gui.UIManager()

        start_new_game_button = arcade.gui.UIFlatButton(text="Play Again", width=320, height=75)
        settings_button = arcade.gui.UIFlatButton(text="Settings", width=150, height=75)
        exit_button = arcade.gui.UIFlatButton(text="Exit", width=150, height=75)

        # Initialise a grid in which widgets can be arranged.
        self.grid = arcade.gui.UIGridLayout(column_count=2, row_count=2, horizontal_spacing=20, vertical_spacing=20)

        # Adding the buttons to the layout.
        self.grid.add(settings_button, col_num=0, row_num=1)
        self.grid.add(start_new_game_button, col_num=0, row_num=0, col_span=2)
        self.grid.add(exit_button, col_num=1, row_num=1)

        self.anchor = self.manager.add(arcade.gui.UIAnchorLayout())

        self.anchor.add(
            anchor_x="center_x",
            anchor_y="center_y",
            child=self.grid,
        )

        self.title = arcade.gui.UILabel(
            text="Game Over",
            font_size=80,
            font_name="Impact",
            text_color=arcade.color.BURNT_ORANGE

        )
        self.anchor.with_padding(all=40)
        self.anchor.add(
            anchor_x="center_x",
            anchor_y="top",
            child=self.title,
        )


        self.main_view = main_view

        @start_new_game_button.event("on_click")
        def on_click_start_new_game_button(event):
            # Create a new view because we are starting a new game.
            main_view.restart()

        @exit_button.event("on_click")
        def on_click_exit_button(event):
            arcade.exit()

        @settings_button.event("on_click")
        def on_click_volume_button(event):
            volume_menu = SubMenu(
                "Settings", "Sound Effects", "Music", self.main_view
            )
            self.manager.add(
                volume_menu,
                layer=1
            )


    def on_hide_view(self):
        # Disable the UIManager when the view is hidden.
        self.manager.disable()

    def on_show_view(self):
        """ This is run once when we switch to this view """

        # Makes the background darker
        # self.menu_background = arcade.load_texture("background.png")
        arcade.set_background_color(arcade.color.DARK_GOLDENROD)

        # Enable the UIManager when the view is showm.
        self.manager.enable()

    def on_draw(self):
        """ Render the screen. """
        # Clear the screen
        self.clear()

        self.manager.draw()

        coin_count_text = "Coins Collected: " + str(self.main_view.coin_score)
        coin_display = arcade.Text(coin_count_text, 330, 200,
                         arcade.color.BURNT_ORANGE, 40, 80, 'left', "Impact")
        coin_display.draw()

        score = int(self.main_view.score)
        if not self.main_view.score_added_to_highscores:
            self.main_view.highscores.add_score(score)
            self.main_view.score_added_to_highscores = True

        score_text = "Score: " + str(score)
        score_display = arcade.Text(score_text, 330, 100,
                  arcade.color.BURNT_ORANGE, 40, 80, 'left', "Impact")
        score_display.draw()


class SubMenu(arcade.gui.UIMouseFilterMixin, arcade.gui.UIAnchorLayout):
    """Acts like a fake view/window."""

    def __init__(self, title: str, toggle_label: str, toggle_label2: str, main_view):
        super().__init__(size_hint=(1, 1))

        self.on_sound = True
        self.main_view = main_view

        self.on_music = True

        # Setup frame which will act like the window.
        frame = self.add(arcade.gui.UIAnchorLayout(width=300, height=300, size_hint=None))
        frame.with_padding(all=20)

        # Add a background to the window.
        # Nine patch smoothes the edges.
        frame.with_background(texture=arcade.gui.NinePatchTexture(
            left=7,
            right=7,
            bottom=7,
            top=7,
            texture=arcade.load_texture(
                "images/orange.jpg"
            )
        ))

        back_button = arcade.gui.UIFlatButton(text="Back", width=250)
        # The type of event listener we used earlier for the button will not work here.
        back_button.on_click = self.on_click_back_button

        title_label = arcade.gui.UILabel(text=title, align="center", font_size=20, multiline=False,
                                         text_color=arcade.color.BLACK)


        # --- Start button
        if not main_view.muted:
            normal_texture = arcade.load_texture(":resources:onscreen_controls/flat_dark/"
                                                 "sound_on.png")
            hover_texture = arcade.load_texture(":resources:onscreen_controls/shaded_dark/"
                                                "sound_on.png")
            press_texture = arcade.load_texture(":resources:onscreen_controls/shaded_dark/"
                                                "sound_on.png")
        else:
            normal_texture = arcade.load_texture(":resources:onscreen_controls/flat_dark/"
                                                 "sound_off.png")
            hover_texture = arcade.load_texture(":resources:onscreen_controls/shaded_dark/"
                                                "sound_off.png")
            press_texture = arcade.load_texture(":resources:onscreen_controls/shaded_dark/"
                                                "sound_off.png")

        toggle_label = arcade.gui.UILabel(text=" Sound")
        # Create our button
        self.start_button = arcade.gui.UITextureButton(
            texture=normal_texture,
            texture_hovered=hover_texture,
            texture_pressed=press_texture,
        )

        # Map that button's on_click method to this view's on_button_click method.
        self.start_button.on_click = self.start_button_clicked  # type: ignore



        # Align toggle and label horizontally next to each other
        toggle_group = arcade.gui.UIBoxLayout(vertical=False, space_between=5)
        toggle_group.add(self.start_button)
        toggle_group.add(toggle_label)


        widget_layout = arcade.gui.UIBoxLayout(align="left", space_between=10)
        widget_layout.add(title_label)
        widget_layout.add(toggle_group)

        widget_layout.add(back_button)

        frame.add(child=widget_layout, anchor_x="center_x", anchor_y="top")



    def on_click_back_button(self, event):
        self.parent.remove(self)

    def sound_button_off(self):
        self.start_button.texture_pressed = \
            arcade.load_texture(":resources:onscreen_controls/shaded_dark/sound_off.png")
        self.start_button.texture = \
            arcade.load_texture(":resources:onscreen_controls/flat_dark/sound_off.png")
        self.start_button.texture_hovered = \
            arcade.load_texture(":resources:onscreen_controls/shaded_dark/sound_off.png")

    def sound_button_on(self):
        self.start_button.texture_pressed = \
            arcade.load_texture(":resources:onscreen_controls/shaded_dark/sound_on.png")
        self.start_button.texture = \
            arcade.load_texture(":resources:onscreen_controls/flat_dark/sound_on.png")
        self.start_button.texture_hovered = \
            arcade.load_texture(":resources:onscreen_controls/shaded_dark/sound_on.png")



    def start_button_clicked(self, *_):
        if self.on_sound:
            self.on_sound = False
            self.sound_button_off()
            self.main_view.muted = True

        else:
            self.on_sound = True
            self.sound_button_on()
            self.main_view.muted = False









