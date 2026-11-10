---
tag: 0BJM9P
kind: definition
slug: regret
name: Regret
aliases:
- cumulative regret
- external regret
- pseudo-regret
- swap regret
- internal regret
area: online-and-streaming/competitive-analysis
level: advanced
summary: The total loss of an online learner minus the total loss of the best fixed action in hindsight. Swap and internal regret compare with modified versions of the learner itself.
prereqs: [online-algorithm, expected-value]
see_also: [expert-problem, competitive-ratio, multiplicative-weights-update, online-convex-optimization, oblivious-adversary, adaptive-adversary, multi-armed-bandit, nash-equilibrium]
sources:
  - book: isbn:9780521841085
    title: Nicolo Cesa-Bianchi and Gabor Lugosi, Prediction, Learning, and Games, Cambridge University Press, 2006
    locator: Chapter 2 (regret against experts), Chapter 3 (lower bounds, among them the bound of order sqrt(T ln n)), Chapter 4 (randomized prediction, internal and swap regret)
  - paper: "James Hannan, Approximation to Bayes risk in repeated play, Contributions to the Theory of Games 3, Annals of Mathematics Studies 39, Princeton University Press, 1957, 97-139"
    locator: the first algorithm with average regret that tends to 0 (Hannan consistency)
  - paper: doi:10.1145/258128.258179
    title: "Nicolo Cesa-Bianchi, Yoav Freund, David Haussler, David P. Helmbold, Robert E. Schapire and Manfred K. Warmuth, How to use expert advice, Journal of the ACM 44(3) (1997), 427-485"
    locator: the matching upper and lower bounds of order sqrt(T ln n) for the absolute loss
  - paper: "Avrim Blum and Yishay Mansour, From external to internal regret, Journal of Machine Learning Research 8 (2007), 1307-1324"
    locator: the definitions of swap and internal regret and the reduction that gives swap regret O(sqrt(T n ln n))
  - paper: "Dean P. Foster and Rakesh V. Vohra, Calibrated learning and correlated equilibrium, Games and Economic Behavior 21(1-2) (1997), 40-55"
    locator: internal regret and its link to correlated equilibria
---

Regret measures how much an online learner loses compared with the best single action that it could have chosen with hindsight. It is the standard measure of quality for the [expert problem](/expert-problem/), [online convex optimization](/online-convex-optimization/) and bandit problems, where the [competitive ratio](/competitive-ratio/) is too strict or not meaningful. An algorithm is *no-regret* if its regret grows more slowly than the number of rounds $T$, so that its average loss per round tends to that of the best fixed action. Swap and internal regret are stronger versions that compare the learner with versions of itself that replace one action by another.

## Definition

**Setting.** A learner and an adversary play $T$ rounds. There is a set $K$ of actions; for experts, $K = \{1, \ldots, n\}$. In round $t$ the learner picks $x_t \in K$, possibly at random, the adversary picks a loss function $\ell_t : K \to [0, 1]$, and the learner pays $\ell_t(x_t)$ and sees $\ell_t$. For experts we write $\ell_{t,i} = \ell_t(i)$; a learner that picks expert $i$ with probability $p_{t,i}$ has expected loss $p_t \cdot \ell_t$ in round $t$.

**External regret.** The (external) regret of the learner after $T$ rounds is

$$R_T = \sum_{t=1}^{T} \ell_t(x_t) - \min_{x \in K} \sum_{t=1}^{T} \ell_t(x).$$

The comparator is the best *fixed* action in hindsight, chosen after all losses are known but the same in every round. When the word "regret" stands alone, it means this quantity.

**Expected regret and pseudo-regret.** For a randomized learner, the expected regret is $\mathbb{E}[R_T]$. The *pseudo-regret* is

$$\bar R_T = \max_{x \in K} \mathbb{E}\left[\sum_{t=1}^{T} \ell_t(x_t) - \ell_t(x)\right] \le \mathbb{E}[R_T],$$

which puts the maximum outside the expectation; the inequality holds because the expectation of a maximum is at least the maximum of the expectations. Against an [oblivious adversary](/oblivious-adversary/), which fixes $\ell_1, \ldots, \ell_T$ in advance, the comparator does not depend on the learner's coins and the two are equal. In a [multi-armed bandit](/multi-armed-bandit/) with random losses they can differ, and bandit bounds are often stated for $\bar R_T$.

**Swap and internal regret.** For experts with distributions $p_t$, and for a map $\varphi : K \to K$, let

$$R_T(\varphi) = \sum_{t=1}^{T} \sum_{i \in K} p_{t,i}\,\bigl(\ell_{t,i} - \ell_{t,\varphi(i)}\bigr).$$

This is how much the learner would gain if it played $\varphi(i)$ each time it played $i$. The *swap regret* is $\max_\varphi R_T(\varphi)$ over all maps. The *internal regret* is the maximum over the maps that move one action $i$ to one action $j$ and fix the others. The external regret is $\max_\varphi R_T(\varphi)$ over the constant maps.

**Scale and rates.** A learner is *no-regret*, or *Hannan consistent*, if $\sup R_T / T \to 0$ as $T \to \infty$, the supremum taken over the adversaries of the stated kind. With losses in $[a, b]$ in place of $[0, 1]$, every regret scales by $b - a$. Bounds are stated as functions of $T$, of $n = |K|$ (or of the diameter of $K$), and of the loss range.

## Examples and non-examples

**A worked example.** Two experts, four rounds, and the learner follows the leader (it picks the expert with the least total loss so far, the lower index on ties).

| round $t$ | $\ell_{t,1}$ | $\ell_{t,2}$ | learner picks | learner loss |
|---|---|---|---|---|
| 1 | 1/2 | 0 | 1 | 1/2 |
| 2 | 0 | 1 | 2 | 1 |
| 3 | 1 | 0 | 1 | 1 |
| 4 | 0 | 1 | 2 | 1 |

The learner loses $7/2$, expert 1 loses $3/2$ and expert 2 loses $2$, so $R_4 = 7/2 - 3/2 = 2$. If the pattern goes on, $R_T \approx T/2$, so [follow the leader](/follow-the-leader/) is not no-regret.

**Good rates.** [Hedge](/multiplicative-weights-update/) has $\mathbb{E}[R_T] \le \sqrt{(T/2) \ln n}$ for experts. [Online gradient descent](/online-gradient-descent/) has $R_T \le \frac32 GD\sqrt{T}$ for convex Lipschitz losses on a set of diameter $D$, and $O((G^2/\lambda)\log T)$ for $\lambda$-strongly convex losses.

**The lower bound.** For each learner and for $n \ge 2$ experts with losses in $[0, 1]$, an oblivious adversary with random losses forces $\mathbb{E}[R_T] \ge (1 - o(1))\sqrt{(T/2)\ln n}$ as $T$ and then $n$ grow (Cesa-Bianchi et al. 1997; Cesa-Bianchi and Lugosi 2006, Chapter 3). So $\Theta(\sqrt{T \ln n})$ is the right rate of external regret, and Hedge attains it with the right constant.

**Deterministic learners have linear regret.** If the adversary knows the learner's choice in round $t$ before it fixes $\ell_t$ (as it does for a deterministic learner), it gives loss $1$ to the chosen expert and $0$ to the other of two experts. The learner loses $T$, and the two experts lose $T$ in total, so one of them loses at most $T/2$, and $R_T \ge T/2$. A no-regret learner must hide its choice in each round, which is why the [expert problem](/expert-problem/) uses randomized learners against an oblivious or a suitably restricted [adaptive adversary](/adaptive-adversary/).

**Non-example: the best action in each round.** The sum $\sum_t \min_x \ell_t(x)$ is not a useful comparator. If the two losses are $(1, 0)$ or $(0, 1)$ with probability $1/2$ each, independently in each round, every learner loses $T/2$ in expectation while $\sum_t \min_x \ell_t(x) = 0$. Comparing with a sequence of actions needs a limit on how often the sequence switches, as in *tracking regret* or *dynamic regret*.

**Non-example: the competitive ratio.** The competitive ratio compares $\mathrm{ALG}(\sigma)$ with the best offline solution, which may change its state at any time, and takes a quotient, not a difference. A regret bound of $o(T)$ says nothing about the ratio, and a ratio bound says nothing about the regret.

**Swap regret is stronger.** Every constant map is a swap, so external regret is at most swap regret, and swap regret is at most $n$ times internal regret, since a swap map splits into at most $n$ moves of one action. The converse fails: a learner can have external regret $O(\sqrt{T \ln n})$ and linear internal regret. Blum and Mansour (2007) turn any external-regret learner into one with swap regret $O(\sqrt{T n \ln n})$.

## Related definitions

- [Expert problem](/expert-problem/) and [online convex optimization](/online-convex-optimization/): the two main settings where regret is the goal.
- [Competitive ratio](/competitive-ratio/): the measure for online problems with a state, compared with a dynamic offline optimum.
- [Oblivious adversary](/oblivious-adversary/) and [adaptive adversary](/adaptive-adversary/): what the adversary may see, which decides whether expected regret and pseudo-regret agree.
- [Nash equilibrium](/nash-equilibrium/) and [zero-sum games](/zero-sum-game/): if all players use no-external-regret learners, the empirical play tends to the set of coarse correlated equilibria; with no internal regret, to correlated equilibria (Foster and Vohra 1997). In a two-player zero-sum game the average strategies tend to the value of the game, which gives a proof of the [minimax theorem](/minimax-theorem/).
- [Counterfactual regret minimization](/counterfactual-regret-minimization/): regret minimization at each information set of an extensive-form game.
- [Doubling trick](/doubling-trick/): turns a regret bound that needs $T$ in advance into one that does not, at a constant factor.

## References
