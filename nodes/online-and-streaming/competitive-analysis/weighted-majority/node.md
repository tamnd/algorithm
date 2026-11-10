---
tag: PJZVZH
kind: algorithm
slug: weighted-majority
name: Weighted majority algorithm
aliases:
- randomized weighted majority
- weighted majority vote
- WM
area: online-and-streaming/competitive-analysis
level: advanced
summary: Predict with the weighted vote of n experts and multiply the weight of each wrong expert by β. At most 2.41(m* + log2 n) mistakes for β = 1/2; the randomized version has regret O(sqrt(T log n)).
solves: [expert-problem]
model: real-ram
complexity:
  vars: {n: the number of experts, T: the number of rounds}
  time: {worst: Θ(n·T)}
  space: {extra: Θ(n)}
properties: {online: true, deterministic: true, comparison: false, recursive: false}
history:
  year: 1989
  people: [Nick Littlestone, Manfred K. Warmuth]
  note: Presented at FOCS 1989 and published in Information and Computation in 1994, with the halving algorithm as the case of a perfect expert and the randomized version for expected mistakes.
prereqs: [expert-problem, regret]
see_also: [multiplicative-weights-update, follow-the-leader, winnow, perceptron, randomized-online-algorithm, online-convex-optimization, boosting, adaboost]
sources:
  - paper: doi:10.1006/inco.1994.1009
    title: "Nick Littlestone and Manfred K. Warmuth, The weighted majority algorithm, Information and Computation 108(2) (1994), 212-261"
    locator: Section 2 (WM and the bound (log n + m log(1/beta)) / log(2/(1+beta))), the randomized version WMR, and the general updates between beta^r and 1 - (1 - beta) r
  - book: isbn:9780521841085
    title: Nicolo Cesa-Bianchi and Gabor Lugosi, Prediction, Learning, and Games, Cambridge University Press, 2006
    locator: Chapter 2 (weighted average and exponentially weighted forecasters) and Chapter 4 (randomized prediction)
  - paper: doi:10.4086/toc.2012.v008a006
    title: "Sanjeev Arora, Elad Hazan and Satyen Kale, The multiplicative weights update method, a meta-algorithm and applications, Theory of Computing 8 (2012), 121-164"
    locator: Section 2 (the weighted majority algorithm, Theorem 2.1, and the randomized version)
---

The weighted majority algorithm of Littlestone and Warmuth predicts a bit with a weighted vote of $n$ experts and, after the outcome, multiplies the weight of each expert that was wrong by a factor $\beta < 1$. For $\beta = 1/2$ it makes at most $2.41(m^* + \log_2 n)$ mistakes, where $m^*$ is the number of mistakes of the best expert. Its randomized version follows one expert drawn in proportion to the weights, and its expected number of mistakes is at most $(1 + \varepsilon)m^* + (\ln n)/\varepsilon$, which gives regret $O(\sqrt{T \log n})$. It is the first multiplicative weights algorithm for the [expert problem](/expert-problem/).

## In plain words

A group of advisors each says yes or no, and you must give one answer. You give every advisor the same weight at the start. In each round you add up the weights of those who say yes and of those who say no, and you go with the larger side. When the true answer comes, you cut the weight of each advisor who was wrong in half.

Each time you are wrong, at least half of the total weight was on the wrong side, so the total weight drops by a quarter or more. The best advisor keeps much of its weight, because it is rarely wrong. The total can never fall below the weight of the best advisor, so you cannot be wrong too often. If you pick one advisor at random, with the weights as chances, you do even better.

## The problem

There are $n$ experts. In each round $t = 1, \ldots, T$, each expert $i$ predicts a bit $f_{t,i}$, the algorithm predicts a bit $\hat y_t$, and then the true bit $y_t$ is revealed. The sequence of predictions and outcomes can be arbitrary, even chosen by an adversary that knows the algorithm. Let $m_i$ be the number of mistakes of expert $i$ and $m^* = \min_i m_i$. The goal is to make few mistakes compared with $m^*$, as in the mistake-bound view of the [expert problem](/expert-problem/).

## The algorithm

```pseudo id=main
WEIGHTED-MAJORITY(n, β)                      ▷ 0 ≤ β < 1, often β = 1/2
L1  for i ← 1 to n do w[i] ← 1
L2  for t ← 1, 2, … do
L3      receive the predictions f[1 .. n] ∈ {0, 1}
L4      W1 ← Σ { w[i] : f[i] = 1 };  W0 ← Σ { w[i] : f[i] = 0 }
L5      predict ŷ ← 1 if W1 ≥ W0, else ŷ ← 0
L6      receive the outcome y
L7      for each i with f[i] ≠ y do w[i] ← β · w[i]
```

The weight of expert $i$ after any number of rounds is $\beta^{(\text{its mistakes so far})}$. With $\beta = 0$, line L7 removes each wrong expert for good, and the algorithm is the *halving algorithm*: it predicts with the majority of the experts that have never been wrong.

**Randomized weighted majority.** Replace line L5 by "pick expert $i$ with probability $w[i] / (W_0 + W_1)$ and predict $f[i]$". Then the probability of a mistake in round $t$ is the weight on the wrong side divided by the total weight. For losses $\ell_{t,i} \in [0, 1]$ in place of mistakes, line L7 becomes $w[i] \leftarrow w[i]\,(1 - (1 - \beta)\ell_{t,i})$; with $\beta^{\ell}$ in place of $1 - (1-\beta)\ell$ this is [Hedge](/multiplicative-weights-update/).

## Example

Three experts and five rounds, $\beta = 1/2$. The columns $W_1$ and $W_0$ are the weights of the two sides before the vote.

| $t$ | $f_t$ | $W_1$ | $W_0$ | $\hat y_t$ | $y_t$ | weights after the round |
|---|---|---|---|---|---|---|
| | | | | | | $1, 1, 1$ |
| 1 | 1, 0, 1 | 2 | 1 | 1 | 0 (mistake) | $1/2, 1, 1/2$ |
| 2 | 0, 1, 1 | 3/2 | 1/2 | 1 | 1 | $1/4, 1, 1/2$ |
| 3 | 1, 1, 0 | 5/4 | 1/2 | 1 | 0 (mistake) | $1/8, 1/2, 1/2$ |
| 4 | 1, 0, 1 | 5/8 | 1/2 | 1 | 1 | $1/8, 1/4, 1/2$ |
| 5 | 0, 1, 0 | 1/4 | 5/8 | 0 | 1 (mistake) | $1/16, 1/4, 1/4$ |

The algorithm makes $m = 3$ mistakes. The experts make $4$, $2$ and $2$, so $m^* = 2$. The final total weight is $9/16$. It lies between the weight $\beta^{m^*} = 1/4$ of a best expert and the bound $n \left(\frac34\right)^m = 81/64$ of the proof.

The randomized version, on the same data, errs in the five rounds with probabilities $2/3$, $1/4$, $5/7$, $4/9$ and $5/7$, so its expected number of mistakes is about $2.79$.

## Correctness

The proof uses the total weight $W$ as a potential. At the start $W = n$. When the algorithm errs, at least half of $W$ was on the wrong side and is multiplied by $\beta$, so $W$ drops by a factor of at least $(1 + \beta)/2$. A best expert keeps weight $\beta^{m^*}$, so $\beta^{m^*} \le W \le n\left(\frac{1+\beta}{2}\right)^m$, which gives

$$m \le \frac{\ln n + m^* \ln(1/\beta)}{\ln \frac{2}{1+\beta}}.$$

For $\beta = 1/2$ both coefficients are $\ln 2/\ln\frac43 \approx 2.409$, so $m \le 2.41(m^* + \log_2 n)$. For the randomized version the same potential gives the expected loss bound $\frac{\ln n + L^* \ln(1/\beta)}{1 - \beta}$, which is at most $(1+\varepsilon)L^* + \frac{\ln n}{\varepsilon}$ for $\beta = 1 - \varepsilon$. The full proof is below.

## Complexity

- **Time.** Lines L4 and L7 take $\Theta(n)$ time per round, so $T$ rounds take $\Theta(nT)$ arithmetic operations.
- **Space.** The algorithm keeps $n$ weights, $\Theta(n)$ space. It does not store the history.
- **Numbers.** After $T$ rounds a weight can be as small as $\beta^T$. Floating-point weights then underflow; keep the logarithms of the weights, or divide all weights by their maximum from time to time, which does not change any vote.

## Properties

- **Mistake bound.** $m \le \frac{\ln n + m^* \ln(1/\beta)}{\ln(2/(1+\beta))}$ for every sequence; $2.41(m^* + \log_2 n)$ for $\beta = 1/2$.
- **Factor 2 is the limit for deterministic rules.** With two experts that always predict $0$ and $1$ and an adversary that sets $y_t$ against $\hat y_t$, every deterministic algorithm errs $T$ times while $m^* \le T/2$. As $\beta \to 1$ the coefficient $\ln(1/\beta)/\ln(2/(1+\beta))$ of $m^*$ tends to $2$, but the coefficient of $\ln n$ grows without bound.
- **Randomized bound.** Expected mistakes at most $(1+\varepsilon)m^* + (\ln n)/\varepsilon$ for $\varepsilon \le 1/2$, against an adversary that may see the weights but not the random choice of the round. With $\varepsilon = \sqrt{\ln n/T}$ the regret is at most $2\sqrt{T \ln n}$.
- **No knowledge needed.** The deterministic algorithm needs neither $T$ nor $m^*$. The tuned randomized version needs $T$ or a bound on $m^*$, or the [doubling trick](/doubling-trick/).
- **Deterministic.** The base algorithm uses no randomness; the randomized version is a [randomized online algorithm](/randomized-online-algorithm/).

## Variants and improvements

- **Halving algorithm** ($\beta = 0$): at most $\lfloor \log_2 n \rfloor$ mistakes when some expert is perfect, which is optimal for deterministic algorithms in that case.
- **Randomized weighted majority (WMR):** expected loss $(1 + \varepsilon)L^* + (\ln n)/\varepsilon$ for losses in $[0, 1]$.
- **Hedge and multiplicative weights:** the update $w_i \leftarrow w_i e^{-\eta \ell_i}$ with regret $\sqrt{(T/2)\ln n}$, and the general framework of Arora, Hazan and Kale. See [multiplicative weights update](/multiplicative-weights-update/).
- **Continuous predictions.** If the prediction may be a number in $[0, 1]$ and the loss is the absolute difference, the weighted average $\sum_i p_i f_{t,i}$ gives the randomized bound without randomness, because the loss is convex in the prediction.
- **Winnow.** [Winnow](/winnow/) uses multiplicative updates on the weights of features to learn sparse linear threshold functions with few mistakes.
- **Shifting experts.** Keep each weight above a small fraction of the total, or mix in the uniform weights, to track a best expert that changes over time (WML in the paper; fixed share of Herbster and Warmuth).

## When to use it

Use weighted majority when you must make binary predictions online from a fixed set of predictors, with no assumption on the data, and want a guarantee against the best predictor. Use the randomized version when the adversary can react to your prediction or when $m^*$ is a large fraction of $T$, since the deterministic factor $2.41$ is then costly. For real-valued losses and for the best constant, use [Hedge](/multiplicative-weights-update/). For a very large or continuous set of predictors, use [online convex optimization](/online-convex-optimization/).

## Pitfalls

- **Unbounded losses.** The analysis needs each loss in $[0, 1]$. Rescale losses in $[a, b]$ by $(\ell - a)/(b - a)$ before the update, and multiply the bound by $b - a$.
- **Underflow.** Products $\beta^{m_i}$ underflow after about a thousand mistakes in double precision for $\beta = 1/2$. Use log weights or renormalize.
- **Deterministic version against a reactive adversary.** If the outcome can depend on the prediction, the deterministic algorithm errs in every round. Only the randomized version keeps an $o(T)$ regret, and only if the adversary does not see the random choice.
- **Tie rule.** Any fixed rule for $W_1 = W_0$ keeps the bound, but code that predicts nothing on a tie, or skips the update in that round, breaks the analysis.
- **Using $\beta = 0$ without a perfect expert.** All weights reach $0$ and the vote is empty. The halving bound holds only when some expert is never wrong.

## Implementations

## History

Littlestone and Warmuth presented weighted majority at FOCS 1989, and the journal version appeared in 1994. The halving algorithm was known before as a rule for learning a concept from a finite class. Vovk (1990) gave the aggregating algorithm, a more general scheme with exponential weights for many loss functions, at about the same time. Freund and Schapire (1997) gave Hedge, the version for general losses with the update $e^{-\eta \ell}$, and used it in boosting. Arora, Hazan and Kale (2012) present weighted majority as the first case of the multiplicative weights method.

## References
