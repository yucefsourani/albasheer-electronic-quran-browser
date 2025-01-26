from gi.repository import Adw
from gi.repository import Gtk,Pango
import albasheerlib.core

def on_b_clicked(button,parent_window,sura,aya):
    i = parent_window.sidelistbox.get_row_at_index(sura-1)
    if i:
        i.get_child().emit("clicked")
        parent_window.props.sura = sura
        parent_window.props.aya  = aya
        parent_window.scrool_to_aya()

def on_search_text_changed(entry,list_box,parent_window):
    parent_window = search_window.get_parent().get_parent()
    list_box.remove_all()
    text = entry.props.text.strip()
    if len(text)>=2 :
        for i in parent_window.ix.findPartial(text.split()):
            sura, aya = parent_window.albasheercore.suraAyaFromAyaId(i)
            name = parent_window.albasheercore.suraInfoById[sura-1][0]
            a = parent_window.albasheercore.ayaIdFromSuraAya(sura,aya)
            a = list(parent_window.albasheercore.getAyatIter(a))[0][1][:103]
            #self.ls.append([i, "%03d %s - %03d" % (sura, name, aya), sura, aya,])
            l = Gtk.Label.new()
            l.set_ellipsize( Pango.EllipsizeMode.END)
            b = Gtk.Button.new()
            b.add_css_class("flat")
            b.add_css_class("amiri")
            list_box.append(b)
            l.props.label = f"{sura} {name} - {aya} {a}..."
            b.set_child(l)
            b.connect("clicked",on_b_clicked,parent_window,sura,aya)



search_window = Adw.PreferencesDialog.new()
search_window.set_title(_("Search"))
search_page   =  Adw.PreferencesPage.new()
search_window.add(search_page)

search_page_group =  Adw.PreferencesGroup.new()
search_page.add(search_page_group)
search_page_group.set_title(_("Search For Aya"))
search_row = Adw.EntryRow.new()
search_row.set_input_hints(Gtk.InputHints.NO_EMOJI )
search_page_group.add(search_row)


aya_page_group =  Adw.PreferencesGroup.new()
aya_page_group.set_size_request(-1, 200)
aya_page_group.vexpand = True
search_page.add(aya_page_group)
#aya_page_group.set_title("Aya")
list_box = Gtk.ListBox.new()

list_box.add_css_class("boxed-list")
aya_page_group.add(list_box)

search_row.connect("changed",on_search_text_changed,list_box,search_window)
