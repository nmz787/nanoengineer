#!/bin/sh -x

# Usage: Run ./buildWin.sh from the Distribution directory.

# Set up path variables
cd ..
TOP_LEVEL=`pwd`
DIST_ROOT=$TOP_LEVEL/cad/src/dist
DIST_CONTENTS=$DIST_ROOT

# Build the base .exe and directory contents
if [ ! -e "$TOP_LEVEL/cad/src" ]; then exit; fi
cd $TOP_LEVEL/cad/src
rm -rf dist build
cp $TOP_LEVEL/Distribution/Win32/setup.py .
c:/python24/python setup.py py2exe --includes=sip,pkg_resources --packages=ctypes --excludes=OpenGL -d dist/program || exit 1
cp c:/python24/Lib/site-packages/PyOpenGL-3.0.0a6-py2.4.egg dist/program/
cd $TOP_LEVEL

mkdir $DIST_CONTENTS/bin

# Build and copy NanoDynamics-1
cd $TOP_LEVEL/sim/src
#cp $TOP_LEVEL/Distribution/Win32/ND1-Makefile ./Makefile
make clean || exit 1
make || exit 1
make pyx || exit 1
cp simulator.exe $DIST_CONTENTS/bin/
if [ ! -e "$DIST_CONTENTS/bin/simulator.exe" ]; then exit; fi
cp sim.dll $DIST_CONTENTS/bin/
if [ ! -e "$DIST_CONTENTS/bin/sim.dll" ]; then exit; fi
cd $TOP_LEVEL

# Copy the gnuplot binary
cp c:/bin/wgnuplot.exe $DIST_CONTENTS/bin/
if [ ! -e "$DIST_CONTENTS/bin/wgnuplot.exe" ]; then exit; fi

# Copy the OpenBabel binaries
unzip $TOP_LEVEL/Distribution/Win32/OpenBabel.MMP.win32.zip -d $DIST_CONTENTS/bin

# Copy the doc/ files
mkdir $DIST_CONTENTS/doc
cp cad/doc/keyboardshortcuts.htm $DIST_CONTENTS/doc/
cp cad/doc/mousecontrols.htm $DIST_CONTENTS/doc/

# Copy partlib tree to a user-visible location and make a symbolic link to it
# for NE1 to use.
cp -R $TOP_LEVEL/cad/partlib $DIST_ROOT/

# Copy images
DIST_IMAGES_DIR=$DIST_ROOT/src/ui/
mkdir -p $DIST_IMAGES_DIR/actions
cp -R cad/src/ui/actions/Edit $DIST_IMAGES_DIR/actions/ 
cp -R cad/src/ui/actions/File $DIST_IMAGES_DIR/actions/
cp -R cad/src/ui/actions/Help $DIST_IMAGES_DIR/actions/
cp -R cad/src/ui/actions/Insert $DIST_IMAGES_DIR/actions/
cp -R cad/src/ui/actions/Properties\ Manager $DIST_IMAGES_DIR/actions/
cp -R cad/src/ui/actions/Simulation $DIST_IMAGES_DIR/actions/
cp -R cad/src/ui/actions/Toolbars $DIST_IMAGES_DIR/actions/
cp -R cad/src/ui/actions/Tools $DIST_IMAGES_DIR/actions/
cp -R cad/src/ui/actions/View $DIST_IMAGES_DIR/actions/
cp -R cad/src/ui/border $DIST_IMAGES_DIR
cp -R cad/src/ui/confcorner $DIST_IMAGES_DIR
cp -R cad/src/ui/cursors $DIST_IMAGES_DIR
cp -R cad/src/ui/dialogs $DIST_IMAGES_DIR
cp -R cad/src/ui/exprs $DIST_IMAGES_DIR
cp -R cad/src/ui/images $DIST_IMAGES_DIR
cp -R cad/src/ui/modeltree $DIST_IMAGES_DIR
cd $TOP_LEVEL

# Copy the ReadeMe.html file and Licenses/ files
cp $TOP_LEVEL/cad/src/ReadMe.html $DIST_ROOT/
mkdir $DIST_ROOT/Licenses
cp $TOP_LEVEL/cad/src/LICENSE $DIST_ROOT/Licenses/NanoEngineer-1_License.txt
cp $TOP_LEVEL/cad/licenses-common/Gnuplot_License $DIST_ROOT/Licenses/Gnuplot_License.txt
cp $TOP_LEVEL/cad/licenses-common/NanoKids_Attribution $DIST_ROOT/Licenses/NanoKids_Attribution.txt
cp $TOP_LEVEL/cad/licenses-common/OpenGL_License.doc $DIST_ROOT/Licenses/
cp $TOP_LEVEL/cad/licenses-common/OpenGL_LicenseOverview $DIST_ROOT/Licenses/OpenGL_LicenseOverview.txt
cp $TOP_LEVEL/cad/licenses-common/PyOpenGL_License $DIST_ROOT/Licenses/PyOpenGL_License.txt
cp $TOP_LEVEL/cad/licenses-common/Python_License $DIST_ROOT/Licenses/Python_License.txt
cp $TOP_LEVEL/cad/licenses-Mac/PyQt_License $DIST_ROOT/Licenses/PyQt_License.txt
cp $TOP_LEVEL/cad/licenses-Mac/Qt_License $DIST_ROOT/Licenses/Qt_License.txt
cp $TOP_LEVEL/Distribution/MacOSX/ctypes_License.txt $DIST_ROOT/Licenses/
cp $TOP_LEVEL/Distribution/MacOSX/numarray_License.txt $DIST_ROOT/Licenses/
cp $TOP_LEVEL/Distribution/MacOSX/NumPy_License.txt $DIST_ROOT/Licenses/
cp $TOP_LEVEL/Distribution/MacOSX/PythonImagingLibrary_License.txt $DIST_ROOT/Licenses/
cp $TOP_LEVEL/Distribution/MacOSX/OracleBerkeleyDB_License.txt $DIST_ROOT/Licenses/
cp $TOP_LEVEL/Distribution/MacOSX/bsddb3_License.txt $DIST_ROOT/Licenses/
cp $TOP_LEVEL/Distribution/MacOSX/OpenBabel_License.txt $DIST_ROOT/Licenses/

# Plugins
#
mkdir $DIST_CONTENTS/plugins

# Build and copy the CoNTub plugin
#cd $TOP_LEVEL/cad/plugins/CoNTub
#make
#cp -R ../CoNTub $DIST_CONTENTS/plugins/
#if [ ! -e "$DIST_CONTENTS/plugins/CoNTub/bin/HJ" ]; then exit; fi
#cd $TOP_LEVEL

# Copy the DNA plugin files
cp -R $TOP_LEVEL/cad/plugins/DNA $DIST_CONTENTS/plugins/
cp -R $TOP_LEVEL/cad/plugins/NanoDynamics-1 $DIST_CONTENTS/plugins/
mkdir $DIST_CONTENTS/plugins/GROMACS
cp -R $TOP_LEVEL/cad/plugins/GROMACS/Pam5Potential.xvg $DIST_CONTENTS/plugins/GROMACS/
cd $TOP_LEVEL

#
# End Plugins

# Remove cruft
rm -rf `find $DIST_ROOT -name CVS`
rm -rf $DIST_ROOT/partlib/*/CVS
rm -rf $DIST_ROOT/partlib/*/*/CVS

# Create the installer
"c:/program files/nsis/makensis.exe" Distribution/Win32/installer.nsi

