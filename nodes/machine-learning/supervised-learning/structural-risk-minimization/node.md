---
tag: NJJCNM
kind: technique
slug: structural-risk-minimization
name: Structural risk minimization
aliases:
- SRM
- SRM principle
area: machine-learning/supervised-learning
level: advanced
summary: "Over nested hypothesis classes with prior weights, pick the hypothesis that minimizes training error plus a class-dependent bound on the generalization gap."
prereqs: [empirical-risk-minimization, agnostic-pac-learning]
see_also: [regularization, minimum-description-length, occams-razor, overfitting, cross-validation, vc-dimension, rademacher-complexity, bias-variance-tradeoff]
sources:
  - book: isbn:9781107057135
    title: Shai Shalev-Shwartz and Shai Ben-David, Understanding Machine Learning, From Theory to Algorithms, Cambridge University Press, 2014
    locator: Chapter 7 (Definition 7.1 nonuniform learnability, Theorems 7.2 and 7.3, Theorem 7.4 and the SRM rule in Section 7.2, Theorem 7.5, Theorem 7.7 for MDL)
  - book: isbn:9780387987804
    title: Vladimir N. Vapnik, The Nature of Statistical Learning Theory, second edition, Springer, 2000
    locator: Chapter 4 (the structural risk minimization principle)
  - book: isbn:9780262039406
    title: Mehryar Mohri, Afshin Rostamizadeh and Ameet Talwalkar, Foundations of Machine Learning, second edition, MIT Press, 2018
    locator: Section 4.3 and Theorem 4.2 (SRM with Rademacher penalties), Theorem 4.4 (cross-validation compared with SRM)
  - paper: doi:10.1109/18.930926
    title: V. Koltchinskii, Rademacher penalties and structural risk minimization, IEEE Transactions on Information Theory 47(5), 2001
    locator: pp. 1902 to 1914 (data dependent penalties)
---

Structural risk minimization (SRM) chooses both a hypothesis and the size of the class it comes from. The learner fixes, before it sees the data, a sequence of [hypothesis classes](/hypothesis-class/) $H_1, H_2, \ldots$ (usually nested) and a weight $w(k) \ge 0$ for each class, with $\sum_k w(k) \le 1$. It then returns the hypothesis that minimizes the training error plus a bound on the generalization gap of its class at confidence $w(k)\delta$. Plain [empirical risk minimization](/empirical-risk-minimization/) over a large class overfits, and over a small class underfits; SRM trades the two terms off from the data. Vapnik and Chervonenkis proposed the principle in the 1970s. Shalev-Shwartz and Ben-David, Chapter 7, prove that it learns every countable union of uniformly convergent classes, even when the union has infinite [VC dimension](/vc-dimension/).

## In plain words

Arrange the candidate models from simple to complex. Give each level some share of your trust, so that the shares add up to at most one. For each level, find the model that fits the training data best, and then add a penalty. The penalty is large when the level is complex or has a small share of trust. Pick the level where the fit plus the penalty is smallest. A complex model wins only when it fits much better than the simple ones. The rule never needs a fixed bound on complexity, but it pays for complexity when the data does not support it.

## When it applies

- The learner can write its hypotheses as a countable union $H = \bigcup_k H_k$ such that each $H_k$ has the uniform convergence property, for example finite VC dimension. A typical structure is nested: $H_1 \subseteq H_2 \subseteq \cdots$, such as polynomials of degree $k$, trees of depth $k$, or linear predictors with $\|w\| \le k$.
- The learner can compute, or bound, the function $\varepsilon_k(n, \delta)$: the least $\varepsilon$ such that $n$ examples make a sample $\varepsilon$-representative for $H_k$ with probability at least $1 - \delta$. For a finite class with a loss in $[0, 1]$, Corollary 4.6 of Shalev-Shwartz and Ben-David (proved on the [agnostic PAC learning](/agnostic-pac-learning/) page) gives
$$\varepsilon_k(n, \delta) = \sqrt{\frac{\ln(2|H_k|/\delta)}{2n}}.$$
- The learner can run ERM, or a good approximation of it, in each class.

The structure and the weights must be chosen before the sample is seen. They are the prior knowledge of the learner.

## The template

Notation: $S$ is a sample of $n$ examples, $L_S$ the empirical risk, $L_D$ the true risk, $\delta$ the confidence parameter.

```pseudo id=main
SRM(S, (H_k), w, δ)                           ▷ Σ_k w(k) ≤ 1, fixed before S is seen
L1  for k = 1, 2, …, K do
L2      h_k ← ERM(H_k, S)                     ▷ least empirical risk in H_k
L3      b_k ← L_S(h_k) + ε_k(n, w(k)·δ)       ▷ training error plus the gap bound of H_k
L4  k⋆ ← the k with the least b_k
L5  return h_{k⋆}
```

Shalev-Shwartz and Ben-David state the rule as $\arg\min_{h \in H} [L_S(h) + \varepsilon_{k(h)}(n, w(k(h))\delta)]$, where $k(h)$ is the least $k$ with $h \in H_k$. For nested classes the loop computes this, because the best $h$ with $k(h) = k$ can be replaced by $h_k$ without a larger $b_k$. For nested classes with weights that decrease in $k$, the penalty grows with $k$, so the loop can stop at a finite $K$: once $\varepsilon_k(n, w(k)\delta)$ exceeds $b_1$, no larger $k$ can win, because $L_S \ge 0$.

**The bound behind the rule (Theorem 7.4).** Let $H = \bigcup_k H_k$ with each $H_k$ uniformly convergent, and let $\sum_k w(k) \le 1$. Then with probability at least $1 - \delta$ over $S$, for every $k$ and every $h \in H_k$,
$$|L_D(h) - L_S(h)| \le \varepsilon_k(n, w(k)\delta).$$

*Proof.* For a fixed $k$, the definition of $\varepsilon_k$ says that the bad event "some $h \in H_k$ has a gap larger than $\varepsilon_k(n, w(k)\delta)$" has probability at most $w(k)\delta$. By the [union bound](/union-bound/) over $k$, some bad event happens with probability at most $\sum_k w(k)\delta \le \delta$. $\blacksquare$

**The guarantee (Theorem 7.5).** On the event of Theorem 7.4, let $h_S$ be the SRM output. For every $h \in H$,
$$L_D(h_S) \le L_S(h_S) + \varepsilon_{k(h_S)} \le L_S(h) + \varepsilon_{k(h)}(n, w(k(h))\delta) \le L_D(h) + 2\varepsilon_{k(h)}(n, w(k(h))\delta).$$
The first and last steps use Theorem 7.4 and the middle step is the choice of the rule. So SRM competes with each $h$ at a rate that depends on the class of $h$. With $w(k) = 6/(\pi^2 k^2)$, Theorem 7.5 of Shalev-Shwartz and Ben-David gives the sample size $m_H^{NUL}(\varepsilon, \delta, h) \le m^{UC}_{H_{k(h)}}(\varepsilon/2, 6\delta/(\pi k(h))^2)$.

**Nonuniform learnability.** A class is *nonuniformly learnable* when some learner, for every $h \in H$, reaches $L_D(A(S)) \le L_D(h) + \varepsilon$ with probability $1 - \delta$ from $m(\varepsilon, \delta, h)$ examples, where the sample size may depend on $h$ but not on $D$ (Definition 7.1). For binary classes, a class is nonuniformly learnable if and only if it is a countable union of agnostic PAC learnable classes (Theorem 7.2), and SRM is a learner for every such class (Theorem 7.3). This is strictly more than [PAC learning](/pac-learning/): the union of all classes of polynomial threshold functions $x \mapsto 1[p(x) \ge 0]$ on $\mathbb{R}$, over all degrees, has infinite VC dimension, so it is not PAC learnable, but SRM learns it.

## Classic examples

**Classes of growing size.** Let $|H_k| = 2^{10k}$, so a member of $H_k$ is named by $10k$ bits. Take $n = 2000$, $\delta = 0.05$ and $w(k) = 6/(\pi^2 k^2)$. Suppose ERM in each class gives the training errors below. The penalty is $\varepsilon_k = \sqrt{(10k \ln 2 + \ln(2/(w(k)\delta)))/(2n)}$.

| $k$ | $L_S(h_k)$ | $w(k)$ | $\varepsilon_k$ | $b_k$ |
|---|---|---|---|---|
| 1 | 0.320 | 0.6079 | 0.0527 | 0.3727 |
| 2 | 0.210 | 0.1520 | 0.0697 | 0.2797 |
| 3 | 0.140 | 0.0675 | 0.0824 | 0.2224 |
| 4 | 0.110 | 0.0380 | 0.0931 | 0.2031 |
| 5 | 0.095 | 0.0243 | 0.1025 | **0.1975** |
| 6 | 0.090 | 0.0169 | 0.1111 | 0.2011 |
| 7 | 0.088 | 0.0124 | 0.1190 | 0.2070 |
| 8 | 0.087 | 0.0095 | 0.1263 | 0.2133 |

SRM returns $h_5$. Plain ERM over $H_1 \cup \cdots \cup H_8$ returns $h_8$, which has the least training error but a worse certified bound, $0.2133$ against $0.1975$. With probability at least $0.95$, $L_D(h_5) \le 0.1975$.

**Minimum description length.** Let $H$ be countable and give each $h$ a binary description $d(h)$ from a prefix-free code. Take $H_k = \{h\}$ for each $h$ and $w(h) = 2^{-|d(h)|}$; Kraft's inequality makes the weights sum to at most 1. Then SRM becomes the rule of [minimum description length](/minimum-description-length/), with the bound $L_D(h) \le L_S(h) + \sqrt{(|d(h)| \ln 2 + \ln(2/\delta))/(2n)}$ for a loss in $[0, 1]$ (Shalev-Shwartz and Ben-David, Theorem 7.7, state it with $|h|$ in place of $|d(h)| \ln 2$, a slightly weaker form since $\ln 2 < 1$). It is a precise form of [Occam's razor](/occams-razor/).

**Norm-bounded linear predictors.** Take $H_k = \{x \mapsto \langle w, x \rangle : \|w\| \le 2^k\}$. The [Rademacher complexity](/rademacher-complexity/) of $H_k$ on data with $\|x\| \le R$ is at most $2^k R/\sqrt{n}$, and SRM over $k$ gives a bound that holds for every norm at once. The data dependent [margin bound](/margin-generalization-bound/) is proved this way.

**Polynomial degree.** In regression or classification with polynomial features, $H_k$ is the set of polynomials of degree at most $k$. SRM picks the degree. In practice the degree is more often picked by [cross-validation](/cross-validation/).

## Variations

- **Rademacher penalties.** Koltchinskii (2001) replaced the VC penalty by the empirical Rademacher complexity of $H_k$ on the sample, which can be much smaller on easy data. Mohri, Rostamizadeh and Talwalkar, Theorem 4.2, prove an SRM guarantee in this form.
- **Regularized loss minimization.** Minimizing $L_S(w) + \lambda \|w\|^2$ is a soft form of SRM over balls of growing radius. The penalty is a smooth function of the complexity instead of the bound $\varepsilon_k$. See [regularization](/regularization/).
- **Validation.** Hold out part of the data, run ERM in each $H_k$ on the rest, and pick $k$ by the held out error. With $K$ classes, the held out error of each $h_k$ is within $\sqrt{\ln(2K/\delta)/(2n_{\text{val}})}$ of its true error. Mohri, Rostamizadeh and Talwalkar, Theorem 4.4, compare this with SRM.
- **Penalty from the VC dimension.** For binary classes of VC dimension $d_k$, use a uniform convergence bound of order $\sqrt{(d_k \ln(n/d_k) + \ln(1/(w(k)\delta)))/n}$; see the [Sauer-Shelah lemma](/sauer-shelah-lemma/) and the [fundamental theorem](/fundamental-theorem-of-statistical-learning/). This is the original form of Vapnik.

## Pitfalls

- **Weights chosen after the data.** The union bound over $k$ is valid only if the structure and the weights are fixed before the sample is drawn. Choosing the classes from the same data breaks the guarantee.
- **The bound is loose.** For moderate $n$, $\varepsilon_k$ is often close to or above the training error, as in the table, and the rule then favours small classes too strongly. Validation or cross-validation often selects better in practice, at the cost of fewer training examples.
- **The prior shapes the rate.** The guarantee for $h$ degrades as $w(k(h))$ shrinks. A hypothesis in a class with a tiny weight needs many more examples. There is no free choice that is good for all targets; see the [no-free-lunch theorem](/no-free-lunch-theorem-learning/).
- **Nonuniform is weaker than uniform.** SRM gives no sample size that works for all $h$ at once. Before the data is seen, the learner cannot say how many examples it needs for a target it does not know.
- **ERM in each class.** The template needs an ERM in each $H_k$. For classes where agnostic ERM is NP-hard, such as halfspaces under the 0-1 loss, the template is a statistical rule, not an efficient algorithm.

## Exercises

1. Keep the training errors and the weights of the table and let $n$ grow. Find, to the nearest thousand, the smallest $n$ for which SRM picks $k = 8$. (Answer: about 108000.)
2. Prove that with $w(k) = 2^{-k}$ the SRM output satisfies $L_D(h_S) \le L_D(h) + 2\varepsilon_{k(h)}(n, 2^{-k(h)}\delta)$ for all $h$, and compare the penalty with that for $w(k) = 6/(\pi^2 k^2)$ for large $k$.
3. Show that the class of all functions from $\mathbb{N}$ to $\{0, 1\}$ with finite support is nonuniformly learnable, but not PAC learnable.
4. Show that the set of all binary functions on $\mathbb{R}$ is not a countable union of classes $H_k$ of finite VC dimension. (Hint: pick disjoint finite sets $A_k$ with $|A_k| = \mathrm{VC}(H_k) + 1$, and build a function that, on each $A_k$, has a labeling that $H_k$ does not realize.)

## References
