# Generated from stompserver-0.9.9.gem by gem2rpm -*- rpm-spec -*-
%define ruby_sitelib %(ruby -rrbconfig -e "puts Config::CONFIG['sitelibdir']")
%define gemdir %(ruby -rubygems -e 'puts Gem::dir' 2>/dev/null)
%define gemname stompserver
%define geminstdir %{gemdir}/gems/%{gemname}-%{version}

Summary: A very light messaging server
Name: rubygem-%{gemname}
Version: 0.9.9
Release: 2%{?dist}
Group: Development/Languages
License: GPLv2+ or Ruby
URL: http://stomp.codehaus.org/
Source0: %{gemname}-%{version}.gem
Source1: stompserver.init
Source2: stompserver.conf
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires: rubygems
Requires: rubygem(daemons) >= 1.0.2
Requires: rubygem(eventmachine) >= 0.7.2
Requires: rubygem(hoe) >= 1.1.1
Requires: rubygem(hoe) >= 1.3.0
BuildRequires: rubygems
BuildArch: noarch
Provides: rubygem(%{gemname}) = %{version}
Requires(post): chkconfig
Requires(preun): chkconfig
Requires(preun): initscripts
Requires(postun): initscripts

%description
Stomp messaging server with file/dbm/memory/activerecord based FIFO queues,
queue monitoring, and basic authentication.


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

# stompserver has some interesting pathing conventions that prevent using
# standard structure. lump everything here for now. 
install -d -m0755 %{buildroot}%{_localstatedir}/lib/stompserver
#install -d -m0755 %{buildroot}%{_localstatedir}/run/stompserver
#install -d -m0755 %{buildroot}%{_localstatedir}/log/stompserver

install -Dp -m0755 %SOURCE1 %{buildroot}%{_initrddir}/stompserver
install -Dp -m0644 %SOURCE2 %{buildroot}%{_sysconfdir}/stompserver.conf

%clean
rm -rf %{buildroot}

%files
%defattr(-, root, root, -)
%{_bindir}/stompserver
%{gemdir}/gems/%{gemname}-%{version}/
%doc %{gemdir}/doc/%{gemname}-%{version}
%doc %{geminstdir}/History.txt
%doc %{geminstdir}/Manifest.txt
%doc %{geminstdir}/README.txt
%doc %{geminstdir}/client/README.txt
%{gemdir}/cache/%{gemname}-%{version}.gem
%{gemdir}/specifications/%{gemname}-%{version}.gemspec
%{_initrddir}/stompserver
%config(noreplace) %{_sysconfdir}/stompserver.conf

%attr(-, stomp, stomp) %{_localstatedir}/lib/stompserver
#%attr(-, stomp, stomp) %{_localstatedir}/run/stompserver
#%attr(-, stomp, stomp) %{_localstatedir}/log/stompserver

%pre
# Add the "stomp" user
# couldn't find anything conflicting with this uid
/usr/sbin/useradd -c "StompServer User" -u 171 \
  -s /sbin/nologin -r -d %{_localstatedir}/lib/stompserver stomp 2> /dev/null || :

%post
# Register the service
/sbin/chkconfig --add stompserver 

%preun
if [ $1 = 0 ]; then
  /sbin/service stompserver stop > /dev/null 2>&1
  /sbin/chkconfig --del stompserver
fi

%changelog
* Thu Mar 26 2009 Matthew Kent <matt@bravenet.com> - 0.9.9-2
- add proper initscript and configuration file
- add stomp user

* Wed Mar 25 2009 Matthew Kent <matt@bravenet.com> - 0.9.9-1
- Initial package
