# Generated from fluentd-0.12.2.gem by gem2rpm -*- rpm-spec -*-
%global gem_name fluentd

%define fluentd_user		fluentd
%define fluentd_group		%{fluentd_user}

%define fluentd_log_dir		%{_localstatedir}/log/fluentd
%define fluentd_buffer_dir	%{_localstatedir}/spool/fluentd/buffer
%define fluentd_pos_dir		%{_localstatedir}/spool/fluentd/pos

Name:    		%{gem_name}
Version: 		0.14.8
Release: 		1%{?dist}
Summary: 		Fluentd event collector
Group:   		Development/Languages
License: 		ASL 2.0
URL:     		http://fluentd.org/
Source0: 		https://rubygems.org/gems/%{gem_name}-%{version}.gem
Source1: 		fluentd.service
Source2: 		fluentd.logrotate

BuildRequires:		systemd
BuildRequires:  	rubygems-devel
BuildRequires:  	ruby >= 1.9.3
BuildRequires:  	rubygem(thread_safe)

## Unit tests requires:
BuildRequires:  	rubygem(test-unit)
BuildRequires:  	rubygem(rr)
BuildRequires:  	rubygem(test-unit-rr)
BuildRequires:		procps-ng
BuildRequires:		hostname
BuildRequires:		rubygem(yajl-ruby) >= 1.0
BuildRequires:		rubygem(serverengine) >= 2.0
BuildRequires:		rubygem(cool.io) >= 1.4.5
BuildRequires:  	rubygem(msgpack) >= 0.7.0
BuildRequires:		rubygem(strptime) >= 0.1.7
BuildRequires:  	rubygem(tzinfo) >= 1.0
BuildRequires:  	rubygem(flexmock) >= 2.0
BuildRequires:  	rubygem(timecop) >= 0.3
BuildRequires:	 	rubygem(http_parser.rb) >= 0.5.1
BuildRequires:		rubygem(simplecov) >= 0.7
BuildRequires:		rubygem(oj) >= 2.14
BuildRequires:		rubygem(parallel_tests) >= 0.15.3

Requires:			logrotate
Requires:			rubygem(msgpack) >= 0.7.0
Requires:			rubygem(yajl-ruby) >= 1.0
Requires:			rubygem(cool.io) >= 1.4.5
Requires:      	 	rubygem(http_parser.rb) >= 0.5.1
Requires:			rubygem(sigdump) >= 0.2.2
Requires:			rubygem(tzinfo) >= 1.0
Requires:			rubygem(tzinfo-data) >= 1.0
Requires:			rubygem(serverengine) >= 2.0
Requires:			rubygem(strptime) >= 0.1.7



Provides:			%{gem_name} = %{version}

Requires(pre):		shadow-utils

Requires(post):		systemd
Requires(preun):	systemd
Requires(postun):	systemd

BuildArch: noarch

%description
Fluentd is an open source data collector designed to scale and simplify log
management. It can collect, process and ship many kinds of data in near
real-time.


%package doc
Summary:        Documentation for %{name}
Group:          Documentation
Requires:       %{name} = %{version}-%{release}
BuildArch:      noarch

%description doc
Documentation for %{name}.

%prep
gem unpack %{SOURCE0}

%setup -q -D -T -n  %{gem_name}-%{version}

gem spec %{SOURCE0} -l --ruby > %{gem_name}.gemspec

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

mkdir -p %{buildroot}%{_sysconfdir}/logrotate.d/fluentd
install -p -m 0644 %{SOURCE2} %{buildroot}%{_sysconfdir}/logrotate.d/fluentd


install -p -d -m 0750 %{buildroot}%{fluentd_log_dir}/
install -p -d -m 0750 %{buildroot}%{fluentd_buffer_dir}/
install -p -d -m 0750 %{buildroot}%{fluentd_pos_dir}/

mkdir -p %{buildroot}%{_unitdir}
install -p -m 0644 %{SOURCE1} %{buildroot}%{_unitdir}/

install -m 0700 -d  %{buildroot}%{_localstatedir}/cache/fluentd

rm -f %{buildroot}%{gem_instdir}/{.gitignore,.travis.yml,appveyor.yml,Vagrantfile,.github/ISSUE_TEMPLATE.md}

# Run the test suite
%check
pushd .%{gem_instdir}
# Tests disabled on EL due to outdated test-unit
%if 0%{?fedora} > 0
ruby -rtest-unit -e 'Test::Unit::AutoRunner.run(true)' -Ilib:test test/**/test_*.rb
%endif
popd

%files
%defattr(-, %{fluentd_user}, %{fluentd_group}, -)
%dir %{gem_instdir}

%attr(755, root, root) %{_bindir}/fluent-cat
%attr(755, root, root) %{_bindir}/fluent-debug
%attr(755, root, root) %{_bindir}/fluent-gem
%attr(755, root, root) %{_bindir}/fluentd
%attr(755, root, root) %{_bindir}/fluent-binlog-reader

%{gem_instdir}/bin
%{gem_libdir}

%attr(644, root, root) /%{_unitdir}/fluentd.service


%exclude %{gem_cache}
%{gem_spec}
%dir %{_sysconfdir}/%{gem_name}
%config(noreplace) %{_sysconfdir}/%{gem_name}/fluent.conf
%dir %{_localstatedir}/log/fluentd
%dir %{_localstatedir}/cache/fluentd
%config(noreplace) %{_sysconfdir}/logrotate.d/fluentd
%doc %{gem_instdir}/AUTHORS
%doc %{gem_instdir}/CONTRIBUTING.md
%doc %{gem_instdir}/COPYING
%doc %{gem_instdir}/ChangeLog
%doc %{gem_instdir}/Gemfile
%doc %{gem_instdir}/README.md


%files doc
%doc %{gem_docdir}
%{gem_instdir}/Rakefile
%{gem_instdir}/test/
%{gem_instdir}/%{gem_name}.gemspec
%{gem_instdir}/example/*

%pre
getent group %{fluentd_group} >/dev/null || groupadd -r %{fluentd_group}
getent passwd %{fluentd_user} >/dev/null || \
    useradd -r -g %{fluentd_group} -d /etc/fluentd -s /sbin/nologin \
    -c "Fluentd data collection agent" %{fluentd_user}
exit 0

%post
%systemd_post fluentd.service

%preun
%systemd_preun fluentd.service

%postun
%systemd_postun	fluentd.service

%changelog
* Fri Oct 14 2016 Andrey Bardin <a15y87@gmail.com> - 0.14.8-1
- Updated to upstream version 0.14.8

* Mon Oct 10 2016 Andrey Bardin <a15y87@gmail.com> - 0.14.7-1
- Updated to upstream version 0.14.7

* Thu Jun 23 2016 Martin Mágr <mmagr@redhat.com> - 0.12.26-1
- Updated to upstream version 0.12.26

* Tue May 24 2016 Andrey Bardin <a15y87@gmail.com> - 0.12.24-1
- upgraded to 0.12.24

* Tue May 17 2016 Andrey Bardin <a15y87@gmail.com> - 0.12.23-2
- add logrotate config

* Wed Jul 29 2015 Graeme Gillies <ggillies@redhat.com> - 0.12.5-3
- Corrected ownership on executable files in /usr/bin

* Tue Jun 02 2015 Graeme Gillies <ggillies@redhat.com> - 0.12.5-2
- Fixed file ownership permissions for package

* Mon Feb 16 2015 Graeme Gillies <ggillies@redhat.com> - 0.12.5-1
- Upgraded to 0.12.5

* Mon Jan 05 2015 Graeme Gillies <ggillies@redhat.com> - 0.12.2-1
- Initial package

