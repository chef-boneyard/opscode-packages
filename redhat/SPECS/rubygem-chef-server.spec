# Generated from chef-server-0.8.8.gem by gem2rpm -*- rpm-spec -*-
%global gemdir %(ruby -rubygems -e 'puts Gem::dir' 2>/dev/null)
%global gemname chef-server
%global geminstdir %{gemdir}/gems/%{gemname}-%{version}

%global rubyabi 1.8

%global chef_user chef
%global chef_group chef

Summary: Merb application providing centralized management for Chef
Name: rubygem-%{gemname}
Version: 0.8.10
Release: 1%{?dist}
Group: Development/Languages
License: ASL 2.0
URL: http://wiki.opscode.com/display/chef
Source0: http://gems.rubyforge.org/gems/%{gemname}-%{version}.gem
# Upstream wants the openid gem installed while we can use ruby-openid just
# fine.
Patch0: rubygem-chef-server-0.8.10-gemspec.patch
## XXX: ticket
Source1: chef-server.1
Source2: chef-server-webui.1
Source3: chef-server.logrotate
Source4: chef-server-webui.logrotate
Source5: chef-server.init
Source6: chef-server-webui.init
Source7: chef-server.sysconf
Source8: chef-server-webui.sysconf
Source9: server.rb
Source10: webui.rb
%if 0%{?rhel}
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
%endif
Requires: ruby >= 1.8.6
Requires: ruby(rubygems)
Requires: ruby(abi) = %{rubyabi}
Requires: rubygem(merb-core)
Requires: rubygem(merb-haml)
Requires: rubygem(merb-assets)
Requires: rubygem(merb-helpers)
Requires: rubygem(thin)
Requires: rubygem(haml)
Requires: ruby(openid)
Requires: rubygem(json)
Requires: rubygem(coderay)
Requires: rubygem(chef)
Requires: rubygem(chef-solr)
BuildRequires: ruby(rubygems)
BuildRequires: ruby(abi) = %{rubyabi}
BuildArch: noarch
Provides: rubygem(%{gemname}) = %{version}

%description
The Chef Server is a Merb application that provides centralized storage and
distribution for recipes stored in "cookbooks," management and authentication
of client nodes and node data, and search indexes for that data.

This package contains the chef-server Merb application and associated files.

%package doc
Summary: Documentation for %{name}
Group: Documentation

Requires: %{name} = %{version}-%{release}

%description doc
This package contains documentation for %{name}.

%package -n chef-server
Summary: Server component of the Chef systems integration framework
Group: System Environment/Base

Requires: %{name} = %{version}-%{release}
Requires: rubygem(chef-server-api) = %{version}-%{release}
Requires: chef-common, chef-solr
Requires(pre): shadow-utils
Requires(post): chkconfig
Requires(preun): chkconfig
Requires(postun): initscripts

%description -n chef-server
The chef-server package provides a merb binary wrapper that loads up
the chef-server-api application.

%package -n chef-server-webui
Summary: WebUI component of the Chef systems integration framework
Group: System Environment/Base

Requires: %{name} = %{version}-%{release}
Requires: rubygem(chef-server-webui) = %{version}-%{release}
Requires: chef-server = %{version}-%{release}
Requires(post): chkconfig
Requires(preun): chkconfig
Requires(postun): initscripts

%description -n chef-server-webui
The chef-server-webui package provides a merb binary wrapper that loads up
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
install -Dp -m0644 %{SOURCE2} %{buildroot}%{_mandir}/man1/chef-server-webui.1

install -Dp -m0644 \
  %{SOURCE3} %{buildroot}%{_sysconfdir}/logrotate.d/chef-server
install -Dp -m0644 \
  %{SOURCE4} %{buildroot}%{_sysconfdir}/logrotate.d/chef-server-webui

# XXX: changes to %%_initddir on > f9
#install -Dp -m0755 \
#  %{buildroot}%{geminstdir}/distro/redhat/etc/init.d/chef-client \
#  %{buildroot}%{_initrddir}/chef-client

install -Dp -m0755 \
  %{SOURCE5} %{buildroot}%{_initrddir}/chef-server
install -Dp -m0755 \
  %{SOURCE6} %{buildroot}%{_initrddir}/chef-server-webui

install -Dp -m0644 \
  %{SOURCE7} %{buildroot}%{_sysconfdir}/sysconfig/chef-server
install -Dp -m0644 \
  %{SOURCE8} %{buildroot}%{_sysconfdir}/sysconfig/chef-server-webui

install -Dp -m0644 \
  %{SOURCE9} %{buildroot}%{_sysconfdir}/chef/server.rb
install -Dp -m0644 \
  %{SOURCE10} %{buildroot}%{_sysconfdir}/chef/webui.rb

mkdir -p %{buildroot}%{_localstatedir}/{log/chef,lib/chef,run/chef,cache/chef}

%clean
rm -rf %{buildroot}

%post -n chef-server
/sbin/chkconfig --add chef-server

%preun -n chef-server
if [ $1 -eq 0 ]; then
  /sbin/service chef-server stop > /dev/null 2>&1 || :
  /sbin/chkconfig --del chef-server
fi

%postun -n chef-server
if [ "$1" -ge "1" ] ; then
    /sbin/service chef-server condrestart >/dev/null 2>&1 || :
fi

%pre -n chef-server
getent group %{chef_group} >/dev/null || groupadd -r %{chef_group}
getent passwd %{chef_user} >/dev/null || \
useradd -r -g %{chef_group} -d %{_localstatedir}/lib/chef -s /sbin/nologin \
  -c "Chef user" %{chef_user}
exit 0

%post -n chef-server-webui
/sbin/chkconfig --add chef-server-webui

%preun -n chef-server-webui
if [ $1 -eq 0 ]; then
  /sbin/service chef-server-webui stop > /dev/null 2>&1 || :
  /sbin/chkconfig --del chef-server-webui
fi

%postun -n chef-server-webui
if [ "$1" -ge "1" ] ; then
    /sbin/service chef-server-webui condrestart >/dev/null 2>&1 || :
fi

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
%{gemdir}/doc/%{gemname}-%{version}

%files -n chef-server
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

%files -n chef-server-webui
%defattr(-,root,root,-)
%{_bindir}/chef-server-webui
%{_mandir}/man1/chef-server-webui.1*
%{_initrddir}/chef-server-webui
%config(noreplace) %{_sysconfdir}/sysconfig/chef-server-webui
%config(noreplace) %{_sysconfdir}/logrotate.d/chef-server-webui
%config(noreplace) %{_sysconfdir}/chef/webui.rb

%changelog
* Mon Apr 05 2010 Matthew Kent <mkent@magoazul.com> - 0.8.10-1
- New upstream version.

* Mon Mar 29 2010 Matthew Kent <mkent@magoazul.com> - 0.8.8-1
- Initial package
- Thanks to Joshua Timberman for the nice descriptions.
