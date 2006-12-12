%include	/usr/lib/rpm/macros.perl
%define		_vimdatadir	%{_datadir}/vim/vimfiles
%define		_ver 2.0
%define		_svnrel 142
Summary:	AppArmor userlevel utilities that are useful in creating AppArmor profiles
Summary(pl):	Narzêdzia przestrzeni u¿ytkownika przydatne do tworzenia profili AppArmor
Name:		apparmor-utils
Version:	%{_ver}.%{_svnrel}
Release:	0.2
Group:		Base
Source0:	http://forgeftp.novell.com/apparmor/Development%20-%20October%20Snapshot/%{name}-%{_ver}-%{_svnrel}.tar.gz
# Source0-md5:	b2447c84edc2df843b7bc4baa8a1eb2c
Source1:	Ycp.pm
Patch0:		%{name}-pld.patch
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

%description -l pl
Ten pakiet dostarcza kilka przydatnych programów pomocnych przy
tworzeniu i zarz±dzaniu profilami AppArmor. Ten pakiet jest czê¶ci±
zestawu narzêdzi zwanych SubDomain.

%package -n vim-syntax-apparmor
Summary:	AppArmor files support for Vim
Summary(pl):	Obs³uga plików AppArmor dla Vima
Group:		Applications/Editors/Vim
Requires:	vim >= 4:6.3.058-3

%description -n vim-syntax-apparmor
AppArmor files support for Vim.

%description -n vim-syntax-apparmor -l pl
Obs³uga plików AppArmor dla Vima.

%prep
%setup -q -n %{name}-%{_ver}
%patch0 -p1

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	BINDIR=$RPM_BUILD_ROOT%{_sbindir} \
	PERLDIR=$RPM_BUILD_ROOT%{perl_vendorlib}/Immunix

%find_lang %{name}

install -d $RPM_BUILD_ROOT%{_vimdatadir}/{syntax,ftdetect}
install apparmor.vim $RPM_BUILD_ROOT%{_vimdatadir}/syntax
install %{SOURCE1} $RPM_BUILD_ROOT%{perl_vendorlib}/Immunix

cat > $RPM_BUILD_ROOT%{_vimdatadir}/ftdetect/apparmor.vim <<-EOF
au BufNewFile,BufRead /etc/apparmor.d/*,/etc/apparmor/profiles/* set filetype=apparmor
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(644,root,root,755)
%dir %{_sysconfdir}/apparmor
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/apparmor/*
%attr(755,root,root) %{_sbindir}/*
%dir %{perl_vendorlib}/Immunix
%{perl_vendorlib}/Immunix/*
%dir /var/log/apparmor

%files -n vim-syntax-apparmor
%defattr(644,root,root,755)
%{_vimdatadir}/ftdetect/*
%{_vimdatadir}/syntax/*
