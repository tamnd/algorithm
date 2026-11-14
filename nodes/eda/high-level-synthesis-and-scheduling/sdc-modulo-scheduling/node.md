---
tag: 6XQDH6
kind: algorithm
slug: sdc-modulo-scheduling
name: SDC-based modulo scheduling
aliases:
- Zhang-Liu modulo scheduling
area: eda/high-level-synthesis-and-scheduling
level: research
summary: Zhang and Liu's loop pipelining scheduler that adds modulo resource constraints to an SDC formulation and repairs conflicts incrementally for a target initiation interval.
solves: [resource-constrained-scheduling]
model: word-ram
complexity:
  vars: {V: the number of operations, E: the number of dependence edges, I: the number of initiation intervals tried, P: the largest initiation interval tried}
  time: {worst: O(I P V^2 (V + E))}
  space: {extra: O(V + E)}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 2013
  people: [Zhiru Zhang, Bin Liu]
  note: Zhang and Liu gave SDC-based modulo scheduling for pipeline synthesis at ICCAD 2013, and Canis, Brown and Anderson added backtracking and recurrence minimization in the LegUp system at FPL 2014.
prereqs: [sdc-scheduling, software-pipelining]
see_also: [iterative-modulo-scheduling, iteration-bound, ilp-scheduling-formulation, difference-constraints, resource-constrained-scheduling, retiming, dsp-folding]
sources:
  - paper: doi:10.1109/ICCAD.2013.6691121
    title: Zhiru Zhang and Bin Liu, SDC-based modulo scheduling for pipeline synthesis, Proceedings of the IEEE/ACM International Conference on Computer-Aided Design, 211 to 218, 2013
    locator: the dependence and timing constraints across iterations, the modulo reservation table, the incremental scheduling of Algorithm 1 and the accumulator example
  - paper: doi:10.1109/FPL.2014.6927490
    title: Andrew Canis, Stephen D. Brown and Jason H. Anderson, Modulo SDC scheduling with recurrence minimization in high-level synthesis, Proceedings of the International Conference on Field Programmable Logic and Applications, 1 to 8, 2014
    locator: the backtracking modulo SDC scheduler and the restructuring of recurrences in LegUp
  - paper: doi:10.1145/192724.192731
    title: B. Ramakrishna Rau, Iterative modulo scheduling, an algorithm for software pipelining loops, Proceedings of the 27th International Symposium on Microarchitecture, 63 to 74, 1994
    locator: the modulo reservation table, ResMII, RecMII and the iterative search over initiation intervals
---

SDC-based modulo scheduling pipelines a loop in [high-level synthesis](/high-level-synthesis/): it schedules one iteration of the loop body so that a new iteration can start every $II$ cycles, the initiation interval, while the earlier iterations are still running. It combines two older ideas. From compilers it takes the modulo reservation table of [iterative modulo scheduling](/iterative-modulo-scheduling/): with a new iteration every $II$ cycles, an operation that starts at step $t$ uses its unit in slot $t \bmod II$ in the steady state, so each slot may hold at most as many operations of a type as there are units. From [SDC scheduling](/sdc-scheduling/) it takes the system of difference constraints, which now also holds the dependences that cross iterations, as rows $s_v - s_u \ge \ell(u) - II \cdot \mathrm{dist}(u, v)$. Zhang and Liu (2013) place the operations that use limited units one at a time and keep the system feasible after each choice. If an operation finds no free slot, the scheduler raises $II$ and starts again. The result always meets all rules, and it is not always the least $II$.

## In plain words

A loop that runs a million times should not wait for one pass to end before the next one starts. If a new pass starts every two clock ticks, the hardware works on several passes at once, like an assembly line. Two things limit how close the passes can be. A value that one pass hands to the next one, such as a running sum, must be ready in time. And if there is one multiplier, every pass gets it only once per two ticks, so its multiplies must fall on ticks with different remainders. The scheduler writes the first kind of rule as simple differences, places the multiplies one by one into free remainder slots, and checks after each step that all rules can still hold.

## The problem

The input is a loop body: operations $V$ with a latency $\ell(v) \ge 0$ and a type $k(v)$, and dependence edges $(u, v)$ with a distance $\mathrm{dist}(u, v) \ge 0$ in iterations. Edges with distance 0 form a graph with no cycle. Units of a limited type $k$ number $a_k$ and are pipelined: each accepts a new operation every cycle. A modulo schedule for $II$ gives starts $s : V \to \{0, 1, \ldots\}$ with

- $s_v + II \cdot \mathrm{dist}(u, v) \ge s_u + \ell(u)$ for each edge, since iteration $i + \mathrm{dist}$ starts $II \cdot \mathrm{dist}$ cycles after iteration $i$;
- for each limited type $k$ and each residue $r \in \{0, \ldots, II - 1\}$, at most $a_k$ operations of type $k$ have $s_v \equiv r \pmod{II}$.

The goal is the least $II$ that admits a modulo schedule, and then a short schedule for it. Two lower bounds hold (Rau, 1994):
$$\mathrm{ResMII} = \max_k \left\lceil \frac{n_k}{a_k} \right\rceil, \qquad \mathrm{RecMII} = \max_{\text{cycles } c} \left\lceil \frac{\sum_{u \in c} \ell(u)}{\sum_{e \in c} \mathrm{dist}(e)} \right\rceil,$$
where $n_k$ is the number of operations of type $k$ and the sums run over the edges of the cycle $c$ and their tails $u$. This page does not treat the hardness of the exact problem; it solves it only by exhaustive search on small loops.

## The algorithm

```pseudo id=main
SDC-MODULO-SCHEDULE(V, E, ℓ, k, a)
L1  II ← max(ResMII, RecMII)
L2  loop
L3      C ← { s_v − s_u ≥ ℓ(u) − II · dist(u, v) : (u, v) ∈ E }
L4      s ← the least solution of C with s ≥ 0
L5      MRT ← an empty table with II slots per limited type
L6      Q ← the operations of limited types, sorted by (s_v, v)
L7      for each v in Q do
L8          for t ← lo(v) to lo(v) + II − 1, where lo(v) is the least start of v that C allows now, do
L9              if MRT has no free unit of type k(v) in slot t mod II then try the next t
L10             if C with s_v = t added has a solution then
L11                 add s_v = t to C; take a unit in slot t mod II; go to the next v
L12         if no t worked then this II fails; leave the for loop
L13     if this II failed then II ← II + 1 and go back to L3
L14     else return II and the least solution of C
```

Each test on line L10 is a longest path run, as on the [SDC scheduling](/sdc-scheduling/) page: a fixed start is a lower bound and an upper bound on one variable, and the system is feasible exactly when the least solution exists and meets every upper bound. This is a simplified form of Zhang and Liu's Algorithm 1. Their scheduler goes step by step, orders the operations by how many other operations a choice perturbs, and updates the SDC solution incrementally after each change instead of solving it again. The form here orders by the least start and tries one full period of starts.

## Example

Take the accumulator loop `acc = acc * c + x[i] * y[i]` with one pipelined multiplier: $m_1 = \mathrm{acc} \cdot c$ and $m_2 = x_i \cdot y_i$ with latency 2, and $a = m_1 + m_2$ with latency 1. The edges are $m_1 \to a$ and $m_2 \to a$ with distance 0, and $a \to m_1$ with distance 1, since the next iteration multiplies the new sum. So $\mathrm{ResMII} = 2$ and $\mathrm{RecMII} = \lceil (2 + 1)/1 \rceil = 3$.

At $II = 3$ the rows are $s_a - s_{m_1} \ge 2$, $s_a - s_{m_2} \ge 2$ and $s_{m_1} - s_a \ge 1 - 3$, so $s_a = s_{m_1} + 2$ exactly. The least solution is $(0, 0, 2)$, so line L6 orders $m_1$ before $m_2$. Line L11 fixes $m_1$ at 0, in slot 0, which forces $s_a = 2$. For $m_2$, start 0 has a full slot, and starts 1 and 2 would need $s_a \ge 3$. So $II = 3$ fails. At $II = 4$, $m_1$ goes to 0, $m_2$ to 1, and $a$ to 3, a valid schedule.

The least $II$ is 3: the schedule $s_{m_1} = 1$, $s_{m_2} = 0$, $s_a = 3$ uses slots 1 and 0 and meets $s_{m_1} + 3 \ge s_a + 1$. The greedy order fixed $m_1$ at its earliest start, which left no room for $m_2$ before it. Zhang and Liu's perturbation order and Canis, Brown and Anderson's backtracking aim at exactly this kind of loss.

## Correctness

What is proved, in the [full proof](proofs/correctness.md):

- **Lower bounds.** Every modulo schedule has $II \ge \mathrm{ResMII}$, by counting residues, and $II \ge \mathrm{RecMII}$, by adding the rows around a cycle. For $II \ge \mathrm{RecMII}$ the rows of L3 have no positive cycle, so line L4 always succeeds.
- **Valid output.** After each fixing step, the rows of $C$ with the fixed starts still have a solution, and the table never holds more than $a_k$ operations of type $k$ in a slot. The returned schedule meets every edge and every slot limit.
- **Full period of candidates.** The starts of $v$ that keep $C$ feasible form an interval of integers that begins at $lo(v)$. So lines L8 to L11 try one start of every residue that the interval offers, and an operation fails only if no feasible start has a free slot.

What is not proved, and is false: that the returned $II$ is the least. The example loses one cycle. In a measured run of the tests, with 150 random loops of at most 5 operations, one unit per limited type and up to two recurrence edges, the scheduler returned an $II$ above the exhaustive optimum on 2 of them. On all 150 the exhaustive optimum equalled $\max(\mathrm{ResMII}, \mathrm{RecMII})$. These are measurements on small random loops, not bounds. The proof also does not show that the outer loop always ends with a schedule; the implementation stops at a cap on $II$, and it never reached the cap in the tests.

## Complexity

RecMII comes from at most $1 + \sum_v \ell(v)$ longest path runs, or from a binary search over $II$, since a positive cycle at some $II$ stays positive at every smaller $II$. For one $II$, line L10 runs at most $II$ times for each of at most $V$ operations, and each run is Bellman-Ford in $O(V (V + E))$ time. So one $II$ costs $O(II \cdot V^2 (V + E))$, and $I$ values of $II$, each at most $P$, cost $O(I P V^2 (V + E))$. Space is $O(V + E)$ for the rows and the table, plus $O(II)$ slots per limited type. An incremental longest path update, as Zhang and Liu use, lowers the cost of each test on line L10 in practice.

## Properties

- **Always valid.** The schedule meets every dependence across iterations and every slot limit.
- **Not exact.** The $II$ may exceed the least one.
- **Global timing view.** Unlike a list scheduler with a reservation table, every fixing step keeps the whole system of timing rules feasible, so a choice never silently breaks a recurrence that is placed later.
- **Extensible.** Any rule that is a difference of starts, such as the cross-iteration chaining rows of Zhang and Liu, joins $C$ without a change to the method.
- **Deterministic.** The order of line L6 and the scan of line L8 are fixed.

## Variants and improvements

- **Perturbation order.** Zhang and Liu order the operations by the number of other operations whose least start a choice moves, with ties broken by ALAP and ASAP starts.
- **Backtracking.** Canis, Brown and Anderson (2014) let a blocked operation evict a placed one, as Rau's iterative modulo scheduler does, with a budget on the number of steps before $II$ grows. They also rewrite associative recurrences to shorten them before scheduling.
- **Chaining across iterations.** With a clock period, a combinational path may cross from one iteration into the next. The pair rule of [SDC scheduling](/sdc-scheduling/) then compares $s_v + II \cdot \mathrm{dist}$ with $s_u$, which is still a difference of two starts.
- **Register pressure.** After the slots are fixed, an LP over the same rows can minimize a weighted sum of value lifetimes. The matrix keeps the form of the SDC page, so the LP has an integral optimum.
- **Exact search.** For small loops, the residues of the limited operations can be enumerated. For fixed residues $r$, writing $s_v = r_v + II \cdot q_v$ turns the rows into difference constraints on the integers $q_v$, so feasibility is one longest path run. The tests use this as the reference.
- **Non-pipelined units.** A unit busy for $d$ cycles takes $d$ consecutive slots modulo $II$ in the table.

## When to use it

Use it to pipeline inner loops in HLS when the throughput target is a small $II$ and the body has many timing rules, such as a clock period with chaining or fixed interface delays. When the body is small, an exact search or an [integer program](/ilp-scheduling-formulation/) gives the least $II$. For signal processing graphs with no control flow, [retiming](/retiming/) and [folding](/dsp-folding/) give the classic alternative.

## Pitfalls

- **Not exact.** Do not report the returned $II$ as the least one, unless it equals $\max(\mathrm{ResMII}, \mathrm{RecMII})$.
- **Distance 0 cycles.** A cycle of edges with distance 0 has no schedule for any $II$. Check the input before computing RecMII.
- **Residues of negative starts.** If starts may be negative, use a residue in $\{0, \ldots, II - 1\}$, not the remainder that some languages give for negative numbers.
- **Prologue and epilogue.** The schedule of one iteration is not the whole design. The controller must also run the first and last iterations, where the pipeline fills and drains.
- **Memory ports.** Loads and stores to one memory bank compete for its ports exactly like units. Leaving them out of the table gives schedules that the memory cannot serve.

## Implementations

## History

Rau (1994) gave iterative modulo scheduling for compilers, with the modulo reservation table, the bounds ResMII and RecMII, and an outer loop over $II$. Cong and Zhang (2006) had shown that most HLS scheduling rules fit a system of difference constraints. Zhang and Liu (2013) combined the two for pipeline synthesis, with rules that cross iterations and an incremental repair when a slot is full. Canis, Brown and Anderson (2014) added backtracking in the LegUp system.

## References
