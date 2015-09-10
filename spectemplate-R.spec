%define packname %(echo %{name} | sed -e 's/^R-//')
%global packrel 1
# Pick one of these (_datadir for noarch, _libdir for others), remove the other
%global rlibdir %{_datadir}/R/library
%global rlibdir %{_libdir}/R/library

Name:           
Version:        
Release:        1%{?dist}
Summary:        

Group:          Applications/Engineering
License:        
URL:            http://cran.r-project.org/web/packages/%{packname}/
Source0:        ftp://cran.r-project.org/pub/R/contrib/main/%{packname}_%{version}-%{packrel}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      
BuildRequires:  R-devel
BuildRequires:  tex(latex)
Requires(post): R-core
Requires(postun): R-core
# Remove this from non-noarch packages
Requires:       R-core

%description


%prep
%setup -q -c -n %{packname}


%build


%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{rlibdir}
%{_bindir}/R CMD INSTALL -l $RPM_BUILD_ROOT%{rlibdir} %{packname}
test -d %{packname}/src && (cd %{packname}/src; rm -f *.o *.so)
rm -f $RPM_BUILD_ROOT%{rlibdir}/R.css


%check
%{_bindir}/R CMD check %{packname}


%clean
rm -rf $RPM_BUILD_ROOT


%files
%{!?_licensedir:%global license %%doc}
%license add-license-file-here
%dir %{rlibdir}/%{packname}
%doc %{rlibdir}/%{packname}/doc
%doc %{rlibdir}/%{packname}/html
%doc %{rlibdir}/%{packname}/DESCRIPTION
%doc %{rlibdir}/%{packname}/NEWS
%{rlibdir}/%{packname}/INDEX
%{rlibdir}/%{packname}/NAMESPACE
%{rlibdir}/%{packname}/Meta
%{rlibdir}/%{packname}/R
%{rlibdir}/%{packname}/R-ex
%{rlibdir}/%{packname}/help


%changelog
