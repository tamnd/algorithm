---
tag: CGCZ15
kind: problem
slug: anti-unification-problem
name: Anti-unification problem
aliases:
- generalization problem
- least general generalization problem
area: logic-and-constraints/unification-and-resolution
level: advanced
summary: Given terms, compute a least general generalization, the most specific pattern that has all of them as instances.
model: word-ram
complexity:
  vars: {N: the total size of the input terms}
  time: {lgg: O(N)}
  space: {extra: O(N)}
prereqs: [term, substitution, unification-problem]
see_also: [plotkin-lgg, most-general-unifier, term-matching, clause-subsumption, equational-unification, substitution-tree, term-indexing]
sources:
  - paper: "G. D. Plotkin, A note on inductive generalization, in B. Meltzer and D. Michie (editors), Machine Intelligence 5, Edinburgh University Press, 1970, pages 153 to 163"
    locator: the least general generalization of terms and of clauses, its existence and uniqueness, and the algorithm
  - paper: "J. C. Reynolds, Transformational systems and the algebraic structure of atomic formulas, in B. Meltzer and D. Michie (editors), Machine Intelligence 5, Edinburgh University Press, 1970, pages 135 to 151"
    locator: the lattice of atomic formulas, with generalization as the meet and unification as the join
  - paper: "G. D. Plotkin, A further note on inductive generalization, in B. Meltzer and D. Michie (editors), Machine Intelligence 6, Edinburgh University Press, 1971, pages 101 to 124"
    locator: generalization relative to background knowledge (relative least general generalization)
---

The **anti-unification problem** asks, for two or more terms, for their **least general generalization** (lgg): the most specific term that has each of them as an instance. It is the dual of the [unification problem](/unification-problem/). Unification looks for a common instance below the terms, and anti-unification looks for a common pattern above them. For first-order terms, Plotkin and Reynolds showed in 1970 that the lgg always exists and is unique up to renaming, and [Plotkin's algorithm](/plotkin-lgg/) computes it in linear time. Modulo equational theories, for clauses, and for higher-order terms, the problem changes: the lgg can be large, can fail to be unique, or can fail to exist.

## In plain words

You have several examples, such as `add(1, 2)` and `add(3, 3)`. You want one pattern that covers all of them, with blanks where they differ. A pattern made of only one blank covers everything, but it says nothing. The problem asks for the most exact pattern that still covers all the examples, such as `add(A, B)` here.

Some examples share more structure. For `pair(1, 1)` and `pair(2, 2)`, the pattern `pair(A, A)` says that the two parts are always equal, so it is more exact than `pair(A, B)`. The answer keeps every such link that holds in all the examples.

## Definition

Notation: $\sigma, \eta, \lambda$ are substitutions, $t\sigma$ is the application of $\sigma$ to $t$, and $N$ is the total number of symbol occurrences of the input. For terms, $h \le g$ means that $g = h\lambda$ for some $\lambda$, so $g$ is an instance of $h$ and $h$ is at least as general as $g$.

A **generalization** of terms $s_1, \ldots, s_n$ is a term $h$ with substitutions $\eta_1, \ldots, \eta_n$ such that $h\eta_i = s_i$ for each $i$. A generalization $g$ is **least general** if $h \le g$ for every generalization $h$.

**Input:** terms $s_1, \ldots, s_n$ with $n \ge 2$.

**Output:** a least general generalization $g$, with substitutions $\theta_1, \ldots, \theta_n$ such that $g\theta_i = s_i$.

A generalization always exists, since a single variable $z$ is one. So the problem has no decision version: the task is to compute the lgg. The variables of the inputs are treated like constants.

**Facts (Plotkin 1970, Reynolds 1970).** For first-order terms:

- the lgg exists;
- it is unique up to renaming of variables;
- its size is at most the size of the smallest input;
- terms modulo renaming, ordered by $\le$ and with a top element added, form a lattice, in which the lgg is the meet and the most general common instance is the join.

## Variants

- **Two terms or $n$ terms.** The lgg is associative and commutative up to renaming, so the lgg of $n$ terms can be computed pairwise. One pass with a table keyed by $n$-tuples of subterms also works.
- **Clauses.** Plotkin defined the lgg of two clauses under [subsumption](/clause-subsumption/): a clause $C$ subsumes $D$ when $C\sigma \subseteq D$ for some $\sigma$. The lgg pairs every literal of the first clause with every literal of the second that has the same predicate and sign, and generalizes all the pairs with one shared table. It exists and is unique up to subsumption equivalence, but it can have $|C| \cdot |D|$ literals, and for $n$ clauses the product of their sizes.
- **Relative lgg.** Plotkin (1971) defined generalization relative to background knowledge. The relative lgg may not be finite, and systems such as Golem compute it relative to a finite set of ground facts.
- **Modulo equational theories.** If some symbols are associative, commutative, or both, a lgg can fail to be unique. The answer is then a minimal complete set of generalizations, which is finite for these theories. Some other theories have no minimal complete set. This mirrors the [unification types](/equational-unification/) of equational unification.
- **Higher-order terms.** For lambda terms, the lgg is not unique in general. For higher-order patterns, where free variables are applied only to distinct bound variables, a unique lgg exists and can be computed efficiently.
- **Matching.** The related test of whether $g \le s$ for given $g$ and $s$ is [term matching](/term-matching/).

## Examples

| inputs | lgg | note |
|---|---|---|
| $f(a, b)$, $f(c, b)$ | $f(Z_0, b)$ | the common $b$ stays |
| $f(a, a)$, $f(b, b)$ | $f(Z_0, Z_0)$ | one pair, one variable |
| $f(a, b)$, $f(b, a)$ | $f(Z_0, Z_1)$ | the pairs $(a, b)$ and $(b, a)$ differ |
| $f(g(a), a, h(a))$, $f(g(b), b, h(c))$ | $f(g(Z_0), Z_0, h(Z_1))$ | the link between positions 1.1 and 2 is kept |
| $f(a)$, $g(a)$ | $Z_0$ | different top symbols |
| $f(x, x)$, $f(x, y)$ | $f(x, Z_0)$ | input variables act like constants |
| $f(a, a, b)$, $f(b, b, a)$, $f(c, c, a)$ | $f(Z_0, Z_0, Z_1)$ | three terms |

The clause example: the lgg of $\{P(a), Q(a)\}$ and $\{P(b), Q(b)\}$ is $\{P(Z_0), Q(Z_0)\}$. The lgg of $\{P(a, b)\}$ and $\{P(b, a), P(a, a)\}$ pairs $P(a, b)$ with both literals and gives $\{P(Z_0, Z_1), P(a, Z_1)\}$, because the pair $(b, a)$ occurs twice and gets one variable. This clause is subsumption equivalent to $\{P(a, Z_1)\}$.

## Known algorithms

| algorithm | setting | time |
|---|---|---|
| [Plotkin's algorithm](/plotkin-lgg/) | two first-order terms | $O(N)$ expected, with hash consing of subterms |
| the same, with a table of $n$-tuples | $n$ first-order terms | $O(N)$ expected |
| Plotkin's clause lgg | two clauses | proportional to the product of the clause sizes |
| completion and rule-based algorithms | modulo associativity and commutativity | finite complete sets |
| pattern anti-unification | higher-order patterns | polynomial |

Plotkin's algorithm walks the terms together, copies agreeing symbols, and puts a new variable at each disagreeing pair, with the same variable for the same pair. The table of pairs is what makes the result least general.

## Bounds

- **First-order terms.** Reading the input takes $\Omega(N)$ time, so the linear time of Plotkin's algorithm is optimal. The output has at most $\min_i |s_i|$ symbols. This is a contrast with unification, where the solved form on trees can be exponentially large.
- **Clauses.** The clause lgg of $n$ clauses can have $\prod_i |C_i|$ literals before reduction, which is exponential in $n$. Reducing it to a smallest equivalent clause needs subsumption tests, and clause subsumption is NP-complete.
- **Equational theories.** For associative or commutative symbols, a minimal complete set of generalizations can have more than one element, so an algorithm must output a set, and its size depends on the input.

## Reductions

- **Duality with unification.** Unification computes the join of the lattice of terms, and anti-unification computes the meet. The two problems are not reducible to each other, but many proofs carry over: existence and uniqueness up to renaming have the same shape as the [unification theorem](/mgu-existence-theorem/).
- **From $n$ terms to two.** By associativity, $\mathrm{lgg}(s_1, \ldots, s_n) = \mathrm{lgg}(\mathrm{lgg}(s_1, \ldots, s_{n-1}), s_n)$ up to renaming.
- **From clauses to terms.** Each pair of compatible literals is a term pair, and one shared table across all pairs gives the clause lgg.
- **Checking a candidate.** Whether $h$ is a generalization of $s$ is a [matching](/term-matching/) problem, so a candidate answer can be checked in linear time.

## Applications

- **Inductive logic programming.** Plotkin introduced the lgg as a model of induction from examples. Clause lgg and relative lgg are the core of systems that learn logic programs from examples.
- **Term indexing.** [Substitution trees](/substitution-tree/) store a set of terms under their common generalizations, so that a query is compared once against the shared part. See [term indexing](/term-indexing/).
- **Program analysis and refactoring.** Anti-unification of syntax trees finds the common shape of similar code fragments, for clone detection and for extracting a function from repeated code.
- **Proof and program synthesis.** Generalizing the steps of several proofs or traces gives a lemma or a loop body.
- **Analogy.** The lgg of two structures is the common structure that an analogy maps.

## References
