---
tag: NZK9TA
kind: algorithm
slug: binary-gcd
name: Binary GCD
aliases:
- Stein's algorithm
- binary Euclidean algorithm
area: number-theory/divisibility-and-gcd
level: core
summary: Computes gcd using only subtraction, parity tests and shifts, avoiding division.
solves: [gcd-of-two-integers]
model: word-ram
complexity:
  vars: {n: the bit length of the larger absolute value of the inputs}
  time: {worst: Θ(n), best: Θ(1)}
  space: {extra: Θ(1)}
  bit_operations: {worst: O(n^2)}
properties: {deterministic: true, recursive: false}
history:
  year: 1967
  people: [Josef Stein]
  note: Published by Stein in a paper on computations in Racah algebra; Knuth's Algorithm B.
prereqs: [greatest-common-divisor, euclidean-algorithm, trailing-zero-count, loop-invariant]
see_also: [euclidean-algorithm, lehmers-gcd, half-gcd, extended-euclidean-algorithm, modular-inverse, lowest-set-bit, timing-attack, gcd-of-array]
sources:
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, third edition
    locator: Section 4.5.2, The greatest common divisor (Algorithm B, the binary gcd algorithm, its analysis and history)
  - paper: "Josef Stein, Computational problems associated with Racah algebra, Journal of Computational Physics 1(3), 1967"
    locator: pages 397 to 405
  - paper: "Damien Stehlé and Paul Zimmermann, A binary recursive gcd algorithm, Algorithmic Number Theory (ANTS VI), Lecture Notes in Computer Science 3076, 2004"
    locator: pages 411 to 425
  - paper: "Daniel J. Bernstein and Bo-Yin Yang, Fast constant-time gcd computation and modular inversion, IACR Transactions on Cryptographic Hardware and Embedded Systems 2019(3)"
    locator: pages 340 to 398
---

Binary GCD, also called Stein's algorithm, computes the [greatest common divisor](/greatest-common-divisor/) of two integers using only parity tests, shifts by powers of two, comparisons and subtractions. It needs no division. It rests on three facts: $\gcd(2u, 2v) = 2\gcd(u, v)$, $\gcd(u, 2v) = \gcd(u, v)$ when $u$ is odd, and $\gcd(u, v) = \gcd(u, v - u)$. The number of loop passes is at most $1 + \lg(|a| \cdot |b|)$, linear in the input length, and the cost is $O(n^2)$ bit operations on $n$-digit inputs, the same order as the [Euclidean algorithm](/euclidean-algorithm/). It is used where division is slow and where shifts and subtractions are cheap.

## In plain words

You want the largest number that divides two given numbers, but dividing is expensive and halving is cheap. First, count how many times both numbers can be halved together; that power of two is part of the answer, and you set it aside. After that, the answer is odd, so halving an even number never loses anything, and you can halve each number until it is odd.

Now both numbers are odd. Subtract the smaller from the larger. The answer does not change, and the difference is even, so you can halve it again at least once. Repeat until the two numbers are equal. That number, times the power of two you set aside, is the answer. Each round at least halves one of the numbers, so the rounds end fast.

## The problem

The input is two integers $a$ and $b$, of any sign, possibly zero. The output is $\gcd(a, b) \ge 0$, with $\gcd(a, 0) = |a|$ and $\gcd(0, 0) = 0$. This is the [GCD of two integers](/gcd-of-two-integers/) problem.

**Cost model.** On the [word RAM](/word-ram/), the inputs fit in a machine word, and a shift, a subtraction, a comparison and a [trailing zero count](/trailing-zero-count/) each cost one step; most processors have an instruction for the count. Bounds in this model count loop passes. For [arbitrary-precision](/arbitrary-precision-arithmetic/) inputs of $n$ binary digits, the cost is in bit operations: a shift or a subtraction of $n$-digit numbers costs $O(n)$.

## The algorithm

Let $\operatorname{tz}(x)$ be the number of trailing zero binary digits of $x > 0$, the exponent of $2$ in $x$.

```pseudo id=main
BINARY-GCD(a, b)
L1  a ← |a|, b ← |b|                 ▷ the gcd does not depend on signs
L2  if a = 0 then return b
L3  if b = 0 then return a
L4  k ← tz(a OR b)                     ▷ 2^k is the largest power of 2 dividing both
L5  a ← a >> tz(a)                     ▷ a is odd from now on
L6  repeat
L7      b ← b >> tz(b)                 ▷ b is odd
L8      if a > b then swap a and b     ▷ now a ≤ b, both odd
L9      b ← b − a                      ▷ b is even and non-negative
L10 until b = 0
L11 return a << k
```

Lines L2 and L3 handle zero, which has no trailing zero count: every number divides $0$, so the gcd is the other number. Line L4 finds the common power of two in one step, because the lowest $1$ digit of $a \mathbin{\mathrm{OR}} b$ is the lower of the lowest $1$ digits of $a$ and $b$. After line L5 the gcd of the remaining pair is odd, so the halvings of line L7 do not change it. Each pass subtracts the smaller odd number from the larger; the difference is even, so the next line L7 removes at least one factor of $2$. The loop ends when the two odd numbers are equal, and that value is the odd part of the gcd.

The version in Knuth's Algorithm B keeps a signed difference $t$ and halves it one digit at a time. The form above, with a trailing zero count, is the usual one in modern code.

## Example

Compute $\gcd(240, 46)$. In binary, $240 = 11110000_2$ and $46 = 101110_2$, so $240 \mathbin{\mathrm{OR}} 46 = 11111110_2$, and $k = 1$. Line L5 turns $240 = 2^4 \cdot 15$ into $a = 15$.

| pass | $b$ before L7 | $b$ after L7 | after L8: $a, b$ | after L9: $b$ |
|---|---|---|---|---|
| 1 | 46 | 23 | 15, 23 | 8 |
| 2 | 8 | 1 | 1, 15 | 14 |
| 3 | 14 | 7 | 1, 7 | 6 |
| 4 | 6 | 3 | 1, 3 | 2 |
| 5 | 2 | 1 | 1, 1 | 0 |

The loop ends with $a = 1$, and line L11 returns $1 \ll 1 = 2$. Indeed $240 = 2^4 \cdot 3 \cdot 5$ and $46 = 2 \cdot 23$, so $\gcd(240, 46) = 2$. Passes 2 to 5 show the slow case: once $a = 1$, each pass removes only one binary digit from $b$.

## Correctness

The proof uses three rules, for $u, v \ge 1$: if $u$ is odd, $\gcd(u, 2^s v) = \gcd(u, v)$, because an odd common divisor of $u$ and $2^s v$ is coprime to $2^s$ and so divides $v$; $\gcd(u, v) = \gcd(u, v - u)$, because the two pairs have the same common divisors; and $\gcd(2^k u, 2^k v) = 2^k \gcd(u, v)$. The [loop invariant](/loop-invariant/) at the start of each pass is: $a$ is odd, $b \ge 1$, and $2^k \gcd(a, b) = \gcd(a_0, b_0)$. Lines L4 and L5 make it true by the first and third rules. Line L7 keeps the gcd by the first rule, the swap keeps it, and line L9 keeps it by the second rule. The loop exits when $b - a = 0$, so $a = b$ and $\gcd(a, b) = a$. Termination follows from the bound below. The full proof is in the proofs.

## Complexity

**Loop passes.** Let $a$ and $b$ be the values just after line L8, so $a \le b$, both odd. If the loop goes on, $b - a$ is even, and the next line L7 halves it at least once, so the product of the pair drops from $ab$ to at most $a(b - a)/2 < ab/2$. The product is at least $1$ and starts at most $|a_0| \cdot |b_0|$, so the loop runs at most $1 + \lg(|a_0| |b_0|) \le 2n + 1$ times. The bound is tight up to a constant factor: on $(2^n - 1, 1)$ the loop runs exactly $n$ times, one binary digit per pass.

**Average case.** For random 64-digit odd inputs, the loop runs about $45$ times on average, about $0.71$ passes for each binary digit of the input. The [Euclidean algorithm](/euclidean-algorithm/) uses about $38$ division steps on the same inputs, so the binary algorithm does more passes, but each pass is a few cheap instructions instead of a division. Brent's analysis of the average, reported by Knuth, explains the constant.

**Time on the word RAM.** With a constant-time trailing zero count, each pass costs $O(1)$, so the time is $\Theta(n)$ in the worst case, where $n \le w$ is the length of the larger input. The best case is $\Theta(1)$: one input is zero, or the two odd parts are equal. Without a trailing zero instruction, halving one digit at a time adds at most $\lg(|a_0| |b_0|)$ shifts in total, since each shift halves a value that stays at least $1$, so the bound is the same. The extra space is $\Theta(1)$ words.

**Bit operations.** For $n$-digit inputs each pass does a constant number of shifts, comparisons and subtractions of $O(n)$ bit operations each, so the total is $O(n^2)$, the same order as the Euclidean algorithm with schoolbook division.

| measure | bound |
|---|---|
| loop passes, worst | $\le 1 + \lg(|a| \cdot |b|) \le 2n + 1$, and $n$ on $(2^n - 1, 1)$ |
| loop passes, average for 64-digit inputs | about $45$ |
| time on the word RAM | worst $\Theta(n)$, best $\Theta(1)$ |
| extra space | $\Theta(1)$ words |
| bit operations | $O(n^2)$ |

## Properties

- **Division free.** Only shifts, subtractions, comparisons and parity tests. This suits hardware without a fast divider, and big numbers stored in binary.
- **Deterministic and iterative.** No recursion and a constant number of variables.
- **Not a remainder sequence.** The intermediate values are not the remainders of the Euclidean algorithm, so the quotients of the [continued fraction](/continued-fraction/) of $a/b$ cannot be read from the run.
- **Data-dependent branches.** The number of passes and the direction of each swap depend on the inputs. This leaks information through timing when the inputs are secret; see the pitfalls.

## Variants and improvements

- **Knuth's Algorithm B.** Keeps a signed difference $t = a - b$ and halves $t$ one digit at a time, choosing which of $a$ and $b$ to replace by the sign of $t$. It avoids the trailing zero instruction.
- **Extended binary GCD.** Keeps Bézout coefficients along with $a$ and $b$, and halves a coefficient modulo the other input when it is odd. It computes a [modular inverse](/modular-inverse/) modulo an odd number without division, and is common in hardware and in big number libraries.
- **[Lehmer's GCD](/lehmers-gcd/) in binary form.** For numbers of many words, run the binary steps on the low or high words only, record them as a $2 \times 2$ matrix, and apply the matrix to the full numbers. This saves a constant factor.
- **Binary recursive GCD.** Stehlé and Zimmermann (2004) gave a divide-and-conquer form, built on the low-order digits, that reaches $O(M(n) \log n)$ bit operations, like the [half-GCD](/half-gcd/), where $M(n)$ is the cost of [multiplying](/integer-multiplication/) two $n$-digit numbers.
- **Constant-time GCD.** Bernstein and Yang (2019) gave a division-step algorithm with a fixed number of iterations and no secret-dependent branches, for modular inversion in cryptography.

## When to use it

Use it for word-sized integers when the processor has a fast trailing zero count and a slow divider; on many current processors it is then faster than the Euclidean algorithm. Use it on small processors and in hardware with no divider at all. For a modular inverse modulo an odd number, the extended binary form avoids division. For numbers of thousands of digits, use [Lehmer's GCD](/lehmers-gcd/) or the [half-GCD](/half-gcd/), which reduce the quadratic cost. When the inputs are secret, as in a cryptographic key, use a constant-time algorithm, not this one.

## Pitfalls

- **Zero inputs.** $\operatorname{tz}(0)$ is undefined: `__builtin_ctz(0)` in C is undefined behaviour, and a loop that halves while the number is even never stops on $0$. Lines L2 and L3 must come before any trailing zero count.
- **Unsigned subtraction.** Line L9 is safe only after the swap of line L8. Without it, $b - a$ wraps around in unsigned arithmetic, or is negative in signed arithmetic, and the loop runs on a wrong value.
- **The most negative integer.** In 64-bit two's complement, $|-2^{63}|$ does not fit, so line L1 overflows. Use unsigned arithmetic for the absolute values.
- **Forgetting the common power of two.** Dropping line L4 or the shift of line L11 returns only the odd part of the gcd: $\gcd(12, 18)$ would come out as $3$.
- **Using it on secret data.** The number of passes and the swaps depend on the inputs, so the running time leaks information about them; this is a [timing attack](/timing-attack/) risk in cryptographic code.

## Implementations

## History

Josef Stein published the algorithm in 1967, in a paper on the numerical computations of Racah algebra in physics, where it served to reduce fractions on a binary computer. Knuth presents it as Algorithm B in Section 4.5.2 and notes that the idea of halving to reduce a fraction may go back much further, to a procedure in the Chinese *Nine Chapters on the Mathematical Art*. Richard Brent analysed the average number of passes in 1976. Stehlé and Zimmermann gave a subquadratic binary form in 2004, and Bernstein and Yang a constant-time form for cryptography in 2019.

## References
