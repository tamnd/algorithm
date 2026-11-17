---
tag: TCA3BR
kind: algorithm
slug: random-walker-segmentation
name: Random walker segmentation
aliases:
- Grady random walker
area: computer-vision/segmentation-and-recognition
level: advanced
summary: Label each pixel with the seed label that a random walk from it most likely reaches first. The probabilities solve a sparse Laplacian system with the seeds as boundary values.
solves: [interactive-segmentation]
model: real-ram
complexity:
  vars: {W: the image width in pixels, H: the image height in pixels, K: the number of labels}
  time: {worst: O(W^3 H^3 + K W^2 H^2), average: O(W^3 H^3 + K W^2 H^2), best: O(K W H)}
  space: {extra: O(W^2 H^2 + K W H)}
properties: {deterministic: true, exact: true, multi_label: true, interactive: true, soft_output: true}
history:
  year: 2006
  people: [Leo Grady]
  note: "Grady (IEEE TPAMI 2006) labeled pixels by first arrival probabilities of random walks to the seeds, computed as the solution of a combinatorial Dirichlet problem. A workshop version with Gareth Funka-Lea appeared in 2004."
prereqs: [interactive-segmentation, laplacian-matrix, markov-chain]
see_also: [boykov-jolly-graph-cuts, intelligent-scissors, grabcut, normalized-cut, conjugate-gradient-method, multigrid-method, closed-form-matting, image-matting]
sources:
  - paper: doi:10.1109/TPAMI.2006.233
    title: "Leo Grady, Random walks for image segmentation, IEEE TPAMI 28(11), 1768-1783, 2006"
    locator: "Section 3.1 (edge weights, equation 1), Section 3.2 (combinatorial Dirichlet problem, equations 6 to 12), Section 3.6 (numerical practicalities), Section 3.7 (algorithm summary), Section 4.3 (properties and Proposition 1)"
  - book: isbn:978-1-84882-934-3
    title: "Richard Szeliski, Computer Vision: Algorithms and Applications, 1st edition, Springer, 2011"
    locator: "Chapter 5, Segmentation"
---

Random walker segmentation is an algorithm that splits an image into $K$ regions from a few pixels that the user marks with labels, the *seeds*. Picture a walker that starts at an unmarked pixel and steps to a neighbor at random. It prefers steps between pixels of similar brightness. Each pixel gets the label of the seed that its walker most likely reaches first. These probabilities need no simulation: they solve one sparse linear system per label, with the graph Laplacian of the image and the seeds as fixed values. The result is a probability for each pixel and label, and it is the exact solution of the system, not a local optimum.

## In plain words

The user marks a few pixels inside each object and a few in the background. Now think of the image as a field of small rooms with doors between neighbors. A door is wide when the two pixels have similar brightness, and narrow when there is an edge between them. A person starts in an unmarked room and walks through doors at random until they reach a marked room. They pass wide doors more often than narrow ones.

For each unmarked pixel, the program finds how likely the walk ends at each kind of mark. The pixel joins the mark with the best chance. Strong edges hold walkers back, so the borders between regions follow the edges. The program finds all chances at once by solving one set of equations.

## The problem

The input is a gray image $I$ with $n = WH$ pixels, a set $M$ of seed pixels, a label $\ell(j) \in \{1, \dots, K\}$ for each seed $j$, and a parameter $\beta > 0$. The pixels are the nodes of a 4-connected grid graph. The output is, for each pixel $i$ and label $s$, the probability $x^s_i$ that a random walk from $i$ reaches a seed of label $s$ before any other seed, and the label $\arg\max_s x^s_i$. The problem is [interactive segmentation](/interactive-segmentation/) with labels as seeds.

The walk moves from $i$ to a neighbor $j$ with probability $w_{ij} / d_i$, where $d_i = \sum_j w_{ij}$ is the degree. Grady (2006, equation 1) uses the weights
$$w_{ij} = \exp\bigl(-\beta\, (g_i - g_j)^2\bigr),$$
where $g_i$ is the gray value. He normalizes the squared differences first but does not fix how. The code of this page divides them by the largest squared difference in the image, so $\beta$ does not depend on the gray scale.

## The algorithm

Order the pixels with the seeds $M$ first and the free pixels $U$ after them. The Laplacian $L = D - W$ then has the blocks
$$L = \begin{pmatrix} L_M & B \\ B^T & L_U \end{pmatrix}.$$
For a label $s$, the vector $m^s$ on the seeds has $m^s_j = 1$ if $\ell(j) = s$ and $0$ otherwise. The probabilities of label $s$ on the free pixels solve (Grady 2006, equation 10)
$$L_U\, x^s_U = -B^T m^s .$$

```pseudo id=main
RANDOM-WALKER(I, seeds, β)
L1  for each grid edge {i, j} do w_ij ← exp(-β (g_i - g_j)² / max (g_p - g_q)²)
L2  L ← D - W                          ▷ sparse, 5 entries per row
L3  split the pixels into seeds M and free pixels U; take the blocks L_U and B
L4  for s ← 1 to K - 1 do m^s_j ← 1 if ℓ(j) = s else 0, for j in M
L5  for s ← 1 to K - 1 do solve L_U x^s_U = -B^T m^s
L6  x^K ← 1 - Σ_{s<K} x^s
L7  for each pixel i do label_i ← argmax_s x^s_i
L8  return x, label
```

Line L6 saves one solve: the probabilities of each pixel sum to 1, so the last label needs no system of its own (Theorem 1 of the proof). All $K - 1$ systems in line L5 have the same matrix, so one factorization serves all of them.

## Example

Take one row of five pixels with the gray values $10, 20, 60, 70, 80$, a seed of label 0 at pixel 0, a seed of label 1 at pixel 4, and $\beta = 2$. The squared differences are $100, 1600, 100, 100$. Divided by the largest, they are $1/16, 1, 1/16, 1/16$, so the weights are
$$e^{-1/8} = 0.8825,\quad e^{-2} = 0.1353,\quad 0.8825,\quad 0.8825 .$$
On a chain the system is a set of resistors in series. Each edge is a resistor of resistance $1 / w$: $1.1331$, $7.3891$, $1.1331$, $1.1331$, with the sum $10.7885$. The probability of label 1 at a pixel is the resistance between pixel 0 and that pixel, divided by the total:

| pixel | 0 | 1 | 2 | 3 | 4 |
|---|---|---|---|---|---|
| value | 10 | 20 | 60 | 70 | 80 |
| $x^1$ | 0 | 0.1050 | 0.7899 | 0.8950 | 1 |
| label | 0 | 0 | 1 | 1 | 1 |

The big step of the probability is at the weak edge between pixels 1 and 2, where the gray value jumps by 40. The labels are $0, 0, 1, 1, 1$. The test file checks these numbers, and it checks the resistor formula.

## Correctness

The full proof is in [proofs/correctness.md](proofs/correctness.md). It needs positive weights and at least one seed in each connected part of the graph. A grid is connected, so one seed is enough there.

- **Theorem (one solution).** $L_U$ is symmetric positive definite, so each system of line L5 has exactly one solution.
- **Theorem (energy).** The solution is the only minimizer of the Dirichlet energy $D[x] = \frac12 \sum w_{ij} (x_i - x_j)^2$ with the seeds fixed. This is equation 6 of the paper.
- **Theorem (random walk).** The solution equals the probability that the walk from $i$ first reaches a seed of label $s$.
- **Theorem (range and sum).** Each $x^s_i$ lies in $[0, 1]$, by the maximum principle, and $\sum_s x^s_i = 1$, which justifies line L6.
- **Theorem (two labels give connected segments).** With $K = 2$, each pixel with label $s$ is joined to a seed of label $s$ through pixels with label $s$. This is Proposition 1 of the paper for $K = 2$.

For $K \ge 3$ that last statement is false, although Grady states it for any $K$. The proof file gives a graph of seven nodes where a node gets label 0 and none of its neighbors does. The test file builds the same pattern on a $2 \times 5$ image.

## Complexity

The cost model is the [real-RAM](/real-ram/), with exact arithmetic on real numbers. Let $n = WH$. Lines L1 to L4 and L6 to L7 cost $O(Kn)$ time. Line L5 dominates.

- **Dense elimination, as in the code.** One LU factorization of $L_U$ costs $O(n^3)$ time and $O(n^2)$ space, and each of the $K - 1$ right sides costs $O(n^2)$. The total is $O(W^3 H^3 + K W^2 H^2)$, the bound in the front matter. The best case is when almost all pixels are seeds, so that $L_U$ is tiny. This is a theorem about the code.
- **Sparse direct solve.** $L_U$ has at most 5 nonzeros per row. With nested dissection on a 2D grid, the factorization costs $O(n^{3/2})$ time and $O(n \log n)$ space (George 1973). This is a theorem for grid graphs.
- **Conjugate gradients.** Each iteration costs $O(n)$. The number of iterations to reduce the error by a factor $\epsilon$ is $O(\sqrt{\kappa} \log(1/\epsilon))$, where $\kappa$ is the condition number of $L_U$. This is a theorem, but $\kappa$ grows with $\beta$ and with the image size, so the bound gives no fixed count.
- **Multigrid.** Grady writes that algebraic multigrid gives near-optimal performance on these systems. That is a claim from experience, not a bound.

Grady reports 2.5 seconds for a $256 \times 256$ image with two seeds with a direct sparse solver in MATLAB on a 2.4 GHz Xeon. That is a benchmark result.

## Properties

- **Soft output.** Each pixel gets a probability for each label, not only a label. The probabilities show where the result is uncertain.
- **Any number of labels.** One extra solve per label, with the same matrix.
- **Weak edges.** Where an edge has a gap, the probability changes smoothly across the gap, and the border tends to close it in a natural way.
- **Less pull toward short borders.** The cut of [Boykov-Jolly](/boykov-jolly-graph-cuts/) can wrap tightly around a small seed, because short cuts are cheap. The random walker has no cost that grows with the length of the border, so this effect is weaker. That is a heuristic observation, not a theorem.
- **Harmonic.** At each free pixel, each $x^s$ is the weighted mean of its neighbors.
- **Seeds matter.** The result depends on where the seeds are, not only on the image. In a flat region, a pixel tends to take the label of the nearest seeds.

## Variants and improvements

- **Color and other features.** Replace $(g_i - g_j)^2$ by $\lVert g_i - g_j \rVert^2$ for color vectors, as the paper suggests.
- **Solvers.** Preconditioned [conjugate gradients](/conjugate-gradient-method/), algebraic [multigrid](/multigrid-method/) and GPU solvers. Grady's Section 3.6 lists these options.
- **Matting.** The [closed-form matting](/closed-form-matting/) method solves the same kind of system, with a different Laplacian, to get a soft alpha matte.
- **Link to cuts.** Later work views the random walker, the graph cut and shortest path methods as one energy with different powers on the weights and on the differences.

## When to use it

Use it for interactive segmentation with several labels, for images with weak or broken edges, and when a probability per pixel is useful, as in medical images. Use [Boykov-Jolly graph cuts](/boykov-jolly-graph-cuts/) for two labels when a hard, short boundary is wanted and the edges are strong. Use [intelligent scissors](/intelligent-scissors/) when the user prefers to trace the boundary. For soft borders such as hair, use [image matting](/image-matting/).

## Pitfalls

- **A large $\beta$ gives a near-singular system.** Weights such as $e^{-30}$ make $L_U$ close to singular, and the solution loses digits. The test file uses moderate values of $\beta$; Grady used $\beta = 900$ with his own normalization.
- **Normalization of the differences.** The value of $\beta$ only means something together with the scale of $(g_i - g_j)^2$. State the normalization with the value.
- **A part of the graph without seeds.** If some connected part has no seed, $L_U$ is singular. A grid is connected, but a graph with zero weights, or a mask that cuts the image, can break this.
- **Ties.** When two labels have equal probability at a pixel, the argmax picks one by its rule. Grady's connectivity result needs strict inequality.
- **More than two labels.** A segment need not touch a seed of its own label, as the correctness section shows.
- **Dense matrices.** The code of this page uses a dense matrix, so it suits small images only. Real images need a sparse solver.

## Implementations

The Python code in `impl/python/random_walker_segmentation.py` builds the weights and the Laplacian of lines L1 and L2 on a 4-connected grid and solves line L5 with the dense solver of `cvla.py`. It also has a function that solves all $K$ systems, a conjugate gradient solver, the Dirichlet energy and a Monte Carlo simulation of the walk. The tests check the resistor example above, the sum rule against $K$ separate solves, the range $[0, 1]$, the mean value property, the minimum of the Dirichlet energy, the agreement with simulated walks, the connectivity for two labels, the counterexample for three labels, and the agreement of conjugate gradients with the direct solve.

## History

Kakutani (1945) linked the Dirichlet problem to Brownian motion: the solution at a point is the expected boundary value where a random path from that point first hits the boundary. Doyle and Snell (1984) explained the discrete version, with random walks on graphs and electric networks, in a short book. Grady and Funka-Lea (2004) used these potentials for multi-label segmentation of medical images, and Grady (2006) gave the full method, with the circuit analogy, the numerics and the properties. The method became a standard tool in medical image analysis and a reference point for later work that joins graph cuts, random walks and shortest paths in one framework.

## References
