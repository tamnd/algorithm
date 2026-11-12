---
tag: BW714H
kind: algorithm
slug: policy-iteration
name: Policy iteration
aliases:
- Howard policy iteration
- Howard's algorithm for MDPs
area: machine-learning/reinforcement-learning
level: intro
summary: "Alternate an exact evaluation of the current policy with a greedy improvement step until the policy no longer changes. The last policy is optimal."
solves: [mdp-planning]
model: real-ram
complexity:
  vars: {S: the number of states, A: the number of actions in each state, k: the number of iterations}
  time: {worst: "O(k (S^3 + S^2 A))"}
  space: {extra: "Θ(S^2)"}
properties: {deterministic: true, online: false, exact: true, recursive: false}
history:
  year: 1960
  people: [Ronald A. Howard]
  note: Howard described policy iteration in his 1960 book Dynamic Programming and Markov Processes, which grew out of his MIT doctoral thesis.
prereqs: [markov-decision-process, policy-evaluation, policy-improvement-theorem]
see_also: [value-iteration, modified-policy-iteration, linear-programming-for-mdps, iterative-policy-evaluation, simplex-method, markov-game, monte-carlo-control, actor-critic]
sources:
  - paper: "Ronald A. Howard, Dynamic Programming and Markov Processes, Technology Press of MIT and John Wiley, 1960"
    locator: the policy iteration method for the discounted and the average reward criteria
  - book: isbn:9780471619772
    title: Martin L. Puterman, Markov Decision Processes, Discrete Stochastic Dynamic Programming, Wiley, 1994
    locator: Section 6.4 (policy iteration for discounted problems, its convergence and its relation to Newton's method)
  - book: isbn:9780262039246
    title: Richard S. Sutton and Andrew G. Barto, Reinforcement Learning, An Introduction, second edition, MIT Press, 2018
    locator: Sections 4.2 and 4.3 (policy improvement and policy iteration)
  - paper: doi:10.1287/moor.1110.0516
    title: "Yinyu Ye, The simplex and policy-iteration methods are strongly polynomial for the Markov decision problem with a fixed discount rate, Mathematics of Operations Research 36(4), 2011, pages 593 to 603"
    locator: the main theorems (iteration bounds for Howard's method and for the simplex method with Dantzig's rule)
  - paper: doi:10.1145/2432622.2432623
    title: "Thomas Dueholm Hansen, Peter Bro Miltersen and Uri Zwick, Strategy iteration is strongly polynomial for 2-player turn-based stochastic games with a constant discount factor, Journal of the ACM 60(1), 2013, article 1"
    locator: the improved bound for Howard's policy iteration and its extension to strategy iteration
  - paper: doi:10.1007/978-3-642-14162-1_46
    title: "John Fearnley, Exponential lower bounds for policy iteration, ICALP 2010, Lecture Notes in Computer Science 6199, pages 551 to 562"
    locator: the MDPs on which Howard's policy iteration needs exponentially many iterations under the total reward and average reward criteria
---

Policy iteration solves [MDP planning](/mdp-planning/) for a known finite [Markov decision process](/markov-decision-process/) with the discounted criterion. It keeps a deterministic policy $\pi$. In each iteration it computes $V^\pi$ exactly by solving a linear system ([policy evaluation](/policy-evaluation/)), then makes $\pi$ greedy with respect to $V^\pi$. By the [policy improvement theorem](/policy-improvement-theorem/) each change makes the policy strictly better, so no policy repeats, and the loop ends after at most $|A|^{|S|}$ iterations with an optimal policy. For a fixed $\gamma$ the number of iterations is also bounded by a polynomial in $|S|$ and $|A|$ (Ye 2011; Hansen, Miltersen and Zwick 2013).

## In plain words

Start with any rule that says what to do in each state. First, work out exactly how good this rule is: for each state, the total discounted reward you collect if you follow the rule from there. Then go through the states. In each one, ask whether some other action, followed by the old rule, would do better. If yes, switch to that action.

The new rule is never worse than the old one in any state, and it is better in at least one state. So you never see the same rule twice. There are only finitely many rules, so the process stops. It stops when no state wants to switch, and then the rule is the best possible. In practice this takes very few rounds, often fewer than ten.

## The problem

The input is a finite MDP $(S, A, P, R, \gamma)$ with transition probabilities $P(s' \mid s, a)$, expected rewards $R(s, a)$ and a discount factor $0 \le \gamma < 1$. The output is a deterministic stationary policy $\pi^*$ with $V^{\pi^*}(s) = V^*(s)$ for every state $s$, together with $V^*$. Such a policy exists for every finite discounted MDP. For a policy $\pi$ write $P_\pi$ for the $|S| \times |S|$ matrix $P_\pi(s, s') = P(s' \mid s, \pi(s))$ and $r_\pi(s) = R(s, \pi(s))$. Then $V^\pi$ is the unique solution of $(I - \gamma P_\pi)V = r_\pi$, the [Bellman expectation equation](/bellman-expectation-equation/), and

$$Q^\pi(s, a) = R(s, a) + \gamma \sum_{s'} P(s' \mid s, a)\, V^\pi(s')$$

is its [action value function](/action-value-function/).

## The algorithm

```pseudo id=main
POLICY-ITERATION(S, A, P, R, γ)
L1  π ← any deterministic policy
L2  repeat
L3      V ← the solution of (I − γ P_π) V = r_π           ▷ evaluation
L4      stable ← true
L5      for each state s do                               ▷ improvement
L6          b ← an action that maximizes Q(s, a) = R(s, a) + γ Σ_{s′} P(s′ | s, a) V(s′); take b = π(s) if π(s) maximizes
L7          if b ≠ π(s) then π(s) ← b, stable ← false
L8  until stable
L9  return π, V
```

Line L3 is an exact evaluation, for example by [Gaussian elimination](/gaussian-elimination/). The matrix $I - \gamma P_\pi$ is invertible because the rows of $\gamma P_\pi$ sum to $\gamma < 1$. Line L6 is the improvement step. The rule "keep $\pi(s)$ if it is among the best actions" matters: without it, two equally good actions can alternate forever. Line L8 stops when no state changed, that is, when $\pi$ is greedy for its own values.

## Example

Take the two-state MDP of the [value iteration](/value-iteration/) page: states L and H, actions stay and move, $\gamma = 0.9$. In L, stay gives 1 and stays, move gives 0 and goes to H with probability $1/2$. In H, stay gives 2 and stays, move gives 0 and goes to L.

| iteration | $\pi$ (L, H) | $V^\pi$ (L, H) | $Q(\mathrm{L}, \cdot)$ (stay, move) | $Q(\mathrm{H}, \cdot)$ (stay, move) | change |
| --- | --- | --- | --- | --- | --- |
| 1 | stay, stay | 10, 20 | 10, 27/2 | 20, 9 | L to move |
| 2 | move, stay | 180/11, 20 | 173/11, 180/11 | 20, 162/11 | none |

In iteration 1, $V^\pi(\mathrm{L}) = 1/(1 - 0.9) = 10$ and $Q(\mathrm{L}, \text{move}) = 0.9 \cdot (20 + 10)/2 = 13.5 > 10$, so L switches. In iteration 2, $V(\mathrm{L})$ solves $V = 0.9 \cdot (20 + V)/2$, so $V = 9/0.55 = 180/11$. No state has a better action, so the loop stops with the optimal values $(180/11, 20)$. Policy iteration needed two linear solves. Value iteration from zero needs 3 sweeps for the optimal greedy policy and 79 sweeps for its $\varepsilon = 0.01$ stopping rule, and its values are never exact.

## Correctness

If line L7 changes $\pi$ to $\pi'$, then $Q^\pi(s, \pi'(s)) \ge V^\pi(s)$ in each state, with strict inequality in each changed state, because the old action was not a maximizer there. The [policy improvement theorem](/policy-improvement-theorem/) then gives $V^{\pi'} \ge V^\pi$ in every state and $V^{\pi'} \ne V^\pi$. So the sequence of values strictly increases in the componentwise order, no policy appears twice, and the loop stops after at most $|A|^{|S|}$ iterations. At the stop, $\pi$ is greedy for $V^\pi$, so $V^\pi = T^\pi V^\pi = TV^\pi$, and $V^\pi$ is the unique fixed point $V^*$ of the Bellman optimality operator $T$ ([Bellman contraction](/bellman-contraction/)). The full proof, with the comparison to value iteration below, is in the proofs section.

## Complexity

**One iteration.** The evaluation of line L3 costs $O(|S|^3)$ arithmetic operations by Gaussian elimination, or $O(|S|^\omega)$ with fast matrix multiplication. The improvement of lines L5 to L7 costs $O(|S|^2|A|)$ with dense transitions. The extra memory is the $|S| \times |S|$ matrix of line L3.

**Number of iterations, trivial bound.** No policy repeats, so there are at most $|A|^{|S|}$ iterations. This bound holds for every $\gamma < 1$.

**Never slower than value iteration.** Let $V_0 = V^{\pi_0}$ and let $\pi_k$ be the policy evaluated in iteration $k + 1$. Then $T^k V_0 \le V^{\pi_k} \le V^*$, so after $k$ iterations policy iteration is at least as close to $V^*$ as $k$ sweeps of [value iteration](/value-iteration/) from the same start. The proof is in the proofs section. In particular $\lVert V^{\pi_k} - V^* \rVert_\infty \le \gamma^k \lVert V^{\pi_0} - V^* \rVert_\infty$.

**Strongly polynomial for a fixed discount.** Let $n = |S|$ and let $m$ be the total number of state-action pairs, $m = |S||A|$ here. Ye (2011) proved that Howard's policy iteration, and the [simplex method](/simplex-method/) with Dantzig's most negative reduced cost rule on the [LP formulation](/linear-programming-for-mdps/), stop after $O\big(\frac{mn}{1-\gamma}\log\frac{n}{1-\gamma}\big)$ iterations. Hansen, Miltersen and Zwick (2013) improved the bound for policy iteration to

$$O\Big(\frac{m}{1-\gamma}\log\frac{n}{1-\gamma}\Big)$$

iterations, and proved the same bound for strategy iteration on 2-player turn-based stochastic games (a [Markov game](/markov-game/) with one player in control of each state). Each iteration costs a polynomial number of arithmetic operations, so for a fixed $\gamma$ the whole algorithm is strongly polynomial. These bounds grow with $1/(1-\gamma)$; they are not polynomial when $\gamma$ is part of the input.

**Lower bounds.** Fearnley (2010) built MDPs on which Howard's policy iteration needs a number of iterations exponential in the number of states under the total reward and the average reward criteria. These are undiscounted settings, so they do not contradict the bounds above. Variants that switch one state at a time with a bad rule can also be slow: Melekopoglou and Condon (1994) gave exponential examples for such single-switch rules, as Ye's paper reports.

## Properties

- **Exact.** With exact arithmetic the output policy is optimal and the output values equal $V^*$, not an approximation.
- **Monotone.** The values of the policies never decrease in any state.
- **Few iterations in practice.** Small and medium problems usually need a handful of iterations, much fewer than value iteration when $\gamma$ is close to 1. This is an observation, not a bound.
- **Newton's method.** Policy iteration is Newton's method applied to the equation $TV - V = 0$, with $-(I - \gamma P_\pi)$ as the derivative at a point where $\pi$ is greedy (Puterman, Section 6.4). This explains the fast final convergence.

## Variants and improvements

- **Modified policy iteration.** Replace the exact solve of line L3 by $m$ backups with the fixed policy. With $m = 0$ this is value iteration, and with $m = \infty$ it is policy iteration. See [modified policy iteration](/modified-policy-iteration/).
- **Iterative evaluation.** Solve line L3 with [iterative policy evaluation](/iterative-policy-evaluation/) to a tolerance instead of by elimination. This is cheap for sparse or large models.
- **Simple policy iteration.** Switch only the one state with the largest gain $Q^\pi(s, a) - V^\pi(s)$. This is exactly the simplex method with Dantzig's rule on the dual LP.
- **Average reward.** Howard also gave a version for the average reward criterion, which evaluates a gain and a bias vector.
- **Generalized policy iteration.** Any interleaving of partial evaluation and partial improvement, as in [Monte Carlo control](/monte-carlo-control/) and [actor-critic](/actor-critic/) methods, follows the same pattern with sampled estimates.

## When to use it

Use policy iteration when the model is known, the state space is small enough for a linear solve (a few thousand states with dense elimination), and you want an exactly optimal policy. It needs far fewer iterations than [value iteration](/value-iteration/) when $\gamma$ is close to 1, but each iteration is more expensive. For large sparse models, [modified policy iteration](/modified-policy-iteration/) with a small $m$ often gives the best total time. For constraints on the policy, use [linear programming](/linear-programming-for-mdps/).

## Pitfalls

- **Ties in line L6.** If line L6 takes the first maximizing action instead of keeping $\pi(s)$ when it is a maximizer, two equally good actions can alternate and the loop of line L8 never stops.
- **Floating point ties.** With floats, rounding can make the current action look a little worse than an equal one. Compare $Q(s, \pi(s)) \ge \max_a Q(s, a) - \tau$ with a small tolerance $\tau$ in line L6.
- **Discount 1.** With $\gamma = 1$ the matrix $I - P_\pi$ is singular, so line L3 fails. Use the stochastic shortest path or the average reward version.
- **Stopping on values.** Stopping when $V$ changes little, instead of when $\pi$ is stable, can stop with a suboptimal policy. The test of line L8 is exact.

## Implementations

## History

Howard published policy iteration in 1960 in Dynamic Programming and Markov Processes, three years after Bellman's value iteration. Puterman and Brumelle (1979) related it to Newton's method, and Puterman and Shin (1978) placed it at one end of the family of [modified policy iteration](/modified-policy-iteration/). Its worst case stayed open for decades. Ye (2011) proved that it is strongly polynomial for a fixed discount, and Hansen, Miltersen and Zwick (2013) sharpened the bound and extended it to games. Fearnley (2010) showed exponential lower bounds in the undiscounted total and average reward settings.

## References
