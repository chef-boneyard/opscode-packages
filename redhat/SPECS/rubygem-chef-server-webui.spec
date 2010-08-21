# Generated from chef-server-webui-0.8.8.gem by gem2rpm -*- rpm-spec -*-
%global gemdir %(ruby -rubygems -e 'puts Gem::dir' 2>/dev/null)
%global gemname chef-server-webui
%global geminstdir %{gemdir}/gems/%{gemname}-%{version}

%global rubyabi 1.8

Summary: Merb app slice providing Web interface to API server for Chef
Name: rubygem-%{gemname}
Version: 0.9.8
Release: 1%{?dist}
Group: Development/Languages
License: ASL 2.0
URL: http://wiki.opscode.com/display/chef
Source0: http://gems.rubyforge.org/gems/%{gemname}-%{version}.gem
# Upstream wants the openid gem installed while we can use ruby-openid just
# fine. Also lightens up on the merb deps.
Patch0: rubygem-chef-server-webui-%{version}-gemspec.patch
Source1: chef-server-webui.1
Source2: chef-server-webui.logrotate
Source3: chef-server-webui.init
Source4: chef-server-webui.sysconf
Source5: webui.rb
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
Requires: rubygem(thin)
Requires: rubygem(haml)
Requires: ruby(openid)
Requires: rubygem(coderay)
BuildRequires: ruby(rubygems)
BuildRequires: ruby(abi) = %{rubyabi}
BuildArch: noarch
Provides: rubygem(%{gemname}) = %{version}

%description
The Chef Server WebUI is a Merb application that accesses the Chef Server API
directly to provide an easy to use interface for managing Chef clients and
Chef server data.

This package contains the Merb slice and assets for the chef-server-webui.

%package doc
Summary: Documentation for %{name}
Group: Documentation

Requires: %{name} = %{version}-%{release}

%description doc
This package contains documentation for %{name}.

%package -n chef-server-webui
Summary: WebUI component of the Chef systems integration framework
Group: System Environment/Base

Requires: %{name} = %{version}-%{release}
Requires: rubygem(chef-server-webui) = %{version}-%{release}
Requires: chef-server-api = %{version}
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

install -Dp -m0644 %{SOURCE1} %{buildroot}%{_mandir}/man1/chef-server-webui.1

install -Dp -m0644 \
  %{SOURCE2} %{buildroot}%{_sysconfdir}/logrotate.d/chef-server-webui

# XXX: changes to %%_initddir on > f9
#install -Dp -m0755 \
#  %{buildroot}%{geminstdir}/distro/redhat/etc/init.d/chef-client \
#  %{buildroot}%{_initrddir}/chef-client

install -Dp -m0755 \
  %{SOURCE3} %{buildroot}%{_initrddir}/chef-server-webui

install -Dp -m0644 \
  %{SOURCE4} %{buildroot}%{_sysconfdir}/sysconfig/chef-server-webui

install -Dp -m0644 \
  %{SOURCE5} %{buildroot}%{_sysconfdir}/chef/webui.rb

#mkdir -p %{buildroot}%{_localstatedir}/{log/chef,lib/chef,run/chef,cache/chef}

%clean
rm -rf %{buildroot}

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

%files -n chef-server-webui
%defattr(-,root,root,-)
%{_bindir}/chef-server-webui
%{_mandir}/man1/chef-server-webui.1*
%{_initrddir}/chef-server-webui
%config(noreplace) %{_sysconfdir}/sysconfig/chef-server-webui
%config(noreplace) %{_sysconfdir}/logrotate.d/chef-server-webui
%config(noreplace) %{_sysconfdir}/chef/webui.rb

%changelog
* Mon Aug 9 2010 Matthew Kent <mkent@magoazul.com> - 0.9.8-1
- New upstream version.

* Sun Jul 18 2010 Matthew Kent <mkent@magoazul.com> - 0.9.6-1
- New upstream version.
- webui package broken out from chef-server.

* Mon May 24 2010 Matthew Kent <mkent@magoazul.com> - 0.8.16-1
- New upstream version.
- Update gemspec patch.

* Mon Apr 05 2010 Matthew Kent <mkent@magoazul.com> - 0.8.10-1
- New upstream version.

* Mon Mar 29 2010 Matthew Kent <mkent@magoazul.com> - 0.8.8-1
- Initial package
- Thanks to Joshua Timberman for the nice descriptions.
