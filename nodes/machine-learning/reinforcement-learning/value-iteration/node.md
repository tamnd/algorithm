---
tag: XRA79Y
kind: algorithm
slug: value-iteration
name: Value iteration
area: machine-learning/reinforcement-learning
level: intro
summary: "Apply the Bellman optimality backup to every state again and again. The values converge geometrically to V*, and the greedy policy of the last values is eps-optimal."
solves: [mdp-planning]
model: real-ram
complexity:
  vars: {S: the number of states, A: the number of actions in each state, k: the number of sweeps}
  time: {worst: "O(k S^2 A)"}
  space: {extra: Θ(S)}
properties: {deterministic: true, online: false, exact: false, recursive: false}
history:
  year: 1957
  people: [Richard Bellman]
  note: Bellman solved the functional equation of the discounted Markovian decision process by successive approximation in 1957.
prereqs: [markov-decision-process, bellman-optimality-equation, bellman-contraction]
see_also: [policy-iteration, modified-policy-iteration, linear-programming-for-mdps, prioritized-sweeping, real-time-dynamic-programming, q-learning, fitted-q-iteration, fixed-point-iteration]
sources:
  - paper: "Richard Bellman, A Markovian decision process, Journal of Mathematics and Mechanics 6, 1957, pages 679 to 684"
    locator: the discounted functional equation and its solution by successive approximation
  - book: isbn:9780471619772
    title: Martin L. Puterman, Markov Decision Processes, Discrete Stochastic Dynamic Programming, Wiley, 1994
    locator: Section 6.3 (value iteration, its convergence and the stopping rule for an eps-optimal policy)
  - book: isbn:9780262039246
    title: Richard S. Sutton and Andrew G. Barto, Reinforcement Learning, An Introduction, second edition, MIT Press, 2018
    locator: Section 4.4 (value iteration) and Section 4.5 (asynchronous dynamic programming)
  - book: isbn:9781886529106
    title: Dimitri P. Bertsekas and John N. Tsitsiklis, Neuro-Dynamic Programming, Athena Scientific, 1996
    locator: Chapter 2 (value iteration for discounted problems and for stochastic shortest paths)
  - paper: "Michael L. Littman, Thomas L. Dean and Leslie Pack Kaelbling, On the complexity of solving Markov decision problems, Proceedings of the Eleventh Conference on Uncertainty in Artificial Intelligence (UAI 1995), pages 394 to 402"
    locator: the section on value iteration (the iteration bound in 1/(1 - gamma) and the input size, after Tseng 1990)
  - paper: "Eugene A. Feinberg and Jefferson Huang, The value iteration algorithm is not strongly polynomial for discounted dynamic programming, Operations Research Letters 42(2), 2014, pages 130 to 131"
    locator: the example in which the number of iterations to an optimal policy grows without bound
---

Value iteration solves [MDP planning](/mdp-planning/) for a known finite [Markov decision process](/markov-decision-process/) with the discounted criterion. It starts from any value vector and applies the Bellman optimality backup $V \leftarrow TV$ to all states in each sweep. Since $T$ is a $\gamma$-contraction in the max norm ([Bellman contraction](/bellman-contraction/)), the error to the optimal values $V^*$ shrinks by the factor $\gamma$ in each sweep. It stops when two sweeps differ by less than $\varepsilon(1-\gamma)/(2\gamma)$ and returns a greedy policy, which is then $\varepsilon$-optimal. Each sweep costs $O(|S|^2|A|)$ arithmetic operations.

## In plain words

Each state keeps a number: a guess of how much reward you can still collect from there. In one sweep, every state looks one step ahead. For each action, it adds the reward of the action to the discounted average of the guesses of the states where the action can lead. The best of these sums is the new guess of the state.

After the first sweep the guesses are right for a game of one step. After the second sweep they are right for two steps, and so on. Because later rewards count less and less, the guesses settle down quickly. When a sweep changes almost nothing, you stop, and in each state you pick the action that looked best in the last sweep.

## The problem

The input is a finite MDP $(S, A, P, R, \gamma)$: a set of states $S$, a set of actions $A$, transition probabilities $P(s' \mid s, a)$, expected rewards $R(s, a)$ and a discount factor $0 \le \gamma < 1$, together with a tolerance $\varepsilon > 0$. The goal is a policy $\pi$ whose value $V^\pi$ is within $\varepsilon$ of the optimal value $V^*$ in every state. The Bellman optimality operator is

$$(TV)(s) = \max_{a \in A} \Big[ R(s, a) + \gamma \sum_{s' \in S} P(s' \mid s, a)\, V(s') \Big],$$

and $V^*$ is its unique fixed point ([Bellman optimality equation](/bellman-optimality-equation/)). A policy $\pi$ is *greedy* for $V$ if $\pi(s)$ attains the maximum in $(TV)(s)$ for each $s$.

## The algorithm

```pseudo id=main
VALUE-ITERATION(S, A, P, R, γ, ε)
L1  V(s) ← 0 for each state s                    ▷ any start works
L2  repeat
L3      for each state s do
L4          V′(s) ← max over a of [R(s, a) + γ Σ_{s′} P(s′ | s, a) V(s′)]
L5      δ ← max over s of |V′(s) − V(s)|
L6      V ← V′
L7  until δ < ε(1 − γ) / (2γ)
L8  for each state s do
L9      π(s) ← an action a that maximizes R(s, a) + γ Σ_{s′} P(s′ | s, a) V(s′)
L10 return V, π
```

Lines L3 and L4 compute $V' = TV$ from the old vector only. This is the synchronous form, also called the Jacobi form. Line L5 measures the change of the sweep, and line L7 turns the tolerance $\varepsilon$ on the policy into a tolerance on the change. Lines L8 and L9 extract a greedy policy from the last vector. With $\gamma = 0$ one sweep gives $V = TV = V^*$, and the test of line L7 must not divide by zero.

## Example

Take two states, L (low) and H (high), two actions, stay and move, and $\gamma = 0.9$. In L, stay gives reward 1 and stays in L, and move gives reward 0 and goes to H with probability $1/2$, else stays in L. In H, stay gives reward 2 and stays in H, and move gives reward 0 and goes to L. Solving the Bellman equations of the four deterministic policies gives $V^* = (180/11, 20) \approx (16.364, 20)$, with the optimal policy "move in L, stay in H".

Start from $V_0 = (0, 0)$:

| sweep $k$ | $V_k(\mathrm{L})$ | $V_k(\mathrm{H})$ | $Q(\mathrm{L}, \text{stay})$ | $Q(\mathrm{L}, \text{move})$ | greedy in L | $\lVert V_k - V^* \rVert_\infty$ |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 1 | 2 | 1.9 | 1.35 | stay | 18 |
| 2 | 1.9 | 3.8 | 2.71 | 2.565 | stay | 16.2 |
| 3 | 2.71 | 5.42 | 3.439 | 3.6585 | move | 14.58 |
| 4 | 3.6585 | 6.878 | 4.29265 | 4.741425 | move | 13.122 |

The two $Q$ columns are computed from $V_k$, so they give $V_{k+1}(\mathrm{L})$ and the greedy action for $V_k$. From sweep 3 on, the greedy policy is optimal, while the values are still far from $V^*$. Here $V_k(\mathrm{H}) = 20(1 - 0.9^k)$, so the error is exactly $0.9^k \lVert V^* \rVert_\infty$: the bound of the next section holds with equality. With $\varepsilon = 0.1$ the loop stops after 57 sweeps, and with $\varepsilon = 0.01$ after 79 sweeps; the final errors are $0.049$ and $0.0049$, both below $\varepsilon/2$.

## Correctness

Write $\lVert \cdot \rVert$ for the max norm and $V_k$ for the vector after $k$ sweeps. The operator $T$ is a $\gamma$-contraction with the fixed point $V^*$, so

$$\lVert V_k - V^* \rVert \le \gamma^k \lVert V_0 - V^* \rVert .$$

This gives termination for $\varepsilon > 0$. When the loop stops with $\lVert V_k - V_{k-1} \rVert < \varepsilon(1-\gamma)/(2\gamma)$, then $\lVert V_k - V^* \rVert < \varepsilon/2$, and the greedy policy $\pi$ of line L9 has $\lVert V^\pi - V^* \rVert < \varepsilon$. The key step is that $T^\pi V_k = T V_k$ for a greedy $\pi$, so both $V^\pi$ and $V^*$ are within $\gamma/(1-\gamma)$ times the last change of $V_k$. The full proof is in the proofs section.

Since there are finitely many deterministic policies, there is a gap between the value of an optimal policy and the best non-optimal one. So after finitely many sweeps every greedy policy is optimal. The number of such sweeps depends on this gap and is not bounded by a function of $|S|$, $|A|$ and $\gamma$ alone (see the complexity section).

## Complexity

**One sweep.** Line L4 does one multiply and one add for each triple $(s, a, s')$ with $P(s' \mid s, a) > 0$. With dense transitions this is $|S|^2|A|$ multiply-adds and $|S|(|A| - 1)$ comparisons, so $O(|S|^2|A|)$ time in the [real RAM](/real-ram/) model. With at most $b$ successors for each pair it is $O(b|S||A|)$. The memory is two vectors of $|S|$ numbers besides the model.

**Number of sweeps for an $\varepsilon$-optimal policy.** Let $|R(s, a)| \le R_{\max}$ and $V_0 = 0$, so $\lVert V^* \rVert \le R_{\max}/(1-\gamma)$. By the triangle inequality, the change of sweep $k$ is at most $\lVert V_k - V^* \rVert + \lVert V_{k-1} - V^* \rVert \le 2\gamma^{k-1} R_{\max}/(1-\gamma)$. So the loop stops after at most

$$k \le 1 + \frac{\ln\big(4\gamma R_{\max} / (\varepsilon (1-\gamma)^2)\big)}{\ln(1/\gamma)} = O\Big(\frac{1}{1-\gamma} \log \frac{R_{\max}}{\varepsilon(1-\gamma)}\Big)$$

sweeps, a worst-case bound, since $\ln(1/\gamma) \ge 1 - \gamma$. The factor $1/(1-\gamma)$ is real: in the example the error falls only by the factor $0.9$ per sweep.

**An exact optimal policy.** With rational data and a fixed $\gamma$, the number of sweeps until the greedy policy is optimal is polynomial in the input size in binary, a result of Tseng (1990) that Littman, Dean and Kaelbling summarize. So value iteration is weakly polynomial for a fixed $\gamma$. Feinberg and Huang (2014) gave a small deterministic example in which this number of sweeps is not bounded by any function of the numbers of states and actions, so value iteration is not strongly polynomial. [Policy iteration](/policy-iteration/) is strongly polynomial for a fixed $\gamma$.

## Properties

- **Anytime.** Each $V_k$ is the optimal value of the $k$-step problem with terminal values $V_0$, and its greedy policy can be used at any time.
- **Monotone from below.** If $TV_0 \ge V_0$ (for example $V_0 = \min_{s,a} R(s,a)/(1-\gamma)$ in each state), the iterates increase to $V^*$, because $T$ is monotone.
- **Not exact.** The output values are within $\varepsilon/2$ of $V^*$, not equal to it. The policy is often optimal well before the values are close, as in the example.
- **Deterministic.** Ties in line L9 are broken by a fixed rule, for example the first maximizing action.

## Variants and improvements

- **Gauss-Seidel value iteration.** Write $V(s)$ in place, so that later states in the sweep use the new values. It is still a $\gamma$-contraction, and it often needs fewer sweeps. This is the [Gauss-Seidel method](/gauss-seidel-method/) idea applied to a nonlinear fixed point.
- **Asynchronous value iteration.** Back up the states in any order, one at a time. It converges if each state is backed up infinitely often (Bertsekas and Tsitsiklis, Chapter 2). [Prioritized sweeping](/prioritized-sweeping/) picks the state with the largest Bellman error, and [real-time dynamic programming](/real-time-dynamic-programming/) backs up the states on simulated trajectories.
- **Finite horizon.** For a horizon $H$, $H$ sweeps from $V_0 = 0$ give the exact optimal values and a non-stationary optimal policy. This is backward induction.
- **Undiscounted problems.** For [stochastic shortest path](/stochastic-shortest-path/) problems with $\gamma = 1$, value iteration converges under conditions on proper policies, and relative value iteration handles the average reward criterion.
- **Partial evaluation steps.** [Modified policy iteration](/modified-policy-iteration/) adds $m$ cheap backups with a fixed policy after each sweep; $m = 0$ is value iteration.
- **Sampled backups.** Replace the expectation by a sample to get [Q-learning](/q-learning/), or fit a function to the backups to get [fitted Q iteration](/fitted-q-iteration/). For POMDPs, [point-based value iteration](/point-based-value-iteration/) backs up a finite set of beliefs.

## When to use it

Use value iteration when the model is known, the state space is small enough to sweep, and an $\varepsilon$-optimal policy is enough. Each sweep is cheap and needs no linear solve, so it scales to larger state spaces than [policy iteration](/policy-iteration/), whose evaluation step costs $O(|S|^3)$ by elimination. When $\gamma$ is close to 1 the number of sweeps grows like $1/(1-\gamma)$, and policy iteration or [modified policy iteration](/modified-policy-iteration/) usually needs far fewer iterations. Use [linear programming](/linear-programming-for-mdps/) when there are extra linear constraints on the policy.

## Pitfalls

- **Stopping on the wrong quantity.** A test $\delta < \varepsilon$ in line L7 does not make the values $\varepsilon$-accurate: the error can be up to $\gamma\delta/(1-\gamma)$, which is $9\delta$ for $\gamma = 0.9$. Use $\delta < \varepsilon(1-\gamma)/(2\gamma)$.
- **Overwriting during a synchronous sweep.** If line L4 writes into $V$ instead of $V'$, the code is the Gauss-Seidel variant. It still converges, but the trace and the bound $\gamma^k$ of the synchronous form no longer describe it step by step.
- **Treating $V$ as the value of the returned policy.** The vector of line L10 is an estimate of $V^*$, not $V^\pi$. Evaluate $\pi$ exactly with [policy evaluation](/policy-evaluation/) when its value matters.
- **Discount 1.** With $\gamma = 1$ the contraction argument fails, the threshold of line L7 is 0, and the values may diverge. Use a stochastic shortest path formulation with a terminal state, or the average reward variants.

## Implementations

## History

Bellman introduced the Markovian decision process and its functional equation in 1957 and solved the equation by successive approximation, which is value iteration. Howard's [policy iteration](/policy-iteration/) followed in 1960. The stopping rule with the threshold $\varepsilon(1-\gamma)/(2\gamma)$ is the standard one in Puterman's book. Tseng (1990) bounded the number of iterations for an exact optimal policy by a polynomial in the input size for a fixed discount, and Feinberg and Huang (2014) showed that no bound in the number of states and actions alone exists.

## References
