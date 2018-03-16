Summary:    Reservoir sampling for the command line.
Name:       rsampling
Version:    0.1.0
Release:    0
License:    GPLv3
BuildArch:  x86_64
BuildRoot:  %{_tmppath}/%{name}-build
Group:      System/Base
Vendor:     Leipzig University Library <http://ub.uni-leipzig.de>
URL:        https://github.com/miku/rsampling

%description

Simple reservoir sampling.

%prep
# the set up macro unpacks the source bundle and changes in to the represented by
# %{name} which in this case would be my_maintenance_scripts. So your source bundle
# needs to have a top level directory inside called my_maintenance _scripts
# %setup -n %{name}

%build
# this section is empty for this example as we're not actually building anything

%install
# create directories where the files will be located
mkdir -p $RPM_BUILD_ROOT/usr/local/sbin

# put the files in to the relevant directories.
# the argument on -m is the permissions expressed as octal. (See chmod man page for details.)
install -m 755 rsampling $RPM_BUILD_ROOT/usr/local/sbin

# mkdir -p $RPM_BUILD_ROOT/usr/local/share/man/man1
# install -m 644 rsampling.1 $RPM_BUILD_ROOT/usr/local/share/man/man1/rsampling.1

%post
# the post section is where you can run commands after the rpm is installed.
# insserv /etc/init.d/my_maintenance

%clean
rm -rf $RPM_BUILD_ROOT
rm -rf %{_tmppath}/%{name}
rm -rf %{_topdir}/BUILD/%{name}

# list files owned by the package here
%files
%defattr(-,root,root)
/usr/local/sbin/rsampling
# /usr/local/share/man/man1/rsampling.1


%changelog
* Fri Mar 16 2018 Martin Czygan
- 0.1.0 initial release

