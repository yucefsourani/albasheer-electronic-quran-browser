import gi
gi.require_version('Soup', '3.0')
from gi.repository import Adw
from gi.repository import Gtk,GObject,Gio
from .utl import suwar_info


class CToolBar():
    def __init__(self,parent):
        self.parent = parent

        self.mainvb = Gtk.Box(orientation = Gtk.Orientation.VERTICAL)
        self.mainvb.props.hexpand = False
        self.mainvb.props.vexpand = False
        #self.mainvb.add_css_class("toolbar")



        self.audiohb = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL)
        self.audiohb.add_css_class("linked")
        self.audiohb.props.halign = Gtk.Align.CENTER
        self.mainvb.append(self.audiohb)

        self.back_seek_button = Gtk.Button.new_from_icon_name("media-seek-backward-symbolic")
        self.back_seek_button.add_css_class("suggested-action")
        self.audiohb.append(self.back_seek_button)
        self.back_seek_button.connect("clicked",self.parent.tilawaplayer.back_seek_audio)

        self.play_button = Gtk.Button.new()
        self.play_button.set_icon_name("media-playback-start-symbolic")
        self.play_button.add_css_class("suggested-action")
        self.audiohb.append(self.play_button)
        self.play_button.connect("clicked",self.parent.tilawaplayer.play)

        self.stop_button = Gtk.Button.new()
        self.stop_button.set_icon_name("media-playback-stop-symbolic")
        self.stop_button.add_css_class("suggested-action")
        self.audiohb.append(self.stop_button)
        self.stop_button.connect("clicked",self.parent.tilawaplayer.stop)

        self.forward_seek_button = Gtk.Button.new_from_icon_name("media-seek-forward-symbolic")
        self.forward_seek_button.add_css_class("suggested-action")
        self.audiohb.append(self.forward_seek_button)
        self.forward_seek_button.connect("clicked",self.parent.tilawaplayer.forward_seek_audio)

        #self.audiohb.append(Gtk.Separator.new(Gtk.Orientation.VERTICAL ))


        self.auto_play_button = Gtk.ToggleButton.new()
        self.audiohb.append(self.auto_play_button)
        self.auto_play_button.add_css_class("suggested-action")
        self.auto_play_button.set_icon_name("media-playlist-repeat-symbolic")
        self.auto_play_button.bind_property("active",self.parent.tilawaplayer, "autoplay",GObject.BindingFlags.BIDIRECTIONAL )


        self.hb = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL)
        self.hb.set_visible(False)
        self.hb.add_css_class("toolbar")
        self.hb.props.hexpand = False
        self.hb.props.halign = Gtk.Align.CENTER
        self.mainvb.append(self.hb)

        self.sura_box = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL)
        #self.sura_box.props.hexpand = True
        #self.sura_box.props.margin_start = 5
        #self.sura_box.props.margin_end = 5
        #self.sura_box.props.margin_top = 0
        #self.sura_box.props.margin_bottom = 2
        self.sura_box.props.halign = Gtk.Align.CENTER
        self.sura_box.add_css_class("linked")



        self.hb.append(self.sura_box)
        self.sura_back_button = Gtk.Button.new_from_icon_name("orientation-portrait-left-symbolic")
        self.sura_back_button.add_css_class("suggested-action")
        self.sura_back_button.connect("clicked",self.on_back_sura_clicked)
        self.sura_box.append(self.sura_back_button)
        self.sura_button = Gtk.Button.new()
        self.sura_button.add_css_class("suggested-action")
        self.sura_box.append(self.sura_button)
        self.sura_forward_button = Gtk.Button.new_from_icon_name("orientation-portrait-right-symbolic")
        self.sura_forward_button.add_css_class("suggested-action")
        self.sura_forward_button.connect("clicked",self.on_forward_sura_clicked)
        self.sura_box.append(self.sura_forward_button)




        self.hb.append(Gtk.Separator.new(Gtk.Orientation.VERTICAL ))
        ##############################################
        self.aya_box = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL)
        self.aya_box.props.halign = Gtk.Align.CENTER
        #self.aya_box.props.hexpand = True
        #self.aya_box.props.margin_start = 5
        #self.aya_box.props.margin_end = 5
        #self.aya_box.props.margin_top = 0
        #self.aya_box.props.margin_bottom = 2
        #self.aya_box.props.halign = Gtk.Align.CENTER
        self.aya_box.add_css_class("linked")
        self.hb.append(self.aya_box)
        self.aya_back_button = Gtk.Button.new_from_icon_name("orientation-portrait-left-symbolic")
        self.aya_back_button.add_css_class("suggested-action")
        self.aya_back_button.connect("clicked",self.on_back_aya_clicked)
        self.aya_box.append(self.aya_back_button)
        self.aya_button = Gtk.Button.new()
        if self.parent.props.sura in (9,1):
            self.aya_button.props.label = _("Aya ") + f"{self.parent.props.aya+1}"
        else:
            if self.parent.props.aya == 0:
                self.aya_button.props.label = _("Aya")
            else:
                self.aya_button.props.label = _("Aya ") + f"{self.parent.props.aya}"
        self.aya_button.add_css_class("suggested-action")
        self.aya_box.append(self.aya_button)
        self.aya_forward_button = Gtk.Button.new_from_icon_name("orientation-portrait-right-symbolic")
        self.aya_forward_button.add_css_class("suggested-action")
        self.aya_forward_button.connect("clicked",self.on_forward_aya_clicked)
        self.aya_box.append(self.aya_forward_button)
        #self.hb.append(Gtk.Separator.new(Gtk.Orientation.VERTICAL ))

        if self.parent.get_direction() == Gtk.TextDirection.RTL:
            action = Gio.SimpleAction.new("backsura", None)
            action.connect("activate", self.on_back_sura_clicked)
            self.parent.app_.set_accels_for_action("win.backsura", ['<Alt>Right'])
            self.parent.add_action(action)

            action = Gio.SimpleAction.new("forwardsura", None)
            action.connect("activate", self.on_forward_sura_clicked)
            self.parent.app_.set_accels_for_action("win.forwardsura", ['<Alt>Left'])
            self.parent.add_action(action)
        else:
            action = Gio.SimpleAction.new("backsura", None)
            action.connect("activate", self.on_back_sura_clicked)
            self.parent.app_.set_accels_for_action("win.backsura", ['<Alt>Left'])
            self.parent.add_action(action)

            action = Gio.SimpleAction.new("forwardsura", None)
            action.connect("activate", self.on_forward_sura_clicked)
            self.parent.app_.set_accels_for_action("win.forwardsura", ['<Alt>Right'])
            self.parent.add_action(action)


        action = Gio.SimpleAction.new("backaya", None)
        action.connect("activate", self.on_back_aya_clicked)
        self.parent.app_.set_accels_for_action("win.backaya", ['<Alt>Up'])
        self.parent.add_action(action)

        action = Gio.SimpleAction.new("forwardaya", None)
        action.connect("activate", self.on_forward_aya_clicked)
        self.parent.app_.set_accels_for_action("win.forwardaya", ['<Alt>Down'])
        self.parent.add_action(action)

    def on_back_sura_clicked(self,*a):
        sura = self.parent.props.sura -1
        if sura ==0:
            sura = 114
        self.parent.props.sura = sura
        i = self.parent.sidelistbox.get_row_at_index(self.parent.props.sura-1)
        if i:
            i.get_child().emit("clicked")
            self.sura_button.props.label = i.get_child().props.label

    def on_forward_sura_clicked(self,*a):
        sura = self.parent.props.sura +1
        if sura ==115:
            sura = 1
        self.parent.props.sura = sura
        i = self.parent.sidelistbox.get_row_at_index(self.parent.props.sura-1)
        if i:
            self.sura_button.props.label = i.get_child().props.label
            i.get_child().emit("clicked")


    def on_back_aya_clicked(self,*a):
        aya = self.parent.props.aya -1
        if aya <0:
            aya = int(suwar_info[str(self.parent.props.sura)]) - 1
            if not self.parent.props.sura in (1,9):
                aya += 1
        self.parent.props.aya = aya
        self.parent.scrool_to_aya()

    def on_forward_aya_clicked(self,*a):
        aya = self.parent.props.aya +1
        max_aya = int(suwar_info[str(self.parent.props.sura)])
        if self.parent.props.sura in (1,9):
            max_aya -= 1
        if aya > max_aya:
            aya = 0
        self.parent.props.aya = aya
        self.parent.scrool_to_aya()

