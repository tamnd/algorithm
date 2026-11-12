---
tag: V3K4X6
kind: algorithm
slug: k-means-plus-plus
name: k-means++ seeding
aliases:
- D^2 seeding
- k-means++
- D-squared sampling
area: machine-learning/clustering
level: core
summary: Randomized seeding that picks each new center with probability proportional to its squared distance to the existing centers.
solves: [k-means-problem]
model: real-ram
complexity:
  vars: {n: the number of points, d: the dimension, k: the number of clusters}
  time: {expected: "O(n k d)"}
  space: {extra: "O(n)"}
properties: {deterministic: false, exact: false, online: false, recursive: false}
history:
  year: 2007
  people: [David Arthur, Sergei Vassilvitskii]
  note: Arthur and Vassilvitskii proved the O(log k) bound in expectation. Ostrovsky, Rabani, Schulman and Swamy studied a similar seeding in 2006.
prereqs: [k-means, weighted-sampling]
see_also: [k-means-plus-plus-guarantee, k-means, k-means-problem, k-median-problem, mini-batch-k-means, coreset, randomized-algorithm]
sources:
  - paper: "David Arthur and Sergei Vassilvitskii, k-means++: the advantages of careful seeding, Proceedings of the 18th Annual ACM-SIAM Symposium on Discrete Algorithms (SODA), 2007, pages 1027 to 1035"
    locator: Section 2.2 (the k-means++ algorithm, steps 1a to 1c), Theorem 3.1 (the 8(ln k + 2) bound), Section 4 (the matching lower bound), Section 5 (D^l seeding)
  - paper: "Rafail Ostrovsky, Yuval Rabani, Leonard J. Schulman and Chaitanya Swamy, The effectiveness of Lloyd-type methods for the k-means problem, 47th IEEE Symposium on Foundations of Computer Science (FOCS), 2006, pages 165 to 176"
    locator: the seeding by squared distances for well separated inputs
  - paper: "Bahman Bahmani, Benjamin Moseley, Andrea Vattani, Ravi Kumar and Sergei Vassilvitskii, Scalable k-means++, Proceedings of the VLDB Endowment 5(7), 2012, pages 622 to 633"
    locator: the k-means|| oversampling seeding
  - paper: "Silvio Lattanzi and Christian Sohler, A better k-means++ algorithm via local search, Proceedings of the 36th International Conference on Machine Learning (ICML), PMLR 97, 2019, pages 3662 to 3671"
    locator: the local search after D^2 seeding with a constant factor in expectation
  - book: isbn:9780262046824
    title: Kevin P. Murphy, Probabilistic Machine Learning, An Introduction, MIT Press, 2022
    locator: Section 21.3 (K-means clustering, the initialization of the centers)
---

k-means++ is a randomized method that chooses the initial centers for the [k-means algorithm](/k-means/). It takes the first center uniformly from the data, and each further center from the data with probability proportional to its squared distance to the nearest center chosen so far. Arthur and Vassilvitskii (2007) proved that the seeds alone have an expected [k-means cost](/k-means-problem/) of at most $8(\ln k + 2)$ times the optimum, and that the factor $\Theta(\log k)$ is the best possible for this seeding. The seeding costs $O(nkd)$ time, the same as one iteration of Lloyd's algorithm.

## In plain words

Lloyd's method for k-means can get stuck when two first guesses fall in the same group. k-means++ is a better way to make the first guesses. Pick the first one at random from the data. For each next one, look at how far each data point is from the nearest guess so far. A point that is far away gets a high chance to be the next guess, and a point that is already near a guess gets a low chance. A point that is already a guess gets no chance.

So the guesses spread out over the groups. They are still random, which protects the method from a few odd points far away. After the guesses are made, the usual k-means steps improve them.

## The problem

The input is a list of points $x_1, \ldots, x_n \in \mathbb{R}^d$ with the Euclidean norm, a number $k$ with $1 \le k \le n$, and a source of random numbers. The output is $k$ data points $c_1, \ldots, c_k$, used as the initial centers of the [k-means algorithm](/k-means/). For a set $C$ of centers let $D(x) = \min_{c \in C} \|x - c\|$ and $\phi(C) = \sum_i D(x_i)^2$. The goal is a small expected value of $\phi$, compared with the optimum $\phi_{\mathrm{OPT}}$ of the [k-means problem](/k-means-problem/). This is a randomized approximation, and the guarantee is on the expected cost.

## The algorithm

```pseudo id=main
KMEANS++(x_1..x_n, k)
L1  c_1 ← x_m, with m uniform in {1, ..., n}
L2  D_i ← ‖x_i − c_1‖² for each i
L3  for j ← 2 to k do
L4      S ← Σ_i D_i
L5      take index m with probability D_m / S
L6      c_j ← x_m
L7      for i ← 1 to n do
L8          D_i ← min(D_i, ‖x_i − c_j‖²)
L9  run LLOYD from c_1, ..., c_k
```

The array $D$ holds the squared distance of each point to its nearest center so far. Line L8 updates it with the new center only, so each round costs $O(nd)$. Line L5 is one draw from a discrete distribution; a scan of the prefix sums with one uniform random number is enough, because each round draws once. See [weighted sampling](/weighted-sampling/). A point that is already a center has $D_m = 0$, so it is never drawn again. If $S = 0$, all points coincide with centers; then any point that is not chosen will do.

Lines L1 to L8 are the seeding of the paper. Line L9 is the second phase, and it only lowers the cost, so the bound of the seeding holds for the final result too.

## Example

Take the four points $0, 1, 6, 7$ on a line, with $k = 2$. The best clusters are $\{0, 1\}$ and $\{6, 7\}$, with cost $\phi_{\mathrm{OPT}} = 1/2 + 1/2 = 1$.

Suppose line L1 picks $c_1 = 0$. Then $D = (0, 1, 36, 49)$ and $S = 86$, so line L5 picks the point $1$, $6$ or $7$ with probability $1/86$, $36/86$ or $49/86$. With probability $85/86$ the second center is in the other natural cluster.

| first center | $D$ | $S$ | probability that the second center is in the other cluster |
|---|---|---|---|
| 0 | (0, 1, 36, 49) | 86 | 85/86 |
| 1 | (1, 0, 25, 36) | 62 | 61/62 |
| 6 | (36, 25, 0, 1) | 62 | 61/62 |
| 7 | (49, 36, 1, 0) | 86 | 85/86 |

When the two seeds are in different clusters the cost is 2, and when they are in the same cluster it is 61. Over all 12 ordered outcomes the exact expected cost of the seeds is $7515/2666 \approx 2.82$, below the bound $8(\ln 2 + 2) \approx 21.5$. Two distinct data points chosen uniformly give an expected cost of $65/3 \approx 21.7$, because with probability $1/3$ both seeds land in the same cluster.

## Correctness

The seeding always returns $k$ distinct data points when the points are distinct, because a chosen point has weight 0. The final result is a fixed point of Lloyd's algorithm, whose cost is at most the cost of the seeds; see [k-means](/k-means/).

The quality claim is the [k-means++ guarantee](/k-means-plus-plus-guarantee/): for every input, the centers $C$ after line L8 satisfy
$$\mathbb{E}[\phi(C)] \le 8(\ln k + 2) \, \phi_{\mathrm{OPT}} .$$
The proof has three steps. A center chosen uniformly from an optimal cluster $A$ has expected cost $2\phi_{\mathrm{OPT}}(A)$ on $A$, by the centroid identity. A center chosen by $D^2$ weights from $A$ has expected cost at most $8\phi_{\mathrm{OPT}}(A)$ on $A$, by the [triangle inequality](/triangle-inequality/) and the power mean inequality. An induction on the number of optimal clusters not yet hit then gives the harmonic number $H_{k-1} \le 1 + \ln k$. The theorem page has the full proof and the matching $\Omega(\log k)$ lower bound.

## Complexity

**Time.** Line L2 costs $O(nd)$. Each of the $k - 1$ rounds of lines L4 to L8 costs $O(n)$ for the sum and the draw and $O(nd)$ for the update. The total is $\Theta(nkd)$ in every run, which is the cost of one iteration of Lloyd's algorithm. Line L9 then costs whatever Lloyd's algorithm costs.

**Space.** The array $D$ takes $O(n)$ numbers beyond the input, and the centers take $O(kd)$.

**Passes.** The seeding needs $k$ passes over the data, one per center, and they cannot run in parallel. This is slow when $k$ is large and the data is on many machines; k-means|| below fixes this.

## Properties

- **Randomized.** The result depends on the random numbers. The guarantee holds in expectation, so a single run can be bad; Markov's inequality gives cost at most $16(\ln k + 2)\phi_{\mathrm{OPT}}$ with probability at least $1/2$.
- **The bound is on the seeds.** The $O(\log k)$ factor holds before Lloyd's algorithm, which can only improve it.
- **Tight up to a constant.** Arthur and Vassilvitskii give inputs on which the expected cost of the seeds is at least $2 \ln k \cdot \phi_{\mathrm{OPT}}$, up to lower order terms.
- **Less greedy than the farthest point rule.** The choice is random, so one far outlier does not always become a center.
- **Data points as centers.** The seeds are data points, so the method also works for any distance if the analysis is not needed.

## Variants and improvements

- **Greedy k-means++.** In each round draw several candidates and keep the one that lowers $\phi$ the most. Arthur and Vassilvitskii suggest $2 + \ln k$ candidates, and scikit-learn uses this number. The $O(\log k)$ proof does not cover this variant.
- **$D^\ell$ seeding.** Weights $D(x)^\ell$ give an expected factor $2^{2\ell}(\ln k + 2)$ for the cost $\sum D(x)^\ell$. With $\ell = 1$ this is a seeding for the [k-median problem](/k-median-problem/).
- **k-means||.** Bahmani and others (2012) draw about $\ell = \Theta(k)$ points per round, in $O(\log n)$ rounds, and then reduce them to $k$ centers by weighted k-means++. Each round is one parallel pass.
- **Local search after seeding.** Lattanzi and Sohler (2019) add $O(k \log \log k)$ steps that each sample a point by $D^2$ weights and swap it with a center when the cost falls. This gives a constant factor in expectation.
- **Bicriteria seeding.** Drawing $O(k)$ centers by $D^2$ weights gives a constant factor with respect to the optimum with $k$ centers (Aggarwal, Deshpande and Kannan, 2009). The extra centers are then merged.
- **Fast sampling.** Markov chain sampling and tree-based structures draw a $D^2$ sample without a full pass over the data.

## When to use it

Use it as the default initialization of the [k-means algorithm](/k-means/). It costs about one Lloyd iteration, it usually lowers both the final cost and the number of iterations, and it is the default in scikit-learn, MATLAB and R packages. Use k-means|| for large $k$ on distributed data, and [mini-batch k-means](/mini-batch-k-means/) or a [coreset](/coreset/) when one pass over the data is already expensive.

## Pitfalls

- **One run is not enough.** The bound is in expectation. Run the seeding and Lloyd's algorithm several times and keep the best result.
- **Outliers.** A far point has a large $D^2$ weight and is often chosen. If the data has outliers, remove them first or use a robust variant.
- **Duplicates.** When many points coincide, $S$ can become 0 before $k$ centers exist. The code must handle this case, for example by taking any point that is not chosen.
- **Floating point.** A draw by prefix sums can, by rounding, select an index past the last positive weight. Restrict the result to points with $D_m > 0$.
- **The farthest point rule is not k-means++.** Taking the farthest point at each step is the greedy rule for the [k-center problem](/k-center-problem/). For k-means it is sensitive to outliers and has no $O(\log k)$ guarantee.

## Implementations

## History

Arthur and Vassilvitskii presented k-means++ at SODA 2007, with the $8(\ln k + 2)$ bound and the $\Omega(\log k)$ lower bound. In 2006 Ostrovsky, Rabani, Schulman and Swamy had analysed a similar seeding and proved a constant factor when the data is well separated. Later work made the seeding parallel (k-means||, 2012), faster to sample, and, with a short local search, a constant factor approximation in expectation (Lattanzi and Sohler, 2019).

## References
