---
tag: XAZCTX
kind: theorem
slug: weak-learnability-equivalence
name: Equivalence of weak and strong learnability
aliases:
- Schapire's theorem
- weak learning implies strong learning
area: machine-learning/supervised-learning
level: advanced
summary: "A class is PAC learnable if and only if some efficient learner always does slightly better than random guessing. Boosting turns such a weak learner into a strong one."
prereqs: [pac-learning]
see_also: [adaboost, boosting, decision-stump, vc-dimension, fundamental-theorem-of-statistical-learning, margin-generalization-bound, multiplicative-weights-update, statistical-query-model]
sources:
  - paper: doi:10.1007/BF00116037
    title: Robert E. Schapire, The strength of weak learnability, Machine Learning 5(2), 1990
    locator: the first proof that weak learnability implies strong learnability, by recursive majorities of three
  - paper: doi:10.1006/inco.1995.1136
    title: Yoav Freund, Boosting a weak learning algorithm by majority, Information and Computation 121(2), 1995
    locator: boost by majority, a single majority vote, and the lower bound on the number of weak hypotheses
  - paper: doi:10.1006/jcss.1997.1504
    title: Yoav Freund and Robert E. Schapire, A decision-theoretic generalization of on-line learning and an application to boosting, Journal of Computer and System Sciences 55(1), 1997
    locator: Section 4 (AdaBoost and the training error bound, Theorem 6)
  - book: isbn:9781107057135
    title: Shai Shalev-Shwartz and Shai Ben-David, Understanding Machine Learning, Cambridge University Press, 2014
    locator: Chapter 10 (weak learnability, Definition 10.1; AdaBoost, Theorem 10.2; the VC dimension of weighted majorities, Section 10.3)
  - book: isbn:9780262017183
    title: Robert E. Schapire and Yoav Freund, Boosting, Foundations and Algorithms, MIT Press, 2012
    locator: Chapter 3 (the training error of AdaBoost) and Chapter 4 (generalization by VC theory and by sample compression)
  - paper: "Michael Kearns and Leslie G. Valiant, Cryptographic limitations on learning Boolean formulae and finite automata, STOC 1989; Journal of the ACM 41(1), 1994"
    locator: the question whether weak learnability implies strong learnability
---

A learning algorithm is *weak* if it always does a little better than random guessing, and *strong* if it reaches any accuracy we ask for. Kearns and Valiant asked whether the two notions of learnability are the same. Schapire (1990) proved that they are: any class that has an efficient weak learner, one that works for every distribution, also has an efficient strong learner. The proof is constructive. It runs the weak learner many times on reweighted data and takes a vote, which is the idea of [boosting](/boosting/). The cleanest proof today uses [AdaBoost](/adaboost/) of Freund and Schapire (1997), whose training error falls like $\exp(-2\sum_t \gamma_t^2)$.

## Statement

Let $C$ be a class of targets $c : X \to \{0, 1\}$, written here with labels in $\{-1, +1\}$.

- $C$ is *strongly learnable* (that is, [PAC learnable](/pac-learning/)) if there is an algorithm that, for every $c \in C$, every distribution $D$ on $X$ and every $\varepsilon, \delta \in (0, 1)$, given examples $(x, c(x))$ with $x \sim D$, outputs $h$ with $\Pr_{x \sim D}[h(x) \ne c(x)] \le \varepsilon$ with probability at least $1 - \delta$.
- $C$ is *weakly learnable* with edge $\gamma > 0$ if there is an algorithm that, for every $c \in C$, every $D$ and every $\delta$, outputs $h$ with $\Pr_{x \sim D}[h(x) \ne c(x)] \le \frac12 - \gamma$ with probability at least $1 - \delta$.

In the efficient version, the running times are polynomial in $1/\varepsilon$, $\log(1/\delta)$, the dimension and the size of $c$, and $1/\gamma$ is bounded by such a polynomial.

**Theorem (Schapire 1990).** A class is efficiently weakly learnable if and only if it is efficiently strongly learnable. The weak learner may output hypotheses from any class $B$ of [VC dimension](/vc-dimension/) $d_B$, and the strong learner outputs a weighted majority vote of them.

**Theorem (Freund and Schapire 1997, the training error of AdaBoost).** Run AdaBoost for $T$ rounds on a sample $S$ of $m$ examples. If the weak hypothesis of round $t$ has weighted error $\varepsilon_t = \frac12 - \gamma_t$ on the distribution of round $t$, then the vote $H = \mathrm{sign}(f_T)$ satisfies

$$\frac1m \big|\{i : H(x_i) \ne y_i\}\big| \;\le\; \prod_{t=1}^{T} 2\sqrt{\varepsilon_t (1 - \varepsilon_t)} \;=\; \prod_{t=1}^{T} \sqrt{1 - 4\gamma_t^2} \;\le\; \exp\Big(-2 \sum_{t=1}^{T} \gamma_t^2\Big).$$

In particular, if every $\gamma_t \ge \gamma$, then $T > \ln(m)/(2\gamma^2)$ rounds give zero training error.

## In plain words

Suppose you have a rule of thumb that is right 55% of the time, whatever mix of examples you show it. Run it once. Then build a new mix of examples where it was right on exactly half of the weight, by giving more weight to its mistakes, and run it again on that mix. The second rule must be right on 55% of the new mix, so it must learn something the first rule missed. Repeat, and let all the rules vote, with more say for the more accurate ones. Each round removes a fixed fraction of the remaining "badness", so the vote soon makes no mistakes on the training data. Because the vote is built from few simple rules, it also does well on new data.

## Proof

**Strong implies weak.** A strong learner run with $\varepsilon = \frac12 - \gamma$ is a weak learner with edge $\gamma$.

**Weak implies strong.** Draw a sample $S = ((x_1, y_1), \ldots, (x_m, y_m))$ from $D$ labeled by $c$, and run AdaBoost:

```pseudo id=adaboost-in-proof
D_1(i) ← 1/m for i = 1..m
for t = 1..T:
    h_t ← WeakLearner run on examples drawn from D_t (a distribution on S)
    ε_t ← Σ_i D_t(i) · [h_t(x_i) ≠ y_i]
    α_t ← ½ ln((1 − ε_t) / ε_t)
    D_{t+1}(i) ← D_t(i) · exp(−α_t y_i h_t(x_i)) / Z_t     (Z_t makes the weights sum to 1)
return H(x) = sign(f_T(x)), where f_T = Σ_t α_t h_t
```

Each $D_t$ is a distribution on $X$ (supported on the points of $S$) labeled by $c$, so the weak learner applies to it: with probability at least $1 - \delta/(2T)$ it returns $h_t$ with $\varepsilon_t \le \frac12 - \gamma$. By the [union bound](/union-bound/), all $T$ rounds succeed with probability at least $1 - \delta/2$.

*Step 1: the final weights.* Unrolling the update,

$$D_{T+1}(i) = \frac{1}{m} \cdot \frac{\exp(-y_i f_T(x_i))}{\prod_{t=1}^{T} Z_t}.$$

*Step 2: training error is at most the exponential loss.* If $H(x_i) \ne y_i$, then $y_i f_T(x_i) \le 0$ and $\exp(-y_i f_T(x_i)) \ge 1$. So, using that the $D_{T+1}(i)$ sum to 1,

$$\frac1m \big|\{i : H(x_i) \ne y_i\}\big| \le \frac1m \sum_{i=1}^{m} \exp(-y_i f_T(x_i)) = \prod_{t=1}^{T} Z_t.$$

*Step 3: each normalizer.* Correct examples are multiplied by $e^{-\alpha_t}$ and wrong ones by $e^{\alpha_t}$, so

$$Z_t = (1 - \varepsilon_t) e^{-\alpha_t} + \varepsilon_t e^{\alpha_t}.$$

This is minimized by $\alpha_t = \frac12 \ln \frac{1 - \varepsilon_t}{\varepsilon_t}$, where $e^{\alpha_t} = \sqrt{(1 - \varepsilon_t)/\varepsilon_t}$ and $Z_t = 2\sqrt{\varepsilon_t (1 - \varepsilon_t)} = \sqrt{1 - 4\gamma_t^2}$.

*Step 4: the exponential form.* Since $1 - x \le e^{-x}$, $\sqrt{1 - 4\gamma_t^2} \le e^{-2\gamma_t^2}$. Multiplying over $t$ proves the training error theorem.

*Step 5: zero training error.* With $\gamma_t \ge \gamma$ and $T = \lfloor \ln(m)/(2\gamma^2) \rfloor + 1$, the training error is below $e^{-\ln m} = 1/m$. It is a multiple of $1/m$, so it is 0. The vote $H$ is consistent with $S$.

*Step 6: generalization (sketch).* $H$ belongs to the class of weighted majorities of $T$ hypotheses from $B$. This class has VC dimension $O(T d_B \log(T d_B))$ (Shalev-Shwartz and Ben-David, Section 10.3). With $T = O(\log(m)/\gamma^2)$, the VC dimension grows only like a polylogarithm of $m$, so by the consistent-learner bound of the [fundamental theorem](/fundamental-theorem-of-statistical-learning/), a sample size $m$ polynomial in $d_B$, $1/\gamma$, $1/\varepsilon$ and $\log(1/\delta)$ makes the error of $H$ at most $\varepsilon$ with probability $1 - \delta/2$. A second route uses sample compression: if the weak learner looks at $k$ examples per round, $H$ is determined by $Tk$ examples of $S$, and a compression bound gives the same conclusion (Schapire and Freund 2012, Chapter 4). AdaBoost makes $T$ calls to the weak learner plus $O(mT)$ other work, so the strong learner is efficient. $\blacksquare$

### Check with decision stumps

The code for this page runs AdaBoost with [decision stumps](/decision-stump/) (a threshold on one coordinate) on 200 points uniform in $[-1, 1]^2$, labeled $+1$ inside the circle $x^2 + y^2 < 0.5$, with seed 1. The test error uses 5000 fresh points (seed 2). No single stump is good here, but every stump that the algorithm picks has an edge.

| round $T$ | $\varepsilon_T$ | training error | $\prod Z_t$ | $\exp(-2\sum \gamma_t^2)$ | test error |
|---|---|---|---|---|---|
| 1 | 0.3850 | 0.385 | 0.9732 | 0.9739 | 0.4322 |
| 3 | 0.3409 | 0.225 | 0.8784 | 0.8835 | 0.2778 |
| 10 | 0.3495 | 0.120 | 0.6375 | 0.6509 | 0.1738 |
| 20 | 0.3411 | 0.015 | 0.4421 | 0.4580 | 0.0562 |
| 35 | 0.3786 | 0 | 0.3007 | 0.3146 | 0.0370 |
| 50 | 0.3875 | 0.005 | 0.2199 | 0.2318 | 0.0374 |
| 100 | 0.4304 | 0 | 0.1076 | 0.1146 | 0.0412 |
| 400 | 0.4493 | 0 | 0.0098 | 0.0106 | 0.0444 |

The tests check, at each of 300 rounds, that the training error is at most $\prod Z_t$, which is at most $\exp(-2\sum \gamma_t^2)$; that $\prod Z_t$ equals the average exponential loss; and that after each update the stump just chosen has weighted error exactly $\frac12$ on the new distribution. Two things in the table are worth noting. The training error is not monotone: it is 0 at round 35 and 0.005 at round 50, because the theorem bounds the exponential loss, not the error itself. And the edges shrink, from $\gamma_1 = 0.115$ to $\gamma_{400} \approx 0.05$, so the bound with a fixed $\gamma$ is pessimistic. On a smaller sample of 30 points, a test checks Step 5: at every round where $\exp(-2\sum \gamma_t^2) < 1/30$, the training error is 0.

## Consequences

- **Learning is all or nothing.** For distribution-free learning there is no class that can be learned to 55% accuracy but not to 99%. To show a class is PAC learnable, it suffices to beat random guessing by $1/\mathrm{poly}$ on every distribution.
- **Hardness transfers.** If a class is not efficiently PAC learnable (for example under a cryptographic assumption, as Kearns and Valiant showed for Boolean formulae), then it is not even efficiently weakly learnable.
- **Boosting algorithms.** The proof gave rise to boosting as a practical method; AdaBoost with trees or stumps is one of the most used classifiers. The vote's margin explains why the test error often keeps falling after the training error is 0; see [margin generalization bounds](/margin-generalization-bound/).
- **Compression and size.** Since a strong learner can be built from $O(\log(1/\varepsilon)/\gamma^2)$ weak hypotheses (Freund 1995), every PAC learnable class has learners whose output is a small vote, which gives bounds on the size of hypotheses and on sample complexity.
- **Game theory.** AdaBoost is the [multiplicative weights](/multiplicative-weights-update/) method applied to a zero-sum game between examples and weak hypotheses; weak learnability for every distribution is, by the minimax theorem, the same as the existence of a weighted vote with margin $2\gamma$ on every example.

## Tightness

- **The number of rounds.** Freund (1995) showed that, in the worst case, a majority vote of weak hypotheses with edge $\gamma$ needs $\Omega(\log(1/\varepsilon)/\gamma^2)$ of them to reach error $\varepsilon$, and his boost-by-majority algorithm meets this bound. AdaBoost meets it up to a constant on the training sample.
- **The bound per round.** If every round has error exactly $\frac12 - \gamma$, then $\prod Z_t = (1 - 4\gamma^2)^{T/2}$, and the only loss in the theorem is the step $\sqrt{1 - 4\gamma^2} \le e^{-2\gamma^2}$, which is tight as $\gamma \to 0$.
- **"Every distribution" cannot be dropped.** Under one fixed distribution, weak learning does not imply strong learning. Let $D$ be uniform on $\{0, 1\}^{d+1}$ and let $C$ contain every $c(x) = x_0 \vee g(x_1, \ldots, x_d)$ with $g$ arbitrary. The rule "predict 1 if $x_0 = 1$, else guess" has error $1/4$ on every target, but on the half of the inputs with $x_0 = 0$ the target is an arbitrary function, so by the [no free lunch theorem](/no-free-lunch-theorem-learning/) no learner gets error near 0 from a small sample when $d$ is large.
- **Noise.** The theorem is for the realizable case. With random label noise, AdaBoost puts more and more weight on the noisy examples, and boosters that minimize a convex potential can be made to fail by such noise (Long and Servedio 2010).

## History

Kearns and Valiant (1989) defined weak learnability and asked whether it equals strong learnability. Schapire (1990) answered yes with a recursive construction that filters the examples into three distributions and takes majorities of three. Freund (1995) gave boost by majority, which uses a single vote with the optimal number of weak hypotheses but needs to know $\gamma$ in advance. Freund and Schapire (1997) gave AdaBoost, which adapts to the actual edges $\gamma_t$ and became the standard algorithm. They received the 2003 Gödel Prize for this paper.

## References
