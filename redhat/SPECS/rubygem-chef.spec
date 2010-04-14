# Generated from chef-0.8.8.gem by gem2rpm -*- rpm-spec -*-
%global gemdir %(ruby -rubygems -e 'puts Gem::dir' 2>/dev/null)
%global gemname chef
%global geminstdir %{gemdir}/gems/%{gemname}-%{version}

%global rubyabi 1.8

%global chef_user chef
%global chef_group chef

Summary: Client libraries for the Chef systems integration framework
Name: rubygem-%{gemname}
Version: 0.8.10
Release: 1%{?dist}
Group: Development/Languages
License: ASL 2.0
URL: http://wiki.opscode.com/display/chef
Source0: http://gems.rubyforge.org/gems/%{gemname}-%{version}.gem
# This are shipped in the gem but a couple are missing and dated
# XXX: ticket #
Source1: chef-client.8
Source2: chef-solo.8
Source3: knife.8
Source4: shef.8
# Not in the gem - fedora specific
# XXX: ticket #
Source5: chef-client.logrotate
# Out of date in the gem
# XXX: ticket #
Source6: chef-client.init
Source7: client.rb
Source8: solo.rb
Source9: chef-client.sysconf
Source10: chef-create-amqp_passwd
%if 0%{?rhel}
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
%endif
Requires: ruby >= 1.8.6
Requires: ruby(rubygems)
Requires: ruby(abi) = %{rubyabi}
Requires: rubygem(mixlib-config)
Requires: rubygem(mixlib-cli)
Requires: rubygem(mixlib-log)
Requires: rubygem(mixlib-authentication)
Requires: rubygem(ohai)
Requires: rubygem(bunny)
Requires: rubygem(json)
Requires: rubygem(erubis)
Requires: rubygem(extlib)
Requires: rubygem(moneta)
# Chef works with passwords
Requires: ruby-shadow
BuildRequires: ruby(rubygems)
BuildRequires: ruby(abi) = %{rubyabi}
BuildArch: noarch
Provides: rubygem(%{gemname}) = %{version}

%description
Chef is a systems integration framework and configuration management library
written in Ruby. Chef provides a Ruby library and API that can be used to
bring the benefits of configuration management to an entire infrastructure.

Chef can be run as a client (chef-client) to a server, or run as a standalone
tool (chef-solo). Configuration recipes are written in a pure Ruby DSL.

%package doc
Summary: Documentation for %{name}
Group: Documentation

Requires: %{name} = %{version}-%{release}

%description doc
This package contains documentation for %{name}.

%package -n chef
Summary: Client component of the Chef systems integration framework
Group: System Environment/Base

Requires: %{name} = %{version}-%{release}
Requires(pre): shadow-utils
Requires(post): chkconfig
Requires(preun): chkconfig
Requires(postun): initscripts

%description -n chef
This package contains the chef-client and chef-solo binaries and associated
files.

%package -n chef-common
Summary: Utility scripts used to config/init Chef
Group: System Environment/Base

Requires: %{name} = %{version}-%{release}

%description -n chef-common
This package contains utility scripts used to configure and initialize Chef.

%prep
%setup -q -c -T

mkdir -p .%{gemdir}
gem install -V \
  --local \
  --install-dir $(pwd)/%{gemdir} \
  --force --rdoc \
  %{SOURCE0}

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

mkdir -p %{buildroot}%{_mandir}/man8
for man in \
  %{SOURCE1} %{SOURCE2} %{SOURCE3} %{SOURCE4}
do $i
  install -p -m0644 $man %{buildroot}%{_mandir}/man8/
done

install -Dp -m0644 \
  %{SOURCE5} %{buildroot}%{_sysconfdir}/logrotate.d/chef-client

# XXX: changes to %%_initddir on > f9
#install -Dp -m0755 \
#  %{buildroot}%{geminstdir}/distro/redhat/etc/init.d/chef-client \
#  %{buildroot}%{_initrddir}/chef-client

install -Dp -m0755 \
  %{SOURCE6} %{buildroot}%{_initrddir}/chef-client

install -Dp -m0644 \
  %{SOURCE7} %{buildroot}%{_sysconfdir}/chef/client.rb
install -Dp -m0644 \
  %{SOURCE8} %{buildroot}%{_sysconfdir}/chef/solo.rb

install -Dp -m0644 \
  %{SOURCE9} %{buildroot}%{_sysconfdir}/sysconfig/chef-client

mkdir -p %{buildroot}%{_localstatedir}/{log/chef,run/chef,cache/chef}

install -Dp -m0755 \
  %{SOURCE10} %{buildroot}%{_sbindir}/chef-create-amqp_passwd


%clean
rm -rf %{buildroot}

%post -n chef
/sbin/chkconfig --add chef-client

%preun -n chef
if [ $1 -eq 0 ]; then
  /sbin/service chef-client stop > /dev/null 2>&1 || :
  /sbin/chkconfig --del chef-client
fi

%postun -n chef
if [ "$1" -ge "1" ] ; then
    /sbin/service chef-client condrestart >/dev/null 2>&1 || :
fi

%pre -n chef
getent group %{chef_group} >/dev/null || groupadd -r %{chef_group}
getent passwd %{chef_user} >/dev/null || \
useradd -r -g %{chef_group} -d %{_localstatedir}/lib/chef -s /sbin/nologin \
  -c "Chef user" %{chef_user}
exit 0

%files
%defattr(-,root,root,-)
%doc %{geminstdir}/[A-Z]*
%dir %{geminstdir}
%{geminstdir}/bin
%{geminstdir}/lib
# We already install what's required - also stuff for other gems is shipped
# XXX: ticket num
%exclude %{geminstdir}/distro
%{gemdir}/cache/%{gemname}-%{version}.gem
%{gemdir}/specifications/%{gemname}-%{version}.gemspec

%files doc
%defattr(-,root,root,-)
%{gemdir}/doc/%{gemname}-%{version}

%files -n chef
%defattr(-,root,root,-)
%{_bindir}/chef-client
%{_bindir}/chef-solo
%{_bindir}/knife
%{_bindir}/shef
%{_mandir}/man8/*
%{_initrddir}/chef-client
%config(noreplace) %{_sysconfdir}/sysconfig/chef-client
%config(noreplace) %{_sysconfdir}/logrotate.d/chef-client
%config(noreplace) %{_sysconfdir}/chef/client.rb
%config(noreplace) %{_sysconfdir}/chef/solo.rb
%attr(-,%{chef_user},root) %dir %{_localstatedir}/log/chef
%attr(-,%{chef_user},root) %dir %{_localstatedir}/cache/chef
%attr(-,%{chef_user},root) %dir %{_localstatedir}/run/chef

%files -n chef-common
%{_sbindir}/chef-create-amqp_passwd

%changelog
* Mon Apr 05 2010 Matthew Kent <mkent@magoazul.com> - 0.8.10-1
- New upstream version.

* Thu Mar 25 2010 Matthew Kent <matt@bravenet.com> - 0.8.8-1
- Initial package
- Thanks to Joshua Timberman for the Debian packaging used as a reference
