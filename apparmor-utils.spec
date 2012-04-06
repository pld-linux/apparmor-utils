%include	/usr/lib/rpm/macros.perl
%define		_vimdatadir	%{_datadir}/vim/vimfiles
Summary:	AppArmor userlevel utilities that are useful in creating AppArmor profiles
Summary(pl.UTF-8):	Narzędzia przestrzeni użytkownika przydatne do tworzenia profili AppArmor
Name:		apparmor-utils
Version:	2.7.2
Release:	1
Epoch:		1
License:	GPL
Group:		Base
Source0:	http://launchpad.net/apparmor/2.7/%{version}/+download/apparmor-%{version}.tar.gz
# Source0-md5:	2863e85bdfdf9ee35b83db6721fed1f1
Source1:	Ycp.pm
URL:		http://apparmor.wiki.kernel.org/
BuildRequires:	gettext-devel
BuildRequires:	rpm-perlprov
Requires:	perl-DBD-SQLite >= 1.08
Provides:	subdomain-utils
Obsoletes:	subdomain-utils
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_noautoreq	'perl(ycp)'

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
%setup -q -n apparmor-%{version}

%install
rm -rf $RPM_BUILD_ROOT
cd utils

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	BINDIR=$RPM_BUILD_ROOT%{_sbindir} \
	PERLDIR=$RPM_BUILD_ROOT%{perl_vendorlib}/Immunix

install -d $RPM_BUILD_ROOT%{_vimdatadir}/{syntax,ftdetect}
install apparmor.vim $RPM_BUILD_ROOT%{_vimdatadir}/syntax
install %{SOURCE1} $RPM_BUILD_ROOT%{perl_vendorlib}/Immunix

# outdated version of pt
%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/locale/pt_PT

cat > $RPM_BUILD_ROOT%{_vimdatadir}/ftdetect/apparmor.vim <<-EOF
au BufNewFile,BufRead /etc/apparmor.d/*,/etc/apparmor/profiles/* set filetype=apparmor
EOF

cd ..

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(644,root,root,755)
%dir %{_sysconfdir}/apparmor
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/apparmor/*.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/apparmor/severity.db
%attr(755,root,root) %{_sbindir}/aa-*
%attr(755,root,root) %{_sbindir}/apparmor_status
%dir %{perl_vendorlib}/Immunix
%{perl_vendorlib}/Immunix/*.pm
%{_mandir}/man5/logprof.conf.5*
%{_mandir}/man8/aa-*.8*
%{_mandir}/man8/apparmor_status.8*

%files -n vim-syntax-apparmor
%defattr(644,root,root,755)
%{_vimdatadir}/ftdetect/apparmor.vim
%{_vimdatadir}/syntax/apparmor.vim
