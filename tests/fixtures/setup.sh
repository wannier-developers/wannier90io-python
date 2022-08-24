#!/bin/bash

set -ex

version=$1

if [ -z "$WANNIER90_TMP" ]; then
  WANNIER90_TMP=/tmp/wannier90
fi

mkdir -p $WANNIER90_TMP

pushd $WANNIER90_TMP

if [ ! -f "v${version}.tar.gz" ]; then
  wget https://github.com/wannier-developers/wannier90/archive/v${version}.tar.gz
fi

tar zxf v${version}.tar.gz

pushd wannier90-${version}

if [ "$version" == "2.0.1" ]; then
  touch make.sys
  echo "F90=gfortran" >> make.sys
  echo "LIBS=-lblas -llapack" >> make.sys
else
  touch make.inc
  echo "F90=gfortran" >> make.inc
  echo "LIBS=-lblas -llapack" >> make.inc
fi

make wannier post w90chk2chk

popd
popd

cp $WANNIER90_TMP/wannier90-${version}/*.x ./wannier90-$1/
cp -r $WANNIER90_TMP/wannier90-${version}/examples ./wannier90-$1/
