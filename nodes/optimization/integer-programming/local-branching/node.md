---
tag: VXSHYR
kind: technique
slug: local-branching
name: Local branching
aliases:
- local branching heuristic
- soft variable fixing
area: optimization/integer-programming
level: research
summary: Primal heuristic that restricts the search to a neighborhood of the incumbent defined by a Hamming-distance constraint.
prereqs: [binary-integer-programming, incumbent-solution, hamming-distance, land-doig-algorithm]
see_also: [relaxation-induced-neighborhood-search, feasibility-pump, diving-heuristic, large-neighborhood-search, variable-neighborhood-search, hamming-distance, incumbent-solution, branch-and-cut]
sources:
  - paper: doi:10.1007/s10107-003-0395-5
    title: Matteo Fischetti and Andrea Lodi, Local branching, Mathematical Programming 98(1 to 3), 2003
    locator: pp. 23 to 47; the local branching constraint, the exact scheme with left and right branches, the node time limit, intensification and diversification, and the comparison with CPLEX 7.0
  - paper: doi:10.1007/s10107-004-0518-7
    title: E. Danna, E. Rothberg and C. Le Pape, Exploring relaxation induced neighborhoods to improve MIP solutions, Mathematical Programming 102(1), 2005
    locator: pp. 71 to 90 (computational comparison of RINS, guided dives and local branching)
  - paper: "Timo Berthold, Primal heuristics for mixed integer programs, Diploma thesis, Technische Universität Berlin, 2006"
    locator: the chapter on large neighborhood search heuristics (local branching as a sub-MIP heuristic in SCIP; chapter number unsure)
---

Local branching is a primal heuristic for [mixed integer programs](/mixed-integer-programming/) with [binary variables](/binary-integer-programming/). Given an [incumbent](/incumbent-solution/) $\bar{x}$, it adds the linear constraint that at most $k$ binary variables differ from $\bar{x}$, solves this smaller problem with an ordinary MIP solver, and repeats from each better point it finds. The reversed constraint, at least $k + 1$ differences, covers the rest of the space, so the method is also a branching scheme that can be run to optimality. Fischetti and Lodi introduced it in 2003.

## In plain words

Suppose a good solution is already known. Better solutions are often close to it: they change only a few of the yes or no decisions. Local branching adds one rule to the model, "change at most $k$ decisions", and lets the solver search this small region. The region is small, so the solver often searches it fast.

If the solver finds a better solution, the region is moved to that solution and the search repeats. The part already searched is excluded by the opposite rule, "change more than $k$ decisions". If the region holds nothing better, the method either searches the rest of the problem in the normal way or makes the region larger.

## When it applies

- A mixed integer program in which the binary variables carry the main decisions, and a feasible point $\bar{x}$ is known, for example from a [diving heuristic](/diving-heuristic/) or the [feasibility pump](/feasibility-pump/).
- A MIP solver is available as a black box for the subproblems, with a time or node limit.
- The best solutions differ from good ones in a moderate number of binary variables. The method looks only at binary variables; general integer and continuous variables stay free in every subproblem.

## The template

Let $B$ be the set of binary variables. For a binary point $\bar{x}$, the *local branching constraint* uses the linear function
$$\Delta(x, \bar{x}) = \sum_{j \in B,\ \bar{x}_j = 1} (1 - x_j) + \sum_{j \in B,\ \bar{x}_j = 0} x_j .$$
For a binary $x$, each term is 1 exactly when $x_j \neq \bar{x}_j$, so $\Delta(x, \bar{x})$ is the [Hamming distance](/hamming-distance/) between $x$ and $\bar{x}$ on $B$. The holes are $k$ (the radius), SOLVE (the subsolver and its limit) and ON-FAIL (what to do when a left problem holds no better point). The problem $P$ is a maximization and $R$ is the set of right branch constraints added so far.

```pseudo id=main
LOCAL-BRANCHING(P, x̄)
L1  R ← ∅
L2  loop until the total limit is reached
L3      y, status ← SOLVE(P with R and Δ(x, x̄) ≤ k)          ▷ the left branch
L4      if y is better than x̄ then
L5          if status = solved then add Δ(x, x̄) ≥ k + 1 to R  ▷ the right branch
L6          else add Δ(x, x̄) ≥ 1 to R                          ▷ only x̄ is excluded
L7          x̄ ← y
L8      else if status = solved then                            ▷ no better point within k
L9          add Δ(x, x̄) ≥ k + 1 to R;  apply ON-FAIL
L10     else k ← ⌈k/2⌉                                          ▷ limit hit, nothing found
L11 return x̄
```

ON-FAIL has two common forms. In the *exact* form, solve $P$ with $R$ by ordinary [branch and bound](/land-doig-algorithm/), keep the better of its answer and $\bar{x}$, and stop. In the *heuristic* form, enlarge the radius, for example $k \leftarrow k + \lceil k/2 \rceil$, and continue; Fischetti and Lodi call this diversification. Line L10, which shrinks the radius when the limit stops a subproblem with no gain, is their intensification step.

**What is proved.** For binary $x$, $\Delta(x, \bar{x})$ is an integer, so every binary point satisfies exactly one of $\Delta(x, \bar{x}) \le k$ and $\Delta(x, \bar{x}) \ge k + 1$. Line L5 adds a right constraint only after the left problem has been solved to optimality, and line L6 removes only the point $\bar{x}$, which is no better than the incumbent. So the constraints in $R$ never remove a point better than the incumbent. Every $y$ that SOLVE returns satisfies all rows of $P$, so every incumbent is feasible. In the exact form, each pass through line L7 strictly raises the incumbent value, the binary part takes finitely many values, and so after finitely many steps no improvement is found. Then the final branch and bound on $P$ with $R$ searches every point not yet excluded, and the result is optimal. The left problem has at most $\sum_{i=0}^{k} \binom{|B|}{i}$ binary points.

**What is not proved.** The heuristic form with limits and diversification returns a feasible point but gives no bound on its quality. The claim that small radii, such as $k$ between 10 and 20, work well is a measured result.

**Example.** Take
$$\max\ 11x_1 + 15x_2 + 15x_3 + 4x_4 + 8x_5 + 10x_6$$
subject to
$$2x_1 + 3x_2 + 5x_3 + 2x_4 + 2x_5 + 2x_6 \le 18, \qquad 3x_1 + 4x_2 + 7x_3 + 7x_4 + 3x_5 + 3x_6 \le 15,$$
$x \in \{0, 1\}^6$, with $k = 2$, exact subproblems and the exact ON-FAIL. Each left problem has at most $1 + 6 + 15 = 22$ binary points.

| step | incumbent $\bar{x}$ | value | left branch $\Delta(x, \bar{x}) \le 2$ with $R$ |
|---|---|---|---|
| 1 | $(0, 0, 0, 1, 1, 1)$ | 22 | best point $(0, 0, 1, 0, 1, 1)$, value 33 |
| 2 | $(0, 0, 1, 0, 1, 1)$ | 33 | best point $(0, 1, 1, 0, 0, 1)$, value 40 |
| 3 | $(0, 1, 1, 0, 0, 1)$ | 40 | best point $(1, 1, 1, 0, 0, 0)$, value 41 |
| 4 | $(1, 1, 1, 0, 0, 0)$ | 41 | no better point |

After step 4, $R$ holds four right constraints, and only 8 of the 39 feasible binary points satisfy all of them. Branch and bound on these 8 points finds $(1, 1, 0, 0, 1, 1)$ with value 44, which is the optimum. This point differs from the last incumbent in three variables, so the left branches with $k = 2$ alone could not reach it. The heuristic form would have enlarged the radius to $k = 3$ instead.

## Classic examples

- **The original study.** Fischetti and Lodi ran local branching with CPLEX 7.0 as the subsolver and compared it with CPLEX 7.0 alone, with the same time limit, on hard instances from MIPLIB and other sources. They report that local branching found better solutions on most of their instances. This is a measured result for one solver version and one test set.
- **Comparison with RINS.** Danna, Rothberg and Le Pape compared [RINS](/relaxation-induced-neighborhood-search/), guided dives and local branching inside CPLEX. On their set of hard models, RINS gave better solutions than local branching on several measures. This is also a measured result.
- **Sub-MIP heuristic in SCIP.** SCIP contains local branching as one of its large neighborhood search heuristics, which add the constraint to a copy of the problem and solve the copy with a node limit, as described by Berthold.

## Variations

- **Asymmetric constraint.** If every feasible point has the same number of ones, as with assignment constraints, then $\Delta(x, \bar{x})$ is twice the first sum alone. The constraint $\sum_{\bar{x}_j = 1} (1 - x_j) \le k'$ is then enough and has fewer terms.
- **General integer variables.** Write the distance with auxiliary variables $d_j \ge x_j - \bar{x}_j$ and $d_j \ge \bar{x}_j - x_j$, and bound $\sum_j d_j$.
- **Local branching as a [large neighborhood search](/large-neighborhood-search/).** Drop the right constraints and use the left problem as one neighborhood among several. With a sequence of radii, this is a form of [variable neighborhood search](/variable-neighborhood-search/).
- **Repairing infeasible points.** Start from an infeasible $\bar{x}$, add slack variables to the violated rows, and minimize the total slack in the neighborhood. Fischetti and Lodi later used this idea to find first feasible points.

## Pitfalls

- **Radius too small or too large.** A small $k$ gives an easy subproblem that seldom holds a better point. A large $k$ gives a subproblem almost as hard as the full one.
- **Wrong right constraint after a limit.** If a left problem was stopped by its limit, it has not been searched fully. Adding $\Delta(x, \bar{x}) \ge k + 1$ then removes points that were never examined, and the exact form is no longer exact. Use $\Delta(x, \bar{x}) \ge 1$ instead, as in line L6.
- **Weak LP bounds.** The constraint $\Delta(x, \bar{x}) \le k$ often does not raise the LP bound much, so the subsolver may still need a large tree.
- **Many right constraints.** Each right constraint is a dense row. After many steps, the LP of the final branch and bound becomes larger and slower.
- **Only binary variables.** The basic constraint ignores general integer and continuous variables. If they carry the main decisions, the neighborhood is not small.

## Exercises

1. Show that for binary $x$ the function $\Delta(x, \bar{x})$ equals the Hamming distance between $x$ and $\bar{x}$, and that it can take fractional values at fractional $x$.
2. In the example, check the four rows of the table and list the 8 points that remain for the final branch and bound.
3. Repeat the example with $k = 3$. How many left problems are solved before the optimum is found?
4. Prove that $\Delta(x, \bar{x}) \le k$ and $\sum_{\bar{x}_j = 1} (1 - x_j) \le k/2$ define the same binary points when every feasible point has exactly $m$ ones.
5. Give an instance where adding $\Delta(x, \bar{x}) \ge k + 1$ after a left problem that hit its limit removes the only optimal solution.

## References
