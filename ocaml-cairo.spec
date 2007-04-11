Summary:	Cairo binding for OCaml
Summary(pl.UTF-8):	Wiązania Cairo dla OCamla
Name:		ocaml-cairo
Version:	1.2.0
%define	_snap 20070411
Release:	0.%{_snap}.1
License:	LGPL
Group:		Libraries
# cvs -d:pserver:anonymous@cvs.cairographics.org:/cvs/cairo co cairo-ocam
Source0:	%{name}-%{version}-%{_snap}.tar.gz
# Source0-md5:	ba63548f5e2eaa5e9f082e737571c2b3
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	cairo-devel >= 1.2.0
BuildRequires:	gtk+2-devel >= 2.8
BuildRequires:	ocaml >= 3.04-7
%requires_eq	ocaml-runtime
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This package contains files needed to run bytecode executables using
this library.

%description -l pl.UTF-8
Pakiet ten zawiera binaria potrzebne do uruchamiania programów
używających tej biblioteki.

%package devel
Summary:	Cairo binding for OCaml - development part
Summary(pl.UTF-8):	Wiązania Cairo dla OCamla - cześć programistyczna
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
%requires_eq	ocaml

%description devel
This package contains files needed to develop OCaml programs using
this library.

%description devel -l pl.UTF-8
Pakiet ten zawiera pliki niezbędne do tworzenia programów używających
tej biblioteki.

%prep
%setup -q -n cairo-ocaml

%build
%{__aclocal} -I support
%{__autoconf}
%configure
%{__make}
%{__make} CC="%{__cc} %{rpmcflags} -fPIC" all opt

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_libdir}/ocaml/{template,stublibs}
install *.cm[ixa]* *.a dll*.so $RPM_BUILD_ROOT%{_libdir}/ocaml/template
install dll*.so $RPM_BUILD_ROOT%{_libdir}/ocaml/stublibs

install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
cp -r foo bar $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

install -d $RPM_BUILD_ROOT%{_libdir}/ocaml/site-lib/template
cat > $RPM_BUILD_ROOT%{_libdir}/ocaml/site-lib/template/META <<EOF
requires = ""
version = "%{version}"
directory = "+template"
archive(byte) = "template.cma"
archive(native) = "template.cmxa"
linkopts = ""
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/ocaml/stublibs/*.so

%files devel
%defattr(644,root,root,755)
%doc LICENSE *.mli
%dir %{_libdir}/ocaml/template
%{_libdir}/ocaml/template/*.cm[ixa]*
%{_libdir}/ocaml/template/*.a
%{_examplesdir}/%{name}-%{version}
%{_libdir}/ocaml/site-lib/template
