---
tag: MYE9WM
kind: theorem
slug: packing-lower-bound
name: Packing lower bound for differential privacy
aliases:
- Hardt-Talwar packing argument
area: security-and-privacy/differential-privacy
level: advanced
summary: "If many datasets close to one dataset each need their own region of outputs, an epsilon-DP mechanism fails on one of them unless there are at most about e^(m epsilon) of them."
history:
  year: 2010
  people: [Moritz Hardt, Kunal Talwar]
  note: Hardt and Talwar used packing arguments at STOC 2010 for lower bounds on linear queries. Beimel, Brenner, Kasiviswanathan and Nissim used one for private learning of point functions.
prereqs: [differential-privacy-definition, approximate-differential-privacy, group-privacy-theorem]
see_also: [dinur-nissim-reconstruction-attack, fingerprinting-codes-lower-bound, private-query-release, laplace-mechanism, exponential-mechanism, gaussian-mechanism, histogram, vc-dimension]
sources:
  - paper: doi:10.1007/978-3-319-57048-8_7
    title: "Salil Vadhan, The complexity of differential privacy, in Tutorials on the Foundations of Cryptography, Springer, 2017, pages 347 to 450"
    locator: "Lemma 2.2 (group privacy), Section 5.2: Theorem 5.13 (packing lower bound), Theorem 5.14 (non-redundant queries) and Theorem 5.15 (packing characterization of sample complexity)"
  - paper: doi:10.1561/0400000042
    title: "Cynthia Dwork and Aaron Roth, The Algorithmic Foundations of Differential Privacy, Foundations and Trends in Theoretical Computer Science 9(3-4), 2014"
    locator: "Section 8.2: Lemma 8.4 (2^s datasets at pairwise distance at most Delta give epsilon at least (ln 2)(s-1)/Delta) and Corollary 8.5"
  - paper: "Moritz Hardt and Kunal Talwar, On the geometry of differential privacy, STOC 2010, pages 705 to 714"
    locator: the packing and volume lower bounds for linear queries under epsilon-DP
  - paper: "Amos Beimel, Hai Brenner, Shiva Prasad Kasiviswanathan and Kobbi Nissim, Bounds on the sample complexity for private learning and private data release, Machine Learning 94(3), 2014, pages 401 to 437"
    locator: the packing lower bound for proper private learning of point functions
---

The packing lower bound is a counting argument that limits every differentially private mechanism. Take a family $C$ of datasets that are all within $m$ changed rows of one dataset $x_0$, and suppose that a mechanism must put each $x \in C$ in its own region $G_x$ of outputs, with the regions disjoint. [Group privacy](/group-privacy-theorem/) says that the output law on $x_0$ is close to the law on each $x \in C$, so $x_0$ must give each region a fair share of its mass. The regions are disjoint and the mass is 1, so $C$ cannot be large: for $\varepsilon$-DP and success $\frac{1}{2}$, $|C| \le 2e^{m\varepsilon}$. For counting queries that tell all elements of the universe $X$ apart, this gives error $\Omega(\log|X|/(\varepsilon n))$ for pure DP, and with $\delta > 0$ the bound $\Omega(\min\{\log|X|, \log(1/\delta)\}/(\varepsilon n))$.

## Statement

**Setting.** A dataset is $x \in X^n$. Two datasets are neighbors if they differ in one row (replace), and $d(x, x')$ is the number of rows in which they differ. $M : X^n \to Y$ is $(\varepsilon, \delta)$-DP. A counting query is $q : X \to \{0, 1\}$, with the answer $q(x) = \frac{1}{n}\sum_i q(x_i)$.

**Theorem 1 (packing; Vadhan Theorem 5.13, Dwork-Roth Lemma 8.4).** Let $C \subseteq X^n$ be datasets with $d(x, x_0) \le m$ for all $x \in C$, and let $\{G_x\}_{x \in C}$ be disjoint sets of outputs. If $P[M(x) \in G_x] \ge p$ for every $x \in C$, then

$$\frac{1}{|C|} \ge p\,e^{-m\varepsilon} - \delta \min\{m, 1/(e^{\varepsilon} - 1)\}.$$

For $p = \frac{1}{2}$ and $\delta = 0$, $|C| \le 2e^{m\varepsilon}$, so $m \ge \ln(|C|/2)/\varepsilon$.

**Theorem 2 (non-redundant queries; Vadhan Theorem 5.14).** Let $Q$ be a set of counting queries that tells all elements of $X$ apart: for all $w \ne w'$ in $X$ some $q \in Q$ has $q(w) \ne q(w')$. Let $M$ be $(\varepsilon, \delta)$-DP with $\varepsilon \le 1$, and suppose that on every dataset, with probability at least $\frac{1}{2}$, $M$ answers all of $Q$ with error at most $\alpha < (n-1)/(2n)$. Then

$$\alpha \ge \frac{1}{2n}\left(\frac{\ln(|X|/4)}{\varepsilon} - 1\right) \quad \text{or} \quad \alpha \ge \frac{1}{2n}\left(\frac{\ln(\varepsilon/(4\delta))}{\varepsilon} - 1\right).$$

So $\alpha \ge \min\{\Omega(\log|X|/(\varepsilon n)), \Omega(\log(1/\delta)/(\varepsilon n)), \frac{1}{2}\}$ when $\delta \le \varepsilon^2/16$, since then $\ln(\varepsilon/(4\delta)) \ge \frac{1}{2}\ln(1/\delta)$.

**Theorem 3 (packing characterization; Vadhan Theorem 5.15, stated without proof).** For pure DP and constant error, the least $n$ is of order $\log P_\beta(K)/(\beta\varepsilon)$, where $K$ is the convex hull of the answer vectors $(q(w))_{q \in Q}$ of single elements $w \in X$ and $P_\beta(K)$ is the largest number of points of $K$ at pairwise $\ell_\infty$ distance above $\beta$. The lower bound is Theorem 1, and the upper bound is the [exponential mechanism](/exponential-mechanism/) over such a packing. See Vadhan for the exact quantifiers over $\alpha$ and $\beta$.

**The lesson.** Pure DP pays the logarithm of the number of outputs that must be told apart, divided by $\varepsilon$, in rows. Approximate DP can avoid this cost once $\log(1/\delta)$ is below $\log|X|$, and then other methods, such as the [fingerprinting code lower bound](/fingerprinting-codes-lower-bound/), give the limits.

## In plain words

A private method must act almost the same on datasets that differ in a few rows. Suppose you have many datasets, all a few rows away from one central dataset, and the method must give a clearly different answer for each.

On the central dataset, the method must still give each of these answers with a fair chance, because the central dataset is close to all of them. But the chances on one dataset add up to at most 1. So only a few datasets can each have their own answer. If the queries must tell apart $|X|$ such datasets, the number of changed rows must be about $\log|X|/\varepsilon$, and that sets a floor on the error.

## Proof

**Group privacy with an exact constant.** Let $d(x, x') = k$ and let $x = y_0, y_1, \dots, y_k = x'$ be a path of neighbors. Apply the definition of $(\varepsilon, \delta)$-DP $k$ times:

$$P[M(x) \in T] \le e^{k\varepsilon} P[M(x') \in T] + \delta \sum_{j=0}^{k-1} e^{j\varepsilon}.$$

This is Vadhan Lemma 2.2, before its last step bounds the sum by $k e^{k\varepsilon}$.

**Theorem 1.** Fix $x \in C$ and apply group privacy with $k = d(x, x_0) \le m$ and $T = G_x$. Since $P[M(x) \in G_x] \ge p$,

$$P[M(x_0) \in G_x] \ge e^{-m\varepsilon}\Big(p - \delta \sum_{j=0}^{m-1} e^{j\varepsilon}\Big) = p\,e^{-m\varepsilon} - \delta \sum_{i=1}^{m} e^{-i\varepsilon}.$$

The last sum is at most $m$, and at most $\sum_{i \ge 1} e^{-i\varepsilon} = 1/(e^{\varepsilon} - 1)$. (A path shorter than $m$ gives a larger right side, so the bound holds for all $x \in C$.) The sets $G_x$ are disjoint, so

$$1 \ge P\Big[M(x_0) \in \bigcup_{x \in C} G_x\Big] = \sum_{x \in C} P[M(x_0) \in G_x] \ge |C|\big(p\,e^{-m\varepsilon} - \delta \min\{m, 1/(e^{\varepsilon} - 1)\}\big).$$

Divide by $|C|$. For $p = \frac{1}{2}$ and $\delta = 0$ this is $|C| \le 2e^{m\varepsilon}$. $\blacksquare$

**Theorem 2.** Let $m = \lfloor 2\alpha n + 1 \rfloor$, so $2\alpha n < m \le 2\alpha n + 1 < n$ by the bound on $\alpha$. Fix $w_0 \in X$. For each $w \in X$, let $x(w)$ have its first $m$ rows equal to $w$ and the other $n - m$ rows equal to $w_0$. Let $C = \{x(w) : w \in X\}$, so $|C| = |X|$ and $d(x(w), x(w_0)) \le m$. Let $G_x$ be the closed $\ell_\infty$ ball of radius $\alpha$ around the answer vector $(q(x))_{q \in Q}$. Then $P[M(x) \in G_x] \ge \frac{1}{2}$. For $w \ne w'$, take $q$ with $q(w) \ne q(w')$: then $|q(x(w)) - q(x(w'))| = m/n > 2\alpha$, so $G_{x(w)}$ and $G_{x(w')}$ are disjoint. Theorem 1 with $x_0 = x(w_0)$, $p = \frac{1}{2}$ and $1/(e^{\varepsilon} - 1) \le 1/\varepsilon$ gives

$$\frac{1}{|X|} \ge \frac{1}{2}e^{-m\varepsilon} - \frac{\delta}{\varepsilon}.$$

So one of the two terms on the right is at least $\frac{1}{4}e^{-m\varepsilon}$. If $1/|X| \ge \frac{1}{4}e^{-m\varepsilon}$, then $m \ge \ln(|X|/4)/\varepsilon$. If $\delta/\varepsilon \ge \frac{1}{4}e^{-m\varepsilon}$, then $m \ge \ln(\varepsilon/(4\delta))/\varepsilon$. In both cases $\alpha \ge (m - 1)/(2n)$ gives the claim. If $\delta \le \varepsilon^2/16$, then $\sqrt\delta \le \varepsilon/4$, so $\varepsilon/(4\delta) \ge \delta^{-1/2}$ and $\ln(\varepsilon/(4\delta)) \ge \frac{1}{2}\ln(1/\delta)$. $\blacksquare$

**A note on the source.** Vadhan Theorem 5.13 prints the term $-\delta$, but its proof derives $-m\delta$ from Lemma 2.2, and $-m\delta$ is what group privacy gives. The form above, with $\delta\min\{m, 1/(e^{\varepsilon} - 1)\}$, is what the proof supports. Vadhan's proof of Theorem 5.14 uses the term $-\delta$; with the corrected term the $\log(1/\delta)$ case needs a condition such as $\delta \le \varepsilon^2/16$, as above.

## Consequences

- **Point functions and attribute means.** For $X = \{0,1\}^d$, the $d$ attribute means $q_j(w) = w_j$ tell all $2^d$ elements apart. So every $\varepsilon$-DP mechanism has error $\Omega(d/(\varepsilon n))$ on them, which the [Laplace mechanism](/laplace-mechanism/) matches (Vadhan, after Theorem 5.14; a theorem). Point functions, which ask "how many rows equal $w$?", give the same $\Omega(d/(\varepsilon n))$ for pure DP and $\Omega(\log(1/\delta)/(\varepsilon n))$ for approximate DP, and a stability-based [histogram](/histogram/) matches the second.
- **Pure and approximate DP differ.** With $\delta > 0$, group privacy says nothing past $m \approx \ln(1/\delta)/\varepsilon$ rows, and Theorem 1 becomes empty. This is why the [Gaussian mechanism](/gaussian-mechanism/) can answer $d$ attribute means with error $O(\sqrt{d \log(1/\delta) \log d}/(\varepsilon n))$, below the pure-DP floor $d/(\varepsilon n)$.
- **Lower bounds for query release.** For [private query release](/private-query-release/) with pure DP, Theorem 3 gives the sample complexity for constant error, and the volume form of Hardt and Talwar gives lower bounds on the error of $d$ linear queries.
- **Learning.** Beimel, Brenner, Kasiviswanathan and Nissim use packing to show that proper private learners of point functions need about $\log|X|/\varepsilon$ samples, which is more than the [VC dimension](/vc-dimension/) predicts.
- **Practice.** The bound does not depend on the noise source. A real mechanism that meets it still needs a cryptographic source of randomness and exact sampling (Mironov 2012; Canonne, Kamath and Steinke 2020).

**A worked example.** Take $X = \{0,1\}^3$, the 3 attribute means, $n = 10$ and $\alpha = 0.1$. Then $m = \lfloor 3 \rfloor = 3$, and the 8 datasets $x(w)$ have 3 rows equal to $w$ and 7 rows equal to $000$. Two of them differ by $3/10 = 0.3 > 2\alpha$ in some mean, so the 8 balls of radius 0.1 are disjoint. Theorem 1 with $\delta = 0$ and $p = \frac{1}{2}$ gives $8 \le 2e^{3\varepsilon}$, so $\varepsilon \ge \ln(4)/3 \approx 0.46$. No $\varepsilon$-DP mechanism with $\varepsilon < 0.46$ answers the 3 means of 10 rows within 0.1 with probability $\frac{1}{2}$ on every dataset.

## Tightness

The bounds are tight in several cases (theorems). For attribute means and pure DP, $\Omega(d/(\varepsilon n))$ matches the Laplace mechanism, which adds $\mathrm{Lap}(d/(\varepsilon n))$ to each mean. Here $\mathrm{Lap}(b)$ has the density $(1/(2b))e^{-|z|/b}$, the variance $2b^2$ and $P(|Z| > t) = e^{-t/b}$. For point functions, the two terms $d/(\varepsilon n)$ and $\log(1/\delta)/(\varepsilon n)$ are matched by the Laplace histogram and the stability-based histogram (Vadhan Proposition 2.8 and Theorem 3.5). The error $\frac{1}{2}$ is reached by the $(0, 0)$-DP mechanism that answers $\frac{1}{2}$ to every query. The bound is weak when $\delta > 0$ and many queries are asked: for $d$ attribute means with $\delta > 0$ the truth is about $\sqrt d/(\varepsilon n)$, which the packing bound cannot show and fingerprinting codes do.

## History

Packing arguments for privacy appear in Hardt and Talwar (STOC 2010), who used them with the geometry of the convex body $K$ to bound the error of linear queries under $\varepsilon$-DP, and in Beimel, Brenner, Kasiviswanathan and Nissim (Machine Learning 2014), for private learning and data release. Dwork and Roth (2014, Section 8.2) give it as Lemma 8.4 in histogram form. Vadhan (2017, Section 5.2) gives the form used here, with the non-redundant queries and the characterization of sample complexity.

## References
