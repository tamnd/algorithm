---
tag: 0YP0ZM
kind: theorem
slug: external-sorting-io-lower-bound
name: I/O lower bound for sorting
aliases:
- Aggarwal-Vitter sorting bound
- sort(N) lower bound
area: sorting/external-sorting
level: advanced
summary: Sorting N records with memory M and block size B needs Theta((N/B) log_{M/B}(N/B)) block transfers in the worst case.
prereqs: [external-sorting-lower-bound, external-memory-model, disk-striping, external-merge-sort]
see_also: [permuting-lower-bound, external-permuting, balance-sort, external-samplesort, funnelsort, comparison-sort-lower-bound]
sources:
  - paper: doi:10.1561/0400000014
    title: Jeffrey Scott Vitter, Algorithms and Data Structures for External Memory, Foundations and Trends in Theoretical Computer Science 2(4), 2008
    locator: Theorem 5.1 (the sorting bound for D disks), Section 4.2 (disk striping, equations 4.1 to 4.4) and Theorem 6.1 (the constant 2)
  - paper: doi:10.1145/48529.48535
    title: Alok Aggarwal and Jeffrey Scott Vitter, The input/output complexity of sorting and related problems, Communications of the ACM 31(9), 1988, pages 1116 to 1127
    locator: Theorem 3.1 (the sorting bound) and Section 4 (the lower bound proofs)
  - paper: doi:10.1007/BF01185207
    title: Jeffrey Scott Vitter and Elizabeth A. M. Shriver, Algorithms for parallel memory I, Two-level memories, Algorithmica 12(2-3), 1994, pages 110 to 147
    locator: the parallel disk model and the randomized distribution sort for D disks
  - paper: "Mark H. Nodine and Jeffrey Scott Vitter, Greed Sort: an optimal sorting algorithm for multiple disks, Journal of the ACM 42(4), 1995"
    locator: pp. 919 to 933, the deterministic merge sort with the optimal bound for D disks
---

The I/O bound for sorting says that $N$ items, with a memory of $M$ items, blocks of $B$ items and $D$ parallel disks, take $\Theta\big(\frac{n}{D}\log_m n\big)$ parallel I/Os to sort, where $n = N/B$ and $m = M/B$. The lower bound for one disk is proved on the page [external sorting lower bound](/external-sorting-lower-bound/). This page proves the bound for $D$ disks from it, shows that a merge sort with [disk striping](/disk-striping/) meets it when $D \le \sqrt m$, and proves that every striped algorithm needs $\Omega\big(\frac nD \log_{m/D} \frac nD\big)$ parallel I/Os, so striping is not optimal when $D$ is close to $m$.

## Statement

**Model.** The parallel disk model of Vitter and Shriver: an internal memory of $M$ items and $D \ge 1$ disks, each with blocks of $B$ items. One *parallel I/O* reads or writes at most one block on each disk, at any position on each disk. The input of $N$ items is *striped*: block $i$ of the file, the items $iB$ to $iB + B - 1$, is at position $\lfloor i/D \rfloor$ on disk $i \bmod D$. The output must be striped in the same way. *Stripe* $j$ is position $j$ on all $D$ disks, that is, blocks $jD$ to $jD + D - 1$ of the file. Items are indivisible, the algorithm is deterministic and learns about keys only by comparisons, and computation in memory is free, as on the page [external sorting lower bound](/external-sorting-lower-bound/). We write $n = N/B$ and $m = M/B$, and assume that $D$ divides $n$ and $m$.

**Theorem.** Assume $B \le M/2$ and $N \ge e^2 B$.

(a) Each sorting algorithm on $D$ disks makes, in the worst case, at least $\dfrac{1}{5D}\, n \log_m n$ parallel reads.

(b) If $m \ge 9$, $D \le \sqrt m$ and $N > M$, striped merge sort sorts with fewer than $16 \frac{n}{D} \log_m n$ parallel I/Os.

(c) A *striped* algorithm is one in which each parallel I/O transfers whole stripes, one block at the same position on each disk. If $DB \le M/2$ and $N \ge e^2 DB$, each striped sorting algorithm makes at least $\dfrac15 \cdot \dfrac nD \log_{m/D} \dfrac nD$ parallel reads in the worst case.

So for $D \le \sqrt m$ the sort bound is $\Theta\big(\frac nD \log_m n\big)$, and striping is optimal up to a constant factor. For each $D \le m/2$ the bound is the same, but only methods that use the disks independently meet it.

## In plain words

Sorting a large file needs a few passes over the data. Each pass reads and writes the whole file. The number of passes depends on how many pieces memory can merge at one time. With several disks, each pass can be faster, because the disks work at the same time.

The page proves three facts. First, several disks can make a sort at most that many times faster: a machine with one disk can copy each step of the many disks with a few single steps. Second, if the disks are few compared with the size of memory, the simple method of treating all disks as one large disk is fast enough. Third, if there are many disks, that simple method is slow, because the large blocks fill memory and make the number of passes grow. Then only methods that use each disk on its own reach the best speed.

## Proof

**(a) Lower bound for D disks.** Let $\mathcal{A}$ be an algorithm on $D$ disks that makes at most $t$ parallel reads on each input of $N$ items. Build an algorithm $\mathcal{A}'$ for one disk with the same $M$ and $B$. It stores block $j$ of disk $d$ of $\mathcal{A}$ in block $jD + d$ of its one disk. Block $i$ of the input file is on disk $i \bmod D$ at position $\lfloor i/D \rfloor$, so it maps to block $\lfloor i/D \rfloor D + (i \bmod D) = i$. So the input of $\mathcal{A}$ maps to the usual input of the one-disk model, blocks $0$ to $n - 1$ in order, and the same holds for the output. $\mathcal{A}'$ runs $\mathcal{A}$ step by step. A parallel read of at most $D$ blocks becomes at most $D$ single reads of the mapped blocks into the same cells of memory. A parallel write becomes at most $D$ single writes. Computation and comparisons are the same. After each step, the memory of $\mathcal{A}'$ and the contents of its disk are the images of those of $\mathcal{A}$, so $\mathcal{A}'$ sorts, and it makes at most $Dt$ reads. $\mathcal{A}'$ satisfies the hypotheses of the theorem on the page [external sorting lower bound](/external-sorting-lower-bound/), with $B \le M/2$ and $N \ge e^2 B$, so

$$Dt \ge \frac15 \cdot \frac NB \log_{M/B} \frac NB = \frac15\, n \log_m n,$$

which is (a).

**(b) Upper bound by striping.** Treat the $D$ disks as one disk with blocks of $B' = DB$ items, as in the template on the page [disk striping](/disk-striping/). Block $j$ of this logical disk is stripe $j$, and one I/O on it is one parallel I/O. The striped input layout is the usual layout of the logical disk. Run [external merge sort](/external-merge-sort/) on the logical disk. The page of the [external memory model](/external-memory-model/) shows that for $N > M \ge 3B'$, with $B'$ dividing $M$, the merge sort makes fewer than $8 \lceil N/B' \rceil \log_{M/B'}(N/B')$ I/Os. Here $M/B' = m/D \ge \sqrt m \ge 3$, because $D \le \sqrt m$ and $m \ge 9$, and $B'$ divides $M$ because $D$ divides $m$. Also $\lceil N/B' \rceil = n/D$. Because $D \le \sqrt m$, $\log(m/D) \ge \frac12 \log m$, and because $D \ge 1$, $\log(n/D) \le \log n$. So

$$8\, \frac nD \log_{m/D} \frac nD = 8\, \frac nD \cdot \frac{\log(n/D)}{\log(m/D)} \le 8\, \frac nD \cdot \frac{\log n}{\frac12 \log m} = 16\, \frac nD \log_m n,$$

which is (b).

**(c) Lower bound for striped algorithms.** In a striped algorithm, each parallel I/O moves whole stripes, and stripe $j$ holds the items $jDB$ to $(j+1)DB - 1$ of the striped layout. So the algorithm is an algorithm for one disk with blocks of $B' = DB$ items, in the usual layout, with one I/O for each parallel I/O. Apply the theorem of the page [external sorting lower bound](/external-sorting-lower-bound/) with block size $B'$. Its hypotheses are $B' \le M/2$ and $N \ge e^2 B'$, which are the hypotheses of (c). It gives at least $\frac15 \frac{N}{B'} \log_{M/B'} \frac{N}{B'} = \frac15 \frac nD \log_{m/D} \frac nD$ reads. $\blacksquare$

## Consequences

- **Passes.** One pass over the data costs $2n/D$ parallel I/Os, so the bound says that sorting takes $\Theta(\log_m n)$ passes, the same number as with one disk. Several disks make each pass faster, but they do not reduce the number of passes.
- **The cost of striping.** By (c), striping loses the factor $\frac{\log(n/D)/\log(m/D)}{\log n/\log m}$, which is about $\log m / \log(m/D)$. For $n = 10^6$ and $m = 1000$, the two terms $\frac nD \log_m n$ and $\frac nD \log_{m/D} \frac nD$ are:

| disks D | $\frac nD \log_m n$ | $\frac nD \log_{m/D} \frac nD$ | ratio |
|---|---|---|---|
| 1 | 2000000 | 2000000 | 1.00 |
| 10 | 200000 | 250000 | 1.25 |
| 31 | 64516 | 96405 | 1.49 |
| 100 | 20000 | 40000 | 2.00 |
| 333 | 6006 | 21868 | 3.64 |

When $D = m/c$ for a constant $c \ge 2$, the ratio is $\Theta(\log m)$ for $n \ge m^2$, so no striped algorithm can be optimal there.

- **Independent disks reach the bound.** Nodine and Vitter's Greed Sort, a merge sort, and their [balance sort](/balance-sort/), a distribution sort, sort with $O\big(\frac nD \log_m n\big)$ parallel I/Os for all $D \le m/2$, deterministically. Vitter and Shriver gave a randomized distribution sort with this bound; distribution sort with randomized cycling, a variant of [external samplesort](/external-samplesort/), is a simpler one. The lower bound (a) shows that all of them are optimal up to a constant factor.
- **Striping only the writes.** Vitter's Section 4.2 explains that an optimal sort needs independent access only for reads or only for writes. A sort can therefore keep striped output, which makes the parity of a RAID array easy to maintain.
- **Permuting.** The same reduction as in (a) moves the permuting bound $\Theta\big(\min\{N, n \log_m n\}\big)$ of the page [permuting lower bound](/permuting-lower-bound/) to $D$ disks, divided by $D$. See [external permuting](/external-permuting/).

## Tightness

- **The constant.** Vitter's Theorem 6.1, from the work of Hutchinson, Sanders and Vitter, gives the lower bound $\sim \frac{2n}{D} \log_m n$ when $B \log m = \omega(\log N)$ and $m$ grows. The factor 2 is one read and one write of each block in each pass. Merge sort with randomized cycling and simple randomized merge sort come close to this constant.
- **The range of (b).** The constant 16 in (b) is not sharp: it comes from the bound 8 for one disk and from $\log(m/D) \ge \frac12 \log m$. For $D \le m^{\varepsilon}$ with a fixed $\varepsilon < 1$, the same steps give the constant $8/(1 - \varepsilon)$.
- **The range of (c).** For $D$ near $m$, striping needs at least the bound of (c), and striped merge sort with fan-in $m/D - 1$ meets it up to a constant factor when $m/D \ge 3$. So (c) is tight for striped algorithms.
- **Small inputs.** If $N \le M$, one read and one write of each stripe sort the items, so the cost is $\Theta(n/D)$, and the term $\log_m n$ is less than 1. The bound is usually written $\Theta\big(\frac nD \frac{\log(1 + n)}{\log(1 + m)}\big)$ to cover this case.

## History

Aggarwal and Vitter proved the bound $\Theta\big(\frac nP \log_m n\big)$ in 1988 for a model in which one I/O moves up to $P$ blocks at any positions. Vitter and Shriver introduced the parallel disk model with $D$ independent disks in 1994 and gave a randomized sort that meets the bound there. Nodine and Vitter gave the first deterministic optimal sorts for this model, Balance Sort and Greed Sort. Vitter's survey of 2008 states the result as Theorem 5.1 and explains in Section 4.2 why disk striping is not optimal.

## References
