---
tag: 8QNZZT
kind: algorithm
slug: newton-integer-root
name: Newton's method for integer roots
aliases:
- Newton integer square root
- Newton k-th root
- Heron's method on integers
area: algebra/integer-arithmetic
level: core
summary: Integer Newton iteration that converges quadratically to the floor of the k-th root.
solves: [integer-square-root, integer-nth-root]
model: word-ram
complexity:
  vars: {n: the number of limbs of N, k: the root index, M: the cost M(j) of multiplying two integers of j limbs}
  time: {worst: O((k + log n) M(n)), best: O(M(n))}
  space: {extra: O(n)}
properties: {deterministic: true, recursive: false, in_place: false}
prereqs: [integer-square-root, newton-raphson-method, long-division]
see_also: [integer-nth-root, digit-by-digit-square-root, newton-square-root, newton-raphson-division, newton-iteration, binary-exponentiation, karatsuba-multiplication]
sources:
  - book: isbn:9780521194693
    title: Richard P. Brent and Paul Zimmermann, Modern Computer Arithmetic, Cambridge University Press, 2010
    locator: Section 1.5.1, Square root (Algorithm SqrtInt, the integer Newton iteration and its proof), and Section 1.5.2, k-th root (Algorithm RootInt)
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, third edition
    locator: Section 4.3.3, How fast can we multiply? (Newton's method makes square roots as fast as multiplication, up to a constant factor)
  - book: isbn:9780195328486
    title: Behrooz Parhami, Computer Arithmetic, Algorithms and Hardware Designs, second edition, Oxford University Press, 2010
    locator: Chapter 21, Square-rooting methods (square-rooting by convergence)
---

Newton's method for integer roots computes $s = \lfloor N^{1/k} \rfloor$ with integer arithmetic only, by the step $x \leftarrow \lfloor ((k - 1)x + \lfloor N / x^{k-1} \rfloor) / k \rfloor$. Started at any integer $x \ge s$, the values decrease strictly until they reach $s$, and the first step that does not decrease shows that the root has been found. For $k = 2$ the step is $x \leftarrow \lfloor (x + \lfloor N / x \rfloor)/2 \rfloor$, the ancient method of Heron on integers. Far from the root the error falls by a constant factor per step, and near it the number of correct digits doubles; from a start of the right binary length the method needs $O(\log n)$ steps for fixed $k$, each a division of $n$-limb numbers, so $O(M(n) \log n)$ limb operations. With the working precision doubled at each step, the cost is $O(M(n))$, the cost of a few multiplications.

## In plain words

To find the square root of 814507, guess a number that is surely too big, say 1024. Divide 814507 by the guess: you get 795. The true root lies between the guess and this quotient, so take their average, 909. Divide again: 814507 divided by 909 is 896. The average of 909 and 896 is 902. Divide once more: you get 903, and the average with 902 is 902 again. The guess stopped going down, so 902 is the answer.

Each step uses whole numbers only, dropping fractions. Starting above the root, the guesses always go down, and they never jump below the root. Once the guess is close, each step about doubles the number of correct digits.

## The problem

The input is integers $N \ge 0$ and $k \ge 1$. The output is $s = \lfloor N^{1/k} \rfloor$, the largest integer with $s^k \le N$; this is the [integer square root](/integer-square-root/) for $k = 2$ and the [integer $k$-th root](/integer-nth-root/) in general. $N$ is a multiprecision integer of $n$ limbs in radix $\beta = 2^w$.

**Cost model.** Word RAM with $w$-bit words. Costs are in limb operations, with $M(n)$ the cost of an $n$-limb product; a division of a $2n$-limb number by an $n$-limb number costs $O(M(n))$ by [Newton-Raphson division](/newton-raphson-division/), or $\Theta(n^2)$ by [long division](/long-division/). Step counts are proved where the page says so, and observed otherwise.

## The algorithm

```pseudo id=main
NEWTON-ROOT(N, k)                          ▷ N ≥ 0, k ≥ 1
L1  if k = 1 or N < 2 then return N
L2  x ← 2^⌈B / k⌉ where B is the binary length of N      ▷ x > N^(1/k)
L3  loop
L4      y ← ⌊((k − 1)·x + ⌊N / x^(k−1)⌋) / k⌋
L5      if y ≥ x then return x
L6      x ← y
```

Line L2 chooses a start above the root: $N < 2^B$, so $N^{1/k} < 2^{B/k} \le 2^{\lceil B/k \rceil}$. It is also less than twice $N^{1/k}$, since $N \ge 2^{B-1}$ gives $2^{\lceil B/k \rceil} \le 2^{(B - 1)/k + 1} \le 2N^{1/k}$. Line L4 is one Newton step for the function $f(x) = x^k - N$, rounded down. Line L5 is the stopping test: the first step that does not decrease $x$.

## Example

**Square root of $N = 814507$.** $B = 20$, so $x_0 = 2^{10} = 1024$.

| step | $x$ | $\lfloor N / x \rfloor$ | $y = \lfloor (x + \lfloor N/x \rfloor)/2 \rfloor$ |
|---|---|---|---|
| 1 | 1024 | 795 | 909 |
| 2 | 909 | 896 | 902 |
| 3 | 902 | 903 | 902 |

In step 3, $y = x$, so the algorithm returns 902. Check: $902^2 = 813604 \le 814507 < 815409 = 903^2$, and the remainder is $903$.

**Cube root of the same $N$.** $x_0 = 2^{\lceil 20/3 \rceil} = 128$, and the iteration $x \leftarrow \lfloor (2x + \lfloor N/x^2 \rfloor)/3 \rfloor$ gives 101, 93, 93: the root is 93, with $93^3 = 804357 \le 814507 < 830584 = 94^3$. Both runs were checked by script.

## Correctness

Let $s = \lfloor N^{1/k} \rfloor$ and $g(x) = ((k - 1)x + N/x^{k-1})/k$, the exact Newton step. Since $(k-1)x$ is an integer, line L4 computes $y = \lfloor g(x) \rfloor$. By the inequality of arithmetic and geometric means applied to $k - 1$ copies of $x$ and one copy of $N/x^{k-1}$, $g(x) \ge (x^{k-1} \cdot N/x^{k-1})^{1/k} = N^{1/k}$, so $y \ge s$: no step goes below the root. If $x > s$, then $x^k > N$, so $N/x^{k-1} < x$ and $g(x) < x$, hence $y < x$. If $x = s$, then $N/x^{k-1} \ge x$ and $y \ge x$. So, starting from $x_0 \ge s$, the values decrease strictly while they are above $s$, never pass below $s$, and the first step with $y \ge x$ happens exactly at $x = s$. The full proof is below.

## Complexity

**Steps.** Each step strictly decreases $x$, so there are at most $x_0 - s + 1$ steps; this crude bound is enough for termination. The real count is much smaller. Write $x = s(1 + e)$. Near the root, Newton's method converges quadratically, $e \mapsto$ about $\frac{k-1}{2} e^2$, so the number of correct binary digits doubles. Far from the root, for $e$ near 1, a step multiplies $x$ by about $(k-1)/k$ for large $k$, a linear phase of $O(k)$ steps. From the start of line L2, with $e \le 1$, this gives the estimate $O(k + \log B)$ steps, where $\log B = O(\log n)$ for fixed $w$. We observed, over 50 random $N$ of $B$ binary digits each, at most 5, 9 and 12 steps for $k = 2$ and $B = 64$, $1000$, $10000$, and at most 5, 20 and 23 steps for $k = 30$.

**Cost per step.** Computing $x^{k-1}$ by [binary exponentiation](/binary-exponentiation/) costs $O(M(n))$ limb operations for fixed $k$ (the power has fewer limbs than $N$), and the division $\lfloor N / x^{k-1} \rfloor$ costs $O(M(n))$. So the algorithm as written costs $O(M(n) \log n)$ for fixed $k$, with all steps at full precision.

**Precision doubling.** The early steps need only a few correct digits. Computing the root of the top $2j$ limbs, and using it as the start for the top $4j$ limbs, makes the step costs a geometric series, and the total is $O(M(n))$ for fixed $k$ (Brent and Zimmermann, Sections 1.5.1 and 1.5.2). Both bounds are proved; which version is faster at a given size is observed, and depends on the multiplication and division code.

## Properties

- **Integers only.** No floating point, so no rounding error and no limit on size.
- **Monotone.** The values decrease strictly to the root; there is no oscillation, unlike the floor iteration started below the root.
- **Self-correcting stop.** The test $y \ge x$ needs no separate check of $x^k \le N$; the theorem guarantees that the returned $x$ is the root.
- **The remainder.** $r = N - s^k$ costs one more power and one subtraction.

## Variants and improvements

- **A better start.** A floating-point root of the top 53 bits of $N$, rounded up and scaled, gives about 50 correct bits at once and saves the linear phase.
- **Precision doubling (Algorithm RootInt).** As above: recursive or iterative doubling of the working precision gives $O(M(n))$.
- **Karatsuba square root.** For $k = 2$, Zimmermann's SqrtRem computes the root and the remainder of the top half recursively, then the next quarter by one division; its cost is $O(M(n))$, and GMP uses it.
- **Inverse square root.** The iteration $x \leftarrow x(3 - Nx^2)/2$ for $1/\sqrt{N}$ uses no division. It is used for floating-point square roots and in fixed-point code, and $\sqrt{N} = N \cdot N^{-1/2}$.
- **Digit by digit.** The [digit-by-digit method](/digit-by-digit-square-root/) finds one root digit per step; it costs $\Theta(n^2)$ but needs no division by a long number.
- **Perfect powers.** To decide whether $N = a^k$ for some $k \ge 2$, compute $\lfloor N^{1/k} \rfloor$ for each $k \le \log_2 N$ and test its power. The implementation includes this test.

## When to use it

Use Newton's method for integer roots of any size, when only integer arithmetic is available, and as the reference implementation against which faster code is tested. For a single word, a hardware or floating-point square root with a correction step is faster. For very large $N$, use the precision-doubling form or the Karatsuba square root; library functions such as Python's `math.isqrt` and GMP's `mpz_sqrtrem` do this.

## Pitfalls

- **Starting below the root.** From $x_0 < s$ the first step goes up, since $y \ge s > x_0$, and the test $y \ge x$ stops at once and returns the wrong value $x_0$. Start at or above the root.
- **The two-cycle of the wrong test.** Testing $y = x$ instead of $y \ge x$ can loop forever: for $k = 2$ and $N = s^2 + 2s$, that is $N + 1$ a perfect square, $s$ and $s + 1$ map to each other. For $N = 8$, $x = 3$ gives $y = \lfloor (3 + 2)/2 \rfloor = 2$, and $x = 2$ gives $y = 3$.
- **Division by zero.** The start must be positive; line L1 handles $N = 0$ and $N = 1$ before any division.
- **Floating-point starts that are too small.** A float root rounded down can be below $s$. Round up, or add one before starting.
- **Large $k$.** For $k > B$ the root is 1, and $x^{k-1}$ is wasted work; stop early when $2^k > N$.

## Implementations

## History

The square root iteration $x \leftarrow (x + N/x)/2$ is described by Heron of Alexandria in the first century, and the method may be older, from Babylonian computation. Newton (1669) and Raphson (1690) gave the general method for equations, of which this is the case $x^k - N$. The integer form with floors, and the proof that it stops exactly at the floor of the root, are standard in computer arithmetic; Brent and Zimmermann give it as Algorithm SqrtInt and Algorithm RootInt with their proofs, and Zimmermann's Karatsuba square root (1999) brought the cost to $O(M(n))$ with a small constant.

## References
