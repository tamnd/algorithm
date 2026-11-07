---
tag: V436BS
kind: algorithm
slug: burnikel-ziegler-division
name: Burnikel-Ziegler division
aliases:
- recursive division
- divide-and-conquer division
- Burnikel-Ziegler recursive division
area: algebra/integer-arithmetic
level: advanced
summary: Recursive division that reduces n-bit division to multiplications, giving subquadratic time.
solves: [integer-division]
model: word-ram
complexity:
  vars: {n: the number of limbs of the divisor, M: the cost of a product of two n-limb numbers (a function of n)}
  time: {worst: O(M(n) log n), average: O(M(n) log n), best: O(M(n) log n)}
  space: {extra: O(n log n)}
properties: {deterministic: true, recursive: true}
history:
  note: Burnikel and Ziegler (1998) gave the recursive 2n-by-n and 3n-by-2n division steps that make long division as fast as Karatsuba multiplication, up to a factor of 2.
prereqs: [long-division, karatsuba-multiplication, integer-division]
see_also: [integer-division, long-division, newton-raphson-division, karatsuba-multiplication, granlund-montgomery-division, master-theorem, toom-cook-multiplication, division-with-remainder]
sources:
  - paper: C. Burnikel and J. Ziegler, Fast recursive division, Research Report MPI-I-98-1-022, Max-Planck-Institut für Informatik, Saarbrücken, 1998
    title: Christoph Burnikel and Joachim Ziegler, Fast recursive division
    locator: Section 2 (Algorithms 1 and 2, the 2n/1n and 3n/2n steps), Lemma 2 (at most two corrections) and Section 3 (the running time 2K(n) + O(n log n))
  - book: isbn:9780521194693
    title: Richard P. Brent and Paul Zimmermann, Modern Computer Arithmetic, Cambridge University Press, 2010
    locator: Section 1.4.3, Divide and conquer division (Algorithm 1.8 RecursiveDivRem and the analysis D(n) = 2D(n/2) + 2M(n/2))
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, third edition
    locator: Section 4.3.1, The classical algorithms (Theorems A and B on the trial quotient, and Algorithm D)
---

Burnikel-Ziegler division divides a $2n$-limb number by an $n$-limb number by recursion, so that most of the work is done by multiplications of half-size numbers. It splits the dividend and the divisor into halves and treats each half of the divisor as one huge "digit": the quotient is computed two half-digits at a time, exactly as in schoolbook [long division](/long-division/), but each trial quotient comes from a recursive division by the top half of the divisor, and the correction for the bottom half costs one multiplication. With [Karatsuba multiplication](/karatsuba-multiplication/), a division costs about twice a multiplication of the same size, against $\Theta(n^2)$ for long division. It is the division used by GMP, Java's `BigInteger` and Python's `int` for medium sizes, below the range where [Newton-Raphson division](/newton-raphson-division/) wins.

## In plain words

Long division by hand guesses one digit of the quotient at a time from the leading digits, multiplies back, and corrects. Burnikel and Ziegler do the same thing with giant digits. Cut the divisor into a top half and a bottom half. To find the top half of the quotient, divide the leading part of the dividend by the top half of the divisor only, which is a smaller division of the same shape and is done the same way, recursively.

That guess is never too small and at most two too large. Multiply it by the bottom half of the divisor, subtract, and fix the guess by adding back the divisor once or twice if the result went negative. Do it again for the bottom half of the quotient. All the expensive work is in half-size products, so fast multiplication makes division fast.

## The problem

Limbs are words of $w$ bits and $\beta = 2^w$. The input is a divisor $B$ of $n$ limbs, *normalized* so that its top limb is at least $\beta/2$, and a dividend $0 \le A < \beta^n B$, which has at most $2n$ limbs. The output is $Q = \lfloor A/B \rfloor$, which is less than $\beta^n$, and $R = A - QB$, with $0 \le R < B$. Any division reduces to this one: shift both numbers to normalize $B$, cut the dividend into blocks of $n$ limbs, and divide one block at a time from the top, carrying the remainder, as the code does.

**Cost model.** The [word RAM](/word-ram/) with $w$-bit words, where an addition or subtraction of $k$-limb numbers costs $\Theta(k)$ and a product of two $k$-limb numbers costs $M(k)$, for a multiplication algorithm with $M(k)/k$ nondecreasing. The recurrence, the bound of two corrections per step, and the bounds $2M(n) + O(n \log n)$ for Karatsuba and $O(M(n) \log n)$ in general are proved; the frequency of corrections and timings are observed.

## The algorithm

```pseudo id=main
DIV2N1N(A, B, n)                          ▷ B normalized, n limbs; 0 ≤ A < β^n B
L1  if n is odd or n ≤ n₀ then return SCHOOLBOOK-DIVREM(A, B)
L2  h ← n/2; write A = [A₁ A₂ A₃ A₄] in blocks of h limbs
L3  (Q₁, R) ← DIV3N2N([A₁ A₂ A₃], B, h)
L4  (Q₂, S) ← DIV3N2N(R · β^h + A₄, B, h)
L5  return (Q₁ β^h + Q₂, S)

DIV3N2N(A, B, h)                          ▷ B = B₁ β^h + B₂ normalized, 0 ≤ A < β^h B, A = [A₁ A₂ A₃]
L6  if A₁ < B₁ then (Q, R₁) ← DIV2N1N([A₁ A₂], B₁, h)       ▷ the trial quotient
L7  else Q ← β^h − 1;  R₁ ← [A₁ A₂] − Q · B₁
L8  R ← R₁ β^h + A₃ − Q · B₂                                  ▷ one h × h product
L9  while R < 0 do Q ← Q − 1;  R ← R + B                     ▷ at most twice
L10 return (Q, R)
```

Here $[A_1 A_2]$ is the number $A_1 \beta^h + A_2$. In DIV3N2N, $A_1 \le B_1$ always, because $A < \beta^h B$; line L7 is the rare case $A_1 = B_1$, where the trial quotient would not fit in $h$ limbs and is capped at $\beta^h - 1$, as in step D3 of Knuth's Algorithm D. The threshold $n_0$ is where schoolbook division becomes faster, in practice a few dozen limbs; the code uses $n_0 \in \{1, 2, 4\}$ so that the recursion is exercised on small numbers.

## Example

Take $\beta = 16$ (hexadecimal limbs), $n = 4$, $h = 2$, $B = \mathtt{C3A5}$ with $B_1 = \mathtt{C3}$ and $B_2 = \mathtt{A5}$, and $A = \mathtt{9F2E71B4}$, so $A_1 = \mathtt{9F}$, $A_2 = \mathtt{2E}$, $A_3 = \mathtt{71}$, $A_4 = \mathtt{B4}$. The top limb $\mathtt{C}$ is at least 8, so $B$ is normalized.

| step | line | computation | result |
|---|---|---|---|
| first DIV3N2N | L6 | $\mathtt{9F} < \mathtt{C3}$, so $\mathtt{9F2E} = \mathtt{D0} \cdot \mathtt{C3} + \mathtt{BE}$ | $Q = \mathtt{D0}$, $R_1 = \mathtt{BE}$ |
| | L8 | $\mathtt{BE71} - \mathtt{D0} \cdot \mathtt{A5} = 48753 - 34320$ | $R = 14433 = \mathtt{3861}$ |
| | L9 | $R \ge 0$ | $Q_1 = \mathtt{D0}$, no correction |
| second DIV3N2N | L4 | dividend $R \beta^2 + A_4$ | $\mathtt{3861B4}$ |
| | L6 | $\mathtt{38} < \mathtt{C3}$, so $\mathtt{3861} = \mathtt{4A} \cdot \mathtt{C3} + \mathtt{03}$ | $Q = \mathtt{4A}$, $R_1 = \mathtt{03}$ |
| | L8 | $\mathtt{03B4} - \mathtt{4A} \cdot \mathtt{A5} = 948 - 12210$ | $R = -11262$ |
| | L9 | one correction: $R + B = -11262 + 50085$ | $Q_2 = \mathtt{49}$, $S = 38823 = \mathtt{97A7}$ |
| result | L5 | $Q_1 \beta^2 + Q_2$ | $Q = \mathtt{D049}$, $R = \mathtt{97A7}$ |

Check: $\mathtt{D049} \cdot \mathtt{C3A5} + \mathtt{97A7} = 53321 \cdot 50085 + 38823 = 2670583093 = \mathtt{9F2E71B4}$. The trial quotient $\mathtt{4A}$ was one too large because it ignored $B_2$; line L9 found that from the sign of $R$.

## Correctness

The precondition $A < \beta^n B$ passes down: $[A_1 A_2 A_3] = \lfloor A/\beta^h \rfloor < \beta^h B$, and since $R < B$, also $R\beta^h + A_4 < \beta^h B$. In DIV3N2N, $A_1 < B_1$ gives $[A_1 A_2] < \beta^h B_1$, the precondition of the recursive call, and $B_1$ is normalized because its top limb is that of $B$. The trial quotient $\hat Q = \min(\lfloor [A_1 A_2]/B_1 \rfloor, \beta^h - 1)$ satisfies $Q^* \le \hat Q \le Q^* + 2$ for the true quotient $Q^*$; this is Knuth's Theorem B on trial quotients, applied in base $\beta^h$, and it needs $B_1 \ge \beta^h/2$, which normalization gives. Line L8 computes $A - \hat Q B$ exactly, which is less than $B$, so at most two additions of $B$ in line L9 bring it into $[0, B)$. The full proof is below.

## Complexity

**Recurrence, proved.** Let $D(n)$ be the cost of DIV2N1N and $D_3(h)$ that of DIV3N2N. Line L6 costs $D(h)$, line L8 one product $M(h)$ and $O(h)$ additions, and line L9 at most two additions, so $D_3(h) = D(h) + M(h) + O(h)$, and

$$D(n) = 2 D(n/2) + 2 M(n/2) + O(n) .$$

For $n = n_0 2^k$, unrolling gives $2^j$ products of size $n/2^j$ at depth $j$, which the test script checks by counting the products: $2$ of size $n/2$, $4$ of size $n/4$, and so on.

**Solutions, proved.** If $M(n) = c n^\alpha$ with $\alpha > 1$, then $D(n) = \frac{c}{2^{\alpha - 1} - 1} n^\alpha + O(n \log n)$. For [Karatsuba](/karatsuba-multiplication/), $\alpha = \log_2 3$ and $2^{\alpha - 1} = 3/2$, so $D(n) \approx 2M(n)$; this is Burnikel and Ziegler's $2K(n) + O(n \log n)$. For schoolbook products, $\alpha = 2$ gives $D(n) \approx M(n) \approx n^2$, no better than long division. For [Toom-3](/toom-cook-multiplication/), $\alpha = \log_3 5$ gives a constant of about $2.6$, since the saving of a faster product is spread over fewer levels. In general, with $M(n)/n$ nondecreasing, each of the $\log_2 n$ levels costs at most $M(n) + O(n)$, so $D(n) = O(M(n) \log n)$, which the [master theorem](/master-theorem/) also gives. A division of a $(k+1)n$-limb number by $n$ limbs costs $k$ calls of DIV2N1N.

**Space.** The recursion has depth $O(\log n)$ and each level keeps $O(n)$ limbs of temporaries, $O(n \log n)$ in this simple form; implementations reuse buffers to get $O(n)$.

**Corrections, observed.** In base 16, on 3000 random divisions of 32 by 16 limbs, line L9 ran 0.32 times per DIV3N2N on average; the frequency falls as the base grows, since the trial quotient is off only when the ignored low half matters.

## Properties

- **Exact.** All arithmetic is on integers; there is no rounding to analyse, unlike Newton's method.
- **Uses the multiplication as a black box.** Any product algorithm can be plugged into line L8, and the division inherits its speed up to a constant factor.
- **Quotient and remainder together.** The remainder comes out for free, which Newton-based division needs an extra product for.
- **Recursive halving needs even sizes.** The divisor is padded so that $n = n_0 2^k$ with $n_0$ at most the threshold, by shifting both operands left by the same amount.

## Variants and improvements

- **Brent and Zimmermann's form.** Algorithm 1.8 of *Modern Computer Arithmetic* divides $n + m$ limbs by $n$ with a quotient of $m$ limbs, splitting at $k = \lfloor m/2 \rfloor$ and allowing unbalanced sizes, with the same recurrence.
- **Unbalanced division.** For a dividend much longer than the divisor, divide in blocks of $n$ limbs from the top; each block costs one DIV2N1N.
- **Short products.** The product $Q B_2$ in line L8 is only needed in full because $R$ must be exact; Mulders's short products and the middle product reduce the constant in related algorithms.
- **Newton-Raphson division.** For very large $n$, computing a reciprocal by Newton's method and multiplying costs about $1.5$ to $2$ products with FFT multiplication, and wins over recursion, whose $\log n$ factor appears once $M(n)$ is quasi-linear.
- **Divide and conquer for polynomials.** The same recursion divides polynomials, where there are no carries and no corrections are needed; it goes back to Moenck and Borodin.

## When to use it

Use recursive division for operands from a few dozen limbs, where Karatsuba multiplication starts to beat schoolbook, up to the size where FFT multiplication takes over and Newton-Raphson division becomes faster, typically several thousand limbs. It is also the method of choice when both the quotient and the remainder are needed. For one-limb divisors, use a precomputed reciprocal as in [Granlund-Montgomery division](/granlund-montgomery-division/), and for small sizes plain long division.

## Pitfalls

- **Skipping normalization.** Without $B_1 \ge \beta^h/2$, the trial quotient of line L6 can be too large by much more than 2, and the loop of line L9 runs many times. Shift $A$ and $B$ left until the top bit of $B$ is set, and shift the remainder back at the end.
- **Calling the recursion when $A_1 = B_1$.** Line L6 with $A_1 \ge B_1$ violates the precondition $[A_1 A_2] < \beta^h B_1$, and the recursive quotient would need $h + 1$ limbs. The right action is line L7, which caps the trial quotient at $\beta^h - 1$.
- **Unsigned temporaries in line L8.** $R$ can be negative, down to about $-2B$. Writing line L8 with unsigned limb arithmetic and no borrow handling turns a negative $R$ into a huge positive one, and line L9 never runs; keep a sign or a borrow word.
- **Odd sizes.** Line L2 needs $n$ even; dividing an odd $n$ in two unequal halves breaks the block structure of line L4. Pad the divisor to $n_0 2^k$ limbs, or fall back to the base case as line L1 does.

## Implementations

## History

Divide-and-conquer division of polynomials goes back to Moenck and Borodin (1972), and the idea of using fast multiplication for long division of integers was folklore. Jebelean (1997) described a practical integer version with Karatsuba complexity, and Burnikel and Ziegler (1998) gave the clean 2n-by-n and 3n-by-2n formulation, with the bound of two corrections and the cost $2K(n) + O(n \log n)$, and implemented it in the LEDA library. It has since been adopted by GMP, by Java's `BigInteger` (Java 8, 2014) and by other big-number libraries.

## References
