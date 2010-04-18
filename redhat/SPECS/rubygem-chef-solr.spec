# thank you mandriva! 
# http://wiki.mandriva.com/en/Rpmbuild_and_git#The_git_Way
%define chef_apply_git_patch_series \
  for patch in $(awk '/^Patch.*:/ { print "%{_sourcedir}/"$2 }' %{_specdir}/%{name}.spec); \
  do \
    if [ -s $patch ]; then \
      git-apply --exclude="spec/*" --exclude="Rakefile" --whitespace=nowarn $patch; \
    fi \
  done
BuildRequires: git

# Generated from chef-solr-0.8.8.gem by gem2rpm -*- rpm-spec -*-
%global gemdir %(ruby -rubygems -e 'puts Gem::dir' 2>/dev/null)
%global gemname chef-solr
%global geminstdir %{gemdir}/gems/%{gemname}-%{version}

%global rubyabi 1.8

%global chef_user chef
%global chef_group chef

Summary: Manages search indexes of Chef node attributes using SOLR
Name: rubygem-%{gemname}
Version: 0.8.10
Release: 2%{?dist}
Group: Development/Languages
License: ASL 2.0
URL: http://wiki.opscode.com/display/chef
Source0: http://gems.rubyforge.org/gems/%{gemname}-%{version}.gem
Source1: chef-solr.1
Source2: chef-solr-indexer.1
Source3: chef-solr-rebuild.8
Source4: chef-solr.logrotate
Source5: chef-solr-indexer.logrotate
Source6: chef-solr.init
Source7: chef-solr-indexer.init
Source8: chef-solr.sysconf
Source9: chef-solr-indexer.sysconf
Source10: solr.rb
Source11: solr-indexer.rb
%if 0%{?rhel}
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
%endif
Requires: ruby >= 1.8.6
Requires: ruby(rubygems)
Requires: ruby(abi) = %{rubyabi}
Requires: rubygem(libxml-ruby)
Requires: rubygem(uuidtools)
Requires: rubygem(chef)
BuildRequires: ruby(rubygems)
BuildRequires: ruby(abi) = %{rubyabi}
BuildArch: noarch
Provides: rubygem(%{gemname}) = %{version}

# Series of patches carried in git @ http://github.com/mdkent/chef/tree/0.8.10-el5
#
# Currently generated via:
# cd chef-solr && git format-patch --relative --suffix=".chef-solr.patch" 0.8.10
Patch0001: 0001-CHEF-1099-Drop-privileges-after-doing-clie.chef-solr.patch
Patch0002: 0002-CHEF-1087-Fix-various-chef-solr-logging-is.chef-solr.patch

%description
This package provides the chef-solr search engine which runs as a
solr-jetty server, and chef-solr-indexer that talks to the AMQP message queue,
by default rabbitmq-server.

The chef indexer listens to a message queue via AMQP for changes to search
indexes. It then either creates or deletes entries in the index according
to the information it is passed.

%package doc
Summary: Documentation for %{name}
Group: Documentation

Requires: %{name} = %{version}-%{release}

%description doc
This package contains documentation for %{name}.

%package -n chef-solr
Summary: SOLR component of the Chef systems integration framework
Group: System Environment/Base

Requires: %{name} = %{version}-%{release}
Requires: rabbitmq-server
Requires: java-1.6.0-openjdk
Requires: chef-common
Requires(pre): shadow-utils
Requires(post): chkconfig
Requires(preun): chkconfig
Requires(postun): initscripts

%description -n chef-solr
The chef-solr package provides:

 * A wrapper to launch the solr+jetty search engine.
 * chef-solr-indexer that talks to rabbitmq-server.

%prep
%setup -q -c -T

mkdir -p .%{gemdir}
gem install -V \
  --local \
  --install-dir $(pwd)/%{gemdir} \
  --force --rdoc \
  %{SOURCE0}

# can't apply normal patches to gems
pushd .%{geminstdir}
  %chef_apply_git_patch_series
popd

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

install -Dp -m0644 %{SOURCE1} %{buildroot}%{_mandir}/man1/chef-solr.1
install -Dp -m0644 %{SOURCE2} %{buildroot}%{_mandir}/man1/chef-solr-indexer.1
install -Dp -m0644 %{SOURCE3} %{buildroot}%{_mandir}/man8/chef-solr-indexer.8

install -Dp -m0644 \
  %{SOURCE4} %{buildroot}%{_sysconfdir}/logrotate.d/chef-solr
install -Dp -m0644 \
  %{SOURCE5} %{buildroot}%{_sysconfdir}/logrotate.d/chef-solr-indexer

# XXX: changes to %%_initddir on > f9
#install -Dp -m0755 \
#  %{buildroot}%{geminstdir}/distro/redhat/etc/init.d/chef-client \
#  %{buildroot}%{_initrddir}/chef-client

install -Dp -m0755 \
  %{SOURCE6} %{buildroot}%{_initrddir}/chef-solr
install -Dp -m0755 \
  %{SOURCE7} %{buildroot}%{_initrddir}/chef-solr-indexer

install -Dp -m0644 \
  %{SOURCE8} %{buildroot}%{_sysconfdir}/sysconfig/chef-solr
install -Dp -m0644 \
  %{SOURCE9} %{buildroot}%{_sysconfdir}/sysconfig/chef-solr-indexer

install -Dp -m0644 \
  %{SOURCE10} %{buildroot}%{_sysconfdir}/chef/solr.rb
install -Dp -m0644 \
  %{SOURCE11} %{buildroot}%{_sysconfdir}/chef/solr-indexer.rb

mkdir -p %{buildroot}%{_localstatedir}/\
{log/chef,lib/chef/solr,run/chef,cache/chef/solr}

mkdir -p %{buildroot}%{_localstatedir}/lib/chef/solr
pushd %{buildroot}%{_localstatedir}/lib/chef/solr
  tar zxvf %{buildroot}%{geminstdir}/solr/solr-home.tar.gz
popd
mkdir -p %{buildroot}%{_localstatedir}/lib/chef/solr/solr-jetty
pushd %{buildroot}%{_localstatedir}/lib/chef/solr/solr-jetty
  tar zxvf %{buildroot}%{geminstdir}/solr/solr-jetty.tar.gz
popd

%clean
rm -rf %{buildroot}

%post -n chef-solr
/sbin/chkconfig --add chef-solr
/sbin/chkconfig --add chef-solr-indexer

# move to indexer init script
# chef-create-amqp_passwd

%preun -n chef-solr
if [ $1 -eq 0 ]; then
  /sbin/service chef-solr stop > /dev/null 2>&1 || :
  /sbin/service chef-solr-indexer stop > /dev/null 2>&1 || :
  /sbin/chkconfig --del chef-solr
  /sbin/chkconfig --del chef-solr-indexer
fi

%postun -n chef-solr
if [ "$1" -ge "1" ] ; then
    /sbin/service chef-solr condrestart >/dev/null 2>&1 || :
    /sbin/service chef-solr-indexer condrestart >/dev/null 2>&1 || :
fi

%pre -n chef-solr
getent group %{chef_group} >/dev/null || groupadd -r %{chef_group}
getent passwd %{chef_user} >/dev/null || \
useradd -r -g %{chef_group} -d %{_localstatedir}/lib/chef -s /sbin/nologin \
  -c "Chef user" %{chef_user}
exit 0

%files
%defattr(-,root,root,-)
%doc %{geminstdir}/LICENSE
%doc %{geminstdir}/README.rdoc
%doc %{geminstdir}/VERSION
%dir %{geminstdir}
%{geminstdir}/bin
%{geminstdir}/lib
# We've already extracted this
%exclude %{geminstdir}/solr
%{gemdir}/cache/%{gemname}-%{version}.gem
%{gemdir}/specifications/%{gemname}-%{version}.gemspec

%files doc
%defattr(-,root,root,-)
%{geminstdir}/Rakefile
%{geminstdir}/spec
%{gemdir}/doc/%{gemname}-%{version}

%files -n chef-solr
%defattr(-,root,root,-)
%{_bindir}/chef-solr
%{_bindir}/chef-solr-indexer
%{_bindir}/chef-solr-rebuild
%{_mandir}/man1/chef-solr*
%{_mandir}/man8/chef-solr*
%{_initrddir}/chef-solr
%{_initrddir}/chef-solr-indexer
%config(noreplace) %{_sysconfdir}/sysconfig/chef-solr
%config(noreplace) %{_sysconfdir}/logrotate.d/chef-solr
%config(noreplace) %{_sysconfdir}/chef/solr.rb
%config(noreplace) %{_sysconfdir}/chef/solr-indexer.rb
%config(noreplace) %{_sysconfdir}/sysconfig/chef-solr-indexer
%config(noreplace) %{_sysconfdir}/logrotate.d/chef-solr-indexer
%attr(-,%{chef_user},root) %dir %{_localstatedir}/log/chef
%attr(-,%{chef_user},root) %dir %{_localstatedir}/cache/chef/solr
%attr(-,%{chef_user},root) %dir %{_localstatedir}/run/chef
%attr(-,%{chef_user},root) %{_localstatedir}/lib/chef/solr

%changelog
* Fri Apr 16 2010 Matthew Kent <mkent@magoazul.com> - 0.8.10-2
- Eat logrotate output.
- Strict directory ownership.

* Mon Apr 05 2010 Matthew Kent <mkent@magoazul.com> - 0.8.10-1
- New upstream version.

* Wed Mar 31 2010 Matthew Kent <mkent@magoazul.com> - 0.8.8-1
- Initial package
