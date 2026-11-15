---
tag: HMHYF4
kind: definition
slug: ord-horn-subclass
name: ORD-Horn subclass
aliases:
- ORD-Horn relations
- ORD-Horn algebra
area: information-retrieval-and-ai-reasoning/qualitative-temporal-and-spatial-reasoning
level: advanced
summary: The 868 interval relations, counting the empty one, that are defined by Horn clauses over endpoint comparisons; path consistency decides their networks.
prereqs: [allens-interval-algebra, horn-clause, point-algebra]
see_also: [nebel-burckert-theorem, interval-algebra-tractable-subclasses, interval-algebra-np-completeness, algebraic-closure, allen-constraint-propagation, horn-sat, point-algebra-consistency]
sources:
  - paper: doi:10.1145/200836.200848
    title: Bernhard Nebel and Hans-Jürgen Bürckert, Reasoning about temporal relations, a maximal tractable subclass of Allen's interval algebra, Journal of the ACM 42(1), 1995
    locator: pages 43 to 66 (ORD clauses, ORD-Horn clauses, the subclass H with 868 relations, its closure properties and the tractability and maximality results)
  - paper: doi:10.1016/b978-1-4832-1447-4.50034-1
    title: Marc Vilain, Henry Kautz and Peter van Beek, Constraint propagation algorithms for temporal reasoning, a revised report, in Readings in Qualitative Reasoning about Physical Systems, Morgan Kaufmann, 1990
    locator: pages 373 to 381 (the pointisable interval relations)
  - paper: doi:10.1016/0004-3702(92)90011-L
    title: Peter van Beek, Reasoning about qualitative temporal information, Artificial Intelligence 58(1-3), 1992
    locator: pages 297 to 326 (the pointisable subclass and its algorithms)
  - paper: doi:10.1145/876638.876639
    title: Andrei Krokhin, Peter Jeavons and Peter Jonsson, Reasoning about temporal relations, the tractable subalgebras of Allen's interval algebra, Journal of the ACM 50(5), 2003
    locator: pages 591 to 640 (ORD-Horn as one of the 18 maximal tractable subalgebras)
  - book: isbn:978-1-84821-252-7
    title: Gérard Ligozat, Qualitative Spatial and Temporal Reasoning, ISTE and Wiley, 2011
    locator: the convex and preconvex interval relations, and their equality with ORD-Horn
---

The ORD-Horn subclass is the set of relations of [Allen's interval algebra](/allens-interval-algebra/) that can be written as a conjunction of [Horn clauses](/horn-clause/) whose literals compare endpoints. Nebel and Bürckert defined it in 1995 and proved that [algebraic closure](/algebraic-closure/) decides consistency of every network whose labels are ORD-Horn, and that no relation can be added without making the problem NP-complete. This page is the definition of the class and how to test membership; the tractability proof is on the page [Nebel-Bürckert theorem](/nebel-burckert-theorem/), and the other maximal classes are on [tractable subclasses of the interval algebra](/interval-algebra-tractable-subclasses/).

## Definition

Write an interval as $X = (x^-, x^+)$ with $x^- < x^+$, and let $Y = (y^-, y^+)$. The *endpoints* of the pair are $x^-, x^+, y^-, y^+$. Following Nebel and Bürckert (1995):

- an **ORD clause** is a disjunction of literals $p \mathrel{\rho} q$, where $p, q$ are endpoints and $\rho \in \{\le, =, \ne\}$;
- an **ORD-Horn clause** is an ORD clause with at most one literal of the form $p \le q$ or $p = q$; all other literals are $p \ne q$;
- an interval relation $R$ is **ORD-Horn** when there is a finite set $\Phi$ of ORD-Horn clauses on $x^-, x^+, y^-, y^+$ such that, for all intervals $X$ and $Y$, $X \mathrel{R} Y$ holds exactly when the endpoints satisfy every clause of $\Phi$.

The set of ORD-Horn relations is written $\mathcal{H}$. The condition $x^- < x^+$ is itself ORD-Horn ($x^- \le x^+$ and $x^- \ne x^+$), and a strict $p < q$ is the pair of clauses $p \le q$ and $p \ne q$, so strict order is allowed.

**Testing membership.** Every set of ORD-Horn clauses on 4 endpoints defines a union of base relations. For a relation $R$, let $\mathrm{hull}(R)$ be the intersection of all clause-defined relations that contain $R$. Then $R \in \mathcal{H}$ exactly when $\mathrm{hull}(R) = R$. There are only finitely many clauses on 4 endpoints, so a program finds $\mathcal{H}$ by checking all 8192 relations. The test of the page [Allen's constraint propagation](/allen-constraint-propagation/) does this.

**Facts** (Nebel and Bürckert 1995; the counts were also checked by machine).

1. $\mathcal{H}$ has 868 relations, counting the empty relation, so 867 non-empty ones, about 10.6% of the 8192.
2. $\mathcal{H}$ contains the 13 base relations and the universal relation, and it is closed under converse, intersection and composition.
3. $\mathcal{H}$ contains the 188 *pointisable* relations (counting the empty one), which are conjunctions of [point algebra](/point-algebra/) constraints between endpoints, and these contain the 83 *convex* relations, which use no $\ne$.
4. Algebraic closure decides consistency of networks over $\mathcal{H}$, and $\mathcal{H}$ is maximal: for every relation $R \notin \mathcal{H}$, consistency over $\mathcal{H} \cup \{R\}$ is NP-complete.
5. $\mathcal{H}$ equals the class of *preconvex* relations of Ligozat, defined geometrically.

## Examples and non-examples

**A convex relation: $\{b, m\}$.** It is the single clause $x^+ \le y^-$: $X$ ends at or before the start of $Y$.

**A pointisable relation that is not convex: $\{d, o\}$.** It is in $\mathcal{H}$ and is a conjunction of point relations, but one of them is $\ne$, so it is not convex.

**ORD-Horn but not pointisable: $\{o, s, fi\}$.** It is defined by

$$x^- \le y^-,\quad x^+ \le y^+,\quad y^- \le x^+,\quad y^- \ne x^+,\quad (x^- \ne y^- \lor x^+ \ne y^+).$$

The first four clauses allow o, s, fi and eq; the last clause, with no positive literal, removes eq. It needs a disjunction, so it is not a conjunction of point relations, but the disjunction has no positive literal, so it is Horn.

**Larger members.** $\{b, m, o\}$, $\{s, eq, si\}$, $\{m, o, fi\}$ and $\{b, di, o, m, fi\}$ are ORD-Horn.

**Non-example: $\{b, bi\}$.** "$X$ is before or after $Y$" is $x^+ < y^- \lor y^+ < x^-$. It needs a clause with two order literals; its hull is $\{b, o, d, di, oi, bi\}$. It is one of the relations of the NP-hardness reduction ([NP-completeness of the interval algebra](/interval-algebra-np-completeness/)).

**Non-example: $\{b, d\}$.** "Before or during" is not ORD-Horn: every clause set that both b and d satisfy also allows o, so the hull of $\{b, d\}$ is $\{b, o, d\}$, which is ORD-Horn.

**Non-example: $\{d, di, oi, si, f\}$.** It is not ORD-Horn either, and by fact 4 adding it to $\mathcal{H}$ makes consistency NP-complete.

### Common errors

- Counting 868 as the number of non-empty relations. The count includes the empty relation.
- Confusing ORD-Horn with pointisable. Pointisable relations are conjunctions of single literals; ORD-Horn allows disjunctions of $\ne$ literals with one positive literal.
- Treating $p = q$ as two positive literals. It is one literal; a clause $p = q \lor r \ne s$ is the same as the two Horn clauses $p \le q \lor r \ne s$ and $q \le p \lor r \ne s$.

## Related definitions

- [Horn clause](/horn-clause/): the clause shape that gives the class its name; Horn satisfiability is in P by [unit propagation](/unit-propagation/).
- [Point algebra](/point-algebra/): the relations that ORD-Horn clauses are built from.
- [Nebel-Bürckert theorem](/nebel-burckert-theorem/): tractability and maximality of $\mathcal{H}$.
- [Tractable subclasses of the interval algebra](/interval-algebra-tractable-subclasses/): the 17 other maximal tractable classes.
- [Algebraic closure](/algebraic-closure/): the procedure that decides networks over $\mathcal{H}$.

## References
