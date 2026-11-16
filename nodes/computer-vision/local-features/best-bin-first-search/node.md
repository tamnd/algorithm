---
tag: THZZ2G
kind: algorithm
slug: best-bin-first-search
name: Best bin first search
aliases:
- BBF search
area: computer-vision/local-features
level: advanced
summary: Approximate nearest neighbor search in a k-d tree that visits bins in order of distance from the query, from a priority queue, and stops after a fixed number of leaves.
solves: [approximate-nearest-neighbor-search, nearest-neighbor-search]
model: real-ram
complexity:
  vars: {n: the number of points, d: the dimension, E: the number of leaves to examine, k: the number of neighbors}
  time: {worst: O(E log n (d + log(E log n)) + E log k), average: O(E log n (d + log(E log n)) + E log k), best: O(d log n)}
  space: {extra: O(E d log n + k)}
properties: {deterministic: true, exact: false, anytime: true, exact_when_unbounded: true}
history:
  year: 1997
  people: [Jeffrey S. Beis, David G. Lowe]
  note: Beis and Lowe described BBF at CVPR 1997 for shape indexing. Arya independently described the same priority search of a k-d tree. Lowe used BBF to match SIFT keypoints in 2004.
prereqs: [kd-tree, priority-queue]
see_also: [kd-tree-nearest-neighbor-search, randomized-kd-forest, approximate-nearest-neighbor-search, best-first-branch-and-bound, feature-matching, lowe-ratio-test, sift, locality-sensitive-hashing]
sources:
  - paper: "Jeffrey S. Beis and David G. Lowe, Shape indexing using approximate nearest-neighbour search in high-dimensional spaces, IEEE Conference on Computer Vision and Pattern Recognition (CVPR), 1997, 1000-1006"
    locator: "Section 4 (the k-d tree with median splits on the dimension of greatest variance, the BBF search with a priority queue and the limit Emax), Section 5 (the experiments on uniform data and on shape indexing)"
  - paper: doi:10.1023/B:VISI.0000029664.99615.94
    title: "David G. Lowe, Distinctive image features from scale-invariant keypoints, International Journal of Computer Vision 60(2), 2004, 91-110"
    locator: "Section 7.2 (BBF with a cut-off after 200 candidates for keypoint matching)"
  - paper: doi:10.1145/293347.293348
    title: "Sunil Arya, David M. Mount, Nathan S. Netanyahu, Ruth Silverman and Angela Y. Wu, An optimal algorithm for approximate nearest neighbor searching in fixed dimensions, Journal of the ACM 45(6), 1998, 891-923"
    locator: the priority search of the leaf cells in order of distance from the query and the incremental distance computation
  - paper: doi:10.1145/355744.355745
    title: "Jerome H. Friedman, Jon Louis Bentley and Raphael Ari Finkel, An algorithm for finding best matches in logarithmic expected time, ACM Transactions on Mathematical Software 3(3), 1977, 209-226"
    locator: the exact k-d tree search with the bounds-overlap-ball test that BBF reorders
---

Best bin first (BBF) search finds an approximate nearest neighbor of a query point in a [k-d tree](/kd-tree/). It keeps the subtrees it has not explored in a [priority queue](/priority-queue/), keyed by the distance from the query to the box (the bin) of each subtree, and always explores the closest bin next. It stops after a fixed number $E$ of leaves and returns the best point found so far, so in high dimension the answer can be wrong; with no limit it is the exact search. Beis and Lowe (1997) introduced it for shape indexing, and Lowe used it to match [SIFT](/sift/) descriptors.

## In plain words

A k-d tree cuts space into boxes, and each box holds a few points. To find the point closest to a query, the plain search goes down to the box that holds the query and then backs up the tree and looks at the neighboring boxes in the order of the tree. In many dimensions the true answer is often in a box far from that order, and the exact search ends up looking at most of the boxes. BBF looks at boxes in the order of their distance from the query instead. It keeps a list of boxes not yet seen, sorted by distance, and takes the closest one each time. Most of the time the true answer is in one of the first boxes it sees. So BBF looks at a fixed number of boxes, for example 200, and returns the best point among them.

## The problem

The input is a set of $n$ points $x^{(1)}, \dots, x^{(n)}$ in $\mathbb{R}^d$, a query $q$, a number of neighbors $k$ and a budget of $E$ leaves. The output is a list of $k$ points of the set with their squared [Euclidean distances](/euclidean-distance/) $D(x) = \lVert x - q \rVert^2$ to $q$, sorted. The ideal answer is the $k$ nearest points. BBF gives that answer when $E$ is large enough, and otherwise a list of points that are close but not always the closest. This is a form of [approximate nearest neighbor search](/approximate-nearest-neighbor-search/) with no guarantee on the error; the [c-approximate](/c-approximate-nearest-neighbor/) form has a guarantee.

The tree is the one of Beis and Lowe. Each internal node takes the dimension of greatest variance of its points, sorts them on that dimension and splits at the median point. The left child gets the first half, with coordinates at most the split value $s$, and the right child gets the rest, with coordinates at least $s$. A leaf holds one point in the paper; our code allows a few. The depth is $\lceil \log_2 n \rceil$ with one point per leaf.

## The algorithm

Each queue entry is a subtree, its key $b$ and an offset vector $o$. The offset $o_t$ is the signed distance from $q$ to the last split on dimension $t$ that the path crossed to the far side, or 0. The key is $b = \sum_t o_t^2$, the squared distance from $q$ to the bin of the subtree. A crossing on dimension $j$ changes one term of the sum, so the new key costs $O(1)$ arithmetic plus the copy of $o$.

```pseudo id=main
BBF-SEARCH(T, q, E, k)
L1  best ← empty list of at most k (distance, point) pairs; checked ← 0
L2  Q ← min-priority queue holding (0, root of T, zero offsets)
L3  while Q is not empty and checked < E do
L4      (b, node, o) ← remove the entry with the smallest key from Q
L5      if best has k items and b ≥ the largest distance in best then stop: the answer is exact
L6      while node is an internal node do
L7          j ← split dimension of node; δ ← q_j - split value of node
L8          if δ < 0 then near, far ← left, right else near, far ← right, left
L9          o' ← o with o'_j = δ; b' ← b - o_j^2 + δ^2
L10         insert (b', far, o') into Q
L11         node ← near
L12     for each point x in the leaf node: put (D(x), x) in best if it is among the k closest so far
L13     checked ← checked + 1
L14 return best
```

The descent of lines L6 to L11 keeps the key $b$ for the near child, because the query is on the near side of the split. Line L5 is the stop rule of the exact search: no unexplored bin is closer than the current $k$-th neighbor. With $E = \infty$, BBF is the exact [k-d tree nearest neighbor search](/kd-tree-nearest-neighbor-search/) that visits the bins in order of distance instead of in the order of the tree.

The original paper describes the queue key as the distance from the query to the bin boundary. Some implementations use only the squared distance to the last split hyperplane, $\delta^2$. That key is also a lower bound, but a weaker one, so it explores more bins before line L5 stops the search. Our code uses the full bin distance.

## Example

Take the six points $(2, 3)$, $(5, 4)$, $(9, 6)$, $(4, 7)$, $(8, 1)$, $(7, 2)$ in the plane, with one point per leaf. The variance of the $x$ coordinates is $5.81$ and of the $y$ coordinates $4.47$, so the root splits on $x$. Sorted on $x$, the median point is $(7, 2)$, so the root splits at $x = 7$. The left half $\{(2,3), (4,7), (5,4)\}$ splits on $y$ at 4, and its right part $\{(5,4), (4,7)\}$ splits on $y$ at 7. The right half $\{(7,2), (8,1), (9,6)\}$ splits on $y$ at 2, and its right part $\{(7,2), (9,6)\}$ splits on $y$ at 6.

The query is $q = (4.5, 1)$. Squared distances are used throughout.

| step | popped key | leaf reached | pushed (key, bin) | best so far |
| --- | --- | --- | --- | --- |
| 1 | 0 | (2, 3), distance 10.25 | (6.25, $x \ge 7$), (9, $x \le 7, y \ge 4$) | (2, 3), 10.25 |
| 2 | 6.25 | (8, 1), distance 12.25 | (7.25, $x \ge 7, y \ge 2$) | (2, 3), 10.25 |
| 3 | 7.25 | (7, 2), distance 7.25 | (31.25, $x \ge 7, y \ge 6$) | (7, 2), 7.25 |
| 4 | 9 | none | none | stop: $9 \ge 7.25$ |

In step 1 the root has $\delta = 4.5 - 7 = -2.5$, so the key of the right half is $2.5^2 = 6.25$. The node below has $\delta = 1 - 4 = -3$, so its far child gets $0 + 9 = 9$. In step 2 the popped entry has the offset $-2.5$ on $x$, and the split $y = 2$ gives $\delta = -1$, so the far child gets $6.25 + 1 = 7.25$. In step 4 the smallest key, 9, is at least the best distance, 7.25, so line L5 stops: the answer $(7, 2)$ is exact after 3 leaves. With $E = 1$ the search returns $(2, 3)$, the plain descent, at distance $\sqrt{10.25} = 3.20$ instead of $\sqrt{7.25} = 2.69$; with $E = 2$ it still returns $(2, 3)$.

A measured example: we ran our code on 5000 points uniform in $[0, 1]^d$, with 100 uniform queries, one point per leaf and seed 7. The table gives the number of queries, out of 100, for which BBF returned the true nearest neighbor, and the mean ratio of the returned distance to the true distance.

| $d$ | $E = 1$ | $E = 10$ | $E = 50$ | $E = 200$ | leaves to prove the answer exact (mean) |
| --- | --- | --- | --- | --- | --- |
| 4 | 15, 1.914 | 88, 1.020 | 100, 1.000 | 100, 1.000 | 16.5 |
| 8 | 14, 1.562 | 60, 1.097 | 96, 1.003 | 100, 1.000 | 129.4 |
| 16 | 6, 1.422 | 32, 1.121 | 58, 1.039 | 89, 1.007 | 2470.6 |

In 16 dimensions the exact search must examine about half of the 5000 leaves, but 200 leaves give the true neighbor 89 times out of 100. This is a measurement on one random data set, not a property of the method.

## Correctness

The proof in `proofs/correctness.md` shows four facts:

- **The key is a lower bound.** For every queue entry $(b, v, o)$, every point $x$ in the subtree of $v$ has $|x_t - q_t| \ge |o_t|$ for each $t$, so $D(x) \ge b$.
- **The keys come out in order.** A crossing on dimension $j$ never makes $|o_j|$ smaller, because each split value is a coordinate of a point inside the bin. So the popped keys do not decrease, and BBF examines the bins in order of distance.
- **Exact when it stops by itself.** If the queue is empty, or line L5 stops the loop, the list holds the $k$ nearest points.
- **More leaves do not hurt.** The search with budget $E$ examines a prefix of the leaves that the search with budget $E' > E$ examines, so its $i$-th distance is never smaller.

There is no bound on the error when the budget stops the search. The success rates in the example and in the papers are measurements.

## Complexity

The model is the real RAM, with one arithmetic operation or comparison on reals at unit cost. Let $h = \lceil \log_2 n \rceil$ be the depth of the tree.

- **Build.** At each of the $h$ levels the code computes $d$ variances over all points and sorts each node on one dimension, which costs $O(d n + n \log n)$ per level and $O(d n \log n + n \log^2 n)$ in total. A linear-time median brings this to $O(d n \log n)$.
- **Search.** Each of the $E$ examined leaves comes from one descent of at most $h$ levels. Each level pushes one entry: $O(d)$ to copy the offsets and $O(\log(E h))$ for the heap. Each leaf point costs $O(d)$ for the distance and $O(\log k)$ for the list. With a constant number of points per leaf, the total is $O(E h (d + \log(E h)) + E \log k)$, and the queue holds at most $E h$ entries of $d + 2$ numbers.
- **Best case.** With $E = 1$ the search is the plain descent, $O(d \log n)$.

The cost depends on $E$ and not on how far the true neighbor is. This is the point of BBF: a fixed time per query. The exact search, by contrast, has a good expected cost only in low dimension. Friedman, Bentley and Finkel (1977) showed a logarithmic expected time for a fixed dimension, with a constant that grows exponentially with $d$; in high dimension the exact search examines a large part of the leaves, as the table above shows.

Beis and Lowe measured this on 100,000 points uniform in the unit hypercube with $E = 200$ and 1000 queries. In 12 dimensions BBF found the true nearest neighbor 94 percent of the time, against 59 percent for the restricted search in the order of the tree, which they allowed 2.4 times as many leaves. The exact search examined over 2400 leaves. Up to 20 dimensions the mean distance that BBF found was only 2 percent greater than the true one. Lowe (2004) stopped BBF after 200 candidates to match SIFT keypoints against 100,000 keypoints and measured a speedup of about two orders of magnitude over exact search, with a loss of less than 5 percent of the correct matches.

## Properties

- **Anytime.** The search can stop after any number of leaves and returns the best points found so far. More leaves never give a worse answer.
- **Exact with no limit.** With $E = \infty$ the result is the exact $k$ nearest neighbors, and the search often proves this early through line L5.
- **Deterministic.** For a fixed tree and query, the order of the leaves is fixed. Ties in the queue are broken by the insertion order.
- **No error bound.** Unlike the $(1 + \varepsilon)$ search of Arya and his coauthors, the fixed budget gives no bound on the ratio of distances.
- **Works for $k > 1$.** The list keeps $k$ neighbors, which the [ratio test](/lowe-ratio-test/) needs with $k = 2$.

## Variants and improvements

- **Priority search with an error bound.** Arya, Mount, Netanyahu, Silverman and Wu stop when the key exceeds the best distance divided by $(1 + \varepsilon)^2$, and prove that the result is within a factor $1 + \varepsilon$ of the true distance. Their tree is the balanced box decomposition tree.
- **Hyperplane key.** Use $\delta^2$ of the last split as the key. It costs less memory, since no offset vector is stored, but the key is a weaker bound.
- **Many trees.** The [randomized k-d forest](/randomized-kd-forest/) builds several trees with random split dimensions and searches all of them with one queue. In the measurements of Silpa-Anan and Hartley and of Muja and Lowe on SIFT descriptors, this does better than one tree at the same number of checks.
- **Other indexes.** [Locality-sensitive hashing](/locality-sensitive-hashing/), [product quantization](/product-quantization/) and graph indexes such as [HNSW](/hnsw/) replace the tree in large systems.
- **Branch and bound.** BBF is [best-first branch and bound](/best-first-branch-and-bound/) with the bin distance as the bound and a limit on the number of nodes.

## When to use it

Use BBF when you need nearest neighbors of many queries in a fixed set of moderate dimension, about 8 to 30, and a fixed time per query matters more than a guarantee. The classic case is [feature matching](/feature-matching/) of SIFT descriptors, where a wrong neighbor only loses one match and [RANSAC](/ransac/) removes it later. In 2 or 3 dimensions use the exact search; it is fast there. For millions of points in high dimension, a forest of trees or a graph index usually gives a better trade of time and accuracy.

## Pitfalls

- **Squared distances.** Keep squared distances in the queue and in the list. A ratio threshold on distances, such as 0.8, becomes 0.64 on squared distances.
- **The key must be a lower bound.** If the key overestimates the distance to the bin, the stop rule of line L5 can stop too early and claim an exact answer that is wrong. Adding $\delta^2$ to the key without removing the old offset on the same dimension overestimates.
- **Budget in leaves or in points.** Beis and Lowe count leaves; FLANN counts the points it checks. With one point per leaf they agree; with larger leaves they do not.
- **No guarantee.** With a budget the result can be wrong. Report the budget with any accuracy number.
- **Ties at the split.** Points equal to the split value can be on both sides. Keep the order $\le s$ on the left and $\ge s$ on the right, or the lower bound on the key fails.
- **Duplicates.** Many equal points have zero variance in every dimension. Stop the split there and keep them in one leaf, or the build does not end.

## Implementations

The Python code in `impl/python/best_bin_first_search.py` builds the tree of Beis and Lowe and runs BBF with the full bin distance and a budget in leaves. It returns the $k$ nearest points it found and a flag that is true when line L5 or an empty queue proved the answer exact. The tests compare the unbounded search with a brute force scan in 1 to 8 dimensions, check that the flag is never wrong, check that the keys are lower bounds and come out in order, and check that a larger budget never gives a worse answer.

## History

Friedman, Bentley and Finkel (1977) gave the exact k-d tree search, which backs up the tree and tests each bin against the ball of the current best distance. Beis and Lowe (1997) changed the order of the search to the order of bin distance and added the fixed number of leaves, for indexing of shape features of moderate dimension. They note that Arya, in a technical report, independently developed the same method under the name priority k-d tree search; Arya, Mount and their coauthors later proved error bounds for a related priority search. Lowe used BBF in SIFT to match keypoints against large databases. Silpa-Anan and Hartley (2008) and Muja and Lowe (2009) extended it to several randomized trees.

## References
