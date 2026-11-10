---
tag: 94DN1Q
kind: model
slug: crcw-pram
name: CRCW PRAM
aliases:
- concurrent-read concurrent-write PRAM
- CRCW
area: parallel/work-span-models
level: core
summary: The PRAM where many processors may read and write a cell in a step, under a write rule (common, arbitrary, priority or combining). It computes OR in O(1), and the maximum in O(1) with n^2 processors.
prereqs: [pram-model, crew-pram]
see_also: [pram-model, erew-pram, crew-pram, bitonic-sort, sorting-network, parallel-reduction, ac0, nc]
sources:
  - book: isbn:9780262031417
    title: Thomas H. Cormen, Charles E. Leiserson and Ronald L. Rivest, Introduction to Algorithms, first edition, MIT Press, 1990
    locator: Chapter 30, Section 30.2 (CRCW versus EREW, the write rules, the maximum in O(1) time with n^2 processors, and Theorem 30.1 on the simulation of a CRCW algorithm on an EREW PRAM)
  - book: isbn:9780201548563
    title: Joseph JaJa, An Introduction to Parallel Algorithms, Addison-Wesley, 1992
    locator: Chapter 1 (the PRAM variants and the rules for concurrent writes)
  - paper: doi:10.1016/0196-6774(83)90033-0
    title: "Uzi Vishkin, Implementation of simultaneous memory address access in models that forbid it, Journal of Algorithms 4(1), 1983"
    locator: pp. 45-50, the simulation of a step with concurrent reads and writes by sorting the requests
  - paper: doi:10.1137/0217049
    title: Richard Cole, Parallel merge sort, SIAM Journal on Computing 17(4), 1988
    locator: sorting n items in O(log n) time with n processors on the EREW PRAM
  - paper: "Stephen Cook, Cynthia Dwork and Ruediger Reischuk, Upper and lower time bounds for parallel random access machines without simultaneous writes, SIAM Journal on Computing 15(1), 1986"
    locator: pp. 87-97, the Omega(log n) lower bound for the OR on PRAMs without simultaneous writes
  - paper: doi:10.1145/65950.65958
    title: Paul Beame and Johan Håstad, Optimal bounds for decision problems on the CRCW PRAM, Journal of the ACM 36(3), 1989
    locator: pp. 643-670, the Omega(log n / log log n) time lower bound for parity with a polynomial number of processors
  - paper: "Yossi Shiloach and Uzi Vishkin, Finding the maximum, merging, and sorting in a parallel computation model, Journal of Algorithms 2(1), 1981"
    locator: pp. 88-102, the maximum in O(log log n) time on a CRCW PRAM (to be checked)
---

The CRCW PRAM (concurrent read, concurrent write) is the [PRAM](/pram-model/) in which any number of processors may read one cell and any number may write one cell in the same step. A *write rule* says which value the cell gets: the *common* rule requires all writers to write the same value, the *arbitrary* rule lets one unknown writer succeed, the *priority* rule lets the writer with the smallest number succeed, and a *combining* rule combines the values with a fixed operator. With these rules the OR of $n$ bits takes one step, and the maximum of $n$ numbers takes $O(1)$ steps with $n^2$ processors, while a [CREW PRAM](/crew-pram/) needs $\Omega(\log n)$ steps for both. An [EREW PRAM](/erew-pram/) can still run each CRCW step in $O(\log p)$ steps, so the gain is at most logarithmic.

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

The machine is the synchronous PRAM of the [PRAM model](/pram-model/) page. All reads of a step see the memory as it was before the step, and then all writes happen. Concurrent reads of a cell are always allowed. When the processors in a set $Q$ with $|Q| \ge 2$ write the values $v_i$ ($i \in Q$) to one cell in one step, the rule fixes the result.

| Rule | Condition on the step | Value of the cell |
|---|---|---|
| common | all $v_i$ are equal | that value |
| arbitrary | none | $v_i$ for some $i \in Q$; the algorithm must be correct for every choice |
| priority | none | $v_i$ for the smallest $i \in Q$ |
| combining with operator $\oplus$ | none | $v_{i_1} \oplus v_{i_2} \oplus \cdots$ over $Q$ in order, for example the sum or the maximum |

A step that breaks the condition of the common rule is illegal, and so is an algorithm that can make such a step on some input.

**Simulation.** The file `crcw_pram.py` runs one step from the read set and the write function of each processor. It groups the writes by cell, applies the rule, and raises an error when a common write has two values, or when a concurrent read or write appears under the EREW or CREW rule. The arbitrary rule takes a function that picks the winner, and the tests pass a seeded random choice.

## What it counts

The measures are those of every PRAM: the time $T(n)$, the number of processors $P(n)$, and the work, either as the cost $P(n)\,T(n)$ or as the number of operations $W(n)$ (JáJá, Section 1.5). The CRCW PRAM often trades processors for time: the maximum below takes $O(1)$ time but $\Theta(n^2)$ work, while the serial maximum takes $n - 1$ comparisons. A page about a CRCW algorithm must name the write rule, because an algorithm for one rule may be illegal or wrong under a weaker one.

## Relation to other models

**Theorem 1 (order of power).** Let a step be legal under a rule in the chain EREW, CREW, common, arbitrary, priority. Then it is legal under each later rule in the chain. If it is legal under EREW, CREW or common, it gives the same memory under each later rule. If it is legal under arbitrary, the memory under priority is one of the memories that the arbitrary rule allows. A combining rule with the operator $(i, v) \oplus (j, w) = $ the pair with the smaller first part, applied to pairs (processor number, value), gives the result of the priority rule.

*Proof.* EREW to CREW: the CREW rule drops one condition and changes no value. CREW to common: in a CREW step each cell has at most one writer, so the condition of the common rule holds, and the cell gets the one value. Common to arbitrary: the arbitrary rule has no condition, and if all writers of a cell write one value $v$, every choice gives $v$. Arbitrary to priority: the priority rule is one choice of a winner, the smallest number. Priority to combining: in each cell the operator keeps the pair with the smallest processor number, which is the priority winner. $\blacksquare$

So an algorithm for a weaker rule runs unchanged, in the same time and with the same processors, under each stronger rule, and the results that this page proves for the common rule hold for all of them. The tests check Theorem 1 on 3000 random steps (on the [PRAM model](/pram-model/) page) and run the maximum below under the common, arbitrary and priority rules.

**The gap to CREW.** The OR in one step (Theorem 3) and the lower bound of Cook, Dwork and Reischuk (1986) for PRAMs without simultaneous writes, which gives $\Omega(\log n)$ steps for the OR, show that the CRCW PRAM with the common rule is strictly stronger than the CREW PRAM.

**Theorem 2 (simulation on EREW).** A $p$-processor EREW PRAM can run one step of a $p$-processor CRCW priority PRAM in $O(\log p)$ steps, with $O(p)$ extra cells (Vishkin, 1983; CLRS, first edition, Theorem 30.1). So a CRCW algorithm with $p$ processors is at most $O(\log p)$ times faster than the best EREW algorithm with $p$ processors.

*Proof of the write part.* Processor $i$ writes the key $(a_i, i, v_i)$ for its request into cell $R[i]$, or a key larger than all others if it has no request. The processors sort $R$ by $(a, i)$ with an EREW sort that takes $O(\log p)$ steps, such as Cole's merge sort (1988). Then processor $k$ copies $R[k - 1]$ into its own cell $L[k]$, and in the next step it reads $R[k]$ and $L[k]$. If $R[k]$ is a real request and its address differs from the address in $L[k]$, then $R[k]$ is the first request in its group of equal addresses, which is the one with the smallest processor number, and processor $k$ writes its value to that address. Each address gets exactly one writer, so the writes are exclusive, and each cell gets the priority value. Every step reads and writes cells that belong to one processor or that the sort uses exclusively, so every step is EREW. $\blacksquare$

The read part sorts the read requests by address in the same way. The first request of each group reads the cell, a segmented copy spreads the value to the rest of its group in $O(\log p)$ doubling steps (in the step with stride $d$, position $k$ reads only position $k - d$, so the reads are exclusive), and position $k$ writes the value into a cell that belongs to the requesting processor.

The test file runs the write part with Batcher's [bitonic sorting network](/bitonic-sort/) in place of Cole's sort. Each comparator is a processor that reads two cells and writes them back in order, and the comparators of one stage use disjoint cells, so each stage is one EREW step. The network has $k(k + 1)/2$ stages for $q = 2^k \ge p$ wires, so this version takes $O(\log^2 p)$ steps. The tests check, for $p$ from 0 to 33 and for 64 and 100, that the result equals one priority step of the CRCW simulator, that the number of steps is $1 + k(k + 1)/2 + 2$, and that each step has at most one reader and one writer for each cell.

**Circuits.** The CRCW PRAM with a polynomial number of processors and constant time is close to the class [AC0](/ac0/) of constant-depth circuits of unbounded fan-in: the OR in one step is an OR gate of fan-in $n$. Like AC0, it cannot compute parity in constant time (Theorem 5).

## Known results in the model

**Theorem 3 (OR in one step).** With the common rule and $n$ processors, the OR of bits $A[0..n-1]$ takes one step: processor $i$ reads $A[i]$ and, if it is 1, writes 1 to a cell $r$ that holds 0 at the start.

*Proof.* If some bit is 1, the cell $r$ has at least one writer, all writers write 1, so the common rule holds and $r = 1$. If all bits are 0, no processor writes, and $r$ keeps the value 0. $\blacksquare$

The same step under the CREW rule is illegal as soon as two bits are 1. The tests check the value, one step and $n$ operations on many sizes and densities.

**Theorem 4 (maximum in constant time).** With the common rule and $n^2$ processors, the maximum of $A[0..n-1]$, with the smallest index among the positions that hold it, takes three steps:

1. processor $i$ sets $M[i] \leftarrow 1$;
2. processor $(i, j)$, for $i \ne j$, reads $A[i]$ and $A[j]$, and sets $M[i] \leftarrow 0$ if $A[j]$ beats $A[i]$, that is, if $A[j] > A[i]$, or $A[j] = A[i]$ and $j < i$;
3. processor $i$ reads $M[i]$, and if it is 1, writes $A[i]$ to the cell *max* and $i$ to the cell *arg*.

*Proof.* "Beats" compares the pairs $(A[i], -i)$ in lexicographic order, which is a strict total order on the $n$ positions, so it has a unique largest position $i^*$: the smallest index that holds the maximum value. In step 2 all writers of a cell write 0, so the common rule holds. After step 2, $M[i] = 0$ if and only if some $j$ beats $i$, so $M[i] = 1$ only for $i^*$. In step 3 only processor $i^*$ writes, so the writes are exclusive, and the cells hold $A[i^*]$ and $i^*$. $\blacksquare$

The algorithm has $3$ steps and $n + n(n - 1) + n$ operations, so it is not work-efficient. It needs both concurrent rules: in step 2 each $A[i]$ is read by $2(n - 1)$ processors, and the smallest item is set to 0 by $n - 1$ processors. The tests check the value and the index on sizes 0 to 32 and 50 with many ties and with few, under the common, arbitrary and priority rules, and check that the EREW rule rejects it for $n \ge 2$ and the CREW rule for $n \ge 3$ with distinct values. Without the tie-break on the index, all positions that hold the maximum write the same value in step 3, which the common rule allows. With fewer processors, the maximum takes $O(\log \log n)$ time with $n$ processors on a CRCW PRAM (Shiloach and Vishkin, 1981).

**The priority rule in one step.** With the priority rule, the position of the first 1 in $A[0..n-1]$ takes one step: each processor $i$ with $A[i] = 1$ writes $i$ to one cell. Under the arbitrary rule the same step gives some position of a 1, and under the common rule it is illegal when two bits are 1. The tests check all three.

**The combining rule.** With the sum as the operator, the sum of $n$ numbers takes one step with $n$ processors: each processor writes its number to one cell. With the maximum as the operator, so does the maximum.

**Theorem 5 (parity is not constant time).** Beame and Håstad (1989) proved that a CRCW PRAM with a polynomial number of processors needs $\Omega(\log n / \log \log n)$ steps to compute the parity of $n$ bits, and that this is optimal. The proof is not given here. A combining PRAM with the sum operator computes the parity in $O(1)$ steps, because it gets the sum of the bits in one step, so such a combining rule lies outside the reach of that bound.

## References
