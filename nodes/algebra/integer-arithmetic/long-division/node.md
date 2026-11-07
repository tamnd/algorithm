---
tag: BHDBGW
kind: algorithm
slug: long-division
name: Long division
aliases:
- schoolbook division
- pencil-and-paper division
- Knuth's Algorithm D
- basecase division
area: algebra/integer-arithmetic
level: intro
summary: Digit-by-digit division that estimates each quotient digit and subtracts.
solves: [integer-division]
model: word-ram
complexity:
  vars: {n: the number of limbs of the divisor, m: the number of limbs of the dividend minus n}
  time: {worst: Θ(n (m + 1)), average: Θ(n (m + 1)), best: Θ(n (m + 1))}
  space: {extra: Θ(m + n)}
properties: {deterministic: true, recursive: false, in_place: false}
prereqs: [positional-number-system, division-with-remainder, schoolbook-multiplication]
see_also: [restoring-division, non-restoring-division, newton-raphson-division, burnikel-ziegler-division, integer-division, multiprecision-integer, floor-division, digit-by-digit-square-root]
sources:
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, third edition
    locator: Section 4.3.1, The classical algorithms, Algorithm D (division of nonnegative integers), with Theorems A and B on the trial quotient and the normalization
  - book: isbn:9780521194693
    title: Richard P. Brent and Paul Zimmermann, Modern Computer Arithmetic, Cambridge University Press, 2010
    locator: Section 1.4.1, Naive division (Algorithm BasecaseDivRem), and Section 1.4.7, Division by a single word
  - book: isbn:9780195328486
    title: Behrooz Parhami, Computer Arithmetic, Algorithms and Hardware Designs, second edition, Oxford University Press, 2010
    locator: Chapter 13, Basic division schemes (shift and subtract division, the paper-and-pencil method in radix 2 and higher radices)
---

Long division computes the quotient and the remainder of two integers one quotient digit at a time, from the top: at each step it guesses the next digit from the leading digits of the current remainder and of the divisor, subtracts that multiple of the divisor, and fixes the guess if it was too large. Done with a good guess, the paper method becomes Knuth's Algorithm D, the standard division of [multiprecision integers](/multiprecision-integer/). After a *normalization* that makes the top digit of the divisor at least half the radix, the guess is never too small and at most 2 too large, and a cheap test with one more digit brings it to at most 1 too large. The cost is $\Theta(n(m + 1))$ limb operations for a divisor of $n$ limbs and a quotient of $m + 1$ limbs, the same order as [schoolbook multiplication](/schoolbook-multiplication/) of the two.

## In plain words

To divide 814600 by 199 by hand, you look at the front of the big number and ask how many times 199 fits into it. 199 fits 4 times into 814, so 4 is the first digit of the answer. You write $4 \times 199 = 796$ under 814, subtract to get 18, bring down the next digit, and ask again with 186. And so on, until the digits run out. What is left at the end is the remainder.

The hard part is "how many times does it fit?". With a long divisor you guess from the first digits, and sometimes the guess is one too big; then the subtraction goes below zero, and you take one less. A computer does the same with very large digits. Scaling both numbers first, so that the divisor begins with a big digit, makes the guesses almost always right.

## The problem

The input is a dividend $U \ge 0$ with $m + n$ digits and a divisor $V > 0$ with $n$ digits, both in a radix $\beta \ge 2$, as digit arrays $u = [u_0, \ldots, u_{m+n-1}]$ and $v = [v_0, \ldots, v_{n-1}]$, least significant digit first, with $v_{n-1} \ne 0$. The output is the quotient $Q = \lfloor U / V \rfloor$ and the remainder $R = U - QV$, with $0 \le R < V$. This is [integer division](/integer-division/) with the [division with remainder](/division-with-remainder/) of the integers.

**Cost model.** On the [word RAM](/word-ram/) with $\beta = 2^w$, a digit is a limb. A limb operation is an addition, a subtraction, or a product of two limbs into two limbs, or a division of a two-limb number by a limb when the quotient fits in one limb. Most processors have this last instruction. Costs are counted in limb operations.

## The algorithm

For $n = 1$, *short division* suffices: going down from the top, divide the two-digit number $r\beta + u_j$ by $v_0$, where $r < v_0$ is the remainder so far, and the quotient is one digit. For $n \ge 2$, Algorithm D:

```pseudo id=main
LONG-DIV(u[0 .. m + n − 1], v[0 .. n − 1])        ▷ n ≥ 2, v[n − 1] ≠ 0
L1  d ← ⌊β / (v[n − 1] + 1)⌋;  u ← d·u (m + n + 1 digits);  v ← d·v (n digits)
L2  for j ← m down to 0 do
L3      (q̂, r̂) ← divmod(u[j + n]·β + u[j + n − 1], v[n − 1])
L4      while r̂ < β and (q̂ ≥ β or q̂·v[n − 2] > r̂·β + u[j + n − 2]) do q̂ ← q̂ − 1;  r̂ ← r̂ + v[n − 1]
L5      u[j .. j + n] ← u[j .. j + n] − q̂·v             ▷ an n-digit multiply and subtract
L6      if the result of L5 is negative then q̂ ← q̂ − 1;  u[j .. j + n] ← u[j .. j + n] + v
L7      q[j] ← q̂
L8  r ← u[0 .. n − 1] / d                             ▷ a short division, exact
L9  return (q, r)
```

Line L1 is the *normalization*: after it, $v_{n-1} \ge \lfloor \beta/2 \rfloor$, and the quotient is unchanged, since $dU / dV = U / V$. When $\beta = 2^w$, one can use a power of two for $d$, and then L1 and L8 are bit shifts. Line L3 is the trial quotient, from the top two digits of the current remainder and the top digit of the divisor. Line L4 compares with one more digit of each, which removes almost all of the wrong guesses. Line L6, the *add back*, is the rare case where $\hat{q}$ is still one too large.

## Example

All values in this section were checked by script. **Divide $U = 814600$ by $V = 199$ in radix 10.** Here $n = 3$ and $m = 3$. The normalization gives $d = \lfloor 10 / 2 \rfloor = 5$, so $u = 4073000$, with $m + n + 1 = 7$ digits, and $v = 995$.

| $j$ | current window | $\hat{q}$ after L3 | after L4 | subtract $\hat{q}v$ | new window | $q_j$ |
|---|---|---|---|---|---|---|
| 3 | 4073 | $\lfloor 40/9 \rfloor = 4$ | 4 | 3980 | 0093 | 4 |
| 2 | 0930 | $\lfloor 9/9 \rfloor = 1$ | 0 | 0 | 0930 | 0 |
| 1 | 9300 | $\lfloor 93/9 \rfloor = 10$ | 9 | 8955 | 0345 | 9 |
| 0 | 3450 | $\lfloor 34/9 \rfloor = 3$ | 3 | 2985 | 0465 | 3 |

At $j = 2$, the test of line L4 is $1 \cdot 9 > 0 \cdot 10 + 3$, so $\hat{q}$ drops to 0. At $j = 1$, $\hat{q} = 10 \ge \beta$ drops to 9, and then $\hat{r} = 3 + 9 = 12 \ge \beta$ ends the loop. The quotient is $Q = 4093$, and the remainder is $465 / 5 = 93$. Check: $4093 \cdot 199 + 93 = 814600$.

**An add back.** Divide $4100$ by $588$ in radix 10. Here $d = \lfloor 10 / 6 \rfloor = 1$. At $j = 1$ the trial digit is $\lfloor 4 / 5 \rfloor = 0$. At $j = 0$, line L3 gives $\hat{q} = \lfloor 41/5 \rfloor = 8$ with $\hat{r} = 1$. Line L4 tests $8 \cdot 8 = 64 > 1 \cdot 10 + 0$, so $\hat{q} = 7$ and $\hat{r} = 6$, and then $7 \cdot 8 = 56 > 60$ is false. But $7 \cdot 588 = 4116 > 4100$, so line L5 goes negative, and line L6 sets $\hat{q} = 6$ and adds back: the remainder is $4100 - 3528 = 572$. So $4100 = 6 \cdot 588 + 572$.

## Correctness

Write $U_j$ for the number in the window $u_j, \ldots, u_{j+n}$ before step $j$. The invariant is $0 \le U_j < \beta V'$, where $V'$ is the normalized divisor, so the true quotient digit $q = \lfloor U_j / V' \rfloor$ is a digit. Two facts about the trial quotient $\hat{q} = \min(\lfloor (u_{j+n}\beta + u_{j+n-1}) / v_{n-1} \rfloor, \beta - 1)$ make the algorithm work (Knuth's Theorems A and B):

- $\hat{q} \ge q$: the trial digit is never too small, because it uses the top digits of $U_j$ and only the top digit of $V'$.
- If $v_{n-1} \ge \lfloor \beta / 2 \rfloor$, then $\hat{q} \le q + 2$.

The test of line L4 decreases $\hat{q}$ only while $\hat{q} v_{n-2} > \hat{r}\beta + u_{j+n-2}$, which implies $\hat{q} V' > U_j$, so it never goes below $q$; after it, $\hat{q} \le q + 1$. Line L6 fixes the last case. So $q_j = q$, and the new window $U_j - qV'$ is in $[0, V')$, which gives the invariant for the next step. At the end, the low $n$ digits hold $dU \bmod dV = d R$, and line L8 recovers $R$. The full proof is below.

## Complexity

Each of the $m + 1$ steps does one division of a two-limb number by a limb (line L3), $O(1)$ limb operations in line L4, whose loop runs a bounded number of times (at most 4 by the argument of the proof, and at most 2 in an exhaustive check of all two-digit divisors for radices up to 16), and an $n$-limb multiply and subtract (line L5), plus in rare cases an $n$-limb addition (line L6). The normalization and the final short division cost $O(m + n)$. The total is $\Theta(n(m + 1))$ limb operations, about $n(m + 1)$ limb products, for every input. For a $2n$-limb dividend and an $n$-limb divisor this is $\Theta(n^2)$, the cost of one schoolbook product of two $n$-limb numbers. These bounds are proved.

How often line L6 runs is a question of probability: Knuth shows that it is rare, of the order of $1/\beta$ per step for random inputs. In our tests on random inputs with 6-limb divisors, it ran in 1.8% of the steps for $\beta = 16$ and in 0.13% for $\beta = 256$, about $0.3/\beta$ in both cases. For $\beta = 2^{64}$ it is so rare that random tests almost never reach it, which is why it needs targeted tests.

## Properties

- **Exact.** The algorithm returns the exact quotient and remainder; there is no rounding.
- **Most significant digit first.** Unlike addition and multiplication, division must work from the top, because each quotient digit depends on the remainder above it.
- **One hardware division per digit.** Line L3 is the only division by a limb. Libraries often replace it by a multiplication with a precomputed reciprocal of $v_{n-1}$, which is faster on most processors.
- **The remainder is a by-product.** No extra work gives $R$.

## Variants and improvements

- **Division by a single limb.** Short division, with one two-by-one division per limb, or with a precomputed reciprocal; Brent and Zimmermann, Section 1.4.7.
- **Binary hardware division.** In radix 2 the trial digit is 0 or 1, decided by a comparison: [restoring division](/restoring-division/) and [non-restoring division](/non-restoring-division/), and SRT division with redundant digits.
- **Divide and conquer.** [Burnikel-Ziegler division](/burnikel-ziegler-division/) splits the problem into two half-size divisions and uses fast multiplication, with cost $O(M(n) \log n)$ for $M(n)$ the cost of an $n$-limb product.
- **Newton's method.** [Newton-Raphson division](/newton-raphson-division/) computes an approximate reciprocal of $V$ and then the quotient with a few multiplications, with cost $O(M(n))$. It wins for large $n$; where it starts to win depends on the machine and the library, and is observed, not proved.
- **Exact division.** When the remainder is known to be 0, Jebelean's method computes the quotient from the low limbs, about twice as fast.
- **Signed operands.** Divide the magnitudes and fix the signs, using the rule of the language: truncation toward 0 in C, or [floor division](/floor-division/) in Python.

## When to use it

Use Algorithm D for multiprecision division when the divisor has up to a few dozen limbs, and as the base case of the divide-and-conquer and Newton methods. Use short division for single-limb divisors, such as the conversion of a number to decimal digits. For very large operands, switch to [Burnikel-Ziegler](/burnikel-ziegler-division/) or Newton division; the switch points are tuned per machine.

## Pitfalls

- **Skipping the normalization.** Without it, $\hat{q}$ can be far too large when $v_{n-1}$ is small, and a single correction does not suffice. With $\beta = 10$ and $v = 199$ unnormalized, the last step of the first example has the window 0690, and the trial digit $\lfloor 6 / 1 \rfloor = 6$ is 3 more than the true digit 3.
- **Leaving out the add back.** Line L6 runs rarely and is easy to get wrong. A bug there passes random tests for $\beta = 2^{64}$. Test with small radices, where it runs often, as the tests of this page do with $\beta = 16$.
- **Overflow in line L4.** The product $\hat{q} v_{n-2}$ and the value $\hat{r}\beta + u_{j+n-2}$ need two limbs. The loop must stop when $\hat{r} \ge \beta$, both for correctness and to avoid overflow.
- **The extra digit.** The normalized dividend has $m + n + 1$ digits, one more than $u$; forgetting it loses the top of $dU$.
- **Leading zeros of the divisor.** Normalize the input first: the algorithm needs $v_{n-1} \ne 0$.
- **Signs.** C rounds toward zero and Python toward minus infinity. A signed wrapper must apply the rule of its language, as the test of this page does against Python's `divmod`.

## Implementations

## History

Long division in its written form goes back to medieval arithmetic, and the present layout spread with the printed arithmetic books of the early modern period. For computers, the method with a trial quotient from the leading digits was studied by Pope and Stein in 1960, and Knuth gave the normalized method, with the proof that the trial digit is at most two too large, as Algorithm D in the first edition of Volume 2, in 1969. It remains the base case of division in GMP and in other libraries.

## References
