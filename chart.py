#!/usr/bin/env python
# coding: utf-8

"""
Run sort -R, shuf and rsampling performance tests.
"""

import collections
import logging
import re
import subprocess
import sys
import tempfile
import time

import matplotlib.pyplot as plt
import pandas as pd

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("b")

def shellout(template, preserve_whitespace=False, executable='/bin/bash',
             ignoremap=None, encoding=None, pipefail=True, **kwargs):
    """

    Takes a shell command template and executes it. The template must use the
    new (2.6+) format mini language. `kwargs` must contain any defined
    placeholder, only `output` is optional and will be autofilled with a
    temporary file if it used, but not specified explicitly.

    If `pipefail` is `False` no subshell environment will be spawned, where a
    failed pipe will cause an error as well. If `preserve_whitespace` is `True`,
    no whitespace normalization is performed. A custom shell executable name can
    be passed in `executable` and defaults to `/bin/bash`.

    Raises RuntimeError on nonzero exit codes. To ignore certain errors, pass a
    dictionary in `ignoremap`, with the error code to ignore as key and a string
    message as value.

    Simple template:

        wc -l < {input} > {output}

    Quoted curly braces:

        ps ax|awk '{{print $1}}' > {output}

    Usage with luigi:

        ...
        tmp = shellout('wc -l < {input} > {output}', input=self.input().path)
        luigi.LocalTarget(tmp).move(self.output().path)
        ....

    """
    if not 'output' in kwargs:
        kwargs.update({'output': tempfile.mkstemp(prefix='gluish-')[1]})
    if ignoremap is None:
        ignoremap = {}
    if encoding:
        command = template.decode(encoding).format(**kwargs)
    else:
        command = template.format(**kwargs)
    if not preserve_whitespace:
        command = re.sub('[ \t\n]+', ' ', command)
    if pipefail:
        command = '(set -o pipefail && %s)' % command
    logger.debug(command)
    code = subprocess.call([command], shell=True, executable=executable)
    if not code == 0:
        if code in ignoremap:
            logger.info("Ignoring error via ignoremap: %s" % ignoremap.get(code))
        else:
            logger.error('%s: %s' % (command, code))
            error = RuntimeError('%s exitcode: %s' % (command, code))
            error.code = code
            raise error
    return kwargs.get('output')


class Timer(object):
    """
    Timing context manager.

        with Timer() as t:
            pass
        if t.elapsed > 1:
            print("too slow")
    """
    def __enter__(self):
        self.start = time.time()
        return self

    def __exit__(self, *args):
        self.end = time.time()
        self.elapsed = self.end - self.start

def safe_plot(df, **kwargs):
    """
    Create a plot and safe it to a file.
    """
    ax = df.plot.bar(grid=True)
    ax.set_title(kwargs.get('title', ''))
    ax.set_xlabel(kwargs.get('xlabel', ''))
    ax.set_ylabel(kwargs.get('ylabel', ''))
    fig = ax.get_figure()
    plt.tight_layout()
    fig.savefig(kwargs.get('filename', 'out.png'))


if __name__ == '__main__':
    # Basic benchmark.
    sizes = (10, 100, 1000, 10000, 20000, 30000, 40000, 50000)
    bm = collections.defaultdict(list)

    # Allow command to be set as first argument.
    cmd = "rsampling"
    if len(sys.argv) > 1:
        cmd = sys.argv[1]

    for n in sizes:
        with Timer() as t:
            shellout("seq {n} | ./{cmd} -n 16", n=n, cmd=cmd)
        bm[cmd].append(t.elapsed)

        with Timer() as t:
            shellout("seq {n} | sort -R | head -16", n=n, pipefail=False)
        bm['sort'].append(t.elapsed)

        with Timer() as t:
            shellout("seq {n} | shuf -n 16", n=n, pipefail=False)
        bm['shuf'].append(t.elapsed)

    df = pd.DataFrame(bm, index=sizes)
    safe_plot(df, title='Random subset (16 from N) via sort -R, shuf and {}'.format(cmd),
              xlabel='N', ylabel='time (s)', filename='images/bm1-{}.png'.format(cmd))

    # Compare shuf and rsampling N = 16
    sizes = (1000000, 10000000, 50000000, 100000000)
    bm = collections.defaultdict(list)

    for n in sizes:
        with Timer() as t:
            shellout("seq {n} | ./{cmd} -n 16", n=n, cmd=cmd)
        bm[cmd].append(t.elapsed)

        with Timer() as t:
            shellout("seq {n} | shuf -n 16", n=n, pipefail=False)
        bm['shuf'].append(t.elapsed)

    df = pd.DataFrame(bm, index=sizes)
    safe_plot(df, title='Random subset (16 from N) via shuf and {}'.format(cmd),
              xlabel='N', ylabel='time (s)', filename='images/bm2-{}.png'.format(cmd))

    # Compare shuf and rsampling N = 100000
    sizes = (1000000, 10000000, 50000000, 100000000)
    bm = collections.defaultdict(list)

    for n in sizes:
        with Timer() as t:
            shellout("seq {n} | ./{cmd} -n 100000 > /dev/null", n=n, cmd=cmd)
        bm[cmd].append(t.elapsed)

        with Timer() as t:
            shellout("seq {n} | shuf -n 100000 > /dev/null", n=n, pipefail=False)
        bm['shuf'].append(t.elapsed)

    df = pd.DataFrame(bm, index=sizes)
    safe_plot(df, title='Random subset (100000 from N) via shuf and {}'.format(cmd),
              xlabel='N', ylabel='time (s)', filename='images/bm3-{}.png'.format(cmd))
