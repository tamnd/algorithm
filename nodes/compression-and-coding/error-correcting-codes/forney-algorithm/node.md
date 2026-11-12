---
tag: 6QZVB2
kind: algorithm
slug: forney-algorithm
name: Forney algorithm
aliases:
- Forney error evaluation
- Forney formula
area: compression-and-coding/error-correcting-codes
level: advanced
summary: "Compute the error values of a Reed-Solomon or BCH decoder from the error locator and the evaluator: Y = -X^(1-b) Omega(1/X) / Lambda'(1/X) for each error locator X."
model: word-ram
complexity:
  vars: {t: the number of correctable errors}
  time: {worst: Θ(t^2), average: Θ(t^2), best: Θ(t^2)}
  space: {extra: Θ(t)}
properties: {deterministic: true, recursive: false, online: false}
history:
  year: 1965
  people: [G. David Forney, Jr.]
  note: Forney gave the closed formula for the error values in his 1965 paper on decoding BCH codes, which also added erasures to the decoder.
prereqs: [reed-solomon-decoding, chien-search]
see_also: [berlekamp-massey, peterson-gorenstein-zierler, reed-solomon-code, bch-code, berlekamp-welch, polynomial-evaluation]
sources:
  - paper: doi:10.1109/TIT.1965.1053825
    title: G. D. Forney, Jr., On decoding BCH codes, IEEE Transactions on Information Theory 11(4), 1965
    locator: pp. 549 to 557 (the error value formula, and the decoding of errors and erasures)
  - book: isbn:9780130426727
    title: Shu Lin and Daniel J. Costello, Jr., Error Control Coding, second edition, Pearson Prentice Hall, 2004
    locator: Chapter 7 (decoding of nonbinary BCH and Reed-Solomon codes, the error-value evaluator and the computation of error values)
  - book: isbn:9780521845045
    title: Ron M. Roth, Introduction to Coding Theory, Cambridge University Press, 2006
    locator: Chapter 6 (the key equation, the error evaluator polynomial and the formula for the error values)
---

The Forney algorithm computes the error values in a [Reed-Solomon](/reed-solomon-decoding/) or nonbinary [BCH](/bch-code/) decoder once the error positions are known. From the syndrome polynomial $S(x)$ and the error locator $\Lambda(x)$, it forms the error evaluator $\Omega(x) = S(x)\Lambda(x) \bmod x^{2t}$. Then each error value is a ratio of two polynomial values: for the error with locator $X_k$,

$$Y_k = -X_k^{\,1-b}\,\frac{\Omega(X_k^{-1})}{\Lambda'(X_k^{-1})},$$

where $\Lambda'$ is the formal derivative and $\alpha^b$ is the first zero of the code. It replaces the solution of a $\nu \times \nu$ Vandermonde system by $O(t)$ operations per error.

## In plain words

After the decoder knows where the errors are, it still has to find how large each error is, so that it can subtract it. The syndromes are sums in which each error appears with a known weight. One way is to solve these sums as a system of equations. Forney found a shortcut. Multiply the syndrome polynomial by the locator polynomial and keep only the low terms. The result, the evaluator, holds every error value, each one multiplied by a product that is zero for all the other errors. So the value of the evaluator at the root of one error, divided by a value of the derivative of the locator at the same point, gives that error alone.

## The algorithm

The code has the consecutive zeros $\alpha^b, \alpha^{b+1}, \ldots, \alpha^{b+2t-1}$. The syndromes are $S_j = r(\alpha^j)$ for these $j$. The error at position $i_k$ has locator $X_k = \alpha^{i_k}$ and value $Y_k$, and $\Lambda(x) = \prod_{k=1}^{\nu}(1 - X_k x)$ with $\nu \le t$. The positions come from the [Chien search](/chien-search/).

```pseudo id=main
FORNEY(S_b .. S_(b+2t−1), Λ, positions i_1 .. i_ν, b)
L1  S(x) ← S_b + S_(b+1) x + … + S_(b+2t−1) x^(2t−1)
L2  Ω(x) ← S(x) · Λ(x) mod x^(2t)              ▷ the error evaluator
L3  Λ'(x) ← Σ_j j Λ_j x^(j−1)                  ▷ the formal derivative
L4  for k ← 1 to ν do
L5      X ← α^(i_k)
L6      Y_k ← −X^(1−b) · Ω(X^(−1)) / Λ'(X^(−1))
L7  return Y_1 .. Y_ν
```

Line L2 needs only the products of degree below $2t$. Line L3 is the formal derivative; in characteristic 2 the factor $j$ is 0 or 1, so $\Lambda'$ keeps only the odd terms of $\Lambda$, shifted down by one. In characteristic 2 the minus sign of line L6 also disappears.

**The factor $X^{1-b}$.** It comes from the first zero of the code. For $b = 1$, the usual textbook case, it is 1, and $Y_k = -\Omega(X_k^{-1})/\Lambda'(X_k^{-1})$. QR codes use $b = 0$, so $Y_k = -X_k\,\Omega(X_k^{-1})/\Lambda'(X_k^{-1})$. CCSDS 131.0-B uses the zeros $\beta^{128-E}, \ldots, \beta^{127+E}$ with $\beta = \alpha^{11}$; then $X_k = \beta^{i_k}$ and $b = 128 - E$.

**Erasures.** If some positions are erasures with locator $\Gamma(x) = \prod (1 - Z_l x)$, line L2 uses the full locator $\Psi = \Lambda \Gamma$, and line L6 uses $\Psi'$. The formula gives the values of errors and erasures alike, for up to $2t$ positions in total.

## Example

Over $\mathrm{GF}(16)$ with $\alpha^4 = \alpha + 1$, the code RS(15, 11) with $b = 1$ and $t = 2$ has errors $\alpha^5$ at position 2 and $\alpha^{11}$ at position 7. The [Berlekamp-Massey](/berlekamp-massey/) page finds $\Lambda(x) = 1 + \alpha^{12} x + \alpha^9 x^2$ from the syndromes $\alpha^4, \alpha^{13}, \alpha^9, \alpha^{10}$, and the Chien search finds the positions 2 and 7.

| step | value |
|---|---|
| L1 | $S(x) = \alpha^4 + \alpha^{13} x + \alpha^9 x^2 + \alpha^{10} x^3$ |
| L2 | $\Omega(x) = \alpha^4 + \alpha^{12} x$ (the terms of degree 2 and 3 cancel) |
| L3 | $\Lambda'(x) = \alpha^{12}$ (only the odd term $\alpha^{12} x$ of $\Lambda$ stays) |
| L6, $X = \alpha^2$ | $\Omega(\alpha^{-2}) = \alpha^2$, $\Lambda'(\alpha^{-2}) = \alpha^{12}$, $Y = \alpha^{2-12} = \alpha^5$ |
| L6, $X = \alpha^7$ | $\Omega(\alpha^{-7}) = \alpha^8$, $\Lambda'(\alpha^{-7}) = \alpha^{12}$, $Y = \alpha^{8-12} = \alpha^{11}$ |

Both values are right. With $b = 1$ the factor $X^{1-b}$ is 1. For the same errors in a code with $b = 0$, the syndromes are $\alpha^3, \alpha^4, \alpha^{13}, \alpha^9$, $\Omega$ changes, and the factor $X$ in line L6 gives the same two values.

## Correctness

Write $S_j = \sum_k Y_k X_k^{\,j}$. The geometric sum gives $S(x) \Lambda(x) \equiv \sum_k Y_k X_k^{\,b} \prod_{l \ne k}(1 - X_l x) \pmod{x^{2t}}$, and the right side has degree below $\nu \le 2t$, so it is $\Omega(x)$ exactly. At $x = X_k^{-1}$ all terms but the $k$-th vanish, and the product rule gives $\Lambda'(X_k^{-1}) = -X_k \prod_{l \ne k}(1 - X_l X_k^{-1})$, which is not zero. The ratio is $-Y_k X_k^{\,b-1}$. The full proof is in [proofs/correctness.md](proofs/correctness.md).

## Complexity

Line L2 costs $O(t \nu) = O(t^2)$ field operations, because only $2t$ coefficients of the product are kept. Line L3 costs $O(\nu)$. Each of the $\nu$ error values costs two evaluations of degree below $\nu$, one power and one division, so the loop costs $O(\nu^2)$ in total. The whole algorithm is $\Theta(t^2)$ in the worst case, and the extra space is $\Theta(t)$. In hardware decoders, the two evaluations run in the Chien search registers at the same time as the root test, so each error value costs one division when its position is found.

## Properties

- **Closed form.** No linear system is solved: each value is a ratio of two polynomial values.
- **Any field.** The derivation uses only the formal derivative and the product rule, which hold over every field. Over $\mathrm{GF}(2^m)$ the formula is simpler because $-1 = 1$ and $\Lambda'$ has only even powers of $x$.
- **Needs distinct locators.** The denominator $\Lambda'(X_k^{-1})$ is nonzero exactly because the $X_k$ are distinct, that is, because $\Lambda$ has no repeated root.
- **Erasures for free.** The same formula with $\Psi = \Lambda\Gamma$ gives the erasure values.

## Variants and improvements

- **From the Euclidean algorithm.** The algorithm of Sugiyama, Kasahara, Hirasawa and Namekawa (1975) returns $\Omega$ together with $\Lambda$, up to a common constant that cancels in line L6.
- **From Berlekamp-Massey.** A second sequence of polynomials in the Berlekamp-Massey loop gives $\Omega$ without the product of line L2; the result is the same.
- **Solving the Vandermonde system.** The [Peterson-Gorenstein-Zierler](/peterson-gorenstein-zierler/) decoder solves $S_j = \sum_k Y_k X_k^{\,j}$ for the $Y_k$ directly. That costs $O(\nu^3)$, or $O(\nu^2)$ with a Vandermonde solver, and gives the same values.
- **The evaluation view.** The [Berlekamp-Welch](/berlekamp-welch/) decoder finds the message polynomial directly and needs no error values.

## When to use it

Use the Forney algorithm in every Reed-Solomon decoder and in decoders for nonbinary BCH codes, after the error locator and the Chien search. Binary BCH codes do not need it, because every error value is 1. Use the erasure form when the demodulator or an inner code marks unreliable symbols.

## Pitfalls

- **The wrong power of $X$.** Line L6 has the factor $X^{1-b}$. A decoder for QR codes ($b = 0$) that copies the $b = 1$ formula from a textbook gets every value wrong by the factor $X_k$. At position 0 the factor is $X_k = 1$, so a test with one error at position 0 does not find the bug.
- **The wrong derivative.** Line L3 is the formal derivative. Over $\mathrm{GF}(2^m)$ the even terms vanish; it is a common error to keep them, or to compute $\Lambda'$ from the reversed locator.
- **Ω modulo the wrong power.** Line L2 reduces modulo $x^{2t}$, with exactly the $2t$ syndromes in use. Keeping more terms of the product gives a wrong $\Omega$.
- **Syndrome indexing.** $S(x)$ in line L1 starts with $S_b$, the syndrome at the first zero, as the constant term. With $S_{b+1}$ first, all values come out wrong.
- **Zero denominator.** If $\Lambda'(X^{-1}) = 0$, the locator has a repeated root or the position list is wrong. A decoder must report a failure, not divide.

## Implementations

## History

G. David Forney, Jr. published the formula in 1965 in "On decoding BCH codes". The paper also showed how to decode errors and erasures together, with the erasure locator multiplied into the error locator. The formula is now part of every syndrome decoder for Reed-Solomon codes, together with the [Berlekamp-Massey algorithm](/berlekamp-massey/) or the Euclidean algorithm and the [Chien search](/chien-search/).

## References
