import os

import addonwindow as pyxbmct

from xbmcswift2 import xbmc, xbmcaddon, xbmcgui

_addon_path = xbmcaddon.Addon().getAddonInfo('path')

COLOR_FO = '0xFFE0B074'
COLOR_NF = '0xFF808080'
COLOR_HEADING = '0xFFD6D6D6'
COLOR_DETAILS = '0xFF707070'
COLOR_SELECTED = '0xFFF1F1F1'


class GameInfo(pyxbmct.AddonDialogWindow):
    def __init__(self, container, game, title=''):
        super(GameInfo, self).__init__(title)
        self.container = container
        self.game = game
        background = None
        if container.get_core().get_active_skin() == 'skin.osmc':
            media_path = '/usr/share/kodi/addons/skin.osmc/media'
            if os.path.exists(media_path):
                background = os.path.join(media_path, 'dialogs/DialogBackground_old.png')

        if background is not None:
            self.background.setImage(background)
            self.removeControl(self.title_background)
            self.removeControl(self.window_close_button)
            self.removeControl(self.title_bar)

        self.setGeometry(1280, 720, 12, 6, padding=50)
        self.set_info_controls(game)
        self.set_active_controls(game)
        self.set_navigation()
        self.connect(pyxbmct.ACTION_NAV_BACK, self.close)
        # init controls
        self.image = None
        self.genre = None
        self.year = None
        self.plot = None
        self.button_play = None
        self.button_cover_art = None
        self.button_fanart = None

    def set_info_controls(self, game):
        title_label = pyxbmct.Label(game.name, alignment=pyxbmct.ALIGN_LEFT, font='XLarge', textColor=COLOR_HEADING)
        self.placeControl(title_label, 0, 0, 2, 3)

        self.image = pyxbmct.Image(game.poster)
        self.placeControl(self.image, 2, 0, 6, 1)

        genre_label = pyxbmct.Label('Genre', alignment=pyxbmct.ALIGN_LEFT, font='Med', textColor=COLOR_DETAILS)
        self.placeControl(genre_label, 2, 2)
        self.genre = pyxbmct.Label(game.get_genre_as_string(), alignment=pyxbmct.ALIGN_LEFT, font='Med')
        self.placeControl(self.genre, 2, 3, columnspan=3)

        year_label = pyxbmct.Label('Year', alignment=pyxbmct.ALIGN_LEFT, font='Med', textColor=COLOR_DETAILS)
        self.placeControl(year_label, 3, 2)
        self.year = pyxbmct.Label(game.year, alignment=pyxbmct.ALIGN_LEFT, font='Med')
        self.placeControl(self.year, 3, 3)

        self.plot = pyxbmct.TextBox()
        self.placeControl(self.plot, 4, 2, 6, 3)
        self.plot.setText(game.plot)

    def set_active_controls(self, game):
        self.button_play = pyxbmct.Button('Play', focusTexture='', noFocusTexture='', focusedColor=COLOR_FO,
                                          textColor=COLOR_NF, font='Med')
        self.placeControl(self.button_play, 11, 0)
        self.connect(self.button_play, self.launch_game)

        self.button_cover_art = pyxbmct.Button('Choose Cover Art', focusTexture='', noFocusTexture='',
                                               focusedColor=COLOR_FO, textColor=COLOR_NF, font='Med')
        self.placeControl(self.button_cover_art, 11, 1)
        self.connect(self.button_cover_art, self.select_cover_art)

        self.button_fanart = pyxbmct.Button('Choose Fanart', focusTexture='', noFocusTexture='',
                                            focusedColor=COLOR_FO, textColor=COLOR_NF, font='Med')
        self.placeControl(self.button_fanart, 11, 2)
        self.connect(self.button_fanart, self.select_fanart)

    def set_navigation(self):
        self.button_play.controlRight(self.button_fanart)
        self.button_play.controlLeft(self.button_fanart)
        self.button_fanart.controlRight(self.button_play)
        self.button_fanart.controlLeft(self.button_play)

        self.setFocus(self.button_play)

    def launch_game(self):
        xbmc.executebuiltin('XBMC.RunPlugin(%s)' % self.container.get_plugin().url_for(
                endpoint='launch_game',
                game_id=self.game.name))

    def select_fanart(self):
        browser = xbmcgui.Dialog().browse(2, 'Select Fanart', 'files', '.jpg|.png', False, False,
                                          self.game.get_fanart(0, ''))
        if browser:
            self.game.selected_fanart = browser
            self.container.get_core().get_storage().sync()

    def select_cover_art(self):
        browser = xbmcgui.Dialog().browse(2, 'Select Cover Art', 'files', '.jpg|.png', False, False,
                                          self.game.get_poster(0, ''))
        if browser:
            self.game.selected_poster = browser
            self.container.get_core().get_storage().sync()

    def setAnimation(self, control):
        control.setAnimations(
                [
                    ('WindowOpen', 'effect=fade start=0 end=100 time=500',),
                    ('WindowClose', 'effect=fade start=100 end=0 time=500',)
                ]
        )
