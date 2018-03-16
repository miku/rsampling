# rsampling

Simple [reservoir
sampling](https://en.wikipedia.org/wiki/Reservoir_sampling#Algorithm_R) for the
command line.

```
$ seq 100 | rsampling -s 8
71
21
83
39
81
47
89
77
```

Sometimes a

```
sort -R  | head -10
```

is fast enough, but sometimes it is not:

```
$ time sort -R fixtures/b | head -10
630163
119338
52446
774497
425201
849943
735918
964258
492182
20209

real	0m19.137s
user	1m12.019s
sys	    0m0.205s

$ time rsampling -s 10 < fixtures/b
624611
645730
368278
871774
388413
546190
605655
178735
16707
298563

real	0m0.187s
user	0m0.168s
sys     0m0.013s
```
