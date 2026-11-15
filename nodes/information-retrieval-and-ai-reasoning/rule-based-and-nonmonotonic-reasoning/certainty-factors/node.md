---
tag: 90V7YH
kind: model
slug: certainty-factors
name: Certainty factors
aliases:
- MYCIN certainty factors
area: information-retrieval-and-ai-reasoning/rule-based-and-nonmonotonic-reasoning
level: advanced
summary: Attaches a number in [-1, 1] to each rule and fact and combines them by fixed formulas, an early non-probabilistic model of uncertainty.
history:
  year: 1975
  people: [Edward H. Shortliffe, Bruce G. Buchanan]
  note: "Shortliffe and Buchanan defined measures of belief and disbelief for the MYCIN system for infectious diseases, because physicians could not give the probabilities that a Bayesian model needed."
prereqs: [bayes-theorem, backward-chaining]
see_also: [bayesian-network, naive-bayes-classifier, production-system, forward-chaining, conflict-resolution-strategy]
sources:
  - paper: doi:10.1016/0025-5564(75)90047-4
    title: "Edward H. Shortliffe and Bruce G. Buchanan, A model of inexact reasoning in medicine, Mathematical Biosciences 23(3-4) (1975)"
    locator: "the definitions of MB, MD and CF in terms of probabilities and the functions for combining them"
  - book: isbn:9780201101720
    title: "Bruce G. Buchanan and Edward H. Shortliffe (eds.), Rule-Based Expert Systems: The MYCIN Experiments of the Stanford Heuristic Programming Project, Addison-Wesley (1984)"
    locator: "the part on reasoning under uncertainty, with the revised combining function and the use of certainty factors in MYCIN and EMYCIN"
  - paper: "David Heckerman, Probabilistic interpretations for MYCIN's certainty factors, in L. N. Kanal and J. F. Lemmer (eds.), Uncertainty in Artificial Intelligence, North-Holland, 167 to 196 (1986)"
    locator: "the inconsistency of the original definitions with the combining functions, the reading of CFs as monotone functions of the likelihood ratio, and the independence conditions"
---

The certainty factor (CF) model is the calculus of uncertainty of the MYCIN expert system. Each rule "if $e$ then $h$" carries a number in $[-1, 1]$ that says how much the evidence $e$ changes the belief in the hypothesis $h$: $1$ means that $e$ makes $h$ certain, $-1$ that it rules $h$ out, and $0$ that it does not change it. A [backward chaining](/backward-chaining/) engine computes a CF for each fact by fixed formulas: the minimum for "and", the product for a rule, and a combining function when several rules conclude the same fact. The formulas are local and cheap, and they do not need prior probabilities. CFs are not probabilities in general. Heckerman (1986) showed that the combining function is exact for one reading of CFs, as a monotone function of a likelihood ratio, and only when the pieces of evidence are conditionally independent given the hypothesis and given its negation.

## The machine

**Definitions of 1975.** Shortliffe and Buchanan defined, for a hypothesis $h$ and evidence $e$, a *measure of belief* and a *measure of disbelief*:

$$\mathrm{MB}(h, e) = \frac{\max(p(h \mid e), p(h)) - p(h)}{1 - p(h)}, \qquad \mathrm{MD}(h, e) = \frac{p(h) - \min(p(h \mid e), p(h))}{p(h)},$$

with $\mathrm{MB} = 1$ when $p(h) = 1$ and $\mathrm{MD} = 1$ when $p(h) = 0$. At most one of the two is positive. The certainty factor is $\mathrm{CF}(h, e) = \mathrm{MB}(h, e) - \mathrm{MD}(h, e)$. So a CF measures a *change* of belief, relative to the room left for the change, and not a degree of belief. In the 1975 model the MB and MD of a hypothesis were combined separately over the pieces of evidence, for example $\mathrm{MB}(h, e_1 \wedge e_2) = \mathrm{MB}(h, e_1) + \mathrm{MB}(h, e_2)(1 - \mathrm{MB}(h, e_1))$, and the CF was formed at the end.

**The rules of the calculus.** In use, nobody computed the probabilities: experts gave a CF for each rule, and the system gave CFs to the facts. The later form, used in EMYCIN and described by Buchanan and Shortliffe (1984), works on one CF per fact:

- **Premises.** $\mathrm{CF}(e_1 \wedge e_2) = \min(\mathrm{CF}(e_1), \mathrm{CF}(e_2))$ and $\mathrm{CF}(e_1 \vee e_2) = \max(\mathrm{CF}(e_1), \mathrm{CF}(e_2))$. A premise counts as true only when its CF is above $0.2$; else the rule does not fire.
- **Sequential combination.** A rule "if $e$ then $h$" with strength $c$ gives $h$ the CF $c \cdot \max(0, \mathrm{CF}(e))$.
- **Parallel combination.** Two rules that give $h$ the CFs $x$ and $y$ combine to

$$x \oplus y = \begin{cases} x + y - x y & \text{if } x, y \ge 0, \\ x + y + x y & \text{if } x, y < 0, \\ \dfrac{x + y}{1 - \min(|x|, |y|)} & \text{otherwise.} \end{cases}$$

The combining function is commutative and associative, $0$ is its identity, and $1 \oplus y = 1$ for $y > -1$. The value of $1 \oplus (-1)$ is not defined, and a system must treat it as a special case.

**Example.** Rule $R_1$, "if $e_1$ and $e_2$ then $h$", has strength $0.8$; rule $R_2$, "if $e_3$ then $h$", has $0.5$; rule $R_3$, "if $e_4$ then $h$", has $-0.4$; rule $R_4$, "if $e_5$ then $h$", has $-0.6$. The facts have $\mathrm{CF}(e_1) = 0.6$, $\mathrm{CF}(e_2) = 0.9$, $\mathrm{CF}(e_3) = 1$, $\mathrm{CF}(e_4) = 0.15$ and $\mathrm{CF}(e_5) = 0.5$.

| step | computation | CF |
|---|---|---|
| $R_1$ | $0.8 \cdot \min(0.6, 0.9)$ | $0.48$ |
| $R_2$ | $0.5 \cdot 1$ | $0.5$ |
| $R_3$ | $0.15$ is not above $0.2$, so $R_3$ does not fire | |
| $R_4$ | $-0.6 \cdot 0.5$ | $-0.3$ |
| $R_1 \oplus R_2$ | $0.48 + 0.5 - 0.48 \cdot 0.5$ | $0.74$ |
| then $\oplus R_4$ | $(0.74 - 0.3) / (1 - 0.3)$ | $0.629$ |

Combining $R_2$ and $R_4$ first gives $0.2 / 0.7 = 0.286$, and then $0.286 \oplus 0.48 = 0.629$ again.

## What it counts

A CF counts the change of belief in a hypothesis caused by the evidence, on a scale from $-1$ to $1$. It does not count how probable the hypothesis is. Under the 1975 definitions, $\mathrm{CF}(\neg h, e) = -\mathrm{CF}(h, e)$, so the CFs of a hypothesis and its negation add up to $0$, while their probabilities add up to $1$. For example, with $p(h) = 0.3$ and $p(h \mid e) = 0.6$, $\mathrm{CF}(h, e) = 0.43$ and $\mathrm{CF}(\neg h, e) = -0.43$.

The cost of inference is small. Each rule application and each combination is a constant number of arithmetic operations, so a backward chaining run that computes each fact once, with [memoization](/memoization/), takes time linear in the size of the ground rules that it uses. Exact probabilistic inference in a general [Bayesian network](/bayesian-network/), by contrast, is [NP-hard](/np-hard/).

## Relation to other models

- **[Bayes' theorem](/bayes-theorem/) in odds form.** With the likelihood ratio $\lambda = p(e \mid h) / p(e \mid \neg h)$, the posterior odds are $\lambda$ times the prior odds. Heckerman's reading of CFs is a function of $\lambda$ (see below).
- **[Naive Bayes](/naive-bayes-classifier/).** Under that reading, the parallel combination multiplies likelihood ratios, which is the naive Bayes update for one hypothesis and conditionally independent evidence.
- **[Bayesian networks](/bayesian-network/).** A network represents the dependencies between pieces of evidence explicitly. The CF model assumes them away, so it is exact only on networks where each piece of evidence bears on the hypothesis independently.
- **[Production systems](/production-system/).** MYCIN and EMYCIN attached CFs to the rules of a goal-directed production system, and the CF calculus runs alongside the chaining.

## Known results in the model

**The original definitions do not fit the combining function.** Read a CF, as in the 1975 definitions, as the relative change of the current probability of $h$. Take $p(h) = 0.4$, evidence $e^+$ with CF $0.7$ and evidence $e^-$ with CF $-0.5$. Applying $e^+$ first gives $0.4 + 0.7 \cdot 0.6 = 0.82$, and then $0.82 \cdot 0.5 = 0.41$. Applying $e^-$ first gives $0.2$, and then $0.2 + 0.7 \cdot 0.8 = 0.76$. The result depends on the order, while $0.7 \oplus (-0.5) = 0.4$ does not. Heckerman (1986) used this kind of example to show that the original definitions are not consistent with the combining function.

**A probabilistic reading.** Heckerman (1986) proposed to define the CF of a rule as a monotone function of its likelihood ratio $\lambda$:

$$\mathrm{CF} = \begin{cases} 1 - 1/\lambda & \text{if } \lambda \ge 1, \\ \lambda - 1 & \text{if } \lambda < 1. \end{cases}$$

Then $x \oplus y$ is exactly the CF of the product of the two likelihood ratios, in all three cases of the combining function. For example, for $x, y \ge 0$ the ratios are $1/(1 - x)$ and $1/(1 - y)$, and $1 - (1 - x)(1 - y) = x + y - x y$. The product of likelihood ratios is the correct update when $e_1$ and $e_2$ are conditionally independent given $h$ and given $\neg h$. So, under these conditions, the parallel combination is a correct probabilistic rule, and the CF of a rule does not depend on the prior of $h$.

**What has no probabilistic reading.** The sequential rule $c \cdot \max(0, \mathrm{CF}(e))$, the minimum and maximum for "and" and "or", and the threshold of $0.2$ do not follow from any reading of this kind in general. When the evidence is not conditionally independent, for example when two rules rest on the same finding, the combining function counts the same evidence twice. So the CFs that a system computes are not probabilities in general, and Heckerman gives the conditions under which the parallel combination has a probabilistic meaning.

## References
