---
tag: Y4YA48
kind: concept
slug: parallel-slackness
name: Parallel slackness
aliases:
- slackness
area: parallel/work-span-models
level: core
summary: The ratio (T_1/T_infinity)/p of the parallelism to the number of processors. Slackness well above 1 gives near perfect linear speedup under a greedy scheduler.
prereqs: [parallelism, brent-theorem]
see_also: [speedup, parallel-efficiency, greedy-scheduling, work-stealing, span-law, bsp-model, work-span-model]
sources:
  - book: isbn:9780262033848
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, third edition
    locator: Chapter 27, Section 27.1, the definition of slackness (T_1/T_infinity)/P, Corollary 27.3, and the rule of thumb that a slackness of at least 10 is enough
  - paper: doi:10.1145/321812.321815
    title: "Richard P. Brent, The parallel evaluation of general arithmetic expressions, Journal of the ACM 21(2), 1974"
    locator: Lemma 2, the bound from which the slackness argument follows
  - paper: doi:10.1145/79173.79181
    title: "Leslie G. Valiant, A bridging model for parallel computation, Communications of the ACM 33(8), 1990"
    locator: parallel slackness as more virtual processors than physical ones in the BSP simulation of the PRAM (DOI to be checked)
---

The parallel slackness of a computation on $p$ processors is the ratio $(T_1/T_\infty)/p$ of its [parallelism](/parallelism/) to $p$. It says by how much the parallelism exceeds the number of processors. With slackness $s$, a greedy scheduler reaches a speedup of at least $p \cdot s/(s + 1)$, so a slackness well above 1 gives near perfect linear speedup. With slackness below 1, perfect linear speedup is impossible.

## In plain words

Suppose a job can keep at most some number of workers busy on average. If you have far fewer workers than that, there is almost always a ready task for each worker, and the workers are nearly never idle. Then the job goes almost as many times faster as you have workers.

If you have about as many workers as the job can use, some of them often wait for tasks to become ready, and you lose a large share of the gain. If you have more workers than the job can use, some of them have nothing to do at all. Slackness is the measure of how much room there is: the number the job can use, divided by the number of workers you have.

## The idea

The cost model is the [work-span model](/work-span-model/), with unit-time strands and a greedy scheduler.

| Symbol | Meaning |
|---|---|
| $n$ | the input size |
| $p$ | the number of processors |
| $W$, $T_1$ | the work |
| $S$, $D$, $T_\infty$ | the span |
| $T_p$ | the time on $p$ processors |
| $W/S$ | the parallelism |
| $s$ | the slackness, $(T_1/T_\infty)/p$ |

**Theorem (slackness gives near linear speedup).** If a computation has slackness $s = T_1/(p T_\infty) > 0$, then a greedy schedule on $p$ processors has

$$T_p \le \frac{T_1}{p}\Big(1 + \frac1s\Big), \qquad \frac{T_1}{T_p} \ge p \cdot \frac{s}{s + 1}, \qquad \frac{T_1}{p\,T_p} \ge \frac{s}{s + 1}.$$

*Proof.* By [Brent's theorem](/brent-theorem/), proved there for any greedy schedule, $T_p \le T_1/p + T_\infty$. By the definition of $s$, $T_\infty = T_1/(sp)$. So $T_p \le T_1/p + T_1/(sp) = (T_1/p)(1 + 1/s)$. Divide $T_1$ by both sides to get the bound on the [speedup](/speedup/), and divide once more by $p$ to get the bound on the [parallel efficiency](/parallel-efficiency/). $\blacksquare$

So the efficiency is at least $1 - 1/(s + 1)$. A slackness of 10 gives at least $10/11 \approx 0.91$, and a slackness of 100 gives at least $0.99$. CLRS (third edition, Section 27.1) gives the rule of thumb that a slackness of at least 10 is enough for good speedup. As $s$ grows, the bound tends to perfect linear speedup, which is CLRS Corollary 27.3: if $p \ll T_1/T_\infty$, then $T_p \approx T_1/p$.

**Slackness below 1.** If $s < 1$, then $p > T_1/T_\infty$. The [span law](/span-law/) gives $T_1/T_p \le T_1/T_\infty = sp < p$, so the speedup is less than $p$ for every scheduler, and the efficiency is at most $s$. This holds for any schedule, not only greedy ones.

**Slackness near 1.** With $s = 1$, the greedy bound gives only an efficiency of at least $1/2$. Between the bounds $s/(s+1)$ from below and $\min(1, s)$ from above, the exact value depends on the DAG and on the tie rule of the scheduler.

The sharper greedy bound $T_p \le (T_1 - T_\infty)/p + T_\infty$ gives a slightly better speedup, $p s/(s + 1 - 1/p)$. The numbers below use it.

## Examples

**Parallel Fibonacci of 30.** With one strand to split, one to join, and one for each leaf, the DAG has $T_1 = 4{,}038{,}805$ strands and span $T_\infty = 59$, so the parallelism is about 68,454.

| $p$ | slackness $s$ | speedup at least | efficiency at least |
|---|---|---|---|
| 8 | 8,556.8 | 8.0 | 1.000 |
| 64 | 1,069.6 | 63.9 | 0.999 |
| 1,024 | 66.85 | 1,008.9 | 0.985 |
| 65,536 | 1.04 | 33,481.9 | 0.511 |
| 1,000,000 | 0.07 | 64,068.6 | 0.064 |

At $p = 10^6$ the slackness is below 1, and the speedup is also at most the parallelism, 68,454, whatever the scheduler.

**Merge sort with a serial merge.** For $n = 2^{20}$ items, $T_1 = 23{,}068{,}671$ and $T_\infty = 2{,}097{,}171$, so the parallelism is only about 11.0. On $p = 8$ processors the slackness is about 1.4, and the greedy bound promises a speedup of only 4.89. On $p = 64$ the slackness is about 0.17, and the speedup is at most 11 for any scheduler. A parallel merge raises the parallelism to $\Theta(n/\log^2 n)$, which gives large slackness for these $p$ (see [parallel merge sort](/parallel-merge-sort/)).

**Parallel sum.** For $n = 2^{20}$, $T_1 = 3{,}145{,}726$ and $T_\infty = 41$. On $p = 1{,}024$ the slackness is about 74.9, and the speedup is at least 1,010.5. On $p = 65{,}536$ the slackness is about 1.17, and the speedup is only known to be at least 35,345.5.

## Where it is used

- **Algorithm design.** In the work-span model, a design goal is parallelism far above the number of processors of the target machines, for example by a factor of 10 or more. Then the term $T_\infty$ of Brent's bound is small, and the time is close to $T_1/p$. This is why a low span matters even when $p$ is modest: it buys slackness.
- **Coarsening.** Cutting off the recursion at a grain size $g$ lowers the parallelism, because the span grows by $\Theta(g)$. The slackness says how large $g$ can be before the speedup suffers.
- **Work stealing.** The expected time $T_1/p + O(T_\infty)$ of [work stealing](/work-stealing/) also becomes close to $T_1/p$ when the slackness is large. The constant hidden in $O(T_\infty)$ makes the needed slackness larger than for a greedy scheduler. This bound is cited, not proved here.
- **BSP.** Valiant (1990) used the name parallel slackness in the [BSP model](/bsp-model/) for a related idea: a program written for $v$ virtual processors runs on $p < v$ physical ones, and the extra virtual processors hide the cost of communication. The ratio there is $v/p$, not $(T_1/T_\infty)/p$.

## References
