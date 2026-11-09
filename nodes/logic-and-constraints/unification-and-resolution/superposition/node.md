---
tag: 8J4M9K
kind: algorithm
slug: superposition
name: Superposition
aliases:
- superposition calculus
- ordered paramodulation
area: logic-and-constraints/unification-and-resolution
level: research
summary: Paramodulation restricted by a reduction ordering, with equality resolution, equality factoring and deletion of redundant clauses. Refutation complete for equality (Bachmair and Ganzinger 1990).
solves: [first-order-theorem-proving]
model: word-ram
complexity:
  vars: {N: the number of clauses stored when the run stops, k: the largest number of literals in a clause, w: the largest clause size in symbols, D: the number of demodulation steps}
  time: {worst: O(N^2 k w (k^k + w^2) + D N w^2)}
  space: {extra: O(N w)}
properties: {deterministic: true, exact: false, online: false, recursive: false, in_place: false}
history:
  year: 1990
  people: [Leo Bachmair, Harald Ganzinger]
  note: Bachmair and Ganzinger proved that ordered paramodulation with equality factoring is refutation complete with a general notion of redundancy, by building a convergent rewrite system as a model.
prereqs: [paramodulation, ordered-resolution, knuth-bendix-ordering, term-rewriting-system]
see_also: [paramodulation, demodulation, ordered-resolution, knuth-bendix-completion, unfailing-completion, well-founded-reduction-ordering, critical-pair, congruence-closure]
sources:
  - paper: "Leo Bachmair and Harald Ganzinger, On restrictions of ordered paramodulation with simplification, in 10th International Conference on Automated Deduction (CADE-10), Lecture Notes in Computer Science 449, Springer, 1990, 427-441"
    locator: the superposition calculus with equality factoring and its completeness with simplification
  - paper: doi:10.1093/logcom/4.3.217
    title: Leo Bachmair and Harald Ganzinger, Rewrite-based equational theorem proving with selection and simplification, Journal of Logic and Computation 4(3), 1994
    locator: the full calculus with selection, the model construction and redundancy
  - book: isbn:9780444508133
    title: Alan Robinson and Andrei Voronkov (eds.), Handbook of Automated Reasoning, Elsevier and MIT Press, 2001
    locator: Chapter 7, Robert Nieuwenhuis and Albert Rubio, Paramodulation-based theorem proving (the superposition rules, the model generation and the completeness proof)
  - paper: "Jieh Hsiang and Michael Rusinowitch, Proving refutational completeness of theorem-proving strategies: the transfinite semantic tree method, Journal of the ACM 38(3), 1991"
    locator: completeness of ordered paramodulation by transfinite semantic trees
---

Superposition is the inference system that most first-order provers use for equality. It is [paramodulation](/paramodulation/) restricted by an ordering on terms: an equation is used only from its larger side to its smaller side, only at a maximal literal, and only into the larger side of a maximal literal. Two more rules complete it. **Equality resolution** removes a disequation $s \ne t$ when $s$ and $t$ unify. **Equality factoring** handles two positive equations with the same larger side. Leo Bachmair and Harald Ganzinger proved in 1990 that this calculus is refutation complete, also when redundant clauses are deleted. Their notion of redundancy covers tautology deletion, subsumption and [demodulation](/demodulation/), so a prover can simplify clauses all the time and stay complete. Without equality the rules reduce to [ordered resolution](/ordered-resolution/), and for unit equations they reduce to [unfailing completion](/unfailing-completion/).

## In plain words

An equation can be used in two directions, and plain paramodulation tries both, everywhere. That makes a flood of new clauses.

Superposition first fixes a way to say which of two terms is "bigger". Then every equation is a rule that only makes terms smaller: replace the big side by the small side. Each clause may only be used through its biggest part. So most steps that paramodulation makes are never made.

At the same time, superposition keeps clauses simple. When a clause can be made smaller with a known rule, the old clause is thrown away. The surprise is that all of this keeps every proof: if the clauses clash, the empty clause still appears.

## The problem

The input is a finite set $S$ of first-order clauses with equality. We write every literal as an equation $s = t$ or a disequation $s \ne t$, and read $s = t$ and $t = s$ as the same literal. A predicate atom $P(\ldots)$ can be coded as $P(\ldots) = \mathit{true}$. The question is whether $S$ is E-unsatisfiable, that is, false in every interpretation in which $=$ is the identity. The loop answers UNSAT with a refutation, SATURATED, or UNKNOWN at the clause limit.

**The ordering.** Fix a reduction ordering $\succ$ on terms that is total on ground terms: well-founded, stable under substitution ($s \succ t \Rightarrow s\sigma \succ t\sigma$), and compatible with contexts ($s \succ t \Rightarrow u[s] \succ u[t]$). The code uses the [Knuth-Bendix ordering](/knuth-bendix-ordering/) with every weight 1 and a total precedence. A literal $s = t$ is compared as the multiset $\{s, t\}$ and $s \ne t$ as $\{s, s, t, t\}$, by the [multiset extension](/multiset-ordering/) of $\succ$. All conditions below are checked on the instances under the most general unifier $\sigma$.

- **Superposition.** From $C \vee l = r$ and $D \vee L[u]$, where $u$ is not a variable and $\sigma$ is an mgu of $l$ and $u$, derive $(C \vee D \vee L[r])\sigma$, when $r\sigma \not\succeq l\sigma$, the literal $l\sigma = r\sigma$ is strictly maximal in its clause, $L\sigma$ is strictly maximal in its clause if it is positive and maximal if it is negative, and $u$ lies in a side $s$ of $L$ whose other side $t$ has $t\sigma \not\succeq s\sigma$.
- **Equality resolution.** From $C \vee s \ne t$, with $\sigma$ an mgu of $s$ and $t$, derive $C\sigma$, when $(s \ne t)\sigma$ is maximal.
- **Equality factoring.** From $C \vee s = t \vee s' = t'$, with $\sigma$ an mgu of $s$ and $s'$, derive $(C \vee t \ne t' \vee s' = t')\sigma$, when $t\sigma \not\succeq s\sigma$ and $(s = t)\sigma$ is maximal.

**Demodulation.** If a unit equation $l = r$ is active, $u = l\theta$ occurs in a literal $L$ of the given clause, $l\theta \succ r\theta$, and $L \succ (l = r)\theta$, replace $u$ by $r\theta$. The rewritten clause and the unit imply the old clause, and both are smaller, so the old clause is redundant and is deleted.

## The algorithm

The loop is a given-clause loop. Line L4 simplifies the given clause before it is used.

```pseudo id=main
SUPERPOSITION(S, ≻, limit, k)
L1  store the clauses of S; active ← ∅
L2  while some stored clause was not taken
L3      G ← the lightest untaken clause, or the oldest one at every k-th pick
L4      rewrite G with the active unit equations to normal form; if G changed, store it, or skip it if it was stored before
L5      if G = □ then return UNSAT
L6      if G is a tautology or a clause of active subsumes G then continue
L7      remove from active every clause that G subsumes
L8      add G to active
L9      new ← the equality resolvents and the equality factors of G
L10     for each clause A of active: add the superpositions from G into A and from A into G to new
L11     store each clause of new that was not stored before
L12     if more than limit clauses are stored then return UNKNOWN
L13 return SATURATED
```

A tautology at line L6 is a clause with a literal $t = t$, or with a literal and its negation. Subsumption at lines L6 and L7 is multiset subsumption: $C\rho$ is part of $D$, distinct literals go to distinct literals, and an equation matches in either direction. Line L10 runs after line L8, so $G$ also meets a renamed copy of itself.

## Example

Take the precedence $f \succ a \succ b$ and the three clauses

$$0: f(f(x)) = x, \quad 1: f(a) = b, \quad 2: f(b) \ne a.$$

In the ordering $f(f(x)) \succ x$, $f(a) \succ b$ and $f(b) \succ a$, so each equation is a rule from left to right. The run:

| pick | given clause | rule at L3 | what happens |
|---|---|---|---|
| 1 | 1: $f(a) = b$ | lightest | into itself at $f(a)$: new 3: $b = b$ |
| 2 | 2: $f(b) \ne a$ | lightest | $f(a)$ does not unify with $f(b)$, so nothing |
| 3 | 3: $b = b$ | lightest | a tautology, deleted at line L6 |
| 4 | 0: $f(f(x)) = x$ | lightest | 1 into 0 at $f(x)$ with $x \mapsto a$: $f(f(a)) = a$ becomes new 4: $f(b) = a$; into itself: new 5: $x = x$ and 6: $f(x) = f(x)$ |
| 5 | 4: $f(b) = a$ | oldest | 4 into 2 at $f(b)$: new 7: $a \ne a$; into itself: new 8: $a = a$ |
| 6 | 5: $x = x$ | lightest | a tautology, deleted |
| 7 | 7: $a \ne a$ | lightest | equality resolution: new 9: $\square$ |

Pick 8 takes $\square$, and line L5 returns UNSAT. The refutation is steps 4, 7 and 9. Paramodulation would also rewrite $b$ into $f(a)$ everywhere, and $x$ into $f(f(x))$ at every term. The ordering forbids both. Without clause 2, the run returns SATURATED. The tests check each refutation step by step, including the order conditions and the mgu.

## Correctness

Each rule is a paramodulation step, an instance of resolution with $x = x$, or a sound consequence, so UNSAT is always right. The completeness proof of Bachmair and Ganzinger builds a model from a saturated set.

1. **The ground model.** Go through the ground instances of the clauses in increasing order. A clause $C \vee s = t$ that is false so far, in which $s = t$ is strictly maximal, $s \succ t$, $s$ cannot be rewritten by the rules so far, and $C$ stays false after adding the rule, **produces** the rule $s \to t$. The produced rules form a ground rewrite system $R$ that terminates, since each rule goes down in $\succ$, and is confluent, since no left side can be rewritten by another rule. Its equality, joinability in $R$, is a congruence, so it defines an E-interpretation.
2. **The smallest counterexample.** If some ground instance were false in this interpretation, the smallest false one gives an inference: superposition if its maximal term can be rewritten by $R$, equality resolution if its maximal literal is a negative $s \ne s$, equality factoring if it fails to produce only because of a second equation. The conclusion is smaller and false. In a saturated set it is redundant, that is, it follows from smaller clauses, which are true, a contradiction.
3. **Lifting and fairness.** The ground inferences lift because $\succ$ is stable under substitution and $u$ is never a variable position: a rewrite below a variable is not needed, because the instance of the variable can be reduced first. Deletions remove only redundant clauses, and fair choice at line L3 gives a saturated limit.

Soundness and ground termination are proved in full in the proof file. For termination, every side of a derived literal has at most as many symbols as the largest side in the input, and there are only finitely many ground terms of a given size. The completeness part of the proof file is an outline with references.

## Complexity

First-order E-unsatisfiability is undecidable, so there is no bound on the run. For example, with $f \succ g$, the overlaps of $f(g(f(x))) = f(g(x))$ with itself give longer and longer equations, such as $f(g(f(g(x)))) = f(g(g(f(x))))$, and the run with the goal $a \ne b$ reaches every clause limit that we tried, up to 1000.

For a run that stores $N$ clauses with at most $k$ literals and $w$ symbols each, a subsumption test by backtracking costs $O(k^k w)$. A pair of clauses has at most $4 k w$ superposition places in each direction, each with a unification and a new clause in $O(w^2)$ time, and the order tests are $O(w)$ per pair of terms with KBO. So the inferences and deletions cost $O(N^2 k w (k^k + w^2))$, as for paramodulation. Each of the $D$ demodulation steps scans at most $w$ positions against at most $N$ units with an $O(w)$ match, which adds $O(D N w^2)$. The store takes $O(N w)$ space. On ground input the loop stops, but the bound on $N$ is exponential in the size of the input terms.

## Properties

- **Sound.** Every UNSAT answer comes with a refutation in which each step can be checked.
- **Refutation complete.** For a reduction ordering that is total on ground terms, with deletion of redundant clauses (Bachmair and Ganzinger 1990, 1994).
- **Saturation means satisfiable.** A saturated set without $\square$ has a model, the rewrite system $R$.
- **Terminates on ground input.** With the KBO of the code, no derived side is larger than the largest input side, so the set of possible clauses is finite.
- **No functional reflexivity, no rewriting into variables.** Both are needed by neither the calculus nor the proof.
- **Simplification is safe.** Demodulation, subsumption and tautology deletion keep completeness.

## Variants and improvements

- **Selection.** Bachmair and Ganzinger (1994) allow a selection function on negative literals, as in [ordered resolution](/ordered-resolution/). All provers below use it.
- **Unit equations.** With only unit equations and one ground goal, superposition is [unfailing completion](/unfailing-completion/), the equational form of [Knuth-Bendix completion](/knuth-bendix-completion/); the superposition inferences between units compute [critical pairs](/critical-pair/).
- **Basic superposition.** Nieuwenhuis and Rubio, and Bachmair, Ganzinger, Lynch and Snyder, forbid inferences into terms that come from a unifier. This prunes more, with some cost in simplification.
- **Indexing.** Real provers find unifiable and matching subterms with [discrimination trees](/discrimination-tree/), [substitution trees](/substitution-tree/) or similar indexes, instead of the pairwise scan of line L10.
- **Theories.** Superposition modulo associativity and commutativity, and its combination with arithmetic, extend the same proof method.

## When to use it

Use superposition for first-order problems with equality: algebra, verification conditions, and the equality part of large first-order problem libraries. The provers E, SPASS and Vampire are built on it. For ground equalities alone, [congruence closure](/congruence-closure/) is much faster, and for ground problems with theories, an SMT solver is the better choice. For pure unit equations, [Knuth-Bendix completion](/knuth-bendix-completion/) may give a decision procedure.

## Pitfalls

- **No equality resolution.** If line L9 forms only equality factors, $\{f(x) = a,\ f(b) \ne a\}$ saturates: superposition gives $a \ne a$, and nothing removes it. Line L9 must form equality resolvents too, and $a \ne a$ gives $\square$.
- **Rewriting upward.** If line L4 rewrites with $l\theta \to r\theta$ when $l\theta \not\succ r\theta$, rewriting may not stop: with $f(x) = f(f(x))$ used from left to right, $f(a)$ becomes $f(f(a))$, then $f(f(f(a)))$, and so on. Rewrite only when $l\theta \succ r\theta$, as line L4 does.
- **Demodulation without the redundancy test.** Line L4 also needs $L \succ (l = r)\theta$. Without it, the deleted clause need not follow from smaller clauses, and the completeness proof does not apply. Keep the test.
- **Shared variables.** If line L10 does not rename one clause apart, $f(x) = x$ does not superpose into $h(f(g(x))) = c$, because $x$ and $g(x)$ do not unify. Rename apart first.
- **Weight only.** If line L3 always takes the lightest clause, a stream of light clauses can postpone a needed heavy clause forever. Take the oldest clause at every $k$-th pick.

## Implementations

## History

Ordered forms of paramodulation were studied in the 1980s, for example by Hsiang and Rusinowitch, whose transfinite semantic tree method proved completeness of ordered paramodulation (published 1991). Leo Bachmair and Harald Ganzinger presented the superposition calculus with equality factoring at CADE-10 in 1990, and its full form with selection and simplification in the Journal of Logic and Computation in 1994. Their model construction and their notion of redundancy became the standard way to prove completeness of saturation calculi. The calculus is the core of E (Stephan Schulz), SPASS (Christoph Weidenbach and others) and Vampire (Andrei Voronkov and others).

## References
