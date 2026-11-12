---
tag: WVJW9K
kind: definition
slug: goppa-code
name: Goppa code
aliases:
- binary Goppa code
area: compression-and-coding/error-correcting-codes
level: research
summary: "The code Gamma(L, g) of words c with sum c_i / (x - a_i) = 0 mod g(x). A binary Goppa code with a squarefree g of degree t has d at least 2t + 1."
history:
  year: 1970
  people: [Valerii D. Goppa]
  note: Goppa defined the codes in 1970 by a rational function modulo a polynomial g; Patterson gave the algebraic decoder for binary Goppa codes in 1975.
prereqs: [bch-code, polynomial-extended-euclidean-algorithm]
see_also: [mceliece-cryptosystem, niederreiter-cryptosystem, reed-solomon-code, parity-check-matrix, minimum-distance, irreducible-polynomial, chien-search, syndrome-decoding-problem]
sources:
  - paper: "V. D. Goppa, A new class of linear correcting codes, Problemy Peredachi Informatsii 6(3), 1970 (English translation in Problems of Information Transmission)"
    title: V. D. Goppa, A new class of linear correcting codes, 1970
    locator: The definition of the codes by the sum of c_i / (x - a_i) modulo g, and the bounds on dimension and distance
  - paper: "N. J. Patterson, The algebraic decoding of Goppa codes, IEEE Transactions on Information Theory 21(2), 1975"
    title: N. J. Patterson, The algebraic decoding of Goppa codes, 1975
    locator: pp. 203 to 207 (decoding t errors of a binary Goppa code with a square root modulo g and the Euclidean algorithm)
  - paper: doi:10.1016/S0019-9958(75)90090-X
    title: Y. Sugiyama, M. Kasahara, S. Hirasawa and T. Namekawa, A method for solving key equation for decoding Goppa codes, Information and Control 27(1), 1975
    locator: pp. 87 to 99 (the key equation of Goppa codes solved by the extended Euclidean algorithm)
  - paper: "E. R. Berlekamp, Goppa codes, IEEE Transactions on Information Theory 19(5), 1973"
    title: E. R. Berlekamp, Goppa codes, 1973
    locator: The survey of the codes, the parity check matrix, and the relation to BCH codes
  - book: isbn:9780444851932
    title: F. J. MacWilliams and N. J. A. Sloane, The Theory of Error-Correcting Codes, North-Holland, 1977
    locator: Chapter 12 (alternant, Goppa and other generalized BCH codes)
---

A Goppa code is a linear code defined by a polynomial $g(x)$ over a finite field $\mathrm{GF}(q^m)$ and a list $L = (a_1, \ldots, a_n)$ of distinct field elements, the *support*, none of which is a root of $g$. A word $c$ over $\mathrm{GF}(q)$ is in the code $\Gamma(L, g)$ when $\sum_i c_i/(x - a_i) \equiv 0 \pmod{g(x)}$. With $\deg g = t$, the code has dimension $k \ge n - m t$ and [minimum distance](/minimum-distance/) $d \ge t + 1$. For binary codes with a squarefree $g$, the bound improves to $d \ge 2t + 1$, so the code corrects $t$ errors with only $m t$ check bits, as a binary [BCH code](/bch-code/) does. Primitive narrow sense BCH codes are Goppa codes with $g(x) = x^{\delta - 1}$. Patterson's algorithm decodes $t$ errors of a binary Goppa code. Binary Goppa codes are the private key of the [McEliece cryptosystem](/mceliece-cryptosystem/).

## Definition

Fix a prime power $q$, an integer $m \ge 1$, a polynomial $g(x) \in \mathrm{GF}(q^m)[x]$ of degree $t \ge 1$, and distinct $a_1, \ldots, a_n \in \mathrm{GF}(q^m)$ with $g(a_i) \ne 0$. Since $g(a_i) \ne 0$, the polynomial $x - a_i$ is a unit modulo $g$, with the inverse

$$\frac{1}{x - a_i} \equiv -\frac{1}{g(a_i)} \cdot \frac{g(x) - g(a_i)}{x - a_i} \pmod{g(x)},$$

where the second factor is a polynomial of degree $t - 1$. The **Goppa code** is

$$\Gamma(L, g) = \Bigl\{ c \in \mathrm{GF}(q)^n : S_c(x) = \sum_{i=1}^{n} \frac{c_i}{x - a_i} \equiv 0 \pmod{g(x)} \Bigr\}.$$

$S_c(x)$ is the *syndrome polynomial* of $c$. The code is **binary** when $q = 2$, **irreducible** when $g$ is irreducible, and **separable** when $g$ is squarefree.

**Parity check matrix.** Expanding the condition coefficient by coefficient gives the $t \times n$ matrix over $\mathrm{GF}(q^m)$

$$H = \begin{pmatrix} 1/g(a_1) & \cdots & 1/g(a_n) \\ a_1/g(a_1) & \cdots & a_n/g(a_n) \\ \vdots & & \vdots \\ a_1^{t-1}/g(a_1) & \cdots & a_n^{t-1}/g(a_n) \end{pmatrix}, \qquad c \in \Gamma(L, g) \iff H c^{\mathsf T} = 0 .$$

This is the parity check matrix of a generalized Reed-Solomon code over $\mathrm{GF}(q^m)$. So $\Gamma(L, g)$ is a *subfield subcode* of it, the words with all symbols in $\mathrm{GF}(q)$; codes of this kind are called *alternant codes*. Writing each entry of $H$ as $m$ symbols of $\mathrm{GF}(q)$ gives a [parity check matrix](/parity-check-matrix/) with $m t$ rows over $\mathrm{GF}(q)$.

**Parameters.**

- Length $n \le q^m$. The support can contain 0.
- Dimension $k \ge n - m t$, from the $m t$ rows over $\mathrm{GF}(q)$.
- Distance $d \ge t + 1$, because $H$ is a Vandermonde matrix times a diagonal matrix, so any $t$ columns are independent.
- For $q = 2$ and $g$ squarefree, $\Gamma(L, g) = \Gamma(L, g^2)$, and so $d \ge 2t + 1$.

**Why the binary bound doubles.** Let $c$ be a binary word of weight $w \ge 1$ with support positions $B$, and $\sigma(x) = \prod_{i \in B}(x - a_i)$. Then $S_c = \sigma'/\sigma$, and $\sigma$ is a unit modulo $g$, so $c \in \Gamma(L, g)$ exactly when $g \mid \sigma'$. In characteristic 2, the derivative $\sigma'$ has only even powers of $x$, so $\sigma' = h^2$ for some $h$. If $g$ is squarefree and $g \mid h^2$, then $g \mid h$, so $g^2 \mid \sigma'$. Since $\sigma$ has distinct roots, $\sigma' \ne 0$, so $w - 1 \ge \deg \sigma' \ge 2t$.

**Patterson's decoder.** Let $g$ be irreducible of degree $t$, $y = c + e$ with $c \in \Gamma(L, g)$ binary, and $e$ of weight at most $t$. Let $\sigma_e(x) = \prod_{e_i = 1}(x - a_i)$, the error locator. Then $S_y = S_e$ and the key equation is $S_e \sigma_e \equiv \sigma_e' \pmod g$. The decoder:

1. computes $S = S_y \bmod g$; if $S = 0$, there is no error;
2. computes $T = S^{-1} \bmod g$ with the [extended Euclidean algorithm](/polynomial-extended-euclidean-algorithm/);
3. if $T = x$, returns $\sigma = x$; otherwise computes $R$ with $R^2 \equiv T + x \pmod g$, which is unique because squaring is a bijection of the field $\mathrm{GF}(2^m)[x]/(g)$;
4. runs the extended Euclidean algorithm on $g$ and $R$ until the remainder $a$ has $\deg a \le \lfloor t/2 \rfloor$, with the cofactor $b$ such that $a \equiv b R \pmod g$ and $\deg b \le \lfloor (t-1)/2 \rfloor$;
5. sets $\sigma = a^2 + x b^2$ and finds its roots in $L$, for example by a [Chien](/chien-search/) style search.

Step 4 works because $\sigma_e = a^2 + x b^2$ for the even and odd parts, $\sigma_e' = b^2$, and the key equation becomes $a^2 \equiv b^2 (T + x)$, so $a \equiv b R$. The cost is $O(n t)$ for the syndrome and the root search and $O(m t^3)$ for the square root by repeated squaring, or less with a precomputed square root of $x$.

A general decoder for alternant codes, such as Berlekamp-Massey or the Euclidean algorithm of Sugiyama et al. applied with $g^2$, also corrects $t$ errors of a binary separable Goppa code. Without the squaring trick, it corrects only $\lfloor t/2 \rfloor$ errors of $\Gamma(L, g)$.

## Examples and non-examples

**A [16, 8, 5] binary Goppa code.** Take $\mathrm{GF}(16)$ with $\alpha^4 = \alpha + 1$, $L$ all 16 field elements in the order $0, 1, \alpha, \ldots, \alpha^{14}$, and $g(x) = x^2 + x + \alpha^3$. The polynomial $g$ has no root in $\mathrm{GF}(16)$, so it is irreducible and every element can be in the support. Here $(g(x) - g(a))/(x - a) = x + a + 1$, so

$$\frac{1}{x + a} \equiv \frac{x + a + 1}{g(a)} \pmod g ,$$

for example $1/x \equiv \alpha^{12}(x + 1)$ and $1/(x + 1) \equiv \alpha^{12} x$. The code has $n = 16$, $k = 16 - 4 \cdot 2 = 8$ and $d = 5 = 2t + 1$. Its weight distribution is $A_0 = 1$, $A_5 = 24$, $A_6 = 44$, $A_7 = 40$, $A_8 = 45$, $A_9 = 40$, $A_{10} = 28$, $A_{11} = 24$, $A_{12} = 10$.

**A decoding step.** In the same code, let the zero codeword have errors at $\alpha^2$ and $\alpha^7$. Patterson's decoder computes

| step | result |
|---|---|
| $S = 1/(x + \alpha^2) + 1/(x + \alpha^7)$ | $\alpha^{12} + \alpha^2 x$ |
| $T = S^{-1} \bmod g$ | $\alpha^4 + \alpha^{14} x$ |
| $T + x$ | $\alpha^4 + \alpha^3 x$ |
| $R = \sqrt{T + x} \bmod g$ | $\alpha^6 + \alpha^9 x$ |
| $a = R$, $b = 1$ (already $\deg R \le 1$) | |
| $\sigma = a^2 + x b^2$ | $\alpha^{12} + x + \alpha^3 x^2 = \alpha^3 (x + \alpha^2)(x + \alpha^7)$ |

The roots $\alpha^2$ and $\alpha^7$ are the error positions.

**A binary Goppa code of length 32 and dimension 17.** Over $\mathrm{GF}(32)$ with $\alpha^5 = \alpha^2 + 1$, the cubic $g(x) = x^3 + \alpha x + 1$ has no root, so it is irreducible. With $L = \mathrm{GF}(32)$, the code has $k = 32 - 5 \cdot 3 = 17$ and $d \ge 7$, and Patterson's decoder corrects every pattern of 3 errors.

**BCH codes.** Let $n = 2^m - 1$, $L = (1, \alpha^{-1}, \ldots, \alpha^{-(n-1)})$ and $g(x) = x^{r}$. Since $1/(x - \beta) = -\beta^{-1} \sum_{j \ge 0} (x/\beta)^j$ in the power series ring, the coefficient of $x^j$ in $S_c$ is $-\sum_i c_i \alpha^{i(j+1)} = -c(\alpha^{j+1})$. So $\Gamma(L, x^r)$ is the narrow sense BCH code with the zeros $\alpha, \ldots, \alpha^{r}$. With $m = 4$ and $r = 4$, this is the binary BCH [15, 7, 5] code with generator $x^8 + x^7 + x^6 + x^4 + 1$.

**McEliece parameters.** McEliece used binary irreducible Goppa codes with $m = 10$, $n = 1024$, $t = 50$ and $k = 524$. The smallest parameter set of Classic McEliece has $m = 12$, $n = 3488$ and $t = 64$. The [McEliece cryptosystem](/mceliece-cryptosystem/) page covers the cryptosystem: the hidden generator matrix, encryption with a random error, the security, and a toy implementation. This page covers the codes: the definition, the parameters, the link to BCH codes, and decoding.

**Non-example: a root of $g$ in the support.** If $g(a_i) = 0$ for some $i$, then $x - a_i$ has no inverse modulo $g$, and the definition does not apply. For example, $g = x$ cannot have 0 in its support.

**Non-example: $g$ not squarefree.** With $L = (1, \alpha^{-1}, \ldots, \alpha^{-14})$ over $\mathrm{GF}(16)$ and $g(x) = x^2$, the code is $\Gamma(L, x^2)$, the BCH code with zeros $\alpha$ and $\alpha^2$. This is the [15, 11, 3] Hamming code, with $d = 3 = t + 1$, not $2t + 1 = 5$. The binary bound $d \ge 2t + 1$ needs a squarefree $g$.

## Related definitions

- [BCH code](/bch-code/): the Goppa codes with $g(x) = x^{\delta - 1}$ and the support of inverse powers of $\alpha$. Unlike BCH codes, most Goppa codes are not cyclic.
- [Reed-Solomon code](/reed-solomon-code/): a Goppa code is a subfield subcode of a generalized Reed-Solomon code, and so is an alternant code.
- [Parity check matrix](/parity-check-matrix/) and [minimum distance](/minimum-distance/): the matrix $H$ above, and the bounds $d \ge t + 1$ and, for binary separable codes, $d \ge 2t + 1$.
- [McEliece cryptosystem](/mceliece-cryptosystem/) and [Niederreiter cryptosystem](/niederreiter-cryptosystem/): public key schemes with a binary Goppa code as the private key. Their security rests on the [syndrome decoding problem](/syndrome-decoding-problem/) for a code that looks random.
- [Irreducible polynomial](/irreducible-polynomial/): an irreducible $g$ makes $\mathrm{GF}(2^m)[x]/(g)$ a field, which Patterson's decoder uses for the inverse and the square root.
- Goppa codes on algebraic curves (algebraic geometry codes) generalize the construction from the projective line to curves of higher genus.

## References
