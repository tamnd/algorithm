---
tag: 0SXB2S
kind: technique
slug: strong-branching
name: Strong branching
aliases:
- strong variable selection
- full strong branching
area: optimization/integer-programming
level: advanced
summary: Choose the branching variable by solving the LP relaxations of the two children of each candidate.
prereqs: [land-doig-algorithm, branching-rule, lp-relaxation, dual-simplex-method]
see_also: [pseudocost-branching, reliability-branching, branching-rule, node-selection-rule, branch-and-cut, mixed-integer-programming, traveling-salesman-problem, orbital-branching]
sources:
  - paper: "David Applegate, Robert E. Bixby, Vašek Chvátal and William Cook, Finding cuts in the TSP (a preliminary report), DIMACS Technical Report 95-05, 1995"
    locator: the branching rule that evaluates candidate branches with a limited number of dual simplex iterations (cited as the origin of strong branching)
  - paper: doi:10.1016/j.orl.2004.04.002
    title: Tobias Achterberg, Thorsten Koch and Alexander Martin, Branching rules revisited, Operations Research Letters 33(1), 2005
    locator: pp. 42 to 54; Section 2.3 (strong branching and full strong branching) and Table 1 of the ZIB-Report 04-13 version (geometric means of nodes and time)
  - paper: doi:10.1287/ijoc.11.2.173
    title: Jeff T. Linderoth and Martin W. P. Savelsbergh, A computational study of search strategies for mixed integer programming, INFORMS Journal on Computing 11(2), 1999
    locator: pp. 173 to 187 (variable selection rules, strong branching estimates and pseudocost initialization)
  - paper: "Tobias Achterberg, Constraint Integer Programming, PhD thesis, Technische Universität Berlin, 2007"
    locator: Chapter 5 (branching rules in SCIP, the product score; chapter number unsure)
---

Strong branching is a [branching rule](/branching-rule/) for LP-based [branch and bound](/land-doig-algorithm/). For each candidate variable it tentatively creates the two children, solves or partly solves their LP relaxations, and branches on the variable whose children improve the bound the most. It produces much smaller trees than simple rules, but each node costs many extra LP solves. Full strong branching tests every fractional variable; practical solvers test only a few candidates, with an iteration limit, and combine the results with [pseudocosts](/pseudocost-branching/).

## In plain words

Branch and bound splits a problem on one variable whose value in the relaxed solution is a fraction. Any such variable gives a correct search, but a good choice can make the search tree much smaller.

Strong branching chooses by trial. For each candidate, it imposes the "round down" condition, solves the relaxation, then does the same with "round up", and notes how much each side worsens the bound. It picks the variable for which both sides worsen the bound the most, because such a split cuts away the most hope of finding a better answer. The trials are expensive, so solvers often stop each trial after a few steps and try only the most promising candidates.

## When it applies

- LP-based branch and bound or [branch-and-cut](/branch-and-cut/) for a [mixed integer program](/mixed-integer-programming/), with variable branching $x_j \le \lfloor \bar{x}_j \rfloor$ or $x_j \ge \lceil \bar{x}_j \rceil$ on a fractional $\bar{x}_j$.
- An LP solver that can change one bound and restart from the current basis, so that a child LP is solved with a few [dual simplex](/dual-simplex-method/) iterations.
- The time per node is worth less than the size of the tree, which is usually true near the root, where decisions affect the largest subtrees.

## The template

The holes are CANDIDATES (which fractional variables to test, and in what order), the iteration limit $\gamma$, SCORE (how two gains become one number) and LOOKAHEAD (when to stop testing). The problem is a maximization, $v$ is the LP value of the node and $z^*$ is the value of the incumbent.

```pseudo id=main
STRONG-BRANCH(N, x̄, v, z*)
L1  C ← CANDIDATES(N, x̄)                          ▷ fractional integer variables, best first
L2  best ← none;  s* ← −∞
L3  for each j in C do
L4      v⁻ ← LP bound of N with x_j ≤ ⌊x̄_j⌋, after at most γ dual simplex iterations
L5      v⁺ ← LP bound of N with x_j ≥ ⌈x̄_j⌉, after at most γ dual simplex iterations
L6      if v⁻ ≤ z* and v⁺ ≤ z* then return PRUNE                 ▷ no better point in N
L7      if v⁻ ≤ z* then add x_j ≥ ⌈x̄_j⌉ to N                     ▷ keep only the up side
L8      if v⁺ ≤ z* then add x_j ≤ ⌊x̄_j⌋ to N                     ▷ keep only the down side
L9      s ← SCORE(v − v⁻, v − v⁺)
L10     if s > s* then best ← j;  s* ← s
L11     if LOOKAHEAD says stop then exit the loop
L12 return best
```

An infeasible child LP counts as a bound of $-\infty$. With $C$ equal to all fractional variables, $\gamma = \infty$ and no lookahead, the rule is *full strong branching*. A common SCORE is $(1 - \mu) \min(q^-, q^+) + \mu \max(q^-, q^+)$ with $\mu = 1/6$, as in Achterberg, Koch and Martin; SCIP uses the product $\max(q^-, \varepsilon) \cdot \max(q^+, \varepsilon)$.

**Why the search stays correct.** Branch and bound is correct for every choice of a fractional variable, so the choice at line L12 cannot make it wrong. The other lines use the bounds $v^-$ and $v^+$, and these must be true upper bounds on the child LPs. They are: in the dual simplex method each iteration keeps a dual feasible basis, and for a maximization its objective value is an upper bound on the LP optimum that only decreases. So a truncated value is still an upper bound, and if it is at most $z^*$, the child contains no integer point better than $z^*$. Lines L6 to L8 therefore remove only parts of $N$ that hold no better point. A child is called infeasible only when the dual simplex proves it, which also holds after few iterations.

**What is not proved.** Strong branching picks the locally best variable for the chosen score. No theorem says that this gives the smallest tree, and the tree can be larger than with another rule on some instances. Its value is measured on test sets.

**Example.** Take
$$\max\ 10x_1 + 10x_2 + 7x_3 \quad \text{s.t.} \quad 6x_1 + 4x_2 + 6x_3 \le 15,\quad 3x_1 + 8x_2 + 2x_3 \le 18,\quad x \in \{0, 1, 2, 3\}^3.$$
The root LP optimum is $\bar{x} = (\tfrac43, \tfrac74, 0)$ with $v = \tfrac{185}{6}$. Both $x_1$ and $x_2$ are fractional.

| candidate | down child | up child | gain $q^-$ | gain $q^+$ | score with $\mu = 1/6$ |
|---|---|---|---|---|---|
| $x_1$ | $x_1 \le 1$: $\tfrac{903}{30}$ | $x_1 \ge 2$: $\tfrac{55}{2}$ | $\tfrac{11}{15}$ | $\tfrac{10}{3}$ | $\tfrac76$ |
| $x_2$ | $x_2 \le 1$: $\tfrac{85}{3}$ | $x_2 \ge 2$: $27$ | $\tfrac52$ | $\tfrac{23}{6}$ | $\tfrac{49}{18}$ |

The most fractional rule picks $x_1$, whose fractional part $\tfrac13$ is closer to $\tfrac12$ than $\tfrac34$ is. Strong branching picks $x_2$. The integer optimum is 27, at $x = (0, 2, 1)$ only. In best-first branch and bound on this instance, counting every node created including the root and the infeasible children, branching on the most fractional variable creates 13 nodes and full strong branching creates 7. A single small instance shows the mechanism, not the size of the effect.

## Classic examples

- **Traveling salesman.** Applegate, Bixby, Chvátal and Cook evaluated candidate branches with a limited number of dual simplex iterations in their TSP code, the work later known as Concorde. Achterberg, Koch and Martin cite this report, and CPLEX 7.5, as the origin of the rule.
- **The study of Achterberg, Koch and Martin.** On instances from MIPLIB 2003 and from the benchmarks of Mittelmann that CPLEX 9.0 solves with at least 5000 nodes within one hour, with cuts only at the root and a one hour limit, they report geometric means of about 7242 nodes and 504 seconds for full strong branching, against about 262369 nodes and 938 seconds for most infeasible branching and about 88707 nodes and 283 seconds for pseudocost branching. So full strong branching gave by far the smallest trees, but it was slower than pseudocost branching. These numbers come from one solver (SIP), one machine and one test set.
- **Modern solvers.** CPLEX, Gurobi, SCIP and others use strong branching mainly at the top of the tree or for variables with unreliable pseudocosts, as in [reliability branching](/reliability-branching/).

## Variations

- **Partial strong branching.** Test only a subset of candidates, ordered by a cheap score such as pseudocosts, and limit the dual simplex iterations to $\gamma$. Achterberg, Koch and Martin set $\gamma$ to twice the average number of iterations per node LP, and stop after $\lambda = 4$ or $\lambda = 8$ candidates without a new best one.
- **Hybrid strong and pseudocost branching.** Use strong branching up to a fixed depth and [pseudocost branching](/pseudocost-branching/) below it.
- **Strong branching as initialization.** Use the gains of strong branching to initialize pseudocosts, and use strong branching on a variable until its pseudocosts are reliable. This is [reliability branching](/reliability-branching/).
- **Strong branching with propagation.** Run bound propagation, or even cuts, in the tentative children, which gives better estimates at a higher cost.
- **Learned approximations.** Several methods train a model to imitate the choice of full strong branching from cheap features of the node. Their results are measured on their own test sets.

## Pitfalls

- **Cost.** Each candidate costs two LP solves. Full strong branching on a node with hundreds of fractional variables can take far longer than the node LP itself.
- **Truncated values as estimates.** A truncated child bound is a valid upper bound but a poor estimate of the child LP value. The score then favours candidates whose LPs converge fast.
- **Infeasible children.** If one child is infeasible, its gain is infinite. The score must cap it, or apply the bound change of lines L7 and L8 and look again, instead of comparing infinite values.
- **Warm start after the trial.** The LP solver must return to the basis of the node after each trial. Otherwise the node LP is solved again from a worse basis.
- **Nodes are not time.** Strong branching reduces the node count much more than the running time. Compare branching rules by total time and by the number of solved instances, as the computational studies do.

## Exercises

1. Check the four child LP values in the example by solving each child LP by hand or with an LP solver.
2. Compute the product score $q^- q^+$ for both candidates in the example. Does it pick the same variable?
3. Prove that after any number of dual simplex iterations on a child LP of a maximization problem, the objective value of the current basis is an upper bound on the child LP value.
4. Search small random instances with a program and find one on which full strong branching creates more nodes than the most fractional rule. Explain what goes wrong.
5. Suppose a node has $k$ fractional variables and each child LP takes $t$ iterations. Estimate the cost of one full strong branching step, and compare it with the cost of the node LP.

## References
