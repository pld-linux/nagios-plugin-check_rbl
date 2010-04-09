#
# Conditional build:
%bcond_without	tests	# do not perform "make test"

%include	/usr/lib/rpm/macros.perl
%define		plugin	check_rbl
Summary:	Nagios plugin to check if an server is blacklisted in RBL servers
Name:		nagios-plugin-%{plugin}
Version:	1.2.0
Release:	1
License:	GPL
Group:		Networking
Source0:	https://trac.id.ethz.ch/projects/nagios_plugins/downloads/%{plugin}-%{version}.tar.gz
# Source0-md5:	630902d9d7b644a0ab6537030ec40f12
Source1:	%{plugin}.cfg
Source2:	%{plugin}.ini
URL:		https://trac.id.ethz.ch/projects/nagios_plugins/wiki/check_rbl
BuildRequires:	perl-ExtUtils-MakeMaker >= 6.42
BuildRequires:	rpm-perlprov >= 4.1-13
BuildRequires:	sed >= 4.0
%if %{with tests}
BuildRequires:	perl-Nagios-Plugin
BuildRequires:	perl-Net-DNS
BuildRequires:	perl-Parallel-Iterator
BuildRequires:	perl-Readonly
%endif
Requires:	nagios-common
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_noautoreq	'perl(utils)'

%define		_sysconfdir	/etc/nagios/plugins
%define		plugindir	%{_prefix}/lib/nagios/plugins

%description
Nagios plugin to check if an server is blacklisted in RBL servers.

%prep
%setup -q -n %{plugin}-%{version}

# https://trac.id.ethz.ch/projects/nagios_plugins/ticket/68
%{__sed} -i -e '
# not needed, so kill to avoid extra dep
/use version;/d
' %{plugin}

%build
%{__perl} Makefile.PL \
	INSTALLVENDORSCRIPT=%{plugindir} \
	INSTALLDIRS=vendor

%{__make}
%{?with_tests:%{__make} test}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_sysconfdir}
cp -a %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/%{plugin}.cfg
cp -a %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/%{plugin}.ini

rm -f $RPM_BUILD_ROOT%{perl_archlib}/perllocal.pod
rm -f $RPM_BUILD_ROOT%{perl_vendorarch}/auto/check_rbl/.packlist
rm -f $RPM_BUILD_ROOT%{perl_vendorlib}/check_rbl.pod

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS Changes NEWS README INSTALL TODO VERSION
%attr(640,root,nagios) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{plugin}.cfg
%attr(640,root,nagios) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{plugin}.ini
%attr(755,root,root) %{plugindir}/%{plugin}
%{_mandir}/man1/check_rbl.1*
