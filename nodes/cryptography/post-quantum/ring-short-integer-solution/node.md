---
tag: NX628Q
kind: problem
slug: ring-short-integer-solution
name: Ring short integer solution problem
aliases:
- Ring-SIS
area: cryptography/post-quantum
level: advanced
summary: SIS over a polynomial ring. Given a_1..a_m in Z_q[x]/(f), find short nonzero z_i with sum a_i z_i = 0. Hard for f = x^n + 1, easy for x^n - 1. Basis of SWIFFT.
prereqs: [short-integer-solution, polynomial-ring]
see_also: [module-short-integer-solution, ring-learning-with-errors, collision-resistance, number-theoretic-transform, fiat-shamir-with-aborts, lattice-based-cryptography, falcon, crystals-dilithium]
sources:
  - paper: "Daniele Micciancio, Generalized compact knapsacks, cyclic lattices, and efficient one-way functions, Computational Complexity 16(4), 2007 (FOCS 2002)"
    locator: the compact knapsack function over Z_q[x]/(x^n - 1) and its one-wayness from worst-case problems on cyclic lattices
  - paper: "Vadim Lyubashevsky and Daniele Micciancio, Generalized compact knapsacks are collision resistant, ICALP 2006, LNCS 4052"
    locator: the collision attack for x^n - 1, the expansion factor, and collision resistance for irreducible f such as x^n + 1 from worst-case problems on ideal lattices
  - paper: "Chris Peikert and Alon Rosen, Efficient collision-resistant hashing from worst-case assumptions on cyclic lattices, TCC 2006, LNCS 3876"
    locator: collision resistance from worst-case problems on cyclic lattices, with the input domain restricted to avoid the factor x - 1
  - paper: "Vadim Lyubashevsky, Daniele Micciancio, Chris Peikert and Alon Rosen, SWIFFT, a modest proposal for FFT hashing, FSE 2008, LNCS 5086"
    locator: the SWIFFT function over Z_257[x]/(x^64 + 1) with m = 16 and binary inputs, and its FFT evaluation
---

The ring short integer solution problem (Ring-SIS) is the [short integer solution problem](/short-integer-solution/) with a matrix that has the structure of a polynomial ring. Given $m$ random polynomials $a_1, \ldots, a_m$ in $R_q = \mathbb{Z}_q[x]/(f)$, find short polynomials $z_1, \ldots, z_m$, not all zero, with $\sum_i a_i z_i = 0$. The key is $m$ polynomials instead of an $n \times mn$ matrix, and the products cost $O(n \log n)$ with the [number-theoretic transform](/number-theoretic-transform/). The choice of $f$ matters: for $f = x^n - 1$ the problem is easy, for $f = x^n + 1$ with $n$ a power of 2 it is as hard as worst-case problems on ideal lattices.

**Notation.** $n$ is the degree of $f$, $q$ the modulus (not a number of queries), $m$ the number of ring elements in the key, and $\beta$ the bound on the solution. $R = \mathbb{Z}[x]/(f)$ and $R_q = R/qR$. For $a \in R$, $\|a\|$ is the Euclidean norm and $\|a\|_\infty$ the largest absolute value of the coefficients. $a(1)$ is the value of $a$ at $x = 1$. $u = 1 + x + \cdots + x^{n-1}$. $\lambda$ is the security parameter.

## In plain words

The plain problem gives a large random table of numbers and asks for a small combination of its columns that adds up to zero. The ring version builds the table from a few short rows by shifting each row again and again, so the table is much smaller to store and much faster to use.

The way the rows wrap around when they are shifted decides if the problem stays hard. If a row wraps around unchanged, there is a shortcut: a special input that makes every row act like a single number, and then a zero sum is easy to find. If the wrapped value changes its sign, the shortcut goes away and no fast method is known.

## Definition

Fix a monic polynomial $f$ of degree $n$, a modulus $q$, a count $m$ and a bound $\beta$.

**Ring-SIS$_{q,m,\beta}$ over $R$.** Given $a_1, \ldots, a_m$ drawn uniformly from $R_q$, find $z_1, \ldots, z_m \in R$, not all zero, with

$$\sum_{i=1}^{m} a_i z_i \equiv 0 \pmod{q} \quad\text{and}\quad \|(z_1, \ldots, z_m)\| \le \beta.$$

Many uses take the infinity norm instead, with $z_i$ having coefficients in $\{-1, 0, 1\}$.

**As SIS.** Multiplication by $a$ in $R_q$ is a linear map. Its matrix $\mathrm{Rot}(a)$ has column $j$ equal to the coefficients of $x^j a \bmod f$. Ring-SIS is SIS with the $n \times mn$ matrix $[\mathrm{Rot}(a_1) \mid \cdots \mid \mathrm{Rot}(a_m)]$. For $f = x^n - 1$ this matrix is a row of circulant blocks; for $f = x^n + 1$ a row of negacyclic blocks, where the wrapped entries change sign.

**The hash function.** The key $(a_1, \ldots, a_m)$ defines $h(z_1, \ldots, z_m) = \sum_i a_i z_i \in R_q$ on inputs with small coefficients. A collision $h(z) = h(z')$ with $z \ne z'$ gives the Ring-SIS solution $z - z'$, with coefficients in $\{-1, 0, 1\}$ for binary inputs.

## Variants

- **Choice of ring.** Lyubashevsky and Micciancio prove hardness for any monic $f$ that is irreducible over $\mathbb{Z}$ and has a small expansion factor, a measure of how much reduction mod $f$ can increase the norm of a product. $x^n + 1$ with $n$ a power of 2 has expansion factor 2 and is the usual choice. Other cyclotomic polynomials, such as $1 + x + \cdots + x^{p-1}$ for prime $p$, also work.
- **Module-SIS.** A small matrix of ring elements instead of one row; see [Module-SIS](/module-short-integer-solution/).
- **Inhomogeneous Ring-SIS.** Find short $z$ with $\sum_i a_i z_i = t$ for a given target $t$, as in hash-and-sign signatures over rings and [Falcon](/falcon/).

## Examples

**The collision for $x^n - 1$.** Over $\mathbb{Z}_q[x]/(x^n - 1)$, $x \cdot u = x + x^2 + \cdots + x^n = u$, because $x^n = 1$. So $x^j u = u$ for every $j$, and for every $a$,

$$a \cdot u = a(1)\, u.$$

Take $n = 4$, $q = 17$, $a_1 = 1 + 2x + 3x^3$, $a_2 = 5 + x + 4x^2 + 2x^3$ and $a_3 = 2 + 7x + x^2 + x^3$. Then $a_1(1) = 6$ and $a_3(1) = 11$, so

$$a_1 u + a_3 u = (6 + 11)(1 + x + x^2 + x^3) = 17 u \equiv 0 \pmod{17}.$$

$z = (u, 0, u)$ is a Ring-SIS solution with eight coefficients equal to 1, so $\|z\| = \sqrt{8}$, for any choice of $a_2$.

**The same input for $x^n + 1$.** In $\mathbb{Z}_{17}[x]/(x^4 + 1)$, $x^4 = -1$, and the same products are $a_1 u = 13 + 6x^3$ and $a_3 u = 10 + 7x + 9x^2 + 11x^3$. Their sum is $6 + 7x + 9x^2$, which is not zero: $u$ is not a common eigenvector there.

**The general attack.** Pick bits $c_1, \ldots, c_m$ and set $z_i = c_i u$. Then $h(z) = \bigl(\sum_i c_i a_i(1)\bigr) u$, which takes only $q$ values. Two bit vectors $c \ne c'$ with $\sum_i c_i a_i(1) \equiv \sum_i c'_i a_i(1) \pmod q$ give a collision. This is a subset sum problem mod $q$ in $m$ numbers, and a birthday search over random bit vectors finds a collision in about $\sqrt{q}$ tries once $2^m$ is well above $q$. For the SWIFFT sizes $n = 64$, $m = 16$, $q = 257$, but with $x^{64} - 1$ in place of $x^{64} + 1$, the search needs about 20 tries. The code with this page runs this attack, checks that the difference is a solution with coefficients in $\{-1, 0, 1\}$, and checks that the same two inputs do not collide over $x^{64} + 1$.

**Non-example.** A solution with $\|z\| \ge q$ is always easy: $z = (q, 0, \ldots, 0)$. Bounds of interest have $\beta$ well below $q$.

## Known algorithms

- **Lattice reduction.** As SIS in dimension $mn$: run [BKZ](/bkz-algorithm/) on the $q$-ary lattice of the rotation matrix. For $f = x^n + 1$ no known attack gains more than small polynomial factors from the ring structure; the rotations $x^j z$ of a solution are also solutions, which saves at most a factor near $n$ in some sieving algorithms.
- **Birthday search.** Hash random binary inputs until two collide; the cost is about $q^{n/2}$ evaluations, as for SIS.
- **Factor attacks.** When $f$ has a factor $g$ of low degree over $\mathbb{Z}$, solving the problem modulo $g$ and lifting the solution through the cofactor $f/g$ gives a short solution, as for $g = x - 1$ above. This is why the hardness results need $f$ irreducible over $\mathbb{Z}$.

The Python code with this page computes the ring hash for $x^n \pm 1$, runs the $x^n - 1$ collision attack and a birthday search on tiny parameters, and checks the link with the rotation matrix. It is for study only, uses toy parameters, and is not constant time. For hashing use SHA-2 or SHA-3 from a standard library or a FIPS 140 validated module.

## Bounds

- **Worst-case hardness.** Lyubashevsky and Micciancio (2006) prove that for irreducible $f$ with a small expansion factor, a large enough $m$ and a large enough polynomial $q$, solving Ring-SIS on average is at least as hard as approximating SVP to within a polynomial factor in the worst case on ideal lattices of $R$. Peikert and Rosen (2006) prove a similar result for cyclic lattices with the input domain restricted to avoid the factor $x - 1$.
- **One-wayness without collision resistance.** Micciancio (2002) proved that the function over $x^n - 1$ is one-way, based on worst-case problems on cyclic lattices. The attack above shows that it is not collision resistant.
- **Existence.** If $2^m > q$, there are more binary inputs ($2^{mn}$) than outputs ($q^n$), so two inputs collide and a solution with coefficients in $\{-1, 0, 1\}$ and norm at most $\sqrt{mn}$ exists. The problem is meaningful for $\sqrt{mn} \le \beta < q$.

## Reductions

- **To SIS.** Ring-SIS is SIS with the matrix $[\mathrm{Rot}(a_1) \mid \cdots \mid \mathrm{Rot}(a_m)]$.
- **From ideal-lattice problems.** As in the Bounds section. Ideal lattices are a smaller class than all lattices, so this is a weaker basis than the one for SIS; see [Ring-LWE hardness](/ring-lwe-hardness/) for the known attacks on ideal lattices, which do not apply to Ring-SIS with these parameters.
- **To and from Module-SIS.** Module-SIS of rank 1 is Ring-SIS; see [Module-SIS](/module-short-integer-solution/).

## Applications

- **SWIFFT.** Lyubashevsky, Micciancio, Peikert and Rosen (2008) take $R_{257} = \mathbb{Z}_{257}[x]/(x^{64} + 1)$, $m = 16$ and binary $z_i$. The function compresses 1024 input bits to 64 elements of $\mathbb{Z}_{257}$. Because $257 \equiv 1 \pmod{128}$, $x^{64} + 1$ splits into linear factors mod 257, and each product is an FFT of length 64 followed by pointwise products. Its collision resistance is backed by the worst-case result, but its pseudorandomness is not, so it is not a drop-in replacement for SHA-2.
- **Signatures.** Lyubashevsky's one-time and Fiat-Shamir signatures over rings rest on Ring-SIS; see [Fiat-Shamir with aborts](/fiat-shamir-with-aborts/). ML-DSA ([CRYSTALS-Dilithium](/crystals-dilithium/)) uses the module form.
- **Commitments.** $\sum_i a_i z_i$ with a short random part of $z$ is a binding commitment under Ring-SIS.

## References
