---
tag: RN6MV6
kind: algorithm
slug: lehmers-gcd
name: Lehmer's GCD
aliases:
- Lehmer's algorithm
area: number-theory/divisibility-and-gcd
level: advanced
summary: Speeds up Euclid on big integers by running single-precision steps on the leading digits.
solves: [gcd-of-two-integers]
model: word-ram
complexity:
  vars: {n: the bit length of the larger absolute value of the inputs, w: the word size}
  time: {worst: O(n^2 / w + n), best: O(n / w + 1)}
  space: {extra: O(n / w)}
  bit_operations: {worst: O(n^2)}
properties: {deterministic: true, recursive: false}
history:
  year: 1938
  people: [Derrick Henry Lehmer]
  note: Lehmer described the method in the American Mathematical Monthly in 1938.
prereqs: [euclidean-algorithm, gcd-recursion-theorem, lames-theorem]
see_also: [half-gcd, binary-gcd, extended-euclidean-algorithm, gcd-of-two-integers, continued-fraction, karatsuba-multiplication, schonhage-strassen-multiplication, word-ram]
sources:
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, third edition
    locator: Section 4.5.2, The Greatest Common Divisor (Algorithm L, Euclid's algorithm for large numbers, with the test on the two quotients and the matrix A, B, C, D)
  - book: isbn:9780521194693
    title: Richard P. Brent and Paul Zimmermann, Modern Computer Arithmetic
    locator: Section 1.6.1, Naive GCD (Lehmer's idea of working on the leading words), and Section 1.6.3, Half binary GCD, divide and conquer GCD
  - paper: "D. H. Lehmer, Euclid's algorithm for large numbers, American Mathematical Monthly 45 (1938)"
    locator: pages 227 to 233
---

Lehmer's GCD computes the [greatest common divisor](/gcd-of-two-integers/) of two long integers with the quotients of the [Euclidean algorithm](/euclidean-algorithm/), but finds most of them from the leading word of each number. It runs Euclid's steps on the top $w$ bits of $u$ and $v$ in single precision, and a test on two quotients, in the form Knuth gives as Algorithm L, proves which of those quotients are the true quotients of the long numbers. Then it applies all the proved steps to $u$ and $v$ at once, with one $2 \times 2$ matrix of single-precision integers. The worst case is still $O(n^2)$ bit operations, but on typical inputs one pass over the long numbers replaces many Euclid steps, which makes it faster than plain Euclid on long numbers. It is the standard gcd for numbers of moderate size, below the threshold where the [half-GCD](/half-gcd/) wins.

## In plain words

Euclid's method for long numbers is slow because each step divides a long number by another long number, just to find a small quotient such as 1 or 2. But the quotient depends almost only on the first digits of the two numbers. So look only at the first digits, which fit in one machine word, and run the cheap steps on them. Keep a small table that records how the steps mix the two numbers. A check tells you how long the short steps still agree with the long ones. When the check fails, apply the recorded mixing to the long numbers in one pass, and start again with their new first digits.

## The problem

**Input.** Integers $a$ and $b$, of any sign, possibly 0.

**Output.** $\gcd(a, b) \ge 0$, with $\gcd(0, 0) = 0$. The algorithm below works on $u = \max(|a|, |b|)$ and $v = \min(|a|, |b|)$; signs do not change the gcd.

**Cost model.** Arbitrary precision on the [word RAM](/word-ram/): integers are arrays of $w$-bit words, each operation on single words costs one unit, and $n$ is the bit length of $u$. Numbers below $2^w$ are **single precision**. Multiplying an $n$-bit number by a single word, or adding two $n$-bit numbers, costs $O(n/w + 1)$.

## The algorithm

```pseudo id=main
LEHMER-GCD(u, v)                                  ▷ u ≥ v ≥ 0; words have w bits
L1  while v ≥ 2^w do
L2      s ← bitlength(u) − w;  û ← ⌊u / 2^s⌋;  v̂ ← ⌊v / 2^s⌋     ▷ leading w bits, same shift
L3      (A, B, C, D) ← (1, 0, 0, 1)
L4      while v̂ + C > 0 and v̂ + D > 0 do
L5          q ← ⌊(û + A) / (v̂ + C)⌋
L6          if q = 0 or q ≠ ⌊(û + B) / (v̂ + D)⌋ then break    ▷ the two quotients must agree
L7          (A, B, C, D) ← (C, D, A − qC, B − qD)
L8          (û, v̂) ← (v̂, û − q v̂)
L9      if B = 0 then (u, v) ← (v, u mod v)                   ▷ no step proved: one long division
L10     else (u, v) ← (A u + B v, C u + D v)                  ▷ apply all proved steps at once
L11 while v ≠ 0 do (u, v) ← (v, u mod v)                      ▷ single-precision Euclid
L12 return u
```

Lines L4 to L8 run Euclid on $(\hat u, \hat v)$ and keep the matrix $M = \begin{pmatrix} A & B \\ C & D \end{pmatrix}$ of the steps done so far, so that the pair the long numbers would reach is $(Au + Bv, Cu + Dv)$. The numbers $\hat u + A$ and $\hat u + B$ bound the leading part of that pair from both sides, and the same holds for $\hat v + C$ and $\hat v + D$, so if both quotients in line L6 agree, the quotient of the long pair is the same. All of $\hat u$, $\hat v$, $A$, $B$, $C$, $D$ stay below $2^w$ in absolute value.

## Example

Take $w = 8$, $u = 27182818$ and $v = 10000000$. Each row is one outer iteration.

| $u$ | $v$ | $s$ | $(\hat u, \hat v)$ | quotients proved | $(A, B; C, D)$ | new $(u, v)$ |
| --- | --- | --- | --- | --- | --- | --- |
| 27182818 | 10000000 | 17 | (207, 76) | 2, 1, 2 | $(-1, 3; 3, -8)$ | (2817182, 1548454) |
| 2817182 | 1548454 | 14 | (171, 94) | 1, 1, 4 | $(-1, 2; 5, -9)$ | (279726, 149824) |
| 279726 | 149824 | 11 | (136, 73) | 1, 1 | $(1, -1; -1, 2)$ | (129902, 19922) |
| 129902 | 19922 | 9 | (253, 38) | 6 | $(0, 1; 1, -6)$ | (19922, 10370) |
| 19922 | 10370 | 7 | (155, 81) | 1, 1 | $(1, -1; -1, 2)$ | (9552, 818) |
| 9552 | 818 | 6 | (149, 12) | none | identity | (818, 554) by line L9 |
| 818 | 554 | 2 | (204, 138) | 1, 2 | $(1, -1; -2, 3)$ | (264, 26) |

Now $v = 26 < 2^8$, and line L11 finishes with the quotients 10, 6 and 2: $264 = 10 \cdot 26 + 4$, $26 = 6 \cdot 4 + 2$, $4 = 2 \cdot 2$. The result is 2. The quotients found, $2, 1, 2, 1, 1, 4, 1, 1, 6, 1, 1, 11, 1, 2, 10, 6, 2$ (with 11 from the long division of 9552 by 818), are exactly those of Euclid's algorithm on $(27182818, 10000000)$, but the long numbers were combined only 7 times instead of 14.

In the first row, after the quotients 2, 1, 2 the test of line L6 compares $\lfloor (\hat u + A)/(\hat v + C) \rfloor = 1$ with $\lfloor (\hat u + B)/(\hat v + D) \rfloor = 4$, which disagree, so the loop stops. In the sixth row, $\hat v = 12$ is too short: the test gives 12 and 11 at once, no step is proved, and line L9 does one ordinary division.

## Correctness

Each outer iteration replaces $(u, v)$ by the result of one or more Euclid steps, so it keeps the gcd by the [GCD recursion theorem](/gcd-recursion-theorem/) and strictly decreases $v$. The key fact is that the quotients accepted in line L6 are the true quotients. Write $u = 2^s(\hat u_0 + \alpha)$ and $v = 2^s(\hat v_0 + \beta)$ with $\alpha, \beta \in [0, 1)$. The current long pair is $(Au + Bv, Cu + Dv)$, and since the signs of $M$ alternate in a checkerboard pattern, $(Au + Bv)/2^s$ lies between $\hat u + A$ and $\hat u + B$, and $(Cu + Dv)/2^s$ between $\hat v + C$ and $\hat v + D$. So the true quotient lies between the two quotients of line L6, and when they agree it equals them. The full proof is in `proofs/correctness.md`.

## Complexity

- **Single-precision parts.** All values in lines L2 to L8 fit in a word plus a sign, so each inner iteration costs $O(1)$. Each inner iteration is a true Euclid step, so by [Lamé's theorem](/lames-theorem/) there are at most $\log_\varphi v + 2 = O(n)$ of them in total.
- **Long parts.** Line L2 costs $O(n/w + 1)$ for the shifts, line L10 costs $O(n/w + 1)$ for four products of a long number by a word, and line L9 costs $O((n/w + 1)(1 + \log_2 q / w))$ for a long division with quotient $q$. The number of outer iterations is at most the number of Euclid steps, $O(n)$, and the sum of $\log_2 q$ over all steps is at most $n$.
- **Worst case.** So the total is $O(n^2 / w + n)$ word operations, which is $O(n^2)$ bit operations, the same order as plain Euclid. The worst case is reached when few steps are proved per pass, for example when the quotients are large.
- **Typical case.** On random inputs, each pass proves a number of steps proportional to $w$, and the number of passes falls by that factor. With the implementation below, on random 3000-bit inputs, a pass proved on average about 7.7 steps with $w = 32$ and about 17 steps with $w = 64$, out of about 1750 Euclid steps in total. The long work is then about 100 passes of $O(n/w)$ each, against about 1750 long divisions for plain Euclid.
- **Space.** The two long numbers and $O(1)$ words: $O(n/w)$ words in all, and $O(1)$ extra beyond the input if the update of line L10 is done in place.

## Properties

- **Same quotients as Euclid.** It produces the exact sequence of Euclid's quotients, grouped. So it also yields the [continued fraction](/continued-fraction/) of $u/v$, and with the product of the matrices it becomes an [extended Euclidean algorithm](/extended-euclidean-algorithm/).
- **Iterative and deterministic.** No recursion.
- **Adaptive to word size.** Larger $w$ proves more steps per pass. Some versions use two words for the leading parts to prove more steps.

## Variants and improvements

- **Collins's and Jebelean's tests.** Knuth's test of line L6 needs two divisions per step. Later conditions decide when to stop from the remainder sequence and the matrix entries alone, with one division per step, and prove almost as many steps.
- **Extended version.** Keep the product of the matrices, or apply each matrix also to the coefficient pairs, to get Bézout coefficients.
- **Double-digit Lehmer.** Use the leading $2w$ bits and a matrix with entries below $2^w$, so that each pass proves about twice as many steps.
- **Half-GCD.** Lehmer's idea, applied recursively to the leading half of the numbers instead of the leading word, gives the [half-GCD](/half-gcd/) with $O(M(n) \log n)$ bit operations, where $M(n)$ is the cost of multiplication.
- **Binary variants.** Lehmer's idea also applies to the [binary GCD](/binary-gcd/), using the trailing bits instead of the leading ones.

## When to use it

Use Lehmer's GCD for integers of a few words up to a few thousand words, where plain Euclid is too slow and the overhead of the half-GCD does not yet pay off; the crossover depends on the multiplication routines and the machine. For single-word inputs, use plain Euclid or the binary GCD. For very long inputs, use the half-GCD.

## Pitfalls

- **Testing only the leading quotient.** Taking $\lfloor \hat u / \hat v \rfloor$ as the quotient is wrong in general. For $w = 8$, $u = 12257478$ and $v = 400528$, the leading parts are $\hat u = 187$ and $\hat v = 6$, with $\lfloor 187/6 \rfloor = 31$, but $\lfloor u/v \rfloor = 30$. The test of line L6 rejects this step.
- **No progress.** If no step is proved, the matrix is the identity and line L10 would change nothing. Line L9 must do an ordinary division, or the loop runs forever. This happens when $v$ is much shorter than $u$.
- **Different shifts.** $\hat u$ and $\hat v$ must use the same shift $s$; shifting each number by its own length loses the ratio.
- **Signs of the matrix.** The entries alternate in sign. In C, compute $Au + Bv$ as a difference of two nonnegative products, chosen by the sign pattern, to avoid signed long arithmetic.
- **Division by zero.** Check $\hat v + C > 0$ and $\hat v + D > 0$ before dividing, as line L4 does.

## Implementations

## History

Derrick Henry Lehmer published the method in "Euclid's algorithm for large numbers" in the American Mathematical Monthly in 1938. Knuth gives it as Algorithm L in Section 4.5.2, with the form of the test used here. Later work by Collins and by Jebelean improved the stopping condition, and the idea of working on leading parts led to the subquadratic [half-GCD](/half-gcd/) of Knuth and Schönhage.

## References
