---
tag: S1T57H
kind: problem
slug: kidney-exchange-problem
name: Kidney exchange problem
aliases:
- kidney paired donation problem
area: algorithmic-game-theory/matching-markets-and-market-equilibria
level: core
summary: Find vertex-disjoint short cycles and chains in a graph of incompatible patient-donor pairs that maximize the number of transplants. It is NP-hard once cycles of length 3 are allowed.
prereqs: [directed-graph, maximum-matching]
see_also: [kidney-exchange-cycle-formulation, top-trading-cycles-and-chains, set-packing, three-dimensional-matching, branch-and-price, apx-completeness, shapley-scarf-housing-market, assignment-problem]
sources:
  - paper: doi:10.1145/1250910.1250954
    title: David J. Abraham, Avrim Blum and Tuomas Sandholm, Clearing algorithms for barter exchange markets, enabling nationwide kidney exchanges, Proceedings of the 8th ACM Conference on Electronic Commerce (EC 2007), 295 to 304
    locator: the NP-completeness of the clearing problem for cycle length at most L for every L at least 3, and the cycle formulation solved by branch and price
  - paper: doi:10.1142/S1793830909000373
    title: Peter Biro, David F. Manlove and Romeo Rizzi, Maximum weight cycle packing in directed graphs, with application to kidney exchange programs, Discrete Mathematics, Algorithms and Applications 1(4), 499 to 517 (2009)
    locator: APX-completeness for short cycles and the polynomial cases
  - paper: doi:10.1016/j.jet.2005.04.004
    title: Alvin E. Roth, Tayfun Sonmez and M. Utku Unver, Pairwise kidney exchange, Journal of Economic Theory 125(2), 151 to 188 (2005)
    locator: exchanges limited to two pairs, solved by maximum matching
---

The kidney exchange problem asks for the largest set of transplants that a pool of incompatible patient-donor pairs can carry out by swapping donors. Each pair is a vertex of a directed graph, with an arc from pair $i$ to pair $j$ when the donor of $i$ can give to the patient of $j$. A cycle of pairs is an exchange: each donor gives to the next patient. All operations of a cycle must take place at the same time, so clinics bound the cycle length by a small $L$, usually 2 or 3. The problem is to pack vertex-disjoint cycles of length at most $L$ that cover as many pairs as possible. For $L = 2$ it is a [maximum matching](/maximum-matching/) problem, and without a bound it is an [assignment problem](/assignment-problem/), but for every fixed $L \ge 3$ it is NP-hard (Abraham, Blum and Sandholm 2007).

## In plain words

A patient needs a kidney, and a relative wants to give one, but the kidney does not fit. Another pair has the same trouble. If each donor fits the other patient, the two pairs swap. With more pairs, longer loops are possible: donor A gives to patient B, donor B to patient C, and donor C to patient A. Each donor only gives if their own patient also gets a kidney, so all operations of a loop happen on the same day, and loops must stay short. The task is to choose loops that do not share a pair and that help as many patients as possible.

## Definition

**Input.** A directed graph $G = (V, A)$ on the pairs, an integer $L \ge 2$, and optionally a weight $w_{ij}$ for each arc (the value of the transplant from the donor of $i$ to the patient of $j$). In the version with chains, some vertices are altruistic donors without a patient, and chains can also be bounded in length.

**Output.** A set of vertex-disjoint directed cycles of $G$, each with at most $L$ arcs, with the most arcs in total (or the largest total weight). Each arc of a chosen cycle is one transplant. With altruistic donors, a solution may also use vertex-disjoint paths that start at an altruistic donor, called chains.

## Variants

- **Pairwise exchange ($L = 2$).** Only swaps of two pairs. Make an undirected graph with an edge $\{i, j\}$ when both arcs $(i, j)$ and $(j, i)$ exist. A set of swaps is a matching of this graph, so a maximum matching solves the problem in polynomial time, also with weights (Roth, Sonmez and Unver 2005).
- **No length bound.** A set of disjoint cycles covering some pairs is a cycle cover of $G$ with self-loops added. It is a perfect matching in the bipartite graph of donors and patients, so the [assignment problem](/assignment-problem/) solves it in polynomial time.
- **Fixed $L \ge 3$.** NP-hard (Abraham, Blum and Sandholm 2007), and APX-complete for short cycles (Biro, Manlove and Rizzi 2009).
- **Chains.** An altruistic donor starts a chain: it gives to a patient, whose donor gives to the next patient, and so on. The last donor may give to the deceased-donor waiting list. Chains do not need simultaneous operations, so they may be longer.
- **Mechanism design.** When patients have preferences and can misreport, the problem becomes one of designing an exchange rule. [Top trading cycles and chains](/top-trading-cycles-and-chains/) is efficient and strategyproof but does not bound cycle lengths.

## Examples

**A 3-cycle helps.** Three pairs with arcs $1 \to 2$, $2 \to 3$, $3 \to 1$ and $2 \to 1$. With $L = 2$ the only exchange is the swap of pairs 1 and 2, which gives 2 transplants. With $L = 3$ the cycle $1 \to 2 \to 3 \to 1$ gives 3 transplants.

**The cycles must be disjoint.** Add pairs 4 and 5 with arcs $3 \to 4$, $4 \to 3$, $4 \to 5$, $5 \to 4$. With $L = 3$, the cycle $1, 2, 3$ uses pair 3, so the best addition is the swap $4, 5$, for 5 transplants in total. The swap $3, 4$ would block both the 3-cycle and the swap $4, 5$.

## Known algorithms

- **$L = 2$.** Maximum matching in a general graph, or maximum weight matching for weights, in polynomial time.
- **No bound.** A minimum cost perfect matching in a bipartite graph with $2n$ vertices, by the [Hungarian algorithm](/hungarian-algorithm/) in $O(n^3)$ time.
- **Fixed $L \ge 3$.** Integer programming. The [cycle formulation](/kidney-exchange-cycle-formulation/) has one binary variable per cycle of length at most $L$ and one packing constraint per pair. Its LP relaxation is strong, and [branch and price](/branch-and-price/) handles pools with thousands of pairs by generating cycles only when they improve the LP (Abraham, Blum and Sandholm 2007). The edge formulation, with one variable per arc and constraints that forbid long cycles, is smaller, but its LP relaxation is usually weaker.
- **Small instances.** Enumerate all cycles of length at most $L$, at most $O(n^L)$ of them, and solve the [set packing](/set-packing/) problem over them by search.

## Bounds

- $L = 2$ and $L = \infty$: polynomial time.
- Fixed $L \ge 3$: NP-hard, by a reduction from [3-dimensional matching](/three-dimensional-matching/) (Abraham, Blum and Sandholm 2007). Biro, Manlove and Rizzi (2009) showed APX-completeness for short cycles, so no polynomial time approximation scheme exists unless P = NP.
- Approximation: a cycle of length at most $L$ is a set of at most $L$ pairs, so greedy and local search for $L$-set packing give constant ratios that depend on $L$.

## Reductions

- To [set packing](/set-packing/): the pairs are the ground set, and each cycle of length at most $L$ is a set of size at most $L$ with weight equal to its length. The kidney exchange problem is this set packing problem over the cycles of $G$.
- From [3-dimensional matching](/three-dimensional-matching/): the NP-hardness proof builds, for each triple, a gadget of pairs whose 3-cycles correspond to choosing the triple.
- To maximum matching for $L = 2$ and to the assignment problem for $L = \infty$, as above.
- Relation to the [housing market](/shapley-scarf-housing-market/): a pair owns a kidney and wants another one, as an agent owns a house. Top trading cycles finds the core of the market, but its cycles can be long.

## Applications

National and regional kidney exchange programs in the United States, the United Kingdom, the Netherlands and other countries solve this problem in each match run, with $L = 2$ or $L = 3$, chains started by altruistic donors, and weights for medical priority. The same model fits other barter markets in which items trade in short cycles.

## References
