---
tag: MA49SE
kind: definition
slug: binary-entropy-function
name: Binary entropy function
aliases:
- binary entropy
area: compression-and-coding/entropy-coding
level: core
summary: h(p) = -p log2 p - (1-p) log2 (1-p), the entropy of a coin with bias p. It estimates binomial coefficients and gives the capacity 1 - h(p) of the binary symmetric channel.
prereqs: [shannon-entropy, binomial-coefficient]
see_also: [binary-symmetric-channel, channel-capacity, hamming-bound, gilbert-varshamov-bound, stirling-approximation, asymptotic-equipartition-property, source-coding-theorem]
sources:
  - book: isbn:9780471241959
    title: Thomas M. Cover and Joy A. Thomas, Elements of Information Theory, second edition, Wiley, 2006
    locator: Section 2.1 (the binary entropy, Example 2.1.1 and Figure 2.1), Section 7.1 (the binary symmetric channel) and Section 11.1 (the size of a type class, Theorem 11.1.3)
  - paper: doi:10.1002/j.1538-7305.1948.tb01338.x
    title: C. E. Shannon, A mathematical theory of communication, Bell System Technical Journal 27(3), 1948
    locator: Section 6, Figure 7 (entropy in the case of two possibilities with probabilities p and 1 - p)
  - book: isbn:9780521642989
    title: David J. C. MacKay, Information Theory, Inference, and Learning Algorithms, Cambridge University Press, 2003
    locator: Chapter 1 (the binary entropy function H_2 and its use to approximate binomial coefficients)
---

The binary entropy function is $h(p) = -p \log_2 p - (1-p) \log_2 (1-p)$ for $0 \le p \le 1$. It is the [Shannon entropy](/shannon-entropy/) of one toss of a coin that shows heads with probability $p$. It is symmetric about $1/2$, concave, and has its maximum 1 at $p = 1/2$. Its second use is counting: $\binom{n}{k}$ is $2^{n h(k/n)}$ to within a factor $n + 1$, and this estimate is behind the capacity of the [binary symmetric channel](/binary-symmetric-channel/), the [Hamming bound](/hamming-bound/) and the [Gilbert-Varshamov bound](/gilbert-varshamov-bound/).

## Definition

Notation. $p \in [0, 1]$ is the probability of one of two outcomes. Logarithms are base 2 and $0 \log 0 = 0$. $n$ is a length and $k$ is a count of ones, with $0 \le k \le n$. The probability model is a single Bernoulli($p$) variable, or $n$ independent ones; the counting results need no model.

**Definition.**

$$h(p) = p \log_2 \frac{1}{p} + (1 - p) \log_2 \frac{1}{1 - p}.$$

So $h(p) = H(X)$ for $X$ with $\Pr[X = 1] = p$, $\Pr[X = 0] = 1 - p$.

### Properties

1. **Values at the ends.** $h(0) = h(1) = 0$.
2. **Symmetry.** $h(p) = h(1 - p)$.
3. **Maximum.** $h(p) \le 1$, with equality only at $p = 1/2$.
4. **Derivative.** On $(0, 1)$, $h'(p) = \log_2 \frac{1 - p}{p}$ and $h''(p) = -\frac{1}{p (1 - p) \ln 2} < 0$. So $h$ is strictly concave, increases on $[0, 1/2]$ and decreases on $[1/2, 1]$. The slope is infinite at the ends: $h'(p) \to +\infty$ as $p \to 0$.
5. **Small $p$.** $h(p) = p \log_2 \frac{1}{p} + p \log_2 e + O(p^2)$, since $(1-p) \log_2 \frac{1}{1-p} = p \log_2 e + O(p^2)$.
6. **Inverse.** On $[0, 1/2]$, $h$ is a continuous increasing bijection onto $[0, 1]$, so it has an inverse $h^{-1} : [0, 1] \to [0, 1/2]$. There is no closed form; bisection finds it, since $h$ is increasing there.

*Proof.* (1) and (2) follow from the formula. (4) Differentiate: $\frac{d}{dp}(-p \log_2 p) = -\log_2 p - \log_2 e$ and $\frac{d}{dp}(-(1-p) \log_2 (1-p)) = \log_2 (1 - p) + \log_2 e$, and the sum is $\log_2 \frac{1-p}{p}$. Differentiate again to get $h''$. (3) $h'(p) > 0$ for $p < 1/2$ and $h'(p) < 0$ for $p > 1/2$, so the only maximum is at $1/2$, where $h = 1$. (5) Use $\ln \frac{1}{1-p} = p + O(p^2)$. $\square$

### The binomial estimate

**Claim.** For $0 \le k \le n$,

$$\frac{1}{n + 1} \, 2^{n h(k/n)} \le \binom{n}{k} \le 2^{n h(k/n)}.$$

*Proof (Cover and Thomas, Section 11.1, in the binary case).* Let $p = k/n$. If $k = 0$ or $k = n$, both sides are easy: $\binom{n}{k} = 1$ and $h(p) = 0$. Otherwise $0 < p < 1$. The terms $t_j = \binom{n}{j} p^j (1-p)^{n-j}$ for $j = 0, \ldots, n$ are the probabilities of a Binomial($n$, $p$) law, so they sum to 1. Also

$$p^k (1 - p)^{n - k} = 2^{k \log_2 p + (n - k) \log_2 (1-p)} = 2^{-n (p \log_2 \frac{1}{p} + (1-p) \log_2 \frac{1}{1-p})} = 2^{-n h(p)},$$

so $t_k = \binom{n}{k} 2^{-n h(p)}$.

Upper bound: $t_k \le \sum_j t_j = 1$, so $\binom{n}{k} \le 2^{n h(p)}$.

Lower bound: $t_k$ is the largest term. The ratio of neighbours is $\frac{t_{j+1}}{t_j} = \frac{(n - j) k}{(j + 1)(n - k)}$. It is at least 1 if and only if $nk \ge jn + n - k$. For $j \le k - 1$ this holds, because $jn + n - k \le kn - k \le kn$. For $j \ge k$ it fails, because $jn + n - k \ge kn + n - k > kn$. So the $t_j$ increase up to $j = k$ and then decrease. The largest of $n + 1$ terms that sum to 1 is at least $\frac{1}{n+1}$, so $\binom{n}{k} 2^{-n h(p)} \ge \frac{1}{n + 1}$. $\square$

**Sums of binomials.** For $0 \le \alpha \le 1/2$ with $\alpha n$ an integer or not, $\sum_{j \le \alpha n} \binom{n}{j} \le 2^{n h(\alpha)}$. *Proof.* For $0 < \alpha \le 1/2$ we have $\frac{\alpha}{1-\alpha} \le 1$, so for $j \le \alpha n$, $\alpha^j (1 - \alpha)^{n - j} = (1-\alpha)^n \left(\frac{\alpha}{1-\alpha}\right)^j \ge (1-\alpha)^n \left(\frac{\alpha}{1-\alpha}\right)^{\alpha n} = 2^{-n h(\alpha)}$. Then $1 \ge \sum_{j \le \alpha n} \binom{n}{j} \alpha^j (1-\alpha)^{n-j} \ge 2^{-n h(\alpha)} \sum_{j \le \alpha n} \binom{n}{j}$. For $\alpha = 0$ the sum is 1. $\square$ The sum is the volume of a Hamming ball of radius $\alpha n$, so a ball of radius $\alpha n$ in $\{0, 1\}^n$ has $2^{n h(\alpha) + O(\log n)}$ points.

### Where the estimate is used

- **Typical sequences.** A Bernoulli($p$) source of length $n$ puts most of its probability on strings with about $pn$ ones, and there are about $2^{n h(p)}$ of them. This is the [asymptotic equipartition property](/asymptotic-equipartition-property/) for a coin, and the reason that $n h(p)$ bits suffice in the [source coding theorem](/source-coding-theorem/).
- **Channel capacity.** The [binary symmetric channel](/binary-symmetric-channel/) flips each bit with probability $p$. Its [capacity](/channel-capacity/) is $C = 1 - h(p)$ bits per use: the output has at most 1 bit of entropy, and the noise adds $h(p)$ bits of uncertainty that the receiver cannot remove.
- **Hamming bound.** Balls of radius $t = \tau n$ around the codewords of a binary code of length $n$ that corrects $t$ errors are disjoint. So the number of codewords is at most $2^n / \binom{n}{t}$, and the rate is at most $1 - h(\tau) + o(1)$.
- **Gilbert-Varshamov bound.** A greedy choice of codewords at distance at least $d = \delta n$ from each other gives at least $2^n / \sum_{j < d} \binom{n}{j}$ codewords, so binary codes of rate at least $1 - h(\delta)$ exist for $\delta < 1/2$.

## Examples and non-examples

**Values.**

| $p$ | $h(p)$ | $1 - h(p)$ |
|---|---|---|
| 0.01 | 0.0808 | 0.9192 |
| 0.05 | 0.2864 | 0.7136 |
| 0.1 | 0.4690 | 0.5310 |
| 0.11 | 0.49992 | 0.50008 |
| 0.2 | 0.7219 | 0.2781 |
| 0.25 | 0.8113 | 0.1887 |
| 1/3 | 0.9183 | 0.0817 |
| 0.5 | 1 | 0 |

So a binary symmetric channel that flips 11% of the bits has capacity about one half. The inverse goes the other way: $h^{-1}(0.5) = 0.1100$, $h^{-1}(0.25) = 0.0417$, $h^{-1}(0.9) = 0.3160$. At $p = 0.1$ the slope is $h'(0.1) = \log_2 9 = 3.17$.

**The binomial estimate for $n = 10$, $k = 3$.** $2^{10 h(0.3)} = 449.7$ and $449.7 / 11 = 40.9$, and $\binom{10}{3} = 120$ lies between them. The factor $n + 1$ is loose, but it is only $O(\log n)$ bits, so $\log_2 \binom{n}{k} = n h(k/n) - O(\log n)$. The code on this page checks both bounds with exact integers for every $k \le n \le 60$; the upper bound is an equality only at $k = 0$ and $k = n$. A sharper form from [Stirling's approximation](/stirling-approximation/) is $\binom{n}{pn} \approx 2^{n h(p)} / \sqrt{2 \pi n p (1 - p)}$.

**Non-examples.**

- $h$ is not the entropy of a coin with three or more sides. For three outcomes use $H(p_1, p_2, p_3)$; grouping gives $H(p_1, p_2, p_3) = h(p_1) + (1 - p_1) h\!\left(\frac{p_2}{1 - p_1}\right)$.
- $h(p) \ne -\log_2 p$. The single-outcome measure $-\log_2 p$ is the [self-information](/self-information/) of heads; $h(p)$ is the mean over heads and tails.
- $h$ is not linear near 0. Halving $p$ from 0.02 to 0.01 lowers $h$ from 0.1414 to 0.0808, not to half of 0.1414.
- $1 - h(p)$ is the capacity of the binary symmetric channel, not of the binary erasure channel, whose capacity is $1 - p$.

## Related definitions

- [Shannon entropy](/shannon-entropy/) is the general case for any finite alphabet; $h$ is the case $\sigma = 2$.
- The $q$-ary entropy function $h_q(x) = x \log_q (q - 1) - x \log_q x - (1 - x) \log_q (1 - x)$ plays the same role for codes over an alphabet of size $q$; for $q = 2$ it is $h$.
- [Conditional entropy](/conditional-entropy/) of the input of a binary symmetric channel given its output is $h(p)$ when the input is uniform.
- The method of types (Cover and Thomas, Chapter 11) extends the binomial estimate to multinomial coefficients: $\binom{n}{n_1, \ldots, n_\sigma} = 2^{n H(n_1/n, \ldots, n_\sigma/n) - O(\sigma \log n)}$.

## References
