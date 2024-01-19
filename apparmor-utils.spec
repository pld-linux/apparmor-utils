Summary:	AppArmor userlevel utilities that are useful in creating AppArmor profiles
Summary(pl.UTF-8):	Narzędzia przestrzeni użytkownika przydatne do tworzenia profili AppArmor
Name:		apparmor-utils
Version:	3.1.6
Release:	1
Epoch:		1
License:	GPL v2
Group:		Base
Source0:	http://launchpad.net/apparmor/3.1/%{version}/+download/apparmor-%{version}.tar.gz
# Source0-md5:	3e23347c5562418b165fd7ec452808aa
Patch0:		%{name}-pysetup.patch
URL:		http://wiki.apparmor.net/
BuildRequires:	gettext-tools
BuildRequires:	python3
Requires:	apparmor-binutils >= %{version}
Requires:	perl-LibAppArmor
Requires:	python3-LibAppArmor
Provides:	subdomain-utils
Obsoletes:	subdomain-utils < 2
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_vimdatadir	%{_datadir}/vim/vimfiles

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
%patch0 -p1

%{__sed} -i -e '1s, */usr/bin/env python,%{__python3},' utils/aa-*

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C utils install \
	PYTHON="%{__python3}" \
	PYSETUP_INSTALL_ARGS="--install-purelib=%{py3_sitescriptdir} --optimize=2" \
	DESTDIR=$RPM_BUILD_ROOT \
	BINDIR=$RPM_BUILD_ROOT%{_sbindir} \
	VIM_INSTALL_PATH=$RPM_BUILD_ROOT%{_vimdatadir}/syntax

install -d $RPM_BUILD_ROOT%{_vimdatadir}/ftdetect
cat > $RPM_BUILD_ROOT%{_vimdatadir}/ftdetect/apparmor.vim <<-EOF
au BufNewFile,BufRead /etc/apparmor.d/*,/etc/apparmor/profiles/* set filetype=apparmor
EOF

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(644,root,root,755)
%dir %{_sysconfdir}/apparmor
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/apparmor/easyprof.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/apparmor/logprof.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/apparmor/notify.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/apparmor/severity.db
%attr(755,root,root) %{_bindir}/aa-easyprof
%attr(755,root,root) %{_sbindir}/aa-audit
%attr(755,root,root) %{_sbindir}/aa-autodep
%attr(755,root,root) %{_sbindir}/aa-cleanprof
%attr(755,root,root) %{_sbindir}/aa-complain
%attr(755,root,root) %{_sbindir}/aa-decode
%attr(755,root,root) %{_sbindir}/aa-disable
%attr(755,root,root) %{_sbindir}/aa-enforce
%attr(755,root,root) %{_sbindir}/aa-genprof
%attr(755,root,root) %{_sbindir}/aa-logprof
%attr(755,root,root) %{_sbindir}/aa-mergeprof
%attr(755,root,root) %{_sbindir}/aa-notify
%attr(755,root,root) %{_sbindir}/aa-remove-unknown
%attr(755,root,root) %{_sbindir}/aa-unconfined
%dir %{_datadir}/apparmor
%{_datadir}/apparmor/easyprof
%{py3_sitescriptdir}/apparmor
%{py3_sitescriptdir}/apparmor-%{version}-py*.egg-info
%{_mandir}/man5/logprof.conf.5*
%{_mandir}/man8/aa-audit.8*
%{_mandir}/man8/aa-autodep.8*
%{_mandir}/man8/aa-cleanprof.8*
%{_mandir}/man8/aa-complain.8*
%{_mandir}/man8/aa-decode.8*
%{_mandir}/man8/aa-disable.8*
%{_mandir}/man8/aa-easyprof.8*
%{_mandir}/man8/aa-enforce.8*
%{_mandir}/man8/aa-genprof.8*
%{_mandir}/man8/aa-logprof.8*
%{_mandir}/man8/aa-mergeprof.8*
%{_mandir}/man8/aa-notify.8*
%{_mandir}/man8/aa-remove-unknown.8*
%{_mandir}/man8/aa-unconfined.8*

%files -n vim-syntax-apparmor
%defattr(644,root,root,755)
%{_vimdatadir}/ftdetect/apparmor.vim
%{_vimdatadir}/syntax/apparmor.vim
%{_mandir}/man5/apparmor.vim.5*
