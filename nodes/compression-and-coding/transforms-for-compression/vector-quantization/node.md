---
tag: ERP96S
kind: technique
slug: vector-quantization
name: Vector quantization
aliases:
- VQ
- codebook coding
- LBG algorithm
- generalized Lloyd algorithm
area: compression-and-coding/transforms-for-compression
level: advanced
summary: "Quantize blocks of k values together by sending the index of the nearest codeword. The LBG algorithm designs the codebook by splitting and Lloyd iterations."
prereqs: [scalar-quantization, k-means]
see_also: [lloyds-algorithm, k-means-problem, product-quantization, color-quantization, nearest-neighbor-search, centroidal-voronoi-tessellation, lattice, lossy-compression]
sources:
  - paper: doi:10.1109/TCOM.1980.1094577
    title: Yoseph Linde, Andrés Buzo and Robert M. Gray, An algorithm for vector quantizer design, IEEE Transactions on Communications 28(1), 1980
    locator: pages 84 to 95 (the generalized Lloyd iteration for a training set, its convergence, and the design by splitting)
  - paper: doi:10.1109/TIT.1982.1056489
    title: Stuart P. Lloyd, Least squares quantization in PCM, IEEE Transactions on Information Theory 28(2), 1982
    locator: pages 129 to 137 (the two optimality conditions and Method I, for scalar quantizers)
  - paper: doi:10.1109/TIT.1979.1056067
    title: Allen Gersho, Asymptotically optimal block quantization, IEEE Transactions on Information Theory 25(4), 1979
    locator: pages 373 to 380 (the high-resolution distortion of k-dimensional quantizers, the normalized second moment and the conjecture on optimal cell shapes)
  - paper: doi:10.1109/18.42217
    title: Tom D. Lookabaugh and Robert M. Gray, High-resolution quantization theory and the vector quantizer advantage, IEEE Transactions on Information Theory 35(5), 1989
    locator: pages 1020 to 1033 (the space-filling, shape and memory advantages)
  - paper: doi:10.1109/18.720541
    title: Robert M. Gray and David L. Neuhoff, Quantization, IEEE Transactions on Information Theory 44(6), 1998
    locator: pages 2325 to 2383 (the history of vector quantization, the Lloyd algorithm and its variants, structured quantizers)
  - book: isbn:9780792391814
    title: Allen Gersho and Robert M. Gray, Vector Quantization and Signal Compression, Kluwer, 1992
    locator: Chapters 10 to 12 (structure and performance, optimality conditions and the generalized Lloyd design, constrained vector quantizers including tree-structured and lattice quantizers)
  - book: isbn:9780387985855
    title: John H. Conway and Neil J. A. Sloane, Sphere Packings, Lattices and Groups, third edition, Springer, 1999
    locator: Chapter 2, Section 3 (the quantizing problem and the normalized second moment G) and Chapter 20 (fast quantizing algorithms for lattices)
---

Vector quantization (VQ) maps a block of $k$ values, a vector in $\mathbb{R}^k$, to the nearest of $N$ *codewords* and sends only the index, $\lg N$ bits, or $\frac{1}{k} \lg N$ bits per value. It is the multi-dimensional form of [scalar quantization](/scalar-quantization/). Coding values together lets the codewords follow the correlation between them and lets the cells take shapes that fill space better than cubes, so at the same rate VQ has lower distortion than any scalar quantizer. Linde, Buzo and Gray (1980) designed codebooks from training data with the generalized Lloyd iteration and a splitting start, the LBG algorithm, which is [k-means](/k-means/) under another name.

## In plain words

Suppose you must send pairs of numbers, such as the heights of two neighbours, and the two numbers are usually close. Sending each number with its own short list of allowed values wastes codes on pairs like "very tall, very short" that almost never happen.

Instead, make one list of typical pairs, the codebook. For each real pair, find the closest typical pair and send its position in the list. The receiver has the same list and looks it up.

To build the list, start with one typical pair, the average. Split each typical pair into two that are a little apart. Then repeat two steps: give each real pair to its closest typical pair, and move each typical pair to the average of the pairs that it received. Stop when nothing improves, then split again until the list is long enough.

## When it applies

Use VQ when the values to code come in blocks with a joint distribution that a product of scalar quantizers fits badly: correlated samples, vectors whose values lie near a curve or a surface, or any source at low rates, where a scalar quantizer cannot spend a fraction of a bit per value. Typical blocks are a few pixels of an image, a few spectral parameters of speech, or the colours of an image. The cost grows fast with the dimension: a codebook at $R$ bits per value has $N = 2^{kR}$ codewords, so full search and storage take $\Theta(k\, 2^{kR})$, and $k R$ stays small, near 10 to 20 bits per vector, unless the codebook has structure.

**Definition.** A $k$-dimensional quantizer with $N$ codewords has a codebook $\{c_1, \ldots, c_N\} \subset \mathbb{R}^k$ and a partition of $\mathbb{R}^k$ into cells $S_1, \ldots, S_N$; $Q(x) = c_i$ for $x \in S_i$. The rate is $R = \frac{1}{k} \lg N$ bits per value with a fixed-length index, and the distortion is $D = \frac{1}{k} E\|X - Q(X)\|^2$ per value.

**The two conditions.** As in one dimension, an optimal quantizer satisfies:

1. *Nearest neighbour.* $S_i = \{x : \|x - c_i\| \le \|x - c_j\| \text{ for all } j\}$, with ties broken by a fixed rule. The cells are the [Voronoi cells](/voronoi-diagram/) of the codewords. Proof: for a fixed codebook, sending each $x$ to its nearest codeword minimizes each term of $E\|X - Q(X)\|^2$.
2. *Centroid.* $c_i = E[X \mid X \in S_i]$. Proof: for a fixed cell, $E[\|X - c\|^2 \mid S_i] = E[\|X - \mu_i\|^2 \mid S_i] + \|\mu_i - c\|^2$ with $\mu_i$ the conditional mean.

A quantizer that satisfies both, for a density, has centroidal Voronoi cells, which is the setting of [Lloyd's algorithm](/lloyds-algorithm/) and [centroidal Voronoi tessellations](/centroidal-voronoi-tessellation/) in geometry. For a finite training set, the problem of the best codebook is the [k-means problem](/k-means-problem/), which is NP-hard in general, so the iteration below finds a local optimum.

**Why VQ wins: the three advantages.** At high rate, a quantizer whose cells are all congruent to a polytope $P$ of volume $V$ has $D \approx G(P)\, V^{2/k}$, where $G(P) = \frac{1}{k} \int_P \|x\|^2 dx \,/\, V^{1 + 2/k}$ is the *normalized second moment* of the cell (Gersho 1979). Lookabaugh and Gray (1989) split the gain of VQ over scalar quantization at the same rate into three factors:

- *Space-filling advantage.* A cube has $G = 1/12$. The regular hexagon has $G = 5/(36\sqrt 3) \approx 0.0802$, a gain of 0.167 dB in two dimensions, and no cell shape in any dimension beats the sphere bound, which tends to $1/(2\pi e) \approx 0.0585$ as $k$ grows. So the space-filling gain is at most $10 \log_{10}(2\pi e / 12) \approx 1.53$ dB, or 0.254 bits per value.
- *Shape advantage.* The codewords can be dense where the density is high, in a way a product of scalar quantizers cannot match for a non-uniform density, even for independent values.
- *Memory advantage.* The codewords can follow the dependence between values. For strongly correlated values this is the largest of the three.

## The template

```pseudo id=main
LBG(T, N, ε)                        ▷ T: training vectors in ℝᵏ, N: a power of 2
L1  C ← {mean of T}
L2  while |C| < N
L3      C ← {c + εδ, c − εδ : c ∈ C}      ▷ split; δ: the spread of each coordinate (hole)
L4      repeat                              ▷ the generalized Lloyd iteration
L5          give each t ∈ T to its nearest codeword   ▷ nearest neighbour condition (hole: the search)
L6          move each codeword to the mean of its vectors; keep it if it has none   ▷ centroid condition
L7          D ← mean of ‖t − Q(t)‖² over T
L8      until D falls by less than a fraction θ of D
L9  return C
```

Each pass of lines L5 and L6 cannot raise $D$: line L5 makes the cells optimal for the codewords, and line L6 makes the codewords optimal for the cells. So $D$ is non-increasing; since there are finitely many partitions of $T$ and no partition repeats while $D$ falls strictly, the iteration stops at a fixed point that satisfies both conditions on the training set. One pass costs $O(|T| N k)$ with full search. Splitting gives every larger codebook a good start: the $2N$ codewords begin at the $N$ optimized ones, slightly moved apart, so the design never starts from random points far from the data.

**The holes.** The search of line L5 (full search, a [tree](/kd-tree/), or a [nearest-neighbour](/nearest-neighbor-search/) index), the start (splitting, random training vectors, or a smaller design), the distortion measure (squared error, weighted squared error, or the Itakura-Saito distortion of speech), and how to treat empty cells.

### Worked examples

**Splitting on six points.** Take $T = \{(0,0), (1,0), (0,1), (4,4), (5,4), (4,5)\}$. With one codeword at the mean $(7/3, 7/3)$, $D = 76/9 \approx 8.44$ per vector. Splitting and one Lloyd pass separate the two clusters, and the codewords move to their centroids $(1/3, 1/3)$ and $(13/3, 13/3)$, with $D = 4/9 \approx 0.44$ per vector. A second pass changes nothing, so the iteration stops.

**VQ against scalar quantization at 1 bit per value.** Take pairs $(a, b)$ of unit Gaussians with correlation $\rho = 0.9$, 2000 training pairs (seed 1) and 2000 test pairs (seed 2). Two scalar Lloyd-Max quantizers with 2 levels, $\pm\sqrt{2/\pi}$, give 4 codewords on a square and a measured test distortion of 0.352 per value (0.363 in theory). LBG with $N = 4$ gives 0.159 per value, 3.4 dB better at the same rate. Its four codewords lie on the line $a = b$, near $\pm 0.4$ and $\pm 1.45$: the design learned that the difference $a - b$ is small and spent all the bits on the sum. The rate distortion bound for this source at 2 bits per pair, by reverse water-filling over the eigenvalues 1.9 and 0.1, is $(1.9/16 + 0.1)/2 \approx 0.109$ per value.

**The hexagonal lattice.** Rounding to the hexagonal lattice with minimum distance 1 has cells of area $\sqrt3/2$. A Monte Carlo run of 100 000 uniform points gives $G$ within 1% of $5/(36\sqrt3) = 0.08019$, against $1/12 = 0.08333$ for the square lattice: a gain of 0.167 dB.

## Classic examples

- **Speech coding.** Linear prediction coefficients, as line spectral frequencies, are coded with split or multi-stage VQ in [linear predictive coding](/linear-predictive-coding/) speech coders, and CELP coders search a codebook of excitation vectors.
- **Colour quantization.** Choosing a palette of 256 colours for an image is VQ of the pixels in a 3D [colour space](/color-spaces/): [colour quantization](/color-quantization/) by k-means, [median cut](/median-cut/) or an [octree](/octree-color-quantization/) designs the codebook, and each pixel stores the index.
- **Image coding.** Early VQ image coders coded $4 \times 4$ blocks of pixels or of transform coefficients; texture compression formats for graphics hardware code small pixel blocks with a few colours per block, a form of VQ with a per-block codebook.
- **Approximate nearest-neighbour search.** [Product quantization](/product-quantization/) cuts a high-dimensional vector into sub-vectors and vector-quantizes each, so that distances can be computed from small tables.

## Variations

- **Tree-structured VQ.** Design a binary tree of 2-codeword quantizers: each node splits the training vectors of its cell. Encoding goes down the tree with two distance computations per level, $O(k \lg N)$ instead of $O(k N)$. The distortion is a little higher than full search over the same leaves, since a vector can go down the wrong branch near a boundary. On the correlated Gaussian above, a tree of depth 3 is never better than full search over its 8 leaves.
- **Lattice VQ.** Take the codewords from a lattice such as the hexagonal lattice $A_2$, $D_4$, $E_8$ or the Leech lattice. There is no codebook to store, and fast algorithms find the nearest lattice point (Conway and Sloane, Chapter 20); for $A_2$ the nearest point is the nearer of the nearest points of two rectangular lattices. Lattices give the space-filling advantage, but no shape or memory advantage on their own, so they are used with entropy coding or after a transform.
- **Product codes.** Gain-shape VQ codes the norm of the vector with a scalar quantizer and its direction with a VQ; mean-removed VQ codes the mean apart; multi-stage VQ codes the error of one VQ with another.
- **Predictive and finite-state VQ.** Predict the next vector from the past and quantize the error, or switch codebooks by a state, to use memory between vectors.
- **Entropy-constrained VQ.** Minimize $D + \lambda R$ with variable-length indices; the encoder adds $\lambda$ times the code length of each index to its distance.
- **Soft assignment.** With a Gaussian mixture in place of hard cells, the iteration becomes [expectation maximization](/expectation-maximization/).

## Pitfalls

- **Exponential size.** The codebook grows as $2^{kR}$. Increase the dimension only with a structured codebook.
- **Local optima.** The Lloyd iteration stops at a fixed point that may be poor. Splitting, several starts or k-means++ seeding help.
- **Empty cells.** A codeword may lose all its training vectors. Keep it, or move it into the cell with the largest distortion.
- **Splitting a zero mean.** Multiplying a codeword by $1 \pm \varepsilon$ does nothing when it is near 0, which is the usual mean of a centred source. Add a perturbation scaled to the data instead, as line L3 does.
- **Training and test data.** The training distortion is optimistic, more so for large codebooks with few vectors per cell. Report the distortion on separate test data, as in the example above.
- **Rate per value.** Compare quantizers at the same rate per value, $\frac{1}{k} \lg N$, not per vector.

## Exercises

1. Show that the generalized Lloyd iteration on a finite training set stops after finitely many passes when ties in line L5 are broken in a fixed way.
2. For the unit square cell, compute $G = 1/12$ directly, and for the regular hexagon with inradius $\frac12$ show that $G = 5/(36\sqrt3)$.
3. For pairs of Gaussians with correlation $\rho$, show that a codebook on the line $a = b$ with $N$ points gives at best $\frac12[(1+\rho) D_N + (1 - \rho)]$ per value, where $D_N$ is the Lloyd-Max distortion of a unit Gaussian with $N$ levels, and compare with the measured 0.159 for $\rho = 0.9$ and $N = 4$.

## References
