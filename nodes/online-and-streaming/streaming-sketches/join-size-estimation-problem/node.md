---
tag: NB3AEP
kind: problem
slug: join-size-estimation-problem
name: Join size estimation problem
aliases:
- self-join size
- inner product of frequency vectors
- AGMS join size estimation
area: online-and-streaming/streaming-sketches
level: core
summary: Estimate the inner product of two frequency vectors, such as the size of a database join.
prereqs: [frequency-vector, frequency-moment-problem, epsilon-delta-guarantee]
see_also: [ams-sketch, count-min-sketch, count-sketch, linear-sketch, disjointness-problem, gap-hamming-distance, frequency-moment-lower-bounds, median-trick]
sources:
  - paper: doi:10.1006/jcss.2001.1813
    title: Noga Alon, Phillip B. Gibbons, Yossi Matias and Mario Szegedy, Tracking join and self-join sizes in limited storage, Journal of Computer and System Sciences 64(3), 2002 (PODS 1999, pages 10 to 20)
    locator: the tug-of-war estimator for the join size with shared signs, its variance bound, and the lower bounds in terms of the join size (to check)
  - paper: doi:10.1006/jcss.1997.1545
    title: Noga Alon, Yossi Matias and Mario Szegedy, The space complexity of approximating the frequency moments, Journal of Computer and System Sciences 58(1), 1999 (STOC 1996)
    locator: the F_2 sketch, which is the self-join case
  - paper: doi:10.1016/j.jalgor.2003.12.001
    title: Graham Cormode and S. Muthukrishnan, An improved data stream summary, the count-min sketch and its applications, Journal of Algorithms 55(1), 2005
    locator: pages 58 to 75, the inner product query with error ε times the product of the L1 norms
  - book: isbn:9781108477444
    title: Graham Cormode and Ke Yi, Small Summaries for Big Data, Cambridge University Press, 2020
    locator: Chapter 3, Summaries for multisets (inner products with the AMS sketch and the Count-Min sketch)
---

The join size estimation problem asks for the inner product $\langle f, g \rangle = \sum_i f_i g_i$ of the [frequency vectors](/frequency-vector/) of two streams. If the streams are the values of a join attribute in two relations $R$ and $S$, this is the number of tuples in the equijoin $R \bowtie S$. The case $f = g$ is the self-join size $F_2$. A relative error is impossible in small space, because deciding whether $\langle f, g \rangle = 0$ is set disjointness. The standard guarantee is additive: the tug-of-war estimator of Alon, Gibbons, Matias and Szegedy (1999) gives an error at most $\varepsilon \sqrt{F_2(f) F_2(g)}$ with probability $1 - \delta$, with $O(\varepsilon^{-2} \log(1/\delta))$ counters for each stream. Here $n$ is the size of the domain of the attribute.

## In plain words

Two tables share a column, such as a customer number. Joining them pairs every row of the first table with every row of the second that has the same number. Before running the join, a database wants to know how large the result will be.

For each number, the join has as many rows as the product of its counts in the two tables. So the size is a sum of products of counts. A sketch of each table, built with the same random signs, gives a fair guess of this sum. The error is small compared with the sizes of the self-joins of the two tables. When the true answer is much smaller than that, no small summary can find it.

## Definition

The input is two streams over the domain $[n]$, which can be interleaved: updates $(R, i, c)$ add $c$ to $f_i$, and updates $(S, i, c)$ add $c$ to $g_i$. In the insertion-only model, each tuple of $R$ with attribute value $i$ is one update $(R, i, 1)$. The join size is
$$ J = |R \bowtie_A S| = \sum_{i=1}^n f_i g_i = \langle f, g \rangle . $$
The self-join size of $R$ is $\langle f, f \rangle = F_2(f)$.

The goal is an estimate $\hat J$ with
$$ \Pr\left[ |\hat J - J| \le \varepsilon \sqrt{F_2(f) F_2(g)} \right] \ge 1 - \delta . $$
By the Cauchy-Schwarz inequality, $|J| \le \sqrt{F_2(f) F_2(g)}$, so this is an error relative to the largest possible join size for the given self-join sizes. The cost is the space in words for each stream, with the sketches of the two streams built with shared random bits.

## Variants

- **Self-join size.** For $f = g$, the additive bound is $\varepsilon F_2$, a relative bound. This is the $F_2$ case of the [frequency moment problem](/frequency-moment-problem/), solved by the [AMS sketch](/ams-sketch/).
- **Error in the first norm.** For non-negative counts, $|\hat J - J| \le \varepsilon \|f\|_1 \|g\|_1 = \varepsilon |R| \, |S|$ is a weaker goal, met by the [count-min sketch](/count-min-sketch/) with $O(\varepsilon^{-1} \log(1/\delta))$ counters.
- **Multi-way joins.** The size of a chain join $R_1 \bowtie R_2 \bowtie \cdots \bowtie R_k$ is a sum of products of counts. With one independent family of signs for each join attribute, the product of the sketches is again unbiased, with a variance that grows exponentially in $k$.
- **Turnstile streams.** Tuples can be inserted and deleted, and the estimators below handle this because they are [linear sketches](/linear-sketch/).

## Examples

Let the join attribute of $R$ have the values $a, a, b, c$ and that of $S$ the values $a, b, b, b, d$. Then $f = (f_a, f_b, f_c, f_d) = (2, 1, 1, 0)$ and $g = (1, 3, 0, 1)$.

- The join size is $J = 2 \cdot 1 + 1 \cdot 3 + 1 \cdot 0 + 0 \cdot 1 = 5$: two tuples of $R$ with $a$ meet one tuple of $S$, and one tuple with $b$ meets three.
- The self-join sizes are $F_2(f) = 6$ and $F_2(g) = 11$, so $\sqrt{F_2(f) F_2(g)} \approx 8.1$.
- With the signs $s = (+1, -1, +1, -1)$, the tug-of-war counters are $Z_f = 2 - 1 + 1 = 2$ and $Z_g = 1 - 3 - 1 = -3$, so one estimate is $-6$.
- Over all 16 sign patterns, the estimate $Z_f Z_g$ takes the values $-6, -2, 0, 6, 10, 12, 20$, with mean exactly 5 and variance exactly 65. The bound below gives $F_2(f) F_2(g) + J^2 - 2 \sum_i f_i^2 g_i^2 = 66 + 25 - 26 = 65$.

## Known algorithms

**The tug-of-war product estimator (Alon, Gibbons, Matias and Szegedy 1999).** Draw a 4-wise independent sign function $s : [n] \to \{-1, +1\}$, and keep $Z_f = \sum_i s(i) f_i$ and $Z_g = \sum_i s(i) g_i$ with the same $s$. Then
$$ \mathbb{E}[Z_f Z_g] = J , \qquad \mathrm{Var}[Z_f Z_g] = F_2(f) F_2(g) + J^2 - 2 \sum_i f_i^2 g_i^2 \le 2 F_2(f) F_2(g) . $$

*Proof.* $Z_f Z_g = \sum_{i,j} f_i g_j s(i) s(j)$, and $\mathbb{E}[s(i) s(j)] = 1[i = j]$, so the mean is $\sum_i f_i g_i$. For the second moment, $Z_f^2 Z_g^2 = \sum_{i,j,k,l} f_i f_j g_k g_l \, s(i) s(j) s(k) s(l)$. With 4-wise independent signs, a term has mean 1 if every index occurs an even number of times and 0 otherwise. The surviving index patterns are $i = j$ with $k = l$, which give $F_2(f) F_2(g)$, and the two patterns $i = k \ne j = l$ and $i = l \ne j = k$, which give $2 \sum_{i \ne j} f_i g_i f_j g_j = 2(J^2 - \sum_i f_i^2 g_i^2)$. So $\mathbb{E}[Z_f^2 Z_g^2] = F_2(f) F_2(g) + 2J^2 - 2\sum_i f_i^2 g_i^2$, and subtracting $J^2$ gives the variance. Finally $J^2 \le F_2(f) F_2(g)$ by Cauchy-Schwarz, and $\sum_i f_i^2 g_i^2 \ge 0$. $\square$

Averaging $t = \lceil 6/\varepsilon^2 \rceil$ independent products gives variance at most $2F_2(f) F_2(g)/t$, so by Chebyshev's inequality the average is within $\varepsilon \sqrt{F_2(f) F_2(g)}$ of $J$ with probability at least $2/3$. The median of $\lceil 18 \ln(1/\delta) \rceil$ such averages is within this error with probability $1 - \delta$, by the [median trick](/median-trick/). The total is $O(\varepsilon^{-2} \log(1/\delta))$ counters for each stream.

**Hashed sketches.** With a [count sketch](/count-sketch/) of each stream, built with the same bucket hashes and 4-wise independent signs, the estimate $\sum_b C_f[j][b] \, C_g[j][b]$ for each row is unbiased with the same kind of variance bound, and each update touches one counter per row.

**The count-min inner product.** With [count-min sketches](/count-min-sketch/) of $f \ge 0$ and $g \ge 0$ with the same hash functions, $\min_j \sum_b C_f[j][b] \, C_g[j][b]$ is at least $J$ and at most $J + \varepsilon \|f\|_1 \|g\|_1$ with probability $1 - \delta$, with $w = \lceil e/\varepsilon \rceil$ columns (Cormode and Muthukrishnan 2005).

**Sampling.** Sampling tuples of each relation and joining the samples estimates $J$, but the variance is large when a few values are common in both relations. Methods such as bifocal sampling treat the common values apart from the rest.

## Bounds

- **Upper bound.** $O(\varepsilon^{-2} \log(1/\delta))$ counters for each stream for the error $\varepsilon \sqrt{F_2(f) F_2(g)}$, by the estimator above.
- **No relative error.** Any algorithm that tells $J = 0$ from $J \ge 1$ with probability $2/3$, even for 0-1 vectors in the insertion-only model, needs $\Omega(n)$ bits. So no small-space algorithm gives $(1 \pm \varepsilon) J$ for any $\varepsilon < 1$. The proof is the reduction from disjointness below.
- **The dependence on $\varepsilon$.** For the error $\varepsilon \sqrt{F_2(f) F_2(g)}$, $\Omega(\varepsilon^{-2})$ bits are needed, by a reduction from the [gap Hamming problem](/gap-hamming-distance/), below.

## Reductions

**From set disjointness.** Let Alice hold $A \subseteq [n]$ and Bob hold $B \subseteq [n]$. Alice feeds the stream of $R$-tuples $(R, i)$ for $i \in A$ into a join size algorithm and sends its memory, $s$ bits, to Bob. Bob continues with $(S, i)$ for $i \in B$ and reads the estimate. Here $f = 1_A$, $g = 1_B$ and $J = |A \cap B|$. If the algorithm tells $J = 0$ from $J \ge 1$ with probability $2/3$, this is a one-way protocol for [disjointness](/disjointness-problem/) with $s$ bits. The randomized communication complexity of disjointness is $\Omega(n)$ (Kalyanasundaram and Schnitger 1992, Razborov 1992), even for one-way protocols, so $s = \Omega(n)$. Any estimate within a factor $1 \pm \varepsilon$ with $\varepsilon < 1$ is 0 exactly when $J = 0$, so it tells the two cases apart.

**From gap Hamming.** Let Alice and Bob hold $x, y \in \{0, 1\}^n$, with the promise that the Hamming distance is at least $n/2 + \sqrt{n}$ or at most $n/2 - \sqrt{n}$. Use $f = x$ and $g = y$ as above, and let Alice also send $|x|$ in $\lceil \log_2(n+1) \rceil$ bits. Then $\mathrm{Ham}(x, y) = |x| + |y| - 2J$, so the two cases differ in $J$ by at least $\sqrt{n}$, and an error below $\sqrt{n}/2$ separates them. Since $\sqrt{F_2(f) F_2(g)} = \sqrt{|x| \, |y|} \le n$, this holds for $\varepsilon < 1/(2\sqrt{n})$. Gap Hamming needs $\Omega(n)$ bits of one-way randomized communication (Woodruff 2004), so the sketch needs $\Omega(n) - O(\log n) = \Omega(\varepsilon^{-2})$ bits.

**To $F_2$.** $\langle f, g \rangle = \frac{1}{4}(F_2(f + g) - F_2(f - g))$, so an $F_2$ sketch of the sum and of the difference of two linear sketches also gives $J$, with error $O(\varepsilon(F_2(f) + F_2(g)))$.

## Applications

- **Query optimization.** Database optimizers choose join orders and algorithms from estimated join sizes. Sketches maintained under inserts and deletes give these estimates without scanning the tables, which was the setting of Alon, Gibbons, Matias and Szegedy.
- **Similarity of streams.** The inner product of two frequency vectors, and through $F_2(f - g)$ their Euclidean distance, compares two traffic streams, two time windows, or two document collections.
- **Correlation and covariance.** For numeric data, inner products of sketched vectors estimate correlations between streams.

## References
