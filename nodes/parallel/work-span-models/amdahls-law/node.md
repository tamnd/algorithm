---
tag: W8TH5A
kind: theorem
slug: amdahls-law
name: Amdahl's law
aliases:
- Amdahl's argument
area: parallel/work-span-models
level: intro
summary: If a fraction f of the one-processor running time can run in parallel and the rest is serial, the speedup on p processors is at most 1/((1 - f) + f/p), and never more than 1/(1 - f).
prereqs: [speedup, work-law]
see_also: [gustafsons-law, strong-scaling, weak-scaling, speedup, parallel-efficiency, parallelism, span-law, brent-theorem]
sources:
  - paper: doi:10.1145/1465482.1465560
    title: "Gene M. Amdahl, Validity of the single processor approach to achieving large scale computing capabilities, AFIPS Spring Joint Computer Conference, 1967"
    locator: pp. 483-485, the argument in words, with no formula
  - book: isbn:9780124159938
    title: Michael McCool, Arch D. Robison and James Reinders, Structured Parallel Programming, Morgan Kaufmann, 2012
    locator: Chapter 2, Section 2.5.4 (Amdahl's Law) and Section 2.5.5 (Gustafson-Barsis' Law)
  - book: isbn:9780201648652
    title: Ananth Grama, Anshul Gupta, George Karypis and Vipin Kumar, Introduction to Parallel Computing, second edition, Addison-Wesley, 2003
    locator: Chapter 5, analytical modeling of parallel programs (speedup, efficiency and scalability)
  - paper: "Alan H. Karp and Horace P. Flatt, Measuring parallel processor performance, Communications of the ACM 33(5), 1990"
    locator: pp. 539-543, the experimentally determined serial fraction
---

Amdahl's law is the bound on the [speedup](/speedup/) of a job of fixed size when a part of it must run serially. If a fraction $f$ of the running time on one processor can be divided among $p$ processors and the rest cannot, the speedup is at most $1/((1 - f) + f/p)$, and it stays below $1/(1 - f)$ for every number of processors. Gene Amdahl gave the argument in words in 1967; the formula is the later standard form. It is the law of [strong scaling](/strong-scaling/), and [Gustafson's law](/gustafsons-law/) is its counterpart for jobs that grow with the machine.

## Statement

The notation is that of the [work-span model](/work-span-model/).

| Symbol | Meaning |
|---|---|
| $n$ | the input size, fixed here |
| $p$ | the number of processors |
| $W = T_1$ | the work, and the time on one processor |
| $S = T_\infty$ | the span |
| $T_p$ | the time on $p$ processors |
| $W/S$ | the [parallelism](/parallelism/) |
| $f$ | the parallel fraction: the part of $T_1$ that can be divided among processors |
| $S_p = T_1/T_p$ | the speedup on $p$ processors |

**Theorem (Amdahl's law).** Let a job take time $T_1 > 0$ on one processor, and let $0 \le f \le 1$. Assume that the job has a serial part of time $(1 - f)T_1$, which runs on one processor at a time and does not overlap with the rest of the job, and a parallel part of time $fT_1$ on one processor, which takes time at least $fT_1/p$ on $p$ processors. Then for each integer $p \ge 1$,

$$T_p \ \ge\ (1 - f)\,T_1 + \frac{f\,T_1}{p}, \qquad S_p = \frac{T_1}{T_p} \ \le\ \frac{1}{(1 - f) + f/p}.$$

Equality holds when the parallel part divides into $p$ equal pieces with no overhead. If $f < 1$, then $S_p < 1/(1 - f)$ for each $p$, and the bound tends to $1/(1 - f)$ as $p \to \infty$.

## In plain words

Some part of every real program has to happen one step at a time: reading the input, setting things up, combining the final answer. More processors make the other part faster, but they do nothing for this serial part. So even with a huge number of processors, the job cannot finish faster than the serial part alone.

If one twentieth of the work is serial, then no machine can make the job more than twenty times faster, however many processors it has. And the gains shrink quickly: the first few processors help a lot, and each new one helps less than the one before. To get a large speedup on a job of fixed size, you must make the serial part very small.

## Proof

Fix $p \ge 1$. The parallel part takes time at least $fT_1/p$ on $p$ processors, by hypothesis. (This is the [work law](/work-law/) for that part: in each unit of time $p$ processors do at most $p$ units of its work.) The serial part takes time $(1 - f)T_1$, because it runs on one processor at a time. The two parts do not overlap, so their times add:

$$T_p \ge (1 - f)\,T_1 + \frac{f\,T_1}{p} = T_1\Big((1 - f) + \frac{f}{p}\Big).$$

The right side is positive, because $(1 - f) + f/p \ge 1/p > 0$. Divide $T_1$ by both sides to get $S_p = T_1/T_p \le 1/((1 - f) + f/p)$. If the parallel part splits into $p$ pieces of time $fT_1/p$ each with no overhead, then $T_p = (1 - f)T_1 + fT_1/p$, and the bound holds with equality.

Now let $f < 1$. Since $f/p \ge 0$, we have $(1 - f) + f/p \ge 1 - f$, so the bound is at most $1/(1 - f)$. If $f > 0$, then $f/p > 0$ and the inequality is strict. If $f = 0$, then $S_p \le 1 = 1/(1 - f)$, with equality. As $p \to \infty$, $f/p \to 0$, so the bound tends to $1/(1 - f)$. $\blacksquare$

The theorem uses $f$ for the parallel fraction. Many texts write the law with the serial fraction $1 - f$ instead; the two forms are the same law.

## Consequences

- **Diminishing returns.** The table gives the bound for some values.

| $f$ | $p = 8$ | $p = 64$ | $p = 1024$ | limit $1/(1-f)$ |
|---|---|---|---|---|
| 0.50 | 1.778 | 1.969 | 1.998 | 2 |
| 0.90 | 4.706 | 8.767 | 9.913 | 10 |
| 0.95 | 5.926 | 15.422 | 19.636 | 20 |
| 0.99 | 7.477 | 39.264 | 91.184 | 100 |

- **Half the limit.** For $0 < f < 1$, the bound reaches exactly half of its limit at $p = f/(1 - f)$, because then $f/p = 1 - f$ and $(1 - f) + f/p = 2(1 - f)$. For $f = 0.95$ this is $p = 19$, with a speedup of 10. Each processor beyond this point gives less than half of what an ideal processor would.
- **Efficiency.** The [parallel efficiency](/parallel-efficiency/) $S_p/p$ is at most $1/(p(1 - f) + f)$, which tends to 0 as $p$ grows. For $f = 0.95$ and $p = 64$ it is at most about $0.241$. So a job of fixed size cannot keep a growing machine busy.
- **Measured serial fraction.** Solving the equality case for the serial fraction gives the Karp-Flatt metric $e = (1/S_p - 1/p)/(1 - 1/p)$ for a measured speedup $S_p$ and $p \ge 2$. If the measured $e$ grows with $p$, the loss comes from overhead that grows with $p$, not only from a fixed serial part.
- **In the work-span model.** A serial part of time $(1 - f)T_1$ is a chain in the DAG, so the span is $T_\infty \ge (1 - f)T_1$ and the parallelism $T_1/T_\infty$ is at most $1/(1 - f)$. The bound of the theorem can be written $T_p \ge T_1/p + (1 - 1/p)(1 - f)T_1$, which is close to the upper bound $T_1/p + T_\infty$ of [Brent's theorem](/brent-theorem/) when the span is mostly the serial part. The [span law](/span-law/) $T_p \ge T_\infty$ is the more general form of the same idea: it needs no split into a serial phase and a parallel phase.

## Tightness

- **The bound is reached.** A chain of $a$ unit steps followed by $b$ independent unit steps has $T_1 = a + b$ and $f = b/(a + b)$. A [greedy schedule](/greedy-scheduling/) takes $a + \lceil b/p \rceil$ steps, which equals the bound when $p$ divides $b$.
- **The hypotheses matter.** A speedup above the bound means that a hypothesis fails. The most common case is superlinear speedup from memory: on $p$ processors the data fits in $p$ caches, so the parallel part takes less than $fT_1/p$. Another case is a serial part that can overlap with the parallel part, for example input that is read while other processors compute.
- **The fraction is not a constant of the program.** For most programs, $f$ depends on the input size $n$: the serial setup often grows more slowly than the parallel work. So the bound for one input size says little about a larger one. [Gustafson's law](/gustafsons-law/) and [weak scaling](/weak-scaling/) look at that case.

## History

Gene Amdahl presented the argument at the AFIPS Spring Joint Computer Conference in April 1967, in a three-page paper that defends fast single processors against arrays of processors. The paper has no formula. It argues in words that the work that must be done serially limits the gain from parallel processing. It uses an estimate that housekeeping takes about 40 percent of the executed instructions, and it gives an upper limit on throughput of five to seven times the sequential processing rate. The formula with a serial fraction is the later standard form of the argument, as in McCool, Robison and Reinders (Section 2.5.4). Karp and Flatt (1990) proposed measuring the serial fraction from observed speedups. Gustafson (1988) argued that the law is too pessimistic for jobs that grow with the machine.

## References
