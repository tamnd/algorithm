---
tag: WG38S9
kind: problem
slug: expert-problem
name: Expert problem
aliases:
- prediction with expert advice
- learning from expert advice
- experts problem
area: online-and-streaming/competitive-analysis
level: advanced
summary: In each round, combine the advice of n experts before the losses are revealed, so that the total loss is close to that of the best expert in hindsight.
prereqs: [regret, online-algorithm, randomized-online-algorithm]
see_also: [weighted-majority, multiplicative-weights-update, follow-the-leader, online-convex-optimization, exp3, winnow, oblivious-adversary, boosting]
sources:
  - book: isbn:9780521841085
    title: Nicolo Cesa-Bianchi and Gabor Lugosi, Prediction, Learning, and Games, Cambridge University Press, 2006
    locator: Chapter 1 (the model), Chapter 2 (exponential weights and regret bounds), Chapter 3 (lower bounds), Chapter 4 (randomized prediction)
  - paper: doi:10.1006/inco.1994.1009
    title: "Nick Littlestone and Manfred K. Warmuth, The weighted majority algorithm, Information and Computation 108(2) (1994), 212-261"
    locator: the mistake-bound model, the halving algorithm and the bound 2.41(m + log2 n) for weighted majority
  - paper: doi:10.1145/258128.258179
    title: "Nicolo Cesa-Bianchi, Yoav Freund, David Haussler, David P. Helmbold, Robert E. Schapire and Manfred K. Warmuth, How to use expert advice, Journal of the ACM 44(3) (1997), 427-485"
    locator: the regret view for the absolute loss and the matching sqrt(T ln n) bounds
  - paper: doi:10.1006/jcss.1997.1504
    title: "Yoav Freund and Robert E. Schapire, A decision-theoretic generalization of on-line learning and an application to boosting, Journal of Computer and System Sciences 55(1) (1997), 119-139"
    locator: Section 2 (the allocation problem and the Hedge algorithm)
---

The expert problem asks a learner to make a decision in each of $T$ rounds after it sees the advice of $n$ experts, when the loss of every expert is revealed only at the end of the round. The goal is a total loss close to that of the best expert in hindsight, whatever the sequence of losses is. There are two standard views: the mistake bound for binary predictions, where [weighted majority](/weighted-majority/) makes at most $2.41(m^* + \log_2 n)$ mistakes, and the [regret](/regret/) view for losses in $[0, 1]$, where [Hedge](/multiplicative-weights-update/) has expected regret at most $\sqrt{(T/2)\ln n}$, which is optimal. It is the base problem of online learning.

## In plain words

Each morning you must say whether it will rain. A group of forecasters each gives an opinion first. In the evening you learn whether it rained, and so whether each forecaster was right. You do not know who is good, and the weather does not need to follow any pattern.

You want to make, over many days, not many more mistakes than the best forecaster in the group, even though you only find out at the end who that was. A good plan is to give each forecaster a weight, follow the weighted opinion, and cut the weight of each forecaster who is wrong. Bad forecasters soon count for little, and you end up close to the best one. A small amount of randomness in your choice makes the plan even safer.

## Definition

**Regret view.** There are $n$ experts and $T$ rounds. In round $t$:

1. the learner chooses a probability vector $p_t$ on $\{1, \ldots, n\}$ (or an expert $I_t$ drawn from it);
2. the adversary chooses a loss vector $\ell_t \in [0, 1]^n$;
3. the learner pays $p_t \cdot \ell_t = \sum_i p_{t,i}\ell_{t,i}$ (the expected loss of $I_t$) and sees all of $\ell_t$.

The input is $\sigma = (\ell_1, \ldots, \ell_T)$. With $L_{T,i} = \sum_t \ell_{t,i}$ and $L^* = \min_i L_{T,i}$, the goal is a small [regret](/regret/)

$$R_T = \sum_{t=1}^{T} p_t \cdot \ell_t - L^*,$$

for every $\sigma$. The adversary is [oblivious](/oblivious-adversary/), or adaptive but blind to $I_t$ in round $t$; the bounds below hold for both, with $p_t \cdot \ell_t$ as the loss.

**Mistake-bound view.** In round $t$ each expert $i$ predicts a bit $f_{t,i}$, the learner predicts a bit $\hat y_t$, and then the true bit $y_t$ is revealed. Expert $i$ makes $m_i$ mistakes in total, and $m^* = \min_i m_i$. The goal is a learner with $m$ mistakes, where $m \le a\,m^* + b \log n$ for small constants $a$ and $b$, for every sequence. This is the case $\ell_{t,i} = \mathbf{1}[f_{t,i} \ne y_t]$, with a deterministic learner and a bound by a ratio plus an additive term.

## Variants

- **Bandit feedback.** The learner sees only the loss of the expert it chose. [EXP3](/exp3/) gets expected regret $O(\sqrt{Tn \ln n})$; this is the adversarial [multi-armed bandit](/multi-armed-bandit/).
- **Convex and mixable losses.** If the learner may predict a mixture and the loss is convex in the prediction, as with the absolute or square loss, the weighted average of the experts' predictions has the same bounds without randomization. For mixable losses such as the log loss, Vovk's aggregating algorithm has regret $O(\ln n)$, with no dependence on $T$.
- **Tracking the best expert.** The comparator may switch experts $k$ times. The fixed-share update of Herbster and Warmuth (1998) mixes a little of the uniform distribution into the weights and pays about $k \ln(nT)$ in place of $\ln n$.
- **Infinitely many experts.** The actions form a convex set and the losses are convex; this is [online convex optimization](/online-convex-optimization/), and the expert problem is its case of linear losses on the simplex.
- **Unknown horizon.** Bounds that need $T$ to set a learning rate carry over to unknown $T$ with the [doubling trick](/doubling-trick/), or with a rate $\eta_t$ that decreases in $t$.

## Examples

Three experts predict whether it rains on five days (1 for rain).

| day | expert 1 | expert 2 | expert 3 | rain |
|---|---|---|---|---|
| 1 | 1 | 0 | 1 | 0 |
| 2 | 0 | 1 | 1 | 1 |
| 3 | 1 | 1 | 0 | 0 |
| 4 | 1 | 0 | 1 | 1 |
| 5 | 0 | 1 | 0 | 1 |

Expert 1 makes 4 mistakes and experts 2 and 3 make 2 each, so $m^* = 2$. Weighted majority with factor $1/2$ makes 3 mistakes on this sequence (days 1, 3 and 5); its bound is $2.41(2 + \log_2 3) \approx 8.6$. The page on [weighted majority](/weighted-majority/) traces the weights.

No expert is perfect here, so the halving algorithm, which drops each expert at its first mistake, keeps only expert 2 after day 1 and has no expert left after day 3.

## Known algorithms

- **Halving algorithm.** If some expert is never wrong, predict with the majority of the experts that have been right so far. At most $\lfloor \log_2 n \rfloor$ mistakes.
- **[Weighted majority](/weighted-majority/)** (Littlestone and Warmuth 1994). Deterministic, multiplies the weight of each wrong expert by $\beta$, at most $2.41(m^* + \log_2 n)$ mistakes for $\beta = 1/2$. The randomized version has expected mistakes $(1 + O(\varepsilon))m^* + O(\ln n / \varepsilon)$.
- **[Hedge, or multiplicative weights](/multiplicative-weights-update/)** (Freund and Schapire 1997). Weights $e^{-\eta L_{t,i}}$, expected regret at most $\ln n/\eta + \eta T/8$, which is $\sqrt{(T/2)\ln n}$ for the best $\eta$.
- **[Follow the leader](/follow-the-leader/).** Pick the expert with the least loss so far. Regret linear in $T$ in the worst case. Follow the perturbed leader (Kalai and Vempala 2005) adds random noise and gets $O(\sqrt{nT})$, or $O(\sqrt{T \ln n})$ with suitable noise.
- **[Online gradient descent](/online-gradient-descent/)** on the simplex: regret $O(\sqrt{T})$ with a factor that grows like $\sqrt{n}$ in place of $\sqrt{\ln n}$ for this geometry.

## Bounds

**Halving makes at most $\lfloor \log_2 n \rfloor$ mistakes if some expert is perfect.** Let $C_t$ be the set of experts with no mistake before round $t$. A perfect expert stays in $C_t$, so $|C_t| \ge 1$. When the learner errs, the majority of $C_t$ was wrong, so $|C_{t+1}| \le |C_t|/2$. After $m$ mistakes, $1 \le n/2^m$, so $m \le \log_2 n$, and $m$ is an integer.

**This is optimal.** Let $n = 2^k$, and let the experts be all $2^k$ bit strings of length $k$, expert $s$ predicting $s_t$ in round $t \le k$. In each round the adversary sets $y_t$ to the opposite of the learner's prediction. The deterministic learner errs $k = \log_2 n$ times, and the expert $s = (y_1, \ldots, y_k)$ is perfect.

**No deterministic learner beats factor 2 in $m^*$.** Take two experts, one predicting $0$ and one predicting $1$ in every round, and let $y_t$ be the opposite of the learner's prediction. The learner errs $T$ times. Each round, exactly one expert errs, so $m_1 + m_2 = T$ and $m^* \le T/2$. So $m \ge 2m^*$, for every $T$. Weighted majority with $\beta \to 1$ comes close to this factor in $m^*$, at the cost of a larger additive term (see [weighted majority](/weighted-majority/)).

**Randomized learners.** The same adversary shows that a deterministic learner has regret at least $T/2$ in the regret view. Randomized learners avoid this: Hedge has $\mathbb{E}[R_T] \le \sqrt{(T/2)\ln n}$ for every oblivious loss sequence, with $T$ known. No algorithm has a better constant in the limit: for losses in $\{0, 1\}$ chosen at random, every learner has $\mathbb{E}[R_T] \ge (1 - o(1))\sqrt{(T/2)\ln n}$ as $T \to \infty$ and then $n \to \infty$ (Cesa-Bianchi et al. 1997; Cesa-Bianchi and Lugosi 2006, Chapter 3). So the regret of the expert problem is $\Theta(\sqrt{T \ln n})$.

**Small best loss.** If $L^* \le L$ is known, Hedge with a tuned $\eta$ has regret $O(\sqrt{L \ln n} + \ln n)$, which is better when the best expert has a small loss.

## Reductions

- **To online convex optimization.** Take the simplex $\Delta_n$ as the action set and $f_t(p) = p \cdot \ell_t$ as the loss. A regret bound for [online convex optimization](/online-convex-optimization/) on $\Delta_n$ gives one for experts. Mirror descent with the entropy as the regularizer gives Hedge (see [mirror descent](/mirror-descent/)).
- **Zero-sum games.** If the row player of a [zero-sum game](/zero-sum-game/) uses a no-regret algorithm against any column player, the average strategies approach the value of the game. This gives an algorithmic proof of the [minimax theorem](/minimax-theorem/) and a method to solve games approximately.
- **Boosting.** Freund and Schapire's [AdaBoost](/adaboost/) runs Hedge with the training examples as experts, so that weight moves to the examples that the weak learners get wrong (see [boosting](/boosting/)).
- **Linear programs.** The [multiplicative weights](/multiplicative-weights-update/) method solves packing and covering linear programs and flow problems approximately by running an expert algorithm over the constraints.

## Applications

- **Ensemble prediction.** Combining forecasts, models or classifiers whose quality is not known in advance, with a guarantee that holds for every sequence of outcomes.
- **Online portfolio selection.** Each expert is a fixed asset or a fixed mix of assets, and the loss is the negative log return. Cover's universal portfolio is an expert algorithm over all constant mixes.
- **Routing and resource choice.** Choosing a route, a server or a cache policy each round, with the losses of all choices observed afterwards. Combining online algorithms in this way, for example several paging policies, gives a learner that is close to the best of them.

## References
