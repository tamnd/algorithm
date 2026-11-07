---
tag: 7J9632
kind: algorithm
slug: restoring-division
name: Restoring division
aliases:
- restoring binary division
- shift and subtract division
- binary long division
area: algebra/integer-arithmetic
level: core
summary: Binary long division that restores the partial remainder after an unsuccessful subtraction.
solves: [integer-division]
model: word-ram
complexity:
  vars: {m: the number of binary digits of the dividend, n: the number of limbs of the divisor}
  time: {worst: Θ(m n), average: Θ(m n), best: Θ(m n)}
  space: {extra: Θ(n)}
properties: {deterministic: true, recursive: false, in_place: false}
prereqs: [long-division, twos-complement, division-with-remainder]
see_also: [non-restoring-division, long-division, newton-raphson-division, ripple-carry-adder, integer-division, digit-by-digit-square-root, floor-division]
sources:
  - book: isbn:9780195328486
    title: Behrooz Parhami, Computer Arithmetic, Algorithms and Hardware Designs, second edition, Oxford University Press, 2010
    locator: Chapter 13, Basic division schemes (shift and subtract division, restoring hardware dividers, and the comparison with non-restoring division)
  - book: isbn:9781558607989
    title: Miloš D. Ercegovac and Tomás Lang, Digital Arithmetic, Morgan Kaufmann, 2004
    locator: Chapter 5, Division by digit recurrence (the radix 2 restoring recurrence as the simplest case)
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, third edition
    locator: Section 4.3.1, The classical algorithms (long division, of which the binary method is the case of radix 2)
---

Restoring division is [long division](/long-division/) in radix 2. It finds the quotient one binary digit at a time, from the top. At each step it shifts the next digit of the dividend into a partial remainder and subtracts the divisor. If the result is not negative, the quotient digit is 1 and the difference is kept. If it is negative, the quotient digit is 0, and the divisor is added back to *restore* the remainder. In radix 2 the quotient digit is 0 or 1, so one trial subtraction decides it, and the method needs only a shifter, an adder and a sign test. That is why it is the textbook design for a sequential hardware divider. An $m$-digit dividend takes $m$ steps, each a subtraction and sometimes an addition of numbers as long as the divisor.

## In plain words

Dividing in binary is like dividing in decimal, but easier: the divisor fits into the current remainder either once or not at all. So the computer tries it. It brings down the next digit of the dividend and subtracts the divisor. If something is left, the answer digit is 1. If it went below zero, the answer digit is 0 and it adds the divisor back to undo the subtraction. It repeats this for every digit of the dividend, from left to right. When the digits run out, what is left is the remainder.

## The problem

The input is a dividend $U \ge 0$ with $m$ binary digits $u_{m-1} \ldots u_0$ and a divisor $V \ge 1$, both as arrays of limbs in radix $\beta = 2^w$, least significant first; $V$ has $n$ limbs. The output is $Q = \lfloor U / V \rfloor$ and $R = U - QV$, with $0 \le R < V$. This is [integer division](/integer-division/).

**Cost model.** [Word RAM](/word-ram/) with $w$-bit words, counting limb operations: a shift of a limb by one place, or an addition or subtraction of two limbs with a carry. The partial remainder has $n + 1$ limbs, and a value below zero shows up as a borrow out of the top limb, as the sign bit of a [two's complement](/twos-complement/) register does in hardware. For a hardware divider the same count is the number of clock cycles, $m$, times the work of one $(n w + 1)$-digit adder.

## The algorithm

```pseudo id=main
RESTORING-DIV(U, V)            ▷ U has m binary digits u[m − 1] … u[0], V ≥ 1
L1  R ← 0;  Q ← 0
L2  for i ← m − 1 down to 0 do
L3      R ← 2R + u[i]          ▷ shift in the next digit of the dividend
L4      R ← R − V              ▷ trial subtraction
L5      if R < 0 then
L6          R ← R + V;  q[i] ← 0       ▷ restore
L7      else q[i] ← 1
L8  return (Q, R)
```

Line L3 is a left shift by one place. Line L4 is the trial subtraction. Lines L5 to L7 choose the quotient digit from its sign, and line L6 is the restoring addition. Since $0 \le R < V$ before line L3, the shifted value is less than $2V$, so after line L4 the value is in $[-V, V)$ and the quotient digit is 0 or 1.

## Example

**Divide $U = 100 = 1100100_2$ by $V = 7 = 111_2$.** Here $m = 7$. The table gives the value after line L3, the trial difference of line L4, and the remainder after the step.

| $i$ | $u_i$ | $2R + u_i$ | $- V$ | action | $q_i$ | $R$ after |
|---|---|---|---|---|---|---|
| 6 | 1 | 1 | $-6$ | restore | 0 | 1 |
| 5 | 1 | 3 | $-4$ | restore | 0 | 3 |
| 4 | 0 | 6 | $-1$ | restore | 0 | 6 |
| 3 | 0 | 12 | 5 | keep | 1 | 5 |
| 2 | 1 | 11 | 4 | keep | 1 | 4 |
| 1 | 0 | 8 | 1 | keep | 1 | 1 |
| 0 | 0 | 2 | $-5$ | restore | 0 | 2 |

The quotient is $0001110_2 = 14$ and the remainder is 2: $14 \cdot 7 + 2 = 100$. Four of the seven steps restore. The table was checked by script, and the test of this page checks the same counts.

## Correctness

Write $P_i = \lfloor U / 2^i \rfloor$ for the number formed by the digits $u_{m-1} \ldots u_i$ of the dividend, so $P_m = 0$, $P_0 = U$ and $P_i = 2P_{i+1} + u_i$. The invariant is that after the step for $i$, $R = P_i \bmod V$, and the quotient digits found so far form $\lfloor P_i / V \rfloor$.

It holds before the first step, with $P_m = 0$. If it holds for $i + 1$, then after line L3, $R' = 2(P_{i+1} \bmod V) + u_i$ satisfies $0 \le R' < 2V$ and $R' \equiv P_i \pmod V$. If $R' \ge V$, line L7 keeps $R' - V \in [0, V)$ and appends the digit 1. If $R' < V$, line L6 restores $R'$ and appends 0. In both cases $R = P_i \bmod V$, and $2\lfloor P_{i+1}/V \rfloor + q_i = \lfloor P_i / V \rfloor$, because $P_i = V(2\lfloor P_{i+1}/V \rfloor) + R'$. At $i = 0$ this gives $Q = \lfloor U/V \rfloor$ and $R = U \bmod V$. The loop has $m$ steps, so it terminates. The full proof is below.

## Complexity

**Steps.** The loop runs exactly $m$ times, whatever the values.

**Cost per step.** Line L3 shifts $n + 1$ limbs, line L4 subtracts $n$ limbs from $n + 1$, and line L6 adds them back when it runs: $\Theta(n)$ limb operations in every case. So the time is $\Theta(mn)$ limb operations in the worst, average and best case, and the extra space is the $n + 1$ limbs of $R$. In the bit complexity model, with $m$-digit and $k$-digit operands, it is $\Theta(mk)$ bit operations. These bounds are proved.

**Restoring additions.** A step restores exactly when its quotient digit is 0. In our tests, with a random dividend of $2k$ binary digits and a random divisor of exactly $k$ digits, the fraction of restoring steps was 0.73, 0.75 and 0.75 for $k = 16$, $64$ and $256$: the first $k - 1$ steps always restore, since the partial remainder is still shorter than $V$, and about half of the other steps do. So a restoring divider makes about $1.5$ additions or subtractions per step on average, an observed figure. This waste is what [non-restoring division](/non-restoring-division/) removes.

For multiprecision numbers this method is slower than long division in radix $2^w$ by a factor of about $w$, since it finds one binary digit per pass over the divisor instead of one limb.

## Properties

- **One trial per digit.** The quotient digit needs no estimate, only the sign of a difference.
- **Simple hardware.** A register for $R$ and $Q$, which can share one shift register as the dividend digits move out and the quotient digits move in, one adder and a sign test.
- **The remainder is correct at the end.** No final correction is needed, unlike non-restoring division.
- **Fixed number of steps.** The time does not depend on the values, only on the length $m$; in hardware this gives constant time, which also matters against timing attacks.

## Variants and improvements

- **Non-performing division.** Compute $R - V$ into a separate register and write it back only if it is not negative. This saves the restoring addition but needs the extra register and a selector. The implementation includes this version.
- **[Non-restoring division](/non-restoring-division/).** Keep the negative remainder and add $V$ in the next step instead of subtracting; one operation per step, and a correction at the end.
- **Higher radix.** Retire two or more quotient digits per step, with a comparison against several multiples of $V$ or with a quotient digit selection table, as in [SRT division](/srt-division/).
- **Normalization first.** Shift $V$ so that its top digit lines up with that of $U$, and skip the leading steps where the quotient digit must be 0; this removes most of the always-restoring prefix.
- **Signed operands.** Divide the magnitudes and set the signs afterwards, by the rules of the language: truncation toward zero in C, [floor division](/floor-division/) in Python. The implementation gives the C rule.
- **Square roots.** The same shift, trial subtract and restore loop, with a trial value that depends on the root found so far, gives the restoring [digit-by-digit square root](/digit-by-digit-square-root/).

## When to use it

Use restoring division in small hardware dividers and microcontroller software without a divide instruction, when the operands are a few words long and simplicity counts more than speed. Use it as the reference when testing faster dividers. For multiprecision numbers, use [long division](/long-division/) in radix $2^w$, and for very long numbers [Newton-Raphson division](/newton-raphson-division/).

## Pitfalls

- **A remainder register that is too short.** After line L3 the value can be as large as $2V - 1$, one binary digit longer than $V$. With only the width of $V$ the top digit is lost and the sign test fails. The implementation keeps $n + 1$ limbs.
- **Testing the sign by the top bit of a short register.** In hardware the sign of $R - V$ is the borrow out of the subtraction, or the top bit of a register one digit wider than $V$; using the top bit of an $n$-digit register mistakes large positive values for negative ones.
- **Division by zero.** With $V = 0$ every trial subtraction succeeds, and the result is all ones in the quotient and $R = U$; check for zero first.
- **Leading zero limbs of the divisor.** They lengthen every step without changing the result. Trim them.
- **Signs.** Two's complement operands must be converted to magnitudes first, and the rule for the sign of the remainder chosen deliberately.

## Implementations

## History

Restoring division is the school method of long division carried out in radix 2, where the quotient digit is decided by one trial subtraction. It was the division method of early binary computers, built from the adder and the shift registers that the machine already had. Non-restoring division was introduced to save the restoring additions, and SRT division, from the late 1950s, went further with redundant quotient digits. Textbooks of computer arithmetic, such as Parhami (Chapter 13) and Ercegovac and Lang (Chapter 5), present the restoring method as the basic shift and subtract scheme and derive the faster dividers from it.

## References
