Summary:	Desktop print icon
Name:		eggcups
Version:	0.20
Release:	1
License:	GPL
Group:		X11/Applications
Source0:	http://ftp.gnome.org/pub/GNOME/sources/eggcups/0.20/%{name}-%{version}.tar.bz2
# Source0-md5:	deaf598120961765bfef61ecd4101ed3
Patch0:		%{name}-dbus.patch
BuildRequires:	cups-devel
BuildRequires:	dbus-devel >= 0.60
BuildRequires:	desktop-file-utils
BuildRequires:	gnome-keyring-devel
BuildRequires:	hal-devel
BuildRequires:	intltool
BuildRequires:	libglade2-devel
BuildRequires:	libgnomecups-devel >= 0.1.12
BuildRequires:	libgnomeui-devel
BuildRequires:	xorg-lib-libXScrnSaver-devel
Requires:	dbus
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Desktop-printing contains eggcups, a program for user print job
notification and control.

%prep
%setup -q
%patch0 -p1

%build
%{configure} \
	--with-session-cupsd=no
# fix dbus paths
find . -type f -print0 \( -name '*.c' -o -name '*.h' -o -name '*.conf' \) | xargs -0 perl -pi -e 's,org/freedesktop/,com/redhat/,g;s,org.freedesktop.,com.redhat.,g'
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
export GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%define schemas eggcups.schemas

%post
%gconf_schema_install %{schemas}
%update_icon_cache hicolor

%preun
%gconf_schema_uninstall %{schemas}

%postun
%update_icon_cache hicolor

%files -f %{name}.lang
%defattr(644, root, root, 755)
%attr(755,root,root) %{_bindir}/eggcups
%attr(755,root,root) %{_bindir}/gnome-default-printer
%{_datadir}/eggcups
%{_desktopdir}/gnome-default-printer.desktop
%{_sysconfdir}/dbus-1/system.d/*.conf
%{_sysconfdir}/gconf/*
