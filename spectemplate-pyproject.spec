Name:           python-...
Version:        ...
Release:        1%{?dist}
Summary:        ...

License:        ...
URL:            https://...
# use a source from git forge or PyPI:
Source:         %{url}/archive/v%{version}/...-%{version}.tar.gz / %{pypi_source ...}

# for pure Python packages:
BuildArch:      noarch
# for packages with extension modules:
BuildRequires:  gcc

BuildRequires:  python3-devel

%global _description %{expand:
...}

%description %_description

%package -n python3-...
Summary:        %{summary}

%description -n python3-... %_description


%prep
%autosetup -p1 -n ...-%{version}


%generate_buildrequires
# use the appropriate flags to get all test dependencies:
%pyproject_buildrequires -x... / -t


%build
%pyproject_wheel


%install
%pyproject_install
# list the installed top-level Python module names:
%pyproject_save_files ...


%check
# testing the package is mandatory, at least somehow:
%tox / %pytest / %pyproject_check_import ...


%files -n python3-... -f %{pyproject_files}
%doc README.*
# only add LICENSE / COPYING if not included in %%{pyproject_files}
%license LICENSE / COPYING
%{_bindir}/...


%changelog
