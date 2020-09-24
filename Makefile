SHELL := /bin/bash
PROJECT := rsampling
TARGETS := rsampling rsampling-scanner

all: $(TARGETS)

%: cmd/%/main.go
	go build -o $@ $<

clean:
	rm -f $(TARGETS)
	rm -f rsampling-*.x86_64.rpm
	rm -f rsampling_*_amd64.deb

.PHONY: images
images:
	python chart.py rsampling
	python chart.py rsampling-scanner

.PHONY: benchmarks
benchmarks: cpu-rsampling.png cpu-rsampling-scanner.png

cpu-%.png: %
	seq 1 100000000 | ./$^ -cpuprofile cpu-$^.pprof -n 16
	go tool pprof -output cpu-$^.png -png $^ cpu-$^.pprof

deb: $(TARGETS)
	mkdir -p packaging/deb/$(PROJECT)/usr/sbin
	cp $(TARGETS) packaging/deb/$(PROJECT)/usr/sbin
	# mkdir -p packaging/deb/$(PROJECT)/usr/local/share/man/man1
	# cp docs/$(PROJECT).1 packaging/deb/$(PROJECT)/usr/local/share/man/man1
	cd packaging/deb && fakeroot dpkg-deb --build $(PROJECT) .
	mv packaging/deb/$(PROJECT)*.deb .

rpm: $(TARGETS)
	mkdir -p $(HOME)/rpmbuild/{BUILD,SOURCES,SPECS,RPMS}
	cp ./packaging/rpm/$(PROJECT).spec $(HOME)/rpmbuild/SPECS
	cp $(TARGETS) $(HOME)/rpmbuild/BUILD
	# cp docs/$(PROJECT).1 $(HOME)/rpmbuild/BUILD
	./packaging/rpm/buildrpm.sh $(PROJECT)
	cp $(HOME)/rpmbuild/RPMS/x86_64/$(PROJECT)*.rpm .
