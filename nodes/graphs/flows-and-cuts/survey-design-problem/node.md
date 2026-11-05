---
tag: BTNE9Y
kind: problem
slug: survey-design-problem
name: Survey design problem
area: graphs/flows-and-cuts
level: core
summary: Chooses which questions to ask which customers, within limits on each person's and each product's counts, solved as a flow with lower and upper bounds.
prereqs: [circulation-problem, bipartite-graph, max-flow-problem, integrality-theorem]
see_also: [hoffman-circulation-theorem, airline-scheduling, baseball-elimination, bipartite-matching, b-matching, f-factor-problem, flow-integrality-theorem]
sources:
  - book: isbn:9780321295354
    title: Jon Kleinberg and Eva Tardos, Algorithm Design
    locator: Section 7.7, Extensions to the Maximum-Flow Problem (circulations with demands and lower bounds), and Section 7.8, Survey Design
  - book: isbn:9780136175490
    title: Ravindra K. Ahuja, Thomas L. Magnanti and James B. Orlin, Network Flows, Theory, Algorithms, and Applications
    locator: Chapter 6, Maximum Flows, Basic Ideas (flows with nonnegative lower bounds and the feasible flow problem)
---

The survey design problem asks which customers to ask about which products, when each customer may be asked only about products they bought, each customer must answer between $c_i$ and $c'_i$ questions, and each product must be asked about between $p_j$ and $p'_j$ times. It is a [circulation with lower and upper bounds](/circulation-problem/) in a [bipartite](/bipartite-graph/) network, so it is decided by one [maximum flow](/max-flow-problem/), and by the [integrality theorem](/integrality-theorem/) an integral circulation gives an actual set of questions. Kleinberg and Tardos use it as the first application of flows with lower bounds; it is the bipartite degree-constrained subgraph problem, a form of [b-matching](/b-matching/) with intervals.

## In plain words

A shop wants feedback. Each customer can be asked only about things they bought. Nobody should get too few or too many questions, and each product should get enough answers, but not too many. Is there a way to pick the questions?

Draw the customers on the left, the products on the right, and a link for each purchase. Choosing questions means choosing links, so that each dot on either side has a number of chosen links within its range. Flow networks can force a pipe to carry at least some amount, not only at most some amount. With that, each customer becomes a pipe with a lower and an upper limit, and so does each product, and a valid flow is a valid survey.

## Definition

**Input.** Customers $1, \ldots, n$ and products $1, \ldots, k$; for each customer $i$ the set $B_i$ of products they bought; integers $0 \le c_i \le c'_i$ for each customer and $0 \le p_j \le p'_j$ for each product.

**Output.** A set $Q$ of pairs $(i, j)$ with $j \in B_i$ such that each customer $i$ is in between $c_i$ and $c'_i$ pairs, and each product $j$ is in between $p_j$ and $p'_j$ pairs, or a report that none exists. Each pair is one question, asked at most once.

**The network.** A directed graph on $\{s, t\} \cup \{\text{customers}\} \cup \{\text{products}\}$, with lower and upper bounds $[\ell, u]$:

- $s \to i$ with $[c_i, c'_i]$ for each customer;
- $i \to j$ with $[0, 1]$ for each $j \in B_i$;
- $j \to t$ with $[p_j, p'_j]$ for each product;
- $t \to s$ with $[0, \infty)$.

All bounds are integers and the graph is directed; it has no antiparallel pairs except possibly $t \to s$ against an edge $s \to t$, which does not occur. A purchase that must never be asked about is an edge $[0, 0]$, which may be dropped.

**Claim.** A survey exists if and only if this network has a feasible circulation, and then it has an integral one, whose edges $i \to j$ with flow 1 form a survey.

*Proof.* A survey $Q$ gives the circulation with 1 on $i \to j$ for $(i, j) \in Q$, the number of questions of $i$ on $s \to i$, the number of answers about $j$ on $j \to t$, and $|Q|$ on $t \to s$; conservation holds at every vertex, and the bounds hold by the definition of a survey. Conversely, a feasible circulation with integer bounds has an integral feasible version by the integrality theorem (Theorem B, incidence matrices are totally unimodular), and its edges $i \to j$ with flow 1 meet the bounds at each customer and product by conservation. $\square$

**Lower bounds to maximum flow.** Replace each edge $(v, w)$ with bounds $[\ell, u]$ by an edge of capacity $u - \ell$, and add $\ell$ to the demand of $w$ and to the supply of $v$. Then add a super-source $s^{*}$ with an edge to each vertex of net supply, a super-sink $t^{*}$ with an edge from each vertex of net demand, and compute a maximum $s^{*}$-$t^{*}$ flow. A feasible circulation exists if and only if this flow saturates every edge out of $s^{*}$, that is, has value $\sum \ell$ in total. This is the reduction of the [circulation problem](/circulation-problem/).

## Variants

- **Only upper bounds.** With $c_i = p_j = 0$, the empty survey works, and the interesting version maximizes $|Q|$: a maximum flow from $s$ to $t$, a bipartite b-matching.
- **Exact counts.** $c_i = c'_i$ and $p_j = p'_j$: a bipartite graph with prescribed degrees, an [f-factor](/f-factor-problem/) of a bipartite graph.
- **Costs or preferences.** A cost for each question gives a [minimum-cost circulation](/min-cost-flow-problem/).
- **Matrix rounding and 0-1 matrices with given row and column sums.** The complete bipartite case with exact counts is the Gale-Ryser question.
- **Several questions per pair.** Raise the upper bound of $i \to j$.

## Examples

Customers $A$, $B$, $C$ and products $X$, $Y$; $A$ bought $X$ and $Y$, $B$ bought $X$, and $C$ bought $X$ and $Y$. So the possible questions are $AX$, $AY$, $BX$, $CX$, $CY$.

| bounds | surveys |
|---|---|
| each customer $[1, 2]$; $X$ $[2, 3]$, $Y$ $[2, 2]$ | $\{AX, AY, BX, CY\}$, $\{AY, BX, CX, CY\}$, $\{AX, AY, BX, CX, CY\}$ |
| each customer $[1, 2]$; $X$ $[2, 3]$, $Y$ $[3, 3]$ | none |
| each customer $[1, 1]$; $X$ $[2, 3]$, $Y$ $[2, 2]$ | none |

The table lists all surveys, found by trying all 32 subsets. In the second row, only $A$ and $C$ bought $Y$, so $Y$ can get at most 2 answers: the edges into $Y$ have total capacity 2, below the lower bound 3 of $Y \to t$. In the third row, the customers answer exactly 3 questions in total, while the products need at least 4: in any circulation the flow on $t \to s$ equals the total on the edges out of $s$, at most 3, and also the total on the edges into $t$, at least 4.

**Zero capacity.** If $B$ may not be asked at all, set $c'_B = 0$; the edge $s \to B$ has bounds $[0, 0]$, and $X$ must get its answers from $A$ and $C$.

**No path.** A product with $p_j \ge 1$ that nobody bought has no edge into it, so no flow reaches $j \to t$, and the survey is infeasible.

## Known algorithms

- **One maximum flow** after the reduction of lower bounds, on $n + k + 4$ vertices and $M + n + k + 1$ edges plus the super-source and super-sink edges, where $M = \sum_i |B_i|$. The flow value is at most $\sum_i c'_i$, so even [Ford-Fulkerson](/ford-fulkerson/) takes $O(M \sum_i c'_i)$ time on the reduced network; [Dinic](/dinic/) on this unit-capacity middle layer is faster.
- **Hoffman's theorem as a certificate.** If no survey exists, a set of vertices whose cut violates [Hoffman's condition](/hoffman-circulation-theorem/) proves it, as in the examples.

## Bounds

The problem is solvable in polynomial time, by the reduction above. A feasible survey and an infeasibility certificate can both be checked in time linear in the size of the input. The flow reduction is the standard method; the general bounds of maximum flow apply.

## Reductions

- **Survey design to circulation with lower bounds,** as in the definition.
- **Circulation with lower bounds to maximum flow,** by the super-source and super-sink construction.
- **Bipartite matching** is the case $c_i = 0$, $c'_i = 1$, $p_j = 0$, $p'_j = 1$, maximizing the flow.
- **[Airline scheduling](/airline-scheduling/)** uses the same lower-bound technique, with a lower bound of 1 on each flight that must be flown.

## Applications

- Designing surveys and questionnaires with balanced coverage.
- Assigning papers to reviewers with load limits and a minimum number of reviews per paper.
- Assigning students to sections with minimum and maximum enrollments.
- Building 0-1 tables with row and column sums in given ranges, as in statistical disclosure control.

## References
