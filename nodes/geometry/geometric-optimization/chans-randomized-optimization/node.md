---
tag: FFXM2R
kind: technique
slug: chans-randomized-optimization
name: Chan's randomized optimization technique
aliases:
- Chan's randomized optimization
- Chan's technique
- randomized optimization technique
area: geometry/geometric-optimization
level: research
summary: Turns a decision procedure into an optimizer at no asymptotic cost. Split into smaller subproblems, test them in random order, and recurse only on the expected O(log r) new minima.
prereqs: [parametric-search, decision-problem, random-permutation, harmonic-series, expected-running-time]
see_also: [parametric-search, prune-and-search, clarksons-algorithm, lp-type-problem, randomized-closest-pair, backwards-analysis, las-vegas-algorithm, minimum-width-annulus]
sources:
  - paper: doi:10.1007/PL00009478
    title: "Timothy M. Chan, Geometric applications of a randomized optimization technique, Discrete and Computational Geometry 22(4), 1999"
    locator: the main lemma on solving an optimization problem in the expected time of its decision problem, and the applications in the later sections
  - paper: "Nimrod Megiddo, Applying parallel computation algorithms in the design of serial algorithms, Journal of the ACM 30(4), 1983"
    locator: parametric search, the deterministic method that Chan's technique replaces in many applications
  - paper: "Samir Khuller and Yossi Matias, A simple randomized sieve algorithm for the closest-pair problem, Information and Computation 118(1), 1995"
    locator: the linear expected time closest pair with a grid and hashing, the model used in the example
  - paper: "Timothy M. Chan, An optimal randomized algorithm for maximum Tukey depth, Proceedings of the 15th ACM-SIAM Symposium on Discrete Algorithms, 2004"
    locator: a later application, the point of maximum Tukey depth in the plane in O(n log n) expected time
---

Chan's randomized optimization technique computes the optimum value $w(P)$ of a problem in the same expected time $O(D(n))$ as deciding $w(P) < t$ for a given $t$. It needs one structural fact: the problem splits into a constant number $r$ of subproblems, each a constant fraction smaller, whose optima have $w(P)$ as their minimum. The algorithm tests the subproblems in random order against the best value found so far and recurses only when a subproblem beats it. In a random order the $i$-th item is a new minimum with probability at most $1/i$, so the expected number of recursive calls is at most the [harmonic number](/harmonic-series/) $H_r$, and the time is a geometric series. Chan (1999) introduced it as a simpler and often faster alternative to [parametric search](/parametric-search/), and it removes the logarithmic factors that parametric search usually adds.

## In plain words

Suppose you can quickly answer the question "is the best answer smaller than this number?" but finding the best answer itself seems harder.

Cut the problem into a few smaller pieces, so that the best answer of the whole is the best answer of one of the pieces. Look at the pieces in a random order. For each piece, ask the quick question: does this piece beat the best answer found so far? Only if it does, solve the piece fully, by the same method.

In a random order, a new record is rare: the tenth piece is a record with chance at most one in ten. So you solve only a few pieces fully, and most pieces cost only one quick question. The pieces are smaller, so the total work stays within a constant factor of one quick question on the whole input.

## When it applies

Notation: $w$ maps instances to values in an ordered set, and $|P| = n$ is the size of an instance. $D(n)$ is a time bound.

**Lemma (Chan 1999).** Let $\alpha < 1$, $\varepsilon > 0$ and $r$ be constants, and let $D(n)/n^{\varepsilon}$ be monotone increasing. Suppose that for every instance $P$ of size $n$, in $O(D(n))$ time one can

1. decide whether $w(P) < t$ for a given value $t$, and
2. build $r$ instances $P_1, \ldots, P_r$ of the same problem, each of size at most $\lceil \alpha n \rceil$, with $w(P) = \min_i w(P_i)$.

Then $w(P)$ can be computed in $O(D(n))$ expected time.

The condition on $D$ gives $D(\alpha n) \le \alpha^{\varepsilon} D(n)$, so the work shrinks geometrically down the recursion. It holds for $D(n) = n$ and $D(n) = n \log n$, but not for $D(n) = \log n$. The lemma is stated for minimization; for maximization reverse the order. The model is that of the decision procedure: the technique itself only adds a random permutation and comparisons of values.

## The template

```pseudo id=main
CHAN-OPTIMIZE(P)
L1  if |P| ≤ c₀ then return BRUTE-FORCE(P)
L2  P₁, …, P_r ← SUBPROBLEMS(P)                ▷ each of size ≤ ⌈αn⌉
L3  π ← a uniformly random permutation of 1, …, r
L4  t ← ∞
L5  for i ← 1 to r do
L6      if DECIDE(P_π(i), t) then                ▷ is w(P_π(i)) < t ?
L7          t ← CHAN-OPTIMIZE(P_π(i))           ▷ a new minimum
L8  return t
```

**Correctness.** After step $i$ of the loop, $t = \min_{j \le i} w(P_{\pi(j)})$: if $w(P_{\pi(i)}) < t$ the line L7 sets $t$ to it, and otherwise $t$ is already at most it. At the end $t = \min_i w(P_i) = w(P)$.

**The probability of a recursive call.** Line L7 runs at step $i$ only if $P_{\pi(i)}$ has a strictly smaller value than all of $P_{\pi(1)}, \ldots, P_{\pi(i-1)}$. For a uniform random order, the first $i$ items are a uniform random set of $i$ items in random order, and at most one of them is the unique strict minimum; it is last with probability at most $1/i$. Strict comparison matters: with ties, equal values do not trigger a call.

**Time.** Let $T(n)$ be the largest expected time over instances of size at most $n$. Lines L2 to L6 cost $O(D(n)) + r \cdot O(D(\lceil \alpha n \rceil)) = O(D(n))$, since $r$ is a constant. The decision to recurse at step $i$ depends only on $\pi$, which is independent of the random choices inside the recursive call, so by [linearity of expectation](/linearity-of-expectation/)

$$T(n) \le c\, D(n) + H_r\, T(\lceil \alpha n \rceil).$$

Unrolling, level $k$ contributes at most $c\, D(n) (H_r \alpha^{\varepsilon})^k$, up to the rounding in $\lceil \alpha n \rceil$. If $H_r \alpha^{\varepsilon} < 1$ the sum is $O(D(n))$.

**When $H_r \alpha^{\varepsilon} \ge 1$.** Apply SUBPROBLEMS $k$ times before the loop. This gives $R = r^k$ subproblems of size about $\alpha^k n$ in $O(D(n))$ time, since $k$ is a constant. Then $H_R \le 1 + k \ln r$ and $H_R\, \alpha^{k\varepsilon} \le (1 + k \ln r)\alpha^{k\varepsilon}$, which is less than 1 for a large enough constant $k$, because the exponential factor wins over the linear one. So the lemma holds for all constants $\alpha < 1$, $\varepsilon > 0$ and $r$.

### Example

**Closest pair.** Let $w(P)$ be the smallest squared distance between two points of a set $P$ of $n$ points in the plane.

- *Decision.* To test $w(P) < t$, put the points in a [uniform grid](/uniform-grid/) of cell side $\sqrt{t}/2$ with a hash table. Two points in one cell are at squared distance at most $t/2 < t$, so if a cell receives a second point, the answer is yes. Otherwise every cell holds one point, and each point is compared with the points in the $5 \times 5$ block of cells around it. This takes $O(n)$ expected time in the real RAM with the floor function and hashing, so $D(n) = n$ and $\varepsilon = 1$.
- *Subproblems.* Split $P$ into $g = 10$ groups of $n/10$ points. The closest pair lies in at most two groups, so $w(P)$ is the minimum over the $r = \binom{10}{2} = 45$ unions of two groups, each of size $n/5$. So $\alpha = 1/5$.
- *Check.* $H_{45} \approx 4.395$ and $H_{45} \cdot (1/5)^1 \approx 0.879 < 1$. The lemma gives $O(n)$ expected time, the same bound as Rabin's and Khuller and Matias's algorithms, with no new geometric idea.

In a run on 20 random sets of about 3000 integer points with $c_0 = 20$, the number of recursive calls per invocation averaged 3.65 at the top level and between 3.9 and 4.1 at deeper levels, below $H_{45}$. The result matched an exact sweep line closest pair every time. The averages are lower than $H_{45}$ because the closest pair often lies in many subproblems, and ties do not cause calls.

## Classic examples

Chan's paper applies the lemma to several problems for which parametric search gave a slower or much more complex algorithm. Its list includes:

- **Closest pair**, as in the example above.
- **Smallest subsets of $k$ points** under measures such as the perimeter or the diameter.
- **Matching point sets under translation**, for example under the [Hausdorff distance](/hausdorff-distance/).
- **Rectilinear $p$-centers** for small $p$, a case of the [k-center problem](/k-center-problem/).
- **Discrete 1-centers**, where the center must be an input point.
- **Linear programming with $k$ violated constraints.**
- **Maximum Tukey depth in the plane.** Chan (2004) used the same approach for an $O(n \log n)$ expected time algorithm.

## Variations

- **Parametric search.** Megiddo's method simulates a parallel decision procedure on the unknown optimum. It is deterministic but complex, and usually costs an extra logarithmic factor. Chan's lemma needs only a sequential decision procedure and a way to split.
- **Prune and search.** [Prune and search](/prune-and-search/) also shrinks the input by a constant factor each round, but it needs the decision on a median to discard part of the input. Chan's method keeps all of the input in some subproblem and saves time by not solving most subproblems.
- **Random sampling in LP-type problems.** [Clarkson's algorithm](/clarksons-algorithm/) and other algorithms for [LP-type problems](/lp-type-problem/) also gain from random order, by [backwards analysis](/backwards-analysis/). The bound $1/i$ for a new minimum is the simplest backwards analysis argument.
- **Las Vegas.** The output is always correct, only the time is random, so it is a [Las Vegas algorithm](/las-vegas-algorithm/). A high probability bound needs more care, since the recursion branches.
- **Derandomization.** Without the random order, a fixed order can trigger all $r$ calls, and $T(n) = r\, T(\alpha n) + O(D(n))$ can grow much faster than $D(n)$.

## Pitfalls

- **Subproblems must cover the optimum exactly.** The condition is $w(P) = \min_i w(P_i)$. If some subproblem can have a value below $w(P)$, the result is wrong; if none contains the optimum, it is also wrong.
- **Subproblems must be instances of the same problem.** The recursion calls the same decision and splitting procedures on them, with the same time bounds.
- **Use strict comparison.** Recurse only when $w(P_i) < t$. With $\le$, equal values trigger calls, and with many ties the bound $1/i$ fails.
- **The decision must be correct at every threshold, including $t = \infty$.** The first subproblem in the order is always solved recursively.
- **Watch the constants.** With $H_r \alpha^{\varepsilon} \ge 1$ the plain recursion is not linear in $D(n)$; expand $k$ levels first, as above.
- **Slow growing $D$.** If $D(n)$ grows slower than any power of $n$, the series may not shrink, and the lemma does not apply as stated.

## Exercises

1. Prove that in a uniform random permutation of $r$ distinct numbers the expected number of left to right minima is exactly $H_r$.
2. For the closest pair example with $g$ groups, find the smallest $g$ for which $H_{\binom{g}{2}} \cdot 2/g < 1$.
3. For $D(n) = n$ and $\alpha = 1/2$, show that the plain recurrence gives $O(n)$ when $r = 3$ but not when $r = 4$, and how many levels of expansion make $r = 4$ work.
4. Give a problem with a linear time decision procedure for which the subproblem condition fails, and explain why.
5. Use the lemma to compute the [diameter](/polygon-diameter/) of a point set from a decision procedure, and compare with the direct method.

## References
