---
tag: F0X9Y9
kind: algorithm
slug: multiplicative-weights-update
name: Multiplicative weights update
aliases:
- Hedge
- MWU
- multiplicative weights method
- exponential weights algorithm
area: online-and-streaming/competitive-analysis
level: advanced
summary: Keep a weight per expert, play the normalized weights, and multiply each weight by (1 - η·cost) or exp(-η·loss). Hedge has regret at most sqrt(T ln n / 2).
solves: [expert-problem]
model: real-ram
complexity:
  vars: {n: the number of experts, T: the number of rounds}
  time: {worst: Θ(n·T)}
  space: {extra: Θ(n)}
properties: {online: true, deterministic: true, comparison: false, recursive: false}
history:
  year: 1997
  people: [Yoav Freund, Robert E. Schapire]
  note: Freund and Schapire gave Hedge for losses in [0, 1] and used it for boosting; Arora, Hazan and Kale (2012) collected the many uses of the method under one theorem.
prereqs: [expert-problem, regret, weighted-majority]
see_also: [weighted-majority, follow-the-leader, online-convex-optimization, mirror-descent, adaboost, zero-sum-game, exp3, doubling-trick]
sources:
  - paper: doi:10.4086/toc.2012.v008a006
    title: "Sanjeev Arora, Elad Hazan and Satyen Kale, The multiplicative weights update method, a meta-algorithm and applications, Theory of Computing 8 (2012), 121-164"
    locator: Section 2 (the algorithm with the update 1 - eta m, the main theorem for costs in [-1, 1] and its proof by a potential, and the exponential variant) and Section 3 (applications to linear programs, zero-sum games and other problems)
  - paper: doi:10.1006/jcss.1997.1504
    title: "Yoav Freund and Robert E. Schapire, A decision-theoretic generalization of on-line learning and an application to boosting, Journal of Computer and System Sciences 55(1) (1997), 119-139"
    locator: Section 2 (the algorithm Hedge(beta) and its loss bound) and Section 4 (AdaBoost)
  - book: isbn:9780521841085
    title: Nicolo Cesa-Bianchi and Gabor Lugosi, Prediction, Learning, and Games, Cambridge University Press, 2006
    locator: Chapter 2 (the exponentially weighted average forecaster, the bound (ln n)/eta + eta T / 8 via Hoeffding's lemma, and the doubling trick) and Appendix A (Hoeffding's lemma)
  - paper: doi:10.1006/inco.1994.1009
    title: "Nick Littlestone and Manfred K. Warmuth, The weighted majority algorithm, Information and Computation 108(2) (1994), 212-261"
    locator: the randomized weighted majority algorithm, the first form of the method
---

The multiplicative weights update method keeps one weight per expert, plays the probability distribution proportional to the weights, and after each round multiplies the weight of each expert by a factor that is small when the expert did badly. With the linear factor $1 - \eta m$ for costs $m \in [-1, 1]$, the total cost is at most $\sum_t m_{t,i} + \eta\sum_t |m_{t,i}| + (\ln n)/\eta$ for every expert $i$ (Arora, Hazan and Kale 2012). With the factor $e^{-\eta \ell}$ for losses in $[0, 1]$ it is Hedge (Freund and Schapire 1997), whose [regret](/regret/) is at most $\sqrt{(T/2)\ln n}$, the optimal rate for the [expert problem](/expert-problem/). The same update solves zero-sum games, approximates linear programs and drives boosting.

## In plain words

You must choose among several options again and again, and after each round you learn how well every option did. You keep a score for each option, all equal at the start. Each round you choose an option at random, with the scores as the odds. When the results come, you shrink the score of each option a little for each unit of loss it had.

Options that keep doing badly soon have tiny scores, so you rarely pick them. Options that do well keep their scores, so you pick them more and more. Over many rounds your average loss comes close to the average loss of the best single option, and this holds whatever the results are, even if someone picks them to hurt you.

## The problem

There are $n$ experts and $T$ rounds. In round $t$ the algorithm picks a probability vector $p_t$, then the adversary reveals a cost vector $m_t \in [-1, 1]^n$ (or a loss vector $\ell_t \in [0, 1]^n$), and the algorithm pays $p_t \cdot m_t$. The adversary may choose $m_t$ after it sees $p_t$. The goal is a total cost close to $\min_i \sum_t m_{t,i}$ for every sequence. This is the [expert problem](/expert-problem/) in its regret form; the loss of a random expert drawn from $p_t$ has expectation $p_t \cdot m_t$.

## The algorithm

```pseudo id=main
MULTIPLICATIVE-WEIGHTS(n, η)                 ▷ 0 < η ≤ 1/2
L1  for i ← 1 to n do w[i] ← 1
L2  for t ← 1 to T do
L3      Φ ← w[1] + ⋯ + w[n];  p[i] ← w[i] / Φ for each i
L4      play the distribution p (or an expert drawn from p)
L5      receive the costs m[1 .. n] ∈ [−1, 1] and pay p · m
L6      for i ← 1 to n do w[i] ← w[i] · (1 − η · m[i])
```

**Hedge.** For losses $\ell \in [0, 1]$, line L6 becomes $w[i] \leftarrow w[i] \cdot e^{-\eta \ell[i]}$, for any $\eta > 0$. Then $p_{t,i}$ is proportional to $e^{-\eta L_{t-1,i}}$, where $L_{t-1,i}$ is the total loss of expert $i$ before round $t$. With $\eta = \sqrt{8 \ln n / T}$ the regret is at most $\sqrt{(T/2)\ln n}$.

**Gains.** For gains in place of costs, use $w[i] \leftarrow w[i](1 + \eta g[i])$, which is line L6 with $m = -g$.

## Example

Two experts, $\eta = 1/2$, and costs $m_1 = (1, 0)$, $m_2 = (0, 1)$, $m_3 = (1, 0)$.

| $t$ | $w_t$ | $p_t$ | $m_t$ | cost $p_t \cdot m_t$ |
|---|---|---|---|---|
| 1 | $1, 1$ | $1/2, 1/2$ | $1, 0$ | $1/2$ |
| 2 | $1/2, 1$ | $1/3, 2/3$ | $0, 1$ | $2/3$ |
| 3 | $1/2, 1/2$ | $1/2, 1/2$ | $1, 0$ | $1/2$ |

After round 3 the weights are $1/4, 1/2$. The algorithm pays $5/3$; expert 1 pays $2$ and expert 2 pays $1$. The theorem with $i = 2$ gives the bound $1 + \frac12 \cdot 1 + 2\ln 2 \approx 2.89$.

## Correctness

The proof follows the potential $\Phi_t = \sum_i w_{t,i}$. Line L6 gives $\Phi_{t+1} = \Phi_t(1 - \eta\,p_t \cdot m_t) \le \Phi_t e^{-\eta\,p_t \cdot m_t}$, so the potential falls fast when the algorithm pays much. It cannot fall below the weight of one expert, $\prod_t(1 - \eta m_{t,i})$, which is at least $(1 - \eta)^{P}(1 + \eta)^{N}$, where $P$ and $N$ are the positive and negative parts of the costs of expert $i$. Taking logarithms gives

$$\sum_{t=1}^{T} p_t \cdot m_t \le \sum_{t=1}^{T} m_{t,i} + \eta\sum_{t=1}^{T} |m_{t,i}| + \frac{\ln n}{\eta}.$$

For Hedge, Hoeffding's lemma gives $\ln(\Phi_{t+1}/\Phi_t) \le -\eta\,p_t \cdot \ell_t + \eta^2/8$, and the same comparison gives regret at most $\frac{\ln n}{\eta} + \frac{\eta T}{8}$. The full proof is below.

## Complexity

- **Time.** $\Theta(n)$ per round for lines L3 to L6, so $\Theta(n \cdot T)$ in total.
- **Space.** $\Theta(n)$ for the weights.
- **Numbers.** Weights shrink like $e^{-\eta L}$. Store $\log w_i$ and subtract the largest one before taking exponents, as the implementation does.
- **Rounds for a target.** To get average regret at most $\varepsilon$, Hedge needs $T \ge \ln n / (2\varepsilon^2)$ rounds. This $O(\ln n/\varepsilon^2)$ count drives the running time of the applications.

## Properties

- **Regret.** Hedge: at most $\sqrt{(T/2)\ln n}$ with $T$ known, for losses in $[0, 1]$, against any adversary that fixes $\ell_t$ without seeing a draw from $p_t$ (it may see $p_t$).
- **Optimal.** For every algorithm, random losses force regret $(1 - o(1))\sqrt{(T/2)\ln n}$ as $T$ and $n$ grow, so the constant of Hedge is the best possible (see [regret](/regret/)).
- **Unknown $T$.** The [doubling trick](/doubling-trick/) or the rate $\eta_t = \sqrt{8 \ln n / t}$ removes the need to know $T$, at a constant factor.
- **Small losses.** With costs in $[0, 1]$ the AHK bound is $(1 + \eta)L_i + (\ln n)/\eta$, so the regret is $O(\sqrt{L^* \ln n} + \ln n)$ with a tuned $\eta$ when the best expert has a small total loss $L^*$.
- **Deterministic.** The distribution $p_t$ is a deterministic function of the past; randomness enters only if one expert is drawn from $p_t$.

## Variants and improvements

- **Randomized [weighted majority](/weighted-majority/):** the update $1 - (1 - \beta)\ell$, the first form of the method.
- **[Mirror descent](/mirror-descent/) with the entropy:** on the simplex, mirror descent with the negative entropy as the regularizer is the exponentiated gradient update, which is Hedge with the gradients as losses. This page is the online-learning view; the mirror descent page covers the optimization view.
- **[Follow the regularized leader](/follow-the-leader/):** Hedge plays $\arg\min_p \{p \cdot L_{t-1} + \frac1\eta \sum_i p_i \ln p_i\}$, so it is follow the leader with an entropy regularizer. Follow the perturbed leader with Gumbel noise gives the same distribution.
- **Bandit feedback:** [EXP3](/exp3/) runs Hedge on unbiased estimates of the losses and gets regret $O(\sqrt{Tn\ln n})$.
- **Fixed share:** mixing a small part of the uniform distribution into $p_t$ tracks a best expert that changes.
- **[AdaBoost](/adaboost/):** Hedge with the training examples as experts and the weak hypotheses as the adversary.

## When to use it

Use multiplicative weights when you combine a finite set of actions online and want a guarantee for every sequence of losses, with a dependence on $n$ of only $\ln n$. It is also a tool for offline problems: to solve a zero-sum game, a packing or covering linear program, or a flow problem approximately, run it for $O(\ln n/\varepsilon^2)$ rounds against an oracle that answers each distribution with a best response. If the actions form a convex set with geometry far from the simplex, use [online gradient descent](/online-gradient-descent/) or mirror descent in [online convex optimization](/online-convex-optimization/).

## Pitfalls

- **Costs out of range.** The AHK bound needs $m \in [-1, 1]$ and $\eta \le 1/2$, so that each factor $1 - \eta m$ stays positive and Lemma 2 of the proof holds. Scale costs by their width $\rho$ and pay a factor $\rho$ in the number of rounds.
- **A rate tuned for the wrong $T$.** With $\eta = \sqrt{8 \ln n / T}$ and a game that lasts much longer than $T$, the bound $\eta T'/8$ grows linearly. Use the doubling trick or a decreasing rate.
- **Overflow and underflow.** $e^{-\eta L}$ underflows for large $L$, and normalizing after the fact gives $0/0$. Work in log space.
- **Showing the draw to the adversary.** The bound is for the expected loss under $p_t$. If the adversary sees the expert drawn in round $t$ before it fixes $\ell_t$, it can make the drawn expert lose in every round, and the regret is linear.
- **Taking the last iterate in games.** In zero-sum games the average strategies converge to equilibrium, but the strategy of the last round can cycle. Return the averages.

## Implementations

## History

The ideas behind the method appear in many fields: in game theory, Hannan (1957) and Blackwell (1956) gave the first strategies with vanishing average regret in repeated games; in machine learning, multiplicative updates appear as weighted majority (Littlestone and Warmuth 1989) and the aggregating algorithm (Vovk 1990), and in optimization in the packing and covering algorithms of Plotkin, Shmoys and Tardos (1995) and Young (1995). Freund and Schapire (1997) gave Hedge and its regret bound, and used it to design AdaBoost. Arora, Hazan and Kale (2012) gave the version with costs in $[-1, 1]$ and showed that one theorem covers all these uses.

## References
