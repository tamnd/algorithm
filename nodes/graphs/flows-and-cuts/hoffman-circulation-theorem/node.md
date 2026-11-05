---
tag: 3R1NQ4
kind: theorem
slug: hoffman-circulation-theorem
name: Hoffman's circulation theorem
aliases:
- Hoffman's theorem on circulations
area: graphs/flows-and-cuts
level: advanced
summary: A feasible circulation exists iff every cut has enough upper capacity to cover its lower bounds.
prereqs: [circulation-problem, max-flow-min-cut-theorem, cut]
see_also: [flow-integrality-theorem, hall-theorem, farkas-lemma, total-unimodularity, airline-scheduling, survey-design-problem, min-cost-flow-problem]
sources:
  - book: isbn:9783540443896
    title: Alexander Schrijver, Combinatorial Optimization, Polyhedra and Efficiency, Volume A
    locator: Chapter 11, Circulations and b-transshipments (Hoffman's circulation theorem and its proof from max-flow min-cut)
  - book: isbn:9780321295354
    title: Jon Kleinberg and Eva Tardos, Algorithm Design
    locator: Section 7.7, Extensions to the Maximum-Flow Problem (the cut condition for circulations with demands)
  - book: isbn:9780136175490
    title: Ravindra K. Ahuja, Thomas L. Magnanti and James B. Orlin, Network Flows, Theory, Algorithms, and Applications
    locator: Chapter 6, Maximum Flows, Basic Ideas (feasibility conditions for flows with lower bounds and for supplies and demands)
---

Hoffman's circulation theorem says exactly when a directed graph with lower and upper bounds on its edges has a feasible circulation: if and only if, for every set $S$ of vertices, the flow that must leave $S$ by the lower bounds is at most the flow that can enter $S$ by the capacities. The condition is clearly necessary; the theorem says it is also sufficient. With demands at the vertices the same holds with the net demand of $S$ added to the condition. It follows from the max-flow min-cut theorem through the reduction of the [circulation problem](/circulation-problem/) to a maximum flow, and it contains [Hall's theorem](/hall-theorem/) and Gale's supply-demand theorem as special cases.

## Statement

Let $G = (V, E)$ be a directed graph, with $0 \le \ell(e) \le c(e)$ on each edge and a demand $d(v)$ at each vertex, where $\sum_{v} d(v) = 0$. The numbers are reals. Parallel and antiparallel edges are allowed and are separate edges, each with its own bounds. A *feasible circulation* is $f : E \to \mathbb{R}$ with $\ell \le f \le c$ and $f^{\text{in}}(v) - f^{\text{out}}(v) = d(v)$ for each $v$, the sign convention of the page [circulation problem](/circulation-problem/). For $S \subseteq V$ write $\delta^{\text{in}}(S)$ and $\delta^{\text{out}}(S)$ for the edges entering and leaving $S$, and $d(S) = \sum_{v \in S} d(v)$.

**Theorem (Hoffman, 1960).** A feasible circulation exists if and only if
$$d(S) \le c(\delta^{\text{in}}(S)) - \ell(\delta^{\text{out}}(S)) \quad \text{for every } S \subseteq V.$$

**Without demands** ($d \equiv 0$), this is Hoffman's original form: a circulation with $\ell \le f \le c$ exists if and only if $\ell(\delta^{\text{out}}(S)) \le c(\delta^{\text{in}}(S))$ for every $S$.

**Integrality.** If $\ell$, $c$ and $d$ are integers and the condition holds, an integer feasible circulation exists.

## In plain words

Think of the vertices as warehouses and the edges as one-way roads, each with a minimum and a maximum load, and each warehouse wanting a fixed net amount. Pick any group of warehouses. The group must take in its net demand, plus everything that the minimums force out of it. All of that has to come in over the roads into the group, and those roads carry at most their maximums. So if any group needs more than its incoming roads can bring, there is no plan.

The theorem says this is the only thing that can go wrong. If every group passes this simple count, a plan exists, and with whole-number data it uses whole numbers.

## Proof

*Necessity.* Let $f$ be feasible and $S \subseteq V$. Summing the conservation equations over $v \in S$, every edge inside $S$ adds and subtracts the same amount, so $d(S) = f(\delta^{\text{in}}(S)) - f(\delta^{\text{out}}(S)) \le c(\delta^{\text{in}}(S)) - \ell(\delta^{\text{out}}(S))$.

*Sufficiency.* Assume the condition. Remove the lower bounds: let $L(v) = \ell(\delta^{\text{in}}(v)) - \ell(\delta^{\text{out}}(v))$, $d'(v) = d(v) - L(v)$ and $c'(e) = c(e) - \ell(e) \ge 0$. A function $g$ with $0 \le g \le c'$ and $g^{\text{in}}(v) - g^{\text{out}}(v) = d'(v)$ gives the feasible circulation $f = g + \ell$, as shown on the page [circulation problem](/circulation-problem/). Since $\sum_v L(v) = 0$, also $\sum_v d'(v) = 0$. Let $D = \sum_{d'(v) > 0} d'(v)$, which is then also $\sum_{d'(v) < 0} (-d'(v))$.

Build the network $N$: the edges of $G$ with capacities $c'$, a source $s^*$ with an edge $(s^*, v)$ of capacity $-d'(v)$ for each $v$ with $d'(v) < 0$, and a sink $t^*$ with an edge $(v, t^*)$ of capacity $d'(v)$ for each $v$ with $d'(v) > 0$. A flow of value $D$ fills all edges at $s^*$ and $t^*$, and its restriction to $E$ is the required $g$. By the [max-flow min-cut theorem](/max-flow-min-cut-theorem/), it suffices to show that every $s^*$-$t^*$ cut has capacity at least $D$.

Take a cut with source side $\{s^*\} \cup A$, $A \subseteq V$, and let $B = V \setminus A$. Its capacity is
$$\sum_{v \in B,\ d'(v) < 0} (-d'(v)) + \sum_{v \in A,\ d'(v) > 0} d'(v) + c'(\delta^{\text{in}}(B)),$$
since the edges of $G$ from $A$ to $B$ are those entering $B$. Subtract $D = \sum_{d'(v) > 0} d'(v)$: the positive terms in $A$ cancel, and the result is $-\sum_{v \in B} d'(v) + c'(\delta^{\text{in}}(B))$. So the cut has capacity at least $D$ if and only if $d'(B) \le c'(\delta^{\text{in}}(B))$.

Now $d'(B) = d(B) - L(B)$, and summing $L$ over $B$ the edges inside $B$ cancel, so $L(B) = \ell(\delta^{\text{in}}(B)) - \ell(\delta^{\text{out}}(B))$. Also $c'(\delta^{\text{in}}(B)) = c(\delta^{\text{in}}(B)) - \ell(\delta^{\text{in}}(B))$. Substituting, the inequality $d'(B) \le c'(\delta^{\text{in}}(B))$ becomes
$$d(B) - \ell(\delta^{\text{in}}(B)) + \ell(\delta^{\text{out}}(B)) \le c(\delta^{\text{in}}(B)) - \ell(\delta^{\text{in}}(B)),$$
that is, $d(B) \le c(\delta^{\text{in}}(B)) - \ell(\delta^{\text{out}}(B))$, which is the assumed condition for $S = B$. So every cut has capacity at least $D$, a flow of value $D$ exists, and a feasible circulation exists.

*Integrality.* If the data are integers, so are the capacities of $N$, and by the [integrality theorem](/flow-integrality-theorem/) a maximum flow can be chosen integral; then $g$ and $f = g + \ell$ are integral. $\square$

The proof also gives an algorithm and a certificate: one maximum flow either gives a circulation, or its minimum cut gives a set $B$ that violates the condition, the vertices not reachable from $s^*$ in the final residual graph.

## Consequences

- **Gale's supply-demand theorem (1957).** With $\ell \equiv 0$ the condition reads $d(S) \le c(\delta^{\text{in}}(S))$: the net demand of each set can be brought in over its entering edges.
- **[Hall's theorem](/hall-theorem/).** For a bipartite graph with sides $X$ and $Y$, take $d \equiv 0$, edges $s \to x$ with $\ell = c = 1$ for $x \in X$, the graph edges $x \to y$ and edges $y \to t$ with capacity 1, and $t \to s$ with capacity $|X|$. A feasible integral circulation is a matching that covers $X$. For $X' \subseteq X$ and $S = V \setminus (X' \cup N(X'))$, the lower bounds force $|X'|$ units out of $S$, and only the $|N(X')|$ edges $y \to t$ with $y \in N(X')$ enter $S$, so for these sets the condition is Hall's condition $|N(X')| \ge |X'|$, and the other sets give nothing stronger.
- **Feasibility of flows with lower bounds.** An s-t flow with lower bounds and value in a range exists if and only if the condition holds after adding an edge $(t, s)$ with those bounds on the value.
- **Max-flow min-cut back again.** Adding the edge $(t, s)$ with lower bound $k$ and capacity $\infty$, the theorem says a flow of value at least $k$ exists if and only if every s-t cut has capacity at least $k$. So Hoffman's theorem and max-flow min-cut imply each other.
- **Applications.** The certificate explains infeasibility in [airline scheduling](/airline-scheduling/), [survey design](/survey-design-problem/) and matrix rounding: it names a group of vertices whose demand cannot be met.

## Tightness

**The condition is needed for all sets, not only single vertices.** Take edges $a \to b$ of capacity 1, $a \to c$ of capacity 1, $b \to c$ of capacity 2 and $c \to b$ of capacity 2, with $\ell \equiv 0$ and demands $d(a) = -3$, $d(b) = 1$, $d(c) = 2$. Each single vertex passes: $d(a) = -3 \le 0$, $d(b) = 1 \le 1 + 2$ and $d(c) = 2 \le 1 + 2$. But $S = \{b, c\}$ has $d(S) = 3 > c(\delta^{\text{in}}(S)) = 2$: the vertex $a$ must send 3 units over two edges of capacity 1. No circulation exists. The antiparallel edges $b \to c$ and $c \to b$ are separate edges and cancel inside $S$.

**Lower bounds alone.** Edges $a \to b$ with bounds $[2, 3]$ and $b \to a$ with bounds $[0, 1]$ and $d \equiv 0$: for $S = \{a\}$, $0 \le c(b, a) - \ell(a, b) = 1 - 2$ fails. The antiparallel pair is two separate edges; merging them would hide the failure.

**The example of the circulation page.** Demands $a$: $-3$, $b$: $-3$, $c$: 0, $d$: 6, and edges $a b$ $[0, 2]$, $a c$ $[1, 3]$, $b c$ $[0, 2]$, $b d$ $[2, 4]$, $c d$ $[0, 1]$. For $S = \{d\}$, $d(S) = 6 > c(b, d) + c(c, d) - 0 = 5$. The maximum flow of the reduction is 3 against $D = 4$, and the vertices not reachable from $s^*$ at the end are exactly $\{d\}$.

**Zero-capacity edges and empty sets.** An edge with $\ell = c = 0$ adds nothing to either side. For $S = \emptyset$ and $S = V$ the condition reads $0 \le 0$, using $\sum_v d(v) = 0$; that hypothesis is needed, since with demands that do not sum to 0 no circulation exists whatever the cuts are.

**Integrality needs integer data.** With $d(a) = -1/2$, $d(b) = 1/2$ and one edge $a b$ of capacity 1, the only feasible circulation is $f(a, b) = 1/2$.

## History

Alan Hoffman stated and proved the circulation theorem in 1960, in a lecture on applications of linear inequalities to combinatorics, as a common generalization of earlier feasibility theorems: Gale's supply-demand theorem of 1957 and the max-flow min-cut theorem of Ford and Fulkerson. Ford and Fulkerson's 1962 book Flows in Networks gives it with the proof by maximum flow, and Schrijver's Combinatorial Optimization treats it in the chapter on circulations.

## References
