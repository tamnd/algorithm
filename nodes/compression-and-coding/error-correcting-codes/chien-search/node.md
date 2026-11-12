---
tag: GDVWFM
kind: algorithm
slug: chien-search
name: Chien search
aliases:
- Chien root search
area: compression-and-coding/error-correcting-codes
level: advanced
summary: Find the error positions of a BCH or Reed-Solomon decoder by evaluating the error locator at every inverse power of alpha, with one constant multiplication per coefficient per step.
model: word-ram
complexity:
  vars: {n: the code length, t: the degree of the error locator}
  time: {worst: Θ(n t), average: Θ(n t), best: Θ(n t)}
  space: {extra: Θ(t)}
properties: {deterministic: true, recursive: false, online: true}
history:
  year: 1964
  people: [Robert T. Chien]
  note: Chien described the search as a cyclic decoding procedure for BCH codes, one code position per clock cycle.
prereqs: [reed-solomon-decoding, horner-rule]
see_also: [berlekamp-massey, forney-algorithm, peterson-gorenstein-zierler, bch-code, reed-solomon-code, multipoint-evaluation, cantor-zassenhaus-algorithm]
sources:
  - paper: doi:10.1109/TIT.1964.1053699
    title: R. T. Chien, Cyclic decoding procedures for Bose-Chaudhuri-Hocquenghem codes, IEEE Transactions on Information Theory 10(4), 1964
    locator: pp. 357 to 363 (the test of each position by a bank of registers that multiply by fixed powers of alpha)
  - book: isbn:9780130426727
    title: Shu Lin and Daniel J. Costello, Jr., Error Control Coding, second edition, Pearson Prentice Hall, 2004
    locator: Chapter 6 (implementation of error correction, the Chien search circuit)
  - book: isbn:9780521553742
    title: Richard E. Blahut, Algebraic Codes for Data Transmission, Cambridge University Press, 2003
    locator: The chapters on the implementation of BCH and Reed-Solomon decoders (the Chien search)
---

Chien search finds the error positions in a [BCH](/bch-code/) or [Reed-Solomon](/reed-solomon-decoding/) decoder. The error locator $\Lambda(x) = \prod_k (1 - X_k x)$ has the roots $X_k^{-1}$, where $X_k = \alpha^{i_k}$ marks an error at position $i_k$. So position $i$ is in error exactly when $\Lambda(\alpha^{-i}) = 0$. Chien search tests $i = 0, 1, \ldots, n-1$ in turn. It keeps one register for each coefficient of $\Lambda$, and from one position to the next it multiplies register $j$ by the fixed constant $\alpha^{-j}$. A step costs $t$ constant multiplications and $t$ additions, which are simple circuits in hardware.

## In plain words

The decoder has a polynomial whose roots tell where the errors are. The roots must be among a short list of known values, one for each position in the block. So the search tries every value on the list. To try the next value, it does not compute the polynomial again from the start. It keeps each term of the polynomial in its own cell, and multiplies each cell by its own fixed number. Then the sum of the cells is the value of the polynomial at the next point. When the sum is zero, that position has an error. In hardware, each cell is a small fixed circuit, and one position is tested per clock tick.

## The algorithm

The input is $\Lambda(x) = \Lambda_0 + \Lambda_1 x + \cdots + \Lambda_\nu x^\nu$ over $\mathrm{GF}(q)$, with $\nu \le t$, a primitive element $\alpha$, and the code length $n \le q - 1$.

```pseudo id=main
CHIEN-SEARCH(Λ_0 .. Λ_ν, n)         ▷ the positions i with Λ(α^(−i)) = 0
L1  for j ← 0 to ν do T_j ← Λ_j
L2  roots ← empty list
L3  for i ← 0 to n − 1 do
L4      if T_0 + T_1 + … + T_ν = 0 then append i to roots
L5      for j ← 1 to ν do T_j ← T_j · α^(−j)
L6  return roots
```

At the test of line L4 in step $i$, register $T_j$ holds $\Lambda_j \alpha^{-ij}$, so the sum is $\Lambda(\alpha^{-i})$. Line L5 moves each register to the next point. The constants $\alpha^{-j}$ do not depend on $\Lambda$, so each multiplier is a fixed linear map of $m$ bits over $\mathrm{GF}(2^m)$, a small XOR network.

A decoder then checks the count. If $\Lambda$ came from at most $t$ errors, it has exactly $\nu = \deg \Lambda$ distinct roots among the positions. If the search finds fewer, the received word has more errors than the code can correct, and the decoder reports a failure.

## Example

Over $\mathrm{GF}(16)$ with $\alpha$ a root of $x^4 + x + 1$, take $\Lambda(x) = 1 + \alpha^{12} x + \alpha^9 x^2$, the locator that the [Berlekamp-Massey](/berlekamp-massey/) page finds for RS(15, 11) with two errors. Then $T_1$ is multiplied by $\alpha^{-1}$ and $T_2$ by $\alpha^{-2}$ at each step.

| $i$ | $T_1 = \alpha^{12 - i}$ | $T_2 = \alpha^{9 - 2i}$ | $\Lambda(\alpha^{-i}) = 1 + T_1 + T_2$ |
|---|---|---|---|
| 0 | $\alpha^{12}$ | $\alpha^{9}$ | $\alpha^{2}$ |
| 1 | $\alpha^{11}$ | $\alpha^{7}$ | $\alpha^{2}$ |
| 2 | $\alpha^{10}$ | $\alpha^{5}$ | **0** |
| 3 | $\alpha^{9}$ | $\alpha^{3}$ | $\alpha^{4}$ |
| 4 | $\alpha^{8}$ | $\alpha$ | $\alpha^{5}$ |
| 5 | $\alpha^{7}$ | $\alpha^{14}$ | $\alpha^{4}$ |
| 6 | $\alpha^{6}$ | $\alpha^{12}$ | $\alpha$ |
| 7 | $\alpha^{5}$ | $\alpha^{10}$ | **0** |
| 8 to 14 | | | nonzero |

The search returns the positions 2 and 7, two roots for $\nu = 2$, so the decoder goes on to the [Forney algorithm](/forney-algorithm/) for the error values. At $i = 2$, for example, $1 + \alpha^{10} + \alpha^5 = 0001 + 0111 + 0110 = 0000$, with the bits written as the coefficients of $\alpha^3, \alpha^2, \alpha, 1$.

## Correctness

The invariant is that $T_j = \Lambda_j \alpha^{-ij}$ for all $j$ at the test of step $i$. Line L1 makes it true for $i = 0$, and line L5 multiplies $T_j$ by $\alpha^{-j}$, which gives $\Lambda_j \alpha^{-(i+1)j}$. So line L4 tests $\Lambda(\alpha^{-i}) = 0$ for each $i$ exactly once. Since $\alpha$ has order $q - 1 \ge n$, the points $\alpha^{-i}$ for $0 \le i < n$ are distinct, and the list of roots is complete within the code positions. The full proof is in [proofs/correctness.md](proofs/correctness.md).

## Complexity

The search does $n$ steps. Each step does $\nu$ multiplications by constants and $\nu$ additions, so the time is $\Theta(n t)$ field operations and the extra space is $\Theta(t)$ registers. Horner's rule at each point also uses $\Theta(n t)$ operations, but with general multiplications. A constant multiplier in $\mathrm{GF}(2^m)$ is a fixed $m \times m$ bit matrix, much smaller than a general multiplier, so the Chien search is the cheap choice in hardware. In a software decoder with log tables, register $j$ can hold the logarithm of $T_j$, and line L5 is an addition of $-j$ modulo $q - 1$.

For long codes with few roots, other methods are faster in theory: [multipoint evaluation](/multipoint-evaluation/) or additive FFTs evaluate $\Lambda$ at all $n$ points in $O(n \log^2 n)$ or fewer operations, and root finding by factorization, such as [Cantor-Zassenhaus](/cantor-zassenhaus-algorithm/), does not touch every position.

## Properties

- **Online.** The positions come out in order $0, 1, 2, \ldots$, one per step. A decoder that sends the highest power first can run the search in reverse, from position $n - 1$ down, with multipliers $\alpha^{j}$, and correct each symbol as it leaves the buffer.
- **Fixed multipliers.** The constants depend only on $j$ and the field, not on the received word.
- **Exact.** It finds every root of $\Lambda$ of the form $\alpha^{-i}$ with $0 \le i < n$, and no other values.

## Variants and improvements

- **Early stop.** Stop when $\nu$ roots have been found. The worst case does not change.
- **Shortened codes.** For a code shortened to length $n < q - 1$, only positions $0, \ldots, n - 1$ exist, and the loop of line L3 stops at $n - 1$. A root at a position $\ge n$ means a decoder failure. If the decoder must start at the top position, it initializes $T_j \leftarrow \Lambda_j \alpha^{-j(n-1)}$ and multiplies by $\alpha^{j}$.
- **Parallel search.** Test $p$ positions per clock with $p$ banks of multipliers by $\alpha^{-j}, \alpha^{-2j}, \ldots, \alpha^{-pj}$.
- **Binary BCH codes.** The error values are all 1, so the decoder flips the bit at each root and needs no Forney step.
- **Roots at $\alpha^{i}$.** Some texts use the reversed locator $\sigma(x) = \prod_k (x - X_k)$ and test $\sigma(\alpha^{i}) = 0$; the registers then multiply by $\alpha^{j}$.

## When to use it

Use the Chien search in every hardware Reed-Solomon or BCH decoder, and in software decoders for codes of length up to a few thousand. It needs no root finding theory, works for any $\Lambda$, and its cost is small next to the syndrome computation, which is also $\Theta(n t)$. For very long codes with few errors, use a root finding method that does not visit every position.

## Pitfalls

- **Wrong point.** Line L4 tests $\Lambda(\alpha^{-i})$, not $\Lambda(\alpha^{i})$, because the roots of $\Lambda = \prod (1 - X_k x)$ are the inverses $X_k^{-1}$. With $\alpha^{i}$, the decoder finds position $n - i$ instead of $i$ when $n = q - 1$.
- **Forgetting $T_0$.** The sum of line L4 includes $T_0 = \Lambda_0$, which never changes. If $\Lambda$ is not normalized to $\Lambda_0 = 1$, use the true $\Lambda_0$.
- **No count check.** A word with more than $t$ errors can give a $\Lambda$ with fewer than $\deg \Lambda$ roots in the field, or roots outside a shortened code. Without the check after line L6, the decoder changes the wrong symbols and does not report the failure.
- **Position numbering.** Position $i$ is the coefficient of $x^i$. A standard that sends the highest power first, as QR codes and CCSDS do, numbers the symbols in the other direction.

## Implementations

## History

Robert T. Chien published the search in 1964 in a paper on cyclic decoding procedures for BCH codes. His contribution was a circuit that does this with one set of fixed multipliers and one position per clock cycle, in step with the cyclic shift of the received word. The method became the standard root search of BCH and Reed-Solomon decoders.

## References
