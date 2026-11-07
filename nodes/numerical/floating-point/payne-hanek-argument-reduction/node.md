---
tag: H4GFMJ
kind: algorithm
slug: payne-hanek-argument-reduction
name: Payne-Hanek argument reduction
aliases:
- Payne-Hanek reduction
- Payne-Hanek range reduction
- radian reduction
area: numerical/floating-point
level: research
summary: Accurate reduction of very large arguments modulo π/2 using high-precision bits of 2/π.
model: floating-point-model
complexity:
  vars: {n: "the precision of the result in bits (53 for binary64), with the window of 2/π a fixed multiple of n"}
  time: {worst: Θ(n^2), average: Θ(n^2), best: Θ(1)}
  space: {extra: Θ(n)}
properties: {deterministic: true, recursive: false, in_place: false}
history:
  year: 1983
  people: [Mary H. Payne, Robert N. Hanek]
  note: Payne and Hanek published the method in 1983 from their work on the DEC VAX math library. K. C. Ng's 1992 fdlibm code made it the standard in Unix libraries.
prereqs: [cody-waite-range-reduction, floating-point-model, ulp]
see_also: [correctly-rounded-elementary-functions, correctly-rounded-functions, double-double-arithmetic, catastrophic-cancellation, table-maker-dilemma, big-integer, error-free-transformations]
sources:
  - paper: doi:10.1145/1057600.1057602
    title: Mary H. Payne and Robert N. Hanek, Radian reduction for trigonometric functions, ACM SIGNUM Newsletter 18(1) (1983), 19-24
    locator: the observation that only a window of bits of 2/π affects the result, and the multi-word product
  - paper: "K. C. Ng, Argument reduction for huge arguments: good to the last bit, technical report, SunPro, 1992"
    title: K. C. Ng, Argument reduction for huge arguments, good to the last bit
    locator: the fdlibm design with 24-bit chunks of 2/π, and the bound on how close a binary64 number can come to a multiple of π/2
  - book: "Jean-Michel Muller, Elementary Functions, Algorithms and Implementation, third edition, Birkhauser, 2016"
    title: Jean-Michel Muller, Elementary Functions, Algorithms and Implementation, third edition (2016)
    locator: Chapter 11, Range reduction (the Payne and Hanek method, and the worst cases of reduction modulo π/2 found with Kahan's continued-fraction method, including 6381956970095103 × 2^797)
  - book: isbn:9783319765259
    title: Jean-Michel Muller et al., Handbook of Floating-Point Arithmetic, second edition, Birkhauser, 2018
    locator: Chapter 10, Evaluating Floating-Point Elementary Functions (range reduction for large arguments)
  - url: https://www.netlib.org/fdlibm/k_rem_pio2.c
    title: Sun Microsystems, fdlibm, k_rem_pio2.c (the Payne-Hanek kernel)
    locator: the table ipio2 of 24-bit chunks of 2/π, the choice of chunks from the exponent, and the recomputation with more terms when the fraction is small
  - paper: doi:10.1109/TC.2005.36
    title: Nicolas Brisebarre, David Defour, Peter Kornerup, Jean-Michel Muller and Nathalie Revol, A new range-reduction algorithm, IEEE Transactions on Computers 54(3) (2005), 331-339
    locator: a table-based reduction for large arguments and its comparison with Payne and Hanek
---

Payne-Hanek reduction computes, for a floating-point number $x$ of any size, an integer $k$ modulo 4 and a reduced argument $r$ with $|r| \le \pi/4$ such that $x = (4j + k)\pi/2 + r$ for some integer $j$. Then $\sin x$ and $\cos x$ follow from $\sin r$ and $\cos r$. The method multiplies the integer significand of $x$ by a window of bits of $2/\pi$ that it picks from the exponent of $x$. It ignores the bits of $2/\pi$ that only add multiples of 4 and the bits too far down to matter. The product is exact integer arithmetic, so the result is accurate even when $x$ is $10^{300}$, or when $x$ is extremely close to a multiple of $\pi/2$.

## In plain words

To find where an angle lands on a circle, you divide it by a quarter turn, keep the whole number of quarter turns modulo 4, and keep the leftover part. For a huge angle the whole number of turns is enormous, but almost all of it does not matter, because full turns bring you back to the start. The trick is to multiply by the digits of "one over a quarter turn" only in the narrow band that can still change the leftover. The digits above that band only add whole turns. The digits below it are too small to change the answer. A band of a few hundred bits always suffices, however large the angle is.

## The problem

Given a finite binary64 $x$, find $k \in \{0, 1, 2, 3\}$ and $r$ with $|r| \le \pi/4$ such that $x - r$ is an integer multiple of $\pi/2$ congruent to $k$ modulo 4. Return $r$ as an unevaluated sum $r_{hi} + r_{lo}$ of two floats, accurate to about $2^{-104}|r|$.

The easy method, $k = \mathrm{round}(x \cdot \mathrm{fl}(2/\pi))$ and $r = x - k\,\mathrm{fl}(\pi/2)$, fails once $|x|$ is large. $\mathrm{fl}(\pi/2)$ is wrong by about $6 \times 10^{-17}$, and $k$ multiplies that error. [Cody-Waite reduction](/cody-waite-range-reduction/) splits $\pi/2$ into two or three floats and works up to about $|x| \approx 2^{20}$ to $2^{30}$. Beyond that the number of bits of $\pi/2$ needed grows with the exponent of $x$, up to more than 1100 bits for $x$ near $2^{1024}$. Payne and Hanek showed that those bits are needed only in a window of fixed width.

## The algorithm

Write $|x| = M \cdot 2^{E}$ with $M$ a 53-bit integer, and write $2/\pi = \sum_{i \ge 1} b_i 2^{-i}$ in binary. Then
$$
x \cdot \tfrac{2}{\pi} = \sum_{i \ge 1} b_i\, M\, 2^{E - i}.
$$
A term with $E - i \ge 2$ is a multiple of 4. It changes neither $k$ nor $r$, so the bits $b_i$ with $i \le E - 2$ are dropped. A term with $i > E + P$ adds less than $2^{53 - P}$ in total, so for a precision $P$ these bits are dropped too. What is left is the window $i_0 \le i \le i_1$, an integer $W$ of at most $P + 2$ bits.

```pseudo id=main
PAYNE-HANEK(x)                     ▷ P = 245 bits after the point, Q = 245 bits of π/2
L1  if |x| ≤ fl(π/4) then return (0, x, 0)
L2  (M, E) ← integer significand and exponent with |x| = M · 2^E
L3  i₀ ← max(1, E − 1);  i₁ ← E + P
L4  W ← bits i₀ … i₁ of 2/π, read as an integer     ▷ W = ⌊2^{i₁} · 2/π⌋ mod 2^{i₁ − i₀ + 1}
L5  Z ← M · W                                         ▷ exact integer product
L6  k ← ⌊Z / 2^P⌋ mod 4;  F ← Z mod 2^P               ▷ Z / 2^P ≈ x · 2/π mod 4
L7  if F ≥ 2^{P−1} then k ← (k + 1) mod 4;  F ← F − 2^P   ▷ fraction into [−1/2, 1/2)
L8  (r_hi, r_lo) ← F · C / 2^{P+Q} rounded to two floats  ▷ C = round(2^Q · π/2)
L9  if x < 0 then k ← (−k) mod 4;  (r_hi, r_lo) ← (−r_hi, −r_lo)
L10 return (k, r_hi, r_lo)
```

Lines L2 and L3 are cheap bit manipulations. Line L4 reads a stored table of $2/\pi$, about $971 + P$ bits for binary64. Line L5 is the only real work, a product of a 53-bit integer and an integer of at most $P + 2$ bits. Library code such as fdlibm stores $2/\pi$ in 24-bit chunks and carries out L5 as a sum of exact floating-point products. The Python implementation uses integers.

## Example

Take $x = 10^{22}$, the classic test value, which is exactly the binary64 number $M \cdot 2^{21}$ with $M = 4768371582031250$.

- L3: $i_0 = 20$ and $i_1 = 266$. The first 19 bits of $2/\pi = 0.101000101111100110000011\ldots_2$ are dropped, because each of them contributes a multiple of 4.
- L4 and L5: $W$ has 247 bit positions, and the product $Z = MW$ has 296 bits.
- L6: $\lfloor Z / 2^{245} \rfloor = 2044964875930755$, which is $3 \bmod 4$, so $k = 3$. The fraction is $F/2^{245} = 0.3505349005744814\ldots$, below $1/2$, so L7 changes nothing.
- L8: $r_{hi} = 0.5506189342358097$ and $r_{lo} = -7.985621383147488 \times 10^{-18}$.

So $\sin(10^{22}) = -\cos r = -0.8522008497671888$, which agrees with a correctly rounded library. The easy method computes $\mathrm{round}(x \cdot \mathrm{fl}(2/\pi)) \cdot \mathrm{fl}(\pi/2)$, and that rounds back to $x$ itself, so it returns $r = 0$. `math.fmod(x, math.pi/2)` is an exact remainder, but by the wrong modulus, and it returns $1.0634\ldots$.

The hardest binary64 input is $x = 6381956970095103 \cdot 2^{797} \approx 5.32 \times 10^{255}$. It is the binary64 number closest to a multiple of $\pi/2$ (Muller 2016, Chapter 11). The algorithm returns $k = 1$ and $r_{hi} = 4.687165924254628 \times 10^{-19} \approx 2^{-60.9}$. A reduction carried out with only 53 bits of the fraction would have lost every bit of this $r$.

## Correctness

Let $T = \sum_{i \in [i_0, i_1]} b_i M 2^{E - i} = Z / 2^{P}$, the window part of $x \cdot 2/\pi$. The dropped head is a multiple of 4. The dropped tail $C'$ satisfies $0 \le C' < M 2^{E - i_1} < 2^{53 - P}$. So $x \cdot 2/\pi = 4j + k + \varphi + C'$, where $\varphi = F/2^{P} \in [-1/2, 1/2)$ after L7. Multiplying by $\pi/2$ gives $|x| - (4j + k)\pi/2 = (\varphi + C')\pi/2$. Line L8 approximates this by $\varphi\,C/2^{Q}$, and the error is at most $2^{53 - P}\pi/2 + 2^{-Q-2}$. The value of $k$ is exact, because the $k$ returned always matches the reduced value returned. Even when $\varphi$ is near $\pm 1/2$ and a more precise computation would pick the neighbouring quadrant, the pair $(k, r)$ still satisfies the equation up to the error bound. Line L9 uses the symmetry $-x = (4(-j) - k)\pi/2 - r$. The full proof is in [proofs/correctness.md](proofs/correctness.md).

With $P = Q = 245$, the absolute error before the final rounding is below $2^{-190}$. That alone is not a relative bound. It becomes one through a separate fact: no binary64 number lies closer than about $2^{-61}$ to a nonzero multiple of $\pi/2$ (Ng 1992; Muller 2016, Chapter 11). So the relative error is below $2^{-128}$ before rounding, and $r_{hi} + r_{lo}$ is within about $2^{-106}|r|$ of $r$. This is a proved bound that depends on the cited worst-case search. The tests compare the result on random arguments, on floats next to $n\pi/2$ for $n < 400$, and on the worst case above against a reference that uses 2600 bits of $\pi$ from a different formula. They find $k$ always exact and $r_{hi}$ always equal to the correctly rounded $r$. That last part is observed, not proved.

## Complexity

The window has $P + 2$ bits with $P$ a fixed multiple of the target precision $n$, so line L5 is one $n \times \Theta(n)$ integer product. Schoolbook multiplication takes $\Theta(n^2)$ word operations. For binary64 this is a constant amount of work, a few dozen products of 24-bit chunks in fdlibm. The best case is the early exit of L1. The extra space is the window and the product, $\Theta(n)$ bits. The stored table of $2/\pi$ has about $e_{\max} + P$ bits. It is a constant of the format, and it is not counted as working space.

## Properties

- **Exact quadrant.** $k$ is consistent with $r$ for every finite input, with no condition on the size of $x$.
- **Fixed window.** The work does not grow with $|x|$. Only the position of the window in the table of $2/\pi$ moves.
- **Independent of the rounding mode.** Lines L2 to L7 are integer operations. Only the final conversion in L8 rounds.
- **Not a floating-point algorithm in the standard model.** The [standard model](/floating-point-model/) cannot express it, since it relies on the exact bit structure of $x$. The error bound is proved by integer arithmetic, not by $|\delta| \le u$ arguments.
- **Deterministic and branch-light.** There are two branches, the early exit and the fold of the fraction into $[-1/2, 1/2)$.

## Variants and improvements

- **Adaptive window (fdlibm).** Start with a few chunks beyond the 53 needed. Add chunks only if the fraction comes out small, since a small fraction means cancellation ate the leading bits. Most arguments need no extra chunks.
- **Floating-point chunks.** Store $2/\pi$ as floats with 24 or 26 bits each. Then every chunk product with $M$ split into halves is exact, and the sum can be done in [double-double arithmetic](/double-double-arithmetic/). This is how C libraries implement L5 without big integers.
- **Reduction modulo $\pi/4$ or $\pi/8$.** Keep one or two more integer bits, giving $k \bmod 8$ or $k \bmod 16$, so that the polynomial for $\sin r$ covers a smaller interval.
- **Cody-Waite first.** Libraries test the size of $x$ and use [Cody-Waite reduction](/cody-waite-range-reduction/), which is cheaper, up to some threshold like $2^{20}\pi/2$. They switch to Payne-Hanek only above it.
- **Table-based methods.** Brisebarre et al. (2005) precompute $2^{i}\pi/2 \bmod \pi/2$ for the exponents that occur. The reduction then becomes a small fixed sum of table entries, which suits hardware.

## When to use it

Use Payne-Hanek in any trigonometric function that claims accuracy for all inputs, in particular in [correctly rounded elementary functions](/correctly-rounded-elementary-functions/) and in libraries that conform to IEEE 754-2019's recommended correctly rounded operations. It is also the right tool for any reduction modulo an irrational constant where the argument can be large: reduction modulo $\ln 2$ never needs it, because $\exp$ overflows long before the argument is large.

## Pitfalls

- **Not enough bits of $2/\pi$.** The window has to reach $E + P$, so the table needs about $1024 + P$ bits for binary64. A table that is too short gives wrong results only for the largest exponents, which random testing rarely hits.
- **Too narrow a window.** $P = 53 + 53$ bits is not enough. Near the worst case, cancellation removes about 61 leading bits of the fraction. That is why fdlibm recomputes with more chunks when the fraction is small.
- **Using `fmod` with `math.pi/2`.** This gives an exact remainder by the wrong number.
- **Forgetting the sign.** Reducing $|x|$ and then forgetting to negate both $k$ and $r$ gives the wrong quadrant for negative arguments.
- **Arguments in degrees.** Reduction of degrees modulo 90 is exact, because `fmod` is exact and 90 is a float. Do not convert to radians first and then reduce, or the conversion error is multiplied by the size of the argument.

## Implementations

## History

Before 1983 most libraries reduced with a two- or three-part constant, following Cody and Waite (1980), and returned garbage or an error for large arguments. Mary Payne and Robert Hanek, working on the VAX math library at Digital Equipment Corporation, published the window method in 1983. W. Kahan had found a continued-fraction method to search for the floating-point numbers closest to multiples of $\pi/2$. It showed that a fixed, modest number of extra bits suffices for each format. K. C. Ng's 1992 fdlibm code combined Payne-Hanek with that bound and with adaptive chunk counts, and was copied into many C libraries. Muller's book on elementary functions tabulates the worst cases for binary32, binary64 and wider formats.

## References
