---
tag: W1EW4J
kind: algorithm
slug: feature-structure-unification
name: Feature structure unification
aliases:
- graph unification
area: natural-language-and-speech/natural-language-parsing
level: advanced
summary: Merge two feature structures, directed graphs of attribute values, into the most general one that has the information of both, or fail.
model: word-ram
complexity:
  vars: {n: the number of nodes of the two inputs, e: the number of arcs of the two inputs}
  time: {expected: O((n + e) α(n) + e log e)}
  space: {extra: O(n + e)}
properties: {deterministic: true, exact: true, online: false, recursive: false, destructive: true}
history:
  year: 1984
  people: [Hassan Aït-Kaci, Stuart M. Shieber]
  note: "Aït-Kaci adapted the union-find unification of Huet (1976) to record-like terms with named features in his 1984 thesis. Shieber's 1986 book made unification of feature structures the standard account for unification-based grammars."
prereqs: [unification-problem, disjoint-set-forest]
see_also: [huet-unification, most-general-unifier, occurs-check, union-by-rank, path-compression, join-semilattice, combinatory-categorial-grammar, tree-adjoining-grammar]
sources:
  - book: isbn:9780937073001
    title: "Stuart M. Shieber, An Introduction to Unification-Based Approaches to Grammar, CSLI Lecture Notes 4, 1986"
    locator: "Chapter 3, The Simplest Unification-Based Formalism, section 3.2 The Informational Domain (3.2.2 Subsumption, 3.2.3 Unification, 3.2.4 Feature Structures as Graphs)"
  - paper: "Hassan Aït-Kaci, A Lattice-Theoretic Approach to Computation Based on a Calculus of Partially-Ordered Type Structures, PhD thesis, University of Pennsylvania, 1984"
    title: "Hassan Aït-Kaci, A Lattice-Theoretic Approach to Computation Based on a Calculus of Partially-Ordered Type Structures"
    locator: "the unification of psi-terms with union and find, after Huet"
  - paper: "Gérard Huet, Résolution d'équations dans des langages d'ordre 1, 2, ..., omega, Thèse d'État, Université Paris VII, 1976"
    title: "Gérard Huet, Résolution d'équations dans des langages d'ordre 1, 2, ..., omega"
    locator: "the almost linear unification of first-order terms with equivalence classes merged by union and find"
  - paper: "Robert E. Tarjan, Efficiency of a Good But Not Linear Set Union Algorithm, Journal of the ACM 22(2), 215-225, 1975"
    title: "Robert E. Tarjan, Efficiency of a Good But Not Linear Set Union Algorithm"
    locator: "the bound for union by rank with path compression"
  - paper: doi:10.3115/981131.981166
    title: "Robert T. Kasper and William C. Rounds, A Logical Semantics for Feature Structures, Proceedings of ACL 1986, 257-266"
    locator: "the consistency problem for feature descriptions with disjunction is NP-complete"
  - paper: "Kevin Knight, Unification: A Multidisciplinary Survey, ACM Computing Surveys 21(1), 93-124, 1989"
    title: "Kevin Knight, Unification: A Multidisciplinary Survey"
    locator: "the sections on Huet's algorithm and on unification in computational linguistics"
---

Feature structure unification takes two feature structures, rooted [directed graphs](/directed-acyclic-graph/) whose arcs carry features such as `number` and whose leaves carry atoms such as `singular`, and builds the most general structure that has the information of both, or fails when they disagree. Two paths can lead to the same node, which is how a grammar says that two values must be equal. It differs from the first-order [unification problem](/unification-problem/) of terms in three ways: features are named, not numbered by position, an empty node plays the role of a variable, and cycles are allowed, so there is no [occurs check](/occurs-check/). It is the one operation of unification-based grammars such as PATR-II, LFG and HPSG, and it adds agreement and other features to [CCG](/combinatory-categorial-grammar/) and [TAG](/tree-adjoining-grammar/).

The method on this page is the one of [Huet's algorithm](/huet-unification/) for terms: put the nodes of both graphs in a [disjoint-set forest](/disjoint-set-forest/) and merge classes that must be equal. Because features are named, a node can gain new features in a merge, and the algorithm must merge feature tables, not fixed argument lists.

## In plain words

A feature structure is a bundle of facts about a phrase. One bundle says that the subject is singular. Another says that the subject is third person. Unification puts the two bundles together, so the result says that the subject is singular and third person. If one bundle says singular and the other says plural, the bundles cannot go together, and unification fails.

Some bundles share parts. A rule can say that the agreement of a verb phrase is the same object as the agreement of its subject. When new facts arrive at one place, they also hold at every place that shares it.

The algorithm keeps groups of nodes that must be the same, starting with the two top nodes. When it joins two groups, a feature that both have gives two more nodes that must be the same, and it joins those too.

## The problem

**Input.** Two feature structures $A$ and $B$ with disjoint node sets. Each has a root, a partial function $\delta(x, f)$ that gives the value of feature $f$ at node $x$, and a partial atom label $\mathrm{atom}(x)$. A node with an atom has no features. A node with no atom and no feature is the empty structure $[\,]$.

**Order.** $A$ subsumes $D$, written $A \sqsubseteq D$, if $D$ has at least the information of $A$: there is a map $h$ from the nodes of $A$ to the nodes of $D$ that sends the root to the root, each arc $x \xrightarrow{f} y$ to an arc $h(x) \xrightarrow{f} h(y)$, and each atom to the same atom. In Shieber's terms: every path of $A$ is a path of $D$ with the same atom value, and paths that share a node in $A$ share a node in $D$. The empty structure subsumes every structure.

**Output.** The unification $A \sqcup B$: a structure $C$ with $A \sqsubseteq C$ and $B \sqsubseteq C$ such that $C \sqsubseteq D$ for every $D$ that both $A$ and $B$ subsume. It is unique up to renaming of the nodes. If no $D$ is subsumed by both inputs, the output is failure.

Write $n$ for the number of nodes and $e$ for the number of arcs of $A$ and $B$ together.

## The algorithm

Every node has the union-find fields parent and rank, an atom or nothing, and a table of features. Only the table of a class root is used; it holds one value for each feature of the class.

```pseudo id=main
UNIFY(a, b)                        ▷ a, b: the roots of the two inputs
L1  stack ← [(a, b)]
L2  while stack is not empty do
L3      pop (u, v);  x ← FIND(u);  y ← FIND(v)
L4      if x = y then continue
L5      if CLASH(x, y) then return FAIL
L6      if rank(x) < rank(y) then swap x and y;  parent(y) ← x;  if rank(x) = rank(y) then rank(x) ← rank(x) + 1
L7      if atom(x) is undefined then atom(x) ← atom(y)
L8      (big, small) ← the tables of x and y, the larger first
L9      for each feature f with value w in small do
L10         if f is in big then push (big[f], w)
L11         else big[f] ← w
L12     table(x) ← big;  clear the table and the atom of y
L13 return FIND(a)

CLASH(x, y) is true if x and y have different atoms, or one of them has an atom and the other has a feature.
```

Line L3 takes a pair of nodes that must be equal and finds their class roots with path compression. Line L6 is [union by rank](/union-by-rank/). Lines L8 to L11 merge the two feature tables. A feature in only one table moves over unchanged. A feature in both tables gives a new pair of nodes that must be equal, which goes on the stack. The loop uses a stack, not recursion, so deep structures such as long lists do not overflow the call stack.

The algorithm is destructive: it changes the input graphs. A parser that needs the inputs again copies them first. On failure the inputs are left half merged, so a parser that unifies in place must copy or undo.

## Example

Shieber's example of reentrancy, from section 3.2.3 of his book. The tag $\boxed{1}$ marks a shared node.

$$A = \begin{bmatrix} \text{agreement}: \boxed{1}\,[\text{number}: \text{singular}] \\ \text{subject}: [\text{agreement}: \boxed{1}] \end{bmatrix} \qquad B = \big[\text{subject}: [\text{agreement}: [\text{person}: \text{third}]]\big]$$

Call the nodes of $A$: $r_A$ (root), $s_A$ (the subject), $g$ (the shared agreement) and the atom node of `singular`. Call the nodes of $B$: $r_B$, $s_B$, $g_B$ and the atom node of `third`. The run:

| pass | pair popped | tables merged | moved | pushed |
|---|---|---|---|---|
| 1 | $(r_A, r_B)$ | {agreement, subject} and {subject} | none | $(s_A, s_B)$ |
| 2 | $(s_A, s_B)$ | {agreement} and {agreement} | none | $(g, g_B)$ |
| 3 | $(g, g_B)$ | {number} and {person} | person | none |

After three merges the stack is empty and the result is

$$A \sqcup B = \begin{bmatrix} \text{agreement}: \boxed{1}\,[\text{number}: \text{singular},\ \text{person}: \text{third}] \\ \text{subject}: [\text{agreement}: \boxed{1}] \end{bmatrix}$$

The new fact `person: third` came in through the subject, and it also holds at the top-level agreement, because the two paths lead to one node. If $A$ had two separate copies of `[number: singular]` instead of one shared node, the result would have `person: third` only under the subject. The tests check both cases.

A clash: $[\text{number}: \text{singular}] \sqcup [\text{number}: \text{plural}]$. Pass 1 merges the roots and pushes the two values of `number`. Pass 2 finds two different atoms at line L5 and returns failure.

A cycle: $A = [a: \boxed{1}\,[\,],\ b: \boxed{1}]$ and $B = [a: [h: \boxed{2}\,[\,]],\ b: \boxed{2}]$. Unification makes the node under $a$ equal to the node under $b$, which is the value of $h$ inside it. The result has a node $x$ with $x.h = x$, so the path $a\,h\,h\,h$ leads back to the node of $a$. With an occurs check this would fail; without one it gives a cyclic structure.

## Correctness

The claim is a theorem: UNIFY returns $A \sqcup B$ when it exists, returns failure exactly when no structure is subsumed by both inputs, and stops after at most $e + 1$ passes. The full proof is in proofs/correctness.md. Its outline:

1. Call an equivalence relation on the nodes a unifying congruence if it puts the two roots together and, whenever it puts $x$ and $y$ together and both have feature $f$, it also puts $\delta(x, f)$ and $\delta(y, f)$ together. Let $\theta$ be the least one.
2. If no class of $\theta$ holds two different atoms, or an atom and a feature, then the quotient graph by $\theta$ is $A \sqcup B$. Any $D$ that both inputs subsume defines a congruence by "same image in $D$", which contains $\theta$, so the quotient maps into $D$. If $\theta$ has a bad class, then so does that congruence, and no $D$ exists.
3. UNIFY keeps the invariant that every pair it joins or pushes is in $\theta$, and that the table of each root holds every feature of its class, with a value that is equal to the value of each member, up to pairs still on the stack. When the stack is empty, the classes are closed under the congruence condition, so they are exactly $\theta$. A clash at line L5 shows a bad class of $\theta$.

## Complexity

**Time.** Each push at line L10 removes one entry from the small table, and no new entries appear, so there are at most $e$ pushes, at most $e + 1$ passes and at most $2(e + 1)$ finds. With union by rank and [path compression](/path-compression/) the finds and the at most $n - 1$ unions cost $O((n + e)\,\alpha(n))$ (Tarjan 1975), where $\alpha$ is the [inverse Ackermann function](/inverse-ackermann-function/). This is a theorem in the word-RAM model.

The feature tables add a term. Merging the smaller table into the larger one makes each moved entry land in a table at least 1.5 times as large, except in merges where most entries collide, and collisions are paid for by the pushes. So each entry moves $O(\log e)$ times, and the table work is $O(e \log e)$ operations on [hash tables](/hash-table/), each of expected constant time. The total is $O((n + e)\,\alpha(n) + e \log e)$ expected. If all complex nodes have the same fixed set of features, as for first-order terms with one function symbol per arity, nothing ever moves, and the bound is the $O((n + e)\,\alpha(n))$ of Huet's algorithm.

**Space.** $O(n + e)$ for the parent and rank fields, the tables and the stack. The stack holds at most $e + 1$ pairs.

**Heuristic, not bound.** In a chart parser the merge is often not the main cost. The parser must keep its edges unchanged, so it copies structures before it unifies them, and most unifications fail. This is the reason for the non-destructive variants below.

## Properties

- **Exact and deterministic.** The result is unique up to renaming of nodes.
- **Idempotent, commutative and associative**, up to renaming: $A \sqcup A = A$, $A \sqcup B = B \sqcup A$, and $(A \sqcup B) \sqcup C = A \sqcup (B \sqcup C)$, where both sides fail together. These follow from the description as a least upper bound. The tests check all three on random structures.
- **Identity.** The empty structure $[\,]$ is the identity: $[\,] \sqcup A = A$.
- **Order.** Up to renaming, the feature structures with an added top element for failure form a [join-semilattice](/join-semilattice/) under $\sqsubseteq$, and unification is the join. The empty structure is the bottom.
- **No occurs check.** Cycles are allowed. A system that forbids cycles adds an acyclicity test on the result, as Huet's algorithm does for terms.
- **Destructive.** The inputs are changed.

## Variants and improvements

- **Non-destructive unification.** A chart parser uses the same edge in many combinations, so it cannot let unification change it. The simplest fix copies both inputs first. Wroblewski (1987) copies only the parts that change, and Tomabechi (1991) delays copying until the unification has succeeded, so failed unifications, the common case in parsing, copy nothing.
- **Typed feature structures.** HPSG gives every node a type from a hierarchy, and unification takes the most general common subtype of the two types, failing when there is none. The merge is the same, with CLASH replaced by a type lookup.
- **Disjunction.** Grammars often write a value as a choice, such as "singular or plural". Deciding whether a description with disjunction has any solution is NP-complete (Kasper and Rounds 1986, a theorem). Unification of plain structures stays almost linear; the cost comes from the choices.
- **First-order terms.** With positional arguments and a function symbol at each node, the same algorithm is [Huet's algorithm](/huet-unification/), and with an occurs check it computes a [most general unifier](/most-general-unifier/). For acyclic terms the linear time algorithm of [Paterson and Wegman](/paterson-wegman-unification/) removes the inverse Ackermann factor.

## When to use it

Use it in a parser for a unification-based grammar, to combine the features of constituents, and in any program that merges partial records where shared fields must stay shared. For a parser, prefer a non-destructive variant, or copy before unifying. For first-order terms in logic programming, use term unification with its occurs check choice; for typed structures, add the type lattice.

## Pitfalls

- **Comparing copies instead of sharing.** Two separate nodes with the same contents are not the same node. Unification adds information to one and not to the other. Build reentrant nodes as one node.
- **Forgetting FIND.** A node that was merged is no longer a root. Reading its table or its atom without FIND gives stale data.
- **Recursion depth.** A recursive version overflows the call stack on long lists, which feature structures use for subcategorization. Use an explicit stack.
- **Failure leaves damage.** After a clash the inputs are partly merged. Copy before unifying, or keep a trail of changes and undo them.
- **Hidden cycles.** Printing or copying a structure by naive recursion loops forever on a cycle. Mark visited nodes.
- **Atoms against complex nodes.** An atom node must not gain features. CLASH must test this case, not only two different atoms.

## Implementations

## History

Kay's functional unification grammar and PATR-II, which Shieber and others built at SRI, made unification of feature structures the central operation of a family of grammar formalisms. Huet (1976) had already given an almost linear algorithm for first-order terms that merges equivalence classes with union and find, and that works on rational (cyclic) terms when the occurs check is dropped. Aït-Kaci (1984) adapted that method to his ψ-terms, records with named features and types, as Knight's 1989 survey describes. Shieber's 1986 book gave the account of subsumption, unification as the least upper bound, and feature structures as graphs that grammar writers still use. Kasper and Rounds (1986) gave a logic of feature descriptions and showed that disjunction makes consistency NP-complete.

## References
