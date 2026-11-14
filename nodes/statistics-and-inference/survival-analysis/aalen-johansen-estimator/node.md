---
tag: ZVA82Z
kind: algorithm
slug: aalen-johansen-estimator
name: Aalen-Johansen estimator
aliases:
- cumulative incidence function estimator
area: statistics-and-inference/survival-analysis
level: advanced
summary: Estimates the transition probabilities of a finite-state Markov process under censoring, and so the cumulative incidence of each cause with competing risks.
model: real-ram
complexity:
  vars: {n: the number of subjects, m: the number of distinct event times, K: the number of causes}
  time: {worst: Θ(n log n + m K)}
  space: {extra: Θ(n + m K)}
properties: {deterministic: true, exact: true, online: false, recursive: false}
history:
  year: 1978
  people: [Odd O. Aalen, Søren Johansen]
  note: Aalen and Johansen defined the empirical transition matrix of a Markov process with censored data as a product integral of Nelson-Aalen increments in 1978. For competing risks it gives the cumulative incidence estimate that actuaries and Kalbfleisch and Prentice had used.
prereqs: [competing-risks, kaplan-meier-estimator, nelson-aalen-estimator, markov-chain]
see_also: [fine-gray-model, censoring, survival-function, greenwood-formula, matrix-exponential, markov-property, log-rank-test, inverse-probability-weighting]
sources:
  - paper: "Odd O. Aalen and Søren Johansen, An empirical transition matrix for non-homogeneous Markov chains based on censored observations, Scandinavian Journal of Statistics 5(3), 1978"
    locator: pp. 141 to 150 (the product-integral estimator of the transition matrix, its martingale representation and its large-sample behavior)
  - book: isbn:9780387945194
    title: Per Kragh Andersen, Ørnulf Borgan, Richard D. Gill and Niels Keiding, Statistical Models Based on Counting Processes, Springer, 1993
    locator: Chapter IV (nonparametric estimation, including the product-limit estimator of a transition matrix and its weak convergence)
  - paper: doi:10.1002/sim.2712
    title: H. Putter, M. Fiocco and R. B. Geskus, Tutorial in biostatistics, competing risks and multi-state models, Statistics in Medicine 26(11), 2007
    locator: pp. 2389 to 2430 (the cumulative incidence estimate, the bias of one minus Kaplan-Meier, and the Aalen-Johansen estimate in multi-state models)
  - book: isbn:9780471363576
    title: John D. Kalbfleisch and Ross L. Prentice, The Statistical Analysis of Failure Time Data, 2nd edition, Wiley, 2002
    locator: Chapter 8 (competing risks, the estimate of the cumulative incidence functions and multistate models)
---

The Aalen-Johansen estimator estimates the probabilities of a process that moves between a finite set of states, from data in which subjects are censored. Its most common use is [competing risks](/competing-risks/): from the time to the first event and its cause, it estimates the cumulative incidence $F_k(t) = P(T \le t, \text{cause} = k)$ of each cause $k$ as

$$\hat F_k(t) = \sum_{j:\, t_j \le t} \hat S(t_{j-1})\,\frac{d_{kj}}{n_j},$$

where $t_j$ are the distinct event times, $n_j$ the number at risk at $t_j$, $d_{kj}$ the number of events of cause $k$ at $t_j$ and $\hat S$ the all-cause [Kaplan-Meier](/kaplan-meier-estimator/) estimate. With one cause it is one minus Kaplan-Meier. The estimates of the $K$ causes and $\hat S$ add up to $1$ exactly. In general, it is the product over event times of $I + d\hat A$, where $d\hat A$ is the matrix of [Nelson-Aalen](/nelson-aalen-estimator/) increments of the transitions.

## In plain words

Follow a group of patients in time. At each time when someone has an event, look at the patients still free of any event. A fraction of them has an event of cause 1, a fraction has cause 2, and so on. The chance of having a cause 1 event at that moment, for a patient at the start, is the chance of still being event-free just before, times the fraction with cause 1. Add these chances over time to get the cumulative incidence of cause 1. A patient who had an event of cause 2 does not stay in the pool, so it cannot later count as a cause 1 event. This is the difference from one minus Kaplan-Meier with cause 2 treated as censored, which pretends that such a patient could still have cause 1.

## The problem

**Input.** Observations $(y_i, c_i)$ for $i = 1, \ldots, n$, where $y_i$ is the observed time and $c_i = k \in \{1, \ldots, K\}$ if subject $i$ had an event of cause $k$ at $y_i$, or $c_i = 0$ if it was censored at $y_i$.

**Model.** The pairs (time to the first event, cause) are independent across subjects, and censoring is independent: among the subjects still at risk at $t$, the cause-specific hazards are those of the whole population. No form is assumed for the hazards.

**Output.** For each distinct event time $t_j$ (of any cause), the number at risk $n_j = \#\{i : y_i \ge t_j\}$, the counts $d_{1j}, \ldots, d_{Kj}$, the all-cause survival $\hat S(t_j)$ and the cumulative incidences $\hat F_1(t_j), \ldots, \hat F_K(t_j)$. The estimates are right-continuous step functions, $\hat S = 1$ and $\hat F_k = 0$ before $t_1$.

**Ties.** A censored time equal to an event time counts as at risk at that time, as for Kaplan-Meier. Events of different causes at the same time all use $\hat S(t_{j-1})$, the survival just before $t_j$.

## The algorithm

```pseudo id=main
AALEN-JOHANSEN(y[1..n], c[1..n], K)
L1  sort the indices 1..n by increasing y
L2  S ← 1;  F[1..K] ← 0;  r ← n;  out ← empty list
L3  for each distinct time t in that order
L4      count d[k] ← #{i : y_i = t, c_i = k} for each k, and leave ← #{i : y_i = t}
L5      if d[1] + ... + d[K] > 0
L6          F[k] ← F[k] + S · d[k] / r  for each k        ▷ uses S before the update
L7          S ← S · (1 - (d[1] + ... + d[K]) / r);  append (t, r, d, S, F) to out
L8      r ← r - leave
```

Line L1 is the only sort. The variable $r$ is the size of the risk set: it starts at $n$, and line L8 removes the subjects with time $t$ only after the time is processed, so a subject censored at $t$ counts at $t$. Line L6 must come before line L7, because the increment of $\hat F_k$ uses the survival just before $t$. The reference code works in Fractions, so its output is exact for exact input. It also has the general form for a multi-state model, described under the variants.

## Example

**Six subjects.** Times $1, 2, 2, 3, 4, 5$ with causes $1, 2, 0, 1, 0, 2$.

| $t$ | $r$ | $d_1$ | $d_2$ | leave | $\hat F_1$ | $\hat F_2$ | $\hat S$ |
|---|---|---|---|---|---|---|---|
| 1 | 6 | 1 | 0 | 1 | $1 \cdot \frac16 = \frac16$ | 0 | $\frac56$ |
| 2 | 5 | 0 | 1 | 2 | $\frac16$ | $\frac56 \cdot \frac15 = \frac16$ | $\frac56 \cdot \frac45 = \frac23$ |
| 3 | 3 | 1 | 0 | 1 | $\frac16 + \frac23 \cdot \frac13 = \frac{7}{18}$ | $\frac16$ | $\frac23 \cdot \frac23 = \frac49$ |
| 4 | 2 | 0 | 0 | 1 | no row | | |
| 5 | 1 | 0 | 1 | 1 | $\frac{7}{18}$ | $\frac16 + \frac49 = \frac{11}{18}$ | $0$ |

At every row $\hat F_1 + \hat F_2 + \hat S = 1$. At $t = 2$ the censored subject is in the risk set of 5, and only then does $r$ fall by 2. Treating cause 2 as censoring gives $1 - \hat S_1^\ast(3) = 1 - \frac56\cdot\frac23 = \frac49$, larger than $\hat F_1(3) = \frac{7}{18}$. The [competing risks](/competing-risks/) page shows the naive values next to these.

**An illness-death model.** States 0 (healthy), 1 (ill) and 2 (dead). Four subjects start healthy. Subject A becomes ill at time 1 and dies at 3. Subject B dies at 2 without illness. Subject C becomes ill at 2 and is censored at 4. Subject D is censored healthy at 2.5. The first row of the product $\prod(I + d\hat A)$ is the estimate of $(P(\text{healthy}), P(\text{ill}), P(\text{dead}))$ at time $t$ for a subject healthy at 0:

| $t$ | transitions (at risk) | row 0 of $I + d\hat A$ | row 1 | $\hat P_{0\cdot}(t)$ |
|---|---|---|---|---|
| 1 | 0 to 1: one of 4 | $(\frac34, \frac14, 0)$ | $(0, 1, 0)$ | $(\frac34, \frac14, 0)$ |
| 2 | 0 to 1 and 0 to 2: one each of 3 | $(\frac13, \frac13, \frac13)$ | $(0, 1, 0)$ | $(\frac14, \frac12, \frac14)$ |
| 3 | 1 to 2: one of 2 | $(1, 0, 0)$ | $(0, \frac12, \frac12)$ | $(\frac14, \frac14, \frac12)$ |

The probability of being ill at time 3 is $\frac14$. It cannot be read from any single Kaplan-Meier curve.

**A simulation.** The tests draw 2000 subjects with cause-specific hazards $1$ and $0.5$ and an independent censoring rate $0.3$, so $F_1(t) = \frac23(1 - e^{-1.5t})$. At $t = 0.2, 0.5, 1$ and $2$ both estimates lie within 4 standard errors of the truth. This is a measurement for one seed, not a proof of consistency.

## Correctness

The proof in [proofs/correctness.md](proofs/correctness.md) shows six things. First, the pass of lines L3 to L8 keeps $r = n_j$ at the start of each time, so every row is $(t_j, n_j, d_{\cdot j}, \hat S(t_j), \hat F_\cdot(t_j))$. Second, with one cause $\hat F_1 = 1 - \hat S$. Third, $\hat S(t) + \sum_k \hat F_k(t) = 1$ for every $t$. Fourth, $1 - \hat S_k^\ast(t) \ge \hat F_k(t)$, where $\hat S_k^\ast$ is Kaplan-Meier with the other causes censored. Fifth, without censoring $\hat F_k(t)$ is the fraction of subjects with an event of cause $k$ by $t$. Sixth, for the general product integral every row of $\hat P$ sums to $1$ with entries in $[0, 1]$, the competing risks case gives lines L6 and L7, and without censoring $\hat P_{0h}(t)$ is the fraction of subjects in state $h$ at $t$. The consistency and the limit law are cited, not proved.

## Complexity

The sort in line L1 costs $\Theta(n \log n)$. The pass visits each subject once and does $O(K)$ work at each of the $m$ event times, so it costs $\Theta(n + mK)$. The output holds $m$ rows of $K + 1$ numbers, $\Theta(mK)$ space. In exact arithmetic the denominators of $\hat S(t_j)$ divide $n_1 \cdots n_j$, so the numbers grow, as for Kaplan-Meier. In floating point there is no cancellation: every increment is a product of nonnegative numbers.

The general product integral for a process with $s$ states costs $\Theta(N \log N)$ to sort the $N$ transitions and censorings. Multiplying by $I + d\hat A(t_j)$ changes only the columns $g$ and $h$ of $\hat P(0, t)$ for each pair $(g, h)$ with a move at $t_j$, so each such pair costs $O(s)$ for the whole matrix, as in the reference code.

## Properties

- **Reduces to Kaplan-Meier.** With $K = 1$, $\hat F_1 = 1 - \hat S$.
- **Additivity.** $\hat S + \sum_k \hat F_k = 1$, and $\sum_{k \in A}\hat F_k$ is the Aalen-Johansen estimate for the merged cause $A$.
- **Bounded by the naive estimate.** $\hat F_k \le 1 - \hat S_k^\ast$, with equality at $t$ only if no other cause has an event before $t$ while cause $k$ still has events.
- **Plug-in form.** $\hat F_k(t) = \int_0^t \hat S(u-)\,d\hat H_k(u)$, where $\hat H_k$ is the Nelson-Aalen estimate of the cause-specific cumulative hazard. It is the population formula of the competing risks page with each part estimated.
- **Inverse probability of censoring weights.** $\hat F_k(t) = \frac1n\sum_i 1\{y_i \le t, c_i = k\}/\hat G(y_i-)$, where $\hat G$ is the Kaplan-Meier estimate of the censoring distribution with the events counted first at tied times. It follows from the identity $n_j/n = \hat S(t_j-)\hat G(t_j-)$, which the [Fine-Gray](/fine-gray-model/) page proves: the increment $\hat S(t_j-)d_{kj}/n_j$ equals $d_{kj}/(n\hat G(t_j-))$.
- **Large samples.** Under independent censoring, $\sqrt n(\hat F_k - F_k)$ converges on $[0, \tau]$ to a Gaussian process (Aalen and Johansen 1978; Andersen et al. 1993, Chapter IV). We cite this and do not prove it. A Greenwood-type formula or the delta method gives the variance.

## Variants and improvements

- **Multi-state models.** For a Markov process with states $0, \ldots, s - 1$, let $N_{gh}(t_j)$ count the moves from $g$ to $h$ at $t_j$ and $Y_g(t_j)$ the subjects in $g$ just before $t_j$ and under observation. With $d\hat A_{gh} = N_{gh}/Y_g$ for $g \ne h$ and the diagonal chosen so each row sums to $0$, the estimate of the transition matrix is $\hat P(s, t) = \prod_{s < t_j \le t}(I + d\hat A(t_j))$, a product integral, the discrete analogue of the [matrix exponential](/matrix-exponential/) of the cumulative intensity. Competing risks is the case with one transient state and $K$ absorbing ones.
- **Delayed entry.** Subjects that enter at $v_i$ are at risk only for $v_i < t \le y_i$. The pass then needs entries and exits in time order.
- **Non-Markov processes.** If the process is not Markov, $\hat P_{0h}(0, t)$ from a start at time 0 is still consistent for the state occupation probabilities under independent censoring (Datta and Satten 2001). Transition probabilities from later times need other estimators.
- **Covariates.** The [Fine-Gray model](/fine-gray-model/) regresses $F_k$ on covariates directly. Cause-specific Cox models, combined through the plug-in formula, give a second route.
- **Comparing groups.** Gray's test compares the cumulative incidence of one cause between groups.

## When to use it

Use it whenever an event of interest can be prevented by other events: to report the risk of relapse when patients can die in remission, the risk of cancer death in elderly cohorts, or the probability of being in each state of a disease process. Do not report one minus Kaplan-Meier with the competing events censored as a risk. Report the curves of all causes, or at least of the main competing cause, so the reader can see why one cause looks rare.

## Pitfalls

- **Censoring the competing events.** It gives $1 - \hat S_k^\ast$, which overstates the risk, and the curves of several causes can add up to more than $1$.
- **Order of the updates.** Updating $\hat S$ before the increment of $\hat F_k$ uses the wrong survival, and the sum of the estimates is then less than $1 - \hat S$.
- **Ties with censoring.** Count a censored subject at $t$ in the risk set at $t$.
- **Dependent censoring.** If the censoring depends on the risk of an event, the estimate is biased, as Kaplan-Meier is. Censoring weights that depend on covariates, as in [inverse probability weighting](/inverse-probability-weighting/), can correct this when the dependence is through measured covariates.
- **Cause-specific hazards are not risks.** The cumulative incidence depends on all the causes. A treatment that lowers the hazard of death from other causes raises the cumulative incidence of cancer death, even with no effect on the cancer hazard.
- **The tail.** With few subjects at risk at the end, each event moves the estimates by a large step.

## Implementations

## History

Odd O. Aalen and Søren Johansen published the empirical transition matrix for non-homogeneous Markov chains with censored data in the Scandinavian Journal of Statistics in 1978, as a product integral of the Nelson-Aalen increments, with its martingale representation and its asymptotic behavior. For one transition it reduces to Kaplan-Meier. The cumulative incidence formula for competing risks was in use before, in the actuarial "crude probability" of death from a cause and in the work of Kalbfleisch and Prentice (1980). Gill and Johansen (1990) developed the theory of product integration that underlies the estimator, and Andersen, Borgan, Gill and Keiding (1993) collected the counting process proofs.

## References
