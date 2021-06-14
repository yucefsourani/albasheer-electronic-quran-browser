# -*- coding: UTF-8 -*-
"""
albasheer - Quran browser
gtkUi - gtk user interface for albasheer API
Copyright © 2009-2013, Muayyad Alsadi <alsadi@ojuba.org>
Copyright © 2019-2020, Yucef Sourani <youssef.m.sourani@gmail.com>

        Released under terms of Waqf Public License.
        This program is free software; you can redistribute it and/or modify
        it under the terms of the latest version Waqf Public License as
        published by Ojuba.org.

        This program is distributed in the hope that it will be useful,
        but WITHOUT ANY WARRANTY; without even the implied warranty of
        MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.

        The Latest version of the license can be found on
        "https://ojuba.org/waqf:license"

"""
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gst', '1.0')
import sys, os, os.path, time
import gettext
import json
from gi.repository import Gtk, Gdk, GLib, Pango, GdkPixbuf,Gst,GObject,Gio
from .core import albasheerCore, searchIndexer
import threading
import zipfile
import sqlite3
import re
from urllib import request
import random

Gst.init(None)
windows = sys.platform.startswith('win')
PY2 = sys.version_info[0]==2
BYTE = str if PY2 else bytes

shortcut_main_window_ui = """<?xml version="1.0" encoding="UTF-8"?>
<interface>
  <object class="GtkShortcutsWindow" id="shortcuts-main-win">
    <property name="modal">1</property>
    <child>
      <object class="GtkShortcutsSection">
        <property name="section-name">editor</property>
        <property name="visible">1</property>
        <property name="title" translatable="yes">Main Window</property>
        <child>
          <object class="GtkShortcutsGroup">
            <property name="title" translatable="yes">General</property>
            <child>
              <object class="GtkShortcutsShortcut">
                <property name="title" translatable="yes">Save</property>
                <property name="accelerator">&lt;ctrl&gt;s</property>
              </object>
            </child>
            <child>
              <object class="GtkShortcutsShortcut">
                <property name="title" translatable="yes">Dark Mode</property>
                <property name="accelerator">&lt;ctrl&gt;d</property>
              </object>
            </child>
            <child>
              <object class="GtkShortcutsShortcut">
                <property name="title" translatable="yes">Find</property>
                <property name="accelerator">&lt;ctrl&gt;f</property>
              </object>
            </child>
            <child>
              <object class="GtkShortcutsShortcut">
                <property name="title" translatable="yes">Zoom In</property>
                <property name="accelerator">&lt;ctrl&gt;z</property>
              </object>
            </child>
            <child>
              <object class="GtkShortcutsShortcut">
                <property name="title" translatable="yes">Zoom Out</property>
                <property name="accelerator">&lt;ctrl&gt;x</property>
              </object>
            </child>
            <child>
              <object class="GtkShortcutsShortcut">
                <property name="title" translatable="yes">Popup Menu</property>
                <property name="accelerator">&lt;ctrl&gt;a</property>
              </object>
            </child>            
            <child>
              <object class="GtkShortcutsShortcut">
                <property name="title" translatable="yes">Popup Sura Combo</property>
                <property name="accelerator">&lt;ctrl&gt;e</property>
              </object>
            </child>  
            <child>
              <object class="GtkShortcutsShortcut">
                <property name="title" translatable="yes">Auto Scrolling On/Off</property>
                <property name="accelerator">&lt;ctrl&gt;c</property>
              </object>
            </child>
            <child>##
              <object class="GtkShortcutsShortcut">
                <property name="title" translatable="yes">Auto Scrolling Speed Up</property>
                <property name="accelerator">&lt;ctrl&gt;b</property>
              </object>
            </child>
            <child>
              <object class="GtkShortcutsShortcut">
                <property name="title" translatable="yes">Auto Scrolling Speed Down</property>
                <property name="accelerator">&lt;ctrl&gt;v</property>
              </object>
            </child>
          </object>
        </child>
        <child>
          <object class="GtkShortcutsGroup">
            <property name="title" translatable="yes"></property>
            <child>
              <object class="GtkShortcutsShortcut">
                <property name="title" translatable="yes">Copy Window</property>
                <property name="accelerator">&lt;ctrl&gt;q</property>
              </object>
            </child>
            <child>
              <object class="GtkShortcutsShortcut">
                <property name="title" translatable="yes">Play Audio</property>
                <property name="accelerator">&lt;ctrl&gt;g</property>
              </object>
            </child>
            <child>
              <object class="GtkShortcutsShortcut">
                <property name="title" translatable="yes">Stop Audio</property>
                <property name="accelerator">&lt;ctrl&gt;h</property>
              </object>
            </child>
            <child>
              <object class="GtkShortcutsShortcut">
                <property name="title" translatable="yes">Seek Audio Backward</property>
                <property name="accelerator">&lt;ctrl&gt;Left</property>
              </object>
            </child> 
            <child>
              <object class="GtkShortcutsShortcut">
                <property name="title" translatable="yes">Seek Audio Forward</property>
                <property name="accelerator">&lt;ctrl&gt;Right</property>
              </object>
            </child> 
          </object>
        </child>
      </object>
    </child>
    <child>
      <object class="GtkShortcutsSection">
        <property name="max-height">16</property>
        <property name="visible">1</property>
        <property name="section-name">Tafasir - Tarajem</property>
        <property name="title" translatable="yes">Tafasir - Tarajem</property>
        <child>
          <object class="GtkShortcutsGroup">
            <property name="title" translatable="yes">General</property>
          <child>
              <object class="GtkShortcutsShortcut">
                <property name="title" translatable="yes">Quit</property>
                <property name="accelerator">Escape</property>
              </object>
            </child>
            <child>
              <object class="GtkShortcutsShortcut">
                <property name="title" translatable="yes">Backward Aya</property>
                <property name="accelerator">&lt;ctrl&gt;Left</property>
              </object>
            </child>
            <child>
              <object class="GtkShortcutsShortcut">
                <property name="title" translatable="yes">Forward Aya</property>
                <property name="accelerator">&lt;ctrl&gt;Right</property>
              </object>
            </child>
            <child>
              <object class="GtkShortcutsShortcut">
                <property name="title" translatable="yes">Zoom In</property>
                <property name="accelerator">&lt;ctrl&gt;z</property>
              </object>
            </child>
            <child>
              <object class="GtkShortcutsShortcut">
                <property name="title" translatable="yes">Zoom Out</property>
                <property name="accelerator">&lt;ctrl&gt;x</property>
              </object>
            </child>
            <child>
              <object class="GtkShortcutsShortcut">
                <property name="title" translatable="yes">Play Audio</property>
                <property name="accelerator">&lt;ctrl&gt;f</property>
              </object>
            </child>
            <child>
              <object class="GtkShortcutsShortcut">
                <property name="title" translatable="yes">Stop Audio</property>
                <property name="accelerator">&lt;ctrl&gt;d</property>
              </object>
            </child>
            <child>
              <object class="GtkShortcutsShortcut">
                <property name="title" translatable="yes">Search</property>
                <property name="accelerator">&lt;ctrl&gt;s</property>
              </object>
            </child>
            <child>
              <object class="GtkShortcutsShortcut">
                <property name="title" translatable="yes">Up Tarajem/Tafasir</property>
                <property name="accelerator">&lt;ctrl&gt;Up</property>
              </object>
            </child>
            <child>
              <object class="GtkShortcutsShortcut">
                <property name="title" translatable="yes">Down Tarajem/Tafasir</property>
                <property name="accelerator">&lt;ctrl&gt;Down</property>
              </object>
            </child>
          </object>
        </child>
      </object>
    </child>
  </object>
</interface>
"""
ajzaa = ("1-3","4-6","7-9","10-12","13-15","16-18","19-21","22-24","25-27","28-30")
ALLTILAWAINFO = {"Al-Husary"                    : "Husary_64kbps",
     "Al-Husary - qasr"             : "husary_qasr_64kbps",
     "Al-Husary Mujawwad"           : "Husary_Mujawwad_64kbps",
     "Al-Husary - Teacher"          : "Hussary.teacher_64kbps",
     "Al-Hudhaify"                  : "Hudhaify_64kbps",
     "Ayman Sowaid - Teacher"       : "Ayman_Sowaid_64kbps",
     "Saad Al-Gamdi"                : "Ghamadi_40kbps",
     "AbdullRahman Al-Sudais"       : "Abdurrahmaan_As-Sudais_64kbps",
     "Saud Al-Shoraim"              : "Saood_ash-Shuraym_64kbps",
     "Maher Al-moaqeli"             : "Maher_AlMuaiqly_64kbps",
     "Ahmad Al-ajami"               : "Ahmed_ibn_Ali_al-Ajamy_64kbps",
     "Nasser Al-Qatami"             : "Nasser_Alqatami_128kbps",
     "Mishari Al-efasi"             : "Alafasy_64kbps",
     "Mohammad Jebreil"             : "Muhammad_Jibreel_64kbps",
     "Abdullah Basfar"              : "Abdullah_Basfar_64kbps",
     "Mostafa Ismail"               : "Mostafa_Ismail_128kbps",
     "Mohammad Ayoub"               : "Muhammad_Ayyoub_64kbps",
     "Al-Menshawy"                  : "Minshawy_Murattal_128kbps",
     "Al-Menshawy - Mojawwad"       : "Minshawy_Mujawwad_64kbps",
     "Al-Menshawy - Teacher"        : "Minshawy_Teacher_128kbps",
     "Yasser Salamah"               : "Yaser_Salamah_128kbps",
     "Hani Al-Refaei"               : "Hani_Rifai_192kbps",
     "Al-Tabalawi"                  : "Mohammad_al_Tablaway_64kbps",
     "Abu Baker Al-shatrei"         : "Abu_Bakr_Ash-Shaatree_64kbps",
     "Abdullbaset"                  : "Abdul_Basit_Murattal_64kbps",
     "Abdullbaset - Mojawwad"       : "AbdulSamad_64kbps",
     "Awad Al-Juhanee"              : "Abdullaah_3awwaad_Al-Juhaynee_128kbps",
     "Abdel-Muhsin Al-Qassem"       : "Muhsin_Al_Qasim_192kbps",
     "Khalefa Al-Tunaiji"           : "tunaiji_64kbps",
     "Al-Husari (Warsh)"            : "warsh_husary_64kbps",
     "Ibrahim Al-Dosary (Warsh)"    : "warsh_dossary_128kbps",
     "Yassin Al-Jazaery (Warsh)"    : "warsh_yassin_64kbps",
     "English Translation"          : "English_Walk",
     "Urdu Translation"             : "ur.khan_46kbs"
     }

suwar_info_ = {'1': '7', '2': '286', '3': '200', '4': '176', '5': '120', '6': '165', '7': '206', '8': '75', '9': '129', '10': '109', 
               '11': '123', '12': '111', '13': '43', '14': '52', '15': '99', '16': '128', '17': '111', '18': '110', '19': '98', 
               '20': '135', '21': '112', '22': '78', '23': '118', '24': '64', '25': '77', '26': '227', '27': '93', '28': '88', 
               '29': '69', '30': '60', '31': '34', '32': '30', '33': '73', '34': '54', '35': '45', '36': '83', '37': '182', 
               '38': '88', '39': '75', '40': '85', '41': '54', '42': '53', '43': '89', '44': '59', '45': '37', '46': '35', 
               '47': '38', '48': '29', '49': '18', '50': '45', '51': '60', '52': '49', '53': '62', '54': '55', '55': '78', 
               '56': '96', '57': '29', '58': '22', '59': '24', '60': '13', '61': '14', '62': '11', '63': '11', '64': '18', 
               '65': '12', '66': '12', '67': '30', '68': '52', '69': '52', '70': '44', '71': '28', '72': '28', '73': '20', 
               '74': '56', '75': '40', '76': '31', '77': '50', '78': '40', '79': '46', '80': '42', '81': '29', '82': '19', 
               '83': '36', '84': '25', '85': '22', '86': '17', '87': '19', '88': '26', '89': '30', '90': '20', '91': '15', 
               '92': '21', '93': '11', '94': '8', '95': '8', '96': '19', '97': '5', '98': '8', '99': '8', '100': '11', '101': '11', 
               '102': '8', '103': '3', '104': '9', '105': '5', '106': '4', '107': '7', '108': '3', '109': '6', '110': '3', '111': '5', 
               '112': '4', '113': '5', '114': '6'}
                            
class MprisQuran():
    def __init__(self,parent=None): #HERE
        xml = """<node name="/org/mpris/MediaPlayer2">
          <interface name="org.freedesktop.DBus.Introspectable">
            <method name="Introspect">
              <arg direction="out" name="xml_data" type="s"/>
            </method>
          </interface>
          <interface name="org.freedesktop.DBus.Properties">
            <method name="Get">
              <arg direction="in" name="interface_name" type="s"/>
              <arg direction="in" name="property_name" type="s"/>
              <arg direction="out" name="value" type="v"/>
            </method>
            <method name="GetAll">
              <arg direction="in" name="interface_name" type="s"/>
              <arg direction="out" name="properties" type="a{sv}"/>
            </method>
            <method name="Set">
              <arg direction="in" name="interface_name" type="s"/>
              <arg direction="in" name="property_name" type="s"/>
              <arg direction="in" name="value" type="v"/>
            </method>
            <signal name="PropertiesChanged">
              <arg name="interface_name" type="s"/>
              <arg name="changed_properties" type="a{sv}"/>
              <arg name="invalidated_properties" type="as"/>
            </signal>
          </interface>
          <interface name="org.mpris.MediaPlayer2">
            <method name="Raise"/>
            <method name="Quit"/>
            <annotation name="org.freedesktop.DBus.Property.EmitsChangedSignal" value="false"/>
            <property name="CanQuit" type="b" access="read"/>
            <property name="CanRaise" type="b" access="read"/>
            <property name="Fullscreen" type="b" access="readwrite"/>
            <property name="CanSetFullscreen" type="b" access="read"/>
            <property name="HasTrackList" type="b" access="read"/>
            <property name="Identity" type="s" access="read"/>
            <property name="DesktopEntry" type="s" access="read"/>
            <property name="SupportedUriSchemes" type="as" access="read"/>
            <property name="SupportedMimeTypes" type="as" access="read"/>
          </interface>
          <interface name="org.mpris.MediaPlayer2.Player">
            <method name="Next"/>
            <method name="Previous"/>
            <method name="Pause"/>
            <method name="PlayPause"/>
            <method name="Stop"/>
            <method name="Play"/>
            <method name="Seek">
              <arg direction="in" name="Offset" type="x"/>
            </method>
            <method name="SetPosition">
              <arg direction="in" name="TrackId" type="o"/>
              <arg direction="in" name="Position" type="x"/>
            </method>
            <method name="OpenUri">
              <arg direction="in" name="Uri" type="s"/>
            </method>
            <signal name="Seeked">
              <arg name="Position" type="x"/>
            </signal>
            <property name="PlaybackStatus" type="s" access="read">
              <annotation name="org.freedesktop.DBus.Property.EmitsChangedSignal" value="true"/>
            </property>
            <property name="LoopStatus" type="s" access="readwrite">
              <annotation name="org.freedesktop.DBus.Property.EmitsChangedSignal" value="true"/>
            </property>
            <property name="Rate" type="d" access="readwrite">
              <annotation name="org.freedesktop.DBus.Property.EmitsChangedSignal" value="true"/>
            </property>
            <property name="Shuffle" type="b" access="readwrite">
              <annotation name="org.freedesktop.DBus.Property.EmitsChangedSignal" value="true"/>
            </property>
            <property name="Metadata" type="a{sv}" access="read">
              <annotation name="org.freedesktop.DBus.Property.EmitsChangedSignal" value="true"/>
            </property>
            <property name="Volume" type="d" access="readwrite">
              <annotation name="org.freedesktop.DBus.Property.EmitsChangedSignal" value="false"/>
            </property>
            <property name="Position" type="x" access="read">
              <annotation name="org.freedesktop.DBus.Property.EmitsChangedSignal" value="false"/>
            </property>
            <property name="MinimumRate" type="d" access="read">
              <annotation name="org.freedesktop.DBus.Property.EmitsChangedSignal" value="true"/>
            </property>
            <property name="MaximumRate" type="d" access="read">
              <annotation name="org.freedesktop.DBus.Property.EmitsChangedSignal" value="true"/>
            </property>
            <property name="CanGoNext" type="b" access="read">
              <annotation name="org.freedesktop.DBus.Property.EmitsChangedSignal" value="true"/>
            </property>
            <property name="CanGoPrevious" type="b" access="read">
              <annotation name="org.freedesktop.DBus.Property.EmitsChangedSignal" value="true"/>
            </property>
            <property name="CanPlay" type="b" access="read">
              <annotation name="org.freedesktop.DBus.Property.EmitsChangedSignal" value="true"/>
            </property>
            <property name="CanPause" type="b" access="read">
              <annotation name="org.freedesktop.DBus.Property.EmitsChangedSignal" value="true"/>
            </property>
            <property name="CanSeek" type="b" access="read">
              <annotation name="org.freedesktop.DBus.Property.EmitsChangedSignal" value="true"/>
            </property>
            <property name="CanControl" type="b" access="read">
              <annotation name="org.freedesktop.DBus.Property.EmitsChangedSignal" value="false"/>
            </property>
          </interface>
          <interface name="org.mpris.MediaPlayer2.Playlists">
            <method name="ActivatePlaylist">
              <arg direction="in" name="PlaylistId" type="o"/>
            </method>
            <method name="GetPlaylists">
              <arg direction="in" name="Index" type="u"/>
              <arg direction="in" name="MaxCount" type="u"/>
              <arg direction="in" name="Order" type="s"/>
              <arg direction="in" name="ReverseOrder" type="b"/>
              <arg direction="out" name="Playlists" type="a(oss)"/>
            </method>
            <signal name="PlaylistChanged">
              <arg name="Playlist" type="a(oss)"/>
            </signal>
            <property name="PlaylistCount" type="u" access="read"></property>
            <property name="Orderings" type="as" access="read"></property>
            <property name="ActivePlaylist" type="(b(oss))" access="read"></property>
          </interface>
        </node>"""
        self.parent       = parent
        if not windows:
            self.bus_name     = "org.mpris.MediaPlayer2.Albasheer"
            self.node         = Gio.DBusNodeInfo.new_for_xml(xml)

            self.owner_id = Gio.bus_own_name(
                Gio.BusType.SESSION, 
                self.bus_name,
                Gio.BusNameOwnerFlags.NONE,  # If other has same name, what to do?
                self.on_bus_acquired,
                self.on_name_acquired,
                self.on_name_lost,
            )
        self.playbackstatus = "Stopped"
        self.canquit        = False
        self.volume         = 1.0
        self.firstrun       = True
        self.orderings      = "Alphabetical"
        self.loopstatus     = "Playlist"
        self.shuffle        = False
        self.fullscreen     = False

    def handle_method_call(self,connection, sender, object_path, interface_name, method_name, params, invocation):
        if method_name == "Introspect":
            string_builder = GLib.String()
            self.node.generate_xml(1,string_builder)
            introspect = GLib.Variant( "s", (string_builder.str,)) # tuple with out parameters 
            #https://lazka.github.io/pgi-docs/index.html#Gio-2.0/classes/DBusMethodInvocation.html#Gio.DBusMethodInvocation

        elif method_name == "Play":
            if self.parent.audio_c.get_sensitive():
                GLib.idle_add(self.parent._play_audio)

        elif method_name == "Stop" or method_name == "Pause":
            if self.parent.audio_c.get_sensitive():
                GLib.idle_add(self.parent._stop_audio)
            
        elif method_name == "Raise":
            GLib.idle_add(self.parent.present)
            
        elif method_name == "Previous":
            playagain = self.parent.pipeline2.get_state(Gst.CLOCK_TIME_NONE )[1]==Gst.State.PLAYING
            if playagain:
                GLib.idle_add(self.parent._stop_audio)
            sura_n,aya_n = self.parent.get_sura_aya()
            sura_n += 1
            if self.loopstatus in ("Track","Playlist"):
                if int(suwar_info_[str(sura_n)]) - (aya_n) == int(suwar_info_[str(sura_n)])-1:
                    aya_n  = int(suwar_info_[str(sura_n)])
                    if self.loopstatus == "Playlist":
                        if sura_n == 1:
                            sura_n = 115
                        if self.shuffle:
                            sura_n = random.randrange(1,114)
                            GLib.idle_add(connection.emit_signal,sender, object_path, "org.mpris.MediaPlayer2.Playlists", "ActivePlaylist",GLib.Variant("(oss)",("/org/mpris/MediaPlayer2/Playlists/"+str(sura_n),str(sura_n),"")))
                            row   = self.parent.listbox_.get_row_at_index(sura_n)
                        else:
                            GLib.idle_add(connection.emit_signal,sender, object_path, "org.mpris.MediaPlayer2.Playlists", "ActivePlaylist",GLib.Variant("(oss)",("/org/mpris/MediaPlayer2/Playlists/"+str(sura_n-1),str(sura_n-1),"")))
                            row   = self.parent.listbox_.get_row_at_index(sura_n-2)
                        GLib.idle_add(self.parent.listbox_.select_row,row)
                        GLib.idle_add(self.parent.viewAya,0)
                    else:
                        GLib.idle_add(self.parent.viewAya,aya_n)
                else:
                    aya_n -= 1
                    GLib.idle_add(self.parent.viewAya,aya_n)
                if playagain:
                    GLib.idle_add(self.parent._play_audio)
            else:
                if int(suwar_info_[str(sura_n)]) - (aya_n) == int(suwar_info_[str(sura_n)])-1:
                    return
                else:
                    aya_n -= 1
                    GLib.idle_add(self.parent.viewAya,aya_n)
                    if playagain:
                        GLib.idle_add(self.parent._play_audio)
                    
            
        elif method_name == "Next":
            playagain = self.parent.pipeline2.get_state(Gst.CLOCK_TIME_NONE )[1]==Gst.State.PLAYING
            if playagain:
                GLib.idle_add(self.parent._stop_audio)
            sura_n,aya_n = self.parent.get_sura_aya()
            sura_n += 1

            if self.loopstatus in ("Track","Playlist"):
                if aya_n+1 > int(suwar_info_[str(sura_n)]):
                    aya_n  = 0
                    if self.loopstatus == "Playlist":
                        if sura_n == 114:
                            sura_n = 0
                        if self.shuffle:
                            sura_n = random.randrange(1,114)
                            GLib.idle_add(connection.emit_signal,sender, object_path, "org.mpris.MediaPlayer2.Playlists", "ActivePlaylist",GLib.Variant("(oss)",("/org/mpris/MediaPlayer2/Playlists/"+str(sura_n),str(sura_n),"")))
                        else:
                            GLib.idle_add(connection.emit_signal,sender, object_path, "org.mpris.MediaPlayer2.Playlists", "ActivePlaylist",GLib.Variant("(oss)",("/org/mpris/MediaPlayer2/Playlists/"+str(sura_n+1),str(sura_n+1),"")))
                        row   = self.parent.listbox_.get_row_at_index(sura_n)
                        GLib.idle_add(self.parent.listbox_.select_row,row)
                    else:
                        GLib.idle_add(self.parent.viewAya,aya_n)
                else:
                    aya_n += 1
                    GLib.idle_add(self.parent.viewAya,aya_n)
                if playagain:
                    GLib.idle_add(self.parent._play_audio)
            else:
                if aya_n+1 > int(suwar_info_[str(sura_n)]):
                    return
                else:
                    aya_n += 1
                    GLib.idle_add(self.parent.viewAya,aya_n)
                    if playagain:
                        GLib.idle_add(self.parent._play_audio)
                    
        elif method_name == "PlayPause":
            if self.parent.audio_c.get_sensitive():
                if self.parent.pipeline2.get_state(Gst.CLOCK_TIME_NONE )[1]!=Gst.State.PLAYING:
                    GLib.idle_add(self.parent._play_audio)
                else:
                    GLib.idle_add(self.parent._stop_audio)
                    
        elif method_name == "Quit":
            if self.canquit:
                GLib.idle_add(self.parent.quit)
                
        elif method_name == "ActivatePlaylist":
            index = int(os.path.basename(params.unpack()[0])) - 1
            row   = self.parent.listbox_.get_row_at_index(index)
            GLib.idle_add(self.parent.listbox_.select_row,row)
            
        elif method_name == "GetPlaylists":
            index , maxcount, order , reverseorder  = params.unpack()
            if index <1:
                index = 1
            elif index > maxcount:
                index = maxcount - 1
            if maxcount < 2:
                maxcount = 3
            elif maxcount > 114:
                maxcount = 114
            if reverseorder:
                r_ = []
                for i in list(map(str,range(index,maxcount)))[::-1]:
                    i = str(i)
                    r_.append(("/org/mpris/MediaPlayer2/Playlists/"+i,i,""))
                GLib.idle_add(invocation.return_value,GLib.Variant("a(oss)",(r_,)))
            else:
                r_ = []
                for i  in map(str,range(index,maxcount)):
                    i = str(i)
                    r_.append(("/org/mpris/MediaPlayer2/Playlists/"+i,i,""))
                GLib.idle_add(invocation.return_value,GLib.Variant("a(oss)",(r_,)))
                
    def on_get_property_closure(self,connection,sender, object_path, interface_name, properties_name):
        if properties_name == "PlaybackStatus":
            value = GLib.Variant("s", self.playbackstatus)
            return value
            
        elif properties_name == "Volume":
            v = self.parent.pipeline2.get_property("volume")
            return GLib.Variant("d",v)
            
        elif properties_name == "LoopStatus":
            return GLib.Variant("s",self.loopstatus)
            
        elif properties_name == "Identity":
            return GLib.Variant("s","Albasheer Quran Browser")

        elif properties_name == "DesktopEntry":
            if os.path.isfile(get_correct_path("albasheer.desktop")):
                return GLib.Variant("s","albasheer")
            else:
                exedir = os.path.dirname(sys.argv[0])
                desktop_entry_file_l  = os.path.join(exedir,'..', 'share',"applications")
                if os.path.isfile(os.path.join(desktop_entry_file_l,"albasheer.desktop")):
                    return GLib.Variant("s","albasheer")
                elif os.path.isfile(os.path.join(desktop_entry_file_l,"com.github.yucefsourani.albasheer-electronic-quran-browser.desktop")):
                    return GLib.Variant("s","com.github.yucefsourani.albasheer-electronic-quran-browser")
                else:
                    return GLib.Variant("s","")
            
        elif properties_name == "SupportedUriSchemes":
            return GLib.Variant("as",("",))
            
        elif properties_name == "SupportedMimeTypes":
            return GLib.Variant("as",("",))
            
        elif properties_name == "HasTrackList":
            return GLib.Variant("b",False)
            
        elif properties_name == "CanRaise":
            return GLib.Variant("b",True)
            
        elif properties_name == "CanQuit":
            return GLib.Variant("b",True)

        elif properties_name == "CanSetFullscreen":
            return GLib.Variant("b",True)
            
        elif properties_name == "Fullscreen":
            return GLib.Variant("b",self.fullscreen) 
            
        elif properties_name == "Rate":
            return GLib.Variant("d",1.0)

        elif properties_name == "CanGoNext":
            return GLib.Variant("b",True)
            
        elif properties_name == "CanGoPrevious":
            return GLib.Variant("b",True)
            
        elif properties_name == "CanPlay":
            return GLib.Variant("b",True)
            
        elif properties_name == "CanPause":
            return GLib.Variant("b",True)

        elif properties_name == "Shuffle":
            return GLib.Variant("b",self.shuffle)
        
        elif properties_name == "CanSeek":
            return GLib.Variant("b",False)
            
        elif properties_name == "Metadata":
            return GLib.Variant("a{sv}",{"None":GLib.Variant("s","")})
            
        elif properties_name == "Position":
            return GLib.Variant("x",0)
            
        elif properties_name == "MinimumRate":
            return GLib.Variant("d",1.0)
            
        elif properties_name == "MaximumRate":
            return GLib.Variant("d",1.0)
            
        elif properties_name == "CanControl":
            return GLib.Variant("b",True)
            
        elif properties_name == "PlaylistCount":
            return GLib.Variant("u",114)

        elif properties_name == "Orderings":
            return GLib.Variant("s",self.orderings)
            
        elif properties_name == "ActivePlaylist":
            sura_n,aya_n = self.parent.get_sura_aya()
            self.activeplaylist = "/org/mpris/MediaPlayer2/Playlists/{}".format(sura_n+1)
            return GLib.Variant("o",self.activeplaylist)
            
    def on_set_property_closure(self,connection, sender, object_path, interface_name, propertie_name, params):
        if propertie_name == "Volume":
            v = params.get_double()
            if v<0:
                v=0
            elif v>1.5:
                v = 1.5
            GLib.idle_add(self.parent.pipeline2.set_property,"volume",v)
            return params
            
        elif propertie_name == "Shuffle":
            self.shuffle = params.get_boolean()
            return params
            
        elif propertie_name == "LoopStatus":
            r = params.get_string()
            if r not in ("None","Track","Playlist"):
                r = "None"
            self.loopstatus = r
            return params
            
        elif propertie_name == "Fullscreen":
            self.fullscreen = params.get_boolean()
            if self.fullscreen:
                GLib.idle_add(self.parent.fullscreen)
            else:
                GLib.idle_add(self.parent.unfullscreen)
            return params
        
    def on_bus_acquired(self,connection, name):
        reg_id2 = connection.register_object("/org/mpris/MediaPlayer2", self.node.interfaces[2], self.handle_method_call, self.on_get_property_closure, self.on_set_property_closure)
        reg_id3 = connection.register_object("/org/mpris/MediaPlayer2", self.node.interfaces[3], self.handle_method_call, self.on_get_property_closure, self.on_set_property_closure)
        reg_id4 = connection.register_object("/org/mpris/MediaPlayer2", self.node.interfaces[4], self.handle_method_call, self.on_get_property_closure, self.on_set_property_closure)

    def on_name_acquired(self,connection, name):
        self.connection = connection

    def on_name_lost(self,connection, name):
        Gio.bus_unown_name(self.owner_id)
        
def fix_certifi():
    if getattr(sys, 'frozen',False) and hasattr(sys, '_MEIPASS'):
        import ssl
        if ssl.get_default_verify_paths().cafile is None:
            try:
                import certifi
                cert_l = certifi.where()
                if os.path.isfile(cert_l):
                    os.environ['SSL_CERT_FILE'] = cert_l
                else:
                    os.environ['SSL_CERT_FILE'] = os.path.join(sys._MEIPASS, 'certifi', 'cacert.pem')
            except:
                try:
                    _create_unverified_https_context = ssl._create_unverified_context
                except AttributeError:
                    pass
                else:
                    ssl._create_default_https_context = _create_unverified_https_context
fix_certifi()

class UnpackTilawaZip(threading.Thread):
    def __init__(self,parent,treeview,iter_string,name,target_location="tillawa"):
        threading.Thread.__init__(self)
        self.parent = parent
        self.treeview         = treeview
        self.iter_string      = iter_string
        self.target_location  = get_correct_path(target_location)
        os.makedirs(self.target_location,exist_ok=True)
        self.name             = name
        selection = self.treeview.get_selection()
        sel = selection.get_selected()
        self.list_store = sel[0]
        self.iteer      = sel[1]
        self.j,self.fraction,self.fs,self.isrunning,self.file_l,self.fsize,self.link,self.psize,self.logs = self.list_store[self.iteer]
        
            
    def run(self):
        self.unpack_file(self.file_l)

    def unpack_file(self,source_location):
        if source_location.endswith('.ayt'):
            fun, mode = zipfile.ZipFile, 'r'
        else:
            return False
        GLib.idle_add(self.parent.emit,"log",_("Extract zip file"),self.name,self.iter_string)
        try:
            file_ = fun(source_location, mode)
            try:
                file_.extractall(self.target_location)
            except:
                GLib.idle_add(self.parent.emit,"log",_("Extract zip file failed"),self.name,self.iter_string)
                return False
            finally:
                file_.close()
                
        except:
            GLib.idle_add(self.parent.emit,"log",_("Extract zip file failed"),self.name.iter_string)
            return False
        GLib.idle_add(self.parent.emit,"log",_("Extract zip file Done"),self.name,self.iter_string)
        GLib.idle_add(self.parent.emit,"success")
        return True
        
class DownloadFile(threading.Thread):    
    def __init__(self,parent,list_store,iteer,iter_string,name,target_location,header={"User-Agent":"Mozilla/5.0"}):
        threading.Thread.__init__(self)
        self.parent          = parent
        self.break_          = False
        self.header          = header
        self.list_store      = list_store
        self.iteer           = iteer
        self.name            = name
        self.target_location = target_location
        self.iter_string     = iter_string
        self.j,self.fraction,self.fs,self.isrunning,self.file_l,self.fsize,self.link,self.psize,self.logs = self.list_store[self.iteer]
        
    def run(self):
        self.break_ = False
        ch = 64*1024 
        try:
            if self.psize == 0:
                mode = "wb"
                os.makedirs(os.path.dirname(self.file_l),exist_ok=True)
            else:
                mode = "ab"
            with open(self.file_l, mode) as op:
                if "Range" in self.header.keys():
                    self.header["Range"] = "bytes={}-{}".format(self.psize,self.fsize)
                else:
                    self.header.setdefault("Range", "bytes={}-{}".format(self.psize,self.fsize))
                
                url   = request.Request(self.link,headers=self.header)
                opurl = request.urlopen(url,timeout=10)
                GLib.idle_add(self.parent.emit,"changedata",self.j,self.fraction,False,True,self.file_l,self.fsize,self.link,self.psize,_("Downloading..."),self.name,self.iter_string)
                while True:
                    if self.break_:
                        GLib.idle_add(self.parent.emit,"changedata",self.j,self.fraction,self.fraction>=100,False,self.file_l,self.fsize,self.link,self.psize,_("Download Canceled"),self.name,self.iter_string)
                        try:
                            opurl.close()
                            op.close()
                        except Exception as e:
                            pass
                        return
                    
                    if self.psize >=int(self.fsize):
                        break
                    n = int(self.fsize)-self.psize
                    if n<ch:
                        ch = n

                    self.fraction = int((self.psize*100)//int(self.fsize))
                    op.write(opurl.read(ch))
                    op.flush()
                    self.psize += ch
                    GLib.idle_add(self.parent.emit,"pulse",self.fraction,self.name,self.iter_string)
                
            GLib.idle_add(self.parent.emit,"changedata",self.j,100,True,False,self.file_l,self.fsize,self.link,self.psize,_("Download Done"),self.name,self.iter_string)
            GLib.idle_add(self.parent.emit,"log",_("Extract zip file"),self.name,self.iter_string)
            try:
                file_ = zipfile.ZipFile(self.file_l, 'r')
                try:
                    file_.extractall(self.target_location)
                except:
                    GLib.idle_add(self.parent.emit,"log",_("Extract zip file failed"),self.name,self.iter_string)
                    return False
                finally:
                    file_.close()
                    
            except:
                GLib.idle_add(self.parent.emit,"log",_("Extract zip file failed"),self.name.iter_string)
                return False
            GLib.idle_add(self.parent.emit,"log",_("Extract zip file Done"),self.name,self.iter_string)
            GLib.idle_add(self.parent.emit,"success")
        except Exception as e:
            GLib.idle_add(self.parent.emit,"changedata",self.j,self.fraction,self.fraction>=100,False,self.file_l,self.fsize,self.link,self.psize,str(e),self.name,self.iter_string)
            print(e)
        finally:
            try:
                opurl.close()
                op.close()
            except Exception as e:
                pass

        
class DownloadTilawaWindow(Gtk.Window):
    __gsignals__ = { "success"     : (GObject.SignalFlags.RUN_LAST, None, ()),
                     "changedata"  : (GObject.SignalFlags.RUN_LAST, None, (str,int,bool,bool,str,int,str,int,str,str,str)),
                     "pulse"       : (GObject.SignalFlags.RUN_LAST, None, (int,str,str)),
                     "log"         : (GObject.SignalFlags.RUN_LAST, None, (str,str,str))
    }
    def __init__(self,parent,download_location="Downloads_f",json_files_location="tilawa_json_files",audio_data_location=""):
        Gtk.Window.__init__(self)
        self.parent = parent
        #self.set_type_hint(Gdk.WindowTypeHint.UTILITY)
        #self.set_modal(True)
        self.set_deletable(True)
        #self.set_transient_for(self.parent)

        self.set_border_width(10)
        self.set_size_request(800, 600)
        self.__download_location  = get_correct_path(download_location)
        self.__json_files_location = get_correct_path(json_files_location)
        self.audio_data_location = audio_data_location
        self.__all_download_thread = dict()
        self.__all_liststore = dict()
        headerbar = Gtk.HeaderBar()
        headerbar.set_show_close_button(True)
        self.set_titlebar(headerbar)

        img = Gtk.Image.new_from_icon_name("system-search-symbolic", Gtk.IconSize.BUTTON)
        self.search_b = Gtk.Button()
        self.search_b.set_tooltip_text(_("Search"))
        self.search_b.add(img)
        self.search_b.connect("clicked", self._on_search_button_clicked)
        headerbar.pack_start(self.search_b)

        open_button = Gtk.Button()
        open_button.get_style_context().add_class("destructive-action")
        open_button.props.label = _("Open Downloads Save Location")
        open_button.connect("clicked",self.on_open_data_location_button_clicked)
        headerbar.pack_end(open_button)

        self.revealer     = Gtk.Revealer()
        self.revealer.set_transition_type(Gtk.RevealerTransitionType.SLIDE_LEFT)

        self.__old_search_text = ""
        self.search_entry = Gtk.SearchEntry(placeholder_text= _("Search..."))
        self.search_entry.props.margin_start  = 15
        self.search_entry.props.margin_end    = 15
        self.search_entry.props.margin_top    = 5
        self.search_entry.props.margin_bottom = 5
        self.search_entry.props.max_length    = 30
        #self.search_entry.set_size_request (100, 1)
        self.revealer.add(self.search_entry)
        headerbar.pack_start(self.revealer)
        

        
        mainvbox = Gtk.VBox()
        self.add(mainvbox)
        mainhbox = Gtk.HBox()
        mainvbox.pack_start(mainhbox,True,True,0)
        
        stack = Gtk.Stack()
        stack.set_hexpand(True)
        stack.set_vexpand(True)
        
        stack_switcher = Gtk.StackSidebar()
        stack_switcher.set_stack(stack)
        mainhbox.pack_start(stack_switcher,False,False,0)
        mainhbox.pack_start(stack,True,True,0)
        
        for i in ALLTILAWAINFO.keys():
            b_ = Gtk.VBox()
            stack.add_titled(b_,i,i)
            liststore = Gtk.ListStore(str,int,bool,bool,str,int,str,int,str)
            self.__all_liststore.setdefault(i,liststore)
            jsonfile = os.path.join(self.__json_files_location,i+".json")
            if os.path.isfile(jsonfile):
                try:
                    with open(jsonfile,"rb") as mf:
                        data = json.load(mf)
                except Exception as e:
                    print(e)
                    data = False
            if data:
                for j,v in data["links_byajzaa"].items():
                    file_name = v[1]
                    file_l    = os.path.join(self.__download_location,i,file_name)
                    file_size = v[2]
                    if os.path.isfile(file_l):
                        current_size = os.path.getsize(file_l)
                    else:
                        current_size = 0
                    
                    fraction = (current_size*100)//file_size
                    if fraction>100:
                        fraction = 100
                    liststore.append([j,fraction,fraction>=100,False,file_l,file_size,v[0],current_size,""])
            
            treeview = Gtk.TreeView(model=liststore)
            b_.pack_start(treeview,True,True,0)
            renderer_text = Gtk.CellRendererText()
            renderer_text.set_property("editable", False)
            renderer_text.set_property("ellipsize", Pango.EllipsizeMode.START)
            
            column_text = Gtk.TreeViewColumn(_("Juz"), renderer_text, text=0)
            column_text.set_resizable(True)
            column_text.set_fixed_width(100)
            column_text.set_min_width(30)
            #column_text.set_max_width(200)
            treeview.append_column(column_text)
            
            renderer_33 = Gtk.CellRendererProgress()

            column_22 = Gtk.TreeViewColumn(_("Progress"),
                    renderer_33, value=1)
            column_22.set_resizable(True)
            column_22.set_min_width(30)
            column_22.set_fixed_width(200)
            treeview.append_column(column_22)
            
            renderer_text1 = Gtk.CellRendererText()
            renderer_text1.set_property("editable", False)
            renderer_text1.set_property("ellipsize", Pango.EllipsizeMode.END)
            
            column_text1 = Gtk.TreeViewColumn(_("Logs"), renderer_text1, text=8)
            column_text1.set_resizable(True)
            column_text1.set_fixed_width(200)
            column_text1.set_min_width(30)
            #column_text.set_max_width(200)
            treeview.append_column(column_text1)
            treeview.connect("row-activated", self.on_row_activated,i)
        
        listbox = stack_switcher.get_child().get_child().get_child()
        listbox.set_filter_func(self.filter_listbox_func)
        
        self.search_entry.connect("search-changed", self._on_search,listbox)
        self.connect("delete-event",self.on_quit)
        self.connect("changedata",self.update_all)
        self.connect("pulse",self.update_progress)
        self.connect("log",self.update_log)
        

    def update_all(self,p,j,fraction,fs,isrunning,file_l,fsize,link,psize,logs,name,iter_string):
        self.__all_liststore[name][self.__all_liststore[name].get_iter_from_string(iter_string)] = [j,fraction,fs,isrunning,file_l,fsize,link,psize,logs]

    def update_progress(self,p,fraction,name,iter_string):
        self.__all_liststore[name][self.__all_liststore[name].get_iter_from_string(iter_string)][1] = fraction
        
    def update_log(self,p,logs,name,iter_string):
        self.__all_liststore[name][self.__all_liststore[name].get_iter_from_string(iter_string)][8] = logs

        
    def on_open_data_location_button_clicked(self,button):
        if  sys.platform.startswith('win'):
            os.system("explorer {}".format(self.__download_location))
        else:
            try:
                Gio.AppInfo.launch_default_for_uri(("file:///"+self.__download_location),None)
            except Exception as e:
                print(e)
                
    def on_row_activated(self,treeview, row, col,name):
        selection = treeview.get_selection()
        sel = selection.get_selected()
        list_store = sel[0]
        iteer      = sel[1]
        if not iteer:
            return
        iter_string = list_store.get_string_from_iter(iteer)
        j,f,fs,isrunning,file_l,fsize,link,psize,logs = list_store[iteer]
        menu = Gtk.Menu()
        menu.set_screen(Gdk.Screen().get_default())
        download_m  = Gtk.MenuItem.new_with_label(_("Download"))
        download_m.connect("activate", self.on_download_clicked,treeview,iter_string,name)
        cancel_m    = Gtk.MenuItem.new_with_label(_("Cancel"))
        cancel_m.connect("activate", self.on_cancel_clicked,file_l)
        self.import_m    = Gtk.MenuItem.new_with_label(_("Import"))
        self.import_m.connect("activate", self.on_import_clicked,treeview,iter_string,name)
        if isrunning:
            download_m.set_sensitive(False)
        else:
            cancel_m.set_sensitive(False)
        
        if fsize!=psize:
            self.import_m.set_sensitive(False)
        else:
            download_m.set_sensitive(False)
        
        menu.append(download_m)
        menu.append(cancel_m)
        menu.append(self.import_m)
        
        menu.show_all()
        self.show_all()
        menu.popup_at_pointer(None)

    def on_import_clicked(self,button,treeview,iter_string,name):
        selection = treeview.get_selection()
        sel = selection.get_selected()
        list_store = sel[0]
        iteer      = sel[1]
        if not iteer:
            return
        t = UnpackTilawaZip(self,treeview,iter_string,name,self.audio_data_location)
        t.setDaemon(True)
        t.start()
            
    def on_cancel_clicked(self,button,file_l):
        if self.__all_download_thread[file_l]:
            self.__all_download_thread[file_l].break_ = True
            del self.__all_download_thread[file_l] 
            
    def on_download_clicked(self,button,treeview,iter_string,name):
        selection = treeview.get_selection()
        sel = selection.get_selected()
        list_store = sel[0]
        iteer      = sel[1]
        if not iteer:
            return
        file_l = list_store[iteer][4]
        t = DownloadFile(self,list_store,iteer,iter_string,name,self.audio_data_location)
        t.setDaemon(True)
        t.start()
        if file_l in self.__all_download_thread.keys():
            self.__all_download_thread[file_l] = t
        else:
            self.__all_download_thread.setdefault(file_l,t)

    def on_quit(self,*argv):
        if threading.active_count()>1:
            check = Yes_Or_No(_("Tasks Running In Background,Are You Sure You Want To Exit?"),self,link_button="")
            check = check.check()
            if  check:
                for i in self.__all_download_thread.values():
                    i.break_ = True
                self.parent.isdownloadwindow = False
            else:
                return True
        self.parent.isdownloadwindow = False

        
    def _on_search(self, entry,listbox):
        listbox.invalidate_filter()
        
    def _on_search_button_clicked(self,button):
        if self.revealer.get_reveal_child():
            self.revealer.set_reveal_child(False)
            self.__old_search_text = self.search_entry.get_text()
            self.search_entry.set_text("") 
        else:
            self.revealer.set_reveal_child(True)
            self.search_entry.set_text(self.__old_search_text)
            self.search_entry.grab_focus_without_selecting()
    
    def filter_listbox_func(self,row):
        text  = self.search_entry.get_text().strip().lower()
        if not text:
            return True
        row_text = row.get_child().props.label.lower()
        if text in row_text:
            return True
            
class searchWindow(Gtk.Window):
    def __init__(self, w):
        Gtk.Window.__init__(self)
        self.w = w
        self.connect('delete-event', lambda w,*a: w.hide() or True)
        self.last_txt = None
        self.set_type_hint(Gdk.WindowTypeHint.UTILITY)
        self.set_modal(True)
        self.set_deletable(True)
        self.set_title(_('Search results'))
        self.set_transient_for(w)
        vb = Gtk.VBox(False,0)
        self.add(vb)
        self.set_position(Gtk.WindowPosition.CENTER_ON_PARENT )
        
        self.search = Gtk.Entry()
        self.search.set_width_chars(15)
        vb.pack_start(self.search, False,False, 0)
        
        self.scroll = Gtk.ScrolledWindow()
        self.scroll.set_policy(Gtk.PolicyType.AUTOMATIC,Gtk.PolicyType.AUTOMATIC)
        self.scroll.set_size_request(100, 250)
        vb.pack_start(self.scroll,True, True, 6)
        
        self.ls = Gtk.ListStore(int,str,int,int)
        self.cells = []
        self.cols = []
        self.cells.append(Gtk.CellRendererText())
        self.cols.append(Gtk.TreeViewColumn(_('Sura'), self.cells[0], text=1))
        self.cols[0].set_sizing(Gtk.TreeViewColumnSizing.AUTOSIZE)
        self.cols[0].set_resizable(True)

        self.cells.append(Gtk.CellRendererText()); # self.cols[-1].set_expand(False)
        self.ls_w = Gtk.TreeView(self.ls)
        self.ls_w.connect("cursor-changed", self.move)
        self.ls_w.set_direction(Gtk.TextDirection.RTL)
        self.ls_w.set_headers_visible(False)
        for i in self.cols:
            self.ls_w.insert_column(i, -1)
        self.scroll.add(self.ls_w)
        self.search.connect("activate", self.search_cb)
        self.show_all()
        self.connect("key-press-event", self._on_key_press)

    def _on_key_press(self,widget, event):
        if event.keyval == Gdk.KEY_Escape :
            self.hide()
            
    def move(self, t):
        a = self.ls_w.get_selection().get_selected()
        if not a or len(a) < 2 or not a[1]:
            return
        sa = self.ls[self.ls.get_path(a[1])]
        self.w.sura_c.set_active(sa[2]-1)
        self.w.viewAya(sa[3], sa[2])

    def search_cb(self, b, *a):
        t = b.get_text()
        self.w.search.set_text(t)
        self.find(t)

    def find(self, txt, backward = False):
        txt = txt.strip()
        if not txt:
            self.hide()
            return
        if type(txt) == BYTE:
            txt = txt.decode('utf-8')
        if txt == self.last_txt:
            # TODO: just move cursor to next/prev result before showing it
            pass
        else:
            self.search.set_text(txt)
            self.last_txt = txt
            self.ls.clear()
            for i in self.w.ix.findPartial(txt.split()):
                sura, aya = self.w.suraAyaFromAyaId(i)
                name = self.w.suraInfoById[sura-1][0]
                self.ls.append([i, "%03d %s - %03d" % (sura, name, aya), sura, aya,])
            self.ls_w.set_cursor(Gtk.TreePath(path=0), None, False)
        self.show_all()

###############################################################################

class ShowTarajemTafasir(Gtk.Window):
    def __init__(self, w=None,tafasir_data_location=None,tooltip="",add_title="",title_="",sura_n=1,aya_n=1,sura="",aya="",msg_if_faild = "",all_audio=None,istarajem=True):
        Gtk.Window.__init__(self)
        self.w            = w
        self.tafasir_data_location = tafasir_data_location
        self.tooltip      = tooltip
        self.add_title    = add_title
        self.sura_n       = sura_n
        self.aya_n        = aya_n
        self.CONST_AYA    = self.aya_n
        self.sura         = sura
        self.aya          = aya
        self.msg_if_faild = msg_if_faild
        self.title_       = title_
        self.__all_audio  = all_audio
        self.istarajem    = istarajem
        self.cleanr       = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
        self.isavailable  = False
        self._all         = True
        self.set_size_request(600, 400)
        self.max_sura_number = suwar_info_[str(self.sura_n)]
        self.pipeline = Gst.ElementFactory.make("playbin", "player")
        
        self.set_position(Gtk.WindowPosition.CENTER_ON_PARENT )

        self.w.set_sensitive(False)
        self.set_deletable(True)
        self.set_title(self.title_)
        self.resize(self.w._current_tarajem_tafasir_window_width,self.w._current_tarajem_tafasir_window_height)
        
        self.header=Gtk.HeaderBar()
        self.header.set_show_close_button(True)
        self.headerhbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.header.pack_start(self.headerhbox)
        self.set_titlebar(self.header)
        img = Gtk.Image.new_from_icon_name("list-add-symbolic", Gtk.IconSize.BUTTON)
        self.add_tafasir = Gtk.Button()
        self.add_tafasir.set_tooltip_text(self.tooltip)
        self.add_tafasir.add(img)
        self.headerhbox.pack_start(self.add_tafasir, False, False, 0)
        self.add_tafasir.connect("clicked", self._on_add_tafasir_clicked)


        self.maincontainer = Gtk.VBox()
        self.add(self.maincontainer)
        self.connect("key-press-event", self._on_key_press)
        self.connect('delete-event', self._on_delete_event)
        self.__all_tafasir = self.get_all_tafasir_location()
        self.albasheercore = albasheerCore()
        self.gui_()

    def _stop_audio(self,button=False):
        if not self.stop_b.get_sensitive():
            return 
        self.pipeline.set_state(Gst.State.NULL)

    def _play_audio(self,button=False):
        if not self.play_b.get_sensitive():
            return 
        self._stop_audio()
        aya   = self.aya_n
        sura  = self.sura_n
        aya_  = str(aya)
        sura_ = str(sura)
        q = self.__all_audio[self.audio_c.get_active_text()]

        if aya==0 and sura not in (9,1) :
            q = os.path.join(q,"001001.mp3")
        else:
            s_ = ("0"*(3-len(sura_)))+sura_
            a_ = ("0"*(3-len(aya_)))+aya_
            #q = os.path.join(q,sura_.zfill(4-len(sura_))+aya_.zfill(4-len(aya_))+".mp3")
            q = os.path.join(q,s_+a_+".mp3")
        if not os.path.isfile(q):
            return
        
        if  sys.platform.startswith('win'):
            q =  "file:///"+os.path.abspath(q).replace(os.sep, '/')
        else:
            q = "file://"+os.path.abspath(q)

        self.pipeline.set_property('uri',q)
        self.pipeline.set_state(Gst.State.PLAYING)


    def _on_add_tafasir_clicked(self,button):
        self.add_w = AddData(self,self.tafasir_data_location,self.add_title,self.istarajem)
        self.add_w.set_title(self.add_title)
        self.add_w.connect("success",self._on_add_tafasir_success)
        
    def _on_add_tafasir_success(self,w=None):
        self.__all_tafasir = self.get_all_tafasir_location()
        #self.add_w.destroy()
        self.gui_()
        #width , height = self.get_size()
        #self.add_w.destroy()
        #self.destroy()
        #s_ = ShowTarajemTafasir(self.w,self.tafasir_data_location,self.tooltip,self.add_title,self.title_,self.sura_n,self.aya_n,self.sura,self.aya,self.msg_if_faild)
        #s_.resize(width , height)

    def get_all_tafasir_location(self):
        result = {}
        if not os.path.isdir(self.tafasir_data_location):
            return False
        for dirname,folder,files in os.walk(self.tafasir_data_location):
            for file_ in files:
                if file_.endswith(".db") or file_.endswith(".ayt") or file_.endswith(".sqlite"):
                    result.setdefault(file_.split(".",1)[0],os.path.join(dirname,file_))
        if result:
            return result
        return False

    def on_back_aya(self,button=None):
        entry = self.entry
        entry_handler = self.entry_handler
        listboxrow = self.listbox_ .get_selected_row()
        if not listboxrow:
            return
        if self.aya_n-1==0:
            return
        self.aya_n-=1
        with GObject.Object.handler_block(entry,entry_handler):
            entry.set_text(str(self.aya_n))
            self.aya = self.albasheercore.getAyatIter(self.albasheercore.ayaIdFromSuraAya(self.sura_n,self.aya_n)).fetchall()[0][0]
            t  = listboxrow.get_child().props.label
            db = self.__all_tafasir[t]
            self.aya_info(db,t)
            self.w.viewAya(self.aya_n)
        
    def on_forward_aya(self,button=None):
        entry = self.entry
        entry_handler = self.entry_handler
        listboxrow = self.listbox_ .get_selected_row()
        if not listboxrow:
            return
        if self.aya_n+1>int(self.max_sura_number):
            return
        self.aya_n+=1
        with GObject.Object.handler_block(entry,entry_handler):
            entry.set_text(str(self.aya_n))
            self.aya = self.albasheercore.getAyatIter(self.albasheercore.ayaIdFromSuraAya(self.sura_n,self.aya_n)).fetchall()[0][0]
            t  = listboxrow.get_child().props.label
            db = self.__all_tafasir[t]
            self.aya_info(db,t)
            self.w.viewAya(self.aya_n)


    def on_up_down(self,up=True):
        selected_row = self.listbox_.get_selected_row()
        if selected_row:
            index_current_row = selected_row.get_index()
            if up:
                if index_current_row == 0 :
                    return
                check_row = self.listbox_.get_row_at_index(index_current_row-1)
                if check_row:
                    self.listbox_.select_row(check_row)
            else:
                check_row = self.listbox_.get_row_at_index(index_current_row+1)
                if check_row:
                    self.listbox_.select_row(check_row)
                else:
                    self.listbox_.select_row(self.listbox_.get_row_at_index(0))
                
            
    def on_entry_activate(self,entry):
        text = entry.get_text()
        listboxrow = self.listbox_.get_selected_row()
        if not listboxrow:
            return
        try:
            it = int(text)
        except:
            return
        if it>int(self.max_sura_number) or it==0:
            return
        else:
            self.aya_n = it
            self.aya = self.albasheercore.getAyatIter(self.albasheercore.ayaIdFromSuraAya(self.sura_n,self.aya_n)).fetchall()[0][0]
            t  = listboxrow.get_child().props.label
            db = self.__all_tafasir[t]
            self.aya_info(db,t)
            self.w.viewAya(self.aya_n)

    def _reset_audio(self,b):
        self.aya_n = self.CONST_AYA
        self.entry.set_text(str(self.aya_n))
        self.entry.emit("activate")
        
        
    def gui_(self):
        self.remove(self.maincontainer)
        self.maincontainer.destroy()
        self.maincontainer = Gtk.HBox()
        self.add(self.maincontainer)
        
        if self.sura_n not in (1,9) and self.aya_n==0:
            self.aya_n=1
            self.CONST_AYA = 1
            self.aya = self.albasheercore.getAyatIter(self.albasheercore.ayaIdFromSuraAya(self.sura_n,self.aya_n)).fetchall()[0][0]
            self.w.viewAya(self.aya_n)
            
        if  self.__all_tafasir:
            self.isavailable = True
            if  self._all :
                hb = Gtk.HBox()
                hb.set_spacing(2)
                hb.pack_start(Gtk.VSeparator(), False, False, 6)
                hb.pack_start(Gtk.Label(_("Audio")), False, False, 0)
                self.audio_c = Gtk.ComboBoxText.new()
                self.audio_c.set_wrap_width(5)
                if self.__all_audio:
                    for i in self.__all_audio.keys():
                        self.audio_c.append_text(i)
                    self.audio_c.set_tooltip_text(_("choose a Audio"))
                    if len(self.__all_audio)-1>self.w._current_tarajem_tafasir_audio_combo_active:
                        self.audio_c.set_active(0)
                    else:
                        self.audio_c.set_active(self.w._current_tarajem_tafasir_audio_combo_active)
                else:
                    self.audio_c.set_sensitive(False)
                    self.audio_c.set_tooltip_text(_("No Audio Available"))
                hb.pack_start(self.audio_c, False, False, 0)

            
                img = Gtk.Image.new_from_icon_name("system-search-symbolic", Gtk.IconSize.BUTTON)
                self.search_b = Gtk.Button()
                self.search_b.set_tooltip_text(_("Search"))
                self.search_b.add(img)
                self.search_b.connect("clicked", self._on_search_button_clicked)
                self.header.pack_start(self.search_b)
            
                self.revealer     = Gtk.Revealer()
                self.revealer.set_transition_type(Gtk.RevealerTransitionType.SLIDE_LEFT)
            
                self.__old_search_text = ""
                self.search_entry = Gtk.SearchEntry(placeholder_text=_("Search..."))
                self.search_entry.props.margin_start  = 15
                self.search_entry.props.margin_end    = 15
                self.search_entry.props.margin_top    = 5
                self.search_entry.props.margin_bottom = 5
                self.search_entry.props.max_length    = 30
                #self.search_entry.set_size_request (100, 1)
                self.revealer.add(self.search_entry)
                self.header.pack_start(self.revealer)
            

            
                audiohb = Gtk.HBox()
                audiohb.set_spacing(2)
                img = Gtk.Image.new_from_icon_name("media-playback-start", Gtk.IconSize.BUTTON)
                self.play_b = Gtk.Button()
                self.play_b.set_tooltip_text(_("Play"))
                self.play_b.add(img)
                audiohb.pack_start(self.play_b, False, False, 0)
                self.play_b.connect("clicked", self._play_audio)
        
                img = Gtk.Image.new_from_icon_name("media-playback-stop", Gtk.IconSize.BUTTON)
                self.stop_b = Gtk.Button()
                self.stop_b.set_tooltip_text(_("Stop"))
                self.stop_b.add(img)
                audiohb.pack_start(self.stop_b, False, False, 0)
                self.stop_b.connect("clicked", self._stop_audio)
            
                if not self.__all_audio:
                    self.play_b.set_sensitive(False)
                    self.stop_b.set_sensitive(False)
            
                zoom_in_out_hb = Gtk.HBox()
                zoom_in_out_hb.pack_start(Gtk.VSeparator(),False, False, 6)
                img = Gtk.Image()
                img.set_from_stock(Gtk.STOCK_ZOOM_IN, Gtk.IconSize.BUTTON)
                b = Gtk.Button()
                b.set_tooltip_text(_("Zoom In"))
                b.add(img)
                zoom_in_out_hb.pack_start(b, False, False, 0)
                b.connect("clicked", self.zoomIn)
        
                img = Gtk.Image()
                img.set_from_stock(Gtk.STOCK_ZOOM_OUT, Gtk.IconSize.BUTTON)
                b = Gtk.Button()
                b.set_tooltip_text(_("Zoom Out"))
                b.add(img)
                zoom_in_out_hb.pack_start(b, False, False, 0)
                b.connect("clicked", self.zoomOut)

            
                self.header.pack_start(hb)
                self.header.pack_start(audiohb)
                self.header.pack_start(zoom_in_out_hb)
        
                h = Gtk.HBox()
                h.props.spacing = 10
                self.entry = Gtk.Entry()
                self.entry.set_max_width_chars(3)
                self.entry.set_input_purpose(Gtk.InputPurpose.DIGITS)
                self.entry.set_text(str(self.aya_n))
                self.entry_handler = self.entry.connect("activate",self.on_entry_activate)
                label_aya_number = Gtk.Label()
                label_aya_number.props.label = "/{}".format(self.max_sura_number)
    
                img = Gtk.Image.new_from_icon_name("media-seek-backward" if  not self.get_direction()== Gtk.TextDirection.RTL else "media-seek-forward", Gtk.IconSize.BUTTON)
                self.rewind_b = Gtk.Button()
                self.rewind_b.add(img)
                h.pack_start(self.rewind_b, False, False, 0)
                self.rewind_b.connect("clicked", self.on_back_aya)

                h.pack_start(self.entry, False, False, 0)
                h.pack_start(label_aya_number, False, False, 0)
            
                img = Gtk.Image.new_from_icon_name("media-seek-forward" if  not self.get_direction()== Gtk.TextDirection.RTL else "media-seek-backward", Gtk.IconSize.BUTTON)
                self.forward_b = Gtk.Button()
                self.forward_b.add(img)
                h.pack_start(self.forward_b, False, False, 0)
                self.forward_b.connect("clicked", self.on_forward_aya)

                img = Gtk.Image.new_from_icon_name("edit-undo-symbolic", Gtk.IconSize.BUTTON)
                self.reset_b = Gtk.Button()
                self.reset_b.set_tooltip_text(_("Reset"))
                self.reset_b.add(img)
                self.reset_b.connect("clicked", self._reset_audio)
                
                self.header.pack_end(h)
                self.header.pack_end(self.reset_b)
                
            sw1=Gtk.ScrolledWindow()
            sw1.set_policy(Gtk.PolicyType.AUTOMATIC,Gtk.PolicyType.AUTOMATIC)
            sw2=Gtk.ScrolledWindow()
            sw2.set_policy(Gtk.PolicyType.AUTOMATIC,Gtk.PolicyType.AUTOMATIC)
            
            sw1.set_size_request(150, 1)
        
            paned = Gtk.Paned()
            paned.props.wide_handle = True
            self.maincontainer.pack_start(paned,True,True,0)
            self.listbox_ = Gtk.ListBox()
            sw1.add(self.listbox_)
            paned.add1(sw1)
            self.__check = True
            self.text_v   = Gtk.TextView()
            self.text_v.modify_font(Pango.FontDescription.from_string("Amiri 32"))
            self.text_v.set_hexpand(True)
            self.text_v.set_vexpand(True)
            self.text_v.props.editable = False
            self.text_v.props.cursor_visible = False
            self.text_v.props.justification = Gtk.Justification.CENTER
            self.text_v.props.wrap_mode = Gtk.WrapMode.WORD
            self.buffer   = self.text_v.get_buffer()
            self.text_v_t = self.buffer.create_tag("s",size=self.w._current_tarajem_tafasir_font_size )
            self.buffer.apply_tag(self.text_v_t, self.buffer.get_start_iter(), self.buffer.get_end_iter())
            sw2.add(self.text_v)
            paned.add2(sw2)
            if self.w._current_tarajem_tafasir_paned_position<=0:
                self.w._current_tarajem_tafasir_paned_position = 1
            paned.set_position(self.w._current_tarajem_tafasir_paned_position)
            paned.connect("notify::position",self.__on_paned_position_changed)
            
            if self.istarajem :
                cc = self.w._current_tarajem
            else:
                cc = self.w._current_tafasir
            self.listbox_.connect("row-selected",self.on_selected_row)
            for category in dict(sorted(self.__all_tafasir.items())).keys():
                category_label = Gtk.Label()
                category_label.set_label(category)
                row_ = Gtk.ListBoxRow()
                row_.props.activatable = True
                row_.props.selectable = True
                row_.add(category_label)
                self.listbox_.add(row_)
                if category==cc:
                    self.listbox_.select_row(row_)

            
            if not cc:
                self.listbox_.select_row(self.listbox_.get_row_at_index(0))
            self.listbox_.set_filter_func(self._listbox_filter_func,self.search_entry)
            self.search_entry.connect("search-changed", self._on_search,self.listbox_)
            self._all = False
        else:
            l = Gtk.Label()
            l.props.label = self.msg_if_faild
            self.maincontainer.add(l)

        self.show_all()
    
    def _on_search_button_clicked(self,button):
        if self.revealer.get_reveal_child():
            self.revealer.set_reveal_child(False)
            self.__old_search_text = self.search_entry.get_text()
            self.search_entry.set_text("") 
        else:
            self.revealer.set_reveal_child(True)
            self.search_entry.set_text(self.__old_search_text)
            self.search_entry.grab_focus_without_selecting()
         
    def _listbox_filter_func(self, listbox,entry):
        text = entry.get_text()
        if not text:
            return listbox
        lbl = listbox.get_child().props.label
        if text.lower() in lbl.lower():
            return listbox 
            
    def _on_search(self, entry,listbox):
        listbox.invalidate_filter()
        
    def __on_paned_position_changed(self,paned,props):
        self.w._current_tarajem_tafasir_paned_position = paned.props.position
        
    def zoomOut(self,button=None):
        if self.w._current_tarajem_tafasir_font_size<6000:
            self.w._current_tarajem_tafasir_font_size = 6000
        self.w._current_tarajem_tafasir_font_size -= 500
        self.text_v_t.props.size = self.w._current_tarajem_tafasir_font_size
        self.buffer.apply_tag(self.text_v_t, self.buffer.get_start_iter(), self.buffer.get_end_iter())

        
    def zoomIn(self,button=None):
        if self.w._current_tarajem_tafasir_font_size>30000:
            self.w._current_tarajem_tafasir_font_size = 30000
        self.w._current_tarajem_tafasir_font_size += 500
        self.text_v_t.props.size = self.w._current_tarajem_tafasir_font_size 
        self.buffer.apply_tag(self.text_v_t, self.buffer.get_start_iter(), self.buffer.get_end_iter())
        
    def on_selected_row(self, listbox,listboxrow):
        t  = listboxrow.get_child().props.label
        db = self.__all_tafasir[t]
        self.aya_info(db,t)
        if self.istarajem :
            self.w._current_tarajem = t
        else:
            self.w._current_tafasir = t

        
    def _on_delete_event(self,*argv):
        self.w.set_sensitive(True)
        self.w._current_tarajem_tafasir_window_width,self.w._current_tarajem_tafasir_window_height = self.get_size()
        if self.isavailable:
            self.w._current_tarajem_tafasir_audio_combo_active = self.audio_c.get_active()
            self._stop_audio()
        self.destroy()
        
    def _on_key_press(self,widget, event):
        if event.keyval == Gdk.KEY_Escape :
            self.w.set_sensitive(True)
            self.w._current_tarajem_tafasir_window_width,self.w._current_tarajem_tafasir_window_height = self.get_size()
            if self.isavailable:
                self.w._current_tarajem_tafasir_audio_combo_active = self.audio_c.get_active()
                self._stop_audio()
            self.destroy()
            
        elif self.isavailable:
            if  (event.state & Gdk.ModifierType.CONTROL_MASK) and event.keyval == Gdk.KEY_Left  :
                self.rewind_b.emit("clicked")
                
            elif   (event.state & Gdk.ModifierType.CONTROL_MASK) and event.keyval == Gdk.KEY_Right  :
                self.forward_b.emit("clicked")
                
            elif  (event.state & Gdk.ModifierType.CONTROL_MASK) and event.keyval == Gdk.KEY_z:
                self.zoomIn()
            
            elif  (event.state & Gdk.ModifierType.CONTROL_MASK) and event.keyval == Gdk.KEY_x:
                self.zoomOut()
            
            elif  (event.state & Gdk.ModifierType.CONTROL_MASK) and event.keyval == Gdk.KEY_f:
                self._play_audio()
                
            elif  (event.state & Gdk.ModifierType.CONTROL_MASK) and event.keyval == Gdk.KEY_d:
                self._stop_audio()
            
            elif  (event.state & Gdk.ModifierType.CONTROL_MASK) and event.keyval == Gdk.KEY_Down :
                if self.revealer.get_reveal_child():
                    return
                self.on_up_down(False)
                
            elif  (event.state & Gdk.ModifierType.CONTROL_MASK) and event.keyval == Gdk.KEY_Up:
                if self.revealer.get_reveal_child():
                    return
                self.on_up_down()
                
            elif  (event.state & Gdk.ModifierType.CONTROL_MASK) and event.keyval == Gdk.KEY_s:
                self.search_b.emit("clicked")
            
    def in_text(self,line,end="\n\n"):
        line = line+end
        self.buffer.insert_markup(self.buffer.get_end_iter(),line,-1)


    def clear_text(self):
        start = self.buffer.get_start_iter()
        end = self.buffer.get_end_iter()
        self.buffer.delete(start, end)

    def aya_info(self,db,table,text="text"):
        self.clear_text()
        try:
            conn = sqlite3.connect(db)
            c = conn.cursor()
            c.execute('SELECT {} FROM {} where sura=? and aya=? ;'.format(text,table),(self.sura_n,self.aya_n))
            rows = c.fetchall()
            if rows:
                self.in_text("<span foreground='blue' size='x-large' weight='bold'>{}</span>".format(self.sura))
                self.in_text("<span foreground='red' size='large' weight='bold'>{}</span>".format(self.aya))
                row = rows[0]
                if row:
                    txt = re.sub(self.cleanr, '', row[0].replace("</p>","\n").replace("<br>","\n"))
                    self.in_text("<span foreground='green' size='x-large'>{}</span>".format(txt))
                    #self.show_all()
                    self.__check = True
                    self.text_v_t.props.size = self.w._current_tarajem_tafasir_font_size 
                    self.buffer.apply_tag(self.text_v_t, self.buffer.get_start_iter(), self.buffer.get_end_iter())
        except sqlite3.OperationalError:
            if self.__check:
                self.__check = False
                return self.aya_info(db,table,"tafsir")
            else:
                pass
        except Exception as e:
            print(e)
            return False
        finally :
            if conn:
                conn.close()
                
class UnpackZip(threading.Thread):
    def __init__(self,sources_location,target_location,spinner,parent):
        threading.Thread.__init__(self)
        self.sources_location = sources_location
        self.target_location  = target_location
        self.spinner          = spinner
        self.parent           = parent
        self.daemon           = True

    def run(self):
        GLib.idle_add(self.spinner.start)
        GLib.idle_add(self.parent.set_sensitive,False)
        result = []
        for source_location in self.sources_location:
            result.append(self.unpack_file(source_location))

        if any(result):
            GLib.idle_add(self.parent.emit,"success")
            
        GLib.idle_add(self.spinner.stop)
        GLib.idle_add(self.parent.set_sensitive,True)

    def unpack_file(self,source_location):
        if source_location.endswith('.ayt'):
            fun, mode = zipfile.ZipFile, 'r'
        else:
            return False
        #cwd = getcwd()
        #chdir(os.path.dirname(self.source_location))
        try:
            file_ = fun(source_location, mode)
            try:
                file_.extractall(self.target_location)
            except:
                #os.chdir(cwd)
                return False
            finally:
                file_.close()
                
        except:
            #os.chdir(cwd)
            return False
        #finally:
            #os.chdir(cwd)
        return True

class DownloadDataThread(object):    
    def __init__(self,parent,pparent,revealer,spinner,link,location,unpack_target,download_button,cancel_button,progressbar):
        self.parent          = parent
        self.pparent         = pparent
        self.revealer        = revealer
        self.spinner         = spinner
        self.link            = link
        self.location        = location
        self.unpack_target   = unpack_target
        self.download_button = download_button
        self.cancel_button   = cancel_button
        self.progressbar     = progressbar
        self._break          = False
    
        self.th              = threading.Thread(target=self._start)
        self.th.daemon       = True
        
    def _start(self):
        GLib.idle_add(self.revealer.set_reveal_child,True)
        GLib.idle_add(self.download_button.set_sensitive,False)
        GLib.idle_add(self.parent.choicefile_b.set_sensitive,False)
        GLib.idle_add(self.parent.cansel_b.set_sensitive,False)
        GLib.idle_add(self.cancel_button.set_sensitive,True)
        try:
            url   = request.Request(self.link,headers={"User-Agent":"Mozilla/5.0"})
            opurl = request.urlopen(url,timeout=6)
            try:
                saveas = opurl.headers["Content-Disposition"].split("=",1)[-1]
            except Exception as e:
                #print(e)
                saveas = os.path.basename(opurl.url)
            saveas = os.path.join(self.location,saveas)
            
            size = int(opurl.headers["Content-Length"])
            psize = 0
            with open(saveas, 'wb') as op:
                while True:
                    if self._break:
                        GLib.idle_add(self.progressbar.set_text,_("Cancel clicked...")) ###
                        GLib.idle_add(self.progressbar.set_fraction,0.0)
                        GLib.idle_add(self.download_button.set_sensitive,True)
                        GLib.idle_add(self.parent.choicefile_b.set_sensitive,True)
                        GLib.idle_add(self.parent.cansel_b.set_sensitive,True)
                        GLib.idle_add(self.cancel_button.set_sensitive,False)
                        return 
                    chunk = opurl.read(600)
                    if not chunk:
                        break
                    count = int((psize*100)//size)
                    fraction = count/100
                    op.write(chunk)
                    psize += 600
                    GLib.idle_add(self.progressbar.set_fraction,fraction)
                    GLib.idle_add(self.progressbar.set_text,_("Downloading ")+str(count)+"%") ###
            
            GLib.idle_add(self.progressbar.set_fraction,1.0)
            GLib.idle_add(self.progressbar.set_text,_("Done")) ###
            GLib.idle_add(self.download_button.set_sensitive,True)
            GLib.idle_add(self.parent.choicefile_b.set_sensitive,True)
            GLib.idle_add(self.parent.cansel_b.set_sensitive,True)
            GLib.idle_add(self.cancel_button.set_sensitive,False)
            UnpackZip([saveas],self.unpack_target,self.spinner,self.parent).start()
            
        except Exception as e:
            print(e)
            GLib.idle_add(self.progressbar.set_fraction,0.0)
            GLib.idle_add(self.progressbar.set_text,str(e))
            GLib.idle_add(self.download_button.set_sensitive,True)
            GLib.idle_add(self.parent.choicefile_b.set_sensitive,True)
            GLib.idle_add(self.parent.cansel_b.set_sensitive,True)
            GLib.idle_add(self.cancel_button.set_sensitive,False)
            return False
        return saveas
        
class AddData(Gtk.Window):
    __gsignals__ = {
        "success"     : (GObject.SignalFlags.RUN_LAST, None, ()),
    }
    
    def __init__(self, w=None,audio_data_location="",msg="",istarajem=None):
        Gtk.Window.__init__(self)
        self.w = w
        self.audio_data_location = audio_data_location
        self.set_size_request(600, 400)
        self.__files = []
        self.msg = msg
        self.set_position(Gtk.WindowPosition.CENTER_ON_PARENT )

        self.connect('delete-event', self._on_cancel_button_clicked)
        self.last_txt = None
        self.set_type_hint(Gdk.WindowTypeHint.UTILITY)
        self.set_modal(True)
        self.set_deletable(True)
        self.set_transient_for(w)
        self.downloaddata = False
        vb = Gtk.VBox()
        hb = Gtk.HBox()
        
        linkbutton = Gtk.LinkButton.new_with_label("http://quran.ksu.edu.sa/ayat/?l=ar&pg=patches","http://quran.ksu.edu.sa")
        
        label      = Gtk.Label()
        label.get_style_context().add_class("h2")
        label.set_label(self.msg)
        self.fvbox = Gtk.VBox(spacing=10)
        self.svbox = Gtk.VBox(spacing=10)
        self.fvbox.set_homogeneous(True)
        self.svbox.set_homogeneous(True)
        self.spinner  = Gtk.Spinner()
        
        
        self.choicefile_label = Gtk.Label()
        self.choicefile_label.get_style_context().add_class("h2")
        self.choicefile_label.set_label(_("Select ayt File"))
        self.choicefile_b = Gtk.Button()
        self.choicefile_b.props.label = _("Choose Files")
        self.choicefile_b.connect("clicked",self.on_file_button_clicked)
        

        self.fvbox.pack_start(self.choicefile_label,False,False,0)
        self.svbox.pack_start(self.choicefile_b,False,False,0)

        self.istarajem = istarajem
        if self.istarajem!=None:
            if self.istarajem:
                self.__uri = "http://quran.ksu.edu.sa/ayat/tarajem.ayt"
            else:
                self.__uri = "http://quran.ksu.edu.sa/ayat/tafasir.ayt"
            
            self.download_button = Gtk.Button()
            self.download_button.props.label = _("Download") 
            
            
            self.cancel_button   = Gtk.Button()
            self.cancel_button.props.label = _("Cancel Download")
            self.cancel_button.set_sensitive(False)
            
            self.revealer   = Gtk.Revealer()
            self.progressbar = Gtk.ProgressBar()
            self.progressbar.props.show_text = True
            
            self.download_button.connect("clicked", self.on_download_clicked)
            self.cancel_button.connect("clicked", self.on_cancel_clicked)
            
            self.revealer.add(self.progressbar)
            self.fvbox.pack_start(self.download_button,True,True,0)
            self.svbox.pack_start(self.cancel_button,True,True,0)
            vb.pack_start(self.revealer,True,True,0)
            
            

        self.open_audio_location_button = Gtk.Button()
        self.open_audio_location_button.props.label = _("Open Data Location")
        self.open_audio_location_button.connect("clicked",self.on_open_data_location_button_clicked)
        
        buttonbox = Gtk.HBox()        
        self.cansel_b = Gtk.Button()
        self.cansel_b.props.label = _("Cancel")
        self.cansel_b.connect("clicked",self._on_cancel_button_clicked)
        
        buttonbox.pack_start(self.open_audio_location_button,True,False,0)
        buttonbox.pack_start(self.cansel_b,True,False,0)
        
        vb.pack_start(linkbutton,True,False,0)
        vb.pack_start(label,True,False,0)
        hb.pack_start(self.fvbox,True,False,0)
        hb.pack_start(self.svbox,True,False,0)
        vb.pack_start(hb,True,False,0)
        vb.pack_start(self.spinner,True,False,0)
        vb.pack_start(buttonbox,True,False,0)
        
        
        self.add(vb)
        self.show_all()
        
    def on_download_clicked(self, button):
        self.downloaddata = DownloadDataThread(self,self.w,self.revealer,self.spinner,self.__uri,os.path.dirname(self.audio_data_location),self.audio_data_location,self.download_button,self.cancel_button,self.progressbar)
        self.downloaddata.th.start()
    
    def on_cancel_clicked(self, button):
        self.downloaddata._break = True
        
    def on_file_button_clicked(self, button):
        self.__files.clear()
        dialog = Gtk.FileChooserDialog(_("Please choose a files"), self,
            Gtk.FileChooserAction.OPEN,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
        
        ayt_filter = Gtk.FileFilter.new()
        zip_filter = Gtk.FileFilter.new()
        ayt_filter.set_name("Ayt file")
        zip_filter.set_name("zip file")
        ayt_filter.add_pattern("*ayt")
        zip_filter.add_mime_type("application/zip")
        dialog.add_filter(ayt_filter)
        dialog.add_filter(zip_filter)
        dialog.set_select_multiple(True)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            self._files =  dialog.get_filenames()
            dialog.destroy()
            self.run_ex_zip()
        else:
            dialog.destroy()
        
    def on_open_data_location_button_clicked(self,button):
        if  sys.platform.startswith('win'):
            os.system("explorer {}".format(self.audio_data_location))
        else:
            try:
                Gio.AppInfo.launch_default_for_uri(("file:///"+self.audio_data_location),None)
            except Exception as e:
                print(e)
        
    def run_ex_zip(self):
        if self._files:
            u_ = UnpackZip(self._files,self.audio_data_location,self.spinner,self)
            u_.start()

    def _on_cancel_button_clicked(self,*argv):
        if self.downloaddata:
            self.downloaddata._break = True
        self.destroy()
        
class Yes_Or_No(Gtk.MessageDialog):
    def __init__(self,msg,parent=None,link_button="https://www.amirifont.org"):
        Gtk.MessageDialog.__init__(self,buttons = Gtk.ButtonsType.YES_NO )
        self.props.message_type = Gtk.MessageType.QUESTION
        self.props.text         = msg
        self.p=parent
        self.link_button        = link_button
        if self.p != None:
            self.parent=self.p
            self.set_transient_for(self.p)
            self.set_modal(True)
            self.p.set_sensitive(False)
        else:
            self.set_position(Gtk.WindowPosition.CENTER)
        if self.link_button:
            linkbutton = Gtk.LinkButton.new(self.link_button)
            ma = self.get_message_area()
            ma.pack_start(linkbutton,True,True,0)
        self.show_all()
    def check(self):
        rrun = self.run()
        if rrun == Gtk.ResponseType.YES:
            self.destroy()
            if self.p != None:
                self.p.set_sensitive(True)
            return True
        else:
            if self.p != None:
                self.p.set_sensitive(True)
            self.destroy()
            return False
            
class NInfo(Gtk.MessageDialog):
    def __init__(self,message,parent=None):
        Gtk.MessageDialog.__init__(self,parent,1,Gtk.MessageType.INFO,Gtk.ButtonsType.OK,message)
        self.parent=parent
        if self.parent != None:
            self.set_transient_for(self.parent)
            self.set_modal(True)
            self.parent.set_sensitive(False)
        else:
            self.set_position(Gtk.WindowPosition.CENTER)
            
    def start(self):
        self.run() 
        if self.parent != None:
            self.parent.set_sensitive(True)
        self.destroy()
        return False
        
def get_correct_path(relative_path):
    if getattr(sys, 'frozen',False) and hasattr(sys, '_MEIPASS'):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)
    
def check_amiri_font(window):
    context = window.get_pango_context()
    for fam in context.list_families():
        font_name = fam.get_name().lower()
        if font_name.strip()== "amiri" :
            return True
    return False
###############################################################################

class albasheerUi(Gtk.Window, albasheerCore):
    def __init__(self,albasheer_data):
        Gtk.Window.set_default_icon_name('albasheer')
        Gtk.Window.__init__(self)
        albasheerCore.__init__(self)
        
        ############################
        self.__can_play = True
        self.isdownloadwindow = False
        self.__isfullscreen = False
        self._current_tafasir = ""
        self._current_tarajem = ""
        self._current_tarajem_tafasir_window_width       = 600
        self._current_tarajem_tafasir_window_height      = 400
        self._current_tarajem_tafasir_audio_combo_active = 0
        self._current_tarajem_tafasir_font_size          = 11000
        self._current_tarajem_tafasir_paned_position     = 150
        self.pipeline = Gst.ElementFactory.make("playbin", "player")
        self.pipeline2 = Gst.ElementFactory.make("playbin", "player")
        self.__bus1 = self.pipeline.get_bus()
        self.__bus1.add_signal_watch()
        self.__bus1.connect("message", self.__on_message,True)
        self.__bus2 = self.pipeline2.get_bus()
        self.__bus2.add_signal_watch()
        self.__bus2.connect("message", self.__on_message)
        self.albasheer_data = albasheer_data
        self.audio_data_location = os.path.join(self.albasheer_data,"ayat_audio")
        os.makedirs(self.audio_data_location,exist_ok=True)
        self.tarajem_data_location = os.path.join(self.albasheer_data,"ayat_tarajem")
        os.makedirs(self.tarajem_data_location,exist_ok=True)
        self.tafasir_data_location = os.path.join(self.albasheer_data,"ayat_tafasir")
        os.makedirs(self.tafasir_data_location,exist_ok=True)
 
        
        css = b"""
                .h1 {
                    font-size: 24px;
                }
                .h2 {
                    font-weight: 300;
                    font-size: 18px;
                }
                .h3 {
                    font-size: 11px;
                }
                .h4 {
                    color: alpha (@text_color, 0.7);
                    font-weight: bold;
                    text-shadow: 0 1px @text_shadow_color;
                }
                .h4 {
                    padding-bottom: 6px;
                    padding-top: 6px;
                }
                paned separator.wide {

                    background-image: linear-gradient(to left, transparent, transparent 1px, #999 1px, #999 4px, transparent 4px);
                    background-size: 100% 15%;
                    background-repeat: no-repeat;
                    background-position: center center;
                }
                paned separator.wide:hover {
                    background-image: linear-gradient(to left, transparent, transparent 1px, #555 1px, #555 4px, transparent 4px);
                }
                paned separator.wide:active {
                    background-image: linear-gradient(to left, transparent, transparent 100px, #555 111px, #555 114px, transparent 114px);
                }
                """

        style_provider = Gtk.CssProvider()
        style_provider.load_from_data(css)
        Gtk.StyleContext.add_provider_for_screen(Gdk.Screen.get_default(), style_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        
        if  sys.platform.startswith('win'):
            if not check_amiri_font(self):
                y_or_n = Yes_Or_No(_("Amiri Font Missing!,install amiri font?"),self)
                if y_or_n.check():
                    os.system("cmd /C fontview.exe {}".format(get_correct_path("amiri_font\\Amiri-Regular.ttf")))
                    ninfo_ = NInfo(_("Re-run albasheer"))
                    ninfo_.start()
                    sys.exit()
                else:
                    sys.exit()
        ############################
        
        self.sw = None
        self.lastSearchText = None
        self.lastSearchResult = []
        self.ix = searchIndexer()
        self.set_title(_('albasheer Quran Browser'))
        self.connect("delete_event", self.quit)
        self.connect('destroy', self.quit)
        self.set_default_size(600, 480)
        self.maximize()
        self.clip1 = Gtk.Clipboard.get(Gdk.SELECTION_PRIMARY)
        self.clip2 = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
        self.accel = Gtk.AccelGroup()

        vb = Gtk.VBox(False,0)
        self.add(vb)
        hb = Gtk.HBox(False,2)
        vb.pack_start(hb, False, False, 0)
        
        self.scroll2 = Gtk.ScrolledWindow()
        self.scroll2.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.ALWAYS)
        self.scroll2.connect_after("size-allocate", self.resize_cb)

        self.scroll1 = Gtk.ScrolledWindow()
        self.scroll1.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.ALWAYS)
        self.scroll1.set_size_request (150, 1)

        hb_search_entry   = Gtk.Grid()
        self.search_entry = Gtk.SearchEntry(placeholder_text= _("Search..."))
        self.search_entry.props.margin_start  = 15
        self.search_entry.props.margin_end    = 15
        self.search_entry.props.margin_top    = 5
        self.search_entry.props.margin_bottom = 5
        self.search_entry.props.max_length    = 30
        hb_search_entry.add(self.search_entry)
                
        overl           = Gtk.Overlay()
        self.listbox_vb = Gtk.VBox()
        self.listbox_   = Gtk.ListBox()
        self.listbox_vb.pack_start(hb_search_entry,False,False,0)
        self.listbox_vb.pack_start(self.scroll1,True,True,0)
        self.scroll1.add(self.listbox_)

        
        self.paned     = Gtk.Paned()
        self.paned.props.position    = 0
        self.paned.props.wide_handle = True
        self.paned.add1(self.listbox_vb)
        self.paned.add2(self.scroll2)
        vb.pack_start(self.paned, True, True, 6)
        

        img = Gtk.Image.new_from_icon_name("system-search-symbolic", Gtk.IconSize.BUTTON)
        self.search_b = Gtk.ToggleButton()
        self.search_b.set_tooltip_text(_("Search For Sura"))
        self.search_b.add(img)
        self.search_b_handler = self.search_b.connect("toggled", self._on_search_button_toggled)
        self.paned_handler    = self.paned.connect("notify::position", self._on_paned_position_changed)
        hb.pack_start(self.search_b ,False, False, 5)
        
        cp_b_label = Gtk.Label()
        cp_b_label.props.label = _("Copy To Clipboard")
        self.cp_b = Gtk.Button()
        self.cp_b.set_relief(Gtk.ReliefStyle.NONE)
        self.cp_b .add(cp_b_label)
        self.cp_b .connect("clicked", self.show_cp_dlg)


        hb.pack_start(Gtk.VSeparator(), False, False, 6)
        hb.pack_start(Gtk.Label(_("Sura")), False, False, 0)

        self.sura_ls = tuple("%d. %s" % (i+1,j[0]) for (i,j) in enumerate(self.suraInfoById))
        self.sura_c = Gtk.ComboBoxText.new()
        self.sura_c.set_wrap_width(5)
        for i in self.sura_ls:
            self.sura_c.append_text(i)
            category_label = Gtk.Label()
            category_label.set_label(i)
            row_ = Gtk.ListBoxRow()
            row_.props.activatable = True
            row_.props.selectable = True
            row_.add(category_label)
            self.listbox_.add(row_)
        

        self.sura_c.set_tooltip_text(_("choose a Sura"))
        self.sura_c_handler = self.sura_c.connect("changed", self.sura_changed_cb)
        hb.pack_start(self.sura_c, False, False, 0)
        self.listbox_.set_filter_func(self._listbox_filter_func,self.search_entry)
        self.search_entry_handler  = self.search_entry.connect("search-changed", self._on_search,self.listbox_)
        self.listbox__handler = self.listbox_.connect("row-selected",self.on_selected_row)


        ##############################################################
        hb.pack_start(Gtk.VSeparator(), False, False, 6)
        hb.pack_start(Gtk.Label(_("Audio")), False, False, 0)
        self.__all_audio = self.get_all_audio_location()
        self.audio_c = Gtk.ComboBoxText.new()
        self.audio_c.set_wrap_width(5)
        if self.__all_audio:
            for i in self.__all_audio.keys():
                self.audio_c.append_text(i)
            self.audio_c.set_tooltip_text(_("choose a Audio"))
            self.audio_c.set_active(0)
        else:
            self.audio_c.set_sensitive(False)
            self.audio_c.set_tooltip_text(_("No Audio Available"))
        hb.pack_start(self.audio_c, False, False, 0)

        audiohb = Gtk.HBox()
        audiohb.set_spacing(2)
        img = Gtk.Image.new_from_icon_name("media-seek-backward" if not self.get_direction()== Gtk.TextDirection.RTL else "media-seek-forward", Gtk.IconSize.BUTTON)
        self.rewind_b = Gtk.Button()
        self.rewind_b.set_tooltip_text(_("Previous"))
        self.rewind_b.add(img)
        audiohb.pack_start(self.rewind_b, False, False, 0)
        self.rewind_b.connect("clicked", self.seek_audio,False)
        
        
        
        img = Gtk.Image.new_from_icon_name("media-playback-start" , Gtk.IconSize.BUTTON)
        self.play_b = Gtk.Button()
        self.play_b.set_tooltip_text(_("Play"))
        self.play_b.add(img)
        audiohb.pack_start(self.play_b, False, False, 0)
        self.play_b.connect("clicked", self._play_audio)

        img = Gtk.Image.new_from_icon_name("media-seek-forward" if  not self.get_direction()== Gtk.TextDirection.RTL else "media-seek-backward", Gtk.IconSize.BUTTON)
        self.forward_b = Gtk.Button()
        self.forward_b.set_tooltip_text(_("Forward"))
        self.forward_b.add(img)
        audiohb.pack_start(self.forward_b, False, False, 0)
        self.forward_b.connect("clicked", self.seek_audio)
        
        img = Gtk.Image.new_from_icon_name("media-playback-stop", Gtk.IconSize.BUTTON)
        self.stop_b = Gtk.Button()
        self.stop_b.set_tooltip_text(_("Stop"))
        self.stop_b.add(img)
        audiohb.pack_start(self.stop_b, False, False, 0)
        self.stop_b.connect("clicked", self._stop_audio)
        if not self.__all_audio:
            self.play_b.set_sensitive(False)
            self.stop_b.set_sensitive(False)
            self.rewind_b.set_sensitive(False)
            self.forward_b.set_sensitive(False)
        hb.pack_start(audiohb, False, False, 10)
        
        img = Gtk.Image.new_from_icon_name("list-add-symbolic", Gtk.IconSize.BUTTON)
        self.add_tilawa = Gtk.Button()
        self.add_tilawa.set_tooltip_text(_("Add Audio Sources"))
        self.add_tilawa.add(img)
        hb.pack_start(self.add_tilawa, False, False, 0)
        self.add_tilawa.connect("clicked", self._on_add_tilawa_clicked)
        
        img = Gtk.Image.new_from_icon_name("send-to-symbolic", Gtk.IconSize.BUTTON)
        self.download_tilawa = Gtk.Button()
        self.download_tilawa.set_tooltip_text(_("Download Audio Sources"))
        self.download_tilawa.add(img)
        hb.pack_start(self.download_tilawa, False, False, 0)
        self.download_tilawa.connect("clicked", self._on_download_tilawa_clicked)
        ###############################################################
        
        
        
        hb.pack_start(Gtk.VSeparator(),False, False, 6)
        img = Gtk.Image()
        img.set_from_stock(Gtk.STOCK_ZOOM_IN, Gtk.IconSize.BUTTON)
        b = Gtk.Button()
        b.set_tooltip_text(_("Zoom In"))
        b.add(img)
        hb.pack_start(b, False, False, 0)
        b.connect("clicked", self.zoomIn)
        
        img = Gtk.Image()
        img.set_from_stock(Gtk.STOCK_ZOOM_OUT, Gtk.IconSize.BUTTON)
        b = Gtk.Button()
        b.set_tooltip_text(_("Zoom Out"))
        b.add(img)
        hb.pack_start(b, False, False, 0)
        b.connect("clicked", self.zoomOut)

        srhbox = Gtk.HBox()
        srhbox.set_spacing(1)
        hb.pack_start(srhbox , False, False, 5)
        
        img = Gtk.Image.new_from_icon_name("go-up-symbolic", Gtk.IconSize.BUTTON)
        b = Gtk.Button()
        b.set_tooltip_text(_("Speed Up Auto Scroll"))
        b.add(img)
        b.connect("clicked", self.speed_up)
        srhbox.pack_start(b , False, False, 0)
        
        
        self.__count = 0
        self.scroll_delay = 200
        img = Gtk.Image.new_from_icon_name("media-playlist-repeat-symbolic", Gtk.IconSize.BUTTON)
        self.tb = Gtk.ToggleButton()
        self.tb.set_tooltip_text(_("Auto Scroll"))
        self.tb.add(img)
        srhbox.pack_start(self.tb , False, False, 0)
        self.autoScrolling = False
        self.tb.connect("clicked", self.autoScrollCb)
        self.source_id = GLib.timeout_add(self.scroll_delay, self.autoScroll, self.tb )
        
        
        img = Gtk.Image.new_from_icon_name("go-down-symbolic", Gtk.IconSize.BUTTON)
        b = Gtk.Button()
        b.set_tooltip_text(_("Speed Down Auto Scroll"))
        b.add(img)
        b.connect("clicked", self.speed_down)
        srhbox.pack_start(b , False, False, 0)

        hb.pack_start(Gtk.VSeparator(), False, False, 6)
        hb.pack_start(Gtk.Image.new_from_stock(Gtk.STOCK_FIND, Gtk.IconSize.BUTTON), False, False, 0)
        search = Gtk.Entry(); search.set_width_chars(15)
        search.set_tooltip_text(_("Search"))
        hb.pack_start(search, False,False, 0)
        search.connect("activate", self.search_cb)
        self.search = search

        about_label  = Gtk.Label()
        about_label.props.label = _("About")
        about_b = Gtk.Button()
        about_b.set_relief(Gtk.ReliefStyle.NONE)
        about_b.add(about_label)
        about_b.connect("clicked", lambda *a: self.show_about_dlg(self))


        ############################
        
        darkmode_switch_label  = Gtk.Label()
        darkmode_switch_label.props.label = "Dark Mode"
        defaultsettings = Gtk.Settings.get_default()
        self.darkmode_switch = Gtk.Switch()
        self.darkmode_switch.connect("state_set",self._on_darkmode_switch_state_changed,defaultsettings)
        self.darkmode_switch.props.active = defaultsettings.props.gtk_application_prefer_dark_theme
        #hb.pack_start(Gtk.VSeparator(),False, False, 6)
        
        
        self.color_button_bg = Gtk.ColorButton.new_with_color(Gdk.Color.parse("#fffff8")[-1])
        self.color_button_bg.set_tooltip_text(_("Background Color"))
        self.color_button_fg = Gtk.ColorButton.new_with_color(Gdk.Color.parse("#204000")[-1])
        self.color_button_fg.set_tooltip_text(_("Foreground Color"))
        self.color_button_bg.connect("color_set",self._on_color_set)
        self.color_button_fg.connect("color_set",self._on_color_set,False)
        #hb.pack_start(Gtk.VSeparator(),False, False, 6)
        #hb.pack_start(self.color_button_bg,False, False, 6)
        #hb.pack_start(self.color_button_fg,False, False, 6)
        
    
        shortcut_label  = Gtk.Label()
        shortcut_label.props.label = _("Shortcut")
        shortcut_b = Gtk.Button()
        shortcut_b.set_relief(Gtk.ReliefStyle.NONE)
        shortcut_b.add(shortcut_label)
        shortcut_b.connect("clicked",self.on_shortcut_button_clicked)

        
        
        img = Gtk.Image.new_from_icon_name("open-menu-symbolic", Gtk.IconSize.BUTTON)
        self.setting_menu_b = Gtk.Button()
        #self.setting_menu_b.set_tooltip_text(_(""))
        self.setting_menu_b.add(img)
        self.setting_menu_b.connect("clicked", self.on_setting_menu_b_clicked)

        setting_menu_vbox = Gtk.VBox()
        setting_menu_vbox.props.spacing = 1
        
        setting_menu_hbox = Gtk.HBox()
        setting_menu_hbox.props.spacing = 1
        
        setting_menu_v1   = Gtk.VBox()
        setting_menu_v1.props.homogeneous = True
        setting_menu_v2   = Gtk.VBox()
        setting_menu_v2.props.homogeneous = True
        
        self.menu_popover = Gtk.Popover.new(self.setting_menu_b)
        self.menu_popover.add(setting_menu_vbox)
        
        setting_menu_v1.pack_start(darkmode_switch_label,True, True, 10)
        setting_menu_v2.pack_start(self.darkmode_switch,True, True, 10)

        
        setting_menu_hbox.pack_start(setting_menu_v1,True, True, 10)
        setting_menu_hbox.pack_start(setting_menu_v2,True, True, 10)
        setting_menu_vbox.pack_start(setting_menu_hbox,True, True, 3)
        setting_menu_vbox.pack_start(Gtk.HSeparator(), True, True, 10)
        setting_menu_vbox.pack_start(self.cp_b,False, False, 1)
        setting_menu_vbox.pack_start(shortcut_b,False, False, 1)
        setting_menu_vbox.pack_start(about_b,False, False, 1)
        hb.pack_start(self.setting_menu_b,False, False, 0)
        
        """hb.pack_start(Gtk.VSeparator(), False, False, 6)
        hb.pack_start(Gtk.Label(_("Tarajem")), False, False, 0)
        self.tarajem_c = Gtk.ComboBoxText.new()
        self.tarajem_c.set_wrap_width(5)
        if self.__all_tarajem:
            print(self.__all_tarajem)
            for i in self.__all_tarajem.keys():
                self.tarajem_c.append_text(i)
            #self.tarajem_c.set_tooltip_text(_("choose tarajem"))
            #self.tarajem_c.set_active(0)
        else:
            self.tarajem_c.set_sensitive(False)
            self.tarajem_c.set_tooltip_text(_("No Tarajem Available"))
        hb.pack_start(self.tarajem_c, False, False, 0)"""
        
        ############################
        
        self.scale = 1
        self.txt = Gtk.ListStore(str,int,str)
        self.cells = []
        self.cols = []
        self.cells.append(Gtk.CellRendererText())
        #self.cols.append(Gtk.TreeViewColumn('Quranic Text', self.cells[0], markup=0))
        self.cols.append(Gtk.TreeViewColumn('Quranic Text', self.cells[0], text = 0))
        self.cells[0].set_property("background","#fffff8")
        self.cells[0].set_property("foreground","#204000")
        #self.cells[0].set_property("alignment",Pango.ALIGN_CENTER)
        self.cells[0].set_property("wrap-mode", Pango.WrapMode.WORD)
        # TODO: on-max-min also readjust this value
        self.cells[0].set_property("wrap-width", 300)
        self.cells[0].set_property("font", "Amiri 32")
        #self.cells[0].set_property("font", "Simplified Naskh 32")
        #self.cells[0].set_property("font","KFGQPC Uthmanic Script HAFS 32")
        self.cells[0].set_property("scale", self.scale)
        self.cols[0].set_sizing(Gtk.TreeViewColumnSizing.AUTOSIZE)

        self.cells.append(Gtk.CellRendererText()); # self.cols[-1].set_expand(False)
        self.txt_list = Gtk.TreeView(self.txt)
        self.txt_list.connect("button-press-event",self._on_button_press_event_treeview)
        self.txt_list.set_activate_on_single_click(True)
        self.txt_list.set_hover_selection(Gtk.SelectionMode.NONE   )
        self.txt_list.set_headers_visible(False)
        self.txt_list.set_direction(Gtk.TextDirection.RTL)
        for i in self.cols:
            self.txt_list.insert_column(i, -1)

        self.scroll2.add(self.txt_list)
        
        ##################################################################
        last_sura_aya = self.get_last_sura_aya()
        
        mpris_t = threading.Thread(target=self.run_mpris_quran)
        mpris_t.start() #HERE
        if last_sura_aya:
            __sura = last_sura_aya[0]
            __aya  = last_sura_aya[1]
            if __sura in (0,8):
                self.sura_c.set_active(__sura)
                self.listbox_.select_row(self.listbox_.get_row_at_index(__sura))
                self.txt_list.get_selection().select_path((__aya-1,))
                self.txt_list.scroll_to_cell(__aya-1,self.cols[0])
                #self.txt_list.row_activated(Gtk.TreePath.new_from_indices([__aya]),self.cols[0])
            else:
                self.sura_c.set_active(__sura)
                self.listbox_.select_row(self.listbox_.get_row_at_index(__sura))
                self.txt_list.get_selection().select_path((__aya,))
                self.txt_list.scroll_to_cell(__aya,self.cols[0])
                #self.txt_list.row_activated(Gtk.TreePath.new_from_indices([__aya]),self.cols[0])
        else:
            self.sura_c.set_active(0)
            self.listbox_.select_row(self.listbox_.get_row_at_index(0))
            self.txt_list.get_selection().select_path((0,))
            #self.txt_list.row_activated(Gtk.TreePath.new_from_indices([0]),self.cols[0])
    
        self.menu = Gtk.Menu()
        self.menu.set_screen(Gdk.Screen().get_default())
        
        self.playmenuitem    = Gtk.MenuItem.new_with_label(_("Play"))
        if not self.__all_audio:
            self.playmenuitem.set_sensitive(False)
        self.tarajemmenuitem  = Gtk.MenuItem.new_with_label(_("Tarajem"))
        self.tafasirmenuitem  = Gtk.MenuItem.new_with_label(_("Tafsir"))
        self.copymenuitem     = Gtk.MenuItem.new_with_label(_("Copy"))
        self.colorbgmenuitem  = Gtk.MenuItem.new_with_label(_("bg Color"))
        self.colorfgmenuitem  = Gtk.MenuItem.new_with_label(_("fg  Color"))
    
        self.playmenuitem.connect("activate", self._play_audio,True)
        self.tarajemmenuitem.connect("activate", self.get_current_info_aya_tarajem)
        self.tafasirmenuitem.connect("activate", self.get_current_info_aya_tafasir)
        self.copymenuitem.connect("activate", self.on_copy_menu)
        self.colorbgmenuitem.connect("activate", self.on_color_menu,self.color_button_bg)
        self.colorfgmenuitem.connect("activate", self.on_color_menu,self.color_button_fg)
        
        self.menu.append(self.playmenuitem)
        self.menu.append(self.tarajemmenuitem)
        self.menu.append(self.tafasirmenuitem)
        self.menu.append(self.copymenuitem)
        self.menu.append(self.colorbgmenuitem)
        self.menu.append(self.colorfgmenuitem)
        self.menu.show_all()
        
        self.build_cp_dlg()
        self.show_all()
        self.zoomOut(None)
        self.connect("key-press-event", self._on_key_press)
        #self.txt_list.connect("row_activated",self.on_row_activated)
        #self.txt_list.connect("cursor_changed",self.on_cursor_changed)
        self.scroll1.get_vadjustment().set_value((self.scroll1.get_vadjustment().get_upper()/114)*self.sura_c.get_active())
    
    def run_mpris_quran(self): #HERE
        self.mprisquran = MprisQuran(self) 
        
    def on_shortcut_button_clicked(self,button):
        self.menu_popover.popdown()
        builder = Gtk.Builder.new_from_string(shortcut_main_window_ui, -1)
        shortcut_window = builder.get_object("shortcuts-main-win")
        shortcut_window.set_transient_for(self) 
        shortcut_window.show_all()

    def on_setting_menu_b_clicked(self,button):
        self.menu_popover.popup()
        self.menu_popover.show_all()

    def _on_paned_position_changed(self,paned,prop):
        with GObject.Object.handler_block(self.search_b,self.search_b_handler):
            if paned.props.position==0 and self.search_b.get_active():
                self.search_b.set_active(False)
            elif paned.props.position!=0 and not self.search_b.get_active():
                self.search_b.set_active(True)
    
    def _on_search_button_toggled(self,button):
        with GObject.Object.handler_block(self.paned,self.paned_handler):
            if button.get_active():
                self.paned.props.position = 200
            else:
                self.paned.props.position = 0

    def on_selected_row(self, listbox,listboxrow):
        with GObject.Object.handler_block(self.sura_c,self.sura_c_handler):
            index_ = listboxrow.get_index()
            self.sura_c.set_active(index_)
            self.viewSura(self.sura_c.get_active() + 1)
            self._stop_audio()
            self.tb.set_active(False)
            t_ = self.search_entry.get_text()
            self.queue_draw()
            #while Gtk.events_pending():
            #    Gtk.main_iteration()
            if t_ :
                self.search_entry.set_text("")
                while Gtk.events_pending():
                    Gtk.main_iteration()
                self.scroll1.get_vadjustment().set_value((self.scroll1.get_vadjustment().get_upper()/114)*index_)

        
    def _listbox_filter_func(self, listbox,entry):
        text = entry.get_text()
        if not text:
            return listbox
        lbl = listbox.get_child().props.label
        if text.lower() in lbl.lower():
            return listbox 
            
            
    def _on_search(self, entry,listbox):
        listbox.invalidate_filter()
        
    def on_color_menu(self,button,color_button):
        color_button.emit("clicked")
    
    def _on_add_tilawa_clicked(self,button):
        self._stop_audio()
        w = AddData(self,self.audio_data_location,_("Add Tilawa audio from ayat"))
        w.set_title(_('Add Tilawa from ayat'))
        w.connect("success",self._on_add_tilawa_success)

    def _on_download_tilawa_clicked(self,button):
        if self.isdownloadwindow :
            self.isdownloadwindow.present()
            return
        self._stop_audio()
        is_pyinstaller = getattr(sys, 'frozen',False) and hasattr(sys, '_MEIPASS')
        if   is_pyinstaller:
            tilawa_json_file_l = get_correct_path('tilawa_json_files')
        else:
            exedir = os.path.dirname(sys.argv[0])
            tilawa_json_file_l = os.path.join(exedir,'..', 'share', 'albasheer','tilawa_json_files')
            if not os.path.exists(tilawa_json_file_l):
                tilawa_json_file_l = os.path.join(exedir, 'tilawa_json_files')
        w = DownloadTilawaWindow(self,os.path.join(self.albasheer_data,"Downloads"),tilawa_json_file_l,self.audio_data_location)
        w.show_all()
        w.connect("success",self._on_add_tilawa_success)
        self.isdownloadwindow  = w
        
    def _on_add_tilawa_success(self,w=None):
        self.__all_audio = self.get_all_audio_location()   
        if self.__all_audio:
            self.audio_c.remove_all()
            for i in self.__all_audio.keys():
                self.audio_c.append_text(i)
            self.audio_c.set_tooltip_text(_("choose a Audio"))
            self.audio_c.set_active(0)
            self.audio_c.set_sensitive(True)
            self.rewind_b.set_sensitive(True)
            self.forward_b.set_sensitive(True)
            self.play_b.set_sensitive(True)
            self.stop_b.set_sensitive(True)
            self.playmenuitem.set_sensitive(True)

        
    def __on_message(self, bus, message,pipeline1=False):
        t = message.type
        if t == Gst.MessageType.EOS:
            if pipeline1:
                self.tb.set_sensitive(True)
            else:
                aya  = self.get_aya()
                sura = self.get_sura_audio()
                if sura in (1,9) :
                    if aya>=len(self.txt):
                        self.tb.set_sensitive(True)
                        self._stop_audio()
                        sura_n,aya_n = self.get_sura_aya() #HERE
                        sura_n += 1
                        if self.mprisquran.loopstatus in ("Track","Playlist"):
                            if aya_n+1 > int(suwar_info_[str(sura_n)]):
                                aya_n  = 0
                                if self.mprisquran.loopstatus == "Playlist":
                                    if sura_n == 114:
                                        sura_n = 0
                                    if self.mprisquran.shuffle:
                                        sura_n = random.randrange(1,114)
                                        if not windows:
                                            self.mprisquran.connection.emit_signal(self.mprisquran.connection.get_unique_name(), "/org/mpris/MediaPlayer2/Playlists", "org.mpris.MediaPlayer2.Playlists", "ActivePlaylist",GLib.Variant("(oss)",("/org/mpris/MediaPlayer2/Playlists/"+str(sura_n),str(sura_n),"")))
                                    else:
                                        if not windows:
                                            self.mprisquran.connection.emit_signal(self.mprisquran.connection.get_unique_name(), "/org/mpris/MediaPlayer2/Playlists", "org.mpris.MediaPlayer2.Playlists", "ActivePlaylist",GLib.Variant("(oss)",("/org/mpris/MediaPlayer2/Playlists/"+str(sura_n+1),str(sura_n+1),"")))
                                    row   = self.listbox_.get_row_at_index(sura_n)
                                    self.listbox_.select_row(row)
                                else:
                                    self.viewAya(aya_n)
                            else:
                                aya_n += 1
                                self.viewAya(aya_n)
                            self._play_audio()
                        else:
                            if aya_n+1 > int(suwar_info_[str(sura_n)]):
                                return
                            else:
                                aya_n += 1
                                self.viewAya(aya_n)
                                self._play_audio()
                        return
                    #self.txt_list.get_selection().select_path((aya,))
                    #self.txt_list.row_activated(Gtk.TreePath.new_from_indices([aya]),self.cols[0])
                    #self.txt_list.scroll_to_cell(aya,self.cols[0])
                else:
                    if aya>=len(self.txt)-1:
                        self.tb.set_sensitive(True)
                        self._stop_audio()
                        
                        sura_n,aya_n = self.get_sura_aya()#HERE
                        sura_n += 1
                        if self.mprisquran.loopstatus in ("Track","Playlist"):
                            if aya_n+1 > int(suwar_info_[str(sura_n)]):
                                aya_n  = 0
                                if self.mprisquran.loopstatus == "Playlist":
                                    if sura_n == 114:
                                        sura_n = 0
                                    if self.mprisquran.shuffle:
                                        sura_n = random.randrange(1,114)
                                        if not windows:
                                            self.mprisquran.connection.emit_signal(self.mprisquran.connection.get_unique_name(), "/org/mpris/MediaPlayer2/Playlists", "org.mpris.MediaPlayer2.Playlists", "ActivePlaylist",GLib.Variant("(oss)",("/org/mpris/MediaPlayer2/Playlists/"+str(sura_n),str(sura_n),"")))
                                    else:
                                        if not windows:
                                            self.mprisquran.connection.emit_signal(self.mprisquran.connection.get_unique_name(), "/org/mpris/MediaPlayer2/Playlists", "org.mpris.MediaPlayer2.Playlists", "ActivePlaylist",GLib.Variant("(oss)",("/org/mpris/MediaPlayer2/Playlists/"+str(sura_n+1),str(sura_n+1),"")))
                                    row   = self.listbox_.get_row_at_index(sura_n)
                                    self.listbox_.select_row(row)
                                else:
                                    self.viewAya(aya_n)
                            else:
                                aya_n += 1
                                self.viewAya(aya_n)
                            self._play_audio()
                        else:
                            if aya_n+1 > int(suwar_info_[str(sura_n)]):
                                return
                            else:
                                aya_n += 1
                                self.viewAya(aya_n)
                                self._play_audio()
                        return
                    #self.txt_list.get_selection().select_path((aya+1,))
                    #self.txt_list.row_activated(Gtk.TreePath.new_from_indices([aya]),self.cols[0])
                    #self.txt_list.scroll_to_cell(aya+1,self.cols[0])
                self.resize_cb()
                self.queue_draw()
                self.viewSura(sura)
                self.viewAya(aya+1)
                self._play_audio()
        elif t == Gst.MessageType.ERROR:
            self._stop_audio()
            self.tb.set_sensitive(True)
    

    def seek_audio(self,button=None,forward=True):
        if not self.__can_play:
            return
        if not forward:
            if self.pipeline2.get_state(Gst.CLOCK_TIME_NONE )[1]==Gst.State.PLAYING:
                pos = self.pipeline2.query_position(Gst.Format.TIME)
                if pos :
                    pos = pos[1]
                    if pos>=2*1000000000:
                        self.pipeline2.seek_simple(Gst.Format.TIME,  Gst.SeekFlags.FLUSH | Gst.SeekFlags.KEY_UNIT,pos-(2*1000000000))
                    else:
                        self.pipeline2.seek_simple(Gst.Format.TIME,  Gst.SeekFlags.FLUSH | Gst.SeekFlags.KEY_UNIT,0)
                        
            elif  self.pipeline.get_state(Gst.CLOCK_TIME_NONE )[1]==Gst.State.PLAYING:
                pos = self.pipeline.query_position(Gst.Format.TIME)
                if pos :
                    pos = pos[1]
                    if pos>=2*1000000000:
                        self.pipeline.seek_simple(Gst.Format.TIME,  Gst.SeekFlags.FLUSH | Gst.SeekFlags.KEY_UNIT,pos-(2*1000000000)) 
                    else:
                        self.pipeline.seek_simple(Gst.Format.TIME,  Gst.SeekFlags.FLUSH | Gst.SeekFlags.KEY_UNIT,0)
        else:
            if  self.pipeline2.get_state(Gst.CLOCK_TIME_NONE )[1]==Gst.State.PLAYING:
                pos = self.pipeline2.query_position(Gst.Format.TIME)
                if pos :
                    pos = pos[1]
                    if pos>=0:
                        self.pipeline2.seek_simple(Gst.Format.TIME,  Gst.SeekFlags.FLUSH | Gst.SeekFlags.KEY_UNIT,pos+(2*1000000000)) 
            elif  self.pipeline.get_state(Gst.CLOCK_TIME_NONE )[1]==Gst.State.PLAYING:
                pos = self.pipeline.query_position(Gst.Format.TIME)
                if pos :
                    pos = pos[1]
                    if pos>=0:
                        self.pipeline.seek_simple(Gst.Format.TIME,  Gst.SeekFlags.FLUSH | Gst.SeekFlags.KEY_UNIT,pos+(2*1000000000))

    def speed_up(self,button=None):
        if self.autoScrolling:
            self.scroll_delay -= 25
            if self.scroll_delay<25:
                self.scroll_delay = 25
            GLib.Source.remove(self.source_id)
            self.source_id = GLib.timeout_add(self.scroll_delay, self.autoScroll, self.tb )
            
    def speed_down(self,button=None):
        if self.autoScrolling:
            self.scroll_delay += 25
            if self.scroll_delay > 500:
                self.scroll_delay = 500
            GLib.Source.remove(self.source_id)
            self.source_id = GLib.timeout_add(self.scroll_delay, self.autoScroll, self.tb )
            

                    
    def _stop_audio(self,button=False):
        self.pipeline2.set_state(Gst.State.NULL)
        self.pipeline.set_state(Gst.State.NULL)
        self.tb.set_sensitive(True)
        self.mprisquran.playbackstatus = "Stopped" #HERE
        
    def _play_audio(self,button=False,oneshot=False):
        if not self.__can_play:
            return
        self._stop_audio()
        self.tb.set_sensitive(False)
        sura = self.get_sura_audio()
        aya  = self.get_aya()
        aya_ = str(aya)
        sura_ = str(sura)
        q = self.__all_audio[self.audio_c.get_active_text()]

        if aya==0 and sura not in (9,1) :
            q = os.path.join(q,"001001.mp3")
        else:
            s_ = ("0"*(3-len(sura_)))+sura_
            a_ = ("0"*(3-len(aya_)))+aya_
            #q = os.path.join(q,sura_.zfill(4-len(sura_))+aya_.zfill(4-len(aya_))+".mp3")
            q = os.path.join(q,s_+a_+".mp3")
        if not os.path.isfile(q):
            self.tb.set_sensitive(True)
            return
        
        if  sys.platform.startswith('win'):
            q =  "file:///"+os.path.abspath(q).replace(os.sep, '/')
        else:
            q = "file://"+os.path.abspath(q)
        if oneshot:
            self.pipeline.set_property('uri',q)
            self.pipeline.set_state(Gst.State.PLAYING)
        else:
            self.pipeline2.set_property('uri',q)
            self.pipeline2.set_state(Gst.State.PLAYING)
            self.mprisquran.playbackstatus = "Playing" #HERE


    def get_all_audio_location(self):
        result = {}
        if not os.path.isdir(self.audio_data_location):
            return False
        for f in os.listdir(self.audio_data_location):
            ll_ = os.path.join(self.audio_data_location,f)
            for dirname,folder,files in os.walk(ll_):
                for file_ in files:
                    if file_.endswith(".mp3"):
                        result.setdefault(os.path.basename(dirname),dirname)
                        break
        if result:
            return result
        return False

         
    def on_copy_menu(self,w):
        a = self.txt_list.get_selection().get_selected()
        if a:
            aya = self.txt[self.txt.get_path(a[1])][0]
            self.clip2.set_text(aya, -1) 
        
    def create_bookmarks_file(self):
        config_location = os.path.join(GLib.get_user_config_dir(),"albasheer")
        config_file     = os.path.join(config_location,"bookmarks.json")
        os.makedirs(config_location,exist_ok=True)
        if not os.path.isfile(config_file):
            try:
                config = {"sura_aya_bookmarks":list()}
                with open(config_file,"w") as mf:
                    json.dump(config,mf,indent=4)
            except Exception as e:
                print(e)
                return False
        try :
            with open(config_file) as mf:
                config = json.load(mf)
        except Exception as e:
            os.remove(config_file)
            return self.create_bookmarks_file()

        return True
        
    def get_is_bookmark(self):
        if not self.create_bookmarks_file():
            return False
        config_file = os.path.join(os.path.join(GLib.get_user_config_dir(),"albasheer"),"bookmarks.json")
        if os.path.isfile(config_file):
            try:
                with open(config_file) as mf:
                    config = json.load(mf)
            except Exception as e:
                print(e)
                return False
            for i in config["sura_aya_bookmarks"]:
                if i==[self.__sura_current,self.__aya_current]:
                    return True
        return False

    def get_bookmark(self):
        if not self.create_bookmarks_file():
            return 
        config_file = os.path.join(os.path.join(GLib.get_user_config_dir(),"albasheer"),"bookmarks.json")
        if os.path.isfile(config_file):
            try:
                with open(config_file) as mf:
                    config = json.load(mf)
            except Exception as e:
                print(e)
                return False
            return config
        return False
        
    def add_bookmark(self):
        if not self.create_bookmarks_file():
            return 
        config_location = os.path.join(GLib.get_user_config_dir(),"albasheer")
        config_file     = os.path.join(config_location,"bookmarks.json")
        config = self.get_bookmark()
        if (self.__sura_current,self.__aya_current) not in config["sura_aya_bookmarks"]:
            config["sura_aya_bookmarks"].append((self.__sura_current,self.__aya_current))
        try:
            with open(config_file,"w") as mf:
                json.dump(config,mf,indent=4)
        except Exception as e:
            print(e)
            return False
        return True
        
    def on_bookmark(self,button):
        if self._is_bookmark:
            return self.remove_bookmark()
        else:
            return self.add_bookmark()
            
    def remove_bookmark(self):
        if not self.create_bookmarks_file():
            return 
        config_location = os.path.join(GLib.get_user_config_dir(),"albasheer")
        config_file     = os.path.join(config_location,"bookmarks.json")
        config = self.get_bookmark()
        result = {"sura_aya_bookmarks": list() }
        for i in config["sura_aya_bookmarks"]:
            if i!=[self.__sura_current,self.__aya_current]:
                result["sura_aya_bookmarks"].append(i)
        try:
            with open(config_file,"w") as mf:
                json.dump(result,mf,indent=4)
        except Exception as e:
            print(e)
            return False
        return True
                
    def _on_button_press_event_treeview(self,treeview,event):
        """self.txt_list.queue_draw()
        self.queue_draw()
        while Gtk.events_pending():
            Gtk.main_iteration()"""

        if event.type == Gdk.EventType.BUTTON_PRESS and event.button == 3:
            """menu = Gtk.Menu()
            menu.set_screen(Gdk.Screen().get_default())
        
            playmenuitem    = Gtk.MenuItem.new_with_label(_("Play"))
            if not self.__all_audio:
                playmenuitem.set_sensitive(False)
            tarajemmenuitem  = Gtk.MenuItem.new_with_label(_("Tarajem"))
            tafasirmenuitem  = Gtk.MenuItem.new_with_label(_("Tafsir"))
            copymenuitem     = Gtk.MenuItem.new_with_label(_("Copy"))
            colorbgmenuitem  = Gtk.MenuItem.new_with_label(_("bg Color"))
            colorfgmenuitem  = Gtk.MenuItem.new_with_label(_("fg  Color"))
            
            self.__sura_current,self.__aya_current = self.getCurrentSuraAya()
            self._is_bookmark = self.get_is_bookmark()
            if not self._is_bookmark:
                bookmarkmenuitem  = Gtk.MenuItem.new_with_label(_("Add To Bookmarks"))
            else:
                bookmarkmenuitem  = Gtk.MenuItem.new_with_label(_("Remove From Bookmarks"))
            
            playmenuitem.connect("activate", self._play_audio,True)
            tarajemmenuitem.connect("activate", self.get_current_info_aya_tarajem)
            tafasirmenuitem.connect("activate", self.get_current_info_aya_tafasir)
            copymenuitem.connect("activate", self.on_copy_menu)
            colorbgmenuitem.connect("activate", self.on_color_menu,self.color_button_bg)
            colorfgmenuitem.connect("activate", self.on_color_menu,self.color_button_fg)
            bookmarkmenuitem.connect("activate", self.on_bookmark)
        
            menu.append(playmenuitem)
            menu.append(tarajemmenuitem)
            menu.append(tafasirmenuitem)
            menu.append(copymenuitem)
            menu.append(colorbgmenuitem)
            menu.append(colorfgmenuitem)
            menu.append(bookmarkmenuitem)
            menu.show_all()
            menu.popup_at_pointer()"""
            self.menu.popup_at_pointer()
            
    def _on_key_press(self,widget, event):
        if (event.state & Gdk.ModifierType.CONTROL_MASK) and event.keyval == Gdk.KEY_s:
            self.save_sura_aya()
            
        elif  (event.state & Gdk.ModifierType.CONTROL_MASK) and event.keyval == Gdk.KEY_d:
            self.darkmode_switch.set_active(not self.darkmode_switch.get_active())
            
        elif  (event.state & Gdk.ModifierType.CONTROL_MASK) and event.keyval == Gdk.KEY_f:
            self.search.grab_focus_without_selecting()
                
        elif  (event.state & Gdk.ModifierType.CONTROL_MASK) and event.keyval == Gdk.KEY_z:
            self.zoomIn()
            
        elif  (event.state & Gdk.ModifierType.CONTROL_MASK) and event.keyval == Gdk.KEY_x:
            self.zoomOut()
            
        elif  (event.state & Gdk.ModifierType.CONTROL_MASK) and event.keyval == Gdk.KEY_a:
            self.menu.popup_at_pointer()
            self.menu.show_all()
            
        elif  (event.state & Gdk.ModifierType.CONTROL_MASK) and event.keyval == Gdk.KEY_e:
            #self.sura_c.grab_focus()
            self.sura_c.popup()
                        
        elif  (event.state & Gdk.ModifierType.CONTROL_MASK) and event.keyval == Gdk.KEY_c :
            if  self.pipeline2.get_state(Gst.CLOCK_TIME_NONE )[1]!=Gst.State.PLAYING:
                self.autoScrolling = not self.autoScrolling
                self.tb.set_active(not self.tb.get_active() )

            
        elif  (event.state & Gdk.ModifierType.CONTROL_MASK) and event.keyval == Gdk.KEY_b and self.autoScrolling:
            self.speed_up()
            
        elif  (event.state & Gdk.ModifierType.CONTROL_MASK) and event.keyval == Gdk.KEY_v and self.autoScrolling:
            self.speed_down()

        elif  (event.state & Gdk.ModifierType.CONTROL_MASK) and event.keyval == Gdk.KEY_q :
            self.cp_b.emit("clicked")
        
        elif  (event.state & Gdk.ModifierType.CONTROL_MASK) and event.keyval == Gdk.KEY_g :
            if self.audio_c.get_sensitive():
                if  self.pipeline2.get_state(Gst.CLOCK_TIME_NONE )[1]!=Gst.State.PLAYING:
                    self._play_audio(None)
                
        elif  (event.state & Gdk.ModifierType.CONTROL_MASK) and event.keyval == Gdk.KEY_h :
            if self.audio_c.get_sensitive():
                self._stop_audio()
                
        elif  (event.state & Gdk.ModifierType.CONTROL_MASK) and event.keyval == Gdk.KEY_Left  :
            if self.audio_c.get_sensitive() and self.pipeline2.get_state(Gst.CLOCK_TIME_NONE )[1]==Gst.State.PLAYING:
                self.seek_audio(None,False)  
                
        elif  (event.state & Gdk.ModifierType.CONTROL_MASK) and event.keyval == Gdk.KEY_Right  :
            if self.audio_c.get_sensitive() and self.pipeline2.get_state(Gst.CLOCK_TIME_NONE )[1]==Gst.State.PLAYING:
                self.seek_audio() 
                

            
        """elif  (event.state & Gdk.ModifierType.SHIFT_MASK) and (event.state & Gdk.ModifierType.CONTROL_MASK | Gdk.ModifierType.SHIFT_MASK):
            print("dddddddddd)"""
        self.queue_draw()
        
    def save_last_sura_aya(self,sura,aya):
        config_location = os.path.join(GLib.get_user_config_dir(),"albasheer")
        config_file     = os.path.join(config_location,"albasheer.json")
        try:
            os.makedirs(config_location,exist_ok=True)
            with open(config_file,"w") as mf:
                json.dump({"sura":sura,"aya":aya},mf,indent=4)
        except Exception as e:
            print(e)
            return False
        return True

    def get_last_sura_aya(self):
        config_file = os.path.join(os.path.join(GLib.get_user_config_dir(),"albasheer"),"albasheer.json")
        if os.path.isfile(config_file):
            try:
                with open(config_file) as mf:
                    config = json.load(mf)
            except Exception as e:
                print(e)
                return False
            return config["sura"],config["aya"]
        return False
    
    def get_sura_aya(self):
        return self.sura_c.get_active(),self.get_aya()
        
    def get_aya(self):
        treemodel_treeiter = self.txt_list.get_selection().get_selected()
        if not treemodel_treeiter:
            aya = 0
        else:
            aya = treemodel_treeiter[0].get_value(treemodel_treeiter[1],1)
        return aya
        
    def get_sura_audio(self):
        return self.sura_c.get_active()+1

    def save_sura_aya(self):
        self.save_last_sura_aya(self.sura_c.get_active(),self.get_aya())
        
    #def on_cursor_changed(self,tree_view):
     #   print(tree_view)

    """def on_row_activated(self,tree_view, path, column):
        treemodel_treeiter = self.txt_list.get_selection().get_selected()
        if not treemodel_treeiter:
            self.__aya = 0
        else:
            self.__aya = treemodel_treeiter[0].get_value(treemodel_treeiter[1],1)
        print(self.__aya)
        soura = self.sura_c.get_active()+1
        aya   = path
        a = tree_view.get_cell_area(aya, column)
        #self.cells[0].get_style_context().add_class("glow")
        for row in self.txt:
            print(self.txt[row.iter][0])
            print(self.txt[row.iter][1])
            print(self.txt[row.iter][2])
        self.txt_list.get_selection().select_path((10,))
        self.txt_list.scroll_to_cell(10,column)"""

        
        
    ############################
    def _on_color_set(self,colorbutton,bg=True):
        if bg:
            self.cells[0].set_property("background",colorbutton.get_color().to_string())
        else:
            self.cells[0].set_property("foreground",colorbutton.get_color().to_string())
        
    def _on_darkmode_switch_state_changed(self,switch,state,defaultsettings):
        defaultsettings.props.gtk_application_prefer_dark_theme  = state
        if state:
            self.color_button_bg.set_color(Gdk.Color.parse("#323030")[-1])
            self.color_button_fg.set_color(Gdk.Color.parse("#fffff8")[-1])
            self.cells[0].set_property("background","#323030")
            self.cells[0].set_property("foreground","#fffff8")
        else:
            self.color_button_bg.set_color(Gdk.Color.parse("#fffff8")[-1])
            self.color_button_fg.set_color(Gdk.Color.parse("#204000")[-1])
            self.cells[0].set_property("background","#fffff8")
            self.cells[0].set_property("foreground","#204000")
    ############################
    
    def show_about_dlg(self, parent):
        self.menu_popover.popdown()
        dlg = Gtk.AboutDialog()
        dlg.set_type_hint(Gdk.WindowTypeHint.DIALOG)
        dlg.set_modal(True)
        dlg.set_transient_for(parent)
        dlg.set_default_response(Gtk.ResponseType.CLOSE)
        dlg.connect('delete-event', lambda w,*a: w.hide() or True)
        dlg.connect('response', lambda w,*a: w.hide() or True)
        try:
            dlg.set_program_name("albasheer")
        except:
            pass
        dlg.set_name(_('albasheer Quran Browser'))
        #dlg.set_version(version)
        dlg.set_copyright("Copyright © 2019-2020, Yucef Sourani <youssef.m.sourani@gmail.com>")
        dlg.set_comments(_("Electronic Mus-haf"))
        dlg.set_license("""
        Released under terms of Waqf Public License.
        This program is free software; you can redistribute it and/or modify
        it under the terms of the latest version Waqf Public License as
        published by Ojuba.org.

        This program is distributed in the hope that it will be useful,
        but WITHOUT ANY WARRANTY; without even the implied warranty of
        MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.

        The Latest version of the license can be found on
        "https://ojuba.org/waqf:license/"

        """)
        dlg.set_website("https://github.com/yucefsourani/albasheer-electronic-quran-browser")
        dlg.set_version("3.0")
        
        dlg.set_authors(["Yucef Sourani <youssef.m.sourani@gmail.com>"])
        dlg.set_translator_credits(_("translator-credits"))
        dlg.add_credit_section("Based on/Special thanks",["Othman Electronic Quran Browser","https://github.com/ojuba-org/othman"])
        dlg.add_credit_section("Special thanks",["Amiri Font","https://www.amirifont.org/"])
        dlg.add_credit_section("This program uses ",["Ayat to provides tilawa/tafasir/tarajem","https://quran.ksu.edu.sa/ayat/"])
        fn = os.path.join(self.data_dir, "quran-kareem.svg")
        try:
            logo = GdkPixbuf.Pixbuf.new_from_file_at_size(fn, 128, 128)
        except:
            fn = os.path.join(self.data_dir, "quran-kareem.png")
            logo = GdkPixbuf.pixbuf_new_from_file(fn)
        dlg.set_logo(logo)
        #dlg.set_logo_icon_name('albasheer')
        dlg.run()
        dlg.destroy()

    def search_cb(self, b, *a):
        if not self.sw:
            self.sw = searchWindow(self)
        self.sw.find(b.get_text())

    def autoScroll(self, b):
        if not self.autoScrolling:
            self.__can_play = True
            self.scroll_delay = 200
            return True
        v = self.scroll2.get_vadjustment()
        m = v.get_upper() - v.get_page_size()
        n = min(m, v.get_value() + 2 )
        if n == m:
            self.scroll_delay = 200
            b.set_active(False)
            self.__can_play = True
        v.set_value(n)
        """if b.get_active() :
            if self.__count>(self.scroll_delay+self.cells[0].get_property("scale")):
                sura,aya = self.get_sura_aya()
                self.txt_list.get_selection().select_path((aya+1,))
                self.__count = 0
            self.__count +=5"""
        return True

    def autoScrollCb(self, b, *a):
        isactive           = b.get_active()
        self.__can_play    = not isactive
        self.autoScrolling = isactive

    def zoomIn(self, *a):
        sura, aya = self.getCurrentSuraAya()
        self.scale += 0.1
        self.cells[0].set_property("scale", self.scale)
        self.resize_cb()
        self.queue_draw()
        self.viewSura(sura)
        self.viewAya(aya)
        self.search_b.set_active(False)

                
    def zoomOut(self, *a):
        sura, aya = self.getCurrentSuraAya()
        self.scale -= 0.1
        self.scale = max(0.2, self.scale)
        self.cells[0].set_property("scale", self.scale)
        self.resize_cb()
        self.queue_draw()
        self.viewSura(sura)
        self.viewAya(aya)
        self.search_b.set_active(False)


    def viewAya(self, aya, sura = None):
        if sura == None:
            sura = self.sura_c.get_active() + 1
        aya = max(1,abs(aya))
        i = aya + int(self.showSunnahBasmala(sura))
        self.txt_list.scroll_to_cell((i - 1,))
        self.txt_list.get_selection().select_path((i - 1,))
        

    def viewSura(self, i):
        #self.play_pause.set_active(False)
        self.txt.clear()
        if self.showSunnahBasmala(i):
            #self.txt.append(['<span foreground="#440000">%s</span>' % self.basmala,0,])
            self.txt.append([self.basmala, 0, "#802000",])
        for j, k in enumerate(self.getSuraIter(i)):
            self.txt.append([k[0], j + 1, "#204000",])
        self.resize_cb()
        self.scroll2.get_vadjustment().set_value(0)
        self.txt_list.get_selection().select_path((0,))
        

    def sura_changed_cb(self, c, *a):
        self.viewSura(self.sura_c.get_active() + 1)
        self._stop_audio()
        self.tb.set_active(False)
        with GObject.Object.handler_block(self.listbox_,self.listbox__handler):
            self.listbox_.select_row(self.listbox_.get_row_at_index(self.sura_c.get_active()))
            self.scroll1.get_vadjustment().set_value((self.scroll1.get_vadjustment().get_upper()/114)*self.sura_c.get_active())

    def resize_cb(self,*args):
        if self.cols[0].get_width() > 10:
            self.cells[0].set_property("wrap-width", self.cols[0].get_width() - 10)

    def cp_cb(self, *a):
        sura = self.cp_sura.get_active() + 1
        aya1 = self.cp_from.get_value()
        aya2 = self.cp_to.get_value()
        n = aya2 - aya1 + 1
        i = self.cp_is_imlai.get_active()
        a = [' ', '\n', ' * ', ' *\n']
        s = a[int(i) * 2 + int(self.cp_aya_perline.get_active())]
        s = s.join([l[i] for l in self.getSuraIter(sura, n, aya1)]) + '\n'
        self.clip1.set_text(s, -1)
        self.clip2.set_text(s, -1)
        self.cp_w.hide()

    def cp_sura_cb(self, *a):
        sura = self.cp_sura.get_active() + 1
        m = self.suraInfoById[sura - 1][5]
        self.cp_from.set_range(1, m)
        self.cp_to.set_range(1, m)
        self.cp_from.set_value(1)
        self.cp_to.set_value(m)

    def show_cp_dlg(self, *a):
        self.menu_popover.popdown()
        sura, aya = self.getCurrentSuraAya()
        aya = max(1, abs(aya))
        self.cp_sura.set_active(sura - 1)
        self.cp_sura_cb()
        self.cp_from.set_value(aya)
        self.cp_w.show_all()

    def build_cp_dlg(self):
        self.cp_w = Gtk.Window()
        self.cp_w.set_position(Gtk.WindowPosition.CENTER )
        self.cp_w.set_title(_('Copy to clipboard'))
        self.cp_w.set_type_hint(Gdk.WindowTypeHint.DIALOG)
        self.cp_w.connect('delete-event', lambda w,*a: w.hide() or True)
        self.cp_sura = Gtk.ComboBoxText.new()
        self.cp_sura.set_wrap_width(5)

        for i in self.sura_ls:
            self.cp_sura.append_text(i)
        self.cp_sura.set_tooltip_text(_("choose a Sura"))
        adj = Gtk.Adjustment(0, 0, 286, 1, 10, 0)
        self.cp_from = s = Gtk.SpinButton()
        s.set_adjustment(adj)
        adj = Gtk.Adjustment(0, 0, 286, 1, 10, 0)
        self.cp_to = s = Gtk.SpinButton()
        s.set_adjustment(adj)
        self.cp_is_imlai = Gtk.CheckButton(_("Imla'i style"))
        self.cp_aya_perline = Gtk.CheckButton(_("an Aya per line"))
        self.cp_ok = Gtk.Button(stock=Gtk.STOCK_OK)
        self.cp_cancel = Gtk.Button(stock=Gtk.STOCK_CANCEL)
        vb = Gtk.VBox(False,0)
        self.cp_w.add(vb)
        hb = Gtk.HBox(False,3)
        vb.pack_start(hb,True,True,3)
        hb.pack_start(Gtk.Label(_("Sorat:")),False,False,3)
        hb.pack_start(self.cp_sura,False,False,6)
        hb = Gtk.HBox(False,6)
        vb.pack_start(hb,True,True,6)
        hb.pack_start(Gtk.Label(_("Ayat from:")),False,False,3)
        hb.pack_start(self.cp_from,False,False,3)
        hb.pack_start(Gtk.Label(_("To")),False,False,3)
        hb.pack_start(self.cp_to,False,False,3)
        hb = Gtk.HBox(False,6)
        vb.pack_start(hb,True,True,6)
        hb.pack_start(self.cp_is_imlai,False,False,3)
        hb.pack_start(self.cp_aya_perline,False,False,3)
        hb = Gtk.HBox(False,6)
        vb.pack_start(hb,True,True,6)
        hb.pack_start(self.cp_ok,False,False,6)
        hb.pack_start(self.cp_cancel,False,False,6)
        self.cp_sura.connect("changed", self.cp_sura_cb)
        self.cp_cancel.connect('clicked', lambda *args: self.cp_w.hide())
        self.cp_ok.connect('clicked', self.cp_cb)
        self.cp_is_imlai.set_active(True)

    def getCurrentSuraAya(self):
        a = self.txt_list.get_selection().get_selected()
        aya = 1
        if a:
            aya = self.txt[self.txt.get_path(a[1])][1]
        aya = max(aya, 1)
        return self.sura_c.get_active() + 1, aya

    def get_current_info_aya_tarajem(self,b=None):
        sura_n,aya_n = self.get_sura_aya()
        conn = None
        sura = self.sura_c.get_active_text()
        a = self.txt_list.get_selection().get_selected()
        aya = self.txt[self.txt.get_path(a[1])][0]
        self._stop_audio()
        ShowTarajemTafasir(self,self.tarajem_data_location ,
                    _("Add Tarajem Sources"),
                    _("Add Tarajem from ayat"),_("Show Tarajem"),sura_n+1,aya_n,sura,aya,_("Tarajem Not Available"),self.__all_audio,True)

    def get_current_info_aya_tafasir(self,b=None):
        sura_n,aya_n = self.get_sura_aya()
        conn = None
        sura = self.sura_c.get_active_text()
        a = self.txt_list.get_selection().get_selected()
        aya = self.txt[self.txt.get_path(a[1])][0]
        self._stop_audio()
        ShowTarajemTafasir(self,self.tafasir_data_location ,
                    _("Add Tafasir Sources"),
                    _("Add Tafasir from ayat"),_("Show Tafasir"),sura_n+1,aya_n,sura,aya,_("Tafasir Not Available"),self.__all_audio,False)

    def quit(self,*args):
        last_sura_aya_config  = self.get_last_sura_aya()
        last_sura_aya_current = self.get_sura_aya()
        if last_sura_aya_config:
            if last_sura_aya_config!=last_sura_aya_current:
                y_o_n = Yes_Or_No(_("Save Current Sura/Aya?"),self,"")
                if y_o_n.check():
                    self.save_sura_aya()
        else:
            self.save_sura_aya()
        Gtk.main_quit()
        return True


"""def set_language(domain,ld):
    languages = []
    for lang in [i for i in os.listdir(ld) if os.path.isdir(os.path.join(ld,i))]:
        if gettext.find(domain, localedir=ld, languages=[lang]):
            languages.append(lang)
    if languages:
        l = gettext.translation(domain, localedir=ld, languages=languages)
        l.install()
        return True
    return False"""
    
def main():
    if sys.platform.startswith('win'):
        import locale
        if os.getenv('LANG') is None:
            lang, enc = locale.getdefaultlocale()
            os.environ['LANG'] = lang
    is_pyinstaller = getattr(sys, 'frozen',False) and hasattr(sys, '_MEIPASS')
    if   is_pyinstaller:
        ld = get_correct_path('locale')
        albasheer_data = os.path.join(GLib.get_user_data_dir(),"albasheer")
    else:
        exedir = os.path.dirname(sys.argv[0])
        ld = os.path.join(exedir,'..', 'share', 'locale')
        if not os.path.exists(ld):
            ld = os.path.join(exedir, 'locale')
        albasheer_data = os.path.abspath(os.path.join(exedir,"albasheer-data"))
        if  not os.path.isdir(albasheer_data):
            albasheer_data = os.path.join(GLib.get_user_data_dir(),"albasheer")
            os.makedirs(albasheer_data,exist_ok=True)
    gettext.install('albasheer', localedir=ld)
    w = albasheerUi(albasheer_data)
    Gtk.main()

if __name__ == "__main__":
    main()

