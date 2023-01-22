Name:           
Version:        
Release:        1%{?dist}
Summary:        

License:        
URL:            
Source0:        

BuildRequires:  cmake

%description
%{summary}.


%prep
%autosetup -q


%build
%cmake
%cmake_build


%install
%cmake_install


%check
%ctest


%files
%license add-license-file-here
%doc add-docs-here


%changelog
