---
tag: 8AZ5A6
kind: algorithm
slug: pluto-algorithm
name: Pluto algorithm
aliases:
- Bondhugula tiling hyperplanes
area: compilers-and-program-analysis/loop-transformations
level: research
summary: Finds affine transformations that allow tiling and parallelism by minimizing a bound on dependence distances with integer linear programming.
model: word-ram
complexity:
  vars: {s: the number of statements, d: the depth of the deepest loop nest, e: the number of dependence edges, I: the cost of one integer linear program solve (exponential in the worst case)}
  time: {worst: O((s d + e) I)}
  space: {extra: O(e d)}
properties: {deterministic: true, recursive: false}
prereqs: [lexicographic-order, linear-programming-problem, simplex-method, farkas-lemma, polyhedral-model, loop-tiling, affine-scheduling-problem]
see_also: [feautrier-scheduling, lamport-hyperplane-method, loop-skewing, loop-fusion, wavefront-parallelism, polyhedral-scanning, unimodular-transformations, tarjan-scc]
sources:
  - paper: doi:10.1145/1375581.1375595
    title: Uday Bondhugula, Albert Hartono, J. Ramanujam and P. Sadayappan, A practical automatic polyhedral parallelizer and locality optimizer, PLDI 2008, 101-113
    locator: the tiling legality constraint, the cost function as a bound u.n + w on the dependence distances, its linearization with Farkas' lemma, the lexicographic minimum, the linear independence constraints, and the iterative algorithm with cuts between strongly connected components
  - paper: doi:10.1007/978-3-540-78791-4_9
    title: Uday Bondhugula, Muthu Baskaran, Sriram Krishnamoorthy, J. Ramanujam, Atanas Rountev and P. Sadayappan, Automatic transformations for communication-minimized parallelization and locality optimization in the polyhedral model, Compiler Construction (CC) 2008, LNCS, 132-146
    locator: the reading of the dependence distance along a tiling hyperplane as communication volume for parallel hyperplanes and as reuse distance for sequential ones, and the bounding function
  - book: isbn:9780471982326
    title: Alexander Schrijver, Theory of Linear and Integer Programming, Wiley, 1986
    locator: Corollary 7.1h (the affine form of Farkas' lemma)
---

The Pluto algorithm finds an affine transformation of a loop program whose outer loops can be tiled and run in parallel. Uday Bondhugula and his coauthors published it in 2008. It builds the new loops one hyperplane at a time. Each hyperplane is an affine form $\phi_S$ per statement that must keep every remaining dependence nonnegative, so that a band of such hyperplanes can be [tiled](/loop-tiling/). Among the legal hyperplanes it picks one that minimizes a bound $u \cdot N + w$ on the dependence distances along it, by integer linear programming. A small distance means little communication between tiles that run in parallel, or short reuse distances for tiles that run in sequence. The constraints on whole dependence polyhedra become linear with the affine form of [Farkas' lemma](/farkas-lemma/), as in [Feautrier's scheduling](/feautrier-scheduling/). Pluto is the base of the source-to-source compiler of the same name and of many later polyhedral optimizers.

## In plain words

A program has loops, and some runs of its statements depend on others. We want to cut the work into blocks, like tiles on a floor, that fit in the cache, and run some blocks at the same time. Cutting is safe when, along each new loop direction, every needed value comes from the same block or from a block that is already done. Pluto looks for such directions one at a time. Among the safe ones, it prefers the direction in which a value travels the shortest way, because short trips mean less data moves between blocks. Each choice is a small integer optimization problem. When no new safe direction exists, Pluto splits the statements into groups that can run one after the other, and starts again.

## The problem

**Input.** A static control program with integer parameters $N$ in a context $K$. Statement $S$ has depth $d_S$ and a domain $D_S$, a polyhedron that is bounded for each $N$. A set $E$ of dependence edges $e : S \to T$ with polyhedra $P_e$ of pairs $(\vec{s}, \vec{t})$ such that $T(\vec{t})$ must run after $S(\vec{s})$. This page uses memory-based dependences (flow, anti and output), one polyhedron per pair of accesses and per depth, as in the [affine scheduling problem](/affine-scheduling-problem/).

**Output.** For each statement, a list of affine forms $\Phi_S = (\phi^1_S, \dots, \phi^m_S)$ such that $\Phi_S(\vec{s}) <_{\mathrm{lex}} \Phi_T(\vec{t})$ on every $P_e$, grouped into *bands* of consecutive hyperplanes. Inside a band, every hyperplane has $\phi_T(\vec{t}) - \phi_S(\vec{s}) \ge 0$ on every dependence that the earlier dimensions do not already order. Such a band is fully permutable, and it can be tiled. Each statement gets $d_S$ linearly independent hyperplanes, so the transformation is one-to-one on its domain.

**Hyperplanes.** A hyperplane is $\phi_S(\vec{i}) = c_S \cdot \vec{i} + c_{S,0}$ with integer $c_S \ge 0$ and $c_{S,0} \ge 0$. For an edge $e$, the *distance along* $\phi$ is $\delta_e(\vec{s}, \vec{t}) = \phi_T(\vec{t}) - \phi_S(\vec{s})$.

## The algorithm

For each hyperplane, Pluto solves one integer linear program. Its unknowns are the coefficients $c_S$, $c_{S,0}$ of every statement, the bound $u \ge 0$ (one entry per parameter) and $w \ge 0$, and the Farkas multipliers. For every remaining edge it asks

$$\delta_e(\vec{s}, \vec{t}) \ge 0 \quad\text{and}\quad u \cdot N + w - \delta_e(\vec{s}, \vec{t}) \ge 0 \qquad \text{on } P_e.$$

Each of the two conditions is "an affine form in $\vec{s}$, $\vec{t}$, $N$ is nonnegative on $P_e$". By the affine Farkas lemma it holds exactly when the form equals $\lambda_0 + \sum_i \lambda_i c_{e,i}$ with $\lambda \ge 0$, where the $c_{e,i} \ge 0$ are the constraints of $P_e$. Matching the coefficients gives linear equations in all the unknowns.

Two more constraints stop the solver from returning zero or repeating a hyperplane. Let $H_S$ be the matrix of the hyperplanes already found for $S$, and $H_S^\perp = I - H_S^T (H_S H_S^T)^{-1} H_S$, the projection onto its orthogonal complement. For each statement that is not yet full rank, Pluto asks $h \cdot c_S \ge 0$ for every row $h$ of $H_S^\perp$ and $\sum_h h \cdot c_S \ge 1$. With no hyperplane found yet, this is $\sum_j c_{S,j} \ge 1$.

```pseudo id=main
PLUTO(program)
L1  E <- the dependence polyhedra of the program; H_S <- empty for each S; the current band is empty
L2  while E is not empty or some H_S has rank less than d_S do
L3      if some H_S is not full: phi, u, w <- the integer lexmin of (u, w, sum of c, sum of c0) with, for e in E, 0 <= delta_e <= u.N + w on P_e (Farkas), and the independence rows
L4      if a solution exists then append phi to the band and to H_S for each S that is not full; continue
L5      if the band is not empty then close it: E <- E minus the edges that some hyperplane of the band strongly satisfies; continue
L6      if E has edges between different strongly connected components then append a scalar dimension with the topological index of the component of S, and remove those edges
L7      else if E is not empty then append place p of the original schedule, p the least place that orders an edge of E, and remove the edges it strongly satisfies
L8      else append, for each S that is not full, a unit vector independent of H_S
L9  close the last band
L10 return the dimensions and the bands
```

**The objective.** The lexicographic minimum puts $u$ first. When $u = 0$, every distance along the hyperplane is a constant at most $w$. When also $w = 0$, no dependence crosses the hyperplane at all, and the loop is parallel with no communication. The sums of the coefficients come next, to keep the loops simple. The implementation bounds every coefficient by 4, $u$ by 4 and $w$ by 30, as Pluto bounds its coefficients. Since all unknowns are then bounded integers, it turns the lexicographic order into one weighted sum, with a last small term that breaks ties toward the original loop order. It finds the integer optimum by branch and bound over an exact simplex method. Pluto itself solves the same problem with parametric integer programming.

**Satisfied edges.** An edge is *strongly satisfied* by $\phi$ if $\delta_e \ge 1$ on $P_e$. The coefficients are integers, so $\delta_e$ is an integer at integer points, and a positive rational minimum of $\delta_e$ over $P_e$ is enough. Edges leave $E$ only when a band closes (line L5), not after each hyperplane. So every hyperplane of a band has $\delta_e \ge 0$ on all edges that were in $E$ when the band began, which is what tiling needs.

**When the solver fails.** If no hyperplane exists, Pluto closes the band. If that removes no edge, it cuts the dependence graph between its [strongly connected components](/tarjan-scc/) and orders them by a scalar dimension (line L6), which is a [loop distribution](/loop-distribution/). Line L7 is a safety net of this implementation for a single component: it reuses one component of the original loop order, which weakly satisfies all remaining edges and strongly satisfies at least one, by the argument on the [Feautrier scheduling](/feautrier-scheduling/) page. Line L8 completes the rank once no edge is left, which is always legal.

## Example

**Gauss-Seidel in one dimension.** The loop `for t = 0 to N: for i = 1 to N-1: A[i] = (A[i-1] + A[i] + A[i+1]) / 3` has dependences in the directions $(0, 1)$, $(1, 0)$, $(1, 1)$ and $(1, -1)$ in $(t, i)$.

- First hyperplane. $\phi = i$ is illegal, because the direction $(1, -1)$ gives $\delta = -1$. $\phi = t$ is legal. With memory-based dependences, the write of `A[i]` at time $t$ conflicts with the accesses at every later time, so $\delta$ reaches $N$, and the solver returns $\phi = t$ with $u = 1$, $w = 0$.
- Second hyperplane. It must be independent of $(1, 0)$, so $c_i \ge 1$, and $(1, -1)$ forces $c_t \ge c_i$. The cheapest choice is $\phi = t + i$, with $u = 1$, $w = 1$.

The band $(t, t + i)$ is a time skewing of the loop. Both hyperplanes keep all dependences nonnegative, so the band can be tiled with rectangular tiles in the skewed space. This is the classic result for stencils, also reached by hand with [loop skewing](/loop-skewing/). With exact dataflow dependences, only nearby time steps are linked, and the distances become constants.

**Two-dimensional stencil.** For `A[i][j] = A[i-1][j] + A[i][j-1]`, the hyperplanes are $i$ and $j$ with $u = 0$ and $w = 1$. The original loops are already a tilable band.

**Fusion with a shift.**

```
for i = 1 to N:  S1: B[i] = A[i]
for i = 1 to N:  S2: C[i] = B[i-1] + B[i+1]
```

A fused loop with $\phi_{S1} = \phi_{S2} = i$ is illegal, because $S2(i)$ reads `B[i+1]`, which $S1(i+1)$ writes later. Pluto returns $\phi_{S1} = i$ and $\phi_{S2} = i + 1$, a [fusion](/loop-fusion/) with a shift, with $u = 0$ and $w = 2$. The edge is not strongly satisfied, because $S2(i-1)$ reads `B[i]` in the same new iteration $i$ as $S1(i)$ writes it. A scalar dimension (0 for $S1$, 1 for $S2$) puts $S1$ first inside the fused loop. The result is $\Phi_{S1} = (i, 0)$ and $\Phi_{S2} = (i + 1, 1)$, one loop in which `B[i]` is used right after it is written.

**Matrix multiplication.** For `C[i][j] = 0` followed by a $k$ loop with `C[i][j] += A[i][k] * B[k][j]`, the first two hyperplanes are $i$ and $j$ for both statements, with $u = w = 0$: both loops are parallel. The third is $k$ for the update and 0 for the initialization, and a scalar dimension puts the initialization first. The three hyperplanes form one band, so all three loops can be tiled.

## Correctness

The full proof is in [the proof page](proofs/correctness.md). It shows four facts.

- **Legality.** Every dimension appended weakly satisfies every edge that is in $E$ at that time, and an edge leaves $E$ only when some appended dimension strongly satisfies it. At the end $E$ is empty, so for every pair in every $P_e$ the first nonzero entry of $\Phi_T(\vec{t}) - \Phi_S(\vec{s})$ is positive.
- **Tiling.** Inside a band, every hyperplane has $\delta_e \ge 0$ on every edge that is in $E$ when the band starts, and a pair that no earlier dimension orders belongs to such an edge. So adding the tile coordinates $\lfloor \phi / \tau \rfloor$ of a band in front of it keeps every dependence in order, for any tile size $\tau \ge 1$.
- **The cost bound.** For each hyperplane found by the integer program and each edge in $E$ at that time, $0 \le \delta_e \le u \cdot N + w$ on all of $P_e$, for every $N$ in the context.
- **Termination.** Each solver success raises the rank of every statement that is not full, each band closes once, and lines L6 and L7 each remove at least one edge.

## Complexity

The integer program succeeds at most $s d$ times, because each success raises the rank of some statement. Each failure is followed by a band closing, a cut or a fallback, and there are at most $s d$ closings and at most $e$ cuts and fallbacks. So there are $O(s d + e)$ integer programs, plus one linear program per edge and hyperplane for the strong satisfaction tests. The integer programs are NP-hard in general, so $I$ is exponential in the worst case. In practice they have tens to hundreds of bounded unknowns, and they stay small for typical kernels. The Farkas multipliers make the programs grow linearly with the number of constraints of the dependence polyhedra.

## Properties

- **Tilable bands.** Every band of two or more hyperplanes can be tiled with rectangular tiles in the new coordinates, and its tiles can run as a pipelined [wavefront](/wavefront-parallelism/) even when no hyperplane in it is parallel.
- **Fusion and distribution together.** The constant terms $c_{S,0}$ let statements of different loops share a hyperplane with a shift, and the cuts between strongly connected components distribute them when that fails.
- **Integer coefficients.** The coefficients are integers by construction, so no scaling is needed.
- **Nonnegative coefficients.** Restricting $c \ge 0$ keeps the integer programs small, at the cost of missing transformations such as loop reversal.

## Variants and improvements

- **Negative coefficients.** Pluto+ (Bondhugula, Acharya and Cohen, 2016) allows negative coefficients, which brings in loop reversal and more skewings, and makes the linear independence constraints complete.
- **Fusion policies.** The Pluto tool has several policies that decide where to cut the dependence graph, from maximal fusion to no fusion, rather than only at the points where the solver fails.
- **Other polyhedral schedulers.** The isl scheduler, used in LLVM's Polly and in PPCG, combines Pluto's proximity cost with Feautrier's greedy fallback when no tilable band exists.
- **Concurrent start.** For stencils, diamond tiling (Bandishti, Pananilath and Bondhugula 2012) adds a constraint so that tiles can start in parallel along a face.

## When to use it

Use Pluto-style scheduling to tile and parallelize dense loop nests with affine accesses, such as stencils, linear algebra kernels and image filters, for cache locality and coarse-grained parallelism on multicores. When the goal is the maximum degree of fine-grained parallelism, [Feautrier's algorithm](/feautrier-scheduling/) is the reference. For one perfect nest with uniform dependences, [unimodular transformations](/unimodular-transformations/) or the [hyperplane method](/lamport-hyperplane-method/) are simpler.

## Pitfalls

- **Affine programs only.** The dependence polyhedra and the Farkas linearization need affine loop bounds and affine subscripts. Index arrays and data-dependent conditions take the program out of the model.
- **A heuristic, not an optimum.** The integer program minimizes a bound on dependence distances. That bound is a proxy for communication volume and reuse distance, not a model of the machine. The lexicographic minimum is optimal for this objective only, and it does not prove that the code runs fastest. Tile sizes, vectorization, prefetching and the cost of the generated loop bounds are all outside the model.
- **A legal schedule can be slow.** A transformation that tiles well can still give loops with complex bounds, many empty tiles or poor vectorization. Measure the result.
- **Memory-based dependences.** Anti and output dependences link far-apart time steps, as in the Gauss-Seidel example where $u = 1$. Exact dataflow dependences, or array expansion, give smaller bounds.
- **The independence trick can fail.** The constraint $\sum_h h \cdot c_S \ge 1$ asks for a positive component in a fixed direction. When the rows of $H_S^\perp$ cancel, for example after a first hyperplane $(1, 1)$ in two dimensions, no new hyperplane passes, even though one exists. The algorithm then falls back to a cut, and the band ends early.
- **Bounded coefficients.** The bounds on the coefficients make the integer programs finite, but a legal hyperplane with larger coefficients is then missed.

## Implementations

## History

Feautrier's 1992 papers set up the affine form of Farkas' lemma for schedules. From 1997, Lim and Lam used affine partitioning with the same tool to find communication-free and pipelined parallelism. In 2008, Bondhugula, Hartono, Ramanujam and Sadayappan (PLDI) and Bondhugula, Baskaran, Krishnamoorthy, Ramanujam, Rountev and Sadayappan (CC) combined these ideas into one practical algorithm. It finds tiling hyperplanes one at a time with a cost function that bounds dependence distances, and handles fusion and distribution in the same framework. The tool Pluto became a reference for polyhedral optimization, and its cost function is the "proximity" objective of the isl scheduler.

## References
