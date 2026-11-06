---
tag: TWEX4X
kind: technique
slug: coppersmith-method
name: Coppersmith's method
aliases:
- Coppersmith's theorem
- Coppersmith's theorem for small roots
- Coppersmith attack
- small roots method
- Howgrave-Graham method
area: number-theory/lattice-reduction
level: research
summary: Uses lattice reduction to find small integer roots of modular or integer polynomials.
prereqs: [lll-algorithm, lattice-determinant, polynomial-root-finding]
see_also: [rsa-cryptosystem, wiener-attack, integer-factorization, lll-approximation-guarantee, resultant, chinese-remainder-theorem, bkz-algorithm, rsa-problem]
sources:
  - paper: "D. Coppersmith, Small solutions to polynomial equations, and low exponent RSA vulnerabilities, Journal of Cryptology 10(4) (1997)"
    locator: pages 233 to 260 (the univariate modular theorem with bound N^(1/d), the bivariate integer case, and the RSA applications)
  - paper: "N. Howgrave-Graham, Finding small roots of univariate modular equations revisited, Cryptography and Coding, LNCS 1355 (1997)"
    locator: pages 131 to 142 (the lattice of shifted polynomials and the lemma that a short polynomial has the root over the integers)
  - paper: "A. May, Using LLL-reduction for solving RSA and factorization problems, in P. Q. Nguyen and B. Vallee (eds.), The LLL Algorithm, Springer (2010)"
    locator: pages 315 to 348 (the divisor version with bound N^(beta^2/d), factoring with known bits, and the multivariate heuristics)
  - paper: "D. Boneh and G. Durfee, Cryptanalysis of RSA with private key d less than N^0.292, IEEE Transactions on Information Theory 46(4) (2000)"
    locator: pages 1339 to 1349 (the small inverse problem and the bivariate heuristic attack)
  - book: isbn:9781107013926
    title: Steven D. Galbraith, Mathematics of Public Key Cryptography, Cambridge University Press, 2012
    locator: Chapter 19 (Coppersmith's method and related applications)
---

Coppersmith's method finds all small integer roots of a polynomial equation modulo an integer $N$ whose factorization is unknown, and of some integer polynomial equations in two variables. It writes many polynomials that share the wanted root modulo a power of $N$, puts their coefficient vectors into a lattice, and uses [LLL](/lll-algorithm/) to find an integer combination with small coefficients. A polynomial with small enough coefficients that vanishes at the root modulo $N^m$ vanishes there over the integers, and roots over the integers are easy to find. For a monic polynomial of degree $d$ modulo $N$ this finds every root $|x_0| \le N^{1/d}$ in time polynomial in $d$ and $\log N$. Its best-known uses break RSA with small public exponents, factor $N = pq$ from half of the digits of $p$, and attack small private exponents.

## In plain words

Solving an equation modulo a number $N$ is hard when nobody knows the factors of $N$, but solving an equation over the ordinary integers is easy. The trick is to turn the first kind of equation into the second kind, which is possible when the unknown is small.

Take the polynomial and multiply it by powers of $x$ and of $N$. All these new polynomials vanish modulo a power of $N$ at the secret root. Any combination of them with integer weights does too. If some combination has small coefficients, its value at the small root is a small number that is also a multiple of a large power of $N$, so it must be exactly zero.

Finding such a combination is a short vector problem in a lattice, and LLL finds one that is short enough. The larger the lattice, the larger the roots it can reach.

## When it applies

Notation is that of the other pages in this area: lattice bases have rows $b_1, \ldots, b_w$ with Gram-Schmidt vectors $b_i^*$, coefficients $\mu_{ij}$ and LLL parameter $\delta$; $\lambda_1(L)$ is the length of a shortest nonzero vector and $\det(L)$ the determinant. For a polynomial $h(x) = \sum_k h_k x^k$, $\|h\|$ is the Euclidean length of its coefficient vector, and $h(xX) = \sum_k h_k X^k x^k$.

- **A univariate modular equation.** $f(x_0) \equiv 0 \pmod b$ for a monic integer polynomial $f$ of degree $d$ and a divisor $b \ge N^\beta$ of a known $N$, with $0 < \beta \le 1$. The case $b = N$, $\beta = 1$ is the original one; $b$ itself need not be known. A polynomial with leading coefficient $a$ is made monic by multiplying by $a^{-1} \bmod N$; if that inverse does not exist, $\gcd(a, N)$ is a factor of $N$.
- **A small root.** The method finds roots with $|x_0| \le X$ for $X$ a little below $N^{\beta^2/d}$. Coppersmith's theorem, in the form of Howgrave-Graham and May, says that all such roots with $|x_0| \le N^{\beta^2/d}$ can be found in time polynomial in $d$ and $\log N$. For $\beta = 1$ this is $N^{1/d}$.
- **Unknown factorization.** If the factors of $N$ are known, one solves modulo each prime power and combines with the [Chinese remainder theorem](/chinese-remainder-theorem/) instead.
- **Several variables, heuristically.** With two or more unknowns the same construction works in practice but needs an assumption: the short vectors must give algebraically independent polynomials, whose common roots are then found by [resultants](/resultant/). Coppersmith's bivariate theorem over the integers, for an irreducible $p(x, y) \in \mathbb{Z}[x, y]$, is a proved exception.

## The template

The algorithm takes $f$ monic of degree $d$, the modulus $N$, a bound $X$ and two parameters $m \ge 1$ and $t \ge 0$, and returns the roots it finds. All arithmetic is exact, on integers of size polynomial in $m d \log N$.

```pseudo id=main
COPPERSMITH(f, N, β, X, m, t)              ▷ f monic of degree d, b | N with b ≥ N^β
L1  for i = 0 .. m − 1 and j = 0 .. d − 1: g_{i,j}(x) ← x^j · N^(m − i) · f(x)^i
L2  for j = 0 .. t − 1: h_j(x) ← x^j · f(x)^m
L3  B ← the coefficient vectors of g(xX) for these w = dm + t polynomials, as rows
L4  run LLL with parameter δ on B, and let v be the first row of the result
L5  h(x) ← Σ_k (v_k / X^k) x^k
L6  R ← the integer roots of h with |x| ≤ X
L7  return the x_0 ∈ R with gcd(f(x_0), N) ≥ N^β
```

**Why every polynomial shares the root.** If $f(x_0) \equiv 0 \pmod b$, then $N^{m-i} f(x_0)^i$ is divisible by $b^{m-i} \cdot b^i = b^m$, and so is $x_0^j f(x_0)^m$. Every integer combination of the rows of $B$ is the coefficient vector of $h(xX)$ for some $h$ with $h(x_0) \equiv 0 \pmod{b^m}$.

**Howgrave-Graham's lemma.** Let $h \in \mathbb{Z}[x]$ have degree less than $w$, let $h(x_0) \equiv 0 \pmod{M}$ with $|x_0| \le X$, and let $\|h(xX)\| < M / \sqrt w$. Then $h(x_0) = 0$.

*Proof.* $|h(x_0)| \le \sum_k |h_k| |x_0|^k \le \sum_k |h_k| X^k \le \sqrt w \, \|h(xX)\| < M$ by the Cauchy-Schwarz inequality, and the only multiple of $M$ in $(-M, M)$ is 0. $\square$

**The determinant.** Order the polynomials by degree: $g_{i,j}$ has degree $di + j$ and leading coefficient $N^{m-i}$, and $h_j$ has degree $dm + j$ and leading coefficient 1, because $f$ is monic. So $B$ is lower triangular with diagonal entries $N^{m-i} X^{di+j}$ and $X^{dm+j}$, the rows are independent, and

$$\det(L(B)) = X^{w(w-1)/2} \, N^{d m (m+1)/2}.$$

**The size condition.** LLL with $\delta = 3/4$ returns $\|b_1\| \le 2^{(w-1)/4} \det(L)^{1/w}$; see the [LLL approximation guarantee](/lll-approximation-guarantee/). By the lemma with $M = b^m \ge N^{\beta m}$, line L6 finds every root $|x_0| \le X$ as soon as

$$2^{(w-1)/4} \, X^{(w-1)/2} \, N^{d m (m+1) / (2w)} < \frac{N^{\beta m}}{\sqrt w}.$$

The polynomial $h$ is nonzero of degree less than $w$, so it has fewer than $w$ roots, and line L7 discards the wrong ones. For $\beta = 1$ and $t = d$, so $w = d(m+1)$, the exponent of $N$ on the left is $m/2$, and the condition becomes, up to the factor $c_w = (2^{(w-1)/4} \sqrt w)^{2/(w-1)}$, which tends to $\sqrt 2$,

$$X < c_w^{-1} \, N^{m / (dm + d - 1)},$$

which tends to $N^{1/d}$ as $m$ grows. For general $\beta$, choosing $w$ near $dm/\beta$ gives $N^{\beta^2/d - \varepsilon}$ with $m$ of order $\beta/(d \varepsilon)$, and an exhaustive search over the top few digits of $x_0$ closes the gap to $N^{\beta^2/d}$.

**Cost.** The lattice has dimension $w = dm + t$, of order $1/\varepsilon$ to get within $N^{-\varepsilon}$ of the bound, and entries of size $O(m \log N + w \log X)$ digits. Exact LLL is polynomial in $w$ and in that size, so the whole method is polynomial in $d$, $\log N$ and $1/\varepsilon$. These are proved worst-case bounds; in practice LLL usually returns vectors shorter than its guarantee, and the method often reaches somewhat larger roots than the condition promises. Root finding in line L6 is polynomial too, for example by real root isolation and an exact check of the nearby integers; see [polynomial root finding](/polynomial-root-finding/).

**Example 1, a quadratic modulo $N$.** Let $N = 10403 = 101 \cdot 103$ and $f(x) = x^2 + 3000 x + 10160$, which has the root $x_0 = 7$ modulo $N$, since $f(7) = 31209 = 3N$. Take $m = t = 1$, so $w = 3$, and $X = 8$; the condition asks for $X < N^{1/3}/\sqrt 6 \approx 8.9$. The basis rows are the coefficient vectors of $N$, $N \cdot xX$ and $f(xX)$:

$$B = \begin{pmatrix} 10403 & 0 & 0 \\ 0 & 83224 & 0 \\ 10160 & 24000 & 64 \end{pmatrix}, \qquad \det(L) = 64 N^2.$$

Exact LLL returns the first row $(-1701, 1552, 448)$, of length $\approx 2345.8 < N/\sqrt 3 \approx 6006.2$, which is the coefficient vector of $h(xX)$ for

$$h(x) = 7x^2 + 194 x - 1701 = 7 f(x) - 2N x - 7N = (x - 7)(7x + 243).$$

Its only integer root is $7$, and $f(7) \equiv 0 \pmod N$.

**Example 2, factoring with known high digits.** Let $N = 1300485107497 = p q$ with $p = 1000357$, and suppose we know $\tilde p = 1000192$, which is $p$ with its last 8 binary digits cleared. Then $x_0 = p - \tilde p = 165 < X = 256$ is a root of $f(x) = \tilde p + x$ modulo the unknown divisor $p \ge N^{1/2}$, so $d = 1$ and $\beta = 1/2$. With $m = t = 2$ ($w = 4$) and $m = t = 3$ ($w = 6$) the reduced first row is too long and gives no root. With $m = t = 4$ ($w = 8$) it gives a polynomial with the integer root $165$, and $\gcd(\tilde p + 165, N) = p$. The size condition only guarantees $X \approx 207$ for $m = t = 4$, so this run did better than the worst-case bound. The limit as $m$ grows is $N^{1/4} \approx 1068$.

## Classic examples

- **Stereotyped messages in RSA.** With public exponent $e = 3$, a ciphertext $c = (M + x_0)^3 \bmod N$ of a message whose known part is $M$ reveals the unknown part as a root of $(M + x)^3 - c$, whenever $|x_0| < N^{1/3}$. So with [RSA](/rsa-cryptosystem/) and no randomized padding, an unknown part of up to a third of the length of $N$ can be recovered.
- **Broadcast with related messages.** If related messages $g_i(M)$ are encrypted with small exponents under several moduli $N_i$, the Chinese remainder theorem combines the equations into one monic equation modulo $\prod N_i$, and the method recovers $M$ once enough ciphertexts are known. This strengthens Håstad's earlier attack.
- **Factoring with half of the digits of $p$.** For $N = pq$ with $p \approx q$, the high half of the digits of $p$ determines $p$, as in Example 2, by the case $d = 1$, $\beta = 1/2$, $X = N^{1/4}$. Coppersmith first proved it with his bivariate integer method; the univariate form is due to Howgrave-Graham. It is used against RSA key generation flaws and side channels that leak part of a key, and it also gives partial key exposure attacks.
- **Small private exponents.** Boneh and Durfee write $e d = 1 + k \varphi(N)$ as the bivariate small inverse problem $x (A + y) + 1 \equiv 0 \pmod e$ and break RSA when $d < N^{0.292}$, under the heuristic for several variables. This improves the bound $N^{1/4}$ of [Wiener's attack](/wiener-attack/).

## Variations

- **Coppersmith's original form.** Coppersmith worked in a dual lattice and reduced a basis with rational entries. Howgrave-Graham's version above, with coefficient vectors of shifted polynomials and his lemma, is the one used today.
- **Divisors.** The parameter $\beta$ handles an unknown divisor $b \ge N^\beta$ of $N$, which is the form needed for factoring with known digits; May gave the general bound $N^{\beta^2/d}$.
- **Several variables.** For $f(x_1, \ldots, x_k) \equiv 0$ one chooses a set of shifts and monomials; the Jochemsz-May strategy gives a general recipe. At least $k$ short vectors are needed, and their resultants yield the roots if they are algebraically independent, which is checked in each run but not proved in general.
- **Bivariate integer equations.** For an irreducible $p(x, y) \in \mathbb{Z}[x, y]$, Coppersmith proved that small roots with $|x_0| \le X$, $|y_0| \le Y$ are found in polynomial time when $XY < W^{2/(3\delta')}$ for polynomials of degree $\delta'$ in each variable, with $W$ the largest coefficient of $p(xX, yY)$. Coron simplified the construction.
- **Faster reduction.** The lattice has a triangular structure with large entries, and the needed vector is only moderately short. Rounding the entries to their leading digits before LLL, and reusing a reduced basis for $m$ in the computation for $m + 1$, both speed up the method in practice. Floating-point LLL as in fplll is the usual tool.
- **Approximate common divisors.** Given $N$ and an approximation of a multiple of an unknown divisor, Howgrave-Graham's method finds the divisor; this is the partial approximate gcd problem behind some fully homomorphic encryption schemes.

## Pitfalls

- **A strict size condition.** The lemma needs $\|h(xX)\| < N^{\beta m}/\sqrt w$ strictly. A run with too small a lattice returns a vector that is just too long, and $h$ then has no useful root, as for $m = t = 2, 3$ in Example 2. Increase $m$ and $t$ or split the range of $x_0$ into pieces.
- **The factor $2^{(w-1)/4}$.** It is negligible for large $N$ but not for small ones; small toy examples need larger lattices than the asymptotic bound suggests.
- **Lattice size.** Reaching $N^{1/d - \varepsilon}$ needs dimension of order $1/\varepsilon$, so the last digits of the bound are expensive. Guessing the top digits of $x_0$ and running a smaller lattice per guess is usually cheaper.
- **Non-monic input.** The template assumes $f$ monic; a non-monic $f$ gives a basis that is not triangular in this way and a wrong determinant. Multiply by the inverse of the leading coefficient modulo $N$ first.
- **Checking the roots.** Line L6 can return integer roots of $h$ that are not roots of $f$ modulo $b$. Always check them, as line L7 does.
- **The multivariate heuristic.** With two or more variables the short vectors can share a common factor, and their resultant is then 0. This happens in practice for some attacks, so test the independence and do not report the method as proved.
- **Precision.** The entries have about $m \log N$ digits. Floating-point LLL with too little precision can loop or return a basis that is not reduced; use exact arithmetic or a library that controls precision.

## Exercises

1. Prove that the basis of the template is lower triangular and compute its determinant for $d = 3$, $m = 2$, $t = 3$.
2. Show that for $\beta = 1$, $t = d$ and $w = d(m+1)$, the size condition becomes $X < c_w^{-1} N^{m/(dm + d - 1)}$, and compute the bound for $d = 3$, $m = 1, 2, 4$.
3. For the stereotyped RSA case with $e = 3$ and a 2048-digit binary modulus, how many binary digits of the message can be unknown according to the theorem?
4. Redo Example 1 by hand: reduce the basis with LLL and check that $h(x) = 7 f(x) - 2Nx - 7N$.
5. Explain why the method cannot find roots of size $N^{1/d + \varepsilon}$ in general. Hint: count the roots of $x^d \equiv 0 \pmod{p^d}$ for $N = p^d$.
6. Write the small inverse problem of Boneh and Durfee from $e d = 1 + k(N + 1 - p - q)$, and say which unknowns are small and how small.

## References
