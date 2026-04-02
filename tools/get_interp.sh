#!/bin/sh

set -e

rmtemp() {
	test "$tempdir" -a -d "$tempdir" || return 0
	rm "$tempdir/conftest" || true
	rmdir "$tempdir"
}
trap rmtemp EXIT
tempdir="$(mktemp -d)"

cd "$tempdir"
echo 'int main(int argc, char **argv) { return 0; }' |
	$@ -o conftest -xc -
${OBJCOPY:-objcopy} -j.interp -Obinary conftest /dev/stdout |
	xargs -0 echo
