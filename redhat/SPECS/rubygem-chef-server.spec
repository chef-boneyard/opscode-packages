# Generated from chef-server-0.6.2.gem by gem2rpm -*- rpm-spec -*-
%define ruby_sitelib %(ruby -rrbconfig -e "puts Config::CONFIG['sitelibdir']")
%define gemdir %(ruby -rubygems -e 'puts Gem::dir' 2>/dev/null)
%define gemname chef-server
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
Requires: couchdb >= 0.9.0
Requires: rubygems
Requires: rubygem(stomp) >= 0
Requires: rubygem(stompserver) >= 0
Requires: rubygem(ferret) >= 0
Requires: rubygem(merb-core) >= 0
Requires: rubygem(merb-haml) >= 0
Requires: rubygem(merb-assets) >= 0
Requires: rubygem(merb-helpers) >= 0
Requires: rubygem(mongrel) >= 0
Requires: rubygem(haml) >= 0
Requires: rubygem(ruby-openid) >= 0
Requires: rubygem(json) >= 0
Requires: rubygem(coderay) >= 0
Requires: rubygem-chef >= %{version}-%{release}
Requires: rubygem-chef-server-slice >= %{version}-%{release}
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
mkdir -p %{buildroot}/%{_bindir}
mv %{buildroot}%{gemdir}/bin/* %{buildroot}/%{_bindir}
rmdir %{buildroot}%{gemdir}/bin
find %{buildroot}%{geminstdir}/bin -type f | xargs chmod a+x
install -Dp -m0644 %SOURCE2 %{buildroot}%{_sysconfdir}/chef/indexer.rb
install -Dp -m0644 %SOURCE2 %{buildroot}%{_sysconfdir}/chef/server.rb

%clean
rm -rf %{buildroot}

%files
%defattr(-, root, root, -)
%{_bindir}/chef-server
%{_bindir}/chef-indexer
%{gemdir}/gems/%{gemname}-%{version}/
%doc %{gemdir}/doc/%{gemname}-%{version}
%doc %{geminstdir}/README.rdoc
%doc %{geminstdir}/LICENSE
%{gemdir}/cache/%{gemname}-%{version}.gem
%{gemdir}/specifications/%{gemname}-%{version}.gemspec

# mkdir -p /var/run/chef
# mkdir -p /var/cache/chef
# mkdir -p /var/log/chef
# mkdir -p /var/lib/chef
# mkdir -p /srv/chef

%post
/sbin/chkconfig --add chef-indexer
/sbin/chkconfig --add chef-server

%preun
if [ $1 = 0 ]; then
  /sbin/service chef-server stop > /dev/null 2>&1
  /sbin/chkconfig --del chef-server
  /sbin/service chef-indexer stop > /dev/null 2>&1
  /sbin/chkconfig --del chef-indexer
fi

%changelog
* Sat Sep 19 2009 Joshua Timberman <joshua@opscode.com> - 0.7.10-2
- Add couchdb to dependencies.
- Add chef-server-slice to dependencies.
- Add server config file.
- Add chef-server,indexer init scripts.
- Add chef-server,indexer man pages.

* Thu Sep 17 2009 Matthew Kent <matt@bravenet.com> - 0.7.10-1
- New upstream version.

* Tue Aug 18 2009 Matthew Kent <matt@bravenet.com> - 0.7.8-4
- Version match chef rpm.

* Mon Aug 17 2009 Matthew Kent <matt@bravenet.com> - 0.7.8-3
- Version match chef rpm.

* Sun Aug 16 2009 Matthew Kent <matt@bravenet.com> - 0.7.8-2
- New upstream version.
- remove requires for syntax
- add requires for coderay

* Mon Jun 29 2009 Matthew Kent <matt@bravenet.com> - 0.7.4-1
- New upstream version.

* Mon Jun 15 2009 Matthew Kent <matt@bravenet.com> - 0.7.0-2
- Version match chef rpms.

* Thu Jun 11 2009 Matthew Kent <matt@bravenet.com> - 0.7.0-1
- New upstream version, drop all patches.

* Tue Jun 09 2009 Matthew Kent <matt@bravenet.com> - 0.6.2-11
- Patches from CHEF-178, already included upstream.

* Mon Jun 08 2009 Matthew Kent <matt@bravenet.com> - 0.6.2-10
- Patches from CHEF-277, already included upstream.

* Thu Jun 04 2009 Matthew Kent <matt@bravenet.com> - 0.6.2-9
- More patches against stable, already included upstream.

* Sat May 30 2009 Matthew Kent <matt@bravenet.com> - 0.6.2-8
- More patches against stable, already included upstream.

* Wed May 27 2009 Matthew Kent <matt@bravenet.com> - 0.6.2-7
- Another patch against stable, submitted as a ticket.

* Fri May 22 2009 Matthew Kent <matt@bravenet.com> - 0.6.2-6
- More patches against stable, all submitted as tickets.
- Mark config files deployed by the chef server recipe.

* Wed May 13 2009 Matthew Kent <matt@bravenet.com> - 0.6.2-5
- More patches against stable, all submitted as tickets. 

* Mon May 11 2009 Matthew Kent <matt@bravenet.com> - 0.6.2-4
- New strategy: package only the rubygem. All other work will be handled by the
  bootstrap. Better meshes with the current development model.

* Wed May 06 2009 Matthew Kent <matt@bravenet.com> - 0.6.2-3
- Break into distinct rpms for the rubygems libraries and the init scripts +
  configs. This should allow someone to use mod_passenger if they want.
- chef-server gets requires on rubygem-chef-server-slice
- move chef user to chef-client
- new init script and config

* Mon May 04 2009 Matthew Kent <matt@bravenet.com> - 0.6.2-1
- run new gem through gem2rpm, merge changes
- rebase patches against 0.6.2 tag, drop those included

* Sun Apr 13 2009 Matthew Kent <matt@bravenet.com> - 0.5.6-4
- new set of patches based off github branch
- bring back yum caching
- bump release to match chef rpm

* Fri Apr 02 2009 Matthew Kent <matt@bravenet.com> - 0.5.6-2
- add proper initscripts and configuration files
- add chef user
- requires couchdb
- generated series of relative patches from git repo of submitted tickets:
  CHEF-192, CHEF-198, CHEF-200. Dropped 0 byte ones.

* Wed Mar 25 2009 Matthew Kent <matt@bravenet.com> - 0.5.6-1
- Initial package
