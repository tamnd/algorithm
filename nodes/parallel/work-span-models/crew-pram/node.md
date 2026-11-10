---
tag: RA6DW1
kind: model
slug: crew-pram
name: CREW PRAM
aliases:
- concurrent-read exclusive-write PRAM
- CREW
area: parallel/work-span-models
level: core
summary: The PRAM in which many processors may read one cell in a step but only one may write it. Merging by ranking uses its concurrent reads, and the OR of n bits still needs Omega(log n) steps on it.
prereqs: [pram-model, erew-pram]
see_also: [pram-model, erew-pram, crcw-pram, merging-sorted-sequences, parallel-merge, parallel-binary-search, shiloach-vishkin-merge, valiant-parallel-merge]
sources:
  - paper: doi:10.1145/800133.804339
    title: "Steven Fortune and James Wyllie, Parallelism in random access machines, STOC 1978"
    locator: pp. 114-118, the P-RAM, which allows simultaneous reads and halts on a simultaneous write
  - book: isbn:9780201548563
    title: Joseph JaJa, An Introduction to Parallel Algorithms, Addison-Wesley, 1992
    locator: Chapter 1 (the PRAM variants) and Chapter 4, Section 4.2 (merging by ranking, and the optimal merging algorithm)
  - paper: "Stephen Cook, Cynthia Dwork and Ruediger Reischuk, Upper and lower time bounds for parallel random access machines without simultaneous writes, SIAM Journal on Computing 15(1), 1986"
    locator: pp. 87-97, a PRAM without simultaneous writes needs at least log_b of the sensitivity steps, with b = (5 + 21^(1/2))/2
  - paper: "Noam Nisan, CREW PRAMs and decision trees, SIAM Journal on Computing 20(6), 1991"
    locator: pp. 999-1007, CREW time of a Boolean function is Theta of the logarithm of its block sensitivity
  - book: isbn:9780262031417
    title: Thomas H. Cormen, Charles E. Leiserson and Ronald L. Rivest, Introduction to Algorithms, first edition, MIT Press, 1990
    locator: Chapter 30, Section 30.2 (CRCW versus EREW, with Theorem 30.1)
---

The CREW PRAM (concurrent read, exclusive write) is the [PRAM](/pram-model/) in which any number of processors may read one memory cell in the same step, but at most one processor may write a cell in a step. It is the model of Fortune and Wyllie's original P-RAM. Concurrent reads make it easy to share a value, so a broadcast takes one step and many binary searches can run on one sorted array at once, as in merging by ranking. Exclusive writes still limit it: Cook, Dwork and Reischuk (1986) proved that the OR of $n$ bits needs $\Omega(\log n)$ steps on a CREW PRAM, however many processors it has.

## The machine

The notation follows the parallel pages of this site.

| Symbol | Meaning |
|---|---|
| $n$ | the input size |
| $p$ | the number of processors |
| $W = T_1$ | the work: the number of operations |
| $S = T_\infty$ | the number of parallel steps, written $T(n)$ |
| $T_p$ | the time on $p$ processors |
| $W/S$ | the parallelism |

The machine is the synchronous PRAM of the [PRAM model](/pram-model/) page. In each step each processor reads a cell, computes and writes a cell, and all reads see the memory as it was before the step. The CREW rule is a condition on each step:

- any number of processors may read one cell, and
- for each cell, at most one processor writes it.

An algorithm is a CREW algorithm only if no step on any input has two writers of one cell. Fortune and Wyllie's P-RAM (1978) is of this kind: it allows simultaneous reads, and a simultaneous write to one cell makes the machine halt and reject.

**Simulation.** The file `crew_pram.py` runs one step at a time. It keeps the local registers of each processor, so a processor can choose the cell it reads from its registers, as a binary search does. It records the readers and the writers of each cell in each step and raises an error when a cell has two writers. With a flag it also rejects concurrent reads, which turns it into an [EREW PRAM](/erew-pram/), so the tests can show which algorithms need concurrent reads.

## What it counts

The measures are those of every PRAM: the time $T(n)$, the number of processors $P(n)$, and the work, either as the cost $P(n)\,T(n)$ or as the number of operations $W(n)$ in the work-time framework (JáJá, Section 1.5). A work-efficient CREW algorithm has work $O(T_{\text{seq}}(n))$ for the best serial time $T_{\text{seq}}(n)$ on a RAM.

Concurrent reads are free in this model. A value that $k$ processors need costs one step, not the $\Omega(\log k)$ steps of an EREW PRAM.

**Broadcast in one step.** If cell $x$ holds a value, then in one step each processor $i$ reads $x$ and writes cell $B[i]$. The reads are concurrent and the writes are to distinct cells, so the step is CREW. On an EREW PRAM the same task needs at least $\log_4 p$ steps (Theorem 1 on [EREW PRAM](/erew-pram/)).

**Merging by ranking.** Let $A = a_0 \le a_1 \le \cdots \le a_{m-1}$ and $B = b_0 \le b_1 \le \cdots \le b_{n-1}$ be sorted. Use $m + n$ processors, one for each item (JáJá, Section 4.2).

1. Processor $(a, i)$ finds $r_i = |\{j : b_j < a_i\}|$ by a [binary search](/parallel-binary-search/) in $B$. Processor $(b, j)$ finds $s_j = |\{i : a_i \le b_j\}|$ by a binary search in $A$. All searches run in lock step, one probe per step.
2. Processor $(a, i)$ writes $a_i$ to $C[i + r_i]$, and processor $(b, j)$ writes $b_j$ to $C[j + s_j]$.

The searches take $\lceil \lg(\max(m, n) + 1) \rceil$ steps, so the time is $O(\log(m + n))$ with $m + n$ processors, and the work is $O((m + n)\log(m + n))$. In the first probe every processor $(a, i)$ reads the middle cell of $B$, so the reads are concurrent. The tests check that each run with $m \ge 2$ has a cell with two or more readers and that the EREW check rejects the run.

*Correctness.* Order all items by value, with an item of $A$ before an item of $B$ of the same value, and items of one list in the order of their indices. The items before $a_i$ in this order are $a_0, \ldots, a_{i-1}$ (they are at most $a_i$, and an equal one has a smaller index) and the $b_j$ with $b_j < a_i$ (an equal $b_j$ comes after $a_i$). So $a_i$ has exactly $i + r_i$ items before it. The items before $b_j$ are the $a_i$ with $a_i \le b_j$ and $b_0, \ldots, b_{j-1}$, so $b_j$ has exactly $j + s_j$ items before it. These counts are the positions of the items in a total order, so they are distinct and they fill $0, \ldots, m + n - 1$. Hence the writes are exclusive and $C$ is the sorted merge. $\blacksquare$

The tests merge lists of all sizes from 0 to 8 and some larger ones, with many ties and with few ties, and compare with `sorted`. A step with two writers would raise an error, so the tests also check that the tie rule gives distinct positions.

Merging by ranking is not work-efficient, because the serial merge takes $O(m + n)$ time. JáJá (Section 4.2) splits the lists into blocks of size about $\log n$ by ranking only some items, then merges the blocks serially, and gets $O(\log n)$ time with $O(n)$ work on a CREW PRAM. See also [parallel merge](/parallel-merge/), [merging sorted sequences](/merging-sorted-sequences/), and the merges of [Shiloach and Vishkin](/shiloach-vishkin-merge/) and [Valiant](/valiant-parallel-merge/).

## Relation to other models

- **EREW.** Every [EREW](/erew-pram/) algorithm is a CREW algorithm. The CREW PRAM is strictly stronger for broadcast: one step against $\Omega(\log p)$.
- **CRCW.** Every CREW algorithm is a [CRCW](/crcw-pram/) algorithm under each write rule, because a step with one writer per cell is legal under every rule and gives the same memory. The CRCW PRAM is strictly stronger: with the common rule and $n$ processors it computes the OR of $n$ bits in one step, and the CREW PRAM needs $\Omega(\log n)$ steps (below).
- **Simulation on EREW.** A $p$-processor EREW PRAM runs one CREW step in $O(\log p)$ steps by sorting the read requests by address and copying each value to all the requests for its cell. This is a special case of the simulation of a CRCW step (Vishkin, 1983; CLRS, first edition, Theorem 30.1). So the CREW PRAM is at most a factor $O(\log p)$ faster than the EREW PRAM with the same number of processors.
- **Decision trees.** Nisan (1991) proved that the CREW time of a Boolean function is $\Theta(\log \mathrm{bs}(f))$, where $\mathrm{bs}(f)$ is its block sensitivity, and that this equals $\Theta(\log D(f))$ for the depth $D(f)$ of a decision tree for $f$. So the CREW time of a Boolean function is fixed, up to a constant factor, by a measure that has nothing to do with parallel machines.

## Known results in the model

**The OR lower bound.** For a Boolean function $f$ of $n$ inputs, the *sensitivity* $s(f)$ is the largest number, over all inputs $x$, of positions $i$ such that changing bit $i$ of $x$ changes $f(x)$. Cook, Dwork and Reischuk (1986) proved:

**Theorem (Cook, Dwork and Reischuk).** A PRAM without simultaneous writes that computes $f$ needs at least $\log_b s(f)$ steps, where $b = \tfrac{1}{2}(5 + \sqrt{21}) \approx 4.79$. The bound holds for any number of processors and any instruction set, because it counts only how information moves through the shared memory.

At the all-zeros input, changing any bit changes the OR, so $s(\mathrm{OR}) = n$, and the OR needs at least $\log_b n \approx 0.44 \lg n$ steps on a CREW PRAM. The balanced tree computes it in $\lceil \lg n \rceil$ steps, so the bound is tight within a constant factor. The same holds for AND, and for the largest of $n$ numbers, because a maximum algorithm on inputs in $\{0, 1\}$ computes the OR. The proof is not given here. The page on [EREW PRAM](/erew-pram/) proves a simpler bound of the same kind for broadcast, where exclusive reads give the factor 4 per step.

**Other results.**

- **Merging.** $O(\log n)$ time and $O(n)$ work (JáJá, Section 4.2), as above.
- **Searching.** $p$ processors can search a sorted array of $n$ items faster than one binary search: in each step they probe $p$ evenly spaced cells, and the interval shrinks by a factor of $p + 1$, so the time is $O(\log n / \log(p + 1))$. Every processor reads the search key, so the method uses concurrent reads. See [parallel binary search](/parallel-binary-search/).
- **Prefix sums, list ranking and sorting.** The EREW algorithms for these problems run on the CREW PRAM unchanged, in $O(\log n)$ time.

## References
