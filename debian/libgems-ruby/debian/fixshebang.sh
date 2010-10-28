#!/bin/sh
ruby="$1"
target_dir="$2"
for f in `find "$target_dir" -type f 2>/dev/null`
do
  cp -pf $f $f.tmp
  sed -e '1,1s,^#![ 	]*\([^ 	]*\)/\(ruby\|env ruby\)$,#!/usr/bin/'$ruby',' \
      -e '1,1s,^#![ 	]*\([^ 	]*\)/\(wish\|perl\)$,#!/usr/bin/\2,' < $f > $f.tmp
  if ! cmp $f $f.tmp >/dev/null
  then
      mv -f $f.tmp $f
  else
      rm -f $f.tmp
  fi
done
