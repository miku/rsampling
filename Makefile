SHELL := /bin/bash
PROJECT := rsampling
TARGETS := rsampling

rsampling: cmd/rsampling/main.go
	go build -o $@ $<

clean:
	rm -f rsampling


deb: rsampling
	mkdir -p packaging/deb/$(PROJECT)/usr/sbin
	cp $(TARGETS) packaging/deb/$(PROJECT)/usr/sbin
	# mkdir -p packaging/deb/$(PROJECT)/usr/local/share/man/man1
	# cp docs/$(PROJECT).1 packaging/deb/$(PROJECT)/usr/local/share/man/man1
	cd packaging/deb && fakeroot dpkg-deb --build $(PROJECT) .
	mv packaging/deb/$(PROJECT)*.deb .

rpm: rsampling
	mkdir -p $(HOME)/rpmbuild/{BUILD,SOURCES,SPECS,RPMS}
	cp ./packaging/rpm/$(PROJECT).spec $(HOME)/rpmbuild/SPECS
	cp $(TARGETS) $(HOME)/rpmbuild/BUILD
	# cp docs/$(PROJECT).1 $(HOME)/rpmbuild/BUILD
	./packaging/rpm/buildrpm.sh $(PROJECT)
	cp $(HOME)/rpmbuild/RPMS/x86_64/$(PROJECT)*.rpm .