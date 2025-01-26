import gi
gi.require_version('Soup', '3.0')
from gi.repository import Adw
from gi.repository import Gtk,Soup,GLib, GObject
from .utl import ALLTILAWAINFO
import os
import threading
import json
from .utl import UnpackZipTilawa

class TilawaDownloadRow():
    def __init__(self,pparent,parent,json_file,albasheer_data,audio_data_location):
        self.pparent    = pparent
        self.parent     = parent
        self.json_file  = json_file
        self.albasheer_data      = albasheer_data
        self.audio_data_location = audio_data_location
        self.row   = Adw.ActionRow.new()

        buttonvbox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL)
        buttonvbox.set_valign(Gtk.Align.CENTER)
        self.row.add_suffix(buttonvbox)
        self.button_content = Adw.ButtonContent.new()
        self.button_content.set_icon_name("folder-download-symbolic")
        self.downloadbutton = Gtk.Button.new()
        self.downloadbutton.add_css_class("suggested-action")
        self.downloadbutton.set_child(self.button_content)
        buttonvbox.append(self.downloadbutton)


        self.cancel_button_content = Adw.ButtonContent.new()
        self.cancel_button_content.set_icon_name("media-playback-stop-symbolic")
        self.cancelbutton = Gtk.Button.new()
        self.cancelbutton.set_visible(False)
        self.cancelbutton.add_css_class("destructive-action")
        self.cancelbutton.set_child(self.cancel_button_content)
        buttonvbox.append(self.cancelbutton)
        self.parent.list_box.append(self.row )
        self.cancelbutton.connect("clicked",self.on_cancel_button_clicked)

        self.check()

    def check(self):
        t = threading.Thread(target=self._check)
        t.daemon = True
        t.start()

    def _check(self):
        with open(self.json_file) as mf:
            self.data_info       = json.load(mf)
        self.name_               = self.data_info["name"]
        self.links               = self.data_info["links"]
        self.allmaxsize          = sum([i[2] for i in self.links ])
        self.loop                = False
        self.audio_data_location = os.path.join(self.audio_data_location,self.name_)
        self.tilawa_download_files_location = os.path.join(self.albasheer_data,"tilawa_download_files",self.name_)
        GLib.idle_add(self.row.set_title,self.name_)


        self.current_size = 0
        if not os.path.exists(self.tilawa_download_files_location):
            os.makedirs(self.tilawa_download_files_location,exist_ok=True)
        else:
            self.current_size += sum([os.stat(os.path.join(self.tilawa_download_files_location,f)).st_size for f in os.listdir(self.tilawa_download_files_location) if os.path.isfile(os.path.join(self.tilawa_download_files_location,f))])
        GLib.idle_add(self.row.set_subtitle,f"{self.data_info['link_count']} Files  {int(self.current_size/1024/1024)}MB/{int(self.allmaxsize/1024/1024)}MB")
        self.current_download_percentage =  int(self.current_size*100/self.allmaxsize)
        GLib.idle_add(self.downloadbutton.set_label,str(self.current_download_percentage)+"%")
        if self.current_download_percentage >= 100:
            GLib.idle_add(self.downloadbutton.set_label,"100%")
            GLib.idle_add(self.row.set_subtitle,f"{self.data_info['link_count']} Files  {int(self.allmaxsize/1024/1024)}MB/{int(self.allmaxsize/1024/1024)}MB")
            GLib.idle_add(self.button_content.set_icon_name,"archive-extract-symbolic")
            self.downloadbutton.connect("clicked",self.extract_all)

        else:
            self.downloadbutton.connect("clicked",self.start)

    def extract_all(self,button=None):
        GLib.idle_add(self.downloadbutton.set_sensitive,False)
        all_zip_files = [os.path.join(self.tilawa_download_files_location,i[1]) for i in self.links]
        UnpackZipTilawa(all_zip_files,self.audio_data_location,self.pparent,self.parent,self.name_).start()

    def start(self,button=None):
        t = threading.Thread(target=self.run)
        t.setDaemon(True)
        t.start()

    def on_cancel_button_clicked(self,button):
        self.loop = False

    def run(self):
        GLib.idle_add(self.parent.parent.mstack.get_page(self.parent.parent.mstack.get_child_by_name("vbox3")).set_needs_attention,False)
        GLib.idle_add(self.row.remove_css_class,"error")
        GLib.idle_add(self.downloadbutton.set_visible,False)
        GLib.idle_add(self.cancelbutton.set_visible,True)
        self.unfinished_download_file = {}
        for i in self.links:
            f = os.path.join(self.tilawa_download_files_location,i[1])
            if not os.path.exists(f):
                self.unfinished_download_file.setdefault(i[0],(f,i[2],0))
            else:
                if os.stat(f).st_size!=i[2] :
                    self.unfinished_download_file.setdefault(i[0],(f,i[2],os.stat(f).st_size))
        self.current_size = 0
        self.current_size += sum([os.stat(os.path.join(self.tilawa_download_files_location,f)).st_size for f in os.listdir(self.tilawa_download_files_location) if os.path.isfile(os.path.join(self.tilawa_download_files_location,f))])
        GLib.idle_add(self.row.set_subtitle,f"{self.data_info['link_count']} Files  {int(self.current_size/1024/1024)}MB/{int(self.allmaxsize/1024/1024)}MB")
        self.current_download_percentage =  int(self.current_size*100/self.allmaxsize)
        GLib.idle_add(self.downloadbutton.set_label,str(self.current_download_percentage)+"%")
        GLib.idle_add(self.cancel_button_content.set_label,str(self.current_download_percentage)+"%")
        try:
            self.loop = True
            for d_link,d_file_info in self.unfinished_download_file.items():
                if not self.loop:
                    self.loop = False
                    GLib.idle_add(self.downloadbutton.set_label,str(self.current_download_percentage)+"%")
                    GLib.idle_add(self.downloadbutton.set_visible,True)
                    GLib.idle_add(self.cancelbutton.set_visible,False)
                    return

                self.session = Soup.Session.new()
                self.session.props.timeout = 10
                self.msg  = Soup.Message.new("GET", d_link)
                self.msg.props.request_headers.append("Range",f"bytes={d_file_info[2]}-{d_file_info[1]}")
                input_stream = self.session.send(self.msg,None)
                self.file_ = open(d_file_info[0],"a+b")

                while self.loop:
                    chunk = input_stream.read_bytes(1024*1024,None)
                    chunk_size = chunk.get_size()
                    if chunk_size>0:
                        self.current_size += chunk_size
                        GLib.idle_add(self.row.set_subtitle,f"{self.data_info['link_count']} Files  {int(self.current_size/1024/1024)}MB/{int(self.allmaxsize/1024/1024)}MB")
                        self.current_download_percentage = int(self.current_size*100/self.allmaxsize)
                        GLib.idle_add(self.cancel_button_content.set_label,str(self.current_download_percentage)+"%")
                        self.file_.write(chunk.unref_to_data())
                        self.file_.flush()
                    else:
                        break
                self.file_.close()
                input_stream.close()
        except Exception as e:
            self.loop = False
            GLib.idle_add(self.downloadbutton.set_label,str(self.current_download_percentage)+"%")
            GLib.idle_add(self.row.add_css_class,"error")
            if self.parent.parent.mstack.props.visible_child_name != "vbox3":
                GLib.idle_add(self.parent.parent.mstack.get_page(self.parent.parent.mstack.get_child_by_name("vbox3")).set_needs_attention,True)
            GLib.idle_add(self.pparent.toastoverlay.add_toast,Adw.Toast(title=_("Download File Faild"),timeout=0))
            GLib.idle_add(self.pparent.toastoverlay.add_toast,Adw.Toast(title=str(e),timeout=0))
            print(e)
            try:
                input_stream.close()
                self.file_.close()
            except Exception as e:
                pass
        finally:
            #GLib.idle_add(self.cancel_button_content.set_label,"")
            GLib.idle_add(self.downloadbutton.set_visible,True)
            GLib.idle_add(self.cancelbutton.set_visible,False)
        if self.loop :
            GLib.idle_add(self.downloadbutton.set_label,"100%")
            GLib.idle_add(self.downloadbutton.set_sensitive,False)
            GLib.idle_add(self.cancel_button_content.set_sensitive,False)
            GLib.idle_add(self.cancel_button_content.set_label,"100%")
            GLib.idle_add(self.row.set_subtitle,f"{self.data_info['link_count']} Files  {int(self.allmaxsize/1024/1024)}MB/{int(self.allmaxsize/1024/1024)}MB")
            if self.unfinished_download_file:
                self.extract_all()

class TilawaDownloadGui(GObject.Object):
    __gsignals__ = { "result"     : (GObject.SignalFlags.RUN_LAST, None, (str,str,bool))}

    def __init__(self,parent,albasheer_data,audio_data_location):
        GObject.Object.__init__(self)
        self.parent = parent
        self.albasheer_data = albasheer_data
        self.audio_data_location = audio_data_location
        self.mainvb = Gtk.Box(orientation = Gtk.Orientation.VERTICAL)
        self.search_page =  Adw.PreferencesPage.new()
        self.search_page_group =  Adw.PreferencesGroup.new()
        self.search_page.add(self.search_page_group)
        self.search_page_group.set_title(_("Search For Tilawa"))
        self.mainvb.append(self.search_page)
        self.search_row = Adw.EntryRow.new()
        self.search_row.set_input_hints(Gtk.InputHints.NO_EMOJI )
        self.search_row.connect("changed",self.on_search_text_changed)
        self.search_page_group.add(self.search_row)

        self.tilawa_page =  Adw.PreferencesPage.new()
        self.tilawa_page_group =  Adw.PreferencesGroup.new()
        self.tilawa_page.add(self.tilawa_page_group)
        #self.tilawa_page_group.set_title("Download Tilawa")
        self.list_box= Gtk.ListBox.new()
        self.list_box.add_css_class("boxed-list")
        self.list_box.set_filter_func(self.listbox_filter_function,self.search_row)
        self.tilawa_page_group.add(self.list_box)
        self.mainvb.append(self.tilawa_page)

        self.tilawa_json_location = os.path.join(os.path.dirname(__file__),"tilawa_json_files")
        for i in os.listdir(self.tilawa_json_location):
            l = os.path.join(self.tilawa_json_location,i)
            t = TilawaDownloadRow(self.parent,self,l,self.albasheer_data,self.audio_data_location)

    def on_search_text_changed(self,search_entry):
        self.list_box.invalidate_filter()

    def listbox_filter_function(self,row,search_entry):
        text = search_entry.props.text.strip().lower()
        if not text:
            return True
        if text in row.props.title.lower() or text in row.props.subtitle.lower():
            return True
        return False
