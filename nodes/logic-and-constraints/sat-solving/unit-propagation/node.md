---
tag: 2156MK
kind: technique
slug: unit-propagation
name: Unit propagation
aliases:
- Boolean constraint propagation
- BCP
- unit clause propagation
area: logic-and-constraints/sat-solving
level: core
summary: Repeatedly assign the literal forced by a unit clause until no clause is unit or some clause is false. The main inference step of DPLL and CDCL.
prereqs: [unit-clause, conjunctive-normal-form]
see_also: [two-watched-literals, unit-resolution, dpll, cdcl, implication-graph, horn-sat, failed-literal-probing, lookahead-sat]
sources:
  - paper: doi:10.1145/321033.321034
    title: Martin Davis and Hilary Putnam, A computing procedure for quantification theory, Journal of the ACM 7(3), 1960
    locator: pages 201 to 215 (the rule for eliminating one-literal clauses)
  - paper: doi:10.1145/368273.368557
    title: Martin Davis, George Logemann and Donald Loveland, A machine program for theorem-proving, Communications of the ACM 5(7), 1962
    locator: pages 394 to 397 (the one-literal clause rule inside the search)
  - paper: doi:10.1016/0743-1066(84)90014-1
    title: William F. Dowling and Jean H. Gallier, Linear-time algorithms for testing the satisfiability of propositional Horn formulae, Journal of Logic Programming 1(3), 1984
    locator: pages 267 to 284 (propagation with a counter per clause in linear time, which decides Horn formulas)
  - paper: doi:10.1145/378239.379017
    title: Matthew W. Moskewicz, Conor F. Madigan, Ying Zhao, Lintao Zhang and Sharad Malik, Chaff, engineering an efficient SAT solver, Proceedings of the 38th Design Automation Conference, 2001
    locator: pages 530 to 535 (Boolean constraint propagation as the dominant cost of a solver, and two watched literals)
  - paper: "Hantao Zhang and Mark E. Stickel, Implementing the Davis-Putnam method, Journal of Automated Reasoning 24(1-2), 2000, pages 277 to 296"
    locator: the head and tail list scheme of SATO for lazy detection of unit clauses
  - book: isbn:9781643681603
    title: Armin Biere, Marijn Heule, Hans van Maaren and Toby Walsh (eds.), Handbook of Satisfiability, second edition, IOS Press, 2021
    locator: Chapter 4, Conflict-Driven Clause Learning SAT Solvers, by Marques-Silva, Lynce and Malik (unit propagation and its lazy data structures)
  - book: isbn:9780201038064
    title: Donald E. Knuth, The Art of Computer Programming, Volume 4B, Combinatorial Algorithms Part 2, 2022
    locator: Section 7.2.2.2, Satisfiability (unit propagation with watched literals in Algorithms D and C)
---

Unit propagation is the inference step that repeats the unit rule: while some clause of the formula is a [unit clause](/unit-clause/) under the current partial assignment, it assigns the one open literal of that clause, and it stops when no clause is unit or when some clause has all its literals false. Every literal it adds is implied by the formula and the assignment, and the result does not depend on the order in which units are processed. It is the main inference of [DPLL](/dpll/) and [CDCL](/cdcl/), where it takes most of the running time, and with [two watched literals](/two-watched-literals/) each assignment touches only a few clauses.

## In plain words

A solver has set some values and keeps a to-do list of the values it has not looked at yet. It takes the next value from the list and checks the rules that this value may hurt, that is, the rules where it rules out an option. If such a rule now has one open option left, that option is forced: the solver sets it and puts it on the to-do list. If a rule has no option left, the solver stops and reports a dead end.

When the list is empty and no dead end came up, no rule forces anything more. The forced values are the same whatever order the solver used, so the order is a matter of speed only.

## When it applies

- The formula is in [CNF](/conjunctive-normal-form/), or in a form with a unit rule of its own, such as XOR clauses, cardinality constraints or theory atoms in [DPLL(T)](/dpll-t/).
- A partial assignment $\tau$ exists, made of decisions and earlier forced literals, and a queue $Q$ holds the literals of $\tau$ whose consequences are not yet processed. At the start of a search, $\tau$ holds the unit clauses of the input.
- The aim is to find cheaply the literals that $F \wedge \tau$ implies through chains of unit clauses, or a clause that $\tau$ falsifies. Unit propagation is not complete: it can stop without a conflict on an unsatisfiable formula, for example on $\{x, y\}, \{x, \neg y\}, \{\neg x, y\}, \{\neg x, \neg y\}$ with $\tau = \emptyset$.

## The template

```pseudo id=main
UNIT-PROPAGATE(F, τ, Q)                       ▷ Q: literals of τ not yet processed
L1  while Q is not empty do
L2      ℓ ← POP(Q)                              ▷ hole ORDER: first in first out, or a stack
L3      for each clause C in CANDIDATES(¬ℓ) do  ▷ hole CANDIDATES: clauses that hold ¬ℓ, or that watch it
L4          s ← STATUS(C, τ)                    ▷ hole STATUS: a scan, a counter, or a watch move
L5          if s is "falsified" then return C   ▷ a conflict, with C as the false clause
L6          if s is "unit with literal u" then
L7              add u to τ; reason(u) ← C; PUSH(Q, u)
L8  return none                                 ▷ no clause of F is unit or false under τ
```

The holes:

- **ORDER.** A queue processes literals by distance from the decision; MiniSat and most solvers use the trail itself as the queue, with a head index. The forced set does not depend on it, but the conflict found, and so the learned clause, does.
- **CANDIDATES.** Every clause that can turn unit or false when $\ell$ becomes true holds $\neg\ell$. So the full occurrence list of $\neg\ell$ is enough. [Two watched literals](/two-watched-literals/) narrows it to the clauses that watch $\neg\ell$.
- **STATUS.** A scan of the clause costs $O(|C|)$. A counter of false literals per clause, decremented on backtrack, gives the status in $O(1)$ (Dowling and Gallier). A watched literal scheme searches for a new watch and finds a unit or a conflict only when none exists.
- **Reasons.** CDCL records the reason of each forced literal, which is the edge set of the [implication graph](/implication-graph/). DPLL does not need them.

**Correctness.** Write $\tau_0$ for the assignment at the call and $\tau^*$ for the assignment at the return. Assume that every literal of $\tau_0$ whose clauses might be unit or false is in $Q$; at the start of a search this means $Q = \tau_0$.

1. *Soundness.* Every model of $F$ that extends $\tau_0$ extends $\tau^*$. By the unit rule, each literal added at line L7 is true in every such model, by induction on the order of addition. So if line L5 returns a clause, $F \wedge \tau_0$ is unsatisfiable.
2. *Closure.* If the call returns none, no clause of $F$ is unit or false under $\tau^*$. A clause can become unit or false only when one of its literals becomes false, so it is in $\mathrm{CANDIDATES}(\neg\ell)$ for that literal's complement $\ell$, which entered $Q$ when it was assigned and was examined after that.
3. *Order independence.* Let $D$ be the set of literals $u$ such that the unit clause $\{u\}$ has a [unit resolution](/unit-resolution/) derivation from $F$ and the unit clauses of $\tau_0$. Then the call returns a conflict exactly when the empty clause has such a derivation, and otherwise $\tau^* = D$. *Proof.* Each literal added at line L7 is derived by resolving its reason with the units of its false literals, and a clause returned at line L5 resolves with the units of its literals to the empty clause; so $\tau^* \subseteq D$, and a conflict means the empty clause is derivable. Conversely, suppose the call returns none. By induction over a unit resolution derivation, every derived clause $E$, obtained from some $C \in F$, has all the literals of $C \setminus E$ false under $\tau^*$, since each removed literal was resolved against a derived unit, which is in $\tau^*$ by the induction. If $E = \{u\}$, then $C$ has all literals except $u$ false under $\tau^*$, and by closure $C$ is not unit or false, so $u$ is true. If $E$ were empty, $C$ would be false under $\tau^*$, against closure. So $D \subseteq \tau^*$ and the empty clause is not derivable. $\blacksquare$

**Cost.** Each variable is assigned at most once in a call, so line L2 runs at most $n$ times. With full occurrence lists and a counter per clause, each assignment touches each clause that holds the complement of the literal once, so the call takes $O(|F|)$ time in total, plus $O(n)$; this is the linear-time Horn-SAT algorithm of Dowling and Gallier. Undoing the counters on backtrack costs the same. With watched literals, nothing is undone on backtrack, and the scans can cost more than $O(|F|)$ in a bad case, but in practice they touch far fewer clauses.

**Example.** Let $F$ have the clauses $C_1 = \{\neg x_1, x_2\}$, $C_2 = \{\neg x_2, x_3\}$, $C_3 = \{\neg x_3, \neg x_1, x_4\}$, $C_4 = \{\neg x_4, x_5, x_6\}$, $C_5 = \{\neg x_2, \neg x_5\}$ and $C_6 = \{\neg x_4, \neg x_6\}$. Decide $x_1$, so $\tau = Q = \{x_1\}$, and use a queue with full occurrence lists.

| step | literal popped | clauses examined (hold its complement) | effect | queue after |
|---|---|---|---|---|
| 1 | $x_1$ | $C_1$, $C_3$ | $C_1$ unit: assign $x_2$; $C_3$ has two open literals | $x_2$ |
| 2 | $x_2$ | $C_2$, $C_5$ | $C_2$ unit: assign $x_3$; $C_5$ unit: assign $\neg x_5$ | $x_3, \neg x_5$ |
| 3 | $x_3$ | $C_3$ | $C_3$ unit: assign $x_4$ | $\neg x_5, x_4$ |
| 4 | $\neg x_5$ | $C_4$ | $C_4$ unit: assign $x_6$ | $x_4, x_6$ |
| 5 | $x_4$ | $C_4$, $C_6$ | $C_4$ satisfied by $x_6$; $C_6 = \{\neg x_4, \neg x_6\}$ false | stop |

The call returns $C_6$. So $F$ implies $\neg x_1$: no model has $x_1$ true. With the decision $\neg x_1$ instead, $C_1$ and $C_3$ are satisfied, nothing is unit, and the call returns none at once.

## Classic examples

- **[DPLL](/dpll/).** The procedure of Davis, Logemann and Loveland runs the unit rule and the [pure literal rule](/pure-literal-elimination/) after each decision. Unit propagation turns a plain [backtracking search](/dpll-backtracking-sat/) into one that prunes a branch as soon as a clause is false.
- **[CDCL](/cdcl/).** Propagation with [two watched literals](/two-watched-literals/) and reasons, so that each conflict can be analyzed in the [implication graph](/implication-graph/) and turned into a [learned clause](/clause-learning/). The Chaff paper reports that propagation takes more than 90 percent of the run time of a solver in most cases.
- **[Horn-SAT](/horn-sat/).** For a Horn formula, unit propagation from the empty assignment decides satisfiability: on no conflict, setting all open variables to false satisfies every clause, because each remaining clause has a negative open literal.
- **[Failed literal probing](/failed-literal-probing/) and [look-ahead](/lookahead-sat/).** Assign a literal $u$, propagate, and if a conflict comes, $\neg u$ is implied; otherwise the number of forced literals measures how good $u$ is as a decision.
- **[DPLL(T)](/dpll-t/).** Theory solvers add their own propagations to the same trail, with explanation clauses as reasons.

## Variations

- **Counter-based propagation.** Each clause keeps the number of its false literals, as in GRASP and in the Horn-SAT algorithm. Every assignment updates every clause with the complement literal, and backtracking undoes it.
- **Head and tail pointers.** SATO kept a pointer at each end of a clause, moving inward past false literals. It is the direct ancestor of watched literals.
- **[Two watched literals](/two-watched-literals/).** Chaff watches two literals that are not false and moves a watch only when it turns false. Backtracking costs nothing.
- **Blocking literals and binary clauses.** Solvers store a literal of the clause next to each watch entry, and skip the clause when that literal is true. Binary clauses keep the other literal in the watch entry and need no clause read.
- **Generalized propagation.** XOR clauses ([XOR-SAT](/xor-sat/) reasoning by Gaussian elimination), cardinality and pseudo-Boolean constraints have unit rules of their own: a constraint forces a literal when every assignment of it that extends $\tau$ makes the literal true.
- **Failed literals and hyper-binary resolution.** Propagation from one probe literal yields new binary clauses implied by $F$, which preprocessors add.

## Pitfalls

- **Checking only for units.** STATUS must also detect a clause whose literals are all false. Missing it lets the search go on below a conflict.
- **Assigning at pop time.** A literal must be assigned when it is pushed (line L7). If it is assigned only when popped, the queue can hold both $u$ and $\neg u$ from two different clauses, and the second is "assigned" over the first.
- **Repeated literals and tautologies.** A clause given as $[x_1, x_1, x_2]$ counts $x_1$ twice: under $\neg x_2$ it has one open literal but a count of two. Remove repeats and drop tautologies before propagation.
- **A queue left full after a conflict.** On a conflict the solver backtracks; the queue must be cleared or reset to the trail position, or stale literals are processed at the wrong level.
- **Deciding before the queue is empty.** Then a literal that a lower level already forced gets the higher level, and conflict analysis on the [implication graph](/implication-graph/) can return a wrong cut.
- **Expecting completeness.** No conflict does not mean satisfiable; unit propagation is complete only for special classes such as Horn and propagation-complete encodings.

## Exercises

1. Prove that unit propagation decides Horn formulas: if it returns none from the empty assignment, the assignment that sets every open variable to false is a model.
2. Give a 2-CNF formula on which unit propagation from the empty assignment does nothing, yet the formula is unsatisfiable. Then show that for 2-CNF, propagation of a single literal $u$ that ends without a conflict satisfies every clause that it touches.
3. Implement the counter version of the template and show that one call costs $O(|F| + n)$ time, including the reset on backtrack.
4. Show by an example that the order of the queue changes which false clause line L5 returns, though not whether one is returned.
5. Show that unit propagation on the [Tseitin](/tseitin-transformation/) encoding of a circuit, with all inputs assigned, assigns every gate variable, so it simulates the evaluation of the circuit.

## References
