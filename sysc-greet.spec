%global debug_package %{nil}

Name:		sysc-greet
Version:	1.1.8
Release:	1
Source0:	https://github.com/Nomadcxx/sysc-greet/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source1:	%{name}-%{version}-vendor.tar.xz
Summary:	A graphical console greeter for greetd
URL:		https://github.com/Nomadcxx/sysc-greet
License:	GPL-3.0-only
Group:		System/Management

BuildRequires:	golang

Requires:	greetd
Requires:	kitty
Requires:	(hyprland or niri or sway or cagebreak)
Recommends:	gslapper

%description
A graphical console greeter for greetd.
Written in Go with the Bubble Tea framework.

%prep
%autosetup -p1
tar -xf %{S:1}

%build
go build -o %{name} ./cmd/%{name}/

%install
## install binary
install -Dm755 %{name} %{buildroot}/usr/local/bin/%{name}

## install assets
mkdir -p %{buildroot}%{_datadir}/%{name}
cp -r ascii_configs %{buildroot}%{_datadir}/%{name}/
cp -r fonts %{buildroot}%{_datadir}/%{name}/
cp -r wallpapers %{buildroot}%{_datadir}/%{name}/

## install polkit rule to allow shutdown & reboot from greeter
install  -Dm644 config/85-greeter.rules %{buildroot}%{_sysconfdir}/polkit-1/rules.d/85-greeter.rules

## install greetd configs
mkdir -p %{buildroot}%{_sysconfdir}/greetd
cp config/kitty-greeter.conf %{buildroot}%{_sysconfdir}/greetd/
cp config/hyprland-greeter-config.conf %{buildroot}%{_sysconfdir}/greetd/
cp config/niri-greeter-config.kdl %{buildroot}%{_sysconfdir}/greetd/
cp config/sway-greeter-config %{buildroot}%{_sysconfdir}/greetd/
cp config/cagebreak-greeter-config %{buildroot}%{_sysconfdir}/greetd/

## create other necessary directories
mkdir -p %{buildroot}/var/lib/greeter/Pictures/wallpapers
mkdir -p %{buildroot}/var/cache/%{name}

%files
%license LICENSE
%doc docs docs-src
/usr/local/bin/%{name}
%{_datadir}/%{name}
%{_sysconfdir}/greetd
%{_sysconfdir}/polkit-1/rules.d/85-greeter.rules
%dir %attr(755, greeter, greeter) /var/lib/greeter
%dir %attr(755, greeter, greeter) /var/cache/%{name}
