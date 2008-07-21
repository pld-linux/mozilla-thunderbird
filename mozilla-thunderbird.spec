# TODO:
# - CHECK all features of enigmail
# - separate spec for enigmail
#
# Conditional builds
%bcond_without	enigmail	# don't build enigmail - GPG/PGP support
%bcond_without	gnomeui		# disable gnomeui support
%bcond_without	gnomevfs	# disable GNOME comp. (gconf+libgnome+gnomevfs) and gnomevfs ext.
%bcond_without	gnome		# disable all GNOME components (gnome+gnomeui+gnomevfs)
%bcond_without	ldap		# disable e-mail address lookups in LDAP directories
#
%if %{without gnome}
%undefine	with_gnomeui
%undefine	with_gnomevfs
%endif
%define		enigmail_ver		0.95.6
%define		thunderbird_ver		2.0.0.14

Summary:	Thunderbird Community Edition - email client
Summary(pl.UTF-8):	Thunderbird Community Edition - klient poczty
Name:		mozilla-thunderbird
Version:	%{thunderbird_ver}
Release:	2
License:	MPL 1.1 or GPL v2+ or LGPL v2.1+
Group:		Applications/Networking
Source0:	http://releases.mozilla.org/pub/mozilla.org/thunderbird/releases/%{version}/source/thunderbird-%{version}-source.tar.bz2
# Source0-md5:	e304510d08f7e226bbfff8e7e549232f
Source1:	http://www.mozilla-enigmail.org/download/source/enigmail-%{enigmail_ver}.tar.gz
# Source1-md5:	cfbe6ff77f80a349b396829757ad952a
Source2:	%{name}.desktop
Source3:	%{name}.sh
Source4:	%{name}-enigmail.manifest
Source5:	%{name}.png
Patch1:		%{name}-lib_path.patch
Patch2:		%{name}-enigmail-shared.patch
Patch3:		%{name}-gcc.patch
Patch4:		%{name}-fonts.patch
Patch5:		%{name}-install.patch
Patch6:		%{name}-myspell.patch
Patch7:		%{name}-regionNames.patch
URL:		http://www.mozilla.org/projects/thunderbird/
%{?with_gnomevfs:BuildRequires:	GConf2-devel >= 1.2.1}
BuildRequires:	automake
BuildRequires:	freetype-devel >= 1:2.1.8
%{?with_gnomevfs:BuildRequires:	gnome-vfs2-devel >= 2.0}
BuildRequires:	gtk+2-devel >= 1:2.0.0
BuildRequires:	libIDL-devel >= 0.8.0
%{?with_gnomevfs:BuildRequires:	libgnome-devel >= 2.0}
%{?with_gnomeui:BuildRequires:	libgnomeui-devel >= 2.2.0}
BuildRequires:	libjpeg-devel >= 6b
BuildRequires:	libpng-devel >= 1.2.0
BuildRequires:	libstdc++-devel
BuildRequires:	myspell-devel
BuildRequires:	nspr-devel >= 1:4.6.1
BuildRequires:	nss-devel >= 1:3.11.3
BuildRequires:	pango-devel >= 1:1.1.0
BuildRequires:	sed >= 4.0
BuildRequires:	xorg-lib-libXext-devel
BuildRequires:	xorg-lib-libXft-devel >= 2.1
BuildRequires:	xorg-lib-libXinerama-devel
BuildRequires:	xorg-lib-libXp-devel
BuildRequires:	xorg-lib-libXt-devel
Requires:	myspell-common
Requires:	nspr >= 1:4.6.1
Requires:	nss >= 1:3.11.3
Obsoletes:	mozilla-thunderbird-dictionary-en-US
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# don't satisfy other packages (don't use %{name} here)
%define		_noautoprovfiles	%{_libdir}/mozilla-thunderbird
# and as we don't provide them, don't require either
%define		_noautoreq		libgfxpsshar.so libgkgfx.so libgtkembedmoz.so libgtkxtbin.so libldap50.so libmozjs.so libprldap50.so libssldap50.so libxpcom.so libxpcom_compat.so libxpcom_core.so

%description
Thunderbird Community Edition is an open-source,fast and portable
email client.

%description -l pl.UTF-8
Thunderbird Community Edition jest open sourcowym, szybkim i
przenośnym klientem poczty.

%package addon-enigmail
Summary:	Extension for the authentication and encryption features provided by GnuPG
Summary(pl.UTF-8):	Rozszerzenie do uwierzytelniania i szyfrowania zapewnianego przez GnuPG
License:	MPL/LGPL
Group:		Applications/Networking
URL:		http://enigmail.mozdev.org/
Requires:	%{name} = %{thunderbird_ver}-%{release}

%description addon-enigmail
Enigmail is an extension to the mail client of Mozilla Thunderbird
which allows users to access the authentication and encryption
features provided by GnuPG.

Main Features:
- Encrypt/sign mail when sending, decrypt/authenticate received mail
- Support for inline-PGP (RFC 2440) and PGP/MIME (RFC 3156)
- Per-Account based encryption and signing defaults
- Per-Recipient rules for automated key selection, and
  enabling/disabling encryption and signing
- OpenPGP key management interface

%description addon-enigmail -l pl.UTF-8
Enigmail to rozszerzenie klienta pocztowego Mozilla Thunderbird
pozwalające użytkownikom na dostęp do uwierzytelniania i szyfrowania
zapewnianego przez GnuPG.

Główne możliwości:
- szyfrowanie/podpisywanie poczty przy wysyłaniu,
  odszyfrowywanie/uwierzytelnianie poczty odebranej
- obsługa inline-PGP (RFC 2440) i PGP/MIME (RFC 3156)
- ustawienia domyślne szyfrowania i podpisywania dla każdego konta
- reguły automatycznego wyboru kluczy i włączenia szyfrowania oraz
  podpisywania dla każdego adresata
- interfejs do zarządzania kluczami OpenPGP

%prep
%setup -q -c
cd mozilla
%{?with_enigmail:tar xvfz %{SOURCE1} -C mailnews/extensions}
%patch1 -p1
%{?with_enigmail:%patch2 -p1}
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1

:> config/gcc_hidden.h

%build
cd mozilla
export CFLAGS="%{rpmcflags} `%{_bindir}/pkg-config mozilla-nspr --cflags-only-I`"
export CXXFLAGS="%{rpmcflags} `%{_bindir}/pkg-config mozilla-nspr --cflags-only-I`"

cp -f %{_datadir}/automake/config.* build/autoconf
cp -f %{_datadir}/automake/config.* nsprpub/build/autoconf
cp -f %{_datadir}/automake/config.* directory/c-sdk/config/autoconf

cat << 'EOF' > .mozconfig
. $topsrcdir/mail/config/mozconfig

ac_add_options --prefix=%{_prefix}
ac_add_options --exec-prefix=%{_exec_prefix}
ac_add_options --bindir=%{_bindir}
ac_add_options --sbindir=%{_sbindir}
ac_add_options --sysconfdir=%{_sysconfdir}
ac_add_options --datadir=%{_datadir}
ac_add_options --includedir=%{_includedir}
ac_add_options --libdir=%{_libdir}
ac_add_options --libexecdir=%{_libexecdir}
ac_add_options --localstatedir=%{_localstatedir}
ac_add_options --sharedstatedir=%{_sharedstatedir}
ac_add_options --mandir=%{_mandir}
ac_add_options --infodir=%{_infodir}
%if %{?debug:1}0
ac_add_options --enable-debug
ac_add_options --enable-debug-modules
%else
ac_add_options --disable-debug
ac_add_options --disable-debug-modules
%endif
%if %{with tests}
ac_add_options --enable-tests
%else
ac_add_options --disable-tests
%endif
%if %{with gnomeui}
ac_add_options --enable-gnomeui
%else
ac_add_options --disable-gnomeui
%endif
%if %{with gnomevfs}
ac_add_options --enable-gnomevfs
%else
ac_add_options --disable-gnomevfs
%endif
%if %{with ldap}
ac_add_options --enable-ldap
%else
ac_add_options --disable-ldap
%endif
ac_add_options --disable-installer
ac_add_options --disable-jsd
ac_add_options --disable-xprint
ac_add_options --enable-canvas
ac_add_options --enable-crypto
ac_add_options --enable-default-toolkit="gtk2"
ac_add_options --enable-extensions="pref,cookie,wallet,spellcheck"
ac_add_options --enable-mathml
ac_add_options --enable-optimize="%{rpmcflags}"
ac_add_options --enable-pango
ac_add_options --enable-reorder
ac_add_options --disable-strip
ac_add_options --disable-strip-libs
ac_add_options --enable-system-cairo
ac_add_options --enable-system-myspell
ac_add_options --enable-svg
ac_add_options --enable-xft
ac_add_options --enable-xinerama
ac_add_options --with-system-jpeg
ac_add_options --with-system-nspr
ac_add_options --with-system-nss
ac_add_options --with-system-png
ac_add_options --with-system-zlib
ac_add_options --with-pthreads
ac_add_options --enable-single-profile
ac_add_options --disable-profilesharing
ac_add_options --with-default-mozilla-five-home=%{_libdir}/%{name}
EOF

%{__make} -j1 -f client.mk build_all \
	CC="%{__cc}" \
	CXX="%{__cxx}"

%if %{with enigmail}
	cd mailnews/extensions/enigmail
	./makemake -r
	%{__make}
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_libdir},%{_pixmapsdir},%{_desktopdir}} \
	$RPM_BUILD_ROOT%{_datadir}/%{name}

cd mozilla
%{__make} -C xpinstall/packager stage-package \
	DESTDIR=$RPM_BUILD_ROOT \
	MOZ_PKG_APPDIR=%{_libdir}/%{name} \
	PKG_SKIP_STRIP=1

# move arch independant ones to datadir
mv $RPM_BUILD_ROOT%{_libdir}/%{name}/chrome $RPM_BUILD_ROOT%{_datadir}/%{name}/chrome
mv $RPM_BUILD_ROOT%{_libdir}/%{name}/defaults $RPM_BUILD_ROOT%{_datadir}/%{name}/defaults
mv $RPM_BUILD_ROOT%{_libdir}/%{name}/greprefs $RPM_BUILD_ROOT%{_datadir}/%{name}/greprefs
mv $RPM_BUILD_ROOT%{_libdir}/%{name}/icons $RPM_BUILD_ROOT%{_datadir}/%{name}/icons
mv $RPM_BUILD_ROOT%{_libdir}/%{name}/init.d $RPM_BUILD_ROOT%{_datadir}/%{name}/init.d
mv $RPM_BUILD_ROOT%{_libdir}/%{name}/isp $RPM_BUILD_ROOT%{_datadir}/%{name}/isp
mv $RPM_BUILD_ROOT%{_libdir}/%{name}/res $RPM_BUILD_ROOT%{_datadir}/%{name}/res
ln -s ../../share/%{name}/chrome $RPM_BUILD_ROOT%{_libdir}/%{name}/chrome
ln -s ../../share/%{name}/defaults $RPM_BUILD_ROOT%{_libdir}/%{name}/defaults
ln -s ../../share/%{name}/greprefs $RPM_BUILD_ROOT%{_libdir}/%{name}/greprefs
ln -s ../../share/%{name}/icons $RPM_BUILD_ROOT%{_libdir}/%{name}/icons
ln -s ../../share/%{name}/init.d $RPM_BUILD_ROOT%{_libdir}/%{name}/init.d
ln -s ../../share/%{name}/isp $RPM_BUILD_ROOT%{_libdir}/%{name}/isp
ln -s ../../share/%{name}/res $RPM_BUILD_ROOT%{_libdir}/%{name}/res

rm -rf $RPM_BUILD_ROOT%{_libdir}/%{name}/dictionaries
ln -s %{_datadir}/myspell $RPM_BUILD_ROOT%{_libdir}/%{name}/dictionaries

%{__sed} -e 's,@LIBDIR@,%{_libdir},' %{SOURCE3} > $RPM_BUILD_ROOT%{_bindir}/mozilla-thunderbird
ln -s %{name} $RPM_BUILD_ROOT%{_bindir}/thunderbird

install %{SOURCE2} $RPM_BUILD_ROOT%{_desktopdir}/%{name}.desktop

%if %{with enigmail}
_enig_dir=$RPM_BUILD_ROOT%{_libdir}/%{name}/extensions/\{847b3a00-7ab1-11d4-8f02-006008948af5\}
install -d $_enig_dir/chrome
install -d $_enig_dir/components
install -d $_enig_dir/defaults/preferences
mv -f $RPM_BUILD_ROOT%{_libdir}/%{name}/chrome/enigmail.jar $_enig_dir/chrome
mv -f $RPM_BUILD_ROOT%{_libdir}/%{name}/chrome/enigmail-skin-tbird.jar $_enig_dir/chrome
mv -f $RPM_BUILD_ROOT%{_libdir}/%{name}/components/enig* $_enig_dir/components
mv -f $RPM_BUILD_ROOT%{_libdir}/%{name}/components/libenigmime.so $_enig_dir/components
mv -f $RPM_BUILD_ROOT%{_libdir}/%{name}/components/ipc.xpt $_enig_dir/components
mv -f $RPM_BUILD_ROOT%{_libdir}/%{name}/defaults/preferences/enigmail.js $_enig_dir/defaults/preferences
cp -f mailnews/extensions/enigmail/package/install.rdf $_enig_dir
rm -rf $RPM_BUILD_ROOT%{_libdir}/%{name}/defaults/preferences
rm -f $RPM_BUILD_ROOT%{_libdir}/%{name}/chrome/enigmail-en-US.jar
rm -f $RPM_BUILD_ROOT%{_libdir}/%{name}/chrome/enigmail-skin.jar
rm -f $RPM_BUILD_ROOT%{_libdir}/%{name}/chrome/enigmime.jar
rm -rf $RPM_BUILD_ROOT%{_libdir}/%{name}/components/enig*
rm -f $RPM_BUILD_ROOT%{_libdir}/%{name}/components/libenigmime.so
rm -f $RPM_BUILD_ROOT%{_libdir}/%{name}/components/ipc.xpt
cp -f %{SOURCE4} $_enig_dir/chrome.manifest
cp -f %{SOURCE5} $RPM_BUILD_ROOT%{_pixmapsdir}/mozilla-thunderbird.png
%endif

# win32 stuff
rm -f $RPM_BUILD_ROOT%{_libdir}/%{name}/dirver

%clean
rm -rf $RPM_BUILD_ROOT

%pretrans
if [ -d %{_libdir}/%{name}/dictionaries ] && [ ! -L %{_libdir}/%{name}/dictionaries ]; then
	mv -v %{_libdir}/%{name}/dictionaries{,.rpmsave}
fi
for d in chrome defaults greprefs icons init.d isp res; do
	if [ -d %{_libdir}/%{name}/$d ] && [ ! -L %{_libdir}/%{name}/$d ]; then
		install -d %{_datadir}/%{name}
		mv %{_libdir}/%{name}/$d %{_datadir}/%{name}/$d
	fi
done
exit 0

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/mozilla-thunderbird
%attr(755,root,root) %{_bindir}/thunderbird
%dir %{_libdir}/%{name}
%attr(755,root,root) %{_libdir}/%{name}/libgfxpsshar.so
%attr(755,root,root) %{_libdir}/%{name}/libgkgfx.so
%attr(755,root,root) %{_libdir}/%{name}/libgtkembedmoz.so
%attr(755,root,root) %{_libdir}/%{name}/libgtkxtbin.so
%attr(755,root,root) %{_libdir}/%{name}/libldap50.so
%attr(755,root,root) %{_libdir}/%{name}/libmozjs.so
%attr(755,root,root) %{_libdir}/%{name}/libprldap50.so
%attr(755,root,root) %{_libdir}/%{name}/libxpcom.so
%attr(755,root,root) %{_libdir}/%{name}/libxpcom_compat.so
%attr(755,root,root) %{_libdir}/%{name}/libxpcom_core.so
%attr(755,root,root) %{_libdir}/%{name}/libxpistub.so
%attr(755,root,root) %{_libdir}/%{name}/mozilla-xremote-client
%attr(755,root,root) %{_libdir}/%{name}/regxpcom
%attr(755,root,root) %{_libdir}/%{name}/run-mozilla.sh
%attr(755,root,root) %{_libdir}/%{name}/thunderbird-bin
%attr(755,root,root) %{_libdir}/%{name}/thunderbird
%{_libdir}/%{name}/LICENSE.txt
%{_libdir}/%{name}/README.txt
%attr(755,root,root) %{_libdir}/%{name}/xpcshell
%attr(755,root,root) %{_libdir}/%{name}/xpicleanup
%attr(755,root,root) %{_libdir}/%{name}/xpidl
%attr(755,root,root) %{_libdir}/%{name}/xpt_dump
%attr(755,root,root) %{_libdir}/%{name}/xpt_link
%dir %{_libdir}/%{name}/components
%attr(755,root,root) %{_libdir}/%{name}/components/libaccessibility.so
%attr(755,root,root) %{_libdir}/%{name}/components/libappcomps.so
%attr(755,root,root) %{_libdir}/%{name}/components/libautoconfig.so
%attr(755,root,root) %{_libdir}/%{name}/components/libcaps.so
%attr(755,root,root) %{_libdir}/%{name}/components/libchrome.so
%attr(755,root,root) %{_libdir}/%{name}/components/libcommandlines.so
%attr(755,root,root) %{_libdir}/%{name}/components/libcomposer.so
%attr(755,root,root) %{_libdir}/%{name}/components/libcookie.so
%attr(755,root,root) %{_libdir}/%{name}/components/libdocshell.so
%attr(755,root,root) %{_libdir}/%{name}/components/libeditor.so
%attr(755,root,root) %{_libdir}/%{name}/components/libembedcomponents.so
%attr(755,root,root) %{_libdir}/%{name}/components/libfileview.so
%attr(755,root,root) %{_libdir}/%{name}/components/libgfx_gtk.so
%attr(755,root,root) %{_libdir}/%{name}/components/libgfxps.so
%attr(755,root,root) %{_libdir}/%{name}/components/libgklayout.so
%attr(755,root,root) %{_libdir}/%{name}/components/libhtmlpars.so
%attr(755,root,root) %{_libdir}/%{name}/components/libi18n.so
%attr(755,root,root) %{_libdir}/%{name}/components/libimglib2.so
%attr(755,root,root) %{_libdir}/%{name}/components/libimport.so
%attr(755,root,root) %{_libdir}/%{name}/components/libjar50.so
%attr(755,root,root) %{_libdir}/%{name}/components/libmail.so
%attr(755,root,root) %{_libdir}/%{name}/components/libmailcomps.so
%attr(755,root,root) %{_libdir}/%{name}/components/libmork.so
%attr(755,root,root) %{_libdir}/%{name}/components/libmozfind.so
%attr(755,root,root) %{_libdir}/%{name}/components/libmozldap.so
%attr(755,root,root) %{_libdir}/%{name}/components/libmsgsmime.so
%attr(755,root,root) %{_libdir}/%{name}/components/libmyspell.so
%attr(755,root,root) %{_libdir}/%{name}/components/libnecko.so
%attr(755,root,root) %{_libdir}/%{name}/components/libnecko2.so
%attr(755,root,root) %{_libdir}/%{name}/components/libnsappshell.so
%attr(755,root,root) %{_libdir}/%{name}/components/libpipboot.so
%attr(755,root,root) %{_libdir}/%{name}/components/libpipnss.so
%attr(755,root,root) %{_libdir}/%{name}/components/libpippki.so
%attr(755,root,root) %{_libdir}/%{name}/components/libpref.so
%attr(755,root,root) %{_libdir}/%{name}/components/librdf.so
%attr(755,root,root) %{_libdir}/%{name}/components/libremoteservice.so
%attr(755,root,root) %{_libdir}/%{name}/components/libspellchecker.so
%attr(755,root,root) %{_libdir}/%{name}/components/libstoragecomps.so
%attr(755,root,root) %{_libdir}/%{name}/components/libsystem-pref.so
%attr(755,root,root) %{_libdir}/%{name}/components/libtoolkitcomps.so
%attr(755,root,root) %{_libdir}/%{name}/components/libtxmgr.so
%attr(755,root,root) %{_libdir}/%{name}/components/libuconv.so
%attr(755,root,root) %{_libdir}/%{name}/components/libucvmath.so
%attr(755,root,root) %{_libdir}/%{name}/components/libwallet.so
%attr(755,root,root) %{_libdir}/%{name}/components/libwalletviewers.so
%attr(755,root,root) %{_libdir}/%{name}/components/libwebbrwsr.so
%attr(755,root,root) %{_libdir}/%{name}/components/libwidget_gtk2.so
%attr(755,root,root) %{_libdir}/%{name}/components/libxpcom_compat_c.so
%attr(755,root,root) %{_libdir}/%{name}/components/libxpconnect.so
%attr(755,root,root) %{_libdir}/%{name}/components/libxpinstall.so
%{_libdir}/%{name}/components/accessibility-atk.xpt
%{_libdir}/%{name}/components/accessibility.xpt
%{_libdir}/%{name}/components/addrbook.xpt
%{_libdir}/%{name}/components/alerts.xpt
%{_libdir}/%{name}/components/appshell.xpt
%{_libdir}/%{name}/components/appstartup.xpt
%{_libdir}/%{name}/components/autocomplete.xpt
%{_libdir}/%{name}/components/autoconfig.xpt
%{_libdir}/%{name}/components/bookmarks.xpt
%{_libdir}/%{name}/components/caps.xpt
%{_libdir}/%{name}/components/chardet.xpt
%{_libdir}/%{name}/components/chrome.xpt
%{_libdir}/%{name}/components/commandhandler.xpt
%{_libdir}/%{name}/components/commandlines.xpt
%{_libdir}/%{name}/components/composer.xpt
%{_libdir}/%{name}/components/content_base.xpt
%{_libdir}/%{name}/components/content_html.xpt
%{_libdir}/%{name}/components/content_htmldoc.xpt
%{_libdir}/%{name}/components/content_xmldoc.xpt
%{_libdir}/%{name}/components/content_xslt.xpt
%{_libdir}/%{name}/components/content_xtf.xpt
%{_libdir}/%{name}/components/cookie.xpt
%{_libdir}/%{name}/components/docshell.xpt
%{_libdir}/%{name}/components/dom.xpt
%{_libdir}/%{name}/components/dom_base.xpt
%{_libdir}/%{name}/components/dom_canvas.xpt
%{_libdir}/%{name}/components/dom_core.xpt
%{_libdir}/%{name}/components/dom_css.xpt
%{_libdir}/%{name}/components/dom_events.xpt
%{_libdir}/%{name}/components/dom_html.xpt
%{_libdir}/%{name}/components/dom_loadsave.xpt
%{_libdir}/%{name}/components/dom_range.xpt
%{_libdir}/%{name}/components/dom_sidebar.xpt
%{_libdir}/%{name}/components/dom_storage.xpt
%{_libdir}/%{name}/components/dom_stylesheets.xpt
%{_libdir}/%{name}/components/dom_svg.xpt
%{_libdir}/%{name}/components/dom_traversal.xpt
%{_libdir}/%{name}/components/dom_views.xpt
%{_libdir}/%{name}/components/dom_xbl.xpt
%{_libdir}/%{name}/components/dom_xpath.xpt
%{_libdir}/%{name}/components/dom_xul.xpt
%{_libdir}/%{name}/components/downloads.xpt
%{_libdir}/%{name}/components/editor.xpt
%{_libdir}/%{name}/components/embed_base.xpt
%{_libdir}/%{name}/components/extensions.xpt
%{_libdir}/%{name}/components/exthandler.xpt
%{_libdir}/%{name}/components/fastfind.xpt
%{_libdir}/%{name}/components/feeds.xpt
%{_libdir}/%{name}/components/filepicker.xpt
%{_libdir}/%{name}/components/find.xpt
%{_libdir}/%{name}/components/gfx.xpt
%{_libdir}/%{name}/components/gksvgrenderer.xpt
%{_libdir}/%{name}/components/history.xpt
%{_libdir}/%{name}/components/htmlparser.xpt
%{_libdir}/%{name}/components/imglib2.xpt
%{_libdir}/%{name}/components/impComm4xMail.xpt
%{_libdir}/%{name}/components/import.xpt
%{_libdir}/%{name}/components/inspector.xpt
%{_libdir}/%{name}/components/intl.xpt
%{_libdir}/%{name}/components/jar.xpt
%{_libdir}/%{name}/components/jsconsole.xpt
%{_libdir}/%{name}/components/layout_base.xpt
%{_libdir}/%{name}/components/layout_printing.xpt
%{_libdir}/%{name}/components/layout_xul.xpt
%{_libdir}/%{name}/components/layout_xul_tree.xpt
%{_libdir}/%{name}/components/locale.xpt
%{_libdir}/%{name}/components/lwbrk.xpt
%{_libdir}/%{name}/components/mailnews.xpt
%{_libdir}/%{name}/components/mailprofilemigration.xpt
%{_libdir}/%{name}/components/mailview.xpt
%{_libdir}/%{name}/components/mime.xpt
%{_libdir}/%{name}/components/mimetype.xpt
%{_libdir}/%{name}/components/mozbrwsr.xpt
%{_libdir}/%{name}/components/mozfind.xpt
%{_libdir}/%{name}/components/mozldap.xpt
%{_libdir}/%{name}/components/msgbase.xpt
%{_libdir}/%{name}/components/msgcompose.xpt
%{_libdir}/%{name}/components/msgdb.xpt
%{_libdir}/%{name}/components/msgimap.xpt
%{_libdir}/%{name}/components/msglocal.xpt
%{_libdir}/%{name}/components/msgnews.xpt
%{_libdir}/%{name}/components/msgsearch.xpt
%{_libdir}/%{name}/components/msgsmime.xpt
%{_libdir}/%{name}/components/necko.xpt
%{_libdir}/%{name}/components/necko_about.xpt
%{_libdir}/%{name}/components/necko_cache.xpt
%{_libdir}/%{name}/components/necko_cookie.xpt
%{_libdir}/%{name}/components/necko_data.xpt
%{_libdir}/%{name}/components/necko_dns.xpt
%{_libdir}/%{name}/components/necko_file.xpt
%{_libdir}/%{name}/components/necko_ftp.xpt
%{_libdir}/%{name}/components/necko_http.xpt
%{_libdir}/%{name}/components/necko_res.xpt
%{_libdir}/%{name}/components/necko_socket.xpt
%{_libdir}/%{name}/components/necko_strconv.xpt
%{_libdir}/%{name}/components/necko_viewsource.xpt
%{_libdir}/%{name}/components/pipboot.xpt
%{_libdir}/%{name}/components/pipnss.xpt
%{_libdir}/%{name}/components/pippki.xpt
%{_libdir}/%{name}/components/pref.xpt
%{_libdir}/%{name}/components/prefetch.xpt
%{_libdir}/%{name}/components/profile.xpt
%{_libdir}/%{name}/components/progressDlg.xpt
%{_libdir}/%{name}/components/proxyObjInst.xpt
%{_libdir}/%{name}/components/rdf.xpt
%{_libdir}/%{name}/components/saxparser.xpt
%{_libdir}/%{name}/components/shellservice.xpt
%{_libdir}/%{name}/components/shistory.xpt
%{_libdir}/%{name}/components/signonviewer.xpt
%{_libdir}/%{name}/components/spellchecker.xpt
%{_libdir}/%{name}/components/storage.xpt
%{_libdir}/%{name}/components/toolkitprofile.xpt
%{_libdir}/%{name}/components/toolkitremote.xpt
%{_libdir}/%{name}/components/txmgr.xpt
%{_libdir}/%{name}/components/txtsvc.xpt
%{_libdir}/%{name}/components/uconv.xpt
%{_libdir}/%{name}/components/unicharutil.xpt
%{_libdir}/%{name}/components/update.xpt
%{_libdir}/%{name}/components/uriloader.xpt
%{_libdir}/%{name}/components/url-classifier.xpt
%{_libdir}/%{name}/components/urlformatter.xpt
%{_libdir}/%{name}/components/wallet.xpt
%{_libdir}/%{name}/components/walleteditor.xpt
%{_libdir}/%{name}/components/walletpreview.xpt
%{_libdir}/%{name}/components/webBrowser_core.xpt
%{_libdir}/%{name}/components/webbrowserpersist.xpt
%{_libdir}/%{name}/components/webshell_idls.xpt
%{_libdir}/%{name}/components/widget.xpt
%{_libdir}/%{name}/components/windowds.xpt
%{_libdir}/%{name}/components/windowwatcher.xpt
%{_libdir}/%{name}/components/xpautocomplete.xpt
%{_libdir}/%{name}/components/xpcom_base.xpt
%{_libdir}/%{name}/components/xpcom_components.xpt
%{_libdir}/%{name}/components/xpcom_ds.xpt
%{_libdir}/%{name}/components/xpcom_io.xpt
%{_libdir}/%{name}/components/xpcom_obsolete.xpt
%{_libdir}/%{name}/components/xpcom_threads.xpt
%{_libdir}/%{name}/components/xpcom_xpti.xpt
%{_libdir}/%{name}/components/xpconnect.xpt
%{_libdir}/%{name}/components/xpinstall.xpt
%{_libdir}/%{name}/components/xulapp.xpt
%{_libdir}/%{name}/components/xuldoc.xpt
%{_libdir}/%{name}/components/xultmpl.xpt
%{_libdir}/%{name}/components/*.js
# gnome subpackage?
%if %{with gnomeui}
%attr(755,root,root) %{_libdir}/%{name}/components/libimgicon.so
%{_libdir}/%{name}/components/imgicon.xpt
%endif
%if %{with gnomevfs}
%attr(755,root,root) %{_libdir}/%{name}/components/libmozgnome.so
%{_libdir}/%{name}/components/mozgnome.xpt
%endif

# symlinks
%{_libdir}/%{name}/chrome
%{_libdir}/%{name}/defaults
%{_libdir}/%{name}/dictionaries
%{_libdir}/%{name}/greprefs
%{_libdir}/%{name}/icons
%{_libdir}/%{name}/init.d
%{_libdir}/%{name}/isp
%{_libdir}/%{name}/res

%{_libdir}/%{name}/dependentlibs.list
%{_libdir}/%{name}/updater
%{_libdir}/%{name}/updater.ini
%{_pixmapsdir}/*.png
%{_desktopdir}/*.desktop

%dir %{_datadir}/%{name}
%{_datadir}/%{name}/chrome
%{_datadir}/%{name}/defaults
%{_datadir}/%{name}/greprefs
%{_datadir}/%{name}/icons
%{_datadir}/%{name}/init.d
%{_datadir}/%{name}/isp
%{_datadir}/%{name}/res

%dir %{_libdir}/%{name}/extensions
%{_libdir}/%{name}/extensions/{972ce4c6-7e08-4474-a285-3208198ce6fd}

%if %{with enigmail}
%files addon-enigmail
%defattr(644,root,root,755)
%dir %{_libdir}/%{name}/extensions/{847b3a00-7ab1-11d4-8f02-006008948af5}
%{_libdir}/%{name}/extensions/{847b3a00-7ab1-11d4-8f02-006008948af5}/chrome
%dir %{_libdir}/%{name}/extensions/{847b3a00-7ab1-11d4-8f02-006008948af5}/components
%attr(755,root,root) %{_libdir}/%{name}/extensions/{847b3a00-7ab1-11d4-8f02-006008948af5}/components/libenigmime.so
%{_libdir}/%{name}/extensions/{847b3a00-7ab1-11d4-8f02-006008948af5}/components/enigmail.xpt
%{_libdir}/%{name}/extensions/{847b3a00-7ab1-11d4-8f02-006008948af5}/components/enigmime.xpt
%{_libdir}/%{name}/extensions/{847b3a00-7ab1-11d4-8f02-006008948af5}/components/ipc.xpt
%{_libdir}/%{name}/extensions/{847b3a00-7ab1-11d4-8f02-006008948af5}/components/enigmail.js
%{_libdir}/%{name}/extensions/{847b3a00-7ab1-11d4-8f02-006008948af5}/components/enigprefs-service.js
%{_libdir}/%{name}/extensions/{847b3a00-7ab1-11d4-8f02-006008948af5}/defaults
%{_libdir}/%{name}/extensions/{847b3a00-7ab1-11d4-8f02-006008948af5}/chrome.manifest
%{_libdir}/%{name}/extensions/{847b3a00-7ab1-11d4-8f02-006008948af5}/install.rdf
%endif
