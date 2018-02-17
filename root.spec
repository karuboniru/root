%global py3soabi %(%{__python3} -c "from distutils import sysconfig; print(sysconfig.get_config_vars().get('SOABI'))" | sed -e 's/None//' -e 's/^..*$/\.&/')

# Ruby support not yet ported to root version 6
%global ruby 0

%global oce 1
%global pythia8 1
%global xrootd 1

%if %{?fedora}%{!?fedora:0} >= 24
# libhdfs is available for all architectures for Fedora 24 and later.
# For Fedora 20-23 it was only available on Intel (ix86 and x86_64).
%global hadoop 1
%else
%global hadoop 0
%endif

%if %{?fedora}%{!?fedora:0} >= 24 || %{?rhel}%{!?rhel:0} >= 8
# Building the experimental ROOT 7 classes requires c++-14.
# This is the default for gcc 6.1 and later.
%global root7 1
%else
%global root7 0
%endif

# Do not create .orig files when patching source
%global _default_patch_flags --no-backup-if-mismatch

# Do not generate autoprovides for libJupyROOT.so
# Note: the ones from libPyROOT.so we do want though
%global __provides_exclude_from ^(%{python2_sitearch}|%{python3_sitearch})/libJupyROOT\\.so$

Name:		root
Version:	6.12.04
%global libversion %(cut -d. -f 1-2 <<< %{version})
Release:	4%{?dist}
Summary:	Numerical data analysis framework

License:	LGPLv2+
URL:		https://root.cern.ch/
#		The upstream source is modified to exclude proprietary fonts:
#		wget -N https://root.cern.ch/download/root_v%{version}.source.tar.gz
#		tar -z -x -f root_v%{version}.source.tar.gz
#		find root-%{version}/fonts -type f -a '!' '(' -name 'STIX*' -o -name DroidSansFallback.ttf ')' -exec rm {} ';'
#		tar -J -c --group root --owner root -f root-%{version}.tar.xz root-%{version}
Source0:	%{name}-%{version}.tar.xz
#		Input data for the tests
Source1:	%{name}-testfiles.tar.xz
#		Script to generate above source
Source2:	%{name}-testfiles.sh
#		systemd unit files
Source3:	rootd.service
Source4:	proofd.service
#		Use system fonts
Patch0:		%{name}-fontconfig.patch
#		Don't link to libjvm (handled properly inside libhdfs)
Patch1:		%{name}-dont-link-jvm.patch
#		Don't create documentation notebooks
Patch2:		%{name}-doc-no-notebooks.patch
#		Don't run gui macros
Patch3:		%{name}-avoid-gui-crash.patch
#		Unbundle gtest
Patch4:		%{name}-unbundle-gtest.patch
#		Horrible hack for broken charmaps in StandardSymbolsPS.otf
#		Hopefully temporary...
#		https://bugzilla.redhat.com/show_bug.cgi?id=1534206
Patch5:		%{name}-urw-otf-hack.patch
#		Use local static script and style files for JupyROOT
Patch6:		%{name}-jupyroot-static.patch
#		Fix some javascript syntax choking yuicompressor
#		Adapt d3 path to updated jsroot
#		https://github.com/root-project/root/pull/1520
Patch7:		%{name}-js-syntax.patch
#		Fix missing -f flag to rm in Makefile
#		Backport from upstream git
Patch8:		%{name}-doxygen-makefile.patch
#		Always use ROOT_ADD_TEST_SUBDIRECTORY when adding test dirs
#		https://github.com/root-project/root/pull/1515
Patch9:		%{name}-test-subdirs.patch
#		No need to use environment variables for system pythia
Patch10:	%{name}-system-pythia.patch
#		Reduce memory usage of build
#		https://github.com/root-project/root/pull/1516
Patch11:	%{name}-memory-usage.patch
#		Fedora's llvm patch
Patch12:	%{name}-PowerPC-Don-t-use-xscvdpspn-on-the-P7.patch
#		Reduce memory usage during linking on ARM by generating
#		smaller debuginfo for the llmv libraries.
#		Fedora builders run out of memory with the default setting.
Patch13:	%{name}-memory-arm.patch
#		Don't run tutorials that crash on ppc64 during doc generation.
#		Ensures content of doc package is the same on all architecture
#		so that koji accepts it as a noarch package.
Patch14:	%{name}-ppc64-doc.patch
#		Fix constructing the GSL MC Integrator
#		Backport from upstream git
Patch15:	%{name}-Fix-constructing-the-GSL-MC-Integrator.patch
#		Check string is not empty before calling front()
#		Backport from upstream git
Patch16:	%{name}-crash-fix.patch
#		Adjust expected file size for ix32
#		Backport from upstream git
Patch17:	%{name}-test-stress-32bit.patch
#		Fixes for failing tests due to new compiler flags
#		https://github.com/root-project/root/pull/1638
Patch18:	%{name}-test-fixes.patch
#		https://github.com/root-project/root/pull/1639
Patch19:	%{name}-out-of-bounds.patch
#		Fix ~ alignment in doxygen markup
#		https://github.com/root-project/root/pull/1640
Patch20:	%{name}-doxygen-tilde.patch
#		Don't install intermediate static libs (mathtext and minicern)
#		Don't add JupyROOT python extension to cmake exports
#		https://github.com/root-project/root/pull/1643
Patch21:	%{name}-noinst.patch

#		s390x suffers from endian issues resulting in failing tests
#		and broken documentation generation
#		https://sft.its.cern.ch/jira/browse/ROOT-8703
ExcludeArch:	s390x

%if %{?fedora}%{!?fedora:0} || %{?rhel}%{!?rhel:0} >= 8
BuildRequires:	cmake >= 3.4.3
%else
BuildRequires:	cmake3 >= 3.4.3
%endif
BuildRequires:	libX11-devel
BuildRequires:	libXpm-devel
BuildRequires:	libXft-devel
BuildRequires:	libXext-devel
BuildRequires:	fontconfig-devel
BuildRequires:	freetype-devel
BuildRequires:	fcgi-devel
BuildRequires:	ftgl-devel
BuildRequires:	glew-devel
BuildRequires:	gl2ps-devel
BuildRequires:	pcre-devel
BuildRequires:	zlib-devel
BuildRequires:	xz-devel
BuildRequires:	lz4-devel
BuildRequires:	xxhash-devel
BuildRequires:	libAfterImage-devel >= 1.20
BuildRequires:	ncurses-devel
BuildRequires:	avahi-compat-libdns_sd-devel
BuildRequires:	avahi-devel
BuildRequires:	libxml2-devel
BuildRequires:	fftw-devel
BuildRequires:	gsl-devel
BuildRequires:	unuran-devel
BuildRequires:	krb5-devel
BuildRequires:	krb5-workstation
BuildRequires:	openldap-devel
%if %{?fedora}%{!?fedora:0} >= 28 || %{?rhel}%{!?rhel:0} >= 8
BuildRequires:	mariadb-connector-c-devel
%else
BuildRequires:	mysql-devel
%endif
BuildRequires:	sqlite-devel
BuildRequires:	unixODBC-devel
BuildRequires:	mesa-libGL-devel
BuildRequires:	mesa-libGLU-devel
BuildRequires:	postgresql-devel
BuildRequires:	python-devel
%if %{?fedora}%{!?fedora:0} >= 15
BuildRequires:	python3-devel
%endif
%if %{?rhel}%{!?rhel:0} == 7
BuildRequires:	python34-devel
%endif
BuildRequires:	qt4-devel
%if %{ruby}
BuildRequires:	ruby
BuildRequires:	ruby-devel
%endif
BuildRequires:	openssl-devel
BuildRequires:	globus-gss-assist-devel
BuildRequires:	globus-gsi-credential-devel
BuildRequires:	globus-proxy-utils
BuildRequires:	libtool-ltdl-devel
BuildRequires:	desktop-file-utils
BuildRequires:	dcap-devel
BuildRequires:	dpm-devel
%if %{xrootd}
BuildRequires:	xrootd-client-devel >= 1:3.3.5
BuildRequires:	xrootd-private-devel >= 1:3.3.5
%endif
BuildRequires:	cfitsio-devel
BuildRequires:	davix-devel >= 0.2.8
BuildRequires:	gfal2-devel
BuildRequires:	srm-ifce-devel
%if %{hadoop}
BuildRequires:	hadoop-devel
%endif
%if %{oce}
BuildRequires:	OCE-devel
%endif
BuildRequires:	R-Rcpp-devel
BuildRequires:	R-RInside-devel
BuildRequires:	readline-devel
%if %{?fedora}%{!?fedora:0} >= 21 || %{?rhel}%{!?rhel:0} >= 8
BuildRequires:	tbb-devel >= 4.3
%endif
BuildRequires:	emacs
BuildRequires:	emacs-el
BuildRequires:	gcc-c++
BuildRequires:	gcc-gfortran
BuildRequires:	graphviz-devel
BuildRequires:	expat-devel
%if %{pythia8}
BuildRequires:	pythia8-devel >= 8.1.80
%endif
BuildRequires:	blas-devel
BuildRequires:	numpy
BuildRequires:	doxygen
BuildRequires:	graphviz
BuildRequires:	yuicompressor
BuildRequires:	perl-generators
BuildRequires:	systemd-units
BuildRequires:	gtest-devel
BuildRequires:	gmock-devel
#		Some of the tests call lsb_release
BuildRequires:	redhat-lsb-core
#		Fonts
BuildRequires:	font(freesans)
BuildRequires:	font(freeserif)
BuildRequires:	font(freemono)
#		Provides "symbol", "dingbats" and "chancery"
BuildRequires:	urw-fonts
#		The root-fonts package provides Droid Sans Fallback for EPEL
%if %{?fedora}%{!?fedora:0} >= 11
BuildRequires:	font(droidsansfallback)
%endif
#		With gdb installed test failures will show backtraces
BuildRequires:	gdb
Requires:	%{name}-core%{?_isa} = %{version}-%{release}
Requires:	%{name}-io%{?_isa} = %{version}-%{release}
Requires:	%{name}-mathcore%{?_isa} = %{version}-%{release}
Requires:	%{name}-multiproc%{?_isa} = %{version}-%{release}
Requires:	%{name}-net%{?_isa} = %{version}-%{release}
Requires:	%{name}-tree%{?_isa} = %{version}-%{release}
Requires:	hicolor-icon-theme
Requires:	emacs-filesystem >= %{_emacs_version}
Provides:	emacs-%{name} = %{version}-%{release}
Provides:	emacs-%{name}-el = %{version}-%{release}
Obsoletes:	emacs-%{name} < 5.34.28
Obsoletes:	emacs-%{name}-el < 5.34.28

%description
The ROOT system provides a set of object oriented frameworks with all
the functionality needed to handle and analyze large amounts of data
in a very efficient way. Having the data defined as a set of objects,
specialized storage methods are used to get direct access to the
separate attributes of the selected objects, without having to touch
the bulk of the data. Included are histogramming methods in an
arbitrary number of dimensions, curve fitting, function evaluation,
minimization, graphics and visualization classes to allow the easy
setup of an analysis system that can query and process the data
interactively or in batch mode, as well as a general parallel
processing framework, PROOF, that can considerably speed up an
analysis.

Thanks to the built-in C++ interpreter cling, the command, the
scripting and the programming language are all C++. The interpreter
allows for fast prototyping of the macros since it removes the, time
consuming, compile/link cycle. It also provides a good environment to
learn C++. If more performance is needed the interactively developed
macros can be compiled using a C++ compiler via a machine independent
transparent compiler interface called ACliC.

The system has been designed in such a way that it can query its
databases in parallel on clusters of workstations or many-core
machines. ROOT is an open system that can be dynamically extended by
linking external libraries. This makes ROOT a premier platform on
which to build data acquisition, simulation and data analysis systems.

%package icons
Summary:	ROOT icon collection
BuildArch:	noarch
Requires:	%{name}-core = %{version}-%{release}

%description icons
This package contains icons used by the ROOT GUI.

%package fonts
Summary:	ROOT font collection
BuildArch:	noarch
%if %{?rhel}%{!?rhel:0}
#		STIX version 0.9 and Driod Sans Fallback
License:	OFL and ASL 2.0
%else
#		STIX version 0.9 only
License:	OFL
%endif
Requires:	%{name}-core = %{version}-%{release}

%description fonts
This package contains fonts used by ROOT that are not available in Fedora.
In particular it contains STIX version 0.9 that is used by TMathText.
%if %{?rhel}%{!?rhel:0}
For EPEL it also provides the Google Droid Sans Fallback font.
%endif

%package doc
Summary:	Documentation for the ROOT system
BuildArch:	noarch
License:	LGPLv2+ and GPLv2+ and BSD
Requires:	mathjax

%description doc
This package contains the automatically generated ROOT class
documentation.

%package tutorial
Summary:	ROOT tutorial scripts and test suite
BuildArch:	noarch
Requires:	%{name} = %{version}-%{release}

%description tutorial
This package contains the tutorial scripts and test suite for ROOT.

%package core
Summary:	ROOT core libraries
License:	LGPLv2+ and BSD
Requires:	%{name}-fonts = %{version}-%{release}
Requires:	%{name}-icons = %{version}-%{release}
#		Dynamic dependencies
Requires:	%{name}-cling%{?_isa} = %{version}-%{release}
Requires:	%{name}-graf-asimage%{?_isa} = %{version}-%{release}
#		Packages providing the libraries listed by "root-config --libs"
#		(Only root-physics and root-multiproc are not dragged in by
#		recursively resolving the dependency on root-graf-asimage
#		above, so it is not that much of a bloat...)
Requires:	%{name}-graf%{?_isa} = %{version}-%{release}
Requires:	%{name}-graf-gpad%{?_isa} = %{version}-%{release}
Requires:	%{name}-graf-postscript%{?_isa} = %{version}-%{release}
Requires:	%{name}-graf3d%{?_isa} = %{version}-%{release}
Requires:	%{name}-hist%{?_isa} = %{version}-%{release}
Requires:	%{name}-io%{?_isa} = %{version}-%{release}
Requires:	%{name}-net%{?_isa} = %{version}-%{release}
Requires:	%{name}-mathcore%{?_isa} = %{version}-%{release}
Requires:	%{name}-matrix%{?_isa} = %{version}-%{release}
Requires:	%{name}-multiproc%{?_isa} = %{version}-%{release}
Requires:	%{name}-physics%{?_isa} = %{version}-%{release}
Requires:	%{name}-tree%{?_isa} = %{version}-%{release}
Requires:	%{name}-tree-player%{?_isa} = %{version}-%{release}
#		Fonts
Requires:	xorg-x11-fonts-ISO8859-1-75dpi
Requires:	font(freesans)
Requires:	font(freeserif)
Requires:	font(freemono)
#		Provides "symbol", "dingbats" and "chancery"
Requires:	urw-fonts
#		The root-fonts package provides Droid Sans Fallback for EPEL
%if %{?fedora}%{!?fedora:0} >= 11
Requires:	font(droidsansfallback)
%endif
%if %{ruby} == 0
Obsoletes:	%{name}-ruby < 6.00.00
%endif
Obsoletes:	%{name}-vdt < 6.10.00

%description core
This package contains the core libraries used by ROOT: libCore, libNew,
libRint and libThread.

%package multiproc
Summary:	Multi-processor support for ROOT
Requires:	%{name}-core%{?_isa} = %{version}-%{release}
Requires:	%{name}-io%{?_isa} = %{version}-%{release}
Requires:	%{name}-net%{?_isa} = %{version}-%{release}

%description multiproc
This package provides ROOT's multi-processor support library: libMultiProc.

%package cling
Summary:	Cling C++ interpreter
License:	NCSA and (NCSA or LGPLv2+)
Requires:	%{name}-core%{?_isa} = %{version}-%{release}
Requires:	%{name}-io%{?_isa} = %{version}-%{release}
#		Root's cling interpreter uses a particular git commit of
#		llvm and clang with application specific changes. It does
#		not work with the system libraries. The bundled llvm and
#		clang are compiled using -fvisibility=hidden, and are not
#		visible outside of the libCling module.
Requires:	gcc-c++
Requires:	redhat-rpm-config
Provides:	bundled(clang-libs)
Provides:	bundled(llvm-libs)
Obsoletes:	%{name}-cint7 < 5.26.00c
Obsoletes:	%{name}-cint < 6.00.00
Obsoletes:	%{name}-cintex < 6.00.00
Obsoletes:	%{name}-reflex < 6.00.00

%description cling
Cling is an interactive C++ interpreter, built on top of Clang and
LLVM compiler infrastructure.

%package proofd
Summary:	Parallel ROOT Facility - distributed, parallel computing
Requires:	%{name}-core%{?_isa} = %{version}-%{release}
Requires:	%{name}-proof%{?_isa} = %{version}-%{release}
#		Dynamic dependency
Requires:	%{name}-net-rpdutils%{?_isa} = %{version}-%{release}
Requires(preun):	systemd-units
Requires(post):		systemd-units
Requires(postun):	systemd-units

%description proofd
This package contains the PROOF server. Proofd is the core daemon of
the PROOF (Parallel ROOT Facility) system for distributed parallel
computing. Installing this package on a machine makes it possible
for the machine to participate in a parallel computing farm (cluster
or via the Internet), either as a master or a slave, using a
transparent interface.

%package rootd
Summary:	ROOT remote file server
#		Dynamic dependency
Requires:	%{name}-net-rpdutils%{?_isa} = %{version}-%{release}
Requires(preun):	systemd-units
Requires(post):		systemd-units
Requires(postun):	systemd-units

%description rootd
This package contains the ROOT file server. Rootd is a server for ROOT
files, serving files over the Internet. Using this daemon, you can
access files on the machine from anywhere on the Internet, using a
transparent interface.

%package -n python2-%{name}
Summary:	Python extension for ROOT
%{?py2_dist:
Provides:	%{py2_dist %{name}} = %{version}
}
Provides:	root-python = %{version}-%{release}
Obsoletes:	root-python < 6.08.00
Requires:	%{name}-core%{?_isa} = %{version}-%{release}
Requires:	%{name}-io%{?_isa} = %{version}-%{release}
Requires:	%{name}-tree%{?_isa} = %{version}-%{release}

%description -n python2-%{name}
This package contains the Python extension for ROOT. This package
provide a Python interface to ROOT, and a ROOT interface to Python.

%package -n python%{python3_pkgversion}-%{name}
Summary:	Python extension for ROOT
%{?py3_dist:
Provides:	%{py3_dist %{name}} = %{version}
}
Provides:	root-python%{python3_pkgversion} = %{version}-%{release}
Obsoletes:	root-python%{python3_pkgversion} < 6.08.00
Requires:	%{name}-core%{?_isa} = %{version}-%{release}
Requires:	%{name}-io%{?_isa} = %{version}-%{release}
Requires:	%{name}-tree%{?_isa} = %{version}-%{release}

%description -n python%{python3_pkgversion}-%{name}
This package contains the Python extension for ROOT. This package
provide a Python interface to ROOT, and a ROOT interface to Python.

%package -n python2-jupyroot
Summary:	ROOT Jupyter kernel
%{?py2_dist:
Provides:	%{py2_dist jupyroot} = %{version}
}
Requires:	python2-%{name}%{?_isa} = %{version}-%{release}
Requires:	python2-jsmva = %{version}-%{release}
Requires:	%{name}-core%{?_isa} = %{version}-%{release}
Requires:	%{name}-notebook = %{version}-%{release}
%if %{?fedora}%{!?fedora:0} >= 26 || %{?rhel}%{!?rhel:0} >= 8
Requires:	python2-ipython
Requires:	python2-metakernel
%else
Requires:	python-ipython-console
#		python-metakernel for python2 not available in
#		Fedora <= 25 or RHEL/EPEL - some functionality missing
%endif
Obsoletes:	%{name}-rootaas < 6.08.00

%description -n python2-jupyroot
The Jupyter kernel for the ROOT notebook.

%package -n python%{python3_pkgversion}-jupyroot
Summary:	ROOT Jupyter kernel
%{?py3_dist:
Provides:	%{py3_dist jupyroot} = %{version}
}
Requires:	python%{python3_pkgversion}-%{name}%{?_isa} = %{version}-%{release}
Requires:	python%{python3_pkgversion}-jsmva = %{version}-%{release}
Requires:	%{name}-core%{?_isa} = %{version}-%{release}
Requires:	%{name}-notebook = %{version}-%{release}
%if %{?fedora}%{!?fedora:0} >= 26 || %{?rhel}%{!?rhel:0} >= 8
Requires:	python%{python3_pkgversion}-ipython
Requires:	python%{python3_pkgversion}-metakernel
%else
%if %{?fedora}%{!?fedora:0}
#		ipython for python3 not available in RHEL/EPEL
Requires:	python%{python3_pkgversion}-ipython-console
%endif
#		python-metakernel for python3 not available in
#		Fedora <= 25 or RHEL/EPEL - some functionality missing
%endif

%description -n python%{python3_pkgversion}-jupyroot
The Jupyter kernel for the ROOT notebook.

%package -n python2-jsmva
Summary:	TMVA interface used by JupyROOT
BuildArch:	noarch
%{?py2_dist:
Provides:	%{py2_dist jsmva} = %{version}
}
Requires:	%{name}-tmva = %{version}-%{release}

%description -n python2-jsmva
TMVA interface used by JupyROOT.

%package -n python%{python3_pkgversion}-jsmva
Summary:	TMVA interface used by JupyROOT
BuildArch:	noarch
%{?py3_dist:
Provides:	%{py3_dist jsmva} = %{version}
}
Requires:	%{name}-tmva = %{version}-%{release}

%description -n python%{python3_pkgversion}-jsmva
TMVA interface used by JupyROOT.

%if %{ruby}
%package ruby
Summary:	Ruby extension for ROOT
Requires:	%{name}-core%{?_isa} = %{version}-%{release}
Requires:	%{name}-hist%{?_isa} = %{version}-%{release}
Requires:	%{name}-mathcore%{?_isa} = %{version}-%{release}
Provides:	ruby(libRuby) = %{version}

%description ruby
This package contains the Ruby extension for ROOT. The interface
goes both ways - that is, you can call ROOT functions from Ruby, and
invoke the Ruby interpreter from ROOT.
%endif

%package r
Summary:	R interface for ROOT
Requires:	%{name}-core%{?_isa} = %{version}-%{release}
Requires:	%{name}-matrix%{?_isa} = %{version}-%{release}

%description r
ROOT R is an interface in ROOT to call R functions using an R C++
interface. This interface opens the possibility in ROOT to use the
very large set of mathematical and statistical tools provided by R.
With ROOT R you can perform a conversion from ROOT's C++ objects to
R's objects, transform the returned R objects into ROOT's C++ objects,
then the R functionality can be used directly for statistical studies
in ROOT.

%package r-tools
Summary:	R Tools
Requires:	%{name}-core%{?_isa} = %{version}-%{release}
Requires:	%{name}-mathcore%{?_isa} = %{version}-%{release}
Requires:	%{name}-matrix%{?_isa} = %{version}-%{release}
Requires:	%{name}-r%{?_isa} = %{version}-%{release}

%description r-tools
This package contains a minimizer module for ROOT that uses the ROOT
R interface.

%package genetic
Summary:	Genetic algorithms for ROOT
Requires:	%{name}-core%{?_isa} = %{version}-%{release}
Requires:	%{name}-mathcore%{?_isa} = %{version}-%{release}
Requires:	%{name}-tmva%{?_isa} = %{version}-%{release}

%description genetic
This package contains a genetic minimizer module for ROOT.

%package geom
Summary:	Geometry library for ROOT
Requires:	%{name}-core%{?_isa} = %{version}-%{release}
Requires:	%{name}-graf-gpad%{?_isa} = %{version}-%{release}
Requires:	%{name}-graf3d%{?_isa} = %{version}-%{release}
Requires:	%{name}-gui%{?_isa} = %{version}-%{release}
Requires:	%{name}-gui-ged%{?_isa} = %{version}-%{release}
Requires:	%{name}-hist%{?_isa} = %{version}-%{release}
Requires:	%{name}-io%{?_isa} = %{version}-%{release}
Requires:	%{name}-mathcore%{?_isa} = %{version}-%{release}
Requires:	%{name}-tree%{?_isa} = %{version}-%{release}

%description geom
This package contains a library for defining geometries in ROOT.

%package gdml
Summary:	GDML import/export for ROOT geometries
Requires:	%{name}-core%{?_isa} = %{version}-%{release}
Requires:	%{name}-geom%{?_isa} = %{version}-%{release}
Requires:	%{name}-hist%{?_isa} = %{version}-%{release}
Requires:	%{name}-io-xml%{?_isa} = %{version}-%{release}

%description gdml
This package contains an import/export module for ROOT geometries.

%if %{oce}
%package geocad
Summary:	OpenCascade import/export for ROOT geometries
Requires:	%{name}-core%{?_isa} = %{version}-%{release}
Requires:	%{name}-geom%{?_isa} = %{version}-%{release}

%description geocad
This package contains an import/export module for ROOT geometries.
%endif

%package graf
Summary:	2D graphics library for ROOT
Requires:	%{name}-core%{?_isa} = %{version}-%{release}
Requires:	%{name}-hist%{?_isa} = %{version}-%{release}
Requires:	%{name}-io%{?_isa} = %{version}-%{release}
Requires:	%{name}-mathcore%{?_isa} = %{version}-%{release}

%description graf
This package contains the 2-dimensional graphics library for ROOT.

%package graf-asimage
Summary:	AfterImage graphics renderer for ROOT
Requires:	%{name}-core%{?_isa} = %{version}-%{release}
Requires:	%{name}-graf%{?_isa} = %{version}-%{release}
Requires:	%{name}-gui%{?_isa} = %{version}-%{release}
Requires:	%{name}-hist%{?_isa} = %{version}-%{release}
Requires:	%{name}-io%{?_isa} = %{version}-%{release}
Requires:	%{name}-mathcore%{?_isa} = %{version}-%{release}

%description graf-asimage
This package contains the AfterImage renderer for ROOT, which allows
you to store output graphics in many formats, including JPEG, PNG and
TIFF.

%package graf-fitsio
Summary:	ROOT interface for the Flexible Image Transport System (FITS)
Requires:	%{name}-core%{?_isa} = %{version}-%{release}
Requires:	%{name}-graf%{?_isa} = %{version}-%{release}
Requires:	%{name}-graf-gpad%{?_isa} = %{version}-%{release}
Requires:	%{name}-hist%{?_isa} = %{version}-%{release}
Requires:	%{name}-matrix%{?_isa} = %{version}-%{release}

%description graf-fitsio
This package contains a library for using the Flexible Image Transport
System (FITS) data format in root.

%package graf-gpad
Summary:	Canvas and pad library for ROOT
Requires:	%{name}-core%{?_isa} = %{version}-%{release}
Requires:	%{name}-graf%{?_isa} = %{version}-%{release}
Requires:	%{name}-hist%{?_isa} = %{version}-%{release}
Requires:	%{name}-io%{?_isa} = %{version}-%{release}
Requires:	%{name}-mathcore%{?_isa} = %{version}-%{release}
#		Dynamic dependency
Requires:	%{name}-graf-postscript%{?_isa} = %{version}-%{release}

%description graf-gpad
This package contains a library for canvas and pad manipulations.

%package graf-gviz
Summary:	Graphviz 2D library for ROOT
Requires:	%{name}-core%{?_isa} = %{version}-%{release}
Requires:	%{name}-graf%{?_isa} = %{version}-%{release}
Requires:	%{name}-hist%{?_isa} = %{version}-%{release}

%description graf-gviz
This package contains the 2-dimensional graphviz library for ROOT.

%package graf-postscript
Summary:	Postscript/PDF renderer library for ROOT
Requires:	%{name}-core%{?_isa} = %{version}-%{release}
Requires:	%{name}-graf%{?_isa} = %{version}-%{release}

%description graf-postscript
This package contains a library for ROOT, which allows rendering
postscript and PDF output.

%package graf-qt
Summary:	Qt renderer for ROOT
Requires:	%{name}-core%{?_isa} = %{version}-%{release}
Requires:	%{name}-graf%{?_isa} = %{version}-%{release}
Requires:	%{name}-graf-gpad%{?_isa} = %{version}-%{release}

%description graf-qt
This package contains the Qt renderer for ROOT.

%package graf-x11
Summary:	X window system renderer for ROOT
Requires:	%{name}-core%{?_isa} = %{version}-%{release}
Requires:	%{name}-graf%{?_isa} = %{version}-%{release}

%description graf-x11
This package contains the X11 renderer for ROOT, which allows using an
X display for showing graphics.

%package graf3d
Summary:	Basic 3D shapes library for ROOT
Requires:	%{name}-core%{?_isa} = %{version}-%{release}
Requires:	%{name}-graf%{?_isa} = %{version}-%{release}
Requires:	%{name}-graf-gpad%{?_isa} = %{version}-%{release}
Requires:	%{name}-hist%{?_isa} = %{version}-%{release}
Requires:	%{name}-mathcore%{?_isa} = %{version}-%{release}

%description graf3d
This library contains the basic 3D shapes and classes for ROOT. For
a more full-blown geometry library, see the root-geom package.

%package graf3d-eve
Summary:	Event display library for ROOT
Requires:	%{name}-core%{?_isa} = %{version}-%{release}
Requires:	%{name}-geom%{?_isa} = %{version}-%{release}
Requires:	%{name}-graf%{?_isa} = %{version}-%{release}
Requires:	%{name}-graf-gpad%{?_isa} = %{version}-%{release}
Requires:	%{name}-graf3d%{?_isa} = %{version}-%{release}
Requires:	%{name}-graf3d-gl%{?_isa} = %{version}-%{release}
Requires:	%{name}-gui%{?_isa} = %{version}-%{release}
Requires:	%{name}-gui-ged%{?_isa} = %{version}-%{release}
Requires:	%{name}-hist%{?_isa} = %{version}-%{release}
Requires:	%{name}-io%{?_isa} = %{version}-%{release}
Requires:	%{name}-mathcore%{?_isa} = %{version}-%{release}
Requires:	%{name}-montecarlo-eg%{?_isa} = %{version}-%{release}
Requires:	%{name}-physics%{?_isa} = %{version}-%{release}
Requires:	%{name}-tree%{?_isa} = %{version}-%{release}
Requires:	%{name}-tree-player%{?_isa} = %{version}-%{release}

%description graf3d-eve
This package contains a library for defining event displays in ROOT.

%package graf3d-gl
Summary:	GL renderer for ROOT
Requires:	%{name}-core%{?_isa} = %{version}-%{release}
Requires:	%{name}-graf%{?_isa} = %{version}-%{release}
Requires:	%{name}-graf-gpad%{?_isa} = %{version}-%{release}
Requires:	%{name}-graf3d%{?_isa} = %{version}-%{release}
Requires:	%{name}-gui%{?_isa} = %{version}-%{release}
Requires:	%{name}-gui-ged%{?_isa} = %{version}-%{release}
Requires:	%{name}-hist%{?_isa} = %{version}-%{release}
Requires:	%{name}-mathcore%{?_isa} = %{version}-%{release}
Requires:	%{name}-tree%{?_isa} = %{version}-%{release}

%description graf3d-gl
This package contains the GL renderer for ROOT. This library provides
3D rendering of volumes and shapes defined in ROOT, as well as 3D
rendering of histograms, and similar. Included is also a high quality
3D viewer for ROOT defined geometries.

%package graf3d-gviz3d
Summary:	Graphviz 3D library for ROOT
Requires:	%{name}-core%{?_isa} = %{version}-%{release}
Requires:	%{name}-geom%{?_isa} = %{version}-%{release}
Requires:	%{name}-graf-gpad%{?_isa} = %{version}-%{release}
Requires:	%{name}-graf3d%{?_isa} = %{version}-%{release}
Requires:	%{name}-graf3d-gl%{?_isa} = %{version}-%{release}
Requires:	%{name}-gui%{?_isa} = %{version}-%{release}
Requires:	%{name}-gui-ged%{?_isa} = %{version}-%{release}

%description graf3d-gviz3d
This package contains the 3-dimensional graphviz library for ROOT.

%package graf3d-x3d
Summary:	X 3D renderer for ROOT
Requires:	%{name}-core%{?_isa} = %{version}-%{release}
Requires:	%{name}-graf3d%{?_isa} = %{version}-%{release}
Requires:	%{name}-gui%{?_isa} = %{version}-%{release}

%description graf3d-x3d
This package contains the X 3D renderer for ROOT. This library provides
3D rendering of volumes and shapes defined in ROOT. Included is also
a low quality 3D viewer for ROOT defined geometries.

%package gui
Summary:	GUI library for ROOT
Requires:	%{name}-core%{?_isa} = %{version}-%{release}
Requires:	%{name}-graf%{?_isa} = %{version}-%{release}
Requires:	%{name}-graf-gpad%{?_isa} = %{version}-%{release}
Requires:	%{name}-io%{?_isa} = %{version}-%{release}
Requires:	%{name}-mathcore%{?_isa} = %{version}-%{release}
Requires:	%{name}-net%{?_isa} = %{version}-%{release}
#		Dynamic dependencies
Requires:	%{name}-graf-x11%{?_isa} = %{version}-%{release}
Requires:	%{name}-gui-ged%{?_isa} = %{version}-%{release}

%description gui
This package contains a library for defining graphical user interfaces.

%package gui-fitpanel
Summary:	GUI element for fits in ROOT
Requires:	%{name}-core%{?_isa} = %{version}-%{release}
Requires:	%{name}-graf-gpad%{?_isa} = %{version}-%{release}
Requires:	%{name}-gui%{?_isa} = %{version}-%{release}
Requires:	%{name}-hist%{?_isa} = %{version}-%{release}
%if %{root7}
Requires:	%{name}-hist-draw%{?_isa} = %{version}-%{release}
Requires:	%{name}-gui-webdisplay%{?_isa} = %{version}-%{release}
%endif
Requires:	%{name}-io%{?_isa} = %{version}-%{release}
Requires:	%{name}-mathcore%{?_isa} = %{version}-%{release}
Requires:	%{name}-tree%{?_isa} = %{version}-%{release}

%description gui-fitpanel
This package contains a library to show a pop-up dialog when fitting
various kinds of data.

%package gui-ged
Summary:	GUI element for editing various ROOT objects
Requires:	%{name}-core%{?_isa} = %{version}-%{release}
Requires:	%{name}-graf%{?_isa} = %{version}-%{release}
Requires:	%{name}-graf-gpad%{?_isa} = %{version}-%{release}
Requires:	%{name}-gui%{?_isa} = %{version}-%{release}
Requires:	%{name}-hist%{?_isa} = %{version}-%{release}
Requires:	%{name}-tree%{?_isa} = %{version}-%{release}
#		Dynamic dependency
Requires:	%{name}-tree-player%{?_isa} = %{version}-%{release}

%description gui-ged
This package contains a library to show a pop-up window for editing
various ROOT objects.

%package guibuilder
Summary:	GUI editor library for ROOT
Requires:	%{name}-core%{?_isa} = %{version}-%{release}
Requires:	%{name}-graf%{?_isa} = %{version}-%{release}
Requires:	%{name}-gui%{?_isa} = %{version}-%{release}
Requires:	%{name}-mathcore%{?_isa} = %{version}-%{release}

%description guibuilder
This package contains a library for editing graphical user interfaces
in ROOT.

%package gui-qt
Summary:	Qt GUI for ROOT
Requires:	%{name}-core%{?_isa} = %{version}-%{release}
Requires:	%{name}-graf-gpad%{?_isa} = %{version}-%{release}
Requires:	%{name}-graf-qt%{?_isa} = %{version}-%{release}
Requires:	%{name}-gui%{?_isa} = %{version}-%{release}

%description gui-qt
This package contains the Qt GUI for ROOT.

%package gui-recorder
Summary:	Interface for recording and replaying events in ROOT
Requires:	%{name}-core%{?_isa} = %{version}-%{release}
Requires:	%{name}-gui%{?_isa} = %{version}-%{release}
Requires:	%{name}-io%{?_isa} = %{version}-%{release}
Requires:	%{name}-tree%{?_isa} = %{version}-%{release}

%description gui-recorder
This library provides interface for recording and replaying events in ROOT.
Recorded events are:
 - Commands typed by user in command line ('new TCanvas')
 - GUI events (mouse movement, button clicks, ...)
All the recorded events from one session are stored in one TFile
and can be replayed again anytime.

%if %{root7}
%package gui-canvaspainter
Summary:	Canvas painter (ROOT 7)
Requires:	%{name}-core%{?_isa} = %{version}-%{release}
Requires:	%{name}-graf%{?_isa} = %{version}-%{release}
Requires:	%{name}-io%{?_isa} = %{version}-%{release}
Requires:	%{name}-gui-webdisplay%{?_isa} = %{version}-%{release}

%description gui-canvaspainter
This package contains a canvas painter extension for ROOT 7

%package gui-webdisplay
Summary:	Web display (ROOT 7)
Requires:	%{name}-core%{?_isa} = %{version}-%{release}
Requires:	%{name}-io%{?_isa} = %{version}-%{release}
Requires:	%{name}-mathcore%{?_isa} = %{version}-%{release}
Requires:	%{name}-net-http%{?_isa} = %{version}-%{release}

%description gui-webdisplay
This package contains a web display extension for ROOT 7
%endif

%package hbook
Summary:	Hbook library for ROOT
Requires:	%{name}-core%{?_isa} = %{version}-%{release}
Requires:	%{name}-hist%{?_isa} = %{version}-%{release}
Requires:	%{name}-io%{?_isa} = %{version}-%{release}
Requires:	%{name}-tree%{?_isa} = %{version}-%{release}

%description hbook
This package contains the Hbook library for ROOT, allowing you to
access legacy Hbook files (NTuples and Histograms from PAW).

%package hist
Summary:	Histogram library for ROOT
Requires:	%{name}-core%{?_isa} = %{version}-%{release}
Requires:	%{name}-io%{?_isa} = %{version}-%{release}
Requires:	%{name}-mathcore%{?_isa} = %{version}-%{release}
Requires:	%{name}-matrix%{?_isa} = %{version}-%{release}
#		Dynamic dependency
Requires:	%{name}-hist-painter%{?_isa} = %{version}-%{release}

%description hist
This package contains a library for histogramming in ROOT.

%if %{root7}
%package hist-draw
Summary:	Histogram drawing (ROOT 7)
Requires:	%{name}-core%{?_isa} = %{version}-%{release}
Requires:	%{name}-graf-gpad%{?_isa} = %{version}-%{release}
Requires:	%{name}-hist%{?_isa} = %{version}-%{release}

%description hist-draw
This package contains an histogram drawing extension for ROOT 7.
%endif

%package hist-painter
Summary:	Histogram painter plugin for ROOT
Requires:	%{name}-core%{?_isa} = %{version}-%{release}
Requires:	%{name}-graf%{?_isa} = %{version}-%{release}
Requires:	%{name}-graf-gpad%{?_isa} = %{version}-%{release}
Requires:	%{name}-hist%{?_isa} = %{version}-%{release}
%if %{root7}
Requires:	%{name}-hist-draw%{?_isa} = %{version}-%{release}
%endif
Requires:	%{name}-mathcore%{?_isa} = %{version}-%{release}
Requires:	%{name}-matrix%{?_isa} = %{version}-%{release}

%description hist-painter
This package contains a painter of histograms for ROOT.

%package spectrum
Summary:	Spectra analysis library for ROOT
Requires:	%{name}-core%{?_isa} = %{version}-%{release}
Requires:	%{name}-hist%{?_isa} = %{version}-%{release}

%description spectrum
This package contains the Spectrum library for ROOT.

%package spectrum-painter
Summary:	Spectrum painter plugin for ROOT
Requires:	%{name}-core%{?_isa} = %{version}-%{release}
Requires:	%{name}-graf%{?_isa} = %{version}-%{release}
Requires:	%{name}-hist%{?_isa} = %{version}-%{release}

%description spectrum-painter
This package contains a painter of spectra for ROOT.

%package hist-factory
Summary:	RooFit PDFs from ROOT histograms
Requires:	%{name}-core%{?_isa} = %{version}-%{release}
Requires:	%{name}-graf%{?_isa} = %{version}-%{release}
Requires:	%{name}-graf-gpad%{?_isa} = %{version}-%{release}
Requires:	%{name}-hist%{?_isa} = %{version}-%{release}
Requires:	%{name}-io%{?_isa} = %{version}-%{release}
Requires:	%{name}-io-xml%{?_isa} = %{version}-%{release}
Requires:	%{name}-matrix%{?_isa} = %{version}-%{release}
Requires:	%{name}-roofit%{?_isa} = %{version}-%{release}
Requires:	%{name}-tree%{?_isa} = %{version}-%{release}

%description hist-factory
Create RooFit probability density functions from ROOT histograms.

%package html
Summary:	HTML documentation generator for ROOT
Requires:	%{name}-core%{?_isa} = %{version}-%{release}
Requires:	%{name}-graf%{?_isa} = %{version}-%{release}
Requires:	graphviz

%description html
This package contains classes to automatically extract documentation
from marked up sources.

%package io
Summary:	Input/output of ROOT objects
Requires:	%{name}-core%{?_isa} = %{version}-%{release}

%description io
This package provides I/O routines for ROOT objects.

%package io-dcache
Summary:	dCache input/output library for ROOT
Requires:	%{name}-core%{?_isa} = %{version}-%{release}
Requires:	%{name}-io%{?_isa} = %{version}-%{release}

%description io-dcache
This package contains the dCache extension for ROOT.

%package io-gfal
Summary:	Grid File Access Library input/output library for ROOT
Requires:	%{name}-core%{?_isa} = %{version}-%{release}
Requires:	%{name}-io%{?_isa} = %{version}-%{release}

%description io-gfal
This package contains the Grid File Access Library extension for ROOT.

%if %{hadoop}
%package io-hdfs
Summary:	Hadoop File System input/output library for ROOT
Requires:	%{name}-core%{?_isa} = %{version}-%{release}
Requires:	%{name}-io%{?_isa} = %{version}-%{release}

%description io-hdfs
This package contains the Hadoop File System extension for ROOT.
%endif

%package io-rfio
Summary:	Remote File input/output library for ROOT
Requires:	%{name}-core%{?_isa} = %{version}-%{release}
Requires:	%{name}-io%{?_isa} = %{version}-%{release}

%description io-rfio
This package contains the Remote File IO extension for ROOT.

%package io-sql
Summary:	SQL input/output library for ROOT
Requires:	%{name}-core%{?_isa} = %{version}-%{release}
Requires:	%{name}-io%{?_isa} = %{version}-%{release}
Requires:	%{name}-net%{?_isa} = %{version}-%{release}

%description io-sql
This package contains the SQL extension for ROOT, that allows
transparent access to files data via an SQL database, using ROOT's
TFile interface.

%package io-xml
Summary:	XML reader library for ROOT
Requires:	%{name}-core%{?_isa} = %{version}-%{release}
Requires:	%{name}-io%{?_isa} = %{version}-%{release}

%description io-xml
This package contains the XML reader library for ROOT.

%package foam
Summary:	A Compact Version of the Cellular Event Generator
Requires:	%{name}-core%{?_isa} = %{version}-%{release}
Requires:	%{name}-hist%{?_isa} = %{version}-%{release}
Requires:	%{name}-mathcore%{?_isa} = %{version}-%{release}

%description foam
The general-purpose self-adapting Monte Carlo (MC) event
generator/simulator mFOAM (standing for mini-FOAM) is a new compact
version of the FOAM program, with a slightly limited functionality
with respect to its parent version. On the other hand, mFOAM is
easier to use for the average user.

%package fftw
Summary:	FFTW library for ROOT
License:	GPLv2+
Requires:	%{name}-core%{?_isa} = %{version}-%{release}

%description fftw
This package contains the Fast Fourier Transform extension for ROOT.
It uses the very fast fftw (version 3) library.

%package fumili
Summary:	Fumili library for ROOT
Requires:	%{name}-core%{?_isa} = %{version}-%{release}
Requires:	%{name}-hist%{?_isa} = %{version}-%{release}
Requires:	%{name}-mathcore%{?_isa} = %{version}-%{release}

%description fumili
This package contains the fumili library for ROOT. This provides an
alternative fitting algorithm for ROOT.

%package genvector
Summary:	Generalized vector library for ROOT
Requires:	%{name}-core%{?_isa} = %{version}-%{release}

%description genvector
This package contains the Genvector library for ROOT. This provides
a generalized vector library.

%package mathcore
Summary:	Core mathematics library for ROOT
Requires:	%{name}-core%{?_isa} = %{version}-%{release}
#		Dynamic dependency
Requires:	%{name}-minuit%{?_isa} = %{version}-%{release}

%description mathcore
This package contains the MathCore library for ROOT.

%package mathmore
Summary:	GSL interface library for ROOT
License:	GPLv2+
Requires:	%{name}-core%{?_isa} = %{version}-%{release}
Requires:	%{name}-mathcore%{?_isa} = %{version}-%{release}

%description mathmore
This package contains the MathMore library for ROOT. This provides
a partial GNU Scientific Library interface for ROOT.
While the rest of root is licensed under LGPLv2+ this optional library
is licensed under GPLv2+ due to its use of GSL.

%package matrix
Summary:	Matrix library for ROOT
Requires:	%{name}-core%{?_isa} = %{version}-%{release}
Requires:	%{name}-mathcore%{?_isa} = %{version}-%{release}

%description matrix
This package contains the Matrix library for ROOT.

%package minuit
Summary:	Minuit library for ROOT
Requires:	%{name}-core%{?_isa} = %{version}-%{release}
Requires:	%{name}-hist%{?_isa} = %{version}-%{release}
Requires:	%{name}-mathcore%{?_isa} = %{version}-%{release}
Requires:	%{name}-matrix%{?_isa} = %{version}-%{release}

%description minuit
This package contains the MINUIT library for ROOT. This provides a
fitting algorithm for ROOT.

%package minuit2
Summary:	Minuit version 2 library for ROOT
Requires:	%{name}-core%{?_isa} = %{version}-%{release}
Requires:	%{name}-hist%{?_isa} = %{version}-%{release}
Requires:	%{name}-mathcore%{?_isa} = %{version}-%{release}

%description minuit2
This package contains the MINUIT version 2 library for ROOT. This
provides an fitting algorithm for ROOT.

%package mlp
Summary:	Multi-layer perceptron extension for ROOT
Requires:	%{name}-core%{?_isa} = %{version}-%{release}
Requires:	%{name}-graf%{?_isa} = %{version}-%{release}
Requires:	%{name}-graf-gpad%{?_isa} = %{version}-%{release}
Requires:	%{name}-hist%{?_isa} = %{version}-%{release}
Requires:	%{name}-mathcore%{?_isa} = %{version}-%{release}
Requires:	%{name}-matrix%{?_isa} = %{version}-%{release}
Requires:	%{name}-tree%{?_isa} = %{version}-%{release}
Requires:	%{name}-tree-player%{?_isa} = %{version}-%{release}

%description mlp
This package contains the mlp library for ROOT. This library provides
a multi-layer perceptron neural network package for ROOT.

%package physics
Summary:	Physics library for ROOT
Requires:	%{name}-core%{?_isa} = %{version}-%{release}
Requires:	%{name}-mathcore%{?_isa} = %{version}-%{release}
Requires:	%{name}-matrix%{?_isa} = %{version}-%{release}

%description physics
This package contains the physics library for ROOT.

%package quadp
Summary:	QuadP library for ROOT
Requires:	%{name}-core%{?_isa} = %{version}-%{release}
Requires:	%{name}-matrix%{?_isa} = %{version}-%{release}

%description quadp
This package contains the QuadP library for ROOT. This provides the a
framework in which to do Quadratic Programming. The quadratic
programming problem involves minimization of a quadratic function
subject to linear constraints.

%package smatrix
Summary:	Sparse matrix library for ROOT
Requires:	%{name}-core%{?_isa} = %{version}-%{release}

%description smatrix
This package contains the Smatrix library for ROOT.

%package splot
Summary:	Splot library for ROOT
Requires:	%{name}-core%{?_isa} = %{version}-%{release}
Requires:	%{name}-hist%{?_isa} = %{version}-%{release}
Requires:	%{name}-matrix%{?_isa} = %{version}-%{release}
Requires:	%{name}-tree%{?_isa} = %{version}-%{release}
Requires:	%{name}-tree-player%{?_isa} = %{version}-%{release}

%description splot
A common method used in High Energy Physics to perform measurements
is the maximum Likelihood method, exploiting discriminating variables
to disentangle signal from background. The crucial point for such an
analysis to be reliable is to use an exhaustive list of sources of
events combined with an accurate description of all the Probability
Density Functions (PDF).

To assess the validity of the fit, a convincing quality check is to
explore further the data sample by examining the distributions of
control variables. A control variable can be obtained for instance by
removing one of the discriminating variables before performing again
the maximum Likelihood fit: this removed variable is a control
variable. The expected distribution of this control variable, for
signal, is to be compared to the one extracted, for signal, from the
data sample. In order to be able to do so, one must be able to unfold
from the distribution of the whole data sample.

The SPlot method allows to reconstruct the distributions for the
control variable, independently for each of the various sources of
events, without making use of any a priori knowledge on this
variable. The aim is thus to use the knowledge available for the
discriminating variables to infer the behavior of the individual
sources of events with respect to the control variable.

SPlot is optimal if the control variable is uncorrelated with the
discriminating variables.

%package unuran
Summary:	Random number generator library
License:	GPLv2+
Requires:	%{name}-core%{?_isa} = %{version}-%{release}
Requires:	%{name}-hist%{?_isa} = %{version}-%{release}
Requires:	%{name}-mathcore%{?_isa} = %{version}-%{release}

%description unuran
Contains universal (also called automatic or black-box) algorithms
that can generate random numbers from large classes of continuous or
discrete distributions, and also from practically all standard
distributions.

To generate random numbers the user must supply some information
about the desired distribution, especially a C-function that computes
the density and - depending on the chosen methods - some additional
information (like the borders of the domain, the mode, the derivative
of the density ...). After a user has given this information an
init-program computes all tables and constants necessary for the
random variate generation. The sample program can then generate
variates from the desired distribution.

%package memstat
Summary:	Memory statistics tool for use with ROOT
Requires:	%{name}-core%{?_isa} = %{version}-%{release}
Requires:	%{name}-hist%{?_isa} = %{version}-%{release}
Requires:	%{name}-io%{?_isa} = %{version}-%{release}
Requires:	%{name}-tree%{?_isa} = %{version}-%{release}

%description memstat
This package contains the memory statistics tool for debugging memory
leaks and such.

%package table
Summary:	Table library for ROOT
Requires:	%{name}-core%{?_isa} = %{version}-%{release}
Requires:	%{name}-graf-gpad%{?_isa} = %{version}-%{release}
Requires:	%{name}-graf3d%{?_isa} = %{version}-%{release}
Requires:	%{name}-hist%{?_isa} = %{version}-%{release}
Requires:	%{name}-io%{?_isa} = %{version}-%{release}
Requires:	%{name}-mathcore%{?_isa} = %{version}-%{release}
Requires:	%{name}-tree%{?_isa} = %{version}-%{release}

%description table
This package contains the Table library for ROOT.

%package montecarlo-eg
Summary:	Event generator library for ROOT
Requires:	%{name}-core%{?_isa} = %{version}-%{release}
Requires:	%{name}-graf%{?_isa} = %{version}-%{release}
Requires:	%{name}-graf-gpad%{?_isa} = %{version}-%{release}
Requires:	%{name}-graf3d%{?_isa} = %{version}-%{release}
Requires:	%{name}-mathcore%{?_isa} = %{version}-%{release}

%description montecarlo-eg
This package contains an event generator library for ROOT.

%if %{pythia8}
%package montecarlo-pythia8
Summary:	Pythia version 8 plugin for ROOT
Requires:	%{name}-core%{?_isa} = %{version}-%{release}
Requires:	%{name}-montecarlo-eg%{?_isa} = %{version}-%{release}

%description montecarlo-pythia8
This package contains the Pythia version 8 plug-in for ROOT. This
package provide the ROOT user with transparent interface to the Pythia
(version 8) event generators for hadronic interactions. If the term
"hadronic" does not ring any bells, this package is not for you.
%endif

%package montecarlo-vmc
Summary:	Virtual Monte-Carlo (simulation) library for ROOT
Requires:	%{name}-core%{?_isa} = %{version}-%{release}
Requires:	%{name}-geom%{?_isa} = %{version}-%{release}
Requires:	%{name}-mathcore%{?_isa} = %{version}-%{release}
Requires:	%{name}-montecarlo-eg%{?_isa} = %{version}-%{release}

%description montecarlo-vmc
This package contains the VMC library for ROOT.

%package net
Summary:	Net library for ROOT
Requires:	%{name}-core%{?_isa} = %{version}-%{release}
Requires:	%{name}-io%{?_isa} = %{version}-%{release}

%description net
This package contains the ROOT networking library.

%package net-rpdutils
Summary:	Authentication utilities used by rootd and proofd
Requires:	%{name}-core%{?_isa} = %{version}-%{release}

%description net-rpdutils
This package contains authentication utilities used by rootd and proofd.

%package net-bonjour
Summary:	Bonjour extension for ROOT
Requires:	%{name}-core%{?_isa} = %{version}-%{release}

%description net-bonjour
This package contains a bonjour extension for ROOT.

%package net-auth
Summary:	Authentication extension for ROOT
Requires:	%{name}-core%{?_isa} = %{version}-%{release}
Requires:	%{name}-io%{?_isa} = %{version}-%{release}
Requires:	%{name}-net%{?_isa} = %{version}-%{release}

%description net-auth
This package contains the basic authentication algorithms used by ROOT.

%package net-davix
Summary:	Davix extension for ROOT
Requires:	davix-libs%{?_isa} >= 0.2.8
Requires:	%{name}-core%{?_isa} = %{version}-%{release}
Requires:	%{name}-io%{?_isa} = %{version}-%{release}

%description net-davix
This package contains the davix extension for ROOT, that provides
access to http based storage such as webdav and S3.

%package net-globus
Summary:	Globus extension for ROOT
Requires:	%{name}-core%{?_isa} = %{version}-%{release}
Requires:	%{name}-net%{?_isa} = %{version}-%{release}
Requires:	%{name}-net-auth%{?_isa} = %{version}-%{release}
Requires:	globus-proxy-utils

%description net-globus
This package contains the Globus extension for ROOT, that allows
authentication and authorization against Globus.

%package net-krb5
Summary:	Kerberos (version 5) extension for ROOT
Requires:	%{name}-core%{?_isa} = %{version}-%{release}
Requires:	%{name}-net%{?_isa} = %{version}-%{release}
Requires:	%{name}-net-auth%{?_isa} = %{version}-%{release}
Requires:	krb5-workstation

%description net-krb5
This package contains the Kerberos (version 5) extension for ROOT, that
allows authentication and authorization using Kerberos tokens.

%package net-ldap
Summary:	LDAP extension for ROOT
Requires:	%{name}-core%{?_isa} = %{version}-%{release}

%description net-ldap
This package contains the LDAP extension for ROOT. This gives you
access to LDAP directories via ROOT.

%package net-http
Summary:	HTTP server extension for ROOT
Requires:	%{name}-core%{?_isa} = %{version}-%{release}
Requires:	%{name}-graf%{?_isa} = %{version}-%{release}
Requires:	%{name}-graf-gpad%{?_isa} = %{version}-%{release}
Requires:	%{name}-hist%{?_isa} = %{version}-%{release}
Requires:	%{name}-io%{?_isa} = %{version}-%{release}
Requires:	%{name}-io-xml%{?_isa} = %{version}-%{release}
Requires:	%{name}-tree%{?_isa} = %{version}-%{release}
Requires:	js-jsroot

%description net-http
This package contains the HTTP server extension for ROOT. It provides
an http interface to arbitrary ROOT applications.

%if %{xrootd}
%package netx
Summary:	NetX extension for ROOT
Requires:	%{name}-core%{?_isa} = %{version}-%{release}
Requires:	%{name}-io%{?_isa} = %{version}-%{release}
Requires:	%{name}-net%{?_isa} = %{version}-%{release}

%description netx
This package contains the NetX extension for ROOT, i.e. a client for
the xrootd server. Both the old (NetX) and the new (NetXNG) version are
provided.
%endif

%package proof
Summary:	PROOF extension for ROOT
Requires:	%{name}-core%{?_isa} = %{version}-%{release}
Requires:	%{name}-graf-gpad%{?_isa} = %{version}-%{release}
Requires:	%{name}-graf3d%{?_isa} = %{version}-%{release}
Requires:	%{name}-hist%{?_isa} = %{version}-%{release}
Requires:	%{name}-io%{?_isa} = %{version}-%{release}
Requires:	%{name}-mathcore%{?_isa} = %{version}-%{release}
Requires:	%{name}-net%{?_isa} = %{version}-%{release}
Requires:	%{name}-tree%{?_isa} = %{version}-%{release}
Requires:	%{name}-tree-player%{?_isa} = %{version}-%{release}
Obsoletes:	%{name}-clarens < 5.34.01
Obsoletes:	%{name}-peac < 5.34.01

%description proof
This package contains the proof extension for ROOT. This provides a
client to use in a PROOF environment.

%package proof-bench
Summary:	PROOF benchmarking
Requires:	%{name}-core%{?_isa} = %{version}-%{release}
Requires:	%{name}-graf%{?_isa} = %{version}-%{release}
Requires:	%{name}-graf-gpad%{?_isa} = %{version}-%{release}
Requires:	%{name}-hist%{?_isa} = %{version}-%{release}
Requires:	%{name}-io%{?_isa} = %{version}-%{release}
Requires:	%{name}-proof%{?_isa} = %{version}-%{release}
Requires:	%{name}-tree%{?_isa} = %{version}-%{release}

%description proof-bench
This package contains the steering class for PROOF benchmarks.

%package proof-pq2
Summary:	PROOF Quick Query (pq2)
Requires:	%{name}-core%{?_isa} = %{version}-%{release}
Requires:	%{name}-hist%{?_isa} = %{version}-%{release}
Requires:	%{name}-io%{?_isa} = %{version}-%{release}
Requires:	%{name}-net%{?_isa} = %{version}-%{release}
Requires:	%{name}-proof%{?_isa} = %{version}-%{release}

%description proof-pq2
Shell-based interface to the PROOF dataset handling.

%package proof-sessionviewer
Summary:	GUI to browse an interactive PROOF session
Requires:	%{name}-core%{?_isa} = %{version}-%{release}
Requires:	%{name}-graf%{?_isa} = %{version}-%{release}
Requires:	%{name}-graf-gpad%{?_isa} = %{version}-%{release}
Requires:	%{name}-gui%{?_isa} = %{version}-%{release}
Requires:	%{name}-hist%{?_isa} = %{version}-%{release}
Requires:	%{name}-mathcore%{?_isa} = %{version}-%{release}
Requires:	%{name}-proof%{?_isa} = %{version}-%{release}
Requires:	%{name}-tree%{?_isa} = %{version}-%{release}

%description proof-sessionviewer
This package contains a library for browsing an interactive PROOF
session in ROOT.

%if %{xrootd}
%package xproof
Summary:	XPROOF extension for ROOT
Requires:	%{name}-core%{?_isa} = %{version}-%{release}
Requires:	%{name}-io%{?_isa} = %{version}-%{release}
Requires:	%{name}-net%{?_isa} = %{version}-%{release}
Requires:	%{name}-proof%{?_isa} = %{version}-%{release}
#		Dynamic dependency
Requires:	%{name}-net-rpdutils%{?_isa} = %{version}-%{release}
Requires:	xrootd-server%{?_isa}

%description xproof
This package contains the xproof extension for ROOT. This provides a
client to be used in a PROOF environment.
%endif

%package roofit
Summary:	ROOT extension for modeling expected distributions
License:	BSD
Requires:	%{name}-core%{?_isa} = %{version}-%{release}
Requires:	%{name}-foam%{?_isa} = %{version}-%{release}
Requires:	%{name}-graf%{?_isa} = %{version}-%{release}
Requires:	%{name}-graf-gpad%{?_isa} = %{version}-%{release}
Requires:	%{name}-hist%{?_isa} = %{version}-%{release}
Requires:	%{name}-io%{?_isa} = %{version}-%{release}
Requires:	%{name}-mathcore%{?_isa} = %{version}-%{release}
Requires:	%{name}-mathmore%{?_isa} = %{version}-%{release}
Requires:	%{name}-matrix%{?_isa} = %{version}-%{release}
Requires:	%{name}-minuit%{?_isa} = %{version}-%{release}
Requires:	%{name}-tree%{?_isa} = %{version}-%{release}

%description roofit
The RooFit packages provide a toolkit for modeling the expected
distribution of events in a physics analysis. Models can be used to
perform likelihood fits, produce plots, and generate "toy Monte
Carlo" samples for various studies. The RooFit tools are integrated
with the object-oriented and interactive ROOT graphical environment.

RooFit has been developed for the BaBar collaboration, a high energy
physics experiment at the Stanford Linear Accelerator Center, and is
primarily targeted to the high-energy physicists using the ROOT
analysis environment, but the general nature of the package make it
suitable for adoption in different disciplines as well.

%package sql-mysql
Summary:	MySQL client plugin for ROOT
Requires:	%{name}-core%{?_isa} = %{version}-%{release}
Requires:	%{name}-net%{?_isa} = %{version}-%{release}

%description sql-mysql
This package contains the MySQL plugin for ROOT. This plugin
provides a thin client (interface) to MySQL servers. Using this
client, one can obtain information from a MySQL database into the
ROOT environment.

%package sql-odbc
Summary:	ODBC plugin for ROOT
Requires:	%{name}-core%{?_isa} = %{version}-%{release}
Requires:	%{name}-net%{?_isa} = %{version}-%{release}

%description sql-odbc
This package contains the ODBC (Open DataBase Connectivity) plugin
for ROOT, that allows transparent access to any kind of database that
supports the ODBC protocol.

%package sql-sqlite
Summary:	Sqlite client plugin for ROOT
Requires:	%{name}-core%{?_isa} = %{version}-%{release}
Requires:	%{name}-net%{?_isa} = %{version}-%{release}

%description sql-sqlite
This package contains the sqlite plugin for ROOT. This plugin
provides a thin client (interface) to sqlite servers. Using this
client, one can obtain information from a sqlite database into the
ROOT environment.

%package sql-pgsql
Summary:	PostgreSQL client plugin for ROOT
Requires:	%{name}-core%{?_isa} = %{version}-%{release}
Requires:	%{name}-net%{?_isa} = %{version}-%{release}

%description sql-pgsql
This package contains the PostGreSQL plugin for ROOT. This plugin
provides a thin client (interface) to PostGreSQL servers. Using this
client, one can obtain information from a PostGreSQL database into the
ROOT environment.

%package tmva
Summary:	Toolkit for multivariate data analysis
License:	BSD
Requires:	%{name}-core%{?_isa} = %{version}-%{release}
Requires:	%{name}-graf-gpad%{?_isa} = %{version}-%{release}
Requires:	%{name}-hist%{?_isa} = %{version}-%{release}
Requires:	%{name}-io%{?_isa} = %{version}-%{release}
Requires:	%{name}-io-xml%{?_isa} = %{version}-%{release}
Requires:	%{name}-mathcore%{?_isa} = %{version}-%{release}
Requires:	%{name}-matrix%{?_isa} = %{version}-%{release}
Requires:	%{name}-minuit%{?_isa} = %{version}-%{release}
Requires:	%{name}-mlp%{?_isa} = %{version}-%{release}
Requires:	%{name}-multiproc%{?_isa} = %{version}-%{release}
Requires:	%{name}-net%{?_isa} = %{version}-%{release}
Requires:	%{name}-tree%{?_isa} = %{version}-%{release}
Requires:	%{name}-tree-player%{?_isa} = %{version}-%{release}

%description tmva
The Toolkit for Multivariate Analysis (TMVA) provides a
ROOT-integrated environment for the parallel processing and
evaluation of MVA techniques to discriminate signal from background
samples. It presently includes (ranked by complexity):

  * Rectangular cut optimization
  * Correlated likelihood estimator (PDE approach)
  * Multi-dimensional likelihood estimator (PDE - range-search approach)
  * Fisher (and Mahalanobis) discriminant
  * H-Matrix (chi-squared) estimator
  * Artificial Neural Network (two different implementations)
  * Boosted Decision Trees

The TMVA package includes an implementation for each of these
discrimination techniques, their training and testing (performance
evaluation). In addition all these methods can be tested in parallel,
and hence their performance on a particular data set may easily be
compared.

%package tmva-python
Summary:	Toolkit for multivariate data analysis (Python)
License:	BSD
Requires:	%{name}-core%{?_isa} = %{version}-%{release}
Requires:	%{name}-tmva%{?_isa} = %{version}-%{release}

%description tmva-python
Python integration with TMVA.

%package tmva-r
Summary:	Toolkit for multivariate data analysis (R)
License:	BSD
Requires:	%{name}-core%{?_isa} = %{version}-%{release}
Requires:	%{name}-matrix%{?_isa} = %{version}-%{release}
Requires:	%{name}-r%{?_isa} = %{version}-%{release}
Requires:	%{name}-tmva%{?_isa} = %{version}-%{release}

%description tmva-r
R integration with TMVA.

%package tmva-gui
Summary:	Toolkit for multivariate data analysis GUI
License:	BSD
Requires:	%{name}-core%{?_isa} = %{version}-%{release}
Requires:	%{name}-graf%{?_isa} = %{version}-%{release}
Requires:	%{name}-graf-gpad%{?_isa} = %{version}-%{release}
Requires:	%{name}-gui%{?_isa} = %{version}-%{release}
Requires:	%{name}-hist%{?_isa} = %{version}-%{release}
Requires:	%{name}-io%{?_isa} = %{version}-%{release}
Requires:	%{name}-io-xml%{?_isa} = %{version}-%{release}
Requires:	%{name}-matrix%{?_isa} = %{version}-%{release}
Requires:	%{name}-tmva%{?_isa} = %{version}-%{release}
Requires:	%{name}-tree-viewer%{?_isa} = %{version}-%{release}

%description tmva-gui
GUI for the Toolkit for Multivariate Analysis (TMVA)

%package tree
Summary:	Tree library for ROOT
Requires:	%{name}-core%{?_isa} = %{version}-%{release}
Requires:	%{name}-io%{?_isa} = %{version}-%{release}
Requires:	%{name}-net%{?_isa} = %{version}-%{release}

%description tree
This package contains the Tree library for ROOT.

%package tree-player
Summary:	Library to loop over a ROOT tree
Requires:	%{name}-core%{?_isa} = %{version}-%{release}
Requires:	%{name}-graf%{?_isa} = %{version}-%{release}
Requires:	%{name}-graf-gpad%{?_isa} = %{version}-%{release}
Requires:	%{name}-graf3d%{?_isa} = %{version}-%{release}
Requires:	%{name}-hist%{?_isa} = %{version}-%{release}
Requires:	%{name}-io%{?_isa} = %{version}-%{release}
Requires:	%{name}-mathcore%{?_isa} = %{version}-%{release}
Requires:	%{name}-multiproc%{?_isa} = %{version}-%{release}
Requires:	%{name}-net%{?_isa} = %{version}-%{release}
Requires:	%{name}-tree%{?_isa} = %{version}-%{release}

%description tree-player
This package contains a plugin to loop over a ROOT tree.

%package tree-viewer
Summary:	GUI to browse a ROOT tree
Requires:	%{name}-core%{?_isa} = %{version}-%{release}
Requires:	%{name}-graf%{?_isa} = %{version}-%{release}
Requires:	%{name}-graf-gpad%{?_isa} = %{version}-%{release}
Requires:	%{name}-gui%{?_isa} = %{version}-%{release}
Requires:	%{name}-gui-ged%{?_isa} = %{version}-%{release}
Requires:	%{name}-hist%{?_isa} = %{version}-%{release}
Requires:	%{name}-io%{?_isa} = %{version}-%{release}
Requires:	%{name}-mathcore%{?_isa} = %{version}-%{release}
Requires:	%{name}-tree%{?_isa} = %{version}-%{release}
Requires:	%{name}-tree-player%{?_isa} = %{version}-%{release}

%description tree-viewer
This package contains a plugin for browsing a ROOT tree in ROOT.

%package unfold
Summary:	Distribution unfolding
Requires:	%{name}-core%{?_isa} = %{version}-%{release}
Requires:	%{name}-hist%{?_isa} = %{version}-%{release}
Requires:	%{name}-io-xml%{?_isa} = %{version}-%{release}
Requires:	%{name}-matrix%{?_isa} = %{version}-%{release}

%description unfold
An algorithm to unfold distributions from detector to truth level.

%package cli
Summary:	ROOT command line utilities
BuildArch:	noarch
Requires:	python2-%{name} = %{version}-%{release}

%description cli
The ROOT command line utilities is a set of scripts for common tasks
written in python.

%package notebook
Summary:	Static files for the Jupyter ROOT Notebook
BuildArch:	noarch
Requires:	%{name}-core = %{version}-%{release}
Requires:	js-jsroot

%description notebook
Javascript and style files for the Jupyter ROOT Notebook.

%prep
%setup -q -a 1

%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1
%patch12 -p1
%patch13 -p1
%patch14 -p1
%patch15 -p1
%patch16 -p1
%patch17 -p1
%patch18 -p1
%patch19 -p1
%patch20 -p1
%patch21 -p1

# Remove bundled sources in order to be sure they are not used
#  * afterimage
rm -rf graf2d/asimage/src/libAfterImage
#  * ftgl
rm -rf graf3d/ftgl/src graf3d/ftgl/inc
#  * freetype
rm -rf graf2d/freetype/src
#  * glew
rm -rf graf3d/glew/src graf3d/glew/inc
#  * pcre
rm -rf core/pcre/src
#  * zlib
rm -rf core/zip/src/[a-z]* core/zip/inc/[a-z]*
#  * lzma
rm -rf core/lzma/src/*.tar.gz
#  * gl2ps
rm graf3d/gl/src/gl2ps.cxx graf3d/gl/src/gl2ps/gl2ps.h
#  * unuran
rm -rf math/unuran/src/*.tar.gz
#  * xrootd-private-devel headers
rm -rf proof/xrdinc
#  * x11 extension headers
rm -rf graf2d/x11/inc/X11
#  * mathjax
rm -rf documentation/doxygen/mathjax.tar.gz
sed /mathjax.tar.gz/d -i documentation/doxygen/Makefile
sed 's!\(MATHJAX_RELPATH\s*=\).*!\1 file:///usr/share/javascript/mathjax!' \
    -i documentation/doxygen/Doxyfile
%if %{root7}
#  * string_view (<experimental/string_view> requires c++-14)
rm core/foundation/inc/libcpp_string_view.h \
   core/foundation/inc/RWrap_libcpp_string_view.h
%endif
#  * jsroot
rm -rf etc/http/*

# Remove bundled fonts provided by the OS distributions
%if %{?fedora}%{!?fedora:0} >= 11
rm fonts/DroidSansFallback.ttf
%endif

# Remove unsupported man page macros
sed -e '/^\.UR/d' -e '/^\.UE/d' -i man/man1/*

# Build PyROOT for python 3
cp -pr bindings/pyroot bindings/python

# Work around missing libraries in Fedora's gmock packaging < 1.8.0
if [ ! -r %{_libdir}/libgmock.so ] ; then
mkdir googlemock
pushd googlemock
g++ %{optflags} -DGTEST_HAS_PTHREAD=1 -c -o gmock-all.o /usr/src/gmock/gmock-all.cc
ar rv libgmock.a gmock-all.o
g++ %{optflags} -DGTEST_HAS_PTHREAD=1 -c -o gmock_main.o /usr/src/gmock/gmock_main.cc
ar rv libgmock_main.a gmock_main.o
popd
fi

# Remove pre-minified script and style files
rm etc/notebook/JsMVA/js/*.min.js
rm etc/notebook/JsMVA/css/*.min.css

%build
unset QTDIR
unset QTLIB
unset QTINC

# Minify script and style files
for s in etc/notebook/JsMVA/js/*.js ; do
    yuicompressor ${s} -o ${s%.js}.min.js
done
for s in etc/notebook/JsMVA/css/*.css ; do
    yuicompressor ${s} -o ${s%.css}.min.css
done

mkdir builddir
pushd builddir

# Avoid overlinking (this used to be the default with the old configure script)
LDFLAGS="-Wl,--as-needed %{?__global_ldflags}"

%if %{?fedora}%{!?fedora:0} || %{?rhel}%{!?rhel:0} >= 8
%cmake \
%else
%cmake3 \
%endif
       -DCMAKE_INSTALL_PREFIX:PATH=%{_prefix} \
       -DCMAKE_INSTALL_LIBDIR:PATH=%{_libdir}/%{name} \
       -DCMAKE_INSTALL_SYSCONFDIR:PATH=%{_datadir}/%{name} \
       -DCMAKE_INSTALL_DOCDIR:PATH=%{_pkgdocdir} \
       -DCMAKE_INSTALL_ELISPDIR:PATH=%{_emacs_sitelispdir}/%{name} \
       -Dgnuinstall:BOOL=ON \
       -Dbuiltin_afterimage:BOOL=OFF \
       -Dbuiltin_cfitsio:BOOL=OFF \
       -Dbuiltin_davix:BOOL=OFF \
       -Dbuiltin_fftw3:BOOL=OFF \
       -Dbuiltin_freetype:BOOL=OFF \
       -Dbuiltin_ftgl:BOOL=OFF \
       -Dbuiltin_gl2ps:BOOL=OFF \
       -Dbuiltin_glew:BOOL=OFF \
       -Dbuiltin_gsl:BOOL=OFF \
       -Dbuiltin_llvm:BOOL=ON \
       -Dbuiltin_lz4:BOOL=OFF \
       -Dbuiltin_lzma:BOOL=OFF \
       -Dbuiltin_openssl:BOOL=OFF \
       -Dbuiltin_pcre:BOOL=OFF \
       -Dbuiltin_tbb:BOOL=OFF \
       -Dbuiltin_unuran:BOOL=OFF \
       -Dbuiltin_vc:BOOL=OFF \
       -Dbuiltin_vdt:BOOL=OFF \
       -Dbuiltin_veccore:BOOL=OFF \
       -Dbuiltin_xrootd:BOOL=OFF \
       -Dbuiltin_zlib:BOOL=OFF \
       -Dafdsmgrd:BOOL=OFF \
       -Dafs:BOOL=OFF \
       -Dalien:BOOL=OFF \
       -Dasimage:BOOL=ON \
       -Dastiff:BOOL=ON \
       -Dbonjour:BOOL=ON \
       -Dcastor:BOOL=OFF \
       -Dccache:BOOL=OFF \
       -Dchirp:BOOL=OFF \
       -Dcling:BOOL=ON \
       -Dcocoa:BOOL=OFF \
       -Dcuda:BOOL=OFF \
%if %{root7}
       -Dcxx14:BOOL=ON \
       -Droot7:BOOL=ON \
%else
       -Dcxx14:BOOL=OFF \
       -Droot7:BOOL=OFF \
%endif
       -Dcxx17:BOOL=OFF \
       -Dcxxmodules:BOOL=OFF \
       -Ddavix:BOOL=ON \
       -Ddcache:BOOL=ON \
       -Dexceptions:BOOL=ON \
       -Dexplicitlink:BOOL=ON \
       -Dfftw3:BOOL=ON \
       -Dfitsio:BOOL=ON \
       -Dfortran:BOOL=ON \
       -Dgdml:BOOL=ON \
       -Dgenvector:BOOL=ON \
%if %{oce}
       -Dgeocad:BOOL=ON \
%else
       -Dgeocad:BOOL=OFF \
%endif
       -Dgfal:BOOL=ON \
       -Dglite:BOOL=OFF \
       -Dglobus:BOOL=ON \
       -Dgsl_shared:BOOL=ON \
       -Dgviz:BOOL=ON \
%if %{hadoop}
       -Dhdfs:BOOL=ON \
%else
       -Dhdfs:BOOL=OFF \
%endif
       -Dhttp:BOOL=ON \
%if %{?fedora}%{!?fedora:0} >= 21 || %{?rhel}%{!?rhel:0} >= 8
       -Dimt:BOOL=ON \
%else
       -Dimt:BOOL=OFF \
%endif
       -Djemalloc:BOOL=OFF \
       -Dkrb5:BOOL=ON \
       -Dldap:BOOL=ON \
       -Dlibcxx:BOOL=OFF \
       -Dmathmore:BOOL=ON \
       -Dmemory_termination:BOOL=OFF \
       -Dmemstat:BOOL=ON \
       -Dminuit2:BOOL=ON \
       -Dmonalisa:BOOL=OFF \
       -Dmysql:BOOL=ON \
       -Dodbc:BOOL=ON \
       -Dopengl:BOOL=ON \
       -Doracle:BOOL=OFF \
       -Dpch:BOOL=ON \
       -Dpgsql:BOOL=ON \
       -Dpythia6:BOOL=OFF \
%if %{pythia8}
       -Dpythia8:BOOL=ON \
%else
       -Dpythia8:BOOL=OFF \
%endif
       -Dpython:BOOL=ON \
       -Dpython3:BOOL=OFF \
       -Dqt:BOOL=ON \
       -Dqtgsi:BOOL=ON \
       -Dr:BOOL=ON \
       -Drfio:BOOL=ON \
       -Droofit:BOOL=ON \
       -Drpath:BOOL=OFF \
%if %{ruby}
       -Druby:BOOL=ON \
%else
       -Druby:BOOL=OFF \
%endif
       -Druntime_cxxmodules:BOOL=OFF \
       -Dsapdb:BOOL=OFF \
       -Dshadowpw:BOOL=ON \
       -Dshared:BOOL=ON \
       -Dsoversion:BOOL=ON \
       -Dsqlite:BOOL=ON \
       -Dsrp:BOOL=OFF \
       -Dssl:BOOL=ON \
       -Dtable:BOOL=ON \
       -Dtcmalloc:BOOL=OFF \
       -Dthread:BOOL=ON \
       -Dtmva:BOOL=ON \
       -Dunuran:BOOL=ON \
       -Dvc:BOOL=OFF \
       -Dvdt:BOOL=OFF \
       -Dveccore:BOOL=OFF \
       -Dvecgeom:BOOL=OFF \
       -Dx11:BOOL=ON \
       -Dxft:BOOL=ON \
       -Dxml:BOOL=ON \
%if %{xrootd}
       -Dxrootd:BOOL=ON \
%else
       -Dxrootd:BOOL=OFF \
%endif
       -Dfail-on-missing:BOOL=ON \
       -Dtesting:BOOL=ON \
       -Dclingtest:BOOL=OFF \
       -Dcoverage:BOOL=OFF \
       -Droottest:BOOL=OFF \
       -Drootbench:BOOL=OFF \
       ..

# Build PyROOT for python 3 (prep)
cp -pr bindings/pyroot bindings/python

make %{?_smp_mflags}

# Build PyROOT for python 3
mkdir python
mv CMakeFiles/Makefile2 CMakeFiles/Makefile2.save
sed 's!bindings/pyroot!bindings/python!g' CMakeFiles/Makefile2.save \
    > CMakeFiles/Makefile2
py2i=`pkg-config --cflags-only-I python2 | sed -e 's/-I//' -e 's/\s*$//'`
py2l=`pkg-config --libs-only-l python2 | sed -e 's/-l//' -e 's/\s*$//'`
py3i=`pkg-config --cflags-only-I python3 | sed -e 's/-I//' -e 's/\s*$//'`
py3l=`pkg-config --libs-only-l python3 | sed -e 's/-l//' -e 's/\s*$//'`
sed -e "s,${py2i},${py3i},g" -e "s,-l${py2l},-l${py3l},g" \
    -e "s,lib${py2l},lib${py3l},g" -e 's,%{__python},%{__python3},g' \
    -e 's,lib/libPyROOT,python/libPyROOT,g' \
    -e 's,lib/libJupyROOT,python/libJupyROOT,g' \
    -e 's!bindings/pyroot!bindings/python!g' -i `find bindings/python -type f`
make %{?_smp_mflags} -f bindings/python/Makefile PyROOT JupyROOT
mv CMakeFiles/Makefile2.save CMakeFiles/Makefile2

popd

%install
pushd builddir
make %{?_smp_mflags} install DESTDIR=%{buildroot}
popd

# Do emacs byte compilation
emacs -batch -no-site-file -f batch-byte-compile \
    %{buildroot}%{_emacs_sitelispdir}/%{name}/*.el

# Install desktop entry and icon
mkdir -p %{buildroot}%{_datadir}/applications
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/48x48/apps

cat > root.desktop << EOF
[Desktop Entry]
Name=Root
GenericName=Root
Comment=Numerical data analysis framework
Exec=root
Icon=root
Terminal=true
Type=Application
MimeType=application/x-root;
Categories=Utility;
Encoding=UTF-8
EOF

desktop-file-install --dir=%{buildroot}%{_datadir}/applications \
		     --vendor "" root.desktop
install -p -m 644 build/package/debian/root-system-bin.png \
    %{buildroot}%{_datadir}/icons/hicolor/48x48/apps/root.png

# Install mime type and icon
mkdir -p %{buildroot}%{_datadir}/mime/packages
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/48x48/mimetypes
install -p -m 644 build/package/debian/root-system-bin.sharedmimeinfo \
    %{buildroot}%{_datadir}/mime/packages/root.xml
install -p -m 644 build/package/debian/application-x-root.png \
    %{buildroot}%{_datadir}/icons/hicolor/48x48/mimetypes

# systemd unit files for services
mkdir -p %{buildroot}%{_unitdir}
install -p -m 644 %SOURCE3 %{buildroot}%{_unitdir}
install -p -m 644 %SOURCE4 %{buildroot}%{_unitdir}

# Move python cli helper to its own directory
mkdir -p %{buildroot}%{_datadir}/%{name}/cli
mv %{buildroot}%{_libdir}/%{name}/cmdLineUtils.py* \
   %{buildroot}%{_datadir}/%{name}/cli

# Move the python modules to sitearch/sitelib
mkdir -p %{buildroot}%{python2_sitearch}
mv %{buildroot}%{_libdir}/%{name}/libPyROOT.so.%{version} \
   %{buildroot}%{python2_sitearch}/libPyROOT.so
mv %{buildroot}%{_libdir}/%{name}/libJupyROOT.so.%{version} \
   %{buildroot}%{python2_sitearch}/libJupyROOT.so
mv %{buildroot}%{_libdir}/%{name}/*.py* %{buildroot}%{python2_sitearch}
rm %{buildroot}%{_libdir}/%{name}/JupyROOT/README.md
rm -rf %{buildroot}%{_libdir}/%{name}/JupyROOT/src
mv %{buildroot}%{_libdir}/%{name}/JupyROOT %{buildroot}%{python2_sitearch}
rm %{buildroot}%{_libdir}/%{name}/libJupyROOT.so.%{libversion}
rm %{buildroot}%{_libdir}/%{name}/libJupyROOT.so

mkdir -p %{buildroot}%{python2_sitelib}
mv %{buildroot}%{_libdir}/%{name}/JsMVA %{buildroot}%{python2_sitelib}

tmpdir=`mktemp -d`

%if %{?fedora}%{!?fedora:0} || %{?rhel}%{!?rhel:0} >= 8
DESTDIR=$tmpdir cmake -P builddir/bindings/python/cmake_install.cmake
%else
DESTDIR=$tmpdir cmake3 -P builddir/bindings/python/cmake_install.cmake
%endif

mkdir -p %{buildroot}%{python3_sitearch}
mv $tmpdir%{_libdir}/%{name}/libPyROOT.so.%{version} \
   %{buildroot}%{python3_sitearch}/libPyROOT%{py3soabi}.so
mv $tmpdir%{_libdir}/%{name}/libJupyROOT.so.%{version} \
   %{buildroot}%{python3_sitearch}/libJupyROOT.so
mv $tmpdir%{_libdir}/%{name}/*.py %{buildroot}%{python3_sitearch}
mv $tmpdir%{_libdir}/%{name}/__pycache__ %{buildroot}%{python3_sitearch}
rm $tmpdir%{_libdir}/%{name}/JupyROOT/README.md
rm -rf $tmpdir%{_libdir}/%{name}/JupyROOT/src
mv $tmpdir%{_libdir}/%{name}/JupyROOT %{buildroot}%{python3_sitearch}
rm $tmpdir%{_libdir}/%{name}/libJupyROOT.so.%{libversion}
rm $tmpdir%{_libdir}/%{name}/libJupyROOT.so

mkdir -p %{buildroot}%{python3_sitelib}
mv $tmpdir%{_libdir}/%{name}/JsMVA %{buildroot}%{python3_sitelib}

rm -rf $tmpdir

%if %{ruby}
# The Ruby interface library must be in two places
mkdir -p %{buildroot}%{ruby_vendorarchdir}
mv %{buildroot}%{_libdir}/%{name}/libRuby.so.%{version} \
   %{buildroot}%{ruby_vendorarchdir}/libRuby.so
ln -s ..`sed 's!%{_libdir}!!' <<< %{ruby_vendorarchdir}`/libRuby.so \
   %{buildroot}%{_libdir}/%{name}/libRuby.so.%{version}
%endif

# Put jupyter stuff in the right places
mkdir -p %{buildroot}%{_datadir}/jupyter/kernels

cp -pr %{buildroot}%{_datadir}/%{name}/notebook/kernels/root \
   %{buildroot}%{_datadir}/jupyter/kernels/python2-jupyroot
sed -e 's/ROOT C++/& (Python 2)/' -e 's!python!/usr/bin/python2!' \
    -i %{buildroot}%{_datadir}/jupyter/kernels/python2-jupyroot/kernel.json

cp -pr %{buildroot}%{_datadir}/%{name}/notebook/kernels/root \
   %{buildroot}%{_datadir}/jupyter/kernels/python%{python3_pkgversion}-jupyroot
sed -e 's/ROOT C++/& (Python 3)/' -e 's!python!/usr/bin/python3!' \
    -i %{buildroot}%{_datadir}/jupyter/kernels/python%{python3_pkgversion}-jupyroot/kernel.json

rm -rf %{buildroot}%{_datadir}/%{name}/notebook/custom
rm -rf %{buildroot}%{_datadir}/%{name}/notebook/html
rm -rf %{buildroot}%{_datadir}/%{name}/notebook/kernels

ln -s /usr/share/javascript/jsroot %{buildroot}%{_datadir}/%{name}/notebook

# Replace the rootnb.exe wrapper with a simpler one
cat > %{buildroot}%{_bindir}/rootnb.exe << EOF
#! /bin/sh
if [ -z "\$(type jupyter 2>/dev/null)" ] ; then
   echo jupyter not found in path. Exiting.
   exit 1
fi
if [ -z "\$(type jupyter-notebook 2>/dev/null)" ] ; then
   echo jupyter-notebook not found in path. Exiting.
   exit 1
fi
rm -rf ~/.rootnb
jupyter notebook
EOF

# These should be in PATH
mv %{buildroot}%{_datadir}/%{name}/proof/utils/pq2/pq2* %{buildroot}%{_bindir}

# Avoid /usr/bin/env shebangs (and adapt cli to cmdLineUtils location)
sed -e 's!/usr/bin/env bash!/bin/bash!' -i %{buildroot}%{_bindir}/root-config
sed -e 's!/usr/bin/env python!/usr/bin/python!' \
    -e '/import sys/d' \
    -e '/import cmdLineUtils/iimport sys' \
    -e '/import cmdLineUtils/isys.path.insert(0, "%{_datadir}/%{name}/cli")' \
    -i %{buildroot}%{_bindir}/rootbrowse \
       %{buildroot}%{_bindir}/rootcp \
       %{buildroot}%{_bindir}/rooteventselector \
       %{buildroot}%{_bindir}/rootls \
       %{buildroot}%{_bindir}/rootmkdir \
       %{buildroot}%{_bindir}/rootmv \
       %{buildroot}%{_bindir}/rootprint \
       %{buildroot}%{_bindir}/rootrm \
       %{buildroot}%{_bindir}/rootslimtree
sed -e '/^\#!/d' \
    -i %{buildroot}%{_datadir}/%{name}/cli/cmdLineUtils.py \
       %{buildroot}%{python2_sitearch}/JupyROOT/kernel/rootkernel.py \
       %{buildroot}%{python3_sitearch}/JupyROOT/kernel/rootkernel.py
sed -e 's!/usr/bin/env python!/usr/bin/python!' \
    -i %{buildroot}%{_bindir}/rootdrawtree \
       %{buildroot}%{_datadir}/%{name}/dictpch/makepch.py \
       %{buildroot}%{_pkgdocdir}/tutorials/histfactory/example.py \
       %{buildroot}%{_pkgdocdir}/tutorials/histfactory/makeQuickModel.py \
       %{buildroot}%{_pkgdocdir}/tutorials/tmva/keras/ApplicationClassificationKeras.py \
       %{buildroot}%{_pkgdocdir}/tutorials/tmva/keras/ApplicationRegressionKeras.py \
       %{buildroot}%{_pkgdocdir}/tutorials/tmva/keras/ClassificationKeras.py \
       %{buildroot}%{_pkgdocdir}/tutorials/tmva/keras/GenerateModel.py \
       %{buildroot}%{_pkgdocdir}/tutorials/tmva/keras/MulticlassKeras.py \
       %{buildroot}%{_pkgdocdir}/tutorials/tmva/keras/RegressionKeras.py

# Remove some junk
rm %{buildroot}%{_datadir}/%{name}/daemons/*.plist
rm %{buildroot}%{_datadir}/%{name}/daemons/*.rc.d
rm %{buildroot}%{_datadir}/%{name}/daemons/*.xinetd
rm %{buildroot}%{_datadir}/%{name}/daemons/README
rm %{buildroot}%{_datadir}/%{name}/hostcert.conf
rm %{buildroot}%{_datadir}/%{name}/proof/*.sample
rm -rf %{buildroot}%{_datadir}/%{name}/proof/utils
rm %{buildroot}%{_datadir}/%{name}/root.desktop
rm %{buildroot}%{_datadir}/%{name}/system.plugins-ios
rm %{buildroot}%{_bindir}/setenvwrap.csh
rm %{buildroot}%{_bindir}/setxrd*
rm %{buildroot}%{_bindir}/thisroot*
rm %{buildroot}%{_mandir}/man1/g2rootold.1
rm %{buildroot}%{_mandir}/man1/genmap.1
rm %{buildroot}%{_mandir}/man1/proofserva.1
rm %{buildroot}%{_mandir}/man1/roota.1
rm %{buildroot}%{_mandir}/man1/setup-pq2.1
%if %{xrootd} == 0
rm %{buildroot}%{_mandir}/man1/xproofd.1
%endif
rm %{buildroot}%{_includedir}/%{name}/*.cw
rm %{buildroot}%{_includedir}/%{name}/*.pri
rm %{buildroot}%{_pkgdocdir}/INSTALL
rm %{buildroot}%{_pkgdocdir}/README.ALIEN
rm %{buildroot}%{_pkgdocdir}/README.MONALISA

# Only used on Windows
rm %{buildroot}%{_datadir}/%{name}/macros/fileopen.C

# Remove plugin definitions for non-built and obsolete plugins
pushd %{buildroot}%{_datadir}/%{name}/plugins
rm TAFS/P010_TAFS.C
rm TDataProgressDialog/P010_TDataProgressDialog.C
rm TDataSetManager/P020_TDataSetManagerAliEn.C
rm TFile/P030_TCastorFile.C
rm TFile/P060_TChirpFile.C
rm TFile/P070_TAlienFile.C
%if %{hadoop} == 0
rm TFile/P110_THDFSFile.C
%endif
rm TGLManager/P020_TGWin32GLManager.C
rm TGLManager/P030_TGOSXGLManager.C
rm TGrid/P010_TAlien.C
rm TGrid/P020_TGLite.C
rm TImagePlugin/P010_TASPluginGS.C
rm TSQLServer/P030_TSapDBServer.C
rm TSQLServer/P040_TOracleServer.C
rm TSystem/P030_TAlienSystem.C
%if %{hadoop} == 0
rm TSystem/P060_THDFSSystem.C
%endif
rm TViewerX3D/P020_TQtViewerX3D.C
rm TVirtualGeoConverter/P010_TGeoVGConverter.C
rm TVirtualGLImp/P020_TGWin32GL.C
rm TVirtualMonitoringWriter/P010_TMonaLisaWriter.C
rm TVirtualX/P030_TGWin32.C
rm TVirtualX/P050_TGQuartz.C
%if %{xrootd} == 0
rm TFile/P100_TXNetFile.C
rm TFileStager/P010_TXNetFileStager.C
rm TProofMgr/P010_TXProofMgr.C
rm TProofServ/P010_TXProofServ.C
rm TSlave/P010_TXSlave.C
rm TSystem/P040_TXNetSystem.C
%endif
rmdir TAFS
rmdir TDataProgressDialog
rmdir TGrid
rmdir TImagePlugin
rmdir TVirtualGeoConverter
popd

# Replace bundled jsroot with symlink to system version
rm -rf %{buildroot}%{_datadir}/%{name}/http
ln -s /usr/share/javascript/jsroot %{buildroot}%{_datadir}/%{name}/http

# Create ldconfig configuration
mkdir -p %{buildroot}%{_sysconfdir}/ld.so.conf.d
echo %{_libdir}/%{name} > \
     %{buildroot}%{_sysconfdir}/ld.so.conf.d/%{name}-%{_arch}.conf

# Rename to avoid name clashes
cp -p interpreter/llvm/src/CREDITS.TXT interpreter/llvm/src/llvm-CREDITS.TXT
cp -p interpreter/llvm/src/LICENSE.TXT interpreter/llvm/src/llvm-LICENSE.TXT
cp -p interpreter/llvm/src/README.txt interpreter/llvm/src/llvm-README.txt

# Generate documentation
pushd documentation/doxygen
ln -s ../../files files
# Create the py-hsimple.root file in advance (needed as input)
ROOTIGNOREPREFIX=1 PATH=${PWD}/../../builddir/bin:${PATH} \
    ROOTSYS=${PWD}/../../builddir \
    LD_LIBRARY_PATH=${PWD}/../../builddir/lib \
    PYTHONPATH=${PWD}/../../builddir/lib \
    python ../../tutorials/pyroot/hsimple.py
ROOTIGNOREPREFIX=1 PATH=${PWD}/../../builddir/bin:${PATH} \
    ROOTSYS=${PWD}/../../builddir \
    LD_LIBRARY_PATH=${PWD}/../../builddir/lib \
    PYTHONPATH=${PWD}/../../builddir/lib \
    make DOXYGEN_OUTPUT_DIRECTORY=${PWD}/doc
mv doc/html %{buildroot}%{_pkgdocdir}/html
popd

# Create includelist files ...
for f in `find builddir -name cmake_install.cmake -a '!' -path '*/llvm/*'` ; do
    l=`sed 's!builddir/\(.*\)/cmake_install.cmake!includelist-\1!' <<< $f`
    l=`tr / - <<< $l`
    tmpdir=`mktemp -d`
%if %{?fedora}%{!?fedora:0} || %{?rhel}%{!?rhel:0} >= 8
    DESTDIR=$tmpdir cmake -DCMAKE_INSTALL_COMPONENT=headers -P $f > /dev/null
%else
    DESTDIR=$tmpdir cmake3 -DCMAKE_INSTALL_COMPONENT=headers -P $f > /dev/null
%endif
    ( cd $tmpdir ; find . -type f -a '!' -name '*.cw' -a '!' -name '*.pri') | \
	sort | sed 's!^\.!!' > $l
    rm -rf $tmpdir
done

# ... and merge some of them
cat includelist-core-{[^mw],m[^au]}* > includelist-core
cat includelist-geom-geom* > includelist-geom
cat includelist-roofit-roo* > includelist-roofit
cat includelist-gui-qt* > includelist-gui-qt
cat includelist-graf2d-x11ttf >> includelist-graf2d-x11
cat includelist-gui-guihtml >> includelist-gui-gui
cat includelist-io-xmlparser >> includelist-io-xml
cat includelist-proof-proofplayer >> includelist-proof-proof
cat includelist-net-netx* > includelist-netx

%check
pushd builddir
pushd test
ln -s ../../files files
popd
pushd runtutorials
ln -s ../../files files
ln -sf ../../files/tutorials/tdf014_CsvDataSource_MuRun2010B.csv
popd
# Exclude some tests that can not be run
#
# - test-stressIOPlugins-*
#   requires network access (by design since they test the remote file IO)
#
# - tutorial-dataframe-tdf101_h1Analysis
# - tutorial-tree-run_h1analysis
# - tutorial-multicore-imt001_parBranchProcessing
# - tutorial-multicore-mp103_processSelector
# - tutorial-multicore-mp104_processH1
# - tutorial-multicore-mp105_processEntryList
#   requires network access: http://root.cern.ch/files/h1/
#
# - tutorial-multicore-imt101_parTreeProcessing
#   requires input data: http://root.cern.ch/files/tp_process_imt.root (707 MB)
#
# - tutorial-pythia-pythia8
#   sometimes times out
excluded="test-stressIOPlugins-.*|tutorial-dataframe-tdf101_h1Analysis|tutorial-tree-run_h1analysis|tutorial-multicore-imt001_parBranchProcessing|tutorial-multicore-mp103_processSelector|tutorial-multicore-mp104_processH1|tutorial-multicore-mp105_processEntryList|tutorial-multicore-imt101_parTreeProcessing|tutorial-pythia-pythia8"

%ifarch %{arm}
# Tests failing on arm
# https://sft.its.cern.ch/jira/browse/ROOT-8500
# - mathcore-testMinim
# - minuit2-testMinimizer
# - test-minexam
# - test-stressfit (but -interpreted works)
# Tests failing on arm on Fedora <= 27
# - test-stressiterators-interpreted
# - tutorial-hist-sparsehist
# - tutorial-multicore-mt303_AsyncSimple
# - tutorial-multicore-mt304_AsyncNested
# - tutorial-multicore-mt305_TFuture
# - tutorial-r-*
excluded="${excluded}|mathcore-testMinim|minuit2-testMinimizer|test-minexam|test-stressfit"
%if %{?fedora}%{!?fedora:0} <= 27 && %{?rhel}%{!?rhel:0} <= 7
excluded="${excluded}|test-stressiterators-interpreted|tutorial-hist-sparsehist|tutorial-multicore-mt303_AsyncSimple|tutorial-multicore-mt304_AsyncNested|tutorial-multicore-mt305_TFuture|tutorial-r-.*"
%endif
%endif

%ifarch ppc64
# Tests failing on ppc64
# https://sft.its.cern.ch/jira/browse/ROOT-6434
# - test-stresshistogram[-interpreted]
# - test-stressroostats[-interpreted]
# - test-stresshistofit[-interpreted]
# - tutorial-roofit-rf511_wsfactory_basic
# - tutorial-roostats-rs102_hypotestwithshapes (work on EPEL 7)
# - tutorial-roostats-rs701_BayesianCalculator
# - tutorial-dataframe-tdf006_ranges-py
excluded="${excluded}|test-stresshistogram|test-stressroostats|test-stresshistofit|tutorial-roofit-rf511_wsfactory_basic|tutorial-roostats-rs102_hypotestwithshapes|tutorial-roostats-rs701_BayesianCalculator|tutorial-dataframe-tdf006_ranges-py"
%endif

%ifarch ppc64le
# Tests failing on ppc64le
# - test-stresshistogram[-interpreted]
excluded="${excluded}|test-stresshistogram"
%endif

make test ARGS="%{?_smp_mflags} --output-on-failure -E \"${excluded}\""
popd

%if %{?rhel}%{!?rhel:0} == 7
%post
touch --no-create %{_datadir}/icons/hicolor >/dev/null 2>&1 || :
update-desktop-database >/dev/null 2>&1 || :
update-mime-database %{_datadir}/mime >/dev/null 2>&1 || :

%postun
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor >/dev/null 2>&1
    gtk-update-icon-cache %{_datadir}/icons/hicolor >/dev/null 2>&1 || :
fi
update-desktop-database >/dev/null 2>&1 || :
update-mime-database %{_datadir}/mime >/dev/null 2>&1 || :

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor >/dev/null 2>&1 || :
%endif

%pre rootd
# Remove old init config when systemd is used
/sbin/chkconfig --del rootd >/dev/null 2>&1 || :

%post rootd
%systemd_post rootd.service

%preun rootd
%systemd_preun rootd.service

%postun rootd
%systemd_postun_with_restart rootd.service

%pre proofd
# Remove old init config when systemd is used
/sbin/chkconfig --del proofd >/dev/null 2>&1 || :

%post proofd
%systemd_post proofd.service

%preun proofd
%systemd_preun proofd.service

%postun proofd
%systemd_postun_with_restart proofd.service

%post -n python2-%{name}
if [ -r /var/lib/alternatives/libPyROOT.so ] ; then
    grep -q %{_libdir}/%{name}/libPyROOT.so.%{version} \
	/var/lib/alternatives/libPyROOT.so || \
    sed 's!\(%{_libdir}/%{name}/libPyROOT\.so\.\).*!\1%{version}!' \
	-i /var/lib/alternatives/libPyROOT.so
    for alt in `grep python2 /var/lib/alternatives/libPyROOT.so` ; do
	if [ "$alt" != "%{python2_sitearch}/libPyROOT.so" ] ; then
	    %{_sbindir}/update-alternatives --remove libPyROOT.so $alt
	fi
    done
fi
%{_sbindir}/update-alternatives --install \
    %{_libdir}/%{name}/libPyROOT.so.%{version} \
    libPyROOT.so %{python2_sitearch}/libPyROOT.so 20
/sbin/ldconfig

%preun -n python2-%{name}
if [ $1 = 0 ]; then
    %{_sbindir}/update-alternatives --remove \
	libPyROOT.so %{python2_sitearch}/libPyROOT.so
fi

%postun -n python2-%{name} -p /sbin/ldconfig

%triggerpostun -n python2-%{name} -- %{name}-python
# Uninstalling the old %{name}-python will remove the alternatives
# for python2-%{name} - put them back in this triggerpostun script
%{_sbindir}/update-alternatives --install \
    %{_libdir}/%{name}/libPyROOT.so.%{version} \
    libPyROOT.so %{python2_sitearch}/libPyROOT.so 20
/sbin/ldconfig

%post -n python%{python3_pkgversion}-%{name}
if [ -r /var/lib/alternatives/libPyROOT.so ] ; then
    grep -q %{_libdir}/%{name}/libPyROOT.so.%{version} \
	/var/lib/alternatives/libPyROOT.so || \
    sed 's!\(%{_libdir}/%{name}/libPyROOT\.so\.\).*!\1%{version}!' \
	-i /var/lib/alternatives/libPyROOT.so
    for alt in `grep python3 /var/lib/alternatives/libPyROOT.so` ; do
	if [ "$alt" != "%{python3_sitearch}/libPyROOT%{py3soabi}.so" ] ; then
	    %{_sbindir}/update-alternatives --remove libPyROOT.so $alt
	fi
    done
fi
%{_sbindir}/update-alternatives --install \
    %{_libdir}/%{name}/libPyROOT.so.%{version} \
    libPyROOT.so %{python3_sitearch}/libPyROOT%{py3soabi}.so 10
/sbin/ldconfig

%preun -n python%{python3_pkgversion}-%{name}
if [ $1 = 0 ]; then
    %{_sbindir}/update-alternatives --remove \
	libPyROOT.so %{python3_sitearch}/libPyROOT%{py3soabi}.so
fi

%postun -n python%{python3_pkgversion}-%{name} -p /sbin/ldconfig

%triggerpostun -n python%{python3_pkgversion}-%{name} -- %{name}-python%{python3_pkgversion}
# Uninstalling the old %{name}-python%{python3_pkgversion} will remove the alternatives
# for python%{python3_pkgversion}-%{name} - put them back in this triggerpostun script
%{_sbindir}/update-alternatives --install \
    %{_libdir}/%{name}/libPyROOT.so.%{version} \
    libPyROOT.so %{python3_sitearch}/libPyROOT%{py3soabi}.so 10
/sbin/ldconfig

%post notebook
mkdir -p /etc/jupyter
if [ -e /etc/jupyter/jupyter_notebook_config.py ] ; then
    sed '/Extra static path for JupyROOT - start/','/Extra static path for JupyROOT - end/'d -i /etc/jupyter/jupyter_notebook_config.py
fi
cat << EOF >> /etc/jupyter/jupyter_notebook_config.py
# Extra static path for JupyROOT - start - do not remove this line
c.NotebookApp.extra_static_paths.append('%{_datadir}/%{name}/notebook')
# Extra static path for JupyROOT - end - do not remove this line
EOF

%postun notebook
if [ $1 -eq 0 ] ; then
    if [ -e /etc/jupyter/jupyter_notebook_config.py ] ; then
	sed '/Extra static path for JupyROOT - start/','/Extra static path for JupyROOT - end/'d -i /etc/jupyter/jupyter_notebook_config.py
	if [ ! -s /etc/jupyter/jupyter_notebook_config.py ] ; then
	    rm /etc/jupyter/jupyter_notebook_config.py
	    rmdir /etc/jupyter 2>/dev/null || :
	fi
    fi
fi

%post core -p /sbin/ldconfig
%postun core -p /sbin/ldconfig
%post multiproc -p /sbin/ldconfig
%postun multiproc -p /sbin/ldconfig
%post cling -p /sbin/ldconfig
%postun cling -p /sbin/ldconfig
%if %{ruby}
%post ruby -p /sbin/ldconfig
%postun ruby -p /sbin/ldconfig
%endif
%post r -p /sbin/ldconfig
%postun r -p /sbin/ldconfig
%post r-tools -p /sbin/ldconfig
%postun r-tools -p /sbin/ldconfig
%post genetic -p /sbin/ldconfig
%postun genetic -p /sbin/ldconfig
%post geom -p /sbin/ldconfig
%postun geom -p /sbin/ldconfig
%post gdml -p /sbin/ldconfig
%postun gdml -p /sbin/ldconfig
%if %{oce}
%post geocad -p /sbin/ldconfig
%postun geocad -p /sbin/ldconfig
%endif
%post graf -p /sbin/ldconfig
%postun graf -p /sbin/ldconfig
%post graf-asimage -p /sbin/ldconfig
%postun graf-asimage -p /sbin/ldconfig
%post graf-fitsio -p /sbin/ldconfig
%postun graf-fitsio -p /sbin/ldconfig
%post graf-gpad -p /sbin/ldconfig
%postun graf-gpad -p /sbin/ldconfig
%post graf-gviz -p /sbin/ldconfig
%postun graf-gviz -p /sbin/ldconfig
%post graf-postscript -p /sbin/ldconfig
%postun graf-postscript -p /sbin/ldconfig
%post graf-qt -p /sbin/ldconfig
%postun graf-qt -p /sbin/ldconfig
%post graf-x11 -p /sbin/ldconfig
%postun graf-x11 -p /sbin/ldconfig
%post graf3d -p /sbin/ldconfig
%postun graf3d -p /sbin/ldconfig
%post graf3d-eve -p /sbin/ldconfig
%postun graf3d-eve -p /sbin/ldconfig
%post graf3d-gl -p /sbin/ldconfig
%postun graf3d-gl -p /sbin/ldconfig
%post graf3d-gviz3d -p /sbin/ldconfig
%postun graf3d-gviz3d -p /sbin/ldconfig
%post graf3d-x3d -p /sbin/ldconfig
%postun graf3d-x3d -p /sbin/ldconfig
%post gui -p /sbin/ldconfig
%postun gui -p /sbin/ldconfig
%post gui-fitpanel -p /sbin/ldconfig
%postun gui-fitpanel -p /sbin/ldconfig
%post gui-ged -p /sbin/ldconfig
%postun gui-ged -p /sbin/ldconfig
%post guibuilder -p /sbin/ldconfig
%postun guibuilder -p /sbin/ldconfig
%post gui-qt -p /sbin/ldconfig
%postun gui-qt -p /sbin/ldconfig
%post gui-recorder -p /sbin/ldconfig
%postun gui-recorder -p /sbin/ldconfig
%if %{root7}
%post gui-canvaspainter -p /sbin/ldconfig
%postun gui-canvaspainter -p /sbin/ldconfig
%post gui-webdisplay -p /sbin/ldconfig
%postun gui-webdisplay -p /sbin/ldconfig
%endif
%post hbook -p /sbin/ldconfig
%postun hbook -p /sbin/ldconfig
%post hist -p /sbin/ldconfig
%postun hist -p /sbin/ldconfig
%if %{root7}
%post hist-draw -p /sbin/ldconfig
%postun hist-draw -p /sbin/ldconfig
%endif
%post hist-painter -p /sbin/ldconfig
%postun hist-painter -p /sbin/ldconfig
%post spectrum -p /sbin/ldconfig
%postun spectrum -p /sbin/ldconfig
%post spectrum-painter -p /sbin/ldconfig
%postun spectrum-painter -p /sbin/ldconfig
%post hist-factory -p /sbin/ldconfig
%postun hist-factory -p /sbin/ldconfig
%post html -p /sbin/ldconfig
%postun html -p /sbin/ldconfig
%post io -p /sbin/ldconfig
%postun io -p /sbin/ldconfig
%post io-dcache -p /sbin/ldconfig
%postun io-dcache -p /sbin/ldconfig
%post io-gfal -p /sbin/ldconfig
%postun io-gfal -p /sbin/ldconfig
%if %{hadoop}
%post io-hdfs -p /sbin/ldconfig
%postun io-hdfs -p /sbin/ldconfig
%endif
%post io-rfio -p /sbin/ldconfig
%postun io-rfio -p /sbin/ldconfig
%post io-sql -p /sbin/ldconfig
%postun io-sql -p /sbin/ldconfig
%post io-xml -p /sbin/ldconfig
%postun io-xml -p /sbin/ldconfig
%post foam -p /sbin/ldconfig
%postun foam -p /sbin/ldconfig
%post fftw -p /sbin/ldconfig
%postun fftw -p /sbin/ldconfig
%post fumili -p /sbin/ldconfig
%postun fumili -p /sbin/ldconfig
%post genvector -p /sbin/ldconfig
%postun genvector -p /sbin/ldconfig
%post mathcore -p /sbin/ldconfig
%postun mathcore -p /sbin/ldconfig
%post mathmore -p /sbin/ldconfig
%postun mathmore -p /sbin/ldconfig
%post matrix -p /sbin/ldconfig
%postun matrix -p /sbin/ldconfig
%post minuit -p /sbin/ldconfig
%postun minuit -p /sbin/ldconfig
%post minuit2 -p /sbin/ldconfig
%postun minuit2 -p /sbin/ldconfig
%post mlp -p /sbin/ldconfig
%postun mlp -p /sbin/ldconfig
%post physics -p /sbin/ldconfig
%postun physics -p /sbin/ldconfig
%post quadp -p /sbin/ldconfig
%postun quadp -p /sbin/ldconfig
%post smatrix -p /sbin/ldconfig
%postun smatrix -p /sbin/ldconfig
%post splot -p /sbin/ldconfig
%postun splot -p /sbin/ldconfig
%post unuran -p /sbin/ldconfig
%postun unuran -p /sbin/ldconfig
%post memstat -p /sbin/ldconfig
%postun memstat -p /sbin/ldconfig
%post table -p /sbin/ldconfig
%postun table -p /sbin/ldconfig
%post montecarlo-eg -p /sbin/ldconfig
%postun montecarlo-eg -p /sbin/ldconfig
%if %{pythia8}
%post montecarlo-pythia8 -p /sbin/ldconfig
%postun montecarlo-pythia8 -p /sbin/ldconfig
%endif
%post montecarlo-vmc -p /sbin/ldconfig
%postun montecarlo-vmc -p /sbin/ldconfig
%post net -p /sbin/ldconfig
%postun net -p /sbin/ldconfig
%post net-rpdutils -p /sbin/ldconfig
%postun net-rpdutils -p /sbin/ldconfig
%post net-bonjour -p /sbin/ldconfig
%postun net-bonjour -p /sbin/ldconfig
%post net-auth -p /sbin/ldconfig
%postun net-auth -p /sbin/ldconfig
%post net-davix -p /sbin/ldconfig
%postun net-davix -p /sbin/ldconfig
%post net-globus -p /sbin/ldconfig
%postun net-globus -p /sbin/ldconfig
%post net-krb5 -p /sbin/ldconfig
%postun net-krb5 -p /sbin/ldconfig
%post net-ldap -p /sbin/ldconfig
%postun net-ldap -p /sbin/ldconfig
%post net-http -p /sbin/ldconfig
%postun net-http -p /sbin/ldconfig

%pretrans net-http -p <lua>
path = "%{_datadir}/%{name}/http"
st = posix.stat(path)
if st and st.type == "directory" then
  os.execute("rm -rf " .. path)
end

%if %{xrootd}
%post netx -p /sbin/ldconfig
%postun netx -p /sbin/ldconfig
%endif
%post proof -p /sbin/ldconfig
%postun proof -p /sbin/ldconfig
%post proof-sessionviewer -p /sbin/ldconfig
%postun proof-sessionviewer -p /sbin/ldconfig
%if %{xrootd}
%post xproof -p /sbin/ldconfig
%postun xproof -p /sbin/ldconfig
%endif
%post roofit -p /sbin/ldconfig
%postun roofit -p /sbin/ldconfig
%post sql-mysql -p /sbin/ldconfig
%postun sql-mysql -p /sbin/ldconfig
%post sql-odbc -p /sbin/ldconfig
%postun sql-odbc -p /sbin/ldconfig
%post sql-sqlite -p /sbin/ldconfig
%postun sql-sqlite -p /sbin/ldconfig
%post sql-pgsql -p /sbin/ldconfig
%postun sql-pgsql -p /sbin/ldconfig
%post tmva -p /sbin/ldconfig
%postun tmva -p /sbin/ldconfig
%post tmva-python -p /sbin/ldconfig
%postun tmva-python -p /sbin/ldconfig
%post tmva-r -p /sbin/ldconfig
%postun tmva-r -p /sbin/ldconfig
%post tmva-gui -p /sbin/ldconfig
%postun tmva-gui -p /sbin/ldconfig
%post tree -p /sbin/ldconfig
%postun tree -p /sbin/ldconfig
%post tree-player -p /sbin/ldconfig
%postun tree-player -p /sbin/ldconfig
%post tree-viewer -p /sbin/ldconfig
%postun tree-viewer -p /sbin/ldconfig
%post unfold -p /sbin/ldconfig
%postun unfold -p /sbin/ldconfig

%files
%{_bindir}/hadd
%{_bindir}/root
%{_bindir}/root.exe
%{_bindir}/rootn.exe
%{_bindir}/roots
%{_bindir}/roots.exe
%{_bindir}/ssh2rpd
%{_mandir}/man1/hadd.1*
%{_mandir}/man1/root.1*
%{_mandir}/man1/root.exe.1*
%{_mandir}/man1/rootn.exe.1*
%{_mandir}/man1/roots.exe.1*
%{_mandir}/man1/ssh2rpd.1*
%{_datadir}/applications/root.desktop
%{_datadir}/icons/hicolor/48x48/apps/root.png
%{_datadir}/icons/hicolor/48x48/mimetypes/application-x-root.png
%{_datadir}/mime/packages/root.xml
%dir %{_emacs_sitelispdir}/%{name}
%{_emacs_sitelispdir}/%{name}/*.elc
%{_emacs_sitelispdir}/%{name}/*.el

%files icons
%{_datadir}/%{name}/icons

%files fonts
%{_datadir}/%{name}/fonts

%files core -f includelist-core
%{_bindir}/memprobe
%{_bindir}/rmkdepend
%{_bindir}/root-config
%{_mandir}/man1/memprobe.1*
%{_mandir}/man1/rmkdepend.1*
%{_mandir}/man1/root-config.1*
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/libCore.*
%{_libdir}/%{name}/libImt.*
%{_libdir}/%{name}/libNew.*
%{_libdir}/%{name}/libRint.*
%{_libdir}/%{name}/libThread.*
%{_libdir}/%{name}/lib*Dict.*
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/allDict.cxx.pch
%{_datadir}/%{name}/class.rules
%{_datadir}/%{name}/gdb-backtrace.sh
%{_datadir}/%{name}/gitinfo.txt
%{_datadir}/%{name}/helgrind-root.supp
%{_datadir}/%{name}/Makefile.arch
%{_datadir}/%{name}/root.mimes
%{_datadir}/%{name}/system.rootauthrc
%{_datadir}/%{name}/system.rootdaemonrc
%{_datadir}/%{name}/system.rootrc
%{_datadir}/%{name}/valgrind-root-python.supp
%{_mandir}/man1/system.rootdaemonrc.1*
%dir %{_datadir}/%{name}/cmake
%{_datadir}/%{name}/cmake/*.cmake
%dir %{_datadir}/%{name}/cmake/modules
%{_datadir}/%{name}/cmake/modules/*.cmake
%{_datadir}/%{name}/cmake/modules/*.cmake.in
%dir %{_datadir}/%{name}/macros
%{_datadir}/%{name}/macros/Dialogs.C
%dir %{_datadir}/%{name}/plugins
%dir %{_datadir}/%{name}/plugins/*
%dir %{_includedir}/%{name}
%{_includedir}/%{name}/RConfigOptions.h
%{_includedir}/%{name}/RConfigure.h
%{_includedir}/%{name}/RGitCommit.h
%{_includedir}/%{name}/compiledata.h
%{_includedir}/%{name}/module.modulemap
%dir %{_includedir}/%{name}/Math
%dir %{_includedir}/%{name}/ROOT
%{_datadir}/aclocal/root.m4
%config(noreplace) %{_sysconfdir}/ld.so.conf.d/%{name}-%{_arch}.conf
%dir %{_pkgdocdir}
# CREDITS and LICENSE are used at runtime by the .credits and .license commands
# They therefore should not be marked doc.
%{_pkgdocdir}/CREDITS
%{_pkgdocdir}/LICENSE
%doc %{_pkgdocdir}/README
%doc %{_pkgdocdir}/ReleaseNotes
%license LICENSE

%files multiproc -f includelist-core-multiproc
%{_libdir}/%{name}/libMultiProc.*
%{_libdir}/%{name}/libMultiProc_rdict.pcm

%files cling
%{_bindir}/genreflex
%{_bindir}/rootcint
%{_bindir}/rootcling
%{_libdir}/%{name}/libCling.*
%{_datadir}/%{name}/cling
%{_datadir}/%{name}/dictpch
%doc interpreter/cling/CREDITS.txt
%doc interpreter/cling/README.md
%license interpreter/cling/LICENSE.TXT
%doc interpreter/llvm/src/llvm-CREDITS.TXT
%doc interpreter/llvm/src/llvm-README.txt
%license interpreter/llvm/src/llvm-LICENSE.TXT

%files doc
%doc %{_pkgdocdir}/html

%files tutorial
%doc %{_pkgdocdir}/test
%doc %{_pkgdocdir}/tutorials

%files proofd
%{_bindir}/proofd
%{_bindir}/proofserv
%{_bindir}/proofserv.exe
%{_bindir}/xpdtest
%{_mandir}/man1/proofd.1*
%{_mandir}/man1/proofserv.1*
%{_mandir}/man1/xpdtest.1*
%{_unitdir}/proofd.service

%files rootd
%{_bindir}/rootd
%{_mandir}/man1/rootd.1*
%{_unitdir}/rootd.service

%files -n python2-%{name} -f includelist-bindings-pyroot
%{_libdir}/%{name}/libPyROOT.rootmap
%{_libdir}/%{name}/libPyROOT.so
%{_libdir}/%{name}/libPyROOT.so.%{libversion}
%ghost %{_libdir}/%{name}/libPyROOT.so.%{version}
%{_libdir}/%{name}/libPyROOT_rdict.pcm
%{python2_sitearch}/libPyROOT.so
%{python2_sitearch}/ROOT.py*
%{python2_sitearch}/cppyy.py*
%{python2_sitearch}/_pythonization.py*

%files -n python%{python3_pkgversion}-%{name} -f includelist-bindings-pyroot
%{_libdir}/%{name}/libPyROOT.rootmap
%{_libdir}/%{name}/libPyROOT.so
%{_libdir}/%{name}/libPyROOT.so.%{libversion}
%ghost %{_libdir}/%{name}/libPyROOT.so.%{version}
%{_libdir}/%{name}/libPyROOT_rdict.pcm
%{python3_sitearch}/libPyROOT%{py3soabi}.so
%{python3_sitearch}/ROOT.py
%{python3_sitearch}/cppyy.py
%{python3_sitearch}/_pythonization.py
%{python3_sitearch}/__pycache__

%files -n python2-jupyroot
%{python2_sitearch}/JupyROOT
%{python2_sitearch}/libJupyROOT.so
%{_datadir}/jupyter/kernels/python2-jupyroot
%doc bindings/pyroot/JupyROOT/README.md

%files -n python%{python3_pkgversion}-jupyroot
%{python3_sitearch}/JupyROOT
%{python3_sitearch}/libJupyROOT.so
%{_datadir}/jupyter/kernels/python%{python3_pkgversion}-jupyroot
%doc bindings/pyroot/JupyROOT/README.md

%files -n python2-jsmva
%{python2_sitelib}/JsMVA

%files -n python%{python3_pkgversion}-jsmva
%{python3_sitelib}/JsMVA

%if %{ruby}
%files ruby -f includelist-bindings-ruby
%{_libdir}/%{name}/libRuby.*
%{_libdir}/%{name}/libRuby_rdict.pcm
%{ruby_vendorarchdir}/libRuby.*
%endif

%files r -f includelist-bindings-r
%{_libdir}/%{name}/libRInterface.*
%{_libdir}/%{name}/libRInterface_rdict.pcm
%doc bindings/r/doc/users-guide/*.md

%files r-tools -f includelist-math-rtools
%{_libdir}/%{name}/libRtools.*
%{_libdir}/%{name}/libRtools_rdict.pcm
%{_datadir}/%{name}/plugins/ROOT@@Math@@Minimizer/P090_RMinimizer.C

%files genetic -f includelist-math-genetic
%{_libdir}/%{name}/libGenetic.*
%{_libdir}/%{name}/libGenetic_rdict.pcm
%{_datadir}/%{name}/plugins/ROOT@@Math@@Minimizer/P080_GeneticMinimizer.C

%files geom -f includelist-geom
%{_libdir}/%{name}/libGeom.*
%{_libdir}/%{name}/libGeom_rdict.pcm
%{_libdir}/%{name}/libGeomBuilder.*
%{_libdir}/%{name}/libGeomBuilder_rdict.pcm
%{_libdir}/%{name}/libGeomPainter.*
%{_libdir}/%{name}/libGeomPainter_rdict.pcm
%{_datadir}/%{name}/plugins/TGeoManagerEditor/P010_TGeoManagerEditor.C
%{_datadir}/%{name}/plugins/TVirtualGeoPainter/P010_TGeoPainter.C
%{_datadir}/%{name}/RadioNuclides.txt

%files gdml -f includelist-geom-gdml
%{_libdir}/%{name}/libGdml.*
%{_libdir}/%{name}/libGdml_rdict.pcm

%if %{oce}
%files geocad -f includelist-geom-geocad
%{_libdir}/%{name}/libGeoCad.*
%{_libdir}/%{name}/libGeoCad_rdict.pcm
%endif

%files graf -f includelist-graf2d-graf
%{_libdir}/%{name}/libGraf.*
%{_libdir}/%{name}/libGraf_rdict.pcm
%{_datadir}/%{name}/plugins/TMinuitGraph/P010_TGraph.C

%files graf-asimage -f includelist-graf2d-asimage
%{_libdir}/%{name}/libASImage.*
%{_libdir}/%{name}/libASImage_rdict.pcm
%{_libdir}/%{name}/libASImageGui.*
%{_libdir}/%{name}/libASImageGui_rdict.pcm
%{_datadir}/%{name}/plugins/TImage/P010_TASImage.C
%{_datadir}/%{name}/plugins/TPaletteEditor/P010_TASPaletteEditor.C

%files graf-fitsio -f includelist-graf2d-fitsio
%{_libdir}/%{name}/libFITSIO.*
%{_libdir}/%{name}/libFITSIO_rdict.pcm

%files graf-gpad -f includelist-graf2d-gpad
%{_libdir}/%{name}/libGpad.*
%{_libdir}/%{name}/libGpad_rdict.pcm
%{_datadir}/%{name}/plugins/TVirtualPad/P010_TPad.C

%files graf-gviz -f includelist-graf2d-gviz
%{_libdir}/%{name}/libGviz.*
%{_libdir}/%{name}/libGviz_rdict.pcm

%files graf-postscript -f includelist-graf2d-postscript
%{_libdir}/%{name}/libPostscript.*
%{_libdir}/%{name}/libPostscript_rdict.pcm
%{_datadir}/%{name}/plugins/TVirtualPS/P010_TPostScript.C
%{_datadir}/%{name}/plugins/TVirtualPS/P020_TSVG.C
%{_datadir}/%{name}/plugins/TVirtualPS/P030_TPDF.C
%{_datadir}/%{name}/plugins/TVirtualPS/P040_TImageDump.C
%{_datadir}/%{name}/plugins/TVirtualPS/P050_TTeXDump.C

%files graf-qt -f includelist-graf2d-qt
%{_libdir}/%{name}/libGQt.*
%{_libdir}/%{name}/libGQt_rdict.pcm
%{_datadir}/%{name}/plugins/TVirtualX/P040_TGQt.C

%files graf-x11 -f includelist-graf2d-x11
%{_libdir}/%{name}/libGX11.*
%{_libdir}/%{name}/libGX11_rdict.pcm
%{_libdir}/%{name}/libGX11TTF.*
%{_libdir}/%{name}/libGX11TTF_rdict.pcm
%{_datadir}/%{name}/plugins/TVirtualX/P010_TGX11.C
%{_datadir}/%{name}/plugins/TVirtualX/P020_TGX11TTF.C

%files graf3d -f includelist-graf3d-g3d
%{_libdir}/%{name}/libGraf3d.*
%{_libdir}/%{name}/libGraf3d_rdict.pcm
%{_datadir}/%{name}/plugins/TView/P010_TView3D.C

%files graf3d-eve -f includelist-graf3d-eve
%{_libdir}/%{name}/libEve.*
%{_libdir}/%{name}/libEve_rdict.pcm

%files graf3d-gl -f includelist-graf3d-gl
%{_libdir}/%{name}/libRGL.*
%{_libdir}/%{name}/libRGL_rdict.pcm
%{_datadir}/%{name}/plugins/TGLHistPainter/P010_TGLHistPainter.C
%{_datadir}/%{name}/plugins/TGLManager/P010_TX11GLManager.C
%{_datadir}/%{name}/plugins/TVirtualGLImp/P010_TX11GL.C
%{_datadir}/%{name}/plugins/TVirtualPadPainter/P010_TGLPadPainter.C
%{_datadir}/%{name}/plugins/TVirtualViewer3D/P020_TGLSAViewer.C
%{_datadir}/%{name}/plugins/TVirtualViewer3D/P030_TGLViewer.C

%files graf3d-gviz3d -f includelist-graf3d-gviz3d
%{_libdir}/%{name}/libGviz3d.*
%{_libdir}/%{name}/libGviz3d_rdict.pcm

%files graf3d-x3d -f includelist-graf3d-x3d
%{_libdir}/%{name}/libX3d.*
%{_libdir}/%{name}/libX3d_rdict.pcm
%{_datadir}/%{name}/plugins/TViewerX3D/P010_TViewerX3D.C
%{_datadir}/%{name}/plugins/TVirtualViewer3D/P010_TVirtualViewerX3D.C

%files gui -f includelist-gui-gui
%{_libdir}/%{name}/libGui.*
%{_libdir}/%{name}/libGui_rdict.pcm
%{_libdir}/%{name}/libGuiHtml.*
%{_libdir}/%{name}/libGuiHtml_rdict.pcm
%{_datadir}/%{name}/plugins/TBrowserImp/P010_TRootBrowser.C
%{_datadir}/%{name}/plugins/TBrowserImp/P020_TRootBrowserLite.C
%{_datadir}/%{name}/plugins/TGPasswdDialog/P010_TGPasswdDialog.C
%{_datadir}/%{name}/plugins/TGuiFactory/P010_TRootGuiFactory.C

%files gui-fitpanel -f includelist-gui-fitpanel
%{_libdir}/%{name}/libFitPanel.*
%{_libdir}/%{name}/libFitPanel_rdict.pcm
%{_datadir}/%{name}/plugins/TFitEditor/P010_TFitEditor.C

%files gui-ged -f includelist-gui-ged
%{_libdir}/%{name}/libGed.*
%{_libdir}/%{name}/libGed_rdict.pcm
%{_datadir}/%{name}/plugins/TVirtualPadEditor/P010_TGedEditor.C

%files guibuilder -f includelist-gui-guibuilder
%{_libdir}/%{name}/libGuiBld.*
%{_libdir}/%{name}/libGuiBld_rdict.pcm
%{_datadir}/%{name}/plugins/TGuiBuilder/P010_TRootGuiBuilder.C
%{_datadir}/%{name}/plugins/TVirtualDragManager/P010_TGuiBldDragManager.C

%files gui-qt -f includelist-gui-qt
%{_libdir}/%{name}/libQtRoot.*
%{_libdir}/%{name}/libQtRoot_rdict.pcm
%{_libdir}/%{name}/libQtGSI.*
%{_libdir}/%{name}/libQtGSI_rdict.pcm
%{_datadir}/%{name}/plugins/TGuiFactory/P020_TQtRootGuiFactory.C

%files gui-recorder -f includelist-gui-recorder
%{_libdir}/%{name}/libRecorder.*
%{_libdir}/%{name}/libRecorder_rdict.pcm

%if %{root7}
%files gui-canvaspainter
%{_libdir}/%{name}/libROOTCanvasPainter.*

%files gui-webdisplay -f includelist-gui-webdisplay
%{_libdir}/%{name}/libROOTWebDisplay.*
%{_libdir}/%{name}/libROOTWebDisplay_rdict.pcm
%endif

%files hbook -f includelist-hist-hbook
%{_bindir}/g2root
%{_bindir}/h2root
%{_mandir}/man1/g2root.1*
%{_mandir}/man1/h2root.1*
%{_libdir}/%{name}/libHbook.*
%{_libdir}/%{name}/libHbook_rdict.pcm

%files hist -f includelist-hist-hist
%{_libdir}/%{name}/libHist.*
%{_libdir}/%{name}/libHist_rdict.pcm
%dir %{_includedir}/%{name}/v5

%if %{root7}
%files hist-draw -f includelist-hist-histdraw
%{_libdir}/%{name}/libROOTHistDraw.*
%{_libdir}/%{name}/libROOTHistDraw_rdict.pcm
%endif

%files hist-painter -f includelist-hist-histpainter
%{_libdir}/%{name}/libHistPainter.*
%{_libdir}/%{name}/libHistPainter_rdict.pcm
%{_datadir}/%{name}/plugins/TVirtualHistPainter/P010_THistPainter.C
%{_datadir}/%{name}/plugins/TVirtualGraphPainter/P010_TGraphPainter.C

%files spectrum -f includelist-hist-spectrum
%{_libdir}/%{name}/libSpectrum.*
%{_libdir}/%{name}/libSpectrum_rdict.pcm

%files spectrum-painter -f includelist-hist-spectrumpainter
%{_libdir}/%{name}/libSpectrumPainter.*
%{_libdir}/%{name}/libSpectrumPainter_rdict.pcm

%files hist-factory -f includelist-roofit-histfactory
%{_bindir}/hist2workspace
%{_bindir}/prepareHistFactory
%{_mandir}/man1/hist2workspace.1*
%{_mandir}/man1/prepareHistFactory.1*
%{_libdir}/%{name}/libHistFactory.*
%{_libdir}/%{name}/libHistFactory_rdict.pcm
%{_datadir}/%{name}/HistFactorySchema.dtd
%dir %{_includedir}/%{name}/RooStats/HistFactory
%doc roofit/histfactory/doc/README

%files html -f includelist-html
%{_libdir}/%{name}/libHtml.*
%{_libdir}/%{name}/libHtml_rdict.pcm
%{_datadir}/%{name}/html

%files io -f includelist-io-io
%{_libdir}/%{name}/libRIO.*
%{_datadir}/%{name}/plugins/TArchiveFile/P010_TZIPFile.C
%{_datadir}/%{name}/plugins/TVirtualStreamerInfo/P010_TStreamerInfo.C

%files io-dcache -f includelist-io-dcache
%{_libdir}/%{name}/libDCache.*
%{_libdir}/%{name}/libDCache_rdict.pcm
%{_datadir}/%{name}/plugins/TFile/P040_TDCacheFile.C
%{_datadir}/%{name}/plugins/TSystem/P020_TDCacheSystem.C

%files io-gfal -f includelist-io-gfal
%{_libdir}/%{name}/libGFAL.*
%{_libdir}/%{name}/libGFAL_rdict.pcm
%{_datadir}/%{name}/plugins/TFile/P050_TGFALFile.C

%if %{hadoop}
%files io-hdfs -f includelist-io-hdfs
%{_libdir}/%{name}/libHDFS.*
%{_libdir}/%{name}/libHDFS_rdict.pcm
%{_datadir}/%{name}/plugins/TFile/P110_THDFSFile.C
%{_datadir}/%{name}/plugins/TSystem/P060_THDFSSystem.C
%endif

%files io-rfio -f includelist-io-rfio
%{_libdir}/%{name}/libRFIO.*
%{_libdir}/%{name}/libRFIO_rdict.pcm
%{_datadir}/%{name}/plugins/TFile/P020_TRFIOFile.C
%{_datadir}/%{name}/plugins/TSystem/P010_TRFIOSystem.C

%files io-sql -f includelist-io-sql
%{_libdir}/%{name}/libSQLIO.*
%{_libdir}/%{name}/libSQLIO_rdict.pcm
%{_datadir}/%{name}/plugins/TFile/P090_TSQLFile.C

%files io-xml -f includelist-io-xml
%{_libdir}/%{name}/libXMLIO.*
%{_libdir}/%{name}/libXMLIO_rdict.pcm
%{_libdir}/%{name}/libXMLParser.*
%{_libdir}/%{name}/libXMLParser_rdict.pcm
%{_datadir}/%{name}/plugins/TFile/P080_TXMLFile.C

%files foam -f includelist-math-foam
%{_libdir}/%{name}/libFoam.*
%{_libdir}/%{name}/libFoam_rdict.pcm
%{_datadir}/%{name}/plugins/ROOT@@Math@@DistSampler/P020_TFoamSampler.C

%files fftw -f includelist-math-fftw
%{_libdir}/%{name}/libFFTW.*
%{_libdir}/%{name}/libFFTW_rdict.pcm
%{_datadir}/%{name}/plugins/TVirtualFFT/P010_TFFTComplex.C
%{_datadir}/%{name}/plugins/TVirtualFFT/P020_TFFTComplexReal.C
%{_datadir}/%{name}/plugins/TVirtualFFT/P030_TFFTRealComplex.C
%{_datadir}/%{name}/plugins/TVirtualFFT/P040_TFFTReal.C

%files fumili -f includelist-math-fumili
%{_libdir}/%{name}/libFumili.*
%{_libdir}/%{name}/libFumili_rdict.pcm
%{_datadir}/%{name}/plugins/ROOT@@Math@@Minimizer/P070_TFumiliMinimizer.C
%{_datadir}/%{name}/plugins/TVirtualFitter/P020_TFumili.C

%files genvector -f includelist-math-genvector
%{_libdir}/%{name}/libGenVector.*
%{_libdir}/%{name}/libGenVector_rdict.pcm
%{_libdir}/%{name}/libGenVector32.rootmap
%{_libdir}/%{name}/libGenVector_G__GenVector32_rdict.pcm
%dir %{_includedir}/%{name}/Math/GenVector

%files mathcore -f includelist-math-mathcore
%{_libdir}/%{name}/libMathCore.*
%{_libdir}/%{name}/libMathCore_rdict.pcm
%dir %{_includedir}/%{name}/Fit

%files mathmore -f includelist-math-mathmore
%{_libdir}/%{name}/libMathMore.*
%{_libdir}/%{name}/libMathMore_rdict.pcm
%{_datadir}/%{name}/plugins/ROOT@@Math@@IRootFinderMethod/P010_Brent.C
%{_datadir}/%{name}/plugins/ROOT@@Math@@IRootFinderMethod/P020_Bisection.C
%{_datadir}/%{name}/plugins/ROOT@@Math@@IRootFinderMethod/P030_FalsePos.C
%{_datadir}/%{name}/plugins/ROOT@@Math@@IRootFinderMethod/P040_Newton.C
%{_datadir}/%{name}/plugins/ROOT@@Math@@IRootFinderMethod/P050_Secant.C
%{_datadir}/%{name}/plugins/ROOT@@Math@@IRootFinderMethod/P060_Steffenson.C
%{_datadir}/%{name}/plugins/ROOT@@Math@@Minimizer/P030_GSLMinimizer.C
%{_datadir}/%{name}/plugins/ROOT@@Math@@Minimizer/P040_GSLNLSMinimizer.C
%{_datadir}/%{name}/plugins/ROOT@@Math@@Minimizer/P050_GSLSimAnMinimizer.C
%{_datadir}/%{name}/plugins/ROOT@@Math@@VirtualIntegrator/P010_GSLIntegrator.C
%{_datadir}/%{name}/plugins/ROOT@@Math@@VirtualIntegrator/P020_GSLMCIntegrator.C

%files matrix -f includelist-math-matrix
%{_libdir}/%{name}/libMatrix.*
%{_libdir}/%{name}/libMatrix_rdict.pcm

%files minuit -f includelist-math-minuit
%{_libdir}/%{name}/libMinuit.*
%{_libdir}/%{name}/libMinuit_rdict.pcm
%{_datadir}/%{name}/plugins/ROOT@@Math@@Minimizer/P020_TMinuitMinimizer.C
%{_datadir}/%{name}/plugins/ROOT@@Math@@Minimizer/P060_TLinearMinimizer.C
%{_datadir}/%{name}/plugins/TVirtualFitter/P010_TFitter.C

%files minuit2 -f includelist-math-minuit2
%{_libdir}/%{name}/libMinuit2.*
%{_libdir}/%{name}/libMinuit2_rdict.pcm
%dir %{_includedir}/%{name}/Minuit2
%{_datadir}/%{name}/plugins/ROOT@@Math@@Minimizer/P010_Minuit2Minimizer.C
%{_datadir}/%{name}/plugins/TVirtualFitter/P030_TFitterMinuit.C
%{_datadir}/%{name}/plugins/TVirtualFitter/P040_TFitterFumili.C

%files mlp -f includelist-math-mlp
%{_libdir}/%{name}/libMLP.*
%{_libdir}/%{name}/libMLP_rdict.pcm

%files physics -f includelist-math-physics
%{_libdir}/%{name}/libPhysics.*
%{_libdir}/%{name}/libPhysics_rdict.pcm

%files quadp -f includelist-math-quadp
%{_libdir}/%{name}/libQuadp.*
%{_libdir}/%{name}/libQuadp_rdict.pcm

%files smatrix -f includelist-math-smatrix
%{_libdir}/%{name}/libSmatrix.*
%{_libdir}/%{name}/libSmatrix_rdict.pcm
%{_libdir}/%{name}/libSmatrix32.rootmap
%{_libdir}/%{name}/libSmatrix_G__Smatrix32_rdict.pcm

%files splot -f includelist-math-splot
%{_libdir}/%{name}/libSPlot.*
%{_libdir}/%{name}/libSPlot_rdict.pcm

%files unuran -f includelist-math-unuran
%{_libdir}/%{name}/libUnuran.*
%{_libdir}/%{name}/libUnuran_rdict.pcm
%{_datadir}/%{name}/plugins/ROOT@@Math@@DistSampler/P010_TUnuranSampler.C

%files memstat -f includelist-misc-memstat
%{_libdir}/%{name}/libMemStat.*
%{_libdir}/%{name}/libMemStat_rdict.pcm

%files table -f includelist-misc-table
%{_libdir}/%{name}/libTable.*
%{_libdir}/%{name}/libTable_rdict.pcm

%files montecarlo-eg -f includelist-montecarlo-eg
%{_libdir}/%{name}/libEG.*
%{_libdir}/%{name}/libEG_rdict.pcm
%{_datadir}/%{name}/pdg_table.txt
%doc %{_pkgdocdir}/cfortran.doc

%if %{pythia8}
%files montecarlo-pythia8 -f includelist-montecarlo-pythia8
%{_libdir}/%{name}/libEGPythia8.*
%{_libdir}/%{name}/libEGPythia8_rdict.pcm
%endif

%files montecarlo-vmc -f includelist-montecarlo-vmc
%{_libdir}/%{name}/libVMC.*
%{_libdir}/%{name}/libVMC_rdict.pcm
%{_datadir}/%{name}/vmc

%files net -f includelist-net-net
%{_libdir}/%{name}/libNet.*
%{_libdir}/%{name}/libNet_rdict.pcm
%{_datadir}/%{name}/plugins/TApplication/P010_TApplicationRemote.C
%{_datadir}/%{name}/plugins/TApplication/P020_TApplicationServer.C
%{_datadir}/%{name}/plugins/TFile/P010_TWebFile.C
%{_datadir}/%{name}/plugins/TFile/P120_TNetFile.C
%{_datadir}/%{name}/plugins/TFile/P150_TS3WebFile.C
%{_datadir}/%{name}/plugins/TFileStager/P020_TNetFileStager.C
%{_datadir}/%{name}/plugins/TSystem/P050_TWebSystem.C
%{_datadir}/%{name}/plugins/TSystem/P070_TNetSystem.C
%{_datadir}/%{name}/plugins/TVirtualMonitoringWriter/P020_TSQLMonitoringWriter.C

%files net-rpdutils
%{_libdir}/%{name}/libSrvAuth.*

%files net-bonjour -f includelist-net-bonjour
%{_libdir}/%{name}/libBonjour.*
%{_libdir}/%{name}/libBonjour_rdict.pcm

%files net-auth -f includelist-net-auth
%{_libdir}/%{name}/libRootAuth.*
%{_libdir}/%{name}/libRootAuth_rdict.pcm
%{_datadir}/%{name}/plugins/TVirtualAuth/P010_TRootAuth.C
%doc %{_pkgdocdir}/README.AUTH

%files net-davix -f includelist-net-davix
%{_libdir}/%{name}/libRDAVIX.*
%{_libdir}/%{name}/libRDAVIX_rdict.pcm
%{_datadir}/%{name}/plugins/TFile/P130_TDavixFile.C
%{_datadir}/%{name}/plugins/TSystem/P045_TDavixSystem.C

%files net-globus
%{_libdir}/%{name}/libGlobusAuth.*
%doc %{_pkgdocdir}/README.GLOBUS

%files net-krb5 -f includelist-net-krb5auth
%{_libdir}/%{name}/libKrb5Auth.*
%{_libdir}/%{name}/libKrb5Auth_rdict.pcm

%files net-ldap -f includelist-net-ldap
%{_libdir}/%{name}/libRLDAP.*
%{_libdir}/%{name}/libRLDAP_rdict.pcm

%files net-http -f includelist-net-http
%{_libdir}/%{name}/libRHTTP.*
%{_libdir}/%{name}/libRHTTP_rdict.pcm
%{_datadir}/%{name}/http
%doc net/http/README.txt net/http/civetweb/*.md

%if %{xrootd}
%files netx -f includelist-netx
%{_libdir}/%{name}/libNetx.*
%{_libdir}/%{name}/libNetx_rdict.pcm
%{_libdir}/%{name}/libNetxNG.*
%{_libdir}/%{name}/libNetxNG_rdict.pcm
%{_datadir}/%{name}/plugins/TFile/P100_TXNetFile.C
%{_datadir}/%{name}/plugins/TFileStager/P010_TXNetFileStager.C
%{_datadir}/%{name}/plugins/TSystem/P040_TXNetSystem.C
%endif

%files proof -f includelist-proof-proof
%{_libdir}/%{name}/libProof.*
%{_libdir}/%{name}/libProof_rdict.pcm
%{_libdir}/%{name}/libProofDraw.*
%{_libdir}/%{name}/libProofDraw_rdict.pcm
%{_libdir}/%{name}/libProofPlayer.*
%{_libdir}/%{name}/libProofPlayer_rdict.pcm
%{_datadir}/%{name}/plugins/TChain/P010_TProofChain.C
%{_datadir}/%{name}/plugins/TDataSetManager/P010_TDataSetManagerFile.C
%{_datadir}/%{name}/plugins/TProof/P010_TProofCondor.C
%{_datadir}/%{name}/plugins/TProof/P020_TProofSuperMaster.C
%{_datadir}/%{name}/plugins/TProof/P030_TProofLite.C
%{_datadir}/%{name}/plugins/TProof/P040_TProof.C
%{_datadir}/%{name}/plugins/TProofMonSender/P010_TProofMonSenderML.C
%{_datadir}/%{name}/plugins/TProofMonSender/P020_TProofMonSenderSQL.C
%{_datadir}/%{name}/plugins/TVirtualProofPlayer/P010_TProofPlayer.C
%{_datadir}/%{name}/plugins/TVirtualProofPlayer/P020_TProofPlayerRemote.C
%{_datadir}/%{name}/plugins/TVirtualProofPlayer/P030_TProofPlayerLocal.C
%{_datadir}/%{name}/plugins/TVirtualProofPlayer/P040_TProofPlayerSlave.C
%{_datadir}/%{name}/plugins/TVirtualProofPlayer/P050_TProofPlayerSuperMaster.C
%{_datadir}/%{name}/plugins/TVirtualProofPlayer/P060_TProofPlayerLite.C
%{_datadir}/%{name}/valgrind-root.supp
%doc %{_pkgdocdir}/README.PROOF

%files proof-bench -f includelist-proof-proofbench
%{_libdir}/%{name}/libProofBench.*
%{_libdir}/%{name}/libProofBench_rdict.pcm
%{_datadir}/%{name}/proof

%files proof-pq2
%{_bindir}/pq2*
%{_mandir}/man1/pq2*.1*

%files proof-sessionviewer -f includelist-gui-sessionviewer
%{_libdir}/%{name}/libSessionViewer.*
%{_libdir}/%{name}/libSessionViewer_rdict.pcm
%{_datadir}/%{name}/plugins/TProofProgressDialog/P010_TProofProgressDialog.C
%{_datadir}/%{name}/plugins/TProofProgressLog/P010_TProofProgressLog.C
%{_datadir}/%{name}/plugins/TSessionViewer/P010_TSessionViewer.C

%if %{xrootd}
%files xproof -f includelist-proof-proofx
%{_bindir}/proofexecv
%{_bindir}/xproofd
%{_mandir}/man1/xproofd.1*
%{_libdir}/%{name}/libProofx.*
%{_libdir}/%{name}/libProofx_rdict.pcm
%{_libdir}/%{name}/libXrdProofd.*
%{_datadir}/%{name}/plugins/TProofMgr/P010_TXProofMgr.C
%{_datadir}/%{name}/plugins/TProofServ/P010_TXProofServ.C
%{_datadir}/%{name}/plugins/TSlave/P010_TXSlave.C
%endif

%files roofit -f includelist-roofit
%{_libdir}/%{name}/libRooFit.*
%{_libdir}/%{name}/libRooFit_rdict.pcm
%{_libdir}/%{name}/libRooFitCore.*
%{_libdir}/%{name}/libRooFitCore_rdict.pcm
%{_libdir}/%{name}/libRooStats.*
%{_libdir}/%{name}/libRooStats_rdict.pcm
%dir %{_includedir}/%{name}/RooStats

%files sql-mysql -f includelist-sql-mysql
%{_libdir}/%{name}/libRMySQL.*
%{_libdir}/%{name}/libRMySQL_rdict.pcm
%{_datadir}/%{name}/plugins/TSQLServer/P010_TMySQLServer.C

%files sql-odbc -f includelist-sql-odbc
%{_libdir}/%{name}/libRODBC.*
%{_libdir}/%{name}/libRODBC_rdict.pcm
%{_datadir}/%{name}/plugins/TSQLServer/P050_TODBCServer.C

%files sql-sqlite -f includelist-sql-sqlite
%{_libdir}/%{name}/libRSQLite.*
%{_libdir}/%{name}/libRSQLite_rdict.pcm
%{_datadir}/%{name}/plugins/TSQLServer/P060_TSQLiteServer.C

%files sql-pgsql -f includelist-sql-pgsql
%{_libdir}/%{name}/libPgSQL.*
%{_libdir}/%{name}/libPgSQL_rdict.pcm
%{_datadir}/%{name}/plugins/TSQLServer/P020_TPgSQLServer.C

%files tmva -f includelist-tmva-tmva
%{_libdir}/%{name}/libTMVA.*
%{_libdir}/%{name}/libTMVA_rdict.pcm
%dir %{_includedir}/%{name}/TMVA
%license tmva/doc/LICENSE

%files tmva-python -f includelist-tmva-pymva
%{_libdir}/%{name}/libPyMVA.*
%{_libdir}/%{name}/libPyMVA_rdict.pcm

%files tmva-r -f includelist-tmva-rmva
%{_libdir}/%{name}/libRMVA.*
%{_libdir}/%{name}/libRMVA_rdict.pcm

%files tmva-gui -f includelist-tmva-tmvagui
%{_libdir}/%{name}/libTMVAGui.*
%{_libdir}/%{name}/libTMVAGui_rdict.pcm

%files tree -f includelist-tree-tree
%{_libdir}/%{name}/libTree.*
%{_libdir}/%{name}/libTree_rdict.pcm
%doc %{_pkgdocdir}/README.SELECTOR

%files tree-player -f includelist-tree-treeplayer
%{_libdir}/%{name}/libTreePlayer.*
%{_libdir}/%{name}/libTreePlayer_rdict.pcm
%{_datadir}/%{name}/plugins/TFileDrawMap/P010_TFileDrawMap.C
%{_datadir}/%{name}/plugins/TVirtualTreePlayer/P010_TTreePlayer.C

%files tree-viewer -f includelist-tree-treeviewer
%{_libdir}/%{name}/libTreeViewer.*
%{_libdir}/%{name}/libTreeViewer_rdict.pcm
%{_datadir}/%{name}/plugins/TVirtualTreeViewer/P010_TTreeViewer.C

%files unfold -f includelist-hist-unfold
%{_libdir}/%{name}/libUnfold.*
%{_libdir}/%{name}/libUnfold_rdict.pcm

%files cli
%{_bindir}/rootbrowse
%{_bindir}/rootcp
%{_bindir}/rootdrawtree
%{_bindir}/rooteventselector
%{_bindir}/rootls
%{_bindir}/rootmkdir
%{_bindir}/rootmv
%{_bindir}/rootprint
%{_bindir}/rootrm
%{_bindir}/rootslimtree
%{_datadir}/%{name}/cli

%files notebook
%{_bindir}/rootnb.exe
%{_datadir}/%{name}/notebook

%changelog
* Fri Feb 16 2018 Mattias Ellert <mattias.ellert@physics.uu.se> - 6.12.04-4
- Fix test failures found with new default compiler flags in Fedora 28

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 6.12.04-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Jan 20 2018 Björn Esser <besser82@fedoraproject.org> - 6.12.04-2
- Rebuilt for switch to libxcrypt

* Tue Dec 19 2017 Mattias Ellert <mattias.ellert@physics.uu.se> - 6.12.04-1
- Update to 6.12.04
- Drop patches accepted upstream
- Drop previously backported patches
- Unbundle jsroot in root-net-http
- Add hack to work around broken charmaps in StandardSymbolsPS.otf
- Use local static script and style files for JupyROOT
- Fix some javascript errors
- Fix build rules for test binaries so that they are not installed
- Address memory usage issue for ARM build
- Drop pre-minified javascript and style files (Fedora packaging guidelines)
- Enable builds on ppc/ppc64/ppc64le (do not pass all tests, but the list
  of failing tests is much shorter with this release)
- Add dependency on python[23]-jsmva to python[23]-jupyroot
- New sub-packages: root-gui-canvaspainter, root-gui-webdisplay and
  root-hist-draw (not for EPEL 7 since they are root7 specific and
  require c++-14)

* Fri Oct 20 2017 Mattias Ellert <mattias.ellert@physics.uu.se> - 6.10.08-1
- Update to 6.10.08
- Add BuildRequires on lz4-devel and xxhash-devel
- Workaround for missing gmock libraries only needed for gmock < 0.1.8
- Address some warnings during documentation generation

* Wed Sep 27 2017 Mattias Ellert <mattias.ellert@physics.uu.se> - 6.10.06-1
- Update to 6.10.06
- Fixes for new mysql_config

* Sat Aug 05 2017 Mattias Ellert <mattias.ellert@physics.uu.se> - 6.10.04-1
- Update to 6.10.04
- Add temporary workaround for broken mariadb headers in Fedora 27

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 6.10.02-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 6.10.02-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jul 12 2017 Mattias Ellert <mattias.ellert@physics.uu.se> - 6.10.02-3
- Remove additional references in cmake files

* Mon Jul 10 2017 Mattias Ellert <mattias.ellert@physics.uu.se> - 6.10.02-2
- Fix removal of mathtext, minicern and JupyROOT references from cmake files

* Fri Jul 07 2017 Mattias Ellert <mattias.ellert@physics.uu.se> - 6.10.02-1
- Update to 6.10.02

* Wed Jun 14 2017 Mattias Ellert <mattias.ellert@physics.uu.se> - 6.10.00-1
- Update to 6.10.00
- Drop patches accepted upstream
- Drop previously backported patches
- New sub-package: root-unfold
- Dropped sub-package: root-vdt

* Tue May 16 2017 Mattias Ellert <mattias.ellert@physics.uu.se> - 6.08.06-7
- Remove JupyROOT references from cmake files
- Do not generate autoprovides for libJupyROOT.so

* Mon May 15 2017 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.08.06-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_27_Mass_Rebuild

* Fri May 12 2017 Mattias Ellert <mattias.ellert@physics.uu.se> - 6.08.06-5
- Fix for macro scope issue (backport from upstream)
- Fix a problem loading the libJupyROOT CDLL module (use absolute path)
- Add ipython dependencies to the jupyroot packages
- Exclude s390x - endian issues
- Re-enable two tests on 32 bit arm - no longer failing
- Add BuildRequires on blas-devel (for TMVA)

* Thu May 11 2017 Richard Shaw <hobbes1069@gmail.com> - 6.08.06-4
- Rebuild for OCE 0.18.1.

* Fri Apr 21 2017 Mattias Ellert <mattias.ellert@physics.uu.se> - 6.08.06-3
- Python 3 compatibility fixes (backport from upstream)

* Wed Mar 15 2017 Mattias Ellert <mattias.ellert@physics.uu.se> - 6.08.06-2
- Fix relocation problems on aarch64 - using patch from the llvm package
- Re-enable building on aarch64 - works again with the above patch

* Thu Mar 02 2017 Mattias Ellert <mattias.ellert@physics.uu.se> - 6.08.06-1
- Update to 6.08.06
- Drop obsolete patch: root-tformulaparsingtests.patch
- Drop patches accepted upstream: root-spectrum-batch.patch and
  root-missing-header-gcc7.patch
- Disable failing tests on s390x

* Wed Mar 01 2017 Mattias Ellert <mattias.ellert@physics.uu.se> - 6.08.04-3
- Disable building on aarch64 (it is now broken again)
- Add missing header (gcc 7)
- Fix a test failure on Fedora 26 i686
- Fix some format warnings/errors in GlobusAuth
- Use the right delimiter when splitting the icon path in TASImage
- Disable two more tests on 32 bit arm

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 6.08.04-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sat Jan 14 2017 Mattias Ellert <mattias.ellert@physics.uu.se> - 6.08.04-1
- Update to 6.08.04
- Fix broken TPad::WaitPrimitive (backport from git)
- Rebuild for gcc 6.3

* Thu Jan 12 2017 Igor Gnatenko <ignatenko@redhat.com> - 6.08.02-4
- Rebuild for readline 7.x

* Tue Jan 10 2017 Orion Poplawski <orion@cora.nwra.com> - 6.08.02-3
- Rebuild for glew 2.0.0

* Thu Dec 22 2016 Miro Hrončok <mhroncok@redhat.com> - 6.08.02-2
- Rebuild for Python 3.6

* Tue Dec 06 2016 Mattias Ellert <mattias.ellert@physics.uu.se> - 6.08.02-1
- Update to 6.08.02
- Drop patches accepted upstream
- Drop previously backported patches
- Drop obsolete patches
- Enable hadoop/hdfs support for all architectures
  * libhdfs is now available for more architectures than ix86 and x86_64
- Enable building on aarch64
- Rename the python packages to python2-root and python3-root
- New sub-packages: python{2,3}-jupyroot, python{2,3}-jsmva
- Dropped sub-package: root-rootaas (replaced by python{2,3}-jupyroot)

* Wed Sep 28 2016 Mattias Ellert <mattias.ellert@physics.uu.se> - 6.06.08-2
- Rebuild for gcc 6.2

* Thu Sep 08 2016 Mattias Ellert <mattias.ellert@physics.uu.se> - 6.06.08-1
- Update to 6.06.08
- Add the packages providing the libraries listed by "root-config --libs"
  as dependencies to root-core
- Add missing scriptlets to root-multiproc

* Sun Aug 14 2016 Mattias Ellert <mattias.ellert@physics.uu.se> - 6.06.06-4
- Convert init scripts to systemd unit files

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.06.06-3
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Mon Jul 18 2016 Mattias Ellert <mattias.ellert@physics.uu.se> - 6.06.06-2
- Add requires on redhat-rpm-config to root-cling

* Sun Jul 10 2016 Mattias Ellert <mattias.ellert@physics.uu.se> - 6.06.06-1
- Update to 6.06.06
- Drop patches root-gfal2.patch and root-keysymbols.patch
- Make root-vdt package noarch

* Sun Jun 19 2016 Mattias Ellert <mattias.ellert@fysast.uu.se> - 6.06.04-4
- Add GuiTypes.h, KeySymbols.h and Buttons.h to dict (backport)
- Minor updates to patches - mostly backported from upstream
- Reenable hadoop/hdfs support for F24+

* Mon Jun 13 2016 Mattias Ellert <mattias.ellert@fysast.uu.se> - 6.06.04-3
- Remove mathtext and minicern references from cmake files
- Fix the spelling of CMAKE_Fortran_FLAGS in a few places

* Sat Jun 04 2016 Mattias Ellert <mattias.ellert@fysast.uu.se> - 6.06.04-2
- Disable hadoop/hdfs support for F24+ (hadoop was retired)

* Mon May 09 2016 Mattias Ellert <mattias.ellert@fysast.uu.se> - 6.06.04-1
- Update to 6.06.04
- Drop patch root-no-hexfloat-const.patch
- Add requires on gcc-c++ to root-cling

* Fri Apr 15 2016 Mattias Ellert <mattias.ellert@fysast.uu.se> - 6.06.02-2
- Rebuild for OCE-0.17.1

* Fri Apr 08 2016 Mattias Ellert <mattias.ellert@fysast.uu.se> - 6.06.02-1
- Update to 6.06.02 (F24+, EPEL7)
- Change to cmake configuration (was using ./configure)
- Change to doxygen documentation generation (was using THTML)
- Run the test suite
- Remove compatibility with older EPEL (Group tags, BuildRoot tag, etc.)
- New sub-packages: root-multiproc, root-cling, root-r, root-r-tools,
  root-geocad, root-tmva-python, root-tmva-r, root-tmva-gui, root-cli,
  root-notebook and root-rootaas
- New subpackage for EPEL7: root-python34
- Dropped sub-packages: root-cint, root-reflex, root-cintex, root-ruby

* Fri Apr 08 2016 Mattias Ellert <mattias.ellert@fysast.uu.se> - 5.34.36-1
- Update to 5.34.36

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 5.34.32-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sat Jan 16 2016 Mamoru TASAKA <mtasaka@fedoraproject.org> - 5.34.32-8
- Rebuild again for https://fedoraproject.org/wiki/Changes/Ruby_2.3

* Thu Jan 14 2016 Adam Jackson <ajax@redhat.com> - 5.34.32-7
- Rebuild for glew 1.13

* Tue Jan 12 2016 Vít Ondruch <vondruch@redhat.com> - 5.34.32-6
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_2.3

* Tue Nov 17 2015 Mattias Ellert <mattias.ellert@fysast.uu.se> - 5.34.32-5
- Adapt to gfal 2.10 - uses a different #define
- Exclude ppc64le - has the same issues with cint as ppc and ppc64

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.34.32-4
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Fri Sep 25 2015 Mattias Ellert <mattias.ellert@fysast.uu.se> - 5.34.32-3
- Add versioned dependencies between packages
- Reenable hadoop/hdfs support for F23+

* Wed Sep 16 2015 David Abdurachmanov <davidlt@cern.ch> - 5.34.32-2
- Disable run-time dependency on gccxml in Reflex (allows installing on aarch64) (#1263206)
- Enable Cintex on aarch64

* Thu Jul 02 2015 Mattias Ellert <mattias.ellert@fysast.uu.se> - 5.34.32-1
- Update to 5.34.32
- New sub-package: root-fonts (STIX version 0.9 required by TMathText)
- Use GNU Free instead of Liberation, works better with TMathText
- Fix segfault when embedding Type 1 fonts
- Drop patch root-no-extra-formats.patch (workaround for above problem)

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.34.30-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Apr 24 2015 Mattias Ellert <mattias.ellert@fysast.uu.se> - 5.34.30-1
- Update to 5.34.30
- New sub-package: root-python3
- Disable hadoop/hdfs support for F23+ (not installable)
- Drop previously backported gcc 5 patches

* Fri Apr 03 2015 Mattias Ellert <mattias.ellert@fysast.uu.se> - 5.34.28-1
- Update to 5.34.28
- Merge emacs support files into main package (guidelines updated)

* Tue Feb 24 2015 Mattias Ellert <mattias.ellert@fysast.uu.se> - 5.34.26-1
- Update to 5.34.26
- Drop patch root-xrdversion.patch

* Thu Jan 29 2015 Mattias Ellert <mattias.ellert@fysast.uu.se> - 5.34.24-3
- Rebuild with fixed cairo (bz 1183242)

* Sat Jan 17 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 5.34.24-2
- Rebuild for https://fedoraproject.org/wiki/Changes/Ruby_2.2

* Fri Dec 19 2014 Mattias Ellert <mattias.ellert@fysast.uu.se> - 5.34.24-1
- Update to 5.34.24
- Drop patch root-bsd-misc.patch

* Thu Aug 28 2014 Mattias Ellert <mattias.ellert@fysast.uu.se> - 5.34.20-2
- Move xproofd binaries from root-proofd to root-xproof
- Adjust EPEL 7 font dependencies
- Rebuild using new binutils (ld bug fixed - F21+)

* Wed Aug 20 2014 Mattias Ellert <mattias.ellert@fysast.uu.se> - 5.34.20-1
- Update to 5.34.20
- Re-enable xrootd support for F21+ and EPEL7 (now ported to xrootd 4)
- Do not depend on wine's fonts
- Drop patch root-gccopt.patch

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.34.19-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Mon Jul 14 2014 Mattias Ellert <mattias.ellert@fysast.uu.se> - 5.34.19-1
- Update to 5.34.19
- Disable xrootd support for F21+ and EPEL7 (root not yet ported to xrootd 4)
- New sub-package: root-net-http
- Drop patches root-thtml-revert.patch, root-gfal2.patch and
  root-proofx-link-iolib.patch

* Mon Jun 30 2014 Mattias Ellert <mattias.ellert@fysast.uu.se> - 5.34.18-4
- Add Requires on root-tree-player to root-gui-ged

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.34.18-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun May 04 2014 Mattias Ellert <mattias.ellert@fysast.uu.se> - 5.34.18-2
- Rebuild for ruby 2.1
- Fix build failure on F21 (missing symbol in libProofx linking)

* Sat Mar 22 2014 Mattias Ellert <mattias.ellert@fysast.uu.se> - 5.34.18-1
- Update to 5.34.18
- Build GFAL module using libgfal2
- New sub-package: root-vdt

* Wed Feb 26 2014 Mattias Ellert <mattias.ellert@fysast.uu.se> - 5.34.17-1
- Update to 5.34.17

* Fri Feb 14 2014 Mattias Ellert <mattias.ellert@fysast.uu.se> - 5.34.15-1
- Update to 5.34.15
- Drop patch root-davix.patch

* Thu Jan 09 2014 Mattias Ellert <mattias.ellert@fysast.uu.se> - 5.34.14-3
- Rebuild for cfitsio 3.360

* Mon Dec 23 2013 Mattias Ellert <mattias.ellert@fysast.uu.se> - 5.34.14-2
- Adapt to davix >= 0.2.8

* Thu Dec 19 2013 Mattias Ellert <mattias.ellert@fysast.uu.se> - 5.34.14-1
- Update to 5.34.14
- New sub-package: root-net-davix
- Drop patch root-pythia8-incdir.patch

* Tue Dec 03 2013 Mattias Ellert <mattias.ellert@fysast.uu.se> - 5.34.13-1
- Update to 5.34.13
- Remove java-devel build dependency (not needed with Fedora's libhdfs)
- Adapt to pythia8 >= 8.1.80

* Mon Nov 25 2013 Orion Poplawski <orion@cora.nwra.com> - 5.34.10-3
- Fix hadoop lib location

* Mon Nov 18 2013 Dave Airlie <airlied@redhat.com> - 5.34.10-2
- rebuilt for GLEW 1.10

* Mon Sep 09 2013 Mattias Ellert <mattias.ellert@fysast.uu.se> - 5.34.10-1
- Update to 5.34.10
- New sub-package: root-io-hdfs (Fedora 20+)
- New sub-package: root-sql-sqlite

* Thu Aug 08 2013 Mattias Ellert <mattias.ellert@fysast.uu.se> - 5.34.09-5
- Exclude armv7hl - cint is not working
- Use _pkgdocdir when defined
- Use texlive-stix

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.34.09-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jul 18 2013 Petr Pisar <ppisar@redhat.com> - 5.34.09-3
- Perl 5.18 rebuild

* Tue Jul 16 2013 Mattias Ellert <mattias.ellert@fysast.uu.se> - 5.34.09-2
- Rebuild for cfitsio 3.350

* Fri Jun 28 2013 Mattias Ellert <mattias.ellert@fysast.uu.se> - 5.34.09-1
- Update to 5.34.09
- New sub-package: root-montecarlo-pythia8
- Drop patch root-gfal-bits.patch
- Use xz compression for source tarfile
- Update ancient root version in EPEL

* Sat Apr 27 2013 Mattias Ellert <mattias.ellert@fysast.uu.se> - 5.34.07-1
- Update to 5.34.07

* Sat Apr 27 2013 Mattias Ellert <mattias.ellert@fysast.uu.se> - 5.34.06-1
- Update to 5.34.06
- Drop patches root-gviz.patch, root-ruby-version.patch,
  root-rev48681.patch and root-rev48831.patch

* Wed Mar 20 2013 Mattias Ellert <mattias.ellert@fysast.uu.se> - 5.34.05-2
- Rebuild for ruby 2.0
- Rebuild for cfitsio 3.340

* Wed Feb 27 2013 Mattias Ellert <mattias.ellert@fysast.uu.se> - 5.34.05-1
- Update to 5.34.05
- Rebuild for xrootd 3.3
- Patch for latest graphviz (libcgraph)
- Drop patches root-glibc.patch and root-tclass-fix.patch

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.34.02-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Dec 13 2012 Adam Jackson <ajax@redhat.com> - 5.34.02-2
- Rebuild for glew 1.9.0

* Fri Oct 12 2012 Mattias Ellert <mattias.ellert@fysast.uu.se> - 5.34.02-1
- Update to 5.34.02

* Sat Jul 28 2012 Mattias Ellert <mattias.ellert@fysast.uu.se> - 5.34.01-2
- Rebuild for glew 1.7

* Tue Jul 17 2012 Mattias Ellert <mattias.ellert@fysast.uu.se> - 5.34.01-1
- Update to 5.34.01
- Remove sub-packages root-clarens and root-peac (dropped by upstream)

* Thu Jul 05 2012 Mattias Ellert <mattias.ellert@fysast.uu.se> - 5.34.00-2
- Do the glibc 2.16 patch properly

* Sat Jun 09 2012 Mattias Ellert <mattias.ellert@fysast.uu.se> - 5.34.00-1
- Update to 5.34.00
- New sub-package: root-io-gfal

* Thu May 17 2012 Mattias Ellert <mattias.ellert@fysast.uu.se> - 5.32.03-1
- Update to 5.32.03

* Thu Mar 29 2012 Mattias Ellert <mattias.ellert@fysast.uu.se> - 5.32.02-1
- Update to 5.32.02

* Sat Mar 17 2012 Mattias Ellert <mattias.ellert@fysast.uu.se> - 5.32.01-2
- Rebuild for xrootd 3.1.1

* Sat Mar 03 2012 Mattias Ellert <mattias.ellert@fysast.uu.se> - 5.32.01-1
- Update to 5.32.01
- Drop patches fixed upstream

* Tue Feb 28 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.32.00-3
- Rebuilt for c++ ABI breakage

* Tue Feb 14 2012 Mattias Ellert <mattias.ellert@fysast.uu.se> - 5.32.00-2
- Adapt to new ruby packaging guidelines

* Fri Feb 10 2012 Mattias Ellert <mattias.ellert@fysast.uu.se> - 5.32.00-1
- Update to 5.32.00

* Fri Feb 10 2012 Petr Pisar <ppisar@redhat.com> - 5.30.04-3
- Rebuild against PCRE 8.30

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.30.04-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Nov 16 2011 Mattias Ellert <mattias.ellert@fysast.uu.se> - 5.30.04-1
- Update to 5.30.04

* Sat Oct 22 2011 Mattias Ellert <mattias.ellert@fysast.uu.se> - 5.30.03-1
- Update to 5.30.03

* Fri Sep 23 2011 Mattias Ellert <mattias.ellert@fysast.uu.se> - 5.30.02-1
- Update to 5.30.02

* Thu Aug 18 2011 Mattias Ellert <mattias.ellert@fysast.uu.se> - 5.30.01-1
- Update to 5.30.01
- Drop patches root-lzma-searchorder.patch and root-cint-i686.patch

* Wed Aug 17 2011 Mattias Ellert <mattias.ellert@fysast.uu.se> - 5.30.00-3
- Backport upstream's fix for the i686 rootcint problem

* Tue Jul 26 2011 Mattias Ellert <mattias.ellert@fysast.uu.se> - 5.30.00-2
- Add workaround for rootcint problem on i686
- Pass default LDFLAGS (relro) to make

* Sun Jul 24 2011 Mattias Ellert <mattias.ellert@fysast.uu.se> - 5.30.00-1
- Update to 5.30.00
- Drop patch root-listbox-height.patch
- New sub-package: root-proof-bench

* Wed Jun 29 2011 Mattias Ellert <mattias.ellert@fysast.uu.se> - 5.28.00e-2
- Change build requires from qt-devel to qt4-devel

* Wed Jun 29 2011 Mattias Ellert <mattias.ellert@fysast.uu.se> - 5.28.00e-1
- Update to 5.28.00e

* Mon Jun 20 2011 ajax@redhat.com - 5.28.00d-2
- Rebuild for new glew soname

* Fri May 13 2011 Mattias Ellert <mattias.ellert@fysast.uu.se> - 5.28.00d-1
- Update to 5.28.00d

* Mon May 02 2011 Mattias Ellert <mattias.ellert@fysast.uu.se> - 5.28.00c-1.1
- Fix emacs Requires on RHEL5

* Thu Apr 21 2011 Mattias Ellert <mattias.ellert@fysast.uu.se> - 5.28.00c-1
- Update to 5.28.00c

* Wed Mar 23 2011 Mattias Ellert <mattias.ellert@fysast.uu.se> - 5.28.00b-2
- Rebuild for mysql 5.5.10

* Sat Mar 19 2011 Mattias Ellert <mattias.ellert@fysast.uu.se> - 5.28.00b-1
- Update to 5.28.00b

* Mon Feb 21 2011 Mattias Ellert <mattias.ellert@fysast.uu.se> - 5.28.00a-1
- Update to 5.28.00a
- Drop patches fixed upstream: root-afterimage.patch, root-htmldoc.patch,
  root-xlibs-ppc.patch, root-cstddef.patch
- Remove the fedpkg workaround - no longer needed

* Sat Feb 12 2011 Mattias Ellert <mattias.ellert@fysast.uu.se> - 5.28.00-4
- Add workaround for changes in fedpkg

* Thu Feb 10 2011 Mattias Ellert <mattias.ellert@fysast.uu.se> - 5.28.00-3
- Add Requires on root-graf-postscript to root-gpad
- Require libAfterImage 1.20 or later to fix issues with circular markers in
  batch mode
- Add python26 subpackage for EPEL 5
- Fix an issue where the last item in a TGFontTypeComboBox is almost
  invisible (backported from upstream)
- Add missing cstddef includes for gcc 4.6

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.28.00-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jan 14 2011 Mattias Ellert <mattias.ellert@fysast.uu.se> - 5.28.00-1.1
- Fix linking of Xlibs on ppc

* Wed Dec 15 2010 Mattias Ellert <mattias.ellert@fysast.uu.se> - 5.28.00-1
- Update to 5.28.00
- Drop patches fixed upstream: root-linker-scripts.patch, root-dpm-rfio.patch,
  root-missing-explicit-link.patch, root-split-latex.patch,
  root-cern-filename.patch, root-make-3.82.patch,
  root-fonttype-combobox-dtor.patch
- New sub-packages: root-genetic, root-graf-fitsio, root-hist-factory,
  root-proof-pq2
- Make root-io a separate package again - the circular dependency with the
  root-core package was resolved upstream

* Fri Nov 12 2010 Mattias Ellert <mattias.ellert@fysast.uu.se> - 5.26.00e-3
- Fix crash in TGFontTypeComboBox destructor
- Add Requires on root-gui-ged to root-gui

* Mon Nov 01 2010 Mattias Ellert <mattias.ellert@fysast.uu.se> - 5.26.00e-2
- Rebuild for updated unuran

* Fri Oct 22 2010 Mattias Ellert <mattias.ellert@fysast.uu.se> - 5.26.00e-1
- Update to 5.26.00e
- Drop patch fixed upstream: root-tmva-segfault.patch
- Add Requires on root-proof to root-proofd

* Sat Oct 02 2010 Mattias Ellert <mattias.ellert@fysast.uu.se> - 5.26.00d-3
- Add Requires on root-graf-asimage to root-core
- Add Requires on root-graf-x11 to root-gui
- Add Requires on root-hist-painter to root-hist
- Add Requires on root-minuit to root-mathcore
- Add Requires on krb5-workstation to root-net-krb5
- Add BuildRequires on krb5-workstation

* Mon Aug 30 2010 Mattias Ellert <mattias.ellert@fysast.uu.se> - 5.26.00d-2
- Adapt makefile to changes in make 3.82

* Fri Aug 27 2010 Mattias Ellert <mattias.ellert@fysast.uu.se> - 5.26.00d-1
- Update to 5.26.00d
- Improved doc generation script

* Mon Aug 02 2010 Mattias Ellert <mattias.ellert@fysast.uu.se> - 5.26.00c-4
- Don't remove the prec_stl directory
- Create a separate tutorial package for the tutorial and test suite

* Thu Jul 29 2010 Mattias Ellert <mattias.ellert@fysast.uu.se> - 5.26.00c-3
- Correct license tags for: cint, core and roofit
- Regenerate source tarball due to upstream retag (again)

* Fri Jul 16 2010 Mattias Ellert <mattias.ellert@fysast.uu.se> - 5.26.00c-2
- Add dependency on gccxml for globus-reflex
- Split some packages to break circular package dependencies
- Merge libRIO into root-core
- Regenerate source tarball due to upstream retag

* Mon Jul 12 2010 Mattias Ellert <mattias.ellert@fysast.uu.se> - 5.26.00c-1
- Update to 5.26.00c
- Disable cint7 package - no longer compiles and has been deprecated upstream

* Wed Jun 09 2010 Mattias Ellert <mattias.ellert@fysast.uu.se> - 5.26.00b-3
- Use external xrootd
- Make documentation selfcontained - can be read without network access

* Wed May 19 2010 Mattias Ellert <mattias.ellert@fysast.uu.se> - 5.26.00b-2
- Fix library detection when linker scripts are used
- Allow building RFIO IO modules using DPM's RFIO implementation

* Sat Mar 20 2010 Mattias Ellert <mattias.ellert@fysast.uu.se> - 5.26.00b-1
- Update to 5.26.00b
- Enable dCache support - dcap library is now in Fedora
- Use system unuran library instead of embedded sources

* Mon Feb  1 2010 Mattias Ellert <mattias.ellert@fysast.uu.se> - 5.26.00a-1
- Update to 5.26.00a
- Disable cintex package for non-intel architectures
- Remove embedded gl2ps sources

* Wed Jan 13 2010 Mattias Ellert <mattias.ellert@fysast.uu.se> - 5.26.00-1
- Update to 5.26.00
- Drop patches fixed upstream: root-globus.patch, root-dot-png.patch,
  root-loadmeta.patch, root-openssl.patch, root-hash-endian.patch

* Fri Nov 27 2009 Mattias Ellert <mattias.ellert@fysast.uu.se> - 5.24.00b-1
- Initial build
