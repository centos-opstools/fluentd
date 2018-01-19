# Generated from fluentd-0.12.2.gem by gem2rpm -*- rpm-spec -*-
%global gem_name fluentd

Name: %{gem_name}
Version: 0.12.41
Release: 2%{?dist}
Summary: Fluentd event collector
Group: Development/Languages
License: ASL 2.0
URL: http://fluentd.org/
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
Source1: fluentd.service

BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: ruby >= 1.9.3
BuildRequires: rubygem(test-unit)
BuildRequires: rubygem(rr)
BuildRequires: rubygem(test-unit-rr)
BuildRequires: rubygem(yajl-ruby)
BuildRequires: rubygem(msgpack)
BuildRequires: rubygem(sigdump)
BuildRequires: rubygem(cool.io)
BuildRequires: rubygem(tzinfo)
BuildRequires: rubygem(http_parser.rb)
BuildRequires: rubygem(thread_safe)
BuildRequires: systemd

Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd
Requires: rubygem(cool.io) >= 1.2.2
Requires: rubygem(cool.io) < 2.0.0
Requires: rubygem(http_parser.rb) >= 0.5.1
Requires: rubygem(http_parser.rb) < 0.7.0
Requires: rubygem(json) >= 1.4.3
Requires: rubygem(msgpack) >= 0.5.11
Requires: rubygem(msgpack) < 2
Requires: rubygem(sigdump) >= 0.2.2
Requires: rubygem(sigdump) < 0.3
Requires: rubygem(string-scrub) >= 0.0.3
Requires: rubygem(string-scrub) <= 0.0.5
Requires: rubygem(thread_safe)
Requires: rubygem(tzinfo) >= 1.0.0
Requires: rubygem(yajl-ruby) >= 1.0
Requires: rubygem(yajl-ruby) < 2
Requires: hostname
BuildArch: noarch
Provides: rubygem(%{gem_name}) = %{version}

%description
Fluentd is an open source data collector designed to scale and simplify log
management. It can collect, process and ship many kinds of data in near
real-time.


%package doc
Summary: Documentation for %{name}
Group: Documentation
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{name}.

%prep
gem unpack %{SOURCE0}

%setup -q -D -T -n  %{gem_name}-%{version}

gem spec %{SOURCE0} -l --ruby > %{gem_name}.gemspec
%gemspec_remove_dep -g tzinfo-data ">= 1.0.0"

%build
# Create the gem as gem install only works on a gem file
gem build %{gem_name}.gemspec

# %%gem_install compiles any C extensions and installs the gem into ./%%gem_dir
# by default, so that we can move it into the buildroot in %%install
%gem_install

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/


mkdir -p %{buildroot}%{_bindir}
cp -pa .%{_bindir}/* \
        %{buildroot}%{_bindir}/

find %{buildroot}%{gem_instdir}/bin -type f | xargs chmod a+x

mkdir -p %{buildroot}%{_sysconfdir}/%{gem_name}
mv %{buildroot}%{gem_instdir}/fluent.conf %{buildroot}%{_sysconfdir}/%{gem_name}

mkdir -p %{buildroot}%{_unitdir}
install -p -m 0644 %{SOURCE1} %{buildroot}%{_unitdir}/

rm -f %{buildroot}%{gem_instdir}/{.gitignore,.travis.yml}

# Run the test suite
%check
pushd .%{gem_instdir}
# Tests disabled on EL due to outdated test-unit
%if 0%{?fedora} > 0
testrb2 -Ilib:test test/**/test_*.rb
%endif
popd

%files
%defattr(-, root, root, -)
%dir %{gem_instdir}
%attr(755, root, root) %{_bindir}/fluent-cat
%attr(755, root, root) %{_bindir}/fluent-debug
%attr(755, root, root) %{_bindir}/fluent-gem
%attr(755, root, root) %{_bindir}/fluentd
%{gem_instdir}/bin
%{gem_libdir}
%attr(644, root, root) /%{_unitdir}/fluentd.service
%exclude %{gem_cache}
%{gem_spec}
%dir %{_sysconfdir}/%{gem_name}
%config(noreplace) %{_sysconfdir}/%{gem_name}/fluent.conf
%license %{gem_instdir}/COPYING


%files doc
%doc %{gem_docdir}
%{gem_instdir}/Rakefile
%{gem_instdir}/test/
%{gem_instdir}/%{gem_name}.gemspec
%{gem_instdir}/example/*
%doc %{gem_instdir}/AUTHORS
%doc %{gem_instdir}/CONTRIBUTING.md
%doc %{gem_instdir}/CHANGELOG.md
%doc %{gem_instdir}/Gemfile
%doc %{gem_instdir}/README.md

%pre
# NOTE(mmagr): httpd logs have 0700 mode now for root, so we need to run
#              fluentd service as root to be able to collect all logs
#getent group fluentd >/dev/null || groupadd -r fluentd
#getent passwd fluentd >/dev/null || \
#    useradd -r -g fluentd -d /etc/fluentd -s /sbin/nologin \
#    -c "Fluentd data collection agent" fluentd
#exit 0

%post
%systemd_post fluentd.service

%preun
%systemd_preun fluentd.service

%postun
%systemd_postun fluentd.service

%changelog
* Fri Jan 19 2018 Sandro Bonazzola <sbonazzo@redhat.com> - 0.12.41-2
- Remove tzinfo-data also from gem spec.

* Thu Dec 07 2017 Richard Megginson <rmeggins@redhat.com> - 0.12.41-1
- version 0.12.41

* Wed Aug 23 2017 Rich Megginson <rmeggins@redhat.com> - 0.12.39-2
- remove utf-8 patch to allow file buffering to work

* Tue Aug 15 2017 Rich Megginson <rmeggins@redhat.com> - 0.12.39-1
- version 0.12.39

* Fri Jul 21 2017 Sandro Bonazzola <sbonazzo@redhat.com> - 0.12.37-2
- Restored runtime dependency hostname lost during rebase on 0.12.37

* Fri Jul 21 2017 Rich Megginson <rmeggins@redhat.com> - 0.12.37-1
- version 0.12.37

* Fri Jul 14 2017 Juan Badia Payno <jbadiapa@redhat.com> - 0.12.31-5
- Add runtime dependency hostname,so this package can be used by
other distros than CentOS

* Thu Jun 15 2017 Sandro Bonazzola <sbonazzo@redhat.com> - 0.12.31-4
- Add missing requirement on rubygem-thread_safe

* Mon Apr 10 2017 Lon Hohberger <lon@redhat.com> - 0.12.31-3
- Fix %defattr line to match expected UID/GIDs (rhbz#1426169)

* Tue Feb 28 2017 Martin Mágr <mmagr@redhat.com> - 0.12.31-2
- Run fluentd service as root to be able to gather httpd logs (rhbz#1426169)

* Mon Jan  9 2017 Rich Megginson <rmeggins@redhat.com> - 0.12.31-1
- update to 0.12.31

* Mon Dec 12 2016 Rich Megginson <rmeggins@redhat.com> - 0.12.30-1
- update to 0.12.30

* Tue Sep 20 2016 Rich Megginson <rmeggins@redhat.com> - 0.12.29-1
- update to 0.12.29

* Thu Aug 04 2016 Rich Megginson <rmeggins@redhat.com> - 0.12.20-2
- Rebuild to add provides for rubygem(fluentd)

* Fri Feb 05 2016 Troy Dawson <tdawson@redhat.com> - 0.12.20-1
- Updated to latest release

* Fri Oct 16 2015 Troy Dawson <tdawson@redhat.com> - 0.12.16-1
- Updated to latest release
- Added patch to fix UTF error

* Wed Sep 09 2015 Troy Dawson <tdawson@redhat.com> - 0.12.15-2
- Add a provides to spec file

* Mon Aug 31 2015 Troy Dawson <tdawson@redhat.com> - 0.12.15-1
- Updated to latest release

* Wed Jul 29 2015 Graeme Gillies <ggillies@redhat.com> - 0.12.5-3
- Corrected ownership on executable files in /usr/bin

* Tue Jun 02 2015 Graeme Gillies <ggillies@redhat.com> - 0.12.5-2
- Fixed file ownership permissions for package

* Mon Feb 16 2015 Graeme Gillies <ggillies@redhat.com> - 0.12.5-1
- Upgraded to 0.12.5

* Mon Jan 05 2015 Graeme Gillies <ggillies@redhat.com> - 0.12.2-1
- Initial package
