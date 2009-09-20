# Generated from ohai-0.3.0.gem by gem2rpm -*- rpm-spec -*-
%define ruby_sitelib %(ruby -rrbconfig -e "puts Config::CONFIG['sitelibdir']")
%define gemdir %(ruby -rubygems -e 'puts Gem::dir' 2>/dev/null)
%define gemname ohai
%define geminstdir %{gemdir}/gems/%{gemname}-%{version}

Summary: Ohai profiles your system and emits JSON
Name: rubygem-%{gemname}
Version: 0.3.0
Release: 1%{?dist}
Group: Development/Languages
License: GPLv2+ or Ruby
URL: http://wiki.opscode.com/display/ohai
Source0: %{gemname}-%{version}.gem
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires: rubygems
Requires: rubygem(json) >= 0
Requires: rubygem(extlib) >= 0
BuildRequires: rubygems
BuildArch: noarch
Provides: rubygem(%{gemname}) = %{version}

%description
Ohai profiles your system and emits JSON


%prep

%build

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{gemdir}
gem install --local --install-dir %{buildroot}%{gemdir} \
            --force --rdoc %{SOURCE0}
mkdir -p %{buildroot}/%{_bindir}
mv %{buildroot}%{gemdir}/bin/* %{buildroot}/%{_bindir}
rmdir %{buildroot}%{gemdir}/bin
find %{buildroot}%{geminstdir}/bin -type f | xargs chmod a+x

%clean
rm -rf %{buildroot}

%files
%defattr(-, root, root, -)
%{_bindir}/ohai
%{gemdir}/gems/%{gemname}-%{version}/
%doc %{gemdir}/doc/%{gemname}-%{version}
%{gemdir}/cache/%{gemname}-%{version}.gem
%{gemdir}/specifications/%{gemname}-%{version}.gemspec


%changelog
* Sun Jun 21 2009 Matthew Kent <matt@bravenet.com> - 0.3.0-1
- New upstream version, drop all patches.

* Wed May 27 2009 Matthew Kent <matt@bravenet.com> - 0.2.0-4
- Add another patch. Second try at fixing zombies, first attempt was hanging 
  chef-client occasionally.

* Tue May 12 2009 Matthew Kent <matt@bravenet.com> - 0.2.0-3
- Include patch for reaping zombie processes.

* Mon May 11 2009 Matthew Kent <matt@bravenet.com> - 0.2.0-2
- Include upstream patch for exception handling issue causing chef-client to
  wipe pid files.

* Wed Mar 25 2009 Matthew Kent <matt@bravenet.com> - 0.2.0-1
- Initial package.
