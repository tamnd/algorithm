---
tag: JHP9MS
kind: algorithm
slug: laderman-algorithm
name: Laderman's algorithm
aliases:
- Laderman's 3×3 algorithm
- Laderman's 23-multiplication scheme
area: algebra/matrix-multiplication
level: advanced
summary: Multiplies two 3×3 matrices with 23 scalar multiplications instead of 27; used recursively on blocks it costs O(n^(log3 23)), about n^2.854, which is worse than Strassen.
model: algebraic-computation-tree
complexity:
  vars: {n: the order of the matrices}
  time: {worst: Θ(n^(log3 23)), average: Θ(n^(log3 23)), best: Θ(n^(log3 23))}
  space: {extra: Θ(n^2)}
properties: {deterministic: true, recursive: true, in_place: false}
history:
  year: 1976
  people: [Julian D. Laderman]
  note: Laderman published a noncommutative scheme for 3×3 matrices with 23 multiplications in the Bulletin of the AMS.
prereqs: [strassen-algorithm, divide-and-conquer-matrix-multiplication]
see_also: [tensor-rank, bilinear-complexity, matrix-multiplication-tensor, matrix-multiplication-exponent, alphatensor, naive-matrix-multiplication, winograd-inner-product-algorithm]
sources:
  - paper: doi:10.1090/S0002-9904-1976-13988-2
    title: Julian D. Laderman, A noncommutative algorithm for multiplying 3×3 matrices using 23 multiplications, Bulletin of the American Mathematical Society 82(1), 1976
    locator: pp. 126 to 128 (the 23 products and the formulas for the nine entries)
  - paper: "Rodney W. Johnson and Aileen M. McLoughlin, Noncommutative bilinear algorithms for 3×3 matrix multiplication, SIAM Journal on Computing 15(2), 1986"
    locator: pp. 595 to 603 (families of 23-product schemes that are not equivalent to Laderman's)
  - paper: "Markus Bläser, On the complexity of the multiplication of matrices of small formats, Journal of Complexity 19(1), 2003"
    locator: the lower bound 19 on the rank of 3×3 matrix multiplication
  - paper: "Marijn J. H. Heule, Manuel Kauers and Martina Seidl, New ways to multiply 3×3-matrices, Journal of Symbolic Computation 104, 2021"
    locator: the SAT search and the thousands of inequivalent schemes with 23 products
  - book: isbn:9783540605829
    title: Peter Bürgisser, Michael Clausen and M. Amin Shokrollahi, Algebraic Complexity Theory
    locator: Chapters 14 and 15 (bilinear complexity, tensor rank and the exponent obtained from a rank bound)
---

Laderman's algorithm multiplies two $3 \times 3$ matrices with $23$ multiplications instead of the $27$ of the [triple loop](/naive-matrix-multiplication/). It does not use commutativity, so, like [Strassen's algorithm](/strassen-algorithm/), it applies to $3 \times 3$ grids of blocks and can recurse. That gives $\Theta(n^{\log_3 23})$ ring operations, about $n^{2.854}$, which is slower than Strassen's $n^{2.807}$. Its value is as a fact about [tensor rank](/tensor-rank/): the rank of $3 \times 3$ matrix multiplication is at most $23$, and after fifty years no one has found a scheme with $22$.

## In plain words

To multiply two three by three tables, the school method makes 27 small products, three for each of the nine answer cells. Laderman found 23 cleverly mixed products: each one multiplies a sum of some entries of the first table by a sum of some entries of the second. Adding and subtracting these 23 results in the right way gives all nine answer cells. The 4 saved products cost many extra additions.

The trick works when the entries are themselves tables, because it never swaps the order of a product. So a large table can be cut into nine blocks, the 23 block products done by the same trick, and so on. This beats the school method on large tables, but loses to Strassen's method, which saves one product in eight on two by two grids. For three by three grids to win against Strassen, one would need 21 products.

## The problem

The input is an $n \times m$ matrix $A$ and an $m \times p$ matrix $B$ over a ring $R$, which need not be commutative but must allow subtraction. The output is $C = AB$. The cost is counted in ring operations in the [algebraic model](/algebraic-computation-tree/), as on the [Strassen page](/strassen-algorithm/). For the bounds we take $n = m = p$.

The scheme, with indices from $1$ to $3$, is a list of $23$ products
$$M_r = \Big(\sum_{i,j} u^{(r)}_{ij} a_{ij}\Big) \Big(\sum_{j,k} v^{(r)}_{jk} b_{jk}\Big), \qquad u^{(r)}_{ij}, v^{(r)}_{jk} \in \{-1, 0, 1\},$$
with the left factor always on the left:

| $r$ | left factor | right factor |
|---|---|---|
| 1 | $a_{11}+a_{12}+a_{13}-a_{21}-a_{22}-a_{32}-a_{33}$ | $b_{22}$ |
| 2 | $a_{11}-a_{21}$ | $-b_{12}+b_{22}$ |
| 3 | $a_{22}$ | $-b_{11}+b_{12}+b_{21}-b_{22}-b_{23}-b_{31}+b_{33}$ |
| 4 | $-a_{11}+a_{21}+a_{22}$ | $b_{11}-b_{12}+b_{22}$ |
| 5 | $a_{21}+a_{22}$ | $-b_{11}+b_{12}$ |
| 6 | $a_{11}$ | $b_{11}$ |
| 7 | $-a_{11}+a_{31}+a_{32}$ | $b_{11}-b_{13}+b_{23}$ |
| 8 | $-a_{11}+a_{31}$ | $b_{13}-b_{23}$ |
| 9 | $a_{31}+a_{32}$ | $-b_{11}+b_{13}$ |
| 10 | $a_{11}+a_{12}+a_{13}-a_{22}-a_{23}-a_{31}-a_{32}$ | $b_{23}$ |
| 11 | $a_{32}$ | $-b_{11}+b_{13}+b_{21}-b_{22}-b_{23}-b_{31}+b_{32}$ |
| 12 | $-a_{13}+a_{32}+a_{33}$ | $b_{22}+b_{31}-b_{32}$ |
| 13 | $a_{13}-a_{33}$ | $b_{22}-b_{32}$ |
| 14 | $a_{13}$ | $b_{31}$ |
| 15 | $a_{32}+a_{33}$ | $-b_{31}+b_{32}$ |
| 16 | $-a_{13}+a_{22}+a_{23}$ | $b_{23}+b_{31}-b_{33}$ |
| 17 | $a_{13}-a_{23}$ | $b_{23}-b_{33}$ |
| 18 | $a_{22}+a_{23}$ | $-b_{31}+b_{33}$ |
| 19 | $a_{12}$ | $b_{21}$ |
| 20 | $a_{23}$ | $b_{32}$ |
| 21 | $a_{21}$ | $b_{13}$ |
| 22 | $a_{31}$ | $b_{12}$ |
| 23 | $a_{33}$ | $b_{33}$ |

The nine outputs are sums of products, all with sign $+$:

$$\begin{aligned}
c_{11} &= M_6+M_{14}+M_{19}, & c_{12} &= M_1+M_4+M_5+M_6+M_{12}+M_{14}+M_{15}, \\
c_{13} &= M_6+M_7+M_9+M_{10}+M_{14}+M_{16}+M_{18}, & c_{21} &= M_2+M_3+M_4+M_6+M_{14}+M_{16}+M_{17}, \\
c_{22} &= M_2+M_4+M_5+M_6+M_{20}, & c_{23} &= M_{14}+M_{16}+M_{17}+M_{18}+M_{21}, \\
c_{31} &= M_6+M_7+M_8+M_{11}+M_{12}+M_{13}+M_{14}, & c_{32} &= M_{12}+M_{13}+M_{14}+M_{15}+M_{22}, \\
c_{33} &= M_6+M_7+M_8+M_9+M_{23}.
\end{aligned}$$

This is Laderman's scheme (1976). Copies differ in the numbering of the products; this table is the one checked by the tests of the implementation.

## The algorithm

For larger matrices the entries $a_{ij}$ and $b_{jk}$ become blocks. A side that is not a multiple of $3$ is padded with zero rows or columns at that level.

```pseudo id=main
LADERMAN(A, B, n0)                     ▷ A is n × m, B is m × p, n0 ≥ 1
L1  if min(n, m, p) ≤ n0 then return the classical product AB
L2  pad n, m and p with zeros up to multiples of 3, recurse, and cut the result back to n × p
L3  split A into 3 × 3 blocks A_ij of size n/3 × m/3, and B into blocks B_jk of size m/3 × p/3
L4  for r ← 1 to 23 do M_r ← LADERMAN(Σ u_ij^(r) A_ij, Σ v_jk^(r) B_jk, n0)
L5  form each block C_ik as the sum of its products M_r from the table of outputs
L6  return the matrix with blocks C_ik
```

Line L1 is the base case; with $n_0 = 1$ only $1 \times 1$ products, and products with an empty side, reach the triple loop. Line L2 runs only when a side is not a multiple of $3$, and its recursive call goes straight to line L3. Line L4 forms the two factors of each product by block additions and recurses on them. Line L5 adds the products. The order of every block product is kept, which is what makes the recursion valid over matrices.

## Example

Take
$$A = \begin{pmatrix} 1 & 2 & 3 \\ 4 & 5 & 6 \\ 7 & 8 & 10 \end{pmatrix}, \qquad B = \begin{pmatrix} 1 & 0 & 2 \\ 0 & 1 & 1 \\ 1 & 1 & 0 \end{pmatrix}, \qquad AB = \begin{pmatrix} 4 & 5 & 4 \\ 10 & 11 & 13 \\ 17 & 18 & 22 \end{pmatrix}.$$

The 23 products are

| $r$ | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| $M_r$ | $-21$ | $-3$ | $-20$ | $16$ | $-9$ | $1$ | $0$ | $6$ | $15$ | $-20$ | $-8$ | $15$ |

| $r$ | 13 | 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| $M_r$ | $0$ | $3$ | $0$ | $16$ | $-3$ | $-11$ | $0$ | $6$ | $8$ | $0$ | $0$ |

For example $M_1 = (1+2+3-4-5-8-10) \cdot 1 = -21$ and $M_{16} = (-3+5+6)(1+1-0) = 16$. Then

- $c_{11} = M_6 + M_{14} + M_{19} = 1 + 3 + 0 = 4$,
- $c_{12} = -21 + 16 - 9 + 1 + 15 + 3 + 0 = 5$,
- $c_{22} = M_2 + M_4 + M_5 + M_6 + M_{20} = -3 + 16 - 9 + 1 + 6 = 11$,
- $c_{31} = 1 + 0 + 6 - 8 + 15 + 0 + 3 = 17$,
- $c_{33} = M_6 + M_7 + M_8 + M_9 + M_{23} = 1 + 0 + 6 + 15 + 0 = 22$,

and the other four entries check the same way. Many products are $0$ here only because $B$ has zeros; on random inputs all $23$ are nonzero.

## Correctness

The nine identities are polynomial identities in the $18$ entries, in which each monomial $a_{ij} b_{jk}$ keeps $a$ on the left. They are proved by grouping. The four partial sums
$$\begin{aligned}
M_2+M_4+M_6 &= a_{21}b_{11}+a_{22}(b_{11}-b_{12}+b_{22}), & M_6+M_7+M_8 &= a_{31}b_{11}+a_{32}(b_{11}-b_{13}+b_{23}), \\
M_{14}+M_{16}+M_{17} &= a_{23}b_{31}+a_{22}(b_{23}+b_{31}-b_{33}), & M_{12}+M_{13}+M_{14} &= a_{33}b_{31}+a_{32}(b_{22}+b_{31}-b_{32})
\end{aligned}$$
each follow in one line, and adding $M_5$, $M_9$, $M_{18}$ or $M_{15}$ to them gives $a_{21}b_{12}+a_{22}b_{22}$, $a_{31}b_{13}+a_{32}b_{23}$, $a_{22}b_{23}+a_{23}b_{33}$ and $a_{32}b_{22}+a_{33}b_{32}$. The outputs $c_{22}$, $c_{33}$, $c_{23}$ and $c_{32}$ add one more product to these. The outputs $c_{21}$ and $c_{31}$ add two groups and the long product $M_3$ or $M_{11}$, which cancels all the unwanted terms. The outputs $c_{12}$ and $c_{13}$ use two completed groups, minus $M_2$ and $M_{13}$, or $M_8$ and $M_{17}$, plus the long product $M_1$ or $M_{10}$. The proofs section writes out each case. A script also checks the nine identities on random integer matrices and the coefficient tables symbolically.

For the recursion, block multiplication gives $C_{ik} = \sum_j A_{ij} B_{jk}$, and the identities hold in any ring, in particular in the ring of block matrices, since no step uses commutativity. Padding with zeros does not change the top-left $n \times p$ block of the product. Termination follows because each call at line L4 has every side at most $\lceil s / 3 \rceil < s$ for each side $s \ge 2$.

## Complexity

- **Multiplications.** For $n = 3^t$ and $n_0 = 1$, $T(n) = 23\, T(n/3)$ with $T(1) = 1$, so exactly $23^t = n^{\log_3 23}$ scalar multiplications, with $\log_3 23 \approx 2.854$.
- **Additions.** The scheme uses $98$ additions and subtractions on blocks: $28$ for the left factors, $28$ for the right factors and $42$ for the outputs, counted as written above. So $S(n) = 23\, S(n/3) + 98 (n/3)^2$ with $S(1) = 0$, whose solution is $S(n) = 7(n^{\log_3 23} - n^2)$. The total is $8 n^{\log_3 23} - 7 n^2$ ring operations, against $2n^3 - n^2$ for the triple loop. Both counts are checked by script.
- **Against the triple loop.** One level of Laderman with classical products of size $s = n/3$ costs $46 s^3 + 75 s^2$ operations, against $54 s^3 - 9 s^2$ for the triple loop, so it wins in operation count when $s \ge 11$, that is for $n \ge 33$.
- **Against Strassen.** Strassen's exponent $\log_2 7 \approx 2.807$ is smaller. A $3 \times 3$ scheme would need at most $21$ products to beat it, since $\log_3 21 \approx 2.771$ while $\log_3 22 \approx 2.814$.
- **Space.** The $23$ products of one level take $23 (n/3)^2$ entries, and the levels form a geometric sum, so $\Theta(n^2)$ extra entries in total.
- **Recursion depth.** $O(\log_3 \max(n, m, p))$.

These are proved operation counts. Running time in practice also depends on memory traffic, and the large number of additions makes the scheme slow on real machines; it is not used in libraries.

## Properties

- **Noncommutative and bilinear.** Each product is a linear form in $A$ times a linear form in $B$. This is what allows the block recursion, and it means the scheme is a rank-$23$ decomposition of the [matrix multiplication tensor](/matrix-multiplication-tensor/) $\langle 3, 3, 3 \rangle$.
- **Coefficients in $\{-1, 0, 1\}$.** So it works over every ring, including $\mathbb{Z}$, $\mathbb{Z}/q\mathbb{Z}$ and $\mathbb{F}_2$, with no division.
- **Not unique.** Many inequivalent schemes with $23$ products exist (Johnson and McLoughlin, 1986; Heule, Kauers and Seidl found thousands by SAT solving, 2021).
- **Numerical behaviour.** Like other fast bilinear schemes, it satisfies only a normwise error bound in floating point, not the componentwise bound of the classical product.

## Variants and improvements

- **Mixed radix.** Combining Laderman's and Strassen's schemes as tensor products gives $\langle 6, 6, 6 \rangle$ with $7 \cdot 23 = 161$ products instead of $216$, and in general handles $n = 2^a 3^b$ with $7^a 23^b$ products.
- **Commutative rings.** If the entries commute, products that are not bilinear are allowed, and Makarov (1986) is reported to use $22$ multiplications for $3 \times 3$. Such a scheme cannot recurse on blocks. The [Winograd inner product algorithm](/winograd-inner-product-algorithm/) is another commutative method.
- **Computer search.** SAT solvers, flip graphs and [AlphaTensor](/alphatensor/) search for low-rank decompositions of small matrix multiplication tensors. None has found a $3 \times 3$ scheme with $22$ products.
- **Rank bounds.** The rank $R(\langle 3,3,3 \rangle)$ is known to lie between $19$ (Bläser, 2003) and $23$. Any rank $r$ gives $\omega \le \log_3 r$, see [the exponent](/matrix-multiplication-exponent/) and [bilinear complexity](/bilinear-complexity/).

## When to use it

Almost never as a practical algorithm: for large matrices Strassen's algorithm has a smaller exponent, fewer additions per product saved, and a simpler structure, and for moderate sizes a [tuned classical product](/blocked-matrix-multiplication/) is faster than either. Laderman's scheme is useful as a test case for search methods, as a small exact witness that $R(\langle 3,3,3 \rangle) \le 23$, and when an application really is made of $3 \times 3$ blocks with very expensive entries, such as large polynomials or matrices over a slow ring, where saving products matters more than the additions.

## Pitfalls

- **Swapping factors.** Writing a product as $(\sum v b)(\sum u a)$ is harmless for numbers but wrong for blocks. Keep every $A$ factor on the left.
- **Misprints.** Copies of the scheme in the literature and online differ in signs and indices. Check any table against the triple loop on random integer matrices before using it.
- **Padding.** Sides that are not powers of $3$ must be padded at each level, or handled with a cutoff; padding only once to the next power of $3$ can multiply the work by up to $23$.
- **Expecting a speedup over Strassen.** $23$ products on $3 \times 3$ is worse, per level of the recursion, than $7$ on $2 \times 2$, since $23 > 7^{\log_2 3} \approx 21.8$.

## Implementations

## History

Strassen's 1969 scheme for $2 \times 2$ matrices raised the question of how many multiplications $3 \times 3$ matrices need. Hopcroft and Kerr, and Winograd, showed in 1971 that $2 \times 2$ needs $7$. Julian Laderman published the $23$ product scheme in 1976 in a three page note in the Bulletin of the AMS. Johnson and McLoughlin described families of other schemes in 1986. Bläser proved the lower bound $19$ in 2003. Heule, Kauers and Seidl used SAT solvers (2021) to find thousands of further schemes, all with $23$ products. Whether $22$ is possible is still open.

## References
