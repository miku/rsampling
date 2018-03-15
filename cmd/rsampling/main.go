package main

import (
	"fmt"
	"math/rand"
	"strconv"
	"strings"
	"time"

	"github.com/fatih/color"
)

type Reservoir struct {
	Counter   int
	Sample    [16]int
	LastIndex int
}

func (r *Reservoir) String() string {
	var vs []string
	for i, v := range r.Sample {
		if i == r.LastIndex {
			green := color.New(color.Bold, color.FgGreen).SprintfFunc()
			vs = append(vs, green(strconv.Itoa(v)))
		} else {
			vs = append(vs, strconv.Itoa(v))
		}
	}

	return fmt.Sprintf("[%04d][%0.8f][%s]", r.Counter, r.P(), strings.Join(vs, ", "))
}

func (r *Reservoir) N() int {
	return len(r.Sample)
}

func (r *Reservoir) P() float64 {
	if r.Counter < r.N() {
		return 0
	}
	return float64(r.N()) / float64(r.Counter)
}

func (r *Reservoir) Add(i int) {
	if r.Counter < r.N() {
		r.Sample[r.Counter] = i
		r.LastIndex = r.Counter
	}
	if r.Counter > r.N() && rand.Float64() < r.P() {
		ix := rand.Intn(r.N())
		r.Sample[ix] = i
		r.LastIndex = ix
	}
	r.Counter++
}

func stream(size int) <-chan int {
	ch := make(chan int)
	go func() {
		for i := 0; i < size; i++ {
			ch <- i
		}
		close(ch)
	}()
	return ch
}

func main() {
	rand.Seed(int64(time.Now().Nanosecond()))
	rr := &Reservoir{}
	for i := range stream(1000) {
		rr.Add(i)
		fmt.Println(rr)
		time.Sleep(10 * time.Millisecond)
	}
}
