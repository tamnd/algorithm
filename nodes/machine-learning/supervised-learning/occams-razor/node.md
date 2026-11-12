---
tag: XZEN4M
kind: concept
slug: occams-razor
name: Occam's razor in learning
aliases:
- Occam learning
- Occam algorithm
area: machine-learning/supervised-learning
level: intro
summary: "A consistent hypothesis that can be written in few bits generalizes: with probability 1 - delta its true error is at most (|h| ln 2 + ln(1/delta))/n."
prereqs: [pac-learning, union-bound, kraft-inequality]
see_also: [minimum-description-length, structural-risk-minimization, no-free-lunch-theorem-learning, generalization-error, greedy-set-cover, elias-gamma-coding, hypothesis-class, overfitting]
sources:
  - paper: doi:10.1016/0020-0190(87)90114-1
    title: Anselm Blumer, Andrzej Ehrenfeucht, David Haussler and Manfred K. Warmuth, Occam's razor, Information Processing Letters 24(6), 1987
    locator: the theorem that a consistent hypothesis of b bits needs about (b ln 2 + ln(1/delta))/epsilon examples, and the definition of an Occam algorithm
  - paper: doi:10.1145/76359.76371
    title: Anselm Blumer, Andrzej Ehrenfeucht, David Haussler and Manfred K. Warmuth, Learnability and the Vapnik-Chervonenkis dimension, Journal of the ACM 36(4), 1989
    locator: the Occam results for classes of infinite size
  - book: isbn:9780262111935
    title: Michael J. Kearns and Umesh V. Vazirani, An Introduction to Computational Learning Theory, MIT Press, 1994
    locator: Chapter 2 (Occam's razor, Occam algorithms, and the greedy set cover learner for conjunctions with few relevant variables)
  - book: isbn:9781107057135
    title: Shai Shalev-Shwartz and Shai Ben-David, Understanding Machine Learning, Cambridge University Press, 2014
    locator: Section 7.3 (minimum description length and Occam's razor, the agnostic bound with prefix-free descriptions)
---

Occam's razor in learning is the theorem that short hypotheses generalize. Fix a prefix-free language for writing down hypotheses, and write $|h|$ for the number of bits of $h$. Then, with probability at least $1 - \delta$ over $n$ independent examples, every hypothesis $h$ that fits all the examples has true error at most $(|h| \ln 2 + \ln(1/\delta))/n$. Blumer, Ehrenfeucht, Haussler and Warmuth (1987) proved this and used it to show that an *Occam algorithm*, one that finds a short consistent hypothesis, is a [PAC learner](/pac-learning/). The old philosophical rule, "do not use more entities than you need", gets here a precise and limited meaning.

## In plain words

If a rule that fits your data is short to write down, you can trust it more than a long rule that fits equally well. The reason is counting, not a belief that nature is simple. There are few short rules, so it is unlikely that a bad short rule fits many random examples by luck. There are many long rules, so some bad long rule will fit by luck. The number of examples you need grows with the length of the rule, in bits. "Short" is measured in a language that you choose before you see the data.

## The idea

**The setting.** Examples $(x, y)$ come independently from a distribution $D$, labeled by an unknown target. $L_D(h)$ is the [true error](/generalization-error/) of $h$, and $h$ is *consistent* with a sample if it labels every example correctly. A description language is a map from bit strings to hypotheses, and $|h|$ is the length of the shortest string for $h$. The language is *prefix-free*: no code word is a prefix of another. So, by the [Kraft inequality](/kraft-inequality/), $\sum_h 2^{-|h|} \le 1$.

**Theorem (the Occam bound).** For every $\delta \in (0, 1)$, with probability at least $1 - \delta$ over a sample of $n$ examples, every $h$ consistent with the sample has

$$L_D(h) \le \varepsilon_h = \frac{|h| \ln 2 + \ln(1/\delta)}{n}.$$

*Proof.* Fix a hypothesis $h$ with $L_D(h) > \varepsilon_h$. Each example is labeled correctly by $h$ with probability less than $1 - \varepsilon_h$, so $h$ is consistent with the whole sample with probability less than

$$(1 - \varepsilon_h)^n \le e^{-\varepsilon_h n} = \delta\, 2^{-|h|}.$$

By the [union bound](/union-bound/) over all such hypotheses, the probability that at least one of them is consistent is less than $\sum_h \delta\, 2^{-|h|} \le \delta$, by Kraft. On the remaining event, every consistent $h$ has $L_D(h) \le \varepsilon_h$. $\blacksquare$

The proof is the finite class bound of [generalization error](/generalization-error/) with a different budget for each hypothesis: a hypothesis of $b$ bits gets the share $\delta\, 2^{-b}$ of the failure probability. Read as a sample size: if the learner returns a consistent hypothesis of at most $b$ bits, then

$$n \ge \frac{b \ln 2 + \ln(1/\delta)}{\varepsilon}$$

examples give error at most $\varepsilon$ with probability at least $1 - \delta$. If the lengths are not prefix-free, the same argument applied to the at most $2^{b+1}$ strings of length at most $b$ gives $((b + 1) \ln 2 + \ln(1/\delta))/\varepsilon$.

**Occam algorithms.** The size of the hypothesis may grow with $n$, and the bound still works if it grows slowly. Blumer et al. call a learner an $(\alpha, \beta)$-Occam algorithm, with $\alpha \ge 0$ and $0 \le \beta < 1$, if on $n$ examples of a target of size $s$ in dimension $d$ it returns, in polynomial time, a consistent hypothesis of at most $(d s)^\alpha n^\beta$ bits. Then $b \ln 2 / n \to 0$ as $n$ grows, and a sample of size polynomial in $1/\varepsilon$, $\ln(1/\delta)$, $d$ and $s$ makes the bound at most $\varepsilon$ (the exponent of $1/\varepsilon$ is $1/(1 - \beta)$). So an Occam algorithm is a PAC learner (Kearns and Vazirani, Chapter 2). The learner does not need to find the shortest consistent hypothesis, only one that is shorter than the sample.

**The agnostic form.** If no hypothesis is consistent, replace the consistency step by [Hoeffding's inequality](/hoeffding-inequality/): $\Pr[|L_S(h) - L_D(h)| > t] \le 2 e^{-2 n t^2}$. Give $h$ the budget $\delta\, 2^{-|h|}$ again. Then with probability at least $1 - \delta$, for every $h$ at once,

$$L_D(h) \le L_S(h) + \sqrt{\frac{|h| \ln 2 + \ln(2/\delta)}{2n}}.$$

Minimizing the right side over $h$ trades fit against length. This is the minimum description length rule of Shalev-Shwartz and Ben-David (Section 7.3), and a case of [structural risk minimization](/structural-risk-minimization/) where the classes are the hypotheses of each length. The rate is $1/\sqrt{n}$ instead of $1/n$, as in every agnostic bound.

### Pitfalls

- **Short in which language?** Every hypothesis is short in some language. The bound holds for a language fixed before the sample is drawn. If you choose the language after you see the data, so that your favourite hypothesis becomes short, the union bound no longer covers it.
- **The theorem is not a claim that simple rules are true.** It says that the training error of a short consistent rule is a good estimate of its true error. If no short rule fits the data, the theorem says nothing about the long rule that does. A short rule that fits poorly is still poor.
- **It is consistent with the [no free lunch theorem](/no-free-lunch-theorem-learning/).** The description language is prior knowledge. It favours some targets, and on targets that have no short description, an Occam learner fails like every other learner.
- **Number of parameters is not description length.** A model with many parameters can still have a short description, for example when the parameters are given with few bits each, or when training only reaches a small part of the parameter space. Counting parameters and calling it complexity can give the wrong answer; see [double descent](/double-descent/).
- **The sample size is an upper bound.** It comes from a union bound, so it is often loose by a large factor, as the example below shows.

## Examples

**Conjunctions with few relevant variables.** The target is a conjunction of $k$ literals over $d$ Boolean variables. Write a hypothesis as its number of literals $s$, coded by the [Elias gamma code](/elias-gamma-coding/) of $s + 1$, followed by each literal in $\lceil \log_2 (2d) \rceil$ bits. This code is prefix-free, because $s$ tells the decoder how many bits follow. The learner (Haussler's method, in Kearns and Vazirani Chapter 2) works in two steps:

1. Keep the literals that are true on every positive example. Every literal of the target is kept.
2. Each negative example must be made false by some chosen literal. Choose literals by [greedy set cover](/greedy-set-cover/): repeatedly take the kept literal that is false on the most negative examples not yet covered.

The target's $k$ literals cover all negative examples, so greedy set cover uses at most $k(\ln m + 1)$ literals, where $m$ is the number of negative examples. The hypothesis then has $O(k \log n \log d)$ bits: an Occam algorithm with $\beta$ as small as we like.

The code for this page runs the learner with $d = 12$, the target $x_0 \wedge \neg x_3 \wedge x_6 \wedge \neg x_8$ (here $k = 4$), uniform inputs, $\delta = 0.05$ and seed 1. The true error is exact, by enumeration of all $2^{12}$ inputs.

| $n$ | negatives | literals found | $\lvert h \rvert$ (bits) | Occam bound | true error |
|---|---|---|---|---|---|
| 10 | 10 | 2 | 13 | 1.2007 | 0.0625 |
| 20 | 19 | 3 | 20 | 0.8429 | 0.1563 |
| 40 | 39 | 3 | 20 | 0.4215 | 0.1563 |
| 80 | 76 | 4 | 25 | 0.2541 | 0 |
| 160 | 151 | 4 | 25 | 0.1270 | 0 |
| 320 | 297 | 4 | 25 | 0.0635 | 0 |

With 10 examples, all negative, the learner returns $x_7 \wedge \neg x_7$, which is always false; it is consistent and short, and its error is the probability $1/16$ that the target is true. From 80 examples on, the learner finds the target. The bound holds in every row, and it is loose.

**Why bits beat counting here.** The class of all conjunctions over $d$ variables has $3^d + 1$ members, so the plain finite class bound needs about $(d \ln 3 + \ln(1/\delta))/\varepsilon$ examples. For $d = 1000$ and $k = 3$, the hypothesis found above has at most $5 + 3 \cdot 11 = 38$ bits when it has 3 literals, so the Occam bound has $38 \ln 2 \approx 26.3$ in place of $1000 \ln 3 \approx 1098.6$. With $\varepsilon = 0.1$ and $\delta = 0.05$, a 38 bit hypothesis needs $n \ge 294$. For small $d$ the order is reversed: with $d = 12$, $12 \ln 3 \approx 13.2$ is less than $25 \ln 2 \approx 17.3$. The language decides which hypotheses count as simple.

**Decision trees and lists.** A decision tree with $t$ nodes over $d$ variables can be written in $O(t \log d)$ bits, so a small consistent tree generalizes with $n$ of order $t \log d / \varepsilon$. This is one justification for pruning (see [cost complexity pruning](/cost-complexity-pruning/)).

## Where it is used

- **PAC learning proofs.** To show that a class is PAC learnable in polynomial time, it suffices to give an Occam algorithm. Learners for conjunctions with few relevant variables, decision lists and small trees are analyzed this way (Kearns and Vazirani, Chapter 2).
- **Model selection.** The agnostic form is a penalty of $|h|$ bits added to the training error. [Minimum description length](/minimum-description-length/) develops this into a full theory of model choice.
- **Compression and boosting.** A learner whose output is determined by a few of its training examples is "short" in a related sense; the [boosting](/boosting/) analysis of Schapire and Freund uses this sample compression argument.
- **The philosophical rule.** William of Ockham, a fourteenth century philosopher, is credited with the rule that one should not assume more than is necessary. In learning theory only the theorem above remains: simplicity, measured in a language chosen in advance, controls how far the training error can be from the true error.

## References
