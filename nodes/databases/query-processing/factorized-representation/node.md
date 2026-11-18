---
tag: 7ZFJ86
kind: data-structure
slug: factorized-representation
name: Factorized representation
aliases:
- factorized database
- f-representation
- d-representation
area: databases/query-processing
level: research
summary: "A join result stored as nested unions and products over a tree of attributes. It can be much smaller than the list of its tuples, and the tuples can still be listed one by one."
model: word-ram
complexity:
  vars: {n: the number of tuples in the input relations, k: the number of attributes, r: the number of relations, s: the parameter s(T) of the f-tree}
  time: {worst: "O(k r (k + n) n^s)"}
  space: {extra: "O(k n^s)"}
prereqs: [relational-join, conjunctive-query, agm-bound]
see_also: [generic-join, yannakakis-algorithm, fractional-hypertree-width, join-dependency, multivalued-dependency, d-dnnf, binary-decision-diagram, leapfrog-triejoin]
sources:
  - paper: doi:10.1145/2656335
    title: "Dan Olteanu and Jakub Závodný, Size bounds for factorised representations of query results, ACM Transactions on Database Systems 40(1), Article 2 (2015)"
    locator: Example 1.1; Definitions 5.1 and 5.2 (f-trees and f-representations); Proposition 5.10 (existence and uniqueness); Proposition 6.1 (the path condition); Corollary 7.6 (the number of singletons); Definition 7.14 and Theorem 7.16 (the parameter s and the upper bound); Theorems 7.1 and 7.2 (the upper bound and the matching lower bounds); Section 8 (computing the representation)
  - paper: doi:10.1137/110859440
    title: "Albert Atserias, Martin Grohe and Dániel Marx, Size bounds and query plans for relational joins, SIAM Journal on Computing 42(4), 1737 to 1767 (2013); first in FOCS 2008, 739 to 748"
    locator: the bound on the size of a join by a fractional edge cover, which gives the bound on each path of the f-tree
---

A factorized representation stores a relation, usually the result of a join, as an expression built from single values with unions and Cartesian products. The nesting of the expression follows a tree of attributes, the *f-tree*. A join result with many tuples that repeat the same combinations can have a representation that is polynomially smaller, with an exponent $s$ that depends only on the query and the f-tree. The tuples can still be listed one at a time with constant delay for a fixed query, so the representation can replace the flat result. Olteanu and Závodný (2015) gave the size bounds and showed that they are tight. The construction on this page reads the input relations directly, in the style of [generic join](/generic-join/), and never builds the flat result.

## In plain words

A shop sells shirts in many colors and sizes, but only some combinations exist for each brand. A list of every brand, color and size combination can be very long.

You can write it in a shorter way: "brand X: (red or blue) and (small, medium or large)". For each brand you list the colors once and the sizes once, and you say that each color goes with each size. This works when, for a fixed brand, the choice of color does not depend on the choice of size.

A factorized representation does this for a whole table, level by level, following a tree of columns. Under each value of a column, the subtrees below it are independent of each other, so the table is a product of short lists. You can still read every row from it, one at a time.

## The abstract type

A factorized representation stands for a relation $R$ over a set of attributes. It supports:

- **build** from a join query and its input relations, or from one relation;
- **enumerate** the tuples of $R$, each once;
- **count** the tuples of $R$ without listing them;
- **size**, the number of singletons, which is the measure of space.

The representation does not support updates in place. Other work, cited by Olteanu and Závodný, applies selections, projections and joins to representations; this is outside this page.

## Representation

A *singleton* $\langle A{:}a \rangle$ is the relation with one tuple, with the value $a$ for the attribute $A$. An *f-representation* is an expression built from singletons with union $\cup$ and Cartesian product $\times$.

An *f-tree* $T$ is a rooted forest in which each node is an attribute. A representation *over* $T$ has this form:

- over a forest with trees $T_1, \dots, T_k$: a product $E_1 \times \dots \times E_k$, with $E_i$ over $T_i$;
- over a tree with root $A$ and child forest $F$: a union $\bigcup_{a} \langle A{:}a \rangle \times E_a$ over distinct values $a$, with each $E_a$ over $F$.

So below each value of $A$, the subtrees of the children are independent. A relation has a representation over $T$ if and only if it has this independence, and then the representation is unique up to the order of the terms. In the code, a union is a list of pairs (value, factors) sorted by value, and the factors are a tuple with one union per child.

For a natural join $Q$ of the relations $R_1, \dots, R_m$, an f-tree with the attributes of $Q$ is *valid* if it satisfies the **path condition**: the attributes of each relation lie on one root-to-leaf path. Two attributes in different subtrees below a node then never occur in one relation, so the join result is independent across these subtrees once the values above them are fixed, and it has a representation over $T$.

## Operations

```pseudo id=main
FROMJOIN(T, D)                            ▷ D holds the relations of the natural join Q
L1  if T and Q have different attributes, or the attributes of some relation are not on one root-to-leaf path of T, then fail
L2  E ← PRODUCT(the roots of T, the empty tuple); return E, or one empty union per root if E = ∅
PRODUCT(F, t)                             ▷ t gives a value to each attribute above the trees of F
L3  for each tree of F, with root A, do
L4      U_A ← UNION(A, t)
L5      if U_A is empty then return ∅
L6  return the product of the unions U_A
UNION(A, t)
L7  V ← the values a such that each relation R that contains A has a tuple that agrees with t above A and has a at A
L8  for each a in V, in increasing order, do
L9      P ← PRODUCT(the children of A, t extended by A = a)
L10     if P ≠ ∅ then add the pair ⟨A:a⟩ × P to the union
L11 return the union
```

Line L7 uses one hash index per relation $R$ and attribute $A$ of $R$: it maps the values of the attributes of $R$ above $A$ to the set of values of $A$. The code intersects these sets, starting from the smallest, as [generic join](/generic-join/) does. Line L10 prunes a value whose subtrees have no tuple, so the result has no dead branches.

- **Factorize one relation.** Group the rows by the value of the root, recurse on each group for the children, and over a forest build each tree on the same rows. The result always contains the relation; it is equal to it, and so a representation of it, exactly when the counts agree. Otherwise the relation has no representation over $T$, and the code raises an error.
- **Count.** Add the counts over the pairs of a union, and multiply the counts over the factors of a product. This takes time linear in the size.
- **Enumerate.** Walk the expression depth first, choosing one pair in each union. Each choice gives one tuple, and no choice is a dead end, so the delay between two tuples depends only on the number of attributes.
- **Size.** Count the singletons.

## Example

Take $R(A, B) = \{(1,1), (1,2), (1,3), (2,4)\}$ and $S(A, C) = \{(1,5), (1,6), (2,7)\}$, and the f-tree with root $A$ and children $B$ and $C$. Both relations lie on a root-to-leaf path, so the f-tree is valid. The join has 7 tuples, 21 values in all. FROMJOIN gives

$$\langle A{:}1 \rangle \times (\langle B{:}1 \rangle \cup \langle B{:}2 \rangle \cup \langle B{:}3 \rangle) \times (\langle C{:}5 \rangle \cup \langle C{:}6 \rangle) \;\cup\; \langle A{:}2 \rangle \times \langle B{:}4 \rangle \times \langle C{:}7 \rangle,$$

with 9 singletons. If one value of $A$ has $n$ values of $B$ and $n$ values of $C$, the join has $n^2$ tuples and the representation has $2n + 1$ singletons.

The f-tree matters. Example 1.1 of Olteanu and Závodný takes the relation of all $(a, b, c)$ with $1 \le a < b < c \le 5$, which has 10 tuples and 30 values. Over the f-tree with root $b$ and children $a$ and $c$, the representation is

$$\langle b{:}2 \rangle \times \langle a{:}1 \rangle \times (\langle c{:}3 \rangle \cup \langle c{:}4 \rangle \cup \langle c{:}5 \rangle) \;\cup\; \langle b{:}3 \rangle \times (\langle a{:}1 \rangle \cup \langle a{:}2 \rangle) \times (\langle c{:}4 \rangle \cup \langle c{:}5 \rangle) \;\cup\; \langle b{:}4 \rangle \times (\langle a{:}1 \rangle \cup \langle a{:}2 \rangle \cup \langle a{:}3 \rangle) \times \langle c{:}5 \rangle,$$

with 15 singletons. Over the path $a, b, c$ it has $3 + 6 + 10 = 19$ singletons. Over the f-tree with root $a$ and children $b$ and $c$ there is no representation, because $b < c$ ties $b$ and $c$ for a fixed $a$.

## Correctness

The proof defines, for each call, the set of partial tuples below the call that agree with every relation they touch. The path condition makes this set split into a product over the subtrees of a forest, and into a union over the values of the root of a tree. Each pruned pair has no partial tuple below it. So FROMJOIN returns a representation of exactly the join result. Since the values in a union are distinct, each tuple is enumerated once, and the occurrences of the singletons of $A$ match the distinct tuples of the result restricted to the path to $A$. The full proof is in [the proof page](proofs/correctness.md).

## Complexity

- **Exact size.** The number of singletons of $A$ is the number of distinct tuples of $Q(D)$ restricted to the path from the root to $A$ (Corollary 7.6). So the size is a sum of $k$ terms, one per attribute.
- **The parameter $s$.** By the [AGM bound](/agm-bound/), each term is at most $n^{\rho^*}$, where $\rho^*$ is the fractional edge cover number of the query restricted to the attributes on the path. The largest of these exponents over the nodes is $s(T)$, and $s(Q)$ is the smallest $s(T)$ over the valid f-trees. The size is $O(k \cdot n^{s(T)})$, while the flat result can have $n^{\rho^*(Q)}$ tuples, and $s(Q) \le \rho^*(Q)$.
- **Tightness.** Olteanu and Závodný show that for each f-tree $T$ of $Q$ there are arbitrarily large databases on which the representation over $T$ has $\Omega((n / |Q|)^{s(Q)})$ singletons (Theorem 7.1). For a fixed query, there are databases on which every representation over every f-tree has $\Omega(n^{s(Q)})$ singletons (Theorem 7.2).
- **Build time.** Each call of UNION at $A$ has as its $t$ a tuple of the join of the relations restricted to the path above $A$, so there are at most $k \cdot n^{s}$ calls. Each call does at most $r (k + n)$ steps with hashing. The algorithm of the paper computes a representation of size $O(n^{s(Q)})$ in time $O(n^{s(Q)} \log n)$ for a fixed query.
- **Queries on it.** Count takes time linear in the size. Enumeration has constant delay for a fixed query.

## Variants

- **Sharing.** If equal subexpressions are stored once and referenced, as a directed acyclic graph, the size can drop further. Olteanu and Závodný give a parameter for this case that is at most $s(Q)$, and they relate it to the [fractional hypertree width](/fractional-hypertree-width/).
- **Query evaluation on representations.** Selections, projections, joins and aggregates can be computed on the representation itself, which changes the f-tree.
- **Other systems with the same idea.** Nested relations, hierarchical clustered schemas and compiled circuits for counting, such as [d-DNNF](/d-dnnf/), also store a set as nested unions and products.

## When to use it

Use a factorized representation for a join result that is much larger than its inputs, such as a many-to-many join that later feeds an aggregate or a learning task. If the query is acyclic and only the output is needed once, [Yannakakis's algorithm](/yannakakis-algorithm/) lists the tuples directly. If the result is small, the flat list is simpler.

## Pitfalls

- **The choice of the f-tree.** The size depends on the f-tree. A path through all attributes is always valid, but it shares only common prefixes. Finding the f-tree with the smallest $s(T)$ means trying many trees, which is cheap only for small queries.
- **Dead branches.** Without the pruning of line L10, a value of an attribute can stay in a union while no tuple goes through it. Then count and enumeration still work, but the size formula and the constant delay fail.
- **Nulls.** The code joins equal values. A null in SQL never joins, so nulls must be removed first.
- **Not every relation factorizes.** A single relation has a representation over an f-tree only if it has the independence that the f-tree states. The code checks this by counting.

## Implementations

## History

Olteanu and Závodný introduced factorized representations of query results in 2012 and gave the full theory in the 2015 article in ACM Transactions on Database Systems: the f-trees, the exact number of singletons, the parameter $s(Q)$ with matching upper and lower bounds, and algorithms that build the representation directly from the input. Their article relates these ideas to earlier work on nested relations and on decompositions of relations, and later systems use them for query processing and machine learning on join results.

## References
