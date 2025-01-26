import gi
from gi.repository import Adw,Gio
from gi.repository import Gtk
from .utl import ALLTILAWAINFO
import os



class TilawaSetings():
    def __init__(self,parent,audio_data_location):
        self.parent              = parent
        self.audio_data_location = audio_data_location

        self.mainvb = Gtk.Box(orientation = Gtk.Orientation.VERTICAL)

        self.settings_page =  Adw.PreferencesPage.new()
        self.settings_page_group =  Adw.PreferencesGroup.new()
        self.settings_page.add(self.settings_page_group)
        self.settings_page_group.set_title(_("Settings For Tilawa"))
        self.mainvb.append(self.settings_page)

        self.stringlist = Gio.ListStore.new(Gtk.StringObject)
        self.single_selection_list_store = Gtk.SingleSelection.new(self.stringlist)
        self.comborow = Adw.ComboRow.new()
        self.parent.app_settings.bind("tilawa", self.comborow, "selected",
                           Gio.SettingsBindFlags.DEFAULT)
        self.comborow.set_model(self.single_selection_list_store)
        self.comborow.add_prefix(Gtk.Image.new_from_icon_name("view-list-symbolic"))
        self.settings_page_group.add(self.comborow)
        self.read_all_tilawa_info()


        volume_scale_icon_hb = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL)
        volume_row = Adw.ActionRow.new()
        self.settings_page_group.add(volume_row)
        volume_row.set_title(_("Volume"))
        self.volume_scale = Gtk.Scale.new_with_range( Gtk.Orientation.HORIZONTAL,0.0,10.0,1.0)
        self.volume_scale.props.hexpand  = True
        self.volume_scale.set_value(self.parent.tilawaplayer.props.volume)
        self.scale_volume_hander = self.volume_scale.connect("value-changed",self.on_volume_changed)
        self.icon_name = self.get_volume_icon_name()
        self.volume_button = Gtk.Button.new_from_icon_name(self.icon_name)
        b_grid = Gtk.Grid.new()
        b_grid.props.valign = Gtk.Align.CENTER
        b_grid.attach(self.volume_button,0,0,50,50)
        self.volume_button.add_css_class("flat")
        self.volume_button.add_css_class("circular")
        self.volume_button.props.vexpand = False
        self.volume_button.props.hexpand = False
        volume_scale_icon_hb.append(self.volume_scale)
        volume_scale_icon_hb.append(b_grid)
        volume_row.add_suffix(volume_scale_icon_hb)


    def on_volume_changed(self,w):
        self.parent.tilawaplayer.props.volume = w.get_value()
        self.icon_name = self.get_volume_icon_name()
        self.volume_button.set_icon_name(self.icon_name)
        self.parent.mstack.get_page(self.parent.mstack.get_child_by_name("vbox3")).set_icon_name(self.icon_name)

    def read_all_tilawa_info(self):
        result = []
        for i in os.listdir(self.audio_data_location):
            result.append(i)
        if result:
            self.stringlist.remove_all()
            old_selected = self.parent.app_settings.get_int("tilawa")
            for k in result:
                self.stringlist.append(Gtk.StringObject.new(k))
            if old_selected <= len(result):
                self.comborow.set_selected(old_selected)
            else:
                self.comborow.set_selected(0)
        return result

    def get_volume_icon_name(self):
        value = int(self.volume_scale.get_value()*10)
        if value <= 0 :
            return "audio-volume-muted-symbolic"
        elif value < 35:
            return "audio-volume-low-symbolic"
        elif value < 70:
            return "audio-volume-medium-symbolic"
        elif value >= 70:
            return "audio-volume-high-symbolic"

