---
tag: PDEFXC
kind: theorem
slug: quadratic-reciprocity
name: Law of quadratic reciprocity
aliases:
- Gauss's reciprocity law
area: number-theory/modular-arithmetic
level: advanced
summary: For distinct odd primes p and q, (p/q)(q/p) = (-1)^(((p-1)/2)((q-1)/2)).
prereqs: [legendre-symbol, euler-criterion]
see_also: [gauss-lemma, jacobi-symbol, quadratic-residue, modular-square-root, solovay-strassen, primitive-root, multiplicative-order, tonelli-shanks]
sources:
  - book: isbn:9780199219865
    title: G. H. Hardy and E. M. Wright, An Introduction to the Theory of Numbers, sixth edition
    locator: Chapter 6, Section 6.11 (Gauss's lemma and the quadratic character of 2), Section 6.12 (the law of reciprocity) and Section 6.13 (proof of the law of reciprocity)
  - book: isbn:9780387973296
    title: Kenneth Ireland and Michael Rosen, A Classical Introduction to Modern Number Theory, second edition, Springer GTM 84
    locator: Chapter 5, Sections 5.2 and 5.3 (the law of quadratic reciprocity and a proof of it)
  - book: isbn:9780849385230
    title: Alfred J. Menezes, Paul C. van Oorschot and Scott A. Vanstone, Handbook of Applied Cryptography, CRC Press, 1997
    locator: Section 2.4.5, Fact 2.146 (properties of the Legendre symbol, including the law of quadratic reciprocity) and Algorithm 2.149
  - paper: "Gotthold Eisenstein, Geometrischer Beweis des Fundamentaltheorems für die quadratischen Reste, Journal für die reine und angewandte Mathematik 28 (1844), 246 to 248"
    locator: pages 246 to 248
---

The law of quadratic reciprocity relates two questions that look unrelated: whether an odd prime $p$ is a square modulo another odd prime $q$, and whether $q$ is a square modulo $p$. In terms of the [Legendre symbol](/legendre-symbol/), $\left(\frac{p}{q}\right)\left(\frac{q}{p}\right) = (-1)^{\frac{p-1}{2}\cdot\frac{q-1}{2}}$: the two answers agree unless both primes are $\equiv 3 \pmod 4$, in which case they are opposite. With the two supplements for $-1$ and $2$, it lets one evaluate any Legendre symbol by repeated reduction and swapping, as in the Euclidean algorithm, without factoring the modulus. Euler and Legendre stated it; Gauss gave the first complete proof in 1796 and published it in 1801.

## Statement

**Theorem (quadratic reciprocity).** Let $p$ and $q$ be distinct odd primes. Then

$$\left(\frac{p}{q}\right)\left(\frac{q}{p}\right) = (-1)^{\frac{p-1}{2}\cdot\frac{q-1}{2}}.$$

Equivalently, $\left(\frac{p}{q}\right) = \left(\frac{q}{p}\right)$ if $p \equiv 1$ or $q \equiv 1 \pmod 4$, and $\left(\frac{p}{q}\right) = -\left(\frac{q}{p}\right)$ if $p \equiv q \equiv 3 \pmod 4$.

**Supplements.** For an odd prime $p$,

$$\left(\frac{-1}{p}\right) = (-1)^{\frac{p-1}{2}}, \qquad \left(\frac{2}{p}\right) = (-1)^{\frac{p^2-1}{8}}.$$

So $-1$ is a square modulo $p$ exactly when $p \equiv 1 \pmod 4$, and $2$ exactly when $p \equiv \pm 1 \pmod 8$.

**Examples.** Both 7 and 11 are $\equiv 3 \pmod 4$, so the symbols are opposite: $(11/7) = (4/7) = 1$ and $(7/11) = -1$, since the squares modulo 11 are $1, 3, 4, 5, 9$.

Is 713 a square modulo the prime 1009? Since $713 = 23 \cdot 31$ and $1009 \equiv 1 \pmod 4$,

- $(23/1009) = (1009/23) = (20/23) = (4/23)(5/23) = (5/23) = (23/5) = (3/5) = -1$;
- $(31/1009) = (1009/31) = (17/31) = (31/17) = (14/17) = (2/17)(7/17) = (7/17) = (17/7) = (3/7) = -1$, using $(2/17) = 1$ since $17 \equiv 1 \pmod 8$, and $(3/7) = -(7/3) = -(1/3) = -1$.

So $(713/1009) = (-1)(-1) = 1$, and $x^2 \equiv 713 \pmod{1009}$ has two solutions. Euler's criterion, $713^{504} \equiv 1 \pmod{1009}$, agrees.

Is 1001 a square modulo the prime 9907? Here $1001 = 7 \cdot 11 \cdot 13$ and $9907 \equiv 3 \pmod 4$, $9907 \equiv 3 \pmod 8$: $(7/9907) = -(9907/7) = -(2/7) = -1$, $(11/9907) = -(9907/11) = -(7/11) = 1$ and $(13/9907) = (9907/13) = (1/13) = 1$. So $(1001/9907) = -1$, and there is no solution.

## In plain words

Take two different odd primes. You can ask whether the first is a perfect square on a clock the size of the second, and the other way round. The law says the two answers are always the same, with one exception. When both primes leave remainder three after division by four, the answers are always opposite. Two extra rules handle minus one and two. Together they let you answer "is this a square on this clock?" by swapping and shrinking numbers, the way Euclid's method shrinks a pair of numbers to find their common divisor.

## Proof

The proof below is Eisenstein's version of Gauss's third proof. Fix an odd prime $p$ and write $h = (p - 1)/2$ and $S = \{1, \ldots, h\}$. We use [Euler's criterion](/euler-criterion/): $(a/p) \equiv a^h \pmod p$ for $p \nmid a$.

**Lemma 1 ([Gauss's lemma](/gauss-lemma/)).** Let $p \nmid a$. For $k \in S$ let $r_k$ be the least positive residue of $ka$ modulo $p$, and let $\mu$ be the number of $k \in S$ with $r_k > p/2$. Then $(a/p) = (-1)^\mu$.

*Proof.* Let $s_k = r_k$ if $r_k < p/2$ and $s_k = p - r_k$ otherwise, so $s_k \in S$ and $ka \equiv \pm s_k \pmod p$, with the minus sign exactly $\mu$ times. The $s_k$ are distinct: if $s_j = s_k$, then $ja \equiv \pm ka$, so $j \equiv \pm k \pmod p$ because $a$ is invertible; $j \equiv -k$ is impossible because $2 \le j + k \le p - 1$, so $j = k$. Hence $\{s_k : k \in S\} = S$. Multiplying the congruences $ka \equiv \pm s_k$ over $k \in S$ gives

$$a^h \cdot h! \equiv (-1)^\mu \cdot h! \pmod p.$$

Since $p \nmid h!$, $a^h \equiv (-1)^\mu$, and Euler's criterion gives $(a/p) = (-1)^\mu$. $\square$

**The second supplement.** For $a = 2$, $r_k = 2k$ for every $k \in S$, and $2k > p/2$ exactly when $k > p/4$. So $\mu = h - \lfloor p/4 \rfloor$. Checking the four cases $p = 8m + 1, 8m + 3, 8m + 5, 8m + 7$ gives $\mu = 2m, 2m + 1, 2m + 1, 2m + 2$, so $\mu$ is even exactly when $p \equiv \pm 1 \pmod 8$, which matches $(-1)^{(p^2-1)/8}$.

**The first supplement.** By Euler's criterion $(-1/p) \equiv (-1)^h$, and both sides are $\pm 1$ with $p > 2$, so they are equal.

**Lemma 2 (Eisenstein).** If $a$ is odd and $p \nmid a$, then $\mu \equiv T(a, p) \pmod 2$, where $T(a, p) = \sum_{k=1}^{h} \lfloor ka/p \rfloor$.

*Proof.* Divide: $ka = p \lfloor ka/p \rfloor + r_k$. Summing over $k \in S$,

$$a \sum_{k \in S} k = p\, T(a, p) + \sum_{r_k < p/2} r_k + \sum_{r_k > p/2} r_k.$$

Since $\{s_k\} = S$,

$$\sum_{k \in S} k = \sum_{r_k < p/2} r_k + \sum_{r_k > p/2} (p - r_k) = \sum_{r_k < p/2} r_k + \mu p - \sum_{r_k > p/2} r_k.$$

Subtracting, $(a - 1) \sum_{k \in S} k = p\,(T(a, p) - \mu) + 2 \sum_{r_k > p/2} r_k$. Reduce modulo 2: $a - 1$ is even and $p$ is odd, so $T(a, p) - \mu$ is even. $\square$

**Lemma 3 (lattice count).** For distinct odd primes $p$ and $q$,

$$T(q, p) + T(p, q) = \frac{p - 1}{2} \cdot \frac{q - 1}{2}.$$

*Proof.* Let $R$ be the set of lattice points $(x, y)$ with $1 \le x \le (p - 1)/2$ and $1 \le y \le (q - 1)/2$; it has $\frac{p-1}{2} \cdot \frac{q-1}{2}$ points. No point of $R$ lies on the line $qx = py$, since that would force $p \mid x$ with $0 < x < p$. Count the points of $R$ below the line, with $y < qx/p$. For a fixed $x$, the admissible $y$ are $1, \ldots, \lfloor qx/p \rfloor$; all of them satisfy $y \le (q - 1)/2$, because $qx/p < q/2$. So there are $\sum_x \lfloor qx/p \rfloor = T(q, p)$ points below the line. By the same argument with the roles of the axes exchanged, there are $T(p, q)$ points above it. $\square$

**Proof of the theorem.** By Lemma 1 and Lemma 2, applied with $a = q$ modulo $p$ and with $a = p$ modulo $q$ (both odd), $(q/p) = (-1)^{T(q, p)}$ and $(p/q) = (-1)^{T(p, q)}$. Multiplying and applying Lemma 3,

$$\left(\frac{p}{q}\right)\left(\frac{q}{p}\right) = (-1)^{T(q, p) + T(p, q)} = (-1)^{\frac{p-1}{2}\cdot\frac{q-1}{2}}. \qquad \blacksquare$$

For example, with $p = 7$ and $q = 11$: $T(11, 7) = 1 + 3 + 4 = 8$ and $T(7, 11) = 0 + 1 + 1 + 2 + 3 = 7$, and $8 + 7 = 15 = 3 \cdot 5$ is odd, so the product of the symbols is $-1$.

## Consequences

- **Computing Legendre and Jacobi symbols.** The law extends to the [Jacobi symbol](/jacobi-symbol/): for odd coprime $m, n > 0$, $(m/n)(n/m) = (-1)^{\frac{m-1}{2}\cdot\frac{n-1}{2}}$, and the supplements hold too. So $(a/n)$ can be computed by reducing $a$ modulo $n$, removing factors 2 and swapping, with no factoring, in $O(k^2)$ bit operations for $k$-digit inputs (HAC, Algorithm 2.149). This is the symbol used by the [Solovay-Strassen test](/solovay-strassen/).
- **Which primes have $a$ as a square.** For a fixed $a$, the value $(a/p)$ depends only on $p$ modulo $4|a|$. For example, $(3/p) = 1$ exactly for $p \equiv \pm 1 \pmod{12}$, $(5/p) = 1$ exactly for $p \equiv \pm 1 \pmod 5$, and $(-3/p) = 1$ exactly for $p \equiv 1 \pmod 3$.
- **Prime factors of special numbers.** If $q \equiv 3 \pmod 4$ and $p = 2q + 1$ is prime, then $p \equiv 7 \pmod 8$, so $(2/p) = 1$ and $2^q = 2^{(p-1)/2} \equiv 1 \pmod p$. So $p$ divides the Mersenne number $2^q - 1$: for example $23 \mid 2^{11} - 1 = 2047$. In the same way every prime factor of $n^2 + 1$ is 2 or $\equiv 1 \pmod 4$, which gives infinitely many primes $\equiv 1 \pmod 4$.
- **Pépin's test.** For a Fermat number $F = 2^{2^m} + 1 > 5$ that is prime, $(3/F) = (F/3) = (2/3) = -1$. So $F$ is prime if and only if $3^{(F-1)/2} \equiv -1 \pmod F$; the converse direction follows from the [order](/multiplicative-order/) of 3. For $F = 65537$, $3^{32768} \equiv -1$.
- **Sums of two squares and quadratic forms.** The first supplement gives a square root of $-1$ modulo $p \equiv 1 \pmod 4$, the start of Fermat's two-squares theorem. More generally, reciprocity decides which primes are represented by binary quadratic forms of a given discriminant.

## Tightness

The sign cannot be dropped: $(3/7) = -1$ while $(7/3) = (1/3) = 1$, and both primes are $\equiv 3 \pmod 4$. The primes must be odd, since for $2$ the second supplement takes the place of the law, and distinct, since $(p/p) = 0$.

The law does not say that $(a/n) = 1$ makes $a$ a square when $n$ is composite. For the Jacobi symbol, $(2/15) = (2/3)(2/5) = (-1)(-1) = 1$, but 2 is not a square modulo 15. The Jacobi version of the law holds anyway; the Kronecker symbol extends it to even moduli with extra sign rules.

Higher powers need their own laws. Cubic reciprocity (Jacobi and Eisenstein) works in $\mathbb{Z}[\omega]$ with $\omega^3 = 1$, biquadratic reciprocity (Gauss and Eisenstein) in $\mathbb{Z}[i]$, and Artin's reciprocity law of 1927 contains all of them as the central statement of class field theory.

## History

Euler found the law by computation and stated it in equivalent forms in the 1740s and in a paper published in 1783. Legendre stated it in the symmetric form in 1785 and introduced his symbol in his Essai sur la théorie des nombres of 1798, but his proof assumed unproved facts, such as the existence of suitable primes in arithmetic progressions. Gauss, who called it the fundamental theorem, found the first complete proof in 1796, at age 18, and published it by induction in the Disquisitiones Arithmeticae of 1801. He gave eight proofs over his life, using induction, binary quadratic forms, Gauss's lemma and Gauss sums. Eisenstein's lattice-point proof of 1844 simplified the third one and is the one given above. Zolotarev (1872) proved it by the signs of permutations. Hundreds of proofs are now known.

## References
