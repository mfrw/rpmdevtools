#!/usr/bin/python -tt
# -*- coding: utf-8 -*-

# rpmdev-rmdevelrpms -- Find (and optionally remove) "development" RPMs
#
# Copyright (c) 2004-2014 Ville Skyttä <ville.skytta@iki.fi>
# Credits: Seth Vidal (yum), Thomas Vander Stichele (mach)
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA


import optparse
import os
import re
import stat
import sys

import rpm

try:
    input = raw_input
except NameError:
    pass


__version__ = "1.15"


dev_re = re.compile(r"-(?:de(?:buginfo|vel)|sdk|static)\b", re.IGNORECASE)
test_re = re.compile(r"^perl-(?:Devel|ExtUtils|Test)-")
lib_re1 = re.compile(r"^lib.+")
lib_re2 = re.compile(r"-libs?$")
a_re = re.compile(r"\w\.a$")
so_re = re.compile(r"\w\.so(?:\.\d+)*$")
comp_re = re.compile(r"^compat-gcc")
# required by Ant, which is required by Eclipse...
jdev_re = re.compile(r"^java-.+-gcj-compat-devel$")


def_devpkgs = \
    ("autoconf", "autoconf213", "automake", "automake14", "automake15",
     "automake16", "automake17", "bison", "byacc", "cmake", "dev86", "djbfft",
     "docbook-utils-pdf", "doxygen", "flex", "gcc-g77", "gcc-gfortran",
     "gcc-gnat", "gcc-objc", "gcc32", "gcc34", "gcc34-c++", "gcc34-java",
     "gcc35", "gcc35-c++", "gcc4", "gcc4-c++", "gcc4-gfortran", "gettext",
     "glade", "glade2", "imake", "intltool", "kernel-source",
     "kernel-sourcecode", "libtool", "m4", "nasm", "perl-Module-Build",
     "pkgconfig", "qt-designer", "scons", "swig", "texinfo", "yasm",
     )

def_nondevpkgs = \
    ("glibc-devel", "libstdc++-devel", "vamp-plugin-sdk",
     )


devpkgs = ()
nondevpkgs = ()
qf = '%{NAME}-%{VERSION}-%{RELEASE}.%{ARCH}'


# http://rpm.org/ticket/869
class myhdr(rpm.hdr):
    def __lt__(self, other):
        return rpm.versionCompare(self, other) < 0


def isDevelPkg(hdr):
    """
    Decides whether a package is a devel one, based on name, configuration
    and contents.
    """
    if not hdr:
        return False
    name = hdr[rpm.RPMTAG_NAME]
    if not name:
        return False
    name = hdr.format("%{NAME}")
    na = hdr.format("%{NAME}.%{ARCH}")
    # Check nondevpkgs first (exclusion overrides inclusion)
    if name in nondevpkgs or na in nondevpkgs:
        return False
    if name in devpkgs or na in devpkgs:
        return True
    if name in def_nondevpkgs or na in def_nondevpkgs:
        return False
    if name in def_devpkgs or na in def_devpkgs:
        return True
    if jdev_re.search(name):
        return False
    if dev_re.search(name) or test_re.search(name) or comp_re.search(name):
        return True
    if lib_re1.search(name) or lib_re2.search(name):
        # Heuristics for lib*, *-lib and *-libs packages (kludgy...)
        a_found = so_found = 0
        fnames = hdr[rpm.RPMTAG_FILENAMES]
        fmodes = hdr[rpm.RPMTAG_FILEMODES]
        for i in range(len(fnames)):
            # Peek into the files in the package.
            if not (stat.S_ISLNK(fmodes[i]) or stat.S_ISREG(fmodes[i])):
                # Not a file or a symlink: ignore.
                pass
            fn = fnames[i]
            if so_re.search(fn):
                # *.so or a *.so.*: cannot be sure, treat pkg as non-devel.
                so_found = 1
                break
            if not a_found and a_re.search(fn):
                # A *.a: mmm... this has potential, let's look further...
                a_found = 1
        # If we have a *.a but no *.so or *.so.*, assume devel.
        return a_found and not so_found


def callback(what, bytes, total, h, user):
    "Callback called during rpm transaction."
    sys.stdout.write(".")
    sys.stdout.flush()


def _usage():
    return '''rpmdev-rmdevelrpms [options]

rpmdev-rmdevelrpms is a script for finding and optionally removing
"development" packages, for example for cleanup purposes before starting to
build a new package.

By default, the following packages are treated as development ones and are
thus candidates for removal: any package whose name matches "-devel\\b",
"-debuginfo\\b", "-sdk\\b", or "-static\\b" (case insensitively) except gcc
requirements; any package whose name starts with "perl-(Devel|ExtUtils|Test)-";
any package whose name starts with "compat-gcc"; packages in the internal list
of known development oriented packages (see def_devpkgs in the source code);
packages determined to be development ones based on some basic heuristic
checks on the package\'s contents.

The default set of packages above is not intended to not reduce a system into
a minimal clean build root, but to keep it usable for general purposes while
getting rid of a reasonably large set of development packages.  The package
set operated on can be configured to meet various scenarios.

To include additional packages in the list of ones treated as development
packages, use the "devpkgs" option in the configuration file.  To exclude
packages from the list use "nondevpkgs" in it.  Exclusion overrides inclusion.

The system wide configuration file is __SYSCONFDIR__/rpmdevtools/rmdevelrpms.conf,
and per user settings (which override system ones) can be specified in
~/.config/rpmdevtools/rmdevelrpms.conf or ~/.rmdevelrpmsrc (deprecated).
These files are written in Python.

Report bugs to <http://bugzilla.redhat.com/>.'''


def version():
    print("rpmdev-rmdevelrpms version %s" % __version__)
    print('''
Copyright (c) 2004-2014 Ville Skyttä <ville.skytta@iki.fi>
This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.''')
    sys.exit(0)


def main():
    "Da meat."

    # TODO: implement -r|--root for checking a specified rpm root
    op = optparse.OptionParser(usage=_usage())
    op.add_option("-l", "--list-only", dest="listonly", action="store_true",
                  help="Output condensed list of packages, do not remove.")
    op.add_option("--qf", "--queryformat", dest="qf", action="store",
                  default=qf, help="Query format to use for output.")
    op.add_option("-y", "--yes", dest="yes", action="store_true",
                  help="Root only: remove without prompting; ignored with -l.")
    op.add_option("-v", "--version", dest="version", action="store_true",
                  help="Print program version and exit.")

    (opts, args) = op.parse_args()

    if opts.version:
        version()

    ts = rpm.TransactionSet("/")
    ts.setVSFlags(~(rpm._RPMVSF_NOSIGNATURES | rpm._RPMVSF_NODIGESTS))
    mi = ts.dbMatch()
    hdrs = []
    for hdr in mi:
        if isDevelPkg(hdr):
            hdrs.append(myhdr(hdr))
            ts.addErase(mi.instance())
    ts.order()

    try:
        if len(hdrs) > 0:
            hdrs.sort(
                key=lambda x: (x[rpm.RPMTAG_NAME], x, x[rpm.RPMTAG_ARCH]))
            indent = ""
            if not opts.listonly:
                indent = "  "
                print("Found %d devel packages:" % len(hdrs))
            for hdr in hdrs:
                print(indent + hdr.sprintf(opts.qf))
            if opts.listonly:
                pass
            else:
                # TODO: is there a way to get arch for the unresolved deps?
                unresolved = ts.check()
                if unresolved:
                    print("...whose removal would cause unresolved "
                          "dependencies:")
                    unresolved.sort(key=lambda x: x[0][0])
                    for t in unresolved:
                        dep = t[1][0]
                        if t[1][1]:
                            dep = dep + " "
                            if t[2] & rpm.RPMSENSE_LESS:
                                dep = dep + "<"
                            if t[2] & rpm.RPMSENSE_GREATER:
                                dep = dep + ">"
                            if t[2] & rpm.RPMSENSE_EQUAL:
                                dep = dep + "="
                            dep = dep + " " + t[1][1]
                        if t[4] == rpm.RPMDEP_SENSE_CONFLICTS:
                            dep = "conflicts with " + dep
                        elif t[4] == rpm.RPMDEP_SENSE_REQUIRES:
                            dep = "requires " + dep
                        print("  %s-%s-%s %s" %
                              (t[0][0], t[0][1], t[0][2], dep))
                    print("Not removed due to dependencies.")
                elif os.geteuid() == 0:
                    if not opts.yes:
                        proceed = input("Remove them? [y/N] ")
                    else:
                        proceed = "y"
                    if (proceed in ("Y", "y")):
                        sys.stdout.write("Removing...")
                        errors = ts.run(callback, "")
                        print("Done.")
                        if errors:
                            for error in errors:
                                print(error)
                            sys.exit(1)
                    else:
                        print("Not removed.")
                else:
                    print("Not running as root, skipping remove.")
        else:
            print("No devel packages found.")
    finally:
        ts.closeDB()
        del ts


for conf in ("__SYSCONFDIR__/rpmdevtools/rmdevelrpms.conf",
             os.path.join(os.environ["HOME"], ".rmdevelrpmsrc"),  # deprecated
             os.path.join(os.environ["HOME"],
                          ".config/rpmdevtools/rmdevelrpms.conf")):
    try:
        with open(conf) as f:
            exec(compile(f.read(), conf, "exec"))
    except IOError:
        pass
    if hasattr(devpkgs, "split"):
        devpkgs = devpkgs.split()
    if hasattr(nondevpkgs, "split"):
        nondevpkgs = nondevpkgs.split()
main()
