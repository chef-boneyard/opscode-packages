# thank you mandriva! 
# http://wiki.mandriva.com/en/Rpmbuild_and_git#The_git_Way
#%define chef_apply_git_patch_series \
#  for patch in $(awk '/^Patch.*:/ { print "%{_sourcedir}/"$2 }' %{_specdir}/%{name}.spec); \
#  do \
#    if [ -s $patch ]; then \
#      git-apply --exclude="spec/*" --whitespace=nowarn $patch; \
#    fi \
#  done
#BuildRequires: git

# Generated from chef-0.6.2.gem by gem2rpm -*- rpm-spec -*-
%define ruby_sitelib %(ruby -rrbconfig -e "puts Config::CONFIG['sitelibdir']")
%define gemdir %(ruby -rubygems -e 'puts Gem::dir' 2>/dev/null)
%define gemname chef
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
Requires: rubygem(mixlib-config) >= 1.0.12
Requires: rubygem(mixlib-cli) >= 0
Requires: rubygem(mixlib-log) >= 0
Requires: rubygem(ruby-openid) >= 0
Requires: rubygem(json) >= 0
Requires: rubygem(erubis) >= 0
Requires: rubygem(extlib) >= 0
Requires: rubygem(stomp) >= 0
Requires: rubygem(ohai) >= 0
BuildRequires: rubygems
BuildArch: noarch
Provides: rubygem(%{gemname}) = %{version}

# Series of patches carried in git @ http://github.com/mdkent/chef/tree/0.7.10-el5
#
# Currently generated from within the chef/ subdirectory via:
# git-format-patch --relative --suffix=".chef.patch" 0.7.10
#Patch0001: 

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

# can't apply normal patches to gems
#pushd %{buildroot}%{geminstdir}
#  %chef_apply_git_patch_series
#popd

%clean
rm -rf %{buildroot}

%files
%defattr(-, root, root, -)
%{_bindir}/chef-client
%{_bindir}/chef-solo
%{gemdir}/gems/%{gemname}-%{version}/
%doc %{gemdir}/doc/%{gemname}-%{version}
%doc %{geminstdir}/README.rdoc
%doc %{geminstdir}/LICENSE
%{gemdir}/cache/%{gemname}-%{version}.gem
%{gemdir}/specifications/%{gemname}-%{version}.gemspec


%changelog
* Thu Sep 17 2009 Matthew Kent <matt@bravenet.com> - 0.7.10-1
- New upstream version.
- Drop patch series.
- mixlib-config requires to 1.0.12.

* Tue Aug 18 2009 Matthew Kent <matt@bravenet.com> - 0.7.8-4
- Roll in fix for CHEF-500.

* Mon Aug 17 2009 Matthew Kent <matt@bravenet.com> - 0.7.8-3
- Roll in fix for CHEF-481.

* Sun Aug 16 2009 Matthew Kent <matt@bravenet.com> - 0.7.8-2
- New upstream version.

* Mon Jun 29 2009 Matthew Kent <matt@bravenet.com> - 0.7.4-1
- New upstream version.
- Drop patch series.

* Mon Jun 15 2009 Matthew Kent <matt@bravenet.com> - 0.7.0-2
- Add set of patches for a few issues, submitted as tickets. 

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
- Remove python-json Requires

* Wed May 13 2009 Matthew Kent <matt@bravenet.com> - 0.6.2-5
- More patches against stable, all submitted as tickets. 

* Mon May 11 2009 Matthew Kent <matt@bravenet.com> - 0.6.2-4
- New strategy: package only the rubygem. All other work will be handled by the
  bootstrap. Better meshes with the current development model.

* Wed May 06 2009 Matthew Kent <matt@bravenet.com> - 0.6.2-3
- Break into distinct rpms for the rubygems libraries and the init scripts +
  configs.
- moved chef user creation here
- new init script and config

* Mon May 04 2009 Matthew Kent <matt@bravenet.com> - 0.6.2-1
- run new gem through gem2rpm, merge changes
- rebase patches against 0.6.2 tag, drop those included
- includes patch to fix extra dependencies caused by executable perl

* Sun Apr 13 2009 Matthew Kent <matt@bravenet.com> - 0.5.6-4
- new set of patches based off github branch

* Wed Apr 08 2009 Matthew Kent <matt@bravenet.com> - 0.5.6-3
- add proper initscripts and configuration files
- yum speed patches (14/16) disabled, need to sort out licensing still
- start/stop not quite working, bug with pid file getting removed

* Fri Apr 02 2009 Matthew Kent <matt@bravenet.com> - 0.5.6-2
- generated series of relative patches from git repo of submitted tickets:
  CHEF-192, CHEF-198, CHEF-200. Dropped 0 byte ones.

* Wed Mar 25 2009 Matthew Kent <matt@bravenet.com> - 0.5.6-1
- Initial package
