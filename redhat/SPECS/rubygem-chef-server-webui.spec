# Generated from chef-server-webui-0.8.8.gem by gem2rpm -*- rpm-spec -*-
%global gemdir %(ruby -rubygems -e 'puts Gem::dir' 2>/dev/null)
%global gemname chef-server-webui
%global geminstdir %{gemdir}/gems/%{gemname}-%{version}

%global rubyabi 1.8

Summary: Merb app slice providing Web interface to API server for Chef
Name: rubygem-%{gemname}
Version: 0.8.10
Release: 1%{?dist}
Group: Development/Languages
License: ASL 2.0
URL: http://wiki.opscode.com/display/chef
Source0: http://gems.rubyforge.org/gems/%{gemname}-%{version}.gem
# Upstream wants the openid gem installed while we can use ruby-openid just
# fine.
Patch0: rubygem-chef-server-webui-0.8.10-gemspec.patch
%if 0%{?rhel}
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
%endif
Requires: ruby >= 1.8.6
Requires: ruby(rubygems)
Requires: ruby(abi) = %{rubyabi}
Requires: rubygem(merb-slices)
Requires: rubygem(merb-core)
Requires: rubygem(merb-haml)
Requires: rubygem(merb-assets)
Requires: rubygem(merb-helpers)
Requires: rubygem(merb-param-protection)
Requires: rubygem(thin)
Requires: rubygem(haml)
Requires: rubygem(json)
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

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc %{geminstdir}/[A-Z]*
%dir %{geminstdir}
%{geminstdir}/app
%{geminstdir}/config
%{geminstdir}/lib
%{geminstdir}/public
%{geminstdir}/stubs
%{geminstdir}/*.ru
%{gemdir}/cache/%{gemname}-%{version}.gem
%{gemdir}/specifications/%{gemname}-%{version}.gemspec

%files doc
%defattr(-,root,root,-)
%{gemdir}/doc/%{gemname}-%{version}

%changelog
* Mon Apr 05 2010 Matthew Kent <mkent@magoazul.com> - 0.8.10-1
- New upstream version.

* Mon Mar 29 2010 Matthew Kent <mkent@magoazul.com> - 0.8.8-1
- Initial package
- Thanks to Joshua Timberman for the nice descriptions.
