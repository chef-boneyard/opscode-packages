# Generated from chef-server-api-0.8.8.gem by gem2rpm -*- rpm-spec -*-
%global gemdir %(ruby -rubygems -e 'puts Gem::dir' 2>/dev/null)
%global gemname chef-server-api
%global geminstdir %{gemdir}/gems/%{gemname}-%{version}

%global rubyabi 1.8

%global chef_user chef
%global chef_group chef

Summary: Merb slice providing REST API for Chef client access
Name: rubygem-%{gemname}
Version: 0.9.8
Release: 2%{?dist}
Group: Development/Languages
License: ASL 2.0
URL: http://wiki.opscode.com/display/chef
Source0: http://gems.rubyforge.org/gems/%{gemname}-%{version}.gem
# Lightens up on the merb and uuidtools deps.
Patch0: rubygem-chef-server-api-%{version}-gemspec.patch
Source1: chef-server.1
Source2: chef-server.logrotate
Source3: chef-server.init
Source4: chef-server.sysconf
Source5: server.rb
%if 0%{?rhel}
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
%endif
Requires: ruby >= 1.8.6
Requires: ruby(rubygems)
Requires: ruby(abi) = %{rubyabi}
Requires: rubygem(merb-core)
Requires: rubygem(merb-slices)
Requires: rubygem(merb-assets)
Requires: rubygem(merb-helpers)
Requires: rubygem(merb-haml)
Requires: rubygem(merb-param-protection)
Requires: rubygem(json)
Requires: rubygem(uuidtools)
Requires: rubygem(thin)
Requires: rubygem(chef-solr)
Requires: couchdb
Requires: rabbitmq-server
BuildRequires: ruby(rubygems)
BuildRequires: ruby(abi) = %{rubyabi}
BuildArch: noarch
Provides: rubygem(%{gemname}) = %{version}
# XXX: Goes away in Fedora
Obsoletes: rubygem(chef-server-slice)

%description
The chef-server-api package provides the API for the Chef Server so
clients can connect and is started with the chef-server program.

This package contains the Merb slice for the chef-server-api.

%package doc
Summary: Documentation for %{name}
Group: Documentation

Requires: %{name} = %{version}-%{release}

%description doc
This package contains documentation for %{name}.

%package -n chef-server-api
Summary: Server component of the Chef systems integration framework
Group: System Environment/Base

Requires: %{name} = %{version}-%{release}
Requires: rubygem(chef-server-api) = %{version}-%{release}
Requires: chef-common = %{version}
Requires: chef-solr = %{version}
Requires(pre): shadow-utils
Requires(post): chkconfig
Requires(preun): chkconfig
Requires(postun): initscripts

%description -n chef-server-api
The chef-server package provides a merb binary wrapper that loads up
the chef-server-api application.

%prep
%setup -q -c -T

mkdir -p .%{gemdir}
gem install -V \
  --local \
  --install-dir $(pwd)/%{gemdir} \
  --force --rdoc \
  %{SOURCE0}

pushd .%{gemdir}
%patch0 -p0

%build

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{gemdir}
cp -a .%{gemdir}/* %{buildroot}%{gemdir}/

mkdir -p %{buildroot}/%{_bindir}
mv %{buildroot}%{gemdir}/bin/* %{buildroot}/%{_bindir}
rmdir %{buildroot}%{gemdir}/bin
find %{buildroot}%{geminstdir}/bin -type f | xargs chmod a+x

find %{buildroot}%{geminstdir}/bin -type f | \
  xargs -n 1 sed -i -e 's"^#!/usr/bin/env ruby"#!/usr/bin/ruby"'

install -Dp -m0644 %{SOURCE1} %{buildroot}%{_mandir}/man1/chef-server.1

install -Dp -m0644 \
  %{SOURCE2} %{buildroot}%{_sysconfdir}/logrotate.d/chef-server

# XXX: changes to %%_initddir on > f9
#install -Dp -m0755 \
#  %{buildroot}%{geminstdir}/distro/redhat/etc/init.d/chef-client \
#  %{buildroot}%{_initrddir}/chef-client

install -Dp -m0755 \
  %{SOURCE3} %{buildroot}%{_initrddir}/chef-server

install -Dp -m0644 \
  %{SOURCE4} %{buildroot}%{_sysconfdir}/sysconfig/chef-server

install -Dp -m0644 \
  %{SOURCE5} %{buildroot}%{_sysconfdir}/chef/server.rb

mkdir -p %{buildroot}%{_localstatedir}/{log/chef,lib/chef,run/chef,cache/chef}

%clean
rm -rf %{buildroot}

%post -n chef-server-api
/sbin/chkconfig --add chef-server

%preun -n chef-server-api
if [ $1 -eq 0 ]; then
  /sbin/service chef-server stop > /dev/null 2>&1 || :
  /sbin/chkconfig --del chef-server
fi

%postun -n chef-server-api
if [ "$1" -ge "1" ] ; then
    /sbin/service chef-server condrestart >/dev/null 2>&1 || :
fi

%pre -n chef-server-api
getent group %{chef_group} >/dev/null || groupadd -r %{chef_group}
getent passwd %{chef_user} >/dev/null || \
useradd -r -g %{chef_group} -d %{_localstatedir}/lib/chef -s /sbin/nologin \
  -c "Chef user" %{chef_user}
exit 0

%files
%defattr(-,root,root,-)
%doc %{geminstdir}/[A-Z]*
%dir %{geminstdir}
%{geminstdir}/app
%{geminstdir}/bin
%{geminstdir}/config
%{geminstdir}/lib
%{geminstdir}/public
%{geminstdir}/*.ru
%{gemdir}/cache/%{gemname}-%{version}.gem
%{gemdir}/specifications/%{gemname}-%{version}.gemspec

%files doc
%defattr(-,root,root,-)
%{geminstdir}/spec
%{gemdir}/doc/%{gemname}-%{version}

%files -n chef-server-api
%defattr(-,root,root,-)
%{_bindir}/chef-server
%{_mandir}/man1/chef-server.1*
%{_initrddir}/chef-server
%config(noreplace) %{_sysconfdir}/sysconfig/chef-server
%config(noreplace) %{_sysconfdir}/logrotate.d/chef-server
%config(noreplace) %{_sysconfdir}/chef/server.rb
%attr(-,%{chef_user},root) %dir %{_localstatedir}/log/chef
%attr(-,%{chef_user},root) %dir %{_localstatedir}/cache/chef
%attr(-,%{chef_user},root) %dir %{_localstatedir}/run/chef
%attr(-,%{chef_user},root) %dir %{_localstatedir}/lib/chef

%changelog
* Mon Aug 9 2010 Matthew Kent <mkent@magoazul.com> - 0.9.8-2
- Dependency on rubygem-merb-haml

* Mon Aug 9 2010 Matthew Kent <mkent@magoazul.com> - 0.9.8-1
- New upstream version.

* Sun Jul 18 2010 Matthew Kent <mkent@magoazul.com> - 0.9.6-1
- New upstream version.
- api package broken out from chef-server.

* Mon May 24 2010 Matthew Kent <mkent@magoazul.com> - 0.8.16-1
- New upstream version.

* Mon Apr 05 2010 Matthew Kent <mkent@magoazul.com> - 0.8.10-1
- New upstream version.

* Wed Mar 31 2010 Matthew Kent <mkent@magoazul.com> - 0.8.8-1
- Initial package
- Thanks to Joshua Timberman for the nice descriptions.
