---
tag: WRNK0C
kind: theorem
slug: prophet-inequality
name: Prophet inequality
aliases:
- Krengel-Sucheston inequality
- single-item prophet inequality
area: online-and-streaming/competitive-analysis
level: advanced
summary: For independent nonnegative random variables seen one at a time, a single threshold rule earns at least half the expected maximum, and the factor 1/2 cannot improve.
prereqs: [expected-value, linearity-of-expectation, probability-distribution]
see_also: [secretary-problem, one-over-e-stopping-rule, competitive-ratio, online-algorithm, matroid, median, optional-stopping-theorem, online-knapsack-problem]
sources:
  - paper: "Ulrich Krengel and Louis Sucheston, Semiamarts and finite values, Bulletin of the American Mathematical Society 83(4) (1977), 745-747"
    locator: the announcement of the inequality E[sup X_n] <= 2 sup E[X_tau] for independent nonnegative variables, with the constant 2 credited to D. J. H. Garling
  - paper: doi:10.1214/aop/1176993150
    title: "Ester Samuel-Cahn, Comparison of threshold stop rules and maximum for independent nonnegative random variables, Annals of Probability 12(4) (1984), 1213-1216"
    locator: the main theorem (a threshold at the median of the maximum gives at least half of E[max])
  - paper: doi:10.1145/2213977.2213991
    title: "Robert Kleinberg and S. Matthew Weinberg, Matroid prophet inequalities, Proceedings of the 44th ACM Symposium on Theory of Computing (STOC), 2012, 123-136"
    locator: the single-item case with the threshold E[max]/2 and its short proof, then the extension to matroids
  - paper: "Theodore P. Hill and Robert P. Kertz, A survey of prophet inequalities in optimal stopping theory, Contemporary Mathematics 125 (1992), 191-207"
    locator: the history of the inequality and the tight example
---

The prophet inequality says that a gambler who sees independent nonnegative random values one at a time, with known distributions, and must take or leave each one at once, can earn at least half of what a prophet earns who sees all values and takes the largest. A single fixed threshold is enough: the median of the maximum (Samuel-Cahn 1984) or half of the expected maximum (Kleinberg and Weinberg 2012). The factor $1/2$ is tight, even for the best possible rule. Krengel and Sucheston proved the inequality in 1977, with the constant 2 due to Garling.

## Statement

Let $X_1, \ldots, X_n$ be independent random variables with values in $[0, \infty)$ and known distributions, and let $M = \max_i X_i$ with $\mathbb{E}[M] < \infty$. The values come in the order $1, \ldots, n$. A *stopping rule* $\tau$ chooses an index $\tau \in \{1, \ldots, n\} \cup \{\infty\}$ such that the event $\{\tau = i\}$ depends only on $X_1, \ldots, X_i$ (and on random bits independent of the $X_j$). It gains $X_\tau$, and $0$ if $\tau = \infty$.

For a threshold $t \ge 0$, let $\tau_t$ be the rule that stops at the first $i$ with $X_i \ge t$, and let $p(t) = \Pr[M \ge t]$ be the probability that it stops.

**Theorem.** For every $t \ge 0$,

$$\mathbb{E}[X_{\tau_t}] \;\ge\; p(t)\, t + \bigl(1 - p(t)\bigr)\bigl(\mathbb{E}[M] - t\bigr).$$

In particular:

1. (Kleinberg and Weinberg) with $t = \mathbb{E}[M]/2$, $\mathbb{E}[X_{\tau_t}] \ge \mathbb{E}[M]/2$;
2. (Samuel-Cahn) if $p(t) = 1/2$, for example if $t$ is a median of $M$ and $M$ has a continuous distribution, then $\mathbb{E}[X_{\tau_t}] \ge \mathbb{E}[M]/2$;
3. (Krengel, Sucheston and Garling) $\sup_\tau \mathbb{E}[X_\tau] \ge \mathbb{E}[M]/2$, and the constant $1/2$ is the best possible.

In the terms of [online algorithms](/online-algorithm/), the gambler is an online algorithm, the prophet is the [offline optimum](/offline-optimum/), and the theorem says that the ratio $\mathbb{E}[M] / \mathbb{E}[\mathrm{ALG}]$ is at most $2$ when the input is drawn from known independent distributions.

## In plain words

Several prizes are shown one at a time. Each prize has a random value, and the gambler knows in advance how each value is distributed. The gambler can keep one prize. At each prize the gambler must keep it or give it up for good. A prophet knows all the values and keeps the best one.

The gambler can do half as well as the prophet, on average, with a plain rule: fix one number in advance and keep the first prize worth at least that number. Half of the prophet's average is a good number. The middle value of the best prize is also good. No rule, however clever, can always do better than half, because the largest prize can be rare and come last.

## Proof

Fix $t \ge 0$ and write $p = p(t)$ and $x^+ = \max(x, 0)$. Let $A_i$ be the event that $X_j < t$ for every $j < i$, which is the event that the rule has not stopped before step $i$. Then $\Pr[A_i] \ge \Pr[A_{n+1}] = 1 - p$, since $A_i \supseteq A_{n+1}$.

**Step 1 (split the gain).** The rule stops at step $i$ exactly on $A_i \cap \{X_i \ge t\}$. On that event $X_i = t + (X_i - t)^+$, and off the event $\{X_i \ge t\}$ the term $(X_i - t)^+$ is $0$. So

$$X_{\tau_t} = t \cdot \mathbf{1}[\tau_t < \infty] + \sum_{i=1}^{n} \mathbf{1}[A_i]\,(X_i - t)^+.$$

**Step 2 (use independence).** The event $A_i$ depends only on $X_1, \ldots, X_{i-1}$, so it is independent of $X_i$. By [linearity of expectation](/linearity-of-expectation/),

$$\mathbb{E}[X_{\tau_t}] = p\,t + \sum_{i=1}^{n} \Pr[A_i]\, \mathbb{E}[(X_i - t)^+] \;\ge\; p\,t + (1 - p) \sum_{i=1}^{n} \mathbb{E}[(X_i - t)^+].$$

Each $\mathbb{E}[(X_i - t)^+] \le \mathbb{E}[X_i] \le \mathbb{E}[M]$ is finite.

**Step 3 (compare with the prophet).** For every outcome, $\sum_i (X_i - t)^+ \ge \max_i (X_i - t)^+ = (M - t)^+ \ge M - t$. Take expectations: $\sum_i \mathbb{E}[(X_i - t)^+] \ge \mathbb{E}[M] - t$. Put this into Step 2 to get the main inequality.

**Step 4 (the two thresholds).** With $t = \mathbb{E}[M]/2$, the right side is $p\,t + (1-p)\,t = \mathbb{E}[M]/2$ for every value of $p$. With $p = 1/2$, the right side is $\frac12 t + \frac12(\mathbb{E}[M] - t) = \mathbb{E}[M]/2$ for every $t$. If $M$ has a continuous distribution, $p(t) = \Pr[M \ge t]$ is continuous in $t$ and goes from $1$ to $0$, so a $t$ with $p(t) = 1/2$ exists. This proves parts 1 and 2, and part 1 gives the first claim of part 3.

**Step 5 (no rule beats one half).** Let $\varepsilon \in (0, 1)$, $X_1 = 1$ with certainty, and $X_2 = 1/\varepsilon$ with probability $\varepsilon$ and $0$ otherwise. Then $\mathbb{E}[M] = (1 - \varepsilon) \cdot 1 + \varepsilon \cdot (1/\varepsilon) = 2 - \varepsilon$. A rule either stops at step 1 and gains $1$, or goes on and gains $\mathbb{E}[X_2] = 1$, or mixes the two. Every rule gains exactly $1$, so

$$\frac{\sup_\tau \mathbb{E}[X_\tau]}{\mathbb{E}[M]} = \frac{1}{2 - \varepsilon} \to \frac12 \quad (\varepsilon \to 0).$$

So no constant larger than $1/2$ holds for all distributions. $\blacksquare$

The proof uses independence only in Step 2, and only to say that $X_i$ does not depend on the past. It does not use the order of the variables, so the bound holds for every order, and even when an adversary chooses the order in advance.

## Consequences

- **Posted prices.** A seller with one item and buyers who arrive one by one with independent values from known distributions can post one price $t = \mathbb{E}[M]/2$ and sell to the first buyer who accepts. The expected welfare is at least half of the best possible welfare. This is the base result of the theory of posted price mechanisms.
- **Matroids and other constraints.** Kleinberg and Weinberg (2012) extend the threshold to the case where the gambler may keep a set of prizes that is independent in a [matroid](/matroid/), with the same factor $1/2$. Their thresholds are again half of an expected loss of the prophet.
- **Link to the secretary problem.** The [secretary problem](/secretary-problem/) has no knowledge of distributions but a random order, and its best rule wins with probability about $1/e$. The prophet inequality has known distributions but an arbitrary order, and gets $1/2$ of the expectation. Both are standard models of online selection with a [competitive ratio](/competitive-ratio/) measured in expectation.
- **Online knapsack and allocation.** Threshold rules of this kind, set from known distributions, are the base of many algorithms for the [online knapsack problem](/online-knapsack-problem/) with stochastic items.

## Tightness

Step 5 shows that the factor $1/2$ cannot improve for general independent distributions in a fixed order. With $\varepsilon = 1/10$: $\mathbb{E}[M] = 19/10$, the best rule gains $1$, and the threshold $t = 19/20$ also gains $1$, since it stops at step 1.

**A worked example.** Let $X_1 \in \{0, 4\}$ with probability $1/2$ each, $X_2 = 1$ with probability $2/3$ and $6$ with probability $1/3$, and $X_3 = 0$ with probability $3/4$ and $12$ with probability $1/4$. Then $\mathbb{E}[M] = 23/4$.

| rule | stop probability | expected gain |
|---|---|---|
| threshold $t = \mathbb{E}[M]/2 = 23/8$ | $3/4$ | $2 + 1 + 1 = 4$ |
| threshold $t = 6$, where $\Pr[M \ge 6] = 1/2$ | $1/2$ | $0 + 2 + 2 = 4$ |
| best rule, by backward induction | | $4$ |
| prophet | $1$ | $23/4$ |

The best rule is computed from the last step back. Before $X_3$ the value of going on is $\mathbb{E}[X_3] = 3$. Before $X_2$ it is $\frac23 \max(1, 3) + \frac13 \max(6, 3) = 4$. Before $X_1$ it is $\frac12 \max(0, 4) + \frac12 \max(4, 4) = 4$. Both thresholds are optimal here, and the ratio is $16/23 \approx 0.70 > 1/2$.

**Better constants with more structure.** The factor $1/2$ improves when the variables are i.i.d.: the best constant is about $0.745$. Kertz (1986) gave i.i.d. instances where no rule gets more than this fraction of $\mathbb{E}[M]$, and Correa, Foncea, Hoeksma, Oosterwijk and Vredeveld (2017) proved that a rule with a sequence of thresholds always gets it. It also improves when the gambler may choose the order of the variables, or when the order is uniformly random.

**Atoms.** If $M$ has atoms, a $t$ with $\Pr[M \ge t] = 1/2$ may not exist. Samuel-Cahn's rule then accepts a value equal to $t$ only with a suitable probability, so that the stop probability is exactly $1/2$; Steps 1 to 4 hold without change for this randomized tie break. The threshold $\mathbb{E}[M]/2$ needs no tie break.

The implementation checks all of these numbers with exact fractions, and checks the main inequality for every threshold on 600 random discrete instances against brute-force enumeration.

## History

Krengel and Sucheston (1977) proved that $\mathbb{E}[\sup_n X_n] \le 2 \sup_\tau \mathbb{E}[X_\tau]$ for independent nonnegative variables, as a part of their work on semiamarts, and credited the constant $2$ to D. J. H. Garling. The name "prophet inequality" comes from the comparison of a gambler with a prophet who sees the future. Samuel-Cahn (1984) showed that a single threshold at the median of the maximum is enough. Kleinberg and Weinberg (2012) gave the threshold $\mathbb{E}[M]/2$ with the short proof above and extended it to matroids, which led to a large body of work on prophet inequalities in mechanism design. Hill and Kertz (1992) survey the probability literature up to that time.

## References
