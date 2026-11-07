---
tag: JGTACH
kind: concept
slug: tensor-rank
name: Tensor rank
aliases:
- rank of a tensor
- CP rank
- canonical polyadic rank
area: algebra/matrix-multiplication
level: advanced
summary: The rank of a tensor is the least count of rank-one tensors u⊗v⊗w that sum to it; for the matrix multiplication tensor it is the fewest multiplications of a bilinear algorithm.
prereqs: [rank, kronecker-product, strassen-algorithm]
see_also: [matrix-multiplication-tensor, bilinear-complexity, border-rank, matrix-multiplication-exponent, matrix-multiplication-quadratic-lower-bound, laderman-algorithm, alphatensor, tensor-product]
sources:
  - book: isbn:9783540605829
    title: Peter Bürgisser, Michael Clausen and M. Amin Shokrollahi, Algebraic Complexity Theory
    locator: Chapter 14, Multiplicative and bilinear complexity (rank of tensors, the equality of rank and bilinear complexity, flattening bounds, and the cyclic symmetry of the matrix multiplication tensor)
  - book: isbn:9780821869079
    title: J. M. Landsberg, Tensors, Geometry and Applications, American Mathematical Society, Graduate Studies in Mathematics 128
    locator: Chapters 2 and 3 (rank and border rank of tensors, flattenings, and the rank of matrix multiplication)
  - paper: doi:10.1137/07070111X
    title: Tamara G. Kolda and Brett W. Bader, Tensor decompositions and applications, SIAM Review 51(3) (2009)
    locator: Section 3, CP decomposition (the CP rank, its dependence on the field, and the gap between rank and border rank)
  - paper: doi:10.1016/0196-6774(90)90014-6
    title: Johan Håstad, Tensor rank is NP-complete, Journal of Algorithms 11(4) (1990)
    locator: pp. 644 to 654 (deciding rank at most r is NP-complete over finite fields and NP-hard over the rationals)
  - paper: "Shmuel Winograd, On multiplication of 2×2 matrices, Linear Algebra and its Applications 4 (1971)"
    locator: the main theorem (7 multiplications are necessary for 2×2 matrices)
  - paper: "Yaroslav Shitov, A counterexample to Strassen's direct sum conjecture, Acta Mathematica 222(2) (2019)"
    locator: the main theorem (tensor rank is not additive under direct sums)
---

The rank of a tensor $T \in U \otimes V \otimes W$ is the least number $r$ such that $T$ is a sum of $r$ tensors of the form $u \otimes v \otimes w$. For a matrix it is the usual [rank](/rank/), but for tensors of order three it behaves very differently: it can depend on the field, it is NP-hard to compute, and it can drop in a limit, which gives the [border rank](/border-rank/). Its importance for algorithms comes from one fact: the rank of the [matrix multiplication tensor](/matrix-multiplication-tensor/) $\langle n, m, p \rangle$ is the least number of multiplications of a [bilinear algorithm](/bilinear-complexity/) for the $n \times m$ by $m \times p$ product, and its growth in $n$ determines the [exponent ω](/matrix-multiplication-exponent/). [Strassen's algorithm](/strassen-algorithm/) is a decomposition of $\langle 2, 2, 2 \rangle$ into $7$ rank-one terms.

## In plain words

A matrix is a flat table of numbers. A tensor of order three is a cube of numbers. The simplest cubes are built from three lists by multiplying one entry from each list in every way. The rank of a cube is the least number of such simple cubes that add up to it.

Multiplying two matrices can be written as one fixed cube of zeros and ones. Each simple cube in a sum for it is one multiplication in a method for matrix products. So the rank of this cube is the least number of multiplications any such method needs. For two by two matrices it is seven, which is Strassen's method.

## The idea

**Definition.** Let $F$ be a field and $U, V, W$ vector spaces over $F$ of dimensions $a, b, c$. A tensor $T \in U \otimes V \otimes W$ is an array $T[i][j][k]$ of size $a \times b \times c$. A rank-one tensor is $u \otimes v \otimes w$ with entries $u_i v_j w_k$, for nonzero vectors. The rank is

$$R(T) = \min \Big\{ r : T = \sum_{s=1}^{r} u_s \otimes v_s \otimes w_s \Big\},$$

and $R(0) = 0$. A sum with $r$ terms is a rank-$r$ (or CP) decomposition. In data analysis the same notion is called the canonical polyadic, CANDECOMP or PARAFAC decomposition.

**Bilinear maps.** A tensor $T$ is the same as the bilinear map $\phi : U^* \times V^* \to W$ with $\phi(x, y)_k = \sum_{i, j} T[i][j][k] \, x_i y_j$. A decomposition $T = \sum_s u_s \otimes v_s \otimes w_s$ is the bilinear algorithm that computes the $r$ products $m_s = \langle u_s, x \rangle \cdot \langle v_s, y \rangle$ of linear forms and outputs $\phi(x, y) = \sum_s m_s w_s$. So $R(T)$ is the bilinear complexity of $\phi$. Up to a factor of at most $2$, it is also the least number of multiplications of any straight-line program, even one that multiplies two forms in the same input.

**Basic properties.**

- **Flattenings.** Reading $T$ as an $a \times bc$ matrix, or as $b \times ac$ or $c \times ab$, gives three matrices, and $R(T)$ is at least the rank of each. This gives the bound $R(\langle n, n, n \rangle) \ge n^2$.
- **Symmetry.** $R$ does not change under invertible linear maps on $U$, $V$, $W$, nor under a permutation of the three factors. For matrix multiplication, $R(\langle n, m, p \rangle) = R(\langle m, p, n \rangle) = R(\langle n, p, m \rangle)$, and so on for all six orders, by the cyclic symmetry of the trace $\operatorname{tr}(XYZ)$ and by transposition.
- **Sums and products.** $R(T \oplus T') \le R(T) + R(T')$ and $R(T \otimes T') \le R(T) R(T')$, where $\otimes$ is the [Kronecker product](/kronecker-product/) of tensors. The second gives the recursion of Strassen's algorithm: $R(\langle 2^k, 2^k, 2^k \rangle) \le 7^k$.
- **Not additive.** Strassen asked in 1973 whether $R(T \oplus T') = R(T) + R(T')$ always holds. Shitov (2019) found a counterexample.
- **Dependence on the field.** Rank can drop in a field extension; see the example of complex multiplication below.
- **Hard to compute.** Deciding $R(T) \le r$ is NP-complete over finite fields and NP-hard over $\mathbb{Q}$ (Håstad 1990), while matrix rank takes polynomial time.
- **Not closed.** The set of tensors of rank at most $r$ need not be closed: a limit of rank-$2$ tensors can have rank $3$. The least $r$ such that $T$ is a limit of tensors of rank at most $r$ is the [border rank](/border-rank/) $\underline{R}(T) \le R(T)$.
- **Generic rank.** A tensor of size $n \times n \times n$ with random entries over $\mathbb{C}$ has rank about $n^2 / 3$ with probability $1$, since the set of tensors of rank $r$ has dimension at most $r(3n - 2)$.

## Examples

- **Matrix multiplication.** $\langle n, m, p \rangle = \sum_{i < n, \, j < m, \, k < p} e_{ij} \otimes e_{jk} \otimes e_{ki}$ in $F^{n \times m} \otimes F^{m \times p} \otimes F^{p \times n}$. The triple loop is the decomposition into its $nmp$ terms, so $R(\langle n, m, p \rangle) \le nmp$. Strassen's algorithm gives $R(\langle 2, 2, 2 \rangle) \le 7$, and Winograd (1971) proved $R(\langle 2, 2, 2 \rangle) = 7$; it also has border rank $7$ (Landsberg 2006). For $\langle 3, 3, 3 \rangle$ the rank is known only to lie between $19$ (Bläser 2003) and $23$ ([Laderman](/laderman-algorithm/) 1976).
- **Complex multiplication.** The product $(a + bi)(c + di) = (ac - bd) + (ad + bc) i$ is a bilinear map $\mathbb{R}^2 \times \mathbb{R}^2 \to \mathbb{R}^2$. The classical formula uses $4$ products. Gauss's formula uses $3$: $k_1 = c(a + b)$, $k_2 = a(d - c)$, $k_3 = b(c + d)$, then the real part is $k_1 - k_3$ and the imaginary part is $k_1 + k_2$. Over $\mathbb{R}$ its rank is exactly $3$. Over $\mathbb{C}$ the same tensor has rank $2$. Put $s = a + ib$, $t = a - ib$, $s' = c + id$ and $t' = c - id$. Then $ss' = (ac - bd) + i(ad + bc)$ and $tt' = (ac - bd) - i(ad + bc)$, so both outputs are linear combinations of the two products $ss'$ and $tt'$.
- **Polynomial multiplication.** The product of two polynomials of degree $n - 1$ has rank $2n - 1$ over a field with at least $2n - 2$ elements: evaluate both at $2n - 1$ points, multiply the values, and interpolate. The flattening bound shows that fewer terms are impossible.
- **A tensor of rank $3$ and border rank $2$.** $W = e_0 \otimes e_0 \otimes e_1 + e_0 \otimes e_1 \otimes e_0 + e_1 \otimes e_0 \otimes e_0$ has rank $3$. But $\frac{1}{\varepsilon} \big( (e_0 + \varepsilon e_1)^{\otimes 3} - e_0^{\otimes 3} \big) = W + \varepsilon (\ldots) + \varepsilon^2 e_1^{\otimes 3}$, so it is a limit of tensors of rank $2$.
- **A non-example.** The identity $\sum_{i} e_i \otimes e_i \otimes e_i$ of size $n \times n \times n$ has rank $n$ (by flattening), not $1$: the rank of a tensor is not the rank of one slice.

## Where it is used

- **Fast matrix multiplication.** Each bound $R(\langle n, m, p \rangle) \le r$ gives $\omega \le 3 \log r / \log(nmp)$. Searches for small decompositions, by hand, by numerical optimization, by SAT solvers and by reinforcement learning ([AlphaTensor](/alphatensor/)), all look for low-rank decompositions of small matrix multiplication tensors.
- **Lower bounds.** The best lower bounds on $R(\langle n, n, n \rangle)$ are about $3n^2$ (Landsberg 2014, and Massarenti and Raviolo 2013), far from the upper bounds. See the [quadratic lower bound](/matrix-multiplication-quadratic-lower-bound/).
- **Asymptotic methods.** Border rank, direct sums and tensor powers lead to the [asymptotic sum inequality](/schonhage-asymptotic-sum-inequality/) and the [laser method](/laser-method/).
- **Data analysis and machine learning.** Low-rank CP decompositions model data with three or more indices, for example in chemometrics, signal processing and the compression of neural network layers. Kruskal's theorem gives conditions under which the decomposition is unique.
- **Other bilinear problems.** The rank of polynomial and integer multiplication, of convolution, and of multiplication in finite field extensions guides the design of algorithms such as [Karatsuba's](/karatsuba-multiplication/) and Toom and Cook's.

## References
