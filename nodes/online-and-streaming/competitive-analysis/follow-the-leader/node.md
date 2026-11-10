---
tag: DKX8AG
kind: algorithm
slug: follow-the-leader
name: Follow the leader
aliases:
- FTL
- follow the perturbed leader
- FTPL
- fictitious play
area: online-and-streaming/competitive-analysis
level: advanced
summary: Play the action with the least total loss so far. It has linear regret on alternating losses; adding random noise to the totals (FTPL) gives regret O(sqrt(T)).
solves: [expert-problem]
model: real-ram
complexity:
  vars: {n: the number of experts, T: the number of rounds}
  time: {worst: Θ(n·T)}
  space: {extra: Θ(n)}
properties: {online: true, deterministic: true, comparison: false, recursive: false}
history:
  year: 2005
  people: [Adam Kalai, Santosh Vempala]
  note: Follow the leader is the oldest online rule, as fictitious play (Brown 1951); Hannan (1957) added random perturbations, and Kalai and Vempala (2005) gave the simple analysis of follow the perturbed leader for linear losses.
prereqs: [expert-problem, regret]
see_also: [multiplicative-weights-update, weighted-majority, online-convex-optimization, online-gradient-descent, regularization, strong-convexity, randomized-online-algorithm, oblivious-adversary]
sources:
  - paper: doi:10.1016/j.jcss.2004.10.016
    title: "Adam Kalai and Santosh Vempala, Efficient algorithms for online decision problems, Journal of Computer and System Sciences 71(3) (2005), 291-307"
    locator: Section 1 (the failure of follow the leader on alternating losses), Section 2 (the be-the-leader lemma and Theorem 1.1, the bound epsilon R A T + D / epsilon for FPL) and the applications to shortest paths and other structured problems
  - paper: "James Hannan, Approximation to Bayes risk in repeated play, Contributions to the Theory of Games 3, Annals of Mathematics Studies 39, Princeton University Press, 1957, 97-139"
    locator: the perturbed version of fictitious play and its vanishing average regret
  - book: isbn:9780521841085
    title: Nicolo Cesa-Bianchi and Gabor Lugosi, Prediction, Learning, and Games, Cambridge University Press, 2006
    locator: Chapter 3 (follow the leader and its regret for exp-concave and strongly convex losses) and Chapter 4 (follow the perturbed leader)
  - paper: doi:10.1561/2400000013
    title: "Elad Hazan, Introduction to online convex optimization, Foundations and Trends in Optimization 2(3-4) (2016), 157-325"
    locator: Chapter 5 (follow the leader, the failure example, and follow the regularized leader)
---

Follow the leader (FTL) is the online rule that, in each round, plays the action whose total loss so far is the least. It is natural and it works when the leader rarely changes, as for squared loss, where it has [regret](/regret/) $O(\log T)$; but for linear losses an alternating sequence makes it switch in every round to the expert that is about to lose, so its regret is about $T/2$. Follow the perturbed leader (FTPL) adds random noise to the totals before taking the minimum, and Kalai and Vempala (2005) showed that its expected regret is $O(\sqrt{T})$, for experts $2\sqrt{2nT}$. Both rules rest on the *be-the-leader* lemma: the leader of the next round never loses to the best fixed action.

## In plain words

Each round you choose among some options, and afterwards you learn how much each option lost. The simplest plan is to choose the option that has lost the least so far. This plan is often good, but it can be fooled. If two options take turns in losing, and each takes the lead just before its turn to lose, you always choose the wrong one.

The fix is to add a little random noise to the running totals before you choose. Then the leader you choose does not depend so tightly on the last loss, and an opponent cannot predict your choice well enough to fool you. With the right amount of noise, your total loss is close to that of the best single option.

## The problem

There are $n$ experts and $T$ rounds. In round $t$ the algorithm chooses an expert $i_t$, then the adversary reveals losses $\ell_t \in [0, 1]^n$, and the algorithm pays $\ell_{t,i_t}$. The goal is a small regret $\sum_t \ell_{t,i_t} - \min_i \sum_t \ell_{t,i}$; this is the [expert problem](/expert-problem/). More generally the actions form a set $K$, the losses are functions $\ell_t : K \to \mathbb{R}$, and FTL plays $x_t \in \arg\min_{x \in K} \sum_{s < t} \ell_s(x)$, as in [online convex optimization](/online-convex-optimization/). For FTPL the adversary is [oblivious](/oblivious-adversary/).

## The algorithm

```pseudo id=main
FOLLOW-THE-LEADER(n)
L1  for i ← 1 to n do L[i] ← 0               ▷ total loss of expert i so far
L2  for t ← 1 to T do
L3      i_t ← the least i with L[i] = min_j L[j]
L4      play expert i_t
L5      receive the losses ℓ[1 .. n] and pay ℓ[i_t]
L6      for i ← 1 to n do L[i] ← L[i] + ℓ[i]
```

**Follow the perturbed leader.** Replace line L3 by: draw $p_t$ uniformly from $[0, 1/\varepsilon]^n$, and let $i_t$ minimize $L[i] - p_t[i]$. With $\varepsilon = \sqrt{2/(nT)}$ the expected regret is at most $2\sqrt{2nT}$. For a general set of decisions $\mathcal{D} \subset \mathbb{R}^d$ and linear losses $x \cdot s_t$, FTPL calls an offline optimizer $M$ once per round on the perturbed total $s_1 + \cdots + s_{t-1} + p_t$. This makes it efficient for problems such as online shortest paths, where $\mathcal{D}$ is exponentially large but $M$ is a shortest-path algorithm.

**Follow the regularized leader.** Replace the minimum of $L$ by the minimum of $L(x) + \frac1\eta R(x)$ for a strongly convex regularizer $R$. With $R$ the negative entropy on the simplex this is [Hedge](/multiplicative-weights-update/); with $R(x) = \frac12\|x\|^2$ and linear losses it is a lazy form of [online gradient descent](/online-gradient-descent/).

## Example

Two experts, with losses $(1/2, 0)$ in round 1, then $(0, 1)$ in even rounds and $(1, 0)$ in odd rounds.

| $t$ | $L$ before the round | FTL picks | $\ell_t$ | FTL pays |
|---|---|---|---|---|
| 1 | $0, 0$ | 1 (tie) | $1/2, 0$ | $1/2$ |
| 2 | $1/2, 0$ | 2 | $0, 1$ | $1$ |
| 3 | $1/2, 1$ | 1 | $1, 0$ | $1$ |
| 4 | $3/2, 1$ | 2 | $0, 1$ | $1$ |

After $T$ rounds FTL pays $T - 1/2$, while expert 2 pays $\lfloor T/2 \rfloor$. So the regret is at least $T/2 - 1$; for $T = 4$ it is $7/2 - 3/2 = 2$. In each round the leader is the expert that is about to lose. FTPL with $T = 200$ and $\varepsilon = 0.05$ adds noise of size up to $20$, which is much larger than the gap of $1/2$ between the totals, so it picks each expert with probability close to $1/2$ and pays about $T/2$, the same as the best expert.

## Correctness

The key fact is the *be-the-leader* lemma: the rule that plays $x_{t+1}$, the leader after round $t$, in round $t$ has total loss at most $\min_x \sum_t \ell_t(x)$. It follows by induction, since $x_T$ minimizes $L_{T-1}$. So the regret of FTL is at most $\sum_t (\ell_t(x_t) - \ell_t(x_{t+1}))$: FTL loses only when the leader changes in a way that matters. For squared loss $(x - z_t)^2$ on $[0, 1]$, FTL plays the running mean, each term is at most $2/t$, and the regret is at most $2(1 + \ln T)$. For FTPL, the lemma applied with the noise as an extra first loss costs $D/\varepsilon$, and the noise makes the leader before and after round $t$ have nearly the same distribution: two cubes of side $1/\varepsilon$ shifted by $s_t$ overlap in a fraction $1 - \varepsilon\|s_t\|_1$. This gives $\mathbb{E}[\text{regret}] \le \varepsilon R A T + D/\varepsilon$. The full proof is below.

## Complexity

- **Time.** FTL and FTPL use $\Theta(n)$ time per round for experts, so $\Theta(n \cdot T)$ in total. For a structured decision set, FTPL makes one call to the offline optimizer per round.
- **Space.** $\Theta(n)$ for the totals, or $\Theta(d)$ for the total loss vector of a structured problem.
- **Randomness.** FTPL draws $n$ uniform numbers per round. The bound also holds if one perturbation is drawn at the start and reused, against an oblivious adversary.

## Properties

- **FTL: linear regret in the worst case.** The example gives regret $T/2 - 1$, for every tie rule up to a constant: no deterministic rule can do better than linear regret against an adaptive adversary.
- **FTL: logarithmic regret for curved losses.** For strongly convex or exp-concave losses, the leader moves by $O(1/t)$ per round and the regret is $O(\log T)$.
- **FTPL: $O(\sqrt{T})$ regret.** Expected regret at most $\varepsilon R A T + D/\varepsilon$, which is $2\sqrt{2nT}$ for experts with the tuned $\varepsilon$. With exponential noise in place of uniform noise the bound improves to $O(\sqrt{T \ln n})$; with Gumbel noise FTPL picks expert $i$ with probability proportional to $e^{-\eta L[i]}$, which is exactly Hedge.
- **Lazy.** FTL and FTPL depend only on the total loss, not on the order of past rounds.

## Variants and improvements

- **Follow the regularized leader (FTRL):** add $\frac1\eta R(x)$ to the total loss. It unifies Hedge, online gradient descent and many other methods; see [online convex optimization](/online-convex-optimization/) and [regularization](/regularization/).
- **FTPL with exponential or Gaussian noise:** better dependence on $n$, and the same efficiency with an offline optimizer.
- **Be the leader with hindsight:** the lemma gives a bound for any rule that plays a near-leader, and is the base of the analysis of FTRL.
- **Fictitious play:** in a two-player game, each player plays a best response to the empirical mix of the opponent's past moves, which is FTL. Brown proposed it in 1951; Robinson (1951) proved that it converges in value in zero-sum games, slowly.

## When to use it

Use FTL when the losses are strongly convex or exp-concave, such as the squared loss or the log loss, since the leader is then stable and the regret is $O(\log T)$. Avoid plain FTL for linear losses, such as the expert problem with 0-1 losses. Use FTPL when the decision set is large and structured and you have an efficient offline optimizer, such as paths, spanning trees or assignments, since it needs only one optimizer call per round. For a small set of experts, [Hedge](/multiplicative-weights-update/) has a better bound.

## Pitfalls

- **Tie rules do not save FTL.** Changing the tie rule changes only round 1 of the example; the alternating pattern still makes FTL pay about $T$.
- **The noise must be large enough.** A perturbation of size $1/\varepsilon$ much smaller than $\sqrt{T}$ leaves FTPL close to FTL, and the regret grows.
- **Adaptive adversaries.** The FTPL bound is for an oblivious adversary, or for one that does not see the draw of the round. With a fresh perturbation each round it extends to adaptive adversaries that see past choices but not the current noise.
- **Wrong sign.** The perturbation must favor experts at random. Code that adds noise and then takes a maximum in place of a minimum follows the worst expert.

## Implementations

## History

Brown (1951) proposed fictitious play, the game-theoretic form of FTL, and Robinson (1951) proved its convergence in zero-sum games. Hannan (1957) showed that adding random perturbations to the totals gives average regret that tends to $0$, which is the origin of FTPL and of the notion of Hannan consistency. Kalai and Vempala (2005) rediscovered the method for online linear optimization, gave the short proof through the be-the-leader lemma, and showed that it is efficient whenever the offline problem is. Follow the regularized leader, studied by Shalev-Shwartz, Hazan and others in the 2000s, replaced the noise with a regularizer.

## References
