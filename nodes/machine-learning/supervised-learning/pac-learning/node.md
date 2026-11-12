---
tag: H72WSE
kind: model
slug: pac-learning
name: PAC learning
aliases:
- probably approximately correct learning
- PAC model
- realizable PAC learning
- Valiant's learning model
area: machine-learning/supervised-learning
level: core
summary: "Valiant's model of learning from examples: from i.i.d. examples labeled by a target in the class, output with probability at least 1 - delta a hypothesis of error at most epsilon."
prereqs: [hypothesis-class, empirical-risk-minimization, union-bound]
see_also: [agnostic-pac-learning, vc-dimension, fundamental-theorem-of-statistical-learning, statistical-query-model, weak-learnability-equivalence, occams-razor, epsilon-net-theorem, halfspace-learning]
sources:
  - paper: doi:10.1145/1968.1972
    title: L. G. Valiant, A theory of the learnable, Communications of the ACM 27(11), 1984
    locator: pp. 1134 to 1142 (the model, and the learnability of conjunctions and other Boolean classes)
  - book: isbn:9781107057135
    title: Shai Shalev-Shwartz and Shai Ben-David, Understanding Machine Learning, From Theory to Algorithms, Cambridge University Press, 2014
    locator: Corollary 2.3 (finite classes, realizable), Definition 3.1 and Corollary 3.2 (PAC learnability, the bound with a ceiling), Chapter 8 (runtime, Section 8.3 on 3-term DNF), Chapter 21 (online learning and the Littlestone dimension)
  - book: isbn:9780262111935
    title: Michael J. Kearns and Umesh V. Vazirani, An Introduction to Computational Learning Theory, MIT Press, 1994
    locator: Chapter 1 (the PAC model, efficient learning, conjunctions, 3-term DNF), Chapter 6 (inherent unpredictability under cryptographic assumptions)
  - book: isbn:9780262039406
    title: Mehryar Mohri, Afshin Rostamizadeh and Ameet Talwalkar, Foundations of Machine Learning, second edition, MIT Press, 2018
    locator: Chapter 2 (Definition 2.3 of PAC learning, Theorem 2.5 for finite consistent learners), Theorem 3.20 (the realizable lower bound)
  - paper: doi:10.1145/48014.63140
    title: L. Pitt and L. G. Valiant, Computational limitations on learning from examples, Journal of the ACM 35(4), 1988
    locator: pp. 965 to 984 (proper learning of k-term DNF is hard unless RP = NP)
  - paper: doi:10.1145/76359.76371
    title: A. Blumer, A. Ehrenfeucht, D. Haussler and M. K. Warmuth, Learnability and the Vapnik-Chervonenkis dimension, Journal of the ACM 36(4), 1989
    locator: pp. 929 to 965 (finite VC dimension characterizes PAC learnability)
---

PAC learning (probably approximately correct learning) is the model of learning from examples that Leslie Valiant defined in 1984. A learner receives examples drawn i.i.d. from an unknown distribution and labeled by an unknown target function from a known [hypothesis class](/hypothesis-class/). It must output, with probability at least $1 - \delta$, a hypothesis whose error on new examples is at most $\varepsilon$. The model counts the examples that this needs (the sample complexity) and, in Valiant's full form, the running time. Its central results are that every finite class is learnable with $\lceil \ln(|H|/\delta)/\varepsilon \rceil$ examples and that a binary class is learnable exactly when its [VC dimension](/vc-dimension/) is finite.

## The machine

**Data model (realizable setting).** $X$ is a domain and $H$ a class of functions $h : X \to \{0, 1\}$. An unknown distribution $D$ on $X$ and an unknown target $f : X \to \{0, 1\}$ fix the task. The learner sees $S = ((x_1, f(x_1)), \ldots, (x_n, f(x_n)))$ with $x_1, \ldots, x_n$ drawn i.i.d. from $D$. The error of a hypothesis $h$ is

$$L_{D, f}(h) = \Pr_{x \sim D}[h(x) \ne f(x)].$$

The **realizability assumption** says that some $h^\star \in H$ has $L_{D, f}(h^\star) = 0$.

**Definition (PAC learnability).** $H$ is PAC learnable if there are a function $m_H : (0, 1)^2 \to \mathbb{N}$ and a learning algorithm $A$ with this property: for every $\varepsilon, \delta \in (0, 1)$, every distribution $D$ on $X$ and every target $f$ for which the realizability assumption holds, if $A$ gets $n \ge m_H(\varepsilon, \delta)$ examples, then with probability at least $1 - \delta$ over the sample (and the coins of $A$), $L_{D, f}(A(S)) \le \varepsilon$. This is Definition 3.1 of Shalev-Shwartz and Ben-David.

- **Probably** refers to $\delta$, the chance that the sample is misleading. **Approximately correct** refers to $\varepsilon$, the error that is allowed.
- The bound $m_H(\varepsilon, \delta)$ must hold for **every** $D$ and every realizable $f$. The learner does not know $D$. This is why the model is called distribution free.
- The **sample complexity** of $H$ is the smallest function $m_H$ that works for some algorithm.

**Efficient PAC learning.** Valiant's definition also asks for a fast learner. The classes come in a family $H_d$ over domains $X_d$ (for example conjunctions over $d$ variables), and each target has a representation size $s$. A learner is efficient when its running time is polynomial in $1/\varepsilon$, $1/\delta$, $d$ and $s$, and its output can be evaluated in polynomial time. Kearns and Vazirani, Chapter 1, give this form. Shalev-Shwartz and Ben-David keep the statistical part in Chapter 3 and add the runtime in Chapter 8.

**Proper and improper learners.** A learner is **proper** if its output always lies in $H$. It is **improper** (or representation independent) if it may output any efficiently evaluable function. The statistical sample complexity is the same either way up to constant factors, but the running time can differ a lot, as the 3-term DNF result below shows.

## What it counts

- **Examples.** The sample complexity $m_H(\varepsilon, \delta)$, in the worst case over $D$ and the realizable target $f$. The probability is only over the sample and the learner's coins.
- **Time.** For efficient learning, the running time of the learner and of the evaluation of its output, in the worst case.
- **What it does not count.** The learner cannot ask for labels of points that it chooses (that is the model of membership queries), and its mistakes during learning are not counted (that is the online mistake bound model). Label noise is outside the realizable model; the [agnostic model](/agnostic-pac-learning/) and the [statistical query model](/statistical-query-model/) deal with it.

## Relation to other models

- **Agnostic PAC learning.** Drop the realizability assumption and ask for error at most $\min_{h \in H} L_D(h) + \varepsilon$ on an arbitrary distribution of labeled examples. The realizable model is the special case $\min_{h \in H} L_D(h) = 0$. The agnostic model needs about $1/\varepsilon^2$ examples instead of $1/\varepsilon$; see [agnostic PAC learning](/agnostic-pac-learning/).
- **Weak learning.** A weak learner only needs error at most $1/2 - \gamma$ for a fixed $\gamma > 0$. Schapire showed that weak and strong PAC learnability are the same; see [weak learnability equivalence](/weak-learnability-equivalence/) and [boosting](/boosting/).
- **Statistical queries.** A learner that only asks for estimates of expectations is a [statistical query learner](/statistical-query-model/). Such learners tolerate random classification noise, and parities are PAC learnable but not SQ learnable.
- **Online learning.** In Littlestone's mistake bound model the examples may be chosen by an adversary. A class with a finite mistake bound is PAC learnable, but the converse fails: thresholds on $[0, 1]$ are PAC learnable and have infinite Littlestone dimension (Shalev-Shwartz and Ben-David, Chapter 21).
- **Nonuniform learning.** If the sample size may depend on the target $h$ as well, countable unions of learnable classes become learnable; see [structural risk minimization](/structural-risk-minimization/).
- **Geometry.** For the class of indicator functions of a [range space](/range-space/), the realizable sample bound is the [epsilon-net theorem](/epsilon-net-theorem/): a sample that hits every range of weight more than $\varepsilon$ makes every consistent hypothesis $\varepsilon$-accurate.

## Known results in the model

**Finite classes (Shalev-Shwartz and Ben-David, Corollary 2.3 and Corollary 3.2).** Let $H$ be finite. Then every [ERM](/empirical-risk-minimization/) rule is a PAC learner for $H$ with

$$m_H(\varepsilon, \delta) \le \left\lceil \frac{\ln(|H|/\delta)}{\varepsilon} \right\rceil.$$

The book writes $\log$ for the natural logarithm. Corollary 2.3 states the condition $n \ge \ln(|H|/\delta)/\varepsilon$; Corollary 3.2 restates it as the bound with the ceiling.

*Proof.* Let $H_B = \{h \in H : L_{D, f}(h) > \varepsilon\}$ be the bad hypotheses. By realizability, $h^\star$ errs on a set of probability 0, so with probability 1 it errs on no example and $L_S(h^\star) = 0$. Then every ERM output $h_S$ has $L_S(h_S) = 0$. So the learner fails only if some bad hypothesis is consistent with the sample. Fix $h \in H_B$. Each example is labeled correctly by $h$ with probability $1 - L_{D, f}(h) < 1 - \varepsilon$, and the examples are independent, so

$$\Pr[L_S(h) = 0] \le (1 - \varepsilon)^n \le e^{-\varepsilon n},$$

where the last step uses $1 - \varepsilon \le e^{-\varepsilon}$. By the [union bound](/union-bound/) over the at most $|H|$ bad hypotheses, the failure probability is at most $|H| e^{-\varepsilon n}$. This is at most $\delta$ when $n \ge \ln(|H|/\delta)/\varepsilon$. $\blacksquare$

*Numbers.* For $|H| = 2^{10} = 1024$, $\varepsilon = 0.05$ and $\delta = 0.01$, the bound is $\lceil \ln(102400)/0.05 \rceil = \lceil 230.73 \rceil = 231$ examples, and indeed $1024\, e^{-0.05 \cdot 231} \approx 0.0099 \le 0.01$. The dependence on $|H|$ is logarithmic: $|H| = 2^{20}$ with $\varepsilon = \delta = 0.01$ needs 1847 examples.

**Conjunctions (Valiant 1984).** Conjunctions of literals over $d$ Boolean variables form a class of $3^d + 1$ functions. The elimination algorithm (start with all $2d$ literals, delete each literal that a positive example falsifies) is a proper ERM rule that runs in $O(nd)$ time. With the bound above, $d = 10$, $\varepsilon = 0.1$ and $\delta = 0.05$ need $\lceil \ln(59050/0.05)/0.1 \rceil = 140$ examples. So conjunctions are efficiently PAC learnable.

**Infinite classes.** The class of thresholds $1[x \ge t]$ on $\mathbb{R}$ is infinite and PAC learnable. In general, a binary class is PAC learnable exactly when its VC dimension $d$ is finite (Blumer, Ehrenfeucht, Haussler and Warmuth 1989), and then

$$C_1 \frac{d + \ln(1/\delta)}{\varepsilon} \le m_H(\varepsilon, \delta) \le C_2 \frac{d \ln(1/\varepsilon) + \ln(1/\delta)}{\varepsilon}$$

for absolute constants $C_1, C_2$, the upper bound being achieved by every ERM rule. Hanneke (2016) removed the factor $\ln(1/\varepsilon)$ with an improper learner. The statement, the proof of the qualitative part and the sources are on the page of the [fundamental theorem of statistical learning](/fundamental-theorem-of-statistical-learning/). Mohri, Rostamizadeh and Talwalkar, Theorem 3.20, give an explicit lower bound: for $d > 1$, every learner has, for some realizable $D$ and $f$, error more than $(d - 1)/(32 n)$ with probability at least $1/100$.

**Representation matters.** Pitt and Valiant (1988) proved that properly learning 3-term DNF formulas is NP-hard in the sense that a polynomial proper learner would give RP = NP. Every 3-term DNF formula is a 3-CNF formula, and 3-CNF formulas are efficiently learnable by elimination over the $O(d^3)$ clauses as variables. So 3-term DNF is efficiently PAC learnable by an improper learner (Kearns and Vazirani, Chapter 1; Shalev-Shwartz and Ben-David, Section 8.3).

**Hardness without representation limits.** Under cryptographic assumptions, some classes with polynomial VC dimension, such as polynomial-size Boolean circuits, are not efficiently PAC learnable by any learner (Kearns and Vazirani, Chapter 6). For such classes the sample complexity is small but no polynomial time learner exists, under those assumptions.

**Halfspaces.** In the realizable case, ERM over halfspaces in $\mathbb{R}^d$ is a linear program, so halfspaces are efficiently PAC learnable with $O((d \ln(1/\varepsilon) + \ln(1/\delta))/\varepsilon)$ examples. The agnostic case is much harder; see [halfspace learning](/halfspace-learning/).

## References
