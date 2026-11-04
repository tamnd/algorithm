---
tag: G8MFT2
kind: concept
slug: conditional-expectation
name: Conditional expectation
area: foundations/probabilistic-analysis
level: core
summary: Expectation of a variable given the value of another, a random variable in its own right.
prereqs: [expected-value, conditional-probability, random-variable, linearity-of-expectation]
see_also: [quicksort-expected-running-time, quickselect-expected-linear, method-of-conditional-expectations, walds-equation, martingale, variance, geometric-distribution, law-of-large-numbers]
sources:
  - book: isbn:9781107154889
    title: Michael Mitzenmacher and Eli Upfal, Probability and Computing, second edition
    locator: Section 2.3, Conditional Expectation; Section 2.5, Application, The Expected Run-Time of Quicksort; Section 6.3, Derandomization Using Conditional Expectations; Section 13.3, Wald's Equation
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 7.4.2, Expected running time (of randomized quicksort), and Section 9.2, Selection in expected linear time
  - book: isbn:9780521474658
    title: Rajeev Motwani and Prabhakar Raghavan, Randomized Algorithms
    locator: Chapter 5, The Probabilistic Method (the method of conditional probabilities)
---

The conditional expectation $\mathrm{E}[X \mid A]$ of a [random variable](/random-variable/) $X$ given an event $A$ with $\Pr[A] > 0$ is the [expected value](/expected-value/) of $X$ when the probabilities are replaced by the [conditional probabilities](/conditional-probability/) $\Pr[\,\cdot \mid A]$. Given a second variable $Y$, the function $y \mapsto \mathrm{E}[X \mid Y = y]$ applied to $Y$ is itself a random variable, written $\mathrm{E}[X \mid Y]$. Its main law, the law of total expectation $\mathrm{E}[\mathrm{E}[X \mid Y]] = \mathrm{E}[X]$, lets you compute an expectation by cases. It is how one sets up the expected-cost recurrences of [randomized quicksort](/randomized-quicksort/) and [quickselect](/randomized-quickselect/), and it is the base of the [method of conditional expectations](/method-of-conditional-expectations/) for derandomization.

## In plain words

Often the cost of a randomized program depends on one early random choice. Quicksort, for example, first picks a pivot, and the rest of the work depends on which pivot it got.

Conditional expectation is the average cost when you already know that choice. For each possible choice you compute the average of the rest of the run. Then you take the average of these numbers, weighted by how likely each choice is. The result is the plain average cost. This is the law of total expectation: average the averages, with the right weights.

When you do not fix the choice in advance, the conditional average is a new random quantity. It depends on the choice, and its own average is the overall average.

## The idea

We work on a [probability space](/probability-space/) with a countable sample space $\Omega$, as in the analysis of algorithms that flip finitely or countably many coins. All variables $X$ here have $\mathrm{E}[|X|] < \infty$.

### Definitions

**Given an event.** For an event $A$ with $\Pr[A] > 0$,

$$\mathrm{E}[X \mid A] = \sum_{x} x\,\Pr[X = x \mid A] = \frac{\mathrm{E}\big[X \cdot I\{A\}\big]}{\Pr[A]}.$$

The two forms agree: $\Pr[X = x \mid A]\Pr[A] = \Pr[\{X = x\} \cap A]$, and $\sum_x x\Pr[\{X = x\} \cap A] = \mathrm{E}[X \cdot I\{A\}]$. The sum converges absolutely because $\mathrm{E}[|X|\,I\{A\}] \le \mathrm{E}[|X|]$.

**Given a value.** For a discrete variable $Y$ and a value $y$ with $\Pr[Y = y] > 0$, $\mathrm{E}[X \mid Y = y]$ is the case $A = \{Y = y\}$.

**Given a variable.** Let $g(y) = \mathrm{E}[X \mid Y = y]$ for each $y$ with $\Pr[Y = y] > 0$. Then $\mathrm{E}[X \mid Y] = g(Y)$. It is a random variable: its value on an outcome $\omega$ is $g(Y(\omega))$. It is a function of $Y$ only. The values of $g$ where $\Pr[Y = y] = 0$ do not matter, because these outcomes have total probability 0.

### Linearity

For each event $A$ with $\Pr[A] > 0$, $\Pr[\,\cdot \mid A]$ is a probability measure on $\Omega$, and $\mathrm{E}[\,\cdot \mid A]$ is the expectation under it. So every rule of expectation holds for it. In particular, [linearity](/linearity-of-expectation/) holds with no independence condition:

$$\mathrm{E}[aX + bZ \mid A] = a\,\mathrm{E}[X \mid A] + b\,\mathrm{E}[Z \mid A], \qquad \mathrm{E}\big[aX + bZ \mid Y\big] = a\,\mathrm{E}[X \mid Y] + b\,\mathrm{E}[Z \mid Y].$$

Also, if $X$ is independent of $Y$, then $\Pr[X = x \mid Y = y] = \Pr[X = x]$, so $\mathrm{E}[X \mid Y = y] = \mathrm{E}[X]$ for each $y$ with $\Pr[Y = y] > 0$.

### The law of total expectation

**Theorem.** Let $\mathrm{E}[|X|] < \infty$, and let $Y$ be a discrete variable with countable range $R = \{y : \Pr[Y = y] > 0\}$. Then

$$\mathrm{E}[X] = \sum_{y \in R} \mathrm{E}[X \mid Y = y]\,\Pr[Y = y], \qquad \text{that is,} \qquad \mathrm{E}\big[\mathrm{E}[X \mid Y]\big] = \mathrm{E}[X].$$

More generally, if events $A_1, A_2, \ldots$ with $\Pr[A_i] > 0$ are pairwise disjoint and their union has probability 1, then $\mathrm{E}[X] = \sum_i \mathrm{E}[X \mid A_i]\Pr[A_i]$.

*Proof.* We prove the general form. The case of $Y$ takes $A_y = \{Y = y\}$ for $y \in R$: these events are disjoint, and their union has probability $\sum_{y \in R}\Pr[Y = y] = 1$.

1. By the definition, $\mathrm{E}[X \mid A_i]\Pr[A_i] = \mathrm{E}[X \cdot I\{A_i\}] = \sum_{\omega \in A_i} X(\omega)\Pr[\omega]$.
2. The series $\mathrm{E}[X] = \sum_{\omega \in \Omega} X(\omega)\Pr[\omega]$ converges absolutely, since $\mathrm{E}[|X|] < \infty$. An absolutely convergent series can be split into groups and summed group by group, in any order, with the same total.
3. Group the outcomes by the event $A_i$ that holds them. Each outcome of positive probability lies in exactly one $A_i$, by disjointness and because the union has probability 1. The outcomes of probability 0 add 0. So $\mathrm{E}[X] = \sum_i \sum_{\omega \in A_i} X(\omega)\Pr[\omega]$.
4. By step 1 the inner sum is $\mathrm{E}[X \mid A_i]\Pr[A_i]$.

For the second form: $\mathrm{E}[X \mid Y] = g(Y)$ takes the value $g(y)$ with probability $\Pr[Y = y]$, so $\mathrm{E}[g(Y)] = \sum_{y \in R} g(y)\Pr[Y = y]$, which is the right side of the first form. The series converges absolutely, since $|g(y)|\Pr[Y = y] \le \mathrm{E}[|X| \cdot I\{Y = y\}]$ and these terms sum to $\mathrm{E}[|X|]$. $\blacksquare$

The same proof, run inside $\Pr[\,\cdot \mid B]$, gives $\mathrm{E}[X \mid B] = \sum_i \mathrm{E}[X \mid A_i \cap B]\,\Pr[A_i \mid B]$ over the $A_i$ with $\Pr[A_i \cap B] > 0$. The method of conditional expectations below uses this form.

### The law of total variance

If $\mathrm{E}[X^2] < \infty$, then

$$\mathrm{Var}[X] = \mathrm{E}\big[\mathrm{Var}[X \mid Y]\big] + \mathrm{Var}\big[\mathrm{E}[X \mid Y]\big],$$

where $\mathrm{Var}[X \mid Y] = \mathrm{E}[X^2 \mid Y] - \mathrm{E}[X \mid Y]^2$. *Proof.* By the law of total expectation, the mean of the first term is $\mathrm{E}[X^2] - \mathrm{E}[\mathrm{E}[X \mid Y]^2]$. The second term is $\mathrm{E}[\mathrm{E}[X \mid Y]^2] - \mathrm{E}[\mathrm{E}[X \mid Y]]^2 = \mathrm{E}[\mathrm{E}[X \mid Y]^2] - \mathrm{E}[X]^2$. The sum is $\mathrm{E}[X^2] - \mathrm{E}[X]^2 = \mathrm{Var}[X]$, see [variance](/variance/). $\square$ The spread of $X$ is the average spread inside each case plus the spread between the cases.

## Examples

**The mean of a geometric variable.** Repeat independent trials with success probability $p \in (0, 1]$, and let $X$ be the number of trials up to and including the first success. First, $\mathrm{E}[X] = \sum_{k \ge 1} k(1-p)^{k-1}p$ is finite by the ratio test. Let $S$ be the event that the first trial succeeds. Then $\mathrm{E}[X \mid S] = 1$. Given $\bar S$, the trials from the second one on are a fresh sequence of independent trials, so $X - 1$ has the same distribution as $X$ and $\mathrm{E}[X \mid \bar S] = 1 + \mathrm{E}[X]$. By the law of total expectation,

$$\mathrm{E}[X] = p \cdot 1 + (1 - p)(1 + \mathrm{E}[X]),$$

so $p\,\mathrm{E}[X] = 1$ and $\mathrm{E}[X] = 1/p$. Rolling a fair die until a six takes 6 rolls on average. The finiteness check is needed: the equation $m = p + (1-p)(1 + m)$ alone cannot rule out $m = \infty$. See the [geometric distribution](/geometric-distribution/).

**Randomized quicksort, by conditioning on the pivot.** Let $C_n$ be the expected number of key comparisons that [randomized quicksort](/randomized-quicksort/) makes on $n$ distinct keys. The partition of $n$ keys compares each of the other $n - 1$ keys with the pivot once, as in [Lomuto's partition](/lomuto-partition/). We prove by strong induction on $n$ that the expectation depends only on $n$, and find it. $C_0 = C_1 = 0$. For $n \ge 2$, let $K$ be the rank of the pivot. It is uniform on $\{1, \ldots, n\}$. Given $K = k$, the two recursive calls get $k - 1$ and $n - k$ distinct keys, and they use fresh random choices, so by the induction hypothesis their expected costs are $C_{k-1}$ and $C_{n-k}$. By linearity of conditional expectation,

$$\mathrm{E}[\text{comparisons} \mid K = k] = n - 1 + C_{k-1} + C_{n-k}.$$

The law of total expectation, with $\Pr[K = k] = 1/n$, gives

$$C_n = n - 1 + \frac1n\sum_{k=1}^n \big(C_{k-1} + C_{n-k}\big) = n - 1 + \frac2n\sum_{k=0}^{n-1} C_k.$$

*Solving it.* Multiply by $n$: $nC_n = n(n-1) + 2\sum_{k=0}^{n-1}C_k$. Write the same for $n - 1$ (valid for $n \ge 2$, since it gives $C_1 = 0$ at $n - 1 = 1$) and subtract: $nC_n - (n-1)C_{n-1} = 2(n-1) + 2C_{n-1}$, so $nC_n = (n+1)C_{n-1} + 2(n-1)$. Divide by $n(n+1)$ and use $\frac{2(n-1)}{n(n+1)} = \frac{4}{n+1} - \frac2n$:

$$\frac{C_n}{n+1} = \frac{C_{n-1}}{n} + \frac{4}{n+1} - \frac2n.$$

Sum from 2 to $n$ with $C_1 = 0$: $\frac{C_n}{n+1} = 4\big(H_{n+1} - \frac32\big) - 2(H_n - 1) = 2H_n + \frac{4}{n+1} - 4$, where $H_n = \sum_{i=1}^n 1/i$ is a [harmonic number](/harmonic-series/). Hence

$$C_n = 2(n+1)H_n - 4n.$$

The recurrence gives $C_2 = 1$, $C_3 = \frac83$, $C_4 = \frac{29}6$, $C_5 = \frac{37}5$, $C_{10} = \frac{30791}{1260} = 24.44$ and $C_{100} = 647.85$, and the closed form matches it exactly for each $n$ from 1 to 100. The page [linearity of expectation](/linearity-of-expectation/) gets the same value with one indicator for each pair of keys and no recurrence. The page [expected running time of quicksort](/quicksort-expected-running-time/) gives the full analysis.

**Quickselect.** The same conditioning on the pivot rank gives the recurrence for [randomized quickselect](/randomized-quickselect/). There only one side is searched, and its size is at most $\max(k - 1, n - k)$, so the cost is at most $n - 1$ plus the average of the larger side. That bound solves to a linear function of $n$; see [quickselect in expected linear time](/quickselect-expected-linear/).

**Derandomizing a cut.** Place each vertex of a graph with $m$ edges on side 0 or 1 by a fair coin. Each edge crosses with probability $\frac12$, so the [cut](/maximum-cut/) $C$ has $\mathrm{E}[C] = m/2$. The [method of conditional expectations](/method-of-conditional-expectations/) turns this into a deterministic algorithm. Fix the sides of the vertices one at a time. Let $B$ be the event that the vertices fixed so far have their chosen sides, and let $v$ be the next vertex. Its coin is independent of $B$, so by the law of total expectation inside $\Pr[\,\cdot \mid B]$,

$$\mathrm{E}[C \mid B] = \tfrac12\,\mathrm{E}[C \mid B, v \to 0] + \tfrac12\,\mathrm{E}[C \mid B, v \to 1].$$

One of the two terms is at least $\mathrm{E}[C \mid B]$. Put $v$ on that side. The value never drops, so the final cut, which is no longer random, has at least $m/2$ edges. Each conditional expectation is easy to compute: it is the number of cut edges between fixed vertices plus half the number of other edges.

Take the vertices $1, \ldots, 5$ and the 7 edges $12, 13, 23, 24, 34, 45, 15$, and break ties toward side 0.

| step | $\mathrm{E}[C \mid \ldots, v \to 0]$ | $\mathrm{E}[C \mid \ldots, v \to 1]$ | side |
|---|---|---|---|
| start | | | $\mathrm{E}[C] = 3.5$ |
| vertex 1 | 3.5 | 3.5 | 0 |
| vertex 2 | 3 | 4 | 1 |
| vertex 3 | 4 | 4 | 0 |
| vertex 4 | 4 | 4 | 0 |
| vertex 5 | 3 | 5 | 1 |

The result has 5 cut edges, at least $3.5$. The maximum cut of this graph has 6 edges. Mitzenmacher and Upfal, Section 6.3, give this method for MAX-CUT, and the same method derandomizes the [random assignment for MAX-3-SAT](/random-assignment-max-3-sat/).

**A random number of terms.** Let $N$ be a non-negative integer variable with $\mathrm{E}[N] < \infty$, and let $X_1, X_2, \ldots$ have the same mean $\mu$ with $\mathrm{E}[|X_i|] \le c$ for a constant $c$, all independent of $N$. Let $S = \sum_{i=1}^N X_i$. By linearity and independence, $\mathrm{E}[S \mid N = n] = \sum_{i=1}^n \mathrm{E}[X_i \mid N = n] = n\mu$, so $\mathrm{E}[S \mid N] = N\mu$ and $\mathrm{E}[S] = \mu\,\mathrm{E}[N]$. (The interchange is valid because $\mathrm{E}[|S|] \le c\,\mathrm{E}[N] < \infty$.) [Wald's equation](/walds-equation/) proves the same result when $N$ is a stopping time, which may depend on the $X_i$ seen so far.

## Where it is used

- **Recurrences for expected cost.** Conditioning on the first random choice gives the recurrence of [randomized quicksort](/quicksort-expected-running-time/), of [quickselect](/quickselect-expected-linear/), of random [binary search trees](/random-bst-expected-depth/), and of many Las Vegas algorithms.
- **Derandomization.** The [method of conditional expectations](/method-of-conditional-expectations/) turns an existence proof by the [probabilistic method](/probabilistic-method/) into a deterministic algorithm, when the conditional expectations can be computed fast.
- **Martingales.** A sequence $Z_0, Z_1, \ldots$ with $\mathrm{E}[Z_{i+1} \mid Z_0, \ldots, Z_i] = Z_i$ is a [martingale](/martingale/). The Doob martingale $Z_i = \mathrm{E}[f \mid X_1, \ldots, X_i]$ reveals the inputs one at a time and leads to the [Azuma inequality](/azuma-inequality/) and the [optional stopping theorem](/optional-stopping-theorem/).
- **Variance by cases.** The law of total variance splits the spread of a cost into the spread inside each case and between the cases.

### Pitfalls

- **Conditioning on an event of probability 0.** The formula $\mathrm{E}[X \cdot I\{A\}]/\Pr[A]$ is undefined when $\Pr[A] = 0$. For continuous variables, $\mathrm{E}[X \mid Y = y]$ needs densities or the general measure-theoretic definition, and it is fixed only up to a set of probability 0.
- **$\mathrm{E}[X \mid Y]$ is a random variable.** It is a function of $Y$, not a number. $\mathrm{E}[X \mid Y = y]$ is a number. Writing $\mathrm{E}[X \mid Y] = \mathrm{E}[X]$ is a claim about each value of $Y$, true for example when $X$ and $Y$ are independent.
- **Wrong weights.** Average the conditional expectations with the weights $\Pr[Y = y]$, not with equal weights. If a hash lookup costs 1 probe with probability $0.9$ and 100 probes with probability $0.1$, the mean is $0.9 \cdot 1 + 0.1 \cdot 100 = 10.9$ probes, not $(1 + 100)/2 = 50.5$.
- **Expectation of a ratio or an inverse.** Conditioning does not let you move a nonlinear function out of the expectation. For $X$ uniform on $\{1, 2\}$, $\mathrm{E}[1/X] = \frac34$ but $1/\mathrm{E}[X] = \frac23$. In the same way, $\mathrm{E}[X/N]$ is in general not $\mathrm{E}[X]/\mathrm{E}[N]$.
- **Subproblems that are not fresh.** The quicksort recurrence needs the claim that, given the pivot rank, each recursive call has expected cost $C_{\text{size}}$. For randomized quicksort this follows from the fresh random choices. For deterministic quicksort on a random input it needs a separate proof that the partition keeps each subarray uniformly random, and a partition that breaks this property breaks the recurrence.
- **Conditioning can create dependence.** Two independent fair bits $X, Y$ are dependent given $X + Y = 1$, since then $Y = 1 - X$. Independence that holds without conditioning does not carry over to the conditional measure.
- **Infinite means.** The law of total expectation needs $\mathrm{E}[|X|] < \infty$, or $X \ge 0$ with $\infty$ allowed as a value. A self-referential equation such as $m = p + (1-p)(1 + m)$ is solved correctly only after $m < \infty$ is known.

## References
