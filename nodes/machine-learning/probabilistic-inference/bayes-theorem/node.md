---
tag: ND3FAB
kind: theorem
slug: bayes-theorem
name: Bayes' theorem
aliases:
- Bayes' rule
- Bayes' law
- Bayes' formula
area: machine-learning/probabilistic-inference
level: intro
summary: "P(A|B) = P(B|A)P(A)/P(B) for events with positive probability. In odds form, the posterior odds are the likelihood ratio times the prior odds."
history:
  year: 1763
  people: [Thomas Bayes, Richard Price, Pierre-Simon Laplace]
  note: Price published the essay of Bayes in 1763, two years after the death of Bayes. Laplace stated the rule for discrete causes in 1774.
prereqs: [conditional-probability]
see_also: [bayesian-inference, marginal-likelihood, conditional-independence, monty-hall-problem, naive-bayes-classifier, bayes-optimal-classifier, maximum-likelihood-decoding, maximum-a-posteriori-estimation]
sources:
  - paper: doi:10.1098/rstl.1763.0053
    title: "Thomas Bayes, An essay towards solving a problem in the doctrine of chances, Philosophical Transactions of the Royal Society of London 53, 1763"
    locator: pp. 370 to 418 (with the introduction and appendix of Richard Price)
  - paper: doi:10.1214/ss/1177013621
    title: "Pierre-Simon Laplace, Memoir on the probability of the causes of events (1774), translated by S. M. Stigler, Statistical Science 1(3), 1986"
    locator: pp. 364 to 378 (the principle for the probability of causes given an event)
  - book: isbn:9780534243128
    title: "George Casella and Roger L. Berger, Statistical Inference, 2nd edition, Duxbury, 2002"
    locator: Section 1.3 (conditional probability, the law of total probability and Bayes' rule)
  - book: isbn:9780387310732
    title: "Christopher M. Bishop, Pattern Recognition and Machine Learning, Springer, 2006"
    locator: Section 1.2 (the sum and product rules, Bayes' theorem) and Section 1.2.3 (Bayesian probabilities)
  - paper: doi:10.1056/NEJM197811022991808
    title: "Ward Casscells, Arno Schoenberger and Thomas B. Graboys, Interpretation by physicians of clinical laboratory results, New England Journal of Medicine 299(18), 1978"
    locator: pp. 999 to 1001 (the question with prevalence 1/1000 and false positive rate 5%)
---

Bayes' theorem gives the probability of an event $A$ given an event $B$ in terms of the reverse [conditional probability](/conditional-probability/): $\Pr(A \mid B) = \Pr(B \mid A)\Pr(A)/\Pr(B)$. It turns a model of how the evidence $B$ comes from a cause $A$ into a probability of the cause given the evidence. Every step of [Bayesian inference](/bayesian-inference/) is one use of it, with a prior in place of $\Pr(A)$ and the [marginal likelihood](/marginal-likelihood/) in place of $\Pr(B)$. This page states and proves the theorem and its odds form; the update of a whole distribution over parameters is on the Bayesian inference page.

## Statement

Let $(\Omega, \mathcal{F}, \Pr)$ be a [probability space](/probability-space/) and let $A, B \in \mathcal{F}$. Write $\bar A = \Omega \setminus A$.

**(1) Two events.** If $\Pr(A) > 0$ and $\Pr(B) > 0$, then

$$
\Pr(A \mid B) = \frac{\Pr(B \mid A)\,\Pr(A)}{\Pr(B)}.
$$

**(2) Partition form.** Let $A_1, A_2, \ldots$ be a finite or countable partition of $\Omega$ into events with $\Pr(A_i) > 0$, and let $\Pr(B) > 0$. Then for each $j$,

$$
\Pr(A_j \mid B) = \frac{\Pr(B \mid A_j)\,\Pr(A_j)}{\sum_i \Pr(B \mid A_i)\,\Pr(A_i)}.
$$

**(3) Odds form.** If $0 < \Pr(A) < 1$, $\Pr(B \mid A) > 0$ and $\Pr(B \mid \bar A) > 0$, then

$$
\underbrace{\frac{\Pr(A \mid B)}{\Pr(\bar A \mid B)}}_{\text{posterior odds}} = \underbrace{\frac{\Pr(B \mid A)}{\Pr(B \mid \bar A)}}_{\text{likelihood ratio}} \cdot \underbrace{\frac{\Pr(A)}{\Pr(\bar A)}}_{\text{prior odds}}.
$$

Taking logarithms, the posterior log odds are the prior log odds plus the log likelihood ratio.

**(4) Densities.** Let random variables $X$ and $Y$ have a joint density $p(x, y)$ with marginal densities $p(x)$ and $p(y)$, and define $p(y \mid x) = p(x, y)/p(x)$ where $p(x) > 0$ and $p(x \mid y) = p(x, y)/p(y)$ where $p(y) > 0$. Then at each $(x, y)$ with $p(x) > 0$ and $p(y) > 0$,

$$
p(x \mid y) = \frac{p(y \mid x)\,p(x)}{p(y)}, \qquad p(y) = \int_{\{x' :\, p(x') > 0\}} p(y \mid x')\,p(x')\,dx' \quad \text{for almost every } y.
$$

## In plain words

You know how often a cause happens, and you know how often each cause produces some evidence. You then see the evidence. The theorem tells you how likely each cause is now. You weigh each cause by how common it was before, times how well it explains the evidence, and then you rescale the weights so that they add up to one. In the odds form you keep the weights as a ratio, so the rescaling step goes away: the new ratio is the old ratio times the ratio of how well the two causes explain what you saw.

## Proof

*(1)* By the definition of conditional probability, $\Pr(A \cap B) = \Pr(A \mid B)\Pr(B)$ because $\Pr(B) > 0$, and $\Pr(A \cap B) = \Pr(B \mid A)\Pr(A)$ because $\Pr(A) > 0$. So $\Pr(A \mid B)\Pr(B) = \Pr(B \mid A)\Pr(A)$. Divide by $\Pr(B) > 0$.

*(2)* The sets $B \cap A_i$ are pairwise disjoint and their union is $B$. Countable additivity gives $\Pr(B) = \sum_i \Pr(B \cap A_i) = \sum_i \Pr(B \mid A_i)\Pr(A_i)$, which is the law of total probability. Put this into (1) with $A = A_j$.

*(3)* From $\Pr(B \mid A) > 0$ and $\Pr(A) > 0$ we get $\Pr(B) \ge \Pr(A \cap B) > 0$. Apply (1) to $A$ and to $\bar A$; both have positive probability. The two results have the same denominator $\Pr(B)$. The second one, $\Pr(\bar A \mid B) = \Pr(B \mid \bar A)\Pr(\bar A)/\Pr(B)$, is positive, so we can divide the first by it, and $\Pr(B)$ cancels.

*(4)* At a point with $p(x) > 0$ and $p(y) > 0$, both definitions give $p(x, y) = p(x \mid y)p(y) = p(y \mid x)p(x)$; divide by $p(y)$. For the denominator, $p(y) = \int p(x', y)\,dx'$. Let $Z = \{x' : p(x') = 0\}$. Then $\int_Z \int p(x', y)\,dy\,dx' = \int_Z p(x')\,dx' = 0$, so by Tonelli's theorem $\int_Z p(x', y)\,dx' = 0$ for almost every $y$. Off $Z$, $p(x', y) = p(y \mid x')p(x')$. $\blacksquare$

## Consequences

**The base rate.** A disease has prevalence $\Pr(D) = 1/1000$. A test finds every case, $\Pr(+ \mid D) = 1$, and gives a false positive with probability $\Pr(+ \mid \bar D) = 5/100$. Casscells, Schoenberger and Graboys (1978) asked physicians and students for $\Pr(D \mid +)$, and the most common answer was 95%. The partition form gives

$$
\Pr(D \mid +) = \frac{1 \cdot \frac{1}{1000}}{1 \cdot \frac{1}{1000} + \frac{5}{100} \cdot \frac{999}{1000}} = \frac{20}{1019} \approx 0.0196.
$$

In odds form: the prior odds are $1 : 999$, the likelihood ratio is $1/(5/100) = 20$, and the posterior odds are $20 : 999$, so the probability is $20/1019$ again. The test multiplies the odds by 20, but the prior odds are so small that a positive person is still very likely healthy. To give $\Pr(+ \mid \bar D) = 5/100$ as the error of the conclusion is the *base rate fallacy*. With the same test and a prevalence of $1/10$, the answer is $20/29 \approx 0.69$; with prevalence $1/1000$ and a sensitivity of $99/100$, it is $11/566 \approx 0.0194$.

| quantity | prevalence 1/1000 | prevalence 1/10 |
|---|---|---|
| prior odds | 1 : 999 | 1 : 9 |
| likelihood ratio of one positive | 20 | 20 |
| posterior odds | 20 : 999 | 20 : 9 |
| $\Pr(D \mid +)$ | 20/1019 | 20/29 |

**Several pieces of evidence.** If two tests are [conditionally independent](/conditional-independence/) given the disease status, the likelihood ratio of two positive results is the product $20 \cdot 20 = 400$. The posterior odds become $400 : 999$ and $\Pr(D \mid +, +) = 400/1399 \approx 0.286$. The same number comes from updating twice, with the first posterior as the second prior. Without conditional independence the product rule for likelihood ratios is false; this is the assumption of the [naive Bayes classifier](/naive-bayes-classifier/).

**Where it is used.** The theorem is the base of [Bayesian inference](/bayesian-inference/), of the [Bayes optimal classifier](/bayes-optimal-classifier/) (predict the class with the largest $\Pr(c \mid x)$), of [MAP estimation](/maximum-a-posteriori-estimation/) and of [maximum likelihood decoding](/maximum-likelihood-decoding/), which equals MAP decoding when all codewords are equally likely. The [Monty Hall problem](/monty-hall-problem/) is a standard exercise. In a [graphical model](/graphical-model/), the denominator $\Pr(B)$ is a sum over all hidden variables, and computing it is the hard part of [marginal inference](/marginal-inference/).

## Tightness

- **The condition $\Pr(B) > 0$ cannot be dropped.** $\Pr(A \mid B)$ is not defined for a null event. For densities, the value of $p(x \mid y)$ at one point $y$ depends on which version of the density is chosen, and two limits that both shrink to the same null event can give different conditional distributions (the Borel-Kolmogorov paradox). The density form holds for almost every $y$, not at every $y$.
- **The prior cannot be dropped.** The table above has the same likelihood ratio in both columns and posteriors of $20/1019$ and $20/29$. No statement about $\Pr(A \mid B)$ follows from $\Pr(B \mid A)$ alone, and confusing the two is the prosecutor's fallacy.
- **The odds form needs $\Pr(B \mid \bar A) > 0$.** If evidence is impossible under $\bar A$, the posterior odds are infinite and $\Pr(A \mid B) = 1$, which the probability form still gives.

## History

Thomas Bayes died in 1761. Richard Price found his essay and had it read to the Royal Society, which published it in 1763. Bayes found the posterior distribution of the success probability of a binomial experiment under a uniform prior. Laplace, who did not know of the essay, stated the rule for a finite set of equally likely causes in a memoir of 1774.

## References
