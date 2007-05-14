Name: TeXmacs
Version: 1.0.6.10
Release: %mkrel 1
Summary: WYSIWYG mathematical text editor
URL: http://www.texmacs.org/
Source0: ftp://ftp.texmacs.org/pub/TeXmacs/targz/%{name}-%{version}-src.tar.gz
Source10: %{name}.16.png
Source11: %{name}.32.png
Source12: %{name}.48.png
Patch0: %{name}-1.0.6.10-build.patch
License: GPL
Group: Editors
Requires: tetex
Requires: guile
Requires: R-base
Requires: axiom
Requires: maxima >= 5.9.1
Obsoletes: TeXmacs-fonts
Provides: TeXmacs-fonts
BuildRequires: X11-devel 
BuildRequires: libguile-devel
BuildRequires: desktop-file-utils
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
GNU TeXmacs is a free scientific text editor, which was both inspired by 
TeX and GNU Emacs. The editor allows you to write structured documents via 
a wysiwyg (what-you-see-is-what-you-get) and user friendly interface. New 
styles may be created by the user. The program implements high-quality 
typesetting algorithms and TeX fonts, which help you to produce professionally 
looking documents.

The high typesetting quality still goes through for automatically generated 
formulas, which makes TeXmacs suitable as an interface for computer algebra 
systems. TeXmacs also supports the Guile/Scheme extension language, so that 
you may customize the interface and write your own extensions to the editor.

TeXmacs currently runs on PC's and PPC's under Gnu/linux (a >200MHz processor 
and >32Mb of memory are recommended) and on sun computers. Converters exist 
for TeX/LaTeX and they are under development for Html/Mathml/Xml. In the 
future, TeXmacs is planned to evoluate towards a complete scientific office 
suite, with spreadsheet capacities, a technical drawing editor and a 
presentation mode.

%prep
%setup -q -n %{name}-%{version}-src
%patch0 -p1

%build
%configure2_5x --disable-optimize
%make TEXMACS

%install
rm -rf %{buildroot}
%{makeinstall_std}
export GUILE_DATA_PATH=`guile-config info pkgdatadir`
export GUILE_LOAD_PATH=`find $GUILE_DATA_PATH -type d | grep ice-9`

# fix calls for R >= 2.0.0
(cd %{buildroot}%{_datadir}/TeXmacs/plugins/r/r/
R CMD build --force TeXmacs
R CMD INSTALL -l `pwd` TeXmacs_0.1.tar.gz)

# icons
install -d %{buildroot}%{_miconsdir}
install -d %{buildroot}%{_liconsdir}
cp -a %{SOURCE10} %{buildroot}%{_miconsdir}/%{name}.png
cp -a %{SOURCE11} %{buildroot}%{_iconsdir}/%{name}.png
cp -a %{SOURCE12} %{buildroot}%{_liconsdir}/%{name}.png

mkdir -p  %{buildroot}%_datadir/applications
cp -a %{buildroot}%_datadir/TeXmacs/misc/mime/texmacs.desktop %{buildroot}%_datadir/applications/

# menu
install -d %{buildroot}%{_menudir}
cat << EOF > %{buildroot}%{_menudir}/%{name}
?package(%{name}):command="texmacs" \
needs="x11" \
icon="%{name}.png" \
section="Office/Wordprocessors" \
title="TeXmacs editor" \
longtitle="A WYSIWYG scientific text editor" \
xdg="true"
EOF

desktop-file-install --vendor="" \
  --remove-category="Application" \
  --add-category="X-MandrivaLinux-Office-Wordprocessors;Office;WordProcessor" \
  --dir %{buildroot}%{_datadir}/applications %{buildroot}%{_datadir}/applications/*

%clean
rm -rf %{buildroot}

%post
%{update_menus}

%postun
%{clean_menus}

%files
%defattr(-,root,root)
%{_bindir}/*
%{_includedir}/TeXmacs.h
%{_mandir}/*/*
%{_libexecdir}/TeXmacs
%{_datadir}/TeXmacs
%{_menudir}/%{name}
%{_miconsdir}/%{name}.png
%{_iconsdir}/%{name}.png
%{_liconsdir}/%{name}.png
%{_datadir}/applications/*
