Summary:	Mozilla Thunderbird - email client
Summary(pl):	Mozilla Thunderbird - klient poczty
Name:		mozilla-thunderbird
Version:	0.5
Release:	0.2
License:	MPL/LGPL
Group:		Applications/Networking
#source file published on mozilla site is broken.
#Source0:	http://ftp.mozilla.org/pub/mozilla.org/thunderbird/releases/%{version}/thunderbird-source-%{version}.tar.bz2
Source0:	http://www.lukasz.mach.com.pl/thsnap/thunderbird-cvs-%{version}.tar.bz2
# Source0-md5:	d809bba990fc8048ef5fbd331cf7391c
Source1:	%{name}.desktop
Patch0:		%{name}-alpha-gcc3.patch
#Patch1:	%{name}-xpcom-aliasing.patch
URL:		http://www.mozilla.org/projects/thunderbird/
BuildRequires:	gtk+2-devel >= 2.0.0
BuildRequires:	libIDL-devel >= 0.8.0
BuildRequires:	libjpeg-devel >= 6b
BuildRequires:	libpng-devel >= 1.2.0
BuildRequires:	libstdc++-devel
BuildRequires:	pango-devel >= 1.1.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Mozilla Thunderbird is an open-source,fast and portable email client.

%description -l pl
Mozilla Thunderbird jest open sourcowym, szybkim i przeno¶nym klientem
poczty.

%prep
%setup -q -n mozilla
%patch0 -p1
#%patch1 -p1

%build
export BUILD_OFFICIAL=1
export MOZ_THUNDERBIRD=1

cat  << EOF >.mozconfig
mk_add_options MOZ_THUNDERBIRD="1"
ac_add_options --with-system-jpeg
ac_add_options --with-system-zlib
ac_add_options --with-system-png
ac_add_options --with-pthreads
ac_add_options --disable-tests
ac_add_options --disable-debug
ac_add_options --disable-xprint
ac_add_options --disable-ldap
ac_add_options --disable-jsd
ac_add_options --disable-gtktest
ac_add_options --disable-freetypetest
ac_add_options --disable-installer
ac_add_options --enable-optimize="%{optflags}"
ac_add_options --enable-crypto
ac_add_options --enable-strip
ac_add_options --enable-strip-libs
ac_add_options --enable-reorder
ac_add_options --enable-mathml
ac_add_options --enable-xinerama
ac_add_options --enable-extensions="pref,cookie,wallet"
ac_add_options --enable-freetype2
ac_add_options --enable-xft
ac_add_options --enable-default-toolkit="gtk2"
ac_add_options --prefix=%{_prefix}
EOF

%{__make} -f client.mk MOZILLA_VERSION="thunderbird" build

%install

rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_libdir},%{_pixmapsdir},%{_desktopdir}}

%{__make} -C xpinstall/packager \
	MOZ_PKG_APPNAME="mozilla-thunderbird" \
	MOZILLA_BIN="\$(DIST)/bin/thunderbird-bin"

ln -sf %{_libdir}/mozilla-thunderbird/thunderbird $RPM_BUILD_ROOT%{_bindir}/mozilla-thunderbird

tar -xvz -C $RPM_BUILD_ROOT%{_libdir} -f dist/mozilla-thunderbird-*-linux-gnu.tar.gz

install mail/app/default.xpm $RPM_BUILD_ROOT%{_pixmapsdir}/mozilla-thunderbird.xpm
install %{SOURCE1} $RPM_BUILD_ROOT%{_desktopdir}/mozilla-thunderbird.desktop

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/mozilla-thunderbird
%dir %{_libdir}/mozilla-thunderbird
%{_libdir}/mozilla-thunderbird/res
%{_libdir}/mozilla-thunderbird/chrome
%{_libdir}/mozilla-thunderbird/components
%{_libdir}/mozilla-thunderbird/plugins
%{_libdir}/mozilla-thunderbird/icons
%{_libdir}/mozilla-thunderbird/defaults
%{_libdir}/mozilla-thunderbird/ipc
%attr(755,root,root) %{_libdir}/mozilla-thunderbird/*.so
%attr(755,root,root) %{_libdir}/mozilla-thunderbird/*.sh
%attr(755,root,root) %{_libdir}/mozilla-thunderbird/*-bin
%attr(755,root,root) %{_libdir}/mozilla-thunderbird/mangle
%attr(755,root,root) %{_libdir}/mozilla-thunderbird/mozipcd
%attr(755,root,root) %{_libdir}/mozilla-thunderbird/mozilla-xremote-client
%attr(755,root,root) %{_libdir}/mozilla-thunderbird/reg*
%attr(755,root,root) %{_libdir}/mozilla-thunderbird/shlibsign
%attr(755,root,root) %{_libdir}/mozilla-thunderbird/thunderbird
%attr(755,root,root) %{_libdir}/mozilla-thunderbird/TestGtkEmbed
%{_libdir}/mozilla-thunderbird/*.chk
%{_libdir}/mozilla-thunderbird/*.txt
%{_libdir}/mozilla-thunderbird/elf-dynstr-gc
%{_libdir}/mozilla-thunderbird/x*
%{_pixmapsdir}/*
%{_desktopdir}/*
