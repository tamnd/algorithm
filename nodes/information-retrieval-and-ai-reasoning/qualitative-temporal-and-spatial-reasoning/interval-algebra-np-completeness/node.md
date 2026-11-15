---
tag: HEBZH8
kind: theorem
slug: interval-algebra-np-completeness
name: NP-completeness of the interval algebra
aliases:
- NP-completeness of interval algebra consistency
area: information-retrieval-and-ai-reasoning/qualitative-temporal-and-spatial-reasoning
level: advanced
summary: Deciding whether a network of Allen interval relations has a solution is NP-complete, by a reduction from 3-SAT; algebraic closure is therefore not a complete test.
prereqs: [allens-interval-algebra, qualitative-constraint-network, 3-sat, np-complete]
see_also: [nebel-burckert-theorem, interval-algebra-tractable-subclasses, algebraic-closure, allen-constraint-propagation, ord-horn-subclass, polynomial-time-reduction, rectangle-algebra]
sources:
  - paper: "Marc Vilain and Henry Kautz, Constraint propagation algorithms for temporal reasoning, Proceedings of AAAI-86, 1986, pages 377 to 382"
    locator: the theorem that consistency of interval networks is NP-hard, and the incompleteness of propagation
  - paper: doi:10.1016/b978-1-4832-1447-4.50034-1
    title: Marc Vilain, Henry Kautz and Peter van Beek, Constraint propagation algorithms for temporal reasoning, a revised report, in Readings in Qualitative Reasoning about Physical Systems, Morgan Kaufmann, 1990
    locator: pages 373 to 381 (the reduction from 3-SAT with variable and clause gadgets)
  - paper: doi:10.1145/200836.200848
    title: Bernhard Nebel and Hans-Jürgen Bürckert, Reasoning about temporal relations, a maximal tractable subclass of Allen's interval algebra, Journal of the ACM 42(1), 1995
    locator: pages 43 to 66 (membership in NP, and the relations that make the problem hard)
  - paper: doi:10.1145/876638.876639
    title: Andrei Krokhin, Peter Jeavons and Peter Jonsson, Reasoning about temporal relations, the tractable subalgebras of Allen's interval algebra, Journal of the ACM 50(5), 2003
    locator: pages 591 to 640 (every subclass of the interval algebra is either tractable or NP-complete)
  - paper: doi:10.1145/182.358434
    title: James F. Allen, Maintaining knowledge about temporal intervals, Communications of the ACM 26(11), 1983
    locator: pages 832 to 843 (the interval algebra and its incomplete propagation)
---

This theorem says that the consistency problem of [Allen's interval algebra](/allens-interval-algebra/) is [NP-complete](/np-complete/): given a [qualitative constraint network](/qualitative-constraint-network/) on $n$ intervals, with a set of the 13 base relations on each pair, deciding whether some intervals on the real line satisfy every label is as hard as [3-SAT](/3-sat/). Vilain and Kautz proved hardness in 1986. The theorem explains why [Allen's constraint propagation](/allen-constraint-propagation/) and [algebraic closure](/algebraic-closure/) can accept a network with no solution, and it is the starting point for the search for tractable subclasses, settled by the [Nebel-Bürckert theorem](/nebel-burckert-theorem/) for ORD-Horn and by the [classification of tractable subclasses](/interval-algebra-tractable-subclasses/).

## Statement

**The problem.** $\mathrm{CSP}(\mathrm{IA})$: the input is a network on intervals $0, \ldots, n-1$ with a label $C_{ij} \subseteq \{b, m, o, s, d, f, eq, fi, di, si, oi, mi, bi\}$ on each pair, given as a 13-bit mask, so the input size is $\Theta(n^2)$. A solution assigns to each interval $i$ two reals $x_i^- < x_i^+$ so that the base relation between $i$ and $j$ is in $C_{ij}$ for all $i < j$.

> **Theorem.** $\mathrm{CSP}(\mathrm{IA})$ is NP-complete. Hardness holds already for networks whose labels are among $\{d\}$, $\{di\}$, $\{m, mi\}$, $\{b, bi\}$, $\{m, s, bi\}$ and $\{b, bi, m, mi\}$.

The reduction below is from 3-SAT with *exactly three distinct literals* in every clause, which is NP-complete: a clause with fewer literals can be padded with new variables in the usual way.

## In plain words

Intervals on a line can stand for true and false. Put one short interval in the middle. For each yes-or-no variable, place a pair of intervals so that one of them must lie left of the middle and the other right of it; left means false, right means true. For each clause, add a long interval around the middle and one helper interval per literal, each wrapped around its literal. A helper of a false literal must sit at the left end of the long interval, and there is room for at most two helpers there, since helpers may touch but not overlap. So every clause needs a true literal. That turns any satisfiability puzzle into an interval puzzle of about the same size, so no fast method can solve every interval puzzle unless it can solve every such puzzle.

## Proof

**Membership in NP.** A solution can be replaced by one whose $2n$ endpoints are integers in $\{0, \ldots, 2n-1\}$, since the base relations depend only on the order of the endpoints: map each endpoint to the number of distinct endpoint values below it. So a certificate is a list of $2n$ such integers. The verifier checks $x_i^- < x_i^+$ for each $i$ and computes the base relation of each pair from 4 comparisons, in $O(n^2)$ time.

**Hardness.** Let $\varphi$ be a 3-CNF formula with variables $v_1, \ldots, v_k$ and clauses $c_1, \ldots, c_m$, each with exactly 3 distinct literals. Build a network with these intervals and labels, where "$X \mathrel{R} Y$" means the label of $(X, Y)$:

- a middle interval $M$;
- for each variable $v$: intervals $X_v$, $P_v$ and $N_v$ with $M \mathrel{\{d\}} X_v$, $P_v \mathrel{\{m, mi\}} X_v$, $N_v \mathrel{\{m, mi\}} X_v$ and $P_v \mathrel{\{b, bi\}} N_v$; the interval of the literal $v$ is $P_v$ and that of $\neg v$ is $N_v$;
- for each clause $c$: an interval $Q_c$ with $Q_c \mathrel{\{di\}} M$, and for each literal $\ell$ of $c$, with literal interval $L$, a placeholder $F_{c,\ell}$ with $F_{c,\ell} \mathrel{\{di\}} L$, $F_{c,\ell} \mathrel{\{b, bi\}} M$ and $F_{c,\ell} \mathrel{\{m, s, bi\}} Q_c$; the three placeholders of $c$ are pairwise $\{b, bi, m, mi\}$.

All other pairs are universal. There are $1 + 3k + 4m$ intervals, so the network is built in polynomial time. Call a literal interval *true* if it lies after $M$ and *false* if it lies before $M$.

*Claim 1 (variables).* In every solution, for each $v$ exactly one of $P_v$, $N_v$ is true. Both meet $X_v$ on one side or the other. They cannot both meet it from the same side, because then they would share an endpoint, which $\{b, bi\}$ forbids. So one ends where $X_v$ starts and the other starts where $X_v$ ends. Since $M$ lies strictly inside $X_v$, the first is before $M$ and the second after $M$.

*Claim 2 (placeholders).* Let $F = F_{c,\ell}$ with literal interval $L$. If $L$ is false, $F$ contains $L$ and so starts before $M$; with $\{b, bi\}$ this gives $F \mathrel{b} M$, and since $M$ lies inside $Q_c$, $F \mathrel{bi} Q_c$ is impossible, so $F \mathrel{m} Q_c$ or $F \mathrel{s} Q_c$.

*Claim 3 (clauses).* At most two placeholders of a clause are in $\{m, s\}$ with $Q_c$. Two placeholders with $m$ both end at the start of $Q_c$, and two with $s$ both start at the start of $Q_c$. In either case they share an endpoint in a way that $\{b, bi, m, mi\}$ forbids. So a third one has no place. With Claim 2, every clause has a true literal, and Claim 1 makes the truth values a well-defined assignment. So a solution gives a satisfying assignment.

*Converse.* Take a satisfying assignment, and order the literal intervals so that all are pairwise disjoint: the false ones in a row left of $M$, the true ones in a row right of $M$, each $X_v$ stretching from the end of its false interval to the start of its true one. Let $M = (0, 1)$. For a clause $c$ with one false literal $L_1$, start $Q_c$ just after the end of $L_1$ and put $F_{c,\ell_1}$ around $L_1$, ending at the start of $Q_c$. With a second false literal $L_2$ further right, start $Q_c$ between $L_1$ and $L_2$ instead, and let $F_{c,\ell_2}$ start with $Q_c$ and end between $L_2$ and $M$. End $Q_c$ just after $M$, and wrap each true literal in its own disjoint placeholder after $Q_c$ ends. The placeholders of one clause meet or are disjoint, every label holds, and the network is consistent. $\square$

The construction and both directions were checked by machine on random 3-CNF formulas with up to 3 variables, including the unsatisfiable formula with all 8 clauses on 3 variables, whose network has 42 intervals.

## Consequences

- **Propagation is incomplete.** Unless P = NP, no polynomial algorithm decides all interval networks, so [algebraic closure](/algebraic-closure/) must accept some networks without a solution. The 42-interval network of the unsatisfiable formula above is one: algebraic closure leaves no label empty. A smaller one has 4 intervals: $0 \mathrel{\{o, si\}} 1$, $0 \mathrel{\{fi, si\}} 2$, $0 \mathrel{\{o, fi\}} 3$, $1 \mathrel{\{m, mi\}} 2$, $1 \mathrel{\{b, f\}} 3$, $2 \mathrel{\{b, s\}} 3$ is closed and has no solution.
- **Search is needed.** Complete solvers backtrack over refinements of the labels, with propagation at each node; see [Allen's constraint propagation](/allen-constraint-propagation/).
- **Related problems are hard.** Computing the minimal network, or deciding whether a base relation is possible between two intervals, is NP-hard, since either decides consistency. Calculi that contain the interval algebra, such as the [rectangle algebra](/rectangle-algebra/), inherit the hardness.
- **Tractable subclasses.** The labels used by the reduction, such as $\{b, bi\}$ and $\{m, mi\}$, must be avoided by any tractable subclass. This leads to the [ORD-Horn subclass](/ord-horn-subclass/) and the [classification of tractable subclasses](/interval-algebra-tractable-subclasses/).

## Tightness

- **Membership is exact.** The problem is in NP for all 8192 relations, so the theorem is not about a harder class.
- **Small labels are enough, but not single ones.** The reduction uses labels of at most 4 base relations. With the 13 base relations alone the problem is in P, since algebraic closure decides atomic networks, so hardness needs some disjunctive labels.
- **Dichotomy.** Krokhin, Jeavons and Jonsson (2003) proved that every subset of the 8192 relations gives a problem that is either in P or NP-complete, and listed the 18 maximal tractable subclasses. The ORD-Horn subclass, 868 relations, is the only one of them that contains all 13 base relations.
- **Three distinct literals.** The clause gadget needs them. With two placeholders, both may be false, one meeting $Q_c$ and one starting it; and two placeholders around the same literal interval cannot be disjoint.

## History

Allen (1983) gave the algebra and noted that his propagation is incomplete. Vilain and Kautz (1986) proved that consistency is NP-hard, and the revised report of Vilain, Kautz and van Beek (1990) gave the reduction from 3-SAT in detail. Nebel and Bürckert (1995) found the maximal tractable ORD-Horn subclass, and Krokhin, Jeavons and Jonsson (2003) completed the classification of all subclasses.

## References
