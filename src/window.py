# window.py
#
# Copyright 2025 yucef sourani
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# SPDX-License-Identifier: GPL-3.0-or-later
from gi.repository import Adw
from gi.repository import Gtk
from gi.repository import GObject,Gio,Gdk,GLib
import albasheerlib.core
import os
from .tafasir_w import TafasirW
from .utl import FONT_SIZE,TilawaPlayer
from .tools_bar import CToolBar
from .tilawa_gui import TilawaGui
from .search_window import search_window
from .copy_gui import make_copy_window

css = b"""
        .amiri {
            color: @success_color;
            font-family:AmiriQuran;
        }
        .amiri_color {
            font-family:AmiriQuranColored ;
        }
        #listv row:selected {
            background-color: #1A1A1A;
            border-style: solid;
            border-width: 1px;
            border-color: gold;
            box-shadow: 0px 0px 15px 5px gold;
            }
        #mainb_t {
            background-color: #1A1A1A;
            }
        #combo_t {
            background-color: #1A1A1A;
            box-shadow: 0px 0px 3px 3px  #00FFFF;
            }
        textview  selection{
            color: gold;

            }
        textview {
            background-color: #1A1A1A;
            }
        #listv  {
            background-color: #1A1A1A;

            }
        Gtkwindow{
        animation-iteration-count: 1;
            animation: burn 1s normal forwards ease-in-out;
            animation: burn 1.5s linear infinite alternate;
            }
@keyframes burn {
  from { box-shadow: -.1em 0 .3em #fefcc9, .1em -.1em .3em #feec85, -.2em -.2em .4em #ffae34, .2em -.3em .3em #ec760c, -.2em -.4em .4em #cd4606, .1em -.5em .7em #973716, .1em -.7em .7em #451b0e; }
  45%  { box-shadow: .1em -.2em .5em #fefcc9, .15em 0 .4em #feec85, -.1em -.25em .5em #ffae34, .15em -.45em .5em #ec760c, -.1em -.5em .6em #cd4606, 0 -.8em .6em #973716, .2em -1em .8em #451b0e; }
  70%  { box-shadow: -.1em 0 .3em #fefcc9, .1em -.1em .3em #feec85, -.2em -.2em .6em #ffae34, .2em -.3em .4em #ec760c, -.2em -.4em .7em #cd4606, .1em -.5em .7em #973716, .1em -.7em .9em #451b0e; }
  to   { box-shadow: -.1em -.2em .6em #fefcc9, -.15em 0 .6em #feec85, .1em -.25em .6em #ffae34, -.15em -.45em .5em #ec760c, .1em -.5em .6em #cd4606, 0 -.8em .6em #973716, -.2em -1em .8em #451b0e; }
}
        """



albasheer_data = os.path.join(GLib.get_user_data_dir(),"albasheer")
audio_data_location = os.path.join(albasheer_data,"ayat_audio")
os.makedirs(audio_data_location,exist_ok=True)
tarajem_data_location = os.path.join(albasheer_data,"ayat_tarajem")
os.makedirs(tarajem_data_location,exist_ok=True)
tafasir_data_location = os.path.join(albasheer_data,"ayat_tafasir")
os.makedirs(tafasir_data_location,exist_ok=True)

class AyaTitle(GObject.GObject):
    __gtype_name__ = 'AyaTitle'
    def __init__(self,aya_number,aya,font_size=False,amiri_color=True,center=False):
        super().__init__()
        self.aya_number  = aya_number
        self.aya         = aya
        self.label = Gtk.Label.new()
        self.label.set_use_markup(True)
        self.label.set_markup(self.aya)
        self.label.props.margin_start = 15
        self.label.set_direction(Gtk.TextDirection.RTL)
        #self.label.props.margin_end   = 10
        #self.label.props.margin_top   = 10
        self.label.set_valign(Gtk.Align.CENTER)
        self.__font_size = font_size
        self.__center = center
        self.__amiri_color = amiri_color
        if self.__center:
            self.label.set_halign(Gtk.Align.CENTER)
        else:
            self.label.set_halign(Gtk.Align.START)
        if self.amiri_color:
            self.label.add_css_class("amiri_color")
        else:
            self.label.add_css_class("amiri")
        self.label.add_css_class(FONT_SIZE[self.__font_size])

        self.label.props.wrap = True

    @GObject.Property(type=bool,default=False)
    def amiri_color(self):
        return self.__amiri_color

    @amiri_color.setter
    def set_amiri_color(self, amiri_color):
        if self.__amiri_color != amiri_color:
            self.__amiri_color = amiri_color
            if amiri_color:
                self.label.remove_css_class("amiri")
                self.label.add_css_class("amiri_color")
            else:
                self.label.remove_css_class("amiri_color")
                self.label.add_css_class("amiri")

    @GObject.Property(type=int,default=0)
    def font_size(self):
        return self.__font_size

    @font_size.setter
    def set_font_size(self, font_size):
        if self.__font_size != font_size:
            self.label.remove_css_class(FONT_SIZE[self.__font_size])
            self.__font_size = font_size
            self.label.add_css_class(FONT_SIZE[font_size])

    @GObject.Property(type=bool,default=False)
    def center(self):
        return self.__center

    @center.setter
    def set_center(self, center):
        if self.__center != center:
            self.__center = center
            if center:
                self.label.set_halign(Gtk.Align.CENTER)
            else:
                self.label.set_halign(Gtk.Align.START)


@Gtk.Template(resource_path='/com/github/yucefsourani/albasheer-electronic-quran-browser/window.ui')
class AlbasheerWindow(Adw.ApplicationWindow):
    __gtype_name__ = 'AlbasheerWindow'

    menubutton = Gtk.Template.Child()

    @GObject.Property(type=int,default=0)
    def sura(self):
        return self.__sura

    @sura.setter
    def set_sura(self, sura):
        if self.__sura != sura:
            self.__sura = sura
            self.tilawaplayer.props.sura = sura
            self.tafasirw.tafasirtool.aya_info()
            self.tafasirw.taragemtool.aya_info()
            self.app_settings.set_int("sura",sura)

    @GObject.Property(type=int,default=200)
    def scroll_delay(self):
        return self.__scroll_delay

    @scroll_delay.setter
    def set_scroll_delay(self, scroll_delay):
        if self.__scroll_delay != scroll_delay:
            self.__scroll_delay = scroll_delay

    @GObject.Property(type=int,default=0)
    def aya(self):
        return self.__aya

    @aya.setter
    def set_aya(self, aya):
        if self.__aya != aya:
            self.__aya = aya
            self.tafasirw.tafasirtool.aya_info()
            self.tafasirw.taragemtool.aya_info()
            self.app_settings.set_int("aya",aya)
            self.tilawaplayer.props.aya = aya
            if self.props.sura in (9,1):
                self.toolbar.aya_button.props.label = _("Aya ") + f"{aya+1}"
            else:
                if aya == 0:
                    self.toolbar.aya_button.props.label = _("Aya")
                else:
                    self.toolbar.aya_button.props.label = "Aya " + f"{aya}"


    @GObject.Property(type=bool,default=False)
    def amiri_color(self):
        return self.__amiri_color

    @amiri_color.setter
    def set_amiri_color(self, amiri_color):
        if self.__amiri_color != amiri_color:
            self.__amiri_color = amiri_color
            self.app_settings.set_boolean("amiri-color",amiri_color)

    @GObject.Property(type=int,default=0)
    def font_size(self):
        return self.__font_size

    @font_size.setter
    def set_font_size(self, font_size):
        if self.__font_size != font_size:
            self.__font_size = font_size
            self.app_settings.set_int("font-size",font_size)
            self.tafasirw.tafasirtool.text_v.set_css_classes(["amiri",FONT_SIZE[self.props.font_size]])
            self.tafasirw.taragemtool.text_v.set_css_classes(["amiri",FONT_SIZE[self.props.font_size]])
            #self.tafasirw.tafasirtool.aya_label.set_css_classes(["amiri",FONT_SIZE[self.props.font_size]])
            #self.tafasirw.taragemtool.aya_label.set_css_classes(["amiri",FONT_SIZE[self.props.font_size]])

    @GObject.Property(type=bool,default=False)
    def center(self):
        return self.__center

    @center.setter
    def set_center(self, center):
        if self.__center != center:
            self.__center = center
            self.app_settings.set_boolean("center",center)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        #Gtk.Widget.set_default_direction( Gtk.TextDirection.RTL)
        #self.set_size_request(435, 500)
        self.app_ = self.get_application()
        self.app_.get_style_manager().set_color_scheme(Adw.ColorScheme.PREFER_DARK)
        self.app_settings = Gio.Settings.new_with_path("com.github.yucefsourani.albasheer-electronic-quran-browser" ,"/com/github/yucefsourani/albasheer_electronic_quran_browser/")
        self.__scroll_delay = self.app_settings.get_int("scroll-delay")
        self.app_settings.bind("width", self, "default-width",
                           Gio.SettingsBindFlags.DEFAULT)
        self.app_settings.bind("height", self, "default-height",
                           Gio.SettingsBindFlags.DEFAULT)
        self.app_settings.bind("is-maximized", self, "maximized",
                           Gio.SettingsBindFlags.DEFAULT)
        self.app_settings.bind("is-fullscreen", self, "fullscreened",
                           Gio.SettingsBindFlags.DEFAULT)
        self.app_settings.bind("scroll-delay", self, "scroll_delay",
                           Gio.SettingsBindFlags.DEFAULT)

        style_provider = Gtk.CssProvider()
        style_provider.load_from_data(css)
        Gtk.StyleContext.add_provider_for_display(Gdk.Display().get_default(),
                                                 style_provider,
                                                 Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

        self.__aya   = self.app_settings.get_int("aya")
        self.__sura  = self.app_settings.get_int("sura")
        self.__font_size  = self.app_settings.get_int("font-size")
        self.tilawaplayer = TilawaPlayer(self,audio_data_location)
        self.__amiri_color = self.app_settings.get_boolean("amiri-color")
        self.__center      = self.app_settings.get_boolean("center")

        self.autoscrolling = False
        self.first_time    = True

        self.albasheercore = albasheerlib.core.albasheerCore()
        self.ix = albasheerlib.core.searchIndexer()

        self.copy_window = None

        self.toastoverlay = Adw.ToastOverlay.new()
        self.set_content(self.toastoverlay )

        self.main_l = Gtk.Box.new(Gtk.Orientation.VERTICAL,0)
        self.main_l.props.hexpand = True
        self.main_l.props.vexpand = True
        self.toastoverlay.set_child(self.main_l)

        if self.get_direction() == Gtk.TextDirection.RTL:
            action = Gio.SimpleAction.new("leftstackswitch", None)
            action.connect("activate", self.on_leftstackswitch_action_activate)
            self.app_.set_accels_for_action("win.leftstackswitch", ['<primary>Right'])
            self.add_action(action)

            action = Gio.SimpleAction.new("rightstackswitch", None)
            action.connect("activate", self.on_rightstackswitch_action_activate)
            self.app_.set_accels_for_action("win.rightstackswitch", ['<primary>Left'])
            self.add_action(action)

        else:
            action = Gio.SimpleAction.new("leftstackswitch", None)
            action.connect("activate", self.on_leftstackswitch_action_activate)
            self.app_.set_accels_for_action("win.leftstackswitch", ['<primary>Left'])
            self.add_action(action)

            action = Gio.SimpleAction.new("rightstackswitch", None)
            action.connect("activate", self.on_rightstackswitch_action_activate)
            self.app_.set_accels_for_action("win.rightstackswitch", ['<primary>Right'])
            self.add_action(action)

        action = Gio.SimpleAction.new("autoplay", None)
        action.connect("activate", self.on_auto_play_action_activate)
        self.app_.set_accels_for_action("win.autoplay", ['<primary>o'])
        self.add_action(action)

        action = Gio.SimpleAction.new_stateful("coloring_font", None, GLib.Variant.new_boolean(self.__amiri_color))
        action.connect("activate", self.on_coloring_font_change_activate)
        self.add_action(action)

        action = Gio.SimpleAction.new_stateful("halign_center", None, GLib.Variant.new_boolean(self.__center))
        self.app_.set_accels_for_action(f"win.halign_center", ['<primary>h'])
        action.connect("activate", self.on_halign_center_change_activate)
        self.add_action(action)


        self.font_action = Gio.SimpleAction.new_stateful("radio", GLib.VariantType.new("s"), GLib.Variant.new_string(str(self.__font_size)))
        self.font_action.connect("activate", self.on_font_size_change_activate)
        self.add_action(self.font_action)

        action = Gio.SimpleAction.new("search", None)
        action.connect("activate", self.on_search_action_activate)
        self.app_.set_accels_for_action(f"win.search", ['<primary>s'])
        self.add_action(action)

        action = Gio.SimpleAction.new("copy", None)
        action.connect("activate", self.on_copy_action_activate)
        self.app_.set_accels_for_action(f"win.copy", ['<primary>b'])
        self.add_action(action)

        action = Gio.SimpleAction.new("toolbarshowhide", None)
        action.connect("activate", self.on_show_hide_toolbar_action_activate)
        self.app_.set_accels_for_action("win.toolbarshowhide", ['<primary>t'])
        self.add_action(action)

        action = Gio.SimpleAction.new("fontsizeplus", None)
        action.connect("activate", self.on_font_size_plus_action_activate)
        self.app_.set_accels_for_action("win.fontsizeplus", ['<primary>plus'])
        self.add_action(action)

        action = Gio.SimpleAction.new("fontsizeminus", None)
        action.connect("activate", self.on_font_size_minus_action_activate)
        self.app_.set_accels_for_action("win.fontsizeminus", ['<primary>minus'])
        self.add_action(action)

        action = Gio.SimpleAction.new("autoscroll", None)
        action.connect("activate", self.on_auto_scroll_action_activate)
        self.app_.set_accels_for_action("win.autoscroll", ['<primary>l'])
        self.add_action(action)

        if self.get_direction() != Gtk.TextDirection.RTL:
            action = Gio.SimpleAction.new("autoscroll_plus", None)
            action.connect("activate", self.auto_scroll_speed_up)
            self.app_.set_accels_for_action("win.autoscroll_plus", ['<primary><shift>Right'])
            self.add_action(action)
            action = Gio.SimpleAction.new("autoscroll_minus", None)
            action.connect("activate", self.auto_scroll_speed_down)
            self.app_.set_accels_for_action("win.autoscroll_minus", ['<primary><shift>Left'])
            self.add_action(action)
        else:
            action = Gio.SimpleAction.new("autoscroll_plus", None)
            action.connect("activate", self.auto_scroll_speed_up)
            self.app_.set_accels_for_action("win.autoscroll_plus", ['<primary><shift>Left'])
            self.add_action(action)
            action = Gio.SimpleAction.new("autoscroll_minus", None)
            action.connect("activate", self.auto_scroll_speed_down)
            self.app_.set_accels_for_action("win.autoscroll_minus", ['<primary><shift>Right'])
            self.add_action(action)


        self.make_header()
        self.make_flap()
        self.make_side()
        self.make_ayat()
        self.make_breakpoint()

    def on_auto_scroll_action_activate(self,simple_action, value=None):
        self.auto_scroll_toggle_button.props.active = not self.auto_scroll_toggle_button.props.active

    def on_font_size_plus_action_activate(self,simple_action, value=None):
        new_positon = max(0,list(FONT_SIZE.keys()).index(self.props.font_size) - 1)
        v = GLib.Variant("s",str(new_positon))
        self.on_font_size_change_activate(self.font_action,v)

    def on_font_size_minus_action_activate(self,simple_action, value=None):
        new_positon = min(3,list(FONT_SIZE.keys()).index(self.props.font_size) + 1)
        v = GLib.Variant("s",str(new_positon))
        self.on_font_size_change_activate(self.font_action,v)

    def on_show_hide_toolbar_action_activate(self,simple_action, value=None):
        self.view_tools_toggle_button.props.active = not self.view_tools_toggle_button.props.active

    def on_leftstackswitch_action_activate(self,simple_action, value=None):
        current_visible = self.mstack.get_visible_child_name()
        if current_visible == "mahbox":
            self.mstack.set_visible_child(self.mstack.get_child_by_name("vbox3"))
        elif current_visible == "vbox2":
            self.mstack.set_visible_child(self.mstack.get_child_by_name("mahbox"))
        elif current_visible == "vbox3":
            self.mstack.set_visible_child(self.mstack.get_child_by_name("vbox2"))

    def on_rightstackswitch_action_activate(self,simple_action, value=None):
        current_visible = self.mstack.get_visible_child_name()
        if current_visible == "mahbox":
            self.mstack.set_visible_child(self.mstack.get_child_by_name("vbox2"))
        elif current_visible == "vbox2":
            self.mstack.set_visible_child(self.mstack.get_child_by_name("vbox3"))
        elif current_visible == "vbox3":
            self.mstack.set_visible_child(self.mstack.get_child_by_name("mahbox"))

    def on_auto_play_action_activate(self,simple_action, value=None):
        self.tilawaplayer.props.autoplay = not self.tilawaplayer.props.autoplay

    def on_copy_action_activate(self,simple_action, value=None):
        if not self.copy_window :
            self.copy_window = make_copy_window(self)
        self.copy_window.present(self)

    def on_search_action_activate(self,simple_action, value=None):
        search_window.present(self)

    def on_font_size_change_activate(self,simple_action, value):
        simple_action.change_state(GLib.Variant.new_string(value.get_string()))
        self.props.font_size = int(value.get_string())

    def on_halign_center_change_activate(self,simple_action, value):
        simple_action.change_state(GLib.Variant.new_boolean(not simple_action.get_state()))
        self.props.center = simple_action.get_state()

    def on_coloring_font_change_activate(self,simple_action, value):
        simple_action.change_state(GLib.Variant.new_boolean(not simple_action.get_state()))
        self.props.amiri_color = simple_action.get_state()


    def make_header(self):
        self.header = Adw.HeaderBar.new()
        self.header.pack_end(self.menubutton)
        self.main_l.append(self.header)


        self.tools_revealer = Gtk.Revealer.new()
        self.tools_revealer.set_reveal_child(False)
        self.main_l.append(self.tools_revealer)
        self.toolbar = CToolBar(self)
        self.tools_revealer.set_child(self.toolbar.mainvb)

        self.view_tools_toggle_button = Gtk.ToggleButton.new()
        self.view_tools_toggle_button.props.icon_name = "focus-top-bar-symbolic"
        self.view_tools_toggle_button.bind_property("active",self.tools_revealer, "reveal-child",GObject.BindingFlags.BIDIRECTIONAL )
        self.view_tools_toggle_button.props.active = self.app_settings.get_boolean("toolbar-toggle")
        self.app_settings.bind("toolbar-toggle", self.view_tools_toggle_button, "active",Gio.SettingsBindFlags.DEFAULT)
        self.header.pack_end(self.view_tools_toggle_button)


        self.auto_scroll_hbox = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL)
        self.header.pack_end(self.auto_scroll_hbox)


        autoscroll_speed_minus = Gtk.Button.new_from_icon_name("zoom-out-symbolic")
        autoscroll_speed_minus.connect("clicked",self.auto_scroll_speed_down)
        self.auto_scroll_hbox.append(autoscroll_speed_minus)

        self.auto_scroll_hbox.add_css_class("linked")
        self.auto_scroll_toggle_button = Gtk.ToggleButton.new()
        self.auto_scroll_hbox.append(self.auto_scroll_toggle_button)
        self.auto_scroll_toggle_button.props.icon_name = "media-playlist-repeat-symbolic"
        self.auto_scroll_toggle_button.connect("toggled", self.on_auto_scroll_toggled)

        autoscroll_speed_plus  = Gtk.Button.new_from_icon_name("zoom-in-symbolic")
        autoscroll_speed_plus.connect("clicked",self.auto_scroll_speed_up)
        self.auto_scroll_hbox.append(autoscroll_speed_plus)



        self.mstack = Adw.ViewStack.new()
        self.mstack.set_hexpand(True)
        self.mstack.set_vexpand(True)
        self.main_l.append(self.mstack)

        self.mahbox = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL)
        self.mahbox.set_hexpand(True)
        self.mahbox.set_vexpand(True)

        self.vbox2  = Gtk.Box(orientation = Gtk.Orientation.VERTICAL)
        self.tafasirw = TafasirW(self,tafasir_data_location,tarajem_data_location)
        self.vbox2.append(self.tafasirw.mainvb)
        self.vbox3  = Gtk.Box(orientation = Gtk.Orientation.VERTICAL)

        self.tilawagui = TilawaGui(self,albasheer_data,audio_data_location)
        self.vbox3.append(self.tilawagui.mainvb)

        self.mstack.add_titled_with_icon(self.mahbox,"mahbox","Quran","emote-love-symbolic")
        self.mstack.add_titled_with_icon(self.vbox2,"vbox2","Tafsir/Tarajem","accessories-dictionary-symbolic")
        tilawa_stack_page = self.mstack.add_titled_with_icon(self.vbox3,"vbox3","Tilawa","audio-volume-high-symbolic")
        self.mstack.connect("notify::visible-child-name",self.on_stack_child_visible_changed)
        tilawa_stack_page.set_icon_name(self.tilawagui.tilawasetings.icon_name)
        self.view_switcher_title = Adw.ViewSwitcherTitle.new()
        self.view_switcher_title.set_stack(self.mstack)
        self.header.set_title_widget(self.view_switcher_title)

        self.view_switcher_bar = Adw.ViewSwitcherBar.new()
        self.main_l.append(self.view_switcher_bar)
        self.view_switcher_bar.set_stack(self.mstack)

    def scrool_to_aya(self):
        self.ayatlistbox.scroll_to(self.props.aya,Gtk.ListScrollFlags.FOCUS | Gtk.ListScrollFlags.SELECT  ,None)
        #if  not self.tilawaplayer.props.autoplay:
         #   GLib.timeout_add(500,self.center_scrool)

    """def center_scrool(self):
        scrolled_window = self.ayatlistbox.get_parent()
        scrolled_window.set_propagate_natural_height(True)
        #scrolled_window.get_child().scroll_to_focus(False)
        v = scrolled_window.get_vadjustment()
        current_v = v.get_value()
        upper     = v.get_upper()
        page_s    = v.get_page_size()
        if current_v != 0 :
            height = self.ayatlistbox.get_model().props.selected_item.label.get_height()
            #if height >= page_s:
             #   print("ooooooooooooo")
              #  r = current_v + ((height-page_s)/2)
            #else:
            print(divmod(upper,current_v))
            print(upper)
            #r = upper - (divmod(upper,current_v)[0]*page_s)
            r =  v.get_value() - self.ayatlistbox.get_model().props.selected_item.label.get_height()
            r = r + (v.get_page_size()-self.ayatlistbox.get_model().props.selected_item.label.get_height())#(v.get_page_size()-self.ayatlistbox.get_model().props.selected_item.label.get_height())
            print(current_v)
            print(r)
            print(height)
            #v.set_value(min(r,current_v+(page_s-height)))

            m = v.get_upper() - v.get_page_size()
            n = min(m, v.get_value() +height )
            v.set_value(r)
        return False"""

    def auto_scroll(self):
        scrolled_window = self.ayatlistbox.get_parent()
        v = scrolled_window.get_vadjustment()
        m = v.get_upper() - v.get_page_size()
        n = min(m, v.get_value() + 2 )
        if n == m:
            self.auto_scroll_toggle_button.props.active = False
        v.set_value(n)
        return True

    def make_breakpoint(self):
        breakpoint_c = Adw.BreakpointCondition.new_length(Adw.BreakpointConditionLengthType.MAX_WIDTH ,660, Adw.LengthUnit.SP)
        breakpoint_ = Adw.Breakpoint.new(breakpoint_c)
        breakpoint_.add_setter(self.header,"show_title",False)
        breakpoint_.add_setter(self.view_switcher_bar,"reveal",True)
        breakpoint_.add_setter(self.toolbar.hb,"orientation",Gtk.Orientation.VERTICAL)


        #breakpoint_.add_setter(self.flap,"collapsed",True)
        #breakpoint_.add_setter(self,"auto",True)
        self.add_breakpoint(breakpoint_)
        breakpoint_c = Adw.BreakpointCondition.new_length(Adw.BreakpointConditionLengthType.MIN_WIDTH ,660, Adw.LengthUnit.SP)
        breakpoint_ = Adw.Breakpoint.new(breakpoint_c)
        breakpoint_.add_setter(self.toolbar.hb,"orientation",Gtk.Orientation.HORIZONTAL)
        #breakpoint_.add_setter(self.toolbar.hb,"homogeneous",True)

        self.add_breakpoint(breakpoint_)
        i = self.sidelistbox.get_row_at_index(self.props.sura-1)
        if i:
            b = i.get_child()
        else:
            b = self.sidelistbox.get_row_at_index(0).get_child()
        self.toolbar.sura_button.props.label = b.props.label

        GLib.timeout_add(1000,b.emit,"clicked")
        context = GLib.MainContext().default()
        while context.pending():
            context.iteration(True)

        GLib.timeout_add(2000,self.scrool_to_aya)


    def make_flap(self):
        self.flap = Adw.OverlaySplitView.new()
        self.flap.set_enable_hide_gesture(True)
        self.flap.set_enable_show_gesture(True)
        self.flap.set_max_sidebar_width(150)
        self.flap.set_min_sidebar_width(150)


        self.mahbox.append(self.flap)

        self.side_vbox = Gtk.Box.new(Gtk.Orientation.VERTICAL,5)
        self.flap.set_sidebar(self.side_vbox)
        self.side_vbox.props.vexpand = True
        self.side_scroll_window = Gtk.ScrolledWindow.new()
        self.side_vbox.append(self.side_scroll_window)
        self.side_scroll_window.set_policy(Gtk.PolicyType.NEVER,Gtk.PolicyType.AUTOMATIC)
        self.side_scroll_window.props.vexpand = True

        self.main_scroll_window   = Gtk.ScrolledWindow.new()
        self.main_scroll_window.set_policy(Gtk.PolicyType.NEVER,Gtk.PolicyType.AUTOMATIC)
        self.main_scroll_window.props.hexpand = True
        self.main_scroll_window.props.vexpand = True
        self.flap.set_content(self.main_scroll_window)


    def make_side(self):
        self.current_sura_label = Gtk.Label.new()
        self.current_sura_label.add_css_class("body")
        self.current_sura_label.add_css_class("success")
        self.current_sura_label_button = Gtk.ToggleButton.new()
        self.current_sura_label_button.set_active(self.flap.props.collapsed)
        #self.current_sura_label_button.add_css_class("pill")
        self.current_sura_label_button.bind_property("active",self.flap, "collapsed",GObject.BindingFlags.BIDIRECTIONAL )
        self.app_settings.bind("collapsed", self.current_sura_label_button, "active",Gio.SettingsBindFlags.DEFAULT)
        self.header.pack_start(self.current_sura_label_button)

        self.current_sura_label_image = Gtk.Image.new_from_icon_name("system-search-symbolic")
        self.current_sura_label_box = Gtk.Box.new(Gtk.Orientation.HORIZONTAL,5)
        self.current_sura_label_button.set_child(self.current_sura_label_box)
        self.current_sura_label_box.append(self.current_sura_label_image)
        self.current_sura_label_box.append(self.current_sura_label)


        self.search_sura_entry = Gtk.SearchEntry.new()
        self.search_sura_entry.props.margin_start = 2
        self.search_sura_entry.props.margin_end   = 2
        self.search_sura_entry.props.margin_top   = 5
        self.search_sura_entry.connect("search-changed",self.on_search_sura_entry_active)
        self.side_vbox.prepend(self.search_sura_entry)


        self.sidelistbox = Gtk.ListBox.new()
        #self.sidelistbox.add_css_class("navigation-sidebar")
        self.sidelistbox.set_filter_func(self.on_sura_filter)
        self.side_scroll_window.set_child(self.sidelistbox)

        for sura,sura_number in self.albasheercore.suraIdByName.items():
            b = Gtk.Button.new()
            b.set_has_frame(False)
            b.props.label = sura
            b.add_css_class("amiri")
            b.sura = sura
            b.sura_number = sura_number - 1
            self.sidelistbox.append(b)
            b.connect("clicked",self.on_sura_name_button_clicked)

    def on_stack_child_visible_changed(self,stack,props):
        if stack.props.visible_child_name == "mahbox":
            self.current_sura_label_button.set_visible(True)
            self.toolbar.hb.set_visible(False)
        else:
            self.current_sura_label_button.set_visible(False)
            self.toolbar.hb.set_visible(True)
        if stack.props.visible_child_name == "vbox3":
            self.mstack.get_page(self.mstack.get_child_by_name("vbox3")).set_needs_attention(False)

    def on_search_sura_entry_active(self,searchentry):
        self.sidelistbox.invalidate_filter()

    def on_sura_filter(self,row):
        text = self.search_sura_entry.get_text().strip()
        if not text:
            return True
        button = row.get_child()
        if text in button.sura:
            return True

    def on_sura_name_button_clicked(self,button):
        self.auto_scroll_toggle_button.props.active = False
        self.current_sura_label.set_label(button.sura)
        self.props.sura = button.sura_number #- 1
        self.viewsura(None,self.props.sura)
        self.sidelistbox.select_row(self.sidelistbox.get_row_at_index(self.props.sura-1))
        side_scroll_window_vadjustment = self.side_scroll_window.get_vadjustment() # to set on toggle
        upper = side_scroll_window_vadjustment.get_upper()
        if upper > 0 :
            side_scroll_window_vadjustment.set_value((upper / 114) * (self.props.sura-1))
        self.toolbar.sura_button.props.label = button.props.label
        if self.props.sura in (9,1):
            self.toolbar.aya_button.props.label = _("Aya ") + f"{self.props.aya+1}"
        else:
            if self.props.aya == 0:
                self.toolbar.aya_button.props.label = _("Aya")
            else:
                self.toolbar.aya_button.props.label = _("Aya ") + f"{self.props.aya}"

    def make_ayat(self):
        self.ayatlistbox = Gtk.ListView.new(None,None)
        #self.ayatlistbox = Gtk.GridView.new(None,None)
        #self.ayatlistbox.set_max_columns(1)
        self.ayatlistbox.set_name("listv")
        self.ayatlistbox.set_single_click_activate(False)

        self.main_scroll_window.set_child(self.ayatlistbox)
        #self.main_scroll_window.show()

        self.ayatliststore = Gio.ListStore.new(AyaTitle)
        self.ayatlistmodel = Gtk.SingleSelection.new(self.ayatliststore)
        self.ayatlistmodel.set_autoselect(True)
        self.ayatlistmodel.set_can_unselect(False)

        self.ayatfactory   = Gtk.SignalListItemFactory.new()


        self.ayatlistbox.set_model(self.ayatlistmodel)
        self.ayatlistbox.set_factory(self.ayatfactory)

        self.ayatfactory.connect("bind",self.on_ayat_add_item)
        self.ayatlistmodel.connect("selection_changed",self.on_aya_row_activated)
        #self.ayatlistbox.connect("activate",self.on_aya_row_activated)

    def on_aya_row_activated(self, model, position,n_items):
        self.props.aya = model.get_selected()

    def on_ayat_add_item(self,factory,itemlist):
        item  = itemlist.get_item()
        itemlist.set_child(item.label)

    def viewsura(self, listview,position):
        position += 1
        if  not self.first_time:
            self.props.aya = 0
        self.first_time = False
        print("p : = {}".format(position))
        self.props.sura  = position
        ayatliststore     = self.ayatlistmodel.get_model()
        ayatliststore.remove_all()

        if self.albasheercore.showSunnahBasmala(self.props.sura):
            aya = AyaTitle(0,self.albasheercore.basmala,self.props.font_size,self.props.amiri_color,self.props.center)
            self.bind_property("font_size",aya, "font_size",GObject.BindingFlags.SYNC_CREATE)
            self.bind_property("amiri_color",aya, "amiri_color",GObject.BindingFlags.SYNC_CREATE)
            self.bind_property("center",aya, "center",GObject.BindingFlags.SYNC_CREATE)
            self.ayatliststore.append(aya)
        for j, k in enumerate(self.albasheercore.getSuraIter(self.props.sura)):
            aya = AyaTitle(j,k[0],self.props.font_size,self.props.amiri_color,self.props.center)
            self.bind_property("font_size",aya, "font_size",GObject.BindingFlags.SYNC_CREATE)
            self.bind_property("amiri_color",aya, "amiri_color",GObject.BindingFlags.SYNC_CREATE)
            self.bind_property("center",aya, "center",GObject.BindingFlags.SYNC_CREATE)
            self.ayatliststore.append(aya)


    def on_auto_scroll_toggled(self,b):
        status = b.get_active()
        if status:
            self.autoscrolling = True
            self.source_id = GLib.timeout_add(self.props.scroll_delay, self.auto_scroll)
        else:
            self.autoscrolling = False
            GLib.Source.remove(self.source_id)

    def auto_scroll_speed_up(self,*a):
        if self.autoscrolling:
            self.props.scroll_delay -= 25
            if self.props.scroll_delay<25:
                self.props.scroll_delay = 25
            GLib.Source.remove(self.source_id)
            self.source_id = GLib.timeout_add(self.props.scroll_delay, self.auto_scroll )

    def auto_scroll_speed_down(self,*a):
        if self.autoscrolling:
            self.props.scroll_delay += 25
            if self.props.scroll_delay > 500:
                self.props.scroll_delay = 500
            GLib.Source.remove(self.source_id)
            self.source_id = GLib.timeout_add(self.props.scroll_delay, self.auto_scroll)
