---
tag: BF0FYC
kind: problem
slug: linear-diophantine-solutions-in-interval
name: Counting solutions of a linear Diophantine equation in an interval
aliases:
- Finding the number of solutions and the solutions in a given interval
area: number-theory/divisibility-and-gcd
level: core
summary: Count the integer solutions of a x plus b y equals c whose x and y both lie in given ranges.
prereqs: [linear-diophantine-equation, linear-diophantine-solution]
see_also: [extended-euclidean-algorithm, linear-congruence, chinese-remainder-theorem, coin-change-counting, lattice-point-counting, integer-division, bezouts-identity, gcd-of-two-integers]
sources:
  - url: "https://cp-algorithms.com/algebra/linear-diophantine-equation.html"
    locator: sections Finding the number of solutions and the solutions in a given interval, and Find the solution with minimum value of x + y
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 31.4, Solving modular linear equations (the solutions of a x = b mod n form one residue class modulo n/d, with d = gcd(a, n))
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, third edition
    locator: Section 4.5.2, The Greatest Common Divisor (Algorithm X, the extended Euclidean algorithm)
---

This problem asks for the number of integer solutions of $ax + by = c$ with $x_{\min} \le x \le x_{\max}$ and $y_{\min} \le y \le y_{\max}$, and possibly for the list of them. Because all solutions of a [linear Diophantine equation](/linear-diophantine-equation/) form one arithmetic progression $(x_0 + k\, b/g,\ y_0 - k\, a/g)$ with $g = \gcd(a, b)$, each bound on $x$ or $y$ turns into a bound on the integer $k$. The answer is the size of an intersection of two intervals of integers. So one run of the [extended Euclidean algorithm](/extended-euclidean-algorithm/) and $O(1)$ more divisions solve it, in $O(1 + \log \min(|a|, |b|))$ word operations, however large the box is.

## In plain words

First find one solution of the equation. All the other solutions come from it by taking equal steps: each step moves the first unknown up by a fixed amount and the second one down by a fixed amount. Number the solutions by how many steps they are from the one you found. The limits on the first unknown allow only a run of step numbers, and the limits on the second unknown allow another run. The solutions you want are the step numbers in both runs, so you count the overlap of two runs of whole numbers. This needs a few divisions, not a search through the box.

## Definition

**Input.** Integers $a$, $b$, $c$ and bounds $x_{\min} \le x_{\max}$, $y_{\min} \le y_{\max}$.

**Output.** The number of pairs in

$$S = \{ (x, y) \in \mathbb{Z}^2 : ax + by = c,\ x_{\min} \le x \le x_{\max},\ y_{\min} \le y \le y_{\max} \},$$

and, in the listing variant, the elements of $S$ in order of increasing $x$.

**Structure.** If $(a, b) \ne (0, 0)$ and $g = \gcd(a, b)$ divides $c$, the solutions without bounds are $(x_0 + k\, d_x,\ y_0 + k\, d_y)$ for $k \in \mathbb{Z}$, with $d_x = b/g$ and $d_y = -a/g$; see the [problem page](/linear-diophantine-equation/). If $g \nmid c$, $S$ is empty. The case $a = b = 0$ is degenerate: every pair of the box solves $0 = c$ when $c = 0$, and none does otherwise.

**Cost models.** On the [word RAM](/word-ram/), the inputs are $w$-bit words and each operation costs one unit; intermediate values such as $x_0$ can need $2w$ bits. With arbitrary precision, $n$ is the largest bit length of the inputs and costs are in bit operations.

## Variants

- **Nonnegative solutions.** $x, y \ge 0$, with the upper bounds implied by $ax + by = c$ when $a, b > 0$. For coprime positive $a$ and $b$, the count has a closed form: it equals $c/(ab) - \{ c\, b'/a \} - \{ c\, a'/b \} + 1$, where $b'$ is the inverse of $b$ modulo $a$, $a'$ is the inverse of $a$ modulo $b$, and $\{\cdot\}$ is the fractional part (a formula of Popoviciu). This is the two-coin case of [counting the ways to make change](/coin-change-counting/).
- **One-sided bounds.** Only $x \ge x_{\min}$, for example the smallest nonnegative $x$: one bound on $k$, and the answer is $x_0 + k d_x$ for the extreme $k$.
- **Optimizing a linear function.** Minimize $x + y$, or any $\alpha x + \beta y$, over $S$. Along the progression, $x + y = x_0 + y_0 + k(d_x + d_y)$ is linear in $k$, so the optimum is at one end of the interval of $k$.
- **Listing.** After the count, output the solutions for $k$ from the lower end to the upper end, in $O(1)$ time each.
- **Inequalities.** Counting the lattice points with $ax + by \le c$, $x, y \ge 0$ is a different problem, a sum of floors; see [lattice point counting](/lattice-point-counting/).

## Examples

**Example 1.** $1071x + 462y = 63$ with $0 \le x \le 100$ and $-300 \le y \le 300$. Here $g = 21$, $(x_0, y_0) = (-9, 21)$, $d_x = 22$ and $d_y = -51$.

| constraint | condition on $k$ | interval of $k$ |
| --- | --- | --- |
| $0 \le -9 + 22k \le 100$ | $9/22 \le k \le 109/22$ | $[1, 4]$ |
| $-300 \le 21 - 51k \le 300$ | $-279/51 \le k \le 321/51$ | $[-5, 6]$ |
| both | | $[1, 4]$ |

So there are 4 solutions: $(13, -30)$, $(35, -81)$, $(57, -132)$ and $(79, -183)$.

**Example 2.** $3x + 5y = 100$ with $0 \le x, y \le 100$. The extended Euclidean algorithm gives $3 \cdot 2 + 5 \cdot (-1) = 1$, so $(x_0, y_0) = (200, -100)$, $d_x = 5$ and $d_y = -3$. The bound on $x$ gives $k \in [-40, -20]$, the bound on $y$ gives $k \in [-66, -34]$, and the intersection $[-40, -34]$ has 7 elements: $(0, 20)$, $(5, 17)$, $(10, 14)$, $(15, 11)$, $(20, 8)$, $(25, 5)$ and $(30, 2)$. The closed form agrees: $b' = 5^{-1} \bmod 3 = 2$, $a' = 3^{-1} \bmod 5 = 2$, and $100/15 - \{200/3\} - \{200/5\} + 1 = 20/3 - 2/3 - 0 + 1 = 7$.

**Example 3.** $6x + 9y = 7$: $g = 3 \nmid 7$, so the count is 0 for every box. **Example 4.** $0x + 4y = 8$ with $-2 \le x \le 2$ and $0 \le y \le 5$: $y = 2$ is forced and $x$ is free, so the count is 5.

## Known algorithms

**Intersect the intervals of $k$.**

1. If $a = b = 0$: return $(x_{\max} - x_{\min} + 1)(y_{\max} - y_{\min} + 1)$ if $c = 0$, else 0.
2. Run the [algorithm for one solution](/linear-diophantine-solution/) to get $g$ and $(x_0, y_0)$, or return 0 if $g \nmid c$.
3. Set $d_x = b/g$ and $d_y = -a/g$.
4. For the coordinate $x$: if $d_x = 0$, the value $x = x_0$ is fixed, and the bound on $x$ allows every $k$ if $x_{\min} \le x_0 \le x_{\max}$ and no $k$ otherwise. If $d_x > 0$, the bound gives $\lceil (x_{\min} - x_0)/d_x \rceil \le k \le \lfloor (x_{\max} - x_0)/d_x \rfloor$. If $d_x < 0$, the inequalities flip: $\lceil (x_{\max} - x_0)/d_x \rceil \le k \le \lfloor (x_{\min} - x_0)/d_x \rfloor$.
5. Do the same for $y$ with $y_0$ and $d_y$.
6. Intersect the two intervals into $[L, R]$ and return $\max(0, R - L + 1)$. Since $(d_x, d_y) \ne (0, 0)$, at least one coordinate gives a finite interval, so the count is finite.

*Correctness.* By the structure theorem, $k \mapsto (x_0 + k d_x, y_0 + k d_y)$ is a bijection from $\mathbb{Z}$ onto the solutions, so $|S|$ is the number of integers $k$ that satisfy both bound pairs. For $d > 0$, the integer $k$ satisfies $u \le x_0 + k d$ if and only if $k \ge (u - x_0)/d$, that is, $k \ge \lceil (u - x_0)/d \rceil$; the other three inequalities are the same with floor or with the sign of $d$ reversed. When exactly one of $d_x$, $d_y$ is 0, that coordinate is constant and its bound is a yes or no test.

*Cost.* Step 2 takes $O(1 + \log \min(|a|, |b|))$ word operations by [Lamé's theorem](/lames-theorem/); steps 3 to 6 take $O(1)$ divisions. With arbitrary precision, $O(n^2)$ bit operations with schoolbook arithmetic, or $O(M(n) \log n)$ with the [half-GCD](/half-gcd/).

**Search.** Trying each $x$ in $[x_{\min}, x_{\max}]$ and testing $b \mid c - ax$ takes $\Theta(x_{\max} - x_{\min} + 1)$ time. It is the brute-force reference for tests, not a method for large boxes.

## Bounds

The count can be as large as $\min(x_{\max} - x_{\min} + 1, y_{\max} - y_{\min} + 1)$ when $g = |a| = |b|$, yet the algorithm above never depends on the size of the box. It needs at least the work to decide whether $g \mid c$, and it needs a particular solution to locate the progression, so its cost is that of the extended gcd up to $O(1)$ operations: $\Theta(1 + \log \min(|a|, |b|))$ word operations in the worst case, attained on consecutive Fibonacci numbers. Listing $s$ solutions costs $O(s)$ more.

## Reductions

- **To one solution.** Steps 3 to 6 above reduce the counting problem to [one solution of the equation](/linear-diophantine-solution/) plus $O(1)$ arithmetic.
- **From a linear congruence in a range.** The number of $x$ in $[u, v]$ with $ax \equiv c \pmod m$ is the case $b = m$ with $y$ unbounded. By the theory of [linear congruences](/linear-congruence/), the solutions form one residue class modulo $m/g$, so the count is that of an arithmetic progression in $[u, v]$.
- **Two periodic events.** The number of common times in $[u, v]$ of two progressions $p + a i$ and $q + b j$ is the count for $ai - bj = q - p$ with the bounds translated to $i$ and $j$; the common times themselves form a progression with difference $\operatorname{lcm}(a, b)$, as in the [Chinese remainder theorem](/chinese-remainder-theorem/).

## Applications

- **Change with two coins.** The number of ways to pay $c$ with coins of values $a$ and $b$ is the count of nonnegative solutions.
- **Scheduling and timetables.** How often two periodic events with offsets coincide within a time window.
- **Lattice points on a segment.** The lattice points of the segment of the line $ax + by = c$ inside a box.
- **Programming contests.** "Count the solutions in a range" and "minimize $x + y$ subject to bounds" are standard tasks built on this method.

## References
