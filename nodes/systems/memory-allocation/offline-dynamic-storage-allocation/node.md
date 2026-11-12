---
tag: CVDZH6
kind: problem
slug: offline-dynamic-storage-allocation
name: Offline dynamic storage allocation
aliases:
- offline DSA
- Garey-Johnson SR2
area: systems/memory-allocation
level: research
summary: "Given each block's size and lifetime in advance, give the blocks fixed addresses so that blocks live at the same time do not overlap, with the least total memory. NP-hard."
prereqs: [online-memory-allocation, np-hard, approximation-ratio]
see_also: [robson-bound, strip-packing, bin-packing, interval-coloring-depth-theorem, online-graph-coloring-problem, maximum-overlap, strong-np-hardness, first-fit-allocation]
sources:
  - book: isbn:9780716710455
    title: Michael R. Garey and David S. Johnson, Computers and Intractability, A Guide to the Theory of NP-Completeness, W. H. Freeman, 1979
    locator: Appendix A4.1, problem SR2, Dynamic Storage Allocation
  - paper: doi:10.1137/S0097539703423941
    title: "Adam L. Buchsbaum, Howard Karloff, Claire Kenyon, Nick Reingold and Mikkel Thorup, OPT versus LOAD in dynamic storage allocation, SIAM Journal on Computing 33(3) (2004), 632-646"
    locator: Section 1 (the problem as rectangles that slide vertically, the history of ratios 80, 6, 5 and 3), the main theorem OPT = LOAD + O((h_max/LOAD)^(1/7)) LOAD, the (2 + epsilon)-approximation and the lower-bound family
  - paper: doi:10.1145/780542.780624
    title: "Adam L. Buchsbaum, Howard Karloff, Claire Kenyon, Nick Reingold and Mikkel Thorup, OPT versus LOAD in dynamic storage allocation, STOC 2003"
    locator: the conference version of the same results
  - paper: doi:10.1137/0401048
    title: "H. A. Kierstead, The linearity of first-fit coloring of interval graphs, SIAM Journal on Discrete Mathematics 1(4) (1988), 526-530"
    locator: the abstract and main theorem (First Fit uses at most 40 omega colors on interval graphs) and the corollary (ratio 80 for the algorithm of Chrobak and Slusarek)
  - paper: doi:10.1007/3-540-61680-2_46
    title: "Jordan Gergov, Approximation algorithms for dynamic storage allocation, ESA 1996, LNCS 1136, 52-61"
    locator: the 5-approximation
---

Offline dynamic storage allocation (DSA) is the [memory allocation](/online-memory-allocation/) problem when the whole request sequence is known in advance. Each block has a size and a lifetime, and each block gets one fixed address, so that two blocks that are live at the same time do not overlap. The aim is to use as little memory as possible. The problem is NP-hard, and it is problem SR2 in Garey and Johnson. The best known polynomial algorithm comes within a factor $2 + \varepsilon$ of the optimum (Buchsbaum, Karloff, Kenyon, Reingold and Thorup, 2003).

## In plain words

A hotel has one long corridor of rooms. Every group of guests has a fixed arrival day, a fixed departure day and a size, and a group must get a run of adjacent rooms for its whole stay. You know all the bookings before the season starts. The question is how few rooms the hotel needs.

There is an easy lower limit: count the guests on the busiest day. The hotel can never need fewer rooms than that. But a good plan may still need more, because the runs of free rooms on a day can be in the wrong places. Finding the true best plan is hard, but you can always come within about twice the easy lower limit.

## Definition

**Input.** Items $1, \dots, k$. Item $i$ has a lifetime $[a_i, d_i)$ with integers $a_i < d_i$, and a size $h_i \ge 1$. Items $i$ and $j$ conflict if their lifetimes meet: $a_i < d_j$ and $a_j < d_i$.

**Output.** An offset $x_i \ge 0$ for each item, such that for every conflicting pair the address ranges $[x_i, x_i + h_i)$ and $[x_j, x_j + h_j)$ are disjoint.

**Objective.** Minimize $\mathrm{OPT} = \max_i (x_i + h_i)$.

**Load.** Let
$$\mathrm{LOAD} = \max_t \sum_{i \,:\, a_i \le t < d_i} h_i,$$
the most memory that is live at one time. Every solution has $\max_i (x_i + h_i) \ge \mathrm{LOAD}$, because the items live at the busiest time need disjoint ranges.

**Geometric form.** Draw item $i$ as a rectangle of width $d_i - a_i$ and height $h_i$, fixed in its horizontal position. The task is to slide each rectangle only vertically, so that no two overlap, and to keep the top as low as possible. This is the form used by Buchsbaum et al. It differs from [strip packing](/strip-packing/), where the rectangles may also move sideways.

## Variants

- **Decision version (SR2).** Given the items and a bound $D$, is there a solution with $\max_i (x_i + h_i) \le D$? Garey and Johnson list it as NP-complete in the strong sense, by a reduction from 3-partition. So there is no pseudo-polynomial algorithm unless P = NP; see [strong NP-hardness](/strong-np-hardness/).
- **Unit sizes.** If every $h_i = 1$, the problem is coloring of an interval graph, and the optimum equals LOAD. First fit by start time reaches it; see the [interval coloring depth theorem](/interval-coloring-depth-theorem/).
- **Online.** The requests arrive in time order and must be answered at once. This is [online memory allocation](/online-memory-allocation/), where the worst case grows like $\log$ of the largest size; see [Robson's bound](/robson-bound/).
- **Relaxed objectives.** Some work bounds OPT by LOAD plus a term in the largest size $h_{\max}$, as in the main theorem of Buchsbaum et al.

## Examples

**A first-fit trap.** Items $(a, d, h)$ are $(0, 5, 1)$, $(1, 9, 1)$, $(2, 5, 1)$, $(3, 9, 1)$ and $(6, 9, 2)$. LOAD is 4: four unit items are live at time 3, and at time 6 the two long unit items and the item of size 2 are live.

| Method | Offsets of the five items | Memory used |
|---|---|---|
| First fit by start time | 0, 1, 2, 3, 4 | 6 |
| Optimum | 2, 0, 3, 1, 2 | 4 |

First fit puts the long items at 1 and 3, so at time 6 the free words 0 and 2 are not adjacent, and the item of size 2 must go to 4. The optimum puts the two long items at the bottom and the two short ones above them, so their space joins into one hole of size 2. Here OPT = LOAD = 4.

**OPT can be above LOAD.** Small random instances almost always have OPT = LOAD, but Buchsbaum et al. give a family of instances with $\mathrm{OPT} \ge \mathrm{LOAD} + c\,(h_{\max}/\mathrm{LOAD})^{1/2 + \varepsilon}\,\mathrm{LOAD}$, so LOAD is not always reachable.

**First fit can be far from OPT.** First fit by start time places the items exactly as online first fit would. Robson's sequences for first fit force about $M \log_2 n$ memory with $\mathrm{LOAD} \le M$, while OPT stays within a constant factor of LOAD. So first fit by start time has no constant ratio.

## Known algorithms

- **First fit by start time.** Process items in order of $a_i$ and give each the lowest offset that is free among the conflicting items placed so far. Fast and simple, but not a constant-factor approximation in general.
- **Chrobak and Slusarek, with Kierstead's analysis (1988).** Kierstead proved that First Fit colors an interval graph with at most $40\omega$ colors, where $\omega$ is the clique size. It follows that a polynomial-time algorithm of Chrobak and Slusarek for DSA has ratio at most 80. The coloring bound itself was later improved, and that history is on the page of the [online graph coloring problem](/online-graph-coloring-problem/).
- **Kierstead (1991), algorithm WIC.** It uses an online algorithm for coloring interval graphs to build a polynomial-time approximation with ratio at most 6 (Discrete Mathematics 88, 231-237). Slusarek found a ratio of 6 independently, in the account of Buchsbaum et al.
- **Gergov (1996).** A 5-approximation, at ESA 1996.
- **Gergov (1999).** An $O(n \log n)$ algorithm that returns a solution of size at most $3 \cdot \mathrm{LOAD}$, so a 3-approximation (SODA 1999).
- **Buchsbaum, Karloff, Kenyon, Reingold and Thorup (2003, 2004).** A polynomial-time $(2 + \varepsilon)$-approximation for every fixed $\varepsilon > 0$. This is the best known ratio.
- **Exact search.** Some optimal solution places the items in some order, each at its lowest free offset: take an optimal solution, place its items in order of offset, and no item rises. So trying all $k!$ orders finds the optimum. The implementation does this for small $k$.

## Bounds

- **Lower bound for every solution.** $\mathrm{OPT} \ge \mathrm{LOAD}$.
- **Upper bounds on OPT in terms of LOAD.** Gergov's algorithm shows $\mathrm{OPT} \le 3 \cdot \mathrm{LOAD}$ for every instance. Buchsbaum et al. show $\mathrm{OPT} = \mathrm{LOAD} + O\big((h_{\max}/\mathrm{LOAD})^{1/7}\big)\,\mathrm{LOAD}$, so OPT is close to LOAD when every item is small compared with LOAD.
- **Lower bounds on OPT in terms of LOAD.** There are instances with $\mathrm{OPT} \ge \mathrm{LOAD} + c\,(h_{\max}/\mathrm{LOAD})^{1/2 + \varepsilon}\,\mathrm{LOAD}$ (Buchsbaum et al.).
- **Approximation.** The best known ratio is $2 + \varepsilon$. The problem is strongly NP-hard, so there is no fully polynomial-time approximation scheme unless P = NP. The sources cited here give no polynomial-time algorithm with a ratio below 2.

## Reductions

- **From 3-partition.** The strong NP-completeness of SR2 comes from 3-partition, in Garey and Johnson.
- **To interval coloring.** With unit sizes the problem is coloring an interval graph by the address of each item, which first fit by start time solves exactly.
- **From online allocation.** Every online allocator gives a solution of the offline problem on the same items, so the offline OPT is at most the online worst case. The offline problem is easier: OPT is within a factor 3 of LOAD, while online allocators can be forced to $\Theta(\log n)$ times LOAD.

## Applications

- Planning buffers for deep learning on a GPU, where the lifetime of every tensor is known from the graph before it runs.
- Register and stack-slot allocation in compilers when values have different sizes.
- Scheduling of memory in embedded and hardware design, where buffers are assigned at compile time.
- Wireless and network bandwidth allocation, where a request needs a contiguous band of frequencies during a time interval.

## References
