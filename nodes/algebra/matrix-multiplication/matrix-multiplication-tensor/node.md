---
tag: DRM7QA
kind: concept
slug: matrix-multiplication-tensor
name: Matrix multiplication tensor
aliases:
- matmul tensor
- Strassen tensor
- tensor of matrix multiplication
area: algebra/matrix-multiplication
level: research
summary: The tensor ⟨n,m,p⟩ = Σ e_ij⊗e_jk⊗e_ki encodes the n×m by m×p matrix product; its rank is the fewest multiplications of a bilinear algorithm, and its growth gives ω.
prereqs: [naive-matrix-multiplication, kronecker-product, tensor-rank]
see_also: [bilinear-complexity, border-rank, matrix-multiplication-exponent, strassen-algorithm, laderman-algorithm, schonhage-asymptotic-sum-inequality, laser-method, alphatensor]
sources:
  - book: isbn:9783540605829
    title: Peter Bürgisser, Michael Clausen and M. Amin Shokrollahi, Algebraic Complexity Theory, Springer, Grundlehren der mathematischen Wissenschaften 315 (1997)
    locator: Chapter 14 (the tensor of a bilinear map, rank, restriction, direct sums and Kronecker products, the cyclic symmetry of ⟨n,m,p⟩) and Chapter 15 (the exponent ω defined from the rank of ⟨n,n,n⟩)
  - book: isbn:9780821869079
    title: J. M. Landsberg, Tensors, Geometry and Applications, American Mathematical Society, Graduate Studies in Mathematics 128 (2012)
    locator: Chapter 2, Section 2.5 and Chapter 3 (the matrix multiplication tensor, its symmetry group and its rank and border rank)
  - paper: doi:10.4086/toc.gs.2013.005
    title: Markus Bläser, Fast Matrix Multiplication, Theory of Computing Graduate Surveys 5 (2013)
    locator: Sections 2 to 4 (bilinear algorithms as tensor decompositions, the notation ⟨k,m,n⟩, permutations and products of matrix multiplication tensors)
  - paper: doi:10.1007/BF02165411
    title: Volker Strassen, Gaussian elimination is not optimal, Numerische Mathematik 13 (1969)
    locator: pp. 354 to 356 (the seven products for 2×2 blocks, which are a decomposition of ⟨2,2,2⟩)
  - paper: "Hans F. de Groote, On varieties of optimal algorithms for the computation of bilinear mappings II. Optimal algorithms for 2×2-matrix multiplication, Theoretical Computer Science 7(2) (1978)"
    locator: the main theorem (all decompositions of ⟨2,2,2⟩ into 7 terms are equivalent under the symmetry group of the tensor)
  - paper: "John E. Hopcroft and Jean Musinski, Duality applied to the complexity of matrix multiplication and other bilinear forms, SIAM Journal on Computing 2(3) (1973)"
    locator: the duality theorem (the six orders of n, m, p need the same number of multiplications)
---

The matrix multiplication tensor $\langle n, m, p \rangle$ is the tensor of order three that encodes the product of an $n \times m$ matrix and an $m \times p$ matrix. Written as a trilinear form it is $\operatorname{tr}(XYZ) = \sum_{i,j,k} x_{ij} y_{jk} z_{ki}$. Every bilinear algorithm for the product is a way to write this tensor as a sum of rank-one tensors, so its [tensor rank](/tensor-rank/) is the least number of multiplications such an algorithm needs. [Strassen's algorithm](/strassen-algorithm/) is a decomposition of $\langle 2, 2, 2 \rangle$ into $7$ terms, and the [exponent ω](/matrix-multiplication-exponent/) is the growth rate of the rank of $\langle n, n, n \rangle$. The tensor has a large symmetry group, it is invariant under cyclic shifts of its three factors, and Kronecker products of these tensors are again matrix multiplication tensors, which is the reason why recursive algorithms work.

## In plain words

Multiplying two matrices means: for each entry of the answer, multiply matching entries of a row and a column, and add. Write down, for each pair of input entries and each output entry, a one if that pair is multiplied into that output entry and a zero if not. This gives a cube of zeros and ones. The cube does not depend on the numbers in the matrices, only on their sizes.

A fast method for multiplying matrices is the same thing as a way to write this cube as a short sum of simple cubes. Each simple cube is one multiplication. So questions about fast matrix products become questions about one fixed cube.

## The idea

**Definition.** Let $F$ be a field, or more generally a commutative ring. Let $e_{ij}$ denote the matrix with a $1$ in position $(i, j)$ and zeros elsewhere. For integers $n, m, p \ge 1$,

$$\langle n, m, p \rangle = \sum_{i=0}^{n-1} \sum_{j=0}^{m-1} \sum_{k=0}^{p-1} e_{ij} \otimes e_{jk} \otimes e_{ki} \;\in\; F^{n \times m} \otimes F^{m \times p} \otimes F^{p \times n}.$$

It is an array of size $nm \times mp \times pn$ with exactly $nmp$ entries equal to $1$ and all others $0$. The entry at $\big((i, j), (j', k), (k', i')\big)$ is $1$ exactly when $j = j'$, $k = k'$ and $i = i'$.

**Three readings of the same object.**

- **Trilinear form.** With matrices of indeterminates $X$ ($n \times m$), $Y$ ($m \times p$) and $Z$ ($p \times n$), the tensor is the polynomial $\sum_{i,j,k} x_{ij} y_{jk} z_{ki} = \operatorname{tr}(XYZ)$.
- **Bilinear map.** The map $(X, Y) \mapsto XY$. The coefficient of $z_{ki}$ in $\operatorname{tr}(XYZ)$ is $\sum_j x_{ij} y_{jk} = (XY)_{ik}$. So the third factor is indexed by the transpose of the output: the $z$ variable $z_{ki}$ stands for the output entry $c_{ik}$. This transpose is a convention, chosen to make the symmetry below visible.
- **Decompositions are algorithms.** A decomposition $\langle n, m, p \rangle = \sum_{s=1}^{r} u_s \otimes v_s \otimes w_s$, with $u_s \in F^{n \times m}$, $v_s \in F^{m \times p}$ and $w_s \in F^{p \times n}$, is the bilinear algorithm that forms the $r$ products $M_s = \big(\sum_{ij} u_s[i][j] \, a_{ij}\big) \cdot \big(\sum_{jk} v_s[j][k] \, b_{jk}\big)$ and outputs $c_{ik} = \sum_s w_s[k][i] \, M_s$. Conversely, each bilinear algorithm with $r$ products gives such a decomposition. So the [rank](/tensor-rank/) $R(\langle n, m, p \rangle)$ is the [bilinear complexity](/bilinear-complexity/) of the product.

**Basic properties.**

- **Cyclic symmetry.** Since $\operatorname{tr}(XYZ) = \operatorname{tr}(YZX)$, moving the factors one step around gives $\langle m, p, n \rangle$. So $R(\langle n, m, p \rangle) = R(\langle m, p, n \rangle) = R(\langle p, n, m \rangle)$. In algorithm terms: a bilinear algorithm for one shape can be turned into one for each cyclic shift with the same number of products.
- **Transposition.** $\operatorname{tr}(XYZ) = \operatorname{tr}(Z^{\mathsf T} Y^{\mathsf T} X^{\mathsf T})$ gives $R(\langle n, m, p \rangle) = R(\langle p, m, n \rangle)$. With the cyclic shifts, the rank is the same for all six orders of $n, m, p$. Hopcroft and Musinski (1973) first proved this duality for algorithms.
- **Kronecker products.** $\langle n, m, p \rangle \otimes \langle n', m', p' \rangle \cong \langle nn', mm', pp' \rangle$, where the product of tensors is the [Kronecker product](/kronecker-product/) taken in each of the three factors. In matrix terms: an $nn' \times mm'$ matrix is an $n \times m$ matrix of $n' \times m'$ blocks. With $R(T \otimes T') \le R(T) R(T')$ this gives $R(\langle n^k, m^k, p^k \rangle) \le R(\langle n, m, p \rangle)^k$, the recursion of every divide and conquer algorithm.
- **Direct sums.** $\langle n, m, p \rangle \oplus \langle n', m', p' \rangle$ is the tensor of two independent products, on disjoint sets of variables. The unit tensor $\langle r \rangle = \sum_{s=1}^{r} e_s \otimes e_s \otimes e_s$ is the direct sum of $r$ copies of $\langle 1, 1, 1 \rangle$, that is $r$ independent scalar products. A tensor $T$ has rank at most $r$ exactly when $T$ is a restriction of $\langle r \rangle$: $T = (A \otimes B \otimes C) \langle r \rangle$ for some linear maps $A, B, C$.
- **Symmetry group.** For invertible $P$ ($n \times n$), $Q$ ($m \times m$) and $S$ ($p \times p$), the substitution $X \mapsto P X Q^{-1}$, $Y \mapsto Q Y S^{-1}$, $Z \mapsto S Z P^{-1}$ leaves $\operatorname{tr}(XYZ)$ unchanged. So it maps each decomposition to another decomposition with the same number of terms. For square sizes the cyclic shift and the transposition join this group. De Groote (1978) proved that all decompositions of $\langle 2, 2, 2 \rangle$ with $7$ terms are equivalent under this group: in this sense Strassen's algorithm is the only optimal one.
- **Flattenings.** Read $\langle n, m, p \rangle$ as a matrix of size $nm \times (mp \cdot pn)$. Its rows are linearly independent, so its rank is $nm$. The three flattenings give $R(\langle n, m, p \rangle) \ge \max(nm, mp, pn)$, which is $n^2$ for square sizes. Much better lower bounds need other tools, see the [quadratic lower bound](/matrix-multiplication-quadratic-lower-bound/).
- **The exponent.** $\omega = \inf \{ \tau : R(\langle n, n, n \rangle) = O(n^{\tau}) \}$, and $R(\langle n, m, p \rangle) \le r$ implies $\omega \le 3 \log r / \log(nmp)$. The same holds with the [border rank](/border-rank/) in place of the rank.

## Examples

The examples below were checked by a script that builds the tensors as arrays, sums the decompositions and computes the flattening ranks over $\mathbb{Q}$.

1. **Small shapes.** $\langle 1, 1, 1 \rangle = e \otimes e \otimes e$ is one scalar product. $\langle 1, m, 1 \rangle$ is a [dot product](/dot-product/) of length $m$; its array is $m \times m \times 1$ with $m$ ones, and its rank is $m$. $\langle n, 1, p \rangle$ is the outer product $x y^{\mathsf T}$ of two vectors; it is the unit tensor $\langle np \rangle$ in disguise, of rank $np$, since all $np$ products $x_i y_k$ are needed. $\langle n, m, 1 \rangle$ is [matrix times vector](/matrix-vector-multiplication/), of rank $nm$.
2. **Flattening ranks.** For $\langle 2, 3, 4 \rangle$ the array is $6 \times 12 \times 8$ with $24$ ones, and the three flattenings have ranks $6$, $12$ and $8$. So $12 \le R(\langle 2, 3, 4 \rangle) \le 24$. For $\langle 3, 3, 3 \rangle$ the array is $9 \times 9 \times 9$ with $27$ ones and each flattening has rank $9$; the true rank lies between $19$ and $23$.
3. **The $2 \times 2$ case.** $\langle 2, 2, 2 \rangle$ is a $4 \times 4 \times 4$ array with $8$ ones, one for each term $a_{ij} b_{jk}$ of the triple loop. Index $A$ and $B$ entries as $2i + j$ and the $z$ entries as $2k + i$. Strassen's products are $M_1 = (a_{00} + a_{11})(b_{00} + b_{11})$, $M_2 = (a_{10} + a_{11}) b_{00}$, $M_3 = a_{00}(b_{01} - b_{11})$, $M_4 = a_{11}(b_{10} - b_{00})$, $M_5 = (a_{00} + a_{01}) b_{11}$, $M_6 = (a_{10} - a_{00})(b_{00} + b_{01})$ and $M_7 = (a_{01} - a_{11})(b_{10} + b_{11})$, with $c_{00} = M_1 + M_4 - M_5 + M_7$, $c_{01} = M_3 + M_5$, $c_{10} = M_2 + M_4$ and $c_{11} = M_1 - M_2 + M_3 + M_6$. The seven rank-one tensors $u_s \otimes v_s \otimes w_s$, where $w_s[k][i]$ is the coefficient of $M_s$ in $c_{ik}$, have $7 \cdot 4 \cdot 4 \cdot 4 = 448$ entries in total; their sum has exactly the $8$ ones of $\langle 2, 2, 2 \rangle$ and zeros elsewhere, and all the other entries cancel.
4. **The Kronecker square.** $\langle 2, 2, 2 \rangle \otimes \langle 2, 2, 2 \rangle$ has $64$ ones in a $16 \times 16 \times 16$ array. Renaming the index pair $((i_1, j_1), (i_2, j_2))$ as $(2 i_1 + i_2, 2 j_1 + j_2)$ in each factor turns it into $\langle 4, 4, 4 \rangle$ exactly. The product of Strassen's decomposition with itself has $49$ terms, so $R(\langle 4, 4, 4 \rangle) \le 49$, against $64$ for the triple loop.
5. **The trilinear form with numbers.** For $X = \begin{pmatrix} 1 & 2 \\ 3 & 4 \end{pmatrix}$, $Y = \begin{pmatrix} 5 & 6 \\ 7 & 8 \end{pmatrix}$ and $Z = \begin{pmatrix} 1 & 0 \\ 2 & -1 \end{pmatrix}$, $XY = \begin{pmatrix} 19 & 22 \\ 43 & 50 \end{pmatrix}$ and $\operatorname{tr}(XYZ) = 13$. The value is $\sum_{i,k} (XY)_{ik} z_{ki} = 19 \cdot 1 + 22 \cdot 2 + 43 \cdot 0 + 50 \cdot (-1) = 13$, which shows how $z_{ki}$ pairs with $c_{ik}$.
6. **Cyclic shift.** Moving each index triple $(a, b, c)$ of $\langle 2, 3, 4 \rangle$ to $(b, c, a)$ gives exactly the array of $\langle 3, 4, 2 \rangle$. So any bilinear algorithm for the $2 \times 3$ by $3 \times 4$ product gives one for the $3 \times 4$ by $4 \times 2$ product with the same number of products.

## Where it is used

- **Fast matrix multiplication.** Each upper bound on $\omega$ starts with a decomposition, or an approximate decomposition, of a matrix multiplication tensor or of a tensor that contains many of them: Strassen's $\langle 2, 2, 2 \rangle$ with $7$ terms, [Laderman's](/laderman-algorithm/) $\langle 3, 3, 3 \rangle$ with $23$, Bini's border rank $5$ for a partial product, and the sums of products used by the [asymptotic sum inequality](/schonhage-asymptotic-sum-inequality/) and the [laser method](/laser-method/).
- **Computer search.** Searches for small decompositions, by numerical optimization, by SAT solvers and by reinforcement learning such as [AlphaTensor](/alphatensor/), all work directly on the array of $\langle n, m, p \rangle$ for small $n, m, p$.
- **Rectangular products.** The symmetry of the six orders shows that the cost of a rectangular product depends only on the multiset $\{n, m, p\}$, which is used in the analysis of rectangular exponents $\omega(a, b, c)$.
- **Lower bounds.** Bounds on rank and border rank, by flattenings, by substitution and by methods from algebraic geometry, are stated for this tensor. See [border rank](/border-rank/) and the [quadratic lower bound](/matrix-multiplication-quadratic-lower-bound/).
- **Other bilinear problems.** The same tensor language describes [polynomial multiplication](/polynomial-multiplication/), multiplication in field extensions and convolution, so methods carry over between them.

## References
