---
tag: 7M9CFD
kind: algorithm
slug: gittins-index
name: Gittins index
aliases:
- Gittins index policy
- dynamic allocation index
area: machine-learning/reinforcement-learning
level: research
summary: "Give each arm in each state the best discounted reward per unit of discounted time it can earn before a stopping time. Pulling the arm with the largest index is optimal."
solves: [multi-armed-bandit]
model: real-ram
complexity:
  vars: {m: the number of states of an arm, L: the number of value iteration sweeps}
  time: {worst: "O(m^3 · L)"}
  space: {extra: "Θ(m)"}
properties: {online: true, deterministic: true, recursive: false}
history:
  year: 1974
  people: [John C. Gittins, David M. Jones]
  note: Gittins and Jones announced the index theorem in 1974, and Gittins gave the full account in 1979. Whittle (1980) gave the retirement proof, and Katehakis and Veinott (1987) the restart formula.
prereqs: [multi-armed-bandit, markov-decision-process, value-iteration, discounted-return]
see_also: [thompson-sampling, exploration-exploitation-tradeoff, bayesian-inference, markov-chain, policy-iteration, bellman-optimality-equation, ucb1]
sources:
  - paper: doi:10.1111/j.2517-6161.1979.tb01068.x
    title: John C. Gittins, Bandit processes and dynamic allocation indices, Journal of the Royal Statistical Society Series B 41(2), 1979
    locator: pp. 148 to 177; the index theorem for families of alternative bandit processes, and the tables of indices for Bernoulli arms
  - paper: doi:10.1111/j.2517-6161.1980.tb01111.x
    title: Peter Whittle, Multi-armed bandits and the Gittins index, Journal of the Royal Statistical Society Series B 42(2), 1980
    locator: pp. 143 to 149; the retirement option and the proof of optimality
  - paper: doi:10.1287/moor.12.2.262
    title: Michael N. Katehakis and Arthur F. Veinott Jr., The multi-armed bandit problem, decomposition and computation, Mathematics of Operations Research 12(2), 1987
    locator: pp. 262 to 268; the restart-in-state problem
  - paper: doi:10.1214/aoap/1177005588
    title: Richard Weber, On the Gittins index for multiarmed bandits, Annals of Applied Probability 2(4), 1992
    locator: pp. 1024 to 1033; the proof by prevailing charges
  - book: isbn:9780470670026
    title: John Gittins, Kevin Glazebrook and Richard Weber, Multi-armed Bandit Allocation Indices, second edition, Wiley, 2011
    locator: Chapter 2 (the index theorem and its proofs)
  - book: isbn:9781108486828
    title: Tor Lattimore and Csaba Szepesvari, Bandit Algorithms, Cambridge University Press, 2020
    locator: Chapter 35, Section 35.4 (the Gittins index, Theorem 35.9) and Section 35.5 (computing the index)
---

The Gittins index is a number attached to each state of each arm of a Markov bandit. The model has $K$ arms, each a Markov chain with rewards. In each round the player pulls one arm, receives a reward that depends on the state of that arm, and only that arm changes state; rewards are discounted by $\gamma < 1$ per round. The index of a state $x$ is the best ratio of expected discounted reward to expected discounted time that the arm can earn from $x$ before a stopping time. Gittins and Jones (1974) and Gittins (1979) proved that the policy that always pulls the arm with the largest index is optimal. This turns one [Markov decision process](/markov-decision-process/) on the product of all state spaces into $K$ small problems, one per arm. A Bayesian bandit is a special case: the state of an arm is its posterior.

## In plain words

You own several projects. Each week you can work on one of them, and it pays you something and then changes. The others wait as they are. Money now is worth more than money later.

For each project, ask: if I work on this one alone, and stop at the best moment, what is the best average pay per week, with later weeks counted for less? That number is the project's index. It depends only on that project. The rule is simple: each week, work on the project with the largest index. Gittins proved that no plan does better. An uncertain project gets a high index, because if it turns out well you keep at it, and if it turns out badly you stop.

## The problem

An arm is a finite Markov chain: a set of states $\{0, \ldots, m-1\}$, a reward $r(x)$ for a pull in state $x$, and transition probabilities $P(x, y)$. The input is $K$ such arms, their start states, and a discount $\gamma \in (0, 1)$. In round $t = 0, 1, 2, \ldots$ the player picks an arm $A_t$, receives $r(x_{A_t})$, and that arm moves by $P$; the other arms keep their states. The goal is a policy that maximizes $\mathbb{E}[\sum_{t\ge0}\gamma^t r_{A_t}(x_{A_t}(t))]$, the [discounted return](/discounted-return/).

The **Gittins index** of state $x$ of an arm is

$$\nu(x) = \sup_{\tau \ge 1}\frac{\mathbb{E}_x\big[\sum_{t=0}^{\tau-1}\gamma^t r(X_t)\big]}{\mathbb{E}_x\big[\sum_{t=0}^{\tau-1}\gamma^t\big]},$$

where $X_0 = x, X_1, \ldots$ is the chain of that arm alone, and $\tau$ ranges over stopping times with $\tau \ge 1$, including $\tau = \infty$.

## The algorithm

The index of each state comes from the restart problem of Katehakis and Veinott (1987). In the restart problem for state $x$, in each state $y$ the player may either pull the arm from $y$, or restart: jump to $x$ and pull from there. Its optimal value $V$ solves

$$V(y) = \max\Big(r(y) + \gamma\sum_z P(y,z)V(z),\ r(x) + \gamma\sum_z P(x,z)V(z)\Big),$$

and $\nu(x) = (1-\gamma)V(x)$. [Value iteration](/value-iteration/) finds $V$.

```pseudo id=main
GITTINS-INDEX(r, P, γ, x)        ▷ index of state x of one arm
L1  V[y] ← 0 for each state y
L2  repeat
L3      R ← r(x) + γ · Σ_z P(x, z) · V[z]            ▷ the value of a restart from x
L4      V[y] ← max(r(y) + γ · Σ_z P(y, z) · V[z], R) for each state y
L5  until the change in V is below (1 − γ) · ε / γ
L6  return (1 − γ) · V[x]

INDEX-POLICY(arms, γ)
    compute ν_k(y) for each arm k and each state y
    in each round pull an arm k with the largest ν_k(current state of k)
```

Two other ways give the same number. Whittle (1980) adds a retirement option: the player may stop and take a lump sum $M$. Then $\nu(x) = (1-\gamma)M^*(x)$, where $M^*(x)$ is the smallest $M$ at which retiring in state $x$ is as good as going on; bisection on $M$ finds it. And for a Bernoulli arm with a $\mathrm{Beta}(a, b)$ posterior, the states are the pairs $(a+s, b+f)$, and the same calibration runs by backward induction over this tree, cut at a large depth.

## Example

**One arm.** Take $\gamma = 0.9$ and an arm with three states. State 0 pays 0 and then moves to state 1 or state 2 with probability $\frac12$ each. State 1 pays 1 once and moves to state 2. State 2 pays 0.2 for ever. The indices of states 1 and 2 are 1 and 0.2: from state 1 the best is to stop after one pull, and state 2 always pays 0.2. For state 0, the best stopping rule is: pull from state 0; if the arm moves to state 1, pull once more and stop; if it moves to state 2, stop. So

$$\nu(0) = \frac{0 + 0.9 \cdot \frac12 \cdot 1}{1 + 0.9 \cdot \frac12} = \frac{0.45}{1.45} = \frac{9}{29} \approx 0.3103.$$

The other rules give less: stopping after one pull gives 0, and stopping after two pulls gives $0.9(0.5 + 0.1)/1.9 \approx 0.284$. Value iteration on the restart problem for state 0 gives these values of $V$:

| sweep | $V(0)$ | $V(1)$ | $V(2)$ | $(1-\gamma)V(0)$ |
|---|---|---|---|---|
| 1 | 0 | 1 | 0.2 | 0 |
| 2 | 0.54 | 1.18 | 0.54 | 0.054 |
| 3 | 0.774 | 1.486 | 0.774 | 0.0774 |
| 4 | 1.017 | 1.6966 | 1.017 | 0.1017 |
| limit | 3.1034 | 3.7931 | 3.1034 | 0.3103 |

In the limit $V(2) = V(0)$: in state 2 the restart is better, which is the rule "stop in state 2". And $V(1) = 1 + 0.9V(0)$: in state 1 the player pulls and then restarts.

**Two arms.** Add a safe arm that pays 0.3 in each round. The myopic rule takes the larger immediate reward, so it pulls the safe arm for ever and gets $0.3/(1-0.9) = 3$. The index of the safe arm is 0.3, and $9/29 > 0.3$, so the index rule first pulls the risky arm, which pays 0. If the risky arm moves to state 1 (index 1), it pulls it again and gets 1, then switches to the safe arm, since $0.2 < 0.3$. The value is $0.9(\frac12(1 + 0.9 \cdot 3) + \frac12 \cdot 3) = 3.015$, which is also the optimal value found by value iteration over the joint states.

**Bernoulli arms.** For a Bernoulli arm with a uniform prior $\mathrm{Beta}(1,1)$, the posterior mean is $0.5$, but the index is $0.7029$ for $\gamma = 0.9$ and $0.8699$ for $\gamma = 0.99$. The difference is the value of learning. Other indices for $\gamma = 0.9$: $\mathrm{Beta}(2,2)$ has $0.6346$, $\mathrm{Beta}(5,5)$ has $0.5676$ and $\mathrm{Beta}(10,10)$ has $0.5373$. With the same mean, a sharper posterior has less to learn, and its index is closer to the mean.

## Correctness

**Theorem** (Gittins and Jones 1974, Gittins 1979; Lattimore and Szepesvari, Theorem 35.9). For arms that are finite Markov chains with bounded rewards, and discount $\gamma \in (0,1)$, the policy that pulls in each round an arm whose current state has the largest index maximizes the expected discounted reward, from every start state.

The algorithm computes the index because of two facts, proved in full on the [proof page](proofs/correctness.md):

- **Restart.** $(1-\gamma)V(x) = \nu(x)$. A policy for the restart problem cuts the run into cycles; each cycle starts at $x$ and ends at a stopping time $\tau$. If one cycle has expected reward $A$ and the discount at its end is $\mathbb{E}[\gamma^\tau]$, the value $C$ satisfies $C = A + \mathbb{E}[\gamma^\tau]C$. Since $1 - \mathbb{E}[\gamma^\tau] = (1-\gamma)\,\mathbb{E}[\sum_{t<\tau}\gamma^t]$, this gives $(1-\gamma)C = A/\mathbb{E}[\sum_{t<\tau}\gamma^t]$, the ratio in the definition.
- **Retirement.** Going on from $x$ beats retiring with $M$ exactly when some $\tau \ge 1$ has ratio above $(1-\gamma)M$.

The proof page also sketches Weber's (1992) proof of the theorem with prevailing charges.

## Complexity

- **Time.** One sweep of line L4 costs $O(m^2)$. The error after $L$ sweeps is at most $\gamma^L$ times the size of $V$, so $L = O(\log(1/\varepsilon)/(1-\gamma))$ sweeps are enough. All $m$ indices cost $O(m^3 L)$. Exact methods, such as the largest-index-first method of Varaiya, Walrand and Buyukkoc (1985), use $O(m^3)$ arithmetic steps for all states.
- **Space.** $\Theta(m)$ for $V$, besides the input matrix.
- **The policy.** The indices of each arm are computed once, alone. A round then costs $O(K)$, or $O(\log K)$ with a heap, since only the pulled arm changes its index. The joint MDP has $m^K$ states; the index policy never builds it.
- **Bernoulli arms.** The tree of posteriors cut at depth $D$ has $\Theta(D^2)$ states, and each bisection step costs $\Theta(D^2)$.

## Properties

- **Decomposition.** The index of an arm depends only on that arm and on $\gamma$, not on the other arms. This is the main point of the theorem.
- **Bayes optimal, not regret optimal.** The policy is optimal for the discounted Bayesian criterion. It is not designed for the frequentist regret over a fixed horizon, and with a fixed $\gamma$ it can stop exploring too early.
- **Fragile assumptions.** The theorem needs geometric discounting, arms that do not move when not pulled, independent arms, one pull per round and no switching costs. If any of these fails, the index policy is in general not optimal.
- **At least the immediate reward.** $\nu(x) \ge r(x)$, from $\tau = 1$, and $\nu(x)$ is at most the largest reward that can be reached from $x$.

## Variants and improvements

- **Whittle index for restless bandits.** When arms change even when not pulled, Whittle (1988) relaxed the constraint of one pull per round with a Lagrange multiplier. The resulting index is optimal only in a limit, and exists only for indexable arms.
- **Finite horizon.** With a horizon $n$ in place of discounting, the index rule is not optimal. Indices with a horizon that shrinks with the remaining rounds are a good heuristic, and Lattimore (2016) analysed a regret-optimal version.
- **Branching bandits and scheduling.** The same idea gives the $c\mu$ rule for queues and Klimov's rule, as special cases of index policies.
- **Approximate indices for Bernoulli arms.** Tables, interpolation in $\gamma$, and closed-form approximations are used when the tree is too large.

## When to use it

Use the Gittins index when the problem really is a discounted Markov bandit: independent arms that change only when used, and a known prior. Examples are scheduling jobs with random lengths, choosing which research project to fund, and Bayesian clinical trials with discounting. When the criterion is regret over a horizon, or the prior is not known, [Thompson sampling](/thompson-sampling/) or [UCB1](/ucb1/) are simpler and have frequentist guarantees.

## Pitfalls

- **Using the posterior mean as the index.** The index includes the value of learning. The myopic rule that compares means is not optimal, as the two-arm example shows.
- **Arms that move when not pulled.** Then the problem is a restless bandit, and the index policy can be far from optimal.
- **Stopping value iteration too early.** The convergence rate is $\gamma$ per sweep, which is slow for $\gamma$ near 1. Bound the error by $\gamma/(1-\gamma)$ times the last change, as in line L5.
- **Truncating the Bernoulli tree too early.** For $\gamma = 0.99$ the depth must be in the hundreds, or the index is too small.
- **Restart from the wrong state.** The restart in line L3 goes to $x$, the state whose index is computed, not to the current state.

## Implementations

## History

Bellman (1956) studied a Bayesian bandit by dynamic programming, and the problem was long thought to be intractable for many arms. Gittins and Jones presented the index theorem at a meeting in 1972, published in 1974, and Gittins gave the full theory and tables of indices for Bernoulli arms in his 1979 paper read to the Royal Statistical Society. Whittle (1980) gave a short proof with the retirement option, Varaiya, Walrand and Buyukkoc (1985) and Katehakis and Veinott (1987) gave ways to compute the index, and Weber (1992) gave the proof by prevailing charges, which is now the standard one.

## References
