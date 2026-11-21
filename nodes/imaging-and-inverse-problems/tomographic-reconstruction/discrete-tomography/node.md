---
tag: BG84ZH
kind: problem
slug: discrete-tomography
name: Discrete tomography
aliases:
- reconstruction of binary images from projections
- binary tomography
area: imaging-and-inverse-problems/tomographic-reconstruction
level: advanced
summary: "Reconstruct an image with few gray values, such as a 0-1 matrix, from a few projections. Two directions are easy, and consistency for three or more is NP-complete."
model: word-ram
prereqs: [tomographic-reconstruction-problem, max-flow-problem, np-complete]
see_also: [sparse-view-ct-reconstruction, max-flow-min-cut-theorem, bipartite-matching, b-matching, integrality-theorem, binary-integer-programming, simulated-annealing, x-ray-transform]
sources:
  - paper: "H. J. Ryser, Combinatorial properties of matrices of zeros and ones, Canadian Journal of Mathematics 9, 1957, 371 to 377"
    locator: the condition for a 0-1 matrix with given row and column sums, and the interchanges that connect all such matrices
  - paper: "David Gale, A theorem on flows in networks, Pacific Journal of Mathematics 7(2), 1957, 1073 to 1082"
    locator: the supply and demand theorem for networks, with the 0-1 matrix condition as an application
  - paper: "R. J. Gardner, P. Gritzmann and D. Prangenberg, On the computational complexity of reconstructing lattice sets from their X-rays, Discrete Mathematics 202, 1999, 45 to 71"
    locator: NP-completeness of the consistency problem for three or more directions in the plane (general locator)
  - book: "Gabor T. Herman and Attila Kuba (editors), Discrete Tomography: Foundations, Algorithms, and Applications, Birkhauser, 1999"
    locator: survey chapters on the two-direction case, complexity, uniqueness and algorithms (general locator)
---

Discrete tomography asks for an image whose pixels take only a few known values, most often 0 and 1, from its line sums in a few directions. In the simplest case the image is an $m \times n$ binary matrix, and the data are its row sums and column sums. The few values replace the smoothness or sparsity priors of [sparse-view CT](/sparse-view-ct-reconstruction/), so two to four directions can be enough to fix an image. For two directions the problem is a flow problem and is solved in polynomial time (Gale 1957, Ryser 1957). For three or more directions in the plane, deciding whether any binary image fits the data is NP-complete (Gardner, Gritzmann and Prangenberg 1999). So practical methods for three or more directions are integer programs, relaxations or heuristics.

## In plain words

Picture a grid of squares, each either black or white. You do not see the grid. You only know, for each row, how many squares in it are black, and the same for each column. Can you draw a grid that fits these counts? Is there only one such grid?

With rows and columns only, a simple rule always finds a fitting grid if one exists. But often many grids fit. If you also know the counts along the diagonals, fewer grids fit, and often only one. The price is that finding a fitting grid then becomes very hard in general: no fast method is known, and none is expected.

## Definition

A **direction** is a nonzero integer vector $v = (p, q)$ with $\gcd(p, q) = 1$. The **X-ray** of a finite set $F \subset \mathbb{Z}^2$ in direction $v$ is the function that gives, for each lattice line parallel to $v$, the number of points of $F$ on that line. A binary image on an $m \times n$ grid is such a set, and its X-rays in the directions $(0, 1)$ and $(1, 0)$ are its row sums and column sums.

Three problems are studied for a fixed set of directions $v_1, \dots, v_k$:

- **Consistency.** Given $k$ functions with finite support, is there a finite set $F$ whose X-rays they are?
- **Reconstruction.** If there is, find one.
- **Uniqueness.** Given $F$, is there another set with the same X-rays?

The input size is the number of lines with a nonzero count plus the bits of the counts. With gray values, the pixels take values in a known finite set $\{g_1, \dots, g_\ell\}$, and the data are the sums along lines, as in CT.

## Variants

- **Two directions.** Row and column sums of a 0-1 matrix. Polynomial for consistency, reconstruction and uniqueness.
- **Three or more directions.** NP-complete consistency in the plane; this case is what makes the field hard.
- **Restricted classes.** Convex lattice sets, connected sets, and sets that are convex along rows and columns (hv-convex). A restriction can make the image unique and can make reconstruction polynomial again. Barcucci, Del Lungo, Nivat and Pinzani (1996) gave a polynomial algorithm for hv-convex polyominoes from row and column sums.
- **Several gray values.** The pixel values come from a known finite set larger than two. The DART method of Batenburg and Sijbers (2011) targets this case with real CT data.
- **Noisy data.** The sums are measured with noise, so the task is to minimize a misfit over binary images, often with a smoothness term, rather than to fit exactly.
- **Higher dimension.** Lattice sets in $\mathbb{Z}^3$, for example crystal lattices seen by electron microscopy.

## Examples

**Two directions with five solutions.** Take a $3 \times 3$ binary image with row sums $r = (2, 1, 1)$ and column sums $c = (2, 1, 1)$. A brute-force search over all $2^9$ images finds exactly 5 that fit (a measurement):
$$
\begin{pmatrix} 0&1&1\\ 1&0&0\\ 1&0&0 \end{pmatrix}\!,\
\begin{pmatrix} 1&0&1\\ 0&1&0\\ 1&0&0 \end{pmatrix}\!,\
\begin{pmatrix} 1&0&1\\ 1&0&0\\ 0&1&0 \end{pmatrix}\!,\
\begin{pmatrix} 1&1&0\\ 0&0&1\\ 1&0&0 \end{pmatrix}\!,\
\begin{pmatrix} 1&1&0\\ 1&0&0\\ 0&0&1 \end{pmatrix}\!.
$$
The last two differ only in rows 2 and 3 and columns 1 and 3, where the pattern $\begin{pmatrix} 0&1\\ 1&0 \end{pmatrix}$ becomes $\begin{pmatrix} 1&0\\ 0&1 \end{pmatrix}$. Such a swap keeps every row and column sum. Ryser showed that any two 0-1 matrices with the same row and column sums are connected by a sequence of such swaps, so the two-direction solution is unique exactly when no swap is possible.

**A third direction decides.** Add the X-ray in the diagonal direction $(1, 1)$: for $k = -2, \dots, 2$, let $d_k$ count the ones in the cells $(i, j)$ with $j - i = k$. The five images above have the diagonal sums $(1, 1, 0, 1, 1)$, $(1, 0, 2, 0, 1)$, $(0, 2, 1, 0, 1)$, $(1, 0, 1, 2, 0)$ and $(0, 1, 2, 1, 0)$, in the order $k = -2, \dots, 2$. They are all different, so the three X-rays together fix the image. You can check each of these sums by hand.

**The greedy rule.** Fill the rows one at a time, and put the ones of each row into the columns with the largest remaining column sums, the leftmost first on ties. For $r = c = (2, 1, 1)$: row 1 takes columns 1 and 2, which leaves $(1, 0, 1)$; row 2 takes column 1, which leaves $(0, 0, 1)$; row 3 takes column 3. The result is the fifth image above.

**No solution.** With $r = (2, 0)$ and $c = (2, 0)$, column 1 needs two ones but only row 1 may hold any. The test below fails at $k = 1$: $c_1 = 2 > \min(2, 1) + \min(0, 1) = 1$.

## Known algorithms

| Case | Method | Cost or status |
|---|---|---|
| Two directions | test of Gale and Ryser | $O(m + n)$ after sorting the column sums; a theorem |
| Two directions | greedy rule above | $O(m n \log n)$ by sorting the remaining column sums for each row; correct whenever a solution exists (a theorem; we also checked it against brute force on 3000 random small cases) |
| Two directions | [max flow](/max-flow-problem/) or [b-matching](/b-matching/) | polynomial; an integral flow is a 0-1 matrix by the [integrality theorem](/integrality-theorem/) |
| Two directions, uniqueness | search for a swappable $2 \times 2$ pattern | polynomial; unique exactly when no swap exists (Ryser 1957) |
| hv-convex polyominoes, two directions | Barcucci, Del Lungo, Nivat and Pinzani (1996) | polynomial |
| Three or more directions | [binary integer programming](/binary-integer-programming/) with branch and bound | exact; exponential time in the worst case |
| Three or more directions | linear programming relaxation, then rounding | polynomial; the rounded image may not fit the data |
| Noisy data, gray values | [simulated annealing](/simulated-annealing/), DART (Batenburg and Sijbers 2011) | heuristics; no guarantee |

## Bounds

- **Two directions (theorem).** Let $c_1 \ge c_2 \ge \dots \ge c_n$ be the column sums in decreasing order. A 0-1 matrix with row sums $r_1, \dots, r_m$ and these column sums exists if and only if $\sum_i r_i = \sum_j c_j$ and, for every $k = 1, \dots, n$,
$$\sum_{j=1}^{k} c_j \le \sum_{i=1}^{m} \min(r_i, k).$$
(Gale 1957, Ryser 1957.) The right side is the largest number of ones that $k$ columns can hold, because row $i$ can place at most $\min(r_i, k)$ ones in them; this is why the condition is necessary.
- **Three or more directions (theorem).** For any fixed set of three or more pairwise nonparallel directions in $\mathbb{Z}^2$, the consistency problem is NP-complete, and so the reconstruction problem is NP-hard (Gardner, Gritzmann and Prangenberg 1999). It lies in NP because a set $F$ is a certificate that is checked by counting.
- **Uniqueness needs restrictions (theorem).** For any finite set of directions, there are two different finite lattice sets with the same X-rays in all of them. So no fixed number of directions determines all binary images, and positive uniqueness results hold only for restricted classes such as convex lattice sets.

## Reductions

- **Two directions to max flow.** Build a network with a source, one node per row, one node per column and a sink. Give the edge from the source to row $i$ the capacity $r_i$, each edge from row $i$ to column $j$ the capacity 1, and the edge from column $j$ to the sink the capacity $c_j$. A 0-1 matrix fits the data exactly when the maximum flow equals $\sum_i r_i$, and the edges with flow 1 mark its ones. By the [max-flow min-cut theorem](/max-flow-min-cut-theorem/), the minimum cuts of this network give the Gale-Ryser inequalities.
- **Two directions to bipartite degree sequences.** A 0-1 matrix is the biadjacency matrix of a [bipartite graph](/bipartite-matching/), and the row and column sums are its degrees.
- **Any number of directions to integer programming.** One binary variable per pixel and one linear equation per line give $A x = y$ with $x \in \{0, 1\}^N$, the CT model with a binary constraint.
- **To sparse-view CT.** Relaxing $x \in \{0, 1\}^N$ to $0 \le x \le 1$ gives a continuous reconstruction problem with box constraints, which [SART](/sart/) or [SIRT](/sirt/) can treat as a starting point.

## Applications

- **Electron microscopy of crystals.** Counting atoms along a few lattice directions in a crystal; this question motivated much of the modern work in the field.
- **Industrial CT of objects made of one or two materials.** Few projections and known densities, as in the DART method.
- **Medical imaging with a known number of tissue classes.** Angiography and other cases where the image is close to binary.
- **Data security.** Deciding whether released row and column totals of a table reveal its 0-1 entries.
- **Puzzles.** Nonograms ask for a binary image from run lengths in the rows and columns, a related but different kind of data.

## References
