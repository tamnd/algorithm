---
tag: 6X13J0
kind: data-structure
slug: substitution-tree
name: Substitution tree
aliases:
- substitution tree index
area: automata-and-parsing/term-rewriting
level: research
summary: A term index whose nodes store substitutions, supporting unification and matching queries.
model: word-ram
complexity:
  vars: {n: the size of the query, m: the size of the inserted term, S: the total size of the substitutions in the tree}
  time: {worst: O(S n)}
  space: {extra: O(S)}
properties: {persistent: false, concurrent: false, external: false}
prereqs: [substitution, term-matching, most-general-unifier]
see_also: [discrimination-tree, term-indexing, plotkin-lgg, robinson-unification, superposition, demodulation, subsumption, trie]
sources:
  - paper: doi:10.1007/3-540-59200-8_52
    title: Peter Graf, Substitution tree indexing, Rewriting Techniques and Applications (RTA 1995), Lecture Notes in Computer Science 914
    locator: pp. 117 to 131 (substitution trees, insertion by most specific common generalization, deletion, and retrieval of generalizations, instances and unifiable terms)
  - book: isbn:9783540610403
    title: Peter Graf, Term Indexing, Lecture Notes in Computer Science 1053, Springer, 1996
    locator: the chapter Tree-based indexing (substitution trees, compared with discrimination trees and other indexes)
  - paper: doi:10.1007/3-540-45744-5_19
    title: Robert Nieuwenhuis, Thomas Hillenbrand, Alexandre Riazanov and Andrei Voronkov, On the evaluation of indexing techniques for theorem proving, International Joint Conference on Automated Reasoning (IJCAR 2001), Lecture Notes in Computer Science 2083
    locator: pp. 257 to 271 (an experimental comparison of term indexing techniques on recorded prover runs)
---

A **substitution tree** is a [term index](/term-indexing/) in which each node stores a [substitution](/substitution/), and each stored term is the composition of the substitutions on the path from the root to its leaf. Terms that agree on some of their structure share the nodes that hold it, wherever in the terms the shared part is. Peter Graf introduced the structure in 1995 for automated theorem provers, which must find among many stored terms the generalizations, the instances or the terms unifiable with a given query. Unlike a [discrimination tree](/discrimination-tree/), it keeps the names of variables, so every answer is exact and comes with its substitution.

## In plain words

Picture a family tree of terms. At the top is a template that all stored terms fit, with holes where they differ. Each child fills some of the holes, perhaps with smaller templates that have new holes of their own, and each leaf is reached when every hole has been filled, so the path to a leaf spells out one stored term.

To find the stored terms that fit a query, start at the top and try to fit each template against the query. Where a template does not fit, the whole branch below it is skipped, because every term there contains that template. To add a term, follow the branches whose templates it fits, and where it fits none, split a branch at the point where the templates stop agreeing.

## The abstract type

We use the notation of the term rewriting pages: a signature $\Sigma$, variables $V$, terms $T(\Sigma, V)$, positions as sequences of positive integers, rules $l \to r$, $\to^*$ for the reflexive transitive closure, and substitutions $\sigma$, applied on the right, so $t\sigma\tau$ applies $\sigma$ first. A term $l$ **matches** $t$ if $l\sigma = t$ for some $\sigma$, where the variables of $t$ act as constants.

The structure stores a multiset of entries $(l, v)$, a term with a value. Given a query $q$, it answers three kinds of question.

- `insert(D, l, v)` adds the entry, and `delete(D, l, v)` removes one copy of it, if there is one.
- `retrieve(D, q, generalizations)` returns the entries with $l\sigma = q$ for some $\sigma$, as needed to find the rules or equations that rewrite $q$, or the clauses that subsume it.
- `retrieve(D, q, instances)` returns the entries with $q\sigma = l$ for some $\sigma$, as needed for backward simplification.
- `retrieve(D, q, unifiable)` returns the entries such that $l$ and $q$ have a [unifier](/most-general-unifier/) after their variables are renamed apart, as needed to find the partners of a resolution or [superposition](/superposition/) inference.

## Representation

The tree uses three disjoint sets of variables. **Indicator variables** $*0, *1, *2, \ldots$ occur only inside the tree and stand for parts not yet fixed. A stored term $l$ is first **normalized**: its variables are renamed $\#1, \#2, \ldots$ in order of first occurrence, giving $\hat l$; two terms that are equal up to renaming have the same normal form. The variables of a query are renamed apart from both, as $?x$ for $x$.

Each node $x$ other than the top stores a substitution $\sigma_x$ whose domain is a set of indicator variables. The top stores the empty substitution. For a node $x$ with path $x_1, \ldots, x_k$ from below the top, its **term** is $*0\, \sigma_{x_1} \cdots \sigma_{x_k}$, and its **open variables** are the indicator variables in its term. A leaf holds a list of entries.

**Invariant.**

- **(S1) Terms.** Every node of the tree has open variables, except the leaves, which have none, and each entry $(l, v)$ at a leaf satisfies $\hat l = $ the term of the leaf. Every entry of the multiset is at exactly one leaf.
- **(S2) Domains.** The domain of $\sigma_x$ is a nonempty set of open variables of the parent of $x$, so each indicator variable is bound at most once on a path.
- **(S3) Linearity.** Each indicator variable occurs at most once in all the ranges of the substitutions of the tree.
- **(S4) Shape.** Each inner node other than the top has at least two children, and each leaf has at least one entry. The count $D.n$ is the number of entries.

So the substitutions on a path build the stored term step by step: each node fills some holes of its parent's term, possibly with new holes.

## Operations

```pseudo id=main
SUBST-INSERT(D, l, v)
L1  τ ← {*0 ↦ normalize(l)}; x ← D.top
L2  while τ is not empty do
L3      find a child c of x and a ρ, binding only the indicator variables in the range of σ_c, with σ_c(y)ρ = τ(y) for all y in dom σ_c; if there is none, exit the loop
L4      τ ← (τ without dom σ_c) ∪ ρ; x ← c
L5  if τ is empty then append (l, v) to x.entries; return              ▷ x is a leaf with a variant of l
L6  for each child c of x do
L7      (μ, α, β) ← GENERALIZE(σ_c, τ); if some μ(y) is not an indicator variable then
L8          replace c by a new node with substitution μ and two children: c with σ_c ← α, and a new leaf with substitution (τ without dom μ) ∪ β holding (l, v); return
L9  add to x a new leaf child with substitution τ, holding (l, v)

SUBST-RETRIEVE(D, q, mode)
L10 θ ← {*0 ↦ q with its variables renamed}; push the children of D.top
L11 while the stack is not empty do
L12     pop an item; if it is an undo mark k, remove the bindings of θ made after mark k, and continue
L13     x ← the popped node; k ← the current mark; unify y with σ_x(y) for every y in dom σ_x, extending θ, with the rigid variables of the mode
L14     if this succeeds and x has children then push the undo mark k, then the children of x; continue
L15     if this succeeds then output the entries of x
L16     remove the bindings of θ made after mark k

SUBST-DELETE(D, l, v)
L17 search from D.top as in lines L2 to L4, following every child that matches, for leaves reached with τ empty
L18 at such a leaf x, remove one copy of (l, v) from x.entries; if there is none anywhere, return false
L19 if x has no entries left then remove x from its parent p
L20 if p is not D.top and p has one child c left then
L21     replace p and c by one node with substitution {y ↦ σ_p(y)σ_c} ∪ (σ_c on the variables that do not occur in the range of σ_p), and the children and entries of c
```

**Insert.** The substitution $\tau$ maps the open variables of the current node $x$ to terms without indicator variables, such that the term of $x$ followed by $\tau$ is $\hat l$. Line L3 looks for a child whose substitution agrees with $\tau$ up to its own new holes, which $\rho$ fills; lines L3 and L4 descend into it. If the descent ends at a leaf, $\hat l$ is already stored, and the entry joins it (line L5). Otherwise no child fits, and line L7 computes a common generalization $\mu$ of $\sigma_c$ and $\tau$ on the domain of $\sigma_c$: walk both terms in parallel, keep the common symbols, keep an indicator variable of $\sigma_c$ where one stands, and put a fresh indicator variable $z$ elsewhere where they differ, with $\alpha(z)$ and $\beta(z)$ the two differing subterms. Then $\mu\alpha = \sigma_c$ and $\mu\beta = \tau$ on that domain. If $\mu$ has some common structure, line L8 splits $c$ there. If no child shares structure, line L9 adds a new leaf.

**Retrieve.** The three queries differ only in which variables may be bound: in a query for generalizations the query variables $?x$ are **rigid**, that is, treated as constants; for instances the stored variables $\#i$ are rigid; for unifiable terms no variable is rigid. Line L13 adds the equations $y = \sigma_x(y)$ of the node to the [unification](/robinson-unification/) problem built along the path, and line L12 or L16 undoes them when the search leaves the node, so the search is a depth-first walk with one shared substitution $\theta$ and a trail of bindings. A node whose equations fail cuts off its whole subtree.

**Delete.** Lines L17 and L18 find the leaf whose term is $\hat l$ and remove the entry. Lines L19 to L21 remove an empty leaf and merge a parent left with one child into that child, so that (S4) holds again.

## Example

Insert $f(x, a)$, $f(x, b)$, $f(g(x), a)$ and $f(x, x)$, with the values 1 to 4.

1. The first term becomes one leaf $\{*0 \mapsto f(\#1, a)\}$.
2. $f(\#1, b)$ does not match it. The generalization of $f(\#1, a)$ and $f(\#1, b)$ is $f(\#1, *1)$, so the leaf splits into a node $\{*0 \mapsto f(\#1, *1)\}$ with the leaves $\{*1 \mapsto a\}$ and $\{*1 \mapsto b\}$.
3. $f(g(\#1), a)$ does not match $f(\#1, *1)$, because $\#1$ is a stored variable, not a hole. The generalization keeps $*1$ and puts a fresh $*2$ in the first argument, so the node splits into $\{*0 \mapsto f(*2, *1)\}$ with a child $\{*2 \mapsto \#1\}$, which keeps the two old leaves, and a new leaf $\{*2 \mapsto g(\#1),\ *1 \mapsto a\}$.
4. $f(\#1, \#1)$ matches $f(*2, *1)$ with $*2 \mapsto \#1$, $*1 \mapsto \#1$, then the child $\{*2 \mapsto \#1\}$, and becomes a third leaf $\{*1 \mapsto \#1\}$ there.

```
{}
└── {*0 ↦ f(*2, *1)}
    ├── {*2 ↦ #1}
    │   ├── {*1 ↦ a}          entry 1, f(x, a)
    │   ├── {*1 ↦ b}          entry 2, f(x, b)
    │   └── {*1 ↦ #1}         entry 4, f(x, x)
    └── {*2 ↦ g(#1), *1 ↦ a}  entry 3, f(g(x), a)
```

**Generalizations of $f(a, a)$.** Start with $\theta = \{*0 \mapsto f(a, a)\}$. The root binds $*2 \mapsto a$ and $*1 \mapsto a$. The node $\{*2 \mapsto \#1\}$ binds $\#1 \mapsto a$. Under it, $\{*1 \mapsto a\}$ succeeds and outputs entry 1, $\{*1 \mapsto b\}$ fails since $a \ne b$, and $\{*1 \mapsto \#1\}$ compares $a$ with $\theta(\#1) = a$ and outputs entry 4. The last node fails at once, since $*2$ is bound to $a$, and $a$ does not unify with $g(\#1)$. The answer is $\{1, 4\}$.

The other queries, run by the implementation: the generalizations of $f(g(b), a)$ are entries 1 and 3; the terms unifiable with $f(a, y)$ are entries 1, 2 and 4; the instances of $f(g(z), y)$ are entry 3 only, since $f(x, a)$ is not an instance of it.

**Delete.** Deleting $f(g(x), a)$ removes the last leaf, which leaves the root with one child. Lines L20 and L21 merge $\{*0 \mapsto f(*2, *1)\}$ and $\{*2 \mapsto \#1\}$ into $\{*0 \mapsto f(\#1, *1)\}$, with the three leaves below it.

## Correctness

The invariant and the claims below are proved in [the correctness proof](proofs/correctness.md).

- **Insert keeps the invariant.** Along the descent, the term of $x$ followed by $\tau$ is always $\hat l$, because $\sigma_c(y)\rho = \tau(y)$. A split puts $\mu$ above both $\alpha$ and the new leaf, and $\mu\alpha = \sigma_c$, $\mu\beta = \tau$ on the domain of $\sigma_c$, so the terms of all old leaves are unchanged and the new leaf has the term $\hat l$.
- **Retrieval is exact.** For a leaf with term $\hat l$, the equations $*0 = q'$ and $y = \sigma_{x_i}(y)$ along its path have a solution that binds no rigid variable iff $\hat l$ and the renamed query $q'$ have one, because the equations of the path only name the parts of $\hat l$. Robinson unification run equation by equation finds such a solution iff one exists, and a failure at a node implies failure at every leaf below. With rigid query variables, a solution is a matcher of $\hat l$ onto $q$; with rigid stored variables, it is a matcher of $q$ onto $\hat l$; with none, it is a unifier.
- **Delete keeps the invariant.** The merged node has the substitution of the path from $p$ to $c$, so no term changes.

## Complexity

Let $n$ be the size of the query, $m$ the size of an inserted or deleted term, and $S$ the total size of the substitutions in the tree. All loops use explicit stacks.

| operation | time |
|---|---|
| insert | $O(S + m)$ |
| retrieve generalizations | $O(S n)$ |
| retrieve instances or unifiable terms | one unification for each visited node |
| delete | $O(S d)$ for a tree of depth $d$ |
| space | $O(S)$ |

**Insert.** Each child of a visited node is tried once by matching (line L3) and at most once by generalization (line L7), and both walk the child's substitution in parallel with $\tau$ and stop at its holes, so they cost $O(|\sigma_c|)$. Each node is visited at most once.

**Generalizations.** With rigid query variables, every variable bound during the search is bound to a subterm of the query, so each variable occurrence in $\sigma_x$ costs $O(n)$, for a comparison or an occurs check, and a node with a substitution of size $s$ costs $O(s n)$.

**Unification queries.** Bindings may now point into the tree, and the cost of one node depends on the unification algorithm; the simple algorithm of the implementation is not linear in the worst case, while a linear-time algorithm such as [Paterson-Wegman unification](/paterson-wegman-unification/) bounds each step by the sizes of the terms involved.

**Delete.** The search may follow several matching children, and copies the path for each.

**Pruning.** The real gain is in the nodes not visited: a failure at a node near the top removes all the stored terms below it, and a stored term is never compared with the query as a whole.

## Variants

- **Most specific common generalization.** Graf (1995) splits with the most specific common generalization of $\sigma_c$ and $\tau$, the [least general generalization](/plotkin-lgg/) of the two substitutions, which uses one indicator variable for each repeated pair of differing subterms. The implementation puts a fresh variable at each differing position, which keeps the indicator variables linear and the matching at line L3 simple, at the price of less sharing for terms with repeated parts.
- **Choice of the child.** Insertion here takes the first child that shares some structure. Other choices give other trees, and the shape of the tree also depends on the order of insertion.
- **Other term indexes.** A [discrimination tree](/discrimination-tree/) shares common prefixes of the preorder string of a term and replaces variables by one symbol, so its answers are only candidates. Path indexing intersects sets of root-to-leaf paths. The [term indexing](/term-indexing/) page compares them.

## When to use it

Use a substitution tree when a large and changing set of terms is queried for all three kinds of retrieval, as in saturation provers for first-order logic with equality: the generalizations of a term find the [demodulators](/demodulation/) that rewrite it and the clauses that [subsume](/subsumption/) it, its instances find the clauses that it can simplify, and unifiable terms find the partners of inferences. When only generalizations are needed and the patterns are mostly linear, a discrimination tree is simpler and fast.

## Pitfalls

- **Treating stored variables as holes.** The stored variables $\#i$ are part of the stored term. At line L3 only indicator variables may be bound; matching $f(\#1, *1)$ against $f(g(\#1), a)$ must fail.
- **Variables of different terms.** All stored terms use the names $\#1, \#2, \ldots$, so the query must be renamed apart, and bindings must be undone on backtracking, or a binding from one branch leaks into another.
- **Occurs check.** Without it, a query for unifiable terms reports $f(x, g(x))$ as unifiable with $f(y, y)$.
- **Shape after deletion.** Without the merge of lines L20 and L21, deletions leave chains of nodes with one child, and the tree loses its sharing.
- **Recursion depth.** Stored terms can be very deep. The implementation uses explicit stacks for matching, generalization, unification and the traversal.

## Implementations

## History

Graf introduced substitution trees in 1995, with insertion by most specific common generalization, deletion, and the three retrieval operations, and described them with other term indexes in his book (Graf, 1996). Nieuwenhuis, Hillenbrand, Riazanov and Voronkov (2001) proposed evaluating term indexes on queries recorded from real prover runs, and compared several indexing techniques that way.

## References
