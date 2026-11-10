---
tag: B8J3PC
kind: definition
slug: speedup
name: Speedup
aliases:
- parallel speedup
area: parallel/work-span-models
level: intro
summary: The ratio T_1/T_p of the time on one processor to the time on p processors. It is at most p (no superlinear speedup in the model) and at most the parallelism T_1/T_infinity.
prereqs: [work-and-span, work-law]
see_also: [parallel-efficiency, parallelism, parallel-slackness, work-efficiency, amdahls-law, gustafsons-law, strong-scaling, weak-scaling]
sources:
  - book: isbn:9780262033848
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, third edition
    locator: Chapter 27, Section 27.1, the definitions of speedup T_1/T_P, linear speedup and perfect linear speedup after the work law
  - book: isbn:9780201648652
    title: Ananth Grama, Anshul Gupta, George Karypis and Vipin Kumar, Introduction to Parallel Computing, second edition
    locator: Chapter 5, Section 5.2 (performance metrics, speedup and superlinear speedup; subsection numbers to be checked)
  - paper: doi:10.1109/12.21127
    title: "Derek L. Eager, John Zahorjan and Edward D. Lazowska, Speedup versus efficiency in parallel systems, IEEE Transactions on Computers 38(3), 1989"
    locator: the bounds on speedup in terms of the average parallelism
---

The speedup of a parallel computation on $p$ processors is the ratio $T_1/T_p$ of its time on one processor to its time on $p$ processors. The speedup is *linear* if $T_1/T_p = \Theta(p)$ and *perfect linear* if $T_1/T_p = p$. In the [work-span model](/work-span-model/), the [work law](/work-law/) gives $T_1/T_p \le p$, so superlinear speedup cannot happen there, though real machines sometimes show it. When the one-processor time is that of the best sequential program instead of the parallel program, the ratio is the *absolute* speedup.

## Definition

The cost model is the work-span model, with unit-time strands.

| Symbol | Meaning |
|---|---|
| $n$ | the input size |
| $p$ | the number of processors |
| $W$, $T_1$ | the work, the time of the parallel program on one processor |
| $S$, $D$, $T_\infty$ | the span |
| $T_p$ | the time on $p$ processors under a given scheduler |
| $W/S$ | the parallelism |
| $T_{seq}$ | the time of the best known sequential program for the same problem |

- The **speedup** on $p$ processors is $T_1/T_p$. Some texts write it $S_p$; this page does not, because $S$ is the span here.
- The speedup is **linear** if $T_1/T_p = \Theta(p)$, and **perfect linear** if $T_1/T_p = p$.
- The **relative speedup** is $T_1/T_p$, with $T_1$ the time of the same parallel program on one processor. The **absolute speedup** is $T_{seq}/T_p$, against the best sequential program. If $T_1 \ge T_{seq}$, the absolute speedup is at most the relative one.
- The speedup is **superlinear** if $T_1/T_p > p$.

**No superlinear speedup in the model.** For every schedule, $T_1/T_p \le p$. *Proof.* The work law says $p\,T_p \ge T_1$, because $p$ processors run at most $p$ strands per step and all $T_1$ strands must run. Divide both sides of $p\,T_p \ge T_1$ by $T_p$. $\blacksquare$

**No speedup beyond the parallelism.** For every $p$ and every schedule, $T_1/T_p \le T_1/T_\infty$, by the [span law](/span-law/) $T_p \ge T_\infty$. So

$$\frac{T_1}{T_p} \le \min\Big(p, \frac{T_1}{T_\infty}\Big).$$

**A lower bound for greedy schedules.** By [Brent's theorem](/brent-theorem/), a greedy schedule has $T_p \le T_1/p + (1 - 1/p) T_\infty$. With the parallelism $A = T_1/T_\infty$, this gives $T_1/T_p \ge pA/(A + p - 1)$, the bound of Eager, Zahorjan and Lazowska (1989) in terms of the average parallelism. It is close to $p$ when $p \ll A$, which is the case of large [parallel slackness](/parallel-slackness/).

## Examples and non-examples

**Small DAGs.** A parallel sum of four numbers has $T_1 = 10$ strands and span 5. A greedy schedule on 2 processors takes 6 steps, a speedup of $10/6 \approx 1.67$. A parallel Fibonacci of 5 has $T_1 = 22$ and span 9, so its parallelism is about 2.44. Greedy schedules take 13, 10, 9 and 9 steps on 2, 3, 4 and 8 processors, speedups of about 1.69, 2.2, 2.44 and 2.44. From 4 processors on, the speedup is stuck at the parallelism.

**Relative and absolute speedup.** The [Hillis-Steele scan](/hillis-steele-scan/) of $n = 2^{20}$ numbers does 19,922,945 additions in 20 rounds. A serial prefix sum does 1,048,575 additions. On 8 processors, a greedy scheduler gives $T_8 \le 19{,}922{,}945/8 + 20$, so the relative speedup is above 7.99, nearly perfect. But the work law gives $T_8 \ge 2{,}490{,}369$, so the absolute speedup is at most $1{,}048{,}575 / 2{,}490{,}369 \approx 0.42$: the parallel program on 8 processors is slower than the serial one. A report of relative speedup alone hides this. The work-efficient [Blelloch scan](/blelloch-scan/) does not have this problem (see [work efficiency](/work-efficiency/)).

**Superlinear speedup in practice.** Measured speedups above $p$ do occur, and they come from effects that the model leaves out. Grama, Gupta, Karypis and Kumar (Chapter 5) give two kinds.

- *Memory effects.* With $p$ processors, the data are split into $p$ parts, and each part may fit in the cache of its processor while the whole does not fit in one cache. Then each processor runs faster per operation than the single processor did. In the model, each strand has the same cost on any number of processors, so this cannot happen.
- *Different work.* In a search, $p$ processors look at different parts of the space at once, and one may find a solution early, so that the parallel program does less work in total than the serial one. The serial program and the parallel one then have different computation DAGs, so $T_1$ is not the work of the parallel run.

**Non-example.** A speedup measured against a slow serial program, for example the parallel program run with one thread and all its overheads, is a relative speedup. It is not evidence that the parallel program beats the best serial one.

## Related definitions

- The [parallel efficiency](/parallel-efficiency/) is the speedup per processor, $T_1/(p\,T_p)$.
- The [parallelism](/parallelism/) $T_1/T_\infty$ is the largest speedup over all $p$.
- [Amdahl's law](/amdahls-law/) bounds the speedup when a fixed fraction of the work is serial, and [Gustafson's law](/gustafsons-law/) gives the speedup when the problem grows with $p$. They model [strong scaling](/strong-scaling/) and [weak scaling](/weak-scaling/).
- A [work-efficient](/work-efficiency/) algorithm has $T_1 = O(T_{seq})$, so its relative and absolute speedups differ only by a constant factor.

## References
