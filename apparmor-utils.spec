#
# Conditional build:
%bcond_with	python3	# use Python 3 instead of Python 2

Summary:	AppArmor userlevel utilities that are useful in creating AppArmor profiles
Summary(pl.UTF-8):	Narzędzia przestrzeni użytkownika przydatne do tworzenia profili AppArmor
Name:		apparmor-utils
Version:	2.13.4
Release:	1
Epoch:		1
License:	GPL v2
Group:		Base
Source0:	http://launchpad.net/apparmor/2.13/%{version}/+download/apparmor-%{version}.tar.gz
# Source0-md5:	a50b793a3362551f07733be3df9c328f
Patch0:		%{name}-pysetup.patch
URL:		http://wiki.apparmor.net/
BuildRequires:	gettext-tools
%if %{with python3}
BuildRequires:	python3
Requires:	python3-LibAppArmor
%else
BuildRequires:	python
Requires:	python-LibAppArmor
%endif
Requires:	apparmor-binutils >= %{version}
Requires:	perl-LibAppArmor
Provides:	subdomain-utils
Obsoletes:	subdomain-utils
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

%if %{with python3}
%{__sed} -i -e '1s, */usr/bin/env python,%{__python3},' utils/aa-*
%else
%{__sed} -i -e '1s, */usr/bin/env python,%{__python},' utils/aa-*
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C utils install \
%if %{with python3}
	PYTHON="%{__python3}" \
	PYSETUP_INSTALL_ARGS="--install-purelib=%{py3_sitescriptdir} --optimize=2" \
%else
	PYTHON="%{__python}" \
	PYSETUP_INSTALL_ARGS="--install-purelib=%{py_sitescriptdir} --optimize=2" \
%endif
	DESTDIR=$RPM_BUILD_ROOT \
	BINDIR=$RPM_BUILD_ROOT%{_sbindir} \
	VIM_INSTALL_PATH=$RPM_BUILD_ROOT%{_vimdatadir}/syntax

install -d $RPM_BUILD_ROOT%{_vimdatadir}/ftdetect
cat > $RPM_BUILD_ROOT%{_vimdatadir}/ftdetect/apparmor.vim <<-EOF
au BufNewFile,BufRead /etc/apparmor.d/*,/etc/apparmor/profiles/* set filetype=apparmor
EOF

%if %{without python3}
%py_postclean
%endif

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
%attr(755,root,root) %{_sbindir}/aa-status
%attr(755,root,root) %{_sbindir}/aa-unconfined
%attr(755,root,root) %{_sbindir}/apparmor_status
%dir %{_datadir}/apparmor
%{_datadir}/apparmor/easyprof
%if %{with python3}
%{py3_sitescriptdir}/apparmor
%{py3_sitescriptdir}/apparmor-%{version}-py*.egg-info
%else
%dir %{py_sitescriptdir}/apparmor
%{py_sitescriptdir}/apparmor/*.py[co]
%dir %{py_sitescriptdir}/apparmor/rule
%{py_sitescriptdir}/apparmor/rule/*.py[co]
%{py_sitescriptdir}/apparmor-%{version}-py*.egg-info
%endif
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
%{_mandir}/man8/aa-status.8*
%{_mandir}/man8/aa-unconfined.8*
%{_mandir}/man8/apparmor_status.8*

%files -n vim-syntax-apparmor
%defattr(644,root,root,755)
%{_vimdatadir}/ftdetect/apparmor.vim
%{_vimdatadir}/syntax/apparmor.vim
%{_mandir}/man5/apparmor.vim.5*
