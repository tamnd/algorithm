---
tag: YQJKEX
kind: algorithm
slug: fuzzy-c-means
name: Fuzzy c-means
aliases:
- fuzzy k-means
- FCM
- Bezdek's fuzzy c-means
area: machine-learning/clustering
level: advanced
summary: Soft clustering in which each point has a graded membership in every cluster.
model: real-ram
complexity:
  vars: {n: the number of points, d: the dimension, c: the number of clusters, t: the number of passes}
  time: {worst: "O(t n c (d + c))"}
  space: {extra: "O(n c + c d)"}
properties: {online: false, deterministic: true, recursive: false}
history:
  year: 1973
  people: [Joseph C. Dunn, James C. Bezdek]
  note: Dunn gave the fuzzy objective with exponent 2 in 1973, and Bezdek generalized it to any fuzzifier m > 1 and studied its convergence from 1973 to 1981.
prereqs: [k-means, hard-and-soft-clustering, lagrange-multiplier]
see_also: [k-means-problem, gaussian-mixture-model, expectation-maximization, convex-function, k-means-plus-plus, silhouette-coefficient, clustering-problem]
sources:
  - paper: "J. C. Dunn, A fuzzy relative of the ISODATA process and its use in detecting compact well-separated clusters, Journal of Cybernetics 3(3):32-57, 1973, doi:10.1080/01969727308546046"
    title: Dunn 1973
    locator: the fuzzy objective with exponent 2 and its alternating minimization
  - book: isbn:9780306406713
    title: "James C. Bezdek, Pattern Recognition with Fuzzy Objective Function Algorithms, Plenum Press, 1981"
    locator: Chapter 3 (the fuzzy c-means objective J_m, the update formulas and the algorithm)
  - paper: "J. C. Bezdek, A convergence theorem for the fuzzy ISODATA clustering algorithms, IEEE Transactions on Pattern Analysis and Machine Intelligence 2(1):1-8, 1980, doi:10.1109/TPAMI.1980.4766964"
    title: Bezdek 1980
    locator: convergence of the iterates to fixed points by Zangwill's theorem
  - paper: "J. C. Bezdek, R. J. Hathaway, M. J. Sabin and W. T. Tucker, Convergence theory for fuzzy c-means: counterexamples and repairs, IEEE Transactions on Systems, Man, and Cybernetics 17(5):873-877, 1987"
    title: Bezdek, Hathaway, Sabin and Tucker 1987
    locator: fixed points that are saddle points rather than local minima
---

Fuzzy c-means is a soft version of [k-means](/k-means/). Each point $x_i$ has a membership $u_{ij} \in [0, 1]$ in each of the $c$ clusters, and the memberships of a point add up to 1. The algorithm minimizes the weighted sum of squared distances $J_m = \sum_i \sum_j u_{ij}^m \|x_i - v_j\|^2$, where $m > 1$ is the fuzzifier. Like Lloyd's algorithm, it alternates two exact steps: the best memberships for fixed centers, and the best centers for fixed memberships. So the objective never increases. Dunn gave the method with $m = 2$ in 1973, and Bezdek developed it for all $m > 1$.

## In plain words

In k-means, each point belongs to exactly one group. In fuzzy c-means, a point can belong a little to every group. A point in the middle between two groups belongs half to each. A point next to the center of one group belongs almost fully to it.

The method repeats two steps. First, each point shares its membership among the groups: a near center gets a large share and a far center gets a small share. Second, each center moves to a weighted middle of all points, where points with a large share count more.

One number controls how soft the groups are. When it is close to 1, the shares are almost all or nothing, and the method acts like k-means. When it is large, every point belongs about equally to all groups.

## The problem

The input is a list of $n$ points $x_1, \ldots, x_n$ in $\mathbb{R}^d$, a number $c \ge 2$ of clusters and a fuzzifier $m > 1$. The output is a membership matrix $U$ with $u_{ij} \ge 0$ and $\sum_j u_{ij} = 1$ for each $i$, and centers $v_1, \ldots, v_c$, that make

$$J_m(U, V) = \sum_{i=1}^{n} \sum_{j=1}^{c} u_{ij}^m \, \|x_i - v_j\|^2$$

small. Without the exponent $m$, that is with $m = 1$, the best $U$ puts each point fully in its nearest cluster, and the problem is the [k-means problem](/k-means-problem/). The exponent $m > 1$ makes shared membership pay off, which gives a [soft clustering](/hard-and-soft-clustering/). The objective is not convex in $(U, V)$ together, so the algorithm looks for a local solution.

## The algorithm

Write $d_{ij} = \|x_i - v_j\|$. Each step is the exact minimizer of $J_m$ over one block of variables. For fixed centers, the best memberships come from a [Lagrange multiplier](/lagrange-multiplier/) for the constraint $\sum_j u_{ij} = 1$:

$$u_{ij} = \frac{1}{\sum_{l=1}^{c} (d_{ij} / d_{il})^{2/(m-1)}}.$$

For fixed memberships, the best centers are the weighted means

$$v_j = \frac{\sum_i u_{ij}^m x_i}{\sum_i u_{ij}^m}.$$

The membership formula divides by $d_{il}$, so it fails when a point sits on a center. In that case any memberships that put all weight on the centers at distance 0 are optimal, and the algorithm shares the weight equally among them.

```pseudo id=main
FUZZY-C-MEANS(x[1..n], c, m, ε)
L1  choose initial centers v_1, ..., v_c (for example c distinct data points)
L2  repeat
L3      for each point i
L4          d_ij ← ||x_i − v_j|| for j = 1, ..., c
L5          if some d_ij = 0 then Z ← {j : d_ij = 0}; u_ij ← 1/|Z| for j in Z and u_ij ← 0 otherwise
L6          else u_ij ← 1 / Σ_l (d_ij / d_il)^(2/(m−1)) for j = 1, ..., c
L7      for j ← 1 to c: v_j ← Σ_i u_ij^m x_i / Σ_i u_ij^m (keep v_j if the sum of weights is 0)
L8  until no membership changed by more than ε since the last pass
L9  return U and the centers v
```

Bezdek's form starts from a random membership matrix and computes the centers first. The two forms are the same loop, started at a different point.

## Example

Take the five points $0, 1, 3, 9, 10$ on the line, $c = 2$, $m = 2$ and initial centers $v_1 = 0$, $v_2 = 10$. With $m = 2$ the exponent $2/(m-1)$ is 2, so $u_{i1} = 1 / (1 + d_{i1}^2 / d_{i2}^2)$.

| point | $d_{i1}^2$ | $d_{i2}^2$ | $u_{i1}$ | $u_{i2}$ |
|---|---|---|---|---|
| 0 | 0 | 100 | 1 (on center 1) | 0 |
| 1 | 1 | 81 | 81/82 | 1/82 |
| 3 | 9 | 49 | 49/58 | 9/58 |
| 9 | 81 | 1 | 1/82 | 81/82 |
| 10 | 100 | 0 | 0 | 1 (on center 2) |

The points 0 and 10 use the rule for $d_{ij} = 0$. With these memberships $J_2 \approx 9.579$. The center step uses the weights $u_{ij}^2$ and gives $v_1 = 5877871/5069869 \approx 1.159$ and $v_2 = 106618373/11309687 \approx 9.427$, and $J_2$ falls to about $5.308$. The next half steps give about $4.989$, $4.955$ and $4.950$. After 14 passes the memberships change by less than $10^{-12}$. The centers are about $1.275$ and $9.484$, and $J_2 \approx 4.950$. The point 3 has membership about $0.934$ in the left cluster, and the point 9 about $0.996$ in the right cluster.

The fuzzifier changes the result. With $m = 1.5$ the memberships of the point 3 are about $0.996$ and $0.004$, almost hard. With $m = 3$ they are about $0.772$ and $0.228$.

## Correctness

The full proof is in the proofs file. For fixed centers, $J_m$ is a sum of one convex function for each point, each on a simplex. If a point is on a center, the rule at line L5 gives the value 0, which is the least possible. Otherwise the formula at line L6 makes all partial derivatives equal, and for a convex function on a simplex this is enough for a global minimum. For fixed memberships, each center is a weighted mean, and $\sum_i w_i \|x_i - v\|^2 = \sum_i w_i \|x_i - \bar v\|^2 + (\sum_i w_i) \|v - \bar v\|^2$ shows that the weighted mean $\bar v$ is the best center. So each half step does not increase $J_m$, and the values converge. Bezdek (1980) showed that the limit points of the iterates are fixed points of the two maps, and Bezdek, Hathaway, Sabin and Tucker (1987) showed that such a fixed point can be a saddle point and not a local minimum.

## Complexity

A pass computes $n c$ distances in $O(n c d)$ time. The memberships of one point need the $c$ ratios for each of its $c$ clusters, which is $O(c^2)$ as written, or $O(c)$ with the third form $u_{ij} = D_{ij}^{-1/(m-1)} / \sum_l D_{il}^{-1/(m-1)}$. The center step takes $O(n c d)$. So $t$ passes take $O(t n c (d + c))$ time. The memberships take $O(n c)$ space and the centers $O(c d)$. Unlike k-means, every point affects every center in every pass, so a pass of fuzzy c-means costs about as much as a full pass of k-means, with no saving from sparse assignments.

## Properties

- **Deterministic** for given initial centers; random starts make it random.
- **Monotone.** The objective $J_m$ does not increase in any half step.
- **Local.** It finds a fixed point, which can be a local minimum or a saddle point, and depends on the start.
- **Soft.** Each membership is positive unless a point lies on a center.
- **Limits in $m$.** As $m \to 1^+$ the memberships become 0 or 1 and the method becomes k-means. As $m \to \infty$ every membership tends to $1/c$ for fixed centers.

## Variants and improvements

- **Other distances.** Gustafson and Kessel (1979) give each cluster its own norm, $\|x - v\|_A^2 = (x - v)^\top A (x - v)$ with $\det A$ fixed, so that the clusters can be ellipsoids. Gath and Geva use fuzzy covariance matrices, close to a [Gaussian mixture model](/gaussian-mixture-model/).
- **Possibilistic c-means** (Krishnapuram and Keller 1993) drops the constraint that memberships sum to 1, so outliers get a small membership in every cluster.
- **Seeding.** Starting from [k-means++](/k-means-plus-plus/) centers or from a k-means solution reduces bad local solutions.
- **Choice of $c$.** Validity indices such as the partition coefficient $\frac{1}{n}\sum_{i,j} u_{ij}^2$ or the Xie and Beni index compare runs with different $c$.
- **Gaussian mixtures.** EM for a [Gaussian mixture model](/gaussian-mixture-model/) also gives soft memberships, but they are posterior probabilities from a probability model. Fuzzy c-means has no such model, and its memberships come from the exponent $m$.

## When to use it

Use fuzzy c-means when points can be truly between clusters and you want a degree of membership for each, for example in image segmentation, where a pixel near an edge mixes two tissues, or in fuzzy control and pattern recognition. If the clusters have different shapes and sizes, or if you need probabilities, use a [Gaussian mixture model](/gaussian-mixture-model/). If you need only a hard partition, k-means is cheaper.

## Pitfalls

- A point that lies exactly on a center makes the formula at line L6 divide by zero. Handle it as at line L5.
- With $m$ close to 1, the exponent $2/(m-1)$ is large, and ratios of distances raised to it can overflow. Compute the memberships with logarithms or with the third form and a scaled maximum.
- With a large $m$, all memberships tend to $1/c$, and all centers can drift to the mean of all the data. The usual choice is $m = 2$.
- Memberships are not probabilities of a model. A far outlier still has memberships that sum to 1, so it pulls on the centers.
- The result depends on the start. Run it several times and keep the smallest $J_m$.

## Implementations

## History

Dunn introduced the method in 1973 as "a fuzzy relative of the ISODATA process", with the exponent 2. Bezdek, in his 1973 doctoral thesis at Cornell and in later papers, replaced the exponent by a general fuzzifier $m > 1$. His 1980 paper proved that the iterates converge to fixed points along subsequences, and the 1987 paper by Bezdek, Hathaway, Sabin and Tucker corrected the claim that these are always local minima, with counterexamples that are saddle points. Bezdek's 1981 book made the method the standard algorithm of fuzzy clustering.

## References
