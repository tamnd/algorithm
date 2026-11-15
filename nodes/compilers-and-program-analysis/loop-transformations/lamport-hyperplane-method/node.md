---
tag: RCRHT9
kind: algorithm
slug: lamport-hyperplane-method
name: Lamport hyperplane method
area: compilers-and-program-analysis/loop-transformations
level: advanced
summary: Finds a linear time function such that all iterations on one hyperplane can run in parallel, for loops with uniform dependences.
model: word-ram
complexity:
  vars: {k: the depth of the loop nest, D: the number of distance vectors, N: the number of iterations}
  time: {worst: O(D k + N k)}
  space: {extra: O(k)}
properties: {deterministic: true, recursive: false}
prereqs: [dependence-distance-vector, unimodular-transformations, fourier-motzkin-elimination]
see_also: [loop-skewing, wavefront-parallelism, unimodular-matrix, affine-scheduling-problem, feautrier-scheduling, doall-loop, loop-tiling, polyhedral-scanning]
sources:
  - paper: doi:10.1145/360827.360844
    title: Leslie Lamport, The parallel execution of DO loops, Communications of the ACM 17(2), 1974, 83-93
    locator: the hyperplane method (a linear function of the loop indices whose level sets can run at the same time, and the change of loop indices that makes it the outer loop) and the coordinate method
  - paper: doi:10.1007/BF01407876
    title: Michael Wolfe, Loop skewing, the wavefront method revisited, International Journal of Parallel Programming 15(4), 1986, 279-293
    locator: the wavefront method obtained as loop skewing followed by loop interchange, and its relation to Lamport's hyperplanes
  - paper: doi:10.1109/71.97902
    title: Michael E. Wolf and Monica S. Lam, A loop transformation theory and an algorithm to maximize parallelism, IEEE Transactions on Parallel and Distributed Systems 2(4), 1991, 452-471
    locator: wavefront transformations as unimodular matrices whose first row has a positive product with every dependence vector, and the completion of that row to a unimodular matrix
---

The hyperplane method takes a perfect loop nest whose dependences have constant [distance vectors](/dependence-distance-vector/) and finds an integer *time function* $t(i) = \pi \cdot i$ with $\pi \cdot d \ge 1$ for every distance $d$. All iterations with the same value of $t$ lie on one hyperplane, and no dependence joins two of them, so each hyperplane, a *front*, can run as one parallel step. The fronts run in increasing $t$. The method completes $\pi$ to a [unimodular matrix](/unimodular-matrix/) $T$ and rewrites the nest as an outer sequential loop over $t$ and inner loops that are all parallel, with bounds from [Fourier-Motzkin elimination](/fourier-motzkin-elimination/). Lamport introduced it in 1974 for the parallel computers of that time; the same fronts come out of [loop skewing](/loop-skewing/) followed by interchange, and they are the [wavefronts](/wavefront-parallelism/) of a stencil.

## In plain words

Picture a grid of tasks in which each task needs results from a few nearby tasks that come before it. You want to do many tasks at the same moment. Give each task a time: a weighted sum of its row and column numbers. Choose the weights so that every task's time is larger than the time of every task it needs. Then all tasks with the same time can run together, because none of them needs another one of them. On a grid, the tasks with the same time lie on a slanted line, and the lines sweep across the grid one after the other. The method gives a simple rule to pick the weights, starting from the innermost loop.

## The problem

**Input.** A perfect nest of depth $k$ with iteration space $P = \{i \in \mathbb{Z}^k : A i + b \ge 0\}$, bounded, and a finite set $D$ of nonzero dependence distance vectors, each lexicographically positive. The body of one iteration runs as a unit.

**Output.** An integer vector $\pi$ with $\pi \cdot d \ge 1$ for every $d \in D$, and a rewritten nest that runs the fronts $F_t = \{i \in P : \pi \cdot i = t\}$ in increasing $t$, each front as a parallel loop.

A dependence with a distance that is not constant, or a nest with statements between the loop headers, is outside the method. The distances come from a [dependence test](/dependence-testing/).

## The algorithm

```pseudo id=main
HYPERPLANE(space P = {i : A i + b >= 0}, distances D)
L1  pi_k <- 1
L2  for l <- k - 1 down to 1 do
L3      need <- 0
L4      for each d in D with d_1 = ... = d_(l-1) = 0 and d_l > 0 do
L5          rest <- pi_(l+1) d_(l+1) + ... + pi_k d_k
L6          need <- max(need, ceil((1 - rest) / d_l))
L7      pi_l <- need
L8  T <- the matrix with rows pi, e_1, ..., e_(k-1)            ▷ det T = +-1
L9  for t <- tmin to tmax do                                    ▷ bounds of y_1 by Fourier-Motzkin on {y : A T^(-1) y + b >= 0}
L10     parallel for (i_1, ..., i_(k-1)) in the bounds of front t do
L11         i_k <- t - (pi_1 i_1 + ... + pi_(k-1) i_(k-1)); BODY(i_1, ..., i_k)
```

Lines L1 to L7 build $\pi$ from the innermost loop outward. At level $l$, the only distances that $\pi_l$ can still fix are those whose first nonzero entry is at $l$; for each of them, line L6 asks for the smallest $\pi_l$ with $\pi_l d_l + \text{rest} \ge 1$. Distances that lead at a deeper level already have their value, and distances that lead at an outer level will be fixed there. Line L8 adds the unit rows, which makes $T$ unimodular because $\pi_k = 1$. In the new coordinates $y = T i$, the first coordinate is the time and the others are $i_1, \dots, i_{k-1}$, so line L11 recovers $i_k$ from $t$. The bounds of lines L9 and L10 come from Fourier-Motzkin elimination of the constraints rewritten with $i = T^{-1} y$.

## Example

The stencil

```
for i = 1 to 4:
  for j = 1 to 5:
    A[i][j] = A[i-1][j] + A[i][j-1] + A[i-1][j+1]
```

has the distances $(1, 0)$, $(0, 1)$ and $(1, -1)$. Line L1 sets $\pi_2 = 1$. At $l = 1$, the distances that lead at level 1 are $(1, 0)$, with rest $0$ and need $\lceil 1/1 \rceil = 1$, and $(1, -1)$, with rest $-1$ and need $\lceil 2/1 \rceil = 2$. So $\pi = (2, 1)$ and $t = 2i + j$. The three distances get $\pi \cdot d = 2, 1, 1$. With $T = \begin{pmatrix} 2 & 1 \\ 1 & 0 \end{pmatrix}$, the inverse is $i = y_2$ and $j = t - 2 y_2$, and the bounds $1 \le i \le 4$, $1 \le t - 2i \le 5$ give:

```
for t = 3 to 13:
  parallel for i = max(1, ceil((t - 5) / 2)) to min(4, floor((t - 1) / 2)):
    j = t - 2i
    A[i][j] = A[i-1][j] + A[i][j-1] + A[i-1][j+1]
```

| $t$ | front | $t$ | front |
|---|---|---|---|
| 3 | (1,1) | 9 | (2,5), (3,3), (4,1) |
| 4 | (1,2) | 10 | (3,4), (4,2) |
| 5 | (1,3), (2,1) | 11 | (3,5), (4,3) |
| 6 | (1,4), (2,2) | 12 | (4,4) |
| 7 | (1,5), (2,3), (3,1) | 13 | (4,5) |
| 8 | (2,4), (3,2) | | |

The 20 iterations fall into 11 fronts, of at most 3 iterations each. In the front $t = 7$, the differences between the iterations are $(1, -2)$ and $(2, -4)$, which are not distances, so the three iterations are independent. A brute-force search over $\pi \in \{0, \dots, 4\}^2$ finds no valid time function with fewer than 11 fronts for this nest.

## Correctness

The full proof is in [proofs/correctness.md](proofs/correctness.md). It has three steps.

**The time function is valid.** Take $d \in D$ with first nonzero entry at level $l$. If $l = k$, then $\pi \cdot d = d_k \ge 1$. Otherwise $\pi \cdot d = \pi_l d_l + r$, where $r$ is the value of rest in line L5 for this $d$, and line L6 gives $\pi_l \ge (1 - r)/d_l$, so $\pi_l d_l + r \ge 1$. So a time function exists as soon as all distances are lexicographically positive, which every real dependence distance is.

**The rewritten nest visits each iteration once, front by front.** $T$ has determinant $\pm 1$: moving its first row to the bottom gives a lower triangular matrix with ones on the diagonal. So $y = T i$ is a bijection of the integer points, and the Fourier-Motzkin bounds scan the integer points of the transformed space exactly once, in lexicographic order, with $y_1 = t$ outermost.

**The fronts keep every dependence.** A dependence from $i$ to $i + d$ has $t(i + d) = t(i) + \pi \cdot d \ge t(i) + 1$, so its sink is in a strictly later front. No dependence joins two iterations of one front, so they can run in any order or at the same time, and by Theorem 1 of the [legality page](/loop-transformation-legality/) the result equals that of the original nest.

## Complexity

Building $\pi$ looks at each distance once, at its leading level, and computes rest in $O(k)$: $O(D k)$ time. The scan does $O(k)$ work per iteration for the bounds and for $i_k$, so $O(N k)$ in total. The Fourier-Motzkin elimination is done once for the nest; its cost depends on $k$ and on the number of constraints, not on $N$ or $D$, and it can grow fast with $k$, but loop nests are shallow. The extra space is $O(k)$ for $\pi$ and the indices. The number of fronts is the number of distinct values of $\pi \cdot i$ over $P$, at most $\sum_l \pi_l (U_l - L_l) + 1$ on a box with bounds $L_l \le i_l \le U_l$, since every $\pi_l \ge 0$.

## Properties

- **Exact legality, no search.** The construction always succeeds on lexicographically positive distances and needs no linear program.
- **Nonnegative coefficients.** Every $\pi_l \ge 0$ and $\pi_k = 1$.
- **One parallel level.** The result has one sequential loop and $k - 1$ parallel loops, with a barrier between fronts.
- **Not minimal.** The number of fronts is not always the smallest possible, as shown below.

## Variants and improvements

- **Fewer fronts.** Choosing $\pi$ to minimize the number of fronts is an integer program: minimize the spread of $\pi \cdot i$ over $P$ subject to $\pi \cdot d \ge 1$. The construction can be far from it. For the single distance $(1, -3)$ on the box $1 \le i, j \le 4$, it gives $\pi = (4, 1)$ and 16 fronts of one iteration, a sequential nest, while $\pi = (1, 0)$ gives 4 fronts of 4 iterations: the inner loop is already parallel. The implementation contains a brute-force search over small $\pi$ for such comparisons. A real compiler solves a [linear program](/linear-programming-problem/) with a rounding step, or an [integer program in fixed dimension](/integer-programming-fixed-dimension/).
- **Completion of any $\pi$.** When $\pi_k \ne 1$ but the entries of $\pi$ have greatest common divisor 1, a unimodular completion still exists, through the [Hermite normal form](/hermite-normal-form/); [unimodular transformations](/unimodular-transformations/) describes the code generation.
- **Skewing and interchange.** For two loops, $t = f i + j$ is skewing by $f$ followed by interchange, as on the [loop skewing](/loop-skewing/) page.
- **Affine schedules.** Allowing a different time function per statement, with a constant term, and dependences that are not uniform, gives the [affine scheduling problem](/affine-scheduling-problem/). [Feautrier's scheduling](/feautrier-scheduling/) solves it with linear programming, one dimension or several.
- **Tiled wavefronts.** On a fully permutable band, [tiling](/loop-tiling/) first and then running the tiles by a time function gives fronts of tiles, with much less synchronization than fronts of single iterations.

## When to use it

Use it for a perfect nest with uniform dependences in which no loop is parallel by itself, such as a Gauss-Seidel sweep or a dynamic programming table filled from its upper and left neighbours. The fronts give parallelism of about the size of a cross-section of the space. If some loop already carries no dependence, a [DOALL loop](/doall-loop/) over it is simpler and has no barriers. If the dependences are not uniform, or the nest is not perfect, use the [polyhedral model](/polyhedral-model/). On machines where a barrier is expensive, tile first.

## Pitfalls

- **Floor instead of ceiling in line L6.** With a floor, $\pi_l d_l + \text{rest}$ can be $0$ and two dependent iterations land in the same front.
- **A wrong filter in line L4.** Line L6 divides by $d_l$, which is safe only when $d_l > 0$. A distance with $d_l < 0$ must not enter line L6 at level $l$: it leads at an outer level, and it gets its value there. Skipping a distance that does lead at $l$ leaves it without a check, and its $\pi \cdot d$ can be $0$ or negative.
- **A zero distance in $D$.** A dependence inside one iteration has $d = 0$ and can never get $\pi \cdot d \ge 1$. Line L4 must see only nonzero distances; the order inside the body is kept by running each iteration as a unit.
- **Box bounds in lines L9 and L10.** The fronts are slanted, so the bounds of the original loops are wrong for them. Copying them visits points outside the space or misses some.
- **Sign of the last index in line L11.** $i_k = t - \sum_{l<k} \pi_l i_l$; with a plus sign the body runs at the wrong iteration.
- **Expecting balance.** In the example, the first and last fronts have one iteration each. The parallel run takes at least one step per front, however many processors there are, and the small fronts near the corners leave most processors idle.

## Implementations

## History

Leslie Lamport's 1974 paper in the Communications of the ACM studied when the iterations of a Fortran DO loop nest can run at the same time on a parallel or array machine. It gave two methods. The *coordinate method* finds a loop whose iterations can run in parallel. The *hyperplane method* finds a linear function of the loop indices whose level sets, hyperplanes in the iteration space, can run in parallel, and it changes the loop indices so that this function becomes the outer loop. Michael Wolfe showed in 1986 that the same wavefronts come from loop skewing followed by loop interchange, which put the method into the vocabulary of restructuring compilers. Wolf and Lam in 1991 described it as a unimodular transformation whose first row has a positive product with every dependence vector. Feautrier's work on affine schedules in 1992 generalized it to non-uniform dependences and one time function per statement.

## References
