---
tag: JDSJ23
kind: definition
slug: ldpc-code
name: LDPC code
aliases:
- low-density parity-check code
area: compression-and-coding/error-correcting-codes
level: advanced
summary: A linear code defined by a sparse parity-check matrix, with few ones per row and column. Belief propagation on its Tanner graph decodes it in linear time close to capacity.
history:
  year: 1962
  people: [Robert G. Gallager, David J. C. MacKay, Radford M. Neal, Thomas J. Richardson, Rüdiger Urbanke]
  note: Gallager defined regular LDPC codes and their iterative decoders in 1962. MacKay and Neal found them again in 1996, and Richardson and Urbanke gave density evolution in 2001.
prereqs: [parity-check-matrix, tanner-graph]
see_also: [belief-propagation-decoding, min-sum-decoding, bit-flipping-decoding, expander-codes, turbo-code, binary-erasure-channel, peeling-decoding, sparse-matrix]
sources:
  - paper: doi:10.1109/TIT.1962.1057683
    title: R. G. Gallager, Low-density parity-check codes, IRE Transactions on Information Theory 8(1), 1962, pages 21 to 28
    locator: The (n, j, k) codes with j ones in each column and k in each row, the construction from j bands, and the iterative decoders
  - paper: "D. J. C. MacKay and R. M. Neal, Near Shannon limit performance of low density parity check codes, Electronics Letters 32(18), 1996, pages 1645 to 1646"
    title: Near Shannon limit performance of low density parity check codes
    locator: The rediscovery of LDPC codes and their simulated performance with belief propagation on the Gaussian channel
  - paper: doi:10.1109/18.910577
    title: T. J. Richardson and R. L. Urbanke, The capacity of low-density parity-check codes under message-passing decoding, IEEE Transactions on Information Theory 47(2), 2001, pages 599 to 618
    locator: Density evolution, the concentration of the ensemble, and the decoding threshold
  - paper: "S. Kudekar, T. J. Richardson and R. L. Urbanke, Threshold saturation via spatial coupling: why convolutional LDPC ensembles perform so well over the BEC, IEEE Transactions on Information Theory 57(2), 2011, pages 803 to 834"
    title: "Threshold saturation via spatial coupling: why convolutional LDPC ensembles perform so well over the BEC"
    locator: Example 5, the belief propagation threshold of the (3, 6) regular ensemble on the BEC, about 0.4294
  - book: isbn:9780521852296
    title: Tom Richardson and Rüdiger Urbanke, Modern Coding Theory, Cambridge University Press, 2008
    locator: Chapter 3 (LDPC ensembles with degree distributions, the design rate, and density evolution on the binary erasure channel)
  - url: https://www.3gpp.org/DynaReport/38212.htm
    title: 3GPP TS 38.212, NR, Multiplexing and channel coding
    locator: Section 5.3.2 (the LDPC codes of the data channels, from two base graphs lifted by a factor Z)
---

A low-density parity-check (LDPC) code is a [linear code](/linear-code/) given as the null space of a [parity-check matrix](/parity-check-matrix/) $H$ that is sparse: each column has a small number of ones, and the number does not grow with the length. The sparseness is not a property of the code alone but of the matrix chosen to describe it, and it is what makes iterative decoding work. The [Tanner graph](/tanner-graph/) of $H$ has one edge per one of $H$, so it has $O(n)$ edges, and [belief propagation decoding](/belief-propagation-decoding/) on it costs $O(n)$ per iteration. Long LDPC codes with well chosen degrees come close to the capacity of many channels. They are used in 5G NR, Wi-Fi, digital television and storage.

## Definition

**LDPC code.** Let $H$ be an $m \times n$ binary matrix. The code is $C = \{c \in \{0, 1\}^n : H c^T = 0\}$. A family of such codes, with $n \to \infty$, is low density when the number of ones in each column is bounded by a constant. The rows of $H$ need not be independent.

**Regular codes (Gallager 1962).** A $(d_v, d_c)$-regular LDPC code has exactly $d_v$ ones in each column and $d_c$ ones in each row, so $n d_v = m d_c$. Its *design rate* is $1 - m/n = 1 - d_v / d_c$. The true rate $k/n$ is at least the design rate, since $\operatorname{rank} H \le m$.

**Irregular codes and degree distributions.** In the Tanner graph, let $\lambda_i$ be the fraction of edges that touch a variable node of degree $i$, and $\rho_i$ the fraction of edges that touch a check node of degree $i$. The edge perspective generating functions are

$$\lambda(x) = \sum_i \lambda_i x^{i-1}, \qquad \rho(x) = \sum_i \rho_i x^{i-1}.$$

The number of variable nodes per edge is $\sum_i \lambda_i / i = \int_0^1 \lambda(x)\,dx$, and the same holds for checks with $\rho$. So $m / n = \int_0^1 \rho / \int_0^1 \lambda$, and the design rate is

$$r(\lambda, \rho) = 1 - \frac{\int_0^1 \rho(x)\, dx}{\int_0^1 \lambda(x)\, dx}.$$

If a fraction $L_i$ of the variable nodes have degree $i$, then $\lambda_i = i L_i / \sum_j j L_j$, since a node of degree $i$ has $i$ edges.

**The ensemble.** For given $n$, $\lambda$ and $\rho$, the ensemble is the set of Tanner graphs with these degrees, where the edges are matched by a uniform random permutation of the edge sockets. Results about LDPC codes are often statements about most codes of an ensemble.

**Density evolution and the threshold (Richardson and Urbanke 2001).** For a channel family with a parameter, such as the erasure probability $\varepsilon$ of the [binary erasure channel](/binary-erasure-channel/), density evolution tracks the distribution of the messages of belief propagation in the limit $n \to \infty$, where the graph looks like a tree to any fixed depth. On the BEC the message is either known or erased, and the erasure probability of a variable to check message after $\ell$ iterations is

$$x_{\ell+1} = \varepsilon\, \lambda\bigl(1 - \rho(1 - x_\ell)\bigr), \qquad x_0 = \varepsilon.$$

A check sends a known value when all its other $d - 1$ inputs are known, which has probability $(1 - x)^{d-1}$, averaged by $\rho$. A variable sends an erasure when its channel value and all its other $d - 1$ inputs are erased. The threshold $\varepsilon^{BP}$ is the largest $\varepsilon$ for which $x_\ell \to 0$. Below it, belief propagation on a random code of the ensemble corrects all but a vanishing fraction of the erasures as $n \to \infty$; above it, a positive fraction stays erased. The threshold is $\inf_{x \in (0, 1]} x / \lambda(1 - \rho(1 - x))$.

## Examples and non-examples

**Gallager's construction.** For $d_c \mid n$, Gallager's matrix has $d_v$ bands of $n / d_c$ rows each. In the first band, row $i$ has ones in the columns $i d_c$ to $i d_c + d_c - 1$. Each other band is the first band with its columns permuted at random. Each column has one 1 in each band. The rows of each band add to the all-ones row, so the $d_v$ bands give $d_v - 1$ linear dependencies among the rows, and the rank is at most $m - d_v + 1$. The implementation checks, for $(n, d_v, d_c) = (12, 3, 4)$, $(24, 3, 6)$, $(40, 4, 8)$ and $(60, 3, 6)$, that the code dimension is at least $n - m + d_v - 1$.

**The (3, 6) ensemble on the BEC.** The design rate is $1 - 3/6 = 1/2$, so the capacity limit is $\varepsilon = 1/2$. Here $\lambda(x) = x^2$ and $\rho(x) = x^5$, and density evolution is $x_{\ell + 1} = \varepsilon (1 - (1 - x_\ell)^5)^2$. Bisection gives the threshold $0.42944$, which matches the value about 0.4294 of Kudekar, Richardson and Urbanke (Example 5). At $\varepsilon = 0.42$ the recursion falls below $10^{-12}$ in 400 iterations; at $\varepsilon = 0.44$ it stays above 0.3. The $(4, 8)$ ensemble has the same design rate but a lower threshold, about 0.3834. Among regular ensembles of rate 1/2, $d_v = 3$ is the best for belief propagation.

**An irregular ensemble.** Let half of the variable nodes have degree 2, 30 percent degree 3 and 20 percent degree 8, with all checks of degree 6. The average variable degree is $1 + 0.9 + 1.6 = 3.5$, so $\lambda_2 = 1/3.5 = 2/7$, $\lambda_3 = 9/35$ and $\lambda_8 = 16/35$. Then $\int \lambda = \tfrac{2/7}{2} + \tfrac{9/35}{3} + \tfrac{16/35}{8} = 2/7$, $\int \rho = 1/6$, and the design rate is $1 - \tfrac{1/6}{2/7} = 5/12$. The same number follows from $m/n = 3.5/6 = 7/12$.

**5G NR.** TS 38.212, Section 5.3.2, defines the LDPC codes of the data channels from two base graphs, base graph 1 for large blocks and high rates and base graph 2 for small blocks and low rates. Each base graph entry is replaced by a $Z \times Z$ zero matrix or a cyclic shift of the identity, for a lifting size $Z$ up to 384. The result is a quasi-cyclic LDPC code; the standard gives the shift values of each base graph in tables and no test vectors of codewords.

**Non-example: the Hamming code.** The [Hamming code](/hamming-code/) $[7, 4]$ has a parity-check matrix with 12 ones out of 21 entries. More to the point, the Hamming codes of length $2^r - 1$ have columns of weight up to $r$, which grows with the length, so they do not form a low density family. Belief propagation on their Tanner graphs, which have many short cycles, is far from optimal.

**Non-example: a sparse $H$ with columns of weight 2.** Such codes are LDPC codes, but poor ones. Their Tanner graphs are the cycle codes of graphs, and their minimum distance grows only like the logarithm of $n$. Gallager showed that most codes with $d_v \ge 3$ have minimum distance that grows linearly in $n$.

## Related definitions

- [Tanner graph](/tanner-graph/): the bipartite graph of $H$ on which the decoders run.
- [Belief propagation decoding](/belief-propagation-decoding/), [min-sum decoding](/min-sum-decoding/) and [bit-flipping decoding](/bit-flipping-decoding/): the three main iterative decoders, from the most to the least accurate.
- [Peeling decoding](/peeling-decoding/): the form of belief propagation on the erasure channel, which density evolution on the BEC describes.
- [Expander codes](/expander-codes/): LDPC codes whose Tanner graph is a good expander, which gives a guarantee for a simple flipping decoder.
- [Turbo code](/turbo-code/): the other iteratively decoded family that comes close to capacity.

## References
