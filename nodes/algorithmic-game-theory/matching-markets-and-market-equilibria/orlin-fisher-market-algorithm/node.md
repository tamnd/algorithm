---
tag: XBSFVW
kind: algorithm
slug: orlin-fisher-market-algorithm
name: "Orlin's strongly polynomial Fisher market algorithm"
aliases:
- "Orlin's algorithm for linear Fisher markets"
area: algorithmic-game-theory/matching-markets-and-market-equilibria
level: research
summary: The first strongly polynomial algorithm for linear Fisher market equilibrium, by scaling and contraction of tight edges.
model: real-ram
complexity:
  vars: {n: the number of buyers plus the number of goods, m: the number of pairs of a buyer and a good with positive utility}
  time: {worst: "O(n^2 log n (m + n log n))"}
  space: {extra: O(n + m)}
properties: {deterministic: true, recursive: false}
history:
  year: 2010
  people: [James B. Orlin]
  note: Orlin gave a scaling algorithm for linear Fisher markets and made it strongly polynomial with abundant edges, which he had used earlier for minimum cost flow. This answered an open question of Devanur, Papadimitriou, Saberi and Vazirani.
prereqs: [fisher-market, dpsv-algorithm]
see_also: [eisenberg-gale-program, capacity-scaling, min-cost-flow-problem, residual-graph, fibonacci-heap, proportional-response-dynamics, max-flow-min-cut-theorem, competitive-equilibrium]
sources:
  - paper: doi:10.1145/1806689.1806731
    title: "James B. Orlin, Improved algorithms for computing Fisher's market clearing prices, STOC 2010, 291-300"
    locator: the whole paper (the scaling algorithm with PriceAndAugment, abundant edges, and the strongly polynomial algorithm)
  - url: https://drops.dagstuhl.de/opus/volltexte/2010/2672
    title: "James B. Orlin, Improved algorithms for computing Fisher's market clearing prices, Dagstuhl Seminar Proceedings 10171, Equilibrium Computation (2010)"
    locator: "Section 3 (Delta-feasibility, PriceAndAugment, ScalingAlgorithm, Lemma 3.3, Lemma 3.4, Theorems 3.1 to 3.3), Section 4 (fertile components, MakeFertile and StrongScaling)"
  - paper: doi:10.1145/1411509.1411512
    title: "Nikhil R. Devanur, Christos H. Papadimitriou, Amin Saberi and Vijay V. Vazirani, Market equilibrium via a primal-dual algorithm for a convex program, Journal of the ACM 55(5), Article 22 (2008)"
    locator: Sections 1.2 and 9 (a strongly polynomial algorithm is stated as an open question) and Sections 5 to 8 (the price raising that Orlin's algorithm reuses)
---

Orlin's algorithm computes the exact equilibrium of a [Fisher market](/fisher-market/) with linear utilities in strongly polynomial time: the number of arithmetic operations depends only on the number of buyers, goods and edges, not on the size of the utilities or budgets. It was the first algorithm with this property. It keeps the price raising of the [DPSV algorithm](/dpsv-algorithm/), in which prices only go up and money flows only along edges of maximum bang per buck, and replaces the maximum flows with [scaling](/capacity-scaling/): money moves in units of $\Delta$, and $\Delta$ is halved from phase to phase. This scaling algorithm is weakly polynomial. To make it strongly polynomial, Orlin uses *abundant* edges, edges that carry so much money that they must carry money at the equilibrium, and a procedure that jumps $\Delta$ down by a large factor when no new abundant edge is near. The implementation on this page is a toy of the scaling algorithm only.

## In plain words

Buyers have money, goods have prices, and each buyer only wants the goods that give her the most pleasure per coin. Start with low prices and nobody owning anything. Hand out money in coins of a fixed size: a buyer with at least one coin left sends it to a good she likes best, maybe pushing another buyer's coin to a different good along the way. If every good she can reach is already paid for, raise the prices of those goods until some good has room again. When no buyer has a full coin left, halve the coin and repeat. Edges that carry many coins can be trusted to be in the final answer. Once those edges fix the prices, check them exactly and stop.

## The problem

There is a set $B$ of buyers and a set $G$ of goods, with one unit of each good, and $n = |B| + |G|$. Buyer $i$ has a budget $e_i > 0$ and utility $u_{ij} \ge 0$ for all of good $j$, linear in the amount. The *edges* are the $m$ pairs with $u_{ij} > 0$. Every buyer likes some good and every good is liked by some buyer. Find prices $p$ and money flows $x_{ij} \ge 0$ (the money that buyer $i$ spends on good $j$) such that every buyer spends exactly $e_i$, only on goods of maximum bang per buck $u_{ij} / p_j$, and every good receives exactly $p_j$.

Write $c_i = e_i - \sum_j x_{ij}$ for the money that buyer $i$ has left and $b_j = \sum_i x_{ij} - p_j$ for the money that good $j$ receives above its price. An *equality edge* at $p$ is an edge with $u_{ij} / p_j = \max_k u_{ik} / p_k$. Let $p^0$ be the starting prices. Following Orlin, $(p, x)$ is *$\Delta$-feasible* when $c_i \ge 0$ for every buyer, $0 \le b_j \le \Delta$ for every good with $p_j > p^0_j$, every $x_{ij} > 0$ is on an equality edge and is a multiple of $\Delta$, and $x, p \ge 0$. It is *$\Delta$-optimal* if also $c_i < \Delta$ for every buyer.

## The algorithm

The residual network $N(p, x)$ has an arc from buyer $i$ to good $j$ for each equality edge and an arc from good $j$ back to buyer $i$ when $x_{ij} > 0$. The pseudocode is the scaling algorithm, which the implementation follows.

```pseudo id=main
ORLIN-SCALING(utilities u, budgets e)
L1  Δ ← max_i e_i / n;  p_j ← max_i u_ij e_i / (n Σ_k u_ik) for every good;  x ← 0
L2  loop
L3      while some buyer r has c_r ≥ Δ do
L4          A ← the nodes that r reaches in N(p, x)
L5          if no good j in A has b_j ≤ 0 then multiply the prices of the goods in A by the least q > 1 at which some good of A gets b_j = 0 or a buyer of A gets a new equality edge; go to L4
L6          send Δ along a path of N(p, x) from r to a good j of A with b_j ≤ 0
L7      S ← the edges with x_ij ≥ 4nΔ
L8      p' ← the prices that S forces; if p' passes the exact max-flow check, return p' and the flow
L9      Δ ← Δ / 2; for every good with b_j > Δ, lower some positive x_ij by Δ
```

Lines L4 to L6 are PriceAndAugment. The price increase of line L5 is the one of the DPSV algorithm: the goods that $r$ can reach all get dearer by the same factor, so the equality edges among them stay, and the step stops when a good runs out of extra money or a new good becomes reachable. Line L6 adds $\Delta$ on the forward arcs of the path and removes $\Delta$ on its backward arcs, so only the root $r$ and the last good $j$ change their totals. Line L9 makes the solution $\Delta/2$-feasible for the next phase.

Line L8 is the stopping test. A set of edges $S$ forces prices when it touches every node: along the edges of each buyer the bang per buck is equal, which fixes the price ratios on each connected part, and the prices of each part add up to the budgets of its buyers. The implementation computes these prices in exact rationals and accepts them only if a maximum flow on the equality edges spends every budget, as on the [Eisenberg-Gale program](/eisenberg-gale-program/) page. Orlin perturbs the utilities so that the equilibrium allocation is unique and its edges form a forest; the toy does not perturb, which is why it checks.

**The strongly polynomial algorithm.** An edge is *abundant* if $x_{ij} \ge 3n\Delta$ at the start of the $\Delta$ phase. In one phase, each $x_{ij}$ changes by $O(n\Delta)$, and $\Delta$ halves from phase to phase, so an abundant edge stays abundant in all later phases (Lemma 3.4 of the Dagstuhl version) and carries money at the equilibrium. With perturbed utilities, there are at most $n - 1$ abundant edges. The scaling algorithm alone can need many phases between two new abundant edges. Orlin's procedure MakeFertile detects this case from the components of the abundant edges and their surplus, and jumps to a new $\Delta' \le \Delta / n^2$ and new prices from which a new abundant edge appears within $O(\log n)$ phases. This gives $O(n \log n)$ phases with $O(n)$ calls of PriceAndAugment each. The toy leaves MakeFertile out.

## Example

Three buyers and three goods, $u_1 = (1, 4, 3)$, $u_2 = (4, 2, 1)$, $u_3 = (1, 1, 2)$, budgets $e = (1, 1, 3)$, so $n = 6$. Line L1 gives $\Delta = 1/2$ and $p^0 = (1/8, 1/8, 1/4)$. The money flows reach their final values in the second phase; after that only the prices move toward the equilibrium $(5/4, 5/4, 5/2)$, and line L8 waits until the edges with $x_{ij} \ge 24\Delta$ force the right prices.

| $\Delta$ at the end of the phase | prices | buyer 3 spends on goods 1, 2, 3 | edges with $x_{ij} \ge 24\Delta$ | line L8 |
|---|---|---|---|---|
| $1/2$ | $(1, 1, 2)$ | $1/2, 1/2, 2$ | none | no prices |
| $1/4$ | $(9/8, 9/8, 9/4)$ | $1/4, 1/4, 5/2$ | none | no prices |
| $1/8$ | $(19/16, 19/16, 19/8)$ | $1/4, 1/4, 5/2$ | none | no prices |
| $1/16$ | $(39/32, 39/32, 39/16)$ | $1/4, 1/4, 5/2$ | $(3, 3)$ | no prices |
| $1/32$ | $(79/64, 79/64, 79/32)$ | $1/4, 1/4, 5/2$ | $(1, 2), (2, 1), (3, 3)$ | $(1, 1, 3)$, rejected |
| $1/64$ | $(159/128, 159/128, 159/64)$ | $1/4, 1/4, 5/2$ | $(1, 2), (2, 1), (3, 3)$ | $(1, 1, 3)$, rejected |
| $1/128$ | $(319/256, 319/256, 319/128)$ | $1/4, 1/4, 5/2$ | all five edges | $(5/4, 5/4, 5/2)$, accepted |

In all phases buyer 1 spends $1$ on good 2 and buyer 2 spends $1$ on good 1. At $\Delta = 1/32$, the three edges form three parts with one buyer each, which force the prices $(1, 1, 3)$; at these prices buyer 3 gets $2/3$ per unit of money from good 3 but $1$ from goods 1 and 2, so the check fails. At $\Delta = 1/128$ the edges $(3, 1)$ and $(3, 2)$ carry $1/4 \ge 24/128$, all five edges form one part, and they force $p = (5/4, 5/4, 5/2)$, which the check accepts. For the market $u_1 = (2, 1)$, $u_2 = (1, 2)$ with budgets $(1, 1)$, the phases $\Delta = 1/4, 1/8, 1/16$ end with prices $(3/4, 3/4)$, $(7/8, 7/8)$ and $(15/16, 15/16)$, and the last one returns $p = (1, 1)$.

## Correctness

The proof for the toy is in `proofs/correctness.md`. Line L5 and line L6 keep $\Delta$-feasibility, and line L9 turns a $\Delta$-optimal solution into a $\Delta/2$-feasible one. Each call of PriceAndAugment ends, because every price step either ends it or makes a new good reachable, and each call lowers the money left with the buyers by $\Delta$, so each phase ends. Prices only rise and stay bounded, and the money flows change by at most $(n + 1)\Delta$ per phase, so both converge, and the limit is an equilibrium; the delicate part is a good that keeps its starting price, which Lemma 3.3 of Orlin handles. Once $\Delta$ is small, the edges with $x_{ij} \ge 4n\Delta$ are exactly the edges that carry money in the limit, and they force the equilibrium prices, so line L8 returns. Whatever line L8 returns is correct, because it passes the exact check.

## Complexity

For integer data, Theorem 3.1 of the Dagstuhl version shows that each phase makes at most $n$ calls of PriceAndAugment and that each call takes $O(m + n \log n)$ time with prices stored implicitly and a [Fibonacci heap](/fibonacci-heap/) of the times at which edges become equality edges. The number of phases of the scaling algorithm depends on the largest utility and budget, so it is weakly polynomial. The strongly polynomial algorithm StrongScaling has $O(n \log n)$ phases and runs in $O(n^2 \log n \, (m + n \log n))$ time, which the abstract states in the weaker form $O(n^4 \log n)$. Orlin also shows that an $\varepsilon$-approximate solution takes $O(\log(n / \varepsilon))$ phases.

The toy stores prices explicitly and recomputes the residual network with breadth-first search, so one price step costs $O(nm)$ and one call of PriceAndAugment $O(n^2 m)$ exact operations; the check of line L8 adds a maximum flow per phase. It has no strongly polynomial bound, because it leaves out MakeFertile.

## Properties

- **Prices only rise**, as in the DPSV algorithm, and money moves in multiples of $\Delta$.
- **Strongly polynomial.** The number of operations of StrongScaling depends only on $n$ and $m$. The numbers themselves are rational, and the bit lengths stay polynomial.
- **Abundant edges are permanent.** Once an edge carries at least $3n\Delta$ at the start of a phase, it carries money in every later phase and at the equilibrium.
- **The scaling algorithm alone is not strongly polynomial.** Orlin's example has one buyer with budget $1$ and two goods with utilities $2^K$ and $1$. The equilibrium spends $1/(2^K + 1)$ on the second good, and the scaling algorithm needs more than $K$ phases before this edge carries enough money to be recognized.

## Variants and improvements

- **Weakly polynomial scaling.** The algorithm of the pseudocode, without MakeFertile, is already faster than the DPSV bound.
- **Approximate equilibria.** Stopping the scaling algorithm after $O(\log(n / \varepsilon))$ phases gives an $\varepsilon$-approximate solution in $O(n (m + n \log n) \log(n / \varepsilon))$ time.
- **Small utilities.** When the utilities are bounded by a polynomial in $n$, Orlin gives a simpler strongly polynomial method (Section 3.7 and Theorem 3.3 of the Dagstuhl version). It sorts the buyers by budget, adds them in groups at the places where the budget drops by a large factor, and needs $O(n^2 \log U_{\max})$ scaling phases in total.
- **Other methods.** The [Eisenberg-Gale program](/eisenberg-gale-program/) can be solved by interior point or ellipsoid methods, and [proportional response dynamics](/proportional-response-dynamics/) converges to the same equilibrium without a central planner.

## When to use it

Use it as the reference algorithm when a guaranteed strongly polynomial bound for linear Fisher markets matters, or as a model of how abundant edges turn a scaling algorithm into a strongly polynomial one. In practice, for small markets the [DPSV algorithm](/dpsv-algorithm/) with exact arithmetic is simpler, and for large markets where an approximate answer is enough the scaling algorithm stopped early or a convex solver is easier to implement.

## Pitfalls

- Raising the prices in line L5 beyond the first good whose extra money $b_j$ reaches $0$ leaves a raised good with $b_j < 0$, which breaks $\Delta$-feasibility: the good is then sold for less than its price.
- Sending more than $\Delta$ in line L6, for example all the money that the root has left, breaks the rule that flows are multiples of $\Delta$ and the bound of $n$ calls per phase.
- Halving $\Delta$ in line L9 without lowering the flows into goods with $b_j > \Delta$ leaves goods with too much money for the next phase.
- Returning the prices forced by the edges of line L7 without the check of line L8 fails without perturbation: in the example, the edges at $\Delta = 1/32$ force $(1, 1, 3)$, which is not an equilibrium.
- Using floating point in line L5 makes the equality tests fail, so arcs of the residual network get lost. Use exact rationals.

## Implementations

## History

Devanur, Papadimitriou, Saberi and Vazirani gave the first combinatorial polynomial time algorithm for linear Fisher markets and asked for a strongly polynomial one. Orlin presented his algorithm at the Dagstuhl seminar on equilibrium computation and at STOC 2010. He used the scaling idea of Edmonds and Karp and the abundant edges that he had introduced for a strongly polynomial minimum cost flow algorithm, the problem on the [minimum cost flow](/min-cost-flow-problem/) page.

## References
