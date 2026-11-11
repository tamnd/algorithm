---
tag: 3KTP1K
kind: problem
slug: multivariate-quadratic-problem
name: Multivariate quadratic problem
aliases:
- MQ problem
area: cryptography/post-quantum
level: advanced
summary: Find a common zero of m quadratic polynomials in n variables over a finite field. NP-complete, and the hard problem under multivariate signatures such as UOV.
prereqs: [multivariate-cryptography, np-complete]
see_also: [xl-algorithm, f4-algorithm, f5-algorithm, groebner-basis, gray-code, unbalanced-oil-and-vinegar, hidden-field-equations, syndrome-decoding-problem]
sources:
  - book: isbn:9780716710455
    title: Michael R. Garey and David S. Johnson, Computers and Intractability, a Guide to the Theory of NP-Completeness, W. H. Freeman, 1979
    locator: Appendix A7.2, problem AN9 (algebraic equations over GF(2), NP-complete)
  - paper: "Jacques Patarin and Louis Goubin, Trapdoor one-way permutations and multivariate polynomials, ICICS 1997, LNCS 1334, pages 356 to 368"
    locator: the proof that solving quadratic systems is NP-hard over any finite field
  - paper: "Charles Bouillaguet, Hsieh-Chung Chen, Chen-Mou Cheng, Tung Chou, Ruben Niederhagen, Adi Shamir and Bo-Yin Yang, Fast exhaustive search for polynomial systems in F2, CHES 2010, LNCS 6225, pages 203 to 218"
    locator: the Gray code enumeration with first and second derivatives, and its cost of about 4 log2(n) 2^n bit operations
  - paper: "Nicolas Courtois, Alexander Klimov, Jacques Patarin and Adi Shamir, Efficient algorithms for solving overdefined systems of multivariate polynomial equations, Eurocrypt 2000, LNCS 1807, pages 392 to 407"
    locator: the XL algorithm and its heuristic analysis
  - paper: "Jean-Charles Faugère, A new efficient algorithm for computing Gröbner bases (F4), Journal of Pure and Applied Algebra 139, pages 61 to 88, 1999"
    locator: the whole paper (F4, Gröbner bases by sparse linear algebra on Macaulay-type matrices)
  - paper: "Jean-Charles Faugère, A new efficient algorithm for computing Gröbner bases without reduction to zero (F5), ISSAC 2002, pages 75 to 83"
    locator: the whole paper (F5 and its signature criterion, which removes the reductions to zero for regular sequences)
  - paper: "Luk Bettale, Jean-Charles Faugère and Ludovic Perret, Hybrid approach for solving multivariate systems over finite fields, Journal of Mathematical Cryptology 3(3), pages 177 to 197, 2009"
    locator: the whole paper (guess k variables, then run F5 on the overdetermined rest, and choose the best k)
  - paper: "Aviad Kipnis, Jacques Patarin and Louis Goubin, Unbalanced oil and vinegar signature schemes, Eurocrypt 1999, LNCS 1592, pages 206 to 222"
    locator: the section on underdetermined systems (polynomial time when n is at least m(m + 1) in characteristic 2)
---

The multivariate quadratic (MQ) problem asks for a common zero of $m$ quadratic polynomials in $n$ variables over a finite field $\mathbb{F}_q$. Its decision version is NP-complete, already over $\mathbb{F}_2$ (Garey and Johnson), and Patarin and Goubin (1997) showed NP-hardness over every finite field. Random instances with $m \approx n$ also look hard: the best algorithms are exponential in $n$, and quantum computers are only known to give about a square root speed-up. MQ is the hard problem that every [multivariate](/multivariate-cryptography/) signature scheme relies on, and it is also the core of algebraic attacks on block ciphers and stream ciphers.

**Notation.** $\mathcal{P} = (p_1, \ldots, p_m)$ with $p_i \in \mathbb{F}_q[x_1, \ldots, x_n]$ of degree at most 2, and $\mathcal{P}(x) = (p_1(x), \ldots, p_m(x))$. $\mathrm{MQ}(q, n, m)$ is the set of such systems. $D$ is the working degree of XL, $d_{\mathrm{reg}}$ the degree of regularity, and $2 \le \omega \le 3$ the exponent of matrix multiplication. $\lambda$ is the security parameter, $\mathcal{A}$ an adversary and $\mathrm{Adv}$ its advantage.

## In plain words

You get a list of equations. Each one adds up products of two unknowns, single unknowns and a constant, and all arithmetic is modulo a small number, for example modulo 2 or modulo 31. You must find values for the unknowns that make every equation zero.

With only single unknowns this is school algebra and fast. The products of two unknowns are what make it hard. Computers can try all values when there are few unknowns, and clever elimination helps when there are many more equations than unknowns. With a hundred or so unknowns and about as many equations, no method known today finishes.

## Definition

**MQ (search).** Given $\mathcal{P} \in \mathrm{MQ}(q, n, m)$ and $y \in \mathbb{F}_q^m$, find $x \in \mathbb{F}_q^n$ with $\mathcal{P}(x) = y$, or report that none exists. The case $y = 0$ is general, because $y$ can be moved into the constant terms.

**MQ (decision).** Decide if $\mathcal{P}(x) = 0$ has a solution. This is in NP, since a solution is checked in $O(mn^2)$ field operations.

**Random MQ.** In cryptography the coefficients are uniform and $y = \mathcal{P}(s)$ for a uniform $s$, so a solution exists. An adversary inverts the random map:

$$\mathrm{Adv}^{\mathrm{MQ}}_{q,n,m}(\mathcal{A}) = \Pr\left[\mathcal{P}(\mathcal{A}(\mathcal{P}, \mathcal{P}(s))) = \mathcal{P}(s)\right],$$

over uniform $\mathcal{P}$, uniform $s$ and the coins of $\mathcal{A}$. The MQ assumption says this is negligible in $\lambda$ for every efficient $\mathcal{A}$ when $n$, $m$ and $q$ grow with $\lambda$ in the chosen way.

## Variants

- **Determined, overdetermined, underdetermined.** $m = n$ is usual for MQ-based identification. $m > n$ makes elimination easier and the solution unique; signature schemes have $n > m$, so many solutions exist.
- **Field size.** Over $\mathbb{F}_2$ the field equations $x_i^2 = x_i$ make every system quadratic in a Boolean sense, and exhaustive search is cheap per point. Over larger fields, guessing costs $q$ per variable, so Gröbner basis methods matter more.
- **Structured MQ.** The public maps of [UOV](/unbalanced-oil-and-vinegar/), [Rainbow](/rainbow-signature/) and [HFE](/hidden-field-equations/) are not random. Their hidden structure can make them easier than random MQ, which is why each scheme also needs its own structural analysis.
- **MinRank.** Find a low rank combination of given matrices. The quadratic forms of a public map are such matrices, so MinRank attacks hit schemes whose central map has low rank.

## Examples

**A small system over $\mathbb{F}_2$.** Solve

$$x_0 x_1 + x_2 + 1 = 0, \quad x_0 x_2 + x_1 + x_0 = 0, \quad x_1 x_2 + x_0 + x_2 = 0.$$

The first equation gives $x_2 = 1 + x_0 x_1$. If $x_0 = 0$, then $x_2 = 1$; the second equation gives $x_1 = 0$, and the third gives $0 + 0 + 1 = 1$, a contradiction. If $x_0 = 1$ and $x_1 = 0$, then $x_2 = 1$, and the second and third give $1 + 0 + 1 = 0$ and $0 + 1 + 1 = 0$. If $x_0 = x_1 = 1$, then $x_2 = 0$, and the third gives $0 + 1 + 0 = 1$. So $(1, 0, 1)$ is the only solution. In Gray code order the points are $000, 100, 110, 010, 011, 111, 101, 001$ (written $x_0 x_1 x_2$), and the search finds the solution at step 6.

**XL sizes.** For $n = 3$ variables and $m = 4$ equations, XL at degree $D$ multiplies each equation by the $\binom{n + D - 2}{D - 2}$ monomials of degree at most $D - 2$ and treats the $\binom{n + D}{D}$ monomials of degree at most $D$ as unknowns. At $D = 2$ that is 4 rows and 10 columns, at $D = 3$ 16 rows and 20 columns, and at $D = 4$ 40 rows and 35 columns. On random toy systems over $\mathbb{F}_{31}$ with a planted solution, the code of this page needed $D = 2$ for $(n, m) = (3, 9)$, $D = 3$ for $(3, 5)$, $D = 4$ for $(4, 6)$ and $D = 5$ for $(4, 5)$: fewer equations need a higher degree.

The Python code for these examples is for study only and not constant time. For real work use a computer algebra system with F4 or F5, such as Magma or msolve, or the libFES library for exhaustive search over $\mathbb{F}_2$.

## Known algorithms

- **Exhaustive search.** Try all $q^n$ points. Over $\mathbb{F}_2$, Bouillaguet et al. (CHES 2010) visit the points in [Gray code](/gray-code/) order, so that consecutive points differ in one bit. Then $\mathcal{P}(x \oplus e_k) = \mathcal{P}(x) + D_k\mathcal{P}(x)$, the first derivative $D_k\mathcal{P}$ is linear, and it changes by a constant second derivative when another bit flips. Each step is two XORs on words that hold all $m$ polynomials, and the whole search costs about $4 \log_2(n) \cdot 2^n$ bit operations.
- **Linearization.** Treat each monomial as a new unknown and solve the linear system. This works when $m \ge \binom{n+2}{2} - 1$, so for very overdetermined systems only.
- **[XL](/xl-algorithm/) (Courtois, Klimov, Patarin and Shamir, 2000).** Multiply the equations by all monomials up to degree $D - 2$, then linearize at degree $D$. Raise $D$ until elimination gives a univariate polynomial; find its roots and substitute. XL is a redundant form of F4.
- **Gröbner bases.** [Buchberger's algorithm](/buchberger-algorithm/), [F4](/f4-algorithm/) (Faugère, 1999) with sparse linear algebra, and [F5](/f5-algorithm/) (Faugère, 2002), which avoids useless reductions to zero. For a semi-regular system F5 works up to the degree of regularity $d_{\mathrm{reg}}$ and costs $O\left(\binom{n + d_{\mathrm{reg}}}{d_{\mathrm{reg}}}^{\omega}\right)$ field operations.
- **Hybrid approach (Bettale, Faugère and Perret, 2009).** Guess $k$ variables, which costs $q^k$, and solve each overdetermined system in $n - k$ variables with F5. The best $k$ balances the two costs; most security estimates for multivariate schemes use it.
- **Faster Boolean solvers.** The crossbred algorithm of Joux and Vitse (2017) and the polynomial method of Lokshtanov, Paturi, Tamaki, Williams and Yu (2017), which beats $2^n$ by an exponential factor over $\mathbb{F}_2$.

## Bounds

- **Exhaustive search** costs $O(q^n)$ evaluations, or about $4 \log_2(n)\, 2^n$ bit operations over $\mathbb{F}_2$.
- **Degree of regularity.** For a semi-regular system over a large field, $d_{\mathrm{reg}}$ is the index of the first coefficient that is not positive in the series $(1 - z^2)^m / (1 - z)^n$. For $m = n$ it is $n + 1$, so F5 is no better than exponential. When $m$ grows like a constant times $n$, $d_{\mathrm{reg}}$ grows linearly in $n$ with a smaller constant, and the cost stays exponential.
- **Easy cases.** Polynomial time when $m \ge \binom{n+2}{2} - 1$ (linearization), heuristically when $m \ge \epsilon n^2$ for a constant $\epsilon$ (XL), and when $n \ge m(m + 1)$ in characteristic 2 (Kipnis, Patarin and Goubin, 1999), a case that UOV parameters must avoid.
- **Quantum.** Grover search gives about $2^{n/2}$ evaluations over $\mathbb{F}_2$. Quantum versions of the hybrid approach do a little better, but no polynomial time quantum algorithm is known.

## Reductions

- **3-SAT to MQ over any field.** For each Boolean variable add $x_i^2 - x_i = 0$, which forces $x_i \in \{0, 1\}$. A clause $(\ell_1 \vee \ell_2 \vee \ell_3)$ holds when $(1 - \ell_1)(1 - \ell_2)(1 - \ell_3) = 0$, with $\ell = x_i$ or $\ell = 1 - x_i$. A new variable $y = (1 - \ell_1)(1 - \ell_2)$ makes both equations quadratic. So a polynomial time algorithm for MQ would solve 3-SAT, which is the argument of Patarin and Goubin.
- **Field change.** A system over $\mathbb{F}_{q^k}$ becomes a system over $\mathbb{F}_q$ with $k$ times as many variables and equations, by writing each element in a basis. This is how the big field schemes give quadratic public maps.
- **To and from other problems.** The [syndrome decoding problem](/syndrome-decoding-problem/) and LPN have algebraic models as polynomial systems, and MinRank reduces to MQ by the Kipnis-Shamir modelling.

## Applications

- **Trapdoor signatures.** [UOV](/unbalanced-oil-and-vinegar/), MAYO, QR-UOV and SNOVA, the multivariate candidates of round 3 of the NIST process for additional signatures, rest on MQ and on the hardness of finding the hidden structure.
- **Schemes with no trapdoor.** The 5-pass identification scheme of Sakumoto, Shirai and Hiwatari (Crypto 2011), MQDSS, and MQOM rest only on random MQ.
- **Algebraic cryptanalysis.** Writing a cipher as a polynomial system and solving it with F4, F5 or SAT solvers.
- **Attacks on multivariate schemes.** Every key recovery or forgery ends in an MQ instance; the art is to make that instance small or overdetermined.

## References
