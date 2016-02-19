
ID := $(shell git describe --tags | sed 's,-,_,g')
PACKAGE_NAME = g2-$(ID)
PACKAGE = $(PACKAGE_NAME).tgz
TARGET = $(shell pwd)

package: $(PACKAGE)

$(PACKAGE): bin tests
	mkdir -p $(PACKAGE_NAME)
	mkdir -p $(PACKAGE_NAME)/bin
	mkdir -p $(PACKAGE_NAME)/tests
	install README.md $(PACKAGE_NAME) 
	install bin/* $(PACKAGE_NAME)/bin
	install tests/* $(PACKAGE_NAME)/tests
	tar czf $(PACKAGE) $(PACKAGE_NAME)
	rm -rf $(PACKAGE_NAME)

rpm: clean g2.spec package
	[ ! -d RPM-BUILD ] && mkdir -p RPM-BUILD/tmp || :
	[ ! -d RPM-BUILD/SOURCES ] && mkdir -p RPM-BUILD/SOURCES || :
	[ ! -d RPM-BUILD/BUILD ] && mkdir -p RPM-BUILD/BUILD || :
	[ ! -d RPM-BUILD/RPMS/noarch ] && mkdir -p RPM-BUILD/RPMS/noarch || :
	cp g2-$(ID).tgz RPM-BUILD/SOURCES
	rpmbuild -D "_topdir $(TARGET)/RPM-BUILD" -D "_tmpdir $(TARGET)/RPM-BUILD/tmp" -bb g2.spec

g2.spec: g2.spec.in
	sed "s,@VERSION@,$(ID),g" g2.spec.in > g2.spec

rpmlint: g2.spec
	rpmlint g2.spec

clean:
	rm -f g2.spec test/*.pyc rpmmacros rpmrc
	rm -rf g2-* RPM-BUILD

.PHONY: package rpm rpmlint clean rpmrc
