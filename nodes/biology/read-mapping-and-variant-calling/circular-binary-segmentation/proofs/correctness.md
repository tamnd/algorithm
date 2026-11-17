---
title: MAX-ARC returns the largest arc statistic, and the permutation p-value of CBS is valid
proves: [correctness]
status: full
---

**Setting.** A segment is a list $y = (y_0, \ldots, y_{n-1})$ of real numbers with $n \ge 2$. Think of $y$ as bent into a circle, so that $y_{n-1}$ is next to $y_0$. An *arc* is a set of positions that are consecutive on the circle, with at least one and at most $n - 1$ positions. For an arc $a$ with $k$ positions, let $\bar y_a$ be the mean of $y$ over $a$ and $\bar y_{\bar a}$ the mean over the other $n - k$ positions. With $s > 0$ the sample standard deviation of $y$,

$$Z(a) = \frac{|\bar y_a - \bar y_{\bar a}|}{s \sqrt{1/k + 1/(n - k)}}, \qquad T(y) = \max_a Z(a).$$

If $s = 0$, all values are equal and the code returns $T = 0$, which never gives a split.

**Lemma 1 (the arcs are the intervals).** Every arc is an interval $[i, j) = \{i, \ldots, j - 1\}$ with $0 \le i < j \le n$ and $1 \le j - i \le n - 1$, or the complement of such an interval. $Z(a) = Z(\bar a)$ for every arc $a$.

*Proof.* An arc that does not contain both $n - 1$ and $0$ is an interval. An arc that contains both wraps around the end of the list, and its complement does not contain $n - 1$ or $0$ (it is not empty and the arc is consecutive on the circle), so the complement is an interval. The complement of an arc is again an arc, with $n - k$ positions. The formula for $Z$ is symmetric under the exchange of $a$ and $\bar a$: the numerator changes sign inside the absolute value, and the sum $1/k + 1/(n-k)$ does not change. $\square$

So the maximum of $Z$ over all arcs equals the maximum over the intervals of Lemma 1, which are the pairs $(i, j)$ that line L14 visits.

**Lemma 2 (MAX-ARC).** MAX-ARC returns $T(y)$ and the first interval $(i, j)$, in the order of $i$ and then $j$, that reaches it.

*Proof.* Line L12 sets $S[t] = y_0 + \cdots + y_{t-1}$, so the sum of $y$ over $[i, j)$ is $S[j] - S[i]$, and the sum over the rest is $S[n] - (S[j] - S[i])$. With $k = j - i$, line L15 computes $d = \bar y_{[i,j)} - \bar y_{\text{rest}}$, and line L16 computes $Z([i, j))$. Line L14 visits every interval of Lemma 1 once, and the code replaces the best value only on a strictly larger $Z$, so the first maximizer is kept. By Lemma 1, the largest value is $T(y)$. $\square$

**Lemma 3 (the standard deviation does not matter for the test).** For every permutation $\pi$ of the positions, the sample standard deviation of $\pi(y)$ equals that of $y$.

*Proof.* The mean and the sum of squared deviations depend only on the multiset of values. $\square$

So the permutation test compares $T$ values that all use the same $s$, and replacing $s$ by any other function of the multiset (a robust scale, for example) gives the same test.

**Theorem (validity of the p-value).** Assume that under the null hypothesis the vector $y$ is exchangeable: its distribution does not change when the positions are permuted, as for independent values with the same distribution. Let lines L6 and L7 draw $N$ independent uniform random permutations $\pi_1, \ldots, \pi_N$ and set $p = (1 + \#\{k : T(\pi_k(y)) \ge T(y)\}) / (N + 1)$. Then $P(p \le \alpha) \le \alpha$ for every $\alpha \in [0, 1]$.

*Proof.* Let $\sigma$ be a uniform random permutation independent of everything else. By exchangeability, $y$ has the same distribution as $\sigma(y)$, so it is enough to prove the claim for $\sigma(y)$, with the same $\pi_k$. The $N + 1$ permutations $\sigma, \pi_1 \sigma, \ldots, \pi_N \sigma$ are independent and uniform: given $\sigma$, each $\pi_k \sigma$ is uniform because $\pi_k$ is, and the $\pi_k$ are independent. So the values $V_0 = T(\sigma(y))$ and $V_k = T(\pi_k(\sigma(y)))$ are exchangeable.

Let $R_l = \#\{l' : V_{l'} \ge V_l\}$, which counts $l$ itself, so that $p = R_0 / (N + 1)$. Fix an integer $r$. At most $r$ indices $l$ have $R_l \le r$: if $r + 1$ indices had it, the one among them with the smallest $V$ would have all $r + 1$ values $\ge$ its own, so its $R$ would be at least $r + 1$. By exchangeability, each $l$ has the same probability of $R_l \le r$, so

$$P(R_0 \le r) = \frac{1}{N + 1} \, E\Bigl[\#\{l : R_l \le r\}\Bigr] \le \frac{r}{N + 1}.$$

With $r = \lfloor \alpha (N + 1) \rfloor$, the event $p \le \alpha$ is the event $R_0 \le r$, so $P(p \le \alpha) \le \alpha$. $\square$

The code counts $T(\pi_k(y)) \ge T(y) - 10^{-12}\max(1, T(y))$ at line L6, so that two arrangements with the same statistic up to rounding count as a tie. This can only increase the count, so the p-value stays valid.

**Exact p-value of the example.** The page example has four high values, 1.1, 0.9, 1.0 and 1.2, among twelve. The positions of the four high values in a random permutation are a uniform set of 4 positions out of 12, and there are $\binom{12}{4} = 495$ such sets. When the four high values form an arc, which happens for 12 of the sets, that arc has the same values as the arc of the data, so $T \ge 3.2247$. A search over all other placements found that their largest $Z$ is 2.918, below 3.2247. So the exact p-value is $12 / 495 = 0.0242$, which the Monte Carlo estimate at line L7 approaches as $N$ grows.

**The recursion.** Lines L1 to L4 and L8 to L11 keep a stack of half-open segments of $x$ that cover it without overlap. Each split at lines L9 and L10 replaces a segment by two or three parts that cover it, and adds the inner end points to the cuts. A segment of length less than 2, or with $T = 0$, is not split. So the returned list is sorted, every cut is strictly inside $(0, n)$, and the segments between the cuts are exactly the parts that the last tests did not split. Each part is shorter than its parent, so the loop ends after at most $n - 1$ splits. The theorem applies to each test on its own. The segments are chosen from the data, so the whole procedure does not have a single error level; CBS treats $\alpha$ as a per-test threshold.

**Cost.** MAX-ARC takes $\Theta(n^2)$ time for a segment of length $n$: $n(n+1)/2 - 1$ intervals at $O(1)$ each after the $\Theta(n)$ prefix sums. One test with $N$ permutations takes $\Theta(N n^2)$ time. In the recursion, the segments at the same depth do not overlap, so their tests cost at most $\Theta(N n^2)$ in total for each depth, and the depth is at most the number of splits.
