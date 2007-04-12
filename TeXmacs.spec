Summary: A wysiwyg mathematical text editor
Name: TeXmacs
Version: 1.0.6.9
Release: %mkrel 1
Source0: ftp://ftp.texmacs.org/pub/TeXmacs/targz/%{name}-%{version}-src.tar.bz2
Url: http://www.texmacs.org
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
Source10:%{name}.16.png.bz2
Source11:%{name}.32.png.bz2
Source12:%{name}.48.png.bz2

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

%build
%configure2_5x --disable-optimize
%make TEXMACS

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install
export GUILE_DATA_PATH=`guile-config info pkgdatadir`
export GUILE_LOAD_PATH=`find $GUILE_DATA_PATH -type d | grep ice-9`

# fix calls for R >= 2.0.0
(cd $RPM_BUILD_ROOT%{_datadir}/TeXmacs/plugins/r/r/
R CMD build --force TeXmacs
R CMD INSTALL -l `pwd` TeXmacs_0.1.tar.gz)

# icons
install -d $RPM_BUILD_ROOT%{_miconsdir}
install -d $RPM_BUILD_ROOT%{_liconsdir}
bzcat %{SOURCE10} > $RPM_BUILD_ROOT%{_miconsdir}/%{name}.png
bzcat %{SOURCE11} > $RPM_BUILD_ROOT%{_iconsdir}/%{name}.png
bzcat %{SOURCE12} > $RPM_BUILD_ROOT%{_liconsdir}/%{name}.png

mkdir -p  $RPM_BUILD_ROOT%_datadir/applications
cp  $RPM_BUILD_ROOT%_datadir/TeXmacs/misc/mime/texmacs.desktop $RPM_BUILD_ROOT%_datadir/applications/

# menu
install -d $RPM_BUILD_ROOT%{_menudir}
cat << EOF > $RPM_BUILD_ROOT%{_menudir}/%{name}
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
  --dir $RPM_BUILD_ROOT%{_datadir}/applications $RPM_BUILD_ROOT%{_datadir}/applications/*


%clean
rm -rf $RPM_BUILD_ROOT

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


