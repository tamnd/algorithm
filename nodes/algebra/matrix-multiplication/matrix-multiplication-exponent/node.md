---
tag: A1QDSH
kind: concept
slug: matrix-multiplication-exponent
name: Matrix multiplication exponent
aliases:
- omega
- ω
- matrix multiplication constant
- exponent of matrix multiplication
area: algebra/matrix-multiplication
level: advanced
summary: The infimum ω of the exponents τ such that two n×n matrices can be multiplied with O(n^τ) ring operations; 2 ≤ ω < 2.371552, and the exact value is open.
prereqs: [strassen-algorithm, matrix-multiplication-quadratic-lower-bound]
see_also: [tensor-rank, border-rank, bilinear-complexity, laser-method, coppersmith-winograd-algorithm, schonhage-asymptotic-sum-inequality, matrix-multiplication-inversion-equivalence, alphatensor]
sources:
  - paper: doi:10.1007/BF02165411
    title: Volker Strassen, Gaussian elimination is not optimal, Numerische Mathematik 13 (1969)
    locator: pp. 354 to 356 (ω ≤ log2 7)
  - paper: doi:10.1016/0020-0190(79)90113-3
    title: Dario Bini, Milvio Capovani, Francesco Romani and Grazia Lotti, O(n^2.7799) complexity for n×n approximate matrix multiplication, Information Processing Letters 8(5) (1979)
    locator: pp. 234 to 235 (border rank and ω < 2.7799)
  - paper: doi:10.1137/0210032
    title: Arnold Schönhage, Partial and total matrix multiplication, SIAM Journal on Computing 10(3) (1981)
    locator: pp. 434 to 455 (the asymptotic sum inequality and ω < 2.522)
  - paper: doi:10.1016/S0747-7171(08)80013-2
    title: Don Coppersmith and Shmuel Winograd, Matrix multiplication via arithmetic progressions, Journal of Symbolic Computation 9(3) (1990)
    locator: pp. 251 to 280 (ω < 2.375477)
  - paper: doi:10.1145/2213977.2214056
    title: Virginia Vassilevska Williams, Multiplying matrices faster than Coppersmith-Winograd, STOC 2012
    locator: pp. 887 to 898 (ω < 2.3729, from the eighth power of the CW tensor)
  - paper: doi:10.1145/2608628.2608664
    title: François Le Gall, Powers of tensors and fast matrix multiplication, ISSAC 2014
    locator: pp. 296 to 303 (ω < 2.3728639)
  - paper: doi:10.1137/1.9781611976465.32
    title: Josh Alman and Virginia Vassilevska Williams, A refined laser method and faster matrix multiplication, SODA 2021
    locator: pp. 522 to 539 (ω < 2.3728596)
  - paper: "Ran Duan, Hongxun Wu and Renfei Zhou, Faster matrix multiplication via asymmetric hashing, 64th IEEE Symposium on Foundations of Computer Science (FOCS 2023), arXiv:2210.10173"
    locator: the main theorem (ω < 2.371866)
  - paper: "Virginia Vassilevska Williams, Yinzhan Xu, Zixuan Xu and Renfei Zhou, New bounds for matrix multiplication: from alpha to omega, 35th ACM-SIAM Symposium on Discrete Algorithms (SODA 2024), arXiv:2307.07970"
    locator: the main theorem (ω < 2.371552)
  - paper: "Josh Alman, Ran Duan, Virginia Vassilevska Williams, Yinzhan Xu, Zixuan Xu and Renfei Zhou, More asymmetry yields faster matrix multiplication, 36th ACM-SIAM Symposium on Discrete Algorithms (SODA 2025), arXiv:2404.16349"
    locator: the abstract and main theorem (ω < 2.371339)
  - paper: doi:10.4086/toc.gs.2013.005
    title: Markus Bläser, Fast Matrix Multiplication, Theory of Computing Graduate Surveys 5 (2013)
    locator: the whole survey (definition of ω by rank, border rank, the asymptotic sum inequality and the laser method)
  - book: isbn:9783540605829
    title: Peter Bürgisser, Michael Clausen and M. Amin Shokrollahi, Algebraic Complexity Theory
    locator: Chapter 15, Asymptotic complexity of matrix multiplication (definition of ω, its characterization by rank and border rank, and the proofs of the bounds up to 1990)
---

The matrix multiplication exponent $\omega$ is the smallest number such that two $n \times n$ matrices can be multiplied with $n^{\omega + \varepsilon}$ ring operations for every $\varepsilon > 0$, up to a constant factor. The output has $n^2$ entries, so $\omega \ge 2$, and the [triple loop](/naive-matrix-multiplication/) gives $\omega \le 3$. [Strassen's algorithm](/strassen-algorithm/) showed $\omega \le \log_2 7 \approx 2.807$ in 1969, and a line of work on the [rank](/tensor-rank/) and [border rank](/border-rank/) of matrix multiplication tensors has lowered the bound to $\omega < 2.371552$ (2024), with a further claimed improvement to $2.371339$. Many problems of linear algebra and graph theory have the exponent $\omega$, so its value matters well beyond matrix products, but the algorithms behind all bounds below about $2.7$ are galactic: they win only for sizes far beyond any computer.

## In plain words

Multiplying two square tables of size $n$ by the school method takes about $n$ times $n$ times $n$ steps. Clever methods need fewer steps, and the number $\omega$ measures how few: the best methods take about $n$ to the power $\omega$ steps. Nobody knows its exact value.

It is at least $2$, because the answer alone has $n$ times $n$ numbers. It is at most $3$, because of the school method. The first clever method brought it below $2.81$. Fifty years of work have brought it to just below $2.372$. Many researchers think that the true value is $2$, but no proof is known. The record methods help only for tables so large that nobody will ever multiply them.

## The idea

**Definition.** Fix a field $F$. Let $MM(n)$ be the least number of ring operations ($+$, $-$, $\times$, and constants of $F$) of a straight-line program that computes the product of two $n \times n$ matrices with indeterminate entries. Then

$$\omega = \omega(F) = \inf \{ \tau \in \mathbb{R} : MM(n) = O(n^{\tau}) \}.$$

A statement such as "an algorithm runs in $O(n^{\omega})$ time" means $O(n^{\omega + \varepsilon})$ for every $\varepsilon > 0$, since the infimum need not be attained. The model is the algebraic model of [algebraic computation trees](/algebraic-computation-tree/); a straight-line program is such a tree with no branch nodes. Allowing divisions does not change $\omega$ (Strassen 1973). Schönhage (1981) showed that $\omega(F)$ depends only on the characteristic of $F$, and all known bounds hold in every characteristic.

**Characterization by rank.** Let $R(\langle n, m, p \rangle)$ be the [tensor rank](/tensor-rank/) of the tensor of the $n \times m$ by $m \times p$ product, which is its [bilinear complexity](/bilinear-complexity/). Strassen showed that

$$\omega = \inf \{ \tau : R(\langle n, n, n \rangle) = O(n^{\tau}) \},$$

so only bilinear algorithms matter, and that one bilinear algorithm for a fixed size, applied recursively, gives a bound:

$$R(\langle n, m, p \rangle) \le r \implies \omega \le \frac{3 \log r}{\log (n m p)}.$$

For $\langle 2, 2, 2 \rangle$ and $r = 7$ this gives $\log_2 7$. The same holds with the [border rank](/border-rank/) $\underline{R}$ in place of $R$ (Bini, Capovani, Romani and Lotti 1979; Bini 1980), since an approximate algorithm with error degree $h$ can be made exact at a cost factor of $O(h^2)$, which disappears in the exponent.

**Sums of products.** [Schönhage's asymptotic sum inequality](/schonhage-asymptotic-sum-inequality/) (1981) allows one algorithm to compute several independent products at once: if $\underline{R}\big(\bigoplus_{i=1}^{s} \langle n_i, m_i, p_i \rangle\big) \le r$, then $\sum_{i=1}^{s} (n_i m_i p_i)^{\omega/3} \le r$. The [laser method](/laser-method/) of Strassen (1986), and all later records, find large direct sums of matrix products hidden in a power of a small tensor with low border rank, such as the tensor of [Coppersmith and Winograd](/coppersmith-winograd-algorithm/).

**Not attained.** Coppersmith and Winograd (1982) proved that no single bilinear algorithm reaches $\omega$: from any algorithm with exponent $\tau > 2$ one can build another with a smaller exponent. So $\omega$ is a limit, and each concrete algorithm has an exponent strictly above it.

**Barriers.** Ambainis, Filmus and Le Gall (2015) showed that the laser method applied to powers of the Coppersmith and Winograd tensor, in the form used up to 2014, cannot give a bound below $2.3078$. Later work by Alman and by Alman and Vassilevska Williams extended such limits to wider classes of methods. These results limit methods, not $\omega$ itself.

## Examples

The history of the upper bound. Each row is a proved theorem in the cited paper; the values are upper bounds on $\omega$.

| year | authors | bound | method |
|---|---|---|---|
| 1969 | Strassen | $\log_2 7 < 2.8074$ | rank $7$ for $\langle 2, 2, 2 \rangle$ |
| 1978 | Pan | $2.795$ | trilinear aggregation, rank $143640$ for $\langle 70, 70, 70 \rangle$ |
| 1979 | Bini, Capovani, Romani and Lotti | $2.7799$ | border rank $5$ for a partial $2 \times 2$ product |
| 1981 | Schönhage | $2.522$ | asymptotic sum inequality |
| 1982 | Romani | $2.517$ | sums of rectangular products |
| 1982 | Coppersmith and Winograd | $2.496$ | refined sums of products |
| 1986 | Strassen | $2.479$ | laser method |
| 1990 | Coppersmith and Winograd | $2.375477$ | laser method on the CW tensor and its square |
| 2010 | Stothers | $2.3737$ | fourth power of the CW tensor |
| 2012 | Vassilevska Williams | $2.372873$ | eighth power, automated analysis |
| 2014 | Le Gall | $2.3728639$ | the thirty-second power, by convex optimization |
| 2021 | Alman and Vassilevska Williams | $2.3728596$ | refined laser method |
| 2023 | Duan, Wu and Zhou | $2.371866$ | asymmetric hashing |
| 2024 | Vassilevska Williams, Xu, Xu and Zhou | $2.371552$ | asymmetric hashing, with new bounds on $\alpha$ |
| 2025 | Alman, Duan, Vassilevska Williams, Xu, Xu and Zhou | $2.371339$ | more asymmetry in the hashing (SODA 2025, arXiv:2404.16349) |

Stothers's bound appeared in his 2010 PhD thesis (University of Edinburgh) and in a 2013 paper with Davie. The rank $143640$ in Pan's row gives $\log 143640 / \log 70 \approx 2.7951$.

Other quantities defined in the same way:

- **Rectangular products.** $\omega(a, b, c)$ is the exponent of the $n^a \times n^b$ by $n^b \times n^c$ product, and $\omega = \omega(1, 1, 1)$. The dual exponent $\alpha = \sup \{ a : \omega(1, a, 1) = 2 \}$ measures how thin the middle can be while the cost stays $n^{2 + o(1)}$. Coppersmith (1982) showed $\alpha > 0.172$, and Le Gall and Urrutia (2018) $\alpha > 0.31389$; the 2024 paper above improved it further. $\omega = 2$ would imply $\alpha = 1$.
- **Problems with exponent $\omega$.** Over a field, [inversion](/matrix-multiplication-inversion-equivalence/), the determinant, LUP decomposition and the solution of linear systems cost $O(n^{\omega})$; the [rank](/rank-computation/) also costs $O(n^{\omega})$, and the [characteristic polynomial](/characteristic-polynomial-computation/) $O(n^{\omega} \log n)$ (Keller-Gehrig 1985). [Boolean matrix multiplication](/boolean-matrix-multiplication/), transitive closure and triangle detection run in $O(n^{\omega})$ time.

## Where it is used

- **Complexity statements.** Running times of the form $O(n^{\omega})$ appear throughout exact linear algebra, graph algorithms (perfect matchings, triangle detection, unweighted shortest paths) and parsing. Each new bound on $\omega$ improves them all at once.
- **Fine-grained complexity.** Conditional lower bounds compare problems with BMM and its exponent; see [Boolean matrix multiplication](/boolean-matrix-multiplication/) and [min-plus matrix multiplication](/min-plus-matrix-multiplication/), which has no known truly subcubic algorithm.
- **Algebraic complexity and geometry.** The search for upper and lower bounds on the rank and border rank of $\langle n, n, n \rangle$ connects $\omega$ to algebraic geometry and representation theory; see [tensor rank](/tensor-rank/). The best lower bounds on the rank are only about $3n^2$, see the [quadratic lower bound](/matrix-multiplication-quadratic-lower-bound/).
- **Practice.** Libraries use the classical algorithm with blocking, and sometimes [Strassen's algorithm](/strassen-algorithm/) for large sizes. The methods with exponents below about $2.7$ are galactic, and computer searches such as [AlphaTensor](/alphatensor/) look instead for small exact algorithms that help at practical sizes.

## References
