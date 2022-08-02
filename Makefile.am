SUBDIRS = emacs qa-robot

pkgsysconfdir = $(sysconfdir)/rpmdevtools
bashcompdir = @bashcompdir@

bin_SCRIPTS = rpmdev-newinit rpmdev-newspec rpmdev-rmdevelrpms
dist_bin_SCRIPTS = rpmdev-checksig rpmdev-diff rpmdev-extract rpmdev-md5 \
	rpmdev-setuptree rpmdev-sort rpmdev-vercmp rpmdev-wipetree rpminfo \
	rpmls rpmdev-bumpspec rpmdev-packager rpmdev-spectool

man1_MANS = rpmdev-diff.1 rpmdev-extract.1 rpmdev-bumpspec.1 rpmdev-newinit.1 \
	rpmdev-newspec.1 rpmdev-packager.1 rpmdev-spectool.1
man8_MANS = rpmdev-rmdevelrpms.8

dist_pkgsysconf_DATA = curlrc newspec.conf rmdevelrpms.conf \
	spectemplate-lib.spec spectemplate-minimal.spec \
	spectemplate-perl.spec spectemplate-php-pear.spec \
	spectemplate-python.spec spectemplate-pyproject.spec spectemplate-ruby.spec \
	spectemplate-ocaml.spec spectemplate-R.spec spectemplate-dummy.spec \
	template.init

bashcomp_DATA = rpmdevtools.bash-completion

EXTRA_DIST = rpmdev-newinit.in rpmdev-newspec.in rpmdev-rmdevelrpms.py \
	rpmdevtools.bash-completion.in

MOSTLYCLEANFILES = $(bin_SCRIPTS) $(man1_MANS) $(man8_MANS) $(bashcomp_DATA)

sums = sum cksum sha1 sha224 sha256 sha384 sha512

all: $(bin_SCRIPTS) $(man1_MANS) $(man8_MANS) $(bashcomp_DATA)

%: %.in
	$(SED) -e 's|__SYSCONFDIR__|$(sysconfdir)|g' $< > $@
	case "$(bin_SCRIPTS)" in *$@*) chmod +x $@ ;; esac

%: %.py
	$(SED) -e 's|__SYSCONFDIR__|$(sysconfdir)|g' $< > $@
	chmod +x $@

rpmdev-spectool.1: rpmdev-spectool
	COLUMNS=1000 $(HELP2MAN) -s 1 -N -h -h -v --version $(<D)/$(<F) -o $@

%.1: %
	PATH="$(<D):$$PATH" COLUMNS=1000 $(HELP2MAN) -s 1 -N -h -h -v -v $(<F) -o $@

%.8: %
	COLUMNS=1000 $(HELP2MAN) -s 8 -N $(<D)/$(<F) -o $@

install-exec-hook:
	cd $(DESTDIR)$(bindir) && \
	for sum in $(sums) ; do ln rpmdev-md5 rpmdev-$$sum ; done

if HAVE_BASHCOMP2
install-data-hook:
	mv $(DESTDIR)$(bashcompdir)/rpmdevtools.bash-completion \
		$(DESTDIR)$(bashcompdir)/rpmdev-bumpspec ; \
	for f in rpmdev-{checksig,cksum,diff,extract,md5,newspec,rmdevelrpms,setuptree,sha{1,224,256,384,512},sum,vercmp} rpminfo rpmls spectool ; do \
		ln -s rpmdev-bumpspec $(DESTDIR)$(bashcompdir)/$$f ; \
	done
endif

uninstall-hook:
	cd $(DESTDIR)$(bindir) && \
	for sum in $(sums) ; do $(RM) rpmdev-$$sum ; done
if HAVE_BASHCOMP2
	cd $(DESTDIR)$(bashcompdir) && \
	$(RM) rpmdev-{bumpspec,checksig,cksum,diff,extract,md5,newspec,rmdevelrpms,setuptree,sha{1,224,256,384,512},sum,vercmp} rpminfo rpmls spectool
endif

python_scripts = rpmdev-bumpspec rpmdev-checksig rpmdev-rmdevelrpms \
	rpmdev-sort rpmdev-vercmp
flake8 = flake8

flake8: $(python_scripts)
	$(flake8) $(python_scripts)

shell_scripts = rpmdev-diff rpmdev-extract rpmdev-md5 rpmdev-newinit \
	rpmdev-newspec rpmdev-packager rpmdev-setuptree rpmdev-wipetree \
	rpminfo rpmls template.init
bashate = bashate
shellcheck = shellcheck

bashate: $(shell_scripts)
	$(bashate) $(shell_scripts)

shellcheck: $(shell_scripts)
	$(shellcheck) $(shell_scripts)

check-local: $(shell_scripts)
	ret=0
	for file in $(shell_scripts) ; do \
		bash -n -O extglob $$file || ret=$$? ; \
	done ; \
	exit $$ret
