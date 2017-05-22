#
# building:
# https://github.com/hashicorp/vault#developing-vault
#
# Conditional build:
%bcond_without	tests	# build without tests

Summary:	A tool for managing secrets
Name:		vault
Version:	0.7.2
Release:	1
License:	MPL-2.0
Group:		Applications/System
Source0:	https://github.com/hashicorp/vault/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	4756f2cc4c039627ff5740078a164108
URL:		https://vaultproject.io/
BuildRequires:	golang >= 1.6
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_enable_debug_packages 0
%define		gobuild(o:) go build -ldflags "${LDFLAGS:-} -B 0x$(head -c20 /dev/urandom|od -An -tx1|tr -d ' \\n')" -a -v -x %{?**};
%define		gopath		%{_libdir}/golang
%define		import_path	github.com/hashicorp/vault

%description
Vault is a tool for securely accessing secrets. A secret is anything
that you want to tightly control access to, such as API keys,
passwords, certificates, and more. Vault provides a unified interface
to any secret, while providing tight access control and recording a
detailed audit log.

%prep
%setup -q

install -d src/$(dirname %{import_path})
ln -s ../../.. src/%{import_path}

%build
export GOPATH=$(pwd)

base=%{import_path}/version
LDFLAGS="-X $base.Version=%{version} -X $base.VersionPrerelease=%{release}"
%gobuild -o bin/%{name}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_bindir}
install -p bin/%{name} $RPM_BUILD_ROOT%{_bindir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.md
%attr(755,root,root) %{_bindir}/vault
