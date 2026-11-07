---
tag: 9WJZVK
kind: technique
slug: modular-methods
name: Modular methods
aliases:
- multimodular method
- evaluation and modular images
- Chinese remaindering method
- small primes method
area: algebra/computer-algebra
level: advanced
summary: Computes results modulo several primes and reconstructs the integer or rational answer with the Chinese remainder theorem.
prereqs: [chinese-remainder-theorem, hadamard-bound, prime-number]
see_also: [brown-modular-gcd, multimodular-determinant, heuristic-gcd, dixon-p-adic-lifting, hensel-lifting, zippel-sparse-interpolation, garner-algorithm, polynomial-factorization]
sources:
  - book: isbn:9781107039032
    title: Joachim von zur Gathen and Jürgen Gerhard, Modern Computer Algebra, third edition, Cambridge University Press, 2013
    locator: Chapter 5, Modular algorithms and interpolation (the big prime and small primes determinant, the Chinese remainder algorithm, rational reconstruction) and Chapter 6, The resultant and gcd computation (modular gcd algorithms and unlucky primes)
  - book: isbn:9780792392590
    title: Keith O. Geddes, Stephen R. Czapor and George Labahn, Algorithms for Computer Algebra, Kluwer, 1992
    locator: Chapter 5, Homomorphisms and Chinese remainder algorithms, and Chapter 7, Polynomial GCD computation (the modular and heuristic gcd methods)
  - paper: doi:10.1145/321662.321664
    title: W. S. Brown, On Euclid's algorithm and the computation of polynomial greatest common divisors, Journal of the ACM 18(4), 478-504, 1971
    locator: the modular gcd algorithm and the treatment of unlucky primes
  - paper: "Paul S. Wang, A p-adic algorithm for univariate partial fractions, SYMSAC 1981"
    locator: rational number reconstruction from a modular image
---

Modular methods compute an exact answer over $\mathbb{Z}$ or $\mathbb{Q}$ without coefficient growth. They solve the problem modulo several primes $p_1, \ldots, p_k$, where all arithmetic is on small numbers, and rebuild the answer from its images with the [Chinese remainder theorem](/chinese-remainder-theorem/). For rational answers they finish with rational reconstruction. The method needs two things: an a priori bound $B$ on the size of the answer, such as the [Hadamard bound](/hadamard-bound/) for determinants, and a way to recognise and discard *unlucky* primes, whose images do not reduce from the true answer. With $k$ primes, the cost is $k$ times the cost of one modular computation plus $O(k^2)$ word operations for the reconstruction. Fraction-free and big-integer methods must instead pay for the growth of intermediate numbers. Brown's [modular gcd](/brown-modular-gcd/), the [multimodular determinant](/multimodular-determinant/), modular Gröbner bases and modular resultants are all instances.

## In plain words

Big integers make every step of a computation slow, even when the final answer is small. A modular method avoids them. It repeats the whole computation several times, each time keeping only remainders modulo a different small prime, so every number fits in a machine word. Each run gives the answer's remainder for that prime. Once the product of the primes exceeds twice the largest possible answer, the remainders fix the answer uniquely, and the Chinese remainder theorem rebuilds it. The only danger is a prime for which the computation behaves differently from the true one, for example a gcd that suddenly has a higher degree. Such primes are rare, and they can be detected and skipped.

## When it applies

- The answer is an integer, an integer vector or matrix, or a polynomial with integer coefficients, and there is a computable bound $B$ on its absolute values. For rational answers, a bound on numerators $N$ and denominators $D$ is needed instead.
- The computation commutes with reduction modulo $p$ for all but finitely many primes. The image of the true answer must equal the answer of the reduced problem, possibly after a normalization.
- *Lucky* primes can be distinguished from unlucky ones. Usually an unlucky image has a visibly wrong shape, such as a higher degree or a different set of leading monomials, or a final check can verify the result.

## The template

Notation: the input has integer data, $B$ bounds the absolute value of every integer in the answer, $T(p)$ is the cost of the computation modulo one prime of word size, and $k$ is the number of primes used. The cost model counts word operations on a word RAM.

```pseudo id=main
MODULAR(x, B)
L1  m ← 1;  y ← undefined
L2  while m ≤ 2B do
L3      p ← a new prime of word size that is not bad for x   ▷ e.g. p ∤ lc
L4      y_p ← SOLVE(x mod p)                                  ▷ all arithmetic in Z/pZ
L5      if y_p has a worse shape than y then continue          ▷ p unlucky: discard
L6      if y_p has a better shape than y then (m, y) ← (1, undefined)  ▷ old primes unlucky
L7      y ← the solution of y' ≡ y (mod m), y' ≡ y_p (mod p)    ▷ Chinese remaindering
L8      m ← m · p
L9  return the symmetric residue of y in (−m/2, m/2]         ▷ or rational reconstruction
```

Line L5 and line L6 compare a "shape" such as the degree of a gcd, the rank of a matrix, or the set of leading monomials of a Gröbner basis. Lucky primes give the shape of the true answer and unlucky ones give a different one, always in the same direction. Line L7 is one step of Garner's mixed-radix [Chinese remainder algorithm](/garner-algorithm/). Since every integer of the answer lies in $[-B, B]$ and $m > 2B$, the symmetric residue of line L9 is the answer.

**Cost.** With $k = O(\log B / \log p)$ lucky primes, the loop costs $k\, T(p)$ plus $O(k^2)$ word operations for the classical Chinese remaindering of each output integer, or $O(M(k) \log k)$ with a subproduct tree. These bounds are proved, given the number of unlucky primes met. That number is bounded by the number of prime divisors of a nonzero integer, such as a resultant, that is not too large, so it is small for primes chosen at random from a large set.

## Classic examples

**Determinant of an integer matrix.** For

$$A = \begin{pmatrix} 2 & -1 & 3 \\ 4 & 5 & -6 \\ 7 & 8 & 9 \end{pmatrix},$$

the Hadamard bound is $\prod_i \|A_i\|_2 = \sqrt{14} \sqrt{77} \sqrt{194} \approx 457.3$, so $m > 914.6$ suffices. Gaussian elimination modulo $11$, $13$ and $17$ gives $\det A \equiv 2$, $8$ and $0$. Chinese remaindering gives $2 \bmod 11$, then $112 \bmod 143$, then $255 \bmod 2431$. Since $2431 > 914.6$, $\det A = 255$. Stopping after two primes would return the wrong value $112$, which shows why the bound matters. Every prime is lucky for determinants. With $n \times n$ matrices and entries of $\lambda$ words, $k = O(n (\log n + \lambda))$ primes are needed. Each costs $O(n^3)$ word operations for the elimination, plus the reduction of the entries, and the Chinese remaindering of the result costs $O(k^2)$ (von zur Gathen and Gerhard, Chapter 5, give the full count). See [multimodular determinant](/multimodular-determinant/).

**Gcd of integer polynomials.** For $f, g \in \mathbb{Z}[x]$, Brown's algorithm computes $\gcd(f \bmod p, g \bmod p)$ for several primes. It scales each image so its leading coefficient is $\gamma = \gcd(\operatorname{lc} f, \operatorname{lc} g) \bmod p$, combines the images, and takes the primitive part. A prime is unlucky when it divides the resultant of $f/h$ and $g/h$ for $h = \gcd(f, g)$, and then the modular gcd has too high a degree. For $f = x^2 + 1$ and $g = x + 3$, $\gcd(f, g) = 1$ and $\operatorname{res}(f, g) = 10$. Modulo $5$, both vanish at $x = 2$, so the modular gcd is $x + 3$ and has degree $1$. Line L5 discards it as soon as a prime with a degree $0$ image is seen. Primes that divide both leading coefficients are *bad* and are excluded at line L3. See [Brown's modular gcd](/brown-modular-gcd/).

**Linear systems over $\mathbb{Q}$.** By Cramer's rule, the solution of $Ax = b$ is $x = y / \det A$ with integer $y$. Either reconstruct $y$ and $\det A$ separately, or reconstruct each entry of $x$ as a fraction by rational reconstruction, which needs $m > 2ND$ for bounds $N$, $D$ on numerators and denominators.

**Gröbner bases and resultants.** Arnold's modular Gröbner bases and the Traverso trace algorithm compute bases modulo primes, reject primes whose leading monomials differ, and reconstruct the coefficients rationally. Resultants and characteristic polynomials follow the template directly, because they are polynomials in the input entries.

## Variations

- **Big prime.** Use one prime $p > 2B$. This is simpler but needs multi-word arithmetic modulo $p$. Von zur Gathen and Gerhard analyse both versions and show that small primes are usually faster.
- **Evaluation and interpolation.** For a polynomial variable instead of integer coefficients, replace "modulo $p$" by "evaluate at $x = a$", and the Chinese remainder theorem by [polynomial interpolation](/polynomial-interpolation/). [Zippel's sparse interpolation](/zippel-sparse-interpolation/) uses far fewer points when the answer has few terms.
- **p-adic lifting.** Compute the answer modulo one prime $p$, then lift it to $p^2, p^3, \ldots$ by Newton or [Hensel](/hensel-lifting/) iteration. [Dixon's method](/dixon-p-adic-lifting/) for linear systems and Hensel lifting in [polynomial factorization](/polynomial-factorization/) are of this kind.
- **Heuristic evaluation at a large integer.** The [heuristic gcd](/heuristic-gcd/) evaluates polynomials at one large integer, computes an integer gcd, and reads the polynomial gcd off its digits. This is a modular method with the "prime" replaced by $x - \xi$.
- **Early termination.** Instead of using the worst-case bound $B$, stop when the reconstructed value has not changed for one or two new primes, then verify the result, for instance by trial division for a gcd. This is output-sensitive: the number of primes depends on the actual size of the answer. It is a heuristic unless the verification is exact.
- **Rational reconstruction with unknown bounds.** Monagan's maximal quotient rational reconstruction returns a fraction as soon as one partial quotient is much larger than the others, which detects success with high probability.

## Pitfalls

- **Unlucky primes.** If unlucky images are combined with lucky ones, the result is garbage, and no error is raised. Every modular algorithm must say which shape it compares and in which direction an unlucky prime moves it.
- **Normalization.** Images are defined only up to a unit modulo $p$: a gcd modulo $p$ is determined up to a scalar. Combining a monic image from one prime with a differently scaled image from another gives nonsense. Fix a normalization that is the image of a normalization over $\mathbb{Z}$, such as the leading coefficient $\gamma$ in Brown's algorithm.
- **Bad primes.** Primes that divide a leading coefficient or a denominator of the input change the problem, for example by lowering a degree, and must be excluded before solving.
- **Too small a bound.** If $m \le 2B$ at the end, two different answers have the same residues. The determinant example above returns $112$ instead of $255$ with only two primes.
- **Symmetric residues.** Negative answers need the representative in $(-m/2, m/2]$, not in $[0, m)$.
- **Probabilistic stopping.** Early termination without a final check can return a wrong answer with small but nonzero probability.

## Exercises

1. Compute $\det \begin{pmatrix} 3 & 7 \\ -5 & 4 \end{pmatrix}$ by the template with the primes $5$, $7$ and $11$. Check that the Hadamard bound $\sqrt{58} \sqrt{41} \approx 48.8$ needs $m > 97.5$, and that $5 \cdot 7 = 35$ is not enough.
2. Show that for $f, g \in \mathbb{Z}[x]$ with $h = \gcd(f, g)$, a prime $p$ that does not divide both leading coefficients is unlucky exactly when $p$ divides $\operatorname{res}(f/h, g/h)$. Conclude that only finitely many primes are unlucky.
3. Show that if $m > 2ND$, then for each $u \in \mathbb{Z}/m\mathbb{Z}$ there is at most one fraction $a/b$ with $|a| \le N$, $0 < b \le D$, $\gcd(b, m) = 1$ and $a \equiv ub \pmod m$.
4. Bound the number of word-size primes that can divide a nonzero integer of absolute value at most $2^{1000}$, and use it to bound the number of unlucky primes in exercise 2.

## References
