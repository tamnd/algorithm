---
tag: 4WACV7
kind: algorithm
slug: k-nearest-neighbors
name: k-nearest neighbors
aliases:
- k-NN
- KNN
- k-NN classifier
- k-nearest neighbor rule
area: machine-learning/supervised-learning
level: intro
summary: Predict the label of a query by a vote of its k closest training points, or its value by their mean. No training step; Θ(n d) work per query by brute force.
solves: [classification, regression]
model: real-ram
complexity:
  vars: {n: the number of training examples, d: the number of features, k: the number of neighbors}
  time: {worst: "O(n d + n log k)", best: "Θ(n d)"}
  space: {extra: Θ(k)}
properties: {deterministic: true, online: true, exact: true, recursive: false}
history:
  year: 1951
  people: [Evelyn Fix, Joseph L. Hodges]
  note: Fix and Hodges defined the k-nearest neighbor rule in a 1951 report for the USAF School of Aviation Medicine and proved it consistent. Cover and Hart bounded the 1-NN error in 1967.
prereqs: [classification, euclidean-distance]
see_also: [cover-hart-theorem, bayes-optimal-classifier, k-nearest-neighbor-search, kd-tree, ball-tree, curse-of-dimensionality, hubness, voronoi-diagram]
sources:
  - paper: doi:10.2307/1403797
    title: "Evelyn Fix and J. L. Hodges, Discriminatory analysis. Nonparametric discrimination: consistency properties, Report No. 4, Project 21-49-004, USAF School of Aviation Medicine, Randolph Field, Texas, 1951; reprinted in International Statistical Review 57(3), 1989"
    locator: pp. 238 to 247 of the reprint (the k-nearest neighbor rule and its consistency when k grows and k/n goes to 0)
  - paper: doi:10.1109/TIT.1967.1053964
    title: Thomas M. Cover and Peter E. Hart, Nearest neighbor pattern classification, IEEE Transactions on Information Theory 13(1), 1967
    locator: pp. 21 to 27 (the k-NN rule and the bound R* ≤ R ≤ 2R*(1 - R*) for 1-NN)
  - paper: doi:10.1214/aos/1176343886
    title: Charles J. Stone, Consistent nonparametric regression, Annals of Statistics 5(4), 1977
    locator: pp. 595 to 645 (universal consistency of nearest neighbor rules when k → ∞ and k/n → 0)
  - paper: doi:10.1145/355744.355745
    title: Jerome H. Friedman, Jon L. Bentley and Raphael A. Finkel, An algorithm for finding best matches in logarithmic expected time, ACM Transactions on Mathematical Software 3(3), 1977
    locator: the k-d tree search for the k nearest neighbors and its expected logarithmic time
  - paper: "S. A. Dudani, The distance-weighted k-nearest-neighbor rule, IEEE Transactions on Systems, Man, and Cybernetics 6(4), 1976"
    locator: the weighted vote (check the page range)
  - paper: doi:10.1109/TIT.1968.1054155
    title: Peter E. Hart, The condensed nearest neighbor rule, IEEE Transactions on Information Theory 14(3), 1968
    locator: the condensed training subset
  - book: isbn:9780387946184
    title: Luc Devroye, László Györfi and Gábor Lugosi, A Probabilistic Theory of Pattern Recognition, Springer, 1996
    locator: Chapter 5 (nearest neighbor rules), Chapter 6 (Stone's theorem) and Chapter 11 (consistency of the k-NN rule)
  - book: isbn:9780387848570
    title: Trevor Hastie, Robert Tibshirani and Jerome Friedman, The Elements of Statistical Learning, second edition, Springer, 2009
    locator: Section 2.3.2 (nearest neighbor methods), Section 2.5 (local methods in high dimensions) and Section 13.3 (k-nearest-neighbor classifiers)
---

The k-nearest neighbors method (k-NN) predicts the output for a query point $q$ from the $k$ training points closest to $q$: for [classification](/classification/) it returns the most common label among them, and for [regression](/regression/) it returns the mean of their values. It has no training step: the model is the stored data set. A brute force query costs $O(n d + n \log k)$ arithmetic operations in the [real RAM](/real-ram/) model. As $n \to \infty$ the 1-NN error is at most twice the Bayes error (the [Cover-Hart theorem](/cover-hart-theorem/)), and with $k \to \infty$ and $k/n \to 0$ the k-NN rule is consistent for every distribution (Stone 1977).

## In plain words

You want to guess the type of a new item. You keep all the items that you have already seen, with their types. To guess, you find the few stored items that are most similar to the new one, for example the five closest. Each of them votes for its own type, and the type with the most votes wins. To guess a number instead of a type, such as a price, you take the average of the numbers of the close items.

The method makes no assumption about the shape of the boundary between the types. With few neighbors it follows the data closely and also follows the noise. With many neighbors it is smoother but blurs small regions. The number of neighbors is the one setting that you must choose.

## The problem

The data model is supervised learning: the training set $S = ((x_1, y_1), \ldots, (x_n, y_n))$ is drawn i.i.d. from an unknown distribution $D$ on $\mathbb{R}^d \times \mathcal{Y}$. For classification $\mathcal{Y}$ is a finite set of classes and the loss is the 0-1 loss. For regression $\mathcal{Y} = \mathbb{R}$ and the loss is the squared loss. The input of a query is $S$, a query point $q \in \mathbb{R}^d$, the number of neighbors $k$ with $1 \le k \le n$, and a distance $\rho$, by default the [Euclidean distance](/euclidean-distance/). The output is a predicted label or value for $q$.

Here $n$ is the number of training examples, $d$ the number of features, and $k$ the number of neighbors (not the number of classes).

## The algorithm

Order the training points by the key $(\rho(x_i, q), i)$: by distance, and by index when two distances are equal. The neighbor set $N_k(q)$ is the $k$ points with the smallest keys. Each neighbor gets a weight $w(\delta)$, where $\delta$ is its distance: $w = 1$ for the plain vote, or $w = 1/\delta$ for the distance weighted vote.

```pseudo id=main
KNN-PREDICT(S, q, k)
L1  H ← an empty max-heap of pairs (δ, i), ordered by the key (δ, i)
L2  for i ← 1 to n do
L3      δ ← ρ(x_i, q)
L4      if |H| < k then insert (δ, i) into H
L5      else if δ < the distance of the maximum of H then
L6          replace the maximum of H with (δ, i)
L7  N ← the pairs of H, sorted by the key (δ, i)
L8  if regression then return Σ_{(δ,i) ∈ N} w(δ) y_i / Σ_{(δ,i) ∈ N} w(δ)
L9  for each class c do v_c ← Σ_{(δ,i) ∈ N, y_i = c} w(δ)
L10 T ← the classes c with the largest v_c
L11 return the class in T of the first pair of N whose label is in T
```

Line L5 uses a strict $<$. The new index $i$ is larger than each index in $H$, so a point at the same distance as the current maximum has a larger key and does not enter. This makes the neighbor set the $k$ smallest keys, with each distance tie broken by the smaller index. Line L11 breaks a tie in the vote: among the tied classes it picks the one with the nearest member. Other common rules are to choose at random among the tied classes, or to drop the farthest neighbor and vote again. An odd $k$ removes vote ties for two classes in the plain vote.

**Distance weighting.** With $w(\delta) = 1/\delta$, close neighbors count more (Dudani 1976). A neighbor at distance 0 would get an infinite weight, so the implementation gives all the weight, in equal parts, to the neighbors at distance 0.

## Example

Seven training points in $\mathbb{R}^2$ with a class and a numeric target, and the query $q = (3, 2)$:

| $i$ | $x_i$ | class | target | $\rho(x_i, q)$ |
| --- | --- | --- | --- | --- |
| 0 | (1, 1) | A | 2 | $\sqrt5 \approx 2.236$ |
| 1 | (2, 1) | A | 3 | $\sqrt2 \approx 1.414$ |
| 2 | (1, 3) | A | 4 | $\sqrt5 \approx 2.236$ |
| 3 | (4, 2) | B | 6 | 1 |
| 4 | (5, 4) | B | 9 | $\sqrt8 \approx 2.828$ |
| 5 | (3, 4) | B | 7 | 2 |
| 6 | (2, 4) | A | 6 | $\sqrt5 \approx 2.236$ |

The order of the keys is 3, 1, 5, 0, 2, 6, 4. Points 0, 2 and 6 are at the same distance, so the index decides their order.

| $k$ | neighbors | votes A : B | plain vote | weighted vote | mean target |
| --- | --- | --- | --- | --- | --- |
| 1 | 3 | 0 : 1 | B | B | 6 |
| 3 | 3, 1, 5 | 1 : 2 | B | B | 16/3 ≈ 5.333 |
| 4 | 3, 1, 5, 0 | 2 : 2 | B (tie, nearest is B) | B | 4.5 |
| 5 | 3, 1, 5, 0, 2 | 3 : 2 | A | A | 4.4 |

For $k = 5$ the weighted votes are $1/\sqrt2 + 2/\sqrt5 \approx 1.602$ for A and $1 + 1/2 = 1.5$ for B, so A still wins. For $k = 3$ the weighted mean of the targets is $(6 + 3/\sqrt2 + 7/2)/(1 + 1/\sqrt2 + 1/2) \approx 5.265$. The prediction changes with $k$: this is why $k$ is chosen by [cross-validation](/cross-validation/).

## Correctness

The claim is that $N$ at line L7 holds the $k$ training points with the smallest keys $(\rho(x_i, q), i)$, in increasing order of key, and that lines L8 to L11 return the weighted mean or the weighted plurality class of $N$ with the stated tie rule. The heap loop keeps this [loop invariant](/loop-invariant/): before iteration $i$, $H$ holds the $\min(k, i - 1)$ smallest keys among the first $i - 1$ points. When $H$ is full, a new key $(\delta, i)$ is smaller than the maximum key $(\delta_{\max}, j)$ if and only if $\delta < \delta_{\max}$, because $i > j$. So line L5 inserts the new point exactly when it belongs to the new set of $k$ smallest keys, and the replaced maximum is exactly the key that leaves the set. Lines L8 to L11 compute their result from $N$ by definition. The full proof is below.

## Complexity

The model is the [real RAM](/real-ram/), with one unit for each arithmetic operation and comparison on reals.

- **Training.** None. The method stores the $n \times d$ matrix $X$ and the labels, in $\Theta(n d)$ memory.
- **One query, brute force.** Line L3 costs $\Theta(d)$ for the Euclidean distance, so the distances cost $\Theta(n d)$ in total. Each heap operation on at most $k$ items costs $O(\log k)$, so lines L4 to L6 cost $O(n \log k)$ in the worst case. Line L7 sorts $k$ items in $O(k \log k)$, and the vote costs $O(k)$. The total is $O(n d + n \log k)$ in the worst case and $\Theta(n d)$ in the best case, when no replacement happens after the first $k$ points. The extra space is $\Theta(k)$.
- **Linear time selection.** [Quickselect](/quickselect/) on the $n$ distances finds the $k$ smallest in $O(n)$ expected time, so a query costs $\Theta(n d)$ expected time, with $\Theta(n)$ extra space.
- **Many queries.** $m$ queries cost $O(m n d)$ by brute force. Leave-one-out [cross-validation](/cross-validation/) of $k$ costs $O(n^2 d)$.
- **Indexes.** A [k-d tree](/kd-tree/), a [ball tree](/ball-tree/) or a [cover tree](/cover-tree/) answers a [k-nearest neighbor search](/k-nearest-neighbor-search/) much faster than brute force in low dimensions. For a fixed small $d$ and well-spread data, Friedman, Bentley and Finkel (1977) showed a $k$-d tree query takes $O(\log n)$ expected time. The cost of these indexes grows fast with $d$, and above about 20 dimensions they often visit most of the points. Then [locality-sensitive hashing](/locality-sensitive-hashing/) and other [approximate nearest neighbor](/approximate-nearest-neighbor-search/) methods trade exactness for speed.

## Properties

- **Nonparametric and lazy.** The number of stored values grows with $n$, and all the work happens at query time.
- **Decision regions.** For $k = 1$ the decision region of a class is the union of the [Voronoi cells](/voronoi-diagram/) of its training points, so the boundary is piecewise linear. For larger $k$ the regions are unions of cells of the [order-k Voronoi diagram](/order-k-voronoi-diagram/).
- **Training error.** With $k = 1$ and distinct training points, the rule classifies each training point correctly, so the training error is 0 and says nothing about the test error.
- **Bias and variance.** A small $k$ gives low bias and high variance, and a large $k$ the reverse. With $k = n$ the rule predicts the most common class (or the mean target) for every query.
- **Asymptotic error of 1-NN.** For $M$ classes, under the conditions of Cover and Hart, the limit $R$ of the 1-NN error satisfies $R^\ast \le R \le R^\ast(2 - M R^\ast/(M - 1))$, where $R^\ast$ is the [Bayes risk](/bayes-optimal-classifier/). See the [Cover-Hart theorem](/cover-hart-theorem/).
- **Universal consistency.** Stone (1977) proved that if $k = k_n \to \infty$ and $k_n / n \to 0$, the expected error of the k-NN rule on $\mathbb{R}^d$ converges to the Bayes risk $R^\ast$ for every distribution of $(X, Y)$, with distance ties broken at random (Devroye, Györfi and Lugosi, Chapters 6 and 11). The same conditions make k-NN regression consistent in mean square when $\mathbb{E}[Y^2] < \infty$. No rate holds for all distributions: the convergence can be arbitrarily slow.
- **Scale dependent.** The Euclidean distance mixes features in their own units. A feature measured in thousands dominates one measured in units, so standardize the features first, or use a learned metric.

## Variants and improvements

- **Distance weighted k-NN.** Weights $1/\delta$, or a kernel $K(\delta/h)$. With a kernel and a fixed radius instead of a fixed $k$, this becomes the Nadaraya-Watson estimator.
- **Condensed and edited nearest neighbors.** Hart (1968) keeps a subset of the training set that classifies the full set correctly with 1-NN, which shrinks the memory. Editing removes points that their own neighbors misclassify, which removes noise.
- **Metric learning.** Learn a Mahalanobis distance $\rho(x, z) = \sqrt{(x - z)^\top A (x - z)}$, with $A$ positive semidefinite, so that neighbors share labels.
- **Approximate neighbors.** Use [locality-sensitive hashing](/locality-sensitive-hashing/), [HNSW](/hnsw/) or another index that returns points within a factor $c$ of the true distance, at much less cost in high dimensions.
- **Other distances.** Manhattan, [cosine](/cosine-similarity/), Hamming or edit distance. The algorithm only needs $\rho$ to be computable. Fast indexes need $\rho$ to be a [metric](/metric-space/).

## When to use it

Use k-NN as a baseline, when the number of features is small, when the data set fits in memory, and when the classes form local groups with irregular boundaries. Use it when new training data arrives often, since adding a point costs nothing. Avoid it when queries must be fast and $n$ is large without a good index, when the dimension is high and the features are noisy, and when you need a model that explains its decisions with a few parameters.

## Pitfalls

- **Unscaled features.** The distance follows the feature with the largest range. Standardize each feature to mean 0 and variance 1, using statistics from the training set only.
- **The curse of dimensionality.** In the unit cube in $\mathbb{R}^d$, a sub-cube that holds a fraction $r$ of uniform data has edge $r^{1/d}$: for $r = 0.1$ this is 0.316 in 2 dimensions, 0.794 in 10 and 0.977 in 100. So the "nearest" neighbors are not local in high dimensions. Distances also concentrate: for 1000 uniform points in $[0, 1]^d$ and one uniform query (seed 1), the ratio of the largest to the smallest distance was 134.3 for $d = 2$, 4.74 for $d = 10$, 1.46 for $d = 100$ and 1.12 for $d = 1000$. See [curse of dimensionality](/curse-of-dimensionality/) and [hubness](/hubness/).
- **Ties.** An even $k$ with two classes gives vote ties, and data on a grid gives distance ties. State a rule for both, or the result depends on the order of the data.
- **Choosing k on the training error.** The training error of 1-NN is 0. Choose $k$ by cross-validation instead.
- **Class imbalance.** A large class wins most votes when $k$ is large. Weight votes by the inverse class frequency if the costs require it.
- **Leakage in leave-one-out.** When you evaluate on a training point, remove that point from the training set, or 1-NN always finds the point itself.

## Implementations

## History

Evelyn Fix and Joseph Hodges defined the k-nearest neighbor rule in a 1951 technical report for the USAF School of Aviation Medicine, as a nonparametric discrimination method, and proved that it is consistent when $k \to \infty$ and $k/n \to 0$ under continuity conditions on the densities. The report was reprinted in the International Statistical Review in 1989. Thomas Cover and Peter Hart proved in 1967 that the asymptotic 1-NN error is at most twice the Bayes error. Charles Stone proved in 1977 that the k-NN rule is consistent for every distribution, with no density assumption. Friedman, Bentley and Finkel gave the expected logarithmic query time of the $k$-d tree for nearest neighbor search in 1977.

## References
