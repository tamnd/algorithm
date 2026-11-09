---
tag: MH6AZP
kind: problem
slug: maxsmt
name: MaxSMT
aliases:
- weighted MaxSMT
- partial weighted MaxSMT
- maximum satisfiability modulo theories
area: logic-and-constraints/smt
level: advanced
summary: Satisfy all hard constraints while maximizing the total weight of satisfied soft constraints.
prereqs: [smt-problem, max-sat, weighted-max-sat]
see_also: [optimization-modulo-theories, partial-max-sat, core-guided-maxsat, unsat-core, incremental-solving, linear-integer-arithmetic-satisfiability, pseudo-boolean-sat, optimization-to-decision-reduction]
sources:
  - paper: doi:10.1007/11814948_18
    title: Robert Nieuwenhuis and Albert Oliveras, On SAT modulo theories and optimization problems, Theory and Applications of Satisfiability Testing (SAT 2006), Lecture Notes in Computer Science 4121, Springer, 2006
    locator: MaxSMT and optimization in DPLL(T) by branch and bound with theory strengthening
  - paper: "Alessandro Cimatti, Anders Franzén, Alberto Griggio, Roberto Sebastiani and Cristian Stenico, Satisfiability modulo the theory of costs, foundations and applications, Tools and Algorithms for the Construction and Analysis of Systems (TACAS 2010), Lecture Notes in Computer Science 6015, Springer, 2010"
    locator: MaxSMT through a theory of costs inside the SMT solver
  - paper: doi:10.1007/978-3-662-46681-0_14
    title: Nikolaj Bjørner, Anh-Dung Phan and Lars Fleckenstein, νZ, an optimizing SMT solver, Tools and Algorithms for the Construction and Analysis of Systems (TACAS 2015), Lecture Notes in Computer Science 9035, Springer, 2015
    locator: the MaxSMT engines of Z3 (core-guided MaxRes and others) and their combination with OMT objectives
  - book: isbn:9781643681603
    title: Biere, Heule, van Maaren and Walsh (eds.), Handbook of Satisfiability, second edition, IOS Press, 2021
    locator: Chapter 24, MaxSAT (Bacchus, Järvisalo and Martins), for the linear search, core-guided and implicit hitting set methods; Chapter 33 for SMT
  - paper: "Mark W. Krentel, The complexity of optimization problems, Journal of Computer and System Sciences 36(3) (1988)"
    locator: weighted MaxSAT is complete for FP^NP (to be checked)
---

MaxSMT is the optimization version of [SMT](/smt-problem/): given *hard* constraints, which must hold, and *soft* constraints with positive weights, which may be violated at a cost, find a model of the hard constraints whose violated soft constraints have the least total weight. The constraints are formulas in a theory such as [linear integer arithmetic](/linear-integer-arithmetic-satisfiability/), so MaxSMT extends [weighted MaxSAT](/weighted-max-sat/) from propositional clauses to theory formulas. It is a special case of [optimization modulo theories](/optimization-modulo-theories/), where the objective is a weighted count of satisfied formulas instead of an arithmetic term.

## In plain words

Some rules must be kept. Other rules are wishes, and each wish has a price that must be paid if it is not met. The rules and wishes talk about numbers or other data, not only true and false. The task is to keep all rules and pay as little as possible for broken wishes.

A solver can first find any answer, note its price, and then ask for an answer that is strictly cheaper, until no cheaper answer exists. Better methods look at small groups of wishes that cannot all be met together, and decide which wish in each group to give up.

## Definition

**Input.** A hard formula $H$ and soft formulas $S_1, \ldots, S_m$ with weights $w_1, \ldots, w_m > 0$, all in a theory $T$ (for example QF_LIA or QF_BV).

**Output.** A model $M$ of $H$ in $T$ that minimizes the cost
$$\mathrm{cost}(M) = \sum_{i : M \not\models S_i} w_i,$$
or the answer that $H$ is unsatisfiable. Equivalently, $M$ maximizes the total weight of the satisfied soft formulas.

**Names.** With all weights equal, the problem is *unweighted*; with $H$ empty, it is not *partial*. *Partial weighted* MaxSMT is the general form above.

**How MaxSMT and OMT differ.** MaxSMT has one objective of a fixed shape: a weighted sum of indicators of soft formulas. [OMT](/optimization-modulo-theories/) minimizes or maximizes an arbitrary term of the theory, such as $3x - y$ over the reals, and supports several objectives. Each MaxSMT instance is an OMT instance with the objective $\sum_i w_i \cdot \mathrm{ite}(S_i, 0, 1)$; the special shape is what lets MaxSMT use the [core-guided](/core-guided-maxsat/) methods of MaxSAT.

## Variants

- **Unweighted and weighted.** Equal weights versus arbitrary positive weights.
- **Lexicographic MaxSMT.** Several groups of soft formulas, optimized one group after the other.
- **MaxSAT.** The theory is propositional logic, and soft formulas are clauses: [weighted MaxSAT](/weighted-max-sat/) and [partial MaxSAT](/partial-max-sat/).
- **Minimal correction sets and maximal satisfiable subsets.** Enumerate the minimal sets of soft formulas whose removal makes the rest satisfiable with $H$, without a weight.
- **OMT.** The objective is a theory term (see the comparison above).

## Examples

Let $x$ and $y$ be integers with the hard constraints $0 \le x \le 5$, $0 \le y \le 5$ and $x + y \le 6$. The soft constraints are $x \ge 4$ (weight 3), $y \ge 4$ (weight 2), $x \le y$ (weight 2) and $x + y = 5$ (weight 1). A script checked all 36 points.

- The minimal sets of soft constraints that conflict with $H$ are $\{x \ge 4, y \ge 4\}$, since $x + y \ge 8 > 6$, and $\{x \ge 4, x \le y\}$, since then $y \ge 4$ too.
- So each model violates $x \ge 4$, or violates both $y \ge 4$ and $x \le y$. The cheapest choice is to give up $x \ge 4$, with cost 3; the models of cost 3 are $(x, y) = (0, 5)$ and $(1, 4)$.

A linear search, which asks each time for a model with a cost below the last one, runs as follows when the solver returns models in some fixed order:

| step | query | model | violated soft constraints | cost |
|---|---|---|---|---|
| 1 | $H$ | $(0, 0)$ | $x \ge 4$, $y \ge 4$, $x + y = 5$ | 6 |
| 2 | $H \wedge \mathrm{cost} < 6$ | $(1, 5)$ | $x \ge 4$, $x + y = 5$ | 4 |
| 3 | $H \wedge \mathrm{cost} < 4$ | $(0, 5)$ | $x \ge 4$ | 3 |
| 4 | $H \wedge \mathrm{cost} < 3$ | none | | optimum is 3 |

## Known algorithms

| method | idea | notes |
|---|---|---|
| linear search (SAT to UNSAT) | find a model, then add $\mathrm{cost} < c$ and repeat | simple; each step is one incremental SMT call |
| binary search on the cost | ask for $\mathrm{cost} \le k$ for a middle value $k$ | $O(\log \sum_i w_i)$ calls |
| branch and bound in DPLL(T) (Nieuwenhuis and Oliveras 2006) | prune a partial assignment when its cost already reaches the best found | the cost bound is a theory constraint that propagates |
| theory of costs (Cimatti et al. 2010) | a dedicated theory solver for the cost sum, combined with the other theories | strong for many soft constraints |
| [core-guided](/core-guided-maxsat/) (Fu-Malik, MaxRes, OLL) | ask for all soft constraints; from the [unsat core](/unsat-core/), relax one member with a cardinality constraint, and repeat | works from the lower bound up; the default in Z3 (Bjørner et al. 2015) |
| implicit hitting sets | collect cores, compute a minimum-weight hitting set with an integer program, and test it | strong when cores are few and weights are diverse |
| [Boolean abstraction](/boolean-abstraction/) to MaxSAT | replace each soft formula by an indicator literal, and keep the theory in the SMT solver | the usual way to reuse MaxSAT algorithms |

In the example, the two cores both contain $x \ge 4$; a minimum-weight hitting set of the cores is $\{x \ge 4\}$ (weight 3), which is cheaper than $\{y \ge 4, x \le y\}$ (weight 4), and it gives the optimum.

## Bounds

**Theorem (linear search).** Let the weights be positive integers with sum $W$, and let the theory solver decide $H \wedge \mathrm{cost} < c$ for each $c$. If $H$ is satisfiable, the linear search stops after at most $W + 1$ solver calls, and the last model it found has minimum cost.

*Proof.* Each model found has a cost strictly below the previous one, since the query requires it, and costs are integers in $[0, W]$; so at most $W + 1$ models are found before a query is unsatisfiable. When the query $H \wedge \mathrm{cost} < c$ is unsatisfiable, with $c$ the cost of the last model $M$, no model of $H$ has a cost below $c$, so $M$ is optimal. $\square$

The constraint $\mathrm{cost} < c$ is a [pseudo-Boolean](/pseudo-boolean-sat/) constraint over the indicators $b_i \leftrightarrow S_i$, or a linear integer constraint when the theory has integers.

**Complexity.** If the satisfiability of $T$ formulas is in NP, then the decision version, "is there a model of $H$ with cost at most $k$?", is in NP: guess the model and check it. It is NP-hard already for propositional logic, since $k = 0$ asks whether $H$ together with all $S_i$ is satisfiable. Computing the optimum of weighted MaxSAT is complete for the class of functions computable in polynomial time with an NP oracle (Krentel 1988), and the same holds for MaxSMT over such theories; binary search on the cost gives the upper bound with $O(\log W)$ oracle calls plus the calls to recover the model.

## Reductions

- **To SMT with a bound.** By the [reduction from optimization to decision](/optimization-to-decision-reduction/): the indicators $b_i \leftrightarrow S_i$ and a linear constraint on $\sum_i w_i (1 - b_i)$.
- **To OMT.** Minimize the objective $\sum_i w_i \cdot \mathrm{ite}(S_i, 0, 1)$.
- **From MaxSAT.** MaxSAT is MaxSMT over propositional logic.
- **To MaxSAT, for theories that can be bit-blasted.** With [bit-blasting](/bit-blasting/), QF_BV MaxSMT becomes weighted partial MaxSAT.

## Applications

- Localizing faults in programs: the hard constraints are the test and the specification, each program statement is a soft constraint, and a minimum set of violated statements points to the likely bug.
- Scheduling and configuration with numeric constraints and preferences.
- Repairing inconsistent specifications or network configurations with the least change.
- Choosing a most likely explanation in diagnosis, where weights are negative log-probabilities.

## References
