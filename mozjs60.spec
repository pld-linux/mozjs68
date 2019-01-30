#
# Conditional build:
%bcond_without	tests	# tests build

Summary:	SpiderMonkey 60 - JavaScript implementation
Summary(pl.UTF-8):	SpiderMonkey 60 - implementacja języka JavaScript
Name:		mozjs60
Version:	60.1.0
Release:	1
License:	MPL v2.0
Group:		Libraries
Source0:	http://ftp.gnome.org/pub/gnome/teams/releng/tarballs-needing-help/mozjs/mozjs-%{version}.tar.bz2
# Source0-md5:	202f71313e53d9b92e7c578107541539
Patch0:		copy-headers.patch
Patch1:		system-virtualenv.patch
Patch2:		include-configure-script.patch
URL:		https://developer.mozilla.org/en-US/docs/Mozilla/Projects/SpiderMonkey
BuildRequires:	autoconf2_13 >= 2.13
# "TestWrappingOperations.cpp:27:1: error: non-constant condition for static assertion" with -fwrapv on gcc 6
%{?with_tests:BuildRequires:	gcc-c++ >= 6:7}
BuildRequires:	libicu-devel >= 59.1
BuildRequires:	libstdc++-devel >= 6:4.4
BuildRequires:	nspr-devel >= 4.9.2
BuildRequires:	perl-base >= 1:5.6
BuildRequires:	pkgconfig
BuildRequires:	python >= 1:2.5
BuildRequires:	python-virtualenv >= 1.9.1-4
BuildRequires:	readline-devel
BuildRequires:	rpm-perlprov
BuildRequires:	rpmbuild(macros) >= 1.294
BuildRequires:	zlib-devel >= 1.2.3
Requires:	nspr >= 4.9.2
Requires:	zlib >= 1.2.3
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
JavaScript Reference Implementation (codename SpiderMonkey). The
package contains JavaScript runtime (compiler, interpreter,
decompiler, garbage collector, atom manager, standard classes) and
small "shell" program that can be used interactively and with .js
files to run scripts.

%description -l pl.UTF-8
Wzorcowa implementacja JavaScriptu (o nazwie kodowej SpiderMonkey).
Pakiet zawiera środowisko uruchomieniowe (kompilator, interpreter,
dekompilator, odśmiecacz, standardowe klasy) i niewielką powłokę,
która może być używana interaktywnie lub z plikami .js do uruchamiania
skryptów.

%package devel
Summary:	Header files for JavaScript reference library
Summary(pl.UTF-8):	Pliki nagłówkowe do biblioteki JavaScript
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	libstdc++-devel
Requires:	nspr-devel >= 4.9.2

%description devel
Header files for JavaScript reference library.

%description devel -l pl.UTF-8
Pliki nagłówkowe do biblioteki JavaScript.

%prep
%setup -q -n mozjs-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
export PYTHON="%{__python}"
export AUTOCONF="%{_bindir}/autoconf2_13"
export SHELL="/bin/sh"
cd js/src
mkdir obj
cd obj

%define configuredir ".."
%configure2_13 \
	--enable-gcgenerational \
	--disable-jemalloc \
	--enable-readline \
	--enable-shared-js \
	%{!?with_tests:--disable-tests} \
	--enable-threadsafe \
	--with-intl-api \
	--with-system-icu \
	--with-system-nspr \
	--with-system-zlib

%{__make} \
	HOST_OPTIMIZE_FLAGS= \
	MODULE_OPTIMIZE_FLAGS= \
	MOZ_OPTIMIZE_FLAGS="-freorder-blocks" \
	MOZ_PGO_OPTIMIZE_FLAGS= \
	MOZILLA_VERSION=%{version}

%install
rm -rf $RPM_BUILD_ROOT

cd js/src/obj

%{__make} -C js/src install \
    DESTDIR=$RPM_BUILD_ROOT \
    MOZILLA_VERSION=%{version}

%{__rm} $RPM_BUILD_ROOT%{_libdir}/*.ajs

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc js/src/README.html
%attr(755,root,root) %{_bindir}/js60
%attr(755,root,root) %{_libdir}/libmozjs-60.so

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/js60-config
%{_includedir}/mozjs-60
%{_pkgconfigdir}/mozjs-60.pc
