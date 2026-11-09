---
tag: 9GTMK7
kind: algorithm
slug: paramodulation
name: Paramodulation
aliases:
- equality inference
- paramodulation rule
area: logic-and-constraints/unification-and-resolution
level: advanced
summary: Inference rule for equality. It replaces a subterm that unifies with one side of an equation by the other side. With resolution, factoring and x = x it is refutation complete (Robinson and Wos 1969).
solves: [first-order-theorem-proving]
model: word-ram
complexity:
  vars: {N: the number of clauses stored when the run stops, k: the largest number of literals in a clause, w: the largest clause size in symbols}
  time: {worst: O(N^2 k w (k^k + w^2))}
  space: {extra: O(N w)}
properties: {deterministic: true, exact: false, online: false, recursive: false, in_place: false}
history:
  year: 1969
  people: [George Robinson, Lawrence Wos]
  note: Robinson and Wos introduced paramodulation and proved it refutation complete for equality, together with resolution and factoring, on sets that contain x = x and the functional reflexivity axioms.
prereqs: [binary-resolution, factoring, robinson-resolution, most-general-unifier]
see_also: [superposition, demodulation, knuth-bendix-completion, congruence-closure, narrowing, equational-theory, robinson-completeness-theorem, lifting-lemma]
sources:
  - paper: "George Robinson and Lawrence Wos, Paramodulation and theorem-proving in first-order theories with equality, in Machine Intelligence 4, Edinburgh University Press, 1969, 135-150"
    locator: the paramodulation rule and the completeness theorem for functionally reflexive sets
  - paper: "Daniel Brand, Proving theorems with the modification method, SIAM Journal on Computing 4(4), 412-430, 1975"
    locator: completeness without the functional reflexivity axioms
  - paper: doi:10.1137/0212006
    title: Gerald E. Peterson, A technique for establishing completeness results in theorem proving with equality, SIAM Journal on Computing 12(1), 1983
    locator: completeness without paramodulation into variables and without functional reflexivity
  - book: isbn:9780121703509
    title: Chin-Liang Chang and Richard Char-Tung Lee, Symbolic Logic and Mechanical Theorem Proving, Academic Press, 1973
    locator: Chapter 8, the equality relation and paramodulation
  - book: isbn:9780444508133
    title: Alan Robinson and Andrei Voronkov (eds.), Handbook of Automated Reasoning, Elsevier and MIT Press, 2001
    locator: Chapter 7, Robert Nieuwenhuis and Albert Rubio, Paramodulation-based theorem proving
---

Paramodulation is the inference rule that lets a resolution prover reason with equality without the equality axioms. From a clause that holds an equation $l = r$ and a clause that holds a term $u$ that unifies with $l$, it builds the second clause with $u$ replaced by $r$, under the most general unifier, together with the other literals of both clauses. George Robinson and Lawrence Wos introduced it in 1969. With [binary resolution](/binary-resolution/), [factoring](/factoring/) and the axiom $x = x$, it is refutation complete for first-order logic with equality: Robinson and Wos proved this when the input also holds the functional reflexivity axioms, and Brand (1975) and Peterson (1983) showed that these axioms are not needed. Paramodulation is unrestricted: any side of any positive equation may replace any non-variable subterm. [Superposition](/superposition/) is its ordered form, and [demodulation](/demodulation/) is the simplification that rewrites with unit equations and deletes the old clause.

## In plain words

Resolution knows nothing about "equals". If a rule says that $f(a)$ equals $g(a)$, and a fact talks about $f(a)$, plain resolution cannot use the rule to talk about $g(a)$.

Paramodulation fills this gap. It takes an equation and a fact. Where the fact contains one side of the equation, it writes a new fact with the other side in that place. Variables may be filled in on the way, so that the two sides fit.

You could instead add rules that say "equals can be swapped" for every symbol. That works, but it makes a huge number of useless steps. Paramodulation does the swap in one step, and it needs only one extra rule: everything equals itself.

## The problem

The input is a finite set $S$ of first-order clauses, in which the binary predicate $=$ means equality. The question is whether $S$ is **E-unsatisfiable**: false in every interpretation in which $=$ is the identity. This holds exactly when $S$ together with the equality axioms (reflexivity, symmetry, transitivity, and substitution for each function and predicate symbol) is unsatisfiable. The loop answers UNSAT with a refutation, SATURATED, or UNKNOWN at the clause limit.

**Paramodulation.** Let $C \vee l = r$ and $D$ be clauses with no common variables, let $u$ be a subterm of a literal of $D$ at a position that does not hold a variable, and let $\sigma$ be a most general unifier of $l$ and $u$. The paramodulant is

$$(C \vee D[r])\sigma,$$

where $D[r]$ is $D$ with this occurrence of $u$ replaced by $r$. The equation is used in both directions: $r = l$ gives the same rule with $l$ and $r$ swapped.

**Functional reflexivity.** For a function symbol $f$ of arity $n$, the axiom $f(x_1, \ldots, x_n) = f(x_1, \ldots, x_n)$. It is an instance of $x = x$, but paramodulation into it builds instances that an inference into a variable would build, for example $f(a) = f(b)$ from $a = b$.

## The algorithm

The loop is the given-clause loop of Robinson's resolution principle with a paramodulation step at line L10.

```pseudo id=main
PARAMODULATION(S, limit, k)
L1  store the clauses of S, the clause x = x, and a functional reflexivity axiom for each function symbol of S
L2  while some stored clause was not taken
L3      G ← the lightest untaken clause, or the oldest one at every k-th pick
L4      if G = □ then return UNSAT
L5      if G was not stored at line L1, and G is a tautology or a clause of active subsumes G, then continue
L6      remove from active every clause not stored at line L1 that G subsumes
L7      add G to active
L8      new ← the factors of G
L9      for each clause A of active: add the binary resolvents of G and A to new
L10         add the paramodulants from G into A and from A into G to new
L11     store each clause of new that was not stored before
L12     if more than limit clauses are stored then return UNKNOWN
L13 return SATURATED
```

Line L10 uses every positive equation of one clause, in both directions, at every non-variable subterm of every literal of the other clause, after the second clause is renamed apart. Line L9 and line L10 run over active after line L7, so $G$ also meets a renamed copy of itself. $C$ subsumes $D$ when $|C| \le |D|$ and $C\rho \subseteq D$ for some $\rho$.

## Example

Take the three clauses

$$0: f(x) = g(x), \quad 1: P(f(a)), \quad 2: \neg P(g(a)).$$

Clauses 1 and 2 do not resolve, because $f(a)$ and $g(a)$ do not unify. Line L1 adds $3: x = x$, $4: f(x) = f(x)$ and $5: g(x) = g(x)$. The run:

| pick | given clause | rule at L3 | what happens |
|---|---|---|---|
| 1 | 1: $P(f(a))$ | lightest | no equation, no complementary literal in active |
| 2 | 2: $\neg P(g(a))$ | lightest | does not resolve with clause 1 |
| 3 | 3: $x = x$ | lightest | no non-variable subterm to paramodulate into |
| 4 | 0: $f(x) = g(x)$ | lightest | into 1 at $f(a)$ with $x \mapsto a$: new 6: $P(g(a))$; into 2 right to left: new 7: $\neg P(f(a))$; into itself: copies of 4 and 5, not stored again |
| 5 | 4: $f(x) = f(x)$ | oldest | from 0 into 4: new 8: $g(x) = f(x)$ |
| 6 | 6: $P(g(a))$ | lightest | resolves with 2: new 9: $\square$ |

Pick 7 takes $\square$, and line L4 returns UNSAT. The refutation is the two steps 6 and 9. The tests check each step of each refutation: the mgu, the position, and the result.

## Correctness

**Soundness.** In an interpretation where $=$ is the identity, let $C \vee l = r$ and $D$ be true, and let $\theta$ assign values to the variables of $(C \vee D[r])\sigma$. If $C\sigma$ is true under $\theta$, so is the paramodulant. Otherwise $l\sigma$ and $r\sigma$ have the same value under $\theta$. As $u\sigma = l\sigma$, the literal of $D\sigma$ that holds $u\sigma$ has the same truth value as the same literal with $r\sigma$ in its place, so $D\sigma$ and $D[r]\sigma$ have the same value, and $D\sigma$ is true. So UNSAT is always right.

**Completeness.** Robinson and Wos proved: if $S$ is E-unsatisfiable and $S$ holds $x = x$ and the functional reflexivity axioms, then $\square$ can be derived from $S$ by binary resolution, factoring and paramodulation. Line L1 adds these clauses, line L10 forms every paramodulant, and the fair choice at line L3 makes sure that every derivation is reached, so with no limit and without the deletions at lines L5 and L6 the loop returns UNSAT. The proof file gives the outline of the argument and the references. This page does not prove that the deletions at lines L5 and L6 keep completeness. The loop never deletes the clauses of line L1, and it deletes a derived clause only when another derived or input clause subsumes it. The tests compare the answer with a [congruence closure](/congruence-closure/) oracle on 500 random ground sets, and every unsatisfiable set gives UNSAT.

## Complexity

First-order E-unsatisfiability is undecidable, so there is no bound on the run. The loop does not even stop on ground input: the functional reflexivity axioms have variables, and from $a = f(a)$ and $P(a)$ paramodulation makes $P(f(a)), P(f(f(a))), \ldots$ without end.

So the cost is stated for a run that stores $N$ clauses, each with at most $k$ literals and at most $w$ symbols. A pick compares $G$ with at most $N$ active clauses in each direction at lines L5 and L6. A subsumption test by backtracking tries at most $k^k$ maps of literals, at $O(w)$ each. At lines L9 and L10, a pair of clauses has at most $k^2$ pairs of literals and at most $4 k w$ choices of equation, direction and position. Each needs a unification and a new clause, $O(w^2)$ with a simple unifier. So one pick costs $O(N k w (k^k + w^2))$, and at most $N$ picks cost $O(N^2 k w (k^k + w^2))$. The store takes $O(N w)$ space. In practice $N$ grows very fast, because every equation can be used at every subterm in both directions.

## Properties

- **Sound.** Every UNSAT answer comes with a refutation in which each step can be checked.
- **Refutation complete for equality.** With resolution, factoring, $x = x$ and functional reflexivity (Robinson and Wos 1969).
- **No equality axioms.** Symmetry, transitivity and substitution are not needed as clauses. Only $x = x$ is.
- **Not into variables.** Line L10 never replaces a variable. The functional reflexivity axioms do the work that such steps would do.
- **Unrestricted.** Both directions of every equation, at every position of every literal. This is the reason for the large search space, and the reason for the ordered form, superposition.

## Variants and improvements

- **Superposition.** Use an ordering on terms: rewrite only with the larger side of an equation, only into the larger side of a maximal literal, and add equality factoring. This is complete and far smaller. See [superposition](/superposition/).
- **Demodulation.** When a unit equation $l = r$ has $l\sigma \succ r\sigma$ in a reduction ordering and $l\sigma$ occurs in a clause, replace the clause by its rewritten form and delete the old one. This is a simplification, not an inference. See [demodulation](/demodulation/).
- **No functional reflexivity.** Brand (1975), with his modification method, and Peterson (1983) showed that the functional reflexivity axioms are not needed.
- **Unit equations only.** For a set of unit equations and one negated goal, unfailing [Knuth-Bendix completion](/knuth-bendix-completion/) is an ordered form of paramodulation that also decides some [word problems](/word-problem/).
- **Ground input.** For ground equations and ground disequations, [congruence closure](/congruence-closure/) decides E-satisfiability in $O(n \log n)$ time, much faster than any paramodulation loop.

## When to use it

Use paramodulation to learn the idea, to check small proofs by hand, or as a reference to test a faster prover against. For real problems with equality, use superposition with demodulation, which keeps completeness and makes far fewer clauses. For ground equalities, use congruence closure.

## Pitfalls

- **No reflexivity axiom.** If line L1 does not add $x = x$, the set $\{a \ne a\}$ saturates without $\square$, because no rule can remove a negative equation. Line L1 must add $x = x$, and then $a \ne a$ resolves with it to give $\square$.
- **No factoring.** If line L8 is left out, $\{P(x) \vee P(y),\ \neg P(u) \vee \neg P(v)\}$ saturates without $\square$, as for plain resolution. Keep line L8.
- **Shared variables.** If line L10 does not rename the second clause apart, $f(x) = x$ does not paramodulate into $P(f(g(x)))$ at $f(g(x))$, because $x$ and $g(x)$ do not unify. Rename apart before unification.
- **Paramodulation into variables.** If line L10 also replaces variables, every equation applies at every variable of every clause, and the search space explodes. Skip variable positions, as line L10 does.
- **Weight only.** If line L3 always takes the lightest clause, a stream of light clauses can postpone a needed heavy clause forever. Take the oldest clause at every $k$-th pick.

## Implementations

## History

George Robinson and Lawrence Wos, at Argonne National Laboratory, published paramodulation in Machine Intelligence 4 (1969). Their completeness proof needed the functional reflexivity axioms, and whether they were needed was an open question until Daniel Brand (1975) and Gerald Peterson (1983) showed that they are not. In the 1980s and 1990s Hsiang, Rusinowitch, Bachmair and Ganzinger restricted paramodulation by term orderings, which led to [superposition](/superposition/), the basis of modern saturation provers.

## References
