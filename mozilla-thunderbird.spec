Summary:	Mozilla Thunderbird - email client
Summary(pl):	Mozilla Thunderbird - klient poczty
Name:		mozilla-thunderbird
Version:	0.7.2
Release:	0.1
License:	MPL/LGPL
Group:		Applications/Networking
Source0:	http://ftp.mozilla.org/pub/mozilla.org/thunderbird/releases/%{version}/thunderbird-%{version}-source.tar.bz2
# Source0-md5:	6e3d516b6d553dde4663c179132f1c2a
Source1:	%{name}.desktop
Patch0:		%{name}-alpha-gcc3.patch
Patch1:		%{name}-nspr.patch
Patch2:		%{name}-nss.patch
URL:		http://www.mozilla.org/projects/thunderbird/
BuildRequires:	automake
BuildRequires:	gtk+2-devel >= 2.0.0
BuildRequires:	libIDL-devel >= 0.8.0
BuildRequires:	libjpeg-devel >= 6b
BuildRequires:	libpng-devel >= 1.2.0
BuildRequires:	libstdc++-devel
BuildRequires:	nspr-devel >= 1:4.5.0
BuildRequires:	nss-devel >= 3.8
BuildRequires:	pango-devel >= 1.1.0
Requires:	nspr >= 1:4.5.0
Requires:	nss >= 3.8
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_noautoreqdep	libgkgfx.so libgtkembedmoz.so libgtkxtbin.so libjsj.so libmozjs.so libxpcom.so libxpcom_compat.so

%description
Mozilla Thunderbird is an open-source,fast and portable email client.

%description -l pl
Mozilla Thunderbird jest open sourcowym, szybkim i przeno¶nym klientem
poczty.

%prep
%setup -q -n mozilla
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
export CFLAGS="%{rpmcflags}"
export CXXFLAGS="%{rpmcflags}"
export BUILD_OFFICIAL=1
export MOZ_THUNDERBIRD=1

cp -f /usr/share/automake/config.* build/autoconf
cp -f /usr/share/automake/config.* nsprpub/build/autoconf
cp -f /usr/share/automake/config.* directory/c-sdk/config/autoconf
%configure2_13 \
%if %{?debug:1}0
	--enable-debug \
	--enable-debug-modules \
%else
	--disable-debug \
	--disable-debug-modules \
%endif
%if %{with tests}
	--enable-tests \
%else
	--disable-tests \
%endif
	--disable-ldap \
	--disable-installer \
	--disable-jsd \
	--disable-xprint \
	--enable-crypto \
	--enable-default-toolkit="gtk2" \
	--enable-extensions="pref,cookie,wallet" \
	--enable-freetype2 \
	--enable-mathml \
	--enable-optimize="%{rpmcflags}" \
	--enable-reorder \
	--enable-strip \
	--enable-strip-libs \
	--enable-xft \
	--enable-xinerama \
	--with-system-jpeg \
	--with-system-nspr \
	--with-system-png \
	--with-system-zlib \
	--with-pthreads

%{__make}

%install

rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_libdir},%{_pixmapsdir},%{_desktopdir}}

%{__make} -C xpinstall/packager \
	MOZ_PKG_APPNAME="mozilla-thunderbird" \
	MOZILLA_BIN="\$(DIST)/bin/thunderbird-bin" \
	EXCLUDE_NSPR_LIBS=1

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
%dir %{_libdir}/mozilla-thunderbird/components
%attr(755,root,root) %{_libdir}/mozilla-thunderbird/components/*.so
%{_libdir}/mozilla-thunderbird/components/*.js
%{_libdir}/mozilla-thunderbird/components/*.xpt
%{_libdir}/mozilla-thunderbird/defaults
%{_libdir}/mozilla-thunderbird/greprefs
%{_libdir}/mozilla-thunderbird/icons
%{_libdir}/mozilla-thunderbird/plugins
%attr(755,root,root) %{_libdir}/mozilla-thunderbird/*.so
%attr(755,root,root) %{_libdir}/mozilla-thunderbird/*.sh
%attr(755,root,root) %{_libdir}/mozilla-thunderbird/*-bin
%attr(755,root,root) %{_libdir}/mozilla-thunderbird/mozilla-xremote-client
%attr(755,root,root) %{_libdir}/mozilla-thunderbird/reg*
%attr(755,root,root) %{_libdir}/mozilla-thunderbird/thunderbird
%attr(755,root,root) %{_libdir}/mozilla-thunderbird/thunderbird-config
%attr(755,root,root) %{_libdir}/mozilla-thunderbird/TestGtkEmbed
%ifarch %{ix86}
%attr(755,root,root) %{_libdir}/mozilla-thunderbird/elf-dynstr-gc
%endif
%{_libdir}/mozilla-thunderbird/*.txt
%{_libdir}/mozilla-thunderbird/x*
%dir %{_libdir}/mozilla-thunderbird/chrome
%{_libdir}/mozilla-thunderbird/chrome/US.jar
%{_libdir}/mozilla-thunderbird/chrome/classic.jar
%{_libdir}/mozilla-thunderbird/chrome/comm.jar
%{_libdir}/mozilla-thunderbird/chrome/en-US-mail.jar
%{_libdir}/mozilla-thunderbird/chrome/en-US.jar
%{_libdir}/mozilla-thunderbird/chrome/en-unix.jar
%{_libdir}/mozilla-thunderbird/chrome/icons
%{_libdir}/mozilla-thunderbird/chrome/mail.jar
%{_libdir}/mozilla-thunderbird/chrome/messenger.jar
%{_libdir}/mozilla-thunderbird/chrome/modern.jar
%{_libdir}/mozilla-thunderbird/chrome/offline.jar
%{_libdir}/mozilla-thunderbird/chrome/pipnss.jar
%{_libdir}/mozilla-thunderbird/chrome/pippki.jar
%{_libdir}/mozilla-thunderbird/chrome/qute.jar
%{_libdir}/mozilla-thunderbird/chrome/toolkit.jar
%{_libdir}/mozilla-thunderbird/chrome/*.txt
%{_pixmapsdir}/*
%{_desktopdir}/*
