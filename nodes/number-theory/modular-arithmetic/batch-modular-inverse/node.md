---
tag: ZYDK39
kind: algorithm
slug: batch-modular-inverse
name: Batch modular inverse
aliases:
- Montgomery's trick for inverses
- simultaneous inversion
area: number-theory/modular-arithmetic
level: advanced
summary: Inverts n residues with one modular inversion and 3(n-1) multiplications.
solves: [modular-inverse]
model: word-ram
complexity:
  vars: {k: the number of residues, m: the modulus, n: the number of binary digits of m, M: the cost of multiplying two n-digit integers}
  time: {worst: Θ(k + log m), best: Θ(k)}
  space: {extra: Θ(k)}
  multiplications: {worst: Θ(k)}
  bit_operations: {worst: O(k M(n) + n^2)}
properties: {deterministic: true, recursive: false}
history:
  year: 1987
  people: [Peter L. Montgomery]
  note: Introduced by Montgomery in his paper on speeding up the Pollard and elliptic curve factoring methods, where many inversions modulo the same number occur together.
prereqs: [modular-inverse, modular-multiplication, extended-euclidean-algorithm]
see_also: [prefix-sums, elliptic-curve-factorization, elliptic-curve-cryptography, pollard-p-minus-1, binomial-coefficient, factorial-modulo-prime, montgomery-multiplication, parallel-prefix]
sources:
  - book: isbn:9780521194693
    title: Richard P. Brent and Paul Zimmermann, Modern Computer Arithmetic, Cambridge University Press, 2010
    locator: Section 2.5.1, Several inversions at once (Algorithm 2.11 MultipleInversion, Theorem 2.7, the count of 3(k - 1) multiplications, Figure 2.1 with the recursive variant, and the dual case of one number and several moduli); Section 2.9, Notes and references (attribution to Montgomery)
  - paper: doi:10.1090/S0025-5718-1987-0866113-7
    title: Peter L. Montgomery, Speeding the Pollard and elliptic curve methods of factorization, Mathematics of Computation 48 (177), 1987
    locator: pages 243 to 264 (the replacement of several inversions modulo N by one inversion and extra multiplications)
  - url: https://cp-algorithms.com/algebra/module-inverse.html
    title: Modular Multiplicative Inverse, cp-algorithms
    locator: sections Finding the modular inverse for array of numbers modulo m, and Finding the modular inverse for prime moduli using Euclidean Division (all inverses of 1 to m - 1 in linear time)
---

A **batch modular inverse** computes the [inverses](/modular-inverse/) of $k$ residues $x_1, \ldots, x_k$ modulo the same $m$ with one inversion and $3(k - 1)$ [modular multiplications](/modular-multiplication/), instead of $k$ inversions. It multiplies the residues together, keeps the [prefix products](/prefix-sums/), inverts the full product once with the [extended Euclidean algorithm](/extended-euclidean-algorithm/), and then peels the factors off one at a time. An inversion costs as much as many multiplications, so the trick saves most of the work whenever $k$ is large. Peter Montgomery introduced it in 1987 for the [elliptic curve factoring method](/elliptic-curve-factorization/); it is now standard in [elliptic curve cryptography](/elliptic-curve-cryptography/), in the tables of inverse factorials for [binomial coefficients](/binomial-coefficient/), and anywhere many fractions share one modulus. If one residue is not invertible, the method finds a factor of $m$ instead.

## In plain words

Inverting a number modulo $m$ is slow, much slower than multiplying two numbers. Suppose you must invert many numbers modulo the same $m$.

First multiply them all together, step by step, and write down every partial product on the way. Then invert only the final product. This one inverse is "one over all the numbers".

Now walk back. Multiply the inverse by the partial product just before the last number: everything cancels except one over the last number. Then multiply the inverse by the last number itself, which gives "one over all numbers except the last". Repeat this until you reach the first number.

You pay for one slow inversion and three multiplications for each extra number.

## The problem

**Input.** A modulus $m \ge 1$ and residues $x_1, \ldots, x_k$ modulo $m$, with $k \ge 0$.

**Output.** The residues $y_1, \ldots, y_k$ with $x_i y_i \equiv 1 \pmod m$ for each $i$, if every $x_i$ is a unit modulo $m$. Otherwise, a divisor $g > 1$ of $m$ that shows that some $x_i$ shares a factor with $m$.

**Representation and range.** Residues are the integers $0, \ldots, m - 1$; inputs outside this range are reduced first. Any modulus $m \ge 1$ is allowed, prime or composite, even or odd. For $m = 1$, every residue is $0$, and $0$ is its own inverse, since $0 \cdot 0 \equiv 1 \pmod 1$. The outputs are residues in $\{0, \ldots, m - 1\}$, in the order of the inputs.

**Cost model.** For a single-word modulus on the [word RAM](/word-ram/), each multiplication with reduction costs $O(1)$ word operations with a double-width product, and the extended Euclidean algorithm takes $O(\log m)$ steps. For a modulus of $n$ binary digits in arbitrary precision, the cost is counted in bit operations: a modular multiplication costs $O(M(n))$, where $M(n)$ is the cost of an $n$-digit multiplication, and one inversion costs $O(n^2)$ with the schoolbook extended Euclidean algorithm, or $O(M(n) \log n)$ with a fast gcd.

## The algorithm

The forward pass stores $z_i = x_1 x_2 \cdots x_i \bmod m$. One inversion gives $q = z_k^{-1}$. In the backward pass, $q$ always holds $z_i^{-1}$, so $q \cdot z_{i-1} = x_i^{-1}$, and $q \cdot x_i = z_{i-1}^{-1}$ moves to the next index.

```pseudo id=main
BATCH-INVERSE(x_1, ..., x_k, m)
L1  if k = 0: return the empty list
L2  z_1 ← x_1
L3  for i ← 2 to k:
L4      z_i ← z_(i−1) · x_i mod m                 ▷ z_i = x_1 ⋯ x_i
L5  (g, q) ← extended Euclid on (z_k, m)            ▷ g = gcd(z_k, m), q·z_k ≡ g
L6  if g ≠ 1: fail with g                          ▷ some x_i is not a unit; g divides m
L7  for i ← k downto 2:                            ▷ invariant: q = z_i^(−1)
L8      y_i ← q · z_(i−1) mod m                    ▷ = x_i^(−1)
L9      q ← q · x_i mod m                          ▷ = z_(i−1)^(−1)
L10 y_1 ← q
L11 return y_1, ..., y_k
```

Line L8 reads $z_{i-1}$ before any write to that position, so the outputs $y_i$ may overwrite the array of prefix products from the top down, as in the Python version.

## Example

Take $m = 101$ and $x = (3, 7, 10, 25)$. The forward pass gives the prefix products $z = (3, 21, 8, 99)$. Since $99 \equiv -2$ and $-2 \cdot 50 = -100 \equiv 1$, line L5 gives $q = 50$.

| step | $i$ | $q$ before | line L8: $y_i = q \cdot z_{i-1}$ | line L9: $q \cdot x_i$ |
|---|---|---|---|---|
| backward | $4$ | $50 = z_4^{-1}$ | $50 \cdot 8 = 400 \equiv 97$ | $50 \cdot 25 = 1250 \equiv 38 = z_3^{-1}$ |
| backward | $3$ | $38$ | $38 \cdot 21 = 798 \equiv 91$ | $38 \cdot 10 = 380 \equiv 77 = z_2^{-1}$ |
| backward | $2$ | $77$ | $77 \cdot 3 = 231 \equiv 29$ | $77 \cdot 7 = 539 \equiv 34 = z_1^{-1}$ |
| line L10 | $1$ | $34$ | $y_1 = 34$ | |

So the inverses are $(34, 29, 91, 97)$. Check: $3 \cdot 34 = 102$, $7 \cdot 29 = 203$, $10 \cdot 91 = 910$ and $25 \cdot 97 = 2425$ are all $\equiv 1 \pmod{101}$. The computation used $3$ multiplications forward, $6$ backward and one inversion.

**A failure that factors.** For $m = 15$ and $x = (2, 7, 6)$, the product is $84 \equiv 9$, and $\gcd(9, 15) = 3$. Line L6 fails with $g = 3$, a factor of $15$, because $6$ is not a unit.

## Correctness

The forward pass keeps $z_i \equiv x_1 \cdots x_i$. The product $z_k$ is a unit if and only if every $x_i$ is a unit: a product of units is a unit, and if $z_k w \equiv 1$, then $x_i$ times $w$ times the other factors is $1$. So line L6 fails exactly when some $x_i$ is not invertible, and then $g = \gcd(z_k, m)$ is a divisor of $m$ greater than $1$. Otherwise, the backward loop keeps the invariant $q \equiv z_i^{-1}$ at the start of the iteration for $i$. Then line L8 gives $q z_{i-1} \equiv z_{i-1}/z_i = x_i^{-1}$, and line L9 gives $q x_i \equiv z_{i-1}^{-1}$, which restores the invariant for $i - 1$. At the end $q \equiv z_1^{-1} = x_1^{-1}$. The full proof is in `proofs/correctness.md`.

## Complexity

The forward pass makes $k - 1$ multiplications and the backward pass $2(k - 1)$, so the total is $3(k - 1)$ modular multiplications and one inversion, for $k \ge 1$.

| measure | bound |
|---|---|
| modular multiplications | exactly $3(k - 1)$ |
| inversions | exactly $1$ (one extended Euclidean algorithm) |
| word operations, single-word $m$ | $\Theta(k + \log m)$ in the worst case, $\Theta(k)$ when the gcd ends quickly |
| bit operations, $n$-digit $m$ | $3(k - 1)$ products of cost $O(M(n))$ each, plus $O(n^2)$ for the inversion; $O(k n^2)$ with schoolbook arithmetic |
| extra space | $k$ residues for the prefix products, reused for the output |

Compared with $k$ separate inversions, the method wins when an inversion costs more than three multiplications, which is the usual case (Brent and Zimmermann, Section 2.5.1). For $n$-digit moduli with schoolbook arithmetic, $k$ separate extended Euclidean runs also cost $O(k n^2)$, but with a much larger constant; with fast multiplication, an inversion costs $\Theta(M(n) \log n)$, so the saving grows by a factor of order $\log n$.

## Properties

- **Deterministic and iterative.** Two loops and one gcd, with no random choices.
- **Exact count.** The number of multiplications depends only on $k$, not on the values.
- **All or nothing.** One non-invertible residue makes the whole product non-invertible, so the basic method returns no inverse at all.
- **A factor for free.** On failure, $g = \gcd(z_k, m)$ divides $m$. When $m$ is composite with unknown factors, this $g$ is often a proper factor. This is the event that the elliptic curve factoring method waits for.
- **Order-preserving.** The output order matches the input order; the factors may be multiplied in any order, since the ring is commutative.
- **Any modulus.** Nothing needs $m$ to be prime or odd, unlike an inversion by [Fermat's little theorem](/fermat-little-theorem/).

## Variants and improvements

- **Tree form (Brent and Zimmermann, Figure 2.1).** Multiply the residues in pairs up a binary tree, invert the root, and go down the tree, multiplying each inverse by the product stored in the sibling node. It uses the same number of multiplications and runs in $O(\log k)$ parallel steps, like a [parallel prefix](/parallel-prefix/) computation.
- **Skipping zeros.** When some inputs may be $0$ but $m$ is prime, replace each zero by $1$ in the product and output $0$ or an error for it. For a composite $m$ with non-invertible inputs that are not zero, the residues have to be split after the failure, for example by recursing on the two halves of the list.
- **One number, several moduli.** The dual problem, $x^{-1} \bmod N_1, \ldots, x^{-1} \bmod N_k$, can be solved by inverting modulo the product $N_1 \cdots N_k$ and reducing down a product tree. Here the numbers grow up the tree, so it pays off less often (Brent and Zimmermann, Section 2.5.1).
- **Inverse factorials.** For a prime $p$ and the factorials $1!, 2!, \ldots, N!$ modulo $p$, invert only $N!$, and get the other inverse factorials by $(i - 1)!^{-1} = i \cdot (i!)^{-1}$. Then $i^{-1} = (i - 1)! \cdot (i!)^{-1}$. This is the same trick on the list $1, 2, \ldots, N$, and it gives the table for [binomial coefficients](/binomial-coefficient/) modulo $p$.
- **All inverses modulo a prime.** For the list $1, \ldots, p - 1$, the recurrence $i^{-1} \equiv -\lfloor p/i \rfloor \cdot (p \bmod i)^{-1} \pmod p$ needs no inversion at all and one multiplication per entry (cp-algorithms).
- **Projective points.** In elliptic curve code, a batch of points in projective coordinates $(X : Y : Z)$ is converted to affine coordinates with one inversion for all the $Z$ values. In the same way, the elliptic curve factoring method can run many curves in affine coordinates at once, with one inversion per step for all of them.

## When to use it

Use a batch inverse when many inversions modulo the same $m$ are known at the same time: converting many elliptic curve points to affine form, running many curves of a factoring method together, building a table of inverse factorials, or dividing many values by different denominators. For a single inversion, or when each inverse is needed before the next input is known, invert directly. If the residues may be non-invertible and each answer matters, plan how to split the batch after a failure.

## Pitfalls

- **One bad residue.** A single $0$, or a single residue that shares a factor with $m$, makes the whole batch fail. Filter zeros first, or use the splitting variant.
- **Overwriting the prefix array too early.** Line L8 needs $z_{i-1}$. Writing $y_i$ into position $i - 1$, or running the backward loop upward, destroys values that are still needed.
- **Index off by one.** The backward loop stops at $i = 2$, and $y_1$ is the final $q$. Running the loop down to $i = 1$ reads a $z_0$ that does not exist.
- **Memory.** The forward pass stores $k$ residues. For very large batches of large residues, process the batch in blocks, each with its own inversion.
- **Timing.** The extended Euclidean algorithm takes data-dependent time. In cryptographic code, invert the product in [constant time](/constant-time/), for example by Fermat's little theorem for a prime modulus.

## Implementations

The Python version follows the main block line by line. It reduces the inputs modulo $m$, inverts the product with an iterative extended Euclidean algorithm, and raises an error that carries $g = \gcd(z_k, m)$ when some residue is not invertible. The output overwrites the list of prefix products. The tests compare it with Python's `pow(x, -1, m)` on the worked examples, on all units for every $m < 200$, and on random lists for moduli $1$, $2$, powers of two, primes, composites and numbers of several hundred digits, with $1$ and $m - 1$ in the lists; they also check that non-invertible inputs give the divisor $\gcd(z_k, m)$ of $m$.

## History

Peter Montgomery described the trick in 1987, in his paper on speeding up the Pollard and elliptic curve methods of factoring, where many inversions modulo the same number occur together. Brent and Zimmermann give it as Algorithm MultipleInversion, also known as batch inversion, and attribute it to Montgomery. It is often called Montgomery's trick, and it is unrelated to [Montgomery multiplication](/montgomery-multiplication/) apart from its author.

## References
