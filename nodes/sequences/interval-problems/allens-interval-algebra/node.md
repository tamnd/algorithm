---
tag: 0W86N9
kind: concept
slug: allens-interval-algebra
name: Allen's interval algebra
aliases:
- Allen's temporal interval relations
area: sequences/interval-problems
level: core
summary: The thirteen mutually exclusive qualitative relations between two intervals.
prereqs: [total-order, interval-containment]
see_also: [path-consistency, constraint-satisfaction-problem, simple-temporal-problem, temporal-logic, interval-list-intersection, interval-containment, helly-property-intervals, interval-overlap-query]
sources:
  - paper: doi:10.1145/182.358434
    title: "James F. Allen, Maintaining knowledge about temporal intervals, Communications of the ACM 26(11) (1983), pages 832 to 843"
    locator: the thirteen relations, the transitivity table and the constraint propagation algorithm
  - paper: "Marc Vilain and Henry Kautz, Constraint propagation algorithms for temporal reasoning, Proceedings of the Fifth National Conference on Artificial Intelligence (AAAI-86), 1986, pages 377 to 382"
    locator: the NP-completeness of consistency for networks over the full interval algebra
  - paper: doi:10.1145/200836.200848
    title: "Bernhard Nebel and Hans-Juergen Buerckert, Reasoning about temporal relations, a maximal tractable subclass of Allen's interval algebra, Journal of the ACM 42(1) (1995), pages 43 to 66"
    locator: the ORD-Horn subclass, on which path consistency decides consistency
---

Allen's interval algebra describes how two intervals of time can lie relative to each other by thirteen basic relations, such as "before", "meets", "overlaps" and "during". For two intervals with positive length, exactly one of the thirteen holds, and each is fixed by how the four end points compare. Unions of basic relations express partial knowledge, and a composition table infers the relation between $X$ and $Z$ from those between $X$ and $Y$ and between $Y$ and $Z$; deciding whether a network of such constraints is consistent is NP-complete in general and polynomial on large subclasses. The relation "meets" is where end point types matter: it says that one interval ends exactly where the next starts, which for closed intervals is one shared point and for half-open intervals is no shared point at all.

## In plain words

Two meetings in one day can relate in only a few ways. One can end before the other starts, with a gap. One can end exactly when the other starts. They can overlap partly. One can start with the other but end sooner, lie strictly inside it, or end with it. They can be the very same time. Turn each of the first six around and you have the other side, so there are thirteen cases in all.

These words let you reason without clock times. If lunch is during the conference, and the keynote is before lunch, then the keynote is before lunch ends, but it may be before the conference, overlap it, or lie inside it. A table of such rules lets a computer draw these conclusions and find contradictions.

## The idea

**Intervals and end points.** An interval is a pair $X = (x^-, x^+)$ of points of a [total order](/total-order/) with $x^- < x^+$. The algebra is about the order of end points only; it does not say whether an interval contains its end points. As sets, the usual reading is the half-open interval $[x^-, x^+)$, under which "meets" means that the two sets are disjoint and their union is an interval. Under the closed reading $[x^-, x^+]$, "meets" means that they share exactly one point. Each relation below is defined by end point comparisons, so it is the same under either reading; what changes is the set operation that matches it.

**The thirteen basic relations.** For $X = (x^-, x^+)$ and $Y = (y^-, y^+)$:

| relation | symbol | end points | inverse |
|---|---|---|---|
| $X$ before $Y$ | b | $x^+ < y^-$ | after, bi |
| $X$ meets $Y$ | m | $x^+ = y^-$ | met by, mi |
| $X$ overlaps $Y$ | o | $x^- < y^- < x^+ < y^+$ | overlapped by, oi |
| $X$ starts $Y$ | s | $x^- = y^-$, $x^+ < y^+$ | started by, si |
| $X$ during $Y$ | d | $y^- < x^-$, $x^+ < y^+$ | contains, di |
| $X$ finishes $Y$ | f | $y^- < x^-$, $x^+ = y^+$ | finished by, fi |
| $X$ equals $Y$ | eq | $x^- = y^-$, $x^+ = y^+$ | itself |

The inverse of a relation $R$ holds between $X$ and $Y$ exactly when $R$ holds between $Y$ and $X$.

**Why exactly thirteen.** Since $x^- < x^+$ and $y^- < y^+$, the relation is fixed by where $y^-$ and $y^+$ lie among the five places that $x^-$ and $x^+$ cut the line into: before $x^-$, at $x^-$, strictly between, at $x^+$, after $x^+$. $y^-$ cannot be after $x^+$ while $y^+$ is earlier, so we count the pairs of places $(p, q)$ with $p \le q$ for $y^- \le y^+$, excluding $p = q$ when that place is a single point, since $y^- < y^+$. There are $15$ pairs with $p \le q$ among five places, minus 2 for the two single points: 13. Every input pair falls in exactly one case, so the basic relations are jointly exhaustive and pairwise disjoint.

**General relations.** A general relation is a set of basic relations, read as a disjunction: $X \{b, m\} Y$ says that $X$ ends at or before the start of $Y$. There are $2^{13} = 8192$ of them. They are closed under union, intersection, inverse and composition.

**Composition.** For basic relations $R$ and $S$, the composition $R \circ S$ is the set of basic relations $T$ such that some intervals have $X \mathbin{R} Y$, $Y \mathbin{S} Z$ and $X \mathbin{T} Z$. Allen tabulated it as a $13 \times 13$ table. Some entries:

| $R$ | $S$ | $R \circ S$ |
|---|---|---|
| m | m | $\{b\}$ |
| b | m | $\{b\}$ |
| d | d | $\{d\}$ |
| s | f | $\{d\}$ |
| o | o | $\{b, m, o\}$ |
| o | d | $\{o, s, d\}$ |
| m | mi | $\{f, fi, eq\}$ |
| d | di | all 13 |

For example, if $X$ meets $Y$ and $Y$ meets $Z$, then $x^+ = y^- < y^+ = z^-$, so $X$ is before $Z$. If $X$ overlaps $Y$ and $Y$ overlaps $Z$, then $x^- < y^- < z^-$ and $x^+ < y^+$, and $x^+$ can lie before, at or after $z^-$, which gives b, m or o.

**Networks and consistency.** A temporal network has a variable for each interval and a general relation on some pairs. It is consistent if there are intervals that satisfy all constraints. This is a [constraint satisfaction problem](/constraint-satisfaction-problem/) with infinite domains. Allen's algorithm enforces [path consistency](/path-consistency/): it replaces the relation $R_{XZ}$ by $R_{XZ} \cap (R_{XY} \circ R_{YZ})$ until nothing changes, in $O(n^3)$ composition steps for $n$ intervals. It finds every contradiction among three intervals, but Vilain and Kautz proved that consistency for the full algebra is NP-complete, so this polynomial method cannot find all contradictions unless P = NP. Nebel and Bürckert found the ORD-Horn subclass, 868 of the 8192 relations, on which path consistency decides consistency; it is the largest tractable subclass that contains all thirteen basic relations.

## Examples

**Touching intervals.** For $X = (1, 3)$ and $Y = (3, 5)$ as end point pairs, $X$ meets $Y$. As closed sets, $[1, 3] \cap [3, 5] = \{3\}$; as half-open sets, $[1, 3) \cap [3, 5) = \emptyset$ and $[1, 3) \cup [3, 5) = [1, 5)$. The relation is the same, and only the set reading differs.

**The relations as interval problems.** Several problems on this site test a union of basic relations:

- [Interval containment](/interval-containment/): $X \subseteq Y$, as sets, is $X \{s, d, f, eq\} Y$.
- Overlap of half-open intervals, the test of an [interval overlap query](/interval-overlap-query/), is every relation except b, m, bi and mi. For closed intervals, m and mi also count as overlap.
- [Interval list intersection](/interval-list-intersection/) outputs a piece for each pair that is not in b or bi; for half-open intervals, m and mi pairs give empty pieces.

**A contradiction found by composition.** Take the constraints $X \{b\} Y$, $Y \{b\} Z$ and $Z \{b, m\} X$. Path consistency computes $R_{XZ} \subseteq b \circ b = \{b\}$, while the constraint from $Z$ to $X$ says $X \{bi, mi\} Z$. The intersection is empty, so the network is inconsistent.

**Partial knowledge.** "The keynote is before lunch, and lunch is during the conference": $K \{b\} L$ and $L \{d\} C$. The composition $b \circ d$ is $\{b, m, o, s, d\}$, so the keynote may start before the conference or with it or inside it, but it ends before the conference ends.

## Where it is used

- **Temporal reasoning in artificial intelligence.** Planning, scheduling and natural language understanding store facts such as "the meeting overlaps lunch" and infer others with the composition table.
- **Temporal databases and logic.** Query languages for time-stamped data use the thirteen relations as predicates, and some [temporal logics](/temporal-logic/) of intervals take them as modalities.
- **Video and event analysis.** Event detection in video and logs describes patterns of events with these relations.
- **Qualitative spatial reasoning.** The same construction on each axis gives the rectangle algebra, with $13^2$ basic relations between two axis-parallel rectangles.
- **Interval algorithms.** The relation names give a precise vocabulary for the tests in interval algorithms, especially for the touching case "meets", which is a frequent source of errors.

## References
