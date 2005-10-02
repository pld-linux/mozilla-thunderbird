#
# Conditional builds
%bcond_without	ft218	    # compile with freetype < 2.1.8
%bcond_without	enigmail    # don't build enigmail - GPG/PGP support
%bcond_without	spellcheck  # build without spellcheck function
#
Summary:	Mozilla Thunderbird - email client
Summary(pl):	Mozilla Thunderbird - klient poczty
Name:		mozilla-thunderbird
Version:	1.0.7
Release:	1
License:	MPL/LGPL
Group:		Applications/Networking
Source0:	http://ftp.mozilla.org/pub/mozilla.org/thunderbird/releases/%{version}/source/thunderbird-%{version}-source.tar.bz2
# Source0-md5:	e6388feb0ffcd189af779f165c124b4d
Source1:	%{name}.desktop
Source2:	%{name}.sh
%if %{with enigmail}
Source3:	http://www.mozilla-enigmail.org/downloads/src/ipc-1.1.3.tar.gz
# Source3-md5:	64ba4c6e3b52568468c4f6680ec7e679
Source4:	http://www.mozilla-enigmail.org/downloads/src/enigmail-0.93.0.tar.gz
# Source4-md5:	cb7126705924cb7f0de205b4ff4e28b4
%endif
Patch0:		%{name}-alpha-gcc3.patch
Patch1:		%{name}-gfx.patch
Patch2:		%{name}-nss.patch
Patch3:		%{name}-lib_path.patch
Patch4:		%{name}-freetype.patch
Patch5:		%{name}-blockimage.patch
Patch6:		%{name}-gcc-bugs.patch
URL:		http://www.mozilla.org/projects/thunderbird/
BuildRequires:	automake
%if %{with ft218}
BuildRequires:	freetype-devel >= 1:2.1.8
%else
BuildRequires:	freetype-devel >= 2.1.3
BuildRequires:	freetype-devel < 1:2.1.8
BuildConflicts:	freetype-devel = 2.1.8
%endif
BuildRequires:	gtk+2-devel >= 1:2.0.0
BuildRequires:	libIDL-devel >= 0.8.0
BuildRequires:	libjpeg-devel >= 6b
BuildRequires:	libpng-devel >= 1.2.0
BuildRequires:	libstdc++-devel
BuildRequires:	nspr-devel >= 1:4.6-0.20041030.1
BuildRequires:	nss-devel >= 3.8
BuildRequires:	pango-devel >= 1:1.1.0
BuildRequires:	sed >= 4.0
%if %{with enigmail}
BuildRequires:	/bin/ex
BuildRequires:	/bin/csh
%endif
%if %{with ft218}
Requires:	freetype >= 1:2.1.3
%else
Requires:	freetype >= 2.1.3
Requires:	freetype < 1:2.1.8
Conflicts:	freetype = 2.1.8
%endif
Requires:	nspr >= 1:4.6-0.20041030.1
Requires:	nss >= 3.8
%if %{with spellcheck}
Provides:	mozilla-thunderbird-spellcheck
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_thunderbirddir		%{_libdir}/%{name}
# mozilla and thunderbird provide their own versions
%define	_noautoreqdep		libgkgfx.so libgtkembedmoz.so libgtkxtbin.so libjsj.so libmozjs.so libxpcom.so libxpcom_compat.so
%define	_noautoprovfiles	libplc4.so libplds4.so

%description
Mozilla Thunderbird is an open-source,fast and portable email client.

%description -l pl
Mozilla Thunderbird jest open sourcowym, szybkim i przeno¶nym klientem
poczty.

%package dictionary-en-US
Summary:	English (US) dictionary for spellchecking
Summary(pl):	Angielski (USA) s³ownik do sprawdzania pisowni
Group:		Applications/Dictionaries
Requires:	mozilla-thunderbird-spellcheck

%description dictionary-en-US
This package contains English (US) myspell-compatible dictionary used
for spellcheck function of mozilla-thunderbird. An alternative for
this can be the OpenOffice's dictionary.

%description dictionary-en-US -l pl
Ten pakiet zawiera angielski (USA) s³ownik kompatybilny z myspellem,
u¿ywany przez funkcjê sprawdzania pisowni mozilli-thunderbird.
Alternatyw± dla niego mo¿e byæ s³ownik OpenOffice'a.

%prep
%setup -q -n mozilla
%if %{with enigmail}
cd extensions
tar xvfz %{SOURCE3}
tar xvfz %{SOURCE4}
cd ..
%endif

%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%{?with_ft218:%patch4 -p1}
%patch5 -p1
%patch6 -p1

# %if %{with enigmail}
# mv ipc extensions/ipc
# mv enigmail extensions/enigmail
# %endif

%build
export CFLAGS="%{rpmcflags} `%{_bindir}/pkg-config mozilla-nspr --cflags-only-I`"
export CXXFLAGS="%{rpmcflags} `%{_bindir}/pkg-config mozilla-nspr --cflags-only-I`"
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
	--enable-extensions="pref,cookie,wallet%{?with_spellcheck:,spellcheck}" \
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
	--with-pthreads \
	--enable-single-profile \
	--disable-profilesharing

%{__make}

%if %{with enigmail}
   cd extensions/ipc
   ./makemake -r
   %{__make}
   cd ../enigmail
   ./makemake -r
   %{__make}
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_libdir},%{_pixmapsdir},%{_desktopdir}}

%{__make} -C xpinstall/packager \
	MOZ_PKG_APPNAME="mozilla-thunderbird" \
	MOZILLA_BIN="\$(DIST)/bin/thunderbird-bin" \
	EXCLUDE_NSPR_LIBS=1

install %{SOURCE2} $RPM_BUILD_ROOT%{_bindir}/mozilla-thunderbird
%{__sed} -i 's@%{_prefix}/lib/@%{_libdir}/@g' $RPM_BUILD_ROOT%{_bindir}/mozilla-thunderbird

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
%if %{with spellcheck}
%dir %{_thunderbirddir}/components/myspell
%endif
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
%{_thunderbirddir}/chrome/classic.jar
%{_thunderbirddir}/chrome/comm.jar
%{_thunderbirddir}/chrome/en-US.jar
%{_thunderbirddir}/chrome/help.jar
%{_thunderbirddir}/chrome/icons
%{_thunderbirddir}/chrome/messenger.jar
%{_thunderbirddir}/chrome/modern.jar
%{_thunderbirddir}/chrome/newsblog.jar
%{_thunderbirddir}/chrome/offline.jar
%{_thunderbirddir}/chrome/pipnss.jar
%{_thunderbirddir}/chrome/pippki.jar
%{_thunderbirddir}/chrome/toolkit.jar
%{_thunderbirddir}/chrome/*.txt
%{_thunderbirddir}/chrome/embed-sample.jar
%if %{with enigmail}
%{_thunderbirddir}/chrome/enigmail-en-US.jar
%{_thunderbirddir}/chrome/enigmail-skin-tbird.jar
%{_thunderbirddir}/chrome/enigmail-skin.jar
%{_thunderbirddir}/chrome/enigmail.jar
%{_thunderbirddir}/chrome/enigmime.jar
%endif
%dir %{_thunderbirddir}/init.d
%{_thunderbirddir}/init.d/README
%{_pixmapsdir}/*
%{_desktopdir}/*

%if %{with spellcheck}
%files dictionary-en-US
%defattr(644,root,root,755)
%{_thunderbirddir}/components/myspell/en-US.dic
%{_thunderbirddir}/components/myspell/en-US.aff
%endif
