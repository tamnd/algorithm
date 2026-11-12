---
tag: 1RG9V7
kind: algorithm
slug: modified-policy-iteration
name: Modified policy iteration
aliases:
- optimistic policy iteration
area: machine-learning/reinforcement-learning
level: advanced
summary: "Each iteration takes a greedy policy and then evaluates it only partially, with m backups. Order m = 0 is value iteration and m = infinity is policy iteration."
solves: [mdp-planning]
model: real-ram
complexity:
  vars: {S: the number of states, A: the number of actions in each state, m: the order (backups with the fixed policy in each iteration), k: the number of iterations}
  time: {worst: "O(k (S^2 A + m S^2))"}
  space: {extra: "Θ(S)"}
properties: {deterministic: true, online: false, exact: false, recursive: false}
history:
  year: 1978
  people: [Martin L. Puterman, Moon Chirl Shin]
  note: Puterman and Shin defined the method and proved its convergence in Management Science in 1978.
prereqs: [value-iteration, policy-iteration]
see_also: [iterative-policy-evaluation, linear-programming-for-mdps, prioritized-sweeping, real-time-dynamic-programming, fitted-q-iteration, actor-critic]
sources:
  - paper: doi:10.1287/mnsc.24.11.1127
    title: "Martin L. Puterman and Moon Chirl Shin, Modified policy iteration algorithms for discounted Markov decision problems, Management Science 24(11), 1978, pages 1127 to 1137"
    locator: the definition of the method of order m and its convergence for a starting vector with a nonnegative Bellman residual
  - book: isbn:9780471619772
    title: Martin L. Puterman, Markov Decision Processes, Discrete Stochastic Dynamic Programming, Wiley, 1994
    locator: Section 6.5 (modified policy iteration, its convergence and its rate)
  - book: isbn:9781886529106
    title: Dimitri P. Bertsekas and John N. Tsitsiklis, Neuro-Dynamic Programming, Athena Scientific, 1996
    locator: Chapter 2 (optimistic policy iteration for discounted problems)
  - book: isbn:9780262039246
    title: Richard S. Sutton and Andrew G. Barto, Reinforcement Learning, An Introduction, second edition, MIT Press, 2018
    locator: Section 4.6 (generalized policy iteration) and the bibliographical remarks of Chapter 4
---

Modified policy iteration solves [MDP planning](/mdp-planning/) for a known finite discounted MDP. It is a family of methods with one integer parameter, the order $m \ge 0$. Each iteration makes the policy greedy for the current values, applies one backup with the Bellman optimality operator, and then applies $m$ more backups with the fixed policy. With $m = 0$ the method is exactly [value iteration](/value-iteration/). With $m = \infty$, which means an exact solve of the linear system, it is exactly [policy iteration](/policy-iteration/). Between these limits, a small $m$ often gives the lowest total cost, because the extra backups are cheaper than full optimality backups and they move the values much further.

## In plain words

Value iteration takes a tiny step with each sweep: it looks one step ahead and stops. Policy iteration takes a huge step: it works out exactly how good the current rule is, which costs a full system solve. Modified policy iteration takes a medium step. It picks the best action in each state for the current estimates, as both methods do. Then it pretends the rule is fixed for a few more rounds and updates the estimates with that rule only. These extra rounds are cheap, because each state looks at one action, not all of them.

A few extra rounds are usually enough to get most of the benefit of an exact solve, so the method needs far fewer sweeps than value iteration and does far less work per iteration than policy iteration.

## The problem

The input is a finite MDP $(S, A, P, R, \gamma)$ with $0 < \gamma < 1$, an order $m \in \{0, 1, 2, \ldots\} \cup \{\infty\}$, and a tolerance $\varepsilon > 0$. The output is a vector $V$ with $\lVert V - V^* \rVert_\infty < \varepsilon/2$ and a deterministic policy $\pi$ with $V^\pi(s) > V^*(s) - \varepsilon$ for each state $s$. For a deterministic policy $\pi$ the policy backup is $(T^\pi V)(s) = R(s, \pi(s)) + \gamma \sum_{s'} P(s' \mid s, \pi(s))\, V(s')$, and the optimality backup is $(TV)(s) = \max_a [R(s, a) + \gamma \sum_{s'} P(s' \mid s, a)\, V(s')]$.

## The algorithm

```pseudo id=main
MODIFIED-POLICY-ITERATION(S, A, P, R, γ, m, ε)
L1  V ← V_0                                    ▷ for example V_0 = 0
L2  loop
L3      π ← a greedy policy for V; keep the old π(s) if it is a maximizer
L4      U ← T^π V                                ▷ this equals T V
L5      if max_s |U(s) − V(s)| < ε (1 − γ) / (2 γ) then
L6          return U and a greedy policy for U
L7      if m = ∞ then
L8          U ← V^π, the solution of (I − γ P_π) U = r_π
L9      else repeat m times
L10         U ← T^π U                          ▷ partial evaluation
L11     V ← U
```

Lines L3 and L4 are one sweep of value iteration that also records the greedy policy. Lines L9 and L10 are $m$ sweeps of [iterative policy evaluation](/iterative-policy-evaluation/) for the fixed policy, started from $U$. So one iteration computes $V \leftarrow (T^\pi)^{m+1} V$ with $\pi$ greedy for $V$. The stopping test of line L5 is the test of value iteration, so the guarantee of the output is the same.

## Example

Take the two-state MDP of the [value iteration](/value-iteration/) page: states L and H, actions stay and move, $\gamma = 0.9$, optimal values $V^* = (180/11, 20) \approx (16.364, 20)$, with move optimal in L and stay optimal in H. Start from $V_0 = (0, 0)$ with $m = 2$.

Iteration 1. The greedy policy for $(0, 0)$ is (stay, stay), because stay gives an immediate reward and move does not. Line L4 gives $U = (1, 2)$. The two backups with (stay, stay) give $(1.9, 3.8)$ and then $(2.71, 5.42)$. This is exactly the third iterate of value iteration, because here the greedy policy for each of the first iterates is the same.

Later iterations. As the values grow, move becomes greedy in L, and the partial evaluations then push the values toward $V^*$ three backups at a time. The table counts the iterations until the stopping test of line L5 passes, with $\varepsilon = 0.01$.

| order $m$ | 0 (value iteration) | 1 | 2 | 5 | 10 | 20 | $\infty$ (policy iteration) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| iterations | 79 | 40 | 27 | 14 | 9 | 5 | 3 |

Each iteration with order $m$ costs one optimality backup plus $m$ policy backups. With $m = \infty$ the method needs two exact evaluations and a third iteration in which line L5 confirms that the values do not change.

## Correctness

Call a vector $V$ *improvable* if $TV \ge V$ in every state. If $V$ is improvable and $\pi$ is greedy for $V$, then $T^\pi V = TV \ge V$, so by monotonicity the vectors $(T^\pi)^j V$ never decrease in $j$, and their limit is $V^\pi \le V^*$. So one iteration maps an improvable $V$ to an improvable $V' = (T^\pi)^{m+1}V$ with $TV \le V' \le V^*$. By induction the iterates satisfy

$$T^k V_0 \le V_k \le V^*,$$

so they are never further from $V^*$ than the iterates of value iteration, and $\lVert V_k - V^* \rVert_\infty \le \gamma^k \lVert V_0 - V^* \rVert_\infty$. A general start reduces to this case: adding a constant $c$ to every entry of $V$ does not change the greedy policy, and one iteration multiplies the constant by $\gamma^{m+1}$. So the iterates from $V_0$ and from the improvable vector $V_0 - c$, for $c$ large enough, differ by $c\gamma^{k(m+1)}$, which tends to 0. The stopping test then gives the same $\varepsilon$ bounds as for value iteration. The full proof is in the proofs section.

## Complexity

**One iteration.** With dense transitions, lines L3 and L4 cost $O(|S|^2|A|)$ and lines L9 and L10 cost $O(m|S|^2)$. With $m = \infty$ line L8 costs $O(|S|^3)$ by Gaussian elimination. With sparse transitions, replace $|S|^2$ by the number of nonzero transition probabilities. The extra memory is $O(|S|)$ for finite $m$.

**Number of iterations.** From an improvable start the error after $k$ iterations is at most $\gamma^k$ times the first error, the same bound as value iteration. This bound does not improve with $m$, but in practice a larger $m$ needs far fewer iterations, as in the table above. The best $m$ depends on the problem and on the relative cost of the two kinds of backup.

## Properties

- **One family.** The order $m = 0$ gives value iteration and $m = \infty$ gives policy iteration exactly. The tests check this: in exact arithmetic, with $m = 0$ the iterates are equal to those of a separate value iteration, and with $m = \infty$ the sequence of policies and values is equal to that of a separate policy iteration.
- **Monotone from an improvable start.** If $TV_0 \ge V_0$, the iterates increase in every state and never exceed $V^*$. A safe choice is $V_0(s) = \min_{s', a} R(s', a)/(1 - \gamma)$ for all $s$.
- **Approximate.** For finite $m$ the output is $\varepsilon$-optimal, as for value iteration.
- **Policy backups are cheap.** A policy backup reads one action per state, so it costs a factor $|A|$ less than an optimality backup.

## Variants and improvements

- **Order that changes.** The order may change from one iteration to the next, and the convergence proof still holds. A common rule increases $m$ as the policy settles.
- **Evaluation to a tolerance.** Replace the fixed $m$ by sweeps of iterative evaluation until the change is small. This is the usual form of [policy iteration](/policy-iteration/) for large sparse models.
- **In-place sweeps.** Use Gauss-Seidel updates in lines L4 and L10. Convergence still holds, and often it is faster.
- **Approximate MPI.** With function approximation, each step is done from samples by regression, as in [fitted Q iteration](/fitted-q-iteration/). Scherrer and others (2015) analyzed the error propagation of approximate modified policy iteration.
- **Generalized policy iteration.** Sutton and Barto use this name for any interleaving of partial evaluation and greedy improvement, which includes [actor-critic](/actor-critic/) methods.

## When to use it

Use modified policy iteration when the model is known and too large for the exact solves of policy iteration, but $\gamma$ is close enough to 1 that value iteration needs many sweeps. Start with $m$ between 5 and 20. Use [value iteration](/value-iteration/) when $\gamma$ is small, and [policy iteration](/policy-iteration/) when the state space is small enough for a fast exact solve.

## Pitfalls

- **Start with negative rewards.** From a start that is not improvable, such as $V_0 = 0$ when all rewards are negative, the iterates do not increase monotonically. They still converge, but the sandwich bound does not apply to them directly.
- **Ties in line L3.** Keep the old action when it is a maximizer. Otherwise the policy can alternate between equally good actions. The values still converge, but the equality with policy iteration at $m = \infty$ is lost.
- **Return the right vector.** Line L6 returns $U = TV$ and a policy greedy for $U$. The error bounds apply to this pair. Returning $V$ with the policy of line L3 gives a weaker bound.
- **Large m is not free.** With $m$ much larger than needed, the method does many policy backups for a policy that the next greedy step will change anyway.

## Implementations

## History

Puterman and Shin defined modified policy iteration in Management Science in 1978. They named the order $m$, proved convergence from a start with nonnegative Bellman residual, and gave numerical comparisons with value and policy iteration. Van Nunen (1976) studied a similar value-oriented method. Puterman's 1994 book presents the method as the general case of which value and policy iteration are the two limits. Bertsekas and Tsitsiklis call it optimistic policy iteration, and Sutton and Barto use the related idea of generalized policy iteration as a frame for most of reinforcement learning.

## References
