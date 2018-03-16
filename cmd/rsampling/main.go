package main

import (
	"bufio"
	"flag"
	"fmt"
	"io"
	"log"
	"math/rand"
	"os"
	"strings"
	"time"
)

var (
	size = flag.Int("s", 16, "number of sample to obtain")
	seed = flag.Int64("r", int64(time.Now().Nanosecond()), "random seed")
)

type Reservoir struct {
	counter int64
	size    int
	sample  []string
}

func NewReservoir() *Reservoir {
	return &Reservoir{size: 16}
}

func NewReservoirSize(size int) *Reservoir {
	return &Reservoir{size: size}
}

func (r *Reservoir) String() string {
	return strings.Join(r.sample, "\n")
}

func (r *Reservoir) Sample() []string {
	return r.sample
}

func (r *Reservoir) P() float64 {
	if r.counter < int64(r.size) {
		return 0
	}
	return float64(r.size) / float64(r.counter)
}

func (r *Reservoir) Add(s string) {
	if r.counter < int64(r.size) {
		r.sample = append(r.sample, s)
	} else {
		if rand.Float64() < r.P() {
			ix := rand.Intn(r.size)
			r.sample[ix] = s
		}
	}
	r.counter++
}

func main() {
	flag.Parse()
	rand.Seed(*seed)
	rr := NewReservoirSize(*size)
	br := bufio.NewReader(os.Stdin)
	for {
		line, err := br.ReadString('\n')
		if err == io.EOF {
			break
		}
		if err != nil {
			log.Fatal(err)
		}
		rr.Add(strings.TrimSpace(line))
	}
	for _, v := range rr.Sample() {
		fmt.Println(v)
	}
}
