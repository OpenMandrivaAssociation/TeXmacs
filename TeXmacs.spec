%define _disable_lto 1

Summary:	WYSIWYW scientifical text editor
Name:		TeXmacs
Version:	1.99.2
Release:	1
License:	GPLv2+
Group:		Editors
URL:		http://www.texmacs.org
Source0:	http://www.texmacs.org/Download/ftp/tmftp/source/%{name}-%{version}-src.tar.gz
Source10:	%{name}.16.png
Source11:	%{name}.32.png
Source12:	%{name}.48.png
Requires:	tetex
Requires:	guile
Requires:	R-base
Requires:	maxima >= 5.9.1
Obsoletes:	TeXmacs-fonts
Provides:	TeXmacs-fonts
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(freetype2)
BuildRequires:	pkgconfig(guile-2.0)
BuildRequires:	desktop-file-utils
BuildRequires:	R-base
BuildRequires:	pkgconfig(xext)
BuildRequires:	qt4-devel

%description
GNU TeXmacs is a free wysiwyw (what you see is what you want) editing platform
with special features for scientists. The software aims to provide a unified
and user friendly framework for editing structured documents with different
types of content (text, graphics, mathematics, interactive content, etc.).
The rendering engine uses high-quality typesetting algorithms so as to produce
professionally looking documents, which can either be printed out or presented
from a laptop.

The software includes a text editor with support for mathematical formulas,
a small technical picture editor and a tool for making presentations from
a laptop. Moreover, TeXmacs can be used as an interface for many external
systems for computer algebra, numerical analysis, statistics, etc. New
presentation styles can be written by the user and new features can be added
to the editor using the Scheme extension language. A native spreadsheet
and tools for collaborative authoring are planned for later. 

%prep
%setup -q -n %{name}-%{version}-src
find . -name '*.cpp' -exec chmod 644 {} \;
find . -name '*.hpp' -exec chmod 644 {} \;

%build
%configure \
	--enable-optimize="%{optflags}" \
	--enable-guile2=yes
	
%make

%install
%makeinstall_std
export GUILE_DATA_PATH=`guile-config info pkgdatadir`
export GUILE_LOAD_PATH=`find $GUILE_DATA_PATH -type d | grep ice-9`

# icons
install -d %{buildroot}%{_iconsdir}/hicolor/{16x16,32x32,48x48}/apps
cp -a %{SOURCE10} %{buildroot}%{_iconsdir}/hicolor/16x16/apps/%{name}.png
cp -a %{SOURCE10} %{buildroot}%{_iconsdir}/hicolor/32x32/apps/%{name}.png
cp -a %{SOURCE10} %{buildroot}%{_iconsdir}/hicolor/48x48/apps/%{name}.png

mkdir -p  %{buildroot}%{_datadir}/applications
cp -a %{buildroot}%{_datadir}/TeXmacs/misc/mime/texmacs.desktop %{buildroot}%{_datadir}/applications/

sed -i -e 's/^Icon=%{name}.xpm$/Icon=%{name}/g' %{buildroot}%{_datadir}/applications/*

desktop-file-install \
  --remove-category="Application" \
  --remove-key="Path" \
  --add-category="Office;WordProcessor;Math;" \
  --dir %{buildroot}%{_datadir}/applications %{buildroot}%{_datadir}/applications/*

chmod 755 %{buildroot}%{_datadir}/TeXmacs/langs/encoding/*.awk

%files
%{_bindir}/*
%{_includedir}/TeXmacs.h
%{_mandir}/*/*
%{_libexecdir}/TeXmacs
%{_datadir}/TeXmacs
%{_iconsdir}/hicolor/*/apps/%{name}.png
%{_datadir}/applications/*
%{_datadir}/application-registry/texmacs.applications
%{_iconsdir}/gnome/scalable/*/*.svg
%{_datadir}/mime-info/texmacs.*
%{_datadir}/mime/packages/texmacs.xml
%{_datadir}/pixmaps/TeXmacs.xpm
