---
tag: 2WYA23
kind: algorithm
slug: patchmatch
name: PatchMatch
aliases:
- randomized correspondence algorithm
area: computer-vision/stereo-and-dense-reconstruction
level: advanced
summary: Find approximate nearest neighbor patches between two images by random initialization, propagation of good offsets to neighbors and random search around them.
solves: [approximate-nearest-neighbor]
model: word-ram
complexity:
  vars: {n: the number of patches of A, p: the number of pixels in a patch, w: the larger side of B in pixels, T: the number of iterations}
  time: {worst: Θ(n p T log w), average: Θ(n p T log w), best: Θ(n p T log w)}
  space: {extra: Θ(n)}
properties: {deterministic: false, exact: false, online: false, recursive: false}
history:
  year: 2009
  people: [Connelly Barnes, Eli Shechtman, Adam Finkelstein, Dan B Goldman]
  note: Barnes et al. (SIGGRAPH 2009) showed that random guesses plus propagation along the scan order find good patch correspondences far faster than tree search, which made interactive image editing with patches possible.
prereqs: [approximate-nearest-neighbor, digital-image]
see_also: [patchmatch-stereo, nearest-neighbor-search, kd-tree, image-inpainting, optical-flow, template-matching, multi-view-stereo, plane-sweep-stereo]
sources:
  - paper: doi:10.1145/1531326.1531330
    title: "Connelly Barnes, Eli Shechtman, Adam Finkelstein and Dan B Goldman, PatchMatch: a randomized correspondence algorithm for structural image editing, ACM Transactions on Graphics 28(3), Article 24, 2009 (SIGGRAPH 2009)"
    locator: Section 3 (the nearest neighbor field, initialization, propagation with the scan order reversed on even iterations, random search of Eq. 1 with alpha = 1/2, halting after 4 to 5 iterations), Section 3.3 (the convergence analysis, Eqs. 2 and 3) and Table 1 (the comparison with a kd-tree)
  - paper: doi:10.5244/C.25.14
    title: Michael Bleyer, Christoph Rhemann and Carsten Rother, PatchMatch Stereo, stereo matching with slanted support windows, British Machine Vision Conference 2011, pages 14.1 to 14.11
    locator: Section 2 (PatchMatch used to search over the infinite set of planes per pixel)
---

PatchMatch computes an approximate nearest neighbor field between two images $A$ and $B$: for each patch of $A$ it finds an offset to a patch of $B$ that looks alike, measured by the sum of squared differences (SSD). The exact field needs, for each of the $n$ patches of $A$, a search over all patches of $B$. PatchMatch instead starts from random offsets and improves them in a few passes over the image. Each pass tries, at each patch, the offsets of its already visited neighbors (propagation), then a few random offsets at falling distances around the current one (random search). It uses one property of natural images: neighboring patches tend to have neighboring matches, so one good guess spreads over a whole region. The method is a general [approximate nearest neighbor](/approximate-nearest-neighbor/) search for image patches; [PatchMatch stereo](/patchmatch-stereo/) uses the same scheme to search over planes per pixel instead of offsets.

## In plain words

You want to know, for each small square of picture A, where a similar square is in picture B. Checking every place in B is slow. So give every square a random guess first. Most guesses are bad, but a few are good by luck. Then walk over the picture in reading order. At each square, ask the left and upper neighbors: "your match, moved by one step, is it better than mine?" If yes, take it. A good guess then flows right and down over the whole area that moves together. After that, try a few random places near the current match, first far away and then closer. On the next pass, walk backward so good matches also flow left and up. Four or five passes are usually enough.

## The problem

**Input.** Two grayscale images $A$ and $B$ with integer pixel values, indexed `img[y][x]`. A patch radius $r \ge 0$, so that a patch has $p = (2r + 1)^2$ pixels. A number of iterations $T$ and a source of random numbers. Only patches that lie fully inside an image are used. Their centers are the pixels with $r \le x < W - r$ and $r \le y < H - r$; there are $n$ such centers in $A$.

**Output.** An offset field $f$ that maps each center $a$ of $A$ to an offset $f(a)$ such that $a + f(a)$ is a center of $B$, and the distances $D(a) = \operatorname{dist}(a, a + f(a))$ with

$$\operatorname{dist}(a, b) = \sum_{|i| \le r} \sum_{|j| \le r} \big(A(a_x + i, a_y + j) - B(b_x + i, b_y + j)\big)^2 .$$

The exact nearest neighbor field has $D(a) = \min_b \operatorname{dist}(a, b)$. PatchMatch gives no such guarantee. Its output is an upper bound on the exact distance at every patch, which gets smaller with more iterations.

## The algorithm

```pseudo id=main
PATCHMATCH(A, B, r, T)
L1  for each center a of A do f[a] ← (a uniformly random center of B) - a; D[a] ← dist(a, a + f[a])
L2  for k ← 1 to T do
L3      if k is odd then visit the centers of A in row order and set s ← -1 else in reverse row order and set s ← +1
L4      for each center a = (x, y) in that order do
L5          for each n in {(x + s, y), (x, y + s)} that is a center of A do
L6              b ← a + f[n]; if b is a center of B and dist(a, b) < D[a] then f[a] ← f[n]; D[a] ← dist(a, b)
L7          v ← a + f[a]
L8          ρ ← w                                       ▷ w = the larger side of B
L9          while ρ ≥ 1 do
L10             b ← a uniformly random center of B with |b_x - v_x| ≤ ρ and |b_y - v_y| ≤ ρ
L11             if dist(a, b) < D[a] then f[a] ← b - a; D[a] ← dist(a, b)
L12             ρ ← ⌊ρ / 2⌋
L13 return f, D
```

Line L1 is the random initialization. Line L3 sets the scan order: odd iterations go from the top left to the bottom right and look at the left and upper neighbors, even iterations go backward and look at the right and lower neighbors. Lines L5 and L6 are the propagation step. Neighbor $n$ was visited before $a$ in this pass, so its offset is already improved; the test asks whether the same offset also fits $a$. Lines L7 to L12 are the random search of Barnes et al. (their Eq. 1, $u_i = v_0 + w \alpha^i R_i$ with $\alpha = 1/2$). The center $v$ stays fixed during the search, and the square of half side $\rho$ is cut to the centers of $B$. With $w$ the larger side of $B$, a patch gets $\lfloor \log_2 w \rfloor + 1$ random tries per iteration. Both steps accept a candidate only when it is strictly better.

The code computes the SSD with early termination: the sum stops as soon as it reaches the current $D[a]$, because the candidate then loses anyway. This is one of the speedups of the paper and does not change the result.

## Example

Take one-row images with $r = 0$, so that a patch is one pixel and the distance is a squared difference. Let $A = (5, 9, 2, 7, 4, 8)$ and $B = (1, 6, 5, 9, 2, 7, 4, 8, 3)$. $A$ is the part of $B$ that starts at column 2, so the true offset is $+2$ everywhere. Start from the offsets $(+6, +2, -1, +4, -3, +1)$. Pixel 1 has the correct offset by chance. To show the propagation alone, turn the random search off.

| after | $f$ at $x = 0, \ldots, 5$ | $D$ at $x = 0, \ldots, 5$ |
|---|---|---|
| L1 | 6, 2, -1, 4, -3, 1 | 1, 0, 16, 1, 4, 16 |
| iteration 1 (forward) | 6, 2, 2, 2, 2, 2 | 1, 0, 0, 0, 0, 0 |
| iteration 2 (backward) | 2, 2, 2, 2, 2, 2 | 0, 0, 0, 0, 0, 0 |

In the forward pass, pixel 2 tries the offset $+2$ of pixel 1. $B(4) = 2 = A(2)$, so the distance drops from 16 to 0 and pixel 2 takes it. Pixels 3, 4 and 5 then do the same, one after the other. Pixel 0 comes before pixel 1 in the forward pass, so it keeps $+6$ with $D = 1$ ($A(0) = 5$, $B(6) = 4$). The backward pass visits pixel 0 last and gives it $+2$ from pixel 1. With the random search on, $w = 9$ gives the radii 9, 4, 2 and 1, so each pixel also gets four random tries per iteration.

## Correctness

PatchMatch is a randomized heuristic for an approximate answer, so its correctness has two parts. The full proofs are in [proofs/correctness.md](proofs/correctness.md).

1. **Invariants.** After every step, $D[a] = \operatorname{dist}(a, a + f[a])$ and $a + f[a]$ is a center of $B$. $D[a]$ never increases, because lines L6 and L11 accept only a strictly smaller distance. So the output is an upper bound on the exact nearest neighbor distance at every patch, and it can only improve with more iterations.
2. **Propagation lemma.** Let $R$ be a rectangle of centers of $A$ and $v$ an offset such that, for each $a$ in $R$, $a + v$ is a center of $B$ with $\operatorname{dist}(a, a + v) = 0$, and no other offset has distance 0. If any one center of $R$ has offset $v$ at the start of a forward pass, then after that pass and the next backward pass every center of $R$ has offset $v$. This is the remark of Barnes et al. that one correct offset in a coherent region fills the region, made exact.

No step proves how fast random search finds a first correct offset. That part is the probabilistic analysis below, and it holds only under its model.

## Complexity

The model is the [word RAM](/word-ram/): pixel values and SSD sums fit a word, and one random integer costs $O(1)$.

- **Time per iteration.** Each of the $n$ centers computes at most 2 propagation distances and $\lfloor \log_2 w \rfloor + 1$ random search distances, each of $p$ pixels. So one iteration costs $\Theta(n p \log w)$ for $w \ge 2$, and the initialization costs $\Theta(n p)$. Early termination lowers the constant but not the worst case.
- **Number of iterations.** $T$ is a parameter. Barnes et al. use 4 to 5 iterations and report that the field changes little after that. The total is $\Theta(n p T \log w)$.
- **Space.** The field and the distances take $\Theta(n)$ words beyond the images.
- **Brute force.** The exact field costs $\Theta(n m p)$, with $m$ the number of centers of $B$. The test file has it as the reference.

**Analysis of Barnes et al. (Section 3.3).** This is a probabilistic model, not a theorem about images. Let $M$ be the number of pixels of $B$. A random offset is the best one for a given patch with probability $1/M$, so among $M$ patches the chance that at least one gets its best offset is $1 - (1 - 1/M)^M \approx 1 - 1/e$. If any of $C$ offsets near the best one leads to it, a region of $m$ pixels that share an offset gets a hit with probability $p = 1 - (1 - C/M)^m$ per try (their Eq. 2). The expected number of failed iterations is $1/p - 1$, which for small $m/M$ is about $M/(C m) - 1/2$ (their Eq. 3). Their simulation reports, for a region of $20^2$ pixels in an image of $2000^2$ pixels, convergence with high probability after 5 iterations. Table 1 of the paper measures a speedup of 20 to 100 times over a kd-tree at similar error, on their test images and hardware (2009).

## Properties

- **Randomized and approximate.** The output depends on the random numbers. It is an upper bound on the exact distance at every patch, never below it.
- **Monotone.** No patch distance ever increases, in any step.
- **Coherence.** The method is fast when the true field is piecewise constant. On two unrelated noise images it is much weaker: in the tests, 16 iterations still leave the total distance above the exact one.
- **Anytime.** The field after each iteration is valid, so the program can stop at any time.
- **Order dependent.** The result depends on the scan order, since a pass uses the offsets improved earlier in the same pass.

## Variants and improvements

- **Prior initialization.** Barnes et al. also start from a field computed at a coarser level of an [image pyramid](/image-pyramid/), and scale it up to the next level.
- **GPU version.** The paper replaces the sequential scan by a jump flood scheme that updates all pixels in parallel, and reports about 7 times speedup over its CPU code.
- **Generalized PatchMatch.** Barnes et al. (ECCV 2010) search over rotations and scales too, keep $k$ nearest neighbors per patch, and allow any distance.
- **Other label spaces.** [PatchMatch stereo](/patchmatch-stereo/) propagates planes of disparity, and multi-view PatchMatch (Galliani et al. 2015, Schönberger et al. 2016) propagates depth and normal per pixel. The structure of propagation and random search stays the same.
- **Exact search.** For small images or few patches, the brute force or a [kd-tree](/kd-tree/) over the patch vectors gives the exact field.

## When to use it

Use PatchMatch for dense patch correspondence in image editing ([inpainting](/image-inpainting/), retargeting, reshuffling, texture transfer), in dense matching between views of a scene, and wherever the field is coherent. Use an exact search when you need the true nearest neighbor of each patch, and an [approximate nearest neighbor](/approximate-nearest-neighbor/) index over patch vectors when the queries are scattered and have no image structure.

## Pitfalls

- **Ties and strict tests.** Lines L6 and L11 must use a strict test. With $\le$ a patch may jump between offsets of equal distance, and the propagation lemma no longer holds.
- **Candidates outside $B$.** In line L6 the offset of a neighbor can point outside the centers of $B$, at the border. Skip such candidates; do not read pixels outside the image.
- **Fixed search center.** Line L7 fixes $v$ before the loop of line L9, as in Eq. 1 of the paper. Many programs move the center to each improvement; that is a variant, and it changes the results for a fixed seed.
- **One scan direction.** If every iteration scans forward, good offsets never flow up or left, and the patch in the upper left corner of a region keeps a bad offset. Alternate the order as in line L3.
- **Overflow.** An SSD sum is at most $p (2^b - 1)^2$ for $b$-bit pixels. A $7 \times 7$ patch of 8-bit pixels needs at most 22 bits, but large patches of 16-bit pixels need wide integers.

## Implementations

## History

Barnes, Shechtman, Finkelstein and Goldman (2009) presented PatchMatch at SIGGRAPH as the core of interactive tools for image retargeting, completion and reshuffling. Earlier texture synthesis already copied the matches of neighbors, but PatchMatch combined that propagation with random search at falling scales and analyzed why a few iterations suffice. Barnes et al. (2010) generalized it to $k$ neighbors, rotations and scales. Bleyer, Rhemann and Rother (2011) used it to search the infinite space of slanted planes in [stereo](/patchmatch-stereo/), and later multi-view stereo systems such as COLMAP adopted the same propagation scheme for depth and normal maps.

## References
