---
tag: H3D7MV
kind: algorithm
slug: cdcl
name: Conflict-driven clause learning
aliases:
- CDCL
- CDCL solver
- conflict-driven clause learning solver
area: logic-and-constraints/sat-solving
level: advanced
summary: Decide SAT by search with unit propagation. Each conflict gives a new clause implied by F, and the search jumps back to where that clause is unit. The base of modern SAT solvers.
solves: [sat]
model: word-ram
complexity:
  vars: {n: the number of variables, m: "the number of clauses, input and learned"}
  time: {worst: 2^Ω(n)}
  space: {extra: O(n m)}
properties: {deterministic: true, exact: true, online: false, recursive: false, in_place: false}
history:
  year: 1996
  people: [João P. Marques-Silva, Karem A. Sakallah]
  note: GRASP added conflict analysis, clause learning and non-chronological backtracking to DPLL. Chaff (Moskewicz et al., 2001) added two watched literals and VSIDS, and MiniSat (Eén and Sörensson, 2003) fixed the design that most solvers still follow.
prereqs: [dpll, clause-learning, non-chronological-backtracking, two-watched-literals]
see_also: [first-uip, implication-graph, vsids, restarts, clause-database, cdcl-simulates-resolution, drat-proof, dpll-t]
sources:
  - paper: doi:10.1109/12.769433
    title: João P. Marques-Silva and Karem A. Sakallah, GRASP, a search algorithm for propositional satisfiability, IEEE Transactions on Computers 48(5), 1999
    locator: pages 506 to 521 (the search procedure, conflict analysis on the implication graph, and non-chronological backtracking)
  - paper: doi:10.1145/378239.379017
    title: Matthew W. Moskewicz, Conor F. Madigan, Ying Zhao, Lintao Zhang and Sharad Malik, Chaff, engineering an efficient SAT solver, Proceedings of the 38th Design Automation Conference, 2001
    locator: pages 530 to 535 (two watched literals, VSIDS and the measured comparison with GRASP and SATO)
  - paper: "Lintao Zhang, Conor F. Madigan, Matthew W. Moskewicz and Sharad Malik, Efficient conflict driven learning in a Boolean satisfiability solver, Proceedings of ICCAD 2001, pages 279 to 285"
    locator: the comparison of learning schemes, where first UIP learning was best
  - paper: doi:10.1007/978-3-540-24605-3_37
    title: Niklas Eén and Niklas Sörensson, An extensible SAT-solver, SAT 2003, Lecture Notes in Computer Science 2919, 2004
    locator: pages 502 to 518 (the MiniSat design, the propagation loop, conflict analysis and the activity heap)
  - paper: doi:10.1145/1217856.1217859
    title: Robert Nieuwenhuis, Albert Oliveras and Cesare Tinelli, Solving SAT and SAT modulo theories, from an abstract Davis-Putnam-Logemann-Loveland procedure to DPLL(T), Journal of the ACM 53(6), 2006
    locator: pages 937 to 977 (the abstract transition system, its soundness and the termination argument by a lexicographic order on the trail)
  - book: isbn:9781643681603
    title: Armin Biere, Marijn Heule, Hans van Maaren and Toby Walsh (eds.), Handbook of Satisfiability, second edition, IOS Press, 2021
    locator: Chapter 4, Conflict-Driven Clause Learning SAT Solvers, by Marques-Silva, Lynce and Malik, pages 133 to 182
  - book: isbn:9780201038064
    title: Donald E. Knuth, The Art of Computer Programming, Volume 4B, Combinatorial Algorithms Part 2, 2022
    locator: Section 7.2.2.2, Satisfiability (Algorithm C, satisfiability by clause learning)
  - book: isbn:9783662504963
    title: Daniel Kroening and Ofer Strichman, Decision Procedures, An Algorithmic Point of View, second edition, 2016
    locator: Chapter 2, Section 2.2 (the CDCL framework, conflict analysis and its termination)
  - paper: "Knot Pipatsrisawat and Adnan Darwiche, On the power of clause-learning SAT solvers as resolution engines, Artificial Intelligence 175(2), 2011, pages 512 to 525"
    locator: the main theorem, that CDCL with restarts and a suitable decision strategy p-simulates general resolution
  - paper: doi:10.1016/0304-3975(85)90144-6
    title: Armin Haken, The intractability of resolution, Theoretical Computer Science 39, 1985
    locator: pages 297 to 308 (exponential lower bound for resolution refutations of the pigeonhole formulas)
  - paper: doi:10.1145/48014.48016
    title: Vašek Chvátal and Endre Szemerédi, Many hard examples for resolution, Journal of the ACM 35(4), 1988
    locator: pages 759 to 768 (random k-CNF formulas with cn clauses need exponential resolution refutations, with high probability)
  - paper: "Alasdair Urquhart, Hard examples for resolution, Journal of the ACM 34(1), 1987, pages 209 to 219"
    locator: the exponential lower bound for the Tseitin formulas of expander graphs
---

Conflict-driven clause learning (CDCL) is the search algorithm for [SAT](/sat/) that is the base of almost every modern SAT solver. It extends [DPLL](/dpll/): when [unit propagation](/unit-propagation/) makes a clause false, it analyzes the conflict into a new clause that follows from the formula, adds that clause, and jumps back to the level where the new clause becomes unit. Its worst case is exponential in the number of variables, as for every known SAT algorithm, but on large formulas from hardware and software verification it is often fast.

## In plain words

The solver guesses a value for one variable at a time. After each guess it follows every forced step: when a clause has only one way left to be true, that way is forced. Sometimes the forced steps make a clause false. DPLL would then undo the last guess and try the other value.

CDCL asks why the clash happened. It follows the forced steps back to a small set of earlier choices that together cause the clash. It writes down a new clause that says "never make these choices together", and keeps it for the rest of the search. Then it undoes all the guesses that played no part in the clash, which can be many at once. The new clause forces a different value at once, so the solver never meets the same clash again.

## The problem

The input is a formula $F$ in [conjunctive normal form](/conjunctive-normal-form/) over the variables $x_1, \ldots, x_n$. A [clause](/clause/) is a set of [literals](/literal/), $m$ is the number of clauses, $k$ is the largest clause width, and $|F|$ is the total number of literal occurrences. The output is SAT with an assignment that makes every clause true, or UNSAT. This is the [SAT problem](/sat/), which is [NP-complete](/np-complete/) ([Cook-Levin theorem](/cook-levin-theorem/)).

## The algorithm

The solver keeps a *trail* $M$: the assigned literals in the order of assignment. Each literal has a *decision level*, the number of decisions made at or before its assignment. A literal is a *decision*, or it is *implied* by a *reason* clause in which all other literals are false. These links form the [implication graph](/implication-graph/). The database holds the input clauses and the set $\Delta$ of learned clauses.

```pseudo id=main
CDCL(F)                                    ▷ F over x1 .. xn
L1  if F has the empty clause or two opposite unit clauses then return UNSAT
L2  M ← the empty trail, Δ ← ∅, dl ← 0
L3  loop
L4      K ← PROPAGATE()                    ▷ two watched literals; K is a false clause or NONE
L5      if K ≠ NONE then
L6          if dl = 0 then return UNSAT
L7          (C, b) ← ANALYZE(K)            ▷ first UIP clause C, b = second highest level in C
L8          BACKJUMP(b), dl ← b
L9          Δ ← Δ ∪ {C}, assign the asserting literal of C with reason C
L10         decay the variable activities (VSIDS)
L11     else if every variable has a value then return SAT and M
L12     else if a restart is due then BACKJUMP(0), dl ← 0
        else
L13         if a reduction is due then delete about half of the unlocked learned clauses
L14         ℓ ← the free variable of highest activity, with its saved phase
L15         dl ← dl + 1, assign ℓ as the decision of level dl
```

The parts are separate pages, and each one is a technique of its own.

- PROPAGATE is [unit propagation](/unit-propagation/) with [two watched literals](/two-watched-literals/). It stops at the first false clause.
- ANALYZE is [clause learning](/clause-learning/). It resolves the false clause with reason clauses, newest literal first, until one literal of the current level is left: the [first UIP](/first-uip/). Then it removes redundant literals by [clause minimization](/clause-minimization/) and computes the [literal block distance](/literal-block-distance/) of the clause.
- BACKJUMP($b$) removes all literals of levels above $b$. This is [non-chronological backtracking](/non-chronological-backtracking/). Each removed variable keeps its last value for [phase saving](/phase-saving/).
- Line L10 and the bump in ANALYZE are [VSIDS](/vsids/). Lines L12 and L13 are the [restart](/restarts/) policy and [clause database reduction](/clause-database-reduction/). The storage of clauses and watch lists is the [clause database](/clause-database/).

This page covers the whole loop and how the parts fit. The [clause learning](/clause-learning/) page covers only the step that turns one conflict into one clause, which is also used outside SAT, for example as [nogood learning](/nogood-learning/) in constraint solvers.

## Example

The formula has 9 variables and these 6 clauses:

$$C_1 = \{x_1, x_2\},\ C_2 = \{x_1, x_3, x_7\},\ C_3 = \{\neg x_2, \neg x_3, x_4\},\ C_4 = \{\neg x_4, x_5, x_8\},\ C_5 = \{\neg x_4, x_6, x_9\},\ C_6 = \{\neg x_5, \neg x_6\}.$$

Let the decisions be $\neg x_7$, $\neg x_8$, $\neg x_9$ and $\neg x_1$, at levels 1 to 4. The first three force nothing. The fourth starts a chain.

| trail position | literal | level | reason |
|---|---|---|---|
| 1 | $\neg x_7$ | 1 | decision |
| 2 | $\neg x_8$ | 2 | decision |
| 3 | $\neg x_9$ | 3 | decision |
| 4 | $\neg x_1$ | 4 | decision |
| 5 | $x_2$ | 4 | $C_1$ |
| 6 | $x_3$ | 4 | $C_2$ |
| 7 | $x_4$ | 4 | $C_3$ |
| 8 | $x_5$ | 4 | $C_4$ |
| 9 | $x_6$ | 4 | $C_5$ |

Now $C_6 = \{\neg x_5, \neg x_6\}$ is false. ANALYZE resolves it with the reason of the newest literal $x_6$, which gives $\{\neg x_5, \neg x_4, x_9\}$. Two literals of level 4 are left, so it resolves with the reason of $x_5$ and gets $\{\neg x_4, x_8, x_9\}$. Only $\neg x_4$ has level 4, so $x_4$ is the first UIP. The learned clause is $\{\neg x_4, x_8, x_9\}$, its other levels are 2 and 3, so $b = 3$, and its LBD is 3.

BACKJUMP(3) removes the level-4 literals, and line L9 assigns $\neg x_4$ at level 3. Say the solver decides $\neg x_1$ again at level 4. Then $C_1$ and $C_2$ force $x_2$ and $x_3$, and $C_3 = \{\neg x_2, \neg x_3, x_4\}$ is false. ANALYZE resolves $C_3$ with $C_2$ and then with $C_1$ and learns $\{x_1, x_4, x_7\}$, with backjump level 3. After BACKJUMP(3), $x_1$ is assigned at level 3. Any values of $x_2, x_3, x_5, x_6$ that keep $C_3$ and $C_6$ true now give a model, for example $x_1$ true and all other variables false. The first learned clause keeps $x_4$ false, so the second conflict came from $C_3$ and not from $C_6$.

## Correctness

The proof keeps two invariants. Every learned clause is true in every model of $F$, because ANALYZE builds it by [resolution](/binary-resolution/) from clauses of the database. Every literal at level 0 is true in every model of $F$, because its reason has all other literals at level 0. So a conflict at level 0 shows that $F$ has no model. A SAT answer comes only after propagation finds no false clause and every variable has a value, so the trail is a model.

ANALYZE stops with exactly one literal of the conflict level, because each step replaces the newest literal of that level with older ones, and the decision of the level is the oldest. So after the backjump, the learned clause is unit, and it was not in the database before: at the end of the propagation before the last decision it was already unit, and complete propagation would have used it.

For termination, compare trails by the vector of level sizes $(|M_0|, |M_1|, \ldots)$ in lexicographic order. Propagation, decisions and backjump with assertion each make this vector strictly larger, and the vectors form a finite set. So CDCL terminates when the restart intervals grow without bound, as with Luby restarts, or when learned clauses are never deleted, because then each conflict adds a new clause and there are at most $3^n$ clauses. The full proof is below.

## Complexity

**Proved bounds.** No bound better than $2^n$ times a polynomial is known for CDCL. Without clause deletion, each conflict learns a new clause, so a run has at most $3^n$ conflicts. Each UNSAT run gives a [resolution](/binary-resolution/) refutation of $F$ whose size is polynomial in the number of conflicts and $n$, because each learned clause comes with a resolution derivation of $O(n)$ steps. So the lower bounds for resolution are lower bounds for CDCL:

- [Haken](/haken-resolution-lower-bound/) (1985) proved that every resolution refutation of the pigeonhole formula with $h + 1$ pigeons and $h$ holes has size $2^{\Omega(h)}$, on $n = h(h+1)$ variables.
- Chvátal and Szemerédi (1988) proved that a random 3-CNF formula with $cn$ clauses, for a large enough constant $c$, has no resolution refutation of size $2^{o(n)}$ with high probability. Urquhart (1987) proved a $2^{\Omega(n)}$ bound for the Tseitin formulas of expander graphs.

So CDCL takes time $2^{\Omega(n)}$ on these UNSAT formulas, with every decision and restart policy. In the other direction, CDCL with restarts and a suitable decision order can simulate general resolution with a polynomial overhead ([CDCL simulates resolution](/cdcl-simulates-resolution/)), so CDCL is as strong as resolution as a proof system.

**Cost of one step.** With two watched literals, assigning a literal visits only the clauses that watch its negation. ANALYZE takes time linear in the size of the reasons it visits, at most the total size of the database. A backjump to level $b$ takes time linear in the number of removed literals. The memory is $O(n + |F|)$ for the input plus the learned clauses, and a learned clause has at most $n$ literals, so the extra space is $O(nm)$ when $m$ counts the clauses that are kept.

**Measured behaviour.** Moskewicz et al. (2001) report that Chaff was one to two orders of magnitude faster than GRASP and SATO on hard instances from electronic design automation. Zhang et al. (2001) compared learning schemes and found first UIP learning the most robust on their benchmarks. These are the authors' measured results on their sets of instances, not proved bounds.

## Properties

- **Complete and sound.** CDCL answers SAT only with a model, and UNSAT only when no model exists. It is a [decision procedure](/decision-procedure/) for SAT, under the termination hypotheses above.
- **Deterministic.** The implementation breaks ties in a fixed way. Many solvers add some random decisions, and then the run is random but still sound.
- **Iterative.** The search is a loop over an explicit trail, not a recursion.
- **Proof producing.** Each learned clause is a resolution consequence, so a solver can log its clauses as a [DRAT proof](/drat-proof/) or an [LRAT proof](/lrat-proof/) that a separate checker verifies.
- **Incremental.** The learned clauses stay valid when more clauses are added to $F$, which [incremental SAT](/incremental-sat/) uses.

## Variants and improvements

- **Preprocessing and inprocessing.** [Bounded variable elimination](/bounded-variable-elimination/), [blocked clause elimination](/blocked-clause-elimination/), [failed literal probing](/failed-literal-probing/) and [subsumption](/clause-subsumption/) shrink the formula before and during the search.
- **Lookahead and cube and conquer.** [Lookahead solvers](/lookahead-sat/) spend more time on each decision. [Cube and conquer](/cube-and-conquer/) splits the formula with lookahead and solves the parts with CDCL.
- **Parallel solving.** A [portfolio](/parallel-portfolio-sat/) runs several CDCL solvers with different settings and shares short learned clauses.
- **SMT.** [DPLL(T)](/dpll-t/) runs CDCL on the Boolean structure of a formula and asks a theory solver for conflicts, which become learned clauses.
- **Other learning schemes.** GRASP learned clauses at several UIPs, and early solvers used the decision scheme, which keeps only decision literals. First UIP is now the standard.

## When to use it

Use CDCL for large structured formulas, such as the formulas from [bounded model checking](/sat-based-bounded-model-checking/), equivalence checking of circuits, [planning](/satplan/), scheduling and cryptanalysis. Use it when an UNSAT answer matters, because it can give a checkable proof. On random formulas near the threshold, [local search](/walksat/) often finds models faster, but it cannot prove UNSAT. For 2-CNF and Horn formulas, use the linear-time [2-SAT algorithm](/two-sat-algorithm/) or [Horn-SAT](/horn-sat/).

## Pitfalls

- **Deleting a reason.** A learned clause that is the reason of a literal on the trail is *locked*. Deleting it breaks ANALYZE, which needs every reason.
- **The wrong backjump level.** The backjump level is the second highest level in the learned clause, not the conflict level minus one. With the wrong level the clause is not unit, or the solver keeps useless decisions.
- **Watches of a new clause.** Watch the asserting literal and a literal of the highest remaining level. Other choices can break the watch invariant after a later backjump.
- **Restarts with deletion.** The termination proof needs unbounded restart intervals or no deletion. A solver with glucose-style restarts and aggressive deletion has no proof of termination.
- **Learning with level-0 literals.** Remove literals of level 0 from a learned clause. They are false forever, and they only make the clause longer.

## Implementations

## History

Davis, Logemann and Loveland gave the backtracking procedure in 1962. Marques-Silva and Sakallah added conflict analysis, clause learning and non-chronological backtracking in GRASP (1996, journal version 1999), and Bayardo and Schrag added learning to relsat in 1997. Chaff (Moskewicz, Madigan, Zhao, Zhang and Malik, 2001) introduced two watched literals and VSIDS, and Zhang et al. (2001) showed the value of first UIP learning. MiniSat (Eén and Sörensson, 2003) gave a short and clear design. Later work added phase saving (2007), Luby restarts in SAT (Huang 2007), learned clause minimization (MiniSat 1.13, 2005) and LBD (Glucose, 2009). Knuth calls the method Algorithm C in Volume 4B.

## References
