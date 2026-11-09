---
tag: R9CQRP
kind: algorithm
slug: dpll-t
name: DPLL(T)
aliases:
- lazy SMT by DPLL
- DPLL modulo theories
- Abstract DPLL Modulo Theories
area: logic-and-constraints/smt
level: advanced
summary: The framework of Nieuwenhuis, Oliveras and Tinelli that joins a DPLL engine to a theory solver by a set of transition rules. Every fair strategy of the rules is sound, complete and terminating.
solves: [smt-problem, euf-satisfiability]
model: word-ram
complexity:
  vars: {n: the number of propositional variables of the input}
  time: {worst: O(2^n n)}
  space: {extra: O(n)}
properties: {deterministic: true, recursive: false}
history:
  year: 2006
  people: [Robert Nieuwenhuis, Albert Oliveras, Cesare Tinelli]
  note: The name DPLL(T) is from Ganzinger, Hagen, Nieuwenhuis, Oliveras and Tinelli (CAV 2004). The abstract rule system is from LPAR 2005 and the Journal of the ACM, 2006.
prereqs: [dpll, smt-problem, boolean-abstraction, unit-propagation, congruence-closure]
see_also: [cdcl-t, lazy-smt, theory-propagation, theory-conflict-explanation, eager-smt-encoding, nelson-oppen, cdcl, chronological-backtracking]
sources:
  - paper: doi:10.1145/1217856.1217859
    title: Robert Nieuwenhuis, Albert Oliveras and Cesare Tinelli, Solving SAT and SAT Modulo Theories, from an abstract Davis-Putnam-Logemann-Loveland procedure to DPLL(T), Journal of the ACM 53(6), 2006, pages 937 to 977
    locator: Section 2 (Abstract DPLL), Section 3 (Abstract DPLL Modulo Theories, with termination, soundness and completeness in Theorem 3.7), and Section 4 (the DPLL(T) architecture)
  - paper: doi:10.1007/978-3-540-27813-9_14
    title: Harald Ganzinger, George Hagen, Robert Nieuwenhuis, Albert Oliveras and Cesare Tinelli, DPLL(T), fast decision procedures, CAV 2004, LNCS 3114, pages 175 to 188
    locator: the DPLL(X) engine and the interface of the theory solver
  - paper: doi:10.1007/978-3-540-32275-7_3
    title: Robert Nieuwenhuis, Albert Oliveras and Cesare Tinelli, Abstract DPLL and Abstract DPLL Modulo Theories, LPAR 2004, LNCS 3452, 2005, pages 36 to 50
    locator: the first form of the transition rules
  - book: isbn:9781643681603
    title: Clark Barrett, Roberto Sebastiani, Sanjit A. Seshia and Cesare Tinelli, Satisfiability Modulo Theories, Chapter 33 of the Handbook of Satisfiability, second edition, IOS Press, 2021
    locator: Section 33.4.4, An abstract framework (Definition 33.4.3, the transition rules, and the fair strategies)
  - book: isbn:9783662504963
    title: Daniel Kroening and Ofer Strichman, Decision Procedures, An Algorithmic Point of View, second edition, Springer, 2016
    locator: Chapter 3, From Propositional to Quantifier-Free Theories (Sections 3.2 to 3.4)
---

DPLL(T) is the standard way to build a lazy SMT solver. A [DPLL](/dpll/) engine searches for a truth assignment of the atoms of a formula, as if they were Boolean variables, and a theory solver for the theory $T$ checks that the literals assigned so far can hold together. Nieuwenhuis, Oliveras and Tinelli wrote the method as a small set of transition rules on states $M \parallel F$, where $M$ is a sequence of literals and $F$ is a set of clauses. A solver is a *strategy* that chooses which rule to apply. Every fair strategy stops, and its answer is correct, if the theory solver is correct on conjunctions of literals. This page is about the rule system and its proof. The [CDCL(T)](/cdcl-t/) page is about the loop that real solvers run inside this framework, with clause learning, theory propagation and restarts. The [lazy SMT](/lazy-smt/) page compares the lazy approach as a whole with the [eager](/eager-smt-encoding/) one.

## In plain words

A formula can mix true-or-false choices with facts about numbers, arrays or functions. A SAT solver is good at the choices but knows nothing about the facts. A theory solver knows the facts but can only check a plain list of them.

DPLL(T) lets them work in turns. The SAT side treats each fact as a yes-or-no switch and picks values one by one. Each time, it asks the theory side whether the switches set so far make sense together. If they do not, the theory side names a small set of switches that cannot all hold. The SAT side adds a rule that forbids this set, goes back one choice, and tries the other value. It stops when all switches are set and the theory side agrees, or when no choice is left to undo.

## The problem

**Input.** A finite set $F$ of clauses. Each literal is a propositional variable or a theory atom, or the negation of one. For EUF the atoms are equalities $s = t$ between ground terms, see [EUF satisfiability](/euf-satisfiability/). The [Boolean abstraction](/boolean-abstraction/) gives each atom a propositional variable, so $F$ is a CNF over $n$ variables.

**Output.** SAT with an assignment $M$ to all $n$ variables that satisfies $F$ and whose theory literals are $T$-consistent, or UNSAT when no such assignment exists, which means $F$ is $T$-unsatisfiable.

**The theory solver.** It gets a set $\mu$ of theory literals. It must be:

- (S1) *sound for conflicts*: it reports a conflict $\eta \subseteq \mu$ only if $\eta$ is $T$-unsatisfiable;
- (S2) *complete*: if $\mu$ is $T$-unsatisfiable, it reports some conflict $\eta \subseteq \mu$;
- (S3) *sound for propagation*: it reports a literal $l$ as entailed only if $\mu \models_T l$.

For EUF, [congruence closure](/congruence-closure/) meets all three. A theory solver that does no propagation meets (S3) trivially.

## The algorithm

**The rules.** A state is $M \parallel F$ or the state Fail. $M$ is a sequence of literals with no repeated variable, and some literals are marked as decisions, written $l^\bullet$. "$M \models \neg C$" means each literal of the clause $C$ is false in $M$. These are the rules of Definition 33.4.3 of the Handbook chapter.

| rule | from | to | when |
|---|---|---|---|
| Propagate | $M \parallel F, C \vee l$ | $M\, l \parallel F, C \vee l$ | $M \models \neg C$ and $l$ is undefined in $M$ |
| Decide | $M \parallel F$ | $M\, l^\bullet \parallel F$ | $l$ or $\neg l$ occurs in $F$, and $l$ is undefined |
| Fail | $M \parallel F, C$ | Fail | $M \models \neg C$ and $M$ has no decision |
| Restart | $M \parallel F$ | $\emptyset \parallel F$ | always |
| T-Propagate | $M \parallel F$ | $M\, l \parallel F$ | $M \models_T l$, $l$ or $\neg l$ occurs in $F$, and $l$ is undefined |
| T-Learn | $M \parallel F$ | $M \parallel F, C$ | each atom of $C$ occurs in $M$ or $F$, and $F \models_T C$ |
| T-Forget | $M \parallel F, C$ | $M \parallel F$ | $F \models_T C$ |
| T-Backjump | $M\, d^\bullet M' \parallel F, C$ | $M\, l' \parallel F, C$ | $M\, d^\bullet M' \models \neg C$, and a clause $C' \vee l'$ has $F, C \models_T C' \vee l'$, $M \models \neg C'$, $l'$ undefined in $M$, and $l'$ or $\neg l'$ occurs in $M\, d^\bullet M' \parallel F$ |

$C$ in T-Backjump is the *conflicting clause*, and $C' \vee l'$ is the *backjump clause*. A theory conflict $\eta \subseteq M$ becomes a propositional conflict by one T-Learn step with the *theory lemma* $\neg \eta$, which $M$ makes false. So the rules need no separate rule for theory conflicts.

**A basic strategy.** The pseudocode is one fair strategy. It calls the theory solver on each partial assignment, which is called *early pruning*, and it uses the negation of the decisions as the backjump clause.

```pseudo id=main
DPLL(T)(F)
L1  M ← the empty sequence
L2  loop
L3      apply Propagate until no clause of F is unit under M
L4      if some clause C of F has M ⊨ ¬C then
L5          if M has no decision then return UNSAT                    ▷ Fail
L6          M ← M1 ¬d, where M = M1 d• M2 and d is the last decision  ▷ T-Backjump
L7          if C was added at line L9 then remove C from F; go to L3  ▷ T-Forget
L8      η ← the conflict that the theory solver finds in the theory literals of M, or nil
L9      if η ≠ nil then add the clause ¬η to F; go to L3              ▷ T-Learn
L10     if the theory solver finds atoms l undefined in M with M ⊨T l then append them to M; go to L3   ▷ T-Propagate
L11     if every variable of F is defined in M then return SAT, M
L12     M ← M l• for an undefined variable l                          ▷ Decide
```

Line L6 is T-Backjump with the backjump clause $\neg d_1 \vee \cdots \vee \neg d_k$, where $d_1, \ldots, d_k$ are the decisions of $M$. So $C' = \neg d_1 \vee \cdots \vee \neg d_{k-1}$ and $l' = \neg d_k$. This is the chronological backtracking of [DPLL](/dpll/). Line L9 adds a lemma that $M$ makes false, so the next pass reaches line L4 at once. After the backjump the lemma is not needed, and line L7 forgets it. So $F$ never holds more than one lemma.

## Example

Take $(a = b \vee a = c) \wedge f(a) \ne f(b) \wedge f(a) \ne f(c)$, with the variables $p_1$ for $a = b$, $p_2$ for $a = c$, $p_3$ for $f(a) = f(b)$ and $p_4$ for $f(a) = f(c)$. The clauses are $\{p_1, p_2\}$, $\{\neg p_3\}$ and $\{\neg p_4\}$. This formula is unsatisfiable, but no single clause shows it.

| step | rule | $M$ after the step | note |
|---|---|---|---|
| 1 | Propagate, twice | $f(a) \ne f(b),\ f(a) \ne f(c)$ | two unit clauses |
| 2 | Decide | $\ldots,\ (a = b)^\bullet$ | the theory check of line L8 passes before this step |
| 3 | T-Learn | unchanged | congruence closure finds $\eta = \{a = b,\ f(a) \ne f(b)\}$, and $F$ gets $\{a \ne b,\ f(a) = f(b)\}$ |
| 4 | T-Backjump | $f(a) \ne f(b),\ f(a) \ne f(c),\ a \ne b$ | the lemma is false, so the decision is flipped |
| 5 | Propagate | $\ldots,\ a \ne b,\ a = c$ | from the clause $\{a = b, a = c\}$ |
| 6 | T-Learn | unchanged | $\eta = \{a = c,\ f(a) \ne f(c)\}$, and $F$ gets $\{a \ne c,\ f(a) = f(c)\}$ |
| 7 | Fail | Fail | the lemma is false and $M$ has no decision |

The answer is UNSAT after one decision and two theory lemmas. The implementation gives this same run.

## Correctness

The proof uses three facts. First, each literal in $M$ is a $T$-consequence of $F$ and the decisions before it. Second, each clause ever in $F$ is a $T$-consequence of the input. With (S1), this shows that UNSAT is correct, because Fail needs a false clause and no decisions. Third, at SAT, $M$ is total, satisfies each clause, and the theory solver has accepted its theory literals, so by (S2) they are $T$-consistent, and $M$ gives a $T$-model of the input. Termination comes from a measure on $M$: write $M = M_0\, d_1^\bullet M_1 \cdots d_k^\bullet M_k$ and compare the tuples $(|M_0|, |M_1|, \ldots, |M_k|)$ in lexicographic order. Propagate, T-Propagate and Decide make the tuple larger, and so does T-Backjump, because it adds one literal at an earlier level. Each T-Learn step is followed at once by T-Backjump or Fail. The tuples are bounded because $M$ has at most $n$ literals. The full proof is in the [proof page](proofs/correctness.md).

The general theorem of Nieuwenhuis, Oliveras and Tinelli (Theorem 3.7 of the 2006 paper) allows any strategy that does not apply T-Learn and T-Forget forever without other steps, and that applies Restart with growing intervals.

## Complexity

Count rule applications. The decisions and backjumps of the strategy walk a binary tree of depth at most $n$, so there are at most $2^n$ backjumps and fewer than $2^n$ decisions. After each decision or backjump at most $n$ literals are added. Each T-Learn is followed by a backjump or by Fail. So a run applies $O(2^n n)$ rules. Each pass of the loop also does one scan of the clauses and at most a few calls of the theory solver, so the time is $O(2^n n)$ times the cost of one pass. The exponential bound cannot be improved in general unless P = NP, because SAT is the case of the empty theory.

The space is $O(n)$ beyond the input: the trail, and at most one lemma of at most $n$ literals.

## Properties

- **Lazy.** The theory solver sees only conjunctions of literals, and the SAT side sees only clauses. The two parts can be changed one at a time.
- **Theory independent.** Any theory with a solver that meets (S1) and (S2) can be plugged in, and the proof does not change.
- **Exact on any formula.** It decides $T$-satisfiability of any ground CNF over the atoms of $T$, and so of any quantifier-free formula after a [Tseitin transformation](/tseitin-transformation/).
- **Online.** The early pruning of line L8 needs a theory solver that can take literals one at a time and undo them, as in [incremental solving](/incremental-solving/).

## Variants and improvements

- **CDCL(T).** Replace the backjump clause of line L6 by a learned clause from conflict analysis over the theory explanations, and backjump many levels at once. This is [CDCL(T)](/cdcl-t/), the loop of modern solvers.
- **Offline or very lazy.** Do not call the theory solver until $M$ is total. If the total $M$ is $T$-inconsistent, learn the blocking clause $\neg \eta$ and restart. This is the first [lazy SMT](/lazy-smt/) scheme. To terminate, it must not forget the blocking clauses.
- **Theory propagation.** Line L10 is [theory propagation](/theory-propagation/). If T-Propagate has priority over Decide and is complete, $M$ can never become $T$-inconsistent, and no theory lemma is needed.
- **Small conflicts.** A small $\eta$ gives a short lemma, which prunes more. See [theory conflict explanation](/theory-conflict-explanation/).
- **Splitting on demand.** Barrett, Nieuwenhuis, Oliveras and Tinelli extend the rules so that the theory solver can ask for a case split on a new atom. This is how integer and array solvers avoid doing case splits inside.
- **Theory combination.** For a union of theories, the theory solver can be a [Nelson-Oppen](/nelson-oppen/) combination, or the SAT side can also decide the equalities between shared variables, as in delayed theory combination and [model-based theory combination](/model-based-theory-combination/).

## When to use it

Use the DPLL(T) rules when you design or prove a lazy SMT solver: they separate what is allowed from what is a good choice. Use the basic strategy of this page for teaching and for small inputs. For a real solver use [CDCL(T)](/cdcl-t/), which is a strategy of the same rules. Use an [eager encoding](/eager-smt-encoding/) instead when the theory has a compact encoding to SAT and the theory reasoning is light, as for small [bit-vectors](/bit-vector-satisfiability/).

## Pitfalls

- **Lemmas with new atoms.** T-Learn allows only atoms of the current state. A lemma with fresh atoms can break termination, because the set of possible assignments grows. Splitting on demand handles new atoms with a bound on them.
- **Forgetting blocking clauses in the offline scheme.** If a strategy restarts after a theory conflict and then forgets the blocking clause, it can find the same assignment again and loop.
- **Large conflicts.** Returning all of $M$ as the conflict is correct, but the lemma then blocks only one assignment, and the search can take $2^n$ steps on easy inputs.
- **Partial checks.** If the theory solver is complete only on total assignments, the early check of line L8 can miss a conflict. This is safe, as long as the check at line L11 is complete.
- **Incomplete theory solvers.** If (S2) fails, for example for nonlinear integer arithmetic, a SAT answer can be wrong. The solver must answer "unknown" instead.

## Implementations

## History

Lazy combinations of a SAT solver and a theory solver appeared around 2002, in the work of Audemard and others on MathSAT, Barrett, Dill and Stump on CVC, and de Moura, Rueß and Sorea on lemmas on demand. Ganzinger, Hagen, Nieuwenhuis, Oliveras and Tinelli named the architecture DPLL(T) at CAV 2004: a general DPLL(X) engine with a solver for $T$ in place of X. Nieuwenhuis, Oliveras and Tinelli gave the abstract transition rules at LPAR 2004 and the full treatment with proofs in the Journal of the ACM in 2006. The rules are now the usual way to describe and compare SMT solvers.

## References
