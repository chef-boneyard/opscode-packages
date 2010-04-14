# Generated from chef-server-api-0.8.8.gem by gem2rpm -*- rpm-spec -*-
%global gemdir %(ruby -rubygems -e 'puts Gem::dir' 2>/dev/null)
%global gemname chef-server-api
%global geminstdir %{gemdir}/gems/%{gemname}-%{version}

%global rubyabi 1.8

Summary: Merb slice providing REST API for Chef client access
Name: rubygem-%{gemname}
Version: 0.8.10
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
Requires: rubygem(merb-slices)
Requires: rubygem(merb-core)
Requires: rubygem(merb-assets)
Requires: rubygem(merb-helpers)
Requires: rubygem(thin)
Requires: rubygem(json)
Requires: rubygem(uuidtools)
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

%files
%defattr(-,root,root,-)
%doc %{geminstdir}/[A-Z]*
%dir %{geminstdir}
%{geminstdir}/app
%{geminstdir}/config
%{geminstdir}/lib
%{geminstdir}/public
%{geminstdir}/stubs
%{gemdir}/cache/%{gemname}-%{version}.gem
%{gemdir}/specifications/%{gemname}-%{version}.gemspec

%files doc
%defattr(-,root,root,-)
%{gemdir}/doc/%{gemname}-%{version}

%changelog
* Mon Apr 05 2010 Matthew Kent <mkent@magoazul.com> - 0.8.10-1
- New upstream version.

* Wed Mar 31 2010 Matthew Kent <mkent@magoazul.com> - 0.8.8-1
- Initial package
- Thanks to Joshua Timberman for the nice descriptions.
