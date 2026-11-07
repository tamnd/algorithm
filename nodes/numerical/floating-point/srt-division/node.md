---
tag: 732WBN
kind: algorithm
slug: srt-division
name: SRT division
aliases:
- Sweeney-Robertson-Tocher division
- SRT algorithm
area: numerical/floating-point
level: advanced
summary: Digit-recurrence division choosing quotient digits from a small lookup table, one digit per step.
model: floating-point-model
complexity:
  vars: {n: "the number of quotient digits (radix 4, so 2n quotient bits)"}
  time: {worst: Θ(n), average: Θ(n), best: Θ(n)}
  space: {extra: Θ(1)}
properties: {deterministic: true, recursive: false, in_place: false}
history:
  year: 1958
  people: [Dura W. Sweeney, James E. Robertson, Keith D. Tocher]
  note: Robertson and Tocher published redundant-digit division independently in 1958; Sweeney had developed it at IBM, and the initials of the three name the method.
prereqs: [floating-point-division, rounding-modes]
see_also: [goldschmidt-division, newton-raphson-division, long-division, round-to-nearest-even, fused-multiply-add, ieee-754]
sources:
  - paper: doi:10.1109/TEC.1958.5222579
    title: James E. Robertson, A new class of digital division methods, IRE Transactions on Electronic Computers EC-7(3) (1958), 218-222
    locator: the redundant quotient digit set and the selection of digits from a truncated partial remainder
  - paper: doi:10.1093/qjmam/11.3.364
    title: K. D. Tocher, Techniques of multiplication and division for automatic binary computers, Quarterly Journal of Mechanics and Applied Mathematics 11(3) (1958), 364-384
    locator: the division method with digits in {-1, 0, 1}
  - book: isbn:9781558607989
    title: Milos D. Ercegovac and Tomas Lang, Digital Arithmetic, Morgan Kaufmann, 2004
    locator: Chapter 5, division by digit recurrence (the recurrence, the containment and continuity conditions, radix-4 selection tables)
  - paper: doi:10.1109/12.609274
    title: Stuart F. Oberman and Michael J. Flynn, Division algorithms and implementations, IEEE Transactions on Computers 46(8) (1997), 833-854
    locator: Section 2, digit recurrence algorithms (SRT, redundancy factor, table sizes)
  - paper: doi:10.1137/S0036144595293959
    title: Alan Edelman, The mathematics of the Pentium division bug, SIAM Review 39(1) (1997), 54-67
    locator: the radix-4 SRT table of the Pentium, its five missing entries, and why errors were rare
---

SRT division computes a quotient one digit at a time, like long division, but lets each digit come from a redundant set such as $\{-2, -1, 0, 1, 2\}$ in radix 4. Because several digits are acceptable at each step, the digit can be chosen by looking up a few leading bits of the partial remainder and of the divisor in a small table, with no full-width comparison. A wrong-looking choice is corrected by later digits, and a single correction at the end gives the exact truncated quotient and remainder, from which the correctly rounded result follows. Variants of SRT division are the usual floating-point division and square root circuits in processors.

## In plain words

In school long division you guess each digit of the answer by comparing the remainder with the divisor, and a wrong guess means rubbing out and trying again. SRT division never rubs out. It allows digits that are negative as well as positive, so a guess that is a little too big can be fixed by a negative digit in the next place.

That freedom means the guess only needs a rough look at the leading few binary digits of the remainder and the divisor. A small fixed table gives the next digit from those few digits. After enough steps the signed digits are turned back into an ordinary answer, and the leftover remainder says how to round it.

## The problem

**Notation.** Binary floating-point with precision $p$ (binary64 by default, $p = 53$), round to nearest, ties to even, $\mathrm{fl}(\cdot)$ for the rounded result; see [floating-point arithmetic](/floating-point-arithmetic/). The [standard model](/floating-point-model/) holds without underflow or overflow. Inside the algorithm all arithmetic is exact fixed-point arithmetic on significands.

**Input.** Significands $x, d \in [1/2, 1)$ (the operands' exponents are handled separately), and a number of steps $n$.

**Output.** An integer $Q$ and a remainder $w$ with $\frac{x}{4d} = Q\,4^{-n} + w\,4^{-n}/d$ and $0 \le w < d$, so $Q = \lfloor x\,4^{n-1}/d \rfloor$. For floating-point division, $n$ is chosen so that $Q$ has at least $p + 1$ bits, and $\mathrm{fl}(a/b)$ is $Q$ rounded to $p$ bits using the next bit and whether $w \ne 0$.

## The algorithm

Radix 4 with digit set $\{-2, \ldots, 2\}$, redundancy factor $\rho = 2/3$, and the invariant $|w_j| \le \rho d$. The table is indexed by $\hat d$, the first 4 bits of $d$ after the binary point ($0.1xxx$), and by $\hat y$, the value $4w_j$ truncated to 3 fractional bits.

```pseudo id=main
SRT-DIVIDE(x, d, n)
L1  w ← x/4; Q ← 0                          ▷ |w| ≤ 1/4 ≤ ρd
L2  for j ← 1 to n do
L3      ŷ ← 4w truncated to 3 fractional bits ▷ ŷ ≤ 4w < ŷ + 1/8
L4      q ← TABLE[d̂, ŷ]                      ▷ a digit in {−2, …, 2}
L5      w ← 4w − q·d                          ▷ |w| ≤ ρd again
L6      Q ← 4Q + q                            ▷ in hardware: two digit registers, no carries
L7  if w < 0 then Q ← Q − 1; w ← w + d          ▷ one correction step
L8  return (Q, w)
```

The table entry for a cell (an interval of $\hat d$ times an interval of $\hat y$) is any digit $k$ with $(k - \rho) d \le y \le (k + \rho) d$ for every $y$ and $d$ in the cell; for $k = \pm 2$ only the inner inequality is needed, since the invariant already bounds $|y| \le 4\rho d$. Computing these intervals exactly gives a table of 275 cells, and the thresholds where the digit changes are:

| $\hat d$ | $0.1000$ | $0.1001$ | $0.1010$ | $0.1011$ | $0.1100$ | $0.1101$ | $0.1110$ | $0.1111$ |
|---|---|---|---|---|---|---|---|---|
| $q \ge 1$ from $\hat y \ge$ | $1/4$ | $3/8$ | $3/8$ | $3/8$ | $1/2$ | $1/2$ | $1/2$ | $5/8$ |
| $q = 2$ from $\hat y \ge$ | $3/4$ | $7/8$ | $1$ | $9/8$ | $5/4$ | $5/4$ | $11/8$ | $3/2$ |

The negative side is the mirror image: $q \le -1$ for $\hat y < -m_1$ and $q = -2$ for $\hat y < -m_2$, where $m_1$ and $m_2$ are the thresholds in the column. With 2 fractional bits of $4w$, or with only 3 bits of $d$, some cell has no valid digit.

## Example

Divide $x = 3/4$ by $d = 5/8$ ($\hat d = 0.1010$), so $x/(4d) = 3/10$.

| step | $4w$ | $\hat y$ | $q$ | new $w$ |
|---|---|---|---|---|
| 1 | $3/4$ | $3/4$ | $1$ | $1/8$ |
| 2 | $1/2$ | $1/2$ | $1$ | $-1/8$ |
| 3 | $-1/2$ | $-1/2$ | $-1$ | $1/8$ |
| 4 | $1/2$ | $1/2$ | $1$ | $-1/8$ |

The digits continue $-1, 1, -1, \ldots$, giving $0.1\,1\,\bar1\,1\,\bar1 \ldots_4$, and $1/4 + 1/16 - 1/64 + \ldots = 3/10$. With $n = 8$ the fixed-point implementation returns $Q = 19660$ and $w = 1/2$: $19660/4^8 + (1/2)/(4^8 \cdot 5/8) = 3/10$ exactly. Note the negative digits: the digit 1 at step 2 is too large, and step 3 compensates.

## Correctness

**Theorem.** If every reachable cell of the table holds a digit satisfying the containment condition above, then for any $x, d \in [1/2, 1)$ and $n \ge 1$, SRT-DIVIDE returns $Q = \lfloor x\,4^{n-1}/d \rfloor$ and $w$ with $\frac{x}{4d} = Q\,4^{-n} + w\,4^{-n}/d$ and $0 \le w < d$.

*Proof sketch.* By induction $|w_j| \le \rho d$: it holds for $w_0 = x/4 < 1/4 \le \rho d$, and if it holds for $w_{j-1}$ then $(y, d) = (4w_{j-1}, d)$ lies in the cell selected by $(\hat d, \hat y)$, so the digit from that cell keeps $|y - qd| \le \rho d$. Unrolling $w_j = 4w_{j-1} - q_j d$ gives $\frac{x}{4d} = \sum_{j=1}^n q_j 4^{-j} + w_n 4^{-n}/d$, and $Q$ is the integer $\sum q_j 4^{n-j}$. Since $|w_n|/d \le 2/3 < 1$, the correction in line L7 moves $w_n/d$ into $[0, 1)$, which identifies $Q$ as the floor. For floating-point division, $Q$ is then the quotient truncated to $2n - 2$ fractional bits and $w \ne 0$ is the sticky bit, so rounding $Q$ to $p$ bits with the guard bit and sticky bit is correct rounding to nearest. The full proof is in [the proof file](proofs/correctness.md).

**Proved and observed.** The theorem is proved for a table that satisfies the containment condition on every reachable cell; the implementation builds the table from that condition in exact rationals and fails if any cell has no digit. The tests observe that `srt_float_divide` agrees with the hardware's correctly rounded `a / b` on 20000 random binary64 pairs (seed 13) and on edge cases including $4195835/3145727$, the input that exposed the Pentium bug.

## Complexity

$n$ steps of a shift, a table lookup and one addition of $\pm d$ or $\pm 2d$: $\Theta(n)$ time for $2n$ quotient bits and $\Theta(1)$ extra space. In hardware each step takes a fixed short time because the remainder is kept in carry-save form, so the subtraction has no carry propagation, and only a few leading bits are converted for the lookup. Binary64 division needs about 28 radix-4 steps, which is why division is several times slower than multiplication; radix 16 or overlapped radix-4 stages reduce the count.

## Properties

- **Redundant digits.** With $\rho = 2/3$ the selection intervals for adjacent digits overlap by $\tfrac13 d$, which is what lets a truncated estimate pick a correct digit.
- **No restoring.** Unlike restoring division, a step never undoes a subtraction; negative digits play that role.
- **Small table.** 4 divisor bits and 6 remainder bits (sign, two integer bits and 3 fractional bits) suffice in radix 4 for an exact remainder; a carry-save remainder, whose truncation error is twice as large, typically needs one more fractional bit.
- **Exact remainder.** The final $w$ is exact, which gives correct rounding in every rounding mode and makes the result exact when the remainder is zero.
- **Square root too.** The same recurrence with a digit-dependent divisor computes square roots, and processors share the circuit.

## Variants and improvements

- **Radix 2.** Digits $\{-1, 0, 1\}$, $\rho = 1$; the digit depends only on whether $2w \ge 1/2$, $2w < -1/2$ or neither, so no divisor bits are needed. This is the original 1958 form.
- **Higher radix.** Radix 8 or 16 with digit sets $\{-a, \ldots, a\}$; tables grow quickly, so radix 16 is usually built from two overlapped radix-4 stages.
- **Prescaling.** Multiplying $x$ and $d$ by a factor that brings $d$ close to 1 makes the selection depend on the remainder only.
- **Quotient conversion on the fly.** Two registers hold $Q$ and $Q - 1$ so the signed digits never need a carry-propagating addition.
- **Multiplicative methods.** [Newton-Raphson](/newton-raphson-division/) and [Goldschmidt division](/goldschmidt-division/) converge quadratically using a multiplier, and win at high precision or where a fast multiplier exists.

## When to use it

SRT is a hardware method: use it in a divider or square-root unit, where it gives correctly rounded results in a fixed number of short cycles with a small area. In software, integer division instructions or multiplicative methods built on [fused multiply-add](/fused-multiply-add/) are faster; SRT in software is mainly for verification, teaching and emulation.

## Pitfalls

- **Missing table entries.** The Intel Pentium's radix-4 table lacked five entries near the top of the reachable region, which returned 0 instead of 2. Errors needed rare remainder patterns, which is why they were found only in 1994. The tests reproduce the effect: blanking five rarely visited cells of this page's table spoils the quotient for 399 of 3000 random inputs (seed 14), while the intact table gets all of them right.
- **Estimate precision.** Too few bits of the remainder or divisor leave cells with no valid digit; the condition must be checked for every cell, including the corners.
- **Reachable cells only.** For $q = \pm 2$ the outer inequality holds automatically by the invariant; demanding it over a whole cell makes some cells look infeasible and forces a needlessly larger table.
- **Final correction.** Forgetting line L7 leaves $Q$ one too large whenever the last remainder is negative, and then the rounding is wrong.
- **Sticky bit.** Rounding from $Q$ alone, without testing $w \ne 0$, breaks round to nearest at halfway points and the directed modes.

## Implementations

## History

Sweeney at IBM, Robertson and Tocher found redundant-digit division independently around 1957 and 1958; Robertson's and Tocher's papers appeared in 1958, and the method is named for the three. It became the standard division method in floating-point hardware. In 1994 Thomas Nicely found that the Pentium returned $4195835/3145727$ wrongly in the fifth significant digit, which was traced to five missing entries in its radix-4 SRT table; Intel's replacement of the chips cost about 475 million dollars, and the episode spurred formal verification of arithmetic circuits.

## References
