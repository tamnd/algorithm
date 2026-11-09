---
tag: VDC291
kind: technique
slug: lazy-smt
name: Lazy SMT approach
aliases:
- offline lazy SMT
- lazy encoding
- lemmas on demand
- lazy approach
area: logic-and-constraints/smt
level: advanced
summary: Solve the Boolean abstraction with a SAT solver, check each model with a theory solver, and add a theory lemma that blocks it when it fails. Theory facts enter the search only when needed.
prereqs: [smt-problem, boolean-abstraction, sat]
see_also: [dpll-t, cdcl-t, eager-smt-encoding, theory-conflict-explanation, theory-propagation, incremental-sat, cegis, unsat-core]
sources:
  - book: isbn:9781643681603
    title: Clark Barrett, Roberto Sebastiani, Sanjit A. Seshia and Cesare Tinelli, Satisfiability Modulo Theories, Chapter 33 of the Handbook of Satisfiability, second edition, IOS Press, 2021
    locator: Section 33.1 (eager and lazy approaches), Section 33.4.1 (features of theory solvers), Section 33.4.2 (the offline and online schemas, Figure 33.3), Section 33.4.3 (early pruning, T-propagation, T-learning)
  - paper: doi:10.1007/3-540-45620-1_35
    title: Leonardo de Moura, Harald Rueß and Maria Sorea, Lazy theorem proving for bounded model checking over infinite domains, CADE 2002, LNCS 2392, pages 438 to 455
    locator: lemmas on demand, the offline refinement loop with small conflict sets
  - paper: doi:10.1007/3-540-45657-0_18
    title: Clark W. Barrett, David L. Dill and Aaron Stump, Checking satisfiability of first-order formulas by incremental translation to SAT, CAV 2002, LNCS 2404, pages 236 to 249
    locator: the CVC loop that adds theory conflict clauses to a SAT solver
  - paper: doi:10.1007/978-3-540-45069-6_34
    title: Cormac Flanagan, Rajeev Joshi, Xinming Ou and James B. Saxe, Theorem proving using lazy proof explication, CAV 2003, LNCS 2725, pages 355 to 367
    locator: Verifun, the names offline and online for the two schemas, and lemmas with new atoms
  - paper: doi:10.1007/3-540-45620-1_17
    title: Gilles Audemard, Piergiorgio Bertoli, Alessandro Cimatti, Artur Korniłowicz and Roberto Sebastiani, A SAT based approach for solving formulas over Boolean and linear mathematical propositions, CADE 2002, LNCS 2392, pages 195 to 210
    locator: MathSAT, an online lazy solver with early pruning
  - book: isbn:9783662504963
    title: Daniel Kroening and Ofer Strichman, Decision Procedures, An Algorithmic Point of View, second edition, Springer, 2016
    locator: Chapter 3, From Propositional to Quantifier-Free Theories (the Lazy-Basic and Lazy-CDCL algorithms)
  - paper: doi:10.3233/sat190034
    title: Roberto Sebastiani, Lazy satisfiability modulo theories, Journal on Satisfiability, Boolean Modeling and Computation 3, 2007, pages 141 to 224
    locator: a survey of the lazy approach and its techniques
---

The lazy approach decides an SMT formula with two separate solvers. A SAT solver works on the [Boolean abstraction](/boolean-abstraction/) of the formula and proposes truth values for its atoms. A theory solver checks whether the proposed theory literals can hold together. If they cannot, it returns a small set of them that is inconsistent, and the negation of this set, a *theory lemma*, is added to the abstraction so that the SAT solver never proposes the same mistake again. The theory enters the search only through these lemmas, and only when a model of the abstraction needs one. That is why it is called lazy. The opposite, the [eager approach](/eager-smt-encoding/), adds enough theory facts as clauses before the search, and then calls SAT once. This page is about the general method and its simplest form, the offline loop with a SAT solver used as a black box. Its refinement inside the SAT search is [DPLL(T)](/dpll-t/), and the loop of real solvers is [CDCL(T)](/cdcl-t/).

## In plain words

Two helpers solve a puzzle together. The first one is fast but knows only the rules of logic. The second one knows arithmetic, or arrays, or functions, but can only check a plain list of facts.

The first helper reads each fact as a switch, sets all switches so that the logic works, and hands the list of facts to the second helper. If the second helper says "these facts fit", the puzzle is solved. If not, it points at a few facts that clash, for example "x is less than 3" and "x is more than 5". The first helper writes down a new rule, "not both of these", and tries again.

Each new rule removes at least one wrong answer, and it is never removed. So the helpers stop after a finite number of rounds.

## When it applies

- The theory has a solver for conjunctions of literals that is fast, and that can return a small conflict set when the conjunction is inconsistent.
- The theory has no small encoding in propositional logic, or the encoding is much larger than the formula, as for linear arithmetic over the reals.
- The Boolean structure of the formula is rich, so a SAT solver is the right tool for the case splits.
- Many atoms are never in conflict with each other, so most of the theory facts that an eager encoding would add are not needed.

## The template

The holes are the SAT solver, the set of literals that the theory solver sees, and the conflict set.

```pseudo id=main
LAZY-SMT(φ)
L1  (F, B) ← the CNF of the Boolean abstraction of φ, and the map from variables to atoms
L2  loop
L3      ν ← a model of F from the SAT solver, or nil      ▷ hole: a new call, or an incremental call
L4      if ν = nil then return UNSAT
L5      μ ← B(ν), the theory literals that ν stands for     ▷ hole: all atoms, or only those that matter
L6      if μ is T-satisfiable then return SAT, a T-model of μ with ν on the plain variables
L7      η ← a T-unsatisfiable subset of μ                  ▷ hole: μ itself, or a small or minimal conflict
L8      add the clause ¬η, written over the variables of B, to F   ▷ the blocking clause, a theory lemma
```

This is the *offline* schema of the Handbook, Section 33.4.2. In the *online* schema the theory solver is called inside the SAT search on partial assignments, and the lemma drives the backjump of the SAT solver at once. This is [DPLL(T)](/dpll-t/).

**Correctness.** Let $a$ be the number of theory atoms of $\varphi$. Then the loop returns after at most $2^a + 1$ SAT calls, and its answer is correct.

*Proof.* Each lemma $\neg \eta$ of line L8 is $T$-valid, because $\eta$ is $T$-unsatisfiable. So adding it does not change the set of $T$-models of $F$ read as a theory formula, and by fact 1 of the [Boolean abstraction](/boolean-abstraction/) page, UNSAT at line L4 means that $\varphi$ has no $T$-model. At line L6, $\nu$ satisfies $F$, so it satisfies the abstraction of $\varphi$, and a $T$-model of $\mu = B(\nu)$ satisfies $\varphi$ by fact 2 of that page. For termination, $\eta \subseteq \mu$, so the lemma is false under $\nu$, and also under every assignment that agrees with $\nu$ on the theory atoms. Lemmas are never removed. So each pass excludes one more assignment of the $a$ theory atoms, and there are $2^a$ such assignments. $\square$

The bound is reached when line L7 returns all of $\mu$: then each lemma excludes exactly one assignment. A small conflict excludes all assignments that contain it, and that is why the choice of $\eta$ matters most.

### A worked example

Take $k \ge 0$ and the EUF formula

$$\varphi_k = (a = b \vee a = c) \wedge f(a) \ne f(b) \wedge f(a) \ne f(c) \wedge \bigwedge_{i=1}^{k} (g_i = h_i \vee g_i = e_i).$$

It is unsatisfiable because of its first three conjuncts. The other $k$ clauses are true in many ways and have nothing to do with the conflict. The abstraction has $3^{k+1}$ models: three for $a = b \vee a = c$ and three for each other clause.

A script ran the loop with a SAT solver that returns the first model in a fixed order, and with two choices for line L7.

| $k$ | models of the abstraction | SAT calls, $\eta = \mu$ | SAT calls, $\eta$ minimal |
|---|---|---|---|
| 0 | 3 | 4 | 3 |
| 1 | 9 | 10 | 3 |
| 2 | 27 | 28 | 3 |

With $\eta = \mu$, each model needs its own lemma, and the run takes $3^{k+1} + 1$ calls. With a minimal conflict, the theory solver returns $\{a = b,\ f(a) \ne f(b)\}$ or $\{a = c,\ f(a) \ne f(c)\}$, and these two lemmas, $a \ne b \vee f(a) = f(b)$ and $a \ne c \vee f(a) = f(c)$, make the abstraction unsatisfiable for every $k$. [Congruence closure](/congruence-closure/) with a proof forest finds such conflicts directly, see [theory conflict explanation](/theory-conflict-explanation/).

## Classic examples

- **Lemmas on demand.** De Moura, Rueß and Sorea used the offline loop in ICS for bounded model checking over infinite domains, with small conflict sets from the theory solver.
- **CVC.** Barrett, Dill and Stump added theory conflict clauses to the SAT solver Chaff during the search, an early form of the online schema.
- **MathSAT.** Audemard and others checked partial assignments of linear arithmetic during the search (early pruning).
- **[DPLL(T)](/dpll-t/) and [CDCL(T)](/cdcl-t/).** The online schema written as transition rules, and the CDCL loop of today's solvers, such as Z3, cvc5, Yices and MathSAT 5.
- **Arrays on demand.** Solvers for [arrays](/array-theory-satisfiability/) can add the read-over-write lemmas only for the reads that a candidate model gets wrong, in place of all of them.
- **[CEGIS](/cegis/).** A synthesis loop with the same shape: a candidate is proposed, a checker finds a counterexample, and the counterexample is added as a constraint.

## Variations

- **Online integration.** Call the theory solver on partial assignments (early pruning), let it derive literals ([theory propagation](/theory-propagation/)), and use its conflicts in conflict analysis. This is [DPLL(T)](/dpll-t/) and [CDCL(T)](/cdcl-t/).
- **Incremental SAT calls.** In the offline loop, keep the SAT solver and its learned clauses between calls, and only add the new lemma, see [incremental SAT](/incremental-sat/).
- **Lemmas with new atoms.** Flanagan, Joshi, Ou and Saxe let the theory solver return lemmas that contain atoms not in $\varphi$. Termination then needs a bound on the new atoms. Splitting on demand is the same idea for case splits.
- **Lazy encodings in eager solvers.** Kroening and others start a small-domain encoding of integer arithmetic with few values per variable, and increase the domain only when the SAT answer needs it (Handbook, Section 33.7.1). Lazy bit-blasting of expensive bit-vector operations follows the same pattern.
- **Theory combination.** With two or more theories, the shared equalities can be part of the abstraction, so that the SAT solver also guesses them. See [Nelson-Oppen](/nelson-oppen/) and [model-based theory combination](/model-based-theory-combination/).

## Pitfalls

- **Large lemmas.** Blocking the whole assignment is correct, but it removes only one model per call. In the example it needs $3^{k+1} + 1$ calls in place of 3.
- **Removing blocking clauses.** In the offline loop every lemma must stay. If a lemma is removed, the SAT solver can return the same model again, and the loop can run forever.
- **Reading the SAT model as the answer.** A model of the abstraction is not a model of $\varphi$ until the theory solver accepts $B(\nu)$.
- **Restarting the SAT solver from scratch.** A new SAT call per lemma throws away the learned clauses. The online schema, or an incremental SAT solver, keeps them.
- **Incomplete theory solvers.** If the theory solver can answer "unknown", as for nonlinear integer arithmetic, line L6 must not answer SAT, and the whole procedure must be able to answer "unknown".
- **Total assignments with irrelevant atoms.** A SAT solver usually returns a total assignment. An atom that does not matter for the Boolean structure still goes into $\mu$, and its value can cause a needless conflict. The Handbook (Section 33.4.3.6) recommends checking only a partial assignment that already satisfies the formula.

## Exercises

1. Show that the loop is still correct, and still terminates, if line L7 returns any $T$-unsatisfiable subset of $\mu$, even one that is not minimal.
2. For $\varphi_k$ of the example, show that every minimal conflict of every model is one of the two conflicts named there. Conclude that the minimal version makes at most 3 SAT calls for every $k$ and every order of models.
3. Change line L8 so that it adds the lemma and then removes all lemmas older than the last $r$. For $r = 1$, give a formula and an order in which the SAT solver returns its models such that the loop does not terminate.

## References
