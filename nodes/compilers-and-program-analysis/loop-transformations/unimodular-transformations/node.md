---
tag: 2X9ZFB
kind: technique
slug: unimodular-transformations
name: Unimodular loop transformations
aliases:
- unimodular framework
area: compilers-and-program-analysis/loop-transformations
level: advanced
summary: Models interchange, reversal and skewing as integer matrices of determinant plus or minus 1 on the iteration space, composed by product.
prereqs: [unimodular-matrix, dependence-distance-vector, loop-transformation-legality, fourier-motzkin-elimination]
see_also: [loop-interchange, loop-skewing, loop-tiling, lamport-hyperplane-method, wolf-lam-locality-algorithm, hermite-normal-form, polyhedral-model, affine-scheduling-problem]
sources:
  - title: Utpal Banerjee, Unimodular transformations of double loops, Proceedings of the Third Workshop on Languages and Compilers for Parallel Computing, Irvine, 1990; reprinted in Advances in Languages and Compilers for Parallel Computing (A. Nicolau, D. Gelernter, T. Gross and D. Padua, editors), MIT Press, 1991, 192-219
    locator: a double loop transformed by a 2 x 2 unimodular matrix, the legality condition on the distance vectors, and the new loop bounds
  - paper: doi:10.1109/71.97902
    title: Michael E. Wolf and Monica S. Lam, A loop transformation theory and an algorithm to maximize parallelism, IEEE Transactions on Parallel and Distributed Systems 2(4), 1991, 452-471
    locator: interchange, reversal and skewing as unimodular matrices, legality as the lexicographic positivity of the transformed dependence vectors, distance and direction entries, and the code generation of the bounds
  - book: isbn:9780805327304
    title: Michael Wolfe, High Performance Compilers for Parallel Computing, Addison-Wesley, 1996
    locator: the chapter on loop restructuring, the unimodular matrix view of loop interchange, reversal and skewing
---

A unimodular transformation of a perfect loop nest of depth $k$ is a $k \times k$ integer matrix $T$ with determinant $\pm 1$. The new nest visits the same iterations, but it names the iteration $i$ by $y = T i$ and runs the points in lexicographic order of $y$. [Interchange](/loop-interchange/), reversal and [skewing](/loop-skewing/) are the elementary cases, and a sequence of them is the product of their matrices, so one test covers every combination: $T$ is legal if and only if $T d \succ 0$ for every [dependence distance](/dependence-distance-vector/) $d$. The determinant $\pm 1$ makes the map a bijection of the integer points, so the new loops visit exactly the old iterations, with bounds computed by [Fourier-Motzkin elimination](/fourier-motzkin-elimination/). The framework, due to Banerjee for double loops and to Wolf and Lam in general, turns the choice of a loop order into the choice of a matrix.

## In plain words

Think of the iterations of a nest as points on a grid. Swapping two loops, running a loop backward, or sliding the rows of the grid are all ways of looking at the same points along new directions. Each of these views can be written as a small table of whole numbers, and doing two of them in a row is the same as multiplying their tables. A table of the right kind loses no point and adds no point. To know whether a new view is safe, take every arrow between two points that depend on each other, look at it through the table, and check that it still points forward. If all arrows point forward, the program gives the same result in the new order.

## When it applies

- **(T1) A perfect nest.** All statements are inside the innermost loop, and all of them are mapped by the same $T$.
- **(T2) Affine bounds.** The iteration space is $\{i \in \mathbb{Z}^k : A i \le b\}$ for an integer matrix $A$ and a vector $b$ that may contain symbolic sizes.
- **(T3) Known distances.** Every dependence has a constant distance vector, or a direction vector whose entries are handled with intervals as Wolf and Lam do.
- **(T4) Unimodular.** $T$ is an integer matrix with $\det T = \pm 1$.

The elementary matrices for two loops are:

| transformation | matrix $T$ | $T (d_1, d_2)$ |
|---|---|---|
| interchange | $\begin{pmatrix} 0 & 1 \\ 1 & 0 \end{pmatrix}$ | $(d_2, d_1)$ |
| reversal of the inner loop | $\begin{pmatrix} 1 & 0 \\ 0 & -1 \end{pmatrix}$ | $(d_1, -d_2)$ |
| skewing the inner loop by $f$ | $\begin{pmatrix} 1 & 0 \\ f & 1 \end{pmatrix}$ | $(d_1, d_2 + f d_1)$ |

Every unimodular integer matrix is a product of such elementary matrices, so the framework covers exactly the sequences of interchanges, reversals and skews.

## The template

```pseudo id=main
UNIMODULAR(nest with space {i : A i <= b}, body BODY(i), distances D, matrix T)
L1  if det T is not 1 or -1 then
L2      return "not unimodular"
L3  for each d in D do
L4      if T d is not lexicographically positive then
L5          return "illegal: T reverses a dependence"
L6  S <- inverse of T                                 ▷ an integer matrix, since det T = +-1
L7  the new space is {y : A S y <= b}
L8  eliminate y_k, ..., y_2 by Fourier-Motzkin to get the bounds of each y_l
L9  emit the nest over y_1, ..., y_k with body BODY(S y)
```

The holes are the nest, its distances and the matrix $T$. Choosing $T$ is the job of an algorithm on top of the framework: the [hyperplane method](/lamport-hyperplane-method/) builds a $T$ whose first row is a time function, the [Wolf-Lam algorithm](/wolf-lam-locality-algorithm/) builds one for locality, and Wolf and Lam's parallelization algorithm builds one with as many parallel loops as possible.

**Theorem.** The transformed nest keeps every dependence pair in order if and only if $T d \succ 0$ for every dependence distance $d$.

*Proof.* The new nest runs $i$ before $i'$ exactly when $T i \prec T i'$. Lexicographic order is compatible with addition, so $u \prec v$ holds exactly when $v - u \succ 0$. A dependence goes from $i$ to $i + d$, and $T(i + d) - T i = T d$. So the source runs first exactly when $T d \succ 0$. If this holds for every $d$, every pair keeps its order, and Theorem 1 of the [legality page](/loop-transformation-legality/) gives the same result. If $T d \prec 0$ for some $d$ (it is never $0$, because $T$ is invertible and $d \neq 0$), every pair with this distance has its sink run first. $\square$

**Why the determinant must be $\pm 1$.** If $T$ is an integer matrix with an integer inverse $S$, then $y = T i$ is an integer vector for every integer $i$, and $i = S y$ is an integer vector for every integer $y$. So the integer points of the new space $\{y : A S y \le b\}$ are exactly the images of the old iterations, one for one, and a nest that scans the integer points of the new space runs each old iteration once. An integer matrix has an integer inverse exactly when its determinant is $\pm 1$, because $\det T \cdot \det S = 1$ with both determinants integers. With $\det T = 2$, for example, half of the integer points of the new space have no preimage, and the code needs extra steps or guards.

**Composition.** If $T_1$ and $T_2$ are legal one after the other, the combined map is $T_2 T_1$, and its legality is again the single test $T_2 T_1 d \succ 0$. An intermediate step need not be legal for the product to be legal, which is why the framework finds sequences that the step-by-step tests reject.

## Classic examples

**A wavefront.** The nest `for i = 1 to n: for j = 1 to m: A[i][j] = A[i-1][j] + A[i][j-1] + A[i-1][j+1]` has the distances $(1, 0)$, $(0, 1)$ and $(1, -1)$. The test for three matrices:

| $T$ | $T(1, 0)$ | $T(0, 1)$ | $T(1, -1)$ | result |
|---|---|---|---|---|
| $\begin{pmatrix} 0 & 1 \\ 1 & 0 \end{pmatrix}$ | $(0, 1)$ | $(1, 0)$ | $(-1, 1)$ | illegal |
| $\begin{pmatrix} 1 & 1 \\ 1 & 0 \end{pmatrix}$ | $(1, 1)$ | $(1, 0)$ | $(0, 1)$ | legal, inner loop carries $(0, 1)$ |
| $\begin{pmatrix} 2 & 1 \\ 1 & 0 \end{pmatrix}$ | $(2, 1)$ | $(1, 0)$ | $(1, 1)$ | legal, inner loop parallel |

The third matrix is skewing by 2 followed by interchange. Its outer loop runs over $y_1 = 2i + j$, and every transformed distance has a positive first entry, so the inner loop is a [DOALL loop](/doall-loop/).

**Bounds by elimination.** Take $T = \begin{pmatrix} 1 & 1 \\ 1 & 0 \end{pmatrix}$, so $y_1 = i + j$ and $y_2 = i$. The inverse gives $i = y_2$ and $j = y_1 - y_2$. The old bounds $1 \le i \le n$ and $1 \le j \le m$ become $1 \le y_2 \le n$ and $y_1 - m \le y_2 \le y_1 - 1$. The inner bounds are $\max(1, y_1 - m) \le y_2 \le \min(n, y_1 - 1)$. Eliminating $y_2$ leaves $2 \le y_1 \le n + m$:

```
for y1 = 2 to n + m:
  for y2 = max(1, y1 - m) to min(n, y1 - 1):
    BODY(i = y2, j = y1 - y2)
```

**Reversal makes interchange legal.** A nest with the single distance $(1, -1)$ cannot be interchanged. The product of the inner reversal and the interchange, $\begin{pmatrix} 0 & -1 \\ 1 & 0 \end{pmatrix}$, maps $(1, -1)$ to $(1, 1)$, which is legal. The new outer loop runs $y_1 = -j$, that is, over $j$ backward.

**Completing a row.** For a parallel inner loop, an algorithm often fixes only the first row $\pi$ of $T$, a time function with $\pi \cdot d \ge 1$ for all $d$. If the entries of $\pi$ have greatest common divisor 1, the [extended Euclidean algorithm](/extended-euclidean-algorithm/), or the [Hermite normal form](/hermite-normal-form/) in higher dimensions, completes $\pi$ to a unimodular matrix. For $\pi = (3, 2)$, the rows $(3, 2)$ and $(1, 1)$ give determinant $3 - 2 = 1$.

## Variations

- **Direction vectors.** With entries like $+$ (any positive value) or $*$ (any value), $T d$ is an interval vector. Wolf and Lam test that it is lexicographically positive for every choice inside the intervals.
- **Non-unimodular maps.** An integer matrix with $|\det T| > 1$ can still be legal, but the new space has holes. The generated code steps by more than 1 or uses guards; the [Hermite normal form](/hermite-normal-form/) of $T$ gives the steps.
- **Tiling on top.** A unimodular $T$ that makes a band fully permutable, usually a skew, is followed by [tiling](/loop-tiling/), which is not a unimodular map.
- **One map per statement.** For imperfect nests and different maps for different statements, the [polyhedral model](/polyhedral-model/) replaces $T$ by one affine schedule per statement, found by solving the [affine scheduling problem](/affine-scheduling-problem/).

## Pitfalls

- **Testing the factors and not the product.** A sequence can be legal as a whole even when one step alone is illegal. Test the product.
- **Forgetting the determinant.** A matrix with determinant 2 passes the dependence test but makes the new nest scan points that are not iterations.
- **Copying the bounds.** The new bounds come from the inverse and elimination, not from the old bounds. They often contain `max` and `min` of several terms, and the outer bounds can need `ceil` and `floor` when a coefficient is not $\pm 1$.
- **Statements outside the inner loop.** The framework maps one perfect nest. A statement between the loop headers has no place in $y$ space; distribute it out first.
- **Equating a legal $T$ with a good one.** The test says nothing about locality or parallelism. The second matrix in the table above is legal, but its inner loop is still sequential.

## Exercises

1. Is $T = \begin{pmatrix} 1 & 0 \\ 1 & 1 \end{pmatrix}$ legal for the distances $(0, 1)$ and $(1, -1)$? *Answer.* $T(0, 1) = (0, 1)$ and $T(1, -1) = (1, 0)$, both positive, so yes.
2. Compute the product of skewing by 1 and then interchange, and apply it to $(1, -1)$. *Answer.* $\begin{pmatrix} 0 & 1 \\ 1 & 0 \end{pmatrix} \begin{pmatrix} 1 & 0 \\ 1 & 1 \end{pmatrix} = \begin{pmatrix} 1 & 1 \\ 1 & 0 \end{pmatrix}$, and $(1, -1)$ maps to $(0, 1)$.
3. Why is $T = \begin{pmatrix} 2 & 0 \\ 0 & 1 \end{pmatrix}$ not used, though it keeps every distance positive? *Answer.* $\det T = 2$. The new outer index $y_1 = 2i$ takes only even values, so a loop over all integers $y_1$ runs points that are not iterations.
4. Complete the row $\pi = (2, 3)$ to a unimodular matrix. *Answer.* Find $a, b$ with $2b - 3a = \pm 1$, for example $a = 1$, $b = 1$: $\begin{pmatrix} 2 & 3 \\ 1 & 1 \end{pmatrix}$ has determinant $2 - 3 = -1$.

## References
