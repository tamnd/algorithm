---
tag: XRMYSW
kind: algorithm
slug: modular-linear-equation-solver
name: Modular linear equation solver
aliases:
- MODULAR-LINEAR-EQUATION-SOLVER
area: number-theory/modular-arithmetic
level: core
summary: Uses the extended Euclidean algorithm to compute gcd(a, n) and list every solution of a x congruent to b modulo n.
solves: [modular-linear-equation]
model: word-ram
complexity:
  vars: {n: the modulus, d: the number of solutions, k: the number of binary digits of n}
  time: {worst: O(log n + d), best: Θ(1)}
  space: {extra: Θ(1)}
  bit_operations: {worst: O(k^2 + d k)}
properties: {deterministic: true, recursive: false}
prereqs: [modular-linear-equation, linear-congruence, extended-euclidean-algorithm, loop-invariant]
see_also: [modular-inverse, chinese-remainder-theorem, linear-diophantine-solution, bezouts-identity, garner-algorithm]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 31.4, Solving modular linear equations (the procedure MODULAR-LINEAR-EQUATION-SOLVER and the theorems behind it)
  - book: isbn:9780849385230
    title: Alfred J. Menezes, Paul C. van Oorschot and Scott A. Vanstone, Handbook of Applied Cryptography, CRC Press, 1997
    locator: Section 2.4.3, Fact 2.119, and Section 2.4.2, Algorithm 2.107 (extended Euclidean algorithm)
  - book: isbn:9780199219865
    title: G. H. Hardy and E. M. Wright, An Introduction to the Theory of Numbers, sixth edition
    locator: Chapter 5, Section 5.4, Linear congruences
---

The modular linear equation solver lists every residue $x \in \{0, \ldots, n - 1\}$ with $ax \equiv b \pmod n$, the [modular linear equation](/modular-linear-equation/), or reports that there is none. It runs the [extended Euclidean algorithm](/extended-euclidean-algorithm/) on $a$ and $n$ to get $d = \gcd(a, n)$ and a coefficient $x'$ with $ax' \equiv d \pmod n$, tests whether $d$ divides $b$, and then writes down the $d$ solutions $x_0, x_0 + n/d, \ldots$ with $x_0 = x'(b/d) \bmod n/d$. It takes $O(\log n + d)$ word operations, which is optimal up to the gcd step, since the output has $d$ entries. The procedure is MODULAR-LINEAR-EQUATION-SOLVER of CLRS Section 31.4.

## In plain words

You want every position on a clock that a given multiplier sends to a given target. First, run the extended form of Euclid's method on the multiplier and the clock size. It gives their largest common factor, and a number that the multiplier sends to that factor. If the factor does not divide the target, stop: there is no answer. Otherwise, scale that number up so that it reaches the target instead. This gives the first answer. All other answers follow from it at even steps of the clock size divided by the factor, and there are as many answers as the size of the factor.

## The problem

The input is three integers $a$, $b$ and $n$ with $n \ge 1$. The output is the list, in increasing order, of all $x$ with $0 \le x < n$ and $n \mid ax - b$. The [linear congruence](/linear-congruence/) page proves that this list is empty when $d = \gcd(a, n)$ does not divide $b$, and otherwise has exactly $d$ entries, spaced $n/d$ apart.

**Cost model.** On the [word RAM](/word-ram/) the inputs fit in words, and an addition, a multiplication or a division with remainder costs one unit. The product $x' \cdot (b/d)$ in line L5 can need two words; see the pitfalls. Residues are the integers $0, \ldots, n - 1$. For arbitrary-precision inputs, $n$ has $k$ binary digits and cost is counted in bit operations.

## The algorithm

```pseudo id=main
MODULAR-LINEAR-EQUATION-SOLVER(a, b, n)        ▷ n ≥ 1
L1  a ← a mod n, b ← b mod n                    ▷ now 0 ≤ a, b < n
L2  (d, x′, y′) ← EXTENDED-EUCLID(a, n)         ▷ d = gcd(a, n) = a·x′ + n·y′
L3  if b mod d ≠ 0 then return the empty list
L4  m ← n / d                                   ▷ the spacing of the solutions
L5  x0 ← (x′ · (b / d)) mod m                   ▷ the smallest solution
L6  X ← the empty list
L7  for i ← 0 to d − 1 do
L8      append x0 + i · m to X
L9  return X
```

Line L1 replaces $a$ and $b$ by their least non-negative residues, which does not change the set of solutions. Line L2 is the [extended Euclidean algorithm](/extended-euclidean-algorithm/); since $n \ge 1$, the result $d$ is at least 1, so the divisions of lines L3 to L5 are defined. When $a = 0$, it returns $(n, 0, 1)$. Line L3 is the solvability test. Line L5 multiplies the [Bézout coefficient](/bezouts-identity/) $x'$ by $b/d$, which turns $ax' \equiv d$ into $a x_0 \equiv b$, and reduces the result modulo $m = n/d$ to get the smallest solution. Since $0 \le x_0 < m$ and $d \cdot m = n$, the loop of lines L7 and L8 produces numbers in $[0, n)$ in increasing order, with no reduction modulo $n$.

CLRS reduces $x_0$ modulo $n$ and prints $(x_0 + i(n/d)) \bmod n$. That gives the same set, but not in sorted order. Reducing modulo $m$ in line L5 gives the sorted list directly.

## Example

Solve $14x \equiv 30 \pmod{100}$, the example of CLRS. Line L1 leaves $a = 14$, $b = 30$. Line L2 runs the extended Euclidean algorithm on $(14, 100)$. Each row shows the remainder pair and the coefficients $s, t$ of the current remainder, with $14s + 100t = r$:

| pass | $q$ | $(r_0, r_1)$ | $(s_0, s_1)$ | $(t_0, t_1)$ |
| --- | --- | --- | --- | --- |
| start | | (14, 100) | (1, 0) | (0, 1) |
| 1 | 0 | (100, 14) | (0, 1) | (1, 0) |
| 2 | 7 | (14, 2) | (1, −7) | (0, 1) |
| 3 | 7 | (2, 0) | (−7, 50) | (1, −7) |

So $d = 2$, $x' = -7$, $y' = 1$, and $14 \cdot (-7) + 100 \cdot 1 = 2$. Line L3: $30 \bmod 2 = 0$, so solutions exist. Line L4: $m = 50$. Line L5: $x_0 = (-7 \cdot 15) \bmod 50 = -105 \bmod 50 = 45$. Lines L7 and L8 give $X = [45, 95]$. Check: $14 \cdot 45 = 630$ and $14 \cdot 95 = 1330$, both $\equiv 30 \pmod{100}$.

A second run, on $35x \equiv 10 \pmod{50}$: the extended Euclidean algorithm gives $d = 5$ and $x' = 3$, since $35 \cdot 3 - 50 \cdot 2 = 5$. Then $m = 10$, $x_0 = 3 \cdot 2 \bmod 10 = 6$, and $X = [6, 16, 26, 36, 46]$.

## Correctness

Line L2 returns $d = \gcd(a, n)$ and $x'$ with $ax' + ny' = d$, by the correctness of the extended Euclidean algorithm. If $d \nmid b$, there is no solution, so line L3 is right to return the empty list. Otherwise $a \cdot x'(b/d) = b - n y'(b/d) \equiv b \pmod n$, so $x'(b/d)$ is a solution. The solutions form one residue class modulo $m = n/d$, so $x_0$, which is congruent to $x'(b/d)$ modulo $m$, is a solution too, and it is the least non-negative one. The loop keeps the [loop invariant](/loop-invariant/) that $X$ holds, in increasing order, the solutions in $[0, i \cdot m)$, and stops at $i = d$, where $d \cdot m = n$. The full proof is below.

## Complexity

**Gcd step.** The loop of the extended Euclidean algorithm on $(a, n)$ with $0 \le a < n$ makes one pass that swaps the two numbers when $a > 0$ (its quotient is 0), and then the passes of the Euclidean algorithm on $(n, a)$, at most $2 + \log_\varphi a$ by [Lamé's theorem](/lames-theorem/), where $\varphi$ is the golden ratio. So line L2 takes $O(\log n)$ time in the worst case.

**The rest.** Lines L1 and L3 to L6 take $O(1)$ operations. The loop makes $d$ passes of $O(1)$ each. The total is $O(\log n + d)$ in the worst case. The best case is $\Theta(1)$, for example when $a \equiv 0$ and $n \nmid b$: the extended Euclidean algorithm makes one pass and line L3 returns.

**Space.** Besides the output list, the algorithm keeps a constant number of integers, all at most $n$ in absolute value: the coefficients of the extended Euclidean algorithm are bounded by $n$ (see its page), and $x_0 < m \le n$. So the extra space is $\Theta(1)$ words.

**Optimality.** The output has $d$ entries, so $\Omega(d)$ time is needed to write it. When $d$ is small the cost is that of one extended gcd.

**Bit operations.** For $n$ of $k$ binary digits, line L2 costs $O(k^2)$ with classical arithmetic, line L5 costs $O(k^2)$, and the loop does $d$ additions of $k$-digit numbers, $O(dk)$. The total is $O(k^2 + dk)$.

## Properties

- **Output-sensitive.** The cost is $O(\log n)$ plus a constant for each solution.
- **Sorted output.** The solutions come in increasing order, because $x_0 < m$.
- **Deterministic and iterative.** No randomness, no recursion. The CLRS version of EXTENDED-EUCLID is recursive; the loop form used here has no stack.
- **Exact.** All intermediate values are integers bounded by $n$, except the product in line L5, which is below $n^2$.

## Variants and improvements

- **Compact output.** Stop after line L5 and return $(x_0, m)$, or "none". This costs $O(\log n)$ even when $d$ is huge, and describes the same set.
- **Through the inverse.** Compute $u = (a/d)^{-1} \bmod m$ with any [modular inverse](/modular-inverse/) method and set $x_0 = u \cdot (b/d) \bmod m$. The extended Euclidean algorithm on $(a/d, m)$ makes the same number of passes as on $(a, n)$, since all remainders are divided by $d$.
- **Half extended gcd.** Line L2 needs only $x'$, not $y'$, so the $t$ column of the extended Euclidean algorithm can be dropped.
- **Many right-hand sides.** For a fixed $a$ and $n$ and many values of $b$, run line L2 once and repeat lines L3 to L9 for each $b$.
- **Several congruences.** To solve a system $a_i x \equiv b_i \pmod{n_i}$, use the compact form for each one and combine the classes with the [Chinese remainder theorem](/chinese-remainder-theorem/).

## When to use it

Use it when every solution modulo $n$ is needed and $d$ is small, as in exercises and in the analysis of small cycles. When only one solution or the general solution is needed, use the compact variant: it avoids output of size up to $n$. When $\gcd(a, n) = 1$ is known in advance, a single [modular inverse](/modular-inverse/) and a product are enough. For a prime modulus and a secret $a$, an inverse by [Fermat's little theorem](/fermat-little-theorem/) avoids the data-dependent branches of the Euclidean algorithm.

## Pitfalls

- **A negative coefficient.** The coefficient $x'$ of line L2 is often negative, as $-7$ in the example. In C, Java and Go, `%` returns a negative remainder for a negative left operand. Line L5 must use a remainder in $[0, m)$, for example `((t % m) + m) % m`.
- **Overflow in line L5.** $|x'| \le n/d$ and $b/d < n/d$, so the product can approach $n^2$. With 64-bit words, compute it with a 128-bit product or a [modular multiplication](/modular-multiplication/) routine, or reduce $x'$ and $b/d$ modulo $m$ first and then multiply with double width.
- **Reducing modulo n instead of m.** Taking $x_0 = x'(b/d) \bmod n$, as in CLRS, and then $x_0 + i m$ without a final reduction modulo $n$ gives numbers above $n$. Either reduce each entry modulo $n$ or, as in line L5, reduce $x_0$ modulo $m$.
- **Skipping line L1.** An EXTENDED-EUCLID that assumes non-negative inputs can return a wrong sign for $d$ when $a < 0$. Reduce $a$ and $b$ first.
- **Listing a huge solution set.** For $a = 0$ and $b = 0$ the list has $n$ entries. With a 64-bit modulus this cannot be stored; return the compact form.

## Implementations

## History

Gauss introduced the notation $a \equiv b \pmod n$ and the systematic theory of congruences, including linear ones, in his *Disquisitiones Arithmeticae* of 1801; Hardy and Wright give the modern treatment in Chapter 5. The method of solving a linear equation in integers by the chain of divisions of Euclid is much older and is described on the [extended Euclidean algorithm](/extended-euclidean-algorithm/) page. The procedure with this name, and the example $14x \equiv 30 \pmod{100}$, are from Section 31.4 of CLRS.

## References
