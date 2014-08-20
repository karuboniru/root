%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

%if "%{?rhel}" == "5"
%global __python26 /usr/bin/python26
%{!?python26_sitearch: %global python26_sitearch %(%{__python26} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}
# Disable the default python byte code compilation
%global __os_install_post %(echo '%{__os_install_post}' | sed -e 's!/usr/lib[^[:space:]]*/brp-python-bytecompile[[:space:]].*$!!g')
%endif

%{!?ruby_sitearchdir: %global ruby_sitearchdir %(ruby -rrbconfig -e 'puts RbConfig::CONFIG["sitearchdir"]' 2>/dev/null)}

%if %{?fedora}%{!?fedora:0} >= 19 || %{?rhel}%{!?rhel:0} >= 7
%global ruby_installdir %{ruby_vendorarchdir}
%else
%if %{?fedora}%{!?fedora:0} >= 17
%global ruby_installdir %{ruby_vendorarchdir}
%global ruby_abi 1.9.1
%else
%global ruby_installdir %{ruby_sitearchdir}
%global ruby_abi 1.8
%endif
%endif

%if %($(pkg-config emacs) ; echo $?)
%global emacs_version 21.4
%global emacs_lispdir %{_datadir}/emacs/site-lisp
%else
%global emacs_version %(pkg-config emacs --modversion)
%global emacs_lispdir %(pkg-config emacs --variable sitepkglispdir)
%endif

%global xrootd 1

%{!?_pkgdocdir: %global _pkgdocdir %{_docdir}/%{name}-%{version}}

Name:		root
Version:	5.34.20
%global libversion %(cut -d. -f 1-2 <<< %{version})
Release:	1%{?dist}
Summary:	Numerical data analysis framework

Group:		Applications/Engineering
License:	LGPLv2+
URL:		http://root.cern.ch/		
#		The upstream source is modified to exclude proprietary fonts:
#		wget -N ftp://root.cern.ch/root/root_v%{version}.source.tar.gz
#		tar -z -x -f root_v%{version}.source.tar.gz
#		rm -rf root/fonts
#		mv root root-%{version}
#		tar -J -c -f root-%{version}.tar.xz root-%{version}
Source0:	%{name}-%{version}.tar.xz
#		Script to extract the list of include files in a subpackage
Source1:	root-includelist
#		Documentation generation script
Source2:	root-html.C
#		Images included in order to make documentation selfcontained
Source3:	http://root.cern.ch/drupal/sites/default/files/rootdrawing-logo.png
Source4:	http://root.cern.ch/drupal/sites/all/themes/newsflash/images/blue/root-banner.png
Source5:	http://root.cern.ch/drupal/sites/all/themes/newsflash/images/info.png
#		Use local copy of input file during documentation generation
Source6:	http://root.cern.ch/files/usa.root
#		Patch for ftgl older than version 2.1.3:
Patch0:		%{name}-ftgl.patch
#		Use system fonts:
Patch1:		%{name}-fontconfig.patch
#		Use system unuran:
Patch2:		%{name}-unuran.patch
#		Remove broken xrootd test:
Patch3:		%{name}-xrootd.patch
#		Fix hardcoded include path:
#		https://savannah.cern.ch/bugs/index.php?91463
Patch4:		%{name}-meta.patch
#		Use TLatex in doc generation:
Patch5:		%{name}-doc-latex.patch
#		Don't save in all image formats:
Patch6:		%{name}-no-extra-formats.patch
#		Fixes for HDFS module
Patch7:		%{name}-hdfs.patch
#		Don't link to libjvm (handled properly inside libhdfs)
Patch8:		%{name}-dont-link-jvm.patch
#		Avoid deprecated __USE_BSD
Patch9:		%{name}-bsd-misc.patch
#		Use local copy of input file during documentation generation
Patch10:	%{name}-usa.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
#		The build segfaults on ppc64 during an invocation of cint:
#		https://savannah.cern.ch/bugs/index.php?70542
ExcludeArch:	ppc64
#		The cint interpreter is not fully ported to arm
#		https://sft.its.cern.ch/jira/browse/ROOT-5398
#		https://sft.its.cern.ch/jira/browse/ROOT-5399
ExcludeArch:	%{arm}

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
%if %{?fedora}%{!?fedora:0} >= 13 || %{?rhel}%{!?rhel:0} >= 6
BuildRequires:	libAfterImage-devel >= 1.20
%else
BuildRequires:	libjpeg-devel
BuildRequires:	libpng-devel
BuildRequires:	libtiff-devel
%endif
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
BuildRequires:	mysql-devel
BuildRequires:	sqlite-devel
BuildRequires:	unixODBC-devel
BuildRequires:	mesa-libGL-devel
BuildRequires:	mesa-libGLU-devel
BuildRequires:	postgresql-devel
BuildRequires:	python-devel
%if "%{?rhel}" == "5"
BuildRequires:	python26-devel
%endif
%if %{?fedora}%{!?fedora:0} >= 9 || %{?rhel}%{!?rhel:0} >= 6
BuildRequires:	qt4-devel
%endif
BuildRequires:	ruby
BuildRequires:	ruby-devel
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
%if %{?fedora}%{!?fedora:0} >= 20
BuildRequires:	hadoop-devel
%endif
BuildRequires:	emacs
BuildRequires:	emacs-el
BuildRequires:	gcc-gfortran
BuildRequires:	graphviz-devel
%if "%{?rhel}" == "5"
BuildRequires:	graphviz-gd
%endif
BuildRequires:	expat-devel
%if %{?fedora}%{!?fedora:0} >= 18 || %{?rhel}%{!?rhel:0} >= 5
BuildRequires:	pythia8-devel >= 8.1.80
%endif
%if %{?fedora}%{!?fedora:0} >= 11 || %{?rhel}%{!?rhel:0} >= 6
BuildRequires:	font(liberationsans)
BuildRequires:	font(liberationserif)
BuildRequires:	font(liberationmono)
%else
BuildRequires:	liberation-fonts
%endif
BuildRequires:	urw-fonts
%if %{?fedora}%{!?fedora:0} >= 11 || %{?rhel}%{!?rhel:0} >= 6
BuildRequires:	font(droidsansfallback)
%endif
%if %{?fedora}%{!?fedora:0} >= 18 || %{?rhel}%{!?rhel:0} >= 7
# STIX font version 1.1 - not backwards compatible with earlier versions
# We use the texlive supplied version 1.0 instead of font(stix)
BuildRequires:	texlive-stix
%else
%if %{?fedora}%{!?fedora:0} >= 14
# STIX font version 1.0
BuildRequires:	font(stixgeneral)
BuildRequires:	font(stixsizeonesym)
%else
%if %{?fedora}%{!?fedora:0} >= 11 || %{?rhel}%{!?rhel:0} >= 6
# STIX font version 0.9
BuildRequires:	font(stixgeneral)
BuildRequires:	font(stixsize1)
%endif
%endif
%endif
Requires:	hicolor-icon-theme

%description
The ROOT system provides a set of object oriented frameworks with all
the functionality needed to handle and analyze large amounts of data
in a very efficient way. Having the data defined as a set of objects,
specialized storage methods are used to get direct access to the
separate attributes of the selected objects, without having to touch
the bulk of the data. Included are histogramming methods in 1, 2 and 3
dimensions, curve fitting, function evaluation, minimization, graphics
and visualization classes to allow the easy setup of an analysis
system that can query and process the data interactively or in batch
mode.

Thanks to the built in CINT C++ interpreter the command language, the
scripting, or macro, language and the programming language are all
C++. The interpreter allows for fast prototyping of the macros since
it removes the time consuming compile/link cycle. It also provides a
good environment to learn C++. If more performance is needed the
interactively developed macros can be compiled using a C++ compiler.

The system has been designed in such a way that it can query its
databases in parallel on MPP machines or on clusters of workstations
or high-end PCs. ROOT is an open system that can be dynamically
extended by linking external libraries. This makes ROOT a premier
platform on which to build data acquisition, simulation and data
analysis systems.

%package icons
Summary:	ROOT icon collection
Group:		Applications/Engineering
%if %{?fedora}%{!?fedora:0} >= 10 || %{?rhel}%{!?rhel:0} >= 6
BuildArch:	noarch
%endif
Requires:	%{name}-core = %{version}-%{release}

%description icons
This package contains icons used by the ROOT GUI.

%package doc
Summary:	Documentation for the ROOT system
Group:		Applications/Engineering
%if %{?fedora}%{!?fedora:0} >= 10 || %{?rhel}%{!?rhel:0} >= 6
BuildArch:	noarch
%endif
License:	LGPLv2+ and GPLv2+ and BSD
Requires:	%{name}-cint = %{version}-%{release}

%description doc
This package contains the automatically generated ROOT class
documentation.

%package tutorial
Summary:	ROOT tutorial scripts and test suite
Group:		Applications/Engineering
%if %{?fedora}%{!?fedora:0} >= 10 || %{?rhel}%{!?rhel:0} >= 6
BuildArch:	noarch
%endif
Requires:	%{name}-cint = %{version}-%{release}

%description tutorial
This package contains the tutorial scripts and test suite for ROOT.

%package core
Summary:	ROOT core libraries
Group:		Applications/Engineering
License:	LGPLv2+ and BSD
Requires:	%{name}-icons = %{version}-%{release}
Requires:	%{name}-graf-asimage%{?_isa} = %{version}-%{release}
Requires:	xorg-x11-fonts-ISO8859-1-75dpi
%if %{?fedora}%{!?fedora:0} >= 11 || %{?rhel}%{!?rhel:0} >= 6
Requires:	font(liberationsans)
Requires:	font(liberationserif)
Requires:	font(liberationmono)
%else
Requires:	liberation-fonts
%endif
Requires:	urw-fonts
%if %{?fedora}%{!?fedora:0} >= 11 || %{?rhel}%{!?rhel:0} >= 6
Requires:	font(droidsansfallback)
%endif
%if %{?fedora}%{!?fedora:0} >= 18 || %{?rhel}%{!?rhel:0} >= 7
# STIX font version 1.1 - not backwards compatible with earlier versions
# We use the texlive supplied version 1.0 instead of font(stix)
Requires:	texlive-stix
%else
%if %{?fedora}%{!?fedora:0} >= 14
# STIX font version 1.0
Requires:	font(stixgeneral)
Requires:	font(stixsizeonesym)
%else
%if %{?fedora}%{!?fedora:0} >= 11 || %{?rhel}%{!?rhel:0} >= 6
# STIX font version 0.9
Requires:	font(stixgeneral)
Requires:	font(stixsize1)
%endif
%endif
%endif

%description core
This package contains the core libraries used by ROOT: libCore, libNew,
libRint and libThread.

%package cint
Summary:	CINT C++ interpreter
Group:		Applications/Engineering
Obsoletes:	%{name}-cint7 < 5.26.00c
License:	MIT

%description cint
This package contains the CINT C++ interpreter version 5.

%package reflex
Summary:	Reflex dictionary generator
Group:		Applications/Engineering
Requires:	gccxml

%description reflex
This package contains the reflex dictionary generator for ROOT.

%ifarch %{ix86} x86_64
#		Cintex does not work on ppc
#		https://savannah.cern.ch/bugs/?22003#comment16
#		./configure only allows --enable-cintex for ix86 and x86_64
%package cintex
Summary:	Reflex to CINT dictionary converter
Group:		Applications/Engineering
Requires:	%{name}-python = %{version}-%{release}

%description cintex
Cintex is a library that converts Reflex dictionary information to
CINT data structures used by ROOT. This package allows to interact
with CINT with any class for which a Reflex dictionary is provided.
%endif

%package proofd
Summary:	Parallel ROOT Facility - distributed, parallel computing
Group:		Applications/Engineering
Requires:	%{name}-net-rpdutils%{?_isa} = %{version}-%{release}
Requires:	%{name}-proof%{?_isa} = %{version}-%{release}
%if %{xrootd}
Requires:	xrootd-server%{?_isa}
%endif
Requires(preun):	chkconfig
Requires(preun):	initscripts
Requires(post):		chkconfig
Requires(postun):	initscripts

%description proofd
This package contains the PROOF server. Proofd is the core daemon of
the PROOF (Parallel ROOT Facility) system for distributed parallel
computing. Installing this package on a machine makes it possible
for the machine to participate in a parallel computing farm (cluster
or via the Internet), either as a master or a slave, using a
transparent interface.

%package rootd
Summary:	ROOT remote file server
Group:		Applications/Engineering
Requires:	%{name}-net-rpdutils%{?_isa} = %{version}-%{release}
Requires(preun):	chkconfig
Requires(preun):	initscripts
Requires(post):		chkconfig
Requires(postun):	initscripts

%description rootd
This package contains the ROOT file server. Rootd is a server for ROOT
files, serving files over the Internet. Using this daemon, you can
access files on the machine from anywhere on the Internet, using a
transparent interface.

%package python
Summary:	Python extension for ROOT
Group:		Applications/Engineering

%description python
This package contains the Python extension for ROOT. This package
provide a Python interface to ROOT, and a ROOT interface to Python.

%if "%{?rhel}" == "5"
%package python26
Summary:	Python extension for ROOT
Group:		Applications/Engineering

%description python26
This package contains the Python extension for ROOT. This package
provide a Python interface to ROOT, and a ROOT interface to Python.
%endif

%package ruby
Summary:	Ruby extension for ROOT
Group:		Applications/Engineering
Provides:	ruby(libRuby) = %{version}
%if %{?ruby_abi:1}%{!?ruby_abi:0}
Requires:	ruby(abi) = %{ruby_abi}
%endif

%description ruby
This package contains the Ruby extension for ROOT. The interface
goes both ways - that is, you can call ROOT functions from Ruby, and
invoke the Ruby interpreter from ROOT.

%package genetic
Summary:	Genetic algorithms for ROOT
Group:		Applications/Engineering

%description genetic
This package contains a genetic minimizer module for ROOT.

%package geom
Summary:	Geometry library for ROOT
Group:		Applications/Engineering

%description geom
This package contains a library for defining geometries in ROOT.

%package gdml
Summary:	GDML import/export for ROOT geometries
Group:		Applications/Engineering
Requires:	%{name}-python = %{version}-%{release}

%description gdml
This package contains an import/export module for ROOT geometries.

%package graf
Summary:	2D graphics library for ROOT
Group:		Applications/Engineering

%description graf
This package contains the 2-dimensional graphics library for ROOT.

%package graf-asimage
Summary:	AfterImage graphics renderer for ROOT
Group:		Applications/Engineering

%description graf-asimage
This package contains the AfterImage renderer for ROOT, which allows
you to store output graphics in many formats, including JPEG, PNG and
TIFF.

%package graf-fitsio
Summary:	ROOT interface for the Flexible Image Transport System (FITS)
Group:		Applications/Engineering

%description graf-fitsio
This package contains a library for using the Flexible Image Transport
System (FITS) data format in root.

%package graf-gpad
Summary:	Canvas and pad library for ROOT
Group:		Applications/Engineering
Requires:	%{name}-graf-postscript%{?_isa} = %{version}-%{release}

%description graf-gpad
This package contains a library for canvas and pad manipulations.

%package graf-gviz
Summary:	Graphviz 2D library for ROOT
Group:		Applications/Engineering

%description graf-gviz
This package contains the 2-dimensional graphviz library for ROOT.

%package graf-postscript
Summary:	Postscript/PDF renderer library for ROOT
Group:		Applications/Engineering

%description graf-postscript
This package contains a library for ROOT, which allows rendering
postscript and PDF output.

%if %{?fedora}%{!?fedora:0} >= 9 || %{?rhel}%{!?rhel:0} >= 6
%package graf-qt
Summary:	Qt renderer for ROOT
Group:		Applications/Engineering

%description graf-qt
This package contains the Qt renderer for ROOT.
%endif

%package graf-x11
Summary:	X window system renderer for ROOT
Group:		Applications/Engineering

%description graf-x11
This package contains the X11 renderer for ROOT, which allows using an
X display for showing graphics.

%package graf3d
Summary:	Basic 3D shapes library for ROOT
Group:		Applications/Engineering

%description graf3d
This library contains the basic 3D shapes and classes for ROOT. For
a more full-blown geometry library, see the root-geom package.

%package graf3d-eve
Summary:	Event display library for ROOT
Group:		Applications/Engineering

%description graf3d-eve
This package contains a library for defining event displays in ROOT.

%package graf3d-gl
Summary:	GL renderer for ROOT
Group:		Applications/Engineering

%description graf3d-gl
This package contains the GL renderer for ROOT. This library provides
3D rendering of volumes and shapes defined in ROOT, as well as 3D
rendering of histograms, and similar. Included is also a high quality
3D viewer for ROOT defined geometries.

%package graf3d-gviz3d
Summary:	Graphviz 3D library for ROOT
Group:		Applications/Engineering

%description graf3d-gviz3d
This package contains the 3-dimensional graphviz library for ROOT.

%package graf3d-x3d
Summary:	X 3D renderer for ROOT
Group:		Applications/Engineering

%description graf3d-x3d
This package contains the X 3D renderer for ROOT. This library provides
3D rendering of volumes and shapes defined in ROOT. Included is also
a low quality 3D viewer for ROOT defined geometries.

%package gui
Summary:	GUI library for ROOT
Group:		Applications/Engineering
Requires:	%{name}-graf-x11%{?_isa} = %{version}-%{release}
Requires:	%{name}-gui-ged%{?_isa} = %{version}-%{release}

%description gui
This package contains a library for defining graphical user interfaces.

%package gui-fitpanel
Summary:	GUI element for fits in ROOT
Group:		Applications/Engineering

%description gui-fitpanel
This package contains a library to show a pop-up dialog when fitting
various kinds of data.

%package gui-ged
Summary:	GUI element for editing various ROOT objects
Group:		Applications/Engineering
Requires:	%{name}-tree-player%{?_isa} = %{version}-%{release}

%description gui-ged
This package contains a library to show a pop-up window for editing
various ROOT objects.

%package guibuilder
Summary:	GUI editor library for ROOT
Group:		Applications/Engineering

%description guibuilder
This package contains a library for editing graphical user interfaces
in ROOT.

%if %{?fedora}%{!?fedora:0} >= 9 || %{?rhel}%{!?rhel:0} >= 6
%package gui-qt
Summary:	Qt GUI for ROOT
Group:		Applications/Engineering

%description gui-qt
This package contains the Qt GUI for ROOT.
%endif

%package gui-recorder
Summary:	Interface for recording and replaying events in ROOT
Group:		Applications/Engineering

%description gui-recorder
This library provides interface for recording and replaying events in ROOT.
Recorded events are:
 - Commands typed by user in command line ('new TCanvas')
 - GUI events (mouse movement, button clicks, ...)
All the recorded events from one session are stored in one TFile
and can be replayed again anytime.

%package hbook
Summary:	Hbook library for ROOT
Group:		Applications/Engineering

%description hbook
This package contains the Hbook library for ROOT, allowing you to
access legacy Hbook files (NTuples and Histograms from PAW).

%package hist
Summary:	Histogram library for ROOT
Group:		Applications/Engineering
Requires:	%{name}-hist-painter%{?_isa} = %{version}-%{release}

%description hist
This package contains a library for histogramming in ROOT.

%package hist-painter
Summary:	Histogram painter plugin for ROOT
Group:		Applications/Engineering

%description hist-painter
This package contains a painter of histograms for ROOT.

%package spectrum
Summary:	Spectra analysis library for ROOT
Group:		Applications/Engineering

%description spectrum
This package contains the Spectrum library for ROOT.

%package spectrum-painter
Summary:	Spectrum painter plugin for ROOT
Group:		Applications/Engineering

%description spectrum-painter
This package contains a painter of spectra for ROOT.

%package hist-factory
Summary:	RooFit PDFs from ROOT histograms
Group:		Applications/Engineering

%description hist-factory
Create RooFit probability density functions from ROOT histograms.

%package html
Summary:	HTML documentation generator for ROOT
Group:		Applications/Engineering
Requires:	graphviz

%description html
This package contains classes to automatically extract documentation
from marked up sources.

%package io
Summary:	Input/output of ROOT objects
Group:		Applications/Engineering

%description io
This package provides I/O routines for ROOT objects.

%package io-dcache
Summary:	dCache input/output library for ROOT
Group:		Applications/Engineering

%description io-dcache
This package contains the dCache extension for ROOT.

%package io-gfal
Summary:	Grid File Access Library input/output library for ROOT
Group:		Applications/Engineering

%description io-gfal
This package contains the Grid File Access Library extension for ROOT.

%if %{?fedora}%{!?fedora:0} >= 20
%package io-hdfs
Summary:	Hadoop File System input/output library for ROOT
Group:		Applications/Engineering

%description io-hdfs
This package contains the Hadoop File System extension for ROOT.
%endif

%package io-rfio
Summary:	Remote File input/output library for ROOT
Group:		Applications/Engineering

%description io-rfio
This package contains the Remote File IO extension for ROOT.

%package io-sql
Summary:	SQL input/output library for ROOT
Group:		Applications/Engineering

%description io-sql
This package contains the SQL extension for ROOT, that allows
transparent access to files data via an SQL database, using ROOT's
TFile interface.

%package io-xml
Summary:	XML reader library for ROOT
Group:		Applications/Engineering

%description io-xml
This package contains the XML reader library for ROOT.

%package foam
Summary:	A Compact Version of the Cellular Event Generator
Group:		Applications/Engineering

%description foam
The general-purpose self-adapting Monte Carlo (MC) event
generator/simulator mFOAM (standing for mini-FOAM) is a new compact
version of the FOAM program, with a slightly limited functionality
with respect to its parent version. On the other hand, mFOAM is
easier to use for the average user.

%package fftw
Summary:	FFTW library for ROOT
Group:		Applications/Engineering
License:	GPLv2+

%description fftw
This package contains the Fast Fourier Transform extension for ROOT.
It uses the very fast fftw (version 3) library.

%package fumili
Summary:	Fumili library for ROOT
Group:		Applications/Engineering

%description fumili
This package contains the fumili library for ROOT. This provides an
alternative fitting algorithm for ROOT.

%package genvector
Summary:	Generalized vector library for ROOT
Group:		Applications/Engineering

%description genvector
This package contains the Genvector library for ROOT. This provides
a generalized vector library.

%package mathcore
Summary:	Core mathematics library for ROOT
Group:		Applications/Engineering
Requires:	%{name}-minuit%{?_isa} = %{version}-%{release}

%description mathcore
This package contains the MathCore library for ROOT.

%package mathmore
Summary:	GSL interface library for ROOT
Group:		Applications/Engineering
License:	GPLv2+

%description mathmore
This package contains the MathMore library for ROOT. This provides
a partial GNU Scientific Library interface for ROOT.
While the rest of root is licensed under LGPLv2+ this optional library
is licensed under GPLv2+ due to its use of GSL.

%package matrix
Summary:	Matrix library for ROOT
Group:		Applications/Engineering

%description matrix
This package contains the Matrix library for ROOT.

%package minuit
Summary:	Minuit library for ROOT
Group:		Applications/Engineering

%description minuit
This package contains the MINUIT library for ROOT. This provides a
fitting algorithm for ROOT.

%package minuit2
Summary:	Minuit version 2 library for ROOT
Group:		Applications/Engineering

%description minuit2
This package contains the MINUIT version 2 library for ROOT. This
provides an fitting algorithm for ROOT.

%package mlp
Summary:	Multi-layer perceptron extension for ROOT
Group:		Applications/Engineering

%description mlp
This package contains the mlp library for ROOT. This library provides
a multi-layer perceptron neural network package for ROOT.

%package physics
Summary:	Physics library for ROOT
Group:		Applications/Engineering

%description physics
This package contains the physics library for ROOT.

%package quadp
Summary:	QuadP library for ROOT
Group:		Applications/Engineering

%description quadp
This package contains the QuadP library for ROOT. This provides the a
framework in which to do Quadratic Programming. The quadratic
programming problem involves minimization of a quadratic function
subject to linear constraints.

%package smatrix
Summary:	Sparse matrix library for ROOT
Group:		Applications/Engineering

%description smatrix
This package contains the Smatrix library for ROOT.

%package splot
Summary:	Splot library for ROOT
Group:		Applications/Engineering

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
Group:		Applications/Engineering
License:	GPLv2+

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

%package vdt
Summary:	VDT mathematical library
Group:		Applications/Engineering

%description vdt
VDT is a library of mathematical functions, implemented in double and
single precision. The implementation is fast and with the aid of
modern compilers (e.g. gcc 4.7) vectorisable.

%package memstat
Summary:	Memory statistics tool for use with ROOT
Group:		Applications/Engineering

%description memstat
This package contains the memory statistics tool for debugging memory
leaks and such.

%package table
Summary:	Table library for ROOT
Group:		Applications/Engineering

%description table
This package contains the Table library for ROOT.

%package montecarlo-eg
Summary:	Event generator library for ROOT
Group:		Applications/Engineering

%description montecarlo-eg
This package contains an event generator library for ROOT.

%if %{?fedora}%{!?fedora:0} >= 18 || %{?rhel}%{!?rhel:0} >= 5
%package montecarlo-pythia8
Summary:	Pythia version 8 plugin for ROOT
Group:		Applications/Engineering

%description montecarlo-pythia8
This package contains the Pythia version 8 plug-in for ROOT. This
package provide the ROOT user with transparent interface to the Pythia
(version 8) event generators for hadronic interactions. If the term
"hadronic" does not ring any bells, this package is not for you.
%endif

%package montecarlo-vmc
Summary:	Virtual Monte-Carlo (simulation) library for ROOT
Group:		Applications/Engineering

%description montecarlo-vmc
This package contains the VMC library for ROOT.

%package net
Summary:	Net library for ROOT
Group:		Applications/Engineering

%description net
This package contains the ROOT networking library.

%package net-rpdutils
Summary:	Authentication utilities used by rootd and proofd
Group:		Applications/Engineering

%description net-rpdutils
This package contains authentication utilities used by rootd and proofd.

%package net-bonjour
Summary:	Bonjour extension for ROOT
Group:		Applications/Engineering

%description net-bonjour
This package contains a bonjour extension for ROOT.

%package net-auth
Summary:	Authentication extension for ROOT
Group:		Applications/Engineering

%description net-auth
This package contains the basic authentication algorithms used by ROOT.

%package net-davix
Summary:	Davix extension for ROOT
Group:		Applications/Engineering
Requires:	davix-libs%{?_isa} >= 0.2.8

%description net-davix
This package contains the davix extension for ROOT, that provides
access to http based storage such as webdav and S3.

%package net-globus
Summary:	Globus extension for ROOT
Group:		Applications/Engineering
Requires:	globus-proxy-utils

%description net-globus
This package contains the Globus extension for ROOT, that allows
authentication and authorization against Globus.

%package net-krb5
Summary:	Kerberos (version 5) extension for ROOT
Group:		Applications/Engineering
Requires:	krb5-workstation

%description net-krb5
This package contains the Kerberos (version 5) extension for ROOT, that
allows authentication and authorization using Kerberos tokens.

%package net-ldap
Summary:	LDAP extension for ROOT
Group:		Applications/Engineering

%description net-ldap
This package contains the LDAP extension for ROOT. This gives you
access to LDAP directories via ROOT.

%package net-http
Summary:	HTTP server extension for ROOT
Group:		Applications/Engineering

%description net-http
This package contains the HTTP server extension for ROOT. It provides
an http interface to arbitrary ROOT applications.

%if %{xrootd}
%package netx
Summary:	NetX extension for ROOT
Group:		Applications/Engineering

%description netx
This package contains the NetX extension for ROOT, i.e. a client for
the xrootd server. Both the old (NetX) and the new (NetXNG) version are
provided.
%endif

%package proof
Summary:	PROOF extension for ROOT
Group:		Applications/Engineering
Obsoletes:	%{name}-clarens < 5.34.01
Obsoletes:	%{name}-peac < 5.34.01

%description proof
This package contains the proof extension for ROOT. This provides a
client to use in a PROOF environment.

%package proof-bench
Summary:	PROOF benchmarking
Group:		Applications/Engineering

%description proof-bench
This package contains the steering class for PROOF benchmarks.

%package proof-pq2
Summary:	PROOF Quick Query (pq2)
Group:		Applications/Engineering

%description proof-pq2
Shell-based interface to the PROOF dataset handling.

%package proof-sessionviewer
Summary:	GUI to browse an interactive PROOF session
Group:		Applications/Engineering

%description proof-sessionviewer
This package contains a library for browsing an interactive PROOF
session in ROOT.

%if %{xrootd}
%package xproof
Summary:	XPROOF extension for ROOT
Group:		Applications/Engineering

%description xproof
This package contains the xproof extension for ROOT. This provides a
client to be used in a PROOF environment.
%endif

%package roofit
Summary:	ROOT extension for modeling expected distributions
Group:		Applications/Engineering
License:	BSD

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
Group:		Applications/Engineering

%description sql-mysql
This package contains the MySQL plugin for ROOT. This plugin
provides a thin client (interface) to MySQL servers. Using this
client, one can obtain information from a MySQL database into the
ROOT environment.

%package sql-odbc
Summary:	ODBC plugin for ROOT
Group:		Applications/Engineering

%description sql-odbc
This package contains the ODBC (Open DataBase Connectivity) plugin
for ROOT, that allows transparent access to any kind of database that
supports the ODBC protocol.

%package sql-sqlite
Summary:	Sqlite client plugin for ROOT
Group:		Applications/Engineering

%description sql-sqlite
This package contains the sqlite plugin for ROOT. This plugin
provides a thin client (interface) to sqlite servers. Using this
client, one can obtain information from a sqlite database into the
ROOT environment.

%package sql-pgsql
Summary:	PostgreSQL client plugin for ROOT
Group:		Applications/Engineering

%description sql-pgsql
This package contains the PostGreSQL plugin for ROOT. This plugin
provides a thin client (interface) to PostGreSQL servers. Using this
client, one can obtain information from a PostGreSQL database into the
ROOT environment.

%package tmva
Summary:	Toolkit for multivariate data analysis
Group:		Applications/Engineering
License:	BSD

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

%package tree
Summary:	Tree library for ROOT
Group:		Applications/Engineering

%description tree
This package contains the Tree library for ROOT.

%package tree-player
Summary:	Library to loop over a ROOT tree
Group:		Applications/Engineering

%description tree-player
This package contains a plugin to loop over a ROOT tree.

%package tree-viewer
Summary:	GUI to browse a ROOT tree
Group:		Applications/Engineering

%description tree-viewer
This package contains a plugin for browsing a ROOT tree in ROOT.

%package -n emacs-%{name}
Summary:	Compiled elisp files to run root under GNU Emacs
Group:		Applications/Engineering
%if %{?fedora}%{!?fedora:0} >= 10 || %{?rhel}%{!?rhel:0} >= 6
BuildArch:	noarch
%endif
Requires:	%{name} = %{version}-%{release}
%if "%{?rhel}" == "5"
Requires:	emacs >= %{emacs_version}
%else
Requires:	emacs(bin) >= %{emacs_version}
%endif

%description -n emacs-%{name}
emacs-root is an add-on package for GNU Emacs. It provides integration
with ROOT.

%package -n emacs-%{name}-el
Summary:	Elisp source files for root under GNU Emacs
Group:		Applications/Engineering
%if %{?fedora}%{!?fedora:0} >= 10 || %{?rhel}%{!?rhel:0} >= 6
BuildArch:	noarch
%endif
Requires:	emacs-%{name} = %{version}-%{release}

%description -n emacs-%{name}-el
This package contains the elisp source files for root under GNU Emacs. You
do not need to install this package to run root. Install the emacs-root
package to use root with GNU Emacs.

%prep
%setup -q
if pkg-config --max-version 2.1.2 ftgl ; then
%patch0 -p1
fi
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

find . '(' -name '*.cxx' -o -name '*.cpp' -o -name '*.C' -o -name '*.c' -o \
	   -name '*.h' -o -name '*.hh' -o -name '*.hi' -o -name '*.py' -o \
	   -name '*.html' -o -name '*.js' -o -name '*.css' -o \
	   -name '*.xpm' -o -name '*.gif' -o -name '*.png' \
       ')' -exec chmod 644 {} ';'

chmod 644 cint/cint/include/makehpib \
	  cint/cint/stl/_climits \
	  test/DrawTest.sh \
	  test/dt_RunDrawTest.sh \
	  test/dt_MakeFiles.sh \
	  test/ProofBench/make_event_par.sh \
	  test/RootIDE/Makefile \
	  tutorials/fitsio/sample1.fits

# Badly named file - not python - aborts python byte compilation
mv tutorials/pyroot/fit1_py.py tutorials/pyroot/fit1_py.txt
sed s/fit1_py.py/fit1_py.txt/ -i tutorials/pyroot/fit1.py

# Remove embedded sources in order to be sure they are not used
#  * afterimage
%if %{?fedora}%{!?fedora:0} >= 13 || %{?rhel}%{!?rhel:0} >= 6
rm -rf graf2d/asimage/src/libAfterImage
%else
rm -rf graf2d/asimage/src/libAfterImage/libjpeg
rm -rf graf2d/asimage/src/libAfterImage/libpng
rm -rf graf2d/asimage/src/libAfterImage/zlib
sed '/zlib\/zlib.h/d' -i graf2d/asimage/src/libAfterImage/.depend
%endif
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
rm graf3d/gl/src/gl2ps.cxx graf3d/gl/inc/gl2ps.h
sed 's/^GLLIBS *:= .* $(OPENGLLIB)/& -lgl2ps/' -i graf3d/gl/Module.mk
#  * unuran
rm -rf math/unuran/src/*.tar.gz

# Remove unsupported man page macros
sed -e '/^\.UR/d' -e '/^\.UE/d' -i man/man1/*

# Make images local
sed 's!http://root.cern.ch/drupal/sites/all/themes/newsflash/images/blue/!!' \
    -i etc/html/ROOT.css
sed 's!http://root.cern.ch/drupal/sites/all/themes/newsflash/images/!!' \
    -i etc/html/ROOT.css
sed 's!http://root.cern.ch/drupal/sites/default/files/!!' \
    -i etc/html/header.html
install -p -m 644 %{SOURCE3} %{SOURCE4} %{SOURCE5} etc/html
sed '/CopyFileFromEtcDir("ROOT.css");/a\
   CopyFileFromEtcDir("info.png");\
   CopyFileFromEtcDir("root-banner.png");\
   CopyFileFromEtcDir("rootdrawing-logo.png");' -i html/src/THtml.cxx

# Rename canvases to avoid name conflicts during doc generation
sed s/c1/c1c/g -i tutorials/graphics/earth.C
sed s/c3/c3c/g -i tutorials/graphs/multipalette.C
sed s/c1/c1simp/g -i tutorials/hsimple.C

%if "%{?rhel}" == "5"
# Build PyROOT for python 2.6
cp -pr bindings/pyroot bindings/pyroot26
sed -e 's/= pyroot/= pyroot26/' -e 's/python /python26 /' \
    -i bindings/pyroot26/Module.mk
%endif

%build
unset QTDIR
unset QTLIB
unset QTINC
./configure --prefix=%{_prefix} \
	    --libdir=%{_libdir}/%{name} \
	    --etcdir=%{_datadir}/%{name} \
	    --docdir=%{_pkgdocdir} \
	    --elispdir=%{emacs_lispdir}/%{name} \
%if %{?fedora}%{!?fedora:0} >= 13 || %{?rhel}%{!?rhel:0} >= 6
	    --disable-builtin-afterimage \
%else
	    --enable-builtin-afterimage \
%endif
	    --disable-builtin-ftgl \
	    --disable-builtin-freetype \
	    --disable-builtin-glew \
	    --disable-builtin-lzma \
	    --disable-builtin-pcre \
	    --disable-builtin-zlib \
	    --enable-asimage \
	    --enable-astiff \
	    --enable-bonjour \
	    --enable-davix \
	    --enable-dcache \
	    --enable-explicitlink \
	    --enable-fftw3 \
	    --enable-fitsio \
	    --enable-gdml \
	    --enable-genvector \
	    --enable-gfal \
	      --with-gfal-incdir=%{_includedir}/gfal2 \
	      --with-gfal-libdir=%{_libdir} \
	    --enable-globus \
	    --enable-gsl-shared \
	    --enable-gviz \
%if %{?fedora}%{!?fedora:0} >= 20
	    --enable-hdfs \
	      --with-hdfs-incdir=%{_includedir}/hadoop \
%else
	    --disable-hdfs \
%endif
	    --enable-http \
	    --enable-krb5 \
	    --enable-ldap \
	    --enable-mathmore \
	    --enable-memstat \
	    --enable-minuit2 \
	    --enable-mysql \
	    --enable-odbc \
	    --enable-opengl \
	    --enable-pgsql \
	    --enable-python \
%if %{?fedora}%{!?fedora:0} >= 18 || %{?rhel}%{!?rhel:0} >= 5
	    --enable-pythia8 \
%else
	    --disable-pythia8 \
%endif
%if %{?fedora}%{!?fedora:0} >= 9 || %{?rhel}%{!?rhel:0} >= 6
	    --enable-qt \
	    --enable-qtgsi \
%else
	    --disable-qt \
	    --disable-qtgsi \
%endif
	    --enable-reflex \
	    --enable-rfio \
	      --with-rfio-incdir=%{_includedir}/dpm \
	      --with-rfio-libdir=%{_libdir} \
	    --enable-roofit \
	    --enable-ruby \
	    --enable-shadowpw \
	    --enable-shared \
	    --enable-soversion \
	    --enable-sqlite \
	    --enable-ssl \
	    --enable-table \
	    --enable-tmva \
	    --enable-unuran \
	    --enable-vdt \
	    --enable-x11 \
	    --enable-xft \
	    --enable-xml \
%if %{xrootd}
	    --enable-xrootd \
	      --with-xrootd-incdir=%{_includedir}/xrootd \
	      --with-xrootd-libdir=%{_libdir} \
%else
	    --disable-xrootd \
%endif
%ifarch %{ix86} x86_64
	    --enable-cintex \
%else
	    --disable-cintex \
%endif
	    --disable-afdsmgrd \
	    --disable-afs \
	    --disable-alien \
	    --disable-alloc \
	    --disable-castor \
	    --disable-chirp \
	    --disable-cling \
	    --disable-cxx11 \
	    --disable-glite \
	    --disable-libcxx \
	    --disable-monalisa \
	    --disable-oracle \
	    --disable-pythia6 \
	    --disable-rpath \
	    --disable-sapdb \
	    --disable-srp \
	    --disable-vc \
	    --disable-werror \
	    --fail-on-missing

make OPTFLAGS="%{optflags}" \
	EXTRA_LDFLAGS="%{?__global_ldflags}" %{?_smp_mflags}

%if "%{?rhel}" == "5"
# Build PyROOT for python 2.6
mkdir pyroot26
cp bindings/pyroot26/ROOT.py pyroot26
cp bindings/pyroot26/cppyy.py pyroot26
make OPTFLAGS="%{optflags}" \
	EXTRA_LDFLAGS="%{?__global_ldflags}" %{?_smp_mflags} \
	MODULES="build cint/cint core/utils bindings/pyroot26" \
	PYTHONINCDIR=/usr/include/python2.6 PYTHONLIB=-lpython2.6 \
	PYROOTLIB=pyroot26/libPyROOT.so \
	ROOTPY="pyroot26/ROOT.py pyroot26/cppyy.py"
%endif

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}

# Move python modules to the sitelib
mkdir -p ${RPM_BUILD_ROOT}%{python_sitearch}
mv ${RPM_BUILD_ROOT}%{_libdir}/%{name}/*.py* \
   ${RPM_BUILD_ROOT}%{python_sitearch}

# Do emacs byte compilation
emacs -batch -no-site-file -f batch-byte-compile \
    ${RPM_BUILD_ROOT}%{emacs_lispdir}/%{name}/*.el

# Install desktop entry and icon
mkdir -p ${RPM_BUILD_ROOT}%{_datadir}/applications
mkdir -p ${RPM_BUILD_ROOT}%{_datadir}/icons/hicolor/48x48/apps

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

desktop-file-install --dir=${RPM_BUILD_ROOT}%{_datadir}/applications \
		     --vendor "" root.desktop
install -p -m 644 build/package/debian/root-system-bin.png \
    ${RPM_BUILD_ROOT}%{_datadir}/icons/hicolor/48x48/apps/root.png

# Install mime type and icon
mkdir -p ${RPM_BUILD_ROOT}%{_datadir}/mime/packages
mkdir -p ${RPM_BUILD_ROOT}%{_datadir}/icons/hicolor/48x48/mimetypes
install -p -m 644 build/package/debian/root-system-bin.sharedmimeinfo \
    ${RPM_BUILD_ROOT}%{_datadir}/mime/packages/root.xml
install -p -m 644 build/package/debian/application-x-root.png \
    ${RPM_BUILD_ROOT}%{_datadir}/icons/hicolor/48x48/mimetypes

# Init scripts for services
mkdir -p ${RPM_BUILD_ROOT}%{_initrddir}
mv ${RPM_BUILD_ROOT}%{_datadir}/%{name}/daemons/proofd.rc.d \
   ${RPM_BUILD_ROOT}%{_initrddir}/proofd
mv ${RPM_BUILD_ROOT}%{_datadir}/%{name}/daemons/rootd.rc.d \
   ${RPM_BUILD_ROOT}%{_initrddir}/rootd

# Turn off services by default
sed 's/\(chkconfig: \)[0-9]*/\1-/' -i ${RPM_BUILD_ROOT}%{_initrddir}/*

# The Python interface library must be in two places
mkdir -p ${RPM_BUILD_ROOT}%{python_sitearch}
mv ${RPM_BUILD_ROOT}%{_libdir}/%{name}/libPyROOT.so.%{libversion} \
   ${RPM_BUILD_ROOT}%{python_sitearch}/libPyROOT.so
%if "%{?rhel}" == "5"
touch ${RPM_BUILD_ROOT}%{_libdir}/%{name}/libPyROOT.so.%{libversion}
%else
ln -s ..`sed 's!%{_libdir}!!' <<< %{python_sitearch}`/libPyROOT.so \
   ${RPM_BUILD_ROOT}%{_libdir}/%{name}/libPyROOT.so.%{libversion}
%endif

%if "%{?rhel}" == "5"
mkdir -p ${RPM_BUILD_ROOT}%{python26_sitearch}
install pyroot26/libPyROOT.so.%{libversion} \
   ${RPM_BUILD_ROOT}%{python26_sitearch}/libPyROOT.so
install -m 644 pyroot26/ROOT.py* ${RPM_BUILD_ROOT}%{python26_sitearch}
install -m 644 pyroot26/cppyy.py* ${RPM_BUILD_ROOT}%{python26_sitearch}
%endif

# Same for the Ruby interface library
mkdir -p ${RPM_BUILD_ROOT}%{ruby_installdir}
mv ${RPM_BUILD_ROOT}%{_libdir}/%{name}/libRuby.so.%{libversion} \
   ${RPM_BUILD_ROOT}%{ruby_installdir}/libRuby.so
ln -s ..`sed 's!%{_libdir}!!' <<< %{ruby_installdir}`/libRuby.so \
   ${RPM_BUILD_ROOT}%{_libdir}/%{name}/libRuby.so.%{libversion}

# These should be in PATH
mv ${RPM_BUILD_ROOT}%{_datadir}/%{name}/proof/utils/pq2/pq2* \
   ${RPM_BUILD_ROOT}%{_bindir}

# Remove some junk
rm ${RPM_BUILD_ROOT}%{_datadir}/%{name}/daemons/*.plist
rm ${RPM_BUILD_ROOT}%{_datadir}/%{name}/daemons/*.xinetd
rm ${RPM_BUILD_ROOT}%{_datadir}/%{name}/daemons/README
rm ${RPM_BUILD_ROOT}%{_datadir}/%{name}/hostcert.conf
rm ${RPM_BUILD_ROOT}%{_datadir}/%{name}/proof/*.sample
rm -rf ${RPM_BUILD_ROOT}%{_datadir}/%{name}/proof/utils
rm ${RPM_BUILD_ROOT}%{_datadir}/%{name}/root.desktop
rm ${RPM_BUILD_ROOT}%{_datadir}/%{name}/system.plugins-ios
rm ${RPM_BUILD_ROOT}%{_datadir}/%{name}/gitinfo.txt
%if %{?fedora}%{!?fedora:0} < 13 && %{?rhel}%{!?rhel:0} < 6
rm ${RPM_BUILD_ROOT}%{_libdir}/%{name}/libAfterImage.a
%endif
rm ${RPM_BUILD_ROOT}%{_libdir}/%{name}/libmathtext.a
rm ${RPM_BUILD_ROOT}%{_bindir}/setxrd*
rm ${RPM_BUILD_ROOT}%{_bindir}/thisroot*
rm ${RPM_BUILD_ROOT}%{_mandir}/man1/cint.1
rm ${RPM_BUILD_ROOT}%{_mandir}/man1/g2rootold.1
rm ${RPM_BUILD_ROOT}%{_mandir}/man1/makecint.1
rm ${RPM_BUILD_ROOT}%{_mandir}/man1/proofserva.1
rm ${RPM_BUILD_ROOT}%{_mandir}/man1/roota.1
rm ${RPM_BUILD_ROOT}%{_mandir}/man1/setup-pq2.1
%if %{xrootd} == 0
rm ${RPM_BUILD_ROOT}%{_mandir}/man1/xproofd.1
%endif
%if %{?fedora}%{!?fedora:0} >= 9 || %{?rhel}%{!?rhel:0} >= 6
rm ${RPM_BUILD_ROOT}%{_includedir}/%{name}/*.cw
rm ${RPM_BUILD_ROOT}%{_includedir}/%{name}/*.pri
%endif
rm ${RPM_BUILD_ROOT}%{_includedir}/%{name}/proofdp.h
rm ${RPM_BUILD_ROOT}%{_includedir}/%{name}/rootdp.h
rm ${RPM_BUILD_ROOT}%{_pkgdocdir}/BUILDSYSTEM
rm ${RPM_BUILD_ROOT}%{_pkgdocdir}/ChangeLog-2-24
rm ${RPM_BUILD_ROOT}%{_pkgdocdir}/INSTALL
rm ${RPM_BUILD_ROOT}%{_pkgdocdir}/README.ALIEN
rm ${RPM_BUILD_ROOT}%{_pkgdocdir}/README.MONALISA

# Remove cintdll sources - keep the prec_stl directory
rm -rf ${RPM_BUILD_ROOT}%{_libdir}/%{name}/cint/cint/lib/{[^p],p[^r]}*

# Only used on Windows
rm ${RPM_BUILD_ROOT}%{_datadir}/%{name}/macros/fileopen.C

# Remove plugin definitions for non-built and obsolete plugins
pushd ${RPM_BUILD_ROOT}%{_datadir}/%{name}/plugins
rm TAFS/P010_TAFS.C
rm TDataProgressDialog/P010_TDataProgressDialog.C
rm TDataSetManager/P020_TDataSetManagerAliEn.C
rm TFile/P030_TCastorFile.C
rm TFile/P060_TChirpFile.C
rm TFile/P070_TAlienFile.C
%if %{?fedora}%{!?fedora:0} < 20
rm TFile/P110_THDFSFile.C
%endif
rm TGLManager/P020_TGWin32GLManager.C
rm TGLManager/P030_TGOSXGLManager.C
rm TGrid/P010_TAlien.C
rm TGrid/P020_TGLite.C
%if %{?fedora}%{!?fedora:0} < 9 && %{?rhel}%{!?rhel:0} < 6
rm TGuiFactory/P020_TQtRootGuiFactory.C
%endif
rm TImagePlugin/P010_TASPluginGS.C
rm TSQLServer/P030_TSapDBServer.C
rm TSQLServer/P040_TOracleServer.C
rm TSystem/P030_TAlienSystem.C
%if %{?fedora}%{!?fedora:0} < 20
rm TSystem/P060_THDFSSystem.C
%endif
rm TViewerX3D/P020_TQtViewerX3D.C
rm TVirtualGLImp/P020_TGWin32GL.C
rm TVirtualMonitoringWriter/P010_TMonaLisaWriter.C
rm TVirtualX/P030_TGWin32.C
%if %{?fedora}%{!?fedora:0} < 9 && %{?rhel}%{!?rhel:0} < 6
rm TVirtualX/P040_TGQt.C
%endif
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
popd

# Create ldconfig configuration
mkdir -p ${RPM_BUILD_ROOT}%{_sysconfdir}/ld.so.conf.d
echo %{_libdir}/%{name} > \
     ${RPM_BUILD_ROOT}%{_sysconfdir}/ld.so.conf.d/%{name}-%{_arch}.conf

# Generate documentation
echo Rint.Includes: 0 > .rootrc
echo Cint.Includes: 0 >> .rootrc
echo Root.StacktraceScript: ${PWD}/etc/gdb-backtrace.sh >> .rootrc
echo Gui.MimeTypeFile: ${PWD}/etc/root.mimes >> .rootrc
sed "s!@PWD@!${PWD}!g" %{SOURCE2} > html.C
install -m 644 -p %{SOURCE6} tutorials/hist/usa.root
LD_LIBRARY_PATH=${PWD}/lib:${PWD}/cint/cint/include:${PWD}/cint/cint/stl \
ROOTSYS=${PWD} ./bin/root.exe -l -b -q html.C
rm .rootrc
mv htmldoc ${RPM_BUILD_ROOT}%{_pkgdocdir}/html

# Create includelist files ...
for module in `find * -name Module.mk` ; do
    module=`dirname $module`
    make -f %{SOURCE1} includelist MODULE=$module
done

# ... and merge some of them
cat includelist-core-{[^mw],m[^a]}* > includelist-core
cat includelist-geom-geom* > includelist-geom
cat includelist-roofit-roo* > includelist-roofit
cat includelist-gui-qt* > includelist-gui-qt
cat includelist-graf2d-x11ttf >> includelist-graf2d-x11
cat includelist-gui-guihtml >> includelist-gui-gui
cat includelist-io-xmlparser >> includelist-io-xml
cat includelist-proof-proofplayer >> includelist-proof-proof
cat includelist-net-netx* > includelist-netx

%if "%{?rhel}" == "5"
# Python byte code compilation
%{__python} -c 'import compileall; compileall.compile_dir("%{buildroot}%{_libdir}/%{name}/python", 10, "%{_libdir}/%{name}/python", 1)' > /dev/null
%{__python} -O -c 'import compileall; compileall.compile_dir("%{buildroot}%{_libdir}/%{name}/python", 10, "%{_libdir}/%{name}/python", 1)' > /dev/null
%{__python} -c 'import compileall; compileall.compile_dir("%{buildroot}%{python_sitearch}", 10, "%{python_sitearch}", 1)' > /dev/null
%{__python} -O -c 'import compileall; compileall.compile_dir("%{buildroot}%{python_sitearch}", 10, "%{python_sitearch}", 1)' > /dev/null
%{__python26} -c 'import compileall; compileall.compile_dir("%{buildroot}%{python26_sitearch}", 10, "%{python26_sitearch}", 1)' > /dev/null
%{__python26} -O -c 'import compileall; compileall.compile_dir("%{buildroot}%{python26_sitearch}", 10, "%{python26_sitearch}", 1)' > /dev/null
%endif

%clean
rm -rf %{buildroot}

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

%post rootd
/sbin/chkconfig --add rootd

%preun rootd
if [ $1 = 0 ] ; then
    /sbin/service rootd stop >/dev/null 2>&1
    /sbin/chkconfig --del rootd
fi

%postun rootd
if [ "$1" -ge "1" ] ; then
    /sbin/service rootd condrestart >/dev/null 2>&1 || :
fi

%post proofd
/sbin/chkconfig --add proofd

%preun proofd
if [ $1 = 0 ] ; then
    /sbin/service proofd stop >/dev/null 2>&1
    /sbin/chkconfig --del proofd
fi

%postun proofd
if [ "$1" -ge "1" ] ; then
    /sbin/service proofd condrestart >/dev/null 2>&1 || :
fi

%if "%{?rhel}" == "5"
%post python
[ -h %{_libdir}/%{name}/libPyROOT.so.%{libversion} ] && \
    readlink %{_libdir}/%{name}/libPyROOT.so.%{libversion} | \
    grep -q site-packages && rm %{_libdir}/%{name}/libPyROOT.so.%{libversion}
%{_sbindir}/update-alternatives --install \
    %{_libdir}/%{name}/libPyROOT.so.%{libversion} \
    libPyROOT.so %{python_sitearch}/libPyROOT.so 20
/sbin/ldconfig

%postun python -p /sbin/ldconfig

%preun python
if [ $1 = 0 ]; then
    %{_sbindir}/update-alternatives --remove \
	libPyROOT.so %{python_sitearch}/libPyROOT.so
fi

%post python26
[ -h %{_libdir}/%{name}/libPyROOT.so.%{libversion} ] && \
    readlink %{_libdir}/%{name}/libPyROOT.so.%{libversion} | \
    grep -q site-packages && rm %{_libdir}/%{name}/libPyROOT.so.%{libversion}
%{_sbindir}/update-alternatives --install \
    %{_libdir}/%{name}/libPyROOT.so.%{libversion} \
    libPyROOT.so %{python26_sitearch}/libPyROOT.so 10
/sbin/ldconfig

%preun python26
if [ $1 = 0 ]; then
    %{_sbindir}/update-alternatives --remove \
	libPyROOT.so %{python26_sitearch}/libPyROOT.so
fi

%postun python26 -p /sbin/ldconfig
%else
%post python -p /sbin/ldconfig
%postun python -p /sbin/ldconfig
%endif

%post core -p /sbin/ldconfig
%postun core -p /sbin/ldconfig
%post cint -p /sbin/ldconfig
%postun cint -p /sbin/ldconfig
%post reflex -p /sbin/ldconfig
%postun reflex -p /sbin/ldconfig
%ifarch %{ix86} x86_64
%post cintex -p /sbin/ldconfig
%postun cintex -p /sbin/ldconfig
%endif
%post ruby -p /sbin/ldconfig
%postun ruby -p /sbin/ldconfig
%post genetic -p /sbin/ldconfig
%postun genetic -p /sbin/ldconfig
%post geom -p /sbin/ldconfig
%postun geom -p /sbin/ldconfig
%post gdml -p /sbin/ldconfig
%postun gdml -p /sbin/ldconfig
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
%if %{?fedora}%{!?fedora:0} >= 9 || %{?rhel}%{!?rhel:0} >= 6
%post graf-qt -p /sbin/ldconfig
%postun graf-qt -p /sbin/ldconfig
%endif
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
%if %{?fedora}%{!?fedora:0} >= 9 || %{?rhel}%{!?rhel:0} >= 6
%post gui-qt -p /sbin/ldconfig
%postun gui-qt -p /sbin/ldconfig
%endif
%post gui-recorder -p /sbin/ldconfig
%postun gui-recorder -p /sbin/ldconfig
%post hbook -p /sbin/ldconfig
%postun hbook -p /sbin/ldconfig
%post hist -p /sbin/ldconfig
%postun hist -p /sbin/ldconfig
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
%if %{?fedora}%{!?fedora:0} >= 20
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
%if %{?fedora}%{!?fedora:0} >= 18 || %{?rhel}%{!?rhel:0} >= 5
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
%post tree -p /sbin/ldconfig
%postun tree -p /sbin/ldconfig
%post tree-player -p /sbin/ldconfig
%postun tree-player -p /sbin/ldconfig
%post tree-viewer -p /sbin/ldconfig
%postun tree-viewer -p /sbin/ldconfig

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

%files icons
%{_datadir}/%{name}/icons

%files core -f includelist-core
%{_bindir}/memprobe
%{_bindir}/rlibmap
%{_bindir}/rmkdepend
%{_bindir}/root-config
%{_mandir}/man1/memprobe.1*
%{_mandir}/man1/rmkdepend.1*
%{_mandir}/man1/rlibmap.1*
%{_mandir}/man1/root-config.1*
%{_libdir}/%{name}/libCore.*
%{_libdir}/%{name}/libNew.*
%{_libdir}/%{name}/libRint.*
%{_libdir}/%{name}/libThread.*
%{_libdir}/%{name}/lib[^R]*Dict.*
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/class.rules
%{_datadir}/%{name}/gdb-backtrace.sh
%{_datadir}/%{name}/helgrind-root.supp
%{_datadir}/%{name}/Makefile.arch
%{_datadir}/%{name}/root.mimes
%{_datadir}/%{name}/system.rootauthrc
%{_datadir}/%{name}/system.rootdaemonrc
%{_datadir}/%{name}/system.rootrc
%{_mandir}/man1/system.rootdaemonrc.1*
%dir %{_datadir}/%{name}/cmake
%{_datadir}/%{name}/cmake/FindROOT.cmake
%dir %{_datadir}/%{name}/macros
%{_datadir}/%{name}/macros/Dialogs.C
%dir %{_datadir}/%{name}/plugins
%dir %{_datadir}/%{name}/plugins/*
%{_includedir}/%{name}/RConfigOptions.h
%{_includedir}/%{name}/RConfigure.h
%{_includedir}/%{name}/compiledata.h
%{_includedir}/%{name}/rmain.cxx
%dir %{_includedir}/%{name}/Math
%{_datadir}/aclocal/root.m4
%doc %{_pkgdocdir}/CREDITS
%doc %{_pkgdocdir}/LICENSE
%doc %{_pkgdocdir}/README

%files cint -f includelist-cint-cint
%{_bindir}/rootcint
%{_mandir}/man1/rootcint.1*
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/libCint.*
%{_libdir}/%{name}/cint
%dir %{_includedir}/%{name}
%config(noreplace) %{_sysconfdir}/ld.so.conf.d/%{name}-%{_arch}.conf
%doc %dir %{_pkgdocdir}
%doc %{_pkgdocdir}/COPYING.CINT

%ifarch %{ix86} x86_64
%files cintex -f includelist-cint-cintex
%{_libdir}/%{name}/libCintex.*
%{python_sitearch}/PyCintex.py*
%dir %{_includedir}/%{name}/Cintex
%endif

%files reflex -f includelist-cint-reflex
%{_bindir}/genmap
%{_bindir}/genreflex
%{_bindir}/genreflex-rootcint
%{_mandir}/man1/genmap.1*
%{_mandir}/man1/genreflex.1*
%{_mandir}/man1/genreflex-rootcint.1*
%{_libdir}/%{name}/libReflex.*
%{_libdir}/%{name}/libReflexDict.*
%{_libdir}/%{name}/python
%dir %{_includedir}/%{name}/Reflex
%dir %{_includedir}/%{name}/Reflex/Builder
%dir %{_includedir}/%{name}/Reflex/internal

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
%if %{xrootd}
%{_bindir}/proofexecv
%{_bindir}/xproofd
%endif
%{_mandir}/man1/proofd.1*
%{_mandir}/man1/proofserv.1*
%{_mandir}/man1/xpdtest.1*
%if %{xrootd}
%{_mandir}/man1/xproofd.1*
%endif
%{_initrddir}/proofd

%files rootd
%{_bindir}/rootd
%{_mandir}/man1/rootd.1*
%{_initrddir}/rootd

%files python -f includelist-bindings-pyroot
%if "%{?rhel}" == "5"
%{_libdir}/%{name}/libPyROOT.rootmap
%{_libdir}/%{name}/libPyROOT.so
%{_libdir}/%{name}/libPyROOT.so.5
%ghost %{_libdir}/%{name}/libPyROOT.so.%{libversion}
%else
%{_libdir}/%{name}/libPyROOT.*
%endif
%{python_sitearch}/libPyROOT.*
%{python_sitearch}/ROOT.py*
%{python_sitearch}/cppyy.py*

%if "%{?rhel}" == "5"
%files python26 -f includelist-bindings-pyroot
%{_libdir}/%{name}/libPyROOT.rootmap
%{_libdir}/%{name}/libPyROOT.so
%{_libdir}/%{name}/libPyROOT.so.5
%ghost %{_libdir}/%{name}/libPyROOT.so.%{libversion}
%{python26_sitearch}/libPyROOT.*
%{python26_sitearch}/ROOT.py*
%{python26_sitearch}/cppyy.py*
%endif

%files ruby -f includelist-bindings-ruby
%{_libdir}/%{name}/libRuby.*
%{ruby_installdir}/libRuby.*

%files genetic -f includelist-math-genetic
%{_libdir}/%{name}/libGenetic.*
%{_datadir}/%{name}/plugins/ROOT@@Math@@Minimizer/P080_GeneticMinimizer.C

%files geom -f includelist-geom
%{_libdir}/%{name}/libGeom.*
%{_libdir}/%{name}/libGeomBuilder.*
%{_libdir}/%{name}/libGeomPainter.*
%{_datadir}/%{name}/plugins/TGeoManagerEditor/P010_TGeoManagerEditor.C
%{_datadir}/%{name}/plugins/TVirtualGeoPainter/P010_TGeoPainter.C
%{_datadir}/%{name}/RadioNuclides.txt

%files gdml -f includelist-geom-gdml
%{_libdir}/%{name}/libGdml.*
%{python_sitearch}/ROOTwriter.py*
%{python_sitearch}/writer.py*

%files graf -f includelist-graf2d-graf
%{_libdir}/%{name}/libGraf.*
%{_datadir}/%{name}/plugins/TMinuitGraph/P010_TGraph.C

%files graf-asimage -f includelist-graf2d-asimage
%{_libdir}/%{name}/libASImage.*
%{_libdir}/%{name}/libASImageGui.*
%{_datadir}/%{name}/plugins/TImage/P010_TASImage.C
%{_datadir}/%{name}/plugins/TPaletteEditor/P010_TASPaletteEditor.C

%files graf-fitsio -f includelist-graf2d-fitsio
%{_libdir}/%{name}/libFITSIO.*

%files graf-gpad -f includelist-graf2d-gpad
%{_libdir}/%{name}/libGpad.*
%{_datadir}/%{name}/plugins/TVirtualPad/P010_TPad.C

%files graf-gviz -f includelist-graf2d-gviz
%{_libdir}/%{name}/libGviz.*

%files graf-postscript -f includelist-graf2d-postscript
%{_libdir}/%{name}/libPostscript.*
%{_datadir}/%{name}/plugins/TVirtualPS/P010_TPostScript.C
%{_datadir}/%{name}/plugins/TVirtualPS/P020_TSVG.C
%{_datadir}/%{name}/plugins/TVirtualPS/P030_TPDF.C
%{_datadir}/%{name}/plugins/TVirtualPS/P040_TImageDump.C
%{_datadir}/%{name}/plugins/TVirtualPS/P050_TTeXDump.C

%if %{?fedora}%{!?fedora:0} >= 9 || %{?rhel}%{!?rhel:0} >= 6
%files graf-qt -f includelist-graf2d-qt
%{_libdir}/%{name}/libGQt.*
%{_datadir}/%{name}/plugins/TVirtualX/P040_TGQt.C
%endif

%files graf-x11 -f includelist-graf2d-x11
%{_libdir}/%{name}/libGX11.*
%{_libdir}/%{name}/libGX11TTF.*
%{_datadir}/%{name}/plugins/TVirtualX/P010_TGX11.C
%{_datadir}/%{name}/plugins/TVirtualX/P020_TGX11TTF.C

%files graf3d -f includelist-graf3d-g3d
%{_libdir}/%{name}/libGraf3d.*
%{_datadir}/%{name}/plugins/TView/P010_TView3D.C

%files graf3d-eve -f includelist-graf3d-eve
%{_libdir}/%{name}/libEve.*

%files graf3d-gl -f includelist-graf3d-gl
%{_libdir}/%{name}/libRGL.*
%{_datadir}/%{name}/plugins/TGLHistPainter/P010_TGLHistPainter.C
%{_datadir}/%{name}/plugins/TGLManager/P010_TX11GLManager.C
%{_datadir}/%{name}/plugins/TVirtualGLImp/P010_TX11GL.C
%{_datadir}/%{name}/plugins/TVirtualPadPainter/P010_TGLPadPainter.C
%{_datadir}/%{name}/plugins/TVirtualViewer3D/P020_TGLSAViewer.C
%{_datadir}/%{name}/plugins/TVirtualViewer3D/P030_TGLViewer.C

%files graf3d-gviz3d -f includelist-graf3d-gviz3d
%{_libdir}/%{name}/libGviz3d.*

%files graf3d-x3d -f includelist-graf3d-x3d
%{_libdir}/%{name}/libX3d.*
%{_datadir}/%{name}/plugins/TViewerX3D/P010_TViewerX3D.C
%{_datadir}/%{name}/plugins/TVirtualViewer3D/P010_TViewerX3D.C

%files gui -f includelist-gui-gui
%{_libdir}/%{name}/libGui.*
%{_libdir}/%{name}/libGuiHtml.*
%{_datadir}/%{name}/plugins/TBrowserImp/P010_TRootBrowser.C
%{_datadir}/%{name}/plugins/TBrowserImp/P020_TRootBrowserLite.C
%{_datadir}/%{name}/plugins/TGPasswdDialog/P010_TGPasswdDialog.C
%{_datadir}/%{name}/plugins/TGuiFactory/P010_TRootGuiFactory.C

%files gui-fitpanel -f includelist-gui-fitpanel
%{_libdir}/%{name}/libFitPanel.*
%{_datadir}/%{name}/plugins/TFitEditor/P010_TFitEditor.C

%files gui-ged -f includelist-gui-ged
%{_libdir}/%{name}/libGed.*
%{_datadir}/%{name}/plugins/TVirtualPadEditor/P010_TGedEditor.C

%files guibuilder -f includelist-gui-guibuilder
%{_libdir}/%{name}/libGuiBld.*
%{_datadir}/%{name}/plugins/TGuiBuilder/P010_TRootGuiBuilder.C
%{_datadir}/%{name}/plugins/TVirtualDragManager/P010_TGuiBldDragManager.C

%if %{?fedora}%{!?fedora:0} >= 9 || %{?rhel}%{!?rhel:0} >= 6
%files gui-qt -f includelist-gui-qt
%{_libdir}/%{name}/libQtRoot.*
%{_libdir}/%{name}/libQtGSI.*
%{_datadir}/%{name}/plugins/TGuiFactory/P020_TQtRootGuiFactory.C
%endif

%files gui-recorder -f includelist-gui-recorder
%{_libdir}/%{name}/libRecorder.*

%files hbook -f includelist-hist-hbook
%{_bindir}/g2root
%{_bindir}/h2root
%{_mandir}/man1/g2root.1*
%{_mandir}/man1/h2root.1*
%{_libdir}/%{name}/libminicern.*
%{_libdir}/%{name}/libHbook.*

%files hist -f includelist-hist-hist
%{_libdir}/%{name}/libHist.*

%files hist-painter -f includelist-hist-histpainter
%{_libdir}/%{name}/libHistPainter.*
%{_datadir}/%{name}/plugins/TVirtualHistPainter/P010_THistPainter.C
%{_datadir}/%{name}/plugins/TVirtualGraphPainter/P010_TGraphPainter.C

%files spectrum -f includelist-hist-spectrum
%{_libdir}/%{name}/libSpectrum.*

%files spectrum-painter -f includelist-hist-spectrumpainter
%{_libdir}/%{name}/libSpectrumPainter.*

%files hist-factory -f includelist-roofit-histfactory
%{_bindir}/hist2workspace
%{_bindir}/prepareHistFactory
%{_mandir}/man1/hist2workspace.1*
%{_mandir}/man1/prepareHistFactory.1*
%{_libdir}/%{name}/libHistFactory.*
%{_datadir}/%{name}/HistFactorySchema.dtd
%dir %{_includedir}/%{name}/RooStats/HistFactory
%doc roofit/histfactory/doc/README

%files html -f includelist-html
%{_libdir}/%{name}/libHtml.*
%{_datadir}/%{name}/html
%{_datadir}/%{name}/macros/html.C

%files io -f includelist-io-io
%{_libdir}/%{name}/libRIO.*
%{_datadir}/%{name}/plugins/TArchiveFile/P010_TZIPFile.C
%{_datadir}/%{name}/plugins/TVirtualStreamerInfo/P010_TStreamerInfo.C

%files io-dcache -f includelist-io-dcache
%{_libdir}/%{name}/libDCache.*
%{_datadir}/%{name}/plugins/TFile/P040_TDCacheFile.C
%{_datadir}/%{name}/plugins/TSystem/P020_TDCacheSystem.C

%files io-gfal -f includelist-io-gfal
%{_libdir}/%{name}/libGFAL.*
%{_datadir}/%{name}/plugins/TFile/P050_TGFALFile.C

%if %{?fedora}%{!?fedora:0} >= 20
%files io-hdfs -f includelist-io-hdfs
%{_libdir}/%{name}/libHDFS.*
%{_datadir}/%{name}/plugins/TFile/P110_THDFSFile.C
%{_datadir}/%{name}/plugins/TSystem/P060_THDFSSystem.C
%endif

%files io-rfio -f includelist-io-rfio
%{_libdir}/%{name}/libRFIO.*
%{_datadir}/%{name}/plugins/TFile/P020_TRFIOFile.C
%{_datadir}/%{name}/plugins/TSystem/P010_TRFIOSystem.C

%files io-sql -f includelist-io-sql
%{_libdir}/%{name}/libSQLIO.*
%{_datadir}/%{name}/plugins/TFile/P090_TSQLFile.C

%files io-xml -f includelist-io-xml
%{_libdir}/%{name}/libXMLIO.*
%{_libdir}/%{name}/libXMLParser.*
%{_datadir}/%{name}/plugins/TFile/P080_TXMLFile.C

%files foam -f includelist-math-foam
%{_libdir}/%{name}/libFoam.*
%{_datadir}/%{name}/plugins/ROOT@@Math@@DistSampler/P020_TFoamSampler.C

%files fftw -f includelist-math-fftw
%{_libdir}/%{name}/libFFTW.*
%{_datadir}/%{name}/plugins/TVirtualFFT/P010_TFFTComplex.C
%{_datadir}/%{name}/plugins/TVirtualFFT/P020_TFFTComplexReal.C
%{_datadir}/%{name}/plugins/TVirtualFFT/P030_TFFTRealComplex.C
%{_datadir}/%{name}/plugins/TVirtualFFT/P040_TFFTReal.C

%files fumili -f includelist-math-fumili
%{_libdir}/%{name}/libFumili.*
%{_datadir}/%{name}/plugins/ROOT@@Math@@Minimizer/P070_TFumiliMinimizer.C
%{_datadir}/%{name}/plugins/TVirtualFitter/P020_TFumili.C

%files genvector -f includelist-math-genvector
%{_libdir}/%{name}/libGenVector.*
%dir %{_includedir}/%{name}/Math/GenVector

%files mathcore -f includelist-math-mathcore
%{_libdir}/%{name}/libMathCore.*
%dir %{_includedir}/%{name}/Fit

%files mathmore -f includelist-math-mathmore
%{_libdir}/%{name}/libMathMore.*
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

%files minuit -f includelist-math-minuit
%{_libdir}/%{name}/libMinuit.*
%{_datadir}/%{name}/plugins/ROOT@@Math@@Minimizer/P020_TMinuitMinimizer.C
%{_datadir}/%{name}/plugins/ROOT@@Math@@Minimizer/P060_TLinearMinimizer.C
%{_datadir}/%{name}/plugins/TVirtualFitter/P010_TFitter.C

%files minuit2 -f includelist-math-minuit2
%{_libdir}/%{name}/libMinuit2.*
%dir %{_includedir}/%{name}/Minuit2
%{_datadir}/%{name}/plugins/ROOT@@Math@@Minimizer/P010_Minuit2Minimizer.C
%{_datadir}/%{name}/plugins/TVirtualFitter/P030_TFitterMinuit.C
%{_datadir}/%{name}/plugins/TVirtualFitter/P040_TFitterFumili.C

%files mlp -f includelist-math-mlp
%{_libdir}/%{name}/libMLP.*

%files physics -f includelist-math-physics
%{_libdir}/%{name}/libPhysics.*

%files quadp -f includelist-math-quadp
%{_libdir}/%{name}/libQuadp.*

%files smatrix -f includelist-math-smatrix
%{_libdir}/%{name}/libSmatrix.*

%files splot -f includelist-math-splot
%{_libdir}/%{name}/libSPlot.*

%files unuran -f includelist-math-unuran
%{_libdir}/%{name}/libUnuran.*
%{_datadir}/%{name}/plugins/ROOT@@Math@@DistSampler/P010_TUnuranSampler.C

%files vdt -f includelist-math-vdt
%dir %{_includedir}/%{name}/vdt
%doc math/vdt/Licence.md math/vdt/ReadMe.md math/vdt/ReleaseNotes.txt

%files memstat -f includelist-misc-memstat
%{_libdir}/%{name}/libMemStat.*

%files table -f includelist-misc-table
%{_libdir}/%{name}/libTable.*

%files montecarlo-eg -f includelist-montecarlo-eg
%{_libdir}/%{name}/libEG.*
%{_datadir}/%{name}/pdg_table.txt
%doc %{_pkgdocdir}/cfortran.doc

%if %{?fedora}%{!?fedora:0} >= 18 || %{?rhel}%{!?rhel:0} >= 5
%files montecarlo-pythia8 -f includelist-montecarlo-pythia8
%{_libdir}/%{name}/libEGPythia8.*
%endif

%files montecarlo-vmc -f includelist-montecarlo-vmc
%{_libdir}/%{name}/libVMC.*
%{_datadir}/%{name}/vmc

%files net -f includelist-net-net
%{_libdir}/%{name}/libNet.*
%{_datadir}/%{name}/plugins/TApplication/P010_TApplicationRemote.C
%{_datadir}/%{name}/plugins/TApplication/P020_TApplicationServer.C
%{_datadir}/%{name}/plugins/TFile/P010_TWebFile.C
%{_datadir}/%{name}/plugins/TFile/P120_TNetFile.C
%{_datadir}/%{name}/plugins/TFile/P150_TS3WebFile.C
%{_datadir}/%{name}/plugins/TFileStager/P020_TNetFileStager.C
%{_datadir}/%{name}/plugins/TSystem/P050_TWebSystem.C
%{_datadir}/%{name}/plugins/TSystem/P070_TNetSystem.C
%{_datadir}/%{name}/plugins/TVirtualMonitoringWriter/P020_TSQLMonitoringWriter.C

%files net-rpdutils -f includelist-net-rpdutils
%{_libdir}/%{name}/libSrvAuth.*

%files net-bonjour -f includelist-net-bonjour
%{_libdir}/%{name}/libBonjour.*

%files net-auth -f includelist-net-auth
%{_libdir}/%{name}/libRootAuth.*
%{_datadir}/%{name}/plugins/TVirtualAuth/P010_TRootAuth.C
%doc %{_pkgdocdir}/README.AUTH

%files net-davix -f includelist-net-davix
%{_libdir}/%{name}/libRDAVIX.*
%{_datadir}/%{name}/plugins/TFile/P130_TDavixFile.C
%{_datadir}/%{name}/plugins/TSystem/P045_TDavixSystem.C

%files net-globus
%{_libdir}/%{name}/libGlobusAuth.*
%doc %{_pkgdocdir}/README.GLOBUS

%files net-krb5 -f includelist-net-krb5auth
%{_libdir}/%{name}/libKrb5Auth.*

%files net-ldap -f includelist-net-ldap
%{_libdir}/%{name}/libRLDAP.*

%files net-http -f includelist-net-http
%{_libdir}/%{name}/libRHTTP.*
%{_datadir}/%{name}/http
%doc net/http/README.txt net/http/civetweb/*.md

%if %{xrootd}
%files netx -f includelist-netx
%{_libdir}/%{name}/libNetx.*
%{_libdir}/%{name}/libNetxNG.*
%{_datadir}/%{name}/plugins/TFile/P100_TXNetFile.C
%{_datadir}/%{name}/plugins/TFileStager/P010_TXNetFileStager.C
%{_datadir}/%{name}/plugins/TSystem/P040_TXNetSystem.C
%endif

%files proof -f includelist-proof-proof
%{_libdir}/%{name}/libProof.*
%{_libdir}/%{name}/libProofDraw.*
%{_libdir}/%{name}/libProofPlayer.*
%{_datadir}/%{name}/plugins/TChain/P010_TProofChain.C
%{_datadir}/%{name}/plugins/TDataSetManager/P010_TDataSetManagerFile.C
%{_datadir}/%{name}/plugins/TProof/P010_TProofCondor.C
%{_datadir}/%{name}/plugins/TProof/P020_TProofSuperMaster.C
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
%{_datadir}/%{name}/proof

%files proof-pq2 -f includelist-proof-pq2
%{_bindir}/pq2*
%{_mandir}/man1/pq2*.1*

%files proof-sessionviewer -f includelist-gui-sessionviewer
%{_libdir}/%{name}/libSessionViewer.*
%{_datadir}/%{name}/plugins/TProofProgressDialog/P010_TProofProgressDialog.C
%{_datadir}/%{name}/plugins/TProofProgressLog/P010_TProofProgressLog.C
%{_datadir}/%{name}/plugins/TSessionViewer/P010_TSessionViewer.C

%if %{xrootd}
%files xproof -f includelist-proof-proofx
%{_libdir}/%{name}/libProofx.*
%{_libdir}/%{name}/libXrdProofd.*
%{_datadir}/%{name}/plugins/TProofMgr/P010_TXProofMgr.C
%{_datadir}/%{name}/plugins/TProofServ/P010_TXProofServ.C
%{_datadir}/%{name}/plugins/TSlave/P010_TXSlave.C
%endif

%files roofit -f includelist-roofit
%{_libdir}/%{name}/libRooFit.*
%{_libdir}/%{name}/libRooFitCore.*
%{_libdir}/%{name}/libRooStats.*
%dir %{_includedir}/%{name}/RooStats

%files sql-mysql -f includelist-sql-mysql
%{_libdir}/%{name}/libRMySQL.*
%{_datadir}/%{name}/plugins/TSQLServer/P010_TMySQLServer.C

%files sql-odbc -f includelist-sql-odbc
%{_libdir}/%{name}/libRODBC.*
%{_datadir}/%{name}/plugins/TSQLServer/P050_TODBCServer.C

%files sql-sqlite -f includelist-sql-sqlite
%{_libdir}/%{name}/libSQLite.*
%{_datadir}/%{name}/plugins/TSQLServer/P060_TSQLiteServer.C

%files sql-pgsql -f includelist-sql-pgsql
%{_libdir}/%{name}/libPgSQL.*
%{_datadir}/%{name}/plugins/TSQLServer/P020_TPgSQLServer.C

%files tmva -f includelist-tmva
%{_libdir}/%{name}/libTMVA.*
%dir %{_includedir}/%{name}/TMVA
%doc tmva/doc/LICENSE

%files tree -f includelist-tree-tree
%{_libdir}/%{name}/libTree.*
%doc %{_pkgdocdir}/README.SELECTOR

%files tree-player -f includelist-tree-treeplayer
%{_libdir}/%{name}/libTreePlayer.*
%{_datadir}/%{name}/plugins/TFileDrawMap/P010_TFileDrawMap.C
%{_datadir}/%{name}/plugins/TVirtualTreePlayer/P010_TTreePlayer.C

%files tree-viewer -f includelist-tree-treeviewer
%{_libdir}/%{name}/libTreeViewer.*
%{_datadir}/%{name}/plugins/TVirtualTreeViewer/P010_TTreeViewer.C

%files -n emacs-%{name}
%dir %{emacs_lispdir}/root
%{emacs_lispdir}/root/*.elc

%files -n emacs-%{name}-el
%{emacs_lispdir}/root/*.el

%changelog
* Sat Aug 16 2014 Mattias Ellert <mattias.ellert@fysast.uu.se> - 5.34.20-1
- Update to 5.34.20
- Re-enable xrootd support for F21+ and EPEL7 (now ported to xrootd 4)
- Do not depend on wine's fonts
- Drop patch root-gccopt.patch

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
