---
tag: SYAD7P
kind: algorithm
slug: iterative-policy-evaluation
name: Iterative policy evaluation
aliases:
- iterative policy evaluation sweep
- successive approximation for a fixed policy
area: machine-learning/reinforcement-learning
level: intro
summary: "Compute the value function of a fixed policy by sweeps of the Bellman expectation backup over all states, until the largest change in a sweep is small."
solves: [policy-evaluation]
model: real-ram
complexity:
  vars: {S: the number of states, A: the number of actions in each state, k: the number of sweeps}
  time: {worst: "O(k S^2 A)"}
  space: {extra: "Θ(S)"}
properties: {deterministic: true, online: false, exact: false, recursive: false}
history:
  year: 1957
  people: [Richard Bellman]
  note: The method is the successive approximation that Bellman used for the functional equations of dynamic programming, applied to one fixed policy. Sutton and Barto gave it its current name.
prereqs: [policy-evaluation, bellman-expectation-equation]
see_also: [policy-iteration, modified-policy-iteration, value-iteration, jacobi-method, gauss-seidel-method, temporal-difference-learning, monte-carlo-policy-evaluation, least-squares-td]
sources:
  - book: isbn:9780262039246
    title: Richard S. Sutton and Andrew G. Barto, Reinforcement Learning, An Introduction, second edition, MIT Press, 2018
    locator: Section 4.1 (iterative policy evaluation, the in-place version and Example 4.1, the 4 x 4 gridworld)
  - book: isbn:9780471619772
    title: Martin L. Puterman, Markov Decision Processes, Discrete Stochastic Dynamic Programming, Wiley, 1994
    locator: Chapter 6 (successive approximation and Gauss-Seidel variants for discounted models)
  - book: isbn:9781886529106
    title: Dimitri P. Bertsekas and John N. Tsitsiklis, Neuro-Dynamic Programming, Athena Scientific, 1996
    locator: Chapter 2 (value iteration for a fixed policy and asynchronous, Gauss-Seidel updates)
---

Iterative policy evaluation solves the [policy evaluation](/policy-evaluation/) problem for a known finite MDP. It finds the [state value function](/state-value-function/) $V^\pi$ of a fixed [policy](/policy/) $\pi$ without solving a linear system. It starts from $V = 0$ and sweeps over the states. In each state it replaces $V(s)$ by the right side of the [Bellman expectation equation](/bellman-expectation-equation/), computed with the current values. For $\gamma < 1$ each sweep shrinks the error by at least the factor $\gamma$, so the values converge geometrically to $V^\pi$. The loop stops when the largest change in a sweep is below a threshold $\theta$. There are two forms: a two-array sweep, in which every update reads the values of the previous sweep, and an in-place sweep, in which every update reads the newest values.

## In plain words

You want to know how good a fixed way of acting is from each position. Start by guessing zero everywhere. Then visit every position and ask: if I act as the rule says, what reward do I get now, and how good is the place I land in, by my current guesses? Write that down as the new guess for this position.

One pass over all positions gives better guesses. Repeat the pass. Each pass passes information one more step back from the rewards, and the guesses settle down to the true values. Stop when a full pass changes no guess by more than a small amount.

If you overwrite the guesses during the pass, later positions already see the new numbers, and the method usually settles in fewer passes.

## The problem

The input is a finite MDP $(S, A, P, R, \gamma)$, a policy that takes action $a$ in state $s$ with probability $\pi(a \mid s)$, and a threshold $\theta > 0$. The output is a vector $V$ close to $V^\pi$, the unique solution of

$$V^\pi(s) = \sum_a \pi(a \mid s)\Big[R(s, a) + \gamma \sum_{s'} P(s' \mid s, a)\, V^\pi(s')\Big] \quad \text{for each } s.$$

Write $T^\pi$ for the map that sends $V$ to the right side of this equation. For $0 \le \gamma < 1$ the map $T^\pi$ is a $\gamma$-contraction in the max norm, as on the [Bellman contraction](/bellman-contraction/) page, so $V^\pi$ exists and is unique. With $\gamma = 1$ the method also works for an episodic task in which the policy reaches a terminal state with zero reward with probability 1.

## The algorithm

```pseudo id=main
ITERATIVE-POLICY-EVALUATION(S, A, P, R, γ, π, θ)
L1  V(s) ← 0 for each state s                    ▷ terminal states keep V = 0
L2  repeat
L3      δ ← 0
L4      for each state s do
L5          v ← Σ_a π(a | s) [R(s, a) + γ Σ_{s′} P(s′ | s, a) V(s′)]
L6          δ ← max(δ, |v − V(s)|)
L7          V(s) ← v                             ▷ in place; the two-array form writes to a copy
L8  until δ < θ
L9  return V
```

In the in-place form, line L7 writes into the same array that line L5 reads, so a state later in the sweep sees the new value of a state earlier in the sweep. This is the Gauss-Seidel method for the linear system $(I - \gamma P_\pi)V = r_\pi$. In the two-array form, line L7 writes into a second array that becomes $V$ after the sweep, so one sweep computes $V \leftarrow T^\pi V$. This is the [Jacobi method](/jacobi-method/) for the same system.

## Example

Take Example 4.1 of Sutton and Barto: a 4 by 4 grid with states 0 to 15 in rows, terminal states 0 and 15 in two corners, four moves (up, down, right, left) that fail at the border and leave the state unchanged, reward $-1$ on every move, $\gamma = 1$, and the policy that picks each move with probability $1/4$.

With two arrays, the values of four states change as follows. State 1 is next to terminal 0, state 2 is next to it, state 3 is the far corner of the top row, and state 5 is on the diagonal.

| sweep $k$ | $V(1)$ | $V(2)$ | $V(3)$ | $V(5)$ |
| --- | --- | --- | --- | --- |
| 0 | 0 | 0 | 0 | 0 |
| 1 | $-1$ | $-1$ | $-1$ | $-1$ |
| 2 | $-7/4$ | $-2$ | $-2$ | $-2$ |
| 3 | $-39/16$ | $-47/16$ | $-3$ | $-23/8$ |
| 10 | $-6.138$ | $-8.352$ | $-8.967$ | $-7.737$ |
| limit | $-14$ | $-20$ | $-22$ | $-18$ |

In sweep 2, state 1 has one neighbor that is terminal, one wall that keeps it in place, and two neighbors with value $-1$, so $V(1) = -1 + \frac{1}{4}(0 - 1 - 1 - 1) = -7/4$. The limit is the expected number of moves to reach a corner, with a minus sign. The full limit, row by row, is $0, -14, -20, -22$; $-14, -18, -20, -20$; $-20, -20, -18, -14$; $-22, -20, -14, 0$.

The in-place form is faster here. After its first sweep in row order, the first row is already $0, -1, -1.25, -1.3125$, because each state sees the new value of its left neighbor. The number of sweeps until $\delta < \theta$, and the largest error at that point:

| threshold $\theta$ | two arrays | in place |
| --- | --- | --- |
| $10^{-2}$ | 89 sweeps, error 0.174 | 62 sweeps, error 0.103 |
| $10^{-4}$ | 173 sweeps, error 0.00176 | 114 sweeps, error 0.00109 |
| $10^{-6}$ | 258 sweeps | 167 sweeps |

The error at the stop is more than ten times $\theta$. With $\gamma = 1$ the bound below does not hold, and the change in the last sweep underestimates the error.

## Correctness

For $\gamma < 1$, one two-array sweep applies $T^\pi$, and one in-place sweep applies a map $G^\pi$ that is also a $\gamma$-contraction in the max norm with fixed point $V^\pi$. So after $k$ sweeps the error is at most $\gamma^k \lVert V^\pi \rVert_\infty$ from the start $V = 0$, and the loop stops. The value of $\delta$ in line L8 is the max norm of the change in the last sweep. If it is below $\theta$, the returned vector satisfies

$$\lVert V - V^\pi \rVert_\infty \le \frac{\gamma}{1 - \gamma}\,\theta .$$

The proof, for both forms, is in the proofs section.

## Complexity

**One sweep.** Line L5 reads one row of transition probabilities for each action with $\pi(a \mid s) > 0$. A sweep costs $O(|S|^2|A|)$ with dense transitions, $O(|S|^2)$ for a deterministic policy, and in general the number of nonzero transition probabilities that the policy uses. The extra memory is one array for the in-place form and two for the two-array form.

**Number of sweeps.** For $\gamma < 1$ the change in sweep $k$ is at most $\gamma^{k-1}$ times the change in sweep 1. So the loop stops after at most $1 + \lceil \ln(\delta_1/\theta) / \ln(1/\gamma) \rceil$ sweeps, where $\delta_1$ is the change in the first sweep. For $\gamma$ close to 1 this is about $\ln(\delta_1/\theta)/(1 - \gamma)$ sweeps. A direct solve by [Gaussian elimination](/gaussian-elimination/) costs $O(|S|^3)$, so the iterative method wins when $|S|$ is large, the transitions are sparse, or the policy is close to a previous one whose values are a good start.

## Properties

- **Approximate.** The output is within $\gamma\theta/(1-\gamma)$ of $V^\pi$, not exact. With exact rational arithmetic every sweep is exact, but the limit is reached only in the limit.
- **Monotone.** If the start satisfies $T^\pi V_0 \ge V_0$, the values never decrease. The start $V = 0$ has this property when all rewards are nonnegative.
- **Order matters for the in-place form.** The number of in-place sweeps depends on the order of the states. Sweeping from the terminal states outward is fastest on shortest path tasks.
- **No model change.** The method uses the model only through the backup in line L5. A learning method that replaces this expectation by a sample gives [temporal difference learning](/temporal-difference-learning/).

## Variants and improvements

- **Asynchronous updates.** Update the states in any order, any number of times, as long as each state is updated infinitely often. The values still converge to $V^\pi$ for $\gamma < 1$ (Bertsekas and Tsitsiklis).
- **Warm start.** Inside [policy iteration](/policy-iteration/), start each evaluation from the values of the previous policy. A fixed number $m$ of sweeps gives [modified policy iteration](/modified-policy-iteration/).
- **Successive over-relaxation.** Move each value past the backup target by a factor $\omega \in (1, 2)$. This can reduce the number of sweeps, as for [Gauss-Seidel](/gauss-seidel-method/) on other linear systems.
- **Sample based.** [Monte Carlo policy evaluation](/monte-carlo-policy-evaluation/) and [temporal difference learning](/temporal-difference-learning/) estimate $V^\pi$ from episodes without a model. [Least squares TD](/least-squares-td/) solves the linear system for a linear approximation.
- **Action values.** The same sweeps on the equation for $Q^\pi$ give the [action value function](/action-value-function/).

## When to use it

Use iterative policy evaluation when the model is known and the state space is too large for an exact linear solve, or as the evaluation step of policy iteration with a warm start. Use a direct solve for a few hundred states or fewer, and when exact values matter. Use sample methods when the model is unknown.

## Pitfalls

- **Small change is not small error.** The change $\delta$ in the last sweep is not the error. The error can be up to $\gamma/(1-\gamma)$ times larger, which is 99 times larger for $\gamma = 0.99$. Choose $\theta$ with this factor in mind.
- **Discount 1.** With $\gamma = 1$ the loop converges only if the policy reaches a terminal state with probability 1. A policy that can loop forever with negative rewards makes the values diverge to $-\infty$, and no error bound in terms of $\theta$ holds.
- **Terminal states.** A terminal state must keep the value 0. Line L1 sets it, and the model must make it absorbing with reward 0.
- **Mixing the two forms.** Writing into the same array that a two-array implementation reads silently turns it into the in-place form. The values still converge, but the intermediate values differ from the published tables.

## Implementations

## History

Successive approximation for the functional equations of dynamic programming goes back to Bellman's 1957 book Dynamic Programming. Howard (1960) evaluated each policy by solving the linear equations directly. Puterman's 1994 book treats successive approximation and its Gauss-Seidel form for discounted models, and Bertsekas and Tsitsiklis (1996) analyze asynchronous updates. Sutton and Barto gave the name iterative policy evaluation, with the in-place form and the 4 by 4 gridworld as the standard example, in their 1998 book and its 2018 second edition.

## References
