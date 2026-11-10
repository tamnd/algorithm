---
tag: QD36BE
kind: definition
slug: smooth-function
name: Smooth function
aliases:
- smooth function property
- (alpha, beta)-smooth function
- smoothness in the sense of Braverman and Ostrovsky
area: online-and-streaming/sliding-windows
level: research
summary: A nonnegative function of a stream that does not grow when old items are dropped, and for which a suffix with almost the same value keeps almost the same value after any common continuation.
prereqs: [sliding-window-model, relative-error, frequency-moment-problem]
see_also: [smooth-histogram, exponential-histogram, dgim-algorithm, sliding-window-distinct-count, frequency-moment-problem, distinct-elements-problem, longest-increasing-subsequence, sliding-window-model]
sources:
  - paper: doi:10.1137/090749281
    title: Vladimir Braverman and Rafail Ostrovsky, Effective computations on sliding windows, SIAM Journal on Computing 39(6), 2010
    locator: Definition 1 (smooth functions), Lemma 4 (L_p norms), Lemma 5 (frequency moments) and Section 3.4 (longest increasing subsequence)
  - paper: doi:10.1137/S0097539701398363
    title: Mayur Datar, Aristides Gionis, Piotr Indyk and Rajeev Motwani, Maintaining stream statistics over sliding windows, SIAM Journal on Computing 31(6), 2002
    locator: the weakly additive functions handled by exponential histograms
  - paper: arxiv:1805.00212
    title: Vladimir Braverman, Elena Grigorescu, Harry Lang, David P. Woodruff and Samson Zhou, Nearly optimal distinct elements and heavy hitters on sliding windows, APPROX/RANDOM 2018
    locator: the use of smooth histograms for distinct elements and the lower bounds
---

A smooth function, in the sense of Braverman and Ostrovsky (2007), is a nonnegative function $f$ of a stream that does not grow when the oldest items are dropped, and that has this stability property: if a suffix $B$ of a stream $A$ has $f(B)$ within a factor $1 - \beta$ of $f(A)$, then $f(B \cup C)$ stays within a factor $1 - \alpha$ of $f(A \cup C)$ for each continuation $C$. Smoothness is the condition under which the [smooth histogram](/smooth-histogram/) turns an insertion-only streaming algorithm for $f$ into a [sliding window](/sliding-window-model/) algorithm with only $O(\frac{1}{\beta} \log W)$ copies. Sums, counts, the maximum, the number of distinct values and the frequency moments $F_p$ are smooth; the largest frequency $F_\infty$ is not. On this page streams are finite sequences, $A \cup C$ is the concatenation of $A$ and then $C$, and $W$ is the window size.

## Definition

For streams $A$ and $B$, write $B \subseteq_r A$ when $B$ is a suffix of $A$: $A$ is some stream followed by $B$. A stream $C$ is *adjacent* to $A$ when it comes right after $A$, so that $A \cup C$ is a stream.

**Definition (Braverman and Ostrovsky, Definition 1).** Let $0 < \beta \le \alpha < 1$. A function $f$ from streams to the reals is **$(\alpha, \beta)$-smooth** if:

1. $f(A) \ge 0$ for each stream $A$.
2. $f(A) \ge f(B)$ whenever $B \subseteq_r A$ (dropping old items does not raise $f$).
3. $f(A)$ is bounded by a polynomial in the length of $A$.
4. For all streams $A$, $B$, $C$ with $B \subseteq_r A$ and $C$ adjacent to $A$:
$$(1 - \beta)\, f(A) \le f(B) \quad\Longrightarrow\quad (1 - \alpha)\, f(A \cup C) \le f(B \cup C).$$

The function is **smooth** if for each $\alpha \in (0, 1)$ there is a $\beta = \beta(\alpha) \in (0, \alpha]$ such that $f$ is $(\alpha, \beta)$-smooth. The number of copies of the smooth histogram grows as $1/\beta$, so a function is more useful when $\beta(\alpha)$ is larger.

Condition 4 says: once a suffix has caught up with the whole stream within a factor $1 - \beta$, no later items can push the two apart by more than a factor $1 - \alpha$. Condition 2 gives the other direction for free: $f(B \cup C) \le f(A \cup C)$, since $B \cup C$ is a suffix of $A \cup C$.

## Examples and non-examples

In each proof below, $B \subseteq_r A$, $C$ is adjacent to $A$, and $f(B) \ge (1 - \beta) f(A)$. Conditions 1 to 3 are direct for these functions.

- **Sum of nonnegative values, and the count.** $f$ is $(\alpha, \alpha)$-smooth for each $\alpha$. With $\beta = \alpha$: $f(B \cup C) = f(B) + f(C) \ge (1 - \alpha) f(A) + f(C) \ge (1 - \alpha)(f(A) + f(C)) = (1 - \alpha) f(A \cup C)$. Basic counting is the case of values in $\{0, 1\}$.
- **Maximum of nonnegative values.** $(\alpha, \alpha)$-smooth: $\max(f(B), f(C)) \ge \max((1 - \alpha) f(A), f(C)) \ge (1 - \alpha) \max(f(A), f(C))$.
- **Number of distinct values, $F_0$.** $(\alpha, \alpha)$-smooth. Write $D(X)$ for the number of distinct values of $X$. Then $D(A \cup C) = D(A) + |C \setminus A|$, where $C \setminus A$ is the set of values of $C$ that do not occur in $A$. Every value of $B$ occurs in $A$, so $|C \setminus B| \ge |C \setminus A|$. Hence $D(B \cup C) = D(B) + |C \setminus B| \ge (1 - \alpha) D(A) + |C \setminus A| \ge (1 - \alpha) D(A \cup C)$.
- **Frequency moments (cited).** For $p \ge 1$, $F_p = \sum_i f_i^p$ is $(\alpha, (\alpha/p)^p)$-smooth, and for $0 < p < 1$ it is $(\alpha, \alpha)$-smooth (Lemma 5 of Braverman and Ostrovsky). The $L_p$ norms are smooth as well (their Lemma 4). For $F_2$ this gives $\beta = \alpha^2/4$.
- **Length of the longest increasing subsequence (cited).** Braverman and Ostrovsky show that the length of the [longest increasing subsequence](/longest-increasing-subsequence/) is smooth, in Section 3.4 of their paper.

Non-examples:

- **The largest frequency $F_\infty$.** It satisfies conditions 1 to 3, but it is not $(\alpha, \beta)$-smooth for any $\alpha < 1/2$ and any $\beta$. Take $A = x^k y^k$ ($k$ copies of $x$, then $k$ copies of $y$), $B = y^k$ and $C = x^k$. Then $f(A) = f(B) = k$, so the hypothesis of condition 4 holds for each $\beta$. But $f(A \cup C) = f(x^k y^k x^k) = 2k$ and $f(B \cup C) = f(y^k x^k) = k$, so condition 4 needs $k \ge (1 - \alpha) 2k$, that is $\alpha \ge 1/2$.
- **Sums with negative values.** Condition 1 fails, because the suffix $-3$ of the stream $5, -3$ has sum $-3$. Condition 2 fails too: the stream $-3, 5$ has sum 2, and its suffix $5$ has sum 5. DGIM show that such sums need $\Omega(W)$ bits over a window.
- **The average and the variance.** Condition 2 fails for both. The stream $0, 4$ has average 2, and its suffix $4$ has average 4. The stream $4, 0, 4$ has population variance $32/9$, and its suffix $0, 4$ has variance $4$.
- **The geometric mean.** Braverman and Ostrovsky give it as an example of a function that is not nondecreasing in the sense of condition 2.

## Related definitions

- **Weakly additive functions.** DGIM handle functions with $f(A) + f(B) \le f(A \cup B) \le C_f\,(f(A) + f(B))$ for adjacent $A$ and $B$, with buckets of the [exponential histogram](/exponential-histogram/). Smoothness asks for less structure: no bucket summaries need to combine, only one insertion-only sketch per start time.
- **Suffix monotone functions.** Conditions 1 and 2 alone describe the functions for which the start of the window can only lower the value. They are needed for any histogram over start times; condition 4 bounds how many start times must be kept.
- **The smooth histogram.** The [smooth histogram](/smooth-histogram/) keeps, for an $(\alpha, \beta)$-smooth $f$, the sketches of $O(\frac{1}{\beta} \log W)$ suffixes and returns a $(1 \pm \alpha)$ approximation of $f$ over the window.
- **The $(\varepsilon, \delta)$ guarantee.** When the sketch of $f$ is randomized, the smooth histogram gives an [(ε, δ) guarantee](/epsilon-delta-guarantee/) on the window value.

## References
