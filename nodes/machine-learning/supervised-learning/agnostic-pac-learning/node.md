---
tag: KASK46
kind: model
slug: agnostic-pac-learning
name: Agnostic PAC learning
aliases:
- agnostic learning
- agnostic PAC model
area: machine-learning/supervised-learning
level: advanced
summary: "PAC learning with no assumption on the labels: from i.i.d. labeled examples, output a hypothesis whose risk is within epsilon of the best in the class, with probability 1 - delta."
prereqs: [pac-learning, hoeffding-inequality]
see_also: [empirical-risk-minimization, fundamental-theorem-of-statistical-learning, rademacher-complexity, bayes-optimal-classifier, halfspace-learning, generalization-error, statistical-query-model, bias-variance-tradeoff]
sources:
  - book: isbn:9781107057135
    title: Shai Shalev-Shwartz and Shai Ben-David, Understanding Machine Learning, From Theory to Algorithms, Cambridge University Press, 2014
    locator: Definitions 3.3 and 3.4 (agnostic PAC learnability), Chapter 4 (Definition 4.3, Corollary 4.4, Corollary 4.6 for finite classes), Section 28.2 (agnostic lower bounds)
  - paper: doi:10.1016/0890-5401(92)90010-D
    title: D. Haussler, Decision theoretic generalizations of the PAC model for neural net and other learning applications, Information and Computation 100(1), 1992
    locator: pp. 78 to 150 (the agnostic model with a general loss, and uniform convergence bounds)
  - paper: doi:10.1007/BF00993468
    title: M. J. Kearns, R. E. Schapire and L. M. Sellie, Toward efficient agnostic learning, Machine Learning 17(2-3), 1994
    locator: pp. 115 to 141 (the name agnostic learning and the computational version of the model)
  - book: isbn:9780262039406
    title: Mehryar Mohri, Afshin Rostamizadeh and Ameet Talwalkar, Foundations of Machine Learning, second edition, MIT Press, 2018
    locator: Theorem 2.13 (finite classes, inconsistent case), Definition 2.14 (agnostic PAC learning), Theorem 3.23 (the agnostic lower bound)
  - paper: "S. Shalev-Shwartz, O. Shamir, N. Srebro and K. Sridharan, Learnability, stability and uniform convergence, Journal of Machine Learning Research 11, 2010"
    locator: pp. 2635 to 2670 (in the general learning setting, learnability does not imply uniform convergence)
---

Agnostic PAC learning is the version of [PAC learning](/pac-learning/) that makes no assumption about how the labels arise. The examples come i.i.d. from an arbitrary distribution on inputs and labels, so the labels may be noisy and no hypothesis of the class need be perfect. The learner must output, with probability at least $1 - \delta$, a hypothesis whose risk is at most the least risk in the class plus $\varepsilon$. Haussler (1992) formalized the model for general losses, and Kearns, Schapire and Sellie (1994) named it and studied its computational side. Finite classes need at most $\lceil 2\ln(2|H|/\delta)/\varepsilon^2 \rceil$ examples, and the dependence on $\varepsilon$ is $1/\varepsilon^2$ instead of the $1/\varepsilon$ of the realizable model.

## The machine

**Data model.** $X$ is a domain, $Y$ a label set, and $D$ an unknown distribution on $Z = X \times Y$. The sample $S = (z_1, \ldots, z_n)$, $z_i = (x_i, y_i)$, is drawn i.i.d. from $D$. A [hypothesis class](/hypothesis-class/) $H$ and a loss $\ell : H \times Z \to \mathbb{R}_{\ge 0}$ are fixed. The true risk is $L_D(h) = \mathbb{E}_{z \sim D}[\ell(h, z)]$ and the empirical risk is $L_S(h) = \frac{1}{n}\sum_{i=1}^n \ell(h, z_i)$. For binary classification, $Y = \{0, 1\}$ and $\ell(h, (x, y)) = 1[h(x) \ne y]$.

**Definition (agnostic PAC learnability).** $H$ is agnostic PAC learnable with respect to $\ell$ if there are a function $m_H : (0, 1)^2 \to \mathbb{N}$ and an algorithm $A$ such that for every $\varepsilon, \delta \in (0, 1)$ and every distribution $D$ on $Z$, when $A$ gets $n \ge m_H(\varepsilon, \delta)$ examples, with probability at least $1 - \delta$,

$$L_D(A(S)) \le \min_{h \in H} L_D(h) + \varepsilon.$$

This is Definition 3.3 (0-1 loss) and Definition 3.4 (general loss) of Shalev-Shwartz and Ben-David; when the minimum is not attained, read it as an infimum. The output need not lie in $H$.

**Uniform convergence.** A sample $S$ is $\varepsilon$-representative if $|L_S(h) - L_D(h)| \le \varepsilon$ for all $h \in H$. The class has the uniform convergence property with function $m^{UC}_H$ if for every $\varepsilon, \delta$ and every $D$, a sample of size $n \ge m^{UC}_H(\varepsilon, \delta)$ is $\varepsilon$-representative with probability at least $1 - \delta$ (Definition 4.3).

## What it counts

- **Examples.** The sample complexity $m_H(\varepsilon, \delta)$, worst case over all distributions on $X \times Y$.
- **Excess risk relative to the class.** The target is the best risk in $H$, not the Bayes risk. The gap between the two is the approximation error of $H$, which no amount of data removes; see the error decomposition on the [hypothesis class](/hypothesis-class/) page and the [Bayes optimal classifier](/bayes-optimal-classifier/).
- **Time.** In the computational version of Kearns, Schapire and Sellie, the learner must also run in polynomial time.

## Relation to other models

- **Realizable PAC learning** is the special case where some $h \in H$ has $L_D(h) = 0$ and the labels are a function of $x$. Every agnostic learner is a PAC learner with the same sample size.
- **Random classification noise** (each label flipped with a fixed probability below $1/2$) lies between the two models: the labels are noisy, but the noise has a known form. The [statistical query model](/statistical-query-model/) gives learners that tolerate this noise.
- **Uniform convergence.** Uniform convergence implies agnostic learnability by [ERM](/empirical-risk-minimization/). For binary classification with the 0-1 loss the converse holds too, by the [fundamental theorem](/fundamental-theorem-of-statistical-learning/). For general losses it fails: Shalev-Shwartz, Shamir, Srebro and Sridharan (2010) give learnable problems without uniform convergence, where ERM fails and a stable rule learns.
- **Data dependent bounds.** [Rademacher complexity](/rademacher-complexity/) gives agnostic bounds that depend on the sample, and the [margin bound](/margin-generalization-bound/) gives bounds for real-valued scores.

## Known results in the model

**Uniform convergence suffices (Corollary 4.4).** If $H$ has uniform convergence with $m^{UC}_H$, then every ERM rule is an agnostic PAC learner with $m_H(\varepsilon, \delta) \le m^{UC}_H(\varepsilon/2, \delta)$. The reason is the chain $L_D(h_S) \le L_S(h_S) + \varepsilon/2 \le L_S(h) + \varepsilon/2 \le L_D(h) + \varepsilon$ on an $\varepsilon/2$-representative sample, proved on the [ERM](/empirical-risk-minimization/) page.

**Finite classes (Shalev-Shwartz and Ben-David, Corollary 4.6).** Let $H$ be finite and let $\ell$ take values in $[0, 1]$. Then

$$m^{UC}_H(\varepsilon, \delta) \le \left\lceil \frac{\ln(2|H|/\delta)}{2\varepsilon^2} \right\rceil, \qquad m_H(\varepsilon, \delta) \le m^{UC}_H(\varepsilon/2, \delta) \le \left\lceil \frac{2\ln(2|H|/\delta)}{\varepsilon^2} \right\rceil,$$

and the second bound is achieved by ERM.

*Proof.* Fix $h \in H$. The numbers $\ell(h, z_1), \ldots, \ell(h, z_n)$ are i.i.d., lie in $[0, 1]$ and have mean $L_D(h)$. By [Hoeffding's inequality](/hoeffding-inequality/),

$$\Pr\big[|L_S(h) - L_D(h)| > \varepsilon\big] \le 2 e^{-2 n \varepsilon^2}.$$

By the [union bound](/union-bound/) over the $|H|$ hypotheses, the probability that $S$ is not $\varepsilon$-representative is at most $2|H| e^{-2n\varepsilon^2}$. This is at most $\delta$ when $n \ge \ln(2|H|/\delta)/(2\varepsilon^2)$, which gives the first bound. Corollary 4.4 with $\varepsilon/2$ in place of $\varepsilon$ replaces $2\varepsilon^2$ by $2(\varepsilon/2)^2 = \varepsilon^2/2$, which gives the second. $\blacksquare$

The same argument, read the other way, says: with probability at least $1 - \delta$, every $h \in H$ has $L_D(h) \le L_S(h) + \sqrt{\ln(2|H|/\delta)/(2n)}$ (Mohri, Rostamizadeh and Talwalkar, Theorem 2.13, in the form $\sqrt{(\ln|H| + \ln(2/\delta))/(2n)}$).

*Numbers.* For $|H| = 1024$, $\varepsilon = 0.05$ and $\delta = 0.01$:

| setting | bound | examples |
|---|---|---|
| realizable, $\lceil \ln(\lvert H \rvert/\delta)/\varepsilon \rceil$ | Corollary 3.2 | 231 |
| uniform convergence, $\lceil \ln(2\lvert H \rvert/\delta)/(2\varepsilon^2) \rceil$ | Corollary 4.6 | 2446 |
| agnostic ERM, $\lceil 2\ln(2\lvert H \rvert/\delta)/\varepsilon^2 \rceil$ | Corollary 4.6 | 9784 |

The factor of about 40 between the first and last rows comes from $1/\varepsilon$ against $4/\varepsilon^2$.

**Why $1/\varepsilon^2$ is needed.** Even for two hypotheses, telling a coin of bias $1/2 + \varepsilon$ from one of bias $1/2 - \varepsilon$ with error probability $\delta$ needs on the order of $\ln(1/\delta)/\varepsilon^2$ tosses. Shalev-Shwartz and Ben-David, Section 28.2, turn this into the lower bound $m_H(\varepsilon, \delta) \ge 0.5 \ln(1/(4\delta))/\varepsilon^2$ and, for a class of VC dimension $d$, $m_H(\varepsilon, 1/8) \ge 8d/\varepsilon^2$, under the conditions on $\varepsilon$ stated there. Mohri, Rostamizadeh and Talwalkar, Theorem 3.23, give a lower bound of the same order, $\sqrt{d/(320 n)}$ on the excess error.

**Classes of finite VC dimension.** A binary class of VC dimension $d$ is agnostic PAC learnable with $m_H(\varepsilon, \delta) = \Theta((d + \ln(1/\delta))/\varepsilon^2)$, and ERM achieves this rate. A class of infinite VC dimension is not learnable even in the realizable model. See the [fundamental theorem of statistical learning](/fundamental-theorem-of-statistical-learning/).

**Computation.** The statistical cost of agnostic learning is mild, but the running time is often the obstacle. Agnostic ERM is NP-hard for halfspaces and for axis aligned rectangles, and hard even to approximate within a constant factor; see [ERM](/empirical-risk-minimization/) and [halfspace learning](/halfspace-learning/). Practical methods replace the 0-1 loss by a convex surrogate and then compete with the best surrogate risk, not with the best 0-1 risk.

## References
