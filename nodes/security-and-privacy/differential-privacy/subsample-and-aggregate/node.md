---
tag: 5N4WXQ
kind: technique
slug: subsample-and-aggregate
name: Subsample and aggregate
aliases:
- sample and aggregate
area: security-and-privacy/differential-privacy
level: advanced
summary: Runs a non-private estimator on disjoint blocks of the data and combines the results with a private aggregator.
prereqs: [laplace-mechanism, global-sensitivity]
see_also: [pate, smooth-sensitivity, propose-test-release, parallel-composition-theorem, median, trimmed-mean, report-noisy-max, exponential-mechanism]
sources:
  - paper: "Kobbi Nissim, Sofya Raskhodnikova and Adam Smith, Smooth sensitivity and sampling in private data analysis, ACM STOC 2007, pages 75 to 84"
    locator: the sample and aggregate framework, with an aggregator of low smooth sensitivity, and its use for k-means cluster centers and mixtures of Gaussians
  - url: "https://doi.org/10.1145/1993636.1993743"
    title: "Adam Smith, Privacy-preserving statistical estimation with optimal convergence rates, ACM STOC 2011, pages 813 to 822"
    locator: the private estimator built from block estimates and a private Winsorized mean, and its asymptotic efficiency for estimators with a normal limit
---

Subsample and aggregate turns almost any estimator into a differentially private one, without a sensitivity analysis of the estimator. Split the data into $k$ disjoint blocks, run the estimator on each block, and combine the $k$ results with a private aggregator. Changing one record changes only the block that holds it, and so only one of the $k$ results. The aggregator must therefore be private with respect to a change of one of its $k$ inputs, which is a much easier task than bounding the sensitivity of the estimator. Nissim, Raskhodnikova and Smith introduced it in 2007, and Smith (2011) showed that for a large class of estimators it loses nothing in the limit of large data. [PATE](/pate/) is the best-known use in machine learning.

## In plain words

Suppose you want a private answer from a complex computation, such as a regression fit, a clustering or a trained model, and you do not know how much one person can change its output. Cut the data into many groups so that each person is in exactly one group. Run the computation on each group on its own. You now have many answers, and one person can change only one of them. Combine them in a way that one answer cannot move much: clip each answer to a known range and average, or take a private median, then add noise scaled to what one answer can do. The noise shrinks as the number of groups grows, but each group gets less data. When the computation gives stable answers on smaller samples, this works well.

## When it applies

Use it when all of these hold.

- **A black box estimator.** The function $f$ has no useful bound on its [global sensitivity](/global-sensitivity/), or the bound is too hard to find, but $f$ can be run on any subset of the data.
- **Stable on subsamples.** On a block of $n/k$ records, $f$ gives an answer close to its answer on the full data, with high probability. Means, regression coefficients, quantiles and cluster centers on well-separated clusters behave this way; the maximum of the data or a rule fitted to a single rare record do not.
- **A known output range.** For the average aggregator, a range $[a, b]$ that contains the useful answers must be fixed before the data is seen. Aggregators based on the median or on votes can work without it.
- **Enough data.** The number of blocks $k$ must be large enough for the aggregator noise to be small, and each block of $n/k$ records must still be large enough for $f$ to work. So $n$ must be large compared with the size that $f$ needs.

## The template

```pseudo id=main
SUBSAMPLE-AND-AGGREGATE(D, k, ε)      ▷ holes: PARTITION, ESTIMATOR, RANGE [a, b], AGGREGATOR
L1  B_1, ..., B_k ← PARTITION(D, k)             ▷ disjoint blocks, chosen without looking at the values
L2  for j = 1 to k do
L3      z_j ← ESTIMATOR(B_j)                     ▷ any non-private estimator
L4      z_j ← min(max(z_j, a), b)                ▷ clamp to the public RANGE
L5  return AGGREGATOR(z_1, ..., z_k, ε)           ▷ ε-DP when one z_j changes
```

The holes are filled as follows.

- **PARTITION** puts each record in exactly one block. Under the replace relation with $n$ known, blocks by position ($i \bmod k$) or by a random permutation drawn independently of the data both work: replacing record $i$ changes the block of record $i$ only.
- **ESTIMATOR** is the non-private $f$. Its own randomness, if any, is fresh for each block.
- **RANGE** is the public interval $[a, b]$, or a box in $\mathbb R^d$.
- **AGGREGATOR** is any $\varepsilon$-DP algorithm on $k$ inputs in $[a, b]$, where two input vectors are neighbors if they differ in one entry. The simplest one is the clamped mean with [Laplace noise](/laplace-mechanism/): $\frac1k\sum_j z_j + \mathrm{Lap}\!\left(\frac{b - a}{k\varepsilon}\right)$. Changing one $z_j$ inside $[a, b]$ moves the mean by at most $(b - a)/k$, which is the sensitivity.

**Why it is private.** Let $D$ and $D'$ differ in one record. By L1 they give the same blocks except one, say $B_j$. Then $z_i = z'_i$ for all $i \ne j$, and the vectors $z$ and $z'$ are neighbors for the aggregator. L5 is $\varepsilon$-DP for such neighbors, so the whole algorithm is $\varepsilon$-DP. This is the argument of [parallel composition](/parallel-composition-theorem/): the estimator itself never needs a privacy proof.

**A walk-through.** Take $k = 10$ blocks, the range $[0, 10]$ and $\varepsilon = 1$. Suppose the block estimates are 4.8, 5.1, 5.0, 4.9, 5.3, 5.2, 4.7, 5.0, 5.1 and 12.0, where the last block holds a few extreme records. L4 clamps 12.0 to 10. The mean is $55.1/10 = 5.51$, and the sensitivity is $(10 - 0)/10 = 1$, so the output is $5.51 + \mathrm{Lap}(1)$, with a noise standard deviation of $\sqrt 2 = 1.414$. If one record moves block 3 from 5.0 to any value in $[0, 10]$, the mean moves by at most 1, which the noise covers. With $k = 100$ blocks of a ten times larger data set, the noise scale would be $0.1$. The clamped mean is pulled by the one extreme block (the other nine have the mean 5.01); a median or a [trimmed mean](/trimmed-mean/) as the aggregator would not be.

**How to choose $k$.** Suppose each block estimate has bias $\beta$ and variance $s^2 k/n$, as for an estimator with variance $s^2/m$ on $m = n/k$ records, and no estimate is clamped. Then the private output has the mean squared error

$$\beta^2 + \frac{s^2}{n} + \frac{2(b - a)^2}{k^2\varepsilon^2}.$$

The averaging recovers the variance $s^2/n$ of the full data, and more blocks shrink the noise term. The bias does not average out, and for many estimators it grows as the blocks get smaller, which limits $k$.

## Classic examples

- **PATE.** The blocks are disjoint parts of the private training data, the estimator trains a classifier, and the aggregator is [report noisy max](/report-noisy-max/) on the vote counts of the $k$ teachers for each public query. One private example moves at most one vote. See [PATE](/pate/).
- **The median as the aggregator.** Nissim, Raskhodnikova and Smith combined the block outputs with an aggregator of low [smooth sensitivity](/smooth-sensitivity/); for real outputs the [median](/median/) of the $k$ values is the natural choice, and it ignores a minority of bad blocks. A private median can also come from the [exponential mechanism](/exponential-mechanism/) with the rank as the score.
- **Cluster centers.** Nissim, Raskhodnikova and Smith used the framework for the centers of [k-means](/k-means/) and for learning [mixtures of Gaussians](/gaussian-mixture-model/): each block gives a set of centers, and the aggregator finds a point near which many block outputs lie.
- **Efficient statistical estimation.** Smith (2011) used block estimates and a private Winsorized mean, close to a [trimmed mean](/trimmed-mean/), and showed that for estimators with a normal limit, such as the maximum likelihood estimator in regular models, the private estimator has the same limit law. So privacy costs nothing in the first order as $n$ grows.
- **The clamped mean.** The walk-through above, with the [Laplace mechanism](/laplace-mechanism/), is the simplest case and is often enough for a scalar statistic with a known range.

## Variations

- **Vector outputs.** For $z_j \in [a, b]^d$, the $\ell_1$ sensitivity of the mean is $d(b - a)/k$ and the $\ell_2$ sensitivity is $\sqrt d\,(b - a)/k$, so Gaussian noise often does better than Laplace noise in high dimension.
- **Votes on discrete outputs.** When $f$ outputs a label, a set of selected features or a model class, count the votes for each output and release the winner with report noisy max or the exponential mechanism.
- **Stability tests.** If most blocks agree on the same output, the mode is stable: replacing a few blocks does not change it. [Propose-test-release](/propose-test-release/) can test this privately and then release the mode with no noise, at a cost in $\delta$.
- **Bias correction.** Smaller blocks make a larger bias, and the average of the blocks keeps it. A correction of each block estimate before the aggregation, such as the jackknife, reduces it at the cost of more computation per block.

## Pitfalls

- **A partition that depends on the data.** Blocks by sorted order, by a clustering of the data, or by position under the add or remove relation (where removing one record shifts every later record to another block) break the argument. Fix the partition with public information, for example a hash of a record identifier or a permutation of the known index set.
- **A range set from the data.** Taking $[a, b]$ as the smallest and largest block estimate leaks them. The range must be public, or set by a separate private step that uses part of the budget.
- **One person in many records.** If a user owns several records, they may fall into several blocks and change several $z_j$. Partition by user, not by record.
- **Too many blocks.** When the blocks are small, the estimator may fail or be badly biased: a regression with $p$ coefficients needs well over $p$ records per block, and a classifier trained on very little data votes almost at random. The noise is then small but the answer is wrong.
- **Repeated queries.** Each run of the aggregator on the same blocks uses budget; $T$ runs give $T\varepsilon$ by [sequential composition](/sequential-composition-theorem/), as in PATE with many public queries.
- **Clamping bias.** If the true value lies near an end of $[a, b]$, many block estimates are clamped and the mean is biased toward the inside of the range.

## Exercises

1. Show that the clamped mean $\frac1k\sum_j \min(\max(z_j, a), b)$ has global sensitivity exactly $(b - a)/k$ with respect to changing one $z_j$, and give two inputs that reach it.
2. Let the blocks be $B_j = \{x_i : i \equiv j \pmod k\}$. Show that under the add or remove relation, removing $x_1$ can change every block. Then give a partition that changes one block only.
3. In the error formula above, let the bias be $\beta = c\,k/n$, as for an estimator with bias $c/m$ on $m$ records. Show that the error is smallest at $k = 2^{1/4}\sqrt{(b - a)\,n/(c\,\varepsilon)}$.
4. For each point $y$ of a finite grid in $[a, b]$, let the score be $u(z, y) = -\left|\#\{j : z_j \le y\} - k/2\right|$. Show that changing one $z_j$ changes each score by at most 1, so that the exponential mechanism with the weights $e^{\varepsilon u(z, y)/2}$ is $\varepsilon$-DP. Explain why this private median, unlike the mean, needs no clamping of the $z_j$.

## References
