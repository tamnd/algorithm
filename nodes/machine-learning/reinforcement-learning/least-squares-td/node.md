---
tag: 6WB7ES
kind: algorithm
slug: least-squares-td
name: Least-squares temporal-difference learning
aliases:
- LSTD
- LSTD(lambda)
- recursive LSTD
area: machine-learning/reinforcement-learning
level: advanced
summary: "Estimate the matrix A and vector b of linear TD from a batch of transitions and solve A theta = b directly. No step size; O(d^2) per step with Sherman-Morrison updates."
solves: [policy-evaluation]
model: real-ram
complexity:
  vars: {T: the number of transitions, d: the number of features}
  time: {worst: "O(T d^2 + d^3)"}
  space: {extra: "O(d^2)"}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 1996
  people: [Steven J. Bradtke, Andrew G. Barto]
  note: "Bradtke and Barto introduced LSTD and recursive LSTD for lambda = 0. Boyan extended it to LSTD(lambda) in 1999 and 2002."
prereqs: [value-function-approximation, sherman-morrison-formula]
see_also: [temporal-difference-learning, td-lambda, gradient-temporal-difference, ordinary-least-squares, eligibility-traces, fitted-q-iteration, policy-evaluation]
sources:
  - paper: doi:10.1007/BF00114723
    title: Steven J. Bradtke and Andrew G. Barto, Linear least-squares algorithms for temporal difference learning, Machine Learning 22, 1996, pages 33 to 57
    locator: the LSTD and RLSTD algorithms and their convergence
  - paper: doi:10.1023/A:1017936530646
    title: Justin A. Boyan, Technical update, Least-squares temporal difference learning, Machine Learning 49, 2002, pages 233 to 246
    locator: LSTD(lambda) with eligibility traces, and the equivalence of LSTD(1) with least-squares regression on returns
  - paper: doi:10.1109/9.580874
    title: John N. Tsitsiklis and Benjamin Van Roy, An analysis of temporal-difference learning with function approximation, IEEE Transactions on Automatic Control 42(5), 1997, pages 674 to 690
    locator: the TD(lambda) fixed point that LSTD(lambda) estimates
  - book: isbn:9780262039246
    title: Richard S. Sutton and Andrew G. Barto, Reinforcement Learning, An Introduction, second edition, MIT Press, 2018
    locator: Section 9.8, Least-Squares TD
---

Least-squares temporal-difference learning (LSTD) evaluates a fixed policy with linear features $\hat{v}(s) = \phi(s)^\top\theta$. Linear TD(0) moves $\theta$ by small steps toward the solution of $A\theta = b$, the TD fixed point of [value function approximation](/value-function-approximation/). LSTD estimates $A$ and $b$ from the data instead and solves the linear system once. It needs no step size, uses each transition fully, and gives the exact solution of the sample TD equations. The cost is $O(d^2)$ per transition and $O(d^2)$ memory for $d$ features, against $O(d)$ for TD. Bradtke and Barto (1996) introduced it, and Boyan (2002) added [eligibility traces](/eligibility-traces/) to get LSTD($\lambda$).

## In plain words

Ordinary TD learning nudges its weights a little after each step, and you must pick how big the nudges are. Pick them too big and the weights jump around; pick them too small and learning is slow.

LSTD keeps a running summary of all the experience instead. The summary is one small table and one list of numbers. At the end it solves for the weights that make the average TD correction over all that experience exactly zero. This is the answer TD would drift toward if you replayed the same data again and again with tiny nudges, but LSTD gets it in one step.

The summary grows with the square of the number of features, so LSTD is a good fit when there are tens or hundreds of features, not millions.

## The problem

Given transitions $(s_t, r_t, s'_t)$ from a fixed policy and a feature map $\phi : \mathcal{S} \to \mathbb{R}^d$, find $\theta$ such that $\phi(s)^\top\theta$ approximates the [state value function](/state-value-function/). This is [policy evaluation](/policy-evaluation/) with linear function approximation. The target of LSTD($\lambda$) is the TD($\lambda$) fixed point: the $\theta$ with $\Phi\theta = \Pi T^{(\lambda)}\Phi\theta$, which for $\lambda = 0$ is the solution of

$$A\theta = b, \qquad A = \Phi^\top D(I - \gamma P)\Phi, \qquad b = \Phi^\top D r.$$

## The algorithm

```pseudo id=main
LSTD(data, φ, γ, λ, ε)
L1  A ← εI;  b ← 0;  z ← 0
L2  for each transition (s, r, s′) in data do
L3      f ← φ(s);  f′ ← φ(s′), or 0 if s′ is terminal
L4      z ← γλ z + f                            ▷ eligibility trace
L5      A ← A + z (f − γ f′)ᵀ
L6      b ← b + r z
L7      if s′ is terminal then z ← 0
L8  return the solution θ of A θ = b
```

With $\lambda = 0$ the trace is $z = \phi(s)$, and line L5 adds $\phi(s)(\phi(s) - \gamma\phi(s'))^\top$. Then $A\theta = b$ says that the TD errors $\delta_t(\theta) = r_t + \gamma\phi(s'_t)^\top\theta - \phi(s_t)^\top\theta$ satisfy $\sum_t \phi(s_t)\delta_t(\theta) = 0$: the TD(0) updates over the batch cancel. The term $\epsilon I$ is a small ridge term that keeps $A$ invertible when the data are few; $\epsilon = 0$ gives plain LSTD.

**Recursive LSTD.** To get $\theta$ after every transition, keep $B = A^{-1}$ instead of $A$. Each transition changes $A$ by the rank one matrix $zv^\top$ with $v = f - \gamma f'$, so the [Sherman-Morrison formula](/sherman-morrison-formula/) updates $B$ in $O(d^2)$ time:

$$B \leftarrow B - \frac{(Bz)(v^\top B)}{1 + v^\top Bz}, \qquad \theta = Bb.$$

Start with $B = \epsilon^{-1}I$, which is the inverse of the $\epsilon I$ of line L1. Then recursive LSTD returns exactly the same $\theta$ as batch LSTD with the same $\epsilon$ after every prefix of the data.

## Example

Use the three-state chain of [value function approximation](/value-function-approximation/): $P$ moves from state 0 to 0 or 1 with probability $1/2$ each, from state 1 to 0, 1, 2 with probabilities $1/4, 1/2, 1/4$, and from state 2 to 1 or 2 with probability $1/2$ each. The reward is $1$ on leaving state 2 and $0$ otherwise, $\gamma = 9/10$, and the features are $\phi(0) = (1, 0)$, $\phi(1) = (1, 1)$, $\phi(2) = (1, 3)$. The stationary distribution is $\mu = (1/4, 1/2, 1/4)$.

The walk $0 \to 0 \to 1 \to 1 \to 1 \to 2 \to 2 \to 1 \to 0$ has 8 transitions, and each pair $(s, s')$ appears exactly $8\mu(s)P(s, s')$ times. Run LSTD with $\lambda = 0$ and $\epsilon = 0$:

| transition | $\phi(s)(\phi(s) - \gamma\phi(s'))^\top$ | $r\,\phi(s)$ |
|---|---|---|
| 0 → 0 | [[1/10, 0], [0, 0]] | (0, 0) |
| 0 → 1 | [[1/10, −9/10], [0, 0]] | (0, 0) |
| 1 → 1 (twice) | [[1/10, 1/10], [1/10, 1/10]] each | (0, 0) |
| 1 → 2 | [[1/10, −17/10], [1/10, −17/10]] | (0, 0) |
| 2 → 2 | [[1/10, 3/10], [3/10, 9/10]] | (1, 3) |
| 2 → 1 | [[1/10, 21/10], [3/10, 63/10]] | (1, 3) |
| 1 → 0 | [[1/10, 1], [1/10, 1]] | (0, 0) |
| sum | [[4/5, 1], [1, 67/10]] | (2, 6) |

The sums are $8A$ and $8b$ for the exact $A$ and $b$ of the chain. Solving gives $\theta = (185/109, 70/109) \approx (1.6972, 0.6422)$, which is the TD fixed point exactly. Semi-gradient TD(0) reaches this point only in the limit: after 120000 sampled steps, its mean over 4 seeds is $(1.692, 0.637)$.

Recursive LSTD with $\epsilon = 1/100$ on the same walk gives $\theta = (0, 0)$ for the first 5 transitions, because no reward has been seen. After the 8 transitions it gives $(74200/44351, 28600/44351) \approx (1.6730, 0.6449)$, the same as batch LSTD with $\epsilon = 1/100$. After the walk is repeated 10 times it gives $(1.6948, 0.6425)$: the ridge term matters less as the data grow.

## Correctness

With $\lambda = 0$ and $\epsilon = 0$, the output solves $\sum_t \phi(s_t)\delta_t(\theta) = 0$. When the pairs $(s, s')$ occur in the data in proportion to $\mu(s)P(s, s')$, the sample matrices are exact multiples of $A$ and $b$, so LSTD returns the TD fixed point exactly. On one trajectory of an ergodic chain the proportions converge, so $\hat{A}/T \to A$ and $\hat{b}/T \to b$, and since $A$ is invertible the output converges to $A^{-1}b$ with probability one. Recursive LSTD equals batch LSTD by induction with the Sherman-Morrison formula. With $\lambda = 1$ on complete episodes, the sums telescope and LSTD(1) is the least-squares fit of the observed returns on the features. The full proofs are below.

## Complexity

- **Batch LSTD.** Each transition costs $O(d^2)$ for the outer product in line L5, and line L8 costs $O(d^3)$ by [Gaussian elimination](/gaussian-elimination/). The total is $O(Td^2 + d^3)$ time and $O(d^2)$ memory, independent of $T$.
- **Recursive LSTD.** Each transition costs $O(d^2)$ for two matrix-vector products and one rank one update, and $\theta$ is available at every step.
- **Compared with TD.** Linear TD costs $O(d)$ per step, so LSTD is $d$ times more expensive per transition. In exchange it needs no step size and uses each transition fully, so it usually needs fewer transitions for the same accuracy.

## Properties

- **No step size.** The only parameters are $\lambda$ and the ridge term $\epsilon$.
- **Data efficient.** Every transition enters $A$ and $b$ with full weight, and old data are never forgotten.
- **Order independent for $\lambda = 0$.** The sums do not depend on the order of the transitions, so LSTD(0) works on any batch of transitions, including shuffled ones.
- **Not robust off-policy.** On data from another policy, the sample $A$ converges to a matrix that need not be positive definite, and the solution can be far from the target. See the [deadly triad](/deadly-triad/).
- **Not suited to changing policies.** LSTD keeps all past data with equal weight. In control, where the policy changes, the statistics must be reset or decayed.

## Variants and improvements

- **LSTD($\lambda$).** Boyan (2002) uses the trace of line L4. LSTD(0) estimates the TD(0) fixed point; LSTD(1) on complete episodes is the least-squares fit to the Monte Carlo returns.
- **Recursive LSTD.** Bradtke and Barto's RLSTD keeps $A^{-1}$ by Sherman-Morrison updates, in $O(d^2)$ per step.
- **LSPE.** Least-squares policy evaluation takes a step toward the solution of a least-squares problem in each iteration, instead of solving $A\theta = b$ (Nedić and Bertsekas 2003).
- **LSTD-Q and LSPI.** Use features $\phi(s, a)$ and the next action from the policy being evaluated. Least-squares policy iteration alternates LSTD-Q with greedy policy improvement (Lagoudakis and Parr 2003).
- **Regularized LSTD.** Add an $\ell_2$ or $\ell_1$ penalty when $d$ is large compared with the data.
- **iLSTD.** Incremental LSTD updates only a few components of $\theta$ per step to reduce the cost toward $O(d)$ when features are sparse.

## When to use it

Use LSTD for policy evaluation with up to a few hundred features, when data are expensive and you want the best estimate from a fixed batch with no step size to tune. Use plain [temporal difference learning](/temporal-difference-learning/) when $d$ is large, as with neural networks, or when the policy keeps changing. Use [gradient temporal difference](/gradient-temporal-difference/) methods when the data are off-policy.

## Pitfalls

- **A singular sample matrix.** With few transitions, or features that do not vary over the data, the sample $A$ is singular. Use $\epsilon > 0$, and remember that it biases the answer toward $0$.
- **The ridge term in recursive LSTD.** $B_0 = \epsilon^{-1}I$ is not the inverse of the empty sum. Recursive LSTD equals batch LSTD with $\epsilon I$ added, not plain LSTD.
- **Terminal states.** The features of a terminal state must be $0$, and the trace must be reset before the next episode, or the sums mix episodes.
- **Numerical error.** Repeated Sherman-Morrison updates in floating point can lose symmetry and accuracy over long runs. Recompute $A^{-1}$ from $A$ from time to time if the run is long.

## Implementations

## History

Bradtke and Barto (1996) derived LSTD as an instrumental variables method for the TD equations and gave the recursive version RLSTD with Sherman-Morrison updates. They proved convergence with probability one for $\lambda = 0$. Boyan (1999) extended the method to LSTD($\lambda$) with eligibility traces and showed that LSTD(1) reduces to least-squares regression on the returns; his 2002 technical update in Machine Learning is the standard reference. Lagoudakis and Parr (2003) built least-squares policy iteration on the action value version.

## References
