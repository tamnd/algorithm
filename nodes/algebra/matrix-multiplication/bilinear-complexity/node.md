---
tag: JR8FWZ
kind: concept
slug: bilinear-complexity
name: Bilinear complexity
aliases:
- bilinear rank
- bilinear multiplicative complexity
- rank of a bilinear map
area: algebra/matrix-multiplication
level: research
summary: The least number of products of a linear form in x and a linear form in y that compute a bilinear map; it equals the tensor rank and is within a factor 2 of the multiplicative complexity.
prereqs: [tensor-rank, matrix-multiplication-tensor, straight-line-program]
see_also: [border-rank, matrix-multiplication-exponent, strassen-algorithm, winograd-inner-product-algorithm, karatsuba-multiplication, polynomial-multiplication, matrix-multiplication-quadratic-lower-bound, alphatensor]
sources:
  - book: isbn:9783540605829
    title: Peter Bürgisser, Michael Clausen and M. Amin Shokrollahi, Algebraic Complexity Theory, Springer, Grundlehren der mathematischen Wissenschaften 315 (1997)
    locator: Chapter 14, Multiplicative and bilinear complexity (quadratic and bilinear computations, the inequalities between multiplicative complexity and rank, and the rank of a tensor)
  - paper: "Volker Strassen, Vermeidung von Divisionen, Journal für die reine und angewandte Mathematik 264 (1973)"
    locator: pp. 184 to 202 (divisions can be removed from programs for polynomials of bounded degree, so quadratic computations are as good as general ones for bilinear maps over infinite fields)
  - paper: "Shmuel Winograd, A new algorithm for inner product, IEEE Transactions on Computers C-17(7) (1968)"
    locator: pp. 693 to 694 (the commutative algorithm with about n^3/2 multiplications for n×n matrices)
  - paper: "Alfred Alder and Volker Strassen, On the algorithmic complexity of associative algebras, Theoretical Computer Science 15(2) (1981)"
    locator: pp. 201 to 211 (the lower bound 2 dim A minus the number of maximal two-sided ideals for the rank of an algebra A)
  - paper: "Markus Bläser, A 5/2 n^2-lower bound for the rank of n×n-matrix multiplication over arbitrary fields, 40th IEEE Symposium on Foundations of Computer Science (FOCS 1999)"
    locator: the main theorem (rank of ⟨n,n,n⟩ at least 5n^2/2 minus 3n)
  - paper: "J. M. Landsberg, New lower bounds for the rank of matrix multiplication, SIAM Journal on Computing 43(1) (2014)"
    locator: the main theorem (rank of ⟨n,n,n⟩ at least 3n^2 minus lower order terms)
  - paper: doi:10.4086/toc.gs.2013.005
    title: Markus Bläser, Fast Matrix Multiplication, Theory of Computing Graduate Surveys 5 (2013)
    locator: Sections 2 and 3 (bilinear algorithms, rank, and the relation between bilinear and general algorithms)
---

The bilinear complexity of a bilinear map $\phi(x, y)$ is the least number $r$ of products $\ell_s(x) \cdot \ell'_s(y)$, each a linear form in $x$ times a linear form in $y$, such that every output of $\phi$ is a linear combination of these products. It is the same number as the [tensor rank](/tensor-rank/) $R(\phi)$ of the tensor of $\phi$, and for the [matrix multiplication tensor](/matrix-multiplication-tensor/) it is the cost measure behind every fast recursive algorithm: [Strassen's algorithm](/strassen-algorithm/) is a bilinear algorithm with $7$ products for $2 \times 2$ matrices. Linear operations (additions, subtractions and multiplications by constants) are free in this measure. Allowing products of forms in which $x$ and $y$ are mixed gives the multiplicative complexity $L(\phi)$, and $L(\phi) \le R(\phi) \le 2 L(\phi)$. Only bilinear algorithms stay correct when the entries do not commute, which is what recursion on blocks needs.

## In plain words

Take a rule that combines two lists of numbers into a third, where each output is a sum of terms "an entry of the first list times an entry of the second list". Multiplying matrices, multiplying polynomials and multiplying complex numbers are all such rules.

A bilinear algorithm first forms some sums of entries of the first list and some sums of entries of the second list. Then it multiplies them in pairs, one sum from each list. Then it gets each output as a sum of these products. Additions are counted as free. The bilinear complexity is the least number of pair products needed. For the product of two by two matrices it is seven, not eight.

## The idea

**Bilinear maps and algorithms.** Let $F$ be a field and let $\phi : F^a \times F^b \to F^c$ be bilinear, $\phi(x, y)_k = \sum_{i, j} t_{ijk} x_i y_j$. A bilinear algorithm of length $r$ for $\phi$ is a list of linear forms $f_1, \ldots, f_r$ on $F^a$, linear forms $g_1, \ldots, g_r$ on $F^b$ and vectors $w_1, \ldots, w_r \in F^c$ with

$$\phi(x, y) = \sum_{s=1}^{r} f_s(x) \, g_s(y) \, w_s \quad \text{for all } x, y.$$

The least such $r$ is the bilinear complexity $R(\phi)$. Comparing coefficients shows that this is the same as $t = \sum_s f_s \otimes g_s \otimes w_s$ for the coefficient tensor $t = (t_{ijk})$, so $R(\phi)$ is the [tensor rank](/tensor-rank/) of $t$. The algorithm is a [straight-line program](/straight-line-program/) of three phases: linear forms, $r$ products, linear combinations.

**Quadratic algorithms and multiplicative complexity.** A quadratic algorithm may multiply two linear forms in all the variables: $\phi(x, y) = \sum_{s=1}^{L} \ell_s(x, y) \, \ell'_s(x, y) \, w_s$. The least such $L$ is the multiplicative complexity $L(\phi)$. Strassen (1973) showed that, over an infinite field, general straight-line programs that count only the nonscalar multiplications and divisions are no better than quadratic algorithms for a bilinear map. So $L(\phi)$ is also the nonscalar complexity of $\phi$.

**Theorem.** $L(\phi) \le R(\phi) \le 2 L(\phi)$.

*Proof.* A bilinear algorithm is a quadratic one, so $L \le R$. For the other inequality take a quadratic algorithm and split each form as $\ell_s(x, y) = a_s(x) + b_s(y)$ and $\ell'_s(x, y) = c_s(x) + d_s(y)$. Then $\ell_s \ell'_s = a_s c_s + (a_s d_s + b_s c_s) + b_s d_s$. The parts $a_s c_s$, of degree two in $x$, and $b_s d_s$, of degree two in $y$, must cancel in the sum over $s$, since $\phi$ has only terms $x_i y_j$. So $\phi = \sum_s (a_s(x) d_s(y) + b_s(y) c_s(x)) w_s$, a bilinear algorithm with $2L$ products. $\square$

**Why bilinear algorithms are the right model for matrices.** A bilinear algorithm never uses $x_i y_j = y_j x_i$ and never multiplies two entries of the same input. So it stays correct when the entries are themselves matrices, which is exactly the situation of a recursive call on blocks. This is why $R(\langle k, k, k \rangle) \le r$ gives an algorithm with $O(n^{\log_k r})$ ring operations over any ring, commutative or not, and why the [exponent ω](/matrix-multiplication-exponent/) can be defined by the rank. A quadratic algorithm that uses the commutativity of the entries, such as [Winograd's inner product algorithm](/winograd-inner-product-algorithm/), saves multiplications once but cannot be applied to blocks. Since $R \le 2L$, both measures give the same exponent.

**Properties.**

- **Field dependence.** $R(\phi)$ can drop in an extension field. Over a small field it can be larger than over $\mathbb{Q}$ because there are fewer points for evaluation and interpolation (see the examples).
- **Sums and products.** $R(\phi \oplus \psi) \le R(\phi) + R(\psi)$, with strict inequality possible (Shitov 2019, see [tensor rank](/tensor-rank/)), and $R(\phi \otimes \psi) \le R(\phi) R(\psi)$.
- **Lower bounds by dimension.** $R(\phi) \ge c$ when the $c$ outputs are linearly independent bilinear forms, and the same with the roles of the factors exchanged. For $\langle n, n, n \rangle$ this gives $n^2$.
- **Lower bounds for algebras.** For an associative algebra $A$ of dimension $d$ with $t$ maximal two-sided ideals, the rank of its multiplication is at least $2d - t$ (Alder and Strassen 1981). For the algebra of $n \times n$ matrices, $d = n^2$ and $t = 1$, so $R(\langle n, n, n \rangle) \ge 2n^2 - 1$. Bläser (1999) raised this to $\frac{5}{2} n^2 - 3n$, and Landsberg (2014) to $3n^2$ minus lower order terms over fields of characteristic zero. The best upper bounds are $n^{\omega + o(1)}$, so the gap is wide.
- **Hard to compute.** Since it is a tensor rank, deciding $R(\phi) \le r$ is NP-hard in general.
- **Approximate version.** Allowing the products to depend on a parameter $\varepsilon$ and taking a limit gives the [border rank](/border-rank/) $\underline{R}(\phi) \le R(\phi)$, which gives the same exponent ω.

## Examples

The products and identities below were checked by a script on random integer inputs, and the claim on $\mathbb{F}_2$ by exhaustive search.

1. **Complex multiplication.** $(a + bi)(c + di)$ is a bilinear map $\mathbb{R}^2 \times \mathbb{R}^2 \to \mathbb{R}^2$. Gauss's three products $k_1 = c(a + b)$, $k_2 = a(d - c)$, $k_3 = b(c + d)$ give $ac - bd = k_1 - k_3$ and $ad + bc = k_1 + k_2$. So $R \le 3$ over $\mathbb{R}$, and in fact $R = 3$ over $\mathbb{R}$ while $R = 2$ over $\mathbb{C}$.
2. **Linear polynomials.** $(a_0 + a_1 t)(b_0 + b_1 t)$ has three coefficients. Karatsuba's products $p_0 = a_0 b_0$, $p_1 = a_1 b_1$, $p_2 = (a_0 + a_1)(b_0 + b_1)$ give them as $p_0$, $p_2 - p_0 - p_1$, $p_1$. Three products are needed since the three outputs are independent. Recursion on halves gives [Karatsuba multiplication](/karatsuba-multiplication/).
3. **Quadratic polynomials, and the field.** $(a_0 + a_1 t + a_2 t^2)(b_0 + b_1 t + b_2 t^2)$ has five coefficients. Over $\mathbb{Q}$, evaluate both factors at $t = 0, 1, -1, 2$, take the product of the leading coefficients $a_2 b_2$ (the point at infinity), and interpolate: $5$ products, which is optimal. Over $\mathbb{F}_2$ there are only two finite points. A search over all $\binom{49}{5}$ sets of five rank-one $3 \times 3$ matrices over $\mathbb{F}_2$ shows that none spans the five coefficient slices, while some set of six does. So the rank is $6$ over $\mathbb{F}_2$ and $5$ over $\mathbb{Q}$.
4. **$2 \times 2$ matrices.** The triple loop is a bilinear algorithm with $8$ products. Strassen's has $7$, and $7$ is optimal: $R(\langle 2, 2, 2 \rangle) = 7$ (Hopcroft and Kerr 1971, Winograd 1971). Applied to blocks, the $7$ products give $O(n^{\log_2 7})$.
5. **A quadratic algorithm that is not bilinear.** Winograd's identity $(x_1 + y_2)(x_2 + y_1) - x_1 x_2 - y_1 y_2 = x_1 y_1 + x_2 y_2$ computes a dot product of length two with one product that mixes $x$ and $y$, plus two corrections that each depend on one input only. For $n \times n$ matrices the row corrections and column corrections are shared, which gives $n^3/2 + n^2$ multiplications for even $n$: $48$ instead of $64$ for $n = 4$, checked on random inputs. The proof of $R \le 2L$ turns the product $(x_1 + y_2)(x_2 + y_1)$ into the two bilinear products $x_1 y_1$ and $y_2 x_2$, so the saving disappears in the bilinear model. The identity needs $y_2 x_2 = x_2 y_2$, so it fails for blocks.
6. **Polynomial multiplication in general.** Two polynomials with $n$ coefficients each have a product with $2n - 1$ coefficients. Over a field with at least $2n - 2$ elements, evaluation at $2n - 2$ points and at infinity, followed by interpolation, gives $R = 2n - 1$. This is the idea of [evaluation and interpolation](/evaluation-interpolation-paradigm/) behind Toom and Cook's methods.

## Where it is used

- **Fast matrix multiplication.** Every recursive algorithm, from Strassen's and [Laderman's](/laderman-algorithm/) to the schemes found by [AlphaTensor](/alphatensor/), is a bilinear algorithm for a small $\langle n, m, p \rangle$, and its exponent is $3 \log r / \log(nmp)$.
- **The exponent ω.** ω can be defined by $R(\langle n, n, n \rangle)$, by the multiplicative complexity, or by the total number of operations, and all give the same value. See the [matrix multiplication exponent](/matrix-multiplication-exponent/).
- **Polynomial and integer multiplication.** Karatsuba's and Toom and Cook's algorithms, and the use of evaluation points in finite fields, are bilinear algorithms for [polynomial multiplication](/polynomial-multiplication/).
- **Lower bounds.** The strongest known lower bounds for explicit problems in the algebraic model are bounds on bilinear complexity and multiplicative complexity, for example the $2n^2 - 1$ and $3n^2$ bounds above. See also the [quadratic lower bound](/matrix-multiplication-quadratic-lower-bound/).
- **Hardware and cryptography.** Fewer multiplications at the cost of more additions pays off when a multiplication is much more expensive than an addition, for example for multiplications in large finite fields.

## References
