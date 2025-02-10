Name:           albasheer
Version:        3.0
Release:        1%{?dist}
Summary:        Electronic Quran Browser
License:        GPLv3     
URL:            https://github.com/yucefsourani/albasheer-electronic-quran-browser
Source0:        https://github.com/yucefsourani/albasheer-electronic-quran-browser/archive/master.zip
BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  gtk-update-icon-cache
BuildRequires:  desktop-file-utils
BuildRequires:  meson
BuildRequires:  gettext
BuildRequires:  glib2-devel
BuildRequires:  libappstream-glib
Requires:       amiri-fonts
Requires:       amiri-quran-fonts
Requires:       amiri-quran-colored-fonts
Requires:       python3-gobject
Requires:       libadwaita
Requires:       gtk4
Requires:       gettext
Requires:       gnome-icon-theme
Requires:       gstreamer1
Requires:       gstreamer1-plugins-base
Requires:       gstreamer1-plugins-good
Requires:       libjpeg
Requires:       libpng

%description
Electronic Quran Browser.


%prep
%autosetup -n albasheer-electronic-quran-browser-master

%build
%meson
%meson_build

%install
rm -rf $RPM_BUILD_ROOT
%meson_install

%check
%meson_test

%find_lang albasheer
%files -f albasheer.lang
%doc README README-ar.txt
%license README README-ar.txt
%{_bindir}/albasheer
%{_datadir}/applications/*
%{_datadir}/albasheer/*
%{_datadir}/dbus-1/services/*
%{_datadir}/pixmaps/*
%{_datadir}/icons/hicolor/*/apps/*
%{_datadir}/glib-2.0/schemas/*
%{python3_sitelib}/albasheerlib/*
%{_metainfodir}/*


%changelog
* Mon Feb 10 2025 yucuf sourani <youssef.m.sourani@gmail.com> 3.0-1
- Initial
