---
tag: EK5MW6
kind: definition
slug: non-adjacent-form
name: Non-adjacent form
aliases:
- NAF
- canonical signed digit representation
- CSD
- Reitwiesner recoding
area: algebra/integer-arithmetic
level: advanced
summary: Signed binary representation with no two adjacent nonzero digits and minimal weight.
prereqs: [signed-digit-representation, positional-number-system]
see_also: [signed-digit-representation, binary-exponentiation, sliding-window-exponentiation, booth-multiplication, addition-chain, elliptic-curve-cryptography, redundant-number-system]
sources:
  - paper: G. W. Reitwiesner, Binary arithmetic, Advances in Computers 1, Academic Press, 1960
    title: George W. Reitwiesner, Binary arithmetic
    locator: pp. 231 to 308 (the minimal signed binary representation, its uniqueness and its construction)
  - book: isbn:9780387952734
    title: Darrel Hankerson, Alfred Menezes and Scott Vanstone, Guide to Elliptic Curve Cryptography, Springer, 2004
    locator: Section 3.3.1, Non-adjacent form (the NAF and its properties, the algorithm to compute it, and the width-w NAF)
  - book: isbn:9780849385230
    title: Alfred J. Menezes, Paul C. van Oorschot and Scott A. Vanstone, Handbook of Applied Cryptography, CRC Press, 1996
    locator: Section 14.7, Exponent recoding (signed-digit representations of exponents)
---

The non-adjacent form, or NAF, of an integer is its representation in radix 2 with digits $-1, 0, 1$ in which no two adjacent digits are both nonzero. Every integer has exactly one NAF, and among all its representations with these digits the NAF has the fewest nonzero digits. For example $7 = 111_2$ has the NAF $100\bar{1}$, that is $8 - 1$, where $\bar{1}$ is the digit $-1$. On average only one third of the digits of a NAF are nonzero, against one half for binary. That makes it the standard recoding of a scalar or exponent when subtraction costs no more than addition: in [elliptic curve](/elliptic-curve-cryptography/) scalar multiplication, where negating a point is free, a NAF scalar needs about $k/3$ additions instead of $k/2$ for a $k$-digit scalar. In hardware the same form is called the canonical signed digit representation, and it is used to multiply by constants with few adders.

## Definition

A **binary signed-digit representation** of an integer $n$ is a finite string $d_{\ell-1} \cdots d_0$ with $d_i \in \{-1, 0, 1\}$ and $n = \sum_i d_i 2^i$; see [signed-digit representation](/signed-digit-representation/). Its *weight* is the number of nonzero digits.

The representation is a **non-adjacent form** if

$$d_i \, d_{i+1} = 0 \quad \text{for all } i ,$$

that is, among any two consecutive digits at least one is 0.

**Facts.**

1. **Existence and uniqueness** (Reitwiesner, 1960). Every integer $n$ has exactly one NAF, up to leading zeros. Write $\mathrm{NAF}(n)$ for it.
2. **Construction.** If $n$ is even, the last digit is 0 and the rest is $\mathrm{NAF}(n/2)$. If $n$ is odd, the last digit is $d_0 = 2 - (n \bmod 4) \in \{1, -1\}$, chosen so that $n - d_0 \equiv 0 \pmod 4$; the next digit is then 0, and the rest is $\mathrm{NAF}((n - d_0)/2)$. This is also the proof of existence. Uniqueness follows because an odd $n$ forces $d_0 \equiv n \pmod 4$ when $d_1 = 0$.
3. **Minimal weight.** No binary signed-digit representation of $n$ has fewer nonzero digits than $\mathrm{NAF}(n)$.
4. **Length.** If $n > 0$ has $k$ binary digits, $\mathrm{NAF}(n)$ has $k$ or $k + 1$ digits, and its leading digit is 1.
5. **Density.** For random $k$-digit $n$, the expected weight of $\mathrm{NAF}(n)$ is about $k/3$. The digit process is a Markov chain in which a nonzero digit is always followed by a 0.
6. **A formula.** With bitwise operations on nonnegative $n$: the positions of the digits $1$ are the set bits of $((3n \oplus n) \wedge 3n) \gg 1$, and those of the digits $-1$ are the set bits of $((3n \oplus n) \wedge n) \gg 1$.
7. **Negation.** $\mathrm{NAF}(-n)$ is $\mathrm{NAF}(n)$ with every digit negated.

## Examples and non-examples

All examples were checked by script, including the facts above for all $|n| \le 255$, against every string of nine digits.

- $7 = 100\bar{1}$, weight 2 against 3 for $111$. $15 = 1000\bar{1}$ and $255 = 10000000\bar{1}$: a run of ones becomes two nonzero digits.
- $11 = 10\bar{1}0\bar{1}$, that is $16 - 4 - 1$, with weight 3, the same as $1011$. The construction gives it step by step: $11 \bmod 4 = 3$, so the last digit is $\bar{1}$; then $12/2 = 6$ gives 0; $3 \bmod 4 = 3$ gives $\bar{1}$; $4/2 = 2$ gives 0; and $1$ gives 1.
- $814507 = 1100\,0110\,1101\,1010\,1011_2$ has weight 12 in binary and the NAF $10\bar{1}00100\bar{1}00\bar{1}00\bar{1}0\bar{1}0\bar{1}0\bar{1}$ of weight 9, with one more digit.
- $-7 = \bar{1}001$, by negating the digits of $\mathrm{NAF}(7)$.
- **Observed density.** Over 2000 random numbers each, the average weight was $0.345k$, $0.337k$ and $0.334k$ for $k = 64$, $256$ and $1024$.

**Non-examples.**

- $1\bar{1}11$, $10\bar{1}1$ and $0111$ all represent 7, but each has two adjacent nonzero digits; only $100\bar{1}$ is the NAF.
- $3 = 11_2$ is not in NAF; its NAF is $10\bar{1}$, which is longer but has the same weight. Minimal weight does not mean minimal length.
- A representation of minimal weight need not be the NAF: $3 = 11$ also has weight 2.

## Related definitions

- **Width-$w$ NAF.** Digits are 0 or odd with $|d_i| < 2^{w-1}$, and among any $w$ consecutive digits at most one is nonzero. The average density is about $1/(w + 1)$; we observed $0.202$ for $w = 4$ at $k = 256$. With precomputed odd multiples it is the signed analogue of [sliding-window exponentiation](/sliding-window-exponentiation/).
- **Booth recoding.** Replacing each run of ones by $+1$ at the top and $-1$ at the bottom; it also gives digits $\pm 1$ but may leave adjacent nonzero digits. See [Booth multiplication](/booth-multiplication/).
- **Joint sparse form.** A recoding of a pair of integers that minimizes the number of positions where either is nonzero, used for computing $aP + bQ$ at once.
- **Addition-subtraction chains.** Binary exponentiation driven by the NAF is an addition-subtraction chain; see [addition chain](/addition-chain/).
- **Signed-digit representation.** The general family; see [signed-digit representation](/signed-digit-representation/).

### History

Reitwiesner introduced the minimal binary signed-digit representation in 1960, with its uniqueness and its construction from the low end. In digital filter design it became known as the canonical signed digit form. In cryptography, Morain and Olivos proposed in 1990 to use addition-subtraction chains, and NAF scalars became standard in elliptic curve implementations, together with the width-$w$ NAF.

## References
