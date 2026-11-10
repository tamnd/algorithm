---
tag: CKX5V3
kind: algorithm
slug: kmv-sketch
name: K-minimum values sketch
aliases:
- BJKST algorithm
- KMV sketch
- bottom-k sketch
- k minimum values
- KMV synopsis
area: online-and-streaming/streaming-sketches
level: core
summary: Keeps the k smallest hash values and estimates distinct count from the k-th smallest.
solves: [distinct-elements-problem]
model: word-ram
complexity:
  vars: {k: the number of kept hash values, n: the universe size}
  time: {worst: O(log k), average: O(1)}
  space: {extra: O(k log n)}
properties: {online: true, deterministic: false, mergeable: true}
history:
  year: 2002
  people: [Ziv Bar-Yossef, T. S. Jayram, Ravi Kumar, D. Sivakumar, Luca Trevisan, Kevin Beyer, Peter J. Haas, Berthold Reinwald, Yannis Sismanis, Rainer Gemulla]
  note: Bar-Yossef, Jayram, Kumar, Sivakumar and Trevisan gave the k smallest hash values estimator with a proof under pairwise independence in 2002. Beyer, Haas, Reinwald, Sismanis and Gemulla gave the unbiased estimator and the estimators for set operations in 2007.
prereqs: [distinct-elements-problem, hash-function, binary-heap]
see_also: [hyperloglog, flajolet-martin-algorithm, minhash, jaccard-similarity, mergeable-summaries, linear-counting, median-trick, priority-queue]
sources:
  - paper: doi:10.1007/3-540-45726-7_1
    title: Ziv Bar-Yossef, T. S. Jayram, Ravi Kumar, D. Sivakumar and Luca Trevisan, Counting distinct elements in a data stream, RANDOM 2002, LNCS 2483
    locator: pp. 1 to 10 (the first algorithm, the t smallest hash values with pairwise independent hashing)
  - paper: doi:10.1145/1247480.1247504
    title: Kevin Beyer, Peter J. Haas, Berthold Reinwald, Yannis Sismanis and Rainer Gemulla, On synopses for distinct-value estimation under multiset operations, SIGMOD 2007
    locator: pp. 199 to 210 (the unbiased estimator (k − 1)/U_(k), its variance, and the estimators for union and intersection)
  - book: isbn:9781108477444
    title: Graham Cormode and Ke Yi, Small Summaries for Big Data, Cambridge University Press, 2020
    locator: Chapter 2 (the k minimum values sketch)
---

The K-minimum values sketch, or KMV, estimates the number $d$ of distinct items by keeping the $k$ smallest hash values seen so far, with the hash values scaled to $(0, 1)$. If $d$ distinct values are spread at random over $(0, 1)$, the $k$-th smallest of them, $v_k$, is close to $k/d$. The estimate $(k-1)/v_k$ is exactly unbiased for an ideal hash, with variance $d(d-k+1)/(k-2)$, so the relative standard error is at most $1/\sqrt{k-2}$. Bar-Yossef, Jayram, Kumar, Sivakumar and Trevisan (2002) proved an $(\varepsilon, \delta)$ guarantee for this kind of estimator with pairwise independent hashing; the form with $k$ values is often called the BJKST algorithm. Beyer, Haas, Reinwald, Sismanis and Gemulla (2007) gave the unbiased form and showed how to estimate unions and intersections. The sketch is a uniform sample of the distinct items, so it answers more than a count: intersections, [Jaccard similarity](/jaccard-similarity/), and counts with a filter. On this page $k$ is the number of kept values, $d$ is the number of distinct items, $n$ is the universe size, and the stream is in the [cash register model](/cash-register-model/).

## In plain words

Drop $d$ random points on a line from 0 to 1. With many points, they are packed close together, and the smallest ones are near 0. With few points, the gaps are wide. So the position of the tenth smallest point tells you how many points there are: if it is at 0.001, there are about ten thousand. KMV hashes each distinct item to such a point, and keeps the $k$ smallest points. Repeats land on the same point, so they change nothing. The $k$ kept items are also a random sample of all the different items, so two sketches can tell how much two sets overlap, by checking how many of the sampled items appear in both.

## The problem

The input is a stream of items from a universe of size $n$, with repeats. The output is an estimate of the number $d$ of distinct items, and, from two sketches, estimates of the size of the union and of the intersection of their sets. The count is the [distinct elements problem](/distinct-elements-problem/).

## The algorithm

Let $h$ map items to integers that are read as numbers $u(x) \in (0, 1]$; for a 64-bit hash $y$, $u = (y + 1)/2^{64}$. The sketch is a max-heap of at most $k$ hash values, with a set for membership tests.

```pseudo id=main
KMV(σ, h, k)
L1  T ← empty max-heap                        ▷ the k smallest hash values so far
L2  for each item x of σ do
L3      y ← h(x)
L4      if y ∈ T, or |T| = k and y ≥ max(T), then skip x
L5      insert y into T; if |T| > k then remove max(T)
L6  if |T| < k then return |T|                ▷ fewer than k distinct items: exact
L7  return (k − 1) / u(max(T))                ▷ max(T) is the k-th smallest value v_k
```

**Merge.** Two sketches with the same $h$ and $k$ merge into the $k$ smallest values of the union of their sets $T_A \cup T_B$. This is the sketch of the union of the two streams.

**Union and intersection.** Let $L$ be the merged sketch, with $k$-th smallest value $v_k$, and let $K$ be the number of values of $L$ that are in both $T_A$ and $T_B$. Then:

- $|A \cup B|$ is estimated by $(k-1)/v_k$.
- $|A \cap B|$ is estimated by $(K/k)\cdot(k-1)/v_k$.
- The Jaccard similarity $|A \cap B|/|A \cup B|$ is estimated by $K/k$.

## Example

Let $k = 3$ and the stream $a, b, c, a, d, e, b, f$ with $d = 6$, and let the scaled hash values be $a \mapsto 0.62$, $b \mapsto 0.11$, $c \mapsto 0.85$, $d \mapsto 0.30$, $e \mapsto 0.47$, $f \mapsto 0.05$.

| item | action | $T$ after |
|---|---|---|
| a | insert | 0.62 |
| b | insert | 0.11, 0.62 |
| c | insert | 0.11, 0.62, 0.85 |
| a | already in $T$ | same |
| d | insert, remove 0.85 | 0.11, 0.30, 0.62 |
| e | insert, remove 0.62 | 0.11, 0.30, 0.47 |
| b | already in $T$ | same |
| f | insert, remove 0.47 | 0.05, 0.11, 0.30 |

So $v_3 = 0.30$ and the estimate is $2/0.30 \approx 6.67$, against $d = 6$. With $k = 10$, the sketch keeps all 6 values and line L6 returns 6, the exact count.

**Intersection.** Let a second stream have the set $B = \{d, e, f, g, h\}$, with $g \mapsto 0.20$ and $h \mapsto 0.70$. Its sketch is $\{0.05, 0.20, 0.30\}$. The merged sketch is the 3 smallest of $\{0.05, 0.11, 0.20, 0.30\}$, which is $\{0.05, 0.11, 0.20\}$, so $v_3 = 0.20$ and the union estimate is $2/0.20 = 10$, against $|A \cup B| = 8$. Only 0.05, the value of $f$, is in both sketches, so $K = 1$. The intersection estimate is $(1/3) \cdot 10 \approx 3.33$, against $|A \cap B| = 3$, and the Jaccard estimate is $1/3$, against $3/8$.

## Correctness

The proof page proves the following for an ideal hash, whose values are independent and uniform on $(0, 1)$.

- **The state.** After the stream, $T$ is the set of the $k$ smallest hash values of the distinct items. The merge rule gives the $k$ smallest values of the union.
- **The law of $v_k$.** When $d \ge k$, $v_k$ has the Beta$(k, d - k + 1)$ distribution.
- **Unbiased count.** $\mathbb{E}[(k-1)/v_k] = d$ for $k \ge 2$, and $\mathrm{Var}((k-1)/v_k) = d(d-k+1)/(k-2)$ for $k \ge 3$. The estimate $k/v_k$, which looks more natural, has mean $dk/(k-1)$ and is biased.
- **Unbiased intersection.** The $k$ items with the smallest values are a uniform random $k$-subset of $A \cup B$, independent of $v_k$. So $\mathbb{E}[K/k] = |A \cap B|/|A \cup B|$, and the intersection estimate is unbiased.

By [Chebyshev's inequality](/chebyshev-inequality/), $k \ge 2 + 1/(\varepsilon^2\delta)$ gives $\Pr[|\hat d - d| > \varepsilon d] \le \delta$. With $\delta = 1/4$ and the [median trick](/median-trick/), $O(\varepsilon^{-2}\log(1/\delta))$ values in total give probability $1 - \delta$.

**Limited independence (cited).** Bar-Yossef et al. analyse the estimate $t/v_t$ with $t = O(1/\varepsilon^2)$ and a pairwise independent hash into a range of size polynomial in $n$, and prove that it is within $1 \pm \varepsilon$ of $d$ with constant probability, by Chebyshev bounds on the number of hash values below $(1 \pm \varepsilon)t/d$. That gives $O(\varepsilon^{-2}\log n)$ bits per copy, including the $O(\log n)$ bits of the seed, and $O(\varepsilon^{-2}\log n\log(1/\delta))$ bits with the median trick.

## Complexity

- **Update time.** $O(1)$ expected for the test of line L4, with a hash set. When a value enters, line L5 costs $O(\log k)$. The $i$-th distinct item enters only if its value is among the $k$ smallest of the first $i$, which has probability $\min(1, k/i)$, so over $d$ distinct items the expected number of heap changes is $k(1 + H_d - H_k) \approx k(1 + \ln(d/k))$ (proved). Most updates take the fast path.
- **Query time.** $O(1)$: the maximum of the heap.
- **Space.** $k$ hash values. With a 64-bit hash, $64k$ bits; in theory $O(\log n)$ bits per value suffice, so $O(k\log n)$ bits, plus the seed of $h$. For the same error, KMV uses more bits than [HyperLogLog](/hyperloglog/), which stores $O(\log\log n)$ bits per register.
- **Accuracy.** Relative standard error $\sqrt{(d-k+1)/(d(k-2))} < 1/\sqrt{k-2}$ (proved, ideal hash). For $k = 1024$, about 3.1%.

## Properties

- **Unbiased.** For an ideal hash, at each $d$, not only in the limit.
- **Exact below $k$.** When $d < k$ the sketch holds all distinct hash values and the count is exact.
- **Mergeable.** The $k$ smallest of the union of two sketches is the sketch of the union. See [mergeable summaries](/mergeable-summaries/).
- **A sample of distinct items.** The kept items are a uniform random $k$-subset of the distinct items, so the sketch can estimate the number of distinct items with a property, by the fraction of kept items with it.
- **Set operations.** Intersections and Jaccard similarity from two sketches. This is the same idea as [MinHash](/minhash/) with one hash function and the $k$ smallest values.
- **No deletions.** When an item leaves, the next smallest value is not known. Beyer et al. add counters to each kept value (the AKMV synopsis) for multiset differences.

## Variants and improvements

- **BJKST.** The form with a pairwise independent hash and the estimate $t/v_t$, with an $(\varepsilon, \delta)$ proof. The same paper has further algorithms with less space.
- **Bottom-$k$ sketches.** The same structure for weighted items and sampling, studied by Cohen and Kaplan, where each item keeps its own value and the sketch estimates sums over subsets.
- **Theta sketches.** Keep all values below a threshold $\theta$, and lower $\theta$ when the sketch grows too large. This handles set operations among many sketches with different sizes.
- **AKMV.** Beyer et al. keep a counter of the multiplicity with each value, for multiset union, intersection and difference.
- **[HyperLogLog](/hyperloglog/).** Less memory for a pure count, but no sample, no unbiased estimate and poor intersections.

## When to use it

Use KMV when you need set operations on many count distinct sketches, such as the size of the overlap of two audiences, or counts with a filter applied after the fact. Use it also when you want an unbiased estimate with a simple proof, or an exact count for small sets. When memory per sketch is the main limit and only the count matters, [HyperLogLog](/hyperloglog/) is smaller.

## Pitfalls

- **Inserting a repeat at line L4.** If the membership test is missing, a repeated item can be inserted twice and push out a real value; the estimate is then too large.
- **Using $k/v_k$ at line L7.** This overestimates by the factor $k/(k-1)$. Use $(k-1)/v_k$.
- **Forgetting line L6.** With fewer than $k$ distinct items, $\max(T)$ is not $v_k$, and $(k-1)/\max(T)$ is wrong. Return the count.
- **A very small $k$ at line L7.** With $k = 1$ the estimate is always 0, and with $k = 2$ it is unbiased but its variance is infinite. Use $k \ge 3$, and in practice $k$ in the hundreds or more. Also scale the values into $(0, 1]$, as $u = (y+1)/2^{64}$ does, so that $u$ is never 0.
- **Intersections from the union formula.** $|A| + |B| - |A \cup B|$ from three estimates has error relative to $|A \cup B|$. Use $K/k$ from the merged sketch.
- **Merging sketches with different $h$ or $k$.** The values are not comparable. With different $k$, merge at the smaller $k$.

## Implementations

## History

Bar-Yossef, Jayram, Kumar, Sivakumar and Trevisan presented "Counting distinct elements in a data stream" at RANDOM 2002. They gave three algorithms; the first keeps the $t$ smallest values of a pairwise independent hash, and its analysis gave the first $(\varepsilon, \delta)$ bound for $F_0$ with $O(\varepsilon^{-2}\log n)$ bits per copy. The idea of the $k$-th smallest hash value also appears in earlier database work. Beyer, Haas, Reinwald, Sismanis and Gemulla (SIGMOD 2007) studied the estimator for database synopses, gave the unbiased form $(k-1)/v_k$ with its variance, and the estimators for multiset operations. Later systems built theta sketches on the same idea.

## References
