Name:           gdb
Version:        7.5
Release:        0
License:        GPL-3.0+
Summary:        A GNU source-level debugger for C, C++, Java and other languages
Url:            http://gnu.org/software/gdb/
Group:          Development/Debuggers
Source:         ftp://ftp.gnu.org/gnu/gdb/gdb-%{version}.tar.bz2
Source1001: 	gdb.manifest
%define gdb_src gdb-%{version}
%define gdb_build build-%{_target_platform}

BuildRequires:  bison
BuildRequires:  expat-devel
BuildRequires:  flex
BuildRequires:  gettext
BuildRequires: 	python-devel
BuildRequires:  gcc-c++
BuildRequires:  ncurses-devel
BuildRequires:  readline-devel
BuildRequires:  rpm-devel
BuildRequires:  makeinfo

%description
GDB, the GNU debugger, allows you to debug programs written in C, C++,
Java, and other languages, by executing them in a controlled fashion
and printing their data.

%package devel
Summary:        Development files for gdb
Group:          Development

%description devel
Development files for gdb.

%package server
Summary:        A standalone server for GDB (the GNU source-level debugger)
Group:          Development/Debuggers

%description server
GDB, the GNU debugger, allows you to debug programs written in C, C++,
Java, and other languages, by executing them in a controlled fashion
and printing their data.

This package provides a program that allows you to run GDB on a different machine than the one which is running the program being debugged.

%prep
%setup -q 
cp %{SOURCE1001} .

# Files have `# <number> <file>' statements breaking VPATH / find-debuginfo.sh .
#rm -f gdb/ada-exp.c gdb/ada-lex.c gdb/c-exp.c gdb/cp-name-parser.c gdb/f-exp.c
#rm -f gdb/jv-exp.c gdb/m2-exp.c gdb/objc-exp.c gdb/p-exp.c

# Remove the info and other generated files added by the FSF release
# process.
rm -f libdecnumber/gstdint.h
rm -f bfd/doc/*.info
rm -f bfd/doc/*.info-*
rm -f gdb/doc/*.info
rm -f gdb/doc/*.info-*

%build
%configure						\
	--with-gdb-datadir=%{_datadir}/gdb		\
	--enable-gdb-build-warnings=,-Wno-unused	\
	--disable-werror				\
	--with-separate-debug-dir=/usr/lib/debug	\
	--disable-sim					\
	--disable-rpath					\
	--with-system-readline				\
	--with-expat					\
	--disable-tui					\
	--enable-64-bit-bfd				\
	--enable-static --disable-shared --enable-debug	\
	%{_target_platform}

make %{?_smp_mflags}


%install
%make_install

%find_lang opcodes
%find_lang bfd
mv opcodes.lang %{name}.lang
cat bfd.lang >> %{name}.lang

%docs_package

%lang_package
%files
%manifest %{name}.manifest
%defattr(-,root,root)
%doc COPYING COPYING.LIB 
%{_bindir}/*
%{_datadir}/gdb

%files server
%manifest %{name}.manifest
%defattr(-,root,root)
%{_bindir}/gdbserver
%{_mandir}/*/gdbserver.1*
%ifarch %{ix86} x86_64
%{_libdir}/libinproctrace.so
%endif

%files devel
%manifest %{name}.manifest
%{_includedir}/*.h
%{_includedir}/gdb/*.h
