#
# Conditional build:
%bcond_without	ocaml_opt	# native optimized binaries (bytecode is always built)

# not yet available on x32 (ocaml 4.02.1), update when upstream will support it
%ifnarch %{ix86} %{x8664} %{arm} aarch64 ppc sparc sparcv9
%undefine	with_ocaml_opt
%endif

Summary:	Cairo binding for OCaml
Summary(pl.UTF-8):	Wiązania Cairo dla OCamla
Name:		ocaml-cairo
Version:	1.2.0
Release:	11
License:	LGPL v2.1
Group:		Libraries
#Source0Download: http://cgit.freedesktop.org/cairo-ocaml/
Source0:	http://cgit.freedesktop.org/cairo-ocaml/snapshot/cairo-ocaml-%{version}.tar.bz2
# Source0-md5:	5d0096328f210a6ed032fec68e1bc141
Patch0:		%{name}-install.patch
# https://gitweb.gentoo.org/repo/gentoo.git/plain/dev-ml/cairo-ocaml/files/ocaml406.patch?id=05cb735234f0cb37b593d8cabf893bc4a8452cde
Patch1:		%{name}-ocaml406.patch
URL:		http://cairographics.org/cairo-ocaml/
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake
BuildRequires:	cairo-devel >= 1.2.0
BuildRequires:	freetype-devel >= 2.0
BuildRequires:	gtk+2-devel >= 2:2.8
BuildRequires:	libsvg-cairo-devel
BuildRequires:	ocaml >= 3.04-7
BuildRequires:	ocaml-lablgtk2-devel
BuildRequires:	pkgconfig
%requires_eq	ocaml-runtime
Requires:	cairo >= 1.2.0
Requires:	ocaml-lablgtk2
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
%setup -q -n cairo-ocaml-%{version}
%patch0 -p1
%patch1 -p1

%build
%{__aclocal} -I support
%{__autoconf}
%configure

%{!?with_ocaml_opt:%{__sed} -i -e 's/OCAMLOPT .*=.*/OCAMLOPT=/' config.make}

%{__make} -j1 CC="%{__cc} %{rpmcflags} -fPIC" all
%{__make} -j1 doc

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

cp -r test/{Makefile,*.ml} $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

cat > $RPM_BUILD_ROOT%{_libdir}/ocaml/cairo/META <<EOF
requires = "bigarray"
version = "%{version}"
directory = "+cairo"
archive(byte) = "cairo.cma"
archive(native) = "cairo.cmxa"
linkopts = ""

package "lablgtk2" (
	requires = "cairo lablgtk2"
	archive(byte) = "cairo_lablgtk.cma"
	archive(native) = "cairo_lablgtk.cmxa"
)
EOF

# some distros include lablgtk2 subpackage for cairo, we used to provide cairo-lablgtk package
install -d $RPM_BUILD_ROOT%{_libdir}/ocaml/cairo-lablgtk
cat > $RPM_BUILD_ROOT%{_libdir}/ocaml/cairo-lablgtk/META <<EOF
requires = "cairo lablgtk2"
version = "%{version}"
directory = "+cairo"
archive(byte) = "cairo_lablgtk.cma"
archive(native) = "cairo_lablgtk.cmxa"
linkopts = ""
EOF

install -d $RPM_BUILD_ROOT%{_libdir}/ocaml/pangocairo
cat > $RPM_BUILD_ROOT%{_libdir}/ocaml/pangocairo/META <<EOF
requires = "cairo lablgtk2"
version = "%{version}"
directory = "+cairo"
archive(byte) = "pango_cairo.cma"
archive(native) = "pango_cairo.cmxa"
linkopts = ""
EOF

install -d $RPM_BUILD_ROOT%{_libdir}/ocaml/svgcairo
cat > $RPM_BUILD_ROOT%{_libdir}/ocaml/svgcairo/META <<EOF
requires = "cairo"
version = "%{version}"
directory = "+cairo"
archive(byte) = "svg_cairo.cma"
archive(native) = "svg_cairo.cmxa"
linkopts = ""
EOF

%{__rm} $RPM_BUILD_ROOT%{_libdir}/ocaml/cairo/*.mli

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc ChangeLog README
%dir %{_libdir}/ocaml/cairo
%{_libdir}/ocaml/cairo/META
%{_libdir}/ocaml/cairo/*.cma
%dir %{_libdir}/ocaml/cairo-lablgtk
%{_libdir}/ocaml/cairo-lablgtk/META
%dir %{_libdir}/ocaml/pangocairo
%{_libdir}/ocaml/pangocairo/META
%dir %{_libdir}/ocaml/svgcairo
%{_libdir}/ocaml/svgcairo/META
%attr(755,root,root) %{_libdir}/ocaml/stublibs/dllmlcairo.so
%attr(755,root,root) %{_libdir}/ocaml/stublibs/dllmlcairo_lablgtk.so
%attr(755,root,root) %{_libdir}/ocaml/stublibs/dllmlpangocairo.so
%attr(755,root,root) %{_libdir}/ocaml/stublibs/dllmlsvgcairo.so

%files devel
%defattr(644,root,root,755)
%doc doc/html src/*.mli
%{_libdir}/ocaml/cairo/*.cmi
%if %{with ocaml_opt}
%{_libdir}/ocaml/cairo/*.cmx
%{_libdir}/ocaml/cairo/*.cmxa
%{_libdir}/ocaml/cairo/cairo.a
%{_libdir}/ocaml/cairo/cairo_lablgtk.a
%{_libdir}/ocaml/cairo/pango_cairo.a
%{_libdir}/ocaml/cairo/svg_cairo.a
%endif
%{_libdir}/ocaml/cairo/libmlcairo.a
%{_libdir}/ocaml/cairo/libmlcairo_lablgtk.a
%{_libdir}/ocaml/cairo/libmlpangocairo.a
%{_libdir}/ocaml/cairo/libmlsvgcairo.a
%{_examplesdir}/%{name}-%{version}
