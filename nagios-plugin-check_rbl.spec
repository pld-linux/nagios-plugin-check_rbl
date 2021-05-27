#
# Conditional build:
%bcond_without	tests	# do not perform "make test"

%define		plugin	check_rbl
Summary:	Nagios plugin to check if an server is blacklisted in RBL servers
Name:		nagios-plugin-%{plugin}
Version:	1.5.7
Release:	1
License:	GPL v3
Group:		Networking
Source0:	https://github.com/matteocorti/check_rbl/releases/download/v%{version}/%{plugin}-%{version}.tar.gz
# Source0-md5:	601b72ef3c63e5343a4eef84ed174590
Source1:	%{plugin}.cfg
Source2:	%{plugin}.ini
URL:		https://github.com/matteocorti/check_rbl/wiki
BuildRequires:	perl-ExtUtils-MakeMaker >= 6.42
BuildRequires:	rpm-perlprov >= 4.1-13
BuildRequires:	sed >= 4.0
%if %{with tests}
BuildRequires:	perl-Data-Validate-Domain
BuildRequires:	perl-Data-Validate-IP
BuildRequires:	perl-Nagios-Plugin >= 0.31
BuildRequires:	perl-Net-DNS
BuildRequires:	perl-Readonly
%endif
Requires:	nagios-common
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir	/etc/nagios/plugins
%define		plugindir	%{_prefix}/lib/nagios/plugins

%description
Nagios plugin to check if an server is blacklisted in RBL servers.

%prep
%setup -q -n %{plugin}-%{version}

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
cp -p %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/%{plugin}.cfg
cp -p %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/%{plugin}.ini

%{__rm} $RPM_BUILD_ROOT%{perl_archlib}/perllocal.pod
%{__rm} $RPM_BUILD_ROOT%{perl_vendorarch}/auto/check_rbl/.packlist
%{__rm} $RPM_BUILD_ROOT%{perl_vendorlib}/check_rbl.pod

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS Changes NEWS README.md INSTALL TODO VERSION
%attr(640,root,nagios) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{plugin}.cfg
%attr(640,root,nagios) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{plugin}.ini
%attr(755,root,root) %{plugindir}/%{plugin}
%{_mandir}/man1/check_rbl.1*
