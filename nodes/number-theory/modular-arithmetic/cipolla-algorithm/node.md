---
tag: W39G65
kind: algorithm
slug: cipolla-algorithm
name: Cipolla's algorithm
aliases:
- Cipolla-Lehmer algorithm
area: number-theory/modular-arithmetic
level: advanced
summary: Computes a square root modulo an odd prime by working in a quadratic extension field.
solves: [modular-square-root]
model: word-ram
complexity:
  vars: {p: the odd prime modulus, k: the number of binary digits of p}
  time: {expected: Θ(log p), best: Θ(log p)}
  space: {extra: Θ(1)}
  bit_operations: {expected: O(k^3)}
properties: {deterministic: false, recursive: false}
history:
  year: 1907
  people: [Michele Cipolla]
  note: Cipolla found the method at the start of the twentieth century; the alias Cipolla-Lehmer algorithm also credits D. H. Lehmer.
prereqs: [modular-square-root, euler-criterion, binary-exponentiation]
see_also: [tonelli-shanks, quadratic-residue, legendre-symbol, jacobi-symbol, hensel-lifting, rabin-cryptosystem, las-vegas-algorithm, fermat-little-theorem]
sources:
  - book: isbn:9780521516440
    title: Victor Shoup, A Computational Introduction to Number Theory and Algebra, second edition
    locator: Section 12.5, Computing modular square roots, and Exercise 12.9 (a probabilistic square root algorithm with arithmetic modulo X^2 - α, expected time O(len(p)^3), faster than Section 12.5.1 when p - 1 is divisible by a large power of 2)
  - book: isbn:9780387947778
    title: Richard Crandall and Carl Pomerance, Prime Numbers, A Computational Perspective, Springer, 2001
    locator: page 157 (Cipolla's method for square roots modulo a prime)
  - url: https://en.wikipedia.org/wiki/Cipolla%27s_algorithm
    title: Cipolla's algorithm, Wikipedia
    locator: lead (Michele Cipolla, 1907), sections Algorithm, Example (p = 13, n = 10, a = 2, root 6), Proof, Speed (4m + 2k - 4 multiplications, about 2 trials, comparison with Tonelli-Shanks) and Prime power moduli
---

**Cipolla's algorithm** finds a [square root modulo an odd prime](/modular-square-root/) $p$: given a [quadratic residue](/quadratic-residue/) $n$, it returns $x$ with $x^2 \equiv n \pmod p$. It picks a random $a$ until $a^2 - n$ is a nonresidue, which happens about every second try, and then computes one power, $(a + \omega)^{(p+1)/2}$, in the field $\mathbb{F}_p(\omega)$ with $\omega^2 = a^2 - n$. The result lies in $\mathbb{F}_p$ and squares to $n$. The cost is an expected $O(\log p)$ multiplications modulo $p$, whatever the shape of $p - 1$. This is its advantage over [Tonelli-Shanks](/tonelli-shanks/), which can need $\Theta(\log^2 p)$ multiplications when $p - 1$ is divisible by a large power of $2$. Square roots modulo primes are needed in the [Rabin cryptosystem](/rabin-cryptosystem/), for points on elliptic curves, and in factoring algorithms; the method is a standard example of computation in a finite field extension.

## In plain words

Some numbers have no square root on the clock of a prime $p$. Cipolla's trick is to add one: invent a new symbol whose square is such a number, as the complex numbers add a symbol whose square is minus one. Numbers now have two parts, an ordinary part and a part with the new symbol.

To build it, try random values of $a$ until $a^2 - n$ has no square root on the clock. Call the new symbol's square exactly this value. Then raise "$a$ plus the new symbol" to the power "half of $p$ plus one", by repeated squaring.

A short argument shows that the symbol part of the result is zero, and that the ordinary part, squared, gives $n$. So the detour through the bigger number system comes back with an ordinary answer.

## The problem

**Input.** An odd prime $p$ and an integer $n$.

**Output.** An $x$ with $0 \le x < p$ and $x^2 \equiv n \pmod p$, or NONE if $n$ is not a square modulo $p$. The other root is $p - x$.

**Representation and range.** Residues modulo $p$ are the integers $0, \ldots, p - 1$, and the input $n$ is reduced first, so $n = 0$ and multiples of $p$ give the root $0$. An element $x + y\omega$ of the extension field is stored as the pair $(x, y)$ of residues, and $\omega$ itself is never stored; only $d = \omega^2 = a^2 - n$ is. The modulus must be prime. The algorithm is defined for odd $p$; for $p = 2$, every residue is its own square root. The implementation does not test primality, but it never returns a wrong root: for a composite modulus it either returns NONE, raises an error when a check fails, or returns a value whose square is $n$.

**Cost model.** For a single-word prime on the [word RAM](/word-ram/), each multiplication modulo $p$ takes $O(1)$ word operations with a double-width product. For a prime of $k$ binary digits in arbitrary precision, the cost is counted in bit operations, $O(k^2)$ per multiplication with schoolbook arithmetic. The random choices are uniform residues, and the bounds are expected values over them.

## The algorithm

Lines L3 and L4 test each candidate with [Euler's criterion](/euler-criterion/). Lines L5 to L10 are [binary exponentiation](/binary-exponentiation/) in $\mathbb{F}_p(\omega)$, with the product $(x + y\omega)(b + c\omega) = (xb + ycd) + (xc + yb)\omega$.

```pseudo id=main
CIPOLLA(n, p)                                   ▷ p an odd prime
L1  n ← n mod p; if n = 0: return 0
L2  if n^((p−1)/2) mod p ≠ 1: return NONE           ▷ Euler's criterion: n is not a square
L3  repeat: choose a uniformly in {0, ..., p − 1}; d ← (a² − n) mod p
L4  until d^((p−1)/2) mod p = p − 1                ▷ d is a nonresidue; ω² = d
L5  (x, y) ← (1, 0); (b, c) ← (a, 1)               ▷ x + yω = 1, b + cω = a + ω
L6  e ← (p + 1)/2
L7  while e > 0:
L8      if e is odd: (x, y) ← (xb + ycd, xc + yb) mod p
L9      (b, c) ← (b² + c²d, 2bc) mod p              ▷ square the base
L10     e ← ⌊e/2⌋
L11 return x                                     ▷ here y = 0 and x² ≡ n
```

## Example

Take $p = 13$ and $n = 10$, as in the Wikipedia article. Euler's criterion gives $10^6 \equiv 1 \pmod{13}$, so $10$ is a square. The values $a$ with $a^2 - 10$ a nonresidue are $2, 4, 5, 8, 9, 11$, six of the thirteen. With $a = 2$, $d = 4 - 10 \equiv 7$, and $7^6 \equiv 12 \equiv -1$, so $7$ is a nonresidue. The exponent is $e = (13 + 1)/2 = 7$, binary $111$.

| $e$ | odd | $(x, y)$ after L8 | $(b, c)$ before L9 | $(b, c)$ after L9 |
|---|---|---|---|---|
| $7$ | yes | $(1, 0)(2, 1) = (2, 1)$ | $(2, 1)$ | $(4 + 7, 4) = (11, 4)$ |
| $3$ | yes | $(2 \cdot 11 + 1 \cdot 4 \cdot 7, 2 \cdot 4 + 1 \cdot 11) \equiv (11, 6)$ | $(11, 4)$ | $(121 + 112, 88) \equiv (12, 10)$ |
| $1$ | yes | $(11 \cdot 12 + 6 \cdot 10 \cdot 7, 11 \cdot 10 + 6 \cdot 12) = (552, 182) \equiv (6, 0)$ | $(12, 10)$ | $(12, 6)$, not used |

The result is $x = 6$, with $y = 0$ as promised: $6^2 = 36 = 2 \cdot 13 + 10$. The other root is $13 - 6 = 7$.

## Correctness

Lines L1 and L2 are correct by Euler's criterion. If $n \not\equiv 0$ is a residue, exactly $(p - 1)/2$ of the $p$ values $a$ give a nonresidue $d = a^2 - n$, so each trial succeeds with probability $(p - 1)/(2p)$. For such $d$, $X^2 - d$ is irreducible, and $F = \mathbb{F}_p[X]/(X^2 - d)$ is a field with $\omega^2 = d$. In characteristic $p$, $(u + v)^p = u^p + v^p$; with [Fermat's little theorem](/fermat-little-theorem/) and $\omega^p = \omega d^{(p-1)/2} = -\omega$, this gives $(a + \omega)^p = a - \omega$. So
$$z = (a + \omega)^{(p+1)/2}, \qquad z^2 = (a + \omega)^p (a + \omega) = (a - \omega)(a + \omega) = a^2 - d = n.$$
The equation $T^2 = n$ has at most two roots in the field $F$, and $\pm r \in \mathbb{F}_p$ are two of them, so $z \in \mathbb{F}_p$. The full proof, with the count of good values $a$, is in `proofs/correctness.md`.

## Complexity

Each trial costs one exponentiation modulo $p$, and the expected number of trials is $2p/(p - 1)$, which is at most $3$ and tends to $2$. The main power has an exponent of about $k$ binary digits. A squaring in $F$ takes $4$ multiplications modulo $p$ ($b^2$, $c^2$, $c^2 d$, $bc$), and a general product takes $5$.

| measure | bound |
|---|---|
| expected trials of L3 and L4 | $2p/(p - 1) \le 3$ |
| multiplications modulo $p$, main power | at most $9k$; Wikipedia counts $4m + 2h - 4$ with a tuned product, for $m$ binary digits of which $h$ are ones |
| multiplications modulo $p$, all | expected $O(\log p)$, with the Euler tests |
| word operations, single-word $p$ | expected $\Theta(\log p)$ |
| bit operations, $k$-digit $p$ | expected $O(k^3)$ with schoolbook arithmetic |
| extra space | $O(1)$ residues |

The cost does not depend on the power of $2$ in $p - 1$. Tonelli-Shanks needs $O(\log p + s^2)$ multiplications, where $2^s$ is the largest power of $2$ dividing $p - 1$, so Cipolla's algorithm is faster when $s$ is large, and Tonelli-Shanks is faster when $s$ is small (Shoup, Exercise 12.9). The Wikipedia article puts the crossover at $s(s - 1) > 8m + 20$ for $p$ of $m$ binary digits.

## Properties

- **Las Vegas.** The search for $a$ is random, but the answer is always correct; only the running time varies. It is a [Las Vegas algorithm](/las-vegas-algorithm/).
- **Iterative.** One loop of trials and one binary exponentiation; no recursion.
- **Independent of $p - 1$.** The number of operations depends only on the length of $p$.
- **Constant space.** Four residues for the power, plus $a$, $d$ and $n$.
- **Two roots.** The algorithm returns one root, $x$ or $p - x$, depending on the random $a$.
- **No deterministic version is known** without unproved hypotheses: finding a nonresidue deterministically is the open part, as for Tonelli-Shanks.

## Variants and improvements

- **Polynomial form (Shoup, Exercise 12.9).** With a random $\gamma$, compute $\mu + \nu X \equiv (\gamma - X)^{(p-1)/2} \pmod{X^2 - n}$. If $\gamma^2 - n$ is a nonresidue, then $\mu = 0$ and $\nu^{-2} = n$, so $\nu^{-1}$ is a root. This works modulo $X^2 - n$ instead of $X^2 - d$, with the exponent $(p - 1)/2$.
- **Faster nonresidue tests.** Test $a^2 - n$ with the [Jacobi symbol](/jacobi-symbol/) in $O(k^2)$ bit operations instead of Euler's power in $O(k^3)$.
- **Deterministic choices.** Trying $a = 0, 1, 2, \ldots$ in order works in practice and is easy to reproduce, but no good bound on the number of trials is proved without the generalized Riemann hypothesis.
- **Prime powers.** A root modulo $p$ lifts to roots modulo $p^e$ by [Hensel lifting](/hensel-lifting/), when $p \nmid n$. The Wikipedia article also gives Cipolla's direct formula for prime powers.
- **Composite moduli.** With the factorization of $m$, take roots modulo each prime power and combine them with the [Chinese remainder theorem](/chinese-remainder-theorem/). Without the factorization, the problem is as hard as factoring.
- **Fixed-shape primes.** For $p \equiv 3 \pmod 4$, $n^{(p+1)/4}$ is a root, with no random choice; Cipolla's algorithm is for the general case.

## When to use it

Use Cipolla's algorithm for square roots modulo a prime $p$ for which $p - 1$ has a large power of $2$, such as the primes $c \cdot 2^s + 1$ used by the number theoretic transform, or when a simple method with a fixed operation count is wanted. For $p \equiv 3 \pmod 4$, use the single power $n^{(p+1)/4}$. For primes with a small power of $2$ in $p - 1$, Tonelli-Shanks is usually a little faster. If the modulus may not be prime, test it first or factor it.

## Pitfalls

- **Skipping Euler's criterion for $n$.** If $n$ is a nonresidue, $(a + \omega)^{(p+1)/2}$ still exists but is not in $\mathbb{F}_p$, and returning its first part gives a wrong root. Check $n$ first, or check $y = 0$ and $x^2 \equiv n$ at the end.
- **The case $n \equiv 0$.** Then $a^2 - n$ is a square for every $a$ (zero for $a = 0$), and the search for a nonresidue never ends. Return $0$ before the loop.
- **A residue $d$.** If $d$ is a square, $X^2 - d$ factors, the ring is not a field, and the result is wrong. Accept $a$ only when $d^{(p-1)/2} \equiv -1$.
- **Composite moduli.** Neither the search nor the final power is meaningful for composite $m$, and the search can run forever: modulo $9$, no $d$ satisfies $d^4 \equiv -1$. Bound the number of trials, or test primality first.
- **Overflow.** The term $y c d$ multiplies three residues. Reduce after each product in fixed-width code.

## Implementations

The Python version follows the main block line by line. It uses its own binary exponentiation for the Euler tests, takes an optional random generator for reproducible tests, handles $p = 2$ directly, and checks $y = 0$ and $x^2 \equiv n$ before it returns, so a composite modulus cannot produce a wrong root. The tests compare it with Python's `pow` and with the set of squares: every residue for every prime below $400$, random squares and random values for primes of $30$ to $1000$ binary digits, including primes $p$ with $2^{900} \mid p - 1$, the values $0$, $1$ and $p - 1$, multiples of $p$, and composite moduli such as powers of two and Carmichael numbers.

## History

Michele Cipolla published the method at the start of the twentieth century; the Wikipedia article dates it to 1907. Its name with D. H. Lehmer, the Cipolla-Lehmer algorithm, also appears in the literature. Modern textbooks, such as Crandall and Pomerance and Shoup, present it next to the algorithm of Tonelli and Shanks, as the method whose cost does not depend on the power of $2$ in $p - 1$.

## References
