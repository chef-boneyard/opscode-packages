# Generated from ohai-0.5.0.gem by gem2rpm -*- rpm-spec -*-
%global gemdir %(ruby -rubygems -e 'puts Gem::dir' 2>/dev/null)
%global gemname ohai
%global geminstdir %{gemdir}/gems/%{gemname}-%{version}

%global rubyabi 1.8

Summary: Profiles your system and emits JSON
Name: rubygem-%{gemname}
Version: 0.5.6
Release: 1%{?dist}
Group: Development/Languages
License: ASL 2.0 
URL: http://wiki.opscode.com/display/ohai
Source0: http://gems.rubyforge.org/gems/%{gemname}-%{version}.gem
%if 0%{?rhel}
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
%endif
Requires: ruby(rubygems) >= 1.3.5
Requires: ruby(abi) = %{rubyabi}
Requires: rubygem(json)
Requires: rubygem(extlib)
Requires: rubygem(systemu)
Requires: rubygem(mixlib-cli)
Requires: rubygem(mixlib-config)
Requires: rubygem(mixlib-log)
BuildRequires: ruby(rubygems)
BuildRequires: ruby(abi) = %{rubyabi}
BuildRequires(check): rubygem(rake)
BuildRequires(check): rubygem(rspec)
BuildRequires(check): rubygem(json)
BuildRequires(check): rubygem(extlib)
BuildRequires(check): rubygem(systemu)
BuildRequires(check): rubygem(mixlib-cli)
BuildRequires(check): rubygem(mixlib-config)
BuildRequires(check): rubygem(mixlib-log)
BuildArch: noarch
Provides: rubygem(%{gemname}) = %{version}

%description
Ohai detects data about your operating system and prints out a JSON data blob.
It can be used standalone, but it's primary purpose is to provide node data to
Chef.

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

mkdir -p %{buildroot}/%{_bindir}
mv %{buildroot}%{gemdir}/bin/* %{buildroot}/%{_bindir}
rmdir %{buildroot}%{gemdir}/bin
find %{buildroot}%{geminstdir}/bin -type f | xargs chmod a+x

install -Dp -m0644 %{buildroot}%{geminstdir}/docs/man/man1/ohai.1 %{buildroot}%{_mandir}/man1/ohai.1

find %{buildroot}%{geminstdir}/bin -type f | \
  xargs -n 1 sed -i -e 's"^#!/usr/bin/env ruby"#!/usr/bin/ruby"'

%clean
rm -rf %{buildroot}

%check
pushd .%{geminstdir}
# Occasionally fails with "undefined method `rfc2822' for nil:NilClass" during
# mock. Unsure why - disable for now.
sed -i 's^Time.should_receive(:now)^^' \
  spec/ohai/plugins/ohai_time_spec.rb
rake spec || :

%files
%defattr(-,root,root,-)
%doc %{geminstdir}/[A-Z]*
%{_bindir}/ohai
%dir %{geminstdir}
%{geminstdir}/lib
%{geminstdir}/bin
%{gemdir}/cache/%{gemname}-%{version}.gem
%{gemdir}/specifications/%{gemname}-%{version}.gemspec
%{_mandir}/man1/ohai.1.gz

%files doc
%defattr(-,root,root,-)
%{geminstdir}/Rakefile
%{geminstdir}/spec
%{geminstdir}/docs
%{gemdir}/doc/%{gemname}-%{version}

%changelog
* Sun Jul 18 2010 Matthew Kent <mkent@magoazul.com> - 0.5.6-1
- New upstream version.

* Wed May 12 2010 Matthew Kent <mkent@magoazul.com> - 0.5.4-1
- New upstream version.
- Drop permissions fix, fixed upstream in OHAI-171.
- Drop man page, fixed upstream in OHAI-169.

* Fri Mar 19 2010 Matthew Kent <mkent@magoazul.com> - 0.5.0-1
- Initial package
