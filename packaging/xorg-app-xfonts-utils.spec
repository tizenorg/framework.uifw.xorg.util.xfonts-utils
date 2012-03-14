Summary: X Window System font utility programs
Name: xorg-app-xfonts-utils
Version: 7.5
Release: 4
License: MIT/X11
Group: User Interface/X
URL: http://www.x.org
Source: xfonts-utils-%{version}.tar.gz

BuildRequires: pkgconfig(xorg-macros)
BuildRequires: pkgconfig(xfont)
BuildRequires: pkgconfig(x11)
BuildRequires: pkgconfig(xproto)
BuildRequires: pkgconfig(freetype2)
BuildRequires: pkgconfig(fontenc)

%define DEF_SUBDIRS bdftopcf mkfontdir mkfontscale font-util fonttosfnt

Provides: %{DEF_SUBDIRS}

%description
xfonts-utils provides a set of utility programs shipped with the X Window
System that are needed for font management.
.
The programs in this package include:
 - bdftopcf, which converts BDF fonts to PCF fonts;
 - bdftruncate and ucs2any, tools to generate fonts with various encodings
   from ISO 10646-encoded fonts
 - mkfontdir, a program to generate fonts.dir files;
 - mkfontscale, a program to generate fonts.scale files;
 - fonttosfnt, a program to wrap bitmap fonts in a sfnt (TrueType) wrapper.

%prep
%setup -q -n xfonts-utils-%{version}

%build
# Build all apps
{
    for app in %{DEF_SUBDIRS}; do
        pushd $app
        %configure \
            --with-mapdir=%{_prefix}/share/fonts/X11/util \
            CPPFLAGS="-D_GNU_SOURCE"
	make
        popd
    done
}

%install
# Install all apps
{
   for app in %{DEF_SUBDIRS} ; do
      pushd $app
      make install DESTDIR=$RPM_BUILD_ROOT
      popd
   done
}

%docs_package

%files
%{_bindir}/*
%{_libdir}/pkgconfig/fontutil.pc
%{_prefix}/share/aclocal/fontutil.m4
%{_prefix}/share/fonts/X11/util/*

