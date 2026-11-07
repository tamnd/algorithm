---
tag: 29AZTH
kind: problem
slug: integer-multiplication
name: Integer multiplication
aliases:
- multiplying big integers
area: algebra/integer-arithmetic
level: intro
summary: Multiply two n-digit integers, the central problem of arbitrary-precision arithmetic.
model: multitape-turing-machine
complexity:
  vars: {N: the length of each operand in binary digits}
  time: {worst: O(N log N)}
prereqs: [positional-number-system, integer-addition, asymptotic-notation]
see_also: [schoolbook-multiplication, karatsuba-multiplication, toom-cook-multiplication, schonhage-strassen-multiplication, furer-multiplication, harvey-van-der-hoeven-multiplication, polynomial-multiplication, integer-division]
sources:
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, third edition
    locator: Section 4.3.1, Algorithm M (classical multiplication), and Section 4.3.3, How fast can we multiply? (Karatsuba, Toom-Cook, the Schönhage-Strassen method, and the history)
  - book: isbn:9780521194693
    title: Richard P. Brent and Paul Zimmermann, Modern Computer Arithmetic, Cambridge University Press, 2010
    locator: Section 1.3, Multiplication (1.3.1 to 1.3.7, with the Karatsuba threshold in 1.3.2 and squaring in 1.3.6), and Section 2.3.3, The Schönhage-Strassen algorithm
  - paper: doi:10.1007/BF02242355
    title: Arnold Schönhage and Volker Strassen, Schnelle Multiplikation großer Zahlen, Computing 7, 1971
    locator: pp. 281 to 292 (the O(n log n log log n) bound and the conjecture that n log n is the right order)
  - paper: doi:10.1137/070711761
    title: Martin Fürer, Faster integer multiplication, SIAM Journal on Computing 39(3), 2009 (conference version STOC 2007, pp. 57 to 66)
    locator: pp. 979 to 1005
  - paper: doi:10.4007/annals.2021.193.2.4
    title: David Harvey and Joris van der Hoeven, Integer multiplication in time O(n log n), Annals of Mathematics 193(2), 2021
    locator: pp. 563 to 617 (the main theorem, on the multitape Turing machine; Section 1 for the history of the bounds after Schönhage and Strassen)
  - paper: doi:10.1016/j.jco.2016.03.001
    title: David Harvey, Joris van der Hoeven and Grégoire Lecerf, Even faster integer multiplication, Journal of Complexity 36, 2016
    locator: pp. 1 to 30 (the bound with the factor 8 to the power log* N)
  - paper: doi:10.4230/LIPIcs.ICALP.2019.10
    title: Peyman Afshani, Casper Benjamin Freksen, Lior Kamma and Kasper Green Larsen, Lower bounds for multiplication via network coding, ICALP 2019, LIPIcs 132
    locator: article 10, the main theorem
  - url: https://dspace.mit.edu/handle/1721.1/148869
    title: Michael S. Paterson, Michael J. Fischer and Albert R. Meyer, An improved overlap argument for on-line multiplication, MIT Project MAC Technical Memorandum 40, 1974 (also SIAM-AMS Proceedings 7, 1974)
    locator: the main theorem (an Omega(N log N) bound for on-line multiplication on multitape Turing machines)
---

Integer multiplication is the problem of computing the product of two integers given by their digits. It is the central problem of [arbitrary-precision arithmetic](/arbitrary-precision-arithmetic/), because division, square roots, radix conversion and the greatest common divisor all cost $O(M(n))$ or $O(M(n) \log n)$, where $M(n)$ is the cost of a multiplication of $n$-limb numbers. The school method takes $\Theta(n^2)$ limb operations. A line of results from [Karatsuba](/karatsuba-multiplication/) (1962) to [Harvey and van der Hoeven](/harvey-van-der-hoeven-multiplication/) (2019, published 2021) brought the bit complexity down to $O(N \log N)$ for $N$-bit operands, and no matching lower bound is known.

## In plain words

At school you multiply two numbers by writing one row for each digit of the second number, each row shifted one place to the left, and then you add all the rows. For two numbers with a hundred digits each, that is ten thousand small products. If the numbers are twice as long, the work is four times as large.

For a long time people thought that this was the best possible method. In the early 1960s a student, Karatsuba, found a way to replace four half-size products with three, and the work then grows much more slowly. Better and better methods followed, many of them based on the fast Fourier transform.

Today the best method is close to the size of the input times a small factor. It is still an open question whether multiplication can be as fast as addition.

## Definition

Fix the base $\beta = 2^w$ of the area, with $w \ge 1$.

**Input.** Two nonnegative integers $A = \sum_{i=0}^{m-1} a_i \beta^i$ and $B = \sum_{j=0}^{n-1} b_j \beta^j$, given by $m$ and $n$ limbs with $0 \le a_i, b_j < \beta$.

**Output.** The limbs $c_0, \ldots, c_{m+n-1}$ with $0 \le c_k < \beta$ and

$$\sum_{k=0}^{m+n-1} c_k \beta^k = A \cdot B .$$

The output exists and is unique, because $0 \le AB \le (\beta^m - 1)(\beta^n - 1) < \beta^{m+n}$. If both inputs are normalized ($a_{m-1} \ne 0$ and $b_{n-1} \ne 0$), then $AB \ge \beta^{m+n-2}$, so the product has $m + n - 1$ or $m + n$ significant limbs. Signed inputs are handled by the sign rule $\operatorname{sign}(AB) = \operatorname{sign}(A)\operatorname{sign}(B)$ and a product of magnitudes.

**Cost measures.** $M(n)$ is the cost of the balanced case $m = n$, in limb operations on the [word RAM](/word-ram/). For the fast methods, the cost is given in bit operations on a [multitape Turing machine](/multitape-turing-machine/) or as the size of a [Boolean circuit](/boolean-circuit/), for $N = nw$ input bits, and written $M(N)$ when the context makes the unit clear.

**The convolution view.** The product of the digit sequences is the [convolution](/convolution/) $t_k = \sum_{i + j = k} a_i b_j$. Then $AB = \sum_k t_k \beta^k$, and the $c_k$ follow from the $t_k$ by one pass of carries. So integer multiplication is [polynomial multiplication](/polynomial-multiplication/) of $A(x) = \sum a_i x^i$ and $B(x)$, followed by the evaluation at $x = \beta$.

## Variants

- **Unbalanced multiplication.** For $m \ge n$, cut $A$ into $\lceil m/n \rceil$ pieces of $n$ limbs. Then the cost is at most $\lceil m/n \rceil M(n) + O(m)$.
- **Squaring.** $A^2$ is a special case, and a general product reduces to two squarings: $AB = \left((A + B)^2 - (A - B)^2\right)/4$. So squaring and multiplication have the same cost up to a constant factor. The school method needs only $n(n+1)/2$ limb products for a square instead of $n^2$, because each cross term $a_i a_j$ with $i \ne j$ appears twice and is computed once.
- **Short and middle products.** Only the low $n$ limbs ($AB \bmod \beta^n$), only the high $n$ limbs, or the middle part. These appear in Newton iterations for division.
- **Multiplication modulo $2^K + 1$.** The core step of the [Schönhage-Strassen algorithm](/schonhage-strassen-multiplication/), where a shift by a power of two is a cheap root of unity.
- **Modular multiplication.** $AB \bmod m$ for a fixed $m$, the step of [modular exponentiation](/modular-exponentiation/), with [Montgomery multiplication](/montgomery-multiplication/) or [Barrett reduction](/barrett-reduction/).
- **Multiplication by a constant.** One operand is fixed and known ahead of time, as a sequence of shifts and additions.
- **Fixed size in hardware.** For one size $n$ of bits, the question is the depth and the number of gates of a circuit: the [array multiplier](/array-multiplier/), the [Wallace tree](/wallace-tree-multiplier/) and the [Dadda multiplier](/dadda-multiplier/), often with [Booth recoding](/booth-multiplication/) of the multiplier.
- **On-line multiplication.** The digits of the inputs arrive one at a time from the low end, and digit $k$ of the product must be output before digit $k + 1$ of the inputs is read.

## Examples

**School method in base 10.** $1234 \times 5678 = 7006652$. Karatsuba's step with $\beta^{1} = 100$ uses $a_1 = 12$, $a_0 = 34$, $b_1 = 56$, $b_0 = 78$, and three products: $z_2 = 12 \cdot 56 = 672$, $z_0 = 34 \cdot 78 = 2652$ and $(12 + 34)(56 + 78) = 46 \cdot 134 = 6164$. Then the middle term is $z_1 = 6164 - 672 - 2652 = 2840$, and

$$672 \cdot 100^2 + 2840 \cdot 100 + 2652 = 7006652 .$$

**A full product of limbs.** In base $\beta = 2^8$, $A = B = [255, 255]$, which is $2^{16} - 1 = 65535$. The product is $4294836225 = \text{0xFFFE0001}$, the limb array $[1, 0, 254, 255]$ with $m + n = 4$ limbs. This is the largest product of two 2-limb numbers, and its top limb is $\beta - 1$.

**A short product.** In base 10, $9 \times 9 = 81$ and $1 \times 1 = 1$: two 1-digit inputs give a product of $m + n = 2$ or $m + n - 1 = 1$ digits.

**How the counts grow.** The table gives $n^2$ against $n^{\log_2 3}$ and $n^{\log_3 5}$, the leading terms of the school method, of Karatsuba and of Toom-3, for a few sizes. They are counts of the main term only: the constant factors and the additions are left out, and these change the real crossover points.

| $n$ | $n^2$ | $n^{\log_2 3}$ | $n^{\log_3 5}$ |
|---|---|---|---|
| 10 | 100 | 38 | 29 |
| 100 | 10,000 | 1,479 | 851 |
| 1,000 | 1,000,000 | 56,871 | 24,827 |
| 10,000 | 100,000,000 | 2,187,006 | 724,259 |

## Known algorithms

| algorithm | year | cost | model |
|---|---|---|---|
| [schoolbook](/schoolbook-multiplication/), [lattice](/lattice-multiplication/), [Russian peasant](/russian-peasant-multiplication/) | ancient | $\Theta(n^2)$ | limb operations |
| [Karatsuba](/karatsuba-multiplication/) | 1962 | $O(n^{\log_2 3}) = O(n^{1.585})$ | limb operations |
| [Toom-Cook](/toom-cook-multiplication/), $k$ parts | Toom 1963, Cook 1966 | $O(n^{\log_k (2k - 1)})$, for example $O(n^{1.465})$ for $k = 3$ | limb operations |
| [Schönhage-Strassen](/schonhage-strassen-multiplication/) | 1971 | $O(N \log N \log\log N)$ | bit operations |
| [Fürer](/furer-multiplication/) | 2007 | $N \log N \cdot 2^{O(\log^* N)}$ | bit operations |
| [Harvey and van der Hoeven](/harvey-van-der-hoeven-multiplication/) | 2019, published 2021 | $O(N \log N)$ | bit operations |

Toom-Cook with a number of parts that grows with $n$ gives $O(n^{1 + \varepsilon})$ for each $\varepsilon > 0$. Between Fürer and Harvey and van der Hoeven, the constant in the exponent $2^{O(\log^* N)}$ was made explicit and lowered: Harvey, van der Hoeven and Lecerf reached $O(N \log N \cdot 8^{\log^* N})$ in 2016, and later work reached $4^{\log^* N}$; Section 1 of the paper of Harvey and van der Hoeven surveys these steps.

**Which method is used in practice.** All bounds in the table are proved. Which method is fastest at a given size is observed, not proved, and depends on the machine and the code. Brent and Zimmermann report that the switch from schoolbook to Karatsuba is best between about 10 and 100 words, depending on the processor. GMP measures its crossover points from schoolbook to Karatsuba, to several Toom-Cook variants, and to its FFT, on each machine, and stores them in tuning files. The algorithms of Fürer and of Harvey and van der Hoeven are not used in practice: their bounds only become better than Schönhage-Strassen for sizes far beyond any computer.

## Bounds

**Upper bound.** $O(N \log N)$ bit operations on a multitape Turing machine, by Harvey and van der Hoeven. This confirms the order that Schönhage and Strassen conjectured in 1971 as the right one.

**Trivial lower bound.** Each algorithm must read all its input, so $\Omega(N)$ bit operations, or $\Omega(n)$ limb operations, are needed. Nothing better is proved for general multitape Turing machines or for Boolean circuits.

**On-line lower bound.** Cook and Aanderaa (1969) proved a lower bound above linear for on-line multiplication on multitape Turing machines, and Paterson, Fischer and Meyer (1974) improved it to $\Omega(N \log N)$. The bound uses the on-line condition and does not hold for general algorithms.

**Conditional lower bound.** Afshani, Freksen, Kamma and Larsen (2019) proved that Boolean circuits of bounded fan-in and fan-out need $\Omega(N \log N)$ gates for multiplication, if a conjecture of Li and Li on network coding is true. Under that conjecture, $O(N \log N)$ is optimal for such circuits.

## Reductions

- **Squaring.** Multiplication reduces to two squarings and $O(n)$ extra work by the identity of the variants, so $M(n) = \Theta(S(n))$ for the cost $S$ of a square.
- **Division and roots.** With [Newton's method](/newton-raphson-division/), a reciprocal, a quotient with remainder and an integer square root cost $O(M(n))$, if $M(n)/n$ does not decrease. In the other direction, a square is a short formula in reciprocals, so division is not easier than multiplication by more than a constant factor. The pages [integer division](/integer-division/) and [Burnikel-Ziegler division](/burnikel-ziegler-division/) give the details.
- **Polynomials.** By [Kronecker substitution](/kronecker-substitution/), a product of integer polynomials is one integer product of large numbers. In the other direction, the convolution view above turns integer multiplication into polynomial multiplication plus one pass of carries. The fast methods ([FFT polynomial multiplication](/fft-polynomial-multiplication/), the [number-theoretic transform](/number-theoretic-transform/)) are used in both directions.
- **Radix conversion.** Conversion between base $2^w$ and base 10 costs $O(M(n) \log n)$ by divide and conquer ([radix conversion](/radix-conversion/)).

## Applications

- Public-key cryptography: RSA, Diffie-Hellman and elliptic curves run many products of numbers of a few hundred to a few thousand bits.
- Primality tests and records: the [Lucas-Lehmer test](/lucas-lehmer-test/) squares numbers of tens of millions of bits, with an FFT.
- Computing constants such as $\pi$ and $e$ to billions of digits, where almost all of the time is spent in multiplication.
- Exact linear algebra and computer algebra, through polynomial and matrix products with large coefficients.

## References
