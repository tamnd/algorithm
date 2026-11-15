---
tag: Z8JAJ3
kind: problem
slug: disjunctive-temporal-problem
name: Disjunctive temporal problem
aliases:
- DTP
area: information-retrieval-and-ai-reasoning/qualitative-temporal-and-spatial-reasoning
level: research
summary: Time points with constraints that are disjunctions of difference inequalities, possibly on different pairs of points. Consistency is NP-complete and is solved by search over STPs.
prereqs: [simple-temporal-problem, difference-constraints, temporal-constraint-satisfaction-problem]
see_also: [difference-logic-satisfiability, smt-problem, lazy-smt, conflict-directed-backjumping, forward-checking, nogood-learning, job-shop-scheduling, temporal-planning]
sources:
  - paper: "Kostas Stergiou and Manolis Koubarakis, Backtracking algorithms for disjunctions of temporal constraints, Artificial Intelligence 120(1), 2000"
    locator: pages 81 to 117 (the DTP, the meta-CSP of disjunct choices, and backtracking, backjumping and forward checking for it)
  - paper: doi:10.1016/S0004-3702(03)00113-9
    title: Ioannis Tsamardinos and Martha E. Pollack, Efficient solution techniques for disjunctive temporal reasoning problems, Artificial Intelligence 151(1-2), 2003
    locator: pages 43 to 89 (the solver Epilitis, with forward checking, conflict-directed backjumping, removal of subsumed variables, semantic branching and no-good recording)
  - paper: doi:10.1016/0004-3702(91)90006-6
    title: Rina Dechter, Itay Meiri and Judea Pearl, Temporal constraint networks, Artificial Intelligence 49(1-3), 1991
    locator: pages 61 to 95 (the STP and the TCSP, the special cases of the DTP)
---

The disjunctive temporal problem (DTP) asks whether time points can be placed so that each constraint holds, where a constraint is a disjunction of difference inequalities $X - Y \le b$, and the disjuncts of one constraint may be on different pairs of points. A [simple temporal problem](/simple-temporal-problem/) is a conjunction of such inequalities, which is a system of [difference constraints](/difference-constraints/) and is solved by shortest paths; the DTP adds disjunction, and consistency becomes NP-complete. It also generalizes the [temporal constraint satisfaction problem](/temporal-constraint-satisfaction-problem/), whose disjuncts are always on the same pair. Stergiou and Koubarakis (2000) named the problem and gave the first search methods for it.

## In plain words

Two jobs need the same machine. Either the first ends before the second starts, or the second ends before the first starts. Each half of this "either, or" compares a different pair of moments, so it is not a rule about one gap.

A DTP is a list of such rules. If you choose one half of every rule, all your choices together are simple gap rules, and a shortest path method tells you at once whether they fit. Solvers search over the choices, test each partial set of choices this way, and learn from the failures which choices do not go together.

## Definition

A DTP has real variables $X_1, \ldots, X_n$ and constraints $C_1, \ldots, C_c$. Each constraint is a disjunction

$$C_k = (X_{i_1} - X_{j_1} \le b_1) \lor \cdots \lor (X_{i_m} - X_{j_m} \le b_m)$$

of *difference atoms*. A *solution* assigns reals that make at least one atom of every constraint true. A *selection* picks one atom from each constraint; the picked atoms form an STP, called a *component STP*. The DTP is consistent if and only if some component STP is consistent, since a solution makes some atom of each constraint true and so solves the STP of those atoms. Write $k$ for the largest number of atoms in a constraint.

The *meta-CSP* view of Stergiou and Koubarakis takes one variable for each constraint $C_k$, whose domain is the set of atoms of $C_k$, and a consistency test that holds when the chosen atoms form a consistent STP.

## Variants

- **Simple temporal problem.** Every constraint has one atom. Consistency is polynomial.
- **TCSP.** Every disjunct of a constraint is a bound on the same difference $X_j - X_i$. The [TCSP](/temporal-constraint-satisfaction-problem/) is a DTP after each interval $[a, b]$ is written as two atoms and the disjunction of conjunctions is put in clause form.
- **Difference logic.** Arbitrary Boolean combinations of difference atoms, with Boolean variables as well; see [difference logic satisfiability](/difference-logic-satisfiability/). A DTP is a difference logic formula in conjunctive normal form with no Boolean variables.
- **Integer DTP.** With integer bounds, a consistent DTP has an integer solution, because each component STP with integer data does.
- **DTP with uncertainty.** Some durations are set by nature, as in a [simple temporal network with uncertainty](/simple-temporal-network-with-uncertainty/), and the question becomes one of controllability.

## Examples

**Two jobs on one machine.** Job $A$ runs from $s_A$ to $e_A$ with $e_A - s_A = 3$, job $B$ from $s_B$ to $e_B$ with $e_B - s_B = 2$. They cannot overlap:

$$(e_A - s_B \le 0) \lor (e_B - s_A \le 0).$$

The two atoms are on the pairs $(e_A, s_B)$ and $(e_B, s_A)$, so this is a DTP constraint but not a TCSP constraint. Add a start point $Z$ with $s_A - Z \ge 0$, $s_B - Z \ge 0$ and a deadline $e_A - Z \le D$, $e_B - Z \le D$. With $D = 5$ the first atom gives the solution $s_A = 0$, $e_A = 3$, $s_B = 3$, $e_B = 5$. With $D = 4$ both component STPs have a negative cycle. For the first atom, the cycle $Z \to e_B \to s_B \to e_A \to s_A \to Z$ has weight $4 - 2 + 0 - 3 + 0 = -1$, and the second is symmetric. So the DTP is inconsistent.

**Many selections.** A DTP with $c$ constraints of $k$ atoms each has $k^c$ selections. Solvers avoid most of them: when a partial selection already gives a negative cycle, every selection that extends it fails, and the atoms on the cycle form a no-good.

## Known algorithms

| method | output | worst-case time | notes |
| --- | --- | --- | --- |
| backtracking over the meta-CSP (Stergiou and Koubarakis, 2000) | consistency and one solution | $O(n m \, k^c)$ for $m$ atoms in the STP | each node tests the partial STP with [Bellman-Ford](/bellman-ford/) or an incremental update |
| [forward checking](/forward-checking/) on the meta-CSP (Stergiou and Koubarakis, 2000) | the same | exponential | removes the atoms that conflict with the current STP from the other constraints |
| Epilitis (Tsamardinos and Pollack, 2003) | the same | exponential | forward checking, [conflict-directed backjumping](/conflict-directed-backjumping/), removal of subsumed variables, semantic branching and [no-good learning](/nogood-learning/) |
| [lazy SMT](/lazy-smt/) with a difference logic theory solver | the same | exponential | a SAT solver picks the atoms, a negative-cycle check explains each conflict |

Semantic branching, in the sense of Tsamardinos and Pollack, adds the negation of an atom to the STP when the search backtracks over it. The negation of $X - Y \le b$ is $Y - X < -b$, which is again a difference constraint. Removal of subsumed variables drops a constraint as soon as the current STP already implies one of its atoms.

## Bounds

**NP-completeness (Turing model, rational bounds in binary).** DTP consistency is NP-complete. It is in NP: a selection is a certificate, and its component STP is checked for a negative cycle in polynomial time. It is NP-hard because the TCSP is a special case, and TCSP consistency is NP-hard (Dechter, Meiri and Pearl, 1991); a direct reduction from [3-SAT](/3-sat/) also works, with a time point $X_v$ and the constraints $0 \le X_v - Z \le 1$ for each Boolean variable, and for each clause the disjunction of the atoms $Z - X_v \le -1$ for a positive literal $v$ and $X_v - Z \le 0$ for a negative one.

**Upper bound (word-RAM).** Backtracking over the selections takes $O(k^c)$ nodes, each with an STP check of $O(n m)$ time with Bellman-Ford, or less with incremental updates. No algorithm with a better exponential base in general is given in the sources here.

**Polynomial case.** If every constraint has one atom, the problem is an STP and is decided in $O(n m)$ time.

## Reductions

- **To component STPs.** The DTP is consistent if and only if one component STP is. Every exact solver searches this space.
- **From the TCSP.** Each TCSP constraint becomes a set of clauses of difference atoms on one pair.
- **From 3-SAT.** In the reduction above, $X_v - Z \in [0, 1]$ and the clause atoms force $X_v - Z = 1$ for a true positive literal and $X_v - Z = 0$ for a true negative literal, so a solution gives a satisfying assignment by reading $X_v - Z \ge 1$ as true, and every satisfying assignment gives a solution with $X_v - Z \in \{0, 1\}$.
- **To SMT.** A DTP is a formula of [difference logic](/difference-logic-satisfiability/) in conjunctive normal form, an instance of the [SMT problem](/smt-problem/).
- **From scheduling.** [Job shop scheduling](/job-shop-scheduling/) with a makespan bound is a DTP: precedence inside each job gives difference constraints, and each pair of operations on the same machine gives one disjunctive constraint as in the example.

## Applications

- Scheduling with resources that can serve one task at a time, as in the example.
- [Temporal planning](/temporal-planning/) and plan merging, where the order of actions from different plans is a disjunction.
- Plan execution systems that keep a DTP and commit to atoms while the plan runs, as in the work of Tsamardinos and Pollack.

## References
