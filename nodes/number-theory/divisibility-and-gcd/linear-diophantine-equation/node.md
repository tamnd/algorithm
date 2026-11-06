---
tag: F4X9CJ
kind: problem
slug: linear-diophantine-equation
name: Linear Diophantine equation
area: number-theory/divisibility-and-gcd
level: core
summary: Find integer pairs x and y satisfying a x plus b y equals c for given integers a, b and c.
prereqs: [greatest-common-divisor, bezouts-identity, extended-euclidean-algorithm]
see_also: [linear-diophantine-solution, linear-diophantine-solutions-in-interval, linear-congruence, chinese-remainder-theorem, gcd-of-array, hermite-normal-form, smith-normal-form, water-jug-problem]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 31.2, Greatest common divisor (EXTENDED-EUCLID), and Section 31.4, Solving modular linear equations (MODULAR-LINEAR-EQUATION-SOLVER)
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, third edition
    locator: Section 4.5.2, The Greatest Common Divisor (Algorithm X, the extended Euclidean algorithm, and its use to solve linear equations in integers)
  - url: "https://cp-algorithms.com/algebra/linear-diophantine-equation.html"
    locator: sections Finding a solution, Getting all solutions, Finding the number of solutions and the solutions in a given interval
  - url: "https://en.wikipedia.org/wiki/Diophantine_equation"
    locator: section Linear Diophantine equations, subsection One equation
---

A linear Diophantine equation in two unknowns is an equation $ax + by = c$ with given integers $a$, $b$ and $c$, to be solved in integers $x$ and $y$. It has a solution if and only if $g = \gcd(a, b)$ divides $c$, and then all solutions are $x = x_0 + k\, b/g$, $y = y_0 - k\, a/g$ for one particular solution $(x_0, y_0)$ and every integer $k$. The [extended Euclidean algorithm](/extended-euclidean-algorithm/) finds $g$ and a particular solution in $O(\log \min(|a|, |b|))$ word operations; the page [finding a solution of a linear Diophantine equation](/linear-diophantine-solution/) gives the algorithm. The problem is the same as a [linear congruence](/linear-congruence/) $ax \equiv c \pmod b$, and it is the step that merges two congruences in the [Chinese remainder theorem](/chinese-remainder-theorem/).

## In plain words

You have two kinds of steps, one of length a and one of length b, and you may take each kind forward or backward any whole number of times. Can you land exactly at distance c? Every place you can reach is a multiple of the largest number that divides both step lengths, and every such multiple can be reached. So the answer is yes exactly when that largest common divisor divides c. Once you have one way to get there, you get all the others by trading some steps of one kind for steps of the other kind that cover the same total distance.

## Definition

**Input.** Integers $a$, $b$ and $c$.

**Output.** Either "no solution", or a description of the set

$$S = \{ (x, y) \in \mathbb{Z}^2 : ax + by = c \}.$$

When $S$ is not empty and $(a, b) \ne (0, 0)$, the description is one particular solution $(x_0, y_0)$ together with the step $(b/g, -a/g)$, as in the theorem below.

**Theorem.** Let $g = \gcd(a, b)$.

1. If $a = b = 0$: $S = \mathbb{Z}^2$ when $c = 0$, and $S$ is empty otherwise.
2. If $(a, b) \ne (0, 0)$: $S$ is not empty if and only if $g \mid c$. In that case, for any $(x_0, y_0) \in S$,
$$S = \left\{ \left(x_0 + k \frac{b}{g},\ y_0 - k \frac{a}{g}\right) : k \in \mathbb{Z} \right\},$$
and different $k$ give different solutions.

*Proof.* Case 1 is direct. For case 2, $g$ divides $ax + by$ for all integers $x$ and $y$, so $g \mid c$ is necessary. By [Bézout's identity](/bezouts-identity/) there are $s$ and $t$ with $as + bt = g$; if $g \mid c$, then $(s\, c/g,\ t\, c/g)$ is a solution. For the general form, let $(x, y)$ and $(x_0, y_0)$ both be solutions. Subtracting, $a(x - x_0) = -b(y - y_0)$; divide by $g$ and write $a' = a/g$, $b' = b/g$, which are [coprime](/coprime-integers/). So $a'(x - x_0) = -b'(y - y_0)$. If $b' \ne 0$, then $b' \mid a'(x - x_0)$, so $b' \mid x - x_0$ by Gauss's lemma; write $x - x_0 = k b'$, and cancelling $b'$ gives $y - y_0 = -k a'$. If $b' = 0$, then $b = 0$ and $a' = \pm 1$, so $x = x_0$, and $k = -(y - y_0)/a'$ is an integer with the required form. Conversely each pair of the stated form is a solution, because $a\, k b' - b\, k a' = k(a b - b a)/g = 0$. Different $k$ give different pairs, since $(b', -a') \ne (0, 0)$. $\square$

**Cost models.** On the [word RAM](/word-ram/), $a$, $b$ and $c$ fit in $w$-bit words and each arithmetic operation costs one unit; the particular solution $(s\, c/g, t\, c/g)$ can need about $2w$ bits, so code must use double-width products or reduce first. With arbitrary precision, let $n$ be the largest bit length of $a$, $b$ and $c$, and count bit operations.

## Variants

- **One particular solution.** Output $(x_0, y_0)$ or "none". This is the [algorithm page](/linear-diophantine-solution/).
- **Solutions in a box.** Count or list the solutions with $x_{\min} \le x \le x_{\max}$ and $y_{\min} \le y \le y_{\max}$. Since the solutions form one arithmetic progression, this takes $O(1)$ extra operations after the particular solution; see [solutions in an interval](/linear-diophantine-solutions-in-interval/).
- **Nonnegative solutions.** Solutions with $x, y \ge 0$, a special case of the box. For coprime positive $a$ and $b$, the equation has a nonnegative solution for every $c > ab - a - b$ and for no $c = ab - a - b$; this is Sylvester's answer to the two-coin case of the Frobenius coin problem.
- **Minimal solution.** The solution with the least $|x|$, or the least $x \ge 0$, or the least $|x| + |y|$: shift $k$ to the right value, found with one division.
- **Several unknowns.** $a_1 x_1 + \cdots + a_m x_m = c$ is solvable if and only if $\gcd(a_1, \ldots, a_m) \mid c$; fold the extended algorithm over the [GCD of an array](/gcd-of-array/). The solution set is a translate of a lattice of rank $m - 1$.
- **Systems.** $A \mathbf{x} = \mathbf{c}$ with an integer matrix $A$: bring $A$ to [Hermite normal form](/hermite-normal-form/) or [Smith normal form](/smith-normal-form/) with unimodular operations, then solve the diagonal or triangular system.

## Examples

| equation | $g$ | particular solution | all solutions |
| --- | --- | --- | --- |
| $3x + 5y = 1$ | 1 | $(2, -1)$ | $(2 + 5k, -1 - 3k)$ |
| $1071x + 462y = 63$ | 21 | $(-9, 21)$ | $(-9 + 22k, 21 - 51k)$ |
| $6x + 9y = 7$ | 3 | none, $3 \nmid 7$ | none |
| $-4x + 6y = 10$ | 2 | $(-1, 1)$ | $(-1 + 3k, 1 + 2k)$ |
| $0x + 0y = 0$ | 0 | $(0, 0)$ | every pair |
| $5x + 0y = 15$ | 5 | $(3, 0)$ | $(3, k)$ |
| $832040x + 1346269y = 1$ | 1 | $(514229, -317811)$ | $(514229 + 1346269k, -317811 - 832040k)$ |

For $1071x + 462y = 63$: the extended Euclidean algorithm gives $1071 \cdot (-3) + 462 \cdot 7 = 21$, and $63 = 3 \cdot 21$, so $(x_0, y_0) = (-9, 21)$. The step is $(462/21, -1071/21) = (22, -51)$. For $k = 1$: $1071 \cdot 13 + 462 \cdot (-30) = 13923 - 13860 = 63$.

The last row uses consecutive Fibonacci numbers $F_{30} = 832040$ and $F_{31} = 1346269$; the solution is $(F_{29}, -F_{28})$, from the identity $F_{30} F_{29} - F_{31} F_{28} = 1$. Consecutive Fibonacci numbers are the worst case for the number of steps of the Euclidean algorithm, by [Lamé's theorem](/lames-theorem/).

## Known algorithms

- **Extended Euclidean algorithm.** Compute $g$, $s$ and $t$ with $as + bt = g$; test $g \mid c$; return $(s\, c/g,\ t\, c/g)$. It takes $O(\log \min(|a|, |b|))$ division steps, so $O(1 + \log \min(|a|, |b|))$ time on the word RAM, and $O(n^2)$ bit operations with schoolbook arithmetic. For positive $a \ne b$, the coefficients it returns satisfy $|s| \le b/(2g)$ and $|t| \le a/(2g)$, so no intermediate value is larger than the inputs; only the final multiplication by $c/g$ can need double width. See [linear Diophantine solution](/linear-diophantine-solution/).
- **Fast extended gcd.** For long integers, the [half-GCD](/half-gcd/) computes $g$, $s$ and $t$ with $O(M(n) \log n)$ bit operations, where $M(n)$ is the cost of multiplying $n$-bit integers. [Lehmer's GCD](/lehmers-gcd/) speeds up the quadratic method by a constant factor.
- **Modular inverse.** If $g = 1$, then $x_0 \equiv c\, a^{-1} \pmod{b}$ and $y_0 = (c - a x_0)/b$; any method for the [modular inverse](/modular-inverse/) works.
- **Kuttaka.** The Indian kuttaka method, from Aryabhata's Aryabhatiya, also derives a solution from the sequence of Euclidean quotients.

## Bounds

The extended gcd solves the problem with $O(1)$ extra multiplications and divisions. Conversely, a solver must decide whether $\gcd(a, b) \mid c$, and on the input $c = \gcd(a, b)$ its output is a pair of Bézout coefficients. No method faster than the gcd is known, so the bounds are those of the [GCD of two integers](/gcd-of-two-integers/): $O(\log \min(|a|, |b|))$ word operations, and between $\Omega(n)$ and $O(M(n) \log n)$ bit operations.

The output can be kept small: if $b \ne 0$, reducing $x_0$ modulo $|b|/g$ gives the particular solution with $0 \le x_0 < |b|/g$, and then $|y_0| = |c - a x_0|/|b| < |c|/|b| + |a|/g$.

## Reductions

- **Linear congruence.** $ax \equiv c \pmod{m}$ has the solutions $x$ of $ax + my = c$, so a [linear congruence](/linear-congruence/) is the same problem with the $y$ part dropped. The solutions modulo $m$ number $g = \gcd(a, m)$ when $g \mid c$; CLRS solves it this way with MODULAR-LINEAR-EQUATION-SOLVER.
- **Merging two congruences.** $x \equiv r_1 \pmod{m_1}$ and $x \equiv r_2 \pmod{m_2}$ means $x = r_1 + m_1 u = r_2 + m_2 v$, that is, $m_1 u - m_2 v = r_2 - r_1$. It is solvable if and only if $\gcd(m_1, m_2) \mid r_2 - r_1$, and then the solution is unique modulo $\operatorname{lcm}(m_1, m_2)$. This is the general [Chinese remainder theorem](/chinese-remainder-theorem/) for two moduli.
- **Meeting of two progressions.** The sequences $p + a i$ and $q + b j$ with $i, j \ge 0$ share a term exactly when $a i - b j = q - p$ has a nonnegative solution.

## Applications

- **Chinese remainder theorem with non-coprime moduli**, as above.
- **Water jugs.** With jugs of $a$ and $b$ liters, an amount $c \le \max(a, b)$ can be measured exactly when $\gcd(a, b) \mid c$; see the [water jug problem](/water-jug-problem/).
- **Lattice points on a line.** The integer points on the line $ax + by = c$ are the solutions; on a segment between two lattice points $(x_1, y_1)$ and $(x_2, y_2)$ there are $\gcd(|x_2 - x_1|, |y_2 - y_1|) + 1$ of them.
- **Change and scheduling.** Paying an amount with two coin values, or finding when two periodic events with offsets coincide, are linear Diophantine equations with sign or range constraints.

## References
