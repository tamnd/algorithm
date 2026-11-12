---
tag: 6S8D6H
kind: algorithm
slug: affinity-propagation
name: Affinity propagation
aliases:
- Frey-Dueck affinity propagation
area: machine-learning/clustering
level: advanced
summary: "Points exchange responsibility and availability messages (max-sum on a factor graph) until a set of exemplars emerges. No convergence or optimality guarantee."
solves: [clustering-problem]
model: real-ram
complexity:
  vars: {n: the number of points, t: the number of iterations}
  time: {worst: "O(t n^2)"}
  space: {extra: "O(n^2)"}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 2007
  people: [Brendan J. Frey, Delbert Dueck]
  note: Frey and Dueck published affinity propagation in Science in 2007 and derived it from the max-sum algorithm on a factor graph. Givoni and Frey gave the derivation on a binary factor graph in 2009.
prereqs: [clustering-problem, factor-graph, max-product]
see_also: [loopy-belief-propagation, facility-location-problem, k-median-problem, partitioning-around-medoids, k-means, spectral-clustering, mean-shift, belief-propagation]
sources:
  - paper: doi:10.1126/science.1136800
    title: "Brendan J. Frey and Delbert Dueck, Clustering by passing messages between data points, Science 315(5814), 2007, pages 972 to 976"
    locator: "the update rules for r(i, k), a(i, k) and a(k, k), the preferences s(k, k), the damping factor and the stopping rule, and the supporting online material (the derivation by max-sum on a factor graph)"
  - paper: "Inmar E. Givoni and Brendan J. Frey, A binary variable model for affinity propagation, Neural Computation 21(6), 2009, pages 1589 to 1600"
    locator: the factor graph with binary variables c_ij, its constraint factors, and the derivation of the responsibility and availability messages
---

Affinity propagation clusters $n$ points by choosing some of the points as *exemplars* and assigning each other point to one exemplar. It does not need the number of clusters. Instead, each point $k$ has a *preference* $s(k, k)$, and a larger preference makes more exemplars. The points exchange two kinds of real-valued messages, *responsibilities* $r(i, k)$ and *availabilities* $a(i, k)$, until the set of exemplars stops changing. The messages are the max-sum (max-product in the log domain) messages on a factor graph of the exemplar problem. Each iteration costs $O(n^2)$ time. The method can fail to converge, and when it converges it can return a set of exemplars that is not optimal.

## In plain words

Each point looks for a leader among the points. Two types of notes go back and forth.

A point sends a note to each candidate leader: "this is how much better you fit me than my best other choice". A candidate collects these notes. If many points like it, it is more willing to lead, and it sends back notes: "this is how available I am for you".

Each point then compares its candidates again, with the new notes in mind, and the rounds repeat. To stop the notes from swinging, each new note is mixed with the old one.

A point becomes a leader when its own interest in leading, plus the support from others, is positive. Each other point joins its most similar leader. A value called the preference says how eager each point is to lead, and so it sets how many groups you get.

## The problem

The input is a matrix of similarities $s(i, k)$ for $i \ne k$, where a larger value means that $k$ is a better exemplar for $i$, and a preference $s(k, k)$ for each point. For points in $\mathbb{R}^d$, Frey and Dueck use $s(i, k) = -\lVert x_i - x_k \rVert^2$ and the same preference for all points; the median of the similarities gives a moderate number of clusters, and their minimum gives a small number.

A clustering is a map $c$ from points to exemplars that is *valid*: if $c(i) = k$ for some $i$, then $c(k) = k$. Its *net similarity* is

$$\sum_{i} s(i, c(i)),$$

which counts $s(k, k)$ once for each exemplar $k$. Affinity propagation searches for a valid $c$ with a large net similarity. With costs $-s$, this is the uncapacitated [facility location problem](/facility-location-problem/) with the points as clients and as sites, which is NP-hard in general. The method is a heuristic for it.

**The messages.** With all messages 0 at the start, one round computes

$$r(i, k) \leftarrow s(i, k) - \max_{k' \ne k} \bigl( a(i, k') + s(i, k') \bigr),$$

$$a(i, k) \leftarrow \min\Bigl(0,\; r(k, k) + \sum_{i' \notin \{i, k\}} \max(0, r(i', k))\Bigr) \quad (i \ne k), \qquad a(k, k) \leftarrow \sum_{i' \ne k} \max(0, r(i', k)).$$

The responsibility $r(i, k)$ says how much better $k$ fits $i$ than the best competitor, with the availabilities of the competitors taken into account. The availability $a(i, k)$ says how much support $k$ has from the other points as an exemplar. It is at most 0 for $i \ne k$, because the support of others can not make $k$ more than fully available, and $a(k, k)$, the self-availability, is at least 0. These are the max-sum messages on the factor graph of Givoni and Frey (2009); the correctness proof derives them.

## The algorithm

```pseudo id=main
AFFINITY-PROPAGATION(s, λ, t_conv, t_max)       ▷ s(k, k) holds the preferences; 0.5 ≤ λ < 1
L1  r(i, k) ← 0, a(i, k) ← 0 for all i, k
L2  repeat for t = 1, 2, ..., t_max
L3      r'(i, k) ← s(i, k) − max_{k' ≠ k} (a(i, k') + s(i, k'))                 for all i, k
L4      r ← λ r + (1 − λ) r'                                                      ▷ damping
L5      a'(i, k) ← min(0, r(k, k) + Σ_{i' ∉ {i,k}} max(0, r(i', k))),  a'(k, k) ← Σ_{i' ≠ k} max(0, r(i', k))
L6      a ← λ a + (1 − λ) a'
L7      E ← { k : a(k, k) + r(k, k) > 0 }
L8  until E has not changed for t_conv rounds
L9  if E is empty then return "no exemplars"
L10 c(k) ← k for k ∈ E;  c(i) ← argmax_{k ∈ E} s(i, k) for each i ∉ E;  return E and c
```

Line L3 costs $O(n^2)$, not $O(n^3)$: for each $i$, find the largest and the second largest of $a(i, k') + s(i, k')$. The maximum over $k' \ne k$ is the largest value, except at the $k$ that attains it, where it is the second largest. Line L5 also costs $O(n^2)$: for each $k$, sum $\max(0, r(i', k))$ over $i' \ne k$ once, and subtract the term of $i$.

Line L10 follows common practice (scikit-learn finds the exemplars in the same way): the decision for the exemplars comes from line L7, and the other points go to their most similar exemplar. Frey and Dueck state the decision as "for each $i$, take the $k$ that maximizes $a(i, k) + r(i, k)$". Line L10 makes the output a valid clustering in every case, while the per-point rule can point to a $k$ that is not itself an exemplar when the messages have not converged.

## Example

Take four points on a line, $x = 0, 1, 5, 6$, with $s(i, k) = -(x_i - x_k)^2$. The off-diagonal similarities are $-1$ (twice), $-16$, $-25$ (twice) and $-36$, each for both orders, and their median is $-20.5$, which is the preference. Use $\lambda = 0.5$.

**Round 1.** With $a = 0$, line L3 gives $r'(i, k) = s(i, k) - \max_{k' \ne k} s(i, k')$:

| $r'(i, k)$ | $k = 0$ | $k = 1$ | $k = 2$ | $k = 3$ |
|---|---|---|---|---|
| $i = 0$ | $-19.5$ | $19.5$ | $-24$ | $-35$ |
| $i = 1$ | $15$ | $-19.5$ | $-15$ | $-24$ |
| $i = 2$ | $-24$ | $-15$ | $-19.5$ | $15$ |
| $i = 3$ | $-35$ | $-24$ | $19.5$ | $-19.5$ |

For example $r'(0, 1) = -1 - (-20.5) = 19.5$: point 1 beats the next best choice of point 0, which is point 0 itself with its preference. Line L4 halves these values. Then line L5 gives, for example, $a'(1, 1) = \max(0, r(0, 1)) = 9.75$ and $a'(0, 1) = \min(0, r(1, 1)) = -9.75$. After line L6 the values $a(k, k) + r(k, k)$ are $-6, -4.875, -4.875, -6$, so there is no exemplar yet.

**At convergence.** The messages converge to

| $k$ | 0 | 1 | 2 | 3 |
|---|---|---|---|---|
| $r(k, k)$ | $-9.75$ | $-9.75$ | $-9.75$ | $-9.75$ |
| $a(k, k)$ | $9$ | $10.5$ | $10.5$ | $9$ |
| $a(k, k) + r(k, k)$ | $-0.75$ | $0.75$ | $0.75$ | $-0.75$ |

So $E = \{1, 2\}$, the points at $x = 1$ and $x = 5$. Line L10 sends point 0 to 1 and point 3 to 2. The net similarity is $2 \cdot (-20.5) - 1 - 1 = -43$. A brute force over all 15 non-empty exemplar sets finds the same optimum value; $\{0, 2\}$ and other mirror choices tie with it.

**The preference sets the number of clusters.** For the eight points $0, 1, 2, 10, 11, 13, 20, 21$, the preference $-200$ gives 2 exemplars, the median $-100$ gives 3, and $-0.5$ makes all 8 points exemplars. In all three runs the result equals the brute-force optimum.

**No optimality.** For the five points $4, 8, 9, 11, 17$ with preference $-80$, the messages converge, for $\lambda = 0.5$, $0.7$ and $0.9$, to the single exemplar 11 with net similarity $-80 - 49 - 9 - 4 - 36 = -178$. The optimum is the single exemplar 9 with $-80 - 25 - 1 - 4 - 64 = -174$. The values $a(k, k) + r(k, k)$ at the fixed point are far from 0 ($109$ for point 11, at most $-31$ for the others), so this is not a tie: max-sum on this loopy graph converges to a wrong answer.

## Correctness

Affinity propagation has no guarantee of convergence and no guarantee of optimality, and the page claims neither. What does hold:

- **The messages are max-sum messages.** On the factor graph with a binary variable $c_{ik}$ for "$i$ chooses $k$", a factor $s(i, k) c_{ik}$, a constraint that each $i$ chooses exactly one $k$, and a constraint that $k$ is chosen by others only if $k$ chooses itself, the max-sum messages (written as differences between the values for 1 and 0) are exactly $r(i, k)$ and $a(i, k)$. The sum of the factors of a feasible assignment is the net similarity. So the method is [loopy max-sum](/loopy-belief-propagation/) for the exemplar problem. On a tree, max-sum is exact; this graph has many loops, so the [max-product](/max-product/) guarantees do not apply.
- **A damped fixed point is a fixed point.** If $m = \lambda m + (1 - \lambda) f(m)$ with $\lambda < 1$, then $m = f(m)$. So at convergence the messages satisfy the update equations exactly. The implementation tests this.
- **The output is valid.** Line L10 maps each exemplar to itself and each other point to an exemplar, so the result is a valid clustering whenever $E$ is not empty.

The full derivation is in the correctness proof.

## Complexity

The costs are in the [real RAM](/real-ram/) model.

- **One round.** Lines L3 and L5 cost $\Theta(n^2)$ with the trick above. Lines L4, L6 and L7 cost $\Theta(n^2)$.
- **Total.** $O(t n^2)$ for $t$ rounds. The number of rounds is not bounded by any function of $n$: the method may not converge, so $t_{\max}$ is needed. Frey and Dueck stop when the decisions stay the same for some number of rounds.
- **Sparse similarities.** If only $m$ pairs have a similarity (the others are $-\infty$), the messages exist only on those pairs, and a round costs $O(n + m)$.
- **Memory.** Three $n \times n$ matrices, $\Theta(n^2)$.

## Properties

- **The number of clusters is not an input.** It follows from the preferences and the data.
- **Exemplars are data points**, as in [k-medoids](/partitioning-around-medoids/), so any similarity works, even one that is not symmetric or not a metric.
- **Deterministic**, unless noise is added to break ties.
- **No guarantee.** It can oscillate, and a fixed point can be suboptimal.

## Variants and improvements

- **Damping.** Frey and Dueck use $\lambda = 0.5$ by default. If the messages oscillate, increase $\lambda$ toward 1; this slows the method but often makes it converge.
- **Noise.** Add a tiny random amount to $s$ to remove exact ties (Frey and Dueck do this). See the pitfalls.
- **Refinement of exemplars.** Some implementations recompute, after line L10, the exemplar of each cluster as the member with the largest total similarity to the others, and assign again.
- **Other clustering by exemplars.** [Partitioning around medoids](/partitioning-around-medoids/) fixes $k$ and does local search. The [k-median problem](/k-median-problem/) and the [facility location problem](/facility-location-problem/) have algorithms with proven approximation ratios on metric data.
- **Other factor graphs.** The binary model of Givoni and Frey (2009) makes it easy to change the constraints; hierarchical affinity propagation adds layers of exemplars in the same way.

## When to use it

Use affinity propagation when the number of clusters is unknown, when the exemplars must be actual data points, and when only a similarity matrix is given, possibly not symmetric. It is practical for a few thousand points with a dense matrix, or more with sparse similarities. Do not use it for very large $n$ with dense similarities, because of the $\Theta(n^2)$ memory, nor when you need a guarantee on the result. For clusters of irregular shape, [spectral clustering](/spectral-clustering/) or [mean shift](/mean-shift/) may fit better.

## Pitfalls

- **Exact ties.** With symmetric data, two candidates can tie, and $a(k, k) + r(k, k)$ can converge to exactly 0. Then line L7 drops them. For the points $0, 1, 2, 10, 11, 13, 20, 21$ with preference $-2$, four points have $a(k, k) + r(k, k) = 0$ at the fixed point, the exemplars are the points at 1 and 13, and the net similarity is $-132$. With tiny noise added, the result has net similarity $-12$, the optimum.
- **Oscillation.** With $\lambda$ too small, the messages swing between states. Raise $\lambda$ and $t_{\max}$, and check whether the run converged.
- **The preference scale.** The preference has the units of $s$. A preference near 0 makes every point an exemplar; a very negative one makes one cluster. Start with the median of the similarities.
- **Undamped updates.** $\lambda = 0$ often oscillates. The implementation requires $\lambda \ge 0.5$.
- **Treating the output as optimal.** It is a fixed point of loopy max-sum, not a certified optimum; see the five-point example.

## Implementations

## History

Frey and Dueck published affinity propagation in Science in 2007. They derived it from the max-sum algorithm on a factor graph with one $n$-valued variable per point, and compared it with many random restarts of k-centers clustering on face images, gene data and other sets, where it found exemplar sets of higher net similarity. Givoni and Frey (2009) gave a simpler derivation on a factor graph with $n^2$ binary variables, which also led to variants with other constraints.

## References
