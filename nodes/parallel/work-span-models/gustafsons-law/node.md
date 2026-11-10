---
tag: 0Z9QC0
kind: theorem
slug: gustafsons-law
name: Gustafson's law
aliases:
- Gustafson-Barsis law
- scaled speedup law
area: parallel/work-span-models
level: intro
summary: If a run on p processors spends a fraction s of its time in serial code, the same job on one processor takes s + p(1 - s) times as long. This scaled speedup grows linearly in p.
prereqs: [speedup, amdahls-law]
see_also: [amdahls-law, weak-scaling, strong-scaling, speedup, parallel-efficiency, parallel-slackness]
sources:
  - paper: doi:10.1145/42411.42415
    title: "John L. Gustafson, Reevaluating Amdahl's law, Communications of the ACM 31(5), 1988"
    locator: pp. 532-533, the scaled speedup s' + p'N with s' + p' = 1 for the time on the parallel machine
  - book: isbn:9780124159938
    title: Michael McCool, Arch D. Robison and James Reinders, Structured Parallel Programming, Morgan Kaufmann, 2012
    locator: Chapter 2, Section 2.5.5 (Gustafson-Barsis' Law) and Section 2.5.4 (Amdahl's Law)
  - book: isbn:9780201648652
    title: Ananth Grama, Anshul Gupta, George Karypis and Vipin Kumar, Introduction to Parallel Computing, second edition, Addison-Wesley, 2003
    locator: Chapter 5, analytical modeling of parallel programs (scaled speedup and scalability)
---

Gustafson's law gives the *scaled speedup* of a job that grows with the machine: if a run on $p$ processors spends a fraction $s$ of its time in serial code, then one processor would need $s + p(1 - s)$ times as long for the same job. The speedup grows linearly in $p$, with slope $1 - s$. John Gustafson stated it in 1988 as an answer to [Amdahl's law](/amdahls-law/). The two laws do not contradict each other: they measure the serial part of different runs, and the page proves the exact conversion.

## Statement

The notation is that of the [work-span model](/work-span-model/).

| Symbol | Meaning |
|---|---|
| $n$ | the input size, which grows with $p$ here |
| $p$ | the number of processors |
| $W = T_1$ | the work, and the time on one processor |
| $S = T_\infty$ | the span |
| $T_p$ | the time on $p$ processors |
| $W/S$ | the [parallelism](/parallelism/) |
| $s$ | the serial fraction *of the run on $p$ processors* |
| $f$ | Amdahl's parallel fraction *of the run on one processor* |

**Theorem 1 (Gustafson's law).** Let a job run on $p \ge 1$ processors in time $T_p > 0$, and let $0 \le s \le 1$. Assume that during a time $s\,T_p$ the job runs serial code on one processor, and during the other $(1 - s)\,T_p$ all $p$ processors do useful work. Assume that one processor runs the serial code in the same time, and does the work of the parallel part in $p$ times the time. Then the time of the same job on one processor is $T_1 = (s + p(1 - s))\,T_p$, and the scaled speedup is

$$\frac{T_1}{T_p} = s + p\,(1 - s) = p - (p - 1)\,s.$$

**Theorem 2 (conversion).** For the job of Theorem 1, the parallel fraction of the run on one processor is

$$f = \frac{p\,(1 - s)}{s + p\,(1 - s)}, \qquad\text{and conversely}\qquad s = \frac{1 - f}{(1 - f) + f/p}.$$

Amdahl's formula $1/((1 - f) + f/p)$ with this $f$ equals $s + p(1 - s)$.

## In plain words

Amdahl's law keeps the job fixed and asks how much faster more processors make it. Gustafson turned the question around. People who buy a bigger machine usually run a bigger job on it, in about the same time. In a bigger job, the parallel part grows, but the serial part often stays about the same.

So measure the serial part on the big machine. Suppose it takes one twentieth of the run there. One processor would need the same time for the serial part, but it would need the whole machine's effort for the rest. That makes the single processor many times slower, and the factor grows almost in step with the number of processors. With this view, large machines are useful, as long as the jobs grow with them.

## Proof

*Theorem 1.* By the hypotheses, one processor runs the serial code in time $s\,T_p$. In the parallel part, $p$ processors work for time $(1 - s)\,T_p$, so one processor needs time $p\,(1 - s)\,T_p$ for that work. The two parts add up to $T_1 = s\,T_p + p\,(1 - s)\,T_p = (s + p(1 - s))\,T_p$. Divide by $T_p > 0$. The second form follows from $s + p - ps = p - (p - 1)s$.

*Theorem 2.* Write $G = s + p(1 - s)$, which is at least 1 because it is a weighted mean of 1 and $p$ with weights $s$ and $1 - s$. The run on one processor takes $G\,T_p$, of which $p(1 - s)\,T_p$ is the parallel part. So $f = p(1 - s)/G$ and $1 - f = s/G$. Then

$$(1 - f) + \frac{f}{p} = \frac{s}{G} + \frac{1 - s}{G} = \frac{1}{G},$$

so Amdahl's formula gives $1/((1 - f) + f/p) = G$. For the converse, the last equation gives $G = 1/((1 - f) + f/p)$, and then $s = (1 - f)\,G = (1 - f)/((1 - f) + f/p)$. $\blacksquare$

So on one job, the two laws give the same number. They differ in what they hold fixed when $p$ changes. Amdahl's law holds $f$ fixed, so the job is fixed. Gustafson's law holds $s$ fixed, so the job grows, and then $1 - f = s/(s + p(1 - s))$ tends to 0 as $p$ grows.

## Consequences

- **Linear growth.** With $s$ fixed, the scaled speedup grows by $1 - s$ for each added processor, with no upper limit.
- **Weak scaling efficiency.** The scaled efficiency is $(s + p(1 - s))/p = (1 - s) + s/p$, which tends to $1 - s$, not to 0. This is the ideal of [weak scaling](/weak-scaling/), and it is the counterpart of the efficiency bound of Amdahl's law in [strong scaling](/strong-scaling/). See also [parallel efficiency](/parallel-efficiency/).
- **Example.** Let $s = 0.05$. The scaled speedup is $7.65$ on 8 processors, $60.85$ on 64, and $972.85$ on 1024. For the job on 1024 processors, Theorem 2 gives $1 - f = 0.05/972.85 \approx 5.14 \times 10^{-5}$: the serial part is 5 percent of the parallel run but only about 0.005 percent of the one-processor run. A fixed job with $f = 0.95$ has an Amdahl bound of only about $19.64$ on 1024 processors.
- **Reading a speedup claim.** A reported [speedup](/speedup/) must say whether the problem size was fixed or scaled. A scaled speedup of 900 and a fixed-size speedup of 20 can describe the same program.

## Tightness

- **Theorem 1 is an identity in its model, not an inequality.** It holds with equality when its hypotheses hold. When the parallel part has overhead, such as communication that grows with $p$, the useful work in the parallel part is less than $p(1 - s)T_p$, and the true scaled speedup is smaller.
- **The one-processor time is often hypothetical.** The scaled job may not fit in the memory of one processor, so $T_1$ is computed, not measured. The law then states how much work the machine did, compared with one processor.
- **The serial part need not stay fixed.** If the serial part grows with the job, for example a serial input phase that is linear in $n$, then $s$ grows with $p$, and the speedup is below the line $p - (p - 1)s$ for the value of $s$ at a small $p$.
- **It does not give a time bound for a fixed job.** For a fixed job, [Amdahl's law](/amdahls-law/) and the [span law](/span-law/) still hold.

## History

John Gustafson published "Reevaluating Amdahl's law" in the Communications of the ACM in May 1988. He wrote the time on the parallel machine as $s' + p' = 1$ and the time of a serial processor as $s' + p'N$ on $N$ processors, and he called the ratio the scaled speedup. He based the argument on work at Sandia National Laboratories, where scaled speedups of about 1016 to 1021 were measured on a hypercube with 1024 processors. McCool, Robison and Reinders call the law the Gustafson-Barsis law (Section 2.5.5).

## References
