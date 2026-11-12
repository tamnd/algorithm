---
tag: YX6WMJ
kind: algorithm
slug: linear-programming-for-mdps
name: Linear programming formulation of MDPs
aliases:
- LP for MDPs
- LP formulation of MDPs
area: machine-learning/reinforcement-learning
level: advanced
summary: "Write a finite MDP as a linear program: the primal over values, the dual over occupancy measures. Solve it with the simplex method and read the policy from the dual."
solves: [mdp-planning]
model: real-ram
complexity:
  vars: {S: the number of states, A: the number of actions in each state, k: the number of simplex pivots}
  time: {worst: "O(k (S^3 + S^2 A))"}
  space: {extra: "Θ(S^2 A)"}
properties: {deterministic: true, online: false, exact: true, recursive: false}
history:
  year: 1960
  people: [Alan S. Manne, F. d'Epenoux]
  note: Manne gave a linear program for an average cost inventory problem in 1960, and d'Epenoux gave the linear program of the discounted problem in 1963.
prereqs: [markov-decision-process, bellman-optimality-equation, simplex-method, dual-linear-program]
see_also: [policy-iteration, value-iteration, mdp-planning, strong-duality, complementary-slackness, reduced-cost, dantzig-pivot-rule, interior-point-method]
sources:
  - paper: doi:10.1287/mnsc.10.1.98
    title: "F. d'Epenoux, A probabilistic production and inventory problem, Management Science 10(1), 1963, pages 98 to 108"
    locator: the linear program of a discounted Markov decision problem
  - paper: "Alan S. Manne, Linear programming and sequential decisions, Management Science 6(3), 1960"
    locator: the linear program of an average cost inventory problem over the stationary state-action frequencies
  - book: isbn:9780471619772
    title: Martin L. Puterman, Markov Decision Processes, Discrete Stochastic Dynamic Programming, Wiley, 1994
    locator: Section 6.9 (the primal and dual linear programs of discounted models, and the correspondence between basic feasible solutions and deterministic policies)
  - paper: doi:10.1287/moor.1110.0516
    title: "Yinyu Ye, The simplex and policy-iteration methods are strongly polynomial for the Markov decision problem with a fixed discount rate, Mathematics of Operations Research 36(4), 2011, pages 593 to 603"
    locator: the iteration bound of the simplex method with Dantzig's rule on the dual program
---

A finite discounted [Markov decision process](/markov-decision-process/) can be written as a linear program. The primal program has one variable $V(s)$ for each state and one constraint for each state-action pair, and its optimal solution is the optimal value function $V^*$. The dual program has one variable $x(s, a)$ for each state-action pair, its feasible solutions are the discounted occupancy measures of policies, and an optimal dual solution gives an optimal policy. This turns [MDP planning](/mdp-planning/) into linear programming, which shows that it is solvable in polynomial time, and it allows linear constraints on the policy that dynamic programming cannot express. On the dual, the [simplex method](/simplex-method/) with Dantzig's rule is a policy iteration that switches one state at a time.

## In plain words

The best values of the states are the smallest numbers that pass a set of checks. There is one check for each place and each action: the value of the place must be at least the reward of the action plus the discounted value of where it leads. Find the smallest numbers that pass all checks, and you have the best values.

The mirror problem counts how often, with discounting, each action is used in each place. These counts must balance like a flow: what enters a place equals what leaves it. Maximize the reward these counts collect. At the best solution, each place uses one action, and that action is the best rule.

## The problem

The input is a finite MDP $(S, A, P, R, \gamma)$ with $0 \le \gamma < 1$ and positive state weights $\alpha(s) > 0$, for example $\alpha(s) = 1$ or a start distribution. The output is $V^*$, an optimal occupancy measure $x^*$, and an optimal deterministic policy $\pi^*$. The two programs are

$$
\begin{aligned}
\text{(P)}\quad & \min_V \ \sum_s \alpha(s) V(s) && \text{subject to } V(s) - \gamma \sum_{s'} P(s' \mid s, a)\, V(s') \ge R(s, a) \ \text{ for each } (s, a), \\
\text{(D)}\quad & \max_{x \ge 0} \ \sum_{s, a} R(s, a)\, x(s, a) && \text{subject to } \sum_a x(s', a) - \gamma \sum_{s, a} P(s' \mid s, a)\, x(s, a) = \alpha(s') \ \text{ for each } s'.
\end{aligned}
$$

They are a pair of [dual linear programs](/dual-linear-program/). The constraints of (P) say $V \ge TV$, where $T$ is the Bellman optimality operator, and the smallest such $V$ is $V^*$. The constraints of (D) are flow balance: the discounted number of visits to $s'$ equals the start weight plus the discounted flow into $s'$. For a policy $\pi$ and the start weights $\alpha$, the occupancy measure $x_\pi(s, a) = \sum_t \gamma^t \Pr_\pi(s_t = s, a_t = a)$ is feasible for (D), and its objective is $\sum_s \alpha(s)V^\pi(s)$.

## The algorithm

We run the revised [simplex method](/simplex-method/) on (D) in the standard form $\max c^\top x$, $Mx = \alpha$, $x \ge 0$. Column $(s, a)$ of $M$ is $e_s - \gamma P(\cdot \mid s, a)$, and $c(s, a) = R(s, a)$. A basis $B$ is a set of $|S|$ columns.

```pseudo id=main
LP-MDP-SIMPLEX(S, A, P, R, γ, α, π_0)
L1  for each pair (s, a): column M(s, a) ← e_s − γ P(· | s, a), cost c(s, a) ← R(s, a)
L2  B ← the columns (s, π_0(s)), one for each state      ▷ no phase 1 is needed
L3  loop
L4      y ← the solution of B^T y = c_B                    ▷ y = V^π for the policy π of B
L5      for each pair (s, a): δ(s, a) ← c(s, a) − y^T M(s, a)  ▷ = Q^π(s, a) − V^π(s)
L6      if δ(s, a) ≤ 0 for every pair then return V = y, x_B = B^{-1} α, and π(s) = the action of the basic column of s
L7      e ← a pair with the largest δ; the first one on ties
L8      u ← B^{-1} M(e); r ← the row with u_r > 0 that minimizes (x_B)_r / u_r
L9      replace the basic column of row r by e
```

Line L2 starts from the basis of any deterministic policy $\pi_0$. Its matrix is $B = (I - \gamma P_{\pi_0})^\top$, which is invertible, and $x_B = (I - \gamma P_{\pi_0}^\top)^{-1}\alpha \ge \alpha > 0$, so the start is feasible and no phase 1 is needed. Line L4 computes the simplex multipliers. They are the values $V^\pi$ of the policy of the basis, because $B^\top y = c_B$ is the system $(I - \gamma P_\pi)y = r_\pi$. Line L5 computes the [reduced costs](/reduced-cost/), and they are the advantages $Q^\pi(s, a) - V^\pi(s)$. Line L7 is [Dantzig's rule](/dantzig-pivot-rule/). Line L8 is the ratio test.

## Example

Take the two-state MDP of the [value iteration](/value-iteration/) page: states L and H, actions stay and move, $\gamma = 0.9$, and $\alpha = (1, 1)$. The primal program is to minimize $V(\mathrm{L}) + V(\mathrm{H})$ subject to

$$V(\mathrm{L}) \ge 1 + 0.9V(\mathrm{L}),\quad V(\mathrm{L}) \ge 0.45V(\mathrm{H}) + 0.45V(\mathrm{L}),\quad V(\mathrm{H}) \ge 2 + 0.9V(\mathrm{H}),\quad V(\mathrm{H}) \ge 0.9V(\mathrm{L}).$$

Start from $\pi_0$ = (stay, stay). Then $B = 0.1 I$, $x_B = (10, 10)$ and $y = (10, 20)$. The reduced costs are $0$ for the two basic columns, $Q(\mathrm{L}, \text{move}) - 10 = 13.5 - 10 = 7/2$, and $Q(\mathrm{H}, \text{move}) - 20 = 9 - 20 = -11$. Column (L, move) enters. Its column is $(0.55, -0.45)$, so $u = (5.5, -4.5)$, only row L passes the ratio test, and (L, stay) leaves.

With the basis (move, stay), $y = (180/11, 20)$. The reduced costs of the two nonbasic columns are $Q(\mathrm{L}, \text{stay}) - 180/11 = 173/11 - 180/11 = -7/11$ and $Q(\mathrm{H}, \text{move}) - 20 = 162/11 - 20 = -58/11$, both negative, so the basis is optimal after one pivot. The dual solution is $x(\mathrm{L}, \text{move}) = 20/11$ and $x(\mathrm{H}, \text{stay}) = 200/11$, with total $20 = 2/(1 - 0.9)$. Its objective $2 \cdot 200/11 = 400/11$ equals the primal objective $180/11 + 20$, as [strong duality](/strong-duality/) requires. The policy read from $x$ moves in L and stays in H.

## Correctness

The full proof is in the proofs section. In outline:

- **Primal.** A feasible $V$ satisfies $V \ge TV$, and by the monotonicity of $T$, $V \ge T^kV \to V^*$. The vector $V^*$ is feasible, since $V^* = TV^*$. With $\alpha > 0$, $V^*$ is the unique optimal solution of (P).
- **Bases are policies.** In a feasible $x$, each state $s$ has $\sum_a x(s, a) \ge \alpha(s) > 0$. A basic feasible solution has at most $|S|$ positive entries, so it has exactly one positive entry in each state. So every [basic feasible solution](/basic-feasible-solution/) is the occupancy measure of a deterministic policy, and it is nondegenerate.
- **Pivots are policy switches.** The basis after a pivot is again a policy, so the leaving column of line L8 is the old column of the same state as the entering column. A pivot switches the action of one state to an action with a positive advantage. Nondegeneracy makes the objective rise strictly, so no basis repeats.
- **Stop.** When all reduced costs are at most 0, $y = V^\pi$ is feasible for (P) and the objectives are equal, so both solutions are optimal, $V^\pi = V^*$, and $\pi$ is optimal.
- **Any optimal dual solution.** If $x$ is optimal for (D), for example from an interior point method, the policy $\pi(a \mid s) = x(s, a)/\sum_b x(s, b)$ is optimal. It may be randomized when there are ties.

## Complexity

**Size.** Program (D) has $|S|$ equality constraints and $|S||A|$ variables, and (P) has the transposed shape. A dense constraint matrix has $|S|^2|A|$ entries.

**One pivot.** The implementation solves two $|S| \times |S|$ systems from scratch in each pivot, which costs $O(|S|^3)$, and the pricing of line L5 costs $O(|S|^2|A|)$. A revised simplex method that updates a factorization of $B$ costs $O(|S|^2)$ per update instead of $O(|S|^3)$.

**Number of pivots.** The pivots are policy switches that strictly improve $\sum_s \alpha(s)V^\pi(s)$, so there are at most $|A|^{|S|}$. Ye (2011) proved that the simplex method with Dantzig's rule on (D) needs $O\big(\frac{|S|^2|A|}{1-\gamma}\log\frac{|S|}{1-\gamma}\big)$ pivots, so it is strongly polynomial for a fixed discount. For deterministic MDPs, Post and Ye showed that the simplex method is strongly polynomial for any discount.

**Polynomial time.** An interior point method or the ellipsoid method solves (P) or (D) in time polynomial in $|S|$, $|A|$ and the bit length of the data, for every $\gamma$ ([LP is in P](/lp-in-p/)). This is the reason MDP planning is in P.

## Properties

- **Exact.** With rational data and exact arithmetic, the simplex method returns $V^*$ and an optimal policy exactly, not an approximation.
- **Nondegenerate.** With $\alpha > 0$, every basic feasible solution of (D) is nondegenerate, so the simplex method cannot cycle under any rule that picks an improving column.
- **Weights.** Every choice of $\alpha > 0$ gives the same optimal $V^*$ and the same set of optimal deterministic policies. The occupancy measure depends on $\alpha$.
- **Simple policy iteration.** The simplex method with Dantzig's rule is the policy iteration that switches only the state-action pair with the largest advantage. [Policy iteration](/policy-iteration/) switches all improvable states at once, which is a block pivot.

## Variants and improvements

- **Average reward.** Manne's 1960 program optimizes the long-run state-action frequencies, with the constraint that they sum to 1. Unichain and multichain models need different programs (Puterman, Chapters 8 and 9).
- **Constrained MDPs.** Add linear constraints on (D), such as a bound on an expected cost $\sum_{s, a} C(s, a)x(s, a) \le b$. The optimal policy may then need randomization in a few states. This is the standard method for constrained MDPs.
- **Interior point methods.** Solve (P) or (D) with an [interior point method](/interior-point-method/). This gives polynomial time for every $\gamma$, but the solution may be a randomized optimal policy when there are ties.
- **Approximate linear programming.** For large state spaces, restrict $V$ to a linear combination of features and sample the constraints (de Farias and Van Roy 2003).
- **Finite horizon and shortest paths.** The same idea, with a time index or without the discount, gives programs for the finite horizon and the [stochastic shortest path](/stochastic-shortest-path/) problems.

## When to use it

Use the LP formulation when the policy must satisfy extra linear constraints (budgets, safety constraints, fairness constraints), when you need an exact solution with a proof of optimality (the dual solution is a certificate), or when you want polynomial time for every $\gamma$ with a solver that is already available. Without constraints, [policy iteration](/policy-iteration/) and [value iteration](/value-iteration/) are usually faster in practice, because they exploit the structure of the program.

## Pitfalls

- **Zero weights.** With $\alpha(s) = 0$ for some states, the dual can be degenerate, and the policy in states that the optimal policy never reaches is arbitrary. Use $\alpha > 0$ everywhere.
- **Randomized output.** A solution that is not basic, as from an interior point method, can split $x(s, \cdot)$ over several optimal actions. Normalize it to a randomized policy, or round it to any action with positive weight in that state.
- **Discount 1.** With $\gamma = 1$, every column of (D) sums to 0 while $\alpha$ sums to a positive number, so (D) is infeasible. Use the average reward or the stochastic shortest path program.
- **Floating point.** A floating point simplex solver can return slightly infeasible values. Check the result with one Bellman backup.

## Implementations

## History

Manne (1960) wrote an average cost inventory problem as a linear program over state-action frequencies. D'Epenoux (1963) gave the linear program of the discounted problem. Wolfe and Dantzig, and later Denardo and Derman, developed the programs and their duals further, and Puterman's 1994 book gives the correspondence between basic feasible solutions and deterministic policies. Ye (2011) proved that the simplex method with Dantzig's rule is strongly polynomial on these programs for a fixed discount, a rare positive result for the simplex method. Approximate linear programming by de Farias and Van Roy (2003) extended the approach to large state spaces.

## References
