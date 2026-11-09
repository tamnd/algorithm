---
tag: HD62FE
kind: algorithm
slug: ordered-resolution
name: Ordered resolution
aliases:
- ordered resolution with selection
- resolution with selection
area: logic-and-constraints/unification-and-resolution
level: research
summary: Resolution that resolves only maximal literals under a term ordering, or selected negative literals. Refutation complete with ordered factoring (Bachmair and Ganzinger).
solves: [first-order-theorem-proving]
model: word-ram
complexity:
  vars: {n: the number of distinct atoms of a ground input}
  time: {worst: O(n^3 9^n)}
  space: {extra: O(n 4^n)}
properties: {deterministic: true, exact: true, online: false, recursive: false, in_place: false}
history:
  year: 1994
  people: [Leo Bachmair, Harald Ganzinger]
  note: Bachmair and Ganzinger proved completeness of ordered inference rules with selection functions and with deletion of redundant clauses, by building a model from a saturated set of clauses.
prereqs: [binary-resolution, factoring, robinson-resolution, knuth-bendix-ordering]
see_also: [superposition, hyperresolution, robinson-completeness-theorem, lifting-lemma, subsumption, multiset-ordering, well-founded-reduction-ordering, set-of-support]
sources:
  - book: isbn:9780444508133
    title: Alan Robinson and Andrei Voronkov (eds.), Handbook of Automated Reasoning, Elsevier and MIT Press, 2001
    locator: Chapter 2, Leo Bachmair and Harald Ganzinger, Resolution theorem proving (ordered resolution with selection, the model construction, redundancy)
  - paper: doi:10.1093/logcom/4.3.217
    title: Leo Bachmair and Harald Ganzinger, Rewrite-based equational theorem proving with selection and simplification, Journal of Logic and Computation 4(3), 1994
    locator: the inference rules with selection; ordered resolution is the case without equality
  - paper: doi:10.1145/321250.321253
    title: John Alan Robinson, A machine-oriented logic based on the resolution principle, Journal of the ACM 12(1), 1965
    locator: binary resolution and factoring, which ordered resolution restricts
---

Ordered resolution is the restriction of [Robinson's resolution principle](/robinson-resolution/) in which a clause may be resolved only on its largest literal, under a fixed ordering of atoms, or on a negative literal that a **selection function** chooses. Factoring is restricted in the same way. Most pairs of clauses then have no inference at all, so the search space is much smaller, and some sets that make unrestricted resolution run forever now saturate. The calculus is still refutation complete when the ordering is well-founded, total on ground atoms and stable under substitution, and the selection function is arbitrary. Bachmair and Ganzinger proved this with a model construction that also shows that deleting tautologies and subsumed clauses is safe. Ordered resolution is the equality-free part of [superposition](/superposition/), the calculus of the main saturation provers.

## In plain words

Plain resolution combines any two rules that share a fact with opposite signs. That makes far too many new rules. Ordered resolution first puts all facts in a fixed rank order. A rule may take part in a step only through its highest-ranked fact. You may also mark one negative fact of a rule, and then the rule must use that one.

So each rule has one or two doors, not many. Most pairs of rules cannot combine at all, and the search shrinks.

You might expect to lose proofs this way. You do not. If the rules clash, the ranked steps still reach the empty rule. If they never reach it, the rules that are left show how to build a world in which all of them hold.

## The problem

The input is a finite set $S$ of first-order clauses. The question is whether $S$ is unsatisfiable. The loop answers UNSAT with a refutation, SATURATED when no new clause can be made, which shows that $S$ is satisfiable, or UNKNOWN when it reaches the clause limit.

The loop needs two parameters.

- An **atom ordering** $\succ$: a strict order on atoms that is well-founded, total on ground atoms and stable under substitution ($A \succ B$ implies $A\sigma \succ B\sigma$). The code uses the [Knuth-Bendix ordering](/knuth-bendix-ordering/) with every weight 1 and a total precedence, and treats a predicate symbol as a function symbol. Literals are compared by the [multiset extension](/multiset-ordering/) of $\succ$, with $A$ read as $\{A\}$ and $\neg A$ as $\{A, A\}$. So $\neg A \succ A$, and both are below every literal whose atom is above $A$.
- A **selection function** $\mathrm{sel}$, which maps a clause to one of its negative literals or to nothing.

A literal $L$ of $C$ is **maximal** in $C$ when no literal of $C$ is greater than $L$, and **strictly maximal** when no other literal of $C$ is greater than or equal to $L$. Let $\sigma$ be a most general unifier.

- **Ordered resolution.** From $C \vee A$ and $D \vee \neg B$, with $\sigma$ an mgu of $A$ and $B$, derive $(C \vee D)\sigma$, when nothing is selected in $C \vee A$ and $A\sigma$ is strictly maximal in $(C \vee A)\sigma$, and $\neg B$ is selected in $D \vee \neg B$, or nothing is selected there and $\neg B\sigma$ is maximal in $(D \vee \neg B)\sigma$.
- **Ordered factoring.** From $C \vee A \vee A'$, with $\sigma$ an mgu of $A$ and $A'$, derive $(C \vee A)\sigma$, when nothing is selected and $A\sigma$ is maximal in $(C \vee A \vee A')\sigma$.

The test is on the instance under $\sigma$, because two literals that cannot be compared may become comparable after unification.

## The algorithm

The loop is the given-clause loop of Robinson's resolution principle, with the ordered rules at lines L8 and L9.

```pseudo id=main
ORDERED-RESOLUTION(S, ≻, sel, limit, k)
L1  store the clauses of S; active ← ∅
L2  while some stored clause was not taken
L3      G ← the lightest untaken clause, or the oldest one at every k-th pick
L4      if G = □ then return UNSAT
L5      if G is a tautology or a clause of active subsumes G then continue
L6      remove from active every clause that G subsumes
L7      add G to active
L8      new ← the ordered factors of G
L9      for each clause A of active: add to new the ordered resolvents of G and A
L10     store each clause of new that was not stored before
L11     if more than limit clauses are stored then return UNKNOWN
L12 return SATURATED
```

Line L9 runs over active after line L7, so $G$ is also resolved with a renamed copy of itself. Lines L5 and L6 use multiset subsumption: $C$ subsumes $D$ when $C\rho \subseteq D$ for a substitution $\rho$ that maps distinct literals of $C$ to distinct literals of $D$. The weight of a clause is the number of symbol and variable occurrences in it.

## Example

Take $p \succ q$, no selection, and the four clauses

$$0: p \vee q, \quad 1: \neg p \vee q, \quad 2: p \vee \neg q, \quad 3: \neg p \vee \neg q.$$

The literal order is $\neg p \succ p \succ \neg q \succ q$. So $p$ is the only eligible literal of clauses 0 and 2, $\neg p$ of clauses 1 and 3. The run picks six clauses and makes only three new ones:

| pick | given clause | rule at L3 | what happens | active after the pick |
|---|---|---|---|---|
| 1 | 0: $p \vee q$ | lightest | no negative literal to meet | 0 |
| 2 | 1: $\neg p \vee q$ | lightest | resolves with 0 on $p$: new clause 4: $q$ | 0, 1 |
| 3 | 4: $q$ | lightest | subsumes 0 and 1, which leave active | 4 |
| 4 | 2: $p \vee \neg q$ | lightest | $\neg q$ is not maximal, so no step with $q$ | 4, 2 |
| 5 | 3: $\neg p \vee \neg q$ | oldest | resolves with 2 on $p$: new clause 5: $\neg q$ | 4, 2, 3 |
| 6 | 5: $\neg q$ | lightest | resolves with 4 on $q$: new clause 6: $\square$ | 4, 2, 3, 5 |

Pick 7 takes $\square$, and line L4 returns UNSAT. Plain resolution would also resolve clause 2 with $q$ at pick 4, which gives $p$, and clause 3 with $q$ at pick 5, which gives $\neg p$. Without clause 3, the run stops with SATURATED and active $\{q,\ p \vee \neg q\}$. This set has the model in which $p$ and $q$ are true, the model that the proof builds.

A first-order example: for $\{P(a),\ \neg P(x) \vee P(f(x))\}$ unrestricted resolution makes $P(f(a)), P(f(f(a))), \ldots$ forever. In the ordering $P(f(x)) \succ P(x)$, so $\neg P(x)$ is not maximal in the second clause, no inference applies, and the loop returns SATURATED at once. The tests check both runs.

## Correctness

Each ordered resolvent is a binary resolvent and each ordered factor is a factor, so UNSAT is always right. The proof of completeness has three steps.

1. **Ground model.** Take the ground instances of the clauses of a saturated set, as multisets of literals, in increasing multiset order. A ground clause that is false so far, has nothing selected and has a strictly maximal positive literal $A$ **produces** $A$, which is made true. If some ground instance were false at the end, the smallest false one would give an ordered inference whose conclusion is smaller and also false. Saturation and subsumption give a smaller false instance, a contradiction.
2. **Lifting.** The ground inference in step 1 lifts to an ordered inference on the clauses themselves, because the ordering is stable under substitution. If $L\tau$ is maximal in $C\tau$, then $L\sigma$ is maximal in $C\sigma$ for an mgu $\sigma$ with $\tau = \sigma\theta$. Ordered factoring handles two positive literals that become equal at the maximal place.
3. **Fairness.** Every stored clause is picked at some time, so the clauses that stay in active form a saturated set, as for Robinson's resolution principle.

The full proof is in the proof file. It needs multiset subsumption at line L5: the step "a smaller false instance" fails if two literals of the subsuming clause may go to one literal.

## Complexity

For first-order input there is no bound: first-order unsatisfiability is undecidable ([Church's theorem](/church-theorem/)), so the loop can run forever on a satisfiable set. With $\neg P(x)$ selected, the set $\{P(a),\ \neg P(x) \vee P(f(x))\}$ gives $P(f(a)), P(f(f(a))), \ldots$ without end.

For a ground input with $n$ distinct atoms, every stored clause is a set of literals over these atoms, so there are at most $4^n$ stored clauses and at most $4^n$ picks, and at most $3^n$ stored clauses are not tautologies. Rank the atoms once at the start, so that a comparison takes $O(1)$ time. A pick of a tautology stops at line L5 after $O(n)$ work. In each of the at most $3^n$ other picks, lines L5 and L6 compare $G$ with at most $3^n$ active clauses at $O(n^2)$ each, and line L9 tries at most $n$ pairs of literals with each active clause, each tested in $O(n)$ time and built in $O(n \log n)$ time. One pick costs $O(n^2 \log n \cdot 3^n)$, and the run costs $O(n^2 \log n \cdot 9^n + n\, 4^n) \subseteq O(n^3\, 9^n)$. The stored clauses and the two heaps take $O(n\, 4^n)$ space. These are the bounds of Robinson's resolution principle. The ordering does not improve the worst case, but in practice it removes most inferences.

## Properties

- **Sound.** Every UNSAT answer comes with a refutation in which each step can be checked.
- **Refutation complete.** If the ordering is well-founded, total on ground atoms and stable under substitution, then for every selection function an unsatisfiable set gives UNSAT when there is no limit.
- **Saturation means satisfiable.** SATURATED is a proof of satisfiability: the proof builds a model from the final active set.
- **Deletion is safe.** Tautology deletion and multiset subsumption keep completeness.
- **Terminates on ground input.** The loop stops after at most $4^n$ picks.
- **Decides some classes.** On some first-order classes, such as the example above, the ordering makes the set of derived clauses finite, so the loop answers SATURATED. Ordered resolution is the base of resolution decision procedures for such classes.

## Variants and improvements

- **Hyperresolution as a case.** If every clause with a negative literal has a negative literal selected, only positive clauses can be resolved on positive literals. This gives a form of [hyperresolution](/hyperresolution/) step by step.
- **Superposition.** With equality in the logic, ordered resolution and ordered factoring are joined by superposition and equality factoring. See [superposition](/superposition/).
- **Redundancy.** Bachmair and Ganzinger define a clause as redundant when it follows from smaller clauses. Subsumption and tautology deletion are special cases, and the same proof covers [demodulation](/demodulation/) in the equational case.
- **Choice of selection.** Saturation provers often select a negative literal of maximal weight, or select all negative literals when a clause has more than one. Each choice is complete, but they behave very differently in practice.

## When to use it

Use ordered resolution, inside a saturation prover, for first-order problems without equality, and use [superposition](/superposition/) when there is equality. Prefer it to unrestricted resolution almost always: it makes far fewer clauses and it keeps completeness. Use the SATURATED answer as evidence that a set is satisfiable. For goal-directed search with little memory, [linear resolution](/linear-resolution/) is an alternative.

## Pitfalls

- **No ordered factoring.** If line L8 is left out, the set $\{P(x) \vee P(y),\ \neg P(u) \vee \neg P(v)\}$ saturates without $\square$, because every resolvent has two literals. Keep line L8: the factor $P(x)$ resolves with $\neg P(u)$ and then $\neg P(v)$ to give $\square$.
- **Subsumption that merges literals.** If lines L5 and L6 use instance-only subsumption, $P(x) \vee P(y)$ subsumes its own factor $P(x)$, and the same set saturates without $\square$. Use multiset subsumption, as lines L5 and L6 do.
- **The test before the unifier.** If line L9 checks maximality in $C$ and not in $C\sigma$, it can still be complete, but it gives up most of the pruning, because many literals are incomparable before unification. Test eligibility on the instance under $\sigma$.
- **Weight only.** If line L3 always takes the lightest clause, a stream of light clauses can postpone a needed heavy clause forever. Take the oldest clause at every $k$-th pick.
- **An ordering that is not stable.** The completeness proof lifts ground inferences through $\tau = \sigma\theta$, and that needs $A \succ B \Rightarrow A\theta \succ B\theta$. An ordering by symbol count alone, without the variable condition of the Knuth-Bendix ordering, does not have this property: it puts $P(f(a))$ above $P(x)$, but $P(f(f(a)))$, the instance under $x \mapsto f(f(a))$, above $P(f(a))$. Use the Knuth-Bendix ordering as line L9 does, or another reduction ordering that is total on ground terms.

## Implementations

## History

Restrictions of resolution by orderings of literals were studied from the late 1960s. Leo Bachmair and Harald Ganzinger gave the form used today, with a selection function and with a notion of redundancy, in their superposition papers of 1990 and 1994 for equational logic, and they gave a full account for resolution in their chapter of the Handbook of Automated Reasoning (2001). Their proof builds a model from a saturated set, so a saturated set without the empty clause is not only a failure to find a proof, it is a description of a model. The calculus, with superposition for equality, is the core of the provers SPASS, E and Vampire.

## References
