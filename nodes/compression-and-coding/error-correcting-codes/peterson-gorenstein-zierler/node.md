---
tag: 7Z5YDC
kind: algorithm
slug: peterson-gorenstein-zierler
name: Peterson-Gorenstein-Zierler algorithm
aliases:
- PGZ decoder
- Peterson decoder
- Gorenstein-Zierler decoder
area: compression-and-coding/error-correcting-codes
level: advanced
summary: Decode Reed-Solomon and BCH codes by solving a Hankel syndrome system for the error locator, then a Vandermonde system for the error values.
solves: [reed-solomon-decoding]
model: word-ram
complexity:
  vars: {n: the code length, t: the number of correctable errors}
  time: {worst: Θ(n t + t^4), average: Θ(n t + t^4), best: Θ(n t + t^3)}
  space: {extra: Θ(t^2)}
properties: {deterministic: true, recursive: false, online: false}
history:
  year: 1960
  people: [W. Wesley Peterson, Daniel Gorenstein, Neal Zierler]
  note: Peterson gave the first algebraic decoder for binary BCH codes in 1960; Gorenstein and Zierler extended it to nonbinary codes, with the error values, in 1961.
prereqs: [reed-solomon-decoding, gaussian-elimination]
see_also: [berlekamp-massey, chien-search, forney-algorithm, bch-code, reed-solomon-code, vandermonde-matrix, determinant, syndrome]
sources:
  - paper: doi:10.1109/TIT.1960.1057586
    title: W. W. Peterson, Encoding and error-correction procedures for the Bose-Chaudhuri codes, IRE Transactions on Information Theory 6(4), 1960
    locator: pp. 459 to 470 (the error locator from a system of linear equations in the syndromes, with the number of errors found by a determinant test)
  - paper: doi:10.1137/0109020
    title: D. Gorenstein and N. Zierler, A class of error-correcting codes in p^m symbols, Journal of the Society for Industrial and Applied Mathematics 9(2), 1961
    locator: pp. 207 to 214 (the nonbinary codes, and the error values from a second linear system)
  - book: isbn:9780130426727
    title: Shu Lin and Daniel J. Costello, Jr., Error Control Coding, second edition, Pearson Prentice Hall, 2004
    locator: Chapter 6 (decoding of BCH codes) and Chapter 7 (nonbinary BCH and Reed-Solomon codes)
  - book: isbn:9780521845045
    title: Ron M. Roth, Introduction to Coding Theory, Cambridge University Press, 2006
    locator: Chapter 6 (decoding of generalized Reed-Solomon codes, the Peterson-Gorenstein-Zierler algorithm)
---

The Peterson-Gorenstein-Zierler (PGZ) algorithm was the first algebraic decoder for [BCH](/bch-code/) and [Reed-Solomon](/reed-solomon-code/) codes. It turns the [syndromes](/syndrome/) into two linear systems. The first is a Hankel system $M_\nu \Lambda = -S$ whose solution is the error locator $\Lambda(x)$. The number of errors $\nu$ is not known, so the decoder starts with $\nu = t$ and reduces $\nu$ until $M_\nu$ is nonsingular. The roots of $\Lambda$ give the error positions, and the second system, a [Vandermonde](/vandermonde-matrix/) system, gives the error values. With [Gaussian elimination](/gaussian-elimination/), each trial costs $O(\nu^3)$ field operations. The [Berlekamp-Massey algorithm](/berlekamp-massey/) later replaced the first system with an $O(t^2)$ method, but PGZ is still a good choice for small $t$ and is the easiest decoder to prove correct.

## In plain words

The decoder gets a short list of check values, the syndromes, from the received block. If there are no errors, they are all zero. Each error adds a known kind of pattern to them, and the patterns of different errors are independent. The decoder guesses the largest number of errors it can correct and sets up a small table of equations from the syndromes. If the guess is too large, the table has no unique answer, so the decoder tries one less. When the table has a unique answer, the answer is a polynomial that marks where the errors are. A second small table then gives how much each bad symbol must change.

## The algorithm

The code has length $n$ and the zeros $\beta^b, \beta^{b+1}, \ldots, \beta^{b+2t-1}$, where $\beta$ has order at least $n$ (usually $\beta = \alpha$). The input is the list of syndromes $S_j = r(\beta^j)$ for $b \le j \le b + 2t - 1$ of a received word $r$. For $1 \le \mu \le t$, let

$$M_\mu = \begin{pmatrix} S_b & S_{b+1} & \cdots & S_{b+\mu-1} \\ S_{b+1} & S_{b+2} & \cdots & S_{b+\mu} \\ \vdots & & & \vdots \\ S_{b+\mu-1} & S_{b+\mu} & \cdots & S_{b+2\mu-2} \end{pmatrix}.$$

```pseudo id=main
PGZ(S_b .. S_(b+2t−1), n)          ▷ error positions and values, or FAIL
L1  ν ← t
L2  while ν > 0 and M_ν is singular do ν ← ν − 1
L3  if ν = 0 then return (no errors) if every S_j = 0, else FAIL
L4  solve M_ν · (Λ_ν, …, Λ_1)ᵀ = −(S_(b+ν), …, S_(b+2ν−1))ᵀ
L5  P ← the positions i, 0 ≤ i < n, with Λ(β^(−i)) = 0, where Λ(x) = 1 + Λ_1 x + … + Λ_ν x^ν
L6  if |P| ≠ ν then return FAIL
L7  solve Σ_k Y_k X_k^(b+i) = S_(b+i) for 0 ≤ i < ν, with X_k = β^(i_k) for the positions i_k in P
L8  return the positions P and the values Y_1, …, Y_ν
```

Line L2 tests each $M_\nu$ by Gaussian elimination. The same elimination also solves line L4, so the implementation does both in one pass. Line L5 is a [Chien search](/chien-search/) or a direct evaluation at each position. Line L7 is the step of Gorenstein and Zierler; the [Forney algorithm](/forney-algorithm/) gives the same values by a formula. For binary BCH codes, every error value is 1, and line L7 is not needed.

The equations of line L4 are the Newton identities of the code: for $0 \le i < \nu$,

$$\sum_{j=0}^{\nu} \Lambda_j S_{b+i+\nu-j} = \sum_k Y_k X_k^{\,b+i+\nu} \Lambda(X_k^{-1}) = 0 .$$

## Example

Take RS(15, 11) over $\mathrm{GF}(16)$ with $\alpha^4 = \alpha + 1$, $b = 1$ and $t = 2$, as on the [Berlekamp-Massey](/berlekamp-massey/) page. Errors $\alpha^5$ at position 2 and $\alpha^{11}$ at position 7 give the syndromes $S_1, \ldots, S_4 = \alpha^4, \alpha^{13}, \alpha^9, \alpha^{10}$.

**Lines L1 and L2.** With $\nu = 2$,

$$M_2 = \begin{pmatrix} \alpha^4 & \alpha^{13} \\ \alpha^{13} & \alpha^9 \end{pmatrix}, \qquad \det M_2 = \alpha^{13} + \alpha^{26} = \alpha^{13} + \alpha^{11} = \alpha^4 \ne 0 .$$

**Line L4.** In characteristic 2, $-S = S$. By Cramer's rule on $M_2 (\Lambda_2, \Lambda_1)^\mathsf{T} = (\alpha^9, \alpha^{10})^\mathsf{T}$,

$$\Lambda_2 = \frac{S_3^2 + S_2 S_4}{\det M_2} = \frac{\alpha^{3} + \alpha^{8}}{\alpha^4} = \alpha^9, \qquad \Lambda_1 = \frac{S_1 S_4 + S_2 S_3}{\det M_2} = \frac{\alpha^{14} + \alpha^{7}}{\alpha^4} = \alpha^{12}.$$

So $\Lambda(x) = 1 + \alpha^{12} x + \alpha^9 x^2$, the same locator as Berlekamp-Massey finds.

**Lines L5 and L6.** The roots are $\alpha^{-2}$ and $\alpha^{-7}$, so $P = \{2, 7\}$, $X_1 = \alpha^2$ and $X_2 = \alpha^7$.

**Line L7.** The system is $Y_1 X_1 + Y_2 X_2 = S_1$ and $Y_1 X_1^2 + Y_2 X_2^2 = S_2$. Its determinant is $X_1 X_2 (X_1 + X_2) = \alpha^9 \cdot \alpha^{12} = \alpha^6$, and

$$Y_1 = \frac{S_1 X_2^2 + S_2 X_2}{\alpha^6} = \frac{\alpha^{3} + \alpha^{5}}{\alpha^6} = \alpha^5, \qquad Y_2 = \alpha^{11}.$$

With one error, at position 4 with value $\alpha^3$, the syndromes are $S_j = \alpha^{3 + 4j}$, so $\det M_2 = S_1 S_3 + S_2^2 = \alpha^{22} + \alpha^{22} = 0$. Line L2 reduces $\nu$ to 1, and $M_1 = (S_1)$ gives $\Lambda_1 = S_2 / S_1 = \alpha^4 = X_1$.

## Correctness

Suppose the received word has $\nu \le t$ errors with distinct locators $X_k$ and nonzero values $Y_k$. Then $S_{b+i} = \sum_k Y_k X_k^{b+i}$, and for every $\mu \le t$

$$M_\mu = V_\mu D V_\mu^{\mathsf{T}}, \qquad V_\mu = \bigl(X_k^{\,i}\bigr)_{0 \le i < \mu,\ 1 \le k \le \nu}, \qquad D = \mathrm{diag}\bigl(Y_k X_k^{\,b}\bigr).$$

For $\mu > \nu$, the rank of $M_\mu$ is at most $\nu < \mu$, so $M_\mu$ is singular. For $\mu = \nu$, $V_\nu$ is a square Vandermonde matrix with distinct nodes and $D$ has a nonzero diagonal, so $M_\nu$ is nonsingular. So line L2 stops at the true $\nu$. The coefficients of the true locator satisfy the Newton identities, so they are the unique solution of line L4. Its roots are exactly the $X_k^{-1}$, so line L5 finds the error positions and line L6 passes. The matrix of line L7 is $V_\nu$ times the nonsingular diagonal $\mathrm{diag}(X_k^b)$, so the values are unique, and they are the true $Y_k$. With $\nu = 0$, every syndrome is 0 and line L3 returns no errors. The full proof is in [proofs/correctness.md](proofs/correctness.md).

## Complexity

The syndromes cost $O(n t)$ and the search of line L5 costs $O(n \nu)$. Each trial of line L2 is one elimination on a $\mu \times \mu$ matrix, $O(\mu^3)$ operations. In the worst case, with few errors, the loop tries $\mu = t, t-1, \ldots, 1$, which is $\sum_\mu \mu^3 = \Theta(t^4)$. If $\nu = t$, it is a single trial, $\Theta(t^3)$. Line L7 is another $O(\nu^3)$ elimination. The extra space is the $t \times t$ matrix, $\Theta(t^2)$.

The loop is not the only way to find $\nu$. Since $M_t = V_t D V_t^\mathsf{T}$ with $V_t$ of full column rank $\nu$, the number of errors is the rank of $M_t$, which one elimination finds in $O(t^3)$. Then the total is $O(n t + t^3)$.

## Properties

- **Exact within the radius.** Every pattern of at most $t = \lfloor (n-k)/2 \rfloor$ errors is corrected, for any $b$ and any generator $\beta$ of the zeros.
- **Same locator as Berlekamp-Massey.** For at most $t$ errors, the Hankel system has a unique solution and Berlekamp-Massey finds the same $\Lambda$. More generally, whenever the shortest LFSR of the syndromes has length $L \le t$, line L2 stops at $\nu = L$ and both methods give the same LFSR.
- **Failure detection.** With more than $t$ errors, the solution of line L4 can have fewer than $\nu$ roots in range, or a coefficient $\Lambda_\nu = 0$. Line L6 then reports a failure. Some patterns with more than $t$ errors are decoded to a wrong codeword within distance $t$; no bounded distance decoder can detect these.
- **Binary BCH codes.** For a narrow sense binary BCH code, $S_{2j} = S_j^2$, so only the odd syndromes must be computed, and Peterson's original form uses a smaller system.

## Variants and improvements

- **Rank first.** Compute $\nu = \operatorname{rank} M_t$ by one elimination and then solve $M_\nu$, which removes the $\Theta(t^4)$ worst case.
- **Closed forms for small $t$.** For $t \le 3$, the solution of line L4 has short explicit formulas. For one error, $X_1 = S_{b+1}/S_b$; for two errors in a binary BCH code with $b = 1$, $\Lambda_1 = S_1$ and $\Lambda_2 = (S_3 + S_1^3)/S_1$. Hardware decoders for short BCH codes use these forms.
- **Forney instead of Vandermonde.** Line L7 can be replaced by the [Forney algorithm](/forney-algorithm/), $O(\nu^2)$ in place of $O(\nu^3)$.
- **Erasures.** With known erasure positions, the erasure locator can be combined into the syndromes (Forney syndromes), and the same Hankel method then finds the errors.
- **Berlekamp-Massey and Euclid.** The [Berlekamp-Massey algorithm](/berlekamp-massey/) and the Euclidean algorithm of Sugiyama et al. solve the same key equation in $O(t^2)$ without the trial loop. See [Reed-Solomon decoding](/reed-solomon-decoding/).

## When to use it

Use PGZ for codes with small $t$, about $t \le 5$, and for binary BCH codes with $t \le 3$, where the closed forms give a decoder with very small latency and no iteration. It is also a clear method to teach and to prove. For larger $t$, such as $t = 8$ in RS(255, 239) or $t = 16$ in CCSDS RS(255, 223), use Berlekamp-Massey or the Euclidean algorithm.

## Pitfalls

- **Index shift for $b \ne 1$.** The matrix starts at $S_b$, not $S_1$. Codes with $b = 0$ (QR codes) or $b = 112$ (CCSDS) need the general form, and line L7 uses $X_k^{b+i}$.
- **Order of the unknowns.** The solution vector of line L4 is $(\Lambda_\nu, \ldots, \Lambda_1)$, in reverse order. If the order is wrong, the locator is the reciprocal polynomial and the positions are wrong.
- **Singular is not the same as no errors.** If $\nu$ reaches 0, then $S_b = 0$ and no $M_\mu$ is nonsingular, but other syndromes can be nonzero. Then the word has more than $t$ errors, and the decoder must report a failure.
- **No root count check.** With more than $t$ errors, the solution of line L4 can be a polynomial with fewer roots in the field than its degree. Without line L6, the decoder changes wrong symbols.

## Implementations

## History

W. Wesley Peterson published the first decoding procedure for binary BCH codes in 1960. He showed that the error locator satisfies a linear system in the syndromes, and that the number of errors is the largest $\nu$ for which the system is nonsingular. In 1961, Daniel Gorenstein and Neal Zierler extended the codes and the decoder to alphabets of $p^m$ symbols, a class that includes the Reed-Solomon codes, and added the second linear system for the error values. Robert Chien gave the hardware root search in 1964, and Forney gave the formula for the values in 1965. In 1968 Elwyn Berlekamp replaced the matrix steps by an iterative algorithm, which Massey in 1969 recast as shift register synthesis.

## References
