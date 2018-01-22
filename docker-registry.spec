%define debug_package %{nil}
%define go_path %{_builddir}/go
%define go_package github.com/docker/distribution
%define go_package_src %{go_path}/src/%{go_package}

Name:           docker-registry
Version:        2.6.2
Release:        1%{?dist}
Summary:        Docker Registry

Group:          Application/Internet
License:        ASL 2.0
URL:            https://docs.docker.com/registry/
Source0:        https://%{go_package}/archive/v%{version}/distribution-%{version}.tar.gz
Source1:        %{name}.service

BuildRequires:  golang git make
BuildRequires:  systemd-units
Requires:       systemd
Requires(pre):  shadow-utils

%description
Docker Registry stores and distributes images centrally. It's where you push 
images to and pull them from; Docker Registry gives team members the ability to 
share images and deploy them to testing, staging and production environments.

%prep
%setup -q -n distribution-%{version}
mkdir -p %{go_package_src}
cp -R * %{go_package_src}/.

%build
export GOPATH=%{go_path}
export PATH=${GOPATH}/bin:${PATH}
go get github.com/tools/godep github.com/golang/lint/golint
cd %{go_package_src}
GOPATH=${GOPATH} make PREFIX=%{go_path} VERSION=%{version} binaries

%install
install -D %{go_path}/bin/registry %{buildroot}/%{_bindir}/%{name}

install -d %{buildroot}/%{_sysconfdir}
install cmd/registry/config-dev.yml %{buildroot}/%{_sysconfdir}/%{name}.yml

install -d %{buildroot}/%{_unitdir}
install %{SOURCE1} %{buildroot}/%{_unitdir}

%pre
getent group %{name} >/dev/null \
    || groupadd -r %{name}
getent passwd %{name} >/dev/null \
    || useradd -r -g %{name} -M -s /sbin/nologin \
    -c "%{name} user" %{name}
install -d -m 750 -o %{name} -g %{name} /var/log/%{name}
exit 0

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service
userdel %{name}

%postun
%systemd_postun_with_restart %{name}.service

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%attr(755, root, root) %{_sysconfdir}/%{name}.yml
%attr(644, root, root) %{_unitdir}/%{name}.service
%attr(755, root, root) %{_bindir}/%{name}

%doc AUTHORS LICENSE MAINTAINERS README.md

%changelog
* Thu Jun 11 2015 Arun Babu Neelicattu <arun.neelicattu@gmail.com> - 2.0.1-1
- Initial release

