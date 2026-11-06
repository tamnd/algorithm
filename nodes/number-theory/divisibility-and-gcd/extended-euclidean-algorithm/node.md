---
tag: QQCABS
kind: algorithm
slug: extended-euclidean-algorithm
name: Extended Euclidean algorithm
aliases:
- extended GCD
- Bézout coefficients algorithm
area: number-theory/divisibility-and-gcd
level: core
summary: Computes gcd(a, b) together with integers x, y satisfying ax + by = gcd(a, b).
solves: [gcd-of-two-integers]
model: word-ram
complexity:
  vars: {m: the smaller of the absolute values of the inputs, n: the bit length of the larger input}
  time: {worst: Θ(log m), best: Θ(1)}
  space: {extra: Θ(1)}
  bit_operations: {worst: O(n^2)}
properties: {deterministic: true, recursive: false}
history:
  year: 499
  people: [Aryabhata, Claude Gaspard Bachet de Méziriac]
  note: Indian kuttaka method for linear equations in integers; Bachet gave the method in Europe in 1624.
prereqs: [euclidean-algorithm, bezouts-identity, loop-invariant]
see_also: [modular-inverse, linear-diophantine-equation, chinese-remainder-theorem, continued-fraction-convergents, binary-gcd, half-gcd, batch-modular-inverse, rsa-cryptosystem]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 31.2, Greatest common divisor (the procedure EXTENDED-EUCLID and its analysis)
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, third edition
    locator: Section 4.5.2, The greatest common divisor (Algorithm X, the extended Euclidean algorithm, and its exercises on the size of the coefficients)
  - book: isbn:9780387252827
    title: Richard Crandall and Carl Pomerance, Prime Numbers, A Computational Perspective, second edition
    locator: Section 2.1.1, Greatest common divisor and inverse (the extended gcd and modular inversion)
  - url: "https://en.wikipedia.org/wiki/Extended_Euclidean_algorithm"
    locator: Wikipedia, Extended Euclidean algorithm (the table form, the bounds on the Bézout coefficients, and the link to continued fractions)
---

The extended Euclidean algorithm computes the [greatest common divisor](/greatest-common-divisor/) $g$ of two integers $a$ and $b$ together with integers $x$ and $y$ such that $ax + by = g$, the coefficients of [Bézout's identity](/bezouts-identity/). It runs the [Euclidean algorithm](/euclidean-algorithm/) and carries along, for each remainder, the way to write it as a combination of $a$ and $b$. The number of steps is the same, $O(\log \min(|a|, |b|))$, and the coefficients it returns are small: $|x| \le |b|/(2g)$ and $|y| \le |a|/(2g)$ except in the trivial case where $b$ divides $a$. It is the standard way to compute a [modular inverse](/modular-inverse/), to solve a [linear Diophantine equation](/linear-diophantine-equation/), and to combine congruences in the [Chinese remainder theorem](/chinese-remainder-theorem/).

## In plain words

The Euclidean algorithm finds the largest number that divides two given numbers by taking remainders again and again. Each remainder is the first number minus some copies of the second, so it can be written as so many copies of the first input plus so many copies of the second, where a count may be negative.

The extended algorithm keeps these two counts for the last two remainders. When a new remainder is made from the last two, its counts are made from their counts in the same way. At the end, the last non-zero remainder is the greatest common divisor, and its two counts are the answer. The counts are the tool for undoing multiplication when you work with remainders, which is what a modular inverse is.

## The problem

The input is two integers $a$ and $b$, of any sign, possibly zero. The output is $(g, x, y)$ with $g = \gcd(a, b) \ge 0$ and $ax + by = g$. For $(0, 0)$ the result is $(0, 1, 0)$. The pair $(x, y)$ is not unique: if $(x, y)$ works, so does $(x + kb/g, \, y - ka/g)$ for each integer $k$. The algorithm returns one particular pair, with the size bounds proved below.

**Cost model.** On the [word RAM](/word-ram/), the inputs fit in a signed machine word, and a division with remainder or a multiplication costs one step; bounds count loop passes. All intermediate values fit in a word, as shown below. For [arbitrary-precision](/arbitrary-precision-arithmetic/) inputs of $n$ binary digits, the cost is in bit operations with schoolbook multiplication and division.

## The algorithm

The loop keeps three pairs. The pair $(r_0, r_1)$ runs through the remainders of the Euclidean algorithm on $(|a|, |b|)$, and the pairs $(s_0, s_1)$ and $(t_0, t_1)$ hold their coefficients, so that $|a| s_j + |b| t_j = r_j$ for $j = 0, 1$ at all times.

```pseudo id=main
EXTENDED-EUCLID(a, b)
L1  (r0, r1) ← (|a|, |b|)
L2  (s0, s1) ← (1, 0)                 ▷ |a|·1 + |b|·0 = r0
L3  (t0, t1) ← (0, 1)                 ▷ |a|·0 + |b|·1 = r1
L4  while r1 ≠ 0 do
L5      q ← ⌊r0 / r1⌋
L6      (r0, r1) ← (r1, r0 − q·r1)    ▷ the Euclidean step
L7      (s0, s1) ← (s1, s0 − q·s1)    ▷ the same step on the coefficients
L8      (t0, t1) ← (t1, t0 − q·t1)
L9  x ← sgn(a)·s0, y ← sgn(b)·t0      ▷ sgn(z) = −1 if z < 0, else 1
L10 return (r0, x, y)
```

Lines L6 to L8 apply the same linear step to the three pairs, so the relation $|a| s + |b| t = r$ carries over from the old values to the new one. At exit $r_0$ is the gcd and $(s_0, t_0)$ are its coefficients for $|a|$ and $|b|$. Line L9 moves the signs of the inputs onto the coefficients, since $a \cdot \operatorname{sgn}(a) = |a|$. Working with $|a|$ and $|b|$ keeps every remainder non-negative, so the result does not depend on how a language rounds the division of negative numbers.

If only $x$ is needed, as for a modular inverse, the $t$ pair (line L8) can be dropped; then $y = (g - ax)/b$ when $b \ne 0$.

## Example

Run the algorithm on $(240, 46)$. Row $i$ shows $r_i$ and its coefficients, with $240 s_i + 46 t_i = r_i$; the quotient $q_i = \lfloor r_{i-1} / r_i \rfloor$ is computed in the pass that leaves row $i$.

| $i$ | $r_i$ | $q_i$ | $s_i$ | $t_i$ |
|---|---|---|---|---|
| 0 | 240 | | 1 | 0 |
| 1 | 46 | 5 | 0 | 1 |
| 2 | 10 | 4 | 1 | −5 |
| 3 | 6 | 1 | −4 | 21 |
| 4 | 4 | 1 | 5 | −26 |
| 5 | 2 | 2 | −9 | 47 |
| 6 | 0 | | 23 | −120 |

The last non-zero remainder is $2$, so the result is $(2, -9, 47)$: $240 \cdot (-9) + 46 \cdot 47 = -2160 + 2162 = 2$. The bounds hold: $|x| = 9 \le 46/4$ and $|y| = 47 \le 240/4$. The last row has $|s_6| = 23 = 46/2$ and $|t_6| = 120 = 240/2$, and $240 \cdot 23 - 46 \cdot 120 = 0$. With signs, $\text{EXTENDED-EUCLID}(-240, 46) = (2, 9, 47)$.

**A modular inverse.** In a textbook [RSA](/rsa-cryptosystem/) example, the public exponent is $e = 17$ and $\varphi = 3120$. EXTENDED-EUCLID$(3120, 17)$ returns $(1, 2, -367)$, so $17 \cdot (-367) \equiv 1 \pmod{3120}$, and the private exponent is $-367 \bmod 3120 = 2753$.

## Correctness

The [loop invariant](/loop-invariant/) is $|a| s_j + |b| t_j = r_j$ for $j = 0, 1$, with $(r_0, r_1)$ the current pair of the Euclidean algorithm. Lines L1 to L3 make it true: $|a| \cdot 1 + |b| \cdot 0 = |a|$ and $|a| \cdot 0 + |b| \cdot 1 = |b|$. A pass keeps it, because the new $r_1$ is $r_0 - q r_1$ and the new $s_1, t_1$ are formed with the same $q$, so $|a|(s_0 - q s_1) + |b|(t_0 - q t_1) = r_0 - q r_1$. The $r$ values are exactly those of the [Euclidean algorithm](/euclidean-algorithm/), so the loop stops with $r_0 = \gcd(a, b)$. Then $|a| s_0 + |b| t_0 = \gcd(a, b)$, and line L9 turns this into $ax + by = \gcd(a, b)$. The full proof, with the bounds on the coefficients, is in the proofs.

## Complexity

**Steps.** The loop runs exactly as many times as the Euclidean algorithm on $(|a|, |b|)$: at most $1 + \log_\varphi m$ times when $|a| \ge |b| \ge 1$, with $m = \min(|a|, |b|)$ and $\varphi$ the golden ratio, and one more when $|a| < |b|$. Consecutive Fibonacci numbers reach the bound. Each pass does one division, two multiplications and three subtractions, so the time on the word RAM is $\Theta(\log m)$ in the worst case and $\Theta(1)$ in the best case, when $b$ divides $a$ or $b = 0$. The extra space is $\Theta(1)$ words.

**Size of the coefficients.** Let $a, b \ge 1$ and $g = \gcd(a, b)$. The signs of $s_0, s_1, s_2, \ldots$ alternate, and so do those of the $t_i$, and $s_i t_{i+1} - s_{i+1} t_i = \pm 1$. From these two facts follow the exact identities

$$|s_i| \, r_{i+1} + |s_{i+1}| \, r_i = b, \qquad |t_i| \, r_{i+1} + |t_{i+1}| \, r_i = a.$$

Since each non-zero $r_i$ is at least $g$, every coefficient during the run satisfies $|s_i| \le b/g$ and $|t_i| \le a/g$, and so does each product $q s_1$, $q t_1$. If $b \nmid a$, the second-to-last remainder is at least $2g$, which gives $|x| \le b/(2g)$ and $|y| \le a/(2g)$. If $b \mid a$ the result is $(b, 0, 1)$. The coefficients after the last pass are $\pm b/g$ and $\mp a/g$, the step between consecutive solutions.

**No overflow.** By these bounds, every value the loop computes has absolute value at most $\max(|a|, |b|)$. So in a language with fixed-size integers the algorithm does not overflow when the inputs fit, as long as the absolute values of line L1 fit; see the pitfalls.

**Bit operations.** For inputs of $n$ binary digits, the $r$ part costs $O(n^2)$ as for the Euclidean algorithm. The coefficients have at most $n$ digits, so the products $q s_1$ and $q t_1$ cost $O((1 + \lg q) n)$ each with schoolbook multiplication. Since the product of the quotients is at most $\max(|a|, |b|)$, the sum of $\lg q$ over the run is at most $n$, and the total stays $O(n^2)$.

| measure | bound |
|---|---|
| loop passes | as the Euclidean algorithm: $\le 1 + \log_\varphi m$, plus one if $|a| < |b|$ |
| time on the word RAM | worst $\Theta(\log m)$, best $\Theta(1)$ |
| extra space | $\Theta(1)$ words |
| coefficients | $|x| \le |b|/(2g)$, $|y| \le |a|/(2g)$ unless $b \mid a$ |
| bit operations | $O(n^2)$ |

## Properties

- **Minimal coefficients.** If $b \nmid a$, then by the bound $|x| \le |b|/(2g)$ the returned $x$ is the solution of least absolute value, or one of the two least when there is a tie; the same holds for $y$. Every other solution is $(x + kb/g, y - ka/g)$.
- **The convergents of $a/b$.** For $a, b > 0$, the fractions $-t_i / s_i$ for $i \ge 2$ are the convergents of the [continued fraction](/continued-fraction/) of $a/b$, whose partial quotients are the $q_i$. In the example, $240/46 = [5; 4, 1, 1, 2]$, with convergents $5/1$, $21/4$, $26/5$, $47/9$ and $120/23$, the values $-t_i/s_i$ for $i = 2, \ldots, 6$. See [continued fraction convergents](/continued-fraction-convergents/).
- **A matrix product.** Each pass multiplies the coefficient matrix by $\begin{pmatrix} 0 & 1 \\ 1 & -q \end{pmatrix}$, which has determinant $-1$; this is why $s_i t_{i+1} - s_{i+1} t_i = \pm 1$. The [half-GCD](/half-gcd/) and [Lehmer's GCD](/lehmers-gcd/) speed the algorithm up by building these matrix products in bulk.
- **Deterministic and iterative.** No recursion, and six working variables.

## Variants and improvements

- **Recursive form.** $\text{ext}(a, 0) = (a, 1, 0)$, and if $\text{ext}(b, a \bmod b) = (g, x', y')$ then $\text{ext}(a, b) = (g, y', x' - \lfloor a/b \rfloor y')$. It is short, but it uses a stack of depth equal to the number of steps; the loop above needs none.
- **Half extended.** Keep only the $s$ pair and recover $y$ by one division at the end. This saves a third of the work when only a [modular inverse](/modular-inverse/) is needed.
- **Extended [binary GCD](/binary-gcd/).** Keeps coefficients through the shifts and subtractions of Stein's algorithm, with no division. It is common for inverses modulo an odd number in hardware and in cryptographic code.
- **[Lehmer's GCD](/lehmers-gcd/) and the [half-GCD](/half-gcd/).** Compute the same $2 \times 2$ matrices from the leading digits, or by divide and conquer, for $O(M(n) \log n)$ bit operations on large numbers.
- **[Batch modular inverse](/batch-modular-inverse/).** Inverts many numbers modulo the same $m$ with one extended gcd and three multiplications for each number.
- **Polynomials.** The same loop works in each [Euclidean domain](/euclidean-domain/). For polynomials over a field it gives [Padé approximation](/pade-approximation/), the key equation solver of [Reed-Solomon decoding](/reed-solomon-decoding/), and rational reconstruction.

## When to use it

Use it whenever a gcd is needed together with its Bézout coefficients: a [modular inverse](/modular-inverse/) of $a$ modulo $m$ when $\gcd(a, m) = 1$, the solutions of $ax + by = c$ ([linear Diophantine equation](/linear-diophantine-equation/)) and of [linear congruences](/linear-congruence/), and the combination step of the [Chinese remainder theorem](/chinese-remainder-theorem/). When $m$ is prime, the inverse can also be computed as $a^{m-2} \bmod m$ by [modular exponentiation](/modular-exponentiation/), but that takes $\Theta(\log m)$ multiplications modulo $m$, against $\Theta(\log m)$ cheaper steps here, and it does not work for composite $m$. For secret inputs in cryptography, use a constant-time variant.

## Pitfalls

- **The sign of the inverse.** The coefficient $x$ may be negative, as in the RSA example. Reduce it with $x \bmod m$, using a modulus operation that returns a non-negative result; in C, Java and Go, `x % m` is negative for negative $x$, so use `((x % m) + m) % m`.
- **Forgetting to check the gcd.** If $\gcd(a, m) = g > 1$, the algorithm still returns $x$ with $ax \equiv g \pmod m$, which is not an inverse. Check that $g = 1$ before using $x$.
- **Negative inputs with truncating division.** Without line L1, a language whose division rounds toward zero can produce a negative final remainder. Either take absolute values first and fix the signs at line L9, as here, or negate $(r_0, s_0, t_0)$ at the end when $r_0 < 0$.
- **The most negative integer.** $|-2^{63}|$ does not fit in a signed 64-bit word. Inputs must be strictly inside the range, or the algorithm must use wider or unsigned types.
- **Swapping the order of updates.** Each new pair needs the old $s_0$ and $s_1$ together. Writing `s0 = s1; s1 = s0 - q*s1` in two statements uses the new $s_0$; use simultaneous assignment or a temporary variable.

## Implementations

## History

Indian mathematicians solved equations $ax + by = c$ in integers by the *kuttaka* ("pulverizer"), a method built on the chain of divisions of the Euclidean algorithm; it appears in the *Aryabhatiya* of Aryabhata, written in 499, and was refined by Brahmagupta and Bhaskara. In Europe, Claude Gaspard Bachet de Méziriac gave the method in 1624, and Bézout extended the identity to polynomials in 1779. The table form with the $s$ and $t$ columns is the one in Knuth's Algorithm X, and in the procedure EXTENDED-EUCLID of Cormen, Leiserson, Rivest and Stein, which is written recursively there.

## References
