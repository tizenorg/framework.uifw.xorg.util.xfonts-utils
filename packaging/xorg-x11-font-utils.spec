%define pkgname font-utils

Summary: X.Org X11 font utilities
Name: xorg-x11-%{pkgname}
# IMPORTANT: If package ever gets renamed to something else, remove the Epoch line!
Epoch: 1
Version: 7.5
Release: 8
License: MIT
Group: User Interface/X
URL: http://www.x.org

Source: %{name}-%{version}.tar.gz

#Source0: ftp://ftp.x.org/pub/individual/app/bdftopcf-1.0.3.tar.bz2
#Source1: ftp://ftp.x.org/pub/individual/app/fonttosfnt-1.0.3.tar.bz2
#Source2: ftp://ftp.x.org/pub/individual/app/mkfontdir-1.0.6.tar.bz2
#Source3: ftp://ftp.x.org/pub/individual/app/mkfontscale-%{mkfontscale}.tar.bz2
#Source4: ftp://ftp.x.org/pub/individual/font/font-util-1.3.0.tar.bz2
# helper script used in %post for xorg-x11-fonts
#Source5: xorg-x11-fonts-update-dirs

#Patch2: mkfontscale-examine-all-encodings.patch

BuildRequires: pkgconfig(xfont) pkgconfig(x11)
#BuildRequires: libfontenc-devel >= 0.99.2-2
BuildRequires: freetype-devel
BuildRequires: zlib-devel
BuildRequires: autoconf

Provides: %{pkgname}
Provides: bdftopcf, fonttosfnt, mkfontdir, mkfontscale, ucs2any

# bdftruncate isn't a perl script anymore (repackaged in f18)
Provides: bdftruncate = %{version}-%{release}
Obsoletes: bdftruncate < %{version}-%{release}

%description
X.Org X11 font utilities required for font installation, conversion,
and generation.

%prep
%setup -q
#%setup -q -c %{name}-%{version} -a1 -a2 -a3 -a4
#oldpwd=$(pwd)
#cd mkfontscale-%{mkfontscale}
#%patch2 -p1 -b .all-encodings
#cd ${oldpwd}

%build
# Build all apps
{
   for app in bdftopcf fonttosfnt mkfontdir mkfontscale font-util ; do
      oldpwd=$(pwd)
      cd $app*
      # this --with-mapdir should be redundant?
      %configure \
      	--with-mapdir=%{_datadir}/X11/fonts/util %{_prefix}/share/fonts/X11/util \
      	CPPFLAGS="${CPPCFLAGS} -D_GNU_SOURCE"
      #%configure --with-mapdir=%{_datadir}/X11/fonts/util 
      make %{?jobs:-j%jobs}
      cd ${oldpwd}
   done
}

%install
rm -rf $RPM_BUILD_ROOT
# Install all apps
{
    for app in bdftopcf fonttosfnt mkfontdir mkfontscale font-util; do
		oldpwd=$(pwd)
		cd $app*
		make install DESTDIR=$RPM_BUILD_ROOT
		cd ${oldpwd}
	done
	#for i in */README ; do
	#	[ -s $i ] && cp $i README-$(echo $i | sed 's/-[0-9].*//')
	#done
	#for i in */COPYING ; do
	#	grep -q stub $i || cp $i COPYING-$(echo $i | sed 's/-[0-9].*//')
	#done
}

#install -m 744 %{SOURCE5} ${RPM_BUILD_ROOT}%{_bindir}/xorg-x11-fonts-update-dirs
#sed -i "s:@DATADIR@:%{_datadir}:" ${RPM_BUILD_ROOT}%{_bindir}/xorg-x11-fonts-update-dirs

%remove_docs

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
#%doc README-* COPYING-bdftopcf COPYING-[c-z]*
%{_bindir}/*
#%{_bindir}/bdftopcf
#%{_bindir}/bdftruncate
#%{_bindir}/fonttosfnt
#%{_bindir}/mkfontdir
#%{_bindir}/mkfontscale
#%{_bindir}/ucs2any
#%{_bindir}/xorg-x11-fonts-update-dirs
%dir %{_datadir}/X11/fonts
%dir %{_datadir}/X11/fonts/util
%{_datadir}/X11/fonts/util/map-*
%{_datadir}/aclocal/fontutil.m4
%{_libdir}/pkgconfig/fontutil.pc
#%{_mandir}/man1/bdftopcf.1*
#%{_mandir}/man1/bdftruncate.1*
#%{_mandir}/man1/fonttosfnt.1*
#%{_mandir}/man1/mkfontdir.1*
#%{_mandir}/man1/mkfontscale.1*
#%{_mandir}/man1/ucs2any.1*
