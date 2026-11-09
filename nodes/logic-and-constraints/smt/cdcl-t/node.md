---
tag: R7T2R4
kind: algorithm
slug: cdcl-t
name: CDCL(T)
aliases:
- conflict-driven DPLL(T)
- CDCL modulo theories
- conflict-driven clause learning modulo theories
area: logic-and-constraints/smt
level: advanced
summary: The main loop of modern lazy SMT solvers. A CDCL SAT solver learns first-UIP clauses from an implication graph whose edges include the explanations of a theory solver.
solves: [smt-problem, euf-satisfiability]
model: word-ram
complexity:
  vars: {n: the number of propositional variables of the input}
  time: {worst: O(3^n n)}
  space: {extra: O(3^n n)}
properties: {deterministic: true, recursive: false}
history:
  year: 2004
  people: [Harald Ganzinger, George Hagen, Robert Nieuwenhuis, Albert Oliveras, Cesare Tinelli]
  note: Lazy solvers with theory conflict clauses and backjumping appeared in 2002 in MathSAT, CVC and ICS. The DPLL(T) paper of CAV 2004 joined theory propagation with explanations to a CDCL engine of the Chaff kind.
prereqs: [dpll-t, cdcl, first-uip, implication-graph, congruence-closure]
see_also: [lazy-smt, theory-propagation, theory-conflict-explanation, incremental-solving, non-chronological-backtracking, clause-learning, restarts, unsat-core]
sources:
  - paper: doi:10.1007/978-3-540-27813-9_14
    title: Harald Ganzinger, George Hagen, Robert Nieuwenhuis, Albert Oliveras and Cesare Tinelli, DPLL(T), fast decision procedures, CAV 2004, LNCS 3114, pages 175 to 188
    locator: the DPLL(X) engine, theory propagation, and the explanation of propagated literals for conflict analysis
  - paper: doi:10.1145/1217856.1217859
    title: Robert Nieuwenhuis, Albert Oliveras and Cesare Tinelli, Solving SAT and SAT Modulo Theories, from an abstract Davis-Putnam-Logemann-Loveland procedure to DPLL(T), Journal of the ACM 53(6), 2006, pages 937 to 977
    locator: Section 2 (Backjump and backjump clauses found by conflict graph analysis), Section 3 (Theorem 3.7), Section 4 (the DPLL(T) architecture and explanations)
  - book: isbn:9781643681603
    title: Clark Barrett, Roberto Sebastiani, Sanjit A. Seshia and Cesare Tinelli, Satisfiability Modulo Theories, Chapter 33 of the Handbook of Satisfiability, second edition, IOS Press, 2021
    locator: Section 33.4.3.4 (T-propagation and T-deduction clauses), Section 33.4.3.5 (T-backjumping and T-learning, with the 1UIP mixed conflict clause of Example 33.4.2)
  - paper: doi:10.1109/12.769433
    title: João P. Marques-Silva and Karem A. Sakallah, GRASP, a search algorithm for propositional satisfiability, IEEE Transactions on Computers 48(5), 1999, pages 506 to 521
    locator: conflict analysis on the implication graph and non-chronological backtracking
  - paper: doi:10.1109/iccad.2001.968634
    title: Lintao Zhang, Conor F. Madigan, Matthew H. Moskewicz and Sharad Malik, Efficient conflict driven learning in a Boolean satisfiability solver, ICCAD 2001, pages 279 to 285
    locator: the first UIP learning scheme
  - paper: doi:10.1007/978-3-540-24605-3_37
    title: Niklas Eén and Niklas Sörensson, An extensible SAT-solver, SAT 2003, LNCS 2919, pages 502 to 518
    locator: the analyze procedure and the interface for clauses whose reasons are computed on demand
  - paper: doi:10.1007/3-540-45620-1_17
    title: Gilles Audemard, Piergiorgio Bertoli, Alessandro Cimatti, Artur Korniłowicz and Roberto Sebastiani, A SAT based approach for solving formulas over Boolean and linear mathematical propositions, CADE 2002, LNCS 2392, pages 195 to 210
    locator: MathSAT, early pruning and theory-driven backjumping and learning
  - paper: doi:10.1007/978-3-540-78800-3_24
    title: Leonardo de Moura and Nikolaj Bjørner, Z3, an efficient SMT solver, TACAS 2008, LNCS 4963, pages 337 to 340
    locator: the architecture of a CDCL(T) solver with a congruence closure core
---

CDCL(T) is the loop that runs inside almost every lazy SMT solver. It is a [CDCL](/cdcl/) SAT solver whose implication graph has two kinds of edges: edges from clauses, and edges from a theory solver. When the theory solver derives a literal, it also gives an *explanation*, a clause that is valid in the theory $T$ and that acts as the reason of the literal. When the theory solver finds a conflict, its conflict clause starts conflict analysis like any false clause. The solver then learns a [first-UIP](/first-uip/) clause that can mix Boolean and theory literals, and it jumps back over the decisions that did not take part. This page is about this loop. The [DPLL(T)](/dpll-t/) page is about the abstract rule system that CDCL(T) is one strategy of, and it proves that every fair strategy is correct. The [lazy SMT](/lazy-smt/) page compares the whole lazy approach with the [eager](/eager-smt-encoding/) one.

## In plain words

A SAT solver is joined to a solver that knows one theory, such as equality or arithmetic. The SAT solver sets switches, one per fact. After each step the theory solver looks at the facts that are switched on or off.

It can do two things. It can see that another fact must now hold, and switch it on, with a note that says why. Or it can see that the facts cannot all hold, and name a small set of them that cannot.

When something fails, the solver follows the notes back from the failure, through Boolean steps and theory steps alike, to the point where one fact alone explains it. It stores a new rule from this, jumps back to the last choice that matters, and goes on. Choices that had no part in the failure are undone too, and are made again later only if needed.

## The problem

**Input.** A finite set $F$ of clauses over $n$ propositional variables. Some variables stand for theory atoms through the [Boolean abstraction](/boolean-abstraction/). Here the theory is EUF, and the atom of a variable is an equality $s = t$ of ground terms, see [EUF satisfiability](/euf-satisfiability/). The other variables are plain Boolean variables.

**Output.** SAT with a total assignment that satisfies $F$ and whose theory literals have a $T$-model, or UNSAT when no such assignment exists.

**The theory solver.** It gets the theory literals $\mu$ of the trail. It must:

- (T1) report a *conflict clause* $\neg \eta$ only if $\eta \subseteq \mu$ and $\eta$ is $T$-unsatisfiable;
- (T2) report some conflict when $\mu$ is $T$-unsatisfiable;
- (T3) report a literal $l$ only together with an *explanation* $\eta \subseteq \mu$ with $\eta \models_T l$. The clause $l \vee \neg \eta$ is then $T$-valid, and it becomes the reason of $l$.

For EUF, [congruence closure](/congruence-closure/) with a proof forest meets all three. Its explanation of an equality $s = t$ is a set of input equalities that implies $s = t$, see [theory conflict explanation](/theory-conflict-explanation/).

## The algorithm

The solver keeps a trail of literals, each with a decision level and a reason. A decision has no reason. A literal from unit propagation has the clause that became unit as its reason. A literal from [theory propagation](/theory-propagation/) has its explanation clause as its reason. Both kinds of reason are clauses $l \vee \neg l_1 \vee \cdots \vee \neg l_k$ whose other literals were on the trail before $l$. So the reasons form one [implication graph](/implication-graph/), and conflict analysis does not need to know which edges came from the theory.

```pseudo id=main
CDCL(T)(F)
L1  loop: run unit propagation; let C be a false clause, or nil
L2      if C = nil then ask the theory solver; it gives a conflict clause C, or propagates literals with explanation reasons
L3          if it propagated a literal then go to L1
L4      if C ≠ nil then
L5          if every literal of C has level 0 then return UNSAT
L6          backtrack to the highest level of a literal of C
L7          (D, b) ← first-UIP analysis of C over the reasons; b is the second highest level in D
L8          backtrack to level b                              ▷ non-chronological backjump
L9          add D to F; put its UIP literal on the trail with reason D
L10         if the number of conflicts since the last restart reaches the limit then backtrack to level 0 and multiply the limit by g > 1
L11     else if every variable is assigned then return SAT, the trail
L12     else open a new level and decide an unassigned variable
```

**First-UIP analysis.** Line L7 starts from the false clause $C$, and resolves it with the reason of the last trail literal of the current level that occurs in it. It stops when exactly one literal of the current level is left. This literal is the negation of the first *unique implication point*: each path in the implication graph from the decision of the current level to the conflict goes through it. Literals of level 0 are dropped, because they follow from $F$ alone. The result $D$ has one literal at the current level and all others at lower levels, so after the backjump of line L8, $D$ is a unit clause, and line L9 puts its UIP literal on the trail. Some solvers then make $D$ shorter, see [clause minimization](/clause-minimization/).

**Line L6.** A theory conflict can involve only literals of levels below the current one, for example when a theory check is lazy. Line L6 moves to the highest level of $C$, so that the analysis starts at a level that $C$ touches.

**The theory solver in the loop.** Line L2 runs after each fixpoint of unit propagation. This is *early pruning*: a conflict is found at the level where it appears. The implementation builds the congruence closure again from the trail at each call, which is simple and slow. A real solver keeps the closure, adds each new literal in place, and undoes merges on a trail when it backjumps, see [incremental solving](/incremental-solving/). Many solvers also compute the explanation of a propagated literal only when conflict analysis asks for its reason.

## Example

Take four plain variables $x, w, y, q$ and three EUF atoms $a = b$, $b = c$ and $f(a) = f(c)$. The clauses are

$$\neg x \vee a = b, \quad \neg y \vee b = c, \quad f(a) \ne f(c) \vee q, \quad f(a) \ne f(c) \vee \neg q, \quad x \vee w.$$

The decision order is $x, w, y, a = b, b = c, f(a) = f(c), q$, each with the value true first. The table shows the trail of the implementation, written as level: literals.

| step | event | trail after the step |
|---|---|---|
| 1 | decide $x$; propagate $a = b$ from $\neg x \vee a = b$ | 1: $x$, $a = b$ |
| 2 | decide $w$ | 2: $w$ |
| 3 | decide $y$; propagate $b = c$ | 3: $y$, $b = c$ |
| 4 | theory propagation: $f(a) = f(c)$ with reason $f(a) = f(c) \vee a \ne b \vee b \ne c$ | 3: $y$, $b = c$, $f(a) = f(c)$ |
| 5 | propagate $q$ from $f(a) \ne f(c) \vee q$; now $f(a) \ne f(c) \vee \neg q$ is false | 3: $y$, $b = c$, $f(a) = f(c)$, $q$ |
| 6 | analysis: resolve with the reason of $q$; only $f(a) = f(c)$ is left at level 3 | learn $f(a) \ne f(c)$, backjump to level 0 |
| 7 | the learned unit is put on the trail; decide $x$, $w$, $y$ again | 0: $f(a) \ne f(c)$; 1: $x$, $a = b$; 2: $w$; 3: $y$, $b = c$ |
| 8 | theory conflict: $a = b$ and $b = c$ give $f(a) = f(c)$ | conflict clause $f(a) = f(c) \vee a \ne b \vee b \ne c$ |
| 9 | analysis: $f(a) = f(c)$ has level 0 and is dropped; $b \ne c$ is the only literal of level 3 | learn $b \ne c \vee a \ne b$, backjump to level 1 |
| 10 | put $b \ne c$ on the trail; propagate $\neg y$; decide $w$ and $q$ | 1: $x$, $a = b$, $b \ne c$, $\neg y$; 2: $w$; 3: $q$ |
| 11 | every variable is assigned | SAT |

Three things in this run are special to CDCL(T). At step 6 the first UIP is $f(a) = f(c)$, a literal that the theory solver derived, so the learned clause is about a theory atom that no decision set. At step 8 the conflict comes from the theory and becomes a clause with three literals, and at step 9 the analysis removes the literal of level 0 from it. At step 9 the solver jumps from level 3 to level 1, over the decision $w$ at level 2, which had no part in the conflict. The plain [DPLL(T)](/dpll-t/) strategy would flip only the last decision $y$.

The model is $x$, $w$, $\neg y$, $q$, $a = b$, $b \ne c$ and $f(a) \ne f(c)$. It has a $T$-model, for example $a = b = 0$, $c = 1$, $f(0) = 0$ and $f(1) = 1$. The implementation gives this same run, with two conflicts, one of them a theory conflict, and one theory propagation.

## Correctness

The proof uses four invariants. Each clause of $F$ is a $T$-consequence of the input $F_0$. Each reason clause is in $F$ or is $T$-valid. Each literal of the trail is a $T$-consequence of $F_0$ and of the decisions of its level and lower levels. Each learned clause is a resolvent of such clauses, so it is a $T$-consequence of $F_0$. With these, UNSAT is correct: a clause whose literals are all false at level 0 shows that $F_0$ has no $T$-model. SAT is correct: the trail is total, every clause is true, and the theory solver accepted the theory literals, so by (T2) they have a $T$-model.

For termination, the key fact is that each learned clause is new. Before the decision that opened the conflict level, unit propagation was at a fixpoint. At that time all literals of $D$ except the UIP literal were already false, and the UIP literal was unassigned. If $D$ were in $F$, unit propagation would have set the UIP literal then. So each conflict adds a new clause to $F$, and nothing is deleted. There are at most $3^n$ clauses over $n$ variables, so there are at most $3^n$ conflicts. Between two conflicts the trail only grows, so the run is finite. The full proof is in the [proof page](proofs/correctness.md).

This argument does not need the growing restart limit of line L10. A solver that also deletes learned clauses needs it, as in Theorem 3.7 of Nieuwenhuis, Oliveras and Tinelli.

## Complexity

Count the steps that change the trail. There are at most $3^n$ conflicts, and between two conflicts at most $n$ literals are put on the trail, so there are $O(3^n n)$ steps. The learned clauses take $O(3^n n)$ space in the worst case. Each step costs one pass of unit propagation and one call of the theory solver. With [two watched literals](/two-watched-literals/) and an incremental congruence closure, the cost of a step is close to the work it does. With the implementation of this page, which scans all clauses and builds the closure again, it is polynomial in the size of the input and of the learned clauses.

The exponential bound cannot be improved in general unless P = NP, because the theory can be empty and then the problem is [SAT](/sat/). In practice the number of conflicts is far smaller than the bound. Real solvers delete most learned clauses from time to time, so the space stays small.

## Properties

- **One implication graph.** Theory steps and Boolean steps are edges of the same graph, so all CDCL methods work without change: first-UIP learning, non-chronological backjumping, clause minimization, and the activity scores of the decision heuristic.
- **Mixed learned clauses.** A learned clause can contain theory atoms and plain Boolean variables, and it is in general not $T$-valid. It follows from the input in $T$.
- **No new atoms.** Explanations and learned clauses use only atoms that are already in the input, so the set of variables does not grow.
- **Deterministic.** With a fixed decision order and restart rule the run is the same each time.

## Variants and improvements

- **Lazy explanations.** The theory solver records only that it propagated $l$, and computes the reason of $l$ when conflict analysis reaches it. This saves time, because most propagated literals never take part in a conflict. The solver interface of the DPLL(T) paper of 2004 has such an on-demand Explain operation.
- **Theory propagation strength.** Exhaustive theory propagation finds every entailed literal, and then the trail never becomes $T$-inconsistent. Cheaper solvers propagate only some literals, such as the equalities that congruence closure finds, and leave the rest to conflicts. See [theory propagation](/theory-propagation/).
- **Final checks only.** Some theories, such as nonlinear arithmetic, are expensive to check. The solver can check them only when the trail is total, and do cheap checks before.
- **Splitting on demand and new atoms.** The theory solver can ask for a case split, as for integers in [linear integer arithmetic](/linear-integer-arithmetic-satisfiability/). Flanagan, Joshi, Ou and Saxe let learned clauses contain new atoms. Termination then needs a bound on the new atoms.
- **Combination of theories.** For more than one theory, the equalities between shared terms can be decided by the SAT side, as in delayed theory combination, or guessed from models, as in [model-based theory combination](/model-based-theory-combination/).
- **Incremental use and unsat cores.** With assumptions and push and pop, the same solver answers many related queries, see [incremental solving](/incremental-solving/). The final conflict over the assumptions gives an [unsat core](/unsat-core/).

## When to use it

Use CDCL(T) when you build or tune a lazy SMT solver for a theory that has a fast solver for conjunctions of literals with explanations. This covers EUF, [linear real arithmetic](/linear-real-arithmetic-satisfiability/) with [simplex](/simplex-for-smt/), [difference logic](/difference-logic-satisfiability/) and arrays. Use the plain [DPLL(T)](/dpll-t/) strategy to teach the rules or to prove a new strategy correct. Use an [eager encoding](/eager-smt-encoding/) when the theory has a compact encoding to SAT, as for small [bit-vectors](/bit-vector-satisfiability/) by [bit-blasting](/bit-blasting/).

## Pitfalls

- **Reasons that are not in the past.** Each literal $\neg l_i$ of a reason must be on the trail before the literal it explains. If an explanation uses a literal that came later, conflict analysis can produce a clause that is not asserting, or it can loop. Explanations from a theory state that is later than the propagation have this bug.
- **Backtracking the theory solver.** After a backjump the theory solver must forget every literal above the new level, and also every merge or bound it derived from them. A merge that stays after a backjump makes the solver report wrong conflicts.
- **Large explanations.** An explanation that is correct but large, such as all equalities on the trail, gives long learned clauses and weak backjumps. Congruence closure with a proof forest gives small explanations.
- **Theory conflicts below the current level.** A theory conflict can lie wholly below the current level. If the analysis starts at the current level without line L6, it finds no literal of that level and fails.
- **Deleting learned clauses.** If a solver deletes learned clauses and restarts too often, termination can fail. Keep the restart intervals growing, or keep some learned clauses forever.
- **Incomplete theory solvers.** If (T2) fails, a SAT answer can be wrong. The solver must answer "unknown".

## Implementations

## History

Clause learning and non-chronological backtracking for SAT came from GRASP of Marques-Silva and Sakallah (1996 and 1999), and Chaff with the first UIP scheme of Zhang, Madigan, Moskewicz and Malik (2001). Around 2002, MathSAT of Audemard and others, CVC of Barrett, Dill and Stump, and ICS with lemmas on demand of de Moura, Rueß and Sorea used theory conflict sets to drive backjumping and learning in a SAT solver. Ganzinger, Hagen, Nieuwenhuis, Oliveras and Tinelli named the architecture DPLL(T) at CAV 2004. They used a CDCL engine, theory propagation, and explanations of propagated literals, which put the theory steps into the implication graph. Nieuwenhuis, Oliveras and Tinelli gave the abstract rules and proofs in 2006. Z3 of de Moura and Bjørner (2008), Yices, CVC4 and cvc5 and MathSAT 5 all have a CDCL(T) core.

## References
