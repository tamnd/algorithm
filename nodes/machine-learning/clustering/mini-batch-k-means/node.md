---
tag: A9SG65
kind: algorithm
slug: mini-batch-k-means
name: Mini-batch k-means
aliases:
- Sculley mini-batch k-means
- web-scale k-means
area: machine-learning/clustering
level: advanced
summary: "A stochastic k-means heuristic that updates the centers from small random batches, with per-center learning rate 1/count."
solves: [k-means-problem]
model: real-ram
complexity:
  vars: {b: the batch size, t: the number of iterations, k: the number of clusters, d: the dimension, n: the number of points}
  time: {worst: "O(t b k d)"}
  space: {extra: "O(k d + b)"}
properties: {deterministic: false, exact: false, online: true, recursive: false}
history:
  year: 2010
  people: [D. Sculley]
  note: Sculley proposed the batch version with per-center learning rates for web-scale data; MacQueen's online k-means of 1967 is the case b = 1.
prereqs: [k-means, stochastic-gradient-descent]
see_also: [k-means, k-means-plus-plus, stochastic-gradient-descent, online-algorithm, birch, coreset, streaming-k-median, hartigan-wong-algorithm]
sources:
  - paper: doi:10.1145/1772690.1772862
    title: D. Sculley, Web-scale k-means clustering, Proceedings of the 19th International Conference on World Wide Web (WWW), 2010, pages 1177 to 1178
    locator: Algorithm 1 (mini-batch k-means with per-center learning rates) and the projection step for sparse centers
  - paper: "Léon Bottou and Yoshua Bengio, Convergence properties of the k-means algorithms, Advances in Neural Information Processing Systems 7 (NIPS 1994), MIT Press, 1995, pages 585 to 592"
    locator: online k-means as stochastic gradient descent with the learning rate 1/count, and batch k-means as a Newton step
  - paper: "James MacQueen, Some methods for classification and analysis of multivariate observations, Proceedings of the Fifth Berkeley Symposium on Mathematical Statistics and Probability, Volume 1, 1967, pages 281 to 297"
    locator: the sequential update of a mean after each new point
---

Mini-batch k-means is a stochastic heuristic for the [k-means problem](/k-means-problem/) on large data sets. Each iteration draws a small random batch of $b$ points, gives each point of the batch to its nearest center, and moves each center a step toward its batch points, with a learning rate of $1/v$ for a center that has received $v$ points so far. An iteration costs $O(bkd)$ instead of the $O(nkd)$ of [Lloyd's algorithm](/k-means/), and Sculley (2010) observed that it reaches a cost close to that of Lloyd's algorithm in much less time. It is a heuristic: it has no approximation guarantee, and its cost does not fall at every step.

## In plain words

Lloyd's method looks at every point in each round. With millions of points, each round is slow. Mini-batch k-means looks at only a small random handful of points in each round. Each point in the handful pulls its nearest center a little toward itself.

How far a center moves depends on how many points it has seen. The first point moves the center all the way onto itself. The second point moves it half way, the third a third of the way, and so on. With this rule each center is always the plain average of all the points it has received. Old points keep their weight, so the centers settle down over time, even though each handful is random.

## The problem

The input is a list of points $x_1, \ldots, x_n \in \mathbb{R}^d$ with the Euclidean norm, the number of clusters $k$, a batch size $b$, a number of iterations $t$, and a source of random numbers. The output is $k$ centers $c_1, \ldots, c_k$. The goal is a small k-means cost $\sum_i \min_j \|x_i - c_j\|^2$. The method gives no bound on the cost relative to the optimum, and the result is random; quality is an observed property.

## The algorithm

```pseudo id=main
MINIBATCH-KMEANS(x_1..x_n, k, b, t)
L1  c_1, ..., c_k ← k points drawn from the data (or from k-means++)
L2  v_j ← 0 for each j
L3  for s ← 1 to t do
L4      M ← b points drawn at random from the data
L5      for each x in M: j(x) ← the index of the nearest center to x
L6      for each x in M do
L7          j ← j(x); v_j ← v_j + 1
L8          η ← 1 / v_j
L9          c_j ← (1 − η) c_j + η x
```

Line L5 computes all the nearest centers of the batch before any center moves; this is the cache of the paper. Line L9 is a step of [stochastic gradient descent](/stochastic-gradient-descent/) on the loss $\frac12\|x - c_j\|^2$, whose gradient with respect to $c_j$ is $c_j - x$. The counts $v_j$ never reset, so the learning rate of each center falls like $1/v_j$.

The implementation draws the batch without replacement inside one iteration and with replacement across iterations. It does not include the optional projection of the paper onto an $L_1$ ball, which makes the centers sparse.

## Example

Take the four points $0, 1, 10, 11$ on a line, $k = 2$, the initial centers $c_1 = 0$ and $c_2 = 10$, and $b = 2$.

| iteration | batch | nearest centers | updates | centers after | counts after |
|---|---|---|---|---|---|
| 1 | 1, 11 | $c_1$, $c_2$ | $\eta = 1$: $c_1 = 1$; $\eta = 1$: $c_2 = 11$ | 1, 11 | 1, 1 |
| 2 | 0, 10 | $c_1$, $c_2$ | $\eta = 1/2$: $c_1 = 1/2$; $\eta = 1/2$: $c_2 = 21/2$ | 1/2, 21/2 | 2, 2 |
| 3 | 1, 0 | $c_1$, $c_1$ | $\eta = 1/3$: $c_1 = 2/3$; $\eta = 1/4$: $c_1 = 1/2$ | 1/2, 21/2 | 4, 2 |

In iteration 1 the rate $\eta = 1$ moves each center onto its first point, so the initial positions are forgotten. After iteration 3 the center $c_1 = 1/2$ is the mean of its four samples $1, 0, 1, 0$, and $c_2 = 21/2$ is the mean of $11, 10$. Here these are also the optimal centers.

## Correctness

The method is a heuristic, so its correctness is about what it computes, not about the optimum.

- **Running mean.** After a center has received the samples $y_1, \ldots, y_v$, it equals their mean $\frac{1}{v}\sum y_l$. The proof is an induction on $v$: $(1 - \frac1v)\frac{1}{v - 1}\sum_{l < v} y_l + \frac1v y_v = \frac1v \sum_{l \le v} y_l$.
- **One full batch is one Lloyd step.** If $b = n$ and the counts are 0, one iteration replaces each center that receives a point by the mean of the points nearest to it, which is exactly one step of Lloyd's algorithm. After that, the centers are means of all samples so far, which is no longer Lloyd's rule.
- **Termination.** The loop runs exactly $t$ iterations.
- **No monotone decrease.** A batch can move a center away from points that are not in the batch, so the cost on the full data can rise. There is no bound on the ratio to the optimum.

The proofs are in the proofs section below. As $v_j$ grows the steps shrink like $1/v_j$, which meets the usual conditions of stochastic approximation (the sum of the rates diverges, the sum of their squares converges). Bottou and Bengio (1995) used this to argue that online k-means converges to a stationary point of the expected loss; this is about convergence, not about the quality of the limit.

## Complexity

**Time.** Line L5 costs $O(bkd)$ per iteration and lines L6 to L9 cost $O(bd)$. The total is $O(tbkd)$, independent of $n$ apart from the cost of drawing a batch. To see each point about once takes $t \approx n / b$ iterations, which costs about as much as one Lloyd iteration.

**Space.** The centers and counts take $O(kd)$, and a batch takes $O(b)$ indices. The data need not be in memory: the method can read batches from a stream or from disk.

**Observed behavior.** On large text data Sculley reported that mini-batch k-means reaches a given cost orders of magnitude faster than Lloyd's algorithm, with a final cost a few percent higher. This is an observation, not a bound.

## Properties

- **Randomized.** The result depends on the batches. Different runs give different centers.
- **Online.** With $b = 1$ it is MacQueen's sequential k-means. With any $b$ it can process a stream.
- **Each center is a running mean.** The rate $1/v_j$ gives equal weight to all samples a center has received, including those assigned under old, poorer centers.
- **Not a descent method.** The full cost can rise after an iteration. A library stops on a smoothed estimate of the cost or after a fixed number of iterations.
- **No guarantee.** There is no approximation bound, and the result is usually a little worse than Lloyd's algorithm from the same seeds.

## Variants and improvements

- **MacQueen's online k-means.** The case $b = 1$, from 1967.
- **Sparse centers.** Sculley adds a projection of each center onto an $L_1$ ball, which keeps the centers sparse for text data.
- **Reassigning weak centers.** scikit-learn moves a center that has received very few points to a random data point, to avoid centers that never win.
- **Fixed or decaying rates.** A constant rate $\eta$ lets the centers track data that drifts over time, at the price of noise.
- **Seeding.** Start from [k-means++](/k-means-plus-plus/) on a sample of the data.
- **Coresets and streaming.** A [coreset](/coreset/) of the data, or a streaming method such as [BIRCH](/birch/) or [streaming k-median](/streaming-k-median/), gives a different way to cluster data that does not fit in memory, with guarantees in the case of coresets.

## When to use it

Use it when $n$ is so large that one Lloyd iteration over the full data is expensive, for example for millions of documents or images, or when the data arrives as a stream. Use full [Lloyd's algorithm](/k-means/) or [Hartigan's method](/hartigan-wong-algorithm/) when the data fits in memory and the last few percent of cost matter.

## Pitfalls

- **A fixed learning rate.** The rate must be $1/v_j$ per center for the running mean. A global rate, or a rate that does not fall, leaves the centers noisy.
- **Updating inside the assignment.** Assign the whole batch first (line L5) and then update. Interleaving them makes the result depend on the order inside the batch.
- **Small batches.** With very small $b$ the early centers are pulled around by single points. Batches of a few hundred to a few thousand points are common.
- **Stopping on the batch cost.** The cost on one batch is noisy. Use a moving average or the cost on a held-out sample.
- **Expecting Lloyd's result.** The centers are means of all samples ever assigned, under old centers too. So the final centers are usually not a fixed point of Lloyd's algorithm. One or two Lloyd steps on the full data can polish them.

## Implementations

## History

MacQueen (1967) introduced the sequential update of the means, which is the case $b = 1$. Bottou and Bengio (1995) analysed online k-means as stochastic gradient descent and batch k-means as a Newton method. Sculley (2010) proposed mini-batches with per-center learning rates for web-scale clustering at Google, and the method became standard in libraries such as scikit-learn.

## References
