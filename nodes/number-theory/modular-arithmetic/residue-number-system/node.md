---
tag: NJH1HQ
kind: concept
slug: residue-number-system
name: Residue number system
aliases:
- RNS
area: number-theory/modular-arithmetic
level: advanced
summary: Represents an integer by its residues modulo pairwise coprime moduli, enabling parallel arithmetic.
prereqs: [chinese-remainder-theorem, congruence]
see_also: [garner-algorithm, positional-number-system, modular-methods, multimodular-determinant, number-theoretic-transform, montgomery-multiplication, homomorphic-encryption, redundant-number-system]
sources:
  - book: isbn:9780849385230
    title: Alfred J. Menezes, Paul C. van Oorschot and Scott A. Vanstone, Handbook of Applied Cryptography, CRC Press, 1997
    locator: Section 14.5.1, Residue number systems (Fact 14.66, Definition 14.67, Fact 14.68, Example 14.69, Note 14.70), and Section 14.5.2, Garner's algorithm (Algorithm 14.71, Example 14.73, Note 14.74)
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, Seminumerical Algorithms, third edition
    locator: Section 4.3.2, Modular Arithmetic
  - book: isbn:9780521194693
    title: Richard P. Brent and Paul Zimmermann, Modern Computer Arithmetic, Cambridge University Press, 2010
    locator: Section 2.1.3, Residue number systems, and Section 2.7, Chinese remainder theorem
  - paper: "Harvey L. Garner, The residue number system, IRE Transactions on Electronic Computers EC-8 (1959), 140 to 147"
    locator: pages 140 to 147
---

A residue number system (RNS) represents an integer $x$ in the range $0 \le x < M$ by the tuple of its residues $(x \bmod m_1, \ldots, x \bmod m_t)$, where the moduli $m_1, \ldots, m_t$ are pairwise coprime and $M = m_1 \cdots m_t$. By the [Chinese remainder theorem](/chinese-remainder-theorem/) the tuple determines $x$, and addition, subtraction and multiplication modulo $M$ act on each residue separately, with no carries between them. So a long operation splits into $t$ short independent ones that can run in parallel. The price is that comparison, sign detection, overflow detection and division need the whole number back, by [Garner's algorithm](/garner-algorithm/) or the Chinese remainder formula. Computer algebra uses residue arithmetic in multimodular algorithms, and it is also used in digital signal processing hardware and in lattice-based cryptography.

## In plain words

Instead of writing a number with digits, write down its remainders after division by a few fixed numbers that share no common factor. For example, use 3, 5 and 7, and write 52 as the remainders 1, 2 and 3. To add or multiply two numbers, add or multiply the matching remainders and take remainders again. Each position works alone, so nothing carries from one position to the next, and all positions can work at the same time. The catch is that the remainders do not show which of two numbers is bigger. To compare them, or to divide, you must first rebuild the ordinary number.

## The idea

**Representation.** Fix pairwise coprime moduli $m_1, \ldots, m_t \ge 2$ and let $M = \prod_i m_i$, the *dynamic range*. The map

$$v(x) = (x \bmod m_1, \ldots, x \bmod m_t)$$

is a bijection from $\{0, \ldots, M - 1\}$ onto $\mathbb{Z}_{m_1} \times \cdots \times \mathbb{Z}_{m_t}$, by the Chinese remainder theorem (HAC, Fact 14.66). For signed values, the usual choice is the range $-\lfloor M/2 \rfloor \le x < \lceil M/2 \rceil$, with $v(-x) = -v(x)$ componentwise.

**Arithmetic.** The map $v$ is a ring isomorphism $\mathbb{Z}_M \cong \prod_i \mathbb{Z}_{m_i}$ (HAC, Fact 14.68):

$$v((x \pm y) \bmod M) = \bigl((x_i \pm y_i) \bmod m_i\bigr)_i, \qquad v(xy \bmod M) = \bigl(x_i y_i \bmod m_i\bigr)_i.$$

So if the true result of a sequence of additions, subtractions and multiplications lies in the range, it is computed exactly, digit by digit, in $t$ independent channels. Exact division by a constant $c$ coprime to $M$ is multiplication by $c^{-1} \bmod m_i$ in each channel, valid when $c$ is known to divide the result.

**Cost.** With $t$ moduli of word size, an RNS addition or multiplication costs $t$ word operations, and all $t$ can run in parallel, versus $O(t^2)$ word operations for a schoolbook multiplication of $t$-word numbers in positional form. Conversion into RNS costs $t$ reductions of an integer of about $t$ words, $O(t^2)$ word operations in total. Conversion back costs $O(t^2)$ word operations with Garner's algorithm (HAC, Note 14.74). Subquadratic conversions in both directions use product and remainder trees.

**What is hard.** The residues carry no information about magnitude. Four operations are expensive:

- *Magnitude comparison.* $x < y$ cannot be read off the residues.
- *Sign detection.* Deciding whether $x$ lies in the upper half of the range, so is negative in the signed range, is as hard as comparison.
- *Overflow detection.* A result that leaves the range wraps around silently modulo $M$.
- *General division and scaling.* Computing $\lfloor x/c \rfloor$ needs the remainder $x \bmod c$, which the channels do not hold unless $c$ is one of the moduli.

These all reduce to conversion. The standard route is the **mixed-radix representation**

$$x = a_1 + a_2 m_1 + a_3 m_1 m_2 + \cdots + a_t m_1 \cdots m_{t-1}, \qquad 0 \le a_i < m_i,$$

whose digits $a_i$ Garner's algorithm computes from the residues using only arithmetic modulo the small $m_i$ (HAC, Algorithm 14.71). Mixed-radix digits compare lexicographically from $a_t$ down, like ordinary digits.

**Base extension.** Many algorithms need the residue of $x$ modulo a new modulus $m_{t+1}$. With mixed-radix digits, $x \bmod m_{t+1}$ follows by Horner's rule modulo $m_{t+1}$. A faster parallel method uses the Chinese remainder formula

$$x = \sum_{i=1}^{t} \bigl(x_i M_i^{-1} \bmod m_i\bigr) M_i - \alpha M, \qquad M_i = M / m_i,$$

where the integer $\alpha$ is less than $t$. It can be found from one extra redundant modulus or estimated from the fractions $(x_i M_i^{-1} \bmod m_i)/m_i$. Base extension is the main step of RNS versions of [Montgomery multiplication](/montgomery-multiplication/), which compute modulo a large $n$ entirely in residue form.

**Choosing moduli.** Hardware designs use moduli for which reduction is cheap, such as the set $\{2^k - 1, 2^k, 2^k + 1\}$ with range $2^k(2^{2k} - 1)$. Software uses primes just below the word size, or primes of the form $c \cdot 2^e + 1$ that support the [number-theoretic transform](/number-theoretic-transform/).

**History.** The idea goes back to the remainder problem in the Sunzi Suanjing, a Chinese text from about the 3rd to 5th century. As a number representation for computers, it was proposed by Svoboda and Valach in Czechoslovakia in the mid-1950s and by Garner in the United States, whose 1959 paper "The residue number system" set out the arithmetic and the conversion method now called Garner's algorithm. Szabo and Tanaka's book of 1967 collected the early work on residue arithmetic in hardware. Knuth's treatment in The Art of Computer Programming made the method standard for multiple-precision software.

## Examples

**Moduli 2, 3, 5** (HAC, Example 14.69), $M = 30$. Then $v(21) = (1, 0, 1)$ and $v(27) = (1, 0, 2)$, and their sum is $(0, 0, 3) = v(18)$, matching $21 + 27 = 48 \equiv 18 \pmod{30}$. Also $v(22) = (0, 1, 2)$ and $v(17) = (1, 2, 2)$, and their product is $(0, 2, 4) = v(14)$, matching $22 \cdot 17 = 374 \equiv 14 \pmod{30}$.

**A product within range.** With moduli $7, 11, 13, 17$, $M = 17017$. Then $v(37) = (2, 4, 11, 3)$ and $v(45) = (3, 1, 6, 11)$. Channel by channel, $2 \cdot 3 = 6$, $4 \cdot 1 = 4$, $11 \cdot 6 = 66 \equiv 1 \pmod{13}$ and $3 \cdot 11 = 33 \equiv 16 \pmod{17}$, so the product is $(6, 4, 1, 16)$, which is $v(1665)$, and indeed $37 \cdot 45 = 1665 < M$.

**Converting back** (HAC, Example 14.73). With moduli $5, 7, 11, 13$ and $M = 5005$, the residues $(2, 1, 3, 8)$ give the mixed-radix digits $2, 4, 7, 5$ by Garner's algorithm, so

$$x = 2 + 4 \cdot 5 + 7 \cdot 35 + 5 \cdot 385 = 2192.$$

**No visible order.** With moduli $3, 5, 7$ and $M = 105$, $v(52) = (1, 2, 3)$ and $v(53) = (2, 3, 4)$, while $v(104) = (2, 4, 6)$ is also $v(-1)$ in the signed range. The residues alone do not tell which number is larger, or whether 104 means $104$ or $-1$.

**Silent overflow.** With the same moduli, $15 \cdot 8 = 120 \ge 105$, and the channels return $(0, 0, 1) = v(15)$, since $120 - 105 = 15$. Nothing in the result flags the overflow.

## Where it is used

- **Multimodular algorithms in computer algebra.** To compute an integer determinant, a resultant, a polynomial gcd or the solution of an integer linear system, compute the answer modulo many word-size primes and rebuild it by the Chinese remainder theorem once the product of the primes exceeds a bound on the answer. Each modular computation uses fast word arithmetic, and they run independently; see [modular methods](/modular-methods/) and the [multimodular determinant](/multimodular-determinant/).
- **Large multiplications and convolutions.** A convolution of integer sequences can be computed by number-theoretic transforms modulo three primes such as $998244353$, $167772161$ and $469762049$, and combined by the Chinese remainder theorem. The three primes have a product of about $7.9 \cdot 10^{25}$, enough for convolutions of length up to $10^7$ with entries below $10^9$.
- **RSA with the private key.** Decryption and signing compute $x^d \bmod pq$ as $x^d \bmod p$ and $x^d \bmod q$ and combine them, an RNS with two moduli, about four times faster than working modulo $pq$ (HAC, Note 14.70 and Note 14.75).
- **Signal processing hardware.** Digital filters and FFT units use RNS channels to avoid long carry chains, with special moduli sets such as $\{2^k - 1, 2^k, 2^k + 1\}$, since filtering is mostly additions and multiplications.
- **Lattice-based and homomorphic cryptography.** Ring-LWE schemes such as BFV and CKKS use a ciphertext modulus that is a product of word-size primes, and "full-RNS" variants keep every coefficient in residue form, using approximate base extension instead of conversion; see [homomorphic encryption](/homomorphic-encryption/).
- **Fault tolerance.** Redundant residue number systems add extra moduli beyond the needed range; a result that falls outside the legitimate range reveals an error in a channel, and with enough redundancy the faulty channel can be found and corrected.

## References
