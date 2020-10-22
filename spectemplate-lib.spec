Name:           
Version:        
Release:        1%{?dist}
Summary:        

License:        
URL:            
Source0:        

BuildRequires:  
Requires:       

%description


%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q


%build
%configure --disable-static
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'


%{?ldconfig_scriptlets}


%files
%{!?_licensedir:%global license %%doc}
%license add-license-file-here
%doc add-main-docs-here
%{_libdir}/*.so.*

%files devel
%doc add-devel-docs-here
%{_includedir}/*
%{_libdir}/*.so


%changelog
