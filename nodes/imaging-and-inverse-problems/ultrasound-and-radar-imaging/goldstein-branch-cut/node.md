---
tag: 5RF5DV
kind: algorithm
slug: goldstein-branch-cut
name: Goldstein branch cut algorithm
aliases:
- branch cut phase unwrapping
area: imaging-and-inverse-problems/ultrasound-and-radar-imaging
level: advanced
summary: Unwrap a 2D phase by connecting residues of opposite sign with cuts and integrating along paths that do not cross the cuts.
solves: [phase-unwrapping]
model: word-ram
complexity:
  vars: {N: the number of pixels, R: the number of residues, b: the largest box radius}
  time: {worst: O(N + R b^3 + R sqrt(N))}
  space: {extra: O(N)}
properties: {deterministic: true, recursive: false, exact: false, congruent: true}
history:
  year: 1988
  people: [Richard M. Goldstein, Howard A. Zebker, Charles L. Werner]
  note: "Goldstein, Zebker and Werner (1988) introduced residues and branch cuts to unwrap satellite radar interferograms. The search for the nearest residue in growing boxes is a heuristic."
prereqs: [phase-unwrapping, breadth-first-search]
see_also: [least-squares-phase-unwrapping, sar-interferometry, flood-fill, union-find-connectivity, min-cost-flow-problem, np-hard, quantitative-susceptibility-mapping, word-ram]
sources:
  - paper: doi:10.1029/RS023i004p00713
    title: "Richard M. Goldstein, Howard A. Zebker and Charles L. Werner, Satellite radar interferometry: two-dimensional phase unwrapping, Radio Science 23(4), 1988, 713"
    locator: "residues, branch cuts placed by a search in growing boxes, and integration that does not cross the cuts (general locator)"
  - paper: doi:10.1364/AO.21.002470
    title: "Kazuyoshi Itoh, Analysis of the phase unwrapping algorithm, Applied Optics 21(14), 1982, 2470"
    locator: "the condition that the true phase differences lie in (-pi, pi) (general locator)"
  - paper: doi:10.1364/JOSAA.17.000401
    title: "Curtis W. Chen and Howard A. Zebker, Network approaches to two-dimensional phase unwrapping: intractability and two new algorithms, Journal of the Optical Society of America A 17(3), 2000, 401"
    locator: "the NP-hardness of minimum L0 phase unwrapping (general locator)"
  - paper: doi:10.1364/JOSAA.14.002692
    title: "Thomas J. Flynn, Two-dimensional phase unwrapping with minimum weighted discontinuity, Journal of the Optical Society of America A 14(10), 1997, 2692"
    locator: "an exact method for the minimum weighted discontinuity problem (general locator)"
  - paper: doi:10.1109/36.673674
    title: "Mario Costantini, A novel phase unwrapping method based on network programming, IEEE Transactions on Geoscience and Remote Sensing 36(3), 1998, 813 to 821"
    locator: "the minimum L1 unwrapping as a minimum cost flow problem (general locator)"
  - book: isbn:9780471249351
    title: "Dennis C. Ghiglia and Mark D. Pritt, Two-Dimensional Phase Unwrapping: Theory, Algorithms, and Software, Wiley, 1998"
    locator: "the chapter on path-following methods (Goldstein's branch cut algorithm)"
---

The Goldstein branch cut algorithm unwraps a two-dimensional phase image by integrating the wrapped differences of neighbouring pixels along paths that never cross a set of cuts. A residue is a $2 \times 2$ square of pixels whose wrapped differences sum to $\pm 2\pi$. A path that goes around a residue gains or loses one turn, so the integral would depend on the path. Goldstein, Zebker and Werner (1988) join each residue to residues of opposite sign, or to the border, by cuts, so that every group of joined residues is neutral or ends at the border. Then no closed path that avoids the cuts encloses a net charge, and a [breadth first search](/breadth-first-search/) over the free edges gives a result that does not depend on the path and differs from the data only by multiples of $2\pi$. The method is fast and local. Its weak point is the placement of the cuts, which is greedy. The cuts are not the shortest possible, and finding the result with the fewest bad edges is NP-hard. It is a classic answer to the [phase unwrapping problem](/phase-unwrapping/), especially in [SAR interferometry](/sar-interferometry/).

## In plain words

A wrapped phase only shows each value up to whole turns. If you walk across the image and add up the small wrapped steps between neighbours, you get the true phase back, as long as no step is larger than half a turn.

Noise and real jumps break this at a few points, the residues. Walk around a residue and you come back one turn higher or lower than where you started. The algorithm builds fences, the cuts, between residues of opposite sign, or from a residue to the edge of the image. Then it walks only along paths that do not cross a fence. Every closed walk of this kind adds up to zero, so the answer does not depend on the route.

## The problem

**Input.** A wrapped phase image $\psi(i, j) \in (-\pi, \pi]$ on an $m \times n$ grid with $N = mn$ pixels, and a largest box radius $b$. $W(x) = x - 2\pi k$ with the integer $k$ that puts the value in $(-\pi, \pi]$.

**Residues.** For the square with the corners $(r, c)$, $(r, c+1)$, $(r+1, c+1)$ and $(r+1, c)$, in this order, the charge is

$$q(r, c) = \frac{1}{2\pi} \sum_{\text{4 edges}} W(\psi(\text{next corner}) - \psi(\text{corner})) \in \{-1, 0, 1\}.$$

**Output.** A set of blocked edges (the cuts) and an image $\varphi$ with $\varphi - \psi \in 2\pi\mathbb{Z}$ at every pixel, such that $\varphi(b) - \varphi(a) = W(\psi(b) - \psi(a))$ on every edge that is not blocked. The goal is to block few edges, and to block them where the true phase really jumps.

## The algorithm

```pseudo id=main
GOLDSTEIN(ψ, b)
L1  q ← charges of all 2 × 2 squares
    for each residue s0 in raster order that is not in a tree
L2      tree ← [s0]
L3      charge ← q(s0)
L4      for k ← 1 to b while charge ≠ 0
            for each t in tree while charge ≠ 0
L5              for each residue u not in a tree in the box of radius k around t
L6                  cut from t to u; add u to tree; charge ← charge + q(u)
L7              if charge ≠ 0 and the box passes the border: cut from t to the border; charge ← 0
L8          k ← k + 1
L9      if charge ≠ 0: cut from s0 to the border
L10 flood fill over the free edges: φ(next) ← φ(current) + W(ψ(next) - ψ(current))
L11 return φ and the cuts
```

A cut is a chain of squares. Each step from one square to the next blocks the pixel edge that they share, so the cut is a fence that the flood fill of line L10 cannot cross. The cut of line L6 is a staircase, first along the rows and then along the columns. A cut to the border goes straight to the nearest side and blocks the last edge on the border too. Each region of pixels joined by free edges starts at its first pixel in raster order, with $\varphi = \psi$ there.

The box is the set of squares at Chebyshev distance at most $k$ from a member of the tree. The box grows only when no member of the tree has found a partner at the present size, so close residues are joined first.

## Example

**An adjacent dipole.** Take a $4 \times 5$ image of zeros with $\psi(1, 2) = -2$ and $\psi(2, 2) = 2$. The true difference across the edge from $(1, 2)$ to $(2, 2)$ is 4, which is more than $\pi$, and it wraps to $4 - 2\pi$. Line L1 finds two residues, $q(1, 1) = -1$ and $q(1, 2) = +1$, the two squares on either side of that edge. Line L2 starts a tree at $(1, 1)$, and line L5 finds $(1, 2)$ in the box of radius 1. Line L6 steps from square $(1, 1)$ to square $(1, 2)$ and blocks the one edge they share, which is the edge from $(1, 2)$ to $(2, 2)$. The charge is 0 and the search stops. Line L10 reaches $(2, 2)$ around the cut and gets $\varphi(2, 2) - \varphi(1, 2) = 4$, the true difference. One edge disagrees with its wrapped difference, which is the minimum.

**Greedy cuts are not shortest.** Take the $3 \times 4$ image

$$\psi = \begin{pmatrix} 1.86 & -1.67 & 1.17 & -0.71 \\ -2.62 & -0.43 & -1.89 & 2.2 \\ 2.24 & 1.74 & 2.19 & 2.8 \end{pmatrix}.$$

Its squares have the charges $+1$ at $(0, 2)$, $-1$ at $(1, 1)$ and $+1$ at $(1, 0)$. The raster order meets $(0, 2)$ first, and its box of radius 1 holds $(1, 1)$. The staircase cut blocks two edges. Then $(1, 0)$ has no free partner, its box passes the border, and line L7 blocks one more edge, to the bottom. That is three blocked edges and an L0 cost of 3. Joining $(1, 0)$ to $(1, 1)$ (one edge) and $(0, 2)$ to the top border (one edge) gives cost 2, and an exhaustive search over all congruent results confirms that 2 is the minimum.

## Correctness

The proofs are in proofs/correctness.md. Items 1 to 5 below are theorems. The quality of the cut placement is a heuristic.

1. **Loop sums are enclosed charge.** For any closed walk $\gamma$ on the pixel grid, the sum of the wrapped differences along $\gamma$ is $2\pi \sum_f w_\gamma(f) q(f)$, where $w_\gamma(f)$ is the winding number of $\gamma$ around square $f$.
2. **The cut invariant.** After line L9, every connected group of squares joined by cuts that contains a residue has total charge 0 or is joined to the border. A tree stops only when its charge is 0 (lines L4 and L5) or when a member is cut to the border (lines L7 and L9).
3. **Path independence.** A closed walk that uses only free edges cannot cross a cut, so its winding number is the same on all the squares of one group, and 0 on a group that touches the border. By 1 and 2, its loop sum is 0.
4. **What the flood fill returns.** By 3, every free edge inside a region has $\varphi(b) - \varphi(a) = W(\psi(b) - \psi(a))$, not only the edges of the search tree. Every pixel has $\varphi - \psi \in 2\pi\mathbb{Z}$. Another seed changes a region only by a constant multiple of $2\pi$.
5. **Exact without residues.** Then nothing is blocked, and if the true phase changes by less than $\pi$ between neighbours (Itoh's condition), the output is the true phase plus $2\pi k$.

The theorems say nothing about the blocked edges. Whether the cuts lie where the true phase really jumps is not proven, and the L0 cost of the output, the number of edges that disagree with their wrapped difference, is not minimal in general.

## Complexity

In the word-RAM model, with Boolean arrays for the charges, the tree marks and the blocked edges, line L1 and the flood fill of line L10 cost $O(N)$. Each residue joins exactly one tree. The scans of the boxes cost $O(k^2)$ per member and radius, $O(R b^3)$ in total. A cut of line L6 has at most $2b$ edges, and a cut to the border at most $\min(m, n) \le \sqrt{N}$, at most once per tree. So the worst case time is $O(N + R b^3 + R \sqrt{N})$ and the extra space is $O(N)$. When the residues are sparse, the time is close to $O(N)$.

## Properties

- **Congruent** (theorem). The output differs from the data by multiples of $2\pi$ at every pixel, unlike [least squares unwrapping](/least-squares-phase-unwrapping/).
- **Path independent** (theorem). The result in each region is fixed up to one multiple of $2\pi$, whatever the order of the search.
- **Exact where it is free** (theorem). Every free edge keeps its wrapped difference, so all the errors sit on the cuts.
- **Not optimal** (theorem for the example). The greedy order can give longer cuts than needed, as in the $3 \times 4$ example. In 200 random $3 \times 4$ images with independent uniform phases (seed 9001), 180 had residues. The output reached the minimum L0 cost in 164 of them and was worse in 16 (measurement).
- **Holes.** A region closed off by cuts gets its own constant. Its relation to the rest of the image is lost.
- **Deterministic.** The result depends on the raster order of the residues and on the box radius $b$.

## Variants and improvements

- **Quality maps and masks.** Residues on the border of a mask, or in regions of low coherence, are joined to the mask edge. The flood fill can visit the pixels in the order of a quality map, so that errors stay in the bad regions.
- **Balancing to the border first.** Residues near the border are often joined to it straight away. This avoids long cuts between residues that are far apart.
- **Shortest cuts.** Choosing the cuts of least total length is a minimum weight matching of the residues, with the border as a free partner. The minimum L1 problem is a [minimum cost flow problem](/min-cost-flow-problem/) on the grid of squares (Costantini 1998). Flynn (1997) gives an exact method for the minimum weighted discontinuity problem. The minimum L0 problem is NP-hard (Chen and Zebker 2000).
- **Other path-following methods.** Quality guided unwrapping without cuts, and mask cut algorithms, are collected with Goldstein's method in the book of Ghiglia and Pritt (1998).
- **Statistical cost functions** in SAR use the coherence and a model of the topography to set the cost of each edge.

## When to use it

Use it when the result must be congruent to the data, for example to keep the exact $2\pi$ multiples of an interferogram, and when the residues are sparse and in pairs, as in good [SAR interferometry](/sar-interferometry/) data or optical fringe patterns. Avoid it when residues are dense, because the cuts then close off whole regions. Use a minimum cost flow method when the cuts must be short, and [least squares unwrapping](/least-squares-phase-unwrapping/) when a smooth result everywhere matters more than congruence.

## Pitfalls

- **Isolated regions.** Dense cuts can close off a region. Its offset of $2\pi k$ against the rest is then arbitrary. Report it, or join it by a quality guided step.
- **Box too small.** With $b = 1$, distant pairs are joined to the border instead of to each other, and the cuts get longer. In the test, two opposite vortices four squares apart need 4 blocked edges as a pair and 8 as two border cuts.
- **Wrong orientation of the charge.** All squares must use the same orientation, or opposite charges look equal and are never paired.
- **Cuts that do not block the shared edge.** The cut is a chain of squares, and each step must block the pixel edge between those two squares. Blocking pixels instead of edges, or skipping the last border edge, leaves a gap that a path can go through.
- **Seed on a cut.** In each region the start value is the wrapped phase itself. Only differences inside a region are meaningful.

## Implementations

The Python code stores the cuts as a set of blocked edges, where ('h', i, j) is the edge from $(i, j)$ to $(i, j+1)$ and ('v', i, j) is the edge from $(i, j)$ to $(i+1, j)$. It needs no shared helper. The tests check a single vortex, exact recovery without residues, congruence and exact free edges on random images, the cut invariant for several box sizes, the effect of the box size on two vortices, the adjacent dipole, a lower bound by exhaustive search on tiny images, the non-optimal $3 \times 4$ example, and the change of seeds.

## History

Itoh (1982) showed that summing wrapped differences gives the true phase when the true differences are less than $\pi$. Goldstein, Zebker and Werner (1988) unwrapped satellite radar interferograms. They found that the inconsistencies sit at residues, and they placed branch cuts between them, which made the integration independent of the path. Their method became the reference path-following method, and the book of Ghiglia and Pritt (1998) presents it in detail. Later work set the cut placement as an optimization problem: Flynn (1997) gave an exact method for minimum weighted discontinuity, Costantini (1998) solved the L1 problem as a minimum cost flow, and Chen and Zebker (2000) proved that the L0 problem is NP-hard.

## References
