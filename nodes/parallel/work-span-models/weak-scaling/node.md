---
tag: MGMPAB
kind: concept
slug: weak-scaling
name: Weak scaling
aliases:
- scaled-size scaling
area: parallel/work-span-models
level: intro
summary: Measuring time as problem size and processor count grow together at fixed work per processor. Gustafson's law gives its ideal, a scaled speedup that grows linearly in p.
prereqs: [speedup, parallel-efficiency, strong-scaling]
see_also: [strong-scaling, gustafsons-law, amdahls-law, speedup, parallel-efficiency, parallel-slackness, parallel-reduce]
sources:
  - paper: doi:10.1145/42411.42415
    title: "John L. Gustafson, Reevaluating Amdahl's law, Communications of the ACM 31(5), 1988"
    locator: pp. 532-533, scaled speedup for a problem that grows with the number of processors
  - book: isbn:9780201648652
    title: Ananth Grama, Anshul Gupta, George Karypis and Vipin Kumar, Introduction to Parallel Computing, second edition, Addison-Wesley, 2003
    locator: Chapter 5, analytical modeling of parallel programs (scaled speedup, scalability and the isoefficiency function)
  - book: isbn:9780124159938
    title: Michael McCool, Arch D. Robison and James Reinders, Structured Parallel Programming, Morgan Kaufmann, 2012
    locator: Chapter 2, Section 2.5.5 (Gustafson-Barsis' Law)
---

Weak scaling is the study of how the running time changes when the problem size and the number of processors grow together, with a fixed amount of work for each processor. Perfect weak scaling keeps the time constant. Its measure is the weak scaling efficiency $T(1, W_1)/T(p, p\,W_1)$, and its ideal is given by [Gustafson's law](/gustafsons-law/), just as [Amdahl's law](/amdahls-law/) gives the limit of [strong scaling](/strong-scaling/).

## In plain words

Give each processor the same amount of work, and then add processors and work together. Two processors get a job twice as large, a thousand processors get a job a thousand times as large. If the program scales perfectly, every run takes the same time.

This is the question that a scientist with a bigger machine usually asks: not "how much faster is my old problem" but "how much bigger a problem can I solve in the same time". Weak scaling is easier to get than strong scaling, because each processor always has a large piece of work. It still fails when some cost grows with the number of processors, such as a step that combines the results of all of them.

## The idea

The notation is that of the [work-span model](/work-span-model/).

| Symbol | Meaning |
|---|---|
| $n$ | the input size, which grows with $p$ in a weak scaling test |
| $p$ | the number of processors |
| $W = T_1$ | the work, and the time on one processor |
| $S = T_\infty$ | the span |
| $T_p$ | the time on $p$ processors |
| $W/S$ | the [parallelism](/parallelism/) |
| $W_1$ | the work given to each processor |
| $T(p, W)$ | the time on $p$ processors of a job with work $W$ |

A weak scaling test picks the input size $n(p)$ for each $p$ so that the work is $W(n(p)) = p\,W_1$. It reports the time $T(p, p\,W_1)$ and the weak scaling efficiency

$$E^{w}_p = \frac{T(1, W_1)}{T(p, p\,W_1)}.$$

Perfect weak scaling is $E^w_p = 1$ for all $p$. The *scaled speedup* is $T(1, p\,W_1)/T(p, p\,W_1)$, the [speedup](/speedup/) of the large job. When one processor does the large job $p$ times as slowly as the small one, the scaled speedup is $p\,E^w_p$.

In the model of Gustafson's law, a fraction $s$ of each parallel run is serial. Then the scaled speedup is $s + p(1 - s)$, and the weak scaling efficiency is $(1 - s) + s/p$, which tends to $1 - s$ and not to 0. In the work-span model, the time on $p$ processors is at most $W/p + S$ by [Brent's theorem](/brent-theorem/), so with $W = p\,W_1$ the time is at most $W_1 + S(n(p))$. Weak scaling is good when the span grows much more slowly than the work, for example as $O(\log n)$.

Fixed work and fixed data per processor are the same only when the work is linear in $n$. For a dense matrix product with work $\Theta(n^3)$ on $n \times n$ matrices, fixed work per processor needs $n \propto p^{1/3}$, so the data per processor, $\Theta(n^2/p)$, shrinks as $p^{-1/3}$. A report must say which of the two it keeps fixed.

## Examples

**A parallel sum.** Each processor has $m = 2^{10}$ numbers, so $n = 2^{10} p$. Each processor adds its numbers in $m - 1$ steps, and then a [parallel reduction](/parallel-reduce/) tree adds the $p$ partial sums in $\lg p$ steps. With one unit of time per addition and no cost for communication, $T(p, \cdot) = m - 1 + \lg p$, so $E^w_p = 1023/(1023 + \lg p)$.

| $p$ | $n$ | $T_p$ | $E^w_p$ | scaled speedup |
|---|---|---|---|---|
| 1 | 1024 | 1023 | 1.000 | 1.0 |
| 16 | 16384 | 1027 | 0.996 | 16.0 |
| 256 | 262144 | 1031 | 0.992 | 254.3 |
| 4096 | 4194304 | 1035 | 0.988 | 4052.5 |
| 1048576 | 1073741824 | 1043 | 0.981 | 1029474.4 |

The same computation scales strongly only while each processor has many numbers (see the table on [strong scaling](/strong-scaling/)). Under weak scaling it keeps an efficiency above 0.98 up to a million processors, because the only growing cost is the $\lg p$ steps of the tree.

**Gustafson's numbers.** With a serial fraction $s = 0.05$ of each parallel run, the scaled speedup is $7.65$ on 8 processors and $972.85$ on 1024, and the weak scaling efficiency on 1024 processors is $0.95 + 0.05/1024 \approx 0.950$.

**A cost that grows with $p$.** If each step of a simulation ends with a global sum over all processors in $c \lg p$ time, then the time per step is $t_1 + c \lg p$, and the weak scaling efficiency is $t_1/(t_1 + c\lg p)$. It falls slowly, but it falls. A step that is linear in $p$, such as a gather of one value from each processor to one processor, makes the efficiency tend to 0.

## Where it is used

- **Large simulations.** Climate, fluid and particle codes are usually run at the largest size that fits in the machine, so weak scaling is the main test of whether a larger machine is useful.
- **Capacity planning.** A weak scaling curve answers how large a problem a machine of a given size can solve in a given time.
- **Scalability analysis.** The isoefficiency function (Grama, Gupta, Karypis and Kumar, Chapter 5) asks how fast the work must grow with $p$ to keep the efficiency fixed. Weak scaling with fixed work per processor is the case of linear growth.
- **Reading benchmark claims.** A reported speedup of nearly $p$ on a large machine is often a scaled speedup. Compare it with a [strong scaling](/strong-scaling/) result before you conclude that the fixed job runs $p$ times faster.

## References
