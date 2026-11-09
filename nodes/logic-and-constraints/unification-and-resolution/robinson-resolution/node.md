---
tag: ZY28KR
kind: algorithm
slug: robinson-resolution
name: Robinson's resolution principle
aliases:
- resolution principle
- resolution refutation
- given-clause resolution
- first-order resolution
area: logic-and-constraints/unification-and-resolution
level: core
summary: Refute first-order clauses by adding factors and binary resolvents, built with most general unifiers, until the empty clause appears. Sound and refutation complete (Robinson 1965).
solves: [first-order-theorem-proving]
model: word-ram
complexity:
  vars: {n: the number of distinct atoms of a ground input}
  time: {worst: O(n^3 9^n)}
  space: {extra: O(n 4^n)}
properties: {deterministic: true, exact: true, online: false, recursive: false, in_place: false}
history:
  year: 1965
  people: [John Alan Robinson]
  note: Robinson joined unification and resolution into one rule, so that a prover no longer had to guess ground instances of the clauses.
prereqs: [binary-resolution, factoring, most-general-unifier, clausal-normal-form]
see_also: [robinson-completeness-theorem, lifting-lemma, subsumption, set-of-support, ordered-resolution, superposition, davis-putnam-elimination, sld-resolution]
sources:
  - paper: doi:10.1145/321250.321253
    title: John Alan Robinson, A machine-oriented logic based on the resolution principle, Journal of the ACM 12(1), 1965
    locator: the resolution principle, the unification algorithm, and the completeness theorem, proved from Herbrand's theorem by lifting
  - book: isbn:9780121703509
    title: Chin-Liang Chang and Richard Char-Tung Lee, Symbolic Logic and Mechanical Theorem Proving, Academic Press, 1973
    locator: Chapter 5, The resolution principle (factors, resolvents, and the completeness proof)
  - book: isbn:9780444508133
    title: Alan Robinson and Andrei Voronkov (eds.), Handbook of Automated Reasoning, Elsevier and MIT Press, 2001
    locator: Chapter 2, Leo Bachmair and Harald Ganzinger, Resolution theorem proving (saturation, redundancy and fair derivations)
  - paper: "William McCune, Otter 3.0 reference manual and guide, Technical Report ANL-94/6, Argonne National Laboratory, 1994"
    locator: the main loop with the lists usable and sos, the given clause, and forward and back subsumption
---

Robinson's resolution principle is a procedure that shows a set $S$ of first-order [clauses](/clause/) to be unsatisfiable. It adds new clauses with two rules, [binary resolution](/binary-resolution/) and [factoring](/factoring/), which use [most general unifiers](/most-general-unifier/) to match literals with variables. When the empty clause $\square$ appears, $S$ has no model, and the derivation is a [refutation](/refutation/). John Alan Robinson published the method in 1965, and it is still the base of most first-order provers.

## In plain words

You want to show that a set of rules cannot all hold at once. Each rule is an "or" of facts, and a fact may hold placeholders that stand for any object.

Take two rules where a fact in one is the denial of a fact in the other, after you fill in the placeholders in the most general way that makes the two facts agree. One of the two facts must fail, so the rest of the two rules gives a new rule. You may also merge two facts of one rule when they can be made equal.

Keep a pile of rules to look at. Take the smallest rule, and every few turns the oldest one. Throw it away if a rule you keep says more. Otherwise keep it and put its new rules on the pile. If the empty rule appears, the set is contradictory.

## The problem

The input is a finite set $S$ of clauses. A clause is a finite set of literals, read as their disjunction, with its variables read as universally quantified. The question is whether $S$ is unsatisfiable. Every first-order formula can be brought to this form with the same satisfiability by [Skolemization](/skolemization/) and a [clausal normal form](/clausal-normal-form/), so this is the core of [first-order theorem proving](/first-order-theorem-proving/). The problem is only semi-decidable, so the procedure has three answers: UNSAT, SATURATED (the set is satisfiable) and UNKNOWN (a limit on the number of clauses was reached).

The two rules are these. Let $C \vee L$ and $D \vee \neg L'$ be clauses with no common variable ([standardization apart](/standardization-apart/)), and let $\sigma$ be a most general unifier of the atoms $L$ and $L'$. The **binary resolvent** is $(C \vee D)\sigma$. If two literals $L_1, L_2$ of a clause $C$ have the same sign and a most general unifier $\sigma$, then $C\sigma$ is a **factor** of $C$. A clause $C$ **subsumes** a clause $D$ when $|C| \le |D|$ and $C\theta \subseteq D$ for some substitution $\theta$ ([clause subsumption](/subsumption/)).

## The algorithm

The **given-clause loop** keeps two sets. The clauses of *active* have been used for all inferences with each other. The clauses of *passive* wait. Each pass takes one clause $G$ out of passive and makes all inferences between $G$ and active.

```pseudo id=main
RESOLUTION-PROVER(S, limit, k)
L1  passive ← S, active ← ∅
L2  while passive ≠ ∅
L3      G ← the lightest clause of passive, but the oldest one at every k-th pick; remove G from passive
L4      if G = □ then return UNSAT
L5      if G is a tautology or a clause of active subsumes G then continue
L6      remove from active every clause that G subsumes
L7      active ← active ∪ {G}
L8      N ← the factors of G and the binary resolvents of G with each clause of active, G included
L9      passive ← passive ∪ (N minus the clauses that were stored before)
L10     if more than limit clauses were stored then return UNKNOWN
L11 return SATURATED
```

The weight of a clause is the number of symbols in it. Line L3 prefers light clauses, because they are short and general and so more likely to lead to $\square$. The pick by age at every $k$-th turn makes the loop **fair**: every clause that enters passive is picked after a finite number of turns. Lines L5 and L6 are **forward** and **backward subsumption**. A tautology is a clause with a literal and its negation, and it is true in every model. Line L8 renames one parent of each resolvent apart, so the two parents share no variable. Line L9 compares clauses after renaming their variables in a fixed order, so a variant of a stored clause is not stored again.

## Example

Take the transitivity clause and three facts:

$$0: \neg L(x, y) \vee \neg L(y, z) \vee L(x, z), \quad 1: L(a, b), \quad 2: L(b, c), \quad 3: \neg L(a, c).$$

The weights are 9, 3, 3 and 3, and the run uses $k = 5$. Each row is one pass of the loop. The new clauses get the next free numbers.

| pick | G | why picked | what happens | new clauses |
|---|---|---|---|---|
| 1 | 1: $L(a,b)$ | lightest | no inference with active | none |
| 2 | 2: $L(b,c)$ | lightest | no inference | none |
| 3 | 3: $\neg L(a,c)$ | lightest | no inference: the facts are ground and different | none |
| 4 | 0 | lightest | 1 factor and 7 resolvents | 4 to 11 |
| 5 | 4: $\neg L(x,x) \vee L(x,x)$ | oldest (5th pick) | tautology, deleted at L5 | none |
| 6 | 5: $\neg L(b,x) \vee L(a,x)$ | lightest (weight 6) | 2 resolvents with units, 2 with clause 0 | 12 to 15 |
| 7 | 12: $L(a,c)$ | lightest | resolves with 3 | 16: $\square$, and others |
| 8 | 16: $\square$ | weight 0 | return UNSAT | |

Clause 4 is the factor of clause 0 by $\{y \mapsto x, z \mapsto x\}$. Clause 5 is the resolvent of 0 and 1 on $\neg L(x, y)$ and $L(a, b)$ with mgu $\{x \mapsto a, y \mapsto b\}$. The other new clauses at pick 4 are $\neg L(x,a) \vee L(x,b)$, $\neg L(c,x) \vee L(b,x)$, $\neg L(x,b) \vee L(x,c)$, $\neg L(x,c) \vee \neg L(a,x)$ and two resolvents of clause 0 with itself, with 4 literals each. Clause 12 is the resolvent of 5 and 2 with mgu $\{x \mapsto c\}$, and 16 is the resolvent of 12 and 3. The refutation uses the clauses 0, 1, 2, 3, 5, 12 and 16.

## Correctness

The procedure is **sound** for both of its definite answers. Each factor and each resolvent is a logical consequence of its parents, so every stored clause follows from $S$, and UNSAT is right when $\square$ is stored. For SATURATED, the loop keeps this invariant: every clause that was ever taken from passive is a tautology or is subsumed by a clause of active. When passive is empty, every factor and every resolvent of clauses of active was stored, so it is a tautology or subsumed by a clause of active. A set with this property that does not contain $\square$ is satisfiable. The proof of this fact goes down to ground instances, merges literals with factors, lifts each ground resolution step with the [lifting lemma](/lifting-lemma/), and ends with [Herbrand's theorem](/herbrand-theorem/). The full proof is in the proof file.

The procedure is also **refutation complete**: if $S$ is unsatisfiable and there is no limit, the loop returns UNSAT. If the loop ran forever, fairness would put every factor and resolvent of the clauses that stay in active into passive, and the same argument would make $S$ satisfiable. Deleting a subsumed clause is safe because only finitely many clauses, up to renaming, subsume a given clause, so every chain of deletions ends in a clause that stays. The proof file has both arguments in full. This is the loop form of the [completeness theorem](/robinson-completeness-theorem/). Bachmair and Ganzinger prove the same for fair derivations with any redundancy criterion, in Chapter 2 of the Handbook of Automated Reasoning.

## Complexity

For first-order input there is no bound: first-order unsatisfiability is undecidable ([Church's theorem](/church-theorem/)), so the loop can run forever on a satisfiable set. Take $\{P(a),\ \neg P(x) \vee P(f(x))\}$: it gives $P(f(a)), P(f(f(a))), \ldots$ without end.

For a ground input with $n$ distinct atoms, each atom is absent, positive, negative or both in a clause. So there are at most $4^n$ clauses, and at most $3^n$ of them are not tautologies. Line L9 stores each clause once, so there are at most $4^n$ picks. A pick of a tautology stops at line L5 after $O(n)$ work. At most $3^n$ picks go further. In one such pick, lines L5 and L6 compare $G$ with at most $3^n$ active clauses at $O(n^2)$ each. Line L8 makes at most $n$ resolvents for each active clause, each built and sorted in $O(n \log n)$ time and looked up by hashing in $O(n)$ expected time. One pick costs $O(n^2 \log n \cdot 3^n)$, and all picks cost $O(n^2 \log n \cdot 9^n + n\, 4^n) \subseteq O(n^3\, 9^n)$. The at most $4^n$ stored clauses and the two heaps take $O(n\, 4^n)$ space. The proof of these counts is in the proof file.

The exponential size is not only an artifact of the bound. A ground run that returns UNSAT gives a resolution refutation, and [Haken's lower bound](/haken-resolution-lower-bound/) shows that the pigeonhole formulas need exponentially many clauses in every resolution refutation.

## Properties

- **Sound.** The answer UNSAT comes with a refutation that a checker can verify step by step.
- **Refutation complete.** With no limit and a fair choice at line L3, an unsatisfiable input always gives UNSAT.
- **A semi-decision procedure.** On satisfiable input the loop may stop with SATURATED, or it may run until the limit.
- **Free of guessing.** Unification computes the needed instances, so the procedure never enumerates ground terms, unlike the procedures of Gilmore and of Davis and Putnam.
- **Deterministic.** The choices at L3 depend only on weights and ages, so the run is the same each time.

## Variants and improvements

- **Restricted resolution.** [Set of support](/set-of-support/), [hyperresolution](/hyperresolution/), [ordered resolution](/ordered-resolution/) and [linear resolution](/linear-resolution/) allow fewer inferences and stay complete. [Unit resolution](/unit-resolution/) and [input resolution](/input-resolution/) are complete only for Horn clauses.
- **Equality.** [Paramodulation](/paramodulation/) and [superposition](/superposition/) add rules that replace equals by equals, and [demodulation](/demodulation/) simplifies clauses with oriented equations.
- **The Otter loop and the DISCOUNT loop.** The pseudocode above simplifies only with active clauses, as in the DISCOUNT loop. The Otter loop also simplifies new clauses against passive at once. The choice changes memory use and speed, not completeness.
- **Indexing.** Real provers find unifiable and subsuming clauses with [term indexing](/term-indexing/), for example [discrimination trees](/discrimination-tree/) and [substitution trees](/substitution-tree/), instead of trying every active clause.
- **SLD resolution.** For Horn clauses, [SLD resolution](/sld-resolution/) is the linear input strategy that Prolog uses.

## When to use it

Use plain resolution with factoring to teach or to check small problems, and as the base that the restricted strategies refine. For problems with equality, use [superposition](/superposition/), as the provers Vampire, E and SPASS do. For propositional input, [CDCL](/cdcl/) solvers are much faster, because they search for a model instead of saturating. For Horn clauses with a goal, [SLD resolution](/sld-resolution/) is simpler.

## Pitfalls

- **No factoring.** If line L8 forms only resolvents, the set $\{P(x) \vee P(y),\ \neg P(u) \vee \neg P(v)\}$ saturates without $\square$, because every resolvent has two literals. Line L8 must add the factors, and then $P(x)$ and $\neg P(u)$ resolve to $\square$.
- **Shared variables.** If line L8 does not rename one parent apart, $P(x)$ and $\neg P(f(x))$ do not unify because of the [occurs check](/occurs-check/), and the refutation is lost. Rename one parent before unification.
- **Weight only.** If line L3 always takes the lightest clause, a stream of light clauses can postpone a needed heavy clause forever. Take the oldest clause at every $k$-th pick.
- **Subsumption without the size test.** In instance-only subsumption, $P(x) \vee P(y)$ subsumes its own factor $P(x)$. If lines L5 and L6 then delete the factor, the refutation of the first pitfall is lost. Keep $|C| \le |D|$ in the test.
- **Reading SATURATED as UNSAT or UNKNOWN as SAT.** Line L10 says only that the limit was reached. It says nothing about satisfiability.

## Implementations

## History

Herbrand's theorem of 1930 reduces first-order unsatisfiability to a propositional test on ground instances. Gilmore (1960) and Davis and Putnam (1960) built provers that generated ground instances and tested them. Prawitz (1960) proposed to delay the choice of instances and to compute them by solving equations between terms. Robinson (1965) made this idea one rule: resolution with a most general unifier, together with factoring, and he proved the rule sound and refutation complete. Wos, Robinson and Carson (1965) added the set-of-support strategy, and the provers built at Argonne National Laboratory, up to Otter and Prover9 by William McCune, used the given-clause loop. Bachmair and Ganzinger (1990, 1994) gave the general theory of saturation with redundancy, which explains why deleting tautologies and subsumed clauses keeps completeness.

## References
