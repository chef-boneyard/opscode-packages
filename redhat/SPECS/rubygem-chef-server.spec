# Generated from chef-server-0.8.8.gem by gem2rpm -*- rpm-spec -*-
%global gemdir %(ruby -rubygems -e 'puts Gem::dir' 2>/dev/null)
%global gemname chef-server
%global geminstdir %{gemdir}/gems/%{gemname}-%{version}

%global rubyabi 1.8

Summary: Merb application providing centralized management for Chef
Name: rubygem-%{gemname}
Version: 0.9.6
Release: 1%{?dist}
Group: Development/Languages
License: ASL 2.0
URL: http://wiki.opscode.com/display/chef
Source0: http://gems.rubyforge.org/gems/%{gemname}-%{version}.gem
%if 0%{?rhel}
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
%endif
Requires: ruby >= 1.8.6
Requires: ruby(rubygems)
Requires: ruby(abi) = %{rubyabi}
Requires: rubygem(chef-server-api) = %{version}
Requires: rubygem(chef-server-webui) = %{version}
Requires: rubygem(chef-solr) = %{version}
BuildRequires: ruby(rubygems)
BuildRequires: ruby(abi) = %{rubyabi}
BuildArch: noarch
Provides: rubygem(%{gemname}) = %{version}

%description
The Chef Server is a Merb application that provides centralized storage and
distribution for recipes stored in "cookbooks," management and authentication
of client nodes and node data, and search indexes for that data.

This package is a meta package that depends on chef-server-api and
chef-server-webui to provide both Server components.

%package doc
Summary: Documentation for %{name}
Group: Documentation

Requires: %{name} = %{version}-%{release}

%description doc
This package contains documentation for %{name}.

%package -n chef-server
Summary: Meta package that depends on Chef Server API and WebUI
Group: System Environment/Base

Requires: %{name} = %{version}-%{release}
Requires: rubygem(chef-server) = %{version}-%{release}
Requires: chef-server-api = %{version}
Requires: chef-server-webui = %{version}

%description -n chef-server
This package is a meta package that depends on chef-server-api and
chef-server-webui to provide both Server components.

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

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc %{geminstdir}/[A-Z]*
%dir %{geminstdir}
%{geminstdir}/lib
%{gemdir}/cache/%{gemname}-%{version}.gem
%{gemdir}/specifications/%{gemname}-%{version}.gemspec

%files doc
%defattr(-,root,root,-)
%{gemdir}/doc/%{gemname}-%{version}

%files -n chef-server

%changelog
* Sun Jul 18 2010 Matthew Kent <mkent@magoazul.com> - 0.9.6-1
- New upstream version.
- We become a meta package to install the required chef server components.

* Mon May 24 2010 Matthew Kent <mkent@magoazul.com> - 0.8.16-1
- New upstream version.
- Update gemspec patch.

* Wed Apr 21 2010 Matthew Kent <mkent@magoazul.com> - 0.8.10-3
- Updated default configs.

* Fri Apr 16 2010 Matthew Kent <mkent@magoazul.com> - 0.8.10-2
- Eat logrotate output.
- Strict directory ownership.

* Mon Apr 05 2010 Matthew Kent <mkent@magoazul.com> - 0.8.10-1
- New upstream version.

* Mon Mar 29 2010 Matthew Kent <mkent@magoazul.com> - 0.8.8-1
- Initial package
- Thanks to Joshua Timberman for the nice descriptions.
