---
tag: HATF0Q
kind: algorithm
slug: kidney-exchange-cycle-formulation
name: Cycle formulation for kidney exchange
aliases:
- Abraham-Blum-Sandholm kidney exchange solver
area: algorithmic-game-theory/matching-markets-and-market-equilibria
level: advanced
summary: Solves kidney exchange with cycle length at most L by an integer program with one variable per short cycle, using branch and price.
solves: [kidney-exchange-problem]
model: real-ram
complexity:
  vars: {n: the number of pairs, L: the bound on the cycle length, C: the number of cycles with at most L pairs (at most n^L)}
  time: {worst: 2^(O(n + C))}
  space: {extra: O(C^2 + n (n + C))}
properties: {deterministic: true, recursive: false}
history:
  year: 2007
  people: [David J. Abraham, Avrim Blum, Tuomas Sandholm]
  note: Abraham, Blum and Sandholm proposed branch and price on the cycle formulation in 2007, and it cleared pools far larger than earlier methods could handle.
prereqs: [kidney-exchange-problem, binary-integer-programming, column-generation]
see_also: [branch-and-price, lp-relaxation, set-packing, lp-duality, integrality-gap, top-trading-cycles-and-chains, enumerating-elementary-cycles, simplex-method]
sources:
  - paper: doi:10.1145/1250910.1250954
    title: David J. Abraham, Avrim Blum and Tuomas Sandholm, Clearing algorithms for barter exchange markets, enabling nationwide kidney exchanges, Proceedings of the 8th ACM Conference on Electronic Commerce (EC 2007), 295 to 304
    locator: the cycle formulation, its solution by branch and price, and the pricing of cycles with the LP duals
  - paper: doi:10.1142/S1793830909000373
    title: Peter Biro, David F. Manlove and Romeo Rizzi, Maximum weight cycle packing in directed graphs, with application to kidney exchange programs, Discrete Mathematics, Algorithms and Applications 1(4), 499 to 517 (2009)
    locator: the complexity of cycle packing with short cycles
---

The cycle formulation is the standard integer program for the [kidney exchange problem](/kidney-exchange-problem/). It has one binary variable $x_c$ for each directed cycle $c$ of at most $L$ pairs in the compatibility graph, and one constraint for each pair: the chosen cycles must not share it. This is a [set packing](/set-packing/) problem over the short cycles. Its [LP relaxation](/lp-relaxation/) is strong, but the number of cycles grows like $n^L$, so Abraham, Blum and Sandholm (2007) solved it by [branch and price](/branch-and-price/): each LP uses only a few cycles and adds a new one when the LP duals show that it can improve the solution. The worst case is exponential, since the problem is NP-hard for $L \ge 3$.

## In plain words

List every short loop of pairs that could swap kidneys. The task is to choose loops that share no pair and give the most transplants. A computer can solve the relaxed problem where a loop may be "half chosen" quickly, and the answer is a good upper bound. If the relaxed answer chooses whole loops only, it is the best answer. If not, pick a half-chosen loop and try two cases: take it, or ban it. To keep the relaxed problems small, start with a few loops and add a loop only when the prices of the pairs, which come from the relaxed problem, say that the loop is worth more than the pairs it uses.

## The problem

The input is a directed graph on $n$ pairs, with an arc $(i, j)$ when the donor of pair $i$ can give to the patient of pair $j$, a bound $L \ge 2$, and integer arc weights $w_{ij}$ (all 1 to count transplants). Let $\mathcal{C}$ be the set of directed cycles with at most $L$ pairs, and $w_c$ the total weight of the arcs of $c$. The cycle formulation is

$$\max \sum_{c \in \mathcal{C}} w_c x_c \quad \text{subject to} \quad \sum_{c \ni v} x_c \le 1 \text{ for every pair } v, \quad x_c \in \{0, 1\}.$$

The LP relaxation replaces $x_c \in \{0, 1\}$ by $x_c \ge 0$. Its dual has a price $y_v \ge 0$ for each pair and asks $\sum_{v \in c} y_v \ge w_c$ for every cycle $c$.

## The algorithm

```pseudo id=main
KIDNEY-EXCHANGE-BRANCH-AND-PRICE(G, L, w)
L1  best ← 0;  best_set ← ∅
L2  push the root node (fixed ← ∅, forbidden ← ∅, columns ← ∅)
L3  while the stack is not empty do
L4      pop a node;  V' ← the pairs not on a fixed cycle
L5      repeat:  solve the LP over the columns, on the pairs of V';  get x and the duals y
L6          add every cycle c of G[V'] with at most L pairs, not forbidden, with w_c − Σ_{v∈c} y_v > 0
L7      until no cycle is added
L8      if w(fixed) + ⌊LP value⌋ ≤ best then discard the node
L9      else if x is integral then best ← w(fixed) + LP value;  best_set ← fixed ∪ {c : x_c = 1}
L10     else c ← a cycle with fractional x_c of largest value
L11         push (fixed, forbidden ∪ {c}) and then (fixed ∪ {c}, forbidden)
L12 return best and best_set
```

Lines L5 to L7 are [column generation](/column-generation/). The LP over a subset of the cycles (the restricted master) gives duals $y$. A cycle with positive reduced cost $w_c - \sum_{v \in c} y_v$ violates the dual, so adding it can raise the LP value. When no cycle has positive reduced cost, $y$ is feasible for the full dual, so by [LP duality](/lp-duality/) the restricted LP value is the value of the full LP relaxation of the node. Here the pricing step enumerates the short cycles of $G[V']$, which is exact. Line L8 uses that the weights are integers, so an LP bound of $3.5$ means at most 3. Line L11 branches on one cycle: the child that takes it is popped first.

## Example

Three pairs with arcs in both directions between each two, and $L = 2$. The short cycles are the swaps $\{1, 2\}$, $\{1, 3\}$ and $\{2, 3\}$, each worth 2.

1. Root. The LP starts with no columns, so $y = 0$, and all three swaps have reduced cost 2. They enter. The LP optimum is $x = (1/2, 1/2, 1/2)$ with value 3, and the duals are $y = (1, 1, 1)$: each swap now has reduced cost $2 - 2 = 0$, so pricing adds nothing. The bound is 3, and $x$ is fractional.
2. Branch on the swap $\{2, 3\}$. The child that takes it has only pair 1 left, so its LP value is 0, and the solution is integral with value 2. Now $\text{best} = 2$.
3. The child that forbids $\{2, 3\}$ has the swaps $\{1, 2\}$ and $\{1, 3\}$. Both use pair 1, so its LP value is 2, and $0 + 2 \le 2$: it is discarded.

The answer is one swap, 2 transplants, after 3 nodes. The gap between 3 and 2 is the [integrality gap](/integrality-gap/) of this instance. With $L = 3$ the cycle $1 \to 2 \to 3 \to 1$ is also a column, the LP gives it $x = 1$, and the root is already integral with value 3.

## Correctness

**Bounds.** At each node, the LP over all allowed cycles of $G[V']$ is a relaxation of the node's integer program, and column generation reaches its optimum value, by the duality argument above. So $w(\text{fixed}) + \lfloor \text{LP value} \rfloor$ bounds every solution in the subtree, and line L8 never discards a better solution.

**Branching.** The two children split the solutions of a node: every packing either uses $c$ or does not. The cycle $c$ is fractional, so it is not forbidden and not fixed already, and each child has one more fixed or forbidden cycle. So the depth is at most $C$, and the search ends.

**Leaves.** If $x$ is integral, it is a packing of cycles with the LP value, and no packing of the node is better. Together with the bounds, the best leaf found is optimal. The proof file gives the details.

## Complexity

The problem is NP-hard for $L \ge 3$, so no polynomial bound is expected. The search tree has depth at most $C$, so at most $2^{C+1}$ nodes. Each node solves LPs with at most $C$ columns and $n$ rows; the [simplex method](/simplex-method/) with Bland's rule visits at most one basis per subset of the $n + C$ columns, and pricing adds at least one column per round, so a node does at most $C$ rounds. All of this is $2^{O(n + C)}$ in the worst case, with $C \le n^L$. Enumerating the cycles costs $O(n d^{L-1})$ for maximum out-degree $d$, which is the method of [elementary cycle enumeration](/enumerating-elementary-cycles/) cut at depth $L$. In practice the LP bound of the cycle formulation is very close to the optimum, and the tree stays small.

The model is the [real RAM](/real-ram/) for the arithmetic of the LP; the implementation uses exact rational numbers.

## Properties

- **Exact.** It returns an optimal packing, not an approximation.
- **Strong relaxation.** The LP relaxation only mixes short cycles, so a fractional solution cannot use long cycles. On real pools its bound is usually very close to the optimum, which keeps the search tree small.
- **Columns, not rows.** The formulation has $n$ constraints and many variables, which is the case where column generation pays off.
- **Weights.** Any integer weights work, so medical priorities and the chance of success can be folded into $w$.

## Variants and improvements

- **Chains.** Altruistic donors start chains. The cycle formulation adds one variable per chain of bounded length, or treats a chain as a cycle through a dummy arc back to the altruistic donor.
- **Pricing by search.** Real pools have too many cycles to enumerate. Pricing then searches for a positive reduced cost cycle with the duals as vertex costs, which is a bounded length cycle problem, solved by dynamic programming or by heuristics followed by an exact check.
- **Other formulations.** Edge formulations and position-indexed formulations have polynomially many variables and are easier to set up, but their LP bounds are usually weaker.
- **$L = 2$.** For swaps only, the LP is the matching LP, and a [maximum matching](/maximum-matching/) algorithm is faster.

## When to use it

Use it for the clearing step of a kidney exchange program with $L = 3$ or similar, and for other barter markets where items trade in short cycles. For $L = 2$ use maximum weight matching. For an unbounded $L$ use the [assignment problem](/assignment-problem/). For a mechanism with incentive properties and no length bound, see [top trading cycles and chains](/top-trading-cycles-and-chains/).

## Pitfalls

- **Enumerating all cycles up front.** With thousands of pairs and $L = 3$, the cycles do not fit in memory. Generate them by pricing.
- **Floating point duals.** A reduced cost of $10^{-12}$ can make column generation loop or stop early. Use a tolerance with care, or exact arithmetic for small cases.
- **Branching on arcs or pairs naively.** Branching on a single arc variable gives unbalanced trees. Branch on cycles, as here, or on pairs, and make sure that the pricing step respects the branch.
- **Forgetting the floor.** With integer weights, the bound $\lfloor \text{LP} \rfloor$ prunes many more nodes than the raw LP value.

## Implementations

The Python version takes the number of pairs, the list of arcs, $L$ and optional integer weights, and returns the optimal value, the chosen cycles and the root LP bound with the node count. It uses the shared exact LP helper in Fraction, so the duals are exact. The tests compare the value with a brute force search over all packings of short cycles on random graphs with up to 8 pairs, check the cycle enumeration against a search over vertex sequences, and check the examples on this page.

## History

Abraham, Blum and Sandholm (2007) showed that the problem is NP-hard for $L \ge 3$ and solved it at the scale of a national program by branch and price on the cycle formulation. Biro, Manlove and Rizzi (2009) settled its approximability for short cycles. Later work added chains and compact formulations.

## References
