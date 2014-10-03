Summary:	Utility for converting text between multiple character sets
Name:		recode
Version:	3.7
Release:	2
License:	GPL v2/LGPL
Group:		Applications/Text
# git://github.com/pinard/Recode.git
# 2fd8385658e5a08700e3b916053f6680ff85fdbd
Source0:	%{name}-%{version}.tar.xz
# Source0-md5:	81131d487947e33bb6ad1a3fa71159d0
URL:		http://recode.progiciels-bpi.ca/index.html
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	flex
BuildRequires:	libtool
BuildRequires:	texinfo
Requires(post,postun):	/usr/sbin/ldconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Free `recode' converts files between various character sets and
surfaces. It supports more than 200 different character sets and
surfaces, including well known ISO-8859, CP-XXXX and Unicode.

%package devel
Summary:	Header files and documentations for librecode
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files and documentations for librecode.

%prep
%setup -q

# automake 1.12.x fixes
%{__sed} -i -e "/AM_C_PROTOTYPES/d" configure.ac
%{__sed} -i -e "s| ansi2knr||g" src/Makefile.am

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__automake}
%configure \
	--disable-static
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/*.la

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
/usr/sbin/ldconfig
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1

%postun
/usr/sbin/ldconfig
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS NEWS README THANKS TODO
%attr(755,root,root) %{_bindir}/recode
%attr(755,root,root) %ghost %{_libdir}/lib*.so.?
%attr(755,root,root) %{_libdir}/lib*.so.*.*.*
%{_infodir}/*info*
%{_mandir}/man1/*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so
%{_includedir}/*.h

