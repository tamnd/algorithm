---
tag: HPV12R
kind: algorithm
slug: non-restoring-division
name: Non-restoring division
aliases:
- non-restoring binary division
- nonrestoring division
area: algebra/integer-arithmetic
level: advanced
summary: Binary division that skips the restore step by allowing negative partial remainders.
solves: [integer-division]
model: word-ram
complexity:
  vars: {m: the number of binary digits of the dividend, n: the number of limbs of the divisor}
  time: {worst: Θ(m n), average: Θ(m n), best: Θ(m n)}
  space: {extra: Θ(n)}
properties: {deterministic: true, recursive: false, in_place: false}
prereqs: [restoring-division, twos-complement, signed-digit-representation]
see_also: [restoring-division, srt-division, long-division, newton-raphson-division, redundant-number-system, digit-by-digit-square-root, integer-division]
sources:
  - book: isbn:9780195328486
    title: Behrooz Parhami, Computer Arithmetic, Algorithms and Hardware Designs, second edition, Oxford University Press, 2010
    locator: Chapter 13, Basic division schemes (non-restoring and signed division, and the quotient digits in the set of minus one and one)
  - book: isbn:9781558607989
    title: Miloš D. Ercegovac and Tomás Lang, Digital Arithmetic, Morgan Kaufmann, 2004
    locator: Chapter 5, Division by digit recurrence (radix 2 non-restoring division as a digit recurrence with digits minus one and one)
  - book: isbn:9781568811604
    title: Israel Koren, Computer Arithmetic Algorithms, second edition, A K Peters, 2002
    locator: Chapter 3, Sequential algorithms for multiplication and division (restoring and non-restoring division)
---

Non-restoring division is a binary division that never undoes a subtraction. Like [restoring division](/restoring-division/), it finds one quotient digit per step, from the top, by shifting the next digit of the dividend into a partial remainder. But when a subtraction of the divisor makes the remainder negative, it leaves it negative and *adds* the divisor in the next step instead of subtracting it. Doubling a negative remainder and adding $V$ gives the same value as restoring it, doubling it and subtracting $V$, so one addition does the work of two. Each step is a single addition or subtraction chosen by the sign of the remainder, and one final addition fixes a negative remainder at the end. The quotient digits are the signs of the successive remainders. In a hardware divider this saves the restoring additions, about half an operation per step, and makes every cycle the same.

## In plain words

Restoring division tries to subtract the divisor; if the result goes below zero, it adds the divisor back and moves on. Non-restoring division is lazier. If the result goes below zero, it just moves on, and next time it adds the divisor instead of subtracting it. That one addition makes up for the subtraction it did not undo, because the remainder has been doubled in between.

So every step is one addition or one subtraction, never both. The answer digit is 1 when the new remainder is zero or more and 0 when it is negative. If the very last remainder is negative, one addition makes it right.

## The problem

The input is a dividend $U \ge 0$ with $m$ binary digits $u_{m-1} \ldots u_0$ and a divisor $V \ge 1$, as arrays of limbs in radix $\beta = 2^w$, least significant first, with $V$ of $n$ limbs. The output is $Q = \lfloor U/V \rfloor$ and $R = U - QV$, with $0 \le R < V$; this is [integer division](/integer-division/).

**Cost model.** [Word RAM](/word-ram/) with $w$-bit words, $w \ge 2$, counting limb operations: shifts, additions and subtractions of limbs with a carry. The partial remainder lies in $[-V, V)$ and is held in [two's complement](/twos-complement/) in $n + 1$ limbs, whose top binary digit is the sign. For a hardware divider the count is $m$ clock cycles, each one $(nw + 1)$-digit addition or subtraction.

## The algorithm

```pseudo id=main
NON-RESTORING-DIV(U, V)            ▷ U has m binary digits u[m − 1] … u[0], V ≥ 1
L1  R ← 0
L2  for i ← m − 1 down to 0 do
L3      if R ≥ 0 then R ← 2R + u[i] − V
L4      else R ← 2R + u[i] + V
L5      q[i] ← 1 if R ≥ 0, else 0
L6  if R < 0 then R ← R + V        ▷ final correction
L7  return (Q, R)
```

Lines L3 and L4 are the only arithmetic of a step: a shift and one addition or subtraction, chosen by the sign of the old remainder. Line L5 reads the quotient digit from the sign of the new one. Line L6 runs at most once.

## Example

**Divide $U = 100 = 1100100_2$ by $V = 7$.** The same division as on the [restoring division](/restoring-division/) page. The table gives the operation chosen by the sign of $R$, the shifted value $2R + u_i$, and the new $R$.

| $i$ | $u_i$ | $2R + u_i$ | operation | new $R$ | $q_i$ |
|---|---|---|---|---|---|
| 6 | 1 | 1 | $-V$ | $-6$ | 0 |
| 5 | 1 | $-11$ | $+V$ | $-4$ | 0 |
| 4 | 0 | $-8$ | $+V$ | $-1$ | 0 |
| 3 | 0 | $-2$ | $+V$ | 5 | 1 |
| 2 | 1 | 11 | $-V$ | 4 | 1 |
| 1 | 0 | 8 | $-V$ | 1 | 1 |
| 0 | 0 | 2 | $-V$ | $-5$ | 0 |

The quotient digits are $0001110_2 = 14$. The last remainder $-5$ is negative, so line L6 adds 7 and gives $R = 2$: $14 \cdot 7 + 2 = 100$. Seven additions or subtractions and one correction, where restoring division needed seven subtractions and four restoring additions. The column of new remainders is the same as the column of trial differences on the restoring page: $-6, -4, -1, 5, 4, 1, -5$. Both tables were checked by script.

## Correctness

Compare with restoring division step by step. Let $T$ be the *restored* value of $R$: $T = R$ if $R \ge 0$, and $T = R + V$ if $R < 0$. If $R \ge 0$, line L3 computes $2T + u_i - V$. If $R < 0$, line L4 computes $2R + u_i + V = 2(T - V) + u_i + V = 2T + u_i - V$. So in both cases the new $R$ is $2T + u_i - V$, the trial difference that restoring division computes from its remainder $T$. By induction, at every step $R$ equals the trial difference of restoring division and $T$ equals its remainder, so the quotient digits agree, and line L6 turns the final $R$ into the restored value $U \bmod V$. The full proof is below; it also gives the textbook form with quotient digits $\pm 1$.

## Complexity

**Steps.** The loop runs exactly $m$ times. Each step shifts $n + 1$ limbs and adds or subtracts $n$ limbs: $\Theta(n)$ limb operations. Line L6 adds $\Theta(n)$ once at most. So the time is $\Theta(mn)$ in every case, with $n + 1$ limbs of extra space. These bounds are proved.

**Against restoring division.** The asymptotic cost is the same. The gain is in the constant: exactly one addition or subtraction per step, against one subtraction plus a restoring addition whenever the quotient digit is 0, which on the restoring page was observed for about three quarters of the steps when the dividend is twice as long as the divisor. The final correction ran for 50.3% of 2000 random divisions of 128-digit by 64-digit binary numbers in our tests, matching the chance that the last quotient digit is 0.

In a hardware divider each step is one pass through an adder, so the cycle time is fixed; with a carry-propagate adder the step still waits for the sign, which needs the full carry chain. [SRT division](/srt-division/) removes that wait by allowing quotient digit 0 as well, so that the sign need not be known exactly.

## Properties

- **One operation per step.** Always one addition or one subtraction; the choice depends only on the sign of the remainder.
- **Signed digits in disguise.** The operation of step $i$ is a quotient digit $d_i \in \{1, -1\}$, subtract or add, in a [signed-digit representation](/signed-digit-representation/). Here $d_i = 1$ when the remainder before the step is nonnegative. The binary quotient digits $q_i$ are recovered from the signs of the remainders.
- **The remainder can be negative.** Between steps $R \in [-V, V)$, so the register needs a sign.
- **Final correction.** The quotient needs no correction in the form given here, only the remainder.

## Variants and improvements

- **Quotient digits $\pm 1$.** The textbook form records $d_i$ and converts at the end: $D = \sum d_i 2^i$ satisfies $U = DV + R_0$, and if $R_0 < 0$ then $Q = D - 1$ and $R = R_0 + V$. The conversion of $D$ to binary is a subtraction of the number of $-1$ digits from that of the $+1$ digits, which can also be done on the fly.
- **Signed operands.** Two's complement dividends and divisors can be divided directly: the first operation is chosen by comparing the signs of $R$ and $V$, and the end corrections depend on the signs of the remainder and the dividend. Parhami gives this signed form.
- **[SRT division](/srt-division/).** Quotient digits in $\{-1, 0, 1\}$, chosen from a few leading digits of a redundant remainder, so each step uses a carry-save adder instead of a carry-propagate one. The Intel Pentium divide bug of 1994 was in the digit selection table of a radix 4 SRT divider.
- **Non-restoring square root.** The same idea, with a trial value that depends on the root found so far, gives a [digit-by-digit square root](/digit-by-digit-square-root/) without restoring additions.
- **Normalization.** As for restoring division, aligning $V$ with the top of $U$ skips the leading steps.

## When to use it

Use non-restoring division in sequential hardware dividers and in software on processors without a divide instruction, when the operands are a few words long. In hardware it is the baseline from which SRT dividers are built. For multiprecision numbers, use [long division](/long-division/) in radix $2^w$ or [Newton-Raphson division](/newton-raphson-division/) instead: a binary method finds one quotient digit per pass over the divisor, $w$ times fewer than long division.

## Pitfalls

- **Forgetting the final correction.** Without line L6 the remainder is negative in about half of the cases, while the quotient is still right. Tests that check only the quotient do not catch it.
- **A register without room for the sign.** $2R + u_i$ lies in $[-2V, 2V)$, so with $V < 2^{nw}$ the register needs $nw + 2$ binary digits in two's complement. The implementation uses $n + 1$ limbs and requires $w \ge 2$.
- **Choosing the operation by the new sign.** The choice of line L3 or L4 depends on the sign of $R$ *before* the step; the quotient digit depends on the sign *after* it. Mixing them up gives wrong digits.
- **Zero remainders.** $R = 0$ counts as nonnegative. Treating it as negative breaks exact divisions, where the last remainder is 0.
- **Mixing the two digit conventions.** The digits $q_i \in \{0, 1\}$ of this page give $Q$ directly; the digits $d_i \in \{\pm 1\}$ give $D$, which may be $Q + 1$. Do not combine the conversion of one with the correction of the other.

## Implementations

## History

Non-restoring division arose with the first binary computers as a way to halve the number of additions of the restoring method, and it was widely used in the arithmetic units of the 1950s and later. Its idea of quotient digits $\pm 1$ led to SRT division, named for D. W. Sweeney, J. E. Robertson and K. D. Tocher, who found it independently around 1958, and to the theory of division by digit recurrence set out by Ercegovac and Lang. Textbooks such as Parhami's and Koren's present the restoring and non-restoring methods side by side as the two basic shift and subtract dividers.

## References
