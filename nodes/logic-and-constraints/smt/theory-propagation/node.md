---
tag: NV6E1E
kind: technique
slug: theory-propagation
name: Theory propagation
aliases:
- theory deduction
- T-propagation
- T-deduction
- theory-driven deduction
area: logic-and-constraints/smt
level: advanced
summary: The theory solver finds unassigned atoms whose value follows from the current theory literals, and gives them to the SAT search with an explanation clause, as unit propagation does for clauses.
prereqs: [dpll-t, unit-propagation]
see_also: [cdcl-t, theory-conflict-explanation, congruence-closure, difference-logic-satisfiability, simplex-for-smt, implication-graph, lazy-smt, e-graph]
sources:
  - book: isbn:9781643681603
    title: Clark Barrett, Roberto Sebastiani, Sanjit A. Seshia and Cesare Tinelli, Satisfiability Modulo Theories, Chapter 33 of the Handbook of Satisfiability, second edition, IOS Press, 2021
    locator: Section 33.4.1 (deduction of unassigned literals as a feature of theory solvers), Section 33.4.3.4 (T-propagation and T-deduction clauses, footnote 17 on the other names)
  - paper: doi:10.1145/1217856.1217859
    title: Robert Nieuwenhuis, Albert Oliveras and Cesare Tinelli, Solving SAT and SAT Modulo Theories, from an abstract Davis-Putnam-Logemann-Loveland procedure to DPLL(T), Journal of the ACM 53(6), 2006, pages 937 to 977
    locator: the TheoryPropagate rule of the abstract DPLL(T) system, and the generation of explanations on demand during conflict analysis
  - paper: doi:10.1007/978-3-540-27813-9_14
    title: Harald Ganzinger, George Hagen, Robert Nieuwenhuis, Albert Oliveras and Cesare Tinelli, DPLL(T), fast decision procedures, CAV 2004, LNCS 3114, pages 175 to 188
    locator: the interface of the theory solver, with SetTrue returning the theory consequences and Explain giving their reasons
  - paper: doi:10.1016/j.ic.2006.08.009
    title: Robert Nieuwenhuis and Albert Oliveras, Fast congruence closure and extensions, Information and Computation 205(4), 2007, pages 557 to 580
    locator: congruence closure with explanations, used for theory propagation in EUF
  - paper: doi:10.1007/11814948_19
    title: Scott Cotton and Oded Maler, Fast and flexible difference constraint propagation for DPLL(T), SAT 2006, LNCS 4121, pages 170 to 183
    locator: incremental propagation of implied difference constraints
  - paper: doi:10.1007/11817963_11
    title: Bruno Dutertre and Leonardo de Moura, A fast linear-arithmetic solver for DPLL(T), CAV 2006, LNCS 4144, pages 81 to 94
    locator: cheap theory propagation of bound atoms in the simplex-based solver
---

Theory propagation is the theory version of [unit propagation](/unit-propagation/). After the SAT part of a [DPLL(T)](/dpll-t/) or [CDCL(T)](/cdcl-t/) solver has set some theory atoms, the theory solver looks for an atom $p$ of the formula that is still unassigned but whose value is already fixed: a subset $\eta$ of the current theory literals entails $p$, or entails $\neg p$, in the theory $T$. It returns that literal, and the SAT part assigns it at once, without a decision. The *explanation clause* $\neg \eta \vee l$ is $T$-valid, and it serves as the reason of $l$ in the [implication graph](/implication-graph/), so that conflict analysis can resolve through theory steps. Without theory propagation, the SAT part can decide the wrong value of $p$, and the error shows only later, as a theory conflict. The Handbook lists the other names: forward reasoning, enhanced early pruning, theory propagation and T-deduction.

## In plain words

A SAT solver already does a cheap kind of thinking ahead. If a rule says "A or B" and A is false, it sets B to true at once, without guessing.

Theory propagation lets the theory expert do the same. Say the solver has set "a equals b" and "b equals c". The atom "a equals c" is still open, but there is nothing to guess: it must be true. The expert says so, and also says why: "because of a equals b and b equals c".

The solver then sets the atom, and keeps the reason. If a clash comes later, the reason lets the solver trace the clash back to the facts that caused it. The trade is the time the expert spends looking for such atoms against the guesses that it saves.

## When it applies

- The theory solver can find entailed atoms cheaply. For EUF, a merge in [congruence closure](/congruence-closure/) shows at once which atoms have both sides in the same class. For [difference logic](/difference-logic-satisfiability/), a new edge gives new shortest paths. For [linear arithmetic](/simplex-for-smt/), a new bound on $x$ entails the weaker bounds on $x$.
- The theory solver can explain each derived literal by a small set of earlier literals, either at once or later on demand.
- The formula has many atoms over the same terms, so that one assignment fixes the values of many others.

## The template

The holes are the set of atoms that the solver checks, the time when it builds the explanation, and how often the step runs.

```pseudo id=main
T-PROPAGATE(M)                           ▷ M is the trail; called when unit propagation finds no conflict
L1  μ ← the theory literals of M
L2  for each atom p of φ that M does not assign   ▷ hole: all atoms, or only the cheap candidates
L3      if μ ⊨_T p then l ← p
L4      else if μ ⊨_T ¬p then l ← ¬p
L5      else continue
L6      η ← a subset of μ with η ⊨_T l           ▷ hole: now, or only when conflict analysis asks for it
L7      assign l on M with the reason clause ¬η ∨ l
L8  return the assigned literals; the caller runs unit propagation again   ▷ hole: after every literal, or only at some points
```

**Soundness.** The clause $\neg \eta \vee l$ is $T$-valid, because $\eta \models_T l$. So every $T$-model of the current partial assignment that extends it to $p$ gives $p$ the value $l$, and assigning $l$ loses no $T$-model of the formula. The clause can be used as an antecedent in conflict analysis, like an input clause, and any clause that analysis learns from it is a $T$-consequence of the formula. This is the argument of fact D in the [CDCL(T)](/cdcl-t/) proof.

**Completeness is not needed.** A solver that propagates only some of the entailed literals is still correct, because the final full check at a total assignment catches every theory conflict. Theory propagation is an optimization, and real solvers do only the cheap part of it.

**Explanations on demand.** Most propagated literals never take part in a conflict. So Nieuwenhuis, Oliveras and Tinelli let line L6 store only a marker, and build $\eta$ when conflict analysis first needs the reason. The explanation must then be computed from the theory state at the time of the propagation, not from the current state, and the solver must make sure that every literal of $\eta$ is earlier on the trail than $l$.

### A worked example

Take the atoms $1: a = b$, $2: b = c$, $3: f(a) = f(c)$ and a Boolean variable $4$, and the clauses

$$(1) \wedge (2) \wedge (\neg 3 \vee 4) \wedge (\neg 3 \vee \neg 4).$$

The formula is unsatisfiable: the theory forces $3$, and the last two clauses force $\neg 3$.

*With theory propagation.* At level 0, unit propagation sets $1$ and $2$. Congruence closure merges $a, b, c$, then $f(a)$ and $f(c)$ by congruence, and atom $3$ is now entailed. Line L7 sets $3$ with the reason $3 \vee \neg 1 \vee \neg 2$. Unit propagation then sets $4$ from the third clause, and the fourth clause is false. The conflict is at level 0, so the answer is UNSAT after 0 decisions and 1 conflict.

*Without theory propagation.* At level 0 the SAT part sets $1$ and $2$, and nothing else. It decides $3$, and unit propagation sets $4$, which gives a Boolean conflict. It learns $\neg 3$ and goes back to level 0. Now the theory finds $f(a) \ne f(c)$ with $f(a) = f(c)$ entailed, which is a theory conflict at level 0. The answer is UNSAT after 1 decision and 2 conflicts.

A script ran the [CDCL(T)](/cdcl-t/) implementation of this site on this example, and on 300 random formulas with 4 constants, terms $f(c_i)$, 6 equality atoms, 3 Boolean variables and 8 clauses of 3 literals. Both versions gave the same answer on every formula. In total, theory propagation reduced the decisions from 2166 to 1758, the conflicts from 84 to 35, and the theory conflicts from 74 to 24.

## Classic examples

- **EUF.** [Congruence closure](/congruence-closure/) keeps, for each class, the atoms that mention its terms. A merge makes $s = t$ true when $s$ and $t$ end in one class, and makes $s = t$ false when it would join two classes that a disequality separates. The proof forest gives the explanation, see [theory conflict explanation](/theory-conflict-explanation/).
- **Difference logic.** Cotton and Maler propagate the atom $x - y \le c$ when the constraint graph has a path from $y$ to $x$ of weight at most $c$, and explain it by the edges of the path.
- **Linear arithmetic.** The simplex-based solver of Dutertre and de Moura propagates bound atoms cheaply: a new bound $x \le 3$ entails the atom $x \le 5$, and a bound on a basic variable can follow from the bounds of the nonbasic ones in its row. See [simplex for SMT](/simplex-for-smt/).
- **Bit-vectors and constraint solvers.** Lazy clause generation in constraint programming uses the same scheme: a propagator gives a literal, and an explanation clause is built when it is needed.

## Variations

- **Exhaustive or cheap.** Exhaustive propagation finds every entailed atom, which for linear arithmetic can cost as much as many satisfiability checks. Cheap propagation only finds what the solver sees as a side effect of its own data structures.
- **Eager or lazy explanations.** Build the explanation clause at once and add it to the clause database, or store only a marker and build the clause on demand.
- **Permanent T-deduction clauses.** The Handbook notes that the clause $\neg \eta \vee l$ can be kept after the backjump, with the same benefits as a learned clause, or dropped.
- **Equality propagation for combination.** In [Nelson-Oppen](/nelson-oppen/) combination, the solvers propagate entailed equalities between shared variables. These are *interface equalities*, which need not be atoms of the input formula.
- **Static learning.** A solver can add some explanation clauses before the search, for example $x \le 3 \rightarrow x \le 5$ for all pairs of bound atoms on $x$. This is propagation done once and eagerly.

## Pitfalls

- **An explanation that comes too late on the trail.** A reason clause must contain only literals that were assigned before $l$. If a lazy explanation uses a literal that came later, conflict analysis can loop or learn a wrong clause.
- **Explanations that are not small.** The trivial explanation $\eta = \mu$, all theory literals, is sound but makes the learned clauses long and the backjumps short.
- **Costly propagation.** If the search for entailed atoms costs more than the decisions that it saves, the solver gets slower. Solvers often skip exhaustive propagation, or run it only at some levels.
- **Propagating new atoms.** A literal on an atom that is not in the formula has no Boolean variable. It must be added as a new atom, which changes the termination argument, as in splitting on demand.

## Exercises

1. Show that without theory propagation, every run on the example makes at least one decision and finds at least two conflicts, whatever value the solver first gives to atom 3.
2. Show that the reason clause of a propagated EUF literal can be found from the proof forest of [congruence closure](/congruence-closure/), and bound its length by the number of equality atoms.
3. For difference logic, give two more constraints that, with $x - y \le 2$, entail the atom $x - z \le 7$ by a path of three edges. Write the explanation clause.

## References
