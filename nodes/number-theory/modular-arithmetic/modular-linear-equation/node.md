---
tag: 9A70GQ
kind: problem
slug: modular-linear-equation
name: Modular linear equation
area: number-theory/modular-arithmetic
level: core
summary: Given a, b and n, find all integers x with a x congruent to b modulo n, or decide none exist.
prereqs: [congruence, greatest-common-divisor]
see_also: [linear-congruence, modular-linear-equation-solver, extended-euclidean-algorithm, modular-inverse, linear-diophantine-equation, chinese-remainder-theorem]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 31.4, Solving modular linear equations (the theorems on the number of solutions and the procedure MODULAR-LINEAR-EQUATION-SOLVER)
  - book: isbn:9780849385230
    title: Alfred J. Menezes, Paul C. van Oorschot and Scott A. Vanstone, Handbook of Applied Cryptography, CRC Press, 1997
    locator: Section 2.4.3, Fact 2.119 (ax ≡ b (mod n) has a solution if and only if d divides b, and then exactly d solutions between 0 and n − 1)
  - book: isbn:9780199219865
    title: G. H. Hardy and E. M. Wright, An Introduction to the Theory of Numbers, sixth edition
    locator: Chapter 5, Section 5.4, Linear congruences
---

The modular linear equation problem takes integers $a$, $b$ and $n \ge 1$ and asks for the list of all residues $x \in \{0, 1, \ldots, n - 1\}$ with $ax \equiv b \pmod n$. This is the form in which CLRS (Section 31.4) poses the [linear congruence](/linear-congruence/): with $d = \gcd(a, n)$, the list is empty when $d \nmid b$ and has exactly $d$ entries, spaced $n/d$ apart, when $d \mid b$. The [modular linear equation solver](/modular-linear-equation-solver/) produces it with one call of the [extended Euclidean algorithm](/extended-euclidean-algorithm/) and $d$ additions. Because the list can be as long as $n$, the cost of the problem is measured in the input and the output size together.

## In plain words

You are asked to list, on a clock of a given size, every position that a given multiplier sends to a given target. The answer is either an empty list or a list of evenly spaced positions. How many positions there are is decided by the largest number that divides both the multiplier and the clock size. One run of Euclid's method finds the first position and the spacing, and the rest of the list is filled by repeated addition. When the multiplier shares a big factor with the clock size, the list is long, and writing it down is the main cost.

## Definition

**Input.** Integers $a$ and $b$, and an integer $n \ge 1$.

**Output.** The set $X = \{ x \in \{0, \ldots, n - 1\} : n \mid ax - b \}$, as a list of its elements. An empty list means that the equation has no solution.

**Facts used.** By the theorem on the [linear congruence](/linear-congruence/) page, with $d = \gcd(a, n)$:

- $X \ne \emptyset$ if and only if $d \mid b$;
- if $d \mid b$ and $x_0$ is any solution, then $X = \{ (x_0 \bmod n/d) + i \cdot n/d : 0 \le i < d \}$, so $|X| = d$;
- if $\gcd(a, n) = 1$, then $|X| = 1$, and the solution is $a^{-1} b \bmod n$ with the [modular inverse](/modular-inverse/).

CLRS states these facts as a theorem and its corollaries in Section 31.4.

**Output size.** For $d \mid b$ the output has $d$ entries of up to $\lceil \lg n \rceil$ binary digits each. Since $d$ can be as large as $n$, for example for $a = 0$ and $b = 0$, the output can be exponentially longer than the input, which has $O(\log n + \log |a| + \log |b|)$ digits.

**Cost models.** On the [word RAM](/word-ram/) with $|a|, |b|, n < 2^w$, each arithmetic operation on words, including division with remainder, costs one unit. For arbitrary-precision inputs with $n$ of $k$ binary digits, cost is in bit operations.

## Variants

- **Compact output.** Return $(x_0, n/d)$ with $0 \le x_0 < n/d$, or "none". This describes the same set in $O(\log n)$ digits and removes the output-size issue. It is the form the [linear congruence](/linear-congruence/) page uses.
- **One solution.** Return any element of $X$, or "none". This is the decision problem plus a witness.
- **Smallest solution.** Return $\min X$. With the compact form this is $x_0$ itself.
- **Counting.** Return $|X|$, which is $d$ or $0$; it needs only $\gcd(a, n)$ and one divisibility test.
- **Solutions in a window.** List the integer solutions in an interval $[L, R]$ that may be longer or shorter than $n$; see [linear Diophantine solutions in an interval](/linear-diophantine-solutions-in-interval/).
- **Coprime case.** If $\gcd(a, n) = 1$ is promised, the problem is one multiplication by a [modular inverse](/modular-inverse/).

## Examples

| $a$ | $b$ | $n$ | $d$ | $X$ |
| --- | --- | --- | --- | --- |
| 8 | 12 | 28 | 4 | 5, 12, 19, 26 |
| 8 | 13 | 28 | 4 | empty, since $4 \nmid 13$ |
| 35 | 10 | 50 | 5 | 6, 16, 26, 36, 46 |
| 64 | 0 | 1024 | 64 | $0, 16, 32, \ldots, 1008$ (64 entries) |
| 5 | 3 | 1 | 1 | 0 |
| 0 | 0 | $n$ | $n$ | all of $0, \ldots, n - 1$ |

For $8x \equiv 12 \pmod{28}$: $d = 4$ divides 12. Dividing by $d$ gives $2x \equiv 3 \pmod 7$, and $2^{-1} \equiv 4 \pmod 7$, so $x \equiv 12 \equiv 5 \pmod 7$. The list is $5, 12, 19, 26$, with spacing $n/d = 7$. Check: $8 \cdot 26 = 208 = 7 \cdot 28 + 12$.

## Known algorithms

- [Modular linear equation solver](/modular-linear-equation-solver/): calls EXTENDED-EUCLID$(a, n)$ to get $d$ and $x'$ with $ax' \equiv d \pmod n$, tests $d \mid b$, sets $x_0 = x'(b/d)$ and lists $x_0 + i(n/d)$. $O(\log n + d)$ word operations.
- Cancel $d$ and invert: compute $(a/d)^{-1} \bmod n/d$ with any [modular inverse](/modular-inverse/) method, multiply by $b/d$, then list.
- Brute force: test each $x \in \{0, \ldots, n - 1\}$, for $\Theta(n)$ operations. It is only a reference for testing.

## Bounds

**Upper bound.** On the word RAM, the extended Euclidean algorithm takes $O(\log n)$ time ([Lamé's theorem](/lames-theorem/)), and the list takes $\Theta(d)$ more. So the time is $O(\log n + d)$ in the worst case, where $d = |X|$ when $X \ne \emptyset$. For $k$-digit arbitrary-precision inputs, it is $O(k^2 + dk)$ bit operations with classical arithmetic.

**Lower bound.** Each algorithm must write its output, so $\Omega(d)$ time is needed when the list has $d$ entries. The bound $O(\log n + d)$ is therefore optimal up to the $O(\log n)$ term, and that term matches the number of steps of the best known gcd methods on word-sized inputs. In terms of the input length alone, the worst case is exponential, because of the output size; the compact variant avoids this.

## Reductions

- **To and from the linear congruence.** The two problems have the same solution set and differ only in its representation. Converting the compact form to the list takes $\Theta(d)$ time; the converse takes $O(1)$ time from the first two entries of a list.
- **To a linear Diophantine equation.** $x \in X$ if and only if $ax - ny = b$ for an integer $y$; see [linear Diophantine equation](/linear-diophantine-equation/).
- **From the modular inverse.** $a^{-1} \bmod n$ is the unique entry of $X$ for $b = 1$ when the list is non-empty.

## Applications

- **The Chinese remainder theorem.** Each combination step of the [Chinese remainder theorem](/chinese-remainder-theorem/) for moduli that are not coprime solves a modular linear equation.
- **RSA and other cryptosystems.** Key generation solves $ed \equiv 1 \pmod{\varphi(N)}$, a modular linear equation with $\gcd(e, \varphi(N)) = 1$.
- **Walks on a ring.** A walk that starts at cell 0 of a ring of $n$ cells and moves $s$ cells at each step is at cell $ts \bmod n$ after $t$ steps. The steps $t < n$ at which it is at cell $c$ are the solutions of $st \equiv c \pmod n$. So the walk reaches only the cells that are multiples of $\gcd(s, n)$, and it reaches each of them $\gcd(s, n)$ times in $n$ steps.

## References
