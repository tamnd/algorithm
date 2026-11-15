---
tag: JQBYP3
kind: technique
slug: loop-skewing
name: Loop skewing
aliases:
- iteration space skewing
area: compilers-and-program-analysis/loop-transformations
level: advanced
summary: Adds a multiple of an outer index to an inner one, so that dependences point forward in both loops and tiling or interchange becomes legal.
prereqs: [dependence-distance-vector, loop-interchange, loop-transformation-legality]
see_also: [loop-tiling, unimodular-transformations, lamport-hyperplane-method, wavefront-parallelism, wolf-lam-locality-algorithm, fourier-motzkin-elimination, unimodular-matrix, doall-loop]
sources:
  - paper: doi:10.1007/BF01407876
    title: Michael Wolfe, Loop skewing, the wavefront method revisited, International Journal of Parallel Programming 15(4), 1986, 279-293
    locator: skewing as a change of the inner index by a multiple of the outer index, the new distance vectors, the factor that makes interchange legal, and the wavefront loop that results
  - paper: doi:10.1109/71.97902
    title: Michael E. Wolf and Monica S. Lam, A loop transformation theory and an algorithm to maximize parallelism, IEEE Transactions on Parallel and Distributed Systems 2(4), 1991, 452-471
    locator: skewing as a unimodular matrix, and the skewing that makes a nest fully permutable before tiling and wavefront parallelization
  - paper: doi:10.1145/76263.76337
    title: Michael Wolfe, More iteration space tiling, Proceedings of Supercomputing '89, ACM, 1989, 655-664
    locator: skewing before tiling, to make the tiles legal
---

Loop skewing replaces the index $j$ of an inner loop by $j' = j + f\,i$, where $i$ is the index of an outer loop and $f \ge 0$ is an integer, the *skew factor*. The body uses $j = j' - f\,i$, and the bounds of the inner loop move by $f\,i$. The set of iterations and the order in which they run do not change, so skewing is always legal. What changes is the coordinate system: a [distance vector](/dependence-distance-vector/) $(d_1, d_2)$ becomes $(d_1, d_2 + f\,d_1)$. For a large enough $f$ every distance has nonnegative entries, and then [loop interchange](/loop-interchange/) and [tiling](/loop-tiling/), which were illegal, become legal. Skewing followed by interchange is how a compiler finds the parallel *wavefronts* of a stencil, the same result as the [hyperplane method](/lamport-hyperplane-method/).

## In plain words

Picture a grid of tasks where each task needs the task above it and the task above and to the right. You cannot do the grid column by column, because the task above and to the right is not done yet. Skewing slides each row to the right by one more place than the row above, so the grid becomes a slanted band. In the slanted picture, every task only needs tasks that are above it or to its left. Nothing about the work or its order has changed yet. But now you may walk the band column by column, or in small squares, and every task still finds its inputs ready. Sliding the rows more steeply gives columns whose tasks do not need each other at all, so they can run at the same time.

## When it applies

The nest has two loops $i$ and $j$, with $j$ inside $i$, step 1 for both, and known constant dependence distances $(d_1, d_2)$, each lexicographically positive. The skew factor $f$ is a nonnegative integer; a negative factor is legal too, but has no use in this goal. In a deeper nest, any loop can be skewed by any combination of the loops outside it.

## The template

```pseudo id=main
SKEW(for i = L1 to U1: for j = L2 to U2: BODY(i, j), dependence distances D)
L1  f <- 0
L2  for each (d1, d2) in D with d1 > 0 do
L3      f <- max(f, ceil(-d2 / d1))                 ▷ smallest f with d2 + f d1 >= 0
L4  for i = L1 to U1 do
L5      for jj = L2 + f i to U2 + f i do            ▷ jj = j + f i
L6          BODY(i, jj - f i)
```

The holes are the nest, the distances, and the use that follows: interchange, tiling or a wavefront. Lines L1 to L3 compute the smallest factor that makes every distance nonnegative. A distance with $d_1 = 0$ has $d_2 > 0$ and needs nothing.

**Skewing changes no order.** Two iterations $p \prec q$ map to $p' \prec q'$. Let $e = q - p$, with first nonzero entry $e_l > 0$. If $l = 1$, then $e'_1 = e_1 > 0$. If $l = 2$, then $e_1 = 0$ and $e'_2 = e_2 + f \cdot 0 = e_2 > 0$. Either way $e'$ has the same first nonzero entry as $e$, and $e' \succ 0$. So the skewed nest, which runs in the lexicographic order of $(i, j')$, runs the iterations in the original order, and every dependence keeps its order without any test.

**Theorem.** With $f$ from lines L1 to L3, every skewed distance $(d_1, d_2 + f\,d_1)$ has both entries nonnegative, so the skewed nest is a fully permutable band.

*Proof.* If $d_1 = 0$, then $d_2 > 0$, and the skewed vector is $(0, d_2)$. If $d_1 > 0$, then $f \ge \lceil -d_2 / d_1 \rceil \ge -d_2 / d_1$, so $f\,d_1 \ge -d_2$ and $d_2 + f\,d_1 \ge 0$. $\square$

**Deeper nests.** For a nest of depth $k$, skew loop by loop: $i'_1 = i_1$ and $i'_l = i_l + f_l\,(i'_1 + \dots + i'_{l-1})$ for $l = 2, \dots, k$, with $f_l = \max(0, \max_d (-d_l))$ over all distances. *Claim:* every skewed distance $d'$ is nonnegative. Let $p$ be the first nonzero level of $d$. For $l < p$, all entries so far are $0$, so $d'_l = 0$. At $l = p$, $d'_p = d_p \ge 1$. For $l > p$, assume $d'_1, \dots, d'_{l-1} \ge 0$; their sum $S$ is at least $d'_p \ge 1$, so $d'_l = d_l + f_l S \ge d_l + f_l \ge 0$. The map is lower triangular with ones on the diagonal, so it is a [unimodular matrix](/unimodular-matrix/), and it keeps the order for the same reason as in two loops. This factor is not the smallest; for two loops, line L3 gives the smallest.

**Bounds.** Skewing a rectangle gives a parallelogram: for each $i$, $j'$ runs from $L_2 + f\,i$ to $U_2 + f\,i$. After an interchange the bounds come from [Fourier-Motzkin elimination](/fourier-motzkin-elimination/), as below.

**Profit.** Skewing alone gives nothing; the code is slightly more complex. Its value is in the step that follows: tiling of the skewed band, or interchange that puts a loop with no carried dependence inside.

## Classic examples

**A stencil.** The nest

```
for i = 1 to n:
  for j = 1 to m:
    A[i][j] = A[i-1][j] + A[i][j-1] + A[i-1][j+1]
```

has the flow distances $(1, 0)$, $(0, 1)$ and $(1, -1)$. Interchange is illegal, because of $(1, -1)$; with $n = 4$, $m = 5$ and random start values, the interchanged nest gives a different array. Tiling is illegal for the same reason.

- **$f = 1$.** The distances become $(1, 1)$, $(0, 1)$ and $(1, 0)$. All are nonnegative, so the skewed nest can be tiled and interchanged. After the interchange, the outer loop runs over $t = i + j$ and the inner loop over $i$. In the order $(d_t, d_i)$ the distances are $(1, 1)$ for $(1, 0)$, $(1, 0)$ for $(0, 1)$, and $(0, 1)$ for $(1, -1)$. The last one is carried by the inner loop, so the inner loop must stay sequential. Run in order it gives the same array; with each inner loop run backward it does not.
- **$f = 2$.** The distances become $(1, 2)$, $(0, 1)$ and $(1, 1)$. After the interchange, with $t = 2i + j$ outer, the distances in the order $(d_t, d_i)$ are $(2, 1)$, $(1, 0)$ and $(1, 1)$: the outer loop carries all of them, and the inner loop is a [DOALL loop](/doall-loop/). Each value of $t$ is a *front* of iterations that can run at the same time.

The bounds for $f = 2$ come from $1 \le i \le n$ and $1 \le t - 2i \le m$:

```
for t = 3 to 2n + m:
  parallel for i = max(1, ceil((t - m) / 2)) to min(n, floor((t - 1) / 2)):
    j = t - 2i
    A[i][j] = A[i-1][j] + A[i][j-1] + A[i-1][j+1]
```

For $n = 4$ and $m = 5$ this has $2n + m - 2 = 11$ fronts that together cover the 20 iterations once each, and running each front in a random order gives the same array as the original nest. This is the [wavefront](/wavefront-parallelism/) of the nest, the function $t = 2i + j$ that the [hyperplane method](/lamport-hyperplane-method/) finds for these distances.

**Tiling a time loop.** A Jacobi-style sweep `for t: for x: B[t][x] = (B[t-1][x-1] + B[t-1][x] + B[t-1][x+1]) / 3` has the distances $(1, 1)$, $(1, 0)$ and $(1, -1)$. Line L3 gives $f = 1$, and the distances become $(1, 2)$, $(1, 1)$ and $(1, 0)$. The skewed band is fully permutable, and tiling it gives parallelogram tiles in the $(t, x)$ plane. This *time skewing* lets a cache keep a tile for several time steps.

**Unimodular view.** Skewing by $f$ is the matrix $\begin{pmatrix} 1 & 0 \\ f & 1 \end{pmatrix}$, and skewing followed by interchange is $\begin{pmatrix} f & 1 \\ 1 & 0 \end{pmatrix}$. Both have determinant $\pm 1$. The [unimodular transformations](/unimodular-transformations/) page treats any such matrix with one legality test.

## Variations

- **Skewing an outer loop by an inner one.** Replacing $i$ by $i + f\,j$ is also a unimodular map, but it changes the order, so it needs the general test $T d \succ 0$.
- **Skewing for tiling in deep nests.** The loop-by-loop factors above make any band fully permutable. The [Wolf-Lam algorithm](/wolf-lam-locality-algorithm/) uses this to tile for locality.
- **Wavefront without interchange.** Generate the code for the fronts directly from the time function, with [Fourier-Motzkin elimination](/fourier-motzkin-elimination/) of the bounds; this is what the hyperplane method does.
- **Diamond and other tile shapes.** Skewing by different factors for the two sides of a tile gives tiles that can start in parallel. These come from the [polyhedral model](/polyhedral-model/).

## Pitfalls

- **Skewing with too small a factor for the goal.** $f = 1$ makes the stencil above tileable, but after interchange its inner loop is still sequential. Parallel fronts need $f = 2$. Compute the factor from the goal: nonnegative distances for tiling, a positive outer entry for every distance for a parallel inner loop.
- **Forgetting to rewrite the body.** The body must use $j = j' - f\,i$. Using $j'$ as $j$ touches the wrong elements.
- **Rectangular bounds after an interchange.** The skewed space is a parallelogram. Copying the old bounds into the interchanged nest runs wrong iterations; derive the bounds again.
- **Short fronts.** Near the corners, a front has only one or two iterations. With few processors the parallel loop then gives little, and the synchronization between fronts costs a barrier each.

## Exercises

1. A nest has the distances $(1, -2)$ and $(2, -3)$. Give the smallest skew factor. *Answer.* $\lceil 2/1 \rceil = 2$ and $\lceil 3/2 \rceil = 2$, so $f = 2$: the distances become $(1, 0)$ and $(2, 1)$.
2. After skewing with $f = 2$ and an interchange, the distances $(1, 0)$, $(0, 1)$ and $(1, -1)$ become what, and why is the inner loop parallel? *Answer.* $(2, 1)$, $(1, 0)$ and $(1, 1)$: the first entry of each is positive, so the outer loop carries all of them.
3. Skew `for i = 0 to 3: for j = 0 to 2` with $f = 1$. What is the range of $j'$ for $i = 2$? *Answer.* $j' = j + 2$ runs from $2$ to $4$.
4. A nest of depth 3 has the distances $(1, -1, 0)$ and $(0, 1, -2)$. Give the loop-by-loop factors and the skewed distances. *Answer.* $f_2 = 1$ and $f_3 = 2$. For $(1, -1, 0)$: $d'_2 = -1 + 1 = 0$, $d'_3 = 0 + 2(1 + 0) = 2$, so $(1, 0, 2)$. For $(0, 1, -2)$: $d'_2 = 1$, $d'_3 = -2 + 2 \cdot 1 = 0$, so $(0, 1, 0)$.

## References
