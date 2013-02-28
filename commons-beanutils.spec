Name:		commons-beanutils
Version:	1.8.3
Release:	1
Summary:	Commons BeanUtils Package
License:	Apache License
Group:		Development/Java
Source0:	http://apache.mirror.clusters.cc/commons/beanutils/source/%name-%version-src.tar.gz
Source1:        pom-maven2jpp-depcat.xsl
Source2:        pom-maven2jpp-newdepmap.xsl
Source3:        pom-maven2jpp-mapdeps.xsl
Source4:        commons-beanutils-1.7.0-jpp-depmap.xml
Source5:        commons-beanutils-1.7.0.pom
Source6:        commons-beanutils-bean-collections-1.7.0.pom
Source7:        commons-beanutils-core-1.7.0.pom
Source8:        commons-build.tar.gz
Source9:        commons-beanutils-maven.xml
Source10:       commons-beanutils-build-other-jars.xml

Url:		http://commons.apache.org/beanutils/
BuildRequires:	ant
BuildRequires:	locales-en
BuildRequires:	commons-collections >= 0:2.0
BuildRequires:	jakarta-commons-logging >= 0:1.0
BuildRequires:	java-rpmbuild > 0:1.5
BuildRequires:	java-1.6.0-openjdk-devel
Requires:	commons-collections >= 0:2.0
Requires:	jakarta-commons-logging >= 0:1.0
BuildArch:	noarch
%rename jakarta-commons-beanutils

%description
The scope of this package is to create a package of Java utility methods
for accessing and modifying the properties of arbitrary JavaBeans.  No
dependencies outside of the JDK are required, so the use of this package
is very lightweight.

%package javadoc
Summary:	Javadoc for %{name}
Group:		Development/Java

%description javadoc
Javadoc for %{name}.

%prep
%setup -q -n %name-%{version}-src
gzip -dc %{SOURCE8} | tar xf -
cp %{SOURCE9} maven.xml
cp %{SOURCE10} build-other-jars.xml
%remove_java_binaries

%build
#export LC_ALL=ISO-8859-1
export CLASSPATH=$(build-classpath commons-collections commons-logging)
export JAVA_HOME=%_prefix/lib/jvm/java-1.6.0
ant -Dbuild.sysclasspath=first dist

%install
# jars
install -d -m 755 $RPM_BUILD_ROOT%{_javadir}
install -m 644 dist/%name-%version.jar $RPM_BUILD_ROOT%{_javadir}/
install -m 644 dist/%name-core-%version.jar $RPM_BUILD_ROOT%{_javadir}/
install -m 644 dist/%name-bean-collections-%version.jar $RPM_BUILD_ROOT%{_javadir}/
(cd $RPM_BUILD_ROOT%{_javadir} && for jar in *-%{version}*; do ln -sf ${jar} jakarta-${jar}; done)
(cd $RPM_BUILD_ROOT%{_javadir} && for jar in *-%{version}*; do ln -sf ${jar} `echo $jar| sed  "s|-%{version}||g"`; done)

%add_to_maven_depmap %{name} %{name} %{version} JPP %{name}
%add_to_maven_depmap %{name} %{name}-core %{version} JPP %{name}-core
%add_to_maven_depmap %{name} %{name}-bean-collections %{version} JPP %{name}-bean-collections

install -d -m 755 $RPM_BUILD_ROOT%{_datadir}/maven2/poms
install -pm 644 %{SOURCE5} \
    $RPM_BUILD_ROOT%{_datadir}/maven2/poms/JPP-%{name}.pom
install -pm 644 %{SOURCE6} \
    $RPM_BUILD_ROOT%{_datadir}/maven2/poms/JPP-%{name}-bean-collections.pom
install -pm 644 %{SOURCE7} \
    $RPM_BUILD_ROOT%{_datadir}/maven2/poms/JPP-%{name}-core.pom


# javadoc
install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -pr dist/docs/api/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}

%post
%update_maven_depmap

%postun
%update_maven_depmap

%files
%defattr(0644,root,root,0755)
%doc RELEASE-NOTES.txt LICENSE.txt
%{_javadir}/*
%{_datadir}/maven2/poms/*
%{_mavendepmapfragdir}

%files javadoc
%defattr(0644,root,root,0755)
%{_javadocdir}/%{name}-%{version}




%changelog
* Fri Dec 03 2010 Oden Eriksson <oeriksson@mandriva.com> 0:1.7.0-6.0.6mdv2011.0
+ Revision: 606046
- rebuild

* Wed Mar 17 2010 Oden Eriksson <oeriksson@mandriva.com> 0:1.7.0-6.0.5mdv2010.1
+ Revision: 522926
- rebuilt for 2010.1

* Wed Sep 02 2009 Christophe Fergeau <cfergeau@mandriva.com> 0:1.7.0-6.0.4mdv2010.0
+ Revision: 425394
- rebuild

* Sat Mar 07 2009 Antoine Ginies <aginies@mandriva.com> 0:1.7.0-6.0.3mdv2009.1
+ Revision: 351266
- rebuild

* Thu Feb 14 2008 Thierry Vignaud <tv@mandriva.org> 0:1.7.0-6.0.2mdv2009.0
+ Revision: 167932
- fix no-buildroot-tag
- kill re-definition of %%buildroot on Pixel's request

* Sun Dec 16 2007 Anssi Hannula <anssi@mandriva.org> 0:1.7.0-6.0.2mdv2008.1
+ Revision: 120900
- buildrequire java-rpmbuild, i.e. build with icedtea on x86(_64)

* Mon Dec 10 2007 Alexander Kurtakov <akurtakov@mandriva.org> 0:1.7.0-6.0.1mdv2008.1
+ Revision: 116860
- add maven poms (jpp sync)

* Sat Sep 15 2007 Anssi Hannula <anssi@mandriva.org> 0:1.7.0-4.5mdv2008.0
+ Revision: 87398
- rebuild to filter out autorequires of GCJ AOT objects
- remove unnecessary Requires(post) on java-gcj-compat

* Sun Sep 09 2007 Pascal Terjan <pterjan@mandriva.org> 0:1.7.0-4.4mdv2008.0
+ Revision: 82887
- rebuild


* Wed Mar 14 2007 Christiaan Welvaart <spturtle@mandriva.org> 1.7.0-4.3mdv2007.1
+ Revision: 143901
- rebuild for 2007.1
- Import jakarta-commons-beanutils

* Fri Aug 04 2006 David Walluck <walluck@mandriva.org> 0:1.7.0-4.2mdv2007.0
- bump release to allow upload

* Sun Jul 23 2006 David Walluck <walluck@mandriva.org> 0:1.7.0-4.1mdv2007.0
- bump release

* Sun Jun 11 2006 David Walluck <walluck@mandriva.org> 0:1.7.0-3.0.1mdv2007.0
- bump release to supercede jpp, even though we don't use maven
- don't always build as noarch

* Fri Jun 02 2006 David Walluck <walluck@mandriva.org> 0:1.7.0-2.2.3mdv2006.0
- rebuild for libgcj.so.7

* Fri Jan 13 2006 David Walluck <walluck@mandriva.org> 0:1.7.0-2.2.2mdk
- quiet %%setup

* Wed Oct 26 2005 David Walluck <walluck@mandriva.org> 0:1.7.0-2.2.1mdk
- natify

* Fri May 20 2005 David Walluck <walluck@mandriva.org> 0:1.7.0-2.1mdk
- release

* Fri May 20 2005 David Walluck <walluck@mandriva.org> 0:1.7.0-2.1mdk
- release

* Sat Jan 29 2005 Ralph Apel <r.apel@r-apel.de> - 0:1.7.0-2jpp
- Use the "dist" target to get a full build, including bean-collections

* Fri Oct 22 2004 Fernando Nasser <fnasser@redhat.com> - 0:1.7.0-1jpp
- Upgrade to 1.7.0

* Tue Aug 24 2004 Randy Watler <rwatler at finali.com> - 0:1.6.1-5jpp
- Rebuild with ant-1.6.2

