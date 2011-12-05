Summary:        Read a preset list of files into memory
Name:           readahead
Version:        1.5.6
Release:        1%{?dist}
Epoch:          1
Group:          System Environment/Base
License:        GPLv2+
Source0:        readahead-%{version}.tar.bz2

URL: 		https://fedorahosted.org/readahead/
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires(post): /sbin/chkconfig, /sbin/service
Requires(preun):  /sbin/chkconfig, /sbin/service
Requires:       procps /bin/gawk upstart /usr/bin/ionice
BuildRequires:  e2fsprogs-devel
BuildRequires:  audit-libs-devel
BuildRequires:  libblkid-devel
BuildRequires:  autoconf automake

%define pkgvardatadir %{_localstatedir}/lib/%{name}

%description
readahead reads the contents of a list of files into memory,
which causes them to be read from cache when they are actually
needed. Its goal is to speed up the boot process.

%prep
%setup -q

%build
%configure --sbindir=/sbin
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=${RPM_BUILD_ROOT}
mkdir -p ${RPM_BUILD_ROOT}%{pkgvardatadir}
%find_lang %{name}

%clean
rm -rf ${RPM_BUILD_ROOT}

%preun
if [ "$1" = "0" ] ; then
 # for updating older packages with service files
 /sbin/service readahead_later stop >/dev/null 2>&1
 /sbin/chkconfig --del readahead_later  >/dev/null 2>&1
 /sbin/service readahead_early stop >/dev/null 2>&1
 /sbin/chkconfig --del readahead_early  >/dev/null 2>&1
 :
fi

%post
%{_sysconfdir}/cron.monthly/readahead-monthly.cron
:

%files -f %{name}.lang
%defattr(-,root,root,- )
%doc COPYING README lists/README.lists NEWS
%{_sysconfdir}/cron.daily/readahead.cron
%{_sysconfdir}/cron.monthly/readahead-monthly.cron
%dir %{pkgvardatadir}
%{_sysconfdir}/init/readahead-collector.conf
%{_sysconfdir}/init/readahead-disable-services.conf
%{_sysconfdir}/init/readahead.conf
%config(noreplace) %{_sysconfdir}/sysconfig/readahead
%config(noreplace) %{_sysconfdir}/readahead.conf
/sbin/readahead
/sbin/readahead-collector

%changelog
* Wed Mar 24 2010 Harald Hoyer <harald@redhat.com> 1.5.6-1
- version 1.5.6
- various bugfixes by Raphael Geissert 
  (#527498, #527505, #527508, #527509, #528781, #528785)
- Related: rhbz#543948

* Wed Mar 24 2010 Harald Hoyer <harald@redhat.com> 1.5.5-1
- version 1.5.5
- exit readahead-collector correctly, if audit is not enabled
- make delay of services configurable
- make minimum memory requirement configurable
- log to /dev/kmsg in upstart scripts
- upstart scripts updated for upstart 0.6 (#546077, #575114)
- Resolves: rhbz#575119, rhbz#561486

* Fri Jan 15 2010 Harald Hoyer <harald@redhat.com> 1.5.4-3
- update for upstart-0.6
- Related: rhbz#543948

* Wed Jan 13 2010 Harald Hoyer <harald@redhat.com> 1.5.4-2
- rebuild for libaudit soname bump
- Related: rhbz#543948

* Tue Oct 13 2009 Harald Hoyer <harald@redhat.com> 1.5.4-1
- cleanup readahead-collector audit rules
- translation update

* Tue Oct 06 2009 Harald Hoyer <harald@redhat.com> 1.5.3-1
- fix readhead for new libaudit (bug #523400)
- don't leak file descriptors (bug #525893)
- also collect openat() calls
- ignore files > 10MB

* Tue Sep 15 2009 Harald Hoyer <harald@redhat.com> 1.5.1-2
- remove console owner from collector (gets killed by SIGHUP)

* Mon Sep 14 2009 Harald Hoyer <harald@redhat.com> 1.5.1-1
- readahead-1.5.1
- add syslog() to collector
- translation update
- let upstart set console owner for collector

* Fri Aug 21 2009 Tomas Mraz <tmraz@redhat.com> - 1:1.5.0-2
- rebuilt with new audit

* Thu Aug 13 2009 Harald Hoyer <harald@redhat.com> 1.5.0-1
- version 1.5.0
- see http://git.fedorahosted.org/git/readahead?p=readahead;a=blob;f=NEWS;hb=HEAD

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.4.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jul 15 2009 Harald Hoyer <harald@redhat.com> 1.4.9-2
- add libblkid-devel BuildRequirement

* Thu Mar 05 2009 Harald Hoyer <harald@redhat.com> 1.4.9-1
- version 1.4.9
- readahead-collector is now triggered by rpm database changes

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.4.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Feb 20 2009 Harald Hoyer <harald@redhat.com> 1.4.8-1
- version 1.4.8
- /etc/readahead.d moved to /var/lib/readahead

* Thu Oct 16 2008 Harald Hoyer <harald@redhat.com> 1.4.7-1
- fixed error message in cron script (rhbz#460795)

* Mon Sep 08 2008 Harald Hoyer <harald@redhat.com> 1.4.6-1
- fixed the selinux=off case

* Sat Sep 06 2008 Harald Hoyer <harald@redhat.com> 1.4.5-3
- marked /etc/sysconfig/readahead as a config file
- removed noreplace from /etc/readahead.conf
- fixed /etc/readahead.conf for /sbin/readahead

* Wed Sep 03 2008 Harald Hoyer <harald@redhat.com> 1.4.5-2
- fixed compiling agaings audit-libs-devel-1.4.5

* Mon Sep 01 2008 Harald Hoyer <harald@redhat.com> 1.4.5-2
- moved readahead to /sbin (bug #460715)

* Thu Aug 28 2008 Harald Hoyer <harald@redhat.com> 1.4.5-1
- new adaptive readahead version

* Tue Jul 22 2008 Karel Zak <kzak@redhat.com> 1:1.4.4-2
- fix #456027 - readahead should use O_NOATIME while opening the files

* Tue Jun 24 2008 Karel Zak <kzak@redhat.com> 1:1.4.4-1
- upgrade to 1.4.4

* Mon Mar  3 2008 Karel Zak <kzak@redhat.com> 1:1.4.2-5
- fix #434277 - readahead failed massrebuild attempt for GCC 4.3

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1:1.4.2-4
- Autorebuild for GCC 4.3

* Wed Oct 17 2007 Karel Zak <kzak@redhat.com> 1:1.4.2-3
- update default lists
- fix #327041 - readahead --sort generates file with "(null)"
- fix #326891 - readahead-collector doesn't collect binaries

* Wed Oct  3 2007 Karel Zak <kzak@redhat.com> 1:1.4.2-2
- cleanup specfile (based on fedora merge review - #226360)

* Mon Oct  1 2007 Karel Zak <kzak@redhat.com> 1:1.4.2-1
- upgrade to 1.4.2 (includes bug fixes only)
   - auparse requires as a record separator (#253226)
   - fix e-mail setting in Makevars  (#308271)
   - remove debug message (#237302)
   - improve init scripts  (#247044, #243685)
   - add pl.po

* Fri Apr 20 2007 Jeremy Katz <katzj@redhat.com> - 1:1.4.1-2
- don't be so noisy (#237302)

* Thu Apr 12 2007 Karel Zak <kzak@redhat.com> - 1:1.4.1-1
- upgrade to new upstream version 1.4.1
- generate new lists

* Tue Feb 27 2007 Karel Zak <kzak@redhat.com> - 1:1.4-1
- upgrade to new upstream version
- cleanup spec file

* Fri Feb  2 2007 Karel Zak <kzak@redhat.com> - 1:1.3-7
- rebuild (update file lists)

* Tue Jan 16 2007 Karel Zak <kzak@redhat.com> - 1:1.3-6
- update file lists (215503)

* Sun Oct 01 2006 Jesse Keating <jkeating@redhat.com> - 1:1.3-5
- rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Fri Sep 22 2006 Karel Zak <kzak@redhat.com> 1:1.3-4
- fix #207631 - clean up package build system and use tarball instead
                separated source files

* Fri Sep 22 2006 Karel Zak <kzak@redhat.com> 1:1.3-3
- fix #207631 - readahead has no debuginfo

* Mon Jul 20 2006 Karel Zak <kzak@redhat.com> 1:1.3-1
- move lists of files to /etc/readahead.d
- add readahead-check to docs
- ignore duplicate files

* Wed Jul 19 2006 Jesse Keating <jkeating@redhat.com> - 1:1.2-3
- fix release for upgrade path (by removing cvs generated release)

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1:1.2-1.26
- rebuild

* Thu Mar 16 2006 Karel Zak <kzak@redhat.com>
- update versions in *.in lists

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1:1.2-1.24.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1:1.2-1.23.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Jan 13 2006 Karel Zak <kzak@redhat.com>
- check & cleanup list of files by readahead-gen script

* Wed Dec 21 2005 Karel Zak <kzak@redhat.com>
- removed double slashes in the directory names
- removed or fixed the rest of X11R6 directories

* Mon Dec 19 2005 Karel Zak <kzak@redhat.com>
- sync versioned gcc, firefox, openoffice.org, evolution dirs with FC5

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Thu Aug  4 2005 Dave Jones <davej@redhat.com>
- Integrated changes from Ville Skytta (#164872)
  - Fix inverted logic in readahead_early also.
  - readahead_early looks useful in more runlevels than just 5.
  - Sync versioned gcc, firefox and openoffice.org dirs with FC4 updates.

* Tue Aug  2 2005 Dave Jones <davej@redhat.com>
- Fix inverted free memory test in startup script. (#164872)

* Wed May 18 2005 Bill Nottingham <notting@redhat.com>
- new readahead.c from Ziga Mahkovec <ziga.mahkovec@klika.si>
  - optimizes read access for more throughput
- regenerate file lists (#128444)
- fix lack of newlines (#146744)
- fix lists so that they are architecture-neutral
- move check for > 384MB into the init scripts, not the %%post

* Tue Mar  1 2005 Dave Jones <davej@redhat.com>
- Rebuild for gcc4

* Thu Feb 10 2005 Dave Jones <davej@redhat.com>
- Remove non-existent files from file lists.

* Fri Jan 14 2005 Dave Jones <davej@redhat.com>
- Don't do readahead if we have less than 256MB of memory.

* Sat Dec 18 2004 Dave Jones <davej@redhat.com>
- Initial packaging, based upon kernel-utils.

