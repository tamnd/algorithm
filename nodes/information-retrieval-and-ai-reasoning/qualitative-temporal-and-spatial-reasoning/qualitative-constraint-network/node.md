---
tag: N9PK9N
kind: definition
slug: qualitative-constraint-network
name: Qualitative constraint network
aliases:
- QCN
- qualitative network
area: information-retrieval-and-ai-reasoning/qualitative-temporal-and-spatial-reasoning
level: advanced
summary: Variables over an infinite domain with a relation of a qualitative calculus on each pair; it is consistent when some assignment satisfies every relation.
prereqs: [qualitative-constraint-calculus, constraint-satisfaction-problem]
see_also: [algebraic-closure, allen-constraint-propagation, point-algebra-consistency, interval-algebra-np-completeness, composition-table, nebel-burckert-theorem, constraint-graph]
sources:
  - paper: doi:10.1145/3038927
    title: Frank Dylla and others, A survey of qualitative spatial and temporal calculi, algebraic and computational properties, ACM Computing Surveys 50(1), 2017
    locator: pages 1 to 39 (constraint networks, scenarios, algebraic closure, and the consistency problem of each calculus)
  - paper: doi:10.1007/11564751_40
    title: Jochen Renz and Gérard Ligozat, Weak composition for qualitative spatial and temporal reasoning, CP 2005, Lecture Notes in Computer Science 3709, Springer, 2005
    locator: pages 534 to 548 (networks, refinements, scenarios and closure under weak composition)
  - paper: doi:10.1016/0004-3702(92)90011-L
    title: Peter van Beek, Reasoning about qualitative temporal information, Artificial Intelligence 58(1-3), 1992
    locator: pages 297 to 326 (consistent scenarios and minimal labels of point and interval networks)
  - paper: doi:10.1145/182.358434
    title: James F. Allen, Maintaining knowledge about temporal intervals, Communications of the ACM 26(11), 1983
    locator: pages 832 to 843 (networks of interval relations)
  - book: isbn:9781558608900
    title: Rina Dechter, Constraint Processing, Morgan Kaufmann, 2003
    locator: Chapter 12, Temporal constraint networks (qualitative networks and their minimal networks)
---

A qualitative constraint network is the input of qualitative reasoning: a set of variables, each standing for an object of the domain of a [qualitative constraint calculus](/qualitative-constraint-calculus/), with a relation of the calculus on each pair, such as "interval 1 is before or meets interval 2". It is a binary [constraint satisfaction problem](/constraint-satisfaction-problem/) whose domain is infinite, so it cannot be solved by trying values. Instead, the reasoning works on the labels with the [composition table](/composition-table/). This page defines the network and the notions used with it: solution, consistency, scenario, refinement, the minimal network and algebraic closure.

## Definition

Fix a calculus with domain $D$, base relations $\mathcal{B}$ and weak composition $\diamond$. A *qualitative constraint network* $N = (V, C)$ on $n$ variables has

- variables $V = \{v_0, \ldots, v_{n-1}\}$, each ranging over $D$;
- a *label* $C_{ij} \subseteq \mathcal{B}$ for each ordered pair, with $C_{ji} = C_{ij}^{\smile}$ and $C_{ii} \subseteq \{\mathrm{id}\}$.

A pair that the input does not mention gets the universal label $\mathcal{B}$. Then

- a **solution** is a map $\sigma : V \to D$ with $(\sigma(v_i), \sigma(v_j)) \in C_{ij}$ for all $i, j$, where a label is read as the union of its base relations;
- $N$ is **consistent** when it has a solution;
- $N'$ is a **refinement** of $N$, written $N' \subseteq N$, when $C'_{ij} \subseteq C_{ij}$ for all $i, j$;
- a **scenario** (or atomic network) is a network in which every label is a single base relation; every solution $\sigma$ fixes the scenario of the base relations that hold between its values;
- the **minimal network** of $N$ has the label $M_{ij} = \{b \in C_{ij} : \text{some solution has } (\sigma(v_i), \sigma(v_j)) \in b\}$;
- $N$ is **algebraically closed** when $C_{ij} \subseteq C_{ik} \diamond C_{kj}$ for all $i, j, k$.

**Facts.**

1. $N$ is consistent exactly when one of its scenarios is consistent, since a solution fixes one.
2. The minimal network is a refinement with the same solutions, and it is algebraically closed, because the table is sound.
3. The [algebraic closure](/algebraic-closure/) of $N$, the largest algebraically closed refinement, has the same solutions as $N$. If it has an empty label, $N$ is inconsistent.
4. For a set $S$ of relations, $\mathrm{CSP}(S)$ is the problem of deciding consistency of networks whose labels are all in $S$. A subclass $S$ is called tractable when $\mathrm{CSP}(S)$ is in P.

## Examples and non-examples

**An interval network that closure solves.** Take intervals 0, 1, 2, 3 with $0 \mathrel{\{b, m\}} 1$, $1 \mathrel{\{b, m\}} 2$, $2 \mathrel{\{d\}} 3$ and $0 \mathrel{\{o, di, bi\}} 3$, in [Allen's interval algebra](/allens-interval-algebra/). Its algebraic closure has $C_{02} = \{b\}$, $C_{03} = \{o\}$ and $C_{13} = \{d\}$, and this is also its minimal network. The trace is on the [algebraic closure](/algebraic-closure/) page.

**Closed but inconsistent.** The interval network $0 \mathrel{\{o, si\}} 1$, $0 \mathrel{\{fi, si\}} 2$, $0 \mathrel{\{o, fi\}} 3$, $1 \mathrel{\{m, mi\}} 2$, $1 \mathrel{\{b, f\}} 3$, $2 \mathrel{\{b, s\}} 3$ is algebraically closed, has no empty label, and has no solution. Closure is not a complete test for interval networks, as [NP-completeness of the interval algebra](/interval-algebra-np-completeness/) predicts.

**Closed but not minimal.** The point network $x_0 \le x_1$, $x_0 \le x_2$, $x_1 \le x_3$, $x_2 \le x_3$ and $x_1 \ne x_2$ is consistent and algebraically closed, with $C_{03} = \{<, =\}$. But $x_0 = x_3$ would force $x_1 = x_2$, so the minimal label is $C_{03} = \{<\}$. This is why minimal labels of point networks with $\ne$ need more than closure (van Beek 1992).

**A scenario.** The atomic network $0 \mathrel{\{m\}} 1$, $1 \mathrel{\{m\}} 2$, $0 \mathrel{\{b\}} 2$ is consistent, for example with the intervals $(0, 1)$, $(1, 2)$ and $(2, 3)$. The atomic network $0 \mathrel{\{m\}} 1$, $1 \mathrel{\{m\}} 2$, $0 \mathrel{\{m\}} 2$ is not, because $m \diamond m = \{b\}$.

**Non-example: a ternary constraint.** "Interval 2 lies between intervals 0 and 1" relates three objects. It is not a label of a binary network; it needs a ternary calculus or extra variables.

**Non-example: a metric bound.** "Interval 1 starts at most 5 minutes after interval 0 ends" uses a number. It belongs to the [simple temporal problem](/simple-temporal-problem/), not to a qualitative network.

### Common errors

- Storing only one direction of a label and forgetting that the other direction is its converse, not the same set.
- Reading "consistent" as "algebraically closed". Closure is necessary; it is sufficient only for some subclasses.
- Treating the universal label as "no information about the pair" and then skipping the pair in propagation. Closure can still shrink it.

## Related definitions

- [Qualitative constraint calculus](/qualitative-constraint-calculus/): the relations that the labels come from.
- [Composition table](/composition-table/): the operation used to tighten labels.
- [Algebraic closure](/algebraic-closure/) and [Allen's constraint propagation](/allen-constraint-propagation/): computing the closed refinement.
- [Point algebra consistency](/point-algebra-consistency/): an exact $O(n^2)$ test for point networks.
- [Constraint graph](/constraint-graph/): the graph of the pairs with a label that is not universal.
- [Nebel-Bürckert theorem](/nebel-burckert-theorem/): for ORD-Horn labels, closure decides consistency.

## References
