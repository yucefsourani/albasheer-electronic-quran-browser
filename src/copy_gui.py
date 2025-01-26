from gi.repository import GLib,Adw,Gtk,Gio,Gdk
from .utl import suwar_info

def cp_cb(button,parent_window,comborow,from_row,to_row,imla_row,per_line_row):
    sura = comborow.props.selected + 1
    aya1 = from_row.get_value()
    aya2 = to_row.get_value()
    n = aya2 - aya1 + 1
    i = imla_row.get_active()
    a = [' ', '\n', ' * ', ' *\n']
    s = a[int(i) * 2 + int(per_line_row.get_active())]
    s = s.join([l[i] for l in parent_window.albasheercore.getSuraIter(sura, n, aya1)]) + '\n'
    clipboard = parent_window.get_clipboard()
    clipboard.set_content(Gdk.ContentProvider.new_for_value(s))

def on_combo_selected_item_changed(comborow,prop,parent_window,from_row,to_row):
    sura = comborow.props.selected
    m = parent_window.albasheercore.suraInfoById[sura][5]
    from_row.set_adjustment(Gtk.Adjustment(lower=1,upper=m,step_increment=1))
    to_row.set_adjustment(Gtk.Adjustment(lower=1,upper=m,step_increment=1))
    from_row.set_value(1)
    to_row.set_value(m)

def make_copy_window(parent_window):
    copy_window = Adw.PreferencesDialog.new()
    copy_window.set_title(_("Copy"))
    copy_page   =  Adw.PreferencesPage.new()
    copy_window.add(copy_page)

    copy_page_group =  Adw.PreferencesGroup.new()
    copy_page_group.set_size_request(-1, 300)
    copy_page.add(copy_page_group)
    copy_page_group.set_title(_("Copy Ayat"))

    copy_button_content = Adw.ButtonContent(label=_("Clipboard"),icon_name="edit-copy-symbolic")
    copy_button = Gtk.Button.new()
    copy_button.set_child(copy_button_content)
    copy_button.add_css_class("suggested-action")
    copy_page_group.set_header_suffix(copy_button)

    stringlist = Gio.ListStore.new(Gtk.StringObject)
    single_selection_list_store = Gtk.SingleSelection.new(stringlist)
    comborow = Adw.ComboRow.new()
    copy_page_group.add(comborow)
    comborow.set_model(single_selection_list_store)
    comborow.add_prefix(Gtk.Image.new_from_icon_name("view-list-symbolic"))

    sura_ls = tuple(f"{i+1}. {j[0]}" for (i,j) in enumerate(parent_window.albasheercore.suraInfoById))
    for k in  sura_ls:
        stringlist.append(Gtk.StringObject.new(k))

    aya_from_row = Adw.SpinRow.new_with_range(1,7,1)
    aya_from_row.props.title = _("From Aya")
    copy_page_group.add(aya_from_row)
    aya_to_row   = Adw.SpinRow.new_with_range(1,7,1)
    aya_to_row.props.value = 7
    aya_to_row.props.title = _("To Aya")
    copy_page_group.add(aya_to_row)

    imla_style_row = Adw.SwitchRow.new()
    imla_style_row.props.title = _("Imla'i style")
    imla_style_row.set_active(True)
    copy_page_group.add(imla_style_row)

    aya_per_line_row = Adw.SwitchRow.new()
    aya_per_line_row.props.title = _("an Aya per line")
    copy_page_group.add(aya_per_line_row)

    comborow.connect("notify::selected-item",on_combo_selected_item_changed,parent_window,aya_from_row,aya_to_row)
    copy_button.connect("clicked",cp_cb,parent_window,comborow,aya_from_row,aya_to_row,imla_style_row,aya_per_line_row)
    return copy_window
