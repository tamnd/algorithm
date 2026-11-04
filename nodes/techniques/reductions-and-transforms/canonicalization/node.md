---
tag: Z36CVT
kind: technique
slug: canonicalization
name: Canonicalization
area: techniques/reductions-and-transforms
level: core
summary: Maps equivalent objects to one standard representative form so that equality can be tested by simple comparison or hashing.
prereqs: [equivalence-relation, canonical-form, hash-table]
see_also: [normal-form-representation, isomorphism-invariant, booth-algorithm, ahu-algorithm, canonical-labeling, reduced-ordered-bdd, hash-consing, reducing-fractions]
sources:
  - paper: doi:10.1016/0020-0190(80)90149-0
    title: "Kellogg S. Booth, Lexicographically least circular substrings, Information Processing Letters 10(4-5) (1980), 240-242"
    locator: the linear-time algorithm for the least rotation
  - book: isbn:9780201000290
    title: Alfred V. Aho, John E. Hopcroft and Jeffrey D. Ullman, The Design and Analysis of Computer Algorithms, Addison-Wesley, 1974
    locator: Chapter 3 (isomorphism of rooted trees in linear time)
  - paper: doi:10.1109/TC.1986.1676819
    title: "Randal E. Bryant, Graph-based algorithms for Boolean function manipulation, IEEE Transactions on Computers C-35(8) (1986), 677-691"
    locator: the canonicity of reduced ordered BDDs for a fixed variable order
  - paper: doi:10.1016/j.jsc.2013.09.003
    title: "Brendan D. McKay and Adolfo Piperno, Practical graph isomorphism, II, Journal of Symbolic Computation 60 (2014), 94-112"
    locator: canonical labelling of graphs in nauty and Traces
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, third edition
    locator: Section 4.5.1, Fractions (lowest terms)
---

Canonicalization is the technique of computing, for each object $x$, a *canonical form* $c(x)$ such that two objects are equivalent exactly when their canonical forms are equal: $x \sim y \iff c(x) = c(y)$. It turns a test of an [equivalence relation](/equivalence-relation/), such as "is an anagram of", "is a rotation of" or "is isomorphic to", into a test of equality, so that $n$ objects can be grouped with one [hash table](/hash-table/) or one sort instead of $\Theta(n^2)$ pairwise tests. The standard examples are sorted letters for anagrams, the least rotation of a string ([Booth's algorithm](/booth-algorithm/)), fractions in lowest terms, the [AHU encoding](/ahu-algorithm/) of rooted trees, [canonical labelling](/canonical-labeling/) of graphs, and [reduced ordered BDDs](/reduced-ordered-bdd/) for Boolean functions.

## In plain words

Many objects can be written in more than one way and still mean the same thing. The fraction two quarters is the same number as one half. The words "listen" and "silent" use the same letters. A tree drawn with its branches swapped is still the same tree.

To decide fast if two such objects are the same, pick one fixed way to write each object, and always convert to it. Then two objects are the same when their fixed forms are equal, letter by letter. To find all groups of equal objects in a big collection, convert each object once and put the forms in a dictionary.

The fixed form must have two properties. Two objects that mean the same thing must always get the same form. And two objects that mean different things must never get the same form.

## When it applies

- An equivalence relation $\sim$ on a set $X$ is given, and the task is to test pairs, to group a collection into classes, to count the classes, or to remove duplicates up to $\sim$.
- Each class has a member that can be described by a rule ("the smallest", "the reduced one", "the sorted one"), and the rule can be computed from any member.
- The objects are built from parts, and each part can be put into canonical form first (bottom-up), as for trees, terms and BDDs.
- The number of comparisons matters more than the cost of one conversion: $n$ conversions replace up to $\binom{n}{2}$ pairwise tests.

## The template

Let $\sim$ be an equivalence relation on a set $X$. A function $c : X \to K$ to a set $K$ with an equality test is a *complete invariant*, or *canonical form function*, when for all $x, y \in X$:

$$x \sim y \iff c(x) = c(y).$$

**Both directions are needed.**

- *Completeness* ($x \sim y \Rightarrow c(x) = c(y)$) says that equivalent objects are never separated. A function with only this property is an [invariant](/isomorphism-invariant/). The length of a string, the multiset of its letters and a hash value are invariants of rotation. An invariant can prove that two objects are *not* equivalent, but equal values prove nothing. For example, cabab and bacab have the same multiset of letters $\{a, a, b, b, c\}$, but they are not rotations of each other.
- *Soundness* ($c(x) = c(y) \Rightarrow x \sim y$) says that non-equivalent objects are never merged. The identity map $c(x) = x$ has this property, but it fails completeness: the fractions $2/4$ and $1/2$ stay apart.

With only completeness, the grouping merges classes and gives false matches. With only soundness, it splits classes and misses matches. Only with both is each group exactly one class.

**Lemma (a recipe).** Let $c : X \to X$ satisfy (i) $c(x) \sim x$ for all $x$, and (ii) $x \sim y \Rightarrow c(x) = c(y)$. Then $x \sim y \iff c(x) = c(y)$.

*Proof.* The direction $\Rightarrow$ is (ii). For $\Leftarrow$, let $c(x) = c(y)$. By (i), $x \sim c(x)$ (using symmetry) and $c(y) \sim y$. Since $c(x) = c(y)$, transitivity gives $x \sim y$. $\square$

So the usual way to build $c$ is to choose one member of each class by a rule that does not depend on which member you start from, such as the least member in a total order. Property (i) then holds because $c(x)$ is a member of the class of $x$, and (ii) holds because the rule depends only on the class.

```pseudo id=main
GROUP-BY-CANONICAL-FORM(x₁, …, xₙ)
L1  H ← empty hash table from forms to lists
L2  for i ← 1 to n do
L3      k ← CANON(xᵢ)                ▷ CANON(x) = CANON(y) iff x ~ y
L4      append xᵢ to H[k]            ▷ creates H[k] when k is new
L5  return the lists in H            ▷ one list for each class present
```

Let CANON take $C$ time on one object and give a form of size $s$. The loop takes $n C$ time plus $O(n s)$ expected time for hashing and comparing forms in the table. Sorting the pairs $(c(x_i), x_i)$ instead of hashing gives a deterministic $O(n C + s \, n \log n)$ bound, and is a [reduction to sorting](/reduction-to-sorting/). The hash of a form is only an invariant: two different forms can collide, so the table must compare the forms themselves, not only their hashes.

## Classic examples

### Anagrams: sorted letters

Two words are anagrams when one is a permutation of the letters of the other. Let $c(w)$ be the letters of $w$ in alphabetical order. $c(w)$ is a permutation of $w$, so (i) holds, and two permutations of each other have the same multiset of letters and so the same sorted list, so (ii) holds. For listen, silent and enlist, $c = $ eilnst for all three; for google, $c = $ eggloo. Computing $c(w)$ for a word of length $L$ takes $O(L \log L)$ time with a comparison sort, or $O(L + \sigma)$ with a [counting sort](/counting-sort/) over an alphabet of size $\sigma$.

### Rotations: the least rotation

Two strings are rotations of each other (conjugates) when $u = ab$ and $v = ba$ for some strings $a, b$. Let $c(w)$ be the lexicographically least rotation of $w$ ([minimal rotation](/minimal-rotation/)). It is a member of the class of $w$, and it depends only on the set of rotations, which is the same for all members of the class. For cabab, abcab and ababc, $c = $ ababc. For bacab, $c = $ abbac, so bacab is in another class. [Booth's algorithm](/booth-algorithm/) (1980) computes $c(w)$ in $O(L)$ time; the brute-force method compares all $L$ rotations and takes $O(L^2)$ time. A string equal to its least rotation and different from its other rotations is a [Lyndon word](/lyndon-word/).

### Fractions: lowest terms

Two fractions $a/b$ and $a'/b'$ with $b, b' \ne 0$ are equal as numbers when $a b' = a' b$. The canonical form divides by $g = \gcd(a, b)$ and makes the denominator positive ([reducing fractions](/reducing-fractions/)). For $42/(-56)$, $g = 14$, and the form is $-3/4$. Both steps are needed: $3/(-4)$ and $-3/4$ are reduced, but without the sign rule they would be different forms of the same number. The [Euclidean algorithm](/euclidean-algorithm/) computes $g$ in $O(\log \min(|a|, |b|))$ division steps.

### Rooted trees: the AHU encoding

Two rooted trees are isomorphic when a bijection of the nodes maps the root to the root and keeps the parent relation. Encode a leaf as "()", and an inner node as "(" followed by the codes of its children in sorted order, then ")". An isomorphism of rooted trees may permute the children of each node, and sorting the child codes removes the order in which the input lists them. The tree whose root has a leaf child and a child with two leaves, and the same tree with the two children of the root swapped, both get the code ((()())()). The tree with $5$ nodes whose root has three children, one of which has a child, gets ((())()()), so it is not isomorphic to them. Built with strings, this code costs $O(n^2)$ time in the worst case. The [AHU algorithm](/ahu-algorithm/) replaces the strings by integer labels, level by level, and runs in $O(n)$ time. For unrooted trees, root the tree at its [center](/tree-center/) (or at each of its two centers and take the smaller code).

### Graphs: canonical labelling

For graphs, $c(G)$ is the adjacency matrix of a relabelled copy of $G$, chosen so that isomorphic graphs give the same matrix ([canonical labeling](/canonical-labeling/)). A canonical form solves the [graph isomorphism problem](/graph-isomorphism-problem/), so no polynomial-time algorithm is known for it. [nauty](/nauty/) and Traces compute it fast in practice by refining a partition of the vertices and searching a tree of choices, with pruning by automorphisms (McKay and Piperno 2014).

### Boolean functions: reduced ordered BDDs

Fix an order of the variables. Bryant (1986) proved that each Boolean function has exactly one [reduced ordered BDD](/reduced-ordered-bdd/) up to isomorphism: no node with two equal children, and no two nodes with the same variable and the same children ([BDD canonicity](/bdd-canonicity/)). When all BDDs share one table of nodes, with each node created only if it is not already present ([hash-consing](/hash-consing/)), isomorphic BDDs are the same node, and two functions are equal exactly when their root pointers are equal: an $O(1)$ test.

## Variations

- **Hash-consing.** Build every value through a table that returns the existing copy of a structurally equal value. Equality of canonical values is then pointer equality. This is canonicalization of the representation in memory.
- **Canonical form by minimization.** Take the least member of the class in a total order: the least rotation, the least relabelled adjacency matrix. This always satisfies the lemma, but it can be costly to compute directly.
- **Canonical form by rewriting.** Apply simplification rules until none applies. If every object reaches one unique result, this result is a canonical form. The general notion is a [normal form](/normal-form-representation/), which is weaker: a normal form need not be unique.
- **Invariants as filters.** When a canonical form is costly, compare cheap invariants first (size, degree sequence, a hash) and compute the canonical form only for objects that agree on them.
- **Canonical augmentation.** To list objects up to isomorphism without storing all of them, build each object from a smaller one and keep it only when the last step is the canonical one ([canonical augmentation](/canonical-augmentation/)).

## Pitfalls

- **An invariant used as a canonical form.** Sorted letters for rotation, the degree sequence for graphs, or a hash value for any object: equal values do not imply equivalence. The result is false matches.
- **A form that depends on the starting member.** The rule "rotate the string so that its first a is in front" maps aab to aab and aba to aba, but aab and aba are rotations of each other. The rule depends on the member, not on the class, so completeness fails. Use a rule that depends only on the class, such as the least rotation.
- **A missing normalization step.** A fraction reduced by the gcd but with a free sign, a path with or without a trailing slash, a string compared with case: each splits one class into several forms.
- **A different equivalence than intended.** Sorted children make trees equal up to reordering of children. If the order of children matters (ordered trees), the sort must be left out. Decide the equivalence first, then design the form.
- **The cost of the form.** The size of the canonical form can be much larger than the object. A ROBDD can have a size exponential in the number of variables, and its size depends on the variable order.
- **Floating-point values.** Two computations of the same real number may differ in the last bits, so the form must round in a fixed way, or the comparison must be exact.

## Exercises

1. Prove that the least rotation satisfies both conditions of the lemma, for the relation "is a rotation of".
2. Group the words post, stop, tops, spot, opts, pots and top by anagram class, and count the classes.
3. Two necklaces of beads are equal when one is a rotation or a reflection of the other. Give a canonical form and its cost for a necklace of $L$ beads.
4. Give two non-isomorphic graphs with the same degree sequence. Explain which direction of the canonical form condition the degree sequence fails.
5. Show that the string encoding of rooted trees without sorting the children is sound but not complete for the relation "is isomorphic to".
6. A set of polynomials is given as lists of terms in any order, with like terms not combined. Define a canonical form for equality as polynomials.

## References
