#
# Conditional builds
%bcond_with	ft218	# compile with freetype >= 2.1.8
#
Summary:	Mozilla Thunderbird - email client
Summary(pl):	Mozilla Thunderbird - klient poczty
Name:		mozilla-thunderbird
Version:	0.8
Release:	0.3
License:	MPL/LGPL
Group:		Applications/Networking
Source0:	http://ftp.mozilla.org/pub/mozilla.org/thunderbird/releases/%{version}/thunderbird-source-%{version}.tar.bz2
# Source0-md5:	76de1827d66ac482cfc4dd32e7b1e257
Source1:	%{name}.desktop
Patch0:		%{name}-alpha-gcc3.patch
Patch1:		%{name}-nss.patch
Patch2:		%{name}-lib_path.patch
Patch3:		%{name}-freetype.patch
URL:		http://www.mozilla.org/projects/thunderbird/
BuildRequires:	automake
%if %{with ft218}
BuildRequires:	freetype-devel >= 1:2.1.8
%else
BuildRequires:	freetype-devel >= 2.1.3
BuildRequires:	freetype-devel < 1:2.1.8
BuildConflicts:	freetype-devel = 2.1.8
%endif
BuildRequires:	gtk+2-devel >= 2.0.0
BuildRequires:	libIDL-devel >= 0.8.0
BuildRequires:	libjpeg-devel >= 6b
BuildRequires:	libpng-devel >= 1.2.0
BuildRequires:	libstdc++-devel
BuildRequires:	nss-devel >= 3.8
BuildRequires:	pango-devel >= 1:1.1.0
%if %{with ft218}
Requires:	freetype >= 1:2.1.3
%else
Requires:	freetype >= 2.1.3
Requires:	freetype < 1:2.1.8
Conflicts:	freetype = 2.1.8
%endif
Requires:	nss >= 3.8
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define	_noautoreqdep		libgkgfx.so libgtkembedmoz.so libgtkxtbin.so libjsj.so libmozjs.so libxpcom.so libxpcom_compat.so libnspr4.so
%define	_noautoprovfiles	libnspr4.so libplc4.so libplds4.so

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
%{?with_ft218:%patch3 -p1}

%build
export CFLAGS="%{rpmcflags}"
export CXXFLAGS="%{rpmcflags}"
export MOZ_THUNDERBIRD=1
export BUILD_OFFICIAL="1"
export MOZILLA_OFFICIAL="1"

cp -f %{_datadir}/automake/config.* build/autoconf
cp -f %{_datadir}/automake/config.* nsprpub/build/autoconf
cp -f %{_datadir}/automake/config.* directory/c-sdk/config/autoconf
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
	--without-system-nspr \
	--with-system-png \
	--with-system-zlib \
	--with-pthreads \
	--enable-single-profile \
	--disable-profilesharing

%{__make}

%install

rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_libdir},%{_pixmapsdir},%{_desktopdir}}

%{__make} -C xpinstall/packager \
	MOZ_PKG_APPNAME="mozilla-thunderbird" \
	MOZILLA_BIN="\$(DIST)/bin/thunderbird-bin" \
	EXCLUDE_NSPR_LIBS=1

%define		_thunderbirddir		%{_libdir}/%{name}
ln -sf %{_thunderbirddir}/thunderbird $RPM_BUILD_ROOT%{_bindir}/mozilla-thunderbird

tar -xvz -C $RPM_BUILD_ROOT%{_libdir} -f dist/mozilla-thunderbird-*-linux-gnu.tar.gz

install mail/app/default.xpm $RPM_BUILD_ROOT%{_pixmapsdir}/mozilla-thunderbird.xpm
install %{SOURCE1} $RPM_BUILD_ROOT%{_desktopdir}/mozilla-thunderbird.desktop

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/mozilla-thunderbird
%dir %{_thunderbirddir}
%{_thunderbirddir}/res
%dir %{_thunderbirddir}/components
%attr(755,root,root) %{_thunderbirddir}/components/*.so
%{_thunderbirddir}/components/*.js
%{_thunderbirddir}/components/*.xpt
%{_thunderbirddir}/defaults
%{_thunderbirddir}/greprefs
%{_thunderbirddir}/icons
%{_thunderbirddir}/plugins
%attr(755,root,root) %{_thunderbirddir}/*.so
%attr(755,root,root) %{_thunderbirddir}/*.sh
%attr(755,root,root) %{_thunderbirddir}/*-bin
%attr(755,root,root) %{_thunderbirddir}/mozilla-xremote-client
%attr(755,root,root) %{_thunderbirddir}/reg*
%attr(755,root,root) %{_thunderbirddir}/thunderbird
%attr(755,root,root) %{_thunderbirddir}/thunderbird-config
%attr(755,root,root) %{_thunderbirddir}/TestGtkEmbed
%ifarch %{ix86}
%attr(755,root,root) %{_thunderbirddir}/elf-dynstr-gc
%endif
%{_thunderbirddir}/*.txt
%{_thunderbirddir}/x*
%dir %{_thunderbirddir}/chrome
%{_thunderbirddir}/chrome/US.jar
%{_thunderbirddir}/chrome/classic.jar
%{_thunderbirddir}/chrome/comm.jar
%{_thunderbirddir}/chrome/en-US.jar
%{_thunderbirddir}/chrome/en-unix.jar
%{_thunderbirddir}/chrome/icons
%{_thunderbirddir}/chrome/messenger.jar
%{_thunderbirddir}/chrome/modern.jar
%{_thunderbirddir}/chrome/offline.jar
%{_thunderbirddir}/chrome/pipnss.jar
%{_thunderbirddir}/chrome/pippki.jar
%{_thunderbirddir}/chrome/toolkit.jar
%{_thunderbirddir}/chrome/*.txt
%{_pixmapsdir}/*
%{_desktopdir}/*
