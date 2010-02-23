%include	/usr/lib/rpm/macros.perl
%define		_vimdatadir	%{_datadir}/vim/vimfiles
%define		_ver 2.3
%define		_svnrel 1269
Summary:	AppArmor userlevel utilities that are useful in creating AppArmor profiles
Summary(pl.UTF-8):	Narzędzia przestrzeni użytkownika przydatne do tworzenia profili AppArmor
Name:		apparmor-utils
Version:	%{_ver}.%{_svnrel}
Release:	1
Epoch:		1
License:	GPL
Group:		Base
Source0:	http://forge.novell.com/modules/xfcontent/private.php/apparmor/AppArmor%202.3-Beta1/%{name}-%{_ver}-%{_svnrel}.tar.gz
# Source0-md5:	8f1e86b10118400fd63be7e768ef4c12
Source1:	Ycp.pm
URL:		http://forge.novell.com/modules/xfmod/project/?apparmor
BuildRequires:	gettext-devel
BuildRequires:	rpm-perlprov
Requires:	perl-DBD-SQLite >= 1.08
Provides:	subdomain-utils
Obsoletes:	subdomain-utils
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This provides some useful programs to help create and manage AppArmor
profiles. This package is part of a suite of tools that used to be
named SubDomain.

%description -l pl.UTF-8
Ten pakiet dostarcza kilka przydatnych programów pomocnych przy
tworzeniu i zarządzaniu profilami AppArmor. Ten pakiet jest częścią
zestawu narzędzi zwanych SubDomain.

%package -n vim-syntax-apparmor
Summary:	AppArmor files support for Vim
Summary(pl.UTF-8):	Obsługa plików AppArmor dla Vima
Group:		Applications/Editors/Vim
# for _vimdatadir existence
Requires:	vim-rt >= 4:6.3.058-3

%description -n vim-syntax-apparmor
AppArmor files support for Vim.

%description -n vim-syntax-apparmor -l pl.UTF-8
Obsługa plików AppArmor dla Vima.

%prep
%setup -q -n %{name}-%{_ver}

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
%{_mandir}/man5/*
%{_mandir}/man8/*

%files -n vim-syntax-apparmor
%defattr(644,root,root,755)
%{_vimdatadir}/ftdetect/*
%{_vimdatadir}/syntax/*
