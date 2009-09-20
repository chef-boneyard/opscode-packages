# Generated from chef-server-slice-0.6.2.gem by gem2rpm -*- rpm-spec -*-
%define ruby_sitelib %(ruby -rrbconfig -e "puts Config::CONFIG['sitelibdir']")
%define gemdir %(ruby -rubygems -e 'puts Gem::dir' 2>/dev/null)
%define gemname chef-server-slice
%define geminstdir %{gemdir}/gems/%{gemname}-%{version}

Summary: A systems integration framework
Name: rubygem-%{gemname}
Version: 0.7.10
Release: 1%{?dist}
Group: Development/Languages
License: Apache 
URL: http://wiki.opscode.com/display/chef
Source0: %{gemname}-%{version}.gem
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires: rubygems
Requires: rubygem(stomp) >= 0
Requires: rubygem(stompserver) >= 0
Requires: rubygem(ferret) >= 0
Requires: rubygem(merb-core) >= 0
Requires: rubygem(merb-haml) >= 0
Requires: rubygem(merb-assets) >= 0
Requires: rubygem(merb-helpers) >= 0
Requires: rubygem(merb-slices) >= 0
Requires: rubygem(mongrel) >= 0
Requires: rubygem(haml) >= 0
Requires: rubygem(ruby-openid) >= 0
Requires: rubygem(json) >= 0
Requires: rubygem(coderay) >= 0
BuildRequires: rubygems
BuildArch: noarch
Provides: rubygem(%{gemname}) = %{version}

%description
A systems integration framework, built to bring the benefits of configuration
management to your entire infrastructure.


%prep

%build

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{gemdir}
gem install --local --install-dir %{buildroot}%{gemdir} \
            --force --rdoc %{SOURCE0}

%clean
rm -rf %{buildroot}

%files
%defattr(-, root, root, -)
%{gemdir}/gems/%{gemname}-%{version}/
%doc %{gemdir}/doc/%{gemname}-%{version}
%doc %{geminstdir}/README.rdoc
%doc %{geminstdir}/LICENSE
%{gemdir}/cache/%{gemname}-%{version}.gem
%{gemdir}/specifications/%{gemname}-%{version}.gemspec


%changelog
* Thu Sep 17 2009 Matthew Kent <matt@bravenet.com> - 0.7.10-1
- New upstream version.

* Tue Aug 18 2009 Matthew Kent <matt@bravenet.com> - 0.7.8-4
- Put back requires for merb-slices, removed upstream by accident.
- Add patch to correct.

* Mon Aug 17 2009 Matthew Kent <matt@bravenet.com> - 0.7.8-3
- Version match chef rpm.

* Sun Aug 16 2009 Matthew Kent <matt@bravenet.com> - 0.7.8-2
- New upstream version.
- remove requires for syntax, merb-slices
- add requires for coderay

* Mon Jun 29 2009 Matthew Kent <matt@bravenet.com> - 0.7.4-1
- New upstream version.

* Mon Jun 15 2009 Matthew Kent <matt@bravenet.com> - 0.7.0-2
- Version match chef rpms.

* Thu Jun 11 2009 Matthew Kent <matt@bravenet.com> - 0.7.0-1
- New upstream version.

* Tue Jun 09 2009 Matthew Kent <matt@bravenet.com> - 0.6.2-11
- Sync release with other 2 packages 

* Mon Jun 08 2009 Matthew Kent <matt@bravenet.com> - 0.6.2-10
- Sync release with other 2 packages 

* Mon Jun 08 2009 Matthew Kent <matt@bravenet.com> - 0.6.2-10
- Sync release with other 2 packages 

* Thu Jun 04 2009 Matthew Kent <matt@bravenet.com> - 0.6.2-9
- Sync release with other 2 packages 

* Sat May 30 2009 Matthew Kent <matt@bravenet.com> - 0.6.2-8
- Sync release with other 2 packages 

* Wed May 27 2009 Matthew Kent <matt@bravenet.com> - 0.6.2-7
- Sync release with other 2 packages 

* Fri May 22 2009 Matthew Kent <matt@bravenet.com> - 0.6.2-6
- Sync release with other 2 packages 

* Wed May 13 2009 Matthew Kent <matt@bravenet.com> - 0.6.2-5
- Sync release with other 2 packages 

* Wed May 06 2009 Matthew Kent <matt@bravenet.com> - 0.6.2-4
- Sync release with other 2 packages 

* Wed May 06 2009 Matthew Kent <matt@bravenet.com> - 0.6.2-3
- Initial package
- Sync release with other 2 packages
