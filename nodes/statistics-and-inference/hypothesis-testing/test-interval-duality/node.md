---
tag: F421N6
kind: theorem
slug: test-interval-duality
name: Duality of tests and confidence sets
aliases:
- test inversion
- inverting a test
area: statistics-and-inference/hypothesis-testing
level: core
summary: The parameter values that a level-alpha test does not reject form a confidence set of level 1 - alpha, and every confidence set defines a test this way.
prereqs: [statistical-hypothesis-test, confidence-interval, p-value]
see_also: [pivotal-quantity, clopper-pearson-interval, wilson-score-interval, fieller-theorem, binomial-test, t-confidence-interval, uniformly-most-powerful-test, karlin-rubin-theorem]
sources:
  - book: isbn:9780387988641
    title: E. L. Lehmann and Joseph P. Romano, Testing Statistical Hypotheses, third edition, Springer, 2005
    locator: Section 3.5 (confidence bounds, with uniformly most accurate bounds) and Chapter 5 (confidence intervals and families of tests)
  - book: isbn:9780534243128
    title: George Casella and Roger L. Berger, Statistical Inference, second edition, Duxbury, 2002
    locator: Section 9.2.1 (inverting a test statistic) and Section 9.3 (methods of evaluating interval estimators)
  - paper: doi:10.1098/rsta.1937.0005
    title: Jerzy Neyman, Outline of a theory of statistical estimation based on the classical theory of probability, Philosophical Transactions of the Royal Society A 236, 1937
    locator: pp. 333 to 380 (confidence intervals from regions of acceptance)
---

A [confidence set](/confidence-interval/) and a family of [hypothesis tests](/statistical-hypothesis-test/) are the same object seen in two directions. If for every candidate value $\psi_0$ of a parameter there is a test of $H_0: \psi = \psi_0$ at level $\alpha$, then the set of values that the tests do not reject, after the data are seen, covers the true value with probability at least $1 - \alpha$. Conversely, a confidence set of level $1 - \alpha$ gives, for every $\psi_0$, a level-$\alpha$ test: reject when $\psi_0$ is not in the set. Most intervals in this area are built this way, and the shape of the set, its coverage and its optimality are inherited from the tests.

## Statement

Let $X$ take values in a sample space $\mathcal X$ with law $P_\theta$, $\theta \in \Theta$, and let $\psi = g(\theta)$ be the parameter of interest, with values in a set $\Psi$. The rest of $\theta$ is a nuisance parameter. For $\psi_0 \in \Psi$ write $\Theta_{\psi_0} = \{\theta : g(\theta) = \psi_0\}$ for the null set of $H_0: \psi = \psi_0$.

A *level-$\alpha$ acceptance region* for $\psi_0$ is a measurable set $A(\psi_0) \subseteq \mathcal X$ with

$$P_\theta(X \in A(\psi_0)) \ge 1 - \alpha \quad \text{for every } \theta \in \Theta_{\psi_0},$$

so that the test "reject $H_0$ when $X \notin A(\psi_0)$" has size at most $\alpha$. A *confidence set of level $1 - \alpha$* is a map $x \mapsto C(x) \subseteq \Psi$, with $\{x : \psi_0 \in C(x)\}$ measurable for each $\psi_0$, such that

$$P_\theta(g(\theta) \in C(X)) \ge 1 - \alpha \quad \text{for every } \theta \in \Theta.$$

**Theorem.**

1. **Tests to sets.** If $A(\psi_0)$ is a level-$\alpha$ acceptance region for each $\psi_0 \in \Psi$, then $C(x) = \{\psi_0 \in \Psi : x \in A(\psi_0)\}$ is a confidence set of level $1 - \alpha$.
2. **Sets to tests.** If $C$ is a confidence set of level $1 - \alpha$, then $A(\psi_0) = \{x : \psi_0 \in C(x)\}$ is a level-$\alpha$ acceptance region for each $\psi_0$.
3. **Exact correspondence.** The two maps are inverse to each other, and under them
$$\inf_{\theta \in \Theta_{\psi_0}} P_\theta(X \in A(\psi_0)) = \inf_{\theta \in \Theta_{\psi_0}} P_\theta(\psi_0 \in C(X)).$$
So the confidence coefficient $\inf_\theta P_\theta(g(\theta) \in C(X))$ equals $1 - \sup_{\psi_0} \text{size}(\psi_0)$. In particular, if every test has size exactly $\alpha$, the coverage is exactly $1 - \alpha$ at its worst $\theta$, and the converse holds.
4. **Optimality carries over.** Let $A^*(\psi)$ be a level-$\alpha$ acceptance region for every $\psi \in \Psi$, with dual set $C^*$. Let $\psi' \neq \psi_0$, and fix $\theta$ with $g(\theta) = \psi_0$. Suppose the region $A^*(\psi')$ maximizes $P_\theta(X \notin A(\psi'))$ among all level-$\alpha$ acceptance regions $A(\psi')$ for $\psi'$. Then $C^*$ has level $1 - \alpha$ and minimizes $P_\theta(\psi' \in C(X))$, the probability of covering the false value $\psi'$, among all confidence sets of level $1 - \alpha$.
5. **p-values.** If $p(x; \psi_0)$ is a valid [p-value](/p-value/) for each $\psi_0$, that is $P_\theta(p(X; \psi_0) \le u) \le u$ for $u \in [0, 1]$ and $\theta \in \Theta_{\psi_0}$, then $C(x) = \{\psi_0 : p(x; \psi_0) > \alpha\}$ is a confidence set of level $1 - \alpha$ for every $\alpha$ at once.

## In plain words

Fix the data. Go through every value the parameter could have and ask the test "would you reject this value?". Keep the values that survive. Before the data are seen, the true value survives with probability at least $1 - \alpha$, because surviving is exactly the event that the test for the true value accepts. So the coverage of the set is the acceptance probability of one test, the one at the truth, and nothing else is needed. Read the other way, a confidence set is a test for every value at once: a value outside the set is rejected.

## Proof

**Part 1.** Fix $\theta \in \Theta$ and put $\psi_0 = g(\theta)$, so $\theta \in \Theta_{\psi_0}$. By the definition of $C$, for every $x$,

$$g(\theta) \in C(x) \iff \psi_0 \in C(x) \iff x \in A(\psi_0).$$

So the events $\{g(\theta) \in C(X)\}$ and $\{X \in A(\psi_0)\}$ are the same event, and

$$P_\theta(g(\theta) \in C(X)) = P_\theta(X \in A(\psi_0)) \ge 1 - \alpha,$$

where the inequality is the level of the test for $\psi_0$, used at a $\theta$ in its null set. Measurability of $\{x : \psi_0 \in C(x)\} = A(\psi_0)$ holds by assumption. Since $\theta$ was arbitrary, $C$ has level $1 - \alpha$. $\square$

**Part 2.** Fix $\psi_0$ and $\theta \in \Theta_{\psi_0}$. Then $g(\theta) = \psi_0$, and $X \in A(\psi_0)$ if and only if $\psi_0 \in C(X)$, that is, if and only if $g(\theta) \in C(X)$. So

$$P_\theta(X \in A(\psi_0)) = P_\theta(g(\theta) \in C(X)) \ge 1 - \alpha,$$

by the level of $C$ at this $\theta$. The set $A(\psi_0)$ is measurable by the assumption on $C$. $\square$

**Part 3.** Starting from a family $A$, forming $C$ and then forming the regions of $C$ gives $\{x : \psi_0 \in C(x)\} = \{x : x \in A(\psi_0)\} = A(\psi_0)$. Starting from $C$ gives $\{\psi_0 : x \in A(\psi_0)\} = \{\psi_0 : \psi_0 \in C(x)\} = C(x)$. So the maps are inverse to each other. The proof of Part 1 showed that $P_\theta(X \in A(\psi_0)) = P_\theta(\psi_0 \in C(X))$ for every $\theta \in \Theta_{\psi_0}$, as an equality of probabilities of one event. Taking the infimum over $\theta \in \Theta_{\psi_0}$ gives the displayed equality. Because the sets $\Theta_{\psi_0}$, $\psi_0 \in \Psi$, partition $\Theta$,

$$\inf_{\theta \in \Theta} P_\theta(g(\theta) \in C(X)) = \inf_{\psi_0} \inf_{\theta \in \Theta_{\psi_0}} P_\theta(X \in A(\psi_0)) = 1 - \sup_{\psi_0} \sup_{\theta \in \Theta_{\psi_0}} P_\theta(X \notin A(\psi_0)),$$

and the inner supremum is the size of the test for $\psi_0$. $\square$

**Part 4.** Let $C$ be any confidence set of level $1 - \alpha$, and let $A(\psi') = \{x : \psi' \in C(x)\}$. By Part 2 this is a level-$\alpha$ acceptance region for $\psi'$. By the optimality of $A^*(\psi')$ at $\theta$,

$$P_\theta(X \notin A^*(\psi')) \ge P_\theta(X \notin A(\psi')), \quad\text{so}\quad P_\theta(X \in A^*(\psi')) \le P_\theta(X \in A(\psi')).$$

By the definitions of the dual sets, the left side is $P_\theta(\psi' \in C^*(X))$ and the right side is $P_\theta(\psi' \in C(X))$. $C^*$ itself has level $1 - \alpha$ by Part 1, because every $A^*(\psi)$ has level $\alpha$. $\square$

**Part 5.** Put $A(\psi_0) = \{x : p(x; \psi_0) > \alpha\}$. For $\theta \in \Theta_{\psi_0}$, $P_\theta(X \notin A(\psi_0)) = P_\theta(p(X; \psi_0) \le \alpha) \le \alpha$, so $A(\psi_0)$ is a level-$\alpha$ acceptance region, and Part 1 applies for each $\alpha$. $\square$

The proof uses no property of $\Psi$ and no continuity. In particular it holds for discrete data, vector parameters and nuisance parameters, and it says nothing about the shape of $C(x)$.

## Consequences

- **Named intervals are inverted tests.** The [t interval](/t-confidence-interval/) is the set of $\mu_0$ that the two-sided [t-test](/student-t-test/) accepts. The [Clopper-Pearson interval](/clopper-pearson-interval/) is the set of $p_0$ for which both one-sided exact [binomial tests](/binomial-test/) have p-value above $\alpha/2$; for $x = 3$, $n = 10$ and $\alpha = 0.05$ it is $(0.06674, 0.65245)$. The [Wilson interval](/wilson-score-interval/) inverts the [score test](/score-test/) and gives $(0.10779, 0.60322)$ for the same data. [Fieller's theorem](/fieller-theorem/) inverts a t-test for a ratio. Every [pivotal quantity](/pivotal-quantity/) gives a family of tests and so fits the same scheme.
- **Coverage is inherited from size.** By Part 3, a conservative test gives a conservative set and an exact test an exact one. The Clopper-Pearson interval has coverage strictly above $1 - \alpha$ at every $p$, because the binomial tail tests it inverts are not randomized and accept the true $p$ with probability above $1 - \alpha$. A test that only holds its level asymptotically, such as the [Wald test](/wald-test/) or the score test, gives a set whose coverage is only asymptotic.
- **Uniformly most accurate bounds.** By Part 4, inverting the [uniformly most powerful](/uniformly-most-powerful-test/) one-sided tests of a monotone likelihood ratio family (from the [Karlin-Rubin theorem](/karlin-rubin-theorem/)) gives a lower confidence bound that is least likely, among all lower bounds of the same level, to lie below any given false value. Unbiased tests give unbiased confidence sets in the same way: if every test rejects each alternative with probability at least $\alpha$, then every false value is covered with probability at most $1 - \alpha$.
- **Reporting.** Since $C(x)$ holds every value that the tests accept, a confidence set reports the result of a test for every null value at once. A test of $\psi_0$ rejects at level $\alpha$ exactly when $\psi_0 \notin C(x)$, which is the reading used in the [z-test](/z-test/) and t-test pages.

## Tightness

- **The set need not be an interval.** The theorem gives a set, not an interval. Inverting the two-sided binomial test with the "minimum likelihood" p-value (the default of the binomial test page) for $x = 1$, $n = 30$ and $\alpha = 0.05$ gives, on a grid of step $5 \times 10^{-6}$, the acceptance set
$$(0.00171, 0.16323) \cup (0.17506, 0.17723),$$
with p-values $0.0491$ at $p_0 = 0.17$ and $0.0503$ at $p_0 = 0.176$. The cause is that this p-value is not monotone in $p_0$ above $x/n$. The doubled-tail test gives the interval $(0.00084, 0.17217)$ instead. Fieller's set can be two rays or the whole line. An interval is guaranteed when, for each $x$, the acceptance set in $\psi_0$ is convex, for example when the p-value is unimodal in $\psi_0$.
- **One test is not enough.** The set needs a level-$\alpha$ test for every $\psi_0$. A test of a single null value says nothing about the other values.
- **Coverage is marginal.** The probability $1 - \alpha$ is over repeated samples at a fixed $\theta$. After the data are seen, $\psi \in C(x)$ is true or false, and the theorem gives no probability for it. With nuisance parameters, the guarantee is the infimum over the null set, so the coverage can be well above $1 - \alpha$ at most $\theta$.
- **The inequality in Part 1 can be strict everywhere.** For a discrete $X$ without randomization the tests cannot have size exactly $\alpha$, and the coverage then exceeds $1 - \alpha$ for every $\theta$. Randomized tests $\phi(x, \psi_0) \in [0, 1]$ correspond in the same way to randomized sets, with $P(\psi_0 \in C(x)) = 1 - \phi(x, \psi_0)$, and can make both exact; the proof is the same with probabilities of events replaced by expectations of $1 - \phi$.
- **The family must be fixed before the data.** If the test for each $\psi_0$ is chosen after looking at $x$, the events in Part 1 are no longer the acceptance events of fixed tests, and the bound fails.

## History

Clopper and Pearson (1934) built their binomial interval from the two tails of the test, and Neyman (1937) gave the general construction of confidence intervals from regions of acceptance, one region for each parameter value, in the paper that set out the theory of confidence intervals. The statement as a correspondence between families of tests and confidence sets, with the transfer of optimality, is the form given in Lehmann's book on testing (first edition 1959); the third edition with Romano has it in Section 3.5 and Chapter 5. Sterne (1954) proposed the minimum-likelihood binomial test, whose inversion gives the non-interval sets shown above.

## References
