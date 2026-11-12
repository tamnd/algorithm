---
tag: N3XXFK
kind: algorithm
slug: exp3
name: EXP3
aliases:
- exponential weights for exploration and exploitation
- Exp3 algorithm
area: machine-learning/reinforcement-learning
level: advanced
summary: "Keep exponential weights on the arms, mix in uniform exploration, and update only the pulled arm with reward over probability. Regret O(sqrt(nK log K)) against any fixed reward table."
solves: [multi-armed-bandit]
model: real-ram
complexity:
  vars: {n: the number of rounds, K: the number of arms}
  time: {worst: "Θ(n·K)"}
  space: {extra: "Θ(K)"}
  regret: {expected: "O(sqrt(n K log(K)))"}
properties: {online: true, deterministic: false, recursive: false}
history:
  year: 2002
  people: [Peter Auer, Nicolo Cesa-Bianchi, Yoav Freund, Robert E. Schapire]
  note: A conference version appeared at FOCS 1995. The journal paper gives Exp3, its bound, and the matching lower bound of order sqrt(nK).
prereqs: [multi-armed-bandit, multiplicative-weights-update]
see_also: [expert-problem, weighted-majority, oblivious-adversary, adaptive-adversary, doubling-trick, ucb1, thompson-sampling, contextual-bandit]
sources:
  - paper: doi:10.1137/S0097539701398375
    title: Peter Auer, Nicolo Cesa-Bianchi, Yoav Freund and Robert E. Schapire, The nonstochastic multiarmed bandit problem, SIAM Journal on Computing 32(1), 2002
    locator: pp. 48 to 77; Section 3 (Figure 1, Exp3; Theorem 3.1 and Corollary 3.2); Section 4 (the doubling version Exp3.1); Section 5 (Theorem 5.1, the lower bound)
  - paper: doi:10.1561/2200000024
    title: Sebastien Bubeck and Nicolo Cesa-Bianchi, Regret analysis of stochastic and nonstochastic multi-armed bandit problems, Foundations and Trends in Machine Learning 5(1), 2012
    locator: Chapter 3 (Section 3.1 Exp3, Theorem 3.4 the minimax lower bound)
  - book: isbn:9781108486828
    title: Tor Lattimore and Csaba Szepesvari, Bandit Algorithms, Cambridge University Press, 2020
    locator: Chapter 11 (Exp3, Theorem 11.1; Section 11.2 importance-weighted estimators) and Chapter 15 (the minimax lower bound)
---

EXP3 is an algorithm for the adversarial [multi-armed bandit](/multi-armed-bandit/), where the rewards are any fixed table, not draws from fixed distributions. It keeps a weight on each arm and pulls arm $i$ with probability $(1-\gamma)w_i/W + \gamma/K$: a mix of the exponential weights of [multiplicative weights](/multiplicative-weights-update/) and uniform exploration. Only the reward of the pulled arm is seen, so EXP3 feeds the weights an unbiased estimate: the reward divided by the probability of the pull, for the pulled arm, and 0 for the others. Auer, Cesa-Bianchi, Freund and Schapire (2002) proved that its expected [regret](/regret/) against the best fixed arm is at most $2\sqrt{e-1}\sqrt{gK\ln K}$ when $g \ge G_{\max}$, so $O(\sqrt{nK\log K})$, and that no algorithm can do better than order $\sqrt{nK}$.

## In plain words

Give each machine a score, and start all scores equal. Each round, pick a machine at random, with a better chance for machines with high scores, but with a small chance for every machine. After the play, raise the score of the machine that you played. Raise it by the payout divided by the chance that you had of picking it.

The division is the key step. A machine that you seldom pick gets a large raise when you do pick it and it pays, so on average every machine gets the raise it would have had if you had seen all payouts. The small chance for every machine keeps the division from blowing up. No one can fool this rule by hiding rewards, because the choice is random.

## The problem

The input is a number of arms $K \ge 2$, a horizon $n$, and a reward table $x_t(i) \in [0,1]$ for rounds $t \le n$ and arms $i \le K$, fixed in advance by an [oblivious adversary](/oblivious-adversary/). In round $t$ the player picks $A_t$ and sees only $x_t(A_t)$. With $G_i = \sum_{t=1}^{n} x_t(i)$, $G_{\max} = \max_i G_i$ and $G = \sum_t x_t(A_t)$, the goal is small regret $G_{\max} - \mathbb{E}[G]$, where the expectation is over the random choices of the player. Since the table is arbitrary, a deterministic player can be beaten: the adversary can set a reward of 0 on each arm that it will pull.

## The algorithm

```pseudo id=main
EXP3(K, n, γ)                  ▷ 0 < γ ≤ 1
L1  for i ← 1 to K do w[i] ← 1
L2  for t ← 1 to n do
L3      for i ← 1 to K do p[i] ← (1 − γ) · w[i] / (w[1] + … + w[K]) + γ / K
L4      draw A from 1 .. K with Pr[A = i] = p[i]
L5      pull arm A and observe the reward X ∈ [0, 1]
L6      X̂ ← X / p[A]               ▷ the estimate of x_t(i) is X̂ for i = A and 0 for the others
L7      w[A] ← w[A] · exp(γ · X̂ / K)
```

The estimate $\hat x_t(i) = x_t(i)\,\mathbb{1}\{A_t = i\}/p_t(i)$ is unbiased: $\mathbb{E}_t[\hat x_t(i)] = p_t(i) \cdot x_t(i)/p_t(i) = x_t(i)$. The arms not pulled have estimate 0, so their weights do not change. The term $\gamma/K$ keeps $p_t(i) \ge \gamma/K$, so $\hat x_t(i) \le K/\gamma$ and the exponent $\gamma\hat x_t(i)/K$ is at most 1, which the proof needs. Corollary 3.2 of the paper sets

$$\gamma = \min\Big\{1,\ \sqrt{\frac{K\ln K}{(e-1)\,g}}\Big\}$$

for a known $g \ge G_{\max}$; $g = n$ always works. In code, keep $\ln w[i]$ and subtract the largest one before line L3, or the weights overflow.

## Example

Take $K = 3$, $\gamma = 0.3$, the reward table below, and `random.Random(2)` for the draws. The columns list $p$ at the start of the round, the arm pulled, its reward and $\hat X$.

| $t$ | $x_t$ | $p[1]$ | $p[2]$ | $p[3]$ | arm | $X$ | $\hat X$ |
|---|---|---|---|---|---|---|---|
| 1 | 1, 0, 0 | 0.333 | 0.333 | 0.333 | 3 | 0 | 0 |
| 2 | 0, 1, 1 | 0.333 | 0.333 | 0.333 | 3 | 1 | 3.000 |
| 3 | 1, 0, 1 | 0.309 | 0.309 | 0.382 | 1 | 1 | 3.237 |
| 4 | 0, 1, 0 | 0.359 | 0.288 | 0.353 | 1 | 0 | 0 |
| 5 | 1, 1, 0 | 0.359 | 0.288 | 0.353 | 3 | 0 | 0 |
| 6 | 0, 0, 1 | 0.359 | 0.288 | 0.353 | 3 | 1 | 2.831 |

In round 2, arm 3 pays 1 with probability $1/3$ of being pulled, so $\hat X = 3$ and $w[3]$ becomes $e^{0.3 \cdot 3/3} = e^{0.3} \approx 1.350$. Then $p[3] = 0.7 \cdot 1.350/3.350 + 0.1 \approx 0.382$. In round 3, arm 1 pays 1 and had probability $0.309$, so its estimate is $3.237$, larger than the 3 of arm 3, and its weight passes that of arm 3. A pull with reward 0 changes nothing. The rewards of arm 2 are never seen, so its weight stays 1, and its probability falls only because the others rise.

**Regret on a trap sequence.** Take $K = 3$. In the first tenth of the rounds only arm 3 pays, 1 in each round. After that, arm 1 pays in 3 of each 5 rounds, arm 2 in 1 of each 2, and arm 3 in 2 of each 5. So arm 1 is best overall, but a player that trusts the start picks arm 3. With $\gamma$ from Corollary 3.2 and $g = n$, the mean regret over the seeds 0 to 19 is 46.9, 137.3 and 344.9 at $n = 1000$, 4000 and 16000, against bounds of 150.5, 301.0 and 602.0.

## Correctness

**Theorem** (Auer, Cesa-Bianchi, Freund and Schapire 2002, Theorem 3.1 and Corollary 3.2). For each $K \ge 2$, each $\gamma \in (0,1]$ and each reward table in $[0,1]$ fixed in advance,

$$G_{\max} - \mathbb{E}[G] \le (e-1)\,\gamma\, G_{\max} + \frac{K\ln K}{\gamma}.$$

With $g \ge G_{\max}$ and $\gamma$ as above, $G_{\max} - \mathbb{E}[G] \le 2\sqrt{e-1}\sqrt{gK\ln K} \le 2.63\sqrt{gK\ln K}$.

The proof tracks the total weight $W_t$. It grows by a factor that is at most $1$ plus a multiple of the reward $X$ of the round, plus a second order term, by $e^z \le 1 + z + (e-2)z^2$ for $z \le 1$. It is also at least the weight of the best arm, which is $e^{(\gamma/K)\sum_t \hat x_t(j)}$. Comparing the two and taking expectations, with the unbiased estimates, gives the theorem. The [proof page](proofs/correctness.md) gives it in full.

**Lower bound** (same paper, Theorem 5.1). For each $K \ge 2$ and $n$ there is a random reward table such that each player has expected regret at least $\frac{1}{20}\min(\sqrt{nK}, n)$. So EXP3 is optimal up to the factor $\sqrt{\ln K}$.

## Complexity

- **Time.** Lines L3 and L4 take $\Theta(K)$ per round, so the run takes $\Theta(nK)$. Since only one weight changes per round, a sum tree over the weights gives $O(\log K)$ per round.
- **Space.** $\Theta(K)$ for the weights.
- **Regret.** $O(\sqrt{nK\log K})$ with $g = n$. If $n$ is not known, the doubling version Exp3.1 of the paper, in the style of the [doubling trick](/doubling-trick/), has bound $8\sqrt{e-1}\sqrt{G_{\max}K\ln K} + 8(e-1)K + 2K\ln K$.

## Properties

- **No statistical assumption.** The bound holds for every reward table, including tables that change over time and tables built to fool the player.
- **Randomized by need.** Each deterministic player has linear regret against some table, so randomization is required.
- **Expectation only.** The bound is on the expected regret. The estimates $\hat X$ can be as large as $K/\gamma$, so the regret of one run varies a lot. Exp3.P, in the same paper, has a bound that holds with high probability.
- **Weak on easy problems.** On a stochastic bandit with a large gap, EXP3 still explores at rate $\gamma$ and has regret of order $\sqrt{n}$, while [UCB1](/ucb1/) has order $\log n$.

## Variants and improvements

- **Exp3 with no forced exploration.** Lattimore and Szepesvari (Theorem 11.1) analyse $p_t(i) \propto \exp(\eta\hat S_{t-1}(i))$ with $\gamma = 0$, using the loss form of the estimator; with $\eta = \sqrt{\ln K/(nK)}$ the regret is at most $2\sqrt{nK\ln K}$.
- **Exp3.P.** Adds an upper confidence term to the estimates, and bounds the regret with high probability. Bounds of this kind are the usual route to guarantees against an [adaptive adversary](/adaptive-adversary/).
- **Exp3.S.** Shares weight between arms and competes with sequences of arms that switch a bounded number of times.
- **Exp4.** Runs exponential weights over experts, each of which gives a distribution over the arms; it is the base of many [contextual bandit](/contextual-bandit/) methods.
- **Implicit exploration (Exp3-IX) and Tsallis-INF.** Bias the estimator to cut its variance, or replace the exponential weights by another regularizer. Tsallis-INF has $O(\sqrt{nK})$ regret against adversaries and $O(\log n)$ on stochastic bandits.

## When to use it

Use EXP3 when the rewards may change over time in ways that no model captures, or may be chosen by someone who reacts to past behavior, such as in games, security and online pricing against strategic users. When the rewards are i.i.d., [UCB1](/ucb1/) and [Thompson sampling](/thompson-sampling/) have much smaller regret. When all rewards are seen each round, use the full information [expert problem](/expert-problem/) methods such as [weighted majority](/weighted-majority/).

## Pitfalls

- **Overflow of the weights.** $\hat X$ can be as large as $K/\gamma$, and the weights grow without limit. Keep logarithms.
- **$\gamma$ too small.** With $\gamma$ near 0 and no other control, $\hat X$ has huge variance. Use the formula of Corollary 3.2, or a variant built for $\gamma = 0$.
- **Updating all arms.** Arms that were not pulled must get estimate 0, not their last reward. Any other value makes the estimate biased.
- **Rewards outside $[0,1]$.** The step $e^z \le 1 + z + (e-2)z^2$ needs $z \le 1$. Scale the rewards first.
- **Comparing with the wrong benchmark.** The bound is against the best single arm in hindsight. If the best arm changes over time, use Exp3.S.

## Implementations

## History

Auer, Cesa-Bianchi, Freund and Schapire presented the nonstochastic bandit problem and EXP3 at FOCS 1995, and the full journal version appeared in the SIAM Journal on Computing in 2002. It joined two lines of work: the exponential weights of the [weighted majority](/weighted-majority/) and Hedge algorithms for full information, and the bandit problem with partial feedback. The paper also gave the lower bound of order $\sqrt{nK}$, Exp3.P for high probability bounds, and Exp4 for experts. Audibert and Bubeck (2009) removed the $\sqrt{\log K}$ factor with the INF policy.

## References
