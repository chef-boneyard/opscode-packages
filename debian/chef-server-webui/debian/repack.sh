#!/bin/sh
# Repackage upstream source to exclude non-distributable files
# should be called as "repack.sh --upstream-source <ver> <downloaded file>
# (for example, via uscan)

set -e
set -u

VER="$2+dfsg"
FILE="$3"
PKG=`dpkg-parsechangelog|grep ^Source:|sed 's/^Source: //'`

REPACK_DIR="$PKG-$VER.orig" # DevRef § 6.7.8.2

echo -e "\nRepackaging $FILE\n"

DIR=`mktemp -d ./tmpRepackXXXXXX`
trap "rm -rf \"$DIR\"" QUIT INT EXIT

# Create an extra directory to cope with rootless tarballs
UP_BASE="$DIR/unpack"
mkdir "$UP_BASE"
tar xzf "$FILE" -C "$UP_BASE"

if [ `ls -1 "$UP_BASE" | wc -l` -eq 1 ]; then
        # Tarball does contain a root directory
        UP_BASE="$UP_BASE/`ls -1 "$UP_BASE"`"
fi

## Remove undistributable files from source.
rm -vfr $UP_BASE/public/javascripts/yetii-min.js
rm -vfr $UP_BASE/public/javascripts/jquery.jeditable.mini.js
rm -vfr $UP_BASE/public/javascripts/jquery.tools.min.js
rm -vfr $UP_BASE/public/javascripts/jquery-ui-1.7.1.custom.min.js
## End

mv "$UP_BASE" "$DIR/$REPACK_DIR"

# Using a pipe hides tar errors!
tar cfC "$DIR/repacked.tar" "$DIR" "$REPACK_DIR"
gzip -9 < "$DIR/repacked.tar" > "$DIR/repacked.tar.gz"
FILE="../${PKG}_${VER}.orig.tar.gz"
mv "$DIR/repacked.tar.gz" "$FILE"

echo "*** $FILE repackaged"

