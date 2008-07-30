Summary:	WYSIWYG mathematical text editor
Name:		TeXmacs
Version:	1.0.6.12
Release:	%mkrel 4
License:	GPLv2+
Group:		Editors
URL:		http://www.texmacs.org
Source0:	ftp://ftp.texmacs.org/pub/TeXmacs/targz/%{name}-%{version}-src.tar.gz
Source10:	%{name}.16.png
Source11:	%{name}.32.png
Source12:	%{name}.48.png

Requires:	tetex
Requires:	guile
Requires:	R-base
Requires:	axiom
Requires:	maxima >= 5.9.1
Obsoletes:	TeXmacs-fonts
Provides:	TeXmacs-fonts
BuildRequires:	X11-devel
BuildRequires:	libguile-devel
BuildRequires:	desktop-file-utils
Requires(post):	desktop-file-utils
Requires(postun): desktop-file-utils
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

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

Converters exist for TeX/LaTeX and they are under development for
Html/Mathml/Xml.

%prep
%setup -q -n %{name}-%{version}-src

%build
%configure2_5x \
	--enable-optimize="%{optflags}"
	
%make

%install
rm -rf %{buildroot}
%makeinstall_std
export GUILE_DATA_PATH=`guile-config info pkgdatadir`
export GUILE_LOAD_PATH=`find $GUILE_DATA_PATH -type d | grep ice-9`

# fix calls for R >= 2.0.0
(cd %{buildroot}%{_datadir}/TeXmacs/plugins/r/r/
R CMD build --force TeXmacs
R CMD INSTALL -l `pwd` TeXmacs_0.1.tar.gz)

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

%clean
rm -rf %{buildroot}

%if %mdkversion < 200900
%post
%{update_menus}
%{update_desktop_database}
%update_icon_cache hicolor
%endif

%if %mdkversion < 200900
%postun
%{clean_menus}
%{clean_desktop_database}
%clean_icon_cache hicolor
%endif

%files
%defattr(-,root,root)
%{_bindir}/*
%{_includedir}/TeXmacs.h
%{_mandir}/*/*
%{_libexecdir}/TeXmacs
%{_datadir}/TeXmacs
%{_iconsdir}/hicolor/*/apps/%{name}.png
%{_datadir}/applications/*
