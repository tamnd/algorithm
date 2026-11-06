---
tag: 6Z0RA0
kind: problem
slug: modular-exponentiation
name: Modular exponentiation
aliases:
- computing a^b mod n
area: number-theory/modular-arithmetic
level: intro
summary: Compute a^b mod n efficiently for large b.
prereqs: [congruence, division-with-remainder]
see_also: [binary-exponentiation, sliding-window-exponentiation, addition-chain, montgomery-multiplication, modular-multiplication, euler-theorem, discrete-logarithm-problem, rsa-cryptosystem]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 31.6, Powers of an element (repeated squaring and the procedure MODULAR-EXPONENTIATION)
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, third edition
    locator: Section 4.6.3, Evaluation of Powers (the binary method, addition chains, the bounds of Brauer and Erdős, and the lower bound lg n)
  - book: isbn:9780849385230
    title: Alfred J. Menezes, Paul C. van Oorschot and Scott A. Vanstone, Handbook of Applied Cryptography, CRC Press, 1997
    locator: Section 14.6, Exponentiation (Algorithms 14.76 and 14.79, binary exponentiation; 14.85, sliding windows; 14.94, Montgomery exponentiation)
  - book: isbn:9780521194693
    title: Richard P. Brent and Paul Zimmermann, Modern Computer Arithmetic, Cambridge University Press, 2010
    locator: Section 2.6, Modular exponentiation
---

Modular exponentiation is the problem of computing $a^b \bmod n$, the remainder of the power $a^b$ after division by $n$, for integers $a$, $b \ge 0$ and $n \ge 1$. The exponent $b$ is often hundreds or thousands of binary digits long, so neither $b$ multiplications nor the number $a^b$ itself fit in any computer. The problem is solved with about $2 \lg b$ [modular multiplications](/modular-multiplication/) by [binary exponentiation](/binary-exponentiation/), because a remainder can be taken after each product. It is the main operation of [RSA](/rsa-cryptosystem/), [Diffie-Hellman](/diffie-hellman/) and the [Miller-Rabin](/miller-rabin/) test.

## In plain words

You must find the remainder of a huge power: a base multiplied by itself a very large number of times, then divided by a modulus. Two facts make this easy. First, you may take the remainder after every multiplication, so the numbers you keep never grow past the modulus. Second, you do not need to multiply one step at a time: squaring a power doubles its exponent, so a few dozen squarings reach exponents with many digits. Combining squares that match the binary digits of the exponent gives the answer with a number of multiplications that grows with the number of digits of the exponent, not with the exponent itself.

## Definition

**Input.** Integers $a$, $b$ and $n$ with $b \ge 0$ and $n \ge 1$. The base $a$ may be any integer; reducing it first gives $0 \le a < n$ without changing the answer.

**Output.** The unique integer $r$ with $0 \le r < n$ and $r \equiv a^b \pmod n$, written $a^b \bmod n$. The convention $a^0 = 1$ holds for every $a$, including $a = 0$, so $0^0 \bmod n = 1 \bmod n$. For $n = 1$ every answer is $0$.

**Residues.** The residues modulo $n$ are represented by the integers $0, 1, \ldots, n - 1$, the least non-negative representatives of the [congruence](/congruence/) classes.

**Cost models.** A bound must say which of these it uses.

- **Word-sized modulus.** On the [word RAM](/word-ram/) with $n < 2^w$, an addition, a comparison or a [division with remainder](/division-with-remainder/) of word-sized numbers costs one unit. The product of two residues has up to $2w$ binary digits, so a product modulo $n$ costs $O(1)$ only if the machine gives the double-width product or a [modular multiplication](/modular-multiplication/) routine is used. The exponent $b$ may be a word or a longer number; its length $\lambda(b) + 1$, with $\lambda(b) = \lfloor \lg b \rfloor$, enters the bounds.
- **Arbitrary precision.** The modulus has $k$ binary digits and the exponent has $e$ binary digits. The cost is counted in bit operations, and $M(k)$ is the cost of a product of two $k$-digit integers: $O(k^2)$ by [schoolbook multiplication](/schoolbook-multiplication/), $O(k^{1.585})$ by [Karatsuba](/karatsuba-multiplication/), $O(k \log k)$ by Harvey and van der Hoeven. A reduction modulo $n$ of a $2k$-digit number costs $O(M(k))$ with [Barrett reduction](/barrett-reduction/) or [Montgomery multiplication](/montgomery-multiplication/).
- **Multiplication count.** Many results count only the multiplications of residues, squarings included, and ignore the rest. This model works in any group or monoid, not only modulo $n$.

## Variants

- **Negative exponent.** $a^{-b} \bmod n$ means $(a^{-1})^b \bmod n$. It exists exactly when $\gcd(a, n) = 1$, and needs a [modular inverse](/modular-inverse/) first.
- **Fixed base.** The base $a$ and the modulus are fixed and many exponents arrive, as for a generator in [Diffie-Hellman](/diffie-hellman/). A table of $a^{2^i}$ or of larger windows, computed once, saves all squarings later.
- **Fixed exponent.** The exponent is fixed, as the public exponent $65537 = 2^{16} + 1$ of RSA. A short [addition chain](/addition-chain/) for $b$ can be found once in advance.
- **Multi-exponentiation.** Compute $a_1^{b_1} a_2^{b_2} \cdots a_t^{b_t} \bmod n$. One shared sequence of squarings (Shamir's trick) costs about as much as one exponentiation instead of $t$.
- **Exponent towers.** Compute $a^{b^c} \bmod n$ when $b^c$ is too large to write down. If $\gcd(a, n) = 1$, then $a^b \equiv a^{b \bmod \varphi(n)} \pmod n$ by [Euler's theorem](/euler-theorem/), and the [Carmichael function](/carmichael-function/) $\lambda(n)$ may replace the [totient](/euler-totient/) $\varphi(n)$. The exponent is then reduced recursively.
- **Other structures.** The same problem in another monoid: powers of a matrix ([matrix exponentiation](/matrix-exponentiation/)), of a polynomial modulo a polynomial, or of a point on an elliptic curve, where the "power" is a scalar multiple.
- **Constant time.** In cryptography the exponent is secret, and the sequence of operations and memory accesses must not depend on its digits. See [timing attack](/timing-attack/).

## Examples

| $a$ | $b$ | $n$ | $a^b \bmod n$ | notes |
| --- | --- | --- | --- | --- |
| 4 | 13 | 497 | 445 | $4^{13} = 67108864$ has 8 decimal digits |
| 3 | 200 | 13 | 9 | $3^3 = 27 \equiv 1$, and $200 = 3 \cdot 66 + 2$ |
| 2 | 10 | 1000 | 24 | the last three digits of $1024$ |
| 2 | 560 | 561 | 1 | $561 = 3 \cdot 11 \cdot 17$ is composite, a [Carmichael number](/carmichael-number/) |
| 7 | $10^{18}$ | $10^9 + 7$ | 259616729 | $10^{18}$ has 60 binary digits |
| 0 | 0 | 7 | 1 | the convention $0^0 = 1$ |
| 5 | 0 | 1 | 0 | every residue modulo 1 is 0 |

For $4^{13} \bmod 497$, the exponent is $13 = 1101_2$. Reading its digits from the left, square the running value and multiply by $4$ when the digit is 1: $1 \to 4$, then $4^2 \cdot 4 = 64$, then $64^2 = 4096 \equiv 120$, then $120^2 \cdot 4 = 57600 \equiv 445$. The values $4, 64, 120, 445$ are $4^1, 4^3, 4^6, 4^{13}$ modulo 497. This takes 3 squarings and 2 more multiplications, and no number ever exceeds $496^2 = 246016$.

For $7^{10^{18}} \bmod (10^9 + 7)$, the binary method uses 59 squarings and 23 more multiplications, since $10^{18}$ has 60 binary digits of which 24 are ones. Repeated multiplication would need $10^{18} - 1$ products.

## Known algorithms

- [Binary exponentiation](/binary-exponentiation/) (square and multiply), from the left or from the right: $\lambda(b)$ squarings and $\nu(b) - 1$ more multiplications, where $\nu(b)$ is the number of ones in the binary form of $b$. CLRS gives it as MODULAR-EXPONENTIATION.
- [Sliding-window exponentiation](/sliding-window-exponentiation/): processes several digits of $b$ at a time with a table of odd powers of $a$, for $\lambda(b) + O(\lambda(b) / \lg \lambda(b))$ multiplications.
- [Addition chain](/addition-chain/) exponentiation: follows a shortest or a short chain $1 = c_0, c_1, \ldots, c_\ell = b$ in which each $c_i$ is a sum of two earlier members; it uses $\ell$ multiplications.
- Each of these methods multiplies residues with a [modular multiplication](/modular-multiplication/) routine: plain division, [Barrett reduction](/barrett-reduction/), or [Montgomery multiplication](/montgomery-multiplication/), which avoids division and is the usual choice for a long exponent with an odd modulus.
- [Integer exponentiation](/integer-exponentiation/) is the same scheme without the reduction, for the exact power $a^b$.
- [Quantum modular exponentiation](/quantum-modular-exponentiation/) is the reversible circuit that [Shor's algorithm](/shor-algorithm/) applies to a superposition of exponents.

## Bounds

**Multiplication count, upper bound.** The binary method uses $\lambda(b) + \nu(b) - 1 \le 2\lambda(b)$ multiplications for $b \ge 1$. Brauer (1939) showed that the length $\ell(b)$ of a shortest addition chain satisfies $\ell(b) \le \lambda(b) + (1 + o(1))\lambda(b)/\lg \lambda(b)$, by a $2^m$-ary method with a suitable $m$ (Knuth, Section 4.6.3).

**Multiplication count, lower bound.** In a chain that only multiplies earlier powers, the largest exponent at most doubles at each step, so after $j$ steps it is at most $2^j$. Hence any such method needs at least $\lceil \lg b \rceil$ multiplications. Erdős (1960) showed that for almost all $b$ the shortest chain has length $\lambda(b) + (1 + o(1))\lambda(b)/\lg \lambda(b)$, so Brauer's bound is tight for most exponents. The binary method is not always optimal: $b = 15$ needs 6 multiplications by the binary method but has the chain $1, 2, 3, 6, 12, 15$ of length 5.

**Word-sized modulus.** With a constant-time product modulo $n$, the binary method takes $\Theta(\log b)$ time in the worst case and $O(1)$ extra words. For $b < 2^w$ this is $O(w)$.

**Arbitrary precision.** With a $k$-digit modulus and an $e$-digit exponent, $O(e)$ products modulo $n$ cost $O(e \cdot M(k))$ bit operations. With schoolbook arithmetic and $e \approx k$, as for an RSA private key, this is $O(k^3)$. Each algorithm must read the input, so $\Omega(k + e)$ bit operations are needed; no general lower bound of higher order is known.

**Finding the best chain.** Computing a shortest addition chain for a single exponent has no known polynomial-time algorithm. Downey, Leong and Sethi (1981) proved that finding a shortest chain that contains each number of a given set is NP-complete (Knuth, Section 4.6.3).

## Reductions

- **Inverse problem.** Given $a$, $n$ and $r$, find $b$ with $a^b \equiv r \pmod n$. This is the [discrete logarithm problem](/discrete-logarithm-problem/), believed to be hard for suitable $n$, while modular exponentiation is easy. This gap is the base of Diffie-Hellman and ElGamal.
- **Root extraction.** Given $b$, $n$ and $r$, find $a$ with $a^b \equiv r \pmod n$. For $b = 2$ this is the [modular square root](/modular-square-root/) problem. For composite $n$ with unknown factors it is the [RSA problem](/rsa-problem/).
- **Modular inverse modulo a prime.** For a prime $p$ and $p \nmid a$, $a^{-1} \equiv a^{p-2} \pmod p$ by [Fermat's little theorem](/fermat-little-theorem/), so a [modular inverse](/modular-inverse/) reduces to one exponentiation.
- **Fibonacci numbers.** $F_m \bmod n$ is an entry of the $m$-th power of $\begin{pmatrix} 1 & 1 \\ 1 & 0 \end{pmatrix}$ modulo $n$, so it reduces to modular exponentiation in the monoid of $2 \times 2$ matrices ([matrix Fibonacci](/matrix-fibonacci/)).

## Applications

- **Public-key cryptography.** Encryption, decryption and signatures in [RSA](/rsa-cryptosystem/), and key exchange in [Diffie-Hellman](/diffie-hellman/), are modular exponentiations with long exponents.
- **Primality testing.** The [Fermat test](/fermat-primality-test/), [Miller-Rabin](/miller-rabin/) and [Solovay-Strassen](/solovay-strassen/) each compute $a^d \bmod n$ for a candidate prime $n$.
- **Square roots and residues.** [Euler's criterion](/euler-criterion/) decides whether $a$ is a [quadratic residue](/quadratic-residue/) modulo a prime $p$ by computing $a^{(p-1)/2} \bmod p$, and the [Tonelli-Shanks algorithm](/tonelli-shanks/) is built from exponentiations.
- **Hashing and checksums.** [Polynomial rolling hashes](/polynomial-rolling-hash/) need $x^m \bmod p$ to remove the oldest character of a window.
- **Number-theoretic transforms.** The [number-theoretic transform](/number-theoretic-transform/) needs a root of unity $g^{(p-1)/N} \bmod p$.

## References
