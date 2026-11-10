---
tag: Z1W3PV
kind: model
slug: erew-pram
name: EREW PRAM
aliases:
- exclusive-read exclusive-write PRAM
- EREW
area: parallel/work-span-models
level: core
summary: The weakest standard PRAM, where no two processors may read or write one cell in one step. Doubling copies a value to p cells in O(log p) steps, and every EREW method needs log_4 p steps.
prereqs: [pram-model]
see_also: [pram-model, crew-pram, crcw-pram, parallel-reduction, parallel-prefix, pointer-jumping, aks-sorting-network, work-efficiency]
sources:
  - book: isbn:9780201548563
    title: Joseph JaJa, An Introduction to Parallel Algorithms, Addison-Wesley, 1992
    locator: Chapter 1 (the PRAM variants, and Section 1.5, the work-time framework) and Chapter 2 (balanced trees, the sum and prefix sums on the EREW PRAM)
  - book: isbn:9780262031417
    title: Thomas H. Cormen, Charles E. Leiserson and Ronald L. Rivest, Introduction to Algorithms, first edition, MIT Press, 1990
    locator: Chapter 30, Section 30.1 (pointer jumping and list ranking on the EREW PRAM) and Section 30.2 (CRCW versus EREW, with Theorem 30.1)
  - paper: doi:10.1016/0196-6774(83)90033-0
    title: "Uzi Vishkin, Implementation of simultaneous memory address access in models that forbid it, Journal of Algorithms 4(1), 1983"
    locator: pp. 45-50, the simulation of concurrent reads and writes on a PRAM that forbids them
  - paper: doi:10.1137/0217049
    title: Richard Cole, Parallel merge sort, SIAM Journal on Computing 17(4), 1988
    locator: sorting n items in O(log n) time with n processors on the EREW PRAM
  - paper: "Stephen Cook, Cynthia Dwork and Ruediger Reischuk, Upper and lower time bounds for parallel random access machines without simultaneous writes, SIAM Journal on Computing 15(1), 1986"
    locator: pp. 87-97, the lower bound for PRAMs without simultaneous writes, which also holds for the EREW PRAM
---

The EREW PRAM (exclusive read, exclusive write) is the [PRAM](/pram-model/) in which no memory cell may be read by two processors in the same step, and no cell may be written by two processors in the same step. It is the weakest of the three standard variants and the closest to a machine whose memory banks serve one request at a time. A value that all $p$ processors need must be copied, and copying by doubling takes $1 + \lceil \lg p \rceil$ steps. This page proves that no EREW algorithm can do it in fewer than $\log_4 p$ steps.

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

The machine is the synchronous PRAM of the [PRAM model](/pram-model/) page: $p$ processors, a shared memory, and steps in which each processor reads, computes and writes. All reads of a step see the memory as it was before the step. The EREW rule is a condition on each step:

- for each cell, at most one processor reads it in the step, and
- for each cell, at most one processor writes it in the step.

A processor may read a cell that another processor writes in the same step, because the read happens first. An algorithm is an EREW algorithm only if the rule holds in every step on every input. When an algorithm lets a processor read two cells in one step, the rule applies to each of the two reads, and the step can be split into two steps of one read each.

**Simulation.** The file `erew_pram.py` runs a step from the read set and the write function of each processor. It records, for each cell, the set of processors that read it and the set that write it, and it raises an error if a set has two members. The tests check the rule at every step of the algorithms below.

## What it counts

The measures are those of every PRAM: the time $T(n)$ in steps, the number of processors $P(n)$, and the work, either as the cost $P(n)\,T(n)$ or as the number of operations $W(n)$ in the work-time framework (JáJá, Section 1.5). A work-efficient EREW algorithm has work $O(T_{\text{seq}}(n))$, where $T_{\text{seq}}(n)$ is the time of the best serial algorithm on a [RAM](/random-access-machine/).

On an EREW PRAM, the cost of sharing is visible in the time. If $k$ processors need one value, the value must first be copied into $k$ cells, and that takes $\Omega(\log k)$ steps (Theorem 1 below). On a [CREW PRAM](/crew-pram/) the $k$ processors read the one cell in one step.

**Broadcast by doubling.** To copy the value in cell $x$ to cells $B[0], \ldots, B[p - 1]$:

1. In step 0, processor 0 reads $x$ and writes $B[0]$.
2. In the step with $d = 1, 2, 4, \ldots$ while $d < p$, each processor $i$ with $d \le i < \min(2d, p)$ reads $B[i - d]$ and writes $B[i]$.

Before the step with stride $d$, the cells $B[0..d-1]$ hold the value; the step fills $B[d..2d-1]$. In one step the processors read the distinct cells $B[i - d]$ and write the distinct cells $B[i]$, so the step is EREW. The algorithm takes $1 + \lceil \lg p \rceil$ steps for $p \ge 1$ and does $p$ operations. The tests check the copies, the number of steps and the EREW rule for $p$ from 0 to 69 and for 127, 128, 129 and 1000. They also check that the one-step broadcast, in which all processors read $x$ at once, breaks the EREW rule and is legal on a CREW PRAM.

**The tree sum.** In the step with stride $d$, processor $i$, for each multiple $i$ of $2d$ with $i + d < n$, sets $A[i] \leftarrow A[i] + A[i + d]$. The cells that two processors use are disjoint, so the step is EREW. After $\lceil \lg n \rceil$ steps, $A[0]$ is the sum; the work is $n - 1$. With $n/\lg n$ processors and the WT scheduling principle, the time is $O(\log n)$ and the work is $O(n)$ (see [parallel reduction](/parallel-reduction/)).

## Relation to other models

- **The other PRAMs.** Every EREW algorithm is a [CREW](/crew-pram/) algorithm and a [CRCW](/crcw-pram/) algorithm with any write rule, because a step with no conflicts is legal under every rule and gives the same memory. So the EREW PRAM is the weakest of the three.
- **Simulating the stronger PRAMs.** A $p$-processor EREW PRAM runs one step of a $p$-processor CRCW priority PRAM in $O(\log p)$ steps, by sorting the read and write requests by address with an $O(\log p)$ EREW sort and then letting one processor in each group of equal addresses act for the group (Vishkin, 1983; CLRS, first edition, Theorem 30.1). The [CRCW PRAM](/crcw-pram/) page gives this simulation. So the EREW PRAM is at most a factor $O(\log p)$ slower than the strongest PRAM with the same number of processors.
- **Networks and circuits.** A [sorting network](/sorting-network/) or a circuit of depth $d$ in which each wire goes to a constant number of gates is close to an EREW algorithm: each comparator or gate is a processor, and the cells it uses in one level are its own. The [AKS sorting network](/aks-sorting-network/) has depth $O(\log n)$, so it gives an EREW sort in $O(\log n)$ time with $O(n)$ processors.

## Known results in the model

**Theorem 1 (broadcast needs logarithmic time).** Let an EREW PRAM, with any number of processors, start with a value $x \in \{0, 1\}$ in one cell, with all other cells and all processors in a state that does not depend on $x$. If after $t$ steps the contents of $p$ given cells depend on $x$ (for example, all of them equal $x$), then $t \ge \log_4 p = \tfrac{1}{2}\lg p$.

*Proof.* Compare the run with $x = 0$ and the run with $x = 1$. After step $t$, call a cell *affected* if its contents differ between the two runs, and call a processor *affected* if its state differs. Let $C_t$ and $K_t$ be the numbers of affected cells and processors after step $t$. Then $C_0 = 1$ and $K_0 = 0$.

Consider step $t + 1$. A processor that is not affected after step $t$ has the same state in both runs, so it reads the same cell in both runs. It becomes affected only if that cell is affected. By the EREW rule, in the run with $x = 0$ each cell is read by at most one processor, so at most $C_t$ unaffected processors read an affected cell. Hence $K_{t+1} \le K_t + C_t$.

A cell is affected after step $t + 1$ only if it was affected before, or if in at least one of the two runs it is written in step $t + 1$ by an affected processor. If neither holds, then either no processor writes it in either run, so it keeps its old equal contents, or its writers in both runs are unaffected. Unaffected processors make the same writes in both runs, and by the EREW rule a cell has at most one writer, so the cell gets the same value in both runs. Each affected processor writes at most one cell in each run, so at most $2K_{t+1}$ cells are written by affected processors. Hence

$$C_{t+1} \le C_t + 2K_{t+1} \le C_t + 2K_t + 2C_t.$$

Adding the two bounds gives $K_{t+1} + C_{t+1} \le 3K_t + 4C_t \le 4(K_t + C_t)$, so $C_t \le K_t + C_t \le 4^t$. The $p$ given cells are affected after $t$ steps, so $p \le 4^t$, that is, $t \ge \log_4 p$. $\blacksquare$

The proof uses the exclusive reads in one place: one affected cell can affect at most one more processor per step. On a CREW PRAM one affected cell can affect all processors in one step, and a broadcast takes $O(1)$ steps. So the bound separates the EREW and CREW PRAMs for broadcast. Doubling takes $1 + \lceil \lg p \rceil$ steps, so the bound is tight within a factor of about 2. In the simulator the processors keep no state between steps, so there the bound is $C_{t+1} \le C_t + 2K_{t+1}$ with $K_{t+1} \le C_t$. The tests check both inequalities and $C_t \le 4^t$ on 400 random EREW programs.

**Other results.**

- **Sum, reduction and prefix sums.** $O(\log n)$ time and $O(n)$ work, by balanced trees (JáJá, Chapter 2; see [parallel reduction](/parallel-reduction/) and [parallel prefix](/parallel-prefix/)).
- **List ranking.** [Pointer jumping](/pointer-jumping/) ranks a list of $n$ items in $O(\log n)$ steps with $n$ processors on an EREW PRAM (CLRS, first edition, Section 30.1). The reads in one step are of distinct cells because each item of a list has at most one predecessor. Its work is $O(n \log n)$, and work-efficient versions do $O(n)$ work (see [list ranking](/list-ranking/)).
- **Sorting.** Cole (1988) sorts $n$ items in $O(\log n)$ time with $n$ processors on an EREW PRAM. This sort is also the tool for the $O(\log p)$ simulation of concurrent access.
- **OR and other sensitive functions.** The lower bound of Cook, Dwork and Reischuk (1986) for PRAMs without simultaneous writes holds for the EREW PRAM, so the OR of $n$ bits needs $\Omega(\log n)$ steps. A tree computes it in $\lceil \lg n \rceil$ steps.

## References
