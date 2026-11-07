---
tag: YDJRCM
kind: problem
slug: polynomial-multiplication
name: Polynomial multiplication
aliases:
- polynomial product
- convolution of coefficients
area: algebra/polynomial-arithmetic
level: intro
summary: Compute the product of two polynomials; equivalent in cost to discrete convolution.
model: blum-shub-smale-machine
complexity:
  vars: {n: the number of coefficients of each factor (so the degrees are less than n)}
  time: {worst: O(n log n log log n)}
prereqs: [polynomial-ring, polynomial-degree]
see_also: [convolution, karatsuba-multiplication, toom-cook-multiplication, fft-polynomial-multiplication, kronecker-substitution, sparse-polynomial-multiplication, integer-multiplication, polynomial-division]
sources:
  - book: isbn:9781107039032
    title: Joachim von zur Gathen and Jürgen Gerhard, Modern Computer Algebra, third edition, Cambridge University Press, 2013
    locator: Section 2.3, Multiplication (p. 34); Chapter 8, Fast multiplication (Sections 8.1 to 8.4, pp. 221 to 247, with the definition of a multiplication time in Section 8.3)
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, Seminumerical Algorithms, third edition
    locator: Section 4.3.3, How Fast Can We Multiply?, and Section 4.6, Polynomial Arithmetic (introduction)
  - book: isbn:9780521194693
    title: Richard P. Brent and Paul Zimmermann, Modern Computer Arithmetic, Cambridge University Press, 2010
    locator: Section 1.3, Multiplication (1.3.1 to 1.3.6), and Section 2.1.5, Link with polynomials
  - book: isbn:9783540605829
    title: Peter Bürgisser, Michael Clausen and M. Amin Shokrollahi, Algebraic Complexity Theory, Springer, 1997
    locator: Chapter 2, Efficient Polynomial Arithmetic
  - paper: doi:10.1007/BF01178683
    title: David G. Cantor and Erich Kaltofen, On fast multiplication of polynomials over arbitrary algebras, Acta Informatica 28(7), 1991
    locator: pp. 693 to 701 (O(n log n log log n) operations over any ring)
  - paper: doi:10.1145/3505584
    title: David Harvey and Joris van der Hoeven, Polynomial multiplication over finite fields in time O(n log n), Journal of the ACM 69(2), 2022
    locator: Article 12 (the bit complexity bound over a finite field, under a hypothesis on primes in arithmetic progressions)
  - paper: "arXiv:cs/0301016"
    title: Peter Bürgisser and Martin Lotz, Lower bounds on the bounded coefficient complexity of bilinear maps, Journal of the ACM 51(3), 2004
    locator: pp. 464 to 482 (the Omega(n log n) bounds for polynomial multiplication and division in bounded coefficient circuits)
---

Polynomial multiplication is the problem of computing the coefficients of the product $fg$ of two polynomials in $R[x]$, where $R$ is a commutative ring. The coefficient sequence of $fg$ is the acyclic [convolution](/convolution/) of the two input sequences, so the problem is the same as discrete convolution. The school method uses $\Theta(n^2)$ operations in $R$ for two factors with $n$ coefficients, [Karatsuba's method](/karatsuba-multiplication/) $O(n^{\log_2 3})$, and [FFT methods](/fft-polynomial-multiplication/) $O(n \log n)$ when $R$ has suitable roots of unity and $O(n \log n \log \log n)$ over any ring. The cost $M(n)$ of this problem is the unit in which the costs of division, gcd, evaluation and interpolation are stated.

## In plain words

A polynomial is a list of numbers, one for each power of the unknown. To multiply two of them, multiply each number of the first list by each number of the second, and add each product into the place given by the sum of the two positions. With two lists of a thousand numbers, that is a million small products.

The same sum appears in signal processing, where it is called a convolution, and in the multiplication of big integers, where the digits play the role of the numbers in the lists. Faster methods exist. One splits each list in half and needs only three half-size products instead of four. The fastest methods change each list into its values at many special points, multiply the values one by one, and change the result back.

## Definition

**Input.** A commutative ring $R$ with $1$, and two polynomials

$$f = \sum_{i=0}^{m-1} a_i x^i, \qquad g = \sum_{j=0}^{n-1} b_j x^j \qquad (a_i, b_j \in R),$$

given by their coefficient vectors $(a_0, \ldots, a_{m-1})$ and $(b_0, \ldots, b_{n-1})$. The vectors may have zero top coefficients.

**Output.** The coefficient vector $(c_0, \ldots, c_{m+n-2})$ of $h = fg$, where

$$c_k = \sum_{\substack{i + j = k \\ 0 \le i < m,\ 0 \le j < n}} a_i b_j \qquad (0 \le k \le m + n - 2).$$

The output is unique. If $R$ is an integral domain and $a_{m-1} b_{n-1} \ne 0$, then $\deg h = m + n - 2$ (see [degree of a polynomial](/polynomial-degree/)). Otherwise the top of the output vector can be zero.

**Cost.** The cost counts operations in $R$, each at unit cost: the arithmetic model of [polynomial ring](/polynomial-ring/). $M(n)$ is the worst-case number of operations of a chosen algorithm for $m = n$. Following von zur Gathen and Gerhard (Section 8.3), a *multiplication time* is a function with $M(n)/n$ nondecreasing and $M(mn) \le m^2 M(n)$. These two conditions give $M(n) + M(m) \le M(n + m)$ and $M(cn) \le c^2 M(n)$, which the cost analyses of Newton iteration and of divide and conquer use.

## Variants

- **Unbalanced product.** $m \ge n$. Cut $f$ into $\lceil m/n \rceil$ blocks of $n$ coefficients, multiply each block by $g$, and add the shifted results. The cost is at most $\lceil m/n \rceil M(n) + O(m)$.
- **Squaring.** $f = g$. When $2$ is a unit of $R$, a product reduces to two squares by $fg = \tfrac{1}{4}\left((f + g)^2 - (f - g)^2\right)$, so squaring and multiplication have the same cost up to a constant factor. The school method needs $n(n+1)/2$ coefficient products for a square instead of $n^2$.
- **Short product.** Only $fg \bmod x^n$, the low $n$ coefficients. It is the step of [Newton iteration](/newton-iteration/) for [power series inversion](/power-series-inversion/).
- **High product and middle product.** Only the top half, or only the coefficients $c_{n-1}, \ldots, c_{2n-2}$ of an $n$ by $2n - 1$ product. By the transposition principle, the middle product costs $M(n) + O(n)$.
- **Cyclic and negacyclic convolution.** $fg \bmod (x^n - 1)$ or $fg \bmod (x^n + 1)$. These are the products that the [discrete Fourier transform](/discrete-fourier-transform/) and the [Schönhage-Strassen method](/schonhage-strassen-multiplication/) compute directly.
- **Integer coefficients, bit cost.** Over $\mathbb{Z}$, the cost in bit operations depends on the size of the coefficients. [Kronecker substitution](/kronecker-substitution/) packs each polynomial into one integer and uses one [integer multiplication](/integer-multiplication/).
- **Sparse inputs.** Only the $t$ nonzero terms are given. The output can have up to $t^2$ terms, and the cost is measured in $t$ and in the output size; see [sparse polynomial multiplication](/sparse-polynomial-multiplication/).
- **Several variables.** $R[x_1, \ldots, x_k]$. Kronecker substitution maps it to one variable when degree bounds are known.

## Examples

- **School method.** $(1 + 2x + 3x^2)(4 + 5x)$: $c_0 = 1 \cdot 4 = 4$, $c_1 = 1 \cdot 5 + 2 \cdot 4 = 13$, $c_2 = 2 \cdot 5 + 3 \cdot 4 = 22$, $c_3 = 3 \cdot 5 = 15$. So the product is $4 + 13x + 22x^2 + 15x^3$.
- **Karatsuba's step.** For $(a_0 + a_1 x)(b_0 + b_1 x)$, compute $p_0 = a_0 b_0$, $p_2 = a_1 b_1$ and $p_1 = (a_0 + a_1)(b_0 + b_1)$. Then the product is $p_0 + (p_1 - p_0 - p_2)x + p_2 x^2$. For $(1 + 2x)(3 + 4x)$: $p_0 = 3$, $p_2 = 8$, $p_1 = 3 \cdot 7 = 21$, so the product is $3 + 10x + 8x^2$, with three multiplications instead of four.
- **Kronecker substitution.** For $f = 1 + 2x + 3x^2$ and $g = 4 + 5x + 6x^2$, each coefficient of $fg$ lies in $[0, 100)$, so put $x = 100$: $f(100) = 30201$ and $g(100) = 60504$. Their product is $1827281304$. Its base-100 digits from the low end are $4, 13, 28, 27, 18$, and $fg = 4 + 13x + 28x^2 + 27x^3 + 18x^4$.
- **Characteristic 2.** Over $\mathbb{F}_2$, $(1 + x)^2 = 1 + x^2$, because the middle coefficient $2$ is $0$. A test of an implementation over $\mathbb{Z}/p\mathbb{Z}$ must reduce after each sum.

## Known algorithms

| algorithm | operations in $R$ for $m = n$ | condition on $R$ |
|---|---|---|
| school method (the definition) | $n^2$ multiplications and $(n-1)^2$ additions | none |
| [Karatsuba](/karatsuba-multiplication/) | $O(n^{\log_2 3}) = O(n^{1.585})$ | none |
| [Toom-Cook](/toom-cook-multiplication/), $k$-way | $O(n^{\log_k (2k-1)})$ | enough points: $2k - 2$ elements whose differences are units |
| [FFT multiplication](/fft-polynomial-multiplication/) | $O(n \log n)$ | a primitive $2^k$-th root of unity with $2^k \ge 2n - 1$, and $2$ a unit (for example $\mathbb{C}$, or $\mathbb{F}_p$ with $2^k \mid p - 1$ through the [NTT](/number-theoretic-transform/)) |
| Schönhage-Strassen and Cantor-Kaltofen | $O(n \log n \log \log n)$ | none |
| [sparse multiplication](/sparse-polynomial-multiplication/) | $O(t^2 \log t)$ for $t$ terms each | none, sparse inputs |

The school method uses exactly $n^2$ products $a_i b_j$ and $n^2 - (2n - 1) = (n-1)^2$ additions, since $2n - 1$ of the products start an output coefficient. The bounds in the table are proved. Which method is fastest at a given size is a matter of measurement: in libraries the school method wins for small degrees, Karatsuba and Toom-Cook for medium degrees and FFT methods for large degrees, and the crossover points depend on the ring, the coefficient size, the machine and the implementation.

## Bounds

- **Upper bound for every ring.** $O(n \log n \log \log n)$ operations in $R$, by Cantor and Kaltofen (1991), who extended the method of Schönhage and Strassen to arbitrary algebras. If $R$ supports the FFT, $O(n \log n)$.
- **Bit complexity.** Over $\mathbb{F}_q$, Harvey and van der Hoeven (2022) multiply polynomials of degree less than $n$ in $O(n \log q \log(n \log q))$ bit operations, under a standard hypothesis on the least prime in an arithmetic progression.
- **Trivial lower bound.** $\Omega(n)$: each of the $2n - 1$ outputs needs at least one operation, and over an infinite field no algorithm can skip an input coefficient.
- **Bilinear lower bound.** Over an infinite field $F$, the bilinear complexity (the number of products of a linear form in the $a_i$ with a linear form in the $b_j$) is exactly $2n - 1$. *Upper bound:* evaluate $f$ and $g$ at $2n - 1$ distinct points, multiply the $2n - 1$ pairs of values, and interpolate; evaluation and interpolation are linear in the inputs. *Lower bound:* each $c_k$ is a linear combination of the $r$ products, and the $2n - 1$ bilinear forms $c_0, \ldots, c_{2n-2}$ are linearly independent (each one contains the term $a_i b_j$ with $i + j = k$ and no other $c_l$ does), so $r \ge 2n - 1$. The additions and the scalar multiplications of this method are not free in the arithmetic model, so this does not give an $O(n)$ algorithm.
- **No superlinear lower bound** for general arithmetic circuits is known. In the restricted model of bounded coefficient circuits over $\mathbb{C}$, Bürgisser and Lotz (2004) proved an $\Omega(n \log n)$ lower bound for multiplication and for division with remainder, which matches the FFT upper bound.

## Reductions

- **Convolution.** Polynomial multiplication is acyclic convolution of the coefficient sequences, so each algorithm for one is an algorithm for the other with the same cost. A cyclic convolution of length $N$ is a product modulo $x^N - 1$, and a product of size $n$ is a cyclic convolution of any length $N \ge 2n - 1$ after padding with zeros.
- **To and from integer multiplication.** Over $\mathbb{Z}$, [Kronecker substitution](/kronecker-substitution/) reduces polynomial multiplication to one product of integers of $O(n(b + \log n))$ bits for coefficients of $b$ bits. In the other direction, [integer multiplication](/integer-multiplication/) is polynomial multiplication of the digit sequences followed by carries.
- **From division.** [Polynomial division](/polynomial-division/) of a polynomial of degree $2n$ by one of degree $n$ costs $O(M(n))$ through [power series inversion](/power-series-inversion/) and Newton iteration, so division is no harder than multiplication, up to a constant factor.
- **From other problems.** The [gcd](/polynomial-gcd/) costs $O(M(n) \log n)$ by the fast Euclidean algorithm. [Multipoint evaluation](/multipoint-evaluation/) and [interpolation](/fast-interpolation/) at $n$ points cost $O(M(n) \log n)$ with a [subproduct tree](/subproduct-tree/).

## Applications

- Every fast algorithm of this area: division, gcd, evaluation, interpolation, factorization, and [composition](/polynomial-composition/).
- [Integer multiplication](/integer-multiplication/) and arbitrary precision arithmetic.
- Digital filters and correlation of signals, as convolution.
- Generating functions in combinatorics: the coefficients of a product count pairs of objects whose sizes add up.
- Reed-Solomon and BCH codes, and lattice-based cryptography, which multiplies in $\mathbb{F}_q[x]/(x^n + 1)$.

## References
