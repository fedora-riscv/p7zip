Summary: Very high compression ratio file archiver
Name: p7zip
Version: 4.20
Release: 1%{?dist}
License: LGPL
Group: Applications/Archiving
URL: http://p7zip.sourceforge.net/
Source: http://dl.sf.net/p7zip/p7zip_%{version}_src.tar.bz2
Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: gcc-c++

%description
p7zip is a port of 7za.exe for Unix. 7-Zip is a file archiver with a very high
compression ratio. The original version can be found at http://www.7-zip.org/.


%package plugins
Summary: Additional plugins for p7zip
Group: Applications/Archiving
Requires: %{name} = %{version}

%description plugins
Additional plugins that can be used with 7z to extend its abilities.
This package contains also a virtual file system for Midnight Commander.


%prep
%setup -n %{name}_%{version}

# Create wrapper scripts, as 7zCon.sfx and Codecs/Formats need to be in the
# same directory as the binaries, and we don't want them in %{_bindir}.
%{__cat} << 'EOF' > 7za.sh
#!/bin/sh
exec %{_libexecdir}/p7zip/7za $@
EOF

%{__cat} << 'EOF' > 7z.sh
#!/bin/sh
exec %{_libexecdir}/p7zip/7z $@
EOF

%build
%ifarch %{ix86} ppc
%{__cp} -f makefile.linux_x86_ppc_alpha makefile.machine
%endif
%ifarch x86_64
%{__cp} -f makefile.linux_amd64 makefile.machine
%endif

# Use optflags
%{__perl} -pi -e 's|^ALLFLAGS=.*|ALLFLAGS=-Wall %{optflags} -fPIC \\|g' \
    makefile.machine
%{__make} %{?_smp_mflags} 7z 7za sfx


%install
%{__rm} -rf %{buildroot}

# Install binaries (7za, 7z, 7zCon.sfx and Codecs/Formats)
%{__mkdir_p} %{buildroot}%{_libexecdir}/p7zip/
%{__cp} -a bin/* %{buildroot}%{_libexecdir}/p7zip/

# Install wrapper scripts
%{__install} -D -m 0755 7z.sh  %{buildroot}%{_bindir}/7z
%{__install} -D -m 0755 7za.sh %{buildroot}%{_bindir}/7za


%clean
%{__rm} -rf %{buildroot}


%files
%defattr(-, root, root, 0755)
%doc ChangeLog README TODO DOCS/*
%{_bindir}/7za
%dir %{_libexecdir}/p7zip/
%{_libexecdir}/p7zip/7za
%{_libexecdir}/p7zip/7zCon.sfx

%files plugins
%defattr(-, root, root, 0755)
%doc contrib/
%{_bindir}/7z
%{_libexecdir}/p7zip/7z
%{_libexecdir}/p7zip/Codecs/
%{_libexecdir}/p7zip/Formats/


%changelog
* Sun Jun 05 2005 Dag Wieers <dag@wieers.com> - 4.20-1
- Updated to release 4.20.

* Sun Apr 10 2005 Dag Wieers <dag@wieers.com> - 4.16-1
- Moved inline scripts to %%prep stage.
- Removed quotes for $@ as it should not be necessary.

* Thu Mar 17 2005 Matthias Saou <http://freshrpms.net/> 4.14.01-1
- Spec file cleanup.
- Fix wrapper scripts : Double quote $@ for filenames with spaces to work.
- Move files from /usr/share to /usr/libexec.
- Various other minor changes.

* Mon Jan 24 2005 Marcin Zaj�czkowski <mszpak@wp.pl>
 - upgraded to 4.14.01

* Sun Jan 16 2005 Marcin Zaj�czkowski <mszpak@wp.pl>
 - upgraded to 4.14

* Mon Dec 20 2004 Marcin Zaj�czkowski <mszpak@wp.pl>
 - added 7za script and moved SFX module to {_datadir}/%{name}/ to allow 7za & 7z
   use it simultaneously
 - returned to plugins in separate package

* Sat Dec 18 2004 Charles Duffy <cduffy@spamcop.net>
 - upgraded to 4.13
 - added 7z (not just 7za) with a shell wrapper
 - added gcc-c++ to the BuildRequires list

* Sat Nov 20 2004 Marcin Zaj�czkowski <mszpak@wp.pl>
 - upgraded to 4.12
 - added virtual file system for Midnight Commander

* Thu Nov 11 2004 Marcin Zaj�czkowski <mszpak@wp.pl>
 - upgraded to 4.10
 - plugins support was dropped out from p7zip

* Sun Aug 29 2004 Marcin Zaj�czkowski <mszpak@wp.pl>
 - initial release

