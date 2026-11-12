---
tag: WSWCCF
kind: algorithm
slug: monte-carlo-policy-evaluation
name: Monte Carlo policy evaluation
aliases:
- first-visit Monte Carlo
- every-visit Monte Carlo
- Monte Carlo prediction
area: machine-learning/reinforcement-learning
level: intro
summary: "Estimate the value of a fixed policy by running full episodes and averaging, for each state, the returns that follow its visits. First-visit averaging is unbiased."
solves: [policy-evaluation]
model: real-ram
complexity:
  vars: {T: the total number of steps in all episodes, S: the number of states, L: the length of the longest episode}
  time: {worst: "O(T)"}
  space: {extra: "O(S + L)"}
properties: {deterministic: true, online: false, exact: false, recursive: false}
history:
  year: 1996
  people: [Satinder Singh, Richard S. Sutton]
  note: Singh and Sutton named and compared the first-visit and the every-visit estimators and related them to TD(1) with replacing and accumulating traces.
prereqs: [state-value-function, discounted-return, monte-carlo-integration, law-of-large-numbers]
see_also: [monte-carlo-control, temporal-difference-learning, iterative-policy-evaluation, td-lambda, eligibility-traces, importance-sampling-off-policy, n-step-td]
sources:
  - book: isbn:9780262039246
    title: Richard S. Sutton and Andrew G. Barto, Reinforcement Learning, An Introduction, second edition, MIT Press, 2018
    locator: Section 5.1 (Monte Carlo prediction, first-visit and every-visit) and Section 6.3 (batch Monte Carlo against batch TD(0))
  - paper: "Satinder P. Singh and Richard S. Sutton, Reinforcement learning with replacing eligibility traces, Machine Learning 22, 1996, pages 123 to 158"
    locator: the section on Monte Carlo algorithms and the bias and variance analysis of the first-visit and every-visit estimators
  - book: isbn:9781886529106
    title: Dimitri P. Bertsekas and John N. Tsitsiklis, Neuro-Dynamic Programming, Athena Scientific, 1996
    locator: Chapter 5 (Monte Carlo simulation for the evaluation of a policy)
---

Monte Carlo policy evaluation estimates the [state value function](/state-value-function/) $V^\pi$ of a fixed [policy](/policy/) $\pi$ in an unknown episodic [Markov decision process](/markov-decision-process/). It runs complete episodes with $\pi$ and sets $V(s)$ to the average of the [discounted returns](/discounted-return/) that follow the visits to $s$. The first-visit version uses only the return after the first visit in each episode, and its estimate is an unbiased sample mean; the every-visit version uses all visits and is biased but consistent. It is the [Monte Carlo integration](/monte-carlo-integration/) of the return, applied to the [policy evaluation](/policy-evaluation/) problem without a model.

## In plain words

You want to know how good each position of a game is when you play with a fixed strategy. You do not know the rules in detail, but you can play. So you play many full games. After each game you go back over it. For each position that you passed through, you add up the rewards that came after it until the end of the game. The value of a position is the average of these sums over all games.

If a position occurs twice in one game, you can count only its first occurrence, or count both. The first choice gives an average that is right on average after any number of games. The second choice uses more data but is a little wrong after few games. Both become right as the number of games grows.

## The problem

The setting is an unknown MDP $(S, A, P, R, \gamma)$ with a terminal state, and a fixed policy $\pi$ under which each episode ends with probability 1. We can only sample episodes $S_0, A_0, R_1, S_1, A_1, R_2, \ldots, S_{T-1}, A_{T-1}, R_T$, where $S_T$ is terminal and $T$ is random. The criterion is the discounted return with $0 \le \gamma \le 1$; $\gamma = 1$ is allowed because episodes end. The return from time $t$ is

$$G_t = R_{t+1} + \gamma R_{t+2} + \cdots + \gamma^{T-t-1} R_T,$$

and the goal is $V^\pi(s) = \mathbb{E}_\pi[G_t \mid S_t = s]$ for each state $s$ that $\pi$ visits. Rewards are bounded. The actions play no role in the estimate, so an episode is written as the pairs $(S_t, R_{t+1})$.

## The algorithm

```pseudo id=main
MC-POLICY-EVALUATION(episodes, γ, first_visit)
L1  N(s) ← 0 and V(s) ← 0 for each state s
L2  for each episode (S_0, R_1), (S_1, R_2), ..., (S_{T−1}, R_T) do
L3      first(s) ← the least t with S_t = s, for each s in the episode
L4      G ← 0
L5      for t ← T − 1 down to 0 do
L6          G ← γ G + R_{t+1}                        ▷ now G = G_t
L7          if first_visit and first(S_t) < t then continue
L8          N(S_t) ← N(S_t) + 1
L9          V(S_t) ← V(S_t) + (G − V(S_t)) / N(S_t)    ▷ running mean
L10 return V, N
```

The loop of line L5 walks the episode backward, so line L6 computes every return $G_t$ with one multiply and one add, from $G_t = R_{t+1} + \gamma G_{t+1}$. Line L7 skips the later visits of a state in the first-visit version. Line L9 keeps the running mean of the returns counted so far, so the algorithm stores no list of returns. Line L3 costs one pass over the episode with a hash map, and it replaces the search "does $S_t$ occur in $S_0, \ldots, S_{t-1}$" of the textbook form, which costs $O(T^2)$ per episode.

## Example

Take two states A and B, $\gamma = 1$, and two episodes, written as (state, next reward):

- episode 1: (A, 3), (A, 2), (B, −4), (A, 4), (B, −3)
- episode 2: (B, −2), (A, 3), (B, −3)

The backward pass of line L6 gives the returns:

| episode | $t$ | $S_t$ | $R_{t+1}$ | $G_t$ | first visit? |
| --- | --- | --- | --- | --- | --- |
| 1 | 4 | B | −3 | −3 | no |
| 1 | 3 | A | 4 | 1 | no |
| 1 | 2 | B | −4 | −3 | yes |
| 1 | 1 | A | 2 | −1 | no |
| 1 | 0 | A | 3 | 2 | yes |
| 2 | 2 | B | −3 | −3 | no |
| 2 | 1 | A | 3 | 0 | yes |
| 2 | 0 | B | −2 | −2 | yes |

First-visit averages: $V(\mathrm{A}) = (2 + 0)/2 = 1$ and $V(\mathrm{B}) = (-3 - 2)/2 = -5/2$. Every-visit averages: $V(\mathrm{A}) = (1 - 1 + 2 + 0)/4 = 1/2$ and $V(\mathrm{B}) = (-3 - 3 - 3 - 2)/4 = -11/4$. After episode 1 alone, first-visit gives $V(\mathrm{A}) = 2$ and every-visit gives $V(\mathrm{A}) = 2/3$. The two versions differ only when a state repeats in an episode.

**The bias of every-visit.** Take one state $s$ with reward 1 on each step, where the episode goes on with probability $p$ and ends with probability $1 - p$. The number $k$ of visits is geometric with mean $1/(1-p)$, so $V^\pi(s) = 1/(1-p)$. The first-visit estimate from one episode is $k$, with mean $1/(1-p)$. The every-visit estimate from one episode is $(k + (k-1) + \cdots + 1)/k = (k+1)/2$, with mean $(1/(1-p) + 1)/2$. For $p = 1/2$ the true value is 2, and the every-visit mean is $3/2$. In the same case, after one episode the mean squared error is 2 for first-visit and $3/4$ for every-visit. After $n$ episodes, $n$ times the mean squared error tends to 2 for first-visit and to 3 for every-visit (by the delta method for the ratio of sums). So here every-visit has the smaller error after one episode, and first-visit has the smaller error in the long run.

## Correctness

**First-visit is unbiased and consistent.** Let $\tau$ be the time of the first visit to $s$ in an episode. It is a stopping time, so by the strong Markov property the process after $\tau$ is a new run of $\pi$ from $s$, independent of the past. So the counted returns of $s$, one per episode that visits $s$, are independent and identically distributed with mean $V^\pi(s)$. Line L9 keeps their sample mean, which is unbiased for every $N(s) \ge 1$ and converges to $V^\pi(s)$ with probability 1 by the strong [law of large numbers](/law-of-large-numbers/). Its standard error falls as $\sigma_s / \sqrt{N(s)}$, where $\sigma_s^2$ is the [variance](/variance/) of the return from $s$.

**Every-visit is consistent.** The estimate is the ratio of the sum of all returns of $s$ to the number of visits to $s$. By the Markov property at each fixed time, the expected sum of the returns in one episode is $V^\pi(s)$ times the expected number of visits. The law of large numbers applied to the top and the bottom of the ratio gives convergence to $V^\pi(s)$ with probability 1. The ratio is biased for a fixed number of episodes, as the example shows. The full proofs are in the proofs section.

## Complexity

Each step of an episode costs $O(1)$ arithmetic operations in lines L3, L6 and L9, with expected $O(1)$ hash map operations. So the total time is $O(T)$, where $T$ is the total number of steps of all episodes. The memory is $O(|S|)$ for $V$ and $N$, plus $O(L)$ to hold the longest episode, since the backward pass needs the whole episode. The method needs no model, and the cost of one update does not depend on $|S|$, unlike a sweep of [iterative policy evaluation](/iterative-policy-evaluation/).

The number of episodes for a given accuracy depends on the variance of the returns. By Chebyshev's inequality, $N(s) \ge \sigma_s^2 / (\varepsilon^2 \delta)$ first visits give $|V(s) - V^\pi(s)| < \varepsilon$ with probability at least $1 - \delta$; with returns in a bounded range $[a, b]$, the [Hoeffding inequality](/hoeffding-inequality/) gives $N(s) \ge (b-a)^2 \ln(2/\delta) / (2\varepsilon^2)$. Both are worst-case bounds for the first-visit estimator. The variance grows with the episode length and with $\gamma$.

## Properties

- **Model free.** It uses sampled episodes only, not $P$ or $R$.
- **No bootstrapping.** The estimate of a state does not use the estimates of other states. So it is not hurt by wrong estimates elsewhere, and a state can be evaluated alone.
- **Offline within an episode.** The updates wait for the end of the episode, because the return is not known before.
- **Robust to non-Markov states.** Episodes are independent, so first-visit MC still converges to the expected return after the first visit when the state signal is not Markov. It never uses the estimate of a next state.
- **Batch optimality.** On a fixed batch of episodes, every-visit MC with repeated presentation converges to the values that minimize the mean squared error to the observed returns, while batch [TD(0)](/temporal-difference-learning/) converges to the certainty-equivalence estimate (Sutton and Barto, Section 6.3).

## Variants and improvements

- **Constant step size.** Replace $1/N(S_t)$ in line L9 by a constant $\alpha$. This tracks a nonstationary policy, but the estimate keeps a variance of order $\alpha$. With steps that meet the [Robbins-Monro conditions](/robbins-monro-conditions/) it still converges.
- **Action values.** Average the returns that follow the pairs $(S_t, A_t)$ to estimate $Q^\pi$. This is the evaluation step of [Monte Carlo control](/monte-carlo-control/).
- **Off-policy evaluation.** Weight each return by the ratio of the target and behavior probabilities of the actions after the visit. This is [importance sampling for off-policy learning](/importance-sampling-off-policy/).
- **Traces.** Offline TD(1) with accumulating traces makes the same total update as constant-$\alpha$ every-visit MC, and with replacing traces the same as first-visit MC (Singh and Sutton 1996). See [eligibility traces](/eligibility-traces/) and [TD(λ)](/td-lambda/).
- **Bootstrapped targets.** [Temporal-difference learning](/temporal-difference-learning/) and [n-step TD](/n-step-td/) replace the tail of the return by a value estimate. They update during the episode and often have lower variance.

## When to use it

Use Monte Carlo evaluation when episodes are short or moderate, when you can simulate the policy but have no model, or when the state signal may not be Markov. It is also the simplest unbiased baseline to test other estimators against. Prefer [TD learning](/temporal-difference-learning/) when episodes are long or do not end, since MC must wait for the end and its variance grows with the length. Prefer [iterative policy evaluation](/iterative-policy-evaluation/) when the model is known and the state space is small.

## Pitfalls

- **Forward computation of the returns.** Summing the rewards forward from each $t$ costs $O(T^2)$ per episode. Compute $G$ backward as in line L6.
- **A search for the first visit.** Testing "is $S_t$ in $S_0, \ldots, S_{t-1}$" by a scan in line L7 also costs $O(T^2)$. Use the index of line L3.
- **Mixing the two versions.** A program that sets $V$ to the first-visit return and also counts later visits in $N$ is neither estimator. Lines L8 and L9 must use the same test as line L7.
- **Episodes that do not end.** With $\gamma = 1$ and a policy that can loop forever, the return is undefined. Make sure the policy is proper, or use $\gamma < 1$ with a horizon long enough that $\gamma^H$ times the reward bound is negligible.
- **Unvisited states.** States that $\pi$ never reaches get no estimate. The value 0 of line L1 is not an estimate for them.

## Implementations

## History

Monte Carlo estimation of expected returns is old, and Bertsekas and Tsitsiklis treat simulation-based policy evaluation in their 1996 book. Singh and Sutton (1996) named the first-visit and the every-visit estimators, showed that the every-visit one is biased and the first-visit one is not, and showed that offline TD(1) with accumulating and with replacing traces equals the every-visit and the first-visit method. Sutton and Barto present first-visit MC prediction as the first model-free method of their book.

## References
