---
tag: F2B3XD
kind: concept
slug: border-rank
name: Border rank
aliases:
- approximate tensor rank
- approximate bilinear complexity
- degeneration rank
area: algebra/matrix-multiplication
level: research
summary: The least r such that a tensor is a limit of tensors of rank r, or equals the lowest term of a rank-r sum over polynomials in ε; it can be below the rank but gives the same exponent ω.
prereqs: [tensor-rank, bilinear-complexity, matrix-multiplication-tensor]
see_also: [schonhage-asymptotic-sum-inequality, laser-method, coppersmith-winograd-algorithm, matrix-multiplication-exponent, strassen-algorithm, lagrange-interpolation, matrix-multiplication-quadratic-lower-bound]
sources:
  - paper: doi:10.1016/0020-0190(79)90113-3
    title: Dario Bini, Milvio Capovani, Francesco Romani and Grazia Lotti, O(n^2.7799) complexity for n×n approximate matrix multiplication, Information Processing Letters 8(5) (1979)
    locator: pp. 234 to 235 (an approximate algorithm with 5 products for a partial 2×2 product, and ω < 2.7799)
  - paper: "Dario Bini, Relations between exact and approximate bilinear algorithms. Applications, Calcolo 17(1) (1980)"
    locator: pp. 87 to 97 (an approximate algorithm of error degree h gives an exact one with a factor polynomial in h, so border rank gives the same exponent)
  - paper: doi:10.1137/0210032
    title: Arnold Schönhage, Partial and total matrix multiplication, SIAM Journal on Computing 10(3) (1981)
    locator: pp. 434 to 455 (the border rank k^2 + 1 of a direct sum of two matrix products, which has a larger rank)
  - book: isbn:9783540605829
    title: Peter Bürgisser, Michael Clausen and M. Amin Shokrollahi, Algebraic Complexity Theory, Springer, Grundlehren der mathematischen Wissenschaften 315 (1997)
    locator: Chapter 15, Sections on degeneration and border rank (approximate computations, the error degree, and the proof that border rank gives the same ω)
  - book: isbn:9780821869079
    title: J. M. Landsberg, Tensors, Geometry and Applications, American Mathematical Society, Graduate Studies in Mathematics 128 (2012)
    locator: Chapters 3 and 5 (border rank, secant varieties, and equations for them such as flattenings and Strassen's equations)
  - paper: "J. M. Landsberg, The border rank of the multiplication of 2×2 matrices is seven, Journal of the American Mathematical Society 19(2) (2006)"
    locator: the main theorem (border rank of ⟨2,2,2⟩ equals 7)
  - paper: "J. M. Landsberg and Giorgio Ottaviani, New lower bounds for the border rank of matrix multiplication, Theory of Computing 11 (2015)"
    locator: the main theorem (border rank of ⟨n,n,n⟩ at least 2n^2 minus n, by Koszul flattenings)
  - paper: doi:10.4086/toc.gs.2013.005
    title: Markus Bläser, Fast Matrix Multiplication, Theory of Computing Graduate Surveys 5 (2013)
    locator: Section 5 (border rank, approximate algorithms and the result of Bini et al.)
---

The border rank $\underline{R}(T)$ of a tensor $T$ is the least $r$ such that $T$ is a limit of tensors of [rank](/tensor-rank/) at most $r$. In algorithm terms it is the least number of products of an approximate bilinear algorithm: one whose products depend on a parameter $\varepsilon$ and whose outputs are exact only in the limit $\varepsilon \to 0$. Border rank can be strictly smaller than rank, and for the [matrix multiplication tensor](/matrix-multiplication-tensor/) it gives the same [exponent ω](/matrix-multiplication-exponent/), because an approximate algorithm can be turned into an exact one at a cost factor that is polynomial in the error degree and so disappears under recursion. Bini, Capovani, Romani and Lotti used it in 1979 to prove $\omega < 2.7799$, and all later bounds on ω go through border rank, through the [asymptotic sum inequality](/schonhage-asymptotic-sum-inequality/) and the [laser method](/laser-method/).

## In plain words

Some products are hard to compute exactly with few multiplications but easy to compute almost exactly. Take a small number $\varepsilon$. Mix $\varepsilon$ into the sums that you multiply, so that the wanted answer appears next to small error terms that carry extra factors of $\varepsilon$. As $\varepsilon$ goes to zero, the error goes away.

The border rank is the least number of multiplications such an almost exact method needs. It can be smaller than the number an exact method needs. For very large matrices this is not a trick that costs accuracy: the almost exact method can be turned into an exact one, with a cost that grows only by a factor that does not change the exponent.

## The idea

**Two definitions.** Let $F$ be a field and $T \in U \otimes V \otimes W$.

- *Topological.* Over $\mathbb{R}$ or $\mathbb{C}$, $\underline{R}(T)$ is the least $r$ such that $T = \lim_{t \to \infty} T_t$ for tensors $T_t$ of rank at most $r$. Over $\mathbb{C}$ the closure in the usual topology is the same as the Zariski closure, so the set of tensors of border rank at most $r$ is an algebraic variety, the $r$-th secant variety of the Segre variety.
- *Algebraic.* Let $\varepsilon$ be an indeterminate. $T$ has border rank at most $r$ if there are vectors $u_s(\varepsilon)$, $v_s(\varepsilon)$ and $w_s(\varepsilon)$ with entries in $F[\varepsilon]$ and an integer $h \ge 0$ with
$$\sum_{s=1}^{r} u_s(\varepsilon) \otimes v_s(\varepsilon) \otimes w_s(\varepsilon) = \varepsilon^{h} T + \varepsilon^{h+1} T'(\varepsilon)$$
for some tensor $T'(\varepsilon)$ with polynomial entries. The least such $h$ is the error degree. This definition works over every field. Over $\mathbb{C}$ the two definitions agree.

Dividing by $\varepsilon^h$ shows how the second definition gives the first: $\varepsilon^{-h} \sum_s u_s \otimes v_s \otimes w_s$ has rank at most $r$ for each $\varepsilon \ne 0$ and tends to $T$.

**Properties.**

- $\underline{R}(T) \le R(T)$, with $h = 0$.
- **Flattening bounds still hold.** A matrix of rank at most $r$ stays of rank at most $r$ in the limit, so each flattening rank is a lower bound for $\underline{R}(T)$. For $\langle n, n, n \rangle$ this gives $\underline{R} \ge n^2$.
- **Sums and products.** $\underline{R}(T \oplus T') \le \underline{R}(T) + \underline{R}(T')$ and $\underline{R}(T \otimes T') \le \underline{R}(T) \, \underline{R}(T')$; error degrees add under the Kronecker product. Unlike rank, border rank can be strictly subadditive on direct sums of matrix products (Schönhage's example below), and this is the key to the [asymptotic sum inequality](/schonhage-asymptotic-sum-inequality/).
- **Equations.** The tensors of border rank at most $r$ are the common zeros of a set of polynomials in the entries. Flattenings, Strassen's equations and Koszul flattenings are known families of such polynomials, and the lower bounds below come from them.

**From approximate to exact.** Suppose $\sum_{s=1}^{r} u_s(\varepsilon) \otimes v_s(\varepsilon) \otimes w_s(\varepsilon) = \varepsilon^{h} T + O(\varepsilon^{h+1})$.

1. *Coefficient extraction.* Write $u_s = \sum_a \varepsilon^a u_s^{(a)}$, and the same for $v_s$ and $w_s$. The coefficient of $\varepsilon^h$ on the left is $\sum_s \sum_{a + b + c = h} u_s^{(a)} \otimes v_s^{(b)} \otimes w_s^{(c)}$, a sum of $r \binom{h+2}{2}$ rank-one terms, and it equals $T$. So $R(T) \le \binom{h+2}{2} \underline{R}(T)$ over every field.
2. *Interpolation.* Drop all terms of degree above $h$ from $u_s$, $v_s$ and $w_s$; this does not change the coefficients of $\varepsilon^0, \ldots, \varepsilon^h$. Then $f(\varepsilon) = \varepsilon^{-h} \sum_s u_s \otimes v_s \otimes w_s$ is a polynomial in $\varepsilon$ of degree at most $2h$ with $f(0) = T$. Choose $2h + 1$ distinct nonzero $\varepsilon_t \in F$. By [Lagrange interpolation](/lagrange-interpolation/), $T = f(0) = \sum_t \lambda_t f(\varepsilon_t)$ for constants $\lambda_t$, and each $f(\varepsilon_t)$ has rank at most $r$. So $R(T) \le (2h + 1) \underline{R}(T)$ when $F$ has more than $2h + 1$ elements.
3. *Same exponent.* If $\underline{R}(\langle k, k, k \rangle) \le r$ with error degree $h$, then the $s$-th Kronecker power has $\underline{R}(\langle k^s, k^s, k^s \rangle) \le r^s$ with error degree $sh$, so $R(\langle k^s, k^s, k^s \rangle) \le (2sh + 1) r^s$. The factor $2sh + 1$ grows only like $\log n$ for $n = k^s$, so $\omega \le \log_k r$. In general $\underline{R}(\langle n, m, p \rangle) \le r$ implies $\omega \le 3 \log r / \log(nmp)$, exactly as for the rank (Bini 1980).

## Examples

The identities below were checked by a script, which expands each sum as a polynomial in $\varepsilon$ and compares the coefficients with the target tensor.

1. **Multiplication of truncated polynomials.** The product in $F[t]/(t^2)$, $(x_0 + x_1 t)(y_0 + y_1 t) = x_0 y_0 + (x_0 y_1 + x_1 y_0) t$, has the tensor $W = e_0 \otimes e_0 \otimes e_0^* + (e_0 \otimes e_1 + e_1 \otimes e_0) \otimes e_1^*$, which has rank $3$. But with the two products $p_1 = (x_0 + \varepsilon x_1)(y_0 + \varepsilon y_1)$ and $p_2 = x_0 y_0$,
$$\frac{p_1 - p_2}{\varepsilon} = x_0 y_1 + x_1 y_0 + \varepsilon x_1 y_1,$$
so both outputs are within $O(\varepsilon)$ of linear combinations of two products: $\underline{R}(W) = 2$, with error degree $1$. With $x = (3, 5)$ and $y = (2, 7)$, the exact coefficient is $31$; the approximate algorithm gives $34.5$ at $\varepsilon = 1/10$ and $31.035$ at $\varepsilon = 1/1000$, an error of exactly $\varepsilon x_1 y_1 = 35 \varepsilon$. Coefficient extraction gives $\binom{3}{2} \cdot 2 = 6$ terms, and interpolation $3 \cdot 2 = 6$; the true rank is $3$.
2. **Bini's partial product.** Take $2 \times 2$ matrices with one entry of $A$ fixed to zero, $a_{22} = 0$. The product has $6$ terms $a_{ij} b_{jk}$, and the obvious algorithm uses $6$ products. Bini, Capovani, Romani and Lotti gave an approximate algorithm with $5$ products and error degree $1$. Two copies of this partial product, one with $a_{22} = 0$ and one with $a_{12} = 0$ placed so that their rows do not overlap, add up to the $3 \times 2$ by $2 \times 2$ product. So $\underline{R}(\langle 3, 2, 2 \rangle) \le 10$, and the cyclic symmetry gives the same for $\langle 2, 2, 3 \rangle$ and $\langle 2, 3, 2 \rangle$. Their Kronecker product is $\langle 12, 12, 12 \rangle$ with border rank at most $1000$, which gives $\omega \le 3 \log 10 / \log 12 \approx 2.7799$. An exact algorithm for $\langle 3, 2, 2 \rangle$ with $11$ products is easy ($7$ for a $2 \times 2$ block and $4$ for the last row), and Alekseyev (1985) proved that $11$ is the rank. So border rank saves one product here, and this one product lowers the bound from $\log_2 7 \approx 2.8074$.
3. **Schönhage's direct sum.** For $k \ge 2$, let $x_1, \ldots, x_k$, $y_1, \ldots, y_k$ and $z_{ij}$ be the variables of the outer product $\langle k, 1, k \rangle$, and let $u_{ij}$, $v_{ij}$ (for $i, j \le k$) and $w$ be variables with $\sum_i u_{ij} = 0$ for each $j$ and $\sum_j v_{ij} = 0$ for each $i$, so that $\sum_{i,j} u_{ij} v_{ij} w$ is a copy of $\langle 1, (k-1)^2, 1 \rangle$, a dot product of length $(k-1)^2$. Then
$$\sum_{i, j = 1}^{k} (x_i + \varepsilon u_{ij})(y_j + \varepsilon v_{ij})(w + \varepsilon^2 z_{ij}) - \Big(\sum_i x_i\Big)\Big(\sum_j y_j\Big) w = \varepsilon^2 \Big( \sum_{i,j} x_i y_j z_{ij} + \sum_{i,j} u_{ij} v_{ij} w \Big) + O(\varepsilon^3).$$
So $\underline{R}(\langle k, 1, k \rangle \oplus \langle 1, (k-1)^2, 1 \rangle) \le k^2 + 1$ with error degree $2$, while the two parts alone need $k^2$ and $(k-1)^2$ products. The check expanded the left side for $k = 2, 3, 4$ with random integer values and the constraints on $u$ and $v$.
4. **Square matrices.** $\underline{R}(\langle 2, 2, 2 \rangle) = 7$ (Landsberg 2006), so border rank gives nothing for the square $2 \times 2$ product. For $\langle 3, 3, 3 \rangle$ approximate algorithms with $20$ products are known (Smirnov 2013), against $23$ for exact ones, and the lower bound is $17$ (Conner, Harper and Landsberg); the exact value is open.

## Where it is used

- **Bounds on ω.** Every bound on ω after 1979 uses border rank, from Bini et al.'s $2.7799$ to the current $\omega < 2.371552$. The [Coppersmith-Winograd tensor](/coppersmith-winograd-algorithm/) has border rank $q + 2$, the least possible for its dimensions, but a larger rank, and the [laser method](/laser-method/) works with its powers.
- **The asymptotic sum inequality.** [Schönhage's inequality](/schonhage-asymptotic-sum-inequality/) is stated for border rank, and Schönhage's direct sum above is its first application.
- **Lower bounds.** Lower bounds on $\underline{R}(\langle n, n, n \rangle)$ are lower bounds on $R$ too. The best known are about $2n^2$: Landsberg and Ottaviani (2015) proved $\underline{R}(\langle n, n, n \rangle) \ge 2n^2 - n$ by Koszul flattenings. The [quadratic lower bound](/matrix-multiplication-quadratic-lower-bound/) page lists the simpler bounds.
- **Numerical practice.** Approximate algorithms with a fixed small $\varepsilon$ have been tried in floating point. The division by $\varepsilon^h$ multiplies the rounding errors, so the accuracy is poor; in practice they are not used, and the exact versions from interpolation are galactic.
- **Geometry.** Border rank is the subject of the study of secant varieties in algebraic geometry, and questions about ω become questions about which matrix multiplication tensors lie on which secant varieties.

## References
