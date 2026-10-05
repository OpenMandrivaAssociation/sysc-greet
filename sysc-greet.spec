%global debug_package %{nil}

Name:		sysc-greet
Version:	1.1.11
Release:	1
Source0:	https://github.com/Nomadcxx/sysc-greet/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
### Source1 vendor instructions ###
# from within source tree run the following:
# go mod vendor
# tar -cJvf sysc-greet-1.1.9-vendor.tar.xz vendor
# place the vendor archive alongside the source archive
Source1:	%{name}-%{version}-vendor.tar.xz
Summary:	A graphical console greeter for greetd
URL:		https://github.com/Nomadcxx/sysc-greet
License:	GPL-3.0-only
Group:		System/Management

BuildRequires:	golang

%description
A graphical console greeter for greetd.
Written in Go with the Bubble Tea framework.

###  Niri compositor
%package niri
Requires:	greetd
Requires:	kitty
Requires:	niri
Recommends:	gslapper
Conflicts:	sysc-greet-sway
Conflicts:	sysc-greet-cagebreak
Conflicts:	sysc-greet
Summary:	Graphical console greeter for greetd (niri compositor)

%description niri
Graphical console greeter for greetd with ASCII art and themes (niri compositor)

%files niri
%license LICENSE
%doc docs-site/content/docs
/usr/local/bin/%{name}
%{_datadir}/%{name}
%{_sysconfdir}/greetd/kitty*
%{_sysconfdir}/greetd/niri*
%{_sysconfdir}/polkit-1/rules.d/85-greeter.rules
%dir %attr(755, greeter, greeter) /var/lib/greeter
%dir %attr(755, greeter, greeter) /var/cache/%{name}

###  Sway compositor
%package sway
Requires:	greetd
Requires:	kitty
Requires:	sway
Recommends:	gslapper
Conflicts:	sysc-greet-niri
Conflicts:	sysc-greet-cagebreak
Conflicts:	sysc-greet
Summary:	Graphical console greeter for greetd (sway compositor)

%description sway
Graphical console greeter for greetd with ASCII art and themes (sway compositor)

%files sway
%license LICENSE
%doc docs-site/content/docs
/usr/local/bin/%{name}
%{_datadir}/%{name}
%{_sysconfdir}/greetd/kitty*
%{_sysconfdir}/greetd/sway*
%{_sysconfdir}/polkit-1/rules.d/85-greeter.rules
%dir %attr(755, greeter, greeter) /var/lib/greeter
%dir %attr(755, greeter, greeter) /var/cache/%{name}

### Cagebreak compositor
%package cagebreak
Requires:	greetd
Requires:	kitty
Requires:	cagebreak
Recommends:	gslapper
Conflicts:	sysc-greet-niri
Conflicts:	sysc-greet-sway
Conflicts:	sysc-greet
Summary:	Graphical console greeter for greetd (cagebreak compositor)

%description cagebreak
Graphical console greeter for greetd with ASCII art and themes (cagebreak compositor)

%files cagebreak
%license LICENSE
%doc docs-site/content/docs
/usr/local/bin/%{name}
%{_datadir}/%{name}
%{_sysconfdir}/greetd/kitty*
%{_sysconfdir}/greetd/cagebreak*
%{_sysconfdir}/polkit-1/rules.d/85-greeter.rules
%dir %attr(755, greeter, greeter) /var/lib/greeter
%dir %attr(755, greeter, greeter) /var/cache/%{name}

###  Mangowm compositor (not yet packaged)
#package mangowm

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
#cp config/mango-greeter-config.conf %{buildroot}%{_sysconfdir}/greetd/
#cp config/mango-greeter-session.sh %{buildroot}%{_sysconfdir}/greetd/
cp config/niri-greeter-config.kdl %{buildroot}%{_sysconfdir}/greetd/
cp config/sway-greeter-config %{buildroot}%{_sysconfdir}/greetd/
cp config/cagebreak-greeter-config %{buildroot}%{_sysconfdir}/greetd/

## create other necessary directories
mkdir -p %{buildroot}/var/lib/greeter/Pictures/wallpapers
mkdir -p %{buildroot}/var/cache/%{name}

