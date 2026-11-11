---
tag: 7N5369
kind: algorithm
slug: miller-algorithm
name: Miller's algorithm
aliases:
- Miller pairing algorithm
area: cryptography/public-key
level: research
summary: "Evaluates the function f with divisor r(P) - (rP) - (r-1)(O) at a point by double-and-add over lines and verticals. It is the core loop of the Weil, Tate and ate pairings."
model: word-ram
complexity:
  vars: {n: the number of binary digits of r, b: the number of binary digits of p, k: the embedding degree}
  time: {worst: Θ(n·k^2·b^2 + k^3·b^3), average: Θ(n·k^2·b^2 + k^3·b^3), best: Θ(n·k^2·b^2 + k^3·b^3)}
  space: {extra: Θ(k·b)}
properties: {deterministic: true, randomized: false}
history:
  year: 1986
  people: [Victor S. Miller]
  note: Written in 1986 as an unpublished IBM note, Short programs for functions on curves, and published in the Journal of Cryptology in 2004.
prereqs: [bilinear-pairing, elliptic-curve-cryptography, binary-exponentiation]
see_also: [menezes-okamoto-vanstone-reduction, bilinear-diffie-hellman, boneh-franklin-ibe, bls-signature, modular-exponentiation, elliptic-curve-discrete-logarithm-problem]
sources:
  - paper: "Victor S. Miller, Short programs for functions on curves, unpublished manuscript, IBM Thomas J. Watson Research Center, 1986"
    locator: the original note with the double-and-add evaluation of functions with a given divisor
  - paper: "Victor S. Miller, The Weil pairing, and its efficient calculation, Journal of Cryptology 17(4), 2004, pages 235 to 261"
    locator: the published version, with the line and vertical functions, the recurrence f_(i+j) = f_i f_j l / v, the algorithm, the normalized Weil pairing (-1)^r f_(r,P)(Q)/f_(r,Q)(P), and its cost
  - paper: "Paulo S. L. M. Barreto, Hae Y. Kim, Ben Lynn and Michael Scott, Efficient algorithms for pairing-based cryptosystems, Crypto 2002, LNCS 2442, pages 354 to 368"
    locator: denominator elimination for even embedding degree and other speedups of the Tate pairing
  - paper: "Florian Hess, Nigel P. Smart and Frederik Vercauteren, The Eta pairing revisited, IEEE Transactions on Information Theory 52(10), 2006, pages 4595 to 4602"
    locator: the ate pairing, with a shorter Miller loop on ordinary curves
  - paper: "Frederik Vercauteren, Optimal pairings, IEEE Transactions on Information Theory 56(1), 2010, pages 455 to 461"
    locator: optimal ate pairings, with a Miller loop of about log2(r)/φ(k) steps
  - paper: "Michael Scott, Naomi Benger, Manuel Charlemagne, Luis J. Dominguez Perez and Ezekiel J. Kachisa, On the final exponentiation for calculating pairings on ordinary elliptic curves, Pairing 2009, LNCS 5671, pages 78 to 88"
    locator: the split of the final exponentiation into an easy part with Frobenius maps and a hard part
  - book: isbn:9781420071467
    title: Lawrence C. Washington, Elliptic Curves, Number Theory and Cryptography, second edition, Chapman and Hall/CRC, 2008
    locator: Chapter 11 (divisors, the Weil and Tate-Lichtenbaum pairings, and the computation of pairings with Miller's algorithm)
---

Miller's algorithm evaluates, at a point $Q$, the rational function $f_{r,P}$ on an elliptic curve whose divisor is $r(P) - ([r]P) - (r-1)(\mathcal{O})$. The degree of this function is about $r$, which in cryptography has 255 binary digits, so it cannot be written out. Victor Miller found in 1986 that it can be evaluated in $O(\log r)$ steps by the same double-and-add pattern as [binary exponentiation](/binary-exponentiation/), multiplying in one line function at each step. This made the Weil and Tate pairings computable. It made the [MOV reduction](/menezes-okamoto-vanstone-reduction/) practical, and later every [pairing-based](/bilinear-pairing/) scheme. The reduced Tate pairing is one Miller loop followed by a final exponentiation.

**Notation.** $E$ is an elliptic curve $y^2 = x^3 + ax + b$ over $\mathbb{F}_p$, $\mathcal{O}$ its point at infinity, and $r$ a prime with $P \in E(\mathbb{F}_p)$ of order $r$. $k$ is the embedding degree (the smallest $k$ with $r \mid p^k - 1$) and $Q \in E(\mathbb{F}_{p^k})$. For points $T$ and $U$, $\ell_{T,U}$ is the line through $T$ and $U$ (the tangent if $T = U$), and $v_V$ is the vertical line $x - x_V$ through $V$, with $v_{\mathcal{O}} = 1$. $f_{j,P}$ is the function with divisor $j(P) - ([j]P) - (j-1)(\mathcal{O})$. $r = (r_t \ldots r_1 r_0)$ in binary with $r_t = 1$; $n = t + 1$ is its number of binary digits.

## In plain words

On an elliptic curve, a pairing needs the value at one point of a function built from another point. This function is huge: written as a polynomial it would have as many terms as the group has elements. Miller's algorithm never writes it down. It builds the value step by step, the way fast exponentiation builds a large power by squaring and multiplying.

At each step the algorithm doubles a running point, or adds the base point to it, as in normal point multiplication. The line drawn through the points for that addition is evaluated at the second point, and the value is multiplied into a running product. After as many steps as the order has binary digits, the product is the value of the huge function. One more exponentiation turns it into the pairing value.

## The problem

Given $P$ of order $r$, a point $Q$, and the curve, compute $f_{r,P}(Q)$, and from it the reduced Tate pairing $t_r(P, Q) = f_{r,P}(Q)^{(p^k - 1)/r}$ (or the Weil pairing, which needs two Miller loops). The function $f_{r,P}$ exists because $r(P) - r(\mathcal{O})$ is a principal divisor: its degree is 0 and its sum is $rP = \mathcal{O}$. It is determined up to a constant factor, which the final exponentiation removes for the Tate pairing.

## The algorithm

```pseudo id=main
MILLER(P, Q, r)                          ▷ r = (r_t … r_0) in binary, r_t = 1
L1  T ← P; f ← 1
L2  for j ← t − 1 down to 0
L3      f ← f² · ℓ_(T,T)(Q) / v_(2T)(Q)          ▷ tangent at T over the vertical at 2T
L4      T ← 2T
L5      if r_j = 1 then
L6          f ← f · ℓ_(T,P)(Q) / v_(T+P)(Q)      ▷ chord through T and P; vertical if T = −P
L7          T ← T + P
L8  return f                              ▷ f = f_(r,P)(Q) and T = rP = O

REDUCED-TATE(P, Q)
L9  return MILLER(P, Q, r)^((p^k − 1)/r)
```

The loop keeps the invariant that, after the bits $r_t \ldots r_j$ are read, $T = [m]P$ and $f = f_{m,P}(Q)$ for $m = (r_t \ldots r_j)_2$. Doubling uses $f_{2m,P} = f_{m,P}^2 \cdot \ell_{T,T} / v_{2T}$, and adding $P$ uses $f_{m+1,P} = f_{m,P} \cdot \ell_{T,P}/v_{T+P}$. A line $\ell$ is $y - y_T - \lambda(x - x_T)$ with the slope $\lambda$ of the point addition, so each step costs a point operation and a few multiplications in $\mathbb{F}_{p^k}$.

**Denominator elimination.** If $k$ is even and $x_Q \in \mathbb{F}_{p^{k/2}}$, every value $v_V(Q) = x_Q - x_V$ lies in $\mathbb{F}_{p^{k/2}}$. Then $p^{k/2} - 1$ divides $(p^k - 1)/r$, so the final exponentiation sends these values to 1, and lines L3 and L6 may skip the divisions. For $k = 2$ and $Q = (-x, iy)$ on $y^2 = x^3 + x$, $x_Q \in \mathbb{F}_p$. For $y^2 = x^3 + 1$ with the distortion map $(x, y) \mapsto (\zeta x, y)$, $x_Q \notin \mathbb{F}_p$ and the denominators must stay; the tests check both cases.

**Final exponentiation for $k = 2$.** $(p^2 - 1)/r = (p - 1) \cdot (p + 1)/r$, and $f^{p-1} = f^p / f = \bar{f}/f$, because the Frobenius map $f \mapsto f^p$ is conjugation $a + bi \mapsto a - bi$ on $\mathbb{F}_p[i]$. So the final exponentiation is one conjugation, one inversion and a power with an exponent of about $b - n$ binary digits.

## Example

Take $E : y^2 = x^3 + x$ over $\mathbb{F}_{59}$. It has 60 points, $r = 5$, and $k = 2$ because $5 \mid 59^2 - 1$ but $5 \nmid 59 - 1$. Let $P = (25, 29)$, of order 5: $2P = (35, 28)$, $3P = (35, 31)$, $4P = (25, 30) = -P$. Let $Q = (-25, 29i) = (34, 29i)$, the image of $P$ under the distortion map. In binary $r = 101$, so the loop reads the bits 0 and 1.

| line | computation | value |
|---|---|---|
| L1 | $T = P$, $f = 1$ | |
| L3 (bit 0) | tangent at $P$: $\lambda = (3 \cdot 25^2 + 1)/(2 \cdot 29) = 12$; $\ell_{P,P}(Q) = 29i - 29 - 12(34 - 25)$ | $40 + 29i$ |
| L3 | $v_{2P}(Q) = 34 - 35$ | $58$ |
| L3, L4 | $f = (40 + 29i)/58$, $T = 2P$ | $f = 19 + 30i$ |
| L3 (bit 1) | tangent at $2P$: $\lambda = 53$; $\ell_{2P,2P}(Q) = 29i - 28 - 53(34 - 35)$ | $25 + 29i$ |
| L3 | $v_{4P}(Q) = 34 - 25$ | $9$ |
| L3, L4 | $f = (19 + 30i)^2 (25 + 29i) / 9$, $T = 4P$ | $f = 28 + 27i$ |
| L6 | $4P = -P$, so $\ell_{4P,P}$ is the vertical $x - 25$: $34 - 25$; $v_{\mathcal{O}} = 1$ | $9$ |
| L6, L7, L8 | $f = (28 + 27i) \cdot 9$, $T = \mathcal{O}$ | $f_{5,P}(Q) = 16 + 7i$ |
| L9 | $(16 + 7i)^{696}$, since $(59^2 - 1)/5 = 696$ | $t_5(P, Q) = 42 + 40i$ |

Without the denominators the loop returns $26 + 4i$ instead of $16 + 7i$, and $(26 + 4i)^{696}$ is also $42 + 40i$. The powers of $42 + 40i$ are $42 + 40i$, $46 + 56i$, $46 + 3i$, $42 + 19i$ and $1$, so the value has order 5. Bilinearity gives $t_5(2P, Q) = t_5(P, 2Q) = 46 + 56i$, and the normalized Weil pairing $e_5(P, Q) = -f_{5,P}(Q)/f_{5,Q}(P)$ is also $46 + 56i$ here.

## Correctness

The line $\ell_{T,U}$ meets $E$ in $T$, $U$ and $-(T+U)$ and has a pole of order 3 at $\mathcal{O}$, so $\mathrm{div}(\ell_{T,U}) = (T) + (U) + (-(T+U)) - 3(\mathcal{O})$. The vertical $v_V$ has $\mathrm{div}(v_V) = (V) + (-V) - 2(\mathcal{O})$. Hence $\mathrm{div}(\ell_{T,U}/v_{T+U}) = (T) + (U) - (T+U) - (\mathcal{O})$. With $T = [i]P$ and $U = [j]P$, adding the divisors of $f_{i,P}$ and $f_{j,P}$ gives exactly the divisor of $f_{i+j,P}$, so $f_{i+j,P} = f_{i,P} f_{j,P} \ell_{[i]P,[j]P}/v_{[i+j]P}$ up to a constant. Lines L3 and L6 are this rule for $i = j = m$ and for $j = 1$ (with $f_{1,P} = 1$). By induction over the bits, line L8 returns $f_{r,P}(Q)$. The proof file gives the full argument, the condition on $Q$, and the proofs of denominator elimination and of the final exponentiation for $k = 2$.

## Complexity

The loop runs $n - 1$ times, with one doubling in each and one addition for each 1 bit after the first. Each step is a point operation in $\mathbb{F}_p$ (one inversion for affine coordinates, or none with projective coordinates), a line evaluation, and one squaring and one or two multiplications in $\mathbb{F}_{p^k}$. A multiplication in $\mathbb{F}_{p^k}$ costs $O(k^2)$ multiplications in $\mathbb{F}_p$ with schoolbook arithmetic, and one in $\mathbb{F}_p$ costs $\Theta(b^2)$ bit operations, so the loop costs $\Theta(n k^2 b^2)$. The final exponentiation, done as a plain power with an exponent of about $k b$ binary digits, costs $\Theta(k^3 b^3)$. Libraries split it into an easy part with Frobenius maps and a hard part that costs much less. The space is a constant number of elements of $\mathbb{F}_{p^k}$, $\Theta(k b)$ bits.

## Properties

- **Deterministic.** The output depends only on $P$, $Q$ and $r$.
- **Generic in the field.** The same loop works for any curve, any field and any $Q$, as long as $Q$ is not a zero or a pole of a line or vertical used in the loop. If $Q \in \langle P \rangle$, some step divides by 0 or the value is degenerate; this is why a Type 1 pairing evaluates at $\phi(Q)$ for a distortion map $\phi$.
- **The raw Miller value is not bilinear.** $f_{r,P}(Q)$ is defined only up to an $r$-th power of a constant and depends on the choice of divisor. The final exponentiation maps it to the unique representative in $\mu_r$, and that value is bilinear.
- **Weil versus Tate.** The Weil pairing needs two Miller loops, $f_{r,P}(Q)$ and $f_{r,Q}(P)$, the second over $\mathbb{F}_{p^k}$, and no final exponentiation. The Tate pairing needs one loop over $\mathbb{F}_p$ points and one final exponentiation, which is cheaper.

## Variants and improvements

- **Denominator elimination** (Barreto, Kim, Lynn and Scott, 2002), as above.
- **Projective coordinates and signed digits.** Points in Jacobian or projective coordinates avoid the inversion in each step, and a signed binary form of $r$ with few nonzero digits reduces the number of additions.
- **Eta, ate and optimal ate pairings.** Loops on a different integer (the trace of Frobenius minus 1, or a short vector in a lattice) replace the loop on $r$. The optimal ate pairing (Vercauteren 2010) needs about $\log_2 r / \varphi(k)$ steps, where $\varphi$ is Euler's function. For BLS12-381 the loop runs on a parameter $|x|$ of 64 binary digits instead of $r$ of 255.
- **Twists.** On BN and BLS12 curves, $Q$ lives on a sextic twist over $\mathbb{F}_{p^2}$, so most of the arithmetic is in $\mathbb{F}_{p^2}$, not in $\mathbb{F}_{p^{12}}$.
- **Multi-pairings.** A product $\prod_i e(P_i, Q_i)$ shares one squaring of $f$ per step and one final exponentiation for all the factors. Signature verification uses this.

## When to use it

Miller's algorithm is inside every pairing library; applications call the pairing, not the loop. Use a maintained library for a standard curve, for example blst or MCL for BLS12-381, or arkworks, gnark or RELIC. Write the loop yourself only to learn it, or when you need an unusual curve for research. Then test bilinearity and non-degeneracy on random points, and compare the fast final exponentiation with the plain power, as the tests here do.

## Pitfalls

- **Dropping denominators when not allowed.** Denominator elimination needs $x_Q$ in a proper subfield that the final exponentiation kills. On $y^2 = x^3 + 1$ with $Q = (\zeta x, y)$, dropping them gives a wrong value; the tests show it.
- **Forgetting the final exponentiation.** The Miller value alone is not well defined and not bilinear.
- **The last step.** At the last addition $T = -P$, the line is vertical and $T + P = \mathcal{O}$. Code that computes a slope there divides by zero.
- **Inputs outside the subgroup.** A point not of order $r$, or a point on a twist, gives values outside $\mu_r$ and can leak secrets in protocols. Check that inputs lie in $\mathbb{G}_1$ and $\mathbb{G}_2$.
- **Side channels.** The loop on a public $r$ has a fixed pattern, but the field arithmetic must still be constant time when $P$ or $Q$ is secret, as in identity-based decryption.
- **Toy curves.** The curves of the example and the code ($p = 59$, and $p$ of 128 binary digits) are not secure.

## Implementations

The Python code implements the Miller loop on $y^2 = x^3 + ax + b$ with $P \in E(\mathbb{F}_p)$ and $Q \in E(\mathbb{F}_{p^2})$, with and without denominators, the reduced Tate pairing with the fast and the plain final exponentiation, and the normalized Weil pairing. It is for study only, it is not constant time, and it must not protect real data; use blst or MCL instead. There are no official test vectors for these toy curves. The tests check the example above step by step, bilinearity on all pairs of the curve over $\mathbb{F}_{59}$, the curve $y^2 = x^3 + 1$ with and without denominators, and bilinearity, non-degeneracy and the Weil pairing on the 128-binary-digit toy curve of the [bilinear pairing](/bilinear-pairing/) page, with fixed seeds.

## History

Weil defined his pairing in 1940 and used it in the theory of abelian varieties, but no efficient way to compute it was known. Miller's 1986 note, written while he was at IBM, gave the double-and-add evaluation. The note was cited for years but not published, and it appeared in the Journal of Cryptology in 2004. Menezes, Okamoto and Vanstone (1993) and Frey and Rück (1994) used the algorithm to attack the discrete logarithm on curves with small embedding degree. From 2000, Joux's three-party key agreement and Boneh and Franklin's identity-based encryption turned it into a building block. The ate and optimal ate pairings of Hess, Smart, Vercauteren and others from 2006 shortened the loop.

## References
