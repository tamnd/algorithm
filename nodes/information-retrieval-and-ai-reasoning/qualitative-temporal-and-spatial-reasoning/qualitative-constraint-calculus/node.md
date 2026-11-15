---
tag: 2CP170
kind: definition
slug: qualitative-constraint-calculus
name: Qualitative constraint calculus
aliases:
- qualitative calculus
- qualitative spatial and temporal calculus
area: information-retrieval-and-ai-reasoning/qualitative-temporal-and-spatial-reasoning
level: advanced
summary: A finite set of jointly exhaustive, pairwise disjoint base relations on an infinite domain, closed under converse, with unions as relations and a weak composition.
prereqs: [constraint-satisfaction-problem]
see_also: [point-algebra, allens-interval-algebra, region-connection-calculus-rcc8, rectangle-algebra, cardinal-direction-calculus, composition-table, qualitative-constraint-network, algebraic-closure]
sources:
  - paper: doi:10.1007/978-3-540-28633-2_8
    title: Gérard Ligozat and Jochen Renz, What is a qualitative calculus? A general framework, PRICAI 2004, Lecture Notes in Computer Science 3157, Springer, 2004
    locator: pages 53 to 64 (partition schemes, weak composition, and the algebras they give)
  - paper: doi:10.1007/11564751_40
    title: Jochen Renz and Gérard Ligozat, Weak composition for qualitative spatial and temporal reasoning, CP 2005, Lecture Notes in Computer Science 3709, Springer, 2005
    locator: pages 534 to 548 (weak and strong composition, and when algebraic closure decides consistency)
  - paper: doi:10.1145/3038927
    title: Frank Dylla and others, A survey of qualitative spatial and temporal calculi, algebraic and computational properties, ACM Computing Surveys 50(1), 2017
    locator: pages 1 to 39 (the definition of a qualitative calculus, the algebraic properties of many calculi, and a table of them)
  - book: isbn:978-1-84821-252-7
    title: Gérard Ligozat, Qualitative Spatial and Temporal Reasoning, ISTE and Wiley, 2011
    locator: Chapters 1 and 11 (the point and interval calculi, and the general notion of a qualitative formalism)
  - paper: doi:10.1145/182.358434
    title: James F. Allen, Maintaining knowledge about temporal intervals, Communications of the ACM 26(11), 1983
    locator: pages 832 to 843 (the first calculus of this kind, for time intervals)
---

A qualitative constraint calculus is a small, fixed vocabulary of relations, such as "before", "meets" or "overlaps", that describes how two objects of an infinite domain lie relative to each other without numbers. It has a finite set of *base relations*, exactly one of which holds between any two objects, and every set of base relations is a relation of the calculus, read as "one of these". Composition is replaced by a finite table, so reasoning works on symbols. This page defines the general notion; [Allen's interval algebra](/allens-interval-algebra/), the [point algebra](/point-algebra/) and [RCC8](/region-connection-calculus-rcc8/) are the main instances, and a set of constraints in a calculus is a [qualitative constraint network](/qualitative-constraint-network/).

## Definition

Let $D$ be a set, the *domain*, usually infinite: the real numbers, the intervals of the real line, the regions of the plane. Following Ligozat and Renz (2004), a *partition scheme* on $D$ is a finite set $\mathcal{B} = \{B_1, \ldots, B_m\}$ of binary relations on $D$, the *base relations*, such that

1. **jointly exhaustive:** $B_1 \cup \cdots \cup B_m = D \times D$;
2. **pairwise disjoint:** $B_a \cap B_b = \emptyset$ for $a \ne b$;
3. **identity:** the identity relation $\{(x, x) : x \in D\}$ is one of the $B_a$;
4. **converse:** for each $B_a$, its converse $B_a^{\smile} = \{(y, x) : (x, y) \in B_a\}$ is also a base relation.

The first two are often called JEPD. A *relation* of the calculus is a union of base relations, written as the set of their names; there are $2^m$ relations, from the empty relation $\emptyset$ to the universal relation $D \times D$. Union, intersection, complement and converse of relations are relations again. The usual composition $R \circ S = \{(x, z) : \exists y,\ (x, y) \in R,\ (y, z) \in S\}$ need not be a union of base relations, so the calculus uses *weak composition*:

$$R \diamond S = \bigcup \{B_c : B_c \cap (R \circ S) \ne \emptyset\},$$

the smallest relation of the calculus that contains $R \circ S$. It distributes over unions, so it is fixed by the $m \times m$ values $B_a \diamond B_b$, the [composition table](/composition-table/). Composition is *strong* when $R \diamond S = R \circ S$ for all relations; then the relations form a relation algebra in the sense of Tarski. With weak composition they form, in general, only a non-associative algebra (Ligozat and Renz 2004).

The *qualitative calculus* is the set of $2^m$ relations with these operations. Its reasoning problem is consistency of [networks](/qualitative-constraint-network/): given variables over $D$ and a relation on some pairs, is there an assignment that satisfies all of them?

## Examples and non-examples

**Point algebra.** $D = \mathbb{R}$ or $\mathbb{Q}$, with the base relations $<$, $=$ and $>$. Composition is strong: between $x < z$ there is always a $y$. The relations are the 8 subsets, such as $\{<, =\}$ for $\le$ and $\{<, >\}$ for $\ne$. See the [point algebra](/point-algebra/).

**Point algebra over the integers.** With $D = \mathbb{Z}$ and the same 3 base relations, the scheme is still JEPD, but composition is only weak. The pairs in $< \circ <$ are those with $z \ge x + 2$, which is not a union of base relations, while $< \diamond < = \{<\}$. The table is the same as over $\mathbb{R}$. A network of the calculus has an integer solution exactly when it has a real one, because only the order of the values matters, so the weaker composition does not change the answers here.

**Allen's interval algebra.** $D$ is the set of pairs $(x^-, x^+)$ of reals with $x^- < x^+$, with 13 base relations given by the order of the 4 endpoints. Composition is strong, and there are $2^{13} = 8192$ relations. See [Allen's interval algebra](/allens-interval-algebra/).

**Region calculi.** [RCC8](/region-connection-calculus-rcc8/) has 8 base relations between regions, such as "disconnected", "externally connected" and "tangential proper part"; [RCC5](/rcc5/) merges some of them into 5. For the standard models of regions, their tables give weak composition (Renz and Ligozat 2005).

**Products.** The [cardinal direction calculus](/cardinal-direction-calculus/) for points of the plane uses one point algebra relation per axis, $3 \times 3 = 9$ base relations. The [rectangle algebra](/rectangle-algebra/) uses one Allen relation per axis, $13 \times 13 = 169$ base relations.

**Non-example: not exhaustive.** $\{<, >\}$ on $\mathbb{R}$ misses the pairs with $x = y$.

**Non-example: not disjoint.** $\{\le, \ge\}$ on $\mathbb{R}$ is exhaustive, but both relations hold when $x = y$, so "exactly one holds" fails and the table cannot be read as a function of the base relations.

**Non-example: metric constraints.** The constraints $a \le x_j - x_i \le b$ of the [simple temporal problem](/simple-temporal-problem/) use infinitely many relations, one per pair $(a, b)$. They are not a qualitative calculus, and they are solved by shortest paths instead of a table.

### Common errors

- Assuming that the table is associative or gives the exact composition. Both hold for the point and interval algebras, but not for every calculus.
- Confusing a base relation with a relation. "$x \mathrel{\{b, m\}} y$" says that one of two base relations holds, not both.
- Taking the identity for granted. If it is not a base relation, a network cannot say that two variables are the same object.

## Related definitions

- [Composition table](/composition-table/): the finite table of $B_a \diamond B_b$ that the calculus computes with.
- [Qualitative constraint network](/qualitative-constraint-network/): a set of variables with a relation of the calculus on each pair.
- [Algebraic closure](/algebraic-closure/): the propagation that uses the table to tighten a network.
- [Constraint satisfaction problem](/constraint-satisfaction-problem/): the general problem; a qualitative network is a binary CSP with an infinite domain.
- [Point algebra](/point-algebra/), [Allen's interval algebra](/allens-interval-algebra/), [RCC8](/region-connection-calculus-rcc8/) and [rectangle algebra](/rectangle-algebra/): the main calculi.

## References
