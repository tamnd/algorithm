---
tag: XA2GD8
kind: concept
slug: strong-scaling
name: Strong scaling
aliases:
- fixed-size scaling
area: parallel/work-span-models
level: intro
summary: Measuring speedup on more processors while the problem size stays fixed. Amdahl's law and the span bound its limit.
prereqs: [speedup, parallel-efficiency]
see_also: [weak-scaling, amdahls-law, gustafsons-law, speedup, parallel-efficiency, parallelism, brent-theorem, parallel-reduce]
sources:
  - book: isbn:9780201648652
    title: Ananth Grama, Anshul Gupta, George Karypis and Vipin Kumar, Introduction to Parallel Computing, second edition, Addison-Wesley, 2003
    locator: Chapter 5, analytical modeling of parallel programs (speedup and efficiency for a fixed problem size, Amdahl's law, scalability)
  - book: isbn:9780124159938
    title: Michael McCool, Arch D. Robison and James Reinders, Structured Parallel Programming, Morgan Kaufmann, 2012
    locator: Chapter 2, Section 2.5.4 (Amdahl's Law)
  - paper: doi:10.1145/1465482.1465560
    title: "Gene M. Amdahl, Validity of the single processor approach to achieving large scale computing capabilities, AFIPS Spring Joint Computer Conference, 1967"
    locator: pp. 483-485, the argument that the serial part limits the gain for a fixed job
---

Strong scaling is the study of how the running time of a job of fixed size falls as the number of processors grows. Its measures are the [speedup](/speedup/) $T_1/T_p$ and the strong scaling efficiency $T_1/(p\,T_p)$, both for the same input. The limit of strong scaling is given by [Amdahl's law](/amdahls-law/) and, in the [work-span model](/work-span-model/), by the [span law](/span-law/). Its counterpart for jobs that grow with the machine is [weak scaling](/weak-scaling/).

## In plain words

Take one job, for example one simulation with a fixed grid. Run it on one processor, then on two, four, eight, and so on, and time each run. If the time halves each time the processors double, the program scales perfectly.

That never goes on forever. Each processor gets a smaller and smaller piece of the job. The parts that only one processor can do stay the same size, and the cost of talking between processors does not shrink as fast as the pieces. At some point more processors stop helping, and they can even make the job slower. A strong scaling test finds that point. It answers the question: how many processors are worth using for this job?

## The idea

The notation is that of the work-span model.

| Symbol | Meaning |
|---|---|
| $n$ | the input size, fixed in a strong scaling test |
| $p$ | the number of processors |
| $W = T_1$ | the work, and the time on one processor |
| $S = T_\infty$ | the span |
| $T_p$ | the time on $p$ processors |
| $W/S$ | the [parallelism](/parallelism/) |

A strong scaling test fixes $n$ and measures $T_p$ for a range of $p$. It reports the speedup $S_p = T_1/T_p$ and the strong scaling efficiency $E_p = S_p/p$, which is the [parallel efficiency](/parallel-efficiency/) for a fixed input. Perfect strong scaling is $T_p = T_1/p$, so $S_p = p$ and $E_p = 1$.

Three bounds limit strong scaling.

- **The work law.** $T_p \ge T_1/p$, so $S_p \le p$ in the model. A measured $S_p > p$ means that the model does not fit, usually because the pieces fit in the caches.
- **The span law.** $T_p \ge T_\infty$, so $S_p \le T_1/T_\infty$, the parallelism. More processors than the parallelism cannot help.
- **Amdahl's law.** If a part $1 - f$ of $T_1$ is serial and cannot overlap with the rest, then $S_p \le 1/((1 - f) + f/p)$ and $E_p \le 1/(p(1 - f) + f)$. So $E_p$ tends to 0 as $p$ grows, for each fixed job with $f < 1$.

From above, [Brent's theorem](/brent-theorem/) gives $T_p \le T_1/p + T_\infty$ for a greedy schedule, so $E_p \ge 1/(1 + p\,T_\infty/T_1)$. The efficiency stays near 1 while $p$ is much smaller than the parallelism, and it falls when $p$ comes near it.

The baseline $T_1$ matters. An *absolute* speedup divides the time of the best serial program by $T_p$. A *relative* speedup divides the time of the parallel program on one processor by $T_p$. The best serial program is at least as fast as the parallel program on one processor, so the relative speedup is never smaller than the absolute one. A report must say which one it gives.

## Examples

**A parallel sum.** Sum $n = 2^{20}$ numbers on $p$ processors, $p$ a power of two: each processor adds its $n/p$ numbers, and then a [parallel reduction](/parallel-reduce/) tree adds the $p$ partial sums in $\lg p$ steps. With one unit of time per addition and no cost for communication, $T_1 = n - 1$ and $T_p = n/p - 1 + \lg p$.

| $p$ | $T_p$ | $S_p$ | $E_p$ |
|---|---|---|---|
| 1 | 1048575 | 1.0 | 1.000 |
| 16 | 65539 | 16.0 | 1.000 |
| 256 | 4103 | 255.6 | 0.998 |
| 4096 | 267 | 3927.2 | 0.959 |
| 65536 | 31 | 33825.0 | 0.516 |
| 1048576 | 20 | 52428.8 | 0.050 |

The efficiency is close to 1 while each processor has thousands of numbers, and it falls fast when the $\lg p$ steps of the tree are a large part of $T_p$. The parallelism of this computation is $(n - 1)/\lg n \approx 52429$, and the last row reaches it.

**Amdahl's law in a table.** A job takes $T_1 = 1000$ seconds, and 1 percent of it is serial ($f = 0.99$). In the best case $T_p = 10 + 990/p$ seconds. Then $T_8 = 133.75$ s with $E_8 \approx 0.935$, $T_{64} \approx 25.47$ s with $E_{64} \approx 0.613$, and $T_{512} \approx 11.93$ s with $E_{512} \approx 0.164$. The time can never go below 10 s, so the speedup stays below 100.

**Surface and volume.** A 3D grid of $N$ cells is split into $p$ equal cubes. Each processor computes on $N/p$ cells, but it exchanges the faces of its cube, about $6(N/p)^{2/3}$ cells, with its neighbours. The ratio of communication to computation is about $6\,(p/N)^{1/3}$, which grows with $p$. So the efficiency of a strong scaling test of a stencil code falls even with no serial code at all.

## Where it is used

- **Choosing a processor count.** A strong scaling curve shows the number of processors at which the efficiency falls below a chosen level, for example one half. Running at that size or below wastes little of the machine.
- **Latency-bound jobs.** When the answer is needed in a fixed time, such as a weather forecast or a real-time control loop, the input size is given, and only strong scaling matters.
- **Finding bottlenecks.** A drop in efficiency at a certain $p$ points to a serial phase, a load imbalance or a communication cost. The Karp-Flatt metric (see [Amdahl's law](/amdahls-law/)) estimates the serial fraction from the measured speedups.
- **Reports of parallel performance.** Benchmarks usually give both a strong scaling and a [weak scaling](/weak-scaling/) curve, because the two answer different questions. [Gustafson's law](/gustafsons-law/) shows why a program can scale weakly well and strongly poorly.

## References
