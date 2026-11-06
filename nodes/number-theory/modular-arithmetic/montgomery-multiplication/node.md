---
tag: C3XQAV
kind: algorithm
slug: montgomery-multiplication
name: Montgomery multiplication
aliases:
- Montgomery reduction
- Montgomery form
area: number-theory/modular-arithmetic
level: advanced
summary: Multiplies residues modulo an odd n kept in the form aR mod n, with R a power of two, using multiplications, masks and shifts instead of division by n.
solves: [modular-multiplication]
model: word-ram
complexity:
  vars: {k: the number of words of n, w: the number of binary digits in a word, M: the cost of multiplying two numbers of k w binary digits}
  time: {worst: Θ(k^2), best: Θ(k^2)}
  space: {extra: Θ(k)}
  bit_operations: {worst: O(M(k w))}
properties: {deterministic: true, recursive: false}
history:
  year: 1985
  people: [Peter L. Montgomery]
  note: Published as "Modular multiplication without trial division"; the word-by-word form used in hardware and libraries was analysed by Koç, Acar and Kaliski in 1996.
prereqs: [modular-multiplication, modular-inverse]
see_also: [barrett-reduction, modular-exponentiation, binary-exponentiation, granlund-montgomery-division, number-theoretic-transform, rsa-cryptosystem, timing-attack, constant-time]
sources:
  - paper: "Peter L. Montgomery, Modular multiplication without trial division, Mathematics of Computation 44(170), 1985"
    locator: pages 519 to 521 (the function REDC and its use for products and exponentiation)
  - book: isbn:9780849385230
    title: Alfred J. Menezes, Paul C. van Oorschot and Scott A. Vanstone, Handbook of Applied Cryptography, CRC Press, 1997
    locator: Section 14.3.2, Montgomery reduction (Algorithm 14.32, Example 14.35, Algorithm 14.36 Montgomery multiplication), and Algorithm 14.94, Montgomery exponentiation
  - book: isbn:9780521194693
    title: Richard P. Brent and Paul Zimmermann, Modern Computer Arithmetic, Cambridge University Press, 2010
    locator: Section 2.4.2, Montgomery's multiplication, and Section 2.1.2, Montgomery's form
  - book: isbn:9780387252827
    title: Richard Crandall and Carl Pomerance, Prime Numbers, A Computational Perspective, second edition
    locator: Section 9.2.1, Montgomery method
  - paper: "Çetin Kaya Koç, Tolga Acar and Burton S. Kaliski Jr., Analyzing and comparing Montgomery multiplication algorithms, IEEE Micro 16(3), 1996"
    locator: pages 26 to 33 (the SOS, CIOS and related word-level variants and their operation counts)
---

Montgomery multiplication computes products modulo an odd integer $n$ without dividing by $n$. It fixes $R = 2^r > n$ and keeps each residue $a$ in the *Montgomery form* $\tilde a = aR \bmod n$. The core step, Montgomery reduction or REDC, maps an integer $T < nR$ to $TR^{-1} \bmod n$ with two multiplications, a mask, a shift and at most one subtraction, because division by $R$ is a shift. Then $\mathrm{REDC}(\tilde a \tilde b) = \widetilde{ab}$, so long chains of products, as in [modular exponentiation](/modular-exponentiation/), stay in Montgomery form and convert only at the start and the end. Peter Montgomery published the method in 1985, and it is the standard reduction in RSA and elliptic curve libraries.

## In plain words

Dividing by the clock size is the slow part of multiplication on a clock. This method avoids it for clock sizes that are odd. It picks a power of two a bit larger than the clock size, because a computer divides by a power of two with a cheap shift. Each number is first moved into a scaled copy of itself. To multiply, you multiply the scaled copies and then add a well chosen multiple of the clock size. This multiple makes the low part of the sum all zeros, so you can shift it away. The result is the scaled copy of the true product, often after one last subtraction. You move back out of the scaled world only at the end.

## The problem

The input is an odd modulus $n \ge 1$ and residues $a, b \in \{0, \ldots, n - 1\}$; the output is $ab \bmod n$. This is [modular multiplication](/modular-multiplication/) with a fixed modulus: many products with one $n$, where a setup step per modulus is allowed.

**Cost model.** On the [word RAM](/word-ram/) with $w$-digit words, a single-word modulus has $n < 2^w$ and $R = 2^w$; then a product and a reduction cost $O(1)$ word operations, with a double-width product. For a modulus of $k$ words, $R = 2^{kw}$, and the word-by-word form below makes $2k^2 + k$ word multiplications per product, or $O(M(kw))$ bit operations with a fast multiplication of cost $M$. Residues are integers in $[0, n)$, held in Montgomery form. The modulus must be odd, so that $\gcd(n, R) = 1$; for an even modulus, use [Barrett reduction](/barrett-reduction/) or split off the power of two with the [Chinese remainder theorem](/chinese-remainder-theorem/).

## The algorithm

```pseudo id=main
MONTGOMERY-SETUP(n)                     ▷ n odd, n ≥ 1
L1  r ← number of binary digits of n; R ← 2^r      ▷ R > n
L2  x ← 1                               ▷ n·x ≡ 1 (mod 2), as n is odd
L3  j ← 1
L4  while j < r do                      ▷ invariant: n·x ≡ 1 (mod 2^j)
L5      j ← min(2j, r); x ← x·(2 − n·x) mod 2^j
L6  n′ ← (−x) mod R                     ▷ n·n′ ≡ −1 (mod R)
L7  R2 ← R² mod n

REDC(T)                                 ▷ 0 ≤ T < n·R
L8  m ← ((T mod R) · n′) mod R          ▷ a mask and a low product
L9  t ← (T + m·n) / R                   ▷ exact; a shift by r
L10 if t ≥ n then t ← t − n
L11 return t                            ▷ t = T·R⁻¹ mod n

MONT-MUL(ã, b̃)                          ▷ ã, b̃ in [0, n)
L12 return REDC(ã · b̃)

TO-MONT(a)                              ▷ a in [0, n)
L13 return REDC(a · R2)                 ▷ = aR mod n

FROM-MONT(ã)
L14 return REDC(ã)                      ▷ = ãR⁻¹ mod n
```

Lines L2 to L5 compute $n^{-1} \bmod R$ by Newton's iteration over the 2-adic integers: if $nx \equiv 1 \pmod{2^j}$, then $1 - n \cdot x(2 - nx) = (1 - nx)^2 \equiv 0 \pmod{2^{2j}}$, so each step doubles the number of correct binary digits. Line L7 is one ordinary division, done once per modulus.

In REDC, line L8 chooses $m$ so that $T + mn \equiv T + T n' n \equiv T - T \equiv 0 \pmod R$, so the division in line L9 is exact and costs a shift. Since $T < nR$ and $m < R$, the quotient is below $2n$, and line L10 brings it into $[0, n)$.

A product of two Montgomery forms is $\mathrm{REDC}(aR \cdot bR) = abR \bmod n$, the form of $ab$. Sums and differences of forms are forms of sums and differences, so additions need no change.

## Example

Take $n = 97$, so $r = 7$ and $R = 128$. Setup: $x$ is 1 modulo 2, 4 and 16 (as $97 \equiv 1 \pmod{16}$), and the last Newton step gives $x = 1 \cdot (2 - 97) \bmod 128 = 33$; indeed $97 \cdot 33 = 3201 = 25 \cdot 128 + 1$. So $n' = 128 - 33 = 95$, and $R2 = 128^2 \bmod 97 = 88$.

Compute $50 \cdot 60 \bmod 97$:

| step | value |
| --- | --- |
| $\tilde a = \mathrm{REDC}(50 \cdot 88)$ | $95 = 50 \cdot 128 \bmod 97$ |
| $\tilde b = \mathrm{REDC}(60 \cdot 88)$ | $17 = 60 \cdot 128 \bmod 97$ |
| $T = \tilde a \tilde b$ | $1615$ |
| L8: $T \bmod 128 = 79$, $m = 79 \cdot 95 \bmod 128$ | $81$ |
| L9: $(1615 + 81 \cdot 97)/128 = 9472/128$ | $74$, below 97, so no subtraction |
| $\mathrm{FROM\text{-}MONT}(74)$ | $90$ |

And $50 \cdot 60 = 3000 = 30 \cdot 97 + 90$. Also $74 = 90 \cdot 128 \bmod 97$, the Montgomery form of 90.

A case with the subtraction: for $30 \cdot 50$, $\tilde a = 57$, $\tilde b = 95$, $T = 5415$, $T \bmod 128 = 39$, $m = 39 \cdot 95 \bmod 128 = 121$, and $(5415 + 121 \cdot 97)/128 = 17152/128 = 134 \ge 97$, so line L10 gives $37$. This is the form of $30 \cdot 50 \bmod 97 = 45$, since $45 \cdot 128 \bmod 97 = 37$.

## Correctness

The setup computes $n'$ with $nn' \equiv -1 \pmod R$: by the Newton step, $nx \equiv 1 \pmod{2^j}$ holds after each pass, and the loop ends with $j = r$. For REDC, line L8 makes $T + mn$ divisible by $R$, so $t = (T + mn)/R$ is an integer with $tR \equiv T \pmod n$, that is, $t \equiv TR^{-1}$. From $0 \le T < nR$ and $0 \le m < R$ follows $0 \le t < 2n$, so after line L10, $t = TR^{-1} \bmod n$. Hence MONT-MUL maps forms to forms, TO-MONT gives $aR^2 R^{-1} = aR$, and FROM-MONT gives $a$. The full proof is below.

## Complexity

**Setup.** Lines L2 to L5 run $\lceil \lg r \rceil$ passes, each with products of at most $r$ binary digits; with any multiplication method whose cost grows at least linearly, the total is $O(M(r))$. Line L7 is one division of a $2r$-digit number by $n$, $O(M(r))$. On the word RAM with $r = w$, the setup is $O(\log w)$ word operations plus one division.

**One product, single word.** For $n < 2^w$ and $R = 2^w$: one double-width product $\tilde a \tilde b$, one low-half product for $m$, one double-width product $mn$, an addition, a shift and a comparison. This is $O(1)$ word operations, without a division instruction.

**One product, $k$ words.** With schoolbook arithmetic, $\tilde a \tilde b$ costs $k^2$ word multiplications. Reduction processes $T$ one word at a time: for each of the $k$ low words, it computes a one-word $m_i = t_i n'_0 \bmod 2^w$, where $n'_0 = -n^{-1} \bmod 2^w$, and adds $m_i n 2^{iw}$, for $k + 1$ word multiplications per word. The total is $2k^2 + k$ word multiplications, $\Theta(k^2)$ in both the best and worst case, since the work does not depend on the values. The extra space is $\Theta(k)$ words for $T$. With a fast multiplication of cost $M$, the whole-number form of REDC uses one full product, one low half product and one high half product, $O(M(kw))$ bit operations.

**Comparison with classical reduction.** Classical reduction of a $2k$-word number by a $k$-word modulus also needs about $k^2$ word multiplications, but each of its $k$ quotient digits needs a division and a possible correction. Montgomery reduction needs no division and no correction inside the loop, so it is simpler and faster in practice, in hardware and in software.

## Properties

- **Odd modulus only.** It needs $\gcd(n, R) = 1$, so $n$ must be odd when $R$ is a power of two.
- **Works on a changed representation.** Inputs and outputs are Montgomery forms. Conversion costs one REDC each way, so the method pays off only for several products with one modulus.
- **Division-free.** After the setup, it uses only multiplication, addition, masks and shifts.
- **Right-to-left.** It consumes the low words first, the opposite of classical division, which is why it is related to 2-adic (Hensel) division.
- **Almost constant-time.** The only data-dependent step is the final subtraction in line L10.
- **Deterministic and iterative.** No randomness and no recursion.

## Variants and improvements

- **Word-by-word reduction.** The form of the complexity section, with the one-word constant $n'_0$ (Dussé and Kaliski, 1990). Koç, Acar and Kaliski compare the orders of loops: SOS (separated operand scanning), CIOS (coarsely integrated operand scanning, which interleaves the product and the reduction and needs only $k + 2$ words of space) and others.
- **Montgomery exponentiation.** Convert the base once, run square-and-multiply with MONT-MUL, and convert back (HAC, Algorithm 14.94). This is the main use.
- **No final subtraction.** If $4n < R$ and inputs are allowed in $[0, 2n)$, then REDC outputs stay in $[0, 2n)$ without line L10 (Walter, 1999). This removes the data-dependent branch.
- **Lazy reduction.** Keep values in $[0, 2n)$ or $[0, 4n)$ inside loops such as the [number-theoretic transform](/number-theoretic-transform/), and reduce fully at the end.
- **Signed Montgomery reduction.** For word-sized primes, a variant with $m$ in $(-R/2, R/2)$ and outputs in $(-n, n)$ is common in lattice cryptography.
- **Montgomery inverse and squaring.** A Montgomery form of $a^{-1}$ can be computed directly; squaring uses a dedicated product with about half the word multiplications.
- **Barrett reduction.** [Barrett reduction](/barrett-reduction/) is the left-to-right counterpart: it works for even moduli and on ordinary residues, at a similar cost.

## When to use it

Use it for many products modulo one odd number: modular exponentiation in RSA, Diffie-Hellman and the Miller-Rabin test, arithmetic on elliptic curves over prime fields, and number-theoretic transforms with word-sized primes. Do not use it for a single product, since the conversions cost as much as a classical reduction. For even moduli, use Barrett reduction or classical division. For special moduli like $2^{255} - 19$ or $2^{61} - 1$, a reduction that uses the special form is faster.

## Pitfalls

- **An even modulus.** $n^{-1} \bmod 2^r$ does not exist, and REDC returns wrong values without an error. Check that $n$ is odd.
- **Mixing representations.** MONT-MUL of an ordinary residue and a form gives $abR^{-1}$, not $ab$. Keep the two kinds of values apart, for example with a separate type.
- **Overflow of $T + mn$.** With $n$ close to $R = 2^w$, the sum $T + mn$ can reach $2nR$, one binary digit more than two words. Keep the carry, or require $n < R/2$.
- **The sign of $n'$.** Some texts use $n' = -n^{-1}$ and add $mn$, others use $n^{-1}$ and subtract. Mixing the two conventions gives results that are wrong but in range.
- **Inputs not below $nR$.** REDC needs $T < nR$. Products of two reduced residues satisfy this; products of unreduced values may not.
- **Timing leaks.** The final subtraction depends on the data, and this has been used to recover RSA keys through timing ([timing attack](/timing-attack/)). Use a [constant-time](/constant-time/) conditional subtraction, or the variant without it.

## Implementations

## History

Peter Montgomery published the method in 1985 in *Mathematics of Computation*, under the title "Modular multiplication without trial division". The idea of reducing from the low end, by adding multiples of the modulus until the low digits are zero, is related to Hensel's 2-adic division. Dussé and Kaliski (1990) observed that the word-level reduction needs only $-n^{-1}$ modulo one word, and Koç, Acar and Kaliski (1996) compared the main word-level loop orders. Walter (1999) showed how to avoid the final subtraction, which matters for resistance to timing attacks. Montgomery multiplication is now the default for odd moduli in multiple-precision libraries and in RSA and elliptic curve code.

## References
