---
tag: YVT6ET
kind: data-structure
slug: sentential-decision-diagram
name: Sentential decision diagram
aliases:
- SDD
area: information-retrieval-and-ai-reasoning/knowledge-representation-and-description-logics
level: research
summary: A canonical circuit for a fixed variable tree that splits a function into prime and sub pairs. It generalizes OBDDs, and its apply is polynomial when the result is not compressed.
model: word-ram
complexity:
  vars: {s: the size of the first SDD (its number of elements), t: the size of the second SDD, n: the number of variables}
  time: {apply_uncompressed: O(s t), negate: O(s), model_count: O(s), evaluate: O(s)}
  space: {sdd: O(s)}
properties: {persistent: true, concurrent: false, external: false}
history:
  year: 2011
  people: [Adnan Darwiche]
  note: Darwiche defined SDDs, proved that compressed and trimmed SDDs are canonical for a fixed vtree, gave the apply operation, and showed that an SDD on a right-linear vtree is an OBDD.
prereqs: [d-dnnf, ordered-binary-decision-diagram, bdd-apply]
see_also: [knowledge-compilation-map, bdd-canonicity, reduced-ordered-bdd, model-counting, treewidth, hash-consing, decision-diagram, bayesian-network]
sources:
  - paper: "Adnan Darwiche, SDD: A new canonical representation of propositional knowledge bases, Proceedings of the Twenty-Second International Joint Conference on Artificial Intelligence (IJCAI), 2011"
    locator: Definition 1 (X-partition), Theorem 3 (the compressed partition is unique), Definitions 4 and 5 (vtree and SDD), Definitions 6 and 8 (compressed and trimmed), Theorem 10 (canonicity), Algorithm 1 (apply), Section 6 (OBDDs as SDDs on right-linear vtrees), Theorems 12 and 13 (size bounds by treewidth and pathwidth)
  - paper: "Guy Van den Broeck and Adnan Darwiche, On the role of canonicity in knowledge compilation, Proceedings of the Twenty-Ninth AAAI Conference on Artificial Intelligence, 2015, pages 1641 to 1648"
    locator: apply with compression can take exponential time, and dropping compression keeps apply polynomial (general locator)
  - paper: "Simone Bova, SDDs are exponentially more succinct than OBDDs, Proceedings of the Thirtieth AAAI Conference on Artificial Intelligence, 2016"
    locator: a family of functions with polynomial SDDs and only exponential OBDDs (general locator)
  - paper: doi:10.1613/jair.989
    title: Adnan Darwiche and Pierre Marquis, A knowledge compilation map, Journal of Artificial Intelligence Research 17, 2002
    locator: Table 5 on page 239 (the polynomial queries of d-DNNF and OBDD)
---

A sentential decision diagram (SDD) is a Boolean circuit that splits a function on a set of variables at a time, where an [OBDD](/ordered-binary-decision-diagram/) splits on one variable at a time. A binary tree over the variables, the *vtree*, fixes which sets are used. Darwiche (2011) introduced SDDs as a target language for [knowledge compilation](/knowledge-compilation/) that keeps the two strengths of OBDDs, a canonical form and an apply operation that combines two diagrams, while it reaches more functions in small size. Every SDD is a [d-DNNF](/d-dnnf/); the d-DNNF page covers the general circuit class and its linear-time queries, and this page covers the vtree, the canonical form and apply, which a general d-DNNF does not have.

## In plain words

Split the variables into a left group and a right group. Any function can be written as a list of cases: for each case, a condition on the left variables and a function of the right variables that holds in that case. The conditions never overlap and together cover everything, so exactly one case applies. Do the same split again inside each condition and each right-hand function, using a fixed tree that says how to split each group. If you also merge cases with the same right-hand function, and store each piece once, every function gets exactly one diagram for a given tree. So two diagrams mean the same thing exactly when they are the same object. To combine two diagrams with "and" or "or", pair up their cases and combine the parts.

## The abstract type

A **vtree** over the variables $X$ is a full binary tree whose leaves are in one-to-one correspondence with $X$. For an inner node $v$, $v^l$ and $v^r$ are its left and right children, and $\mathrm{vars}(v)$ is the set of variables at the leaves below $v$.

For a function $f$ and a split of its variables into $X$ and $Y$, an **$X$-partition** of $f$ (Darwiche 2011, Definition 1) is a set $\{(p_1, s_1), \ldots, (p_k, s_k)\}$ of **elements** with **primes** $p_i$ over $X$ and **subs** $s_i$ over $Y$ such that

$$f = (p_1 \wedge s_1) \vee \cdots \vee (p_k \wedge s_k),$$

each prime is satisfiable, the primes are pairwise inconsistent, and $p_1 \vee \cdots \vee p_k \equiv \mathit{true}$. The partition is **compressed** if the subs are distinct. Each function has exactly one compressed $X$-partition (Theorem 3): the subs are the distinct functions $f|x$ over the assignments $x$ to $X$, and the prime of a sub $s$ is the set of $x$ with $f|x = s$.

An **SDD** that respects the vtree node $v$ (Definitions 4 and 5) is $\mathit{true}$, $\mathit{false}$, a literal of the variable at a leaf $v$, or a **decomposition** at an inner node $v$: a set of elements $(p_i, s_i)$ where the $p_i$ are SDDs that respect nodes in the subtree of $v^l$, the $s_i$ are SDDs that respect nodes in the subtree of $v^r$, and the functions of the $p_i$ form a $\mathrm{vars}(v^l)$-partition. An SDD is **compressed** if every decomposition has distinct subs, and **trimmed** if no decomposition has the form $\{(\mathit{true}, \alpha)\}$ or $\{(\alpha, \mathit{true}), (\neg\alpha, \mathit{false})\}$ (Definitions 6 and 8). For a fixed vtree, two equivalent compressed and trimmed SDDs are equal (Theorem 10).

Read as a circuit, a decomposition is an or-node over and-nodes $p_i \wedge s_i$. The and-nodes are decomposable, because $p_i$ and $s_i$ use the disjoint sets $\mathrm{vars}(v^l)$ and $\mathrm{vars}(v^r)$, and the or-node is deterministic, because the primes are pairwise inconsistent. So an SDD is a d-DNNF in which the vtree fixes how each and-node splits the variables.

The operations are APPLY with $\wedge$ or $\vee$, NEGATE, COUNT (the model count) and the equivalence test, which is a comparison of two node ids.

## Representation

A manager holds one vtree and every node built for it. Node 0 is $\mathit{false}$ and node 1 is $\mathit{true}$. A literal node stores the literal, and a decomposition node stores its vtree node $v$ and the sorted tuple of its elements as pairs of node ids. Each node also records the vtree node it respects, written $\mathrm{vt}(u)$. A unique table maps each key to one id ([hash-consing](/hash-consing/)), so by canonicity two ids are equal if and only if their functions are equal. Each vtree node stores its parent, its depth and the interval of its leaves in left-to-right order. The interval gives the test "is $a$ in the subtree of $v$" in constant time, and the depth gives the lowest common ancestor by walking up. APPLY keeps a cache keyed by the operator and the two ids, and NEGATE keeps a cache by id. The size of an SDD is the total number of elements in its decompositions.

## Operations

APPLY combines two SDDs for the same vtree. It brings both to the lowest common ancestor $v$ of the vtree nodes they respect and multiplies their partitions.

```pseudo id=main
APPLY(α, β, ∘)                            ▷ ∘ is ∧ or ∨; returns a compressed, trimmed SDD
L1  if α or β is a constant, or α = β, then return the result by the rules of ∘
L2  if (∘, α, β) is in the cache then return it
L3  if α and β are the two literals of one variable then r ← false if ∘ = ∧, else true
L4  else v ← the lowest common ancestor of vt(α) and vt(β)
L5      E ← ∅
L6      for each (p, s) in ELEMENTS(α, v) do
L7          for each (q, t) in ELEMENTS(β, v) do
L8              pq ← APPLY(p, q, ∧)
L9              if pq ≠ false then add (pq, APPLY(s, t, ∘)) to E
L10     r ← UNIQUE(v, E)
L11 store r in the cache; return r
```

ELEMENTS writes a node as a partition at an ancestor, and UNIQUE makes the result compressed and trimmed and looks it up.

```pseudo id=helpers
ELEMENTS(u, v)                            ▷ vt(u) is in the subtree of v
L12 if vt(u) = v then return the elements of u
L13 if vt(u) is in the subtree of v^l then return {(u, true), (NEGATE(u), false)}
L14 return {(true, u)}

UNIQUE(v, E)                              ▷ E is a partition at v
L15 merge the elements with equal subs: (p, s) and (p', s) become (APPLY(p, p', ∨), s)
L16 if one element (true, s) is left then return s
L17 if the elements are (a, true) and (b, false) then return a
L18 return the node for (v, E) from the unique table, made if it is new

NEGATE(u)                                 ▷ constants swap
L19 if u is a literal then return the opposite literal
L20 return UNIQUE(vt(u), {(p, NEGATE(s)) : (p, s) ∈ u})

COUNT(u, w)                               ▷ models of u over vars(w); vt(u) is in the subtree of w
L21 if u = false then return 0; if u = true then return 2^|vars(w)|
L22 c ← 1 if u is a literal, else the sum over (p, s) ∈ u of COUNT(p, v^l) · COUNT(s, v^r), with v = vt(u)
L23 return c · 2^(|vars(w)| - |vars(vt(u))|)
```

To build the SDD of a formula, start from literals and apply the connectives bottom up. The model count over all variables is COUNT$(u, \text{root})$, with a memo on $u$ for line L22. Two SDDs for the same vtree are equivalent if and only if they are the same node.

## Example

Take $f = (x_1 \wedge x_2) \vee (x_3 \wedge x_4)$ and the balanced vtree $((x_1, x_2), (x_3, x_4))$. At the root the left variables are $\{x_1, x_2\}$. The assignments to them give two distinct subfunctions, $\mathit{true}$ when $x_1 \wedge x_2$ and $x_3 \wedge x_4$ otherwise, so the root decomposition is

$$\{(x_1 \wedge x_2,\ \mathit{true}),\ (\neg(x_1 \wedge x_2),\ x_3 \wedge x_4)\}.$$

The primes and the sub are decompositions at the two inner children:

| function | vtree node | elements |
|---|---|---|
| $x_1 \wedge x_2$ | $(x_1, x_2)$ | $(x_1, x_2), (\neg x_1, \mathit{false})$ |
| $\neg(x_1 \wedge x_2)$ | $(x_1, x_2)$ | $(x_1, \neg x_2), (\neg x_1, \mathit{true})$ |
| $x_3 \wedge x_4$ | $(x_3, x_4)$ | $(x_3, x_4), (\neg x_3, \mathit{false})$ |

The size is $2 + 2 + 2 + 2 = 8$. COUNT at the root gives $1 \cdot 4 + 3 \cdot 1 = 7$: the prime $x_1 \wedge x_2$ has 1 model over $\{x_1, x_2\}$ and the sub $\mathit{true}$ has 4 over $\{x_3, x_4\}$, and the prime $\neg(x_1 \wedge x_2)$ has 3 models and the sub $x_3 \wedge x_4$ has 1. On the right-linear vtree $(x_1, (x_2, (x_3, x_4)))$ the same function has three decompositions of two elements each, size 6. They are the OBDD nodes for $x_1$, $x_2$ and $x_3$, and the OBDD node for $x_4$ is the literal $x_4$. With the order $x_1, x_3, x_2, x_4$ on a right-linear vtree the size is 8.

The vtree decides the size. For $f_k = (x_1 \wedge y_1) \vee \cdots \vee (x_k \wedge y_k)$, the implementation on this page gives these sizes:

| $k$ | right-linear, $x_1, y_1, x_2, y_2, \ldots$ | right-linear, $x_1, \ldots, x_k, y_1, \ldots, y_k$ | balanced, $x_1, y_1, x_2, y_2, \ldots$ |
|---|---|---|---|
| 1 | 2 | 2 | 2 |
| 2 | 6 | 8 | 8 |
| 3 | 10 | 22 | 17 |
| 4 | 14 | 52 | 22 |
| 5 | 18 | 114 | 36 |

The first column grows linearly and the second exponentially, as for OBDDs with the same orders.

## Correctness

The proofs are in the [correctness proof](proofs/correctness.md). In short:

- **APPLY computes $\alpha \circ \beta$.** After ELEMENTS, both inputs are partitions at the same node $v$. The nonempty products $p \wedge q$ are pairwise inconsistent and cover all assignments to $\mathrm{vars}(v^l)$, and on an assignment in $p \wedge q$ the function $\alpha \circ \beta$ equals $s \circ t$. So $E$ is a partition of $\alpha \circ \beta$.
- **UNIQUE keeps the function.** Merging two elements with the same sub gives one element whose prime is the union, which keeps the partition. A partition with one element has the prime $\mathit{true}$, and a partition with the subs $\mathit{true}$ and $\mathit{false}$ is equal to the prime of $\mathit{true}$.
- **The result is compressed and trimmed**, by lines L15 to L17 and induction on the calls.
- **Canonicity.** A compressed and trimmed decomposition depends on a variable on each side of its vtree node, so the node it respects is the lowest common ancestor of the variables the function depends on. Its elements are the unique compressed partition of Theorem 3. By induction the primes and subs are unique, and the unique table returns one id.
- **COUNT.** The primes of a decomposition have disjoint model sets, and each model of $p_i \wedge s_i$ over $\mathrm{vars}(v)$ is a model of $p_i$ over $\mathrm{vars}(v^l)$ joined with a model of $s_i$ over $\mathrm{vars}(v^r)$, so the counts multiply and add. Variables of $w$ outside $\mathrm{vars}(\mathrm{vt}(u))$ are free, which gives the factor of line L23.

## Complexity

| operation | time |
|---|---|
| APPLY without lines L15 to L17 | $O(s t)$ (Darwiche 2011, Algorithm 1) |
| APPLY with compression | exponential in the worst case (Van den Broeck and Darwiche 2015) |
| NEGATE | $O(s)$ expected |
| COUNT | $O(s)$ additions and multiplications of numbers of at most $n$ bits |
| equivalence | $O(1)$ |

Without compression, each pair of elements makes at most one recursive pair of calls, and the cache gives each pair of nodes one call, which bounds the work by the product of the sizes. Compression calls APPLY with $\vee$ on primes inside UNIQUE, and Van den Broeck and Darwiche (2015) give functions for which this makes the result, and the time, exponential in the input sizes. The implementation on this page compresses, so it pays this cost when it occurs. NEGATE does no merging, because the negated subs are still distinct and are never exactly $\{\mathit{true}, \mathit{false}\}$ unless the original subs were, which trimming excludes.

As a d-DNNF, an SDD supports in polynomial time all the queries that Darwiche and Marquis (2002, Table 5) list for d-DNNF, including consistency, validity, clause entailment, model counting and model enumeration. Canonicity adds the equivalence test. Darwiche (2011, Theorems 12 and 13) shows that a CNF with $n$ variables and [treewidth](/treewidth/) $w$ has an SDD of size $O(n 2^w)$, while the corresponding OBDD bound uses the pathwidth in place of the treewidth. Bova (2016) gives functions with SDDs of polynomial size whose OBDDs all have exponential size.

## Variants

- **OBDD.** On a right-linear vtree, where every left child is a leaf, every prime is a literal or a constant, and the SDD is the reduced OBDD for the left-to-right order of the leaves (Darwiche 2011, Section 6). APPLY then works like [OBDD apply](/bdd-apply/).
- **Uncompressed SDDs.** Dropping line L15 gives polynomial APPLY at the cost of canonicity (Van den Broeck and Darwiche 2015).
- **Weighted counting.** Replace the 1 of a literal at line L22 by its weight and the power of 2 at lines L21 and L23 by the product of the sums of the weights of the free variables. With weights from a [Bayesian network](/bayesian-network/) this gives probabilities.

## When to use it

Use an SDD when a knowledge base is built up incrementally by conjunction and disjunction, as with an OBDD, and an OBDD for every variable order is too large. Choose the vtree from the structure of the problem: a vtree that follows a tree decomposition of a CNF gives the treewidth bound above. When the knowledge base is fixed and only needs counting or entailment queries, a [d-DNNF](/d-dnnf/) compiled by search can be smaller, because it does not have to follow one vtree.

## Pitfalls

- **Mixing vtrees.** APPLY and the equivalence test are defined only for two SDDs of one manager. The same function has different SDDs on different vtrees.
- **Normalizing at the wrong node.** The result of APPLY must be trimmed. If a decomposition $\{(\mathit{true}, s)\}$ is kept, the same function has two ids, and the equivalence test by id fails.
- **Counting over the wrong variables.** A node that respects $v$ counts models over $\mathrm{vars}(v)$ only. A sub $\mathit{true}$, or a node that respects a lower vtree node, needs the factor of line L23.
- **Primes that are not exclusive.** Building a decomposition by hand from overlapping conditions gives a circuit that is not deterministic, and COUNT then overcounts.

## Implementations

## History

Darwiche introduced SDDs in 2011 with the canonicity theorem, the apply operation and the treewidth bound, and showed that OBDDs are the SDDs on right-linear vtrees. Van den Broeck and Darwiche (2015) showed that apply with compression is not polynomial in the worst case and studied SDDs without compression. Bova (2016) showed that SDDs are exponentially more succinct than OBDDs.

## References
