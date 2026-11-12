---
tag: E208HD
kind: algorithm
slug: fast-johnson-lindenstrauss-transform
name: Fast Johnson-Lindenstrauss transform
aliases:
- FJLT
- Ailon-Chazelle transform
area: machine-learning/dimensionality-reduction
level: research
summary: "A preconditioned sparse projection that embeds in O(d log d + k^3) time per point."
model: real-ram
complexity:
  vars: {d: the input dimension padded to a power of two, k: the target dimension, n: the number of points}
  time: {worst: "O(d log d + k log^2 n)"}
  space: {extra: "O(d + k log^2 n)"}
properties: {deterministic: false, exact: false, online: true, recursive: false}
history:
  year: 2006
  people: [Nir Ailon, Bernard Chazelle]
  note: "Ailon and Chazelle presented the transform at STOC 2006 (journal version 2009) for approximate nearest neighbor search; the subsampled randomized Hadamard transform is the variant that replaces the sparse Gaussian matrix by coordinate sampling."
prereqs: [johnson-lindenstrauss-lemma, fast-walsh-hadamard-transform, sparse-random-projection]
see_also: [random-projection, walsh-hadamard-transform, fast-fourier-transform, approximate-nearest-neighbor, randomized-pca, restricted-isometry-property, compressed-sensing, johnson-lindenstrauss-optimality]
sources:
  - paper: doi:10.1137/060673096
    title: Nir Ailon and Bernard Chazelle, The fast Johnson-Lindenstrauss transform and approximate nearest neighbors, SIAM Journal on Computing 39(1), 2009, pages 302 to 322
    locator: Lemma 1 (the FJLT lemma, Phi = PHD with q = min(Theta(eps^(p-2) log^p n / d), 1), success probability 2/3, time O(d log d + min(d eps^-2 log n, eps^(p-4) log^(p+1) n))) and the bound on the largest coordinate of HDx in its proof
  - paper: "Nir Ailon and Bernard Chazelle, Approximate nearest neighbors and the fast Johnson-Lindenstrauss transform, Proceedings of the 38th ACM Symposium on Theory of Computing (STOC), 2006, pages 557 to 563"
    locator: the conference version of the transform
  - paper: "Joel A. Tropp, Improved analysis of the subsampled randomized Hadamard transform, Advances in Adaptive Data Analysis 3(1-2), 2011, pages 115 to 126"
    locator: the subsampled randomized Hadamard transform and its subspace embedding bound
  - paper: "Jiří Matoušek, On variants of the Johnson-Lindenstrauss lemma, Random Structures and Algorithms 33(2), 2008, pages 142 to 156"
    locator: the simplified FJLT with a sparse matrix of random signs instead of Gaussian entries
---

The fast Johnson-Lindenstrauss transform (FJLT) of Ailon and Chazelle is a random linear map $\Phi = P H D$ from $\mathbb{R}^d$ to $\mathbb{R}^k$ with the guarantee of the [Johnson-Lindenstrauss lemma](/johnson-lindenstrauss-lemma/) and a lower cost per point. $D$ flips the sign of each coordinate at random, $H$ is the normalized Walsh-Hadamard matrix, and $P$ is a very sparse random matrix. The product $HD$ spreads the mass of every vector over all coordinates, so that after it a [sparse projection](/sparse-random-projection/) is safe even for vectors that were concentrated on a few coordinates. With the [fast Walsh-Hadamard transform](/fast-walsh-hadamard-transform/), $HDx$ costs $O(d \log d)$, and the whole map costs $O(d \log d + \min(d\varepsilon^{-2}\log n,\ \varepsilon^{-2}\log^3 n))$ per point, which is $O(d \log d + k^3)$ for $k = \Theta(\varepsilon^{-2} \log n)$. The subsampled randomized Hadamard transform (SRHT) replaces $P$ by the sampling of $k$ coordinates.

## In plain words

A sparse random projection is cheap, but it can miss a point whose length sits in one or two coordinates: most of the few random sums do not touch those coordinates. The fix is to mix the coordinates first.

The mixing step flips random signs and then applies a fixed transform that makes every new coordinate a plus or minus sum of all old coordinates. After it, with high probability every vector has its length spread almost evenly over all coordinates. Then a sparse projection, or even picking a few coordinates at random, keeps the length well. The fixed transform has a fast method, so the mixing costs little more than reading the vector.

## The problem

Input: $n$ vectors $x_1, \ldots, x_n \in \mathbb{R}^{d}$ (for distances, the vectors are the differences of the points), an accuracy $\varepsilon \in (0, 1/2)$, and a target dimension $k = c\, \varepsilon^{-2} \log n$.
Output: a random linear map $\Phi$ with, with probability at least $2/3$,

$$(1 - \varepsilon)\|x_i\| \le \|\Phi x_i\| \le (1 + \varepsilon)\|x_i\| \quad\text{for all } i,$$

such that $\Phi x$ can be computed for any $x$ in much less than the $O(dk)$ time of a dense [random projection](/random-projection/). Ailon and Chazelle also treat the target norm $\ell_1$; this page covers the Euclidean case.

## The algorithm

Let $d$ be a power of two (pad with zeros otherwise; padding does not change any norm). The three matrices are:

- $D$: a $d \times d$ diagonal matrix with independent entries $D_{ii} = \pm 1$, each with probability $1/2$.
- $H$: the $d \times d$ normalized Walsh-Hadamard matrix, $H_{ij} = d^{-1/2} (-1)^{\langle i - 1, j - 1 \rangle}$, where $\langle a, b \rangle$ is the number of positions in which the binary expansions of $a$ and $b$ both have a 1. $H$ is orthogonal.
- $P$: a $k \times d$ matrix with independent entries; $P_{ij} = 0$ with probability $1 - q$, and $P_{ij} \sim N(0, q^{-1})$ with probability $q$. For the Euclidean case $q = \min(\Theta(\log^2 n / d), 1)$.

The map is $\Phi x = P H D x / \sqrt{k}$. (The paper keeps the factor $\sqrt{k}$ inside the constant $\alpha_2$ of its statement; here the scale is in the map, so that $\mathbb{E}\|\Phi x\|^2 = \|x\|^2$.)

```pseudo id=main
FJLT(x ∈ ℝ^{d_0}, k, q)
L1  d ← the least power of two ≥ d_0; pad x with zeros to length d
L2  draw D_1..D_d independent, each +1 or −1 with probability 1/2         ▷ once, for all points
L3  draw P: each P_rj is 0 with probability 1 − q, else N(0, 1/q)         ▷ once, for all points
L4  u_i ← D_i · x_i for i ← 1 to d
L5  h ← 1
L6  while h < d do                                                        ▷ fast Walsh-Hadamard transform
L7      for each i with ⌊(i − 1)/h⌋ even: (u_i, u_{i+h}) ← (u_i + u_{i+h}, u_i − u_{i+h})
L8      h ← 2h
L9  u ← u / √d                                                            ▷ now u = H D x
L10 return P u / √k
```

Lines L5 to L8 are the iterative [fast Walsh-Hadamard transform](/fast-walsh-hadamard-transform/): $\log_2 d$ rounds of $d/2$ butterflies, $d \log_2 d$ additions and subtractions in total. Line L10 touches only the nonzero entries of $P$, about $k q d$ of them.

**SRHT.** Replace line L3 by "draw $c_1, \ldots, c_k$ uniform in $\{1, \ldots, d\}$" and line L10 by "return $\sqrt{d/k}\,(u_{c_1}, \ldots, u_{c_k})$". The map is $\sqrt{d/k}\, S H D$ with a sampling matrix $S$. It needs no random Gaussian numbers, and with a pruned transform the cost is $O(d \log k)$.

## Example

**The Walsh-Hadamard step.** Let $d = 8$ and $Dx = (1, 2, 3, 4, 0, 0, 0, 0)$. Before the division by $\sqrt{d}$:

| round | $h$ | vector after the round |
|---|---|---|
| start | | $(1, 2, 3, 4, 0, 0, 0, 0)$ |
| 1 | 1 | $(3, -1, 7, -1, 0, 0, 0, 0)$ |
| 2 | 2 | $(10, -2, -4, 0, 0, 0, 0, 0)$ |
| 3 | 4 | $(10, -2, -4, 0, 10, -2, -4, 0)$ |

Each round adds and subtracts pairs at distance $h$. The result equals the product of the $\pm 1$ Hadamard matrix with the vector. Its squared norm is $2(100 + 4 + 16) = 240 = 8 \cdot 30$, which is $d$ times the squared norm $30$ of the input, so after the division by $\sqrt{8}$ the norm is kept.

**Spreading a spike.** Let $d = 256$ and $x = 3 e_1$, a vector with all its mass on one coordinate. Every row of $H$ has entries $\pm 1/16$, so $HDx$ has all 256 coordinates equal to $\pm 3/16$. A sparse $P$ with $q = 1/16$ would see the original $x$ in a given row only with probability $1/16$, but it sees $HDx$ in about 16 coordinates of every row.

**Cost.** For $n = 10^6$ points, $d = 2^{16}$ and $\varepsilon = 0.2$, a dense Gaussian projection to $k = 3189$ dimensions costs $dk \approx 2.1 \cdot 10^8$ multiplications per point. The Walsh-Hadamard step costs $d \log_2 d \approx 10^6$ additions, and $P$ with $q = \ln^2 n / d \approx 0.0029$ has about $k (\ln n)^2 \approx 6.1 \cdot 10^5$ nonzeros.

## Correctness

The full proofs are in the [correctness proof](proofs/correctness.md). The argument has three parts.

1. **The transform is exact and keeps norms.** Lines L5 to L8 compute the product with the Sylvester-Hadamard matrix, by induction on $h$. $H$ and $D$ are orthogonal, so $\|HDx\| = \|x\|$.
2. **$HD$ flattens every vector.** Each coordinate of $HDx$ is $d^{-1/2} \sum_j \pm x_j$ with independent random signs. Hoeffding's bound gives $\Pr[|(HDx)_i| \ge s \|x\|] \le 2 e^{-s^2 d / 2}$, and a union bound over the $n d$ coordinates of the $n$ vectors gives, with probability at least $19/20$,

$$\max_{i} \|H D x_i\|_\infty \le \sqrt{\frac{2 \ln(40 n d)}{d}}\ \|x_i\| = O\Big(\sqrt{\frac{\log n}{d}}\Big)\|x_i\| \quad\text{when } \log d = O(\log n).$$

3. **A sparse projection is accurate on flat vectors.** For a fixed $u = HDx$ with $\|u\| = 1$, each row gives $\mathbb{E}(P_r u)^2 = 1$ and $\operatorname{Var}(P_r u)^2 = 2 + 3\frac{1 - q}{q}\sum_j u_j^4$. On flat vectors $\sum_j u_j^4 \le \|u\|_\infty^2 = O(\log n / d)$, so $q = \Theta(\log^2 n / d)$ keeps the variance $O(1)$, as for a dense Gaussian row. Ailon and Chazelle turn this into the tail bound of the JL lemma (their Lemma 1). For the SRHT, the proof file gives a complete argument: given the flat event, each sampled $d\,u_{c}^2$ lies in $[0, 2\ln(40nd)]$ with mean 1, and a Chernoff bound shows that $k \ge 6\varepsilon^{-2}\ln(40nd)\ln(40n)$ samples keep all $n$ norms within $1 \pm \varepsilon$ with probability at least $9/10$.

## Complexity

- **Time per point.** $O(d)$ for $D$, $d \log_2 d$ additions for the Walsh-Hadamard transform, and $O(kqd)$ expected for $P$. With $q = \min(\Theta(\log^2 n / d), 1)$ this is $O(d \log d + \min(dk,\ k \log^2 n))$, the bound $O(d \log d + \min(d\varepsilon^{-2}\log n,\ \varepsilon^{-2}\log^3 n))$ of the paper. Since $\varepsilon^{-2}\log^3 n \le k^3$ for $k = \Theta(\varepsilon^{-2}\log n)$, this is $O(d \log d + k^3)$.
- **SRHT time per point.** $O(d \log d)$ with the full transform, or $O(d \log k)$ when only the $k$ sampled outputs are computed.
- **Space.** $d$ signs and $O(k \log^2 n)$ expected nonzeros of $P$, or $k$ indices for the SRHT; $O(d)$ working space for the transform.
- **Comparison.** A dense projection costs $O(dk)$ per point. The FJLT is faster whenever $k$ is much larger than $\log d$, and it is faster than a [sparse projection](/sparse-random-projection/) with a guarantee for every vector when the density of the latter must be high.

## Properties

- Randomized, oblivious, and linear; one draw of $D$ and $P$ serves all points, including later ones.
- Unbiased: $\mathbb{E}\|\Phi x\|^2 = \|x\|^2$ for every $x$, without any flatness condition. Flatness is needed for the concentration only.
- The success probability in Lemma 1 of Ailon and Chazelle is $2/3$; repeating with fresh randomness and checking, or a larger constant in $k$, raises it.
- The Walsh-Hadamard step is exact in integer arithmetic; only $P$ and the final scale need real numbers.
- The FJLT keeps the target dimension $k = O(\varepsilon^{-2}\log n)$, which is optimal ([Johnson-Lindenstrauss optimality](/johnson-lindenstrauss-optimality/)); the SRHT analysis above needs an extra factor $\log(nd)$.

## Variants and improvements

- **SRHT.** $\sqrt{d/k}\, S H D$ with coordinate sampling. The simple Chernoff argument needs $k = O(\varepsilon^{-2}\log(nd)\log n)$. Tropp (2011) analysed it as a subspace embedding for randomized low-rank approximation and least squares, where it is the standard fast sketch; see [randomized PCA](/randomized-pca/).
- **Sign entries in $P$.** Matoušek (2008) showed that $P$ can have entries $\pm q^{-1/2}$ instead of Gaussian ones, with the same bounds.
- **Other orthogonal transforms.** The discrete Fourier transform or the discrete cosine transform with random signs also flatten vectors, with the [fast Fourier transform](/fast-fourier-transform/) in place of the Walsh-Hadamard transform.
- **Faster for small $k$.** Ailon and Liberty (2009) gave a transform with $O(d \log k)$ time for $k$ up to about $d^{1/2}$. Krahmer and Ward (2011) showed that any matrix with the [restricted isometry property](/restricted-isometry-property/), with random column signs, is a JL map; applied to the subsampled Hadamard matrix this gives $O(d \log d)$ time with $k = O(\varepsilon^{-2}\log n \cdot \mathrm{polylog}\, d)$.
- **Sparse JL.** The sparse transform of Kane and Nelson avoids the transform step and costs $O(\varepsilon^{-1}\log n)$ per nonzero input coordinate, which is better for very sparse inputs.

## When to use it

Use the FJLT or the SRHT for dense vectors in high dimension when $k$ is large enough that $dk$ dominates the cost, for example $d$ in the tens of thousands and $k$ in the hundreds or thousands. It is the standard fast sketch in randomized numerical linear algebra. For sparse inputs, a [sparse projection](/sparse-random-projection/) or a [count sketch](/count-sketch/) that costs time in proportion to the nonzeros is better, because $HD$ makes every vector dense. For small $d$ or small $k$, a dense projection is simpler and the constant factors favor it.

## Pitfalls

- **The same $D$ for all points.** $D$, $P$ (or the sample $S$) must be drawn once and kept, as for every random projection.
- **Padding.** For $d_0$ not a power of two, pad to $d$; this at most doubles the length. Using a Hadamard matrix of the wrong size, or truncating instead of padding, breaks orthogonality.
- **Normalization.** The fast transform computes the unnormalized $\pm 1$ product; the division by $\sqrt{d}$ is easy to forget, and it changes all norms by $\sqrt{d}$.
- **Sparse inputs.** $HD$ destroys sparsity, so a vector with 10 nonzeros costs as much as a dense one.
- **Low success probability.** The guarantee holds with probability $2/3$ in the paper. In a pipeline, check the distortion on a sample of pairs, or use a larger constant in $k$.
- **SRHT sampling.** Sampling with replacement is the easiest to analyse; without replacement is also fine. Forgetting the factor $\sqrt{d/k}$ scales all norms.

## Implementations

## History

Ailon and Chazelle introduced the transform at STOC 2006, with the journal version in SIAM Journal on Computing in 2009, as a fast first step for [approximate nearest neighbor](/approximate-nearest-neighbor/) search. The idea of a randomized Hadamard or Fourier transform as a preconditioner was used at the same time in randomized least squares by Sarlós (2006) and later by Rokhlin and Tygert (2008). Matoušek (2008) simplified the construction. Ailon and Liberty (2009) and Krahmer and Ward (2011) reduced the time further, and the SRHT became a standard tool of randomized numerical linear algebra through the analysis of Tropp (2011).

## References
