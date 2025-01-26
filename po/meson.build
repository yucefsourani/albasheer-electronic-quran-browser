add_global_arguments('-DGETTEXT_PACKAGE="@0@"'.format (meson.project_name()), language:'c')

i18n.gettext(meson.project_name(),
    args: '--directory=' + meson.project_source_root(),
    preset: 'glib'
)