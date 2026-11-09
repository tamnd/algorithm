---
tag: P8QYS3
kind: algorithm
slug: min-conflicts
name: Min-conflicts
aliases:
- min-conflicts heuristic
- min-conflicts local search
- min-conflicts hill climbing
area: logic-and-constraints/constraint-satisfaction
level: core
summary: Local search for a CSP that starts from a complete assignment and repeatedly gives a conflicted variable the value with the fewest conflicts. Fast on large loose problems, but incomplete.
solves: [constraint-satisfaction-problem]
model: word-ram
complexity:
  vars: {n: the number of variables, d: the largest domain size, s: the number of steps}
  time: {worst: O(s n d)}
  space: {extra: O(n)}
properties: {deterministic: false, exact: false, online: false, recursive: false, in_place: true}
history:
  year: 1990
  people: [Steven Minton, Mark D. Johnston, Andrew B. Philips, Philip Laird]
  note: Minton, Johnston, Philips and Laird presented the heuristic at AAAI-90 and in Artificial Intelligence in 1992. It came from the analysis of a neural network that Johnston and Adorf used to schedule observations for the Hubble Space Telescope.
prereqs: [constraint-satisfaction-problem, local-search, hill-climbing]
see_also: [walksat, gsat, tabu-search, simulated-annealing, stochastic-local-search, n-queens-problem, local-optimum, maximum-csp]
sources:
  - paper: doi:10.1016/0004-3702(92)90007-K
    title: Steven Minton, Mark D. Johnston, Andrew B. Philips and Philip Laird, Minimizing conflicts, a heuristic repair method for constraint satisfaction and scheduling problems, Artificial Intelligence 58(1-3), 1992
    locator: pages 161 to 205 (the heuristic, the n-queens experiments, the analysis of why it works, and the Hubble Space Telescope scheduling application)
  - paper: "Steven Minton, Mark D. Johnston, Andrew B. Philips and Philip Laird, Solving large-scale constraint satisfaction and scheduling problems using a heuristic repair method, Proceedings of AAAI-90, 1990, pages 17 to 24"
    locator: the first report of the method and of the million-queens result
  - book: isbn:9780134610993
    title: Stuart Russell and Peter Norvig, Artificial Intelligence, A Modern Approach, 4th edition, Pearson, 2020
    locator: Chapter 6, Constraint satisfaction problems, local search for CSPs (the MIN-CONFLICTS procedure)
  - book: isbn:9780444527264
    title: Francesca Rossi, Peter van Beek and Toby Walsh (eds.), Handbook of Constraint Programming, Elsevier, 2006
    locator: Chapter 5, Local search methods, by Holger H. Hoos and Edward Tsang (min-conflicts and its variants)
---

Min-conflicts is a [local search](/local-search/) method for [constraint satisfaction problems](/constraint-satisfaction-problem/). It starts from a complete assignment, which usually violates some constraints. At each step it picks a variable that is in a violated constraint and gives it a value that violates the fewest constraints, given the current values of the other variables. It stops when no constraint is violated or after a fixed number of steps. Minton, Johnston, Philips and Laird (1990, 1992) showed that on [n-queens](/n-queens-problem/) the number of repairs it needs stays about the same as $n$ grows, and solved the million-queens problem in less than four minutes. Min-conflicts is incomplete: it can run forever on a problem that has a solution, and it can never prove that there is none.

## In plain words

Instead of building a solution one variable at a time, start with every variable already set, even if many rules are broken. Then repair. Pick one variable that breaks a rule, try all its values, and keep the one that breaks the fewest rules, given where everything else is now. Repeat until no rule is broken.

On many large puzzles this finds a solution after a small number of repairs. But it can also get stuck: every single change may make things worse or keep them the same, while a solution needs several changes at once. Then it goes round in circles. So a failure to find a solution does not prove that none exists.

## The problem

The input is a [constraint satisfaction problem](/constraint-satisfaction-problem/) with variables $x_1, \ldots, x_n$, finite domains $D(x_i)$ and constraints, and a limit $s$ on the number of steps. For a complete assignment $\sigma$, let $\text{conflicts}(x, v, \sigma)$ be the number of constraints on $x$ that are violated when $x$ takes the value $v$ and every other variable keeps its value in $\sigma$. A variable $x$ is *conflicted* if $\text{conflicts}(x, \sigma(x), \sigma) > 0$. The output is a solution, or "failure" after $s$ steps. Failure does not mean that no solution exists.

Notation: $n$ variables, $d$ the largest domain size, $s$ the step limit.

## The algorithm

```pseudo id=main
MIN-CONFLICTS(x_1, ..., x_n, D, C, s)
L1  σ ← a complete assignment (random, or built greedily)
L2  for step ← 1 to s do
L3      if no variable is conflicted then return σ
L4      x ← a conflicted variable, chosen at random
L5      v ← a value of x with the smallest conflicts(x, v, σ), ties broken at random
L6      σ(x) ← v
L7  return failure
```

This is the form in Russell and Norvig. Line L5 may keep the current value of $x$ if no value is better. Random choices at lines L4 and L5 are important: with fixed choices the search falls into short cycles more often. Minton and colleagues also used a greedy start for line L1, which places the variables one by one, each at a value with the fewest conflicts with the variables already placed.

The implementation keeps, for each variable, the number of violated constraints on it, and the list of conflicted variables. When $x$ changes, only the counts of $x$ and of its neighbours change.

## Example

Take 4-queens, with $x_i$ the row of the queen in column $i$, and start from $\sigma = (1, 2, 3, 4)$, all queens on one diagonal. Every variable is conflicted. The rows of the table give, for the chosen variable, the number of conflicts of each row value.

| step | $\sigma$ before | chosen variable | conflicts for rows 1, 2, 3, 4 | new value |
|---|---|---|---|---|
| 1 | $(1, 2, 3, 4)$ | $x_1$ | 3, 1, 2, 1 | 2 (tie with 4) |
| 2 | $(2, 2, 3, 4)$ | $x_3$ | 1, 2, 2, 2 | 1 |
| 3 | $(2, 2, 1, 4)$ | $x_2$ | 2, 3, 1, 1 | 4 (tie with 3) |
| 4 | $(2, 4, 1, 4)$ | $x_4$ | 1, 3, 0, 1 | 3 |
| | $(2, 4, 1, 3)$ | | | solution |

This run is one of the shortest. With random choices, the implementation needs between 3 and 44 steps from the start $(1, 1, 1, 1)$ on the seeds 0 to 5.

**A case where it is stuck.** Take $a, b, c \in \{0, 1\}$ with $a = c$, $b = c$, and a constraint on $a$ and $b$ that allows only $(1, 1)$. The only solution is $(1, 1, 1)$. Start from $(0, 0, 0)$. Only the constraint on $a$ and $b$ is violated, so $a$ and $b$ are conflicted. For $a$, the value 0 has 1 conflict and the value 1 has 2 (it breaks $a = c$ and still breaks the constraint on $a$ and $b$, since $b = 0$). The same holds for $b$. So line L5 always keeps the current value, and the search never moves. The tests check that no seed escapes.

## Correctness

**Soundness.** Line L3 returns $\sigma$ only when no variable is conflicted. Every constraint has at least one variable, and a violated constraint makes each of its variables conflicted. So when no variable is conflicted, no constraint is violated, and $\sigma$ is a solution.

**Incompleteness.** The stuck case above has a solution, but from $(0, 0, 0)$ every step leaves $\sigma$ unchanged, so MIN-CONFLICTS returns failure for every $s$ and every sequence of random choices. So the method is not complete. It also never returns "no solution": on a problem with no solution it runs until the step limit. The full proof is below.

There is no general bound on the number of steps that min-conflicts needs on problems that have a solution. Results on its speed are measurements.

## Complexity

- **Per step.** Line L5 computes $\text{conflicts}(x, v, \sigma)$ for each of at most $d$ values. For binary constraints each count looks at the at most $n - 1$ neighbours of $x$, so a step costs $O(n d)$ in the word-RAM. The update of the counts after line L6 costs $O(n)$.
- **Total.** $O(s n d)$ for $s$ steps, plus $O(n d + e)$ to set up the counts for $e$ constraints.
- **Space.** $O(n)$ besides the input: the assignment, the counts and the list of conflicted variables.

## Properties

- **Sound, incomplete.** Any answer is a solution. A failure says nothing.
- **Randomized.** The result and the number of steps depend on the seed.
- **Measured behaviour on n-queens.** Minton and colleagues reported that the number of repairs stays approximately constant as $n$ grows, with a greedy start, and that the method solves the million-queens problem in less than four minutes on a SPARCstation 1. With a random start, the implementation here needs a median of 41, 94, 71 and 111 steps for $n = 8, 16, 32, 48$ on 10 seeds each. For $n = 8$, one of the 10 runs did not finish within 5000 steps. In these runs the median does not grow steadily with $n$, which agrees with the report of Minton and colleagues.
- **Good for loose, large problems.** Minton and colleagues explain the speed by the large number of solutions, which are spread through the space, so a local repair is often enough.

## Variants and improvements

- **Random walk.** With some probability, give the variable a random value instead of the best one. This is the move of [WalkSAT](/walksat/) for SAT, and it lets the search leave a stuck state.
- **Tabu search.** Forbid recent (variable, value) pairs for a few steps. See [tabu search](/tabu-search/).
- **Weights.** Breakout (Morris, 1993) adds weight to the constraints that are violated in a stuck state, which changes the landscape until the state is no longer a [local optimum](/local-optimum/).
- **Restarts.** Start again from a new assignment after a number of steps. See [random-restart hill climbing](/random-restart-hill-climbing/).
- **Simulated annealing.** Accept worse values with a probability that falls over time. See [simulated annealing](/simulated-annealing/).
- **For Max-CSP.** The same steps give an approximate answer to [Max-CSP](/maximum-csp/), keeping the best assignment seen.
- **For SAT.** [GSAT](/gsat/) is the SAT form of the same idea, choosing a flip that reduces the number of unsatisfied clauses the most.

## When to use it

Use min-conflicts for large problems with many solutions, where a complete search would be slow, and for repair tasks where a nearly correct assignment already exists, such as rescheduling after a small change. Its incremental nature fits online scheduling. Do not use it to prove that a problem has no solution, and add noise, tabu or weights when the problem is tight, because plain min-conflicts gets stuck there.

## Pitfalls

- **Treating failure as a proof.** A return of "failure" after $s$ steps does not mean that the problem has no solution.
- **Deterministic tie-breaking.** Always taking the first best value or the first conflicted variable makes cycles much more likely. Break ties at random.
- **Moving every step.** Forcing a change of value at every step, even when the current value is the best, is a different method. It can escape some stuck states, but it can also undo good values.
- **Recomputing all conflicts at each step.** On large problems, keep the counts and update only the neighbours of the changed variable, or the step cost grows with the number of constraints.

## Implementations

## History

Johnston and Adorf built a neural network (GDS) to schedule observations for the Hubble Space Telescope. Minton, Johnston, Philips and Laird analysed why it worked well, extracted the min-conflicts heuristic, and presented it at AAAI-90. The 1992 paper in Artificial Intelligence gives the full experiments on n-queens and graph coloring, an analysis of the heuristic, and its use in the telescope scheduler. Selman, Levesque and Mitchell (1992) gave [GSAT](/gsat/), the same idea for SAT, and later work added noise and weights to escape [local optima](/local-optimum/).

## References
