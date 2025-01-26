import gi
from gi.repository import Adw
from gi.repository import Gtk,GObject
from .tilawa_download import TilawaDownloadGui
from .tilawa_settings import TilawaSetings

class TilawaGui():
    def __init__(self,parent,albasheer_data,audio_data_location):
        self.parent = parent
        self.albasheer_data      = albasheer_data
        self.audio_data_location = audio_data_location
        self.mainvb = Gtk.Box(orientation = Gtk.Orientation.VERTICAL)

        self.button_stack_switcher_box = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL)
        self.mainvb.append(self.button_stack_switcher_box)
        self.button_stack_switcher_box.add_css_class("linked")
        self.button_stack_switcher_box.props.margin_top  = 10
        self.button_stack_switcher_box.props.homogeneous = True
        self.button_stack_switcher_box.props.hexpand     = False
        self.button_stack_switcher_box.props.vexpand     = False
        self.button_stack_switcher_box.props.halign      = Gtk.Align.CENTER

        self.tilawa_setting_stack_toggle_button = Gtk.ToggleButton.new()
        self.tilawa_setting_stack_toggle_button.props.active  = True
        self.tilawa_setting_stack_toggle_button.connect("toggled",self.on_stack_switcher_button_toggled)
        self.tilawa_setting_stack_toggle_button.props.label   = _("Settings")
        self.button_stack_switcher_box.append(self.tilawa_setting_stack_toggle_button)

        self.tilawa_download_stack_toggle_button = Gtk.ToggleButton.new()
        #self.tilawa_download_stack_toggle_button.connect("toggled",self.on_stack_switcher_button_toggled)
        self.tilawa_download_stack_toggle_button.set_group(self.tilawa_setting_stack_toggle_button)
        self.tilawa_download_stack_toggle_button.props.label  = _("Download")
        self.button_stack_switcher_box.append(self.tilawa_download_stack_toggle_button)


        self.stack = Gtk.Stack.new()
        self.mainvb.append(self.stack)
        self.stack.props.hexpand = True
        self.stack.props.vexpand = True

        self.tilawasetings = TilawaSetings(parent,audio_data_location)
        self.stack.add_named(self.tilawasetings.mainvb,_("settings"))

        self.tilawadownloadgui = TilawaDownloadGui(self.parent,self.albasheer_data,self.audio_data_location)
        self.stack.add_named(self.tilawadownloadgui.mainvb,_("download"))

        self.tilawadownloadgui.connect("result",self.on_download_tilawa_done)

    def on_download_tilawa_done(self,w,name_,target_location,status):
        self.tilawasetings.read_all_tilawa_info()

    def on_stack_switcher_button_toggled(self,button):
        if button.props.active:
            self.stack.set_visible_child_name(_("settings"))
        else:
            self.stack.set_visible_child_name(_("download"))



