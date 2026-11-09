---
tag: 75TMKH
kind: problem
slug: maximum-csp
name: Maximum constraint satisfaction problem
aliases:
- MAX-CSP
- weighted CSP
- Max-CSP
- partial constraint satisfaction
area: logic-and-constraints/constraint-satisfaction
level: advanced
summary: Find an assignment that satisfies the largest number of constraints, or the largest total weight. It is NP-hard even for two values and binary constraints, and exact solvers use branch and bound.
prereqs: [constraint-satisfaction-problem, depth-first-branch-and-bound, np-hard]
see_also: [soft-constraints, max-sat, weighted-max-sat, max-2-sat, forward-checking, bucket-elimination, min-conflicts, bounding-function]
sources:
  - paper: doi:10.1016/0004-3702(92)90004-H
    title: Eugene C. Freuder and Richard J. Wallace, Partial constraint satisfaction, Artificial Intelligence 58(1-3), 1992
    locator: pages 21 to 70 (partial constraint satisfaction, Max-CSP, branch and bound with partial forward checking and its lower bound)
  - paper: "Thomas Schiex, Hélène Fargier and Gérard Verfaillie, Valued constraint satisfaction problems, hard and easy problems, Proceedings of IJCAI-95, 1995, pages 631 to 637"
    locator: the valued CSP framework, with Max-CSP and weighted CSP as instances
  - book: isbn:9780444527264
    title: Francesca Rossi, Peter van Beek and Toby Walsh (eds.), Handbook of Constraint Programming, Elsevier, 2006
    locator: Chapter 9, Soft constraints, by Pedro Meseguer, Francesca Rossi and Thomas Schiex (weighted CSP, branch and bound, soft local consistency)
  - paper: "Javier Larrosa, Pedro Meseguer and Thomas Schiex, Maintaining reversible DAC for Max-CSP, Artificial Intelligence 107(1), 1999, pages 149 to 163"
    locator: lower bounds from directed arc consistency counts in branch and bound
  - paper: "Nadia Creignou, A dichotomy theorem for maximum generalized satisfiability problems, Journal of Computer and System Sciences 51(3), 1995, pages 511 to 522"
    locator: Boolean Max-CSP over a fixed constraint language is either polynomial or NP-hard
  - paper: "Prasad Raghavendra, Optimal algorithms and inapproximability results for every CSP?, Proceedings of STOC 2008, pages 245 to 254"
    locator: under the Unique Games Conjecture, a semidefinite program gives the best approximation ratio for every Max-CSP
---

The maximum constraint satisfaction problem (Max-CSP) takes a [constraint satisfaction problem](/constraint-satisfaction-problem/) that may have no solution, and asks for an assignment that satisfies as many constraints as possible. In the weighted form, each constraint has a weight, and the goal is the largest total weight of satisfied constraints. This is the same as the smallest total weight of violated constraints. Freuder and Wallace (1992) studied it as *partial constraint satisfaction* and gave branch and bound with a lower bound from forward checking. Max-CSP is NP-hard even with two values and binary constraints, since it contains [Max-2-SAT](/max-2-sat/) and Max-Cut. Max-CSP is one problem. [Soft constraints](/soft-constraints/) is the general framework, with the semiring and valued CSP models, and it treats Max-CSP and weighted CSP as special cases.

## In plain words

Sometimes the rules contradict each other, so no answer meets them all. Then a useful answer breaks as few rules as possible, or breaks only rules that do not matter much. Give each rule a weight that says how bad it is to break it. The task is to find the answer whose broken rules have the smallest total weight.

Checking a single answer is easy. Finding the best one is hard in general, because it includes the question of whether all rules can be met at once, and that question is already hard.

## Definition

An instance has variables $x_1, \ldots, x_n$ with finite domains $D(x_i)$ of size at most $d$, and constraints $C_1, \ldots, C_m$, each with a scope and a relation. In the weighted form each $C_t$ has a weight $w_t > 0$. For a complete assignment $\sigma$, its *cost* is

$$\text{cost}(\sigma) = \sum_{t \,:\, \sigma \text{ violates } C_t} w_t .$$

- **Max-CSP.** All $w_t = 1$. Find $\sigma$ with the smallest cost, that is, with the largest number of satisfied constraints.
- **Weighted Max-CSP.** Find $\sigma$ with the smallest cost for the given weights.
- **Decision form.** Given $K$, is there a $\sigma$ with $\text{cost}(\sigma) \le K$?

The CSP is the special case "is the smallest cost 0?". Some authors use "weighted CSP" (WCSP) for the more general model where each constraint is a cost function that gives a cost to each tuple. That model belongs to [soft constraints](/soft-constraints/).

## Variants

- **Max-k-CSP over a domain of size d.** Every constraint has at most $k$ variables. Max-2-CSP is the binary case.
- **Fixed constraint languages.** Max-CSP($\Gamma$) allows only relations from a set $\Gamma$. Max-SAT, Max-Cut and Max-2-SAT are examples.
- **Hard and soft constraints.** Some constraints must hold and the others have weights. This matches [partial Max-SAT](/partial-max-sat/).
- **Min-CSP.** Minimize the number of satisfied constraints. Its approximability is different.
- **Max-CSP with a target.** Decide whether at least $m - K$ constraints can hold, for a parameter $K$, which is studied in parameterized complexity.

## Examples

**A triangle with two colors.** Variables $x_0, x_1, x_2$ with domain $\{0, 1\}$ and the three constraints $x_0 \neq x_1$, $x_0 \neq x_2$, $x_1 \neq x_2$. The CSP has no solution, since two of three variables share a value. The optimum cost is 1. With weights 3, 2 and 1 for the three constraints, the optimum gives up the lightest one, $x_1 \neq x_2$: the assignment $(0, 1, 1)$ has cost 1.

**Branch and bound on the weighted triangle.** Assign $x_0, x_1, x_2$ in order and values in the order 0, 1. Let $g$ be the cost of the violated constraints among the assigned variables. Let $\text{ic}(x_j, b)$ be the weight of the constraints between $x_j$ and the assigned variables that $x_j = b$ would violate. The lower bound is $g + \sum_{j \text{ unassigned}} \min_b \text{ic}(x_j, b)$. The upper bound UB is the cost of the best complete assignment found so far.

| node | $g$ | ic of unassigned variables | lower bound | UB | action |
|---|---|---|---|---|---|
| $x_0 = 0$ | 0 | $x_1$: (3, 0), $x_2$: (2, 0) | 0 | none | go down |
| $x_1 = 0$ | 3 | $x_2$: (3, 0) | 3 | none | go down |
| $x_2 = 0$, $x_2 = 1$ | 6, 3 | | | | leaves, UB becomes 3 |
| $x_1 = 1$ | 0 | $x_2$: (2, 1) | 1 | 3 | go down |
| $x_2 = 0$, $x_2 = 1$ | 2, 1 | | | | leaves, UB becomes 1 with $(0, 1, 1)$ |
| $x_0 = 1$ | 0 | $x_1$: (0, 3), $x_2$: (0, 2) | 0 | 1 | go down |
| $x_1 = 0$ | 0 | $x_2$: (1, 2) | 1 | 1 | prune |
| $x_1 = 1$ | 3 | | 3 | 1 | prune |

The search tries 10 value assignments. With the bound $g$ alone, it must also try $x_2 = 0$ and $x_2 = 1$ under $x_0 = 1, x_1 = 0$, which gives 12.

**Over-constrained queens.** Put $n$ queens in $n$ columns of a board with $n - 1$ rows, with one constraint for each pair of queens. For $n = 5, 6, 7, 8$ the smallest number of attacking pairs is 2, 1, 1 and 1. The implementation reaches the optimum after 148, 280, 900 and 2625 value assignments with the forward-checking bound, against 304, 460, 1818 and 5404 with $g$ alone.

## Known algorithms

| method | type | time | notes |
|---|---|---|---|
| [depth-first branch and bound](/depth-first-branch-and-bound/) with partial forward checking (Freuder and Wallace 1992) | exact | $O(d^n \cdot m)$ worst case | the bound in the example |
| branch and bound with directed arc consistency counts (Wallace 1995; Larrosa, Meseguer and Schiex 1999) | exact | exponential | adds a bound from the constraints among the unassigned variables |
| Russian doll search (Verfaillie, Lemaître and Schiex 1996) | exact | exponential | solves the problems on the last $1, 2, \ldots, n$ variables and uses their optima as bounds |
| soft arc consistency in branch and bound | exact | exponential | moves costs between constraints to raise the bound; see [soft constraints](/soft-constraints/) |
| [bucket elimination](/bucket-elimination/) | exact | $O(m \, d^{w + 1})$ | $w$ is the induced width of the order |
| random assignment | approximation | $O(n + m)$ | satisfies an expected fraction at least $1 / d^k$ of the optimum for Max-k-CSP |
| semidefinite programming (Goemans and Williamson 1995 for Max-Cut; Raghavendra 2008) | approximation | polynomial | the best ratio for every Max-CSP if the Unique Games Conjecture holds |
| [min-conflicts](/min-conflicts/), [tabu search](/tabu-search/) | heuristic | per step | keep the best assignment seen; no guarantee |

**Why the forward-checking bound is valid.** At a node, a constraint among assigned variables is counted in $g$. A constraint between an assigned variable and an unassigned $x_j$ is counted at most once, in $\text{ic}(x_j, \cdot)$. A constraint among unassigned variables is not counted. For any completion $\sigma$ of the node, $\sigma$ pays $g$, and for each unassigned $x_j$ it pays at least $\text{ic}(x_j, \sigma(x_j)) \ge \min_b \text{ic}(x_j, b)$, and these sets of constraints do not overlap. So the bound is at most the cost of every completion, and pruning when it reaches UB never loses a strictly better assignment. The tests check the optimum against brute force over all $d^n$ assignments, and they check that this bound never visits more nodes than $g$ alone.

## Bounds

- **NP-hardness.** Max-CSP is NP-hard with domain size 2 and binary constraints. The constraint $x \neq y$ on $\{0, 1\}$ makes Max-CSP into Max-Cut, which is NP-hard (Karp 1972). Each 2-clause is a binary constraint, so [Max-2-SAT](/max-2-sat/) is also a special case, and it is NP-hard (Garey, Johnson and Stockmeyer 1976). The decision form is in NP, since the cost of a given assignment is easy to check, so it is [NP-complete](/np-complete/).
- **Approximation.** A uniform random assignment satisfies each satisfiable constraint of arity $k$ with probability at least $1 / d^k$. So its expected value is at least $1 / d^k$ of the optimum, and the method of conditional expectations makes this deterministic. Max-Cut and Max-2-SAT are APX-hard, so they have no polynomial-time approximation scheme unless P = NP.
- **Dichotomies.** For Boolean domains, Creignou (1995) showed that Max-CSP($\Gamma$) is either polynomial or NP-hard for every fixed $\Gamma$. Thapper and Živný (2013) showed that every finite-valued CSP is solved by its basic linear programming relaxation or is NP-hard.
- **Exact time.** Brute force takes $O(d^n m)$ time. Bucket elimination takes time exponential only in the induced width, so it is polynomial on bounded [treewidth](/treewidth/).

## Reductions

- **From CSP.** A CSP has a solution if and only if its Max-CSP optimum is 0.
- **From and to Max-SAT.** [Max-SAT](/max-sat/) is Boolean Max-CSP with clause constraints. A weighted Max-CSP over finite domains maps to [weighted Max-SAT](/weighted-max-sat/): encode each value with a Boolean variable, make the encoding constraints hard, and give each forbidden tuple of a constraint a clause with the weight of that constraint.
- **To soft constraints.** Weighted Max-CSP is a valued CSP over the valuation structure $(\mathbb{N} \cup \{\infty\}, +, \le)$. See [soft constraints](/soft-constraints/).
- **To integer programming.** Use a 0/1 variable for each (variable, value) pair and a 0/1 variable for each violated constraint. This is a [mixed integer program](/mixed-integer-programming/).

## Applications

- Over-constrained scheduling and timetabling, where some wishes must be given up.
- The frequency assignment benchmarks (CELAR), where interference constraints have weights.
- The selection of satellite photographs (the SPOT5 benchmarks), where requests have values.
- Diagnosis: the smallest set of violated constraints points to the faulty parts.

## References
