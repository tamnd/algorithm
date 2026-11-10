---
tag: J7WGQD
kind: concept
slug: linear-sketch
name: Linear sketch
aliases:
- linear projection sketch
- linear summary
- sketching matrix
area: online-and-streaming/streaming-sketches
level: core
summary: A summary that is a linear function of the frequency vector, so updates add and deletions subtract.
prereqs: [turnstile-model, frequency-vector, k-wise-independent-hashing]
see_also: [mergeable-summaries, count-min-sketch, count-sketch, ams-sketch, indyk-p-stable-sketch, l0-sampler, agm-graph-sketch, hyperloglog]
sources:
  - paper: doi:10.1145/2591796.2591812
    title: Yi Li, Huy L. Nguyen and David P. Woodruff, Turnstile streaming algorithms might as well be linear sketches, STOC 2014
    locator: pp. 174 to 183 (the main theorem and its conditions)
  - paper: doi:10.1145/3357713.3384278
    title: John Kallaugher and Eric Price, Separations and equivalences between turnstile streaming and linear sketching, STOC 2020
    locator: pp. 1223 to 1236
  - paper: doi:10.1561/0400000060
    title: David P. Woodruff, Sketching as a tool for numerical linear algebra, Foundations and Trends in Theoretical Computer Science 10(1 and 2), 2014
    locator: pp. 1 to 157, Chapter 1 (sketching matrices and subspace embeddings)
  - paper: doi:10.1016/j.jalgor.2003.12.001
    title: Graham Cormode and S. Muthukrishnan, An improved data stream summary, the count-min sketch and its applications, Journal of Algorithms 55(1), 2005
    locator: pp. 58 to 75
  - paper: doi:10.1016/S0304-3975(03)00400-6
    title: Moses Charikar, Kevin Chen and Martin Farach-Colton, Finding frequent items in data streams, Theoretical Computer Science 312(1), 2004
    locator: pp. 3 to 15
---

A linear sketch of a stream is the vector $Sf$, where $f \in \mathbb{Z}^n$ is the [frequency vector](/frequency-vector/) and $S$ is a random $k \times n$ matrix with $k \ll n$. The algorithm never stores $S$: it stores a short seed from which each column of $S$ can be computed, and the $k$ entries of $Sf$. Because $S(f + g) = Sf + Sg$, an update $(i, \Delta)$ just adds $\Delta$ times column $i$, deletions are updates with $\Delta < 0$, and the sketches of two streams add up to the sketch of the combined stream. So linear sketches work in the general [turnstile model](/turnstile-model/) and are [mergeable](/mergeable-summaries/) by addition. Li, Nguyen and Woodruff (2014) showed that, under some conditions, every turnstile streaming algorithm can be turned into a linear sketch. On this page $n$ is the universe size and $k$ is the number of rows.

## In plain words

Think of a few running totals, each a weighted sum of all the item counts. Each item has its own fixed weight in each total, chosen at random before the stream starts. When an item arrives, you add its weights to the totals. When an item is removed, you take them away again. The order of the arrivals and the removals does not matter, because addition does not care about order. Two machines that keep the same kind of totals, with the same weights, can add their totals together to get the totals for all their data. A good choice of weights lets you read off useful facts from the few totals, such as which items are frequent, or how many items there are.

## The idea

**Definition.** A linear sketch is a pair: a distribution over matrices $S \in R^{k \times n}$, over the integers, the reals or $\mathbb{Z}_q$, and a query map $D$ that turns $Sf$ into an answer. The algorithm draws $S$ before the stream, keeps $y = Sf$, and answers $D(y)$.

- **Update.** For an update $(i, \Delta)$, $y \leftarrow y + \Delta\, S e_i$. If column $i$ has $d$ nonzero entries, as in the [count-min sketch](/count-min-sketch/), an update costs $O(d)$ time.
- **Space.** $k$ counters, each of $O(\log(nM))$ bits when the entries of $S$ and $f$ are integers of size $\mathrm{poly}(n)$ and $|f_i| \le M$, plus the seed. The columns come from [k-wise independent hash functions](/k-wise-independent-hashing/), so the seed has $O(\log n)$ bits per hash function, not $kn$ entries.
- **Query.** $D(y)$, for example a minimum, a median or an average over rows.

**Why linearity gives turnstile streams and merges (proved here).** Let a stream $\sigma$ have updates $(i_1, \Delta_1), \ldots, (i_m, \Delta_m)$, and let $y$ start at 0. After the updates, $y = \sum_j \Delta_j S e_{i_j} = S \sum_j \Delta_j e_{i_j} = Sf$, by linearity of the product, for any order and any signs of the $\Delta_j$. If $\sigma_1$ and $\sigma_2$ are processed with the same $S$, giving $y_1 = Sf_1$ and $y_2 = Sf_2$, then $y_1 + y_2 = S(f_1 + f_2)$, which is the sketch of the concatenation, and $y_1 - y_2 = S(f_1 - f_2)$ is the sketch of the difference. $\square$

**The theorem of Li, Nguyen and Woodruff (cited).** Consider a one-pass algorithm in the turnstile model that computes a function of $f \in \{-M, \ldots, M\}^n$, correct with constant probability for each stream. Then there is an algorithm that draws $A$ uniformly from a fixed set of $O(n \log M)$ integer matrices, with entries of size $\mathrm{poly}(n)$, keeps $Af$ (with its entries reduced modulo fixed integers), and computes the same function with about the same space. The conditions matter.

- The original algorithm must be correct on streams of any length, also when the counts in the middle of the stream are much larger than $M$.
- The new algorithm is non-uniform: the set of matrices exists, but the proof does not say how to compute it efficiently.

Kallaugher and Price (2020) showed that when the stream length is bounded, or the counts in the middle are bounded, there are problems where turnstile algorithms use much less space than any linear sketch, and they also gave conditions under which the equivalence still holds. So lower bounds for linear sketches are lower bounds for turnstile streaming only under the conditions of the theorem.

**What is not linear.** [HyperLogLog](/hyperloglog/) keeps maxima, the [KMV sketch](/kmv-sketch/) keeps the smallest hash values, and the [Misra-Gries summary](/misra-gries-summary/) keeps a few items with counters. These merge, but by a maximum or a combine step, not by a sum, and they cannot undo a deletion.

## Examples

All examples use the universe $\{a, b, c, d\}$, the stream $f = (3, 2, 1, 0)$ of the [frequency vector](/frequency-vector/) page, and a second stream $g = (0, 1, 0, 2)$.

**One row of count-min.** Let the hash map $a, c \mapsto 0$ and $b, d \mapsto 1$. Then
$$S = \begin{pmatrix} 1 & 0 & 1 & 0 \\ 0 & 1 & 0 & 1 \end{pmatrix}, \qquad Sf = (4, 2), \qquad Sg = (0, 3), \qquad S(f + g) = (4, 5) = Sf + Sg.$$
The point query for $a$ reads the bucket of $a$: 4 for $f$, against $f_a = 3$; the extra 1 is $f_c$, which shares the bucket. The deletion $(a, -1)$ changes $Sf$ to $(3, 2)$, as the sketch of $(2, 2, 1, 0)$ must be.

**One AMS estimator.** Let the signs be $s = (+1, +1, -1, +1)$. Then $Z = \langle s, f \rangle = 3 + 2 - 1 + 0 = 4$ and $Z^2 = 16$. Over 4-wise independent random signs, $\mathbb{E}[Z^2] = F_2 = 14$. The [AMS sketch](/ams-sketch/) keeps many such rows and combines them by the [median trick](/median-trick/).

**Other linear sketches.**

- The [count sketch](/count-sketch/): one $\pm 1$ entry per column in each row, with point queries within $\varepsilon\|f\|_2$.
- The [p-stable sketch](/indyk-p-stable-sketch/) of Indyk: entries drawn from a [p-stable distribution](/p-stable-distribution/), for $\|f\|_p$ with $0 < p \le 2$.
- A Gaussian matrix with $k = O(\varepsilon^{-2}\log(1/\delta))$ rows: $\|Sf\|_2/\sqrt k$ is within $1 \pm \varepsilon$ of $\|f\|_2$ with probability $1 - \delta$, the Johnson-Lindenstrauss lemma.
- The fingerprint $\sum_i f_i z^i \bmod p$, a one-row sketch over $\mathbb{Z}_p$ that tests $f = 0$ (proved on the [turnstile model](/turnstile-model/) page).
- The [L0 sampler](/l0-sampler/) and the [AGM sketch](/agm-graph-sketch/), which find nonzero entries and graph connectivity under deletions.

## Where it is used

- **Turnstile streams.** Nearly all known turnstile algorithms are linear sketches, which the theorem above explains.
- **Distributed data.** Each site sketches its part with the same seed, and a coordinator adds the sketches. The difference of two sketches compares two data sets, for example two days of network traffic.
- **Databases.** Sketches of the frequency vectors of two relations estimate the size of their join, $\langle f, g \rangle$; see [join size estimation](/join-size-estimation-problem/).
- **Compressed sensing and sparse recovery.** Recovering a sparse $f$ from $Sf$ is the same task, studied with other goals.
- **Numerical linear algebra.** Random sketching matrices reduce the size of regression and low rank problems (Woodruff 2014).
- **Lower bounds.** A lower bound for linear sketches, proved with linear algebra or communication complexity, is a lower bound for turnstile streaming under the conditions of the theorem of Li, Nguyen and Woodruff.

## References
