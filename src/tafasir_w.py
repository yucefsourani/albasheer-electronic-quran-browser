import gi
gi.require_version('Soup', '3.0')
from gi.repository import Adw
from gi.repository import Gtk
from gi.repository import GObject,Gio,Gdk,GLib,Soup,Pango
import os
import re
from .utl import UnpackZipTafasirTaragem
import tempfile
import sqlite3
from .utl import FONT_SIZE

class TafasirW():
    def __init__(self,parent,tafasir_data_location,taragem_data_location):
        self.parent = parent
        self.tafasir_data_location = tafasir_data_location
        self.taragem_data_location = taragem_data_location
        self.mainvb = Gtk.Box(orientation = Gtk.Orientation.VERTICAL)
        self.mainvb.props.hexpand = True
        self.mainvb.props.vexpand = True
        self.tabbar = Adw.TabBar.new()
        self.tabbar.props.extra_drag_preload = False
        self.mainvb.append(self.tabbar)
        self.tabview = Adw.TabView.new()
        self.tabview.connect("close_page",self.on_close_tabpage)
        self.tabbar.set_view(self.tabview)
        self.mainvb.append(self.tabview)

        self.tafasirtool = Tafasir(self.parent,self.tafasir_data_location)
        tafasir_tabpage = self.tabview.append(self.tafasirtool.mainvb)
        tafasir_tabpage.set_title(_("Tafasir"))

        self.taragemtool = Taragem(self.parent,self.taragem_data_location)
        taragem_tabpage = self.tabview.append(self.taragemtool.mainvb)
        taragem_tabpage.set_title(_("Tarajem"))

    def on_close_tabpage(self,*a):
        return Gdk.EVENT_STOP

class Tafasir(GObject.Object):
    __gsignals__ = { "result"     : (GObject.SignalFlags.RUN_LAST, None, (bool,))}

    @GObject.Property(type=str,default="")
    def table(self):
        return self.__table

    @table.setter
    def set_table(self, table):
        if self.__table != table:
            self.__table = table

    def __init__(self,parent,tafasir_data_location):
        GObject.Object.__init__(self)
        self.parent = parent
        self.cleanr       = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
        self.__check = True
        self.tafasir_data_location = tafasir_data_location
        self.ayt_file_location = os.path.join(tempfile.mkdtemp(),"tafasir.ayt")
        self.mainvb = Gtk.Box(orientation = Gtk.Orientation.VERTICAL)
        self.mainvb.set_name("mainb_t")
        self.__all_tafasir = self.get_all_tafasir_location()
        self.count = 0
        self.text_v   = Gtk.TextView()
        #self.text_v.modify_font(Pango.FontDescription.from_string("Amiri 32"))
        self.text_v.set_hexpand(True)
        self.text_v.set_vexpand(True)
        self.text_v.props.editable = False
        self.text_v.props.cursor_visible = False
        self.text_v.props.justification = Gtk.Justification.CENTER
        self.text_v.props.wrap_mode = Gtk.WrapMode.WORD
        self.buffer   = self.text_v.get_buffer()
        self.__table  = self.parent.app_settings.get_string("tafasir-table")
        self.parent.app_settings.bind("tafasir-table", self, "table",Gio.SettingsBindFlags.DEFAULT)
        if not self.__all_tafasir:
            self.statuspage = Adw.StatusPage.new()
            self.statuspage.props.vexpand = True
            self.statuspage.props.icon_name = "action-unavailable-symbolic"
            self.statuspage.props.title = _("Tafasir unavailable")
            self.statuspage.props.description = _("Download Tafasir")
            self.button_content = Adw.ButtonContent.new()
            self.button_content.set_icon_name("folder-download-symbolic")

            self.downloadbutton = Gtk.Button.new()
            self.downloadbutton.add_css_class("suggested-action")
            self.downloadbutton.set_child(self.button_content)
            b_clamp = Adw.Clamp(maximum_size=200,child=self.downloadbutton)
            self.downloadbutton.connect("clicked",self.on_download_button_clicked)
            self.statuspage.set_child(b_clamp)
            self.mainvb.append(self.statuspage)
            self.connect("result",self.on_unpack_file_finish)
        else:
            self.build_gui(False)

    def on_unpack_file_finish(self,gobject,result):
        if result:
            self.build_gui()

    def build_gui(self,rebuild=True):
        if rebuild:
            self.__all_tafasir = self.get_all_tafasir_location()
            if not self.__all_tafasir:
                return
            self.mainvb.remove(self.statuspage)

        listbox = Gtk.ListBox.new()
        listbox.set_css_classes(["boxed-list"])
        combo_clamp  = Adw.Clamp(maximum_size=180,child=listbox)
        combo_clamp.props.margin_top = 10
        combo_clamp.props.margin_bottom = 10
        self.stringlist = Gtk.StringList.new(None)
        self.single_selection_list_store = Gtk.SingleSelection.new(self.stringlist)
        self.comborow = Adw.ComboRow.new()
        self.comborow.set_name("combo_t")
        self.comborow.set_model(self.single_selection_list_store)
        self.comborow.add_prefix(Gtk.Image.new_from_icon_name("view-list-symbolic"))
        listbox.append(self.comborow)
        self.mainvb.append(combo_clamp)
        #self.aya_label = Gtk.Label.new()
        #self.aya_label.props.margin_bottom = 10
        #self.aya_label.set_wrap(True)
        #self.aya_label.set_wrap_mode(Pango.WrapMode.WORD)
        #self.aya_label.set_css_classes(["amiri",FONT_SIZE[self.parent.props.font_size]])
        #self.mainvb.append(self.aya_label)

        sw=Gtk.ScrolledWindow()
        self.text_v.props.margin_start = 10
        self.text_v.props.margin_end = 10
        self.text_v.props.margin_top = 10
        self.text_v.props.margin_bottom = 10
        self.text_v.set_css_classes(["amiri",FONT_SIZE[self.parent.props.font_size]])
        sw.set_policy(Gtk.PolicyType.AUTOMATIC,Gtk.PolicyType.AUTOMATIC)
        sw.set_child(self.text_v)
        self.mainvb.append(sw)
        for table in self.__all_tafasir.keys():
            self.stringlist.append(table)

        if self.props.table in self.__all_tafasir.keys():
            self.comborow.set_selected(list(self.__all_tafasir.keys()).index(self.props.table))
        else:
            self.comborow.set_selected(0)
        self.comborow.connect("notify::selected-item",self.on_selected_item_changed)
        self.aya_info()

    def on_selected_item_changed(self,combo, props):
        table = combo.props.selected_item.props.string
        self.props.table = table
        self.aya_info()

    def in_text(self,line,end="\n\n"):
        line = line+end
        self.buffer.insert_markup(self.buffer.get_end_iter(),line,-1)

    def clear_text(self):
        start = self.buffer.get_start_iter()
        end = self.buffer.get_end_iter()
        self.buffer.delete(start, end)


    def on_download_button_clicked(self,button):
        button.set_sensitive(False)
        self.session = Soup.Session.new()
        self.msg  = Soup.Message.new("GET", "http://quran.ksu.edu.sa/ayat/tafasir.ayt")
        self.session.send_async(self.msg,GLib.PRIORITY_LOW,None,self.on_connect_finish,None)

    def on_connect_finish(self,session, result, data):
        try:
            input_stream = session.send_finish(result)
            self.size = self.msg.props.response_headers.get_content_length()

            self.file_ = open(self.ayt_file_location,"a+b")
            input_stream.read_bytes_async(1024*500,GLib.PRIORITY_HIGH_IDLE  ,None,self.on_read_finish)
        except Exception as e:
            self.count = 0
            self.button_content.set_label("")
            self.downloadbutton.set_sensitive(True)
            self.parent.toastoverlay.add_toast(Adw.Toast(title=_("Connect Faild"),timeout=0)) #If timeout is 0, the toast is displayed indefinitely until manually dismissed
            print(e)

    def on_read_finish(self,input_stream, result):
        try:
            chunk = input_stream.read_bytes_finish(result)
            chunk_size = chunk.get_size()
            if chunk_size>0:
                self.count += chunk_size
                r = int(self.count*100/self.size)
                self.button_content.set_label(str(r)+"%")
                self.file_.write(chunk.unref_to_data())
                input_stream.read_bytes_async(1024*500,GLib.PRIORITY_HIGH_IDLE  ,None,self.on_read_finish)
            else:
                #self.current_pixbuf.__picture_type = self.msg.props.response_headers.get_one("Content-Type").split("/")[1]
                #self.current_pixbuf.__file_name = self.msg.props.response_headers.get_one("x-imgix-id")+"."+self.current_pixbuf.__picture_type
                self.file_.close()
                input_stream.close()
                self.count = 0
                self.downloadbutton.set_sensitive(True)
                UnpackZipTafasirTaragem([self.ayt_file_location],self.tafasir_data_location,self.parent,self).start()
        except Exception as e:
            self.count = 0
            self.button_content.set_label("")
            self.downloadbutton.set_sensitive(True)
            self.parent.toastoverlay.add_toast(Adw.Toast(title=_("Download File Faild"),timeout=0))
            print(e)
            try:
                input_stream.close()
                self.file_.close()
            except Exception as e:
                pass
            print(e)

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

    def aya_info(self,text="text"):
        if  not self.__all_tafasir:
            return
        self.clear_text()
        table = self.comborow.get_selected_item().props.string
        if not table:
            return
        db    = self.__all_tafasir[table]
        try:
            conn = sqlite3.connect(db)
            c = conn.cursor()
            if self.parent.props.sura in  (9,1):
                aya_n = self.parent.props.aya + 1
                aya = self.parent.albasheercore.getAyatIter(self.parent.albasheercore.ayaIdFromSuraAya(self.parent.props.sura,self.parent.props.aya+1)).fetchall()[0][0]
            else:
                aya_n = self.parent.props.aya
                if aya_n == 0:
                    aya = self.parent.albasheercore.basmala
                    self.in_text("<span foreground='#00FFFF'>{}</span>".format(aya))
                    #self.aya_label.set_markup("<span foreground='#00FFFF'>{}</span>".format(aya))
                    return
                else:
                    aya = self.parent.albasheercore.getAyatIter(self.parent.albasheercore.ayaIdFromSuraAya(self.parent.props.sura,self.parent.props.aya)).fetchall()[0][0]
            c.execute('SELECT {} FROM {} where sura=? and aya=? ;'.format(text,table),(self.parent.props.sura,aya_n))
            rows = c.fetchall()
            if rows:
                #sura =  self.parent.sidelistbox.get_row_at_index(self.props.sura-1).get_child().get_label()
                #self.in_text("<span foreground='blue' size='x-large' weight='bold'>{}</span>".format(self.sura))
                self.in_text("<span foreground='#00FFFF'>{}</span>".format(aya))
                #self.aya_label.set_markup("<span foreground='#00FFFF'>{}</span>".format(aya))
                row = rows[0]
                if row:
                    txt = re.sub(self.cleanr, '', row[0].replace("</p>","\n").replace("<br>","\n"))
                    self.in_text(txt)
        except sqlite3.OperationalError:
            return self.aya_info("tafsir")

        except Exception as e:
            print(e)
            return False
        finally :
            if conn:
                conn.close()


class Taragem(GObject.Object):
    __gsignals__ = { "result"     : (GObject.SignalFlags.RUN_LAST, None, (bool,))}

    @GObject.Property(type=str,default="")
    def table(self):
        return self.__table

    @table.setter
    def set_table(self, table):
        if self.__table != table:
            self.__table = table

    def __init__(self,parent,taragem_data_location):
        GObject.Object.__init__(self)
        self.parent = parent
        self.cleanr       = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
        self.__check = True
        self.taragem_data_location = taragem_data_location
        self.ayt_file_location = os.path.join(tempfile.mkdtemp(),"tarajem.ayt")
        self.mainvb = Gtk.Box(orientation = Gtk.Orientation.VERTICAL)
        self.mainvb.set_name("mainb_t")
        self.__all_taragem = self.get_all_taragem_location()
        self.count = 0
        self.text_v   = Gtk.TextView()
        self.text_v.set_hexpand(True)
        self.text_v.set_vexpand(True)
        self.text_v.props.editable = False
        self.text_v.props.cursor_visible = False
        self.text_v.props.justification = Gtk.Justification.CENTER
        self.text_v.props.wrap_mode = Gtk.WrapMode.WORD
        self.buffer   = self.text_v.get_buffer()
        self.__table  = self.parent.app_settings.get_string("taragem-table")
        self.parent.app_settings.bind("taragem-table", self, "table",Gio.SettingsBindFlags.DEFAULT)
        if not self.__all_taragem:
            self.statuspage = Adw.StatusPage.new()
            self.statuspage.props.vexpand = True
            self.statuspage.props.icon_name = "action-unavailable-symbolic"
            self.statuspage.props.title = _("Tarajem unavailable")
            self.statuspage.props.description = _("Download Tarajem")
            self.button_content = Adw.ButtonContent.new()
            self.button_content.set_icon_name("folder-download-symbolic")

            self.downloadbutton = Gtk.Button.new()
            self.downloadbutton.add_css_class("suggested-action")
            self.downloadbutton.set_child(self.button_content)
            b_clamp = Adw.Clamp(maximum_size=200,child=self.downloadbutton)
            self.downloadbutton.connect("clicked",self.on_download_button_clicked)
            self.statuspage.set_child(b_clamp)
            self.mainvb.append(self.statuspage)
            self.connect("result",self.on_unpack_file_finish)
        else:
            self.build_gui(False)

    def on_unpack_file_finish(self,gobject,result):
        if result:
            self.build_gui()

    def build_gui(self,rebuild=True):
        if rebuild:
            self.__all_taragem = self.get_all_taragem_location()
            if not self.__all_taragem:
                return
            self.mainvb.remove(self.statuspage)

        listbox = Gtk.ListBox.new()
        listbox.set_css_classes(["boxed-list"])
        combo_clamp  = Adw.Clamp(maximum_size=180,child=listbox)
        combo_clamp.props.margin_top = 10
        combo_clamp.props.margin_bottom = 10
        self.stringlist = Gtk.StringList.new(None)
        self.single_selection_list_store = Gtk.SingleSelection.new(self.stringlist)
        self.comborow = Adw.ComboRow.new()
        self.comborow.set_name("combo_t")
        self.comborow.set_model(self.single_selection_list_store)
        self.comborow.add_prefix(Gtk.Image.new_from_icon_name("view-list-symbolic"))
        listbox.append(self.comborow)
        self.mainvb.append(combo_clamp)

        #self.aya_label = Gtk.Label.new()
        #self.aya_label.set_wrap(True)
        #self.aya_label.props.margin_bottom = 10
        #self.aya_label.set_wrap_mode(Pango.WrapMode.WORD)
        #self.aya_label.set_css_classes(["amiri",FONT_SIZE[self.parent.props.font_size]])
        #self.mainvb.append(self.aya_label)

        sw=Gtk.ScrolledWindow()
        self.text_v.props.margin_start = 10
        self.text_v.props.margin_end = 10
        self.text_v.props.margin_top = 10
        self.text_v.props.margin_bottom = 10
        self.text_v.set_css_classes(["amiri",FONT_SIZE[self.parent.props.font_size]])
        sw.set_policy(Gtk.PolicyType.AUTOMATIC,Gtk.PolicyType.AUTOMATIC)
        sw.set_child(self.text_v)
        self.mainvb.append(sw)
        for table in self.__all_taragem.keys():
            self.stringlist.append(table)

        if self.props.table in self.__all_taragem.keys():
            self.comborow.set_selected(list(self.__all_taragem.keys()).index(self.props.table))
        else:
            self.comborow.set_selected(0)
        self.comborow.connect("notify::selected-item",self.on_selected_item_changed)
        self.aya_info()

    def on_selected_item_changed(self,combo, props):
        table = combo.props.selected_item.props.string
        self.props.table = table
        self.aya_info()

    def in_text(self,line,end="\n\n"):
        line = line+end
        self.buffer.insert_markup(self.buffer.get_end_iter(),line,-1)

    def clear_text(self):
        start = self.buffer.get_start_iter()
        end = self.buffer.get_end_iter()
        self.buffer.delete(start, end)


    def on_download_button_clicked(self,button):
        button.set_sensitive(False)
        self.session = Soup.Session.new()
        self.msg  = Soup.Message.new("GET", "http://quran.ksu.edu.sa/ayat/tarajem.ayt")
        self.session.send_async(self.msg,GLib.PRIORITY_LOW,None,self.on_connect_finish,None)

    def on_connect_finish(self,session, result, data):
        try:
            input_stream = session.send_finish(result)
            self.size = self.msg.props.response_headers.get_content_length()

            self.file_ = open(self.ayt_file_location,"a+b")
            input_stream.read_bytes_async(1024*500,GLib.PRIORITY_HIGH_IDLE  ,None,self.on_read_finish)
        except Exception as e:
            self.count = 0
            self.button_content.set_label("")
            self.downloadbutton.set_sensitive(True)
            self.parent.toastoverlay.add_toast(Adw.Toast(title=_("Connect Faild"),timeout=0)) #If timeout is 0, the toast is displayed indefinitely until manually dismissed
            print(e)

    def on_read_finish(self,input_stream, result):
        try:
            chunk = input_stream.read_bytes_finish(result)
            chunk_size = chunk.get_size()
            if chunk_size>0:
                self.count += chunk_size
                r = int(self.count*100/self.size)
                self.button_content.set_label(str(r)+"%")
                self.file_.write(chunk.unref_to_data())
                input_stream.read_bytes_async(1024*500,GLib.PRIORITY_HIGH_IDLE  ,None,self.on_read_finish)
            else:
                #self.current_pixbuf.__picture_type = self.msg.props.response_headers.get_one("Content-Type").split("/")[1]
                #self.current_pixbuf.__file_name = self.msg.props.response_headers.get_one("x-imgix-id")+"."+self.current_pixbuf.__picture_type
                self.file_.close()
                input_stream.close()
                self.count = 0
                self.downloadbutton.set_sensitive(True)
                UnpackZipTafasirTaragem([self.ayt_file_location],self.taragem_data_location,self.parent,self).start()
        except Exception as e:
            self.count = 0
            self.button_content.set_label("")
            self.downloadbutton.set_sensitive(True)
            self.parent.toastoverlay.add_toast(Adw.Toast(title=_("Download File Faild"),timeout=0))
            print(e)
            try:
                input_stream.close()
                self.file_.close()
            except Exception as e:
                pass
            print(e)

    def get_all_taragem_location(self):
        result = {}
        if not os.path.isdir(self.taragem_data_location):
            return False
        for dirname,folder,files in os.walk(self.taragem_data_location):
            for file_ in files:
                if file_.endswith(".db") or file_.endswith(".ayt") or file_.endswith(".sqlite"):
                    result.setdefault(file_.split(".",1)[0],os.path.join(dirname,file_))
        if result:
            return result
        return False

    def aya_info(self,text="text"):
        if  not self.__all_taragem:
            return
        self.clear_text()
        table = self.comborow.get_selected_item().props.string
        if not table:
            return
        db    = self.__all_taragem[table]
        try:
            conn = sqlite3.connect(db)
            c = conn.cursor()
            if self.parent.props.sura in  (9,1):
                aya_n = self.parent.props.aya + 1
                aya = self.parent.albasheercore.getAyatIter(self.parent.albasheercore.ayaIdFromSuraAya(self.parent.props.sura,self.parent.props.aya+1)).fetchall()[0][0]
            else:
                aya_n = self.parent.props.aya
                if aya_n == 0:
                    aya = self.parent.albasheercore.basmala
                    self.in_text("<span foreground='#00FFFF'>{}</span>".format(aya))
                    #self.aya_label.set_markup("<span foreground='#00FFFF'>{}</span>".format(aya))
                    return
                else:
                    aya = self.parent.albasheercore.getAyatIter(self.parent.albasheercore.ayaIdFromSuraAya(self.parent.props.sura,self.parent.props.aya)).fetchall()[0][0]
            c.execute('SELECT {} FROM {} where sura=? and aya=? ;'.format(text,table),(self.parent.props.sura,aya_n))
            rows = c.fetchall()
            if rows:
                #sura =  self.parent.sidelistbox.get_row_at_index(self.props.sura-1).get_child().get_label()
                #self.in_text("<span foreground='blue' size='x-large' weight='bold'>{}</span>".format(self.sura))
                self.in_text("<span foreground='#00FFFF'>{}</span>".format(aya))
                #self.aya_label.set_markup("<span foreground='#00FFFF'>{}</span>".format(aya))
                row = rows[0]
                if row:
                    txt = re.sub(self.cleanr, '', row[0].replace("</p>","\n").replace("<br>","\n"))
                    self.in_text(txt)
        except sqlite3.OperationalError:
            return self.aya_info("tafsir")

        except Exception as e:
            print(e)
            return False
        finally :
            if conn:
                conn.close()

