---
tag: 6HZ5A8
kind: algorithm
slug: relaxation-induced-neighborhood-search
name: Relaxation induced neighborhood search
aliases:
- RINS
- relaxation induced neighbourhood search
area: optimization/integer-programming
level: research
summary: Primal heuristic that fixes variables agreeing between the LP relaxation and the incumbent, then solves the remaining subproblem.
solves: [mixed-integer-programming]
model: real-ram
complexity:
  vars: {M: the node limit of the sub-search, L: the time of one linear program solve, n: the number of variables}
  time: {worst: O((M + 1) L)}
  space: {extra: O(M^2 + n)}
properties: {deterministic: true, recursive: false}
prereqs: [mixed-integer-programming, lp-relaxation, incumbent-solution, land-doig-algorithm]
see_also: [local-branching, feasibility-pump, diving-heuristic, large-neighborhood-search, branch-and-cut, depth-first-branch-and-bound]
sources:
  - paper: doi:10.1007/s10107-004-0518-7
    title: E. Danna, E. Rothberg and C. Le Pape, Exploring relaxation induced neighborhoods to improve MIP solutions, Mathematical Programming 102(1), 2005
    locator: pp. 71 to 90
  - paper: doi:10.1007/s10107-003-0395-5
    title: M. Fischetti and A. Lodi, Local branching, Mathematical Programming 98(1), 2003
    locator: pp. 23 to 47
  - paper: "T. Berthold, Primal heuristics for mixed integer programs, Diploma thesis, Technische Universität Berlin, 2006"
    locator: chapter on large neighborhood search heuristics (RINS and related methods)
---

Relaxation induced neighborhood search (RINS) is a primal heuristic for [mixed integer programs](/mixed-integer-programming/). It compares the [incumbent](/incumbent-solution/), the best feasible point known, with an optimal solution of the [LP relaxation](/lp-relaxation/), fixes every integer variable on which the two agree, and solves the smaller program that remains with a limited [branch and bound](/land-doig-algorithm/) search. Danna, Rothberg and Le Pape introduced it in 2005. The result is never worse than the incumbent, but it need not be optimal.

## In plain words

A solver that searches for the best solution usually holds two pieces of information. One is the best real solution found so far. The other is the solution of an easier problem in which whole-number variables may take fractional values. That second solution is often not usable, but it points in a good direction.

Where the two agree on a variable, that value is probably right, so RINS fixes it. The remaining variables form a much smaller problem. RINS solves that small problem with a short search and a limit on the work. If it finds a better solution, it replaces the old one. The fixing makes the search fast, but it can also cut away the best solution.

## The problem

The input is a mixed integer program

$$\min\ c^\top x \quad \text{subject to} \quad A x \le b,\quad x \ge 0,\quad x_j \in \mathbb{Z}\ (j \in I),$$

with rational data, a feasible point $\bar{x}$ (the incumbent) and a node limit $M$. This page assumes that the LP relaxation $P = \{x \ge 0 : A x \le b\}$ is bounded, so that each linear program of the method has an optimum. The output is a feasible point $x$ with $c^\top x \le c^\top \bar{x}$.

## The algorithm

```pseudo id=main
RINS(c, A, b, I, x̄, M)
L1  x* ← an optimal solution of the LP relaxation (at the current node of the main search)
L2  F ← {j ∈ I : x̄ⱼ = x*ⱼ}
L3  Q ← the program with the added constraints xⱼ = x̄ⱼ for all j ∈ F
L4  best ← x̄;  S ← a stack that holds the root node of Q;  count ← 0
L5  while S ≠ ∅ and count < M do
L6      pop a node from S;  count ← count + 1;  solve its LP relaxation, with solution x and value v
L7      if the LP is infeasible or v ≥ cᵀbest then continue
L8      if xⱼ is integer for all j ∈ I then best ← x;  continue
L9      choose j ∈ I with xⱼ fractional;  push the nodes with xⱼ ≥ ⌈xⱼ⌉ and with xⱼ ≤ ⌊xⱼ⌋
L10 return best
```

Lines L1 to L3 build the *neighborhood*: the set of feasible points that agree with the incumbent on $F$. Lines L4 to L9 are a [depth-first branch and bound](/depth-first-branch-and-bound/) on $Q$, with the [fathoming rules](/fathoming-rule/) of line L7 and a [branching rule](/branching-rule/) that takes the first fractional variable at line L9. The node of the second push is popped first. The incumbent is the start value of `best`, so line L7 prunes every node that cannot give a strictly better point.

## Example

A [knapsack problem](/knapsack-problem/) with weights $(6, 2, 5, 7, 3)$, profits $(6, 8, 3, 7, 4)$ and capacity 14, written as a minimum of the negated profit. The incumbent $\bar{x} = (1, 1, 1, 0, 0)$ has profit 17. The LP relaxation has the optimum $x^* = (1, 1, 0, 3/7, 1)$ with profit 21. The two agree only on $x_1 = x_2 = 1$, so $F = \{1, 2\}$, and $Q$ has capacity $14 - 6 - 2 = 6$ for items 3, 4 and 5.

| node | constraints added in $Q$ | LP profit | action |
|---|---|---|---|
| 1 | none | 21 | branch on $x_4 = 3/7$ |
| 2 | $x_4 \le 0$ | 99/5 | branch on $x_3 = 3/5$ |
| 3 | $x_4 \le 0$, $x_3 \le 0$ | 18 | integer: new best $(1, 1, 0, 0, 1)$ |
| 4 | $x_4 \le 0$, $x_3 \ge 1$ | 55/3 | branch on $x_5 = 1/3$ |
| 5 | $x_4 \le 0$, $x_3 \ge 1$, $x_5 \le 0$ | 17 | pruned: $17 \le 18$ |
| 6 | $x_4 \le 0$, $x_3 \ge 1$, $x_5 \ge 1$ | none | infeasible |
| 7 | $x_4 \ge 1$ | none | infeasible |

RINS returns $(1, 1, 0, 0, 1)$ with profit 18, after 7 nodes. This is the best point of the neighborhood. The optimum of the whole problem is $(0, 1, 0, 1, 1)$ with profit 19. It has $x_1 = 0$, so it lies outside the neighborhood: the incumbent and the LP solution agreed on a value that the optimum does not have.

## Correctness

**Theorem.** Assume $P$ is bounded and $\bar{x}$ is feasible. RINS stops after at most $M + 1$ linear programs. It returns a feasible point $x$ with $c^\top x \le c^\top \bar{x}$. If the loop ends because $S$ is empty, the returned point is an optimal solution of $Q$.

The full proof is below. Each point stored in `best` is $\bar{x}$ or an integer optimal solution of a node LP, so it is feasible, and line L7 only accepts strictly better values. For the optimality claim, the incumbent $\bar{x}$ lies in $Q$ because it meets the fixings, and the depth-first search keeps the usual invariant of branch and bound: each point of $Q$ with a value below $c^\top \mathrm{best}$ lies in some node on the stack. RINS gives no guarantee about the optimum of the original program, as the example shows.

## Complexity

Line L1 is one linear program, and each node of the loop is one more, so there are at most $M + 1$ linear programs, and the time is $O((M + 1) L)$ in the worst case. The other work at a node is $O(n)$ for the integer test and is part of $O(L)$. In depth-first order the stack has at most $M + 1$ entries, and each entry holds at most one bound change for each level of the tree, so the extra space is $O(M^2 + n)$ when the bound changes are stored as (index, value) pairs. The depth of the tree is at most $M$.

The method is useful because $|I \setminus F|$ is often much smaller than $|I|$. A full search of $Q$ can still take time exponential in $|I \setminus F|$, which is why the node limit $M$ is part of the method.

## Properties

- **Never worse.** The returned point is at least as good as the incumbent.
- **Exact on the neighborhood, heuristic overall.** A complete sub-search solves $Q$ exactly, but the fixings can remove every optimal solution of the original program.
- **Needs an incumbent.** RINS improves a point; it does not find a first one. The [feasibility pump](/feasibility-pump/) or a [dive](/diving-heuristic/) can supply that point.
- **Adaptive neighborhood.** The neighborhood depends on the LP solution of the current node, so RINS at different nodes of the main tree searches different neighborhoods.

## Variants and improvements

- **Call frequency.** Danna, Rothberg and Le Pape call RINS at nodes of the main [branch and cut](/branch-and-cut/) tree at a fixed frequency, with a node limit for each sub-search, because each call is a small branch and bound.
- **Minimum fixing rate.** Implementations skip the sub-search when too few variables are fixed, because then $Q$ is almost as hard as the original program. The RINS of SCIP has a parameter for this rate.
- **Local branching.** [Local branching](/local-branching/) of Fischetti and Lodi defines the neighborhood by a bound on the number of binary variables that differ from the incumbent, instead of fixing variables.
- **Guided dives.** The same paper of Danna, Rothberg and Le Pape also introduces guided dives, which choose the child of a node by the incumbent value of the branching variable.
- **Large neighborhood search.** RINS is an instance of [large neighborhood search](/large-neighborhood-search/), where an exact solver explores a neighborhood that is too big to list.

## When to use it

Use RINS inside a [branch and cut](/branch-and-cut/) solver once an incumbent exists and the gap between the incumbent and the bound is still large. It works well when the LP solution and the incumbent agree on most variables, which is common in models with many binary variables. CPLEX, Gurobi and SCIP all include a RINS heuristic. Danna, Rothberg and Le Pape report that, on a set of hard models, RINS and guided dives give better solutions than default CPLEX and than local branching on several measures. That is a computational result on their test set, not a proof.

## Pitfalls

- **Too few fixings.** If the LP solution and the incumbent agree on few variables, the sub-MIP is nearly as large as the original program, and the node limit stops the search before it improves anything.
- **Equality test in floating point.** Real solvers compare $\bar{x}_j$ and $x^*_j$ with a tolerance. Too large a tolerance fixes variables that disagree.
- **No cutoff.** Without the cutoff of line L7 the sub-search spends nodes on points that are not better than the incumbent.
- **Reading the result as an optimum.** A complete sub-search gives the optimum of $Q$ only; the example has a better point outside $Q$.

## Implementations

The Python code uses an exact two-phase simplex in `fractions.Fraction` with [Bland's rule](/bland-rule/), and a depth-first branch and bound with a node limit for the sub-MIP. The tests check that the returned point is feasible and never worse than the incumbent, on random instances in a box with random feasible incumbents. With no node limit they check that the value equals the optimum of $Q$ from brute force over the box. They do not check that RINS finds the optimum of the original program.

## History

Danna, Rothberg and Le Pape, at ILOG, published RINS and guided dives in 2005, and compared them with the local branching of Fischetti and Lodi from 2003. Berthold described the RINS implementation of SCIP in his 2006 thesis.

## References
