---
tag: 9B01H6
kind: definition
slug: composition-table
name: Composition table
aliases:
- transitivity table
- weak composition table
area: information-retrieval-and-ai-reasoning/qualitative-temporal-and-spatial-reasoning
level: advanced
summary: The m by m table that gives, for base relations a and b of a qualitative calculus, every base relation that can hold between x and z when x a y and y b z.
prereqs: [qualitative-constraint-calculus, allens-interval-algebra]
see_also: [point-algebra, algebraic-closure, allen-constraint-propagation, qualitative-constraint-network, region-connection-calculus-rcc8, rectangle-algebra, path-consistency]
sources:
  - paper: doi:10.1145/182.358434
    title: James F. Allen, Maintaining knowledge about temporal intervals, Communications of the ACM 26(11), 1983
    locator: pages 832 to 843 (the transitivity table of the 13 interval relations)
  - paper: doi:10.1007/978-3-540-28633-2_8
    title: Gérard Ligozat and Jochen Renz, What is a qualitative calculus? A general framework, PRICAI 2004, Lecture Notes in Computer Science 3157, Springer, 2004
    locator: pages 53 to 64 (weak composition and the laws it obeys)
  - paper: doi:10.1007/11564751_40
    title: Jochen Renz and Gérard Ligozat, Weak composition for qualitative spatial and temporal reasoning, CP 2005, Lecture Notes in Computer Science 3709, Springer, 2005
    locator: pages 534 to 548 (weak and strong composition tables)
  - paper: doi:10.1145/176584.176585
    title: Peter B. Ladkin and Roger D. Maddux, On binary constraint problems, Journal of the ACM 41(3), 1994
    locator: pages 435 to 469 (composition tables as the atom structures of relation algebras)
  - paper: doi:10.1145/3038927
    title: Frank Dylla and others, A survey of qualitative spatial and temporal calculi, algebraic and computational properties, ACM Computing Surveys 50(1), 2017
    locator: pages 1 to 39 (which calculi have associative and strong composition)
---

A composition table is the finite multiplication table of a [qualitative constraint calculus](/qualitative-constraint-calculus/): for two base relations $a$ and $b$, the entry $a \diamond b$ lists every base relation that can hold between $x$ and $z$ when $x \mathrel{a} y$ and $y \mathrel{b} z$. It is what lets a program reason about infinite domains with finite symbols, and every propagation method, from [algebraic closure](/algebraic-closure/) to [Allen's constraint propagation](/allen-constraint-propagation/), is a loop around it. The page [Allen's interval algebra](/allens-interval-algebra/) shows sample entries of the $13 \times 13$ interval table; this page is about tables in general: their definition, the laws they obey, how to compute one, and the shape of the interval table as a whole.

## Definition

Let the calculus have domain $D$ and base relations $B_0, \ldots, B_{m-1}$. Its **composition table** is the $m \times m$ array

$$T[a][b] = \{c : \exists x, y, z \in D,\ (x, y) \in B_a,\ (y, z) \in B_b,\ (x, z) \in B_c\}.$$

For relations $R, S \subseteq \{B_0, \ldots, B_{m-1}\}$, the (weak) composition is the union $R \diamond S = \bigcup_{a \in R,\ b \in S} T[a][b]$. A program that stores relations as $m$-bit masks computes it with at most $|R| \cdot |S|$ table look-ups, or once for all pairs of masks.

The table is **strong** (or extensional) when $B_a \circ B_b = \bigcup_{c \in T[a][b]} B_c$ as sets of pairs, that is, when for every $c \in T[a][b]$ and every pair $(x, z) \in B_c$ there is a $y$ with $x \mathrel{B_a} y$ and $y \mathrel{B_b} z$. Otherwise the table is only **weak**: it is still the smallest union of base relations that contains $B_a \circ B_b$.

**Laws.** For every calculus, with $\smile$ the converse and $\mathrm{id}$ the identity:

1. **identity:** $T[\mathrm{id}][b] = T[b][\mathrm{id}] = \{b\}$;
2. **converse:** $c \in T[a][b]$ exactly when $c^{\smile} \in T[b^{\smile}][a^{\smile}]$;
3. **cycle law:** $c \in T[a][b]$ exactly when $a \in T[c][b^{\smile}]$, exactly when $b \in T[a^{\smile}][c]$.

*Proof of the cycle law.* $c \in T[a][b]$ means that there are $x, y, z$ with $x \mathrel{a} y$, $y \mathrel{b} z$ and $x \mathrel{c} z$. The same three points have $x \mathrel{c} z$, $z \mathrel{b^{\smile}} y$ and $x \mathrel{a} y$, which says $a \in T[c][b^{\smile}]$; the other case is the same with $x$ and $z$ in the roles of the middle point. The converse law is the same argument read from $z$ to $x$. $\square$

If the table is strong, then composition is associative, $(R \diamond S) \diamond U = R \diamond (S \diamond U)$, and the relations form a relation algebra. For a weak table, associativity can fail (Ligozat and Renz 2004).

**Computing a table.** When a finite set of values realizes every configuration of three objects, the table is the set of triples of base relations seen on that set. For the [point algebra](/point-algebra/), the values $\{0, 1, 2\}$ suffice. For intervals, three intervals have 6 endpoints, so every order type of them appears among the $15$ intervals with endpoints in $\{0, \ldots, 5\}$, and the $15^3 = 3375$ triples give all 169 entries. The implementations on the algebraic closure page compute both tables this way, and check the converse law and associativity, instead of typing the table in.

## Examples and non-examples

**Point algebra.** The base relations $<$, $=$ and $>$ on $\mathbb{R}$ give this table, where "all" is $\{<, =, >\}$:

| $\diamond$ | $<$ | $=$ | $>$ |
|---|---|---|---|
| $<$ | $<$ | $<$ | all |
| $=$ | $<$ | $=$ | $>$ |
| $>$ | all | $>$ | $>$ |

The entry $< \diamond >$ is "all" because $x < y$ and $y > z$ say nothing about $x$ and $z$. The table is strong over $\mathbb{R}$ and $\mathbb{Q}$, which are dense, and only weak over $\mathbb{Z}$, where $x < y < z$ needs $z \ge x + 2$.

**Allen's interval algebra.** The $13 \times 13 = 169$ entries hold 409 base relations in total. 97 entries are single relations, 42 have 3, 24 have 5, 3 have 9 and 3 are universal ($b \diamond bi$, $bi \diamond b$ and $d \diamond di$). Every entry has an odd size. The table is strong and associative. A few entries that the interval page does not list:

| $a$ | $b$ | $a \diamond b$ |
|---|---|---|
| b | d | $\{b, m, o, s, d\}$ |
| o | oi | $\{o, s, d, f, eq, fi, di, si, oi\}$ |
| s | si | $\{s, eq, si\}$ |
| f | fi | $\{f, eq, fi\}$ |

For example, $x \mathrel{s} y$ and $y \mathrel{si} z$ say that $x$ and $z$ both start with $y$; then $x$ and $z$ start together, and either can end first, which gives s, eq or si.

**Region calculi.** The 64 entries of the [RCC8](/region-connection-calculus-rcc8/) table come from the topology of regions. For the standard models of regions, the RCC8 table is weak (Renz and Ligozat 2005).

**Product calculi.** For the [rectangle algebra](/rectangle-algebra/), $T[(a_1, a_2)][(b_1, b_2)] = T_{\mathrm{IA}}[a_1][b_1] \times T_{\mathrm{IA}}[a_2][b_2]$, so the $169 \times 169$ table is never stored; it is read off two interval tables.

**Non-example: a table of rules.** "If $x$ is before $y$ and $y$ is before $z$ then $x$ is before $z$" is one entry, not a table. A table must cover every pair of base relations, so that the composition of any two relations is defined.

**Non-example: unions as input.** The entry for the relations $\{b, m\}$ and $\{b\}$ is not a separate row of the table. It is the union of $T[b][b]$ and $T[m][b]$, so the table has only $m^2$ entries even though there are $2^m$ relations.

### Common errors

- Reading the table in the wrong order. $T[a][b]$ assumes $x \mathrel{a} y$ and $y \mathrel{b} z$; swapping $a$ and $b$ gives a different entry, for example $b \diamond d = \{b, m, o, s, d\}$ while $d \diamond b = \{b\}$.
- Typing a 169-entry table by hand. Small errors survive for a long time. Generate the table from concrete values and check the converse and cycle laws.
- Assuming that a table that is used for propagation is strong. A weak table still gives sound propagation, but algebraic closure may then say less about consistency.

## Related definitions

- [Qualitative constraint calculus](/qualitative-constraint-calculus/): the base relations whose table this is.
- [Allen's interval algebra](/allens-interval-algebra/) and [point algebra](/point-algebra/): the two classical tables.
- [Algebraic closure](/algebraic-closure/): the propagation that applies the table to all triples of a network.
- [Path consistency](/path-consistency/): the same use of composition in general CSPs, where relations are stored explicitly instead of by table.
- [Qualitative constraint network](/qualitative-constraint-network/): the networks the table is used on.

## References
