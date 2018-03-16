rsampling: cmd/rsampling/main.go
	go build -o $@ $<

clean:
	rm -f rsampling

