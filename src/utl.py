import threading
import zipfile
from gi.repository import GLib,Adw,GObject,Gtk,Gio,Gst
import os



ALLTILAWAINFO = {"Al-Husary"        : "Husary_64kbps",
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

suwar_info = {'1': '7', '2': '286', '3': '200', '4': '176', '5': '120', '6': '165', '7': '206', '8': '75', '9': '129', '10': '109',
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

FONT_SIZE = {
                0 : "large-title",
                1 : "title-1",
                2 : "title-2",
                3 : "title-4",
}

class UnpackZipTafasirTaragem(threading.Thread):
    def __init__(self,sources_location,target_location,pparent,parent):
        threading.Thread.__init__(self)
        self.sources_location = sources_location
        self.target_location  = target_location
        self.pparent          = pparent
        self.parent           = parent
        self.daemon           = False

    def run(self):
        GLib.idle_add(self.parent.mainvb.set_sensitive,False)
        result = []
        for source_location in self.sources_location:
            result.append(self.unpack_file(source_location))

        if any(result):
            toast= Adw.Toast(title=_("Done"),timeout=0)
            GLib.idle_add(self.pparent.toastoverlay.add_toast,toast)
            GLib.idle_add(self.parent.emit,"result",True)
        else:
            toast= Adw.Toast(title=_("Unpack File Faild"),timeout=0)
            GLib.idle_add(self.pparent.toastoverlay.add_toast,toast)
            GLib.idle_add(self.parent.emit,"result",False)

        GLib.idle_add(self.parent.mainvb.set_sensitive,True)


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

class UnpackZipTilawa(threading.Thread):
    def __init__(self,sources_location,target_location,pparent,parent,name_):
        threading.Thread.__init__(self)
        self.sources_location = sources_location
        self.target_location  = target_location
        self.pparent          = pparent
        self.parent           = parent
        self.name_            = name_
        self.daemon           = False

    def run(self):
        result = []
        for source_location in self.sources_location:
            result.append(self.unpack_file(source_location))

        if any(result):
            toast= Adw.Toast(title=_("Done"),timeout=0)
            GLib.idle_add(self.pparent.toastoverlay.add_toast,toast)
            GLib.idle_add(self.parent.emit,"result",self.name_,self.target_location,True)
        else:
            toast= Adw.Toast(title=_("Unpack File Faild"),timeout=0)
            GLib.idle_add(self.pparent.toastoverlay.add_toast,toast)
            GLib.idle_add(self.parent.emit,"result","","",False)

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

class TilawaPlayer(GObject.Object):
    @GObject.Property(type=bool,default=False)
    def autoplay(self):
        return self.__autoplay

    @autoplay.setter
    def set_autoplay(self, autoplay):
        if self.__autoplay != autoplay:
            self.__autoplay = autoplay
            if autoplay:
                self.play()
            else:
                self.stop()

    @GObject.Property(type=int,default=10)
    def volume(self):
        return self.__volume

    @volume.setter
    def set_volume(self, volume):
        if self.__volume != volume:
            self.__volume = volume
            if self.player.get_state(Gst.CLOCK_TIME_NONE )[1] == Gst.State.PLAYING:
                self.player.props.volume = volume / 10
            self.parent.app_settings.set_int("volume",int(volume))

    @GObject.Property(type=int,default=0)
    def aya(self):
        return self.__aya

    @aya.setter
    def set_aya(self, aya):
        if self.__aya != aya:
            self.__aya = aya
            self.stop()
            if self.props.autoplay:
                self.play()
            else:
                self.stop()

    @GObject.Property(type=int,default=0)
    def sura(self):
        return self.__sura

    @sura.setter
    def set_sura(self, sura):
        if self.__sura != sura:
            self.__sura= sura
            if self.props.autoplay:
                self.play()
            else:
                self.stop()

    def __init__(self,parent,audio_data_location):
        GObject.Object.__init__(self)
        self.parent = parent
        self.audio_data_location = audio_data_location
        self.__aya      = self.parent.aya
        self.__sura     = self.parent.sura
        self.__autoplay = False
        self.__volume   = self.parent.app_settings.get_int("volume")
        self.player = Gst.ElementFactory.make("playbin", "player")
        self.__bus = self.player.get_bus()
        self.__bus.add_signal_watch()
        self.__bus.connect("message", self.__on_message)


        action = Gio.SimpleAction.new("seekbacktilawa", None)
        action.connect("activate", self.back_seek_audio)
        self.parent.app_.set_accels_for_action("win.seekbacktilawa", ['<Primary>a'])
        self.parent.add_action(action)

        action = Gio.SimpleAction.new("seekforwardtilawa", None)
        action.connect("activate", self.forward_seek_audio)
        self.parent.app_.set_accels_for_action("win.seekforwardtilawa", ['<Primary>z'])
        self.parent.add_action(action)

        action = Gio.SimpleAction.new("playstoptilawa", None)
        action.connect("activate", self.play_stop_audio)
        self.parent.app_.set_accels_for_action("win.playstoptilawa", ['<Primary>p'])
        self.parent.add_action(action)


    def __on_message(self, bus, message):
        t = message.type
        if t == Gst.MessageType.EOS :
            if self.props.autoplay:
                self.parent.toolbar.on_forward_aya_clicked()
            else:
                self.stop()
        elif t == Gst.MessageType.ERROR:
            if self.props.autoplay:
                self.parent.toolbar.auto_play_button.props.active = False
            self.stop()

    def play(self,b=None):
        if b  and self.props.autoplay:
            self.parent.toolbar.auto_play_button.props.active = False
            self.props.autoplay = False
        if self.set_filename():
            self.player.set_state(Gst.State.PLAYING)

    def stop(self,b=None):
        if b  and self.props.autoplay:
            self.parent.toolbar.auto_play_button.props.active = False
            self.props.autoplay = False
        if self.player.get_state(Gst.CLOCK_TIME_NONE )[1] == Gst.State.PLAYING:
            self.player.set_state(Gst.State.NULL)

    def set_filename(self):
        self.stop()
        if self.props.sura  in (9,1):
            aya  = self.props.aya  +1
        else:
            aya  = self.props.aya
        sura = self.props.sura
        item = self.parent.tilawagui.tilawasetings.comborow.get_selected_item()
        if not item:
            if self.props.autoplay:
                self.parent.toolbar.auto_play_button.props.active = False
                self.props.autoplay = False
            toast= Adw.Toast(title=_("TILAWA NOT FOUND! Download Tilawa"),timeout=0)
            self.parent.toastoverlay.add_toast(toast)
            return False
        tilawa = item.props.string
        filename = os.path.join(self.audio_data_location,tilawa,"audio",ALLTILAWAINFO[tilawa])
        if aya==0 and sura not in (9,1) :
            filename = os.path.join(filename,"001001.mp3")
        else:
            sura_ = str(sura)
            aya_  = str(aya)
            s_ = ("0"*(3-len(sura_)))+sura_
            a_ = ("0"*(3-len(aya_)))+aya_
            filename = os.path.join(filename,s_+a_+".mp3")
        if os.path.isfile(filename):
            self.player.set_property('uri',"file://"+filename)
        else:
            return False
        self.player.props.volume = self.props.volume / 10
        return True

    def back_seek_audio(self,*button):
        if self.player.get_state(Gst.CLOCK_TIME_NONE )[1]==Gst.State.PLAYING:
            pos = self.player.query_position(Gst.Format.TIME)
            if pos :
                pos = pos[1]
                if pos>=2*1000000000:
                    self.player.seek_simple(Gst.Format.TIME,  Gst.SeekFlags.FLUSH | Gst.SeekFlags.KEY_UNIT,pos-(2*1000000000))
                else:
                    self.player.seek_simple(Gst.Format.TIME,  Gst.SeekFlags.FLUSH | Gst.SeekFlags.KEY_UNIT,0)

    def forward_seek_audio(self,*a):
        if  self.player.get_state(Gst.CLOCK_TIME_NONE )[1]==Gst.State.PLAYING:
            pos = self.player.query_position(Gst.Format.TIME)
            if pos :
                pos = pos[1]
                if pos>=0:
                    self.player.seek_simple(Gst.Format.TIME,  Gst.SeekFlags.FLUSH | Gst.SeekFlags.KEY_UNIT,pos+(2*1000000000))

    def play_stop_audio(self,*a):
        if self.props.autoplay:
            self.parent.toolbar.auto_play_button.props.active = False
            self.props.autoplay = False
        if self.player.get_state(Gst.CLOCK_TIME_NONE )[1]==Gst.State.PLAYING:
            self.stop()
        else:
            self.play()

