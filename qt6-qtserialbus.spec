#define beta rc
#define snapshot 20200627
%define major 6

%define _qtdir %{_libdir}/qt%{major}

Name:		qt6-qtserialbus
Version:	6.5.0
Release:	%{?beta:0.%{beta}.1}%{?snapshot:0.%{snapshot}.}2
%if 0%{?snapshot:1}
# "git archive"-d from "dev" branch of git://code.qt.io/qt/qtbase.git
Source:		qtserialbus-%{?snapshot:%{snapshot}}%{!?snapshot:%{version}}.tar.zst
%else
Source:		http://download.qt-project.org/%{?beta:development}%{!?beta:official}_releases/qt/%(echo %{version}|cut -d. -f1-2)/%{version}%{?beta:-%{beta}}/submodules/qtserialbus-everywhere-src-%{version}%{?beta:-%{beta}}.tar.xz
%endif
Group:		System/Libraries
Summary:	Qt %{major} Serial Bus module
BuildRequires:	cmake
BuildRequires:	ninja
BuildRequires:	cmake(Qt%{major}Core)
BuildRequires:	cmake(Qt%{major}Network)
BuildRequires:	cmake(Qt%{major}SerialPort)
BuildRequires:	cmake(Qt%{major}Widgets)
BuildRequires:	qt%{major}-cmake
License:	LGPLv3/GPLv3/GPLv2

%description
Qt %{major} serial bus module

%global extra_files_SerialBus \
%{_qtdir}/bin/canbusutil \
%{_qtdir}/plugins/canbus

%qt6libs SerialBus

%package examples
Summary: Examples for the Qt %{major} Web Sockets module
Group: Development/KDE and Qt

%description examples
Examples for the Qt %{major} Web Sockets module

%files examples
%optional %{_qtdir}/examples/serialbus

%prep
%autosetup -p1 -n qtserialbus%{!?snapshot:-everywhere-src-%{version}%{?beta:-%{beta}}}
%cmake -G Ninja \
	-DCMAKE_INSTALL_PREFIX=%{_qtdir} \
	-DQT_BUILD_EXAMPLES:BOOL=ON \
	-DQT_WILL_INSTALL:BOOL=ON

%build
export LD_LIBRARY_PATH="$(pwd)/build/lib:${LD_LIBRARY_PATH}"
%ninja_build -C build

%install
%ninja_install -C build
%qt6_postinstall
