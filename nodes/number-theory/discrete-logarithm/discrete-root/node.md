---
tag: J18RAX
kind: problem
slug: discrete-root
name: Discrete root
area: number-theory/discrete-logarithm
level: core
summary: Given a, k and a prime p, find all x with x^k congruent to a modulo p. A primitive root and one discrete logarithm reduce it to a linear congruence modulo p - 1.
prereqs: [discrete-logarithm-problem, primitive-root, linear-congruence]
see_also: [modular-square-root, tonelli-shanks, cipolla-algorithm, euler-criterion, baby-step-giant-step, pohlig-hellman, polynomial-factorization-over-finite-fields, primitive-roots-existence]
sources:
  - url: https://cp-algorithms.com/algebra/discrete-root.html
    locator: cp-algorithms, Discrete root (the reduction to a discrete logarithm and a linear congruence, and the formula for all solutions)
  - book: isbn:9780849385230
    title: Alfred J. Menezes, Paul C. van Oorschot and Scott A. Vanstone, Handbook of Applied Cryptography, CRC Press, 1996
    locator: Chapter 3, Section 3.5.1, square roots modulo a prime (Algorithms 3.34, 3.36, 3.37 and 3.39); Section 3.6, Definition 3.48 and Fact 3.50 (rules for logarithms)
  - paper: doi:10.1109/sfcs.1977.18
    title: Leonard Adleman, Kenneth Manders and Gary Miller, On taking roots in finite fields, 18th Annual Symposium on Foundations of Computer Science, 1977
    locator: pages 175 to 178 (r-th roots in a finite field without a discrete logarithm, the generalization of the Tonelli-Shanks method)
---

The discrete root problem asks, given a prime $p$, an integer $k \ge 1$ and a residue $a$, for all $x$ with $x^k \equiv a \pmod p$. It is the inverse of the problem solved by the [discrete logarithm](/discrete-logarithm-problem/): there the exponent is unknown, here the base is. With a [primitive root](/primitive-root/) $g$ modulo $p$, writing $x = g^y$ and $a = g^A$ turns the equation into the [linear congruence](/linear-congruence/) $k y \equiv A \pmod{p - 1}$, which has either no solution or exactly $\gcd(k, p - 1)$ of them.

## In plain words

You know the result of raising some unknown number to a known power, and you want the number back. Over ordinary numbers this is taking a root. In clock arithmetic modulo a prime the same question can have no answer, one answer or several answers.

The trick is to rename every nonzero number by its position in the cycle of powers of one fixed element that runs through all of them. Under this renaming, raising to a power becomes multiplying the position, so the root problem becomes a division problem on positions, which is easy. The hard part is the renaming itself, which is a discrete logarithm. When the power shares no factor with the length of the cycle, the renaming is not needed: one more power undoes the first.

## Definition

**Input.** A prime $p$, an integer $k \ge 1$ and an integer $a$ with $0 \le a < p$.

**Output.** The set

$$R(a) = \{\, x \in \{0, \dots, p - 1\} : x^k \equiv a \pmod p \,\},$$

possibly empty.

If $a = 0$ then $R(a) = \{0\}$, because $\mathbb{Z}/p\mathbb{Z}$ is a field. For $a \ne 0$, every solution is nonzero and lies in the group $(\mathbb{Z}/p\mathbb{Z})^*$, which is cyclic of order $p - 1$ by the [existence of primitive roots](/primitive-roots-existence/). Fix a primitive root $g$, let $A = \log_g a$ and $d = \gcd(k, p - 1)$. Then $x = g^y$ solves the problem exactly when

$$k y \equiv A \pmod{p - 1}.$$

This congruence has a solution exactly when $d \mid A$, and then it has $d$ solutions modulo $p - 1$, namely $y_0 + j (p - 1)/d$ for $j = 0, \dots, d - 1$, where $y_0$ is any one solution. So

$$R(a) = \{\, x_0 \zeta^j : 0 \le j < d \,\}, \qquad x_0 = g^{y_0},\ \zeta = g^{(p-1)/d},$$

and $\zeta$ is a primitive $d$-th root of unity. In particular, $a \ne 0$ is a $k$-th power exactly when

$$a^{(p-1)/d} \equiv 1 \pmod p,$$

the generalization of [Euler's criterion](/euler-criterion/), which can be tested with one [modular exponentiation](/modular-exponentiation/) and no logarithm.

**Cost model.** Arithmetic is on residues of $O(\log p)$ bits; one multiplication modulo $p$ costs $O(\log^2 p)$ bit operations with schoolbook arithmetic. The output can have up to $p - 1$ elements, so the cost is measured in the input size $\log p + \log k$ and the output size $d$.

## Variants

- **Square roots.** $k = 2$: the [modular square root](/modular-square-root/). There are two roots of a [quadratic residue](/quadratic-residue/), found by [Tonelli-Shanks](/tonelli-shanks/) or [Cipolla](/cipolla-algorithm/) in randomized polynomial time without any discrete logarithm.
- **One root only.** Find a single $x$, or decide that none exists. All other roots are $x \zeta^j$.
- **Exponent coprime to $p - 1$.** If $d = 1$, the map $x \mapsto x^k$ is a bijection and its inverse is $x \mapsto x^{u}$ with $u = k^{-1} \bmod (p - 1)$, one exponentiation. This is the decryption step of RSA, done modulo each prime factor.
- **Composite modulus.** For $n = \prod p_i^{e_i}$, solve modulo each prime power and combine with the [Chinese remainder theorem](/chinese-remainder-theorem/). Modulo $p^e$ with $p$ odd the group of units is again cyclic, of order $p^{e-1}(p-1)$, so the same reduction applies; Hensel lifting is an alternative when $p \nmid k$.
- **Finite fields.** In $\mathbb{F}_q$ the same reasoning holds with $q - 1$ in place of $p - 1$.
- **Decision version.** Is $a$ a $k$-th power residue? Answered by the criterion $a^{(p-1)/d} \equiv 1$.

## Examples

Let $p = 23$ and $g = 5$; the table of powers of $5$ is in the [discrete logarithm](/discrete-logarithm-problem/) page.

- $x^4 \equiv 9$. Here $d = \gcd(4, 22) = 2$ and $9^{11} \equiv 1$, so there are two roots. From $\log_5 9 = 10$ the congruence $4 y \equiv 10 \pmod{22}$ gives $2 y \equiv 5 \pmod{11}$, so $y \equiv 8 \pmod{11}$, $y \in \{8, 19\}$, and $x \in \{5^8, 5^{19}\} = \{16, 7\}$. Indeed $16^2 \equiv 3$ and $3^2 = 9$, and $7^2 \equiv 3$ as well.
- $x^4 \equiv 5$. Here $5^{11} \equiv 22 \equiv -1$, so $5$ is not a square and certainly not a fourth power: no solution. In logarithms, $\log_5 5 = 1$ is odd and $4 y \equiv 1 \pmod{22}$ is impossible.
- $x^3 \equiv 10$. Here $d = 1$, so the root is unique: $u = 3^{-1} \bmod 22 = 15$ and $x = 10^{15} \bmod 23 = 5$. Check: $5^3 = 125 = 5 \cdot 23 + 10$.
- $x^{11} \equiv 1$. Here $d = 11$, and the roots are the $11$ powers of $\zeta = 5^2 = 2$: the subgroup $\{1, 2, 3, 4, 6, 8, 9, 12, 13, 16, 18\}$.
- $x^k \equiv 0$ has the single root $0$ for every $k$.

## Known algorithms

- **Via a discrete logarithm.** Find a primitive root $g$ (needs the factorization of $p - 1$), compute $A = \log_g a$ with [baby-step giant-step](/baby-step-giant-step/), [Pohlig-Hellman](/pohlig-hellman/) or [index calculus](/index-calculus/), solve $k y \equiv A$ with the [extended Euclidean algorithm](/extended-euclidean-algorithm/), and list the $d$ roots. The cost is that of one discrete logarithm plus $O(\log p + d)$ multiplications. This is the method of the cp-algorithms page.
- **Without a logarithm.** Write $k = k_1 k_2$ where $k_2$ is coprime to $p - 1$ and every prime factor of $k_1$ divides $p - 1$. The $k_2$-th root is one exponentiation, as above. For a prime $r \mid p - 1$, the algorithm of Adleman, Manders and Miller (1977) takes $r$-th roots in the style of Tonelli-Shanks, working in the Sylow $r$-subgroup; its cost grows with $r$, since it solves small discrete logarithms in a subgroup of order $r$. Repeating it for each prime factor of $k_1$ gives one root, and the others follow by multiplying with roots of unity.
- **Via polynomial factorization.** The roots are the roots in $\mathbb{F}_p$ of $\gcd(X^k - a, X^p - X)$, and the [factorization of polynomials over finite fields](/polynomial-factorization-over-finite-fields/), for example [Cantor-Zassenhaus](/cantor-zassenhaus-algorithm/), finds them in expected time polynomial in $k$ and $\log p$.
- **Exhaustive search.** Test all $x$: $O(p)$ exponentiations.

## Bounds

For a fixed $k$, all roots are found in randomized time polynomial in $\log p$, by either of the last two methods. When $k$ is large and $d = \gcd(k, p - 1)$ has a large prime factor $r$, the methods above either cost a power of $r$ or need a discrete logarithm in a group of order divisible by $r$; no algorithm polynomial in $\log p$ and $\log k$ is known in general. The output can have $d$ elements, so $\Omega(d)$ is a lower bound for listing them.

## Reductions

- **To the discrete logarithm.** As in the Definition: one logarithm to a primitive root, one linear congruence and $d$ multiplications.
- **To square roots and coprime powers.** When $k$ is a power of $2$ times a number coprime to $p - 1$, repeated square roots and one exponentiation suffice.
- **Root of unity.** Listing all roots needs only one root and a primitive $d$-th root of unity $\zeta$, which is $g^{(p-1)/d}$ for any primitive root $g$, or $c^{(p-1)/d}$ for any $c$ whose power $c^{(p-1)/r} \ne 1$ for every prime $r \mid d$.

## Applications

- **RSA.** Decryption is a $k$-th root modulo $N = p q$ with $\gcd(k, \varphi(N)) = 1$, computed as one exponentiation once the factorization is known.
- **Rabin cryptosystem.** Decryption is a square root modulo $N = p q$, with four roots that the receiver must choose from.
- **Roots of unity.** Number theoretic transforms need a primitive $d$-th root of unity modulo a prime with $d \mid p - 1$, a special case of this problem.
- **Power residue symbols.** The criterion $a^{(p-1)/d} \equiv 1$ decides $k$-th power residuosity, used in higher reciprocity and in some cryptosystems based on residuosity.

## References
