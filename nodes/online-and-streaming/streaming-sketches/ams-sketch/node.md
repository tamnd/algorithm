---
tag: ATY7TN
kind: algorithm
slug: ams-sketch
name: AMS sketch
aliases:
- tug-of-war sketch
- Alon-Matias-Szegedy sketch
- AMS F_2 sketch
area: online-and-streaming/streaming-sketches
level: core
summary: Estimates the second frequency moment F_2 with random sign projections.
solves: [frequency-moment-problem]
model: streaming-model
complexity:
  vars: {}
  time: {worst: O((1/ε²) log(1/δ))}
  space: {extra: O((1/ε²) log(1/δ))}
properties: {online: true, deterministic: false, comparison: false, recursive: false}
prereqs: [frequency-vector, turnstile-model, k-wise-independence, chebyshev-inequality, median-trick]
see_also: [count-sketch, frequency-moment-problem, join-size-estimation-problem, indyk-p-stable-sketch, frequency-moment-lower-bounds, linear-sketch, johnson-lindenstrauss-lemma, k-wise-independent-hashing]
sources:
  - paper: doi:10.1006/jcss.1997.1545
    title: Noga Alon, Yossi Matias and Mario Szegedy, The space complexity of approximating the frequency moments, Journal of Computer and System Sciences 58(1), 1999 (STOC 1996)
    locator: Section 2.2, the improved estimate of F_2 with 4-wise independent signs (section number to check)
  - book: isbn:9781108477444
    title: Graham Cormode and Ke Yi, Small Summaries for Big Data, Cambridge University Press, 2020
    locator: Chapter 3, Summaries for multisets (the AMS sketch, its variance and its fast form with hashing)
  - paper: doi:10.1561/0400000002
    title: S. Muthukrishnan, Data Streams, Algorithms and Applications, Foundations and Trends in Theoretical Computer Science 1(2), 2005
    locator: the sections on sketches and on the estimation of F_2
---

The AMS sketch, or tug-of-war sketch, estimates the second frequency moment $F_2 = \sum_i f_i^2$ of a stream. It is due to Alon, Matias and Szegedy (1996). Each counter holds $Z = \sum_i s(i) f_i$ for a random sign function $s$, and $Z^2$ is an unbiased estimate of $F_2$ with variance at most $2F_2^2$ when the signs are 4-wise independent. The average of $t = \lceil 6/\varepsilon^2 \rceil$ such squares is within a factor $1 \pm \varepsilon$ of $F_2$ with probability at least $2/3$, and the median of $r = O(\log(1/\delta))$ such averages raises this to $1 - \delta$. The sketch uses $O((1/\varepsilon^2) \log(1/\delta))$ counters, works in the general [turnstile model](/turnstile-model/), and is a [linear sketch](/linear-sketch/). Here $m$ is the stream length, $n$ the universe size, and $f$ the [frequency vector](/frequency-vector/).

## In plain words

Split the items into two teams at random, as in a tug of war. Keep one number: add one for each arrival of a team A item and subtract one for each arrival of a team B item. At the end, square the number.

If one item is much more common than the rest, the number is about its count, and the square is about its count squared. In general, the cross terms between items have random signs and cancel on average, so the square is right on average.

One square can be far off, so repeat with many independent team splits. Average the squares in groups, and report the middle value of the group averages.

## The problem

The input is a stream of updates $(i, c)$ that add $c$ to $f_i$, with $i \in \{0, \ldots, n - 1\}$ and integers $c$ of any sign. The goal is an estimate $\hat F_2$ with $|\hat F_2 - F_2| \le \varepsilon F_2$ with probability at least $1 - \delta$, the relative form of the [epsilon-delta guarantee](/epsilon-delta-guarantee/). This is the case $p = 2$ of the [frequency moment problem](/frequency-moment-problem/). $F_2$ is the self-join size of a relation and the squared Euclidean length of $f$.

## The algorithm

The sketch keeps $r$ groups of $t$ counters. Counter $(g, k)$ has its own sign function $s_{g,k}$, drawn from a 4-wise independent family, and all these functions are independent.

```pseudo id=main
AMS-UPDATE(Z, i, c)                      ▷ add c to f_i
L1  for each group g and each k ← 1 to t do
L2      Z[g][k] ← Z[g][k] + s_{g,k}(i) · c

AMS-ESTIMATE(Z)
L3  for g ← 1 to r do Y_g ← (1/t) · Σ_k Z[g][k]²
L4  return the median of Y_1, …, Y_r

AMS-MERGE(Z, Z′)                         ▷ same sign functions
L5  return Z + Z′, counter by counter
```

Take $t = \lceil 6/\varepsilon^2 \rceil$ and $r = \lceil 18 \ln(1/\delta) \rceil$. For an even $r$, the code returns the lower median.

**The sign functions.** A sign function is 4-wise independent if for any four distinct items the four signs are independent fair signs, as in [k-wise independence](/k-wise-independence/). One family: pick a random polynomial $q(x) = a_3 x^3 + a_2 x^2 + a_1 x + a_0$ over the field $GF(2^b)$ with $2^b \ge n$, and let $s(i) = (-1)^{\text{low bit of } q(i)}$. The values of $q$ at four distinct points are independent and uniform, because a polynomial of degree at most 3 is fixed by its values at four points. Each function costs four field elements, $O(\log n)$ bits.

## Example

Take three items with $f = (2, 1, 1)$, so $F_2 = 4 + 1 + 1 = 6$. For three items, 4-wise independent signs are fully independent, so each of the 8 sign patterns has probability $1/8$. A pattern and its negation give the same $Z^2$.

| $s(1), s(2), s(3)$ | $Z = 2s(1) + s(2) + s(3)$ | $Z^2$ |
|---|---|---|
| $+, +, +$ | 4 | 16 |
| $+, +, -$ | 2 | 4 |
| $+, -, +$ | 2 | 4 |
| $+, -, -$ | 0 | 0 |

The mean of $Z^2$ is $(16 + 4 + 4 + 0)/4 = 6 = F_2$. The mean of $Z^4$ is $(256 + 16 + 16 + 0)/4 = 72$, so the variance is $72 - 36 = 36$. The formula in the proof gives $4 \sum_{i < j} f_i^2 f_j^2 = 4(4 + 4 + 1) = 36$, below $2F_2^2 = 72$.

One counter is often far off: it returns 0 or 16 with probability $1/4$ each. With $t = 24$ counters for $\varepsilon = 0.5$, the average has variance $36/24 = 1.5$, a standard deviation of about $1.22$, against the allowed error $3$.

## Correctness

**Theorem.** Let $Z = \sum_i s(i) f_i$ for a 4-wise independent fair sign function $s$. Then $\mathbb{E}[Z^2] = F_2$ and
$$ \mathrm{Var}[Z^2] = 4 \sum_{i < j} f_i^2 f_j^2 \le 2F_2^2 . $$

Expand $Z^2 = \sum_i f_i^2 + \sum_{i \ne j} s(i) s(j) f_i f_j$. The cross terms have mean 0 by pairwise independence, which gives the mean. For the variance, expand $Z^4$. A product $s(i) s(j) s(k) s(l)$ has mean 1 if each item in it appears an even number of times and mean 0 otherwise; this needs 4-wise independence. The surviving terms give $\mathbb{E}[Z^4] = F_2^2 + 2\sum_{i \ne j} f_i^2 f_j^2$. Since $2\sum_{i<j} f_i^2 f_j^2 \le (\sum_i f_i^2)^2 = F_2^2$, the variance is at most $2F_2^2$.

**Corollary.** The average $Y$ of $t \ge 6/\varepsilon^2$ independent copies has $\mathrm{Var}[Y] \le 2F_2^2/t$. By [Chebyshev's inequality](/chebyshev-inequality/), $\Pr[|Y - F_2| > \varepsilon F_2] \le 2/(t \varepsilon^2) \le 1/3$. The median of $r \ge 18 \ln(1/\delta)$ independent averages fails only if at least half of them fail, which by the Hoeffding bound has probability at most $e^{-r/18} \le \delta$. This is the [median trick](/median-trick/).

The full proof, with the expansion of $Z^4$ term by term, is below. The tests check $\mathbb{E}[Z^2] = F_2$ and the exact variance by listing all $8^4$ sign functions of a 4-wise independent family over $GF(8)$.

## Complexity

- **Space.** $tr = O((1/\varepsilon^2) \log(1/\delta))$ counters of $O(\log(mn))$ bits each, for updates of bounded size, and $4tr$ field elements of $O(\log n)$ bits for the sign functions.
- **Update time.** $O(tr) = O((1/\varepsilon^2) \log(1/\delta))$ sign evaluations, one for each counter. The fast form below reduces this to $O(\log(1/\delta))$.
- **Query time.** $O(tr)$ to form the averages and $O(r)$ for the median.
- **Merge.** $O(tr)$ additions.

## Properties

- **Linear.** $Z$ is a linear function of $f$, so deletions, negative weights and merges are free. The sketch of $f - g$ estimates $\|f - g\|_2^2$.
- **Randomized, with a relative guarantee.** The error is $\varepsilon F_2$, a factor of the answer, not of the stream length.
- **Limited independence suffices.** The proof needs only 4-wise independent signs, so the random bits fit in $O(\log n)$ bits for each counter.
- **Optimal up to constants in $\varepsilon$.** Any one-pass algorithm for a $(1 \pm \varepsilon)$ estimate of $F_2$ needs $\Omega(1/\varepsilon^2)$ bits, by a reduction from the gap Hamming problem; see [frequency moment lower bounds](/frequency-moment-lower-bounds/).

## Variants and improvements

- **Fast AMS.** Hash each item to one of $w$ buckets in each row, with a 4-wise independent sign, and estimate $F_2$ by $\sum_b C[j][b]^2$ for each row. This is a [count sketch](/count-sketch/) with 4-wise independent signs, used for $F_2$ by Thorup and Zhang (2004). Each update touches one counter per row, so the update time is $O(\log(1/\delta))$.
- **Inner products.** With the same signs for two streams, $Z_f Z_g$ is an unbiased estimate of $\langle f, g \rangle$ with variance at most $2F_2(f) F_2(g)$. This is the [join size](/join-size-estimation-problem/) estimator of Alon, Gibbons, Matias and Szegedy (1999).
- **Gaussian projections.** Replacing the signs by independent Gaussian values gives the same mean, a projection of the [Johnson-Lindenstrauss lemma](/johnson-lindenstrauss-lemma/) type, and the [Indyk p-stable sketch](/indyk-p-stable-sketch/) for $p = 2$.
- **The AMS sampling estimator for $F_k$.** For $k \ge 1$, pick a uniform random position $p$ of an insertion-only stream, let $R$ be the number of times the item $a_p$ occurs from position $p$ to the end, and output $X = m(R^k - (R - 1)^k)$. Then $\mathbb{E}[X] = F_k$, and $O(k n^{1 - 1/k} \varepsilon^{-2} \log(1/\delta))$ copies give a $(1 \pm \varepsilon)$ estimate. Alon, Matias and Szegedy gave this estimator in the same paper.

## When to use it

Use the AMS sketch to estimate $F_2$, the self-join size, the squared Euclidean distance between two streams, or the variance of the counts, especially when the stream has deletions or is split over many machines. Use the fast form in practice; the plain form with one sign evaluation for each counter is slow for small $\varepsilon$. For single counts rather than $F_2$, use the [count sketch](/count-sketch/). For $F_p$ with $p < 2$, use the [Indyk p-stable sketch](/indyk-p-stable-sketch/).

## Pitfalls

- **Pairwise signs for the variance.** Pairwise independence gives the right mean but not the variance bound: the proof of $\mathbb{E}[Z^4]$ uses products of four distinct signs. With only pairwise independent signs, the variance can be much larger.
- **Averaging without the median, or the median without averaging.** The average alone needs $O(1/(\varepsilon^2 \delta))$ counters for failure probability $\delta$. The median alone of single squares does not converge to $F_2$, since the median of $Z^2$ is not its mean.
- **An additive reading.** The guarantee is relative to $F_2$. If $F_2$ is near 0, as for the difference of two nearly equal streams, a small absolute error can be a large relative one.
- **Field size.** The polynomial family needs a field with at least $n$ elements, and the items must map to distinct field elements.

## Implementations

## History

Noga Alon, Yossi Matias and Mario Szegedy presented *The space complexity of approximating the frequency moments* at STOC 1996, with a journal version in JCSS in 1999. The paper started the theory of streaming algorithms. It gave the sampling estimator for $F_k$, the tug-of-war sketch for $F_2$ with 4-wise independent signs in $O(\log n + \log m)$ bits for each counter, and lower bounds showing that $F_k$ needs polynomial space for $k > 5$ and that $F_\infty$ needs linear space. The authors received the Gödel Prize in 2005 for this work. Alon, Gibbons, Matias and Szegedy (1999) used the same sketch for join sizes. The fast form with hashing appeared in work of Thorup and Zhang (2004) and of Cormode and Garofalakis (2005).

## References
