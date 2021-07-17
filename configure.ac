AC_INIT(rpmdevtools, 9.5)
AM_INIT_AUTOMAKE([foreign 1.11 dist-xz no-dist-gzip
                          -Wall -Wno-portability -Werror])

AC_PROG_SED

AC_PATH_PROG([HELP2MAN], [help2man])
if test -z "$HELP2MAN" ; then
    AC_MSG_ERROR([help2man is required])
fi

AC_PATH_PROG([POD2MAN], [pod2man])
if test -z "$POD2MAN" ; then
    AC_MSG_ERROR([pod2man is required])
fi

PKG_CHECK_VAR([bashcompdir], [bash-completion], [completionsdir],
    [HAVE_BASHCOMP2=1], [bashcompdir="${sysconfdir}/bash_completion.d"])
AM_CONDITIONAL([HAVE_BASHCOMP2], [test "$HAVE_BASHCOMP2" = 1])
AC_SUBST(bashcompdir)

AC_OUTPUT(
Makefile
emacs/Makefile
qa-robot/Makefile
)
