---
tag: 43RZPV
kind: model
slug: pram-model
name: PRAM model
aliases:
- parallel random-access machine
- PRAM
area: parallel/work-span-models
level: core
summary: The parallel random-access machine has p processors that run in lock step on one shared memory, with unit cost per step. Its variants differ in the rules for two processors that use one cell.
prereqs: [random-access-machine, unit-cost-model]
see_also: [erew-pram, crew-pram, crcw-pram, work-span-model, brent-theorem, work-efficiency, nc, bsp-model]
sources:
  - paper: doi:10.1145/800133.804339
    title: "Steven Fortune and James Wyllie, Parallelism in random access machines, STOC 1978"
    locator: pp. 114-118, the P-RAM with simultaneous reads, a halt on simultaneous writes, processors started by FORK, and the result that polynomial time on the P-RAM equals PSPACE
  - book: isbn:9780201548563
    title: Joseph JaJa, An Introduction to Parallel Algorithms, Addison-Wesley, 1992
    locator: Chapter 1 (the PRAM model and its variants, and Section 1.5, the work-time presentation framework and the WT scheduling principle)
  - book: isbn:9780262031417
    title: Thomas H. Cormen, Charles E. Leiserson and Ronald L. Rivest, Introduction to Algorithms, first edition, MIT Press, 1990
    locator: Chapter 30 (algorithms for parallel computers), Section 30.2 (CRCW versus EREW, with Theorem 30.1) and Section 30.3 (Brent's theorem and work efficiency)
  - paper: "Stephen Cook, Cynthia Dwork and Ruediger Reischuk, Upper and lower time bounds for parallel random access machines without simultaneous writes, SIAM Journal on Computing 15(1), 1986"
    locator: pp. 87-97, the lower bound of log_b of the sensitivity with b = (5 + 21^(1/2))/2 on a CREW PRAM, so Omega(log n) for the OR of n inputs
  - paper: doi:10.1016/0196-6774(83)90033-0
    title: "Uzi Vishkin, Implementation of simultaneous memory address access in models that forbid it, Journal of Algorithms 4(1), 1983"
    locator: pp. 45-50, the simulation of a concurrent-access step on an exclusive-access PRAM by sorting the requests
  - paper: doi:10.1137/0217049
    title: Richard Cole, Parallel merge sort, SIAM Journal on Computing 17(4), 1988
    locator: sorting n items in O(log n) time with n processors on the EREW PRAM
---

The PRAM (parallel random-access machine) is the classic model of a shared-memory parallel computer: $p$ processors, each a [random access machine](/random-access-machine/), run one program in lock step and use one shared memory. Each step costs one unit of time, as in the [unit-cost model](/unit-cost-model/). Fortune and Wyllie defined it in 1978. Its variants, [EREW](/erew-pram/), [CREW](/crew-pram/) and [CRCW](/crcw-pram/), differ only in what they allow when two processors read or write one memory cell in the same step.

## The machine

The notation follows the parallel pages of this site.

| Symbol | Meaning |
|---|---|
| $n$ | the input size |
| $p$ | the number of processors |
| $W = T_1$ | the work: the number of operations, and the time on one processor |
| $S = T_\infty$ | the span: here the number of parallel steps, written $T(n)$ |
| $T_p$ | the time on $p$ processors |
| $W/S$ | the parallelism |

A PRAM has processors $P_1, P_2, \ldots, P_p$ and an unbounded shared memory of cells $M[0], M[1], \ldots$. Each processor has its own local registers and knows its own number $i$. The input is in the first cells of the shared memory, and the output is written there. All processors run the same program, but they can branch on $i$, so each can do a different thing.

A global clock drives the machine. In one step, each active processor does three things in order:

1. it reads at most one shared cell,
2. it does one operation on its local registers,
3. it writes at most one shared cell.

All reads of a step happen before all writes of the step, so a value written in step $t$ is first seen in step $t + 1$. A step with a constant number of reads and writes per processor can be split into a constant number of steps of this form, so algorithms often let a processor read two cells in one step.

**The access rules.** The variants say what happens when processors use one cell in one step.

| Variant | Concurrent read | Concurrent write |
|---|---|---|
| [EREW](/erew-pram/) (exclusive read, exclusive write) | not allowed | not allowed |
| [CREW](/crew-pram/) (concurrent read, exclusive write) | allowed | not allowed |
| [CRCW](/crcw-pram/) (concurrent read, concurrent write) | allowed | allowed, with a write rule |

A CRCW PRAM needs a rule for the value that the cell gets. The *common* rule requires all writers to write the same value. Under the *arbitrary* rule one writer succeeds, and the algorithm must be correct for every choice. Under the *priority* rule the writer with the smallest number succeeds. Under a *combining* rule the cell gets the values combined by a fixed operator, such as the sum or the maximum. An algorithm that breaks the rule of its variant is not a legal algorithm for that variant.

**Fortune and Wyllie's P-RAM.** The original P-RAM (Fortune and Wyllie, 1978) allows simultaneous reads, and a simultaneous write to one cell makes the machine halt and reject. So it is a CREW machine. It starts with one processor, and a processor starts a new one with a FORK instruction. Fortune and Wyllie proved that the sets of languages accepted in polynomial time on the P-RAM are exactly [PSPACE](/pspace/). The proof uses the exponential number of processors that FORK can start in polynomial time, so realistic results bound the number of processors by a polynomial in $n$.

**Simulation.** The file `pram_model.py` simulates one step from a list of read sets and write functions, one for each processor. It takes all values from the old memory, checks the read rule, builds the write set of each cell, applies the write rule, and returns a new memory. The tests check each rule on steps with conflicts, check that reads see the old memory (two processors swap two cells in one step), and run an EREW tree sum.

## What it counts

A PRAM algorithm has three measures, all functions of $n$.

- The **time** $T(n)$ is the number of steps.
- The **number of processors** $P(n)$.
- The **work**. Two forms are in use. The *cost* is the product $P(n)\,T(n)$, which counts idle processors too. The *work* $W(n)$ in the work-time framework counts only the operations that are done.

An algorithm is *work-optimal*, or [work-efficient](/work-efficiency/), if its work is $O(T_{\text{seq}}(n))$, where $T_{\text{seq}}(n)$ is the time of the best known serial algorithm on a [RAM](/random-access-machine/). A page must say which serial bound it uses.

**The work-time framework.** JáJá (1992, Section 1.5) describes a PRAM algorithm as a sequence of time units. Each unit is a set of operations that can run at the same time, written with a `pardo` loop, and the algorithm does not say which processor does which operation. If step $k$ has $W_k$ operations, then $W = \sum_k W_k$ and $T$ is the number of steps. The *WT scheduling principle* runs the algorithm on $p$ processors: step $k$ takes $\lceil W_k/p \rceil$ steps, so the total time is

$$T_p \le \sum_{k=1}^{T} \left\lceil \frac{W_k}{p} \right\rceil \le \sum_{k=1}^{T} \left( \left\lfloor \frac{W_k}{p} \right\rfloor + 1 \right) \le \left\lfloor \frac{W}{p} \right\rfloor + T.$$

This is the PRAM form of [Brent's theorem](/brent-theorem/), and it holds if each processor can find out at no cost which operations it does in each step. When the $p$ processors do one step in rounds, the writes of all rounds must wait until the last round, so that each round still reads the old memory. The test file checks that this gives the same memory as one step of the full machine.

**Example: the tree sum.** To add $n$ numbers in cells $A[0..n-1]$, the step with stride $d = 1, 2, 4, \ldots$ lets processor $i$, for each multiple $i$ of $2d$ with $i + d < n$, set $A[i] \leftarrow A[i] + A[i + d]$. After $\lceil \lg n \rceil$ steps, $A[0]$ holds the sum. The work is $n - 1$ additions, and no two processors use one cell in one step, so the algorithm is EREW. On $p = n/\lg n$ processors, the WT principle gives time $O(\lg n)$ and work $O(n)$, which is work-optimal. The tests check the sum, $T = \lceil \lg n \rceil$ and $W = n - 1$ for $n$ from 0 to 69 and some larger values, with the EREW rule checked at each step.

## Relation to other models

- **The RAM.** A PRAM with one processor is a RAM. A PRAM with $p$ processors and time $T$ can be run on a RAM in time $O(pT)$, one processor after another in each step, with the writes of a step held back until the step ends.
- **The work-span model.** The [work-span model](/work-span-model/) keeps the work and the span and leaves out the processors and the memory rules. The work-time framework of the PRAM is close to it: the number of steps $T$ plays the role of the span, and Brent's principle turns both into a time bound. A [fork-join](/fork-join-model/) program does not name processors and does not run in lock step.
- **Circuits.** A PRAM algorithm with polylogarithmic time and a polynomial number of processors is the usual definition of a fast parallel algorithm, and the problems that have one form the class [NC](/nc/) (with care about the word size and the uniformity of the circuits). See also [AC0](/ac0/) and [circuit complexity](/circuit-complexity/).
- **More realistic models.** The PRAM charges nothing for communication and assumes a global clock. The [BSP model](/bsp-model/) of Valiant (1990) adds supersteps, a cost $g$ per word of communication and a cost $L$ for each barrier. Many PRAM algorithms are first designed in the PRAM and then mapped to such a model.

## Known results in the model

- **The order of power.** Each EREW algorithm is a CREW algorithm, each CREW algorithm is a CRCW common algorithm, each common algorithm is correct under the arbitrary rule, and each arbitrary algorithm is correct under the priority rule (proved on [CRCW PRAM](/crcw-pram/)). The tests check, on 3000 random steps, that a step that is legal under one rule gives the same memory under each stronger rule.
- **CRCW is faster than CREW.** A CRCW common PRAM computes the OR of $n$ bits in $O(1)$ time with $n$ processors. Cook, Dwork and Reischuk (1986) proved that a CREW PRAM needs at least $\log_b s(f)$ steps for a Boolean function $f$ of sensitivity $s(f)$, with $b = (5 + \sqrt{21})/2 \approx 4.79$, even with any number of processors. The OR has sensitivity $n$, so it needs $\Omega(\log n)$ steps on a CREW PRAM.
- **The gap is at most logarithmic.** An EREW PRAM with $p$ processors can run one step of a $p$-processor CRCW priority PRAM in $O(\log p)$ steps, by sorting the access requests by address (Vishkin, 1983, with an $O(\log p)$ EREW sort such as Cole's merge sort, 1988; CLRS, first edition, Theorem 30.1). So a CRCW algorithm is at most $O(\log p)$ times faster than the best EREW algorithm with the same number of processors.
- **Basic algorithms.** Sum, [prefix sums](/parallel-prefix/) and [reduction](/parallel-reduction/) take $O(\log n)$ time and $O(n)$ work on an EREW PRAM. [List ranking](/list-ranking/) by [pointer jumping](/pointer-jumping/) takes $O(\log n)$ time and $O(n \log n)$ work, and work-efficient versions take $O(n)$ work. Merging two sorted lists takes $O(\log n)$ time on a CREW PRAM by [ranking](/crew-pram/). Cole (1988) sorts $n$ items in $O(\log n)$ time with $n$ processors on an EREW PRAM.
- **Polynomial time.** Polynomial time on Fortune and Wyllie's P-RAM, with no bound on the number of processors, equals PSPACE.

## References
