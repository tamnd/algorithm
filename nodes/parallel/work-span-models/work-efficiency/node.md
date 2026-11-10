---
tag: QE42AJ
kind: definition
slug: work-efficiency
name: Work efficiency
aliases:
- cost-optimality
- work-optimality
- work-efficient
- work-optimal
area: parallel/work-span-models
level: core
summary: A parallel algorithm is work-efficient if its work is O(T_seq), the time of the best sequential algorithm for the same problem, so that it does no more than a constant factor of extra work.
prereqs: [work-and-span, work-law]
see_also: [blelloch-scan, hillis-steele-scan, parallel-efficiency, speedup, parallelism, list-ranking, parallel-merge-sort, brent-theorem]
sources:
  - paper: "Guy E. Blelloch, Prefix sums and their applications, Technical Report CMU-CS-90-190, School of Computer Science, Carnegie Mellon University, 1990"
    title: "Guy E. Blelloch, Prefix sums and their applications, 1990"
    locator: the up-sweep and down-sweep scan with O(n) work and O(log n) depth
  - paper: doi:10.1145/7902.7903
    title: "W. Daniel Hillis and Guy L. Steele Jr., Data parallel algorithms, Communications of the ACM 29(12), 1986"
    locator: the prefix sum by recursive doubling in lg n steps (pp. 1170-1183 for the paper)
  - book: isbn:9780201548563
    title: Joseph JaJa, An Introduction to Parallel Algorithms
    locator: Chapter 1, the work-time framework and the notion of a work-optimal algorithm (section number to be checked)
  - paper: doi:10.1145/227234.227246
    title: "Guy E. Blelloch, Programming parallel algorithms, Communications of the ACM 39(3), 1996"
    locator: the work and depth of algorithms and the aim of work-efficient parallel algorithms
---

A parallel algorithm is work-efficient if its work is $W(n) = O(T_{seq}(n))$, where $T_{seq}(n)$ is the time of the best sequential algorithm for the same problem. It then does at most a constant factor more operations than a serial program. Work efficiency matters most when the number of processors is small, because then the time is about $W/p$, and extra work costs time directly. The [Blelloch scan](/blelloch-scan/) is work-efficient and the [Hillis-Steele scan](/hillis-steele-scan/) is not.

## Definition

The cost model is the [work-span model](/work-span-model/), with unit-time strands. In the PRAM work-time framework the same definition applies, with the work as the total number of operations.

| Symbol | Meaning |
|---|---|
| $n$ | the input size |
| $p$ | the number of processors |
| $W$, $T_1$ | the work |
| $S$, $D$, $T_\infty$ | the span |
| $T_p$ | the time on $p$ processors |
| $W/S$ | the parallelism |
| $T_{seq}$ | the time of the best sequential algorithm, which must be named |

- A parallel algorithm is **work-efficient** if $W(n) = O(T_{seq}(n))$.
- It is **work-optimal** if, in addition, $T_{seq}$ is a lower bound for the problem, so that no algorithm, serial or parallel, does asymptotically less work. JáJá uses the word optimal in this sense for PRAM algorithms in the work-time framework.

The definition depends on which sequential bound is used, so a claim of work efficiency should name it. A parallel matrix product with $\Theta(n^3)$ work is work-efficient against the standard $\Theta(n^3)$ algorithm, but not against [Strassen's algorithm](/strassen-algorithm/).

**Cost-optimality is a related but different notion.** An algorithm on $p$ processors is cost-optimal if $p\,T_p = O(T_{seq})$ (see [parallel efficiency](/parallel-efficiency/)). The cost $p\,T_p$ counts idle steps too, so it is at least $W$ by the [work law](/work-law/). So cost-optimal implies work-efficient. The converse holds when the schedule wastes little: a greedy schedule has $p\,T_p \le W + (p - 1)T_\infty$, so a work-efficient algorithm is cost-optimal on $p = O(W/T_\infty)$ processors.

**Why work efficiency matters more than span for small $p$.** By the work law and [Brent's theorem](/brent-theorem/), a greedy schedule has

$$\frac{W}{p} \le T_p \le \frac{W}{p} + S.$$

When $p$ is well below the [parallelism](/parallelism/) $W/S$, the term $W/p$ is much larger than $S$, so $T_p \approx W/p$. An algorithm that does $c$ times the work of another then runs about $c$ times slower, whatever its span. A smaller span helps only through the term $S$, which is already small. And a parallel algorithm with work $W$ beats the serial one only if $W/p < T_{seq}$, that is, on more than $W/T_{seq}$ processors. An algorithm that does $\lg n$ times too much work needs more than $\lg n$ processors to break even. When $p$ is near or above $W/S$, the term $S$ takes over, and then the span matters more.

## Examples and non-examples

**Prefix sums.** The serial prefix sum of $n$ numbers takes $n - 1$ additions, which is optimal.

- The **Blelloch scan** (Blelloch 1990) does an up-sweep of $n - 1$ additions and a down-sweep of $n - 1$ additions, so $W = 2(n - 1) = \Theta(n)$ and $S = 2 \lg n = \Theta(\log n)$ for $n$ a power of 2. It is work-efficient.
- The **Hillis-Steele scan** (Hillis and Steele 1986) runs $\lg n$ rounds, and round $j$ adds to each of the $n - 2^j$ positions $i \ge 2^j$ the value at $i - 2^j$. So $W = n \lg n - n + 1 = \Theta(n \log n)$ and $S = \lg n$. It is not work-efficient: it does $\Theta(\log n)$ times too much work.

For $n = 2^{20}$:

| algorithm | $W$ (additions) | $S$ (steps) | $T_8$, by the work law and Brent | absolute speedup on 8 processors |
|---|---|---|---|---|
| serial loop | 1,048,575 | 1,048,575 | 1,048,575 | 1 |
| Hillis-Steele | 19,922,945 | 20 | at least 2,490,369 | at most 0.43 |
| Blelloch | 2,097,150 | 40 | at most 262,183 | at least 3.99 |

The Hillis-Steele scan has half the span of the Blelloch scan, but on 8 processors it is slower than the serial loop, by the work law alone. It beats the serial loop only on $p \ge 20$ processors, since $19{,}922{,}945/19 > 1{,}048{,}575$. The Blelloch scan has an absolute speedup of at most $p/2$, because it does twice the serial work, and it gets close to $p/2$ when $p$ is well below its parallelism.

**More examples.**

- [Parallel merge sort](/parallel-merge-sort/) with a parallel merge has work $\Theta(n \log n)$. This matches the bound for [comparison sorts](/comparison-sort-lower-bound/), so it is work-optimal among comparison sorts.
- [List ranking](/list-ranking/) by [pointer jumping](/pointer-jumping/) does $\Theta(n \log n)$ work against the serial $\Theta(n)$, so it is not work-efficient. Work-efficient versions exist (see [parallel list ranking](/parallel-list-ranking/)).
- P-FIB of CLRS, the [parallel Fibonacci](/parallel-fibonacci/) procedure, does $\Theta(\phi^n)$ work to compute $F_n$, which a serial loop computes in $\Theta(n)$ additions. It is a teaching example of the model, not a work-efficient algorithm.

**Non-example.** High parallelism is not work efficiency. The Hillis-Steele scan has a parallelism of about $n$, larger than the $\Theta(n / \log n)$ of the Blelloch scan, but it is the less efficient of the two.

## Related definitions

- The [parallel efficiency](/parallel-efficiency/) $T_1/(p\,T_p)$ measures waste in the schedule. Work efficiency measures waste in the algorithm. The absolute efficiency $T_{seq}/(p\,T_p)$ is the product of the two ratios $T_{seq}/T_1$ and $T_1/(p\,T_p)$.
- The relative and absolute [speedups](/speedup/) differ by the factor $T_1/T_{seq}$, which is a constant exactly for work-efficient algorithms.
- The class [NC](/nc/) asks for polylogarithmic time with polynomial work. It does not ask for work efficiency.

## References
