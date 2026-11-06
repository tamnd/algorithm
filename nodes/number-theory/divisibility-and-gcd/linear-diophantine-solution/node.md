---
tag: 747E8M
kind: algorithm
slug: linear-diophantine-solution
name: Finding a solution of a linear Diophantine equation
area: number-theory/divisibility-and-gcd
level: core
summary: Uses the extended Euclidean algorithm to find one integer solution of a x plus b y equals c, or reports that none exists.
solves: [linear-diophantine-equation]
model: word-ram
complexity:
  vars: {m: the smaller of the absolute values of a and b, n: "the largest bit length of a, b and c"}
  time: {worst: Θ(1 + log m), best: Θ(1)}
  space: {extra: Θ(1)}
  bit_operations: {worst: O(n^2)}
properties: {deterministic: true, recursive: false}
prereqs: [linear-diophantine-equation, extended-euclidean-algorithm, gcd-recursion-theorem]
see_also: [linear-diophantine-solutions-in-interval, bezouts-identity, linear-congruence, modular-linear-equation-solver, chinese-remainder-theorem, modular-inverse, half-gcd, lames-theorem]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 31.2, Greatest common divisor (EXTENDED-EUCLID and the bound on its recursive calls), and Section 31.4, Solving modular linear equations
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, third edition
    locator: Section 4.5.2, The Greatest Common Divisor (Algorithm X, the extended Euclidean algorithm, with its invariant and its use for linear equations in integers)
  - book: isbn:9780521194693
    title: Richard P. Brent and Paul Zimmermann, Modern Computer Arithmetic
    locator: Section 1.6.2, Extended GCD
  - url: "https://cp-algorithms.com/algebra/linear-diophantine-equation.html"
    locator: sections Finding a solution and Getting all solutions (the reduction to the extended algorithm on absolute values, with the signs fixed afterward)
---

This algorithm finds one integer solution $(x, y)$ of the [linear Diophantine equation](/linear-diophantine-equation/) $ax + by = c$, or reports that there is none. It runs the [extended Euclidean algorithm](/extended-euclidean-algorithm/) on $|a|$ and $|b|$ to get $g = \gcd(a, b)$ and coefficients $s$, $t$ with $|a| s + |b| t = g$. If $g$ does not divide $c$ there is no solution; otherwise it scales the coefficients by $c/g$ and restores the signs. It takes $O(1 + \log \min(|a|, |b|))$ word operations and $O(1)$ extra space, and every other solution is the returned one plus a multiple of $(b/g, -a/g)$.

## In plain words

First find the largest number that divides both coefficients, by the usual method of repeated division with remainder. While doing so, keep track of how each remainder is built from the two coefficients: so many of the first one, plus so many of the second one. The last nonzero remainder is the largest common divisor, and you then know how to build it from the two coefficients. If that divisor does not divide the right side, no answer exists. If it does, build the right side by repeating the same recipe the right number of times. Minus signs in the input only flip the signs of the answer.

## The problem

**Input.** Integers $a$, $b$ and $c$, of any sign, possibly 0.

**Output.** Integers $(x, y)$ with $ax + by = c$, or NONE if no such pair exists.

By the theorem on the [problem page](/linear-diophantine-equation/), a solution exists if and only if $g = \gcd(a, b)$ divides $c$ (with the convention $\gcd(0, 0) = 0$ and "0 divides only 0").

**Cost model.** On the [word RAM](/word-ram/), $a$, $b$ and $c$ are $w$-bit words and each arithmetic operation costs one unit; the intermediate values fit in a word, but the output can need $2w$ bits (see Pitfalls). With arbitrary precision, $n$ is the largest bit length of $a$, $b$ and $c$, and the cost is counted in bit operations.

## The algorithm

Let $\sigma_a = -1$ if $a < 0$ and $\sigma_a = 1$ otherwise, and the same for $\sigma_b$.

```pseudo id=main
LINEAR-DIOPHANTINE(a, b, c)                  ▷ one solution of a x + b y = c, or NONE
L1  if a = 0 and b = 0 then
L2      if c = 0 then return (0, 0) else return NONE
L3  (r₀, s₀, t₀) ← (|a|, 1, 0); (r₁, s₁, t₁) ← (|b|, 0, 1)
L4  while r₁ ≠ 0 do                            ▷ rᵢ = |a| sᵢ + |b| tᵢ for i = 0, 1
L5      q ← ⌊r₀ / r₁⌋
L6      (r₀, r₁) ← (r₁, r₀ − q r₁)
L7      (s₀, s₁) ← (s₁, s₀ − q s₁)
L8      (t₀, t₁) ← (t₁, t₀ − q t₁)
L9  g ← r₀                                     ▷ g = gcd(a, b) = |a| s₀ + |b| t₀
L10 if g does not divide c then return NONE
L11 x ← σ_a s₀ (c / g); y ← σ_b t₀ (c / g)
L12 return (x, y)
```

Lines L3 to L9 are the extended Euclidean algorithm in its iterative form, with the three sequences updated by the same quotient. Line L11 uses $a \sigma_a = |a|$ and $b \sigma_b = |b|$. The division $c/g$ in line L11 is exact.

## Example

Solve $1071x + 462y = 63$. The loop runs on $(1071, 462)$:

| step | $q$ | $r_0$ | $r_1$ | $s_0$ | $s_1$ | $t_0$ | $t_1$ |
| --- | --- | --- | --- | --- | --- | --- | --- |
| start | | 1071 | 462 | 1 | 0 | 0 | 1 |
| 1 | 2 | 462 | 147 | 0 | 1 | 1 | $-2$ |
| 2 | 3 | 147 | 21 | 1 | $-3$ | $-2$ | 7 |
| 3 | 7 | 21 | 0 | $-3$ | 22 | 7 | $-51$ |

Each row satisfies $r_i = 1071 s_i + 462 t_i$; for example $147 = 1071 \cdot 1 + 462 \cdot (-2)$. The loop stops with $g = 21$, $s_0 = -3$, $t_0 = 7$: $1071 \cdot (-3) + 462 \cdot 7 = 21$. Since $63 / 21 = 3$, line L11 gives $(x, y) = (-9, 21)$, and $1071 \cdot (-9) + 462 \cdot 21 = -9639 + 9702 = 63$. The last column pair $(s_1, t_1) = (22, -51)$ is $(b/g, -a/g)$, the step between consecutive solutions.

With signs: for $-4x + 6y = 10$ the loop runs on $(4, 6)$, gives $g = 2 = 4 \cdot (-1) + 6 \cdot 1$, and line L11 returns $x = -1 \cdot (-1) \cdot 5 = 5$, $y = 1 \cdot 5 = 5$; indeed $-20 + 30 = 10$. For $6x + 9y = 7$, $g = 3$ does not divide 7, and line L10 returns NONE.

## Correctness

The loop keeps the [loop invariant](/loop-invariant/) $r_0 = |a| s_0 + |b| t_0$, $r_1 = |a| s_1 + |b| t_1$, $r_0, r_1 \ge 0$ and $\gcd(r_0, r_1) = \gcd(a, b)$. It holds at line L3. Lines L6 to L8 replace each pair by the same combination (second, first minus $q$ times second), so the linear relations stay true, and $\gcd(r_1, r_0 - q r_1) = \gcd(r_0, r_1)$ by the [GCD recursion theorem](/gcd-recursion-theorem/). The value $r_1$ is a nonnegative integer that strictly decreases after the first iteration, so the loop ends, with $r_1 = 0$ and $g = r_0 = \gcd(a, b) \ge 1$ (the inputs are not both 0). If $g \nmid c$ there is no solution, because $g$ divides $ax + by$ for all integers. Otherwise $ax + by = (|a| s_0 + |b| t_0)(c/g) = c$. The full proof is in `proofs/correctness.md`.

## Complexity

- **Iterations.** After the first iteration $r_0 > r_1$, and the loop is the Euclidean algorithm on $(|a|, |b|)$. By [Lamé's theorem](/lames-theorem/) it takes at most $\log_\varphi m + 2$ iterations, where $m = \min(|a|, |b|) \ge 1$ and $\varphi$ is the golden ratio, plus one iteration that swaps the inputs when $|a| < |b|$. If $m = 0$, it takes at most one iteration. Each iteration does one division and three multiply-subtract steps, so the time is $\Theta(1 + \log m)$ in the worst case, reached by consecutive Fibonacci numbers, and $\Theta(1)$ in the best case, for example when $|b| = 1$.
- **Space.** Six integers and $q$: $\Theta(1)$ words.
- **Size of the coefficients.** For positive $|a| \ne |b|$, the final coefficients satisfy $|s_0| \le |b|/(2g)$ and $|t_0| \le |a|/(2g)$, and every intermediate $|s_i|$, $|t_i|$ is at most $\max(|a|, |b|)/g$. So all values in the loop fit in a word.
- **Bit operations.** With schoolbook arithmetic on $n$-bit inputs, dividing $r_0$ by $r_1$ costs $O((1 + \log q) \cdot n)$, and the sum of $\log q$ over the run is at most $\log(|a| / g) \le n$, so the remainders cost $O(n^2)$. The coefficient updates obey the same bound, since $|s_i|, |t_i| < 2^n$. The final products with $c/g$ cost $O(n^2)$. In total $O(n^2)$ bit operations.

## Properties

- **Deterministic and iterative.** No recursion, so no stack depth issue on long inputs.
- **Returns a specific solution.** The pair is $(\sigma_a s_0\, c/g,\ \sigma_b t_0\, c/g)$ with the Bézout coefficients of the extended Euclidean algorithm. It is not the smallest solution; see Variants.
- **The step comes free.** At the end, $(s_1, t_1) = \pm (|b|/g, -|a|/g)$, which gives the general solution without another division.
- **Total.** It handles $a = 0$, $b = 0$, negative values and $c = 0$ (returning $(0, 0)$ when $c = 0$).

## Variants and improvements

- **All solutions.** Return $(x_0, y_0)$ and the step $(b/g, -a/g)$; the solutions are $(x_0 + k b/g,\ y_0 - k a/g)$ for $k \in \mathbb{Z}$.
- **Smallest nonnegative $x$.** If $b \ne 0$, replace $x_0$ by $x_0 \bmod (|b|/g)$ and recompute $y_0 = (c - a x_0)/b$. Then $0 \le x_0 < |b|/g$, and the output has about as many bits as the input.
- **Solutions in a range.** Shift $k$ into the allowed interval of $x$ and of $y$ and count; see [solutions in an interval](/linear-diophantine-solutions-in-interval/).
- **Only $x$.** Drop the $t$ sequence (lines L8) and compute $y = (c - a x)/b$ at the end. This saves a third of the work and is the usual form for a [modular inverse](/modular-inverse/).
- **Faster gcd.** For long integers, replace lines L3 to L9 by an extended [Lehmer's GCD](/lehmers-gcd/) or [half-GCD](/half-gcd/), which give $g$, $s_0$ and $t_0$ in $O(n^2)$ with a smaller constant or in $O(M(n) \log n)$ bit operations.
- **Several unknowns.** Fold the algorithm over $a_1, \ldots, a_k$ as in the [GCD of an array](/gcd-of-array/).

## When to use it

Use it to solve one equation $ax + by = c$, to solve a [linear congruence](/linear-congruence/), to compute a [modular inverse](/modular-inverse/), and to merge two congruences in the [Chinese remainder theorem](/chinese-remainder-theorem/), especially when the moduli need not be coprime. For a modular inverse modulo a prime $p$, Fermat's little theorem $a^{p-2}$ is an alternative with $O(\log p)$ multiplications, but the extended algorithm is usually faster and also works for composite moduli.

## Pitfalls

- **Overflow of the output.** The coefficients fit in a word, but $s_0 \cdot (c/g)$ can need about $2w$ bits. For $a = F_{45} = 1134903170$, $b = F_{46} = 1836311903$ and $c = 2^{31} - 1$, all below $2^{31}$, the coefficients are $s_0 = -701408733$ and $t_0 = 433494437$, and $x = s_0 c = -1506263783980489251$ has 61 bits. Use a double-width product, or reduce $x_0$ modulo $|b|/g$ before multiplying, as in Variants.
- **Signs.** Running the algorithm on $a$ and $b$ with a language's truncated division gives a correct $g$ only up to sign. Work with $|a|$ and $|b|$ and put the signs back at line L11, or normalize $g$ to be positive.
- **Forgetting $c/g$.** The coefficients solve $ax + by = g$, not $ax + by = c$. Multiply by $c/g$, not by $c$.
- **The case $a = b = 0$.** Here $g = 0$ and line L10 would divide by zero; lines L1 and L2 handle it.
- **Recursion.** The recursive form of the extended algorithm is fine in C, but in Python the iterative form avoids the recursion limit on numbers with thousands of digits.

## Implementations

## History

The solution of $ax + by = c$ by the Euclidean algorithm is old. The Indian kuttaka method, which derives a solution from the sequence of Euclidean quotients, appears in Aryabhata's Aryabhatiya (around 499). In Europe, Claude Gaspard Bachet de Méziriac gave the method for integers in the seventeenth century, and Étienne Bézout proved the analogous identity for polynomials in the eighteenth. Knuth presents the iterative extended algorithm as Algorithm X in Section 4.5.2, and CLRS gives the recursive EXTENDED-EUCLID in Section 31.2.

## References
