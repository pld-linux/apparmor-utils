%include	/usr/lib/rpm/macros.perl
%define		_ver 2.0
%define		_svnrel 6379
Summary:	AppArmor userlevel utilities that are useful in creating AppArmor profiles
Name:		apparmor-utils
Version:	%{_ver}.%{_svnrel}
Release:	0.1
Group:		Base
Source0:	http://forge.novell.com/modules/xfcontent/private.php/apparmor/Development%20-%20April%20Snapshot/%{name}-%{_ver}-%{_svnrel}.tar.gz
# Source0-md5:	0144c81537fd724eaa6e23822edaaae1
License:	GPL
URL:		http://forge.novell.com/modules/xfmod/project/?apparmor
BuildRequires:	gettext-devel
BuildRequires:	rpm-perlprov
Provides:	subdomain-utils
Obsoletes:	subdomain-utils
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This provides some useful programs to help create and manage AppArmor
profiles. This package is part of a suite of tools that used to be
named SubDomain.

%prep
%setup -q -n %{name}-%{_ver}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	BINDIR=$RPM_BUILD_ROOT%{_sbindir} \
	PERLDIR=$RPM_BUILD_ROOT%{perl_vendorlib}/Immunix

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(644,root,root,755)
%dir %{_sysconfdir}/apparmor
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/apparmor/*
%attr(755,root,root) %{_sbindir}/*
%{perl_vendorlib}/Immunix/*
%dir /var/log/apparmor
