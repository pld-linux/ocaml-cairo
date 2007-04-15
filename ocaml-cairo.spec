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
Patch0:		%{name}-install.patch
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	cairo-devel >= 1.2.0
BuildRequires:	gtk+2-devel >= 2:2.8
BuildRequires:	libsvg-cairo-devel
BuildRequires:	ocaml >= 3.04-7
BuildRequires:	ocaml-lablgtk2-devel
%requires_eq	ocaml-runtime
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This package contains files needed to run OCaml bytecode executables
using Cairo library.

%description -l pl.UTF-8
Pakiet ten zawiera binaria potrzebne do uruchamiania programów w
OCamlu używających biblioteki Cairo.

%package devel
Summary:	Cairo binding for OCaml - development part
Summary(pl.UTF-8):	Wiązania Cairo dla OCamla - cześć programistyczna
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
%requires_eq	ocaml

%description devel
This package contains files needed to develop OCaml programs using
Cairo library.

%description devel -l pl.UTF-8
Pakiet ten zawiera pliki niezbędne do tworzenia programów używających
biblioteki Cairo.

%prep
%setup -q -n cairo-ocaml
%patch0 -p1

%build
%{__aclocal} -I support
%{__autoconf}
%configure

%{__make} -j1 CC="%{__cc} %{rpmcflags} -fPIC" all opt
%{__make} -j1 doc

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

cp -r test/{Makefile,*.ml} $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

install -d $RPM_BUILD_ROOT%{_libdir}/ocaml/site-lib/cairo
cat > $RPM_BUILD_ROOT%{_libdir}/ocaml/site-lib/cairo/META <<EOF
requires = ""
version = "%{version}"
directory = "+cairo"
archive(byte) = "cairo.cma"
archive(native) = "cairo.cmxa"
linkopts = ""
EOF

install -d $RPM_BUILD_ROOT%{_libdir}/ocaml/site-lib/cairo-lablgtk
cat > $RPM_BUILD_ROOT%{_libdir}/ocaml/site-lib/cairo-lablgtk/META <<EOF
requires = "cairo lablgtk2"
version = "%{version}"
directory = "+cairo"
archive(byte) = "cairo_lablgtk.cma"
archive(native) = "cairo_lablgtk.cmxa"
linkopts = ""
EOF

install -d $RPM_BUILD_ROOT%{_libdir}/ocaml/site-lib/svgcairo
cat > $RPM_BUILD_ROOT%{_libdir}/ocaml/site-lib/svgcairo/META <<EOF
requires = "cairo"
version = "%{version}"
directory = "+cairo"
archive(byte) = "svg_cairo.cma"
archive(native) = "svg_cairo.cmxa"
linkopts = ""
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/ocaml/stublibs/*.so

%files devel
%defattr(644,root,root,755)
%doc README doc/html src/*.mli
%dir %{_libdir}/ocaml/cairo
%{_libdir}/ocaml/cairo/*.cm[ixa]*
%{_libdir}/ocaml/cairo/*.a
%{_examplesdir}/%{name}-%{version}
%{_libdir}/ocaml/site-lib/*cairo*
