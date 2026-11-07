---
tag: N8HHBP
kind: algorithm
slug: fibonacci-fast-doubling
name: Fast doubling method for Fibonacci numbers
aliases:
- Fast doubling method for Fibonacci
- Fibonacci fast doubling
area: algebra/integer-arithmetic
level: core
summary: Computes the n-th Fibonacci number in logarithmic time using identities that give F(2k) and F(2k+1) from F(k) and F(k+1).
solves: [fibonacci-numbers]
model: multitape-turing-machine
complexity:
  vars: {n: the index of the Fibonacci number, M: the cost of multiplying two numbers of the given length in binary digits}
  time: {worst: O(M(n)), average: O(M(n)), best: O(M(n))}
  space: {extra: Θ(n)}
  multiplications: {worst: Θ(log n)}
properties: {deterministic: true, recursive: false}
history:
  note: The doubling identities are cases of the addition law for Fibonacci numbers, studied by Lucas in the 1870s; Dijkstra wrote them up as an algorithm in 1978 (EWD654).
prereqs: [fibonacci-numbers, binary-exponentiation, loop-invariant]
see_also: [matrix-fibonacci, binary-exponentiation, integer-exponentiation, pisano-period, cassini-identity, binet-formula]
sources:
  - url: https://www.cs.utexas.edu/~EWD/ewd06xx/EWD654.PDF
    title: Edsger W. Dijkstra, In honour of Fibonacci, EWD654, 1978
    locator: the whole note (the formulas for F(2n) and F(2n + 1) and the logarithmic algorithm)
  - book: isbn:9780201896831
    title: Donald E. Knuth, The Art of Computer Programming, Volume 1, third edition
    locator: Section 1.2.8, Fibonacci numbers (the matrix identity, equation (4) on F(n + m), and the exercises on computing F(n) quickly)
  - paper: doi:10.1016/S0020-0190(00)00112-5
    title: Daisuke Takahashi, A fast algorithm for computing large Fibonacci numbers, Information Processing Letters 75(6), 2000
    locator: pp. 243 to 246 (the operation counts of the doubling methods, and the Lucas number variant with fewer multiplications)
  - book: isbn:9780073523408
    title: Sanjoy Dasgupta, Christos Papadimitriou and Umesh Vazirani, Algorithms, McGraw-Hill, 2008
    locator: Chapter 0, Prologue, Section 0.2 and Exercise 0.4 (Fibonacci numbers by matrix powers and the cost of the multiplications)
---

Fast doubling computes the Fibonacci number $F_n$ by walking down the bits of $n$ and keeping the pair $(F_k, F_{k+1})$, where $k$ is the number formed by the bits read so far. Each bit doubles $k$, and possibly adds one, using the identities

$$F_{2k} = F_k\,(2F_{k+1} - F_k), \qquad F_{2k+1} = F_k^2 + F_{k+1}^2 .$$

So it uses $\lfloor \log_2 n \rfloor + 1$ passes with three multiplications each, against $n - 1$ additions for the plain loop. Its bit cost is $O(M(n))$, where $M$ is the cost of a [multiplication](/integer-multiplication/), because the numbers double in length at each pass and the last pass dominates. It is the [binary exponentiation](/binary-exponentiation/) of the matrix $\begin{pmatrix} 1 & 1 \\ 1 & 0 \end{pmatrix}$ with the redundant entries removed.

## In plain words

Suppose you know two neighbors of the Fibonacci sequence, say the 5th and the 6th numbers, 5 and 8. Two short formulas then give you the 10th and the 11th numbers directly, without the numbers in between: 5 times (16 minus 5) is 55, and 25 plus 64 is 89. So knowing a pair at position $k$ gives the pair at position $2k$, and one addition more gives the pair at position $2k + 1$.

To reach position $n$, write $n$ in binary. Start at position 0, and for each binary digit, jump from $k$ to $2k$ or to $2k + 1$. After as many jumps as $n$ has binary digits, you are at position $n$. For the millionth Fibonacci number that is 20 jumps, instead of a million additions.

## The problem

The input is an integer $n \ge 0$. The output is $F_n$, where $F_0 = 0$, $F_1 = 1$ and $F_{m} = F_{m-1} + F_{m-2}$; the algorithm also returns $F_{n+1}$. This is the [Fibonacci numbers](/fibonacci-numbers/) problem. The cost is counted in multiplications, and in bit operations on numbers of $\Theta(n)$ digits, since $F_n$ has about $0.694\, n$ binary digits.

## The algorithm

Let $t_{L-1} \cdots t_1 t_0$ be the binary digits of $n$, with $L = \lfloor \log_2 n \rfloor + 1$ for $n \ge 1$ (and $L = 1$, the single digit 0, for $n = 0$).

```pseudo id=main
FAST-DOUBLING(n)                       ▷ returns (F_n, F_{n+1})
L1  (a, b) ← (0, 1)                     ▷ (F_k, F_{k+1}) with k = 0
L2  for each binary digit t of n, from the most significant to the least do
L3      c ← a · (2b − a)                 ▷ F_{2k}
L4      d ← a² + b²                      ▷ F_{2k+1}
L5      if t = 0 then (a, b) ← (c, d)            ▷ k ← 2k
L6      else (a, b) ← (d, c + d)                 ▷ k ← 2k + 1
L7  return (a, b)
```

Line L6 uses $F_{2k+2} = F_{2k} + F_{2k+1}$, so the odd step costs one addition more than the even step. For $F_n \bmod m$, reduce $a$ and $b$ modulo $m$ after each pass; since $2b - a$ can be negative, take the result of line L3 modulo $m$ as a nonnegative number.

## Example

Compute $F_{11}$, with $11 = 1011_2$.

| pass | digit $t$ | $k$ before | $c = F_{2k}$ | $d = F_{2k+1}$ | $k$ after | $(a, b)$ after |
|---|---|---|---|---|---|---|
| start | | | | | 0 | $(0, 1)$ |
| 1 | 1 | 0 | $0 \cdot 2 = 0$ | $0 + 1 = 1$ | 1 | $(1, 1)$ |
| 2 | 0 | 1 | $1 \cdot 1 = 1$ | $1 + 1 = 2$ | 2 | $(1, 2)$ |
| 3 | 1 | 2 | $1 \cdot 3 = 3$ | $1 + 4 = 5$ | 5 | $(5, 8)$ |
| 4 | 1 | 5 | $5 \cdot 11 = 55$ | $25 + 64 = 89$ | 11 | $(89, 144)$ |

So $F_{11} = 89$ and $F_{12} = 144$, after 4 passes and 12 multiplications. The same method gives $F_{100} = 354224848179261915075$ in 7 passes.

## Correctness

The invariant of the loop of line L2 is $(a, b) = (F_k, F_{k+1})$, where $k$ is the number formed by the digits of $n$ read so far. It holds at the start with $k = 0$. A pass reads a digit $t$ and changes $k$ to $2k + t$, and lines L3 to L6 compute $(F_{2k+t}, F_{2k+t+1})$ by the doubling identities. These follow from the matrix identity

$$\begin{pmatrix} 1 & 1 \\ 1 & 0 \end{pmatrix}^k = \begin{pmatrix} F_{k+1} & F_k \\ F_k & F_{k-1} \end{pmatrix}$$

by squaring both sides. After the last digit, $k = n$. The full proof is below.

## Complexity

- **Passes and multiplications.** The loop runs $L = \lfloor \log_2 n \rfloor + 1$ times. Each pass does one product $a \cdot (2b - a)$ and two squares $a^2$ and $b^2$, plus a few additions and a doubling, so there are $3L = \Theta(\log n)$ multiplications. This is the multiplications entry of the front matter.
- **Bit cost.** At the pass where $k$ becomes $k'$, the operands are $F_k$ and $F_{k+1}$, with about $0.694\, k$ binary digits, and $k \le n / 2^{L - j}$ at pass $j$. So the products have sizes about $0.347\, n, 0.174\, n, \ldots$, from the last pass back. If $M(m)/m$ does not decrease, $\sum_j M(0.347\, n / 2^j) \le 2M(0.347\, n)$, and the total is $O(M(n))$; the additions add $O(n)$. With $M(n) = O(n \log n)$ ([integer multiplication](/integer-multiplication/)) this is $O(n \log n)$.
- **Against the loop.** The loop $(a, b) \leftarrow (b, a + b)$ costs $\sum_{k < n} \Theta(k) = \Theta(n^2)$ bit operations. With schoolbook products, fast doubling costs $\Theta(n^2)$ bit operations too, so in the pure bit model it gains only a constant factor. On a word RAM with $w$-bit words, the loop costs $\Theta(n^2 / w)$ word operations and schoolbook doubling $\Theta(n^2 / w^2)$, a gain of a factor $\Theta(w)$; fast multiplication gains more. As one observation on one machine (CPython, with Karatsuba products), $F_{200000}$ took about 1 s by the loop and 0.01 s by fast doubling.
- **Space.** $a$, $b$, $c$ and $d$ have $O(n)$ digits.

## Properties

- **Iterative.** The loop reads the binary digits of $n$ from the top, so no recursion and no stack are needed. The common recursive form, which computes the pair for $\lfloor n/2 \rfloor$ first, has recursion depth $\log_2 n$.
- **Exact.** All arithmetic is on integers; no rounding is involved, unlike [Binet's formula](/binet-formula/) in floating point.
- **Both neighbors.** It returns $F_{n+1}$ as well as $F_n$, which also gives $F_{n-1} = F_{n+1} - F_n$.
- **Ring-generic.** The identities hold in every commutative ring, so the same code computes $F_n \bmod m$ with numbers below $m$, in $\Theta(\log n)$ multiplications modulo $m$.

## Variants and improvements

- **Matrix powers.** [Matrix Fibonacci](/matrix-fibonacci/) raises the $2 \times 2$ matrix to the power $n$ by repeated squaring. A naive $2 \times 2$ product uses 8 multiplications; using the symmetry of the matrix brings it down, and fast doubling is that idea taken to the end, with 3 multiplications per bit.
- **Two squarings per bit.** Takahashi's method computes Lucas numbers along with $F_k$, using $L_{2k} = L_k^2 - 2(-1)^k$ and $F_{2k} = F_k L_k$, which needs about two squarings per bit and favors squaring, which is cheaper than a general product. Other forms, such as $F_{2k+1} = 4F_k^2 - F_{k-1}^2 + 2(-1)^k$, also replace products by squares.
- **Stop one pass early.** In the last pass, only $a$ is needed, so one of the two new values need not be computed. This saves up to a third of the largest pass.
- **Modular Fibonacci.** Reduce modulo $m$ after each pass. For huge $n$, first reduce $n$ modulo the [Pisano period](/pisano-period/) of $m$ if it is known.
- **General recurrences.** The same doubling works for any linear recurrence of order 2, such as the Lucas sequences $U_n(P, Q)$ used in primality tests, with identities for $U_{2k}$ and $U_{2k+1}$.

## When to use it

Use fast doubling for a single large $F_n$, or for $F_n \bmod m$ with a large $n$: it is the simplest method with $O(\log n)$ multiplications. For small $n$ (up to a few hundred), or when all of $F_0, \ldots, F_n$ are needed, the plain loop is simpler and as fast. For the very largest $n$, with fast multiplication, the variants that use mostly squarings, such as Takahashi's, gain a constant factor.

## Pitfalls

- **The order of the digits.** Line L2 reads the binary digits of $n$ from the most significant one. Reading them from the least significant one, as in the right-to-left binary power, makes this loop compute $F$ of the number with the digits of $n$ reversed: for $n = 6 = 110_2$ it returns $F_3 = 2$ instead of $F_6 = 8$.
- **A negative intermediate in modular code.** In line L3, $2b - a$ is negative when $a > 2b$, which happens after a reduction modulo $m$. In languages where `%` truncates toward zero, reduce $2b - a + m$ instead, or the result is a negative residue.
- **Overflow in fixed width.** In 64-bit arithmetic, $F_{93}$ is the largest Fibonacci number that fits in an unsigned word, and the squares of line L4 overflow long before; for $F_n \bmod m$ with $m$ near $2^{64}$, the products of line L3 and line L4 need 128-bit intermediates.
- **Mixing up the two cases.** Line L5 keeps $(F_{2k}, F_{2k+1})$ and line L6 shifts to $(F_{2k+1}, F_{2k+2})$. Swapping them computes the Fibonacci number of a wrong index.

## Implementations

## History

The doubling identities are special cases of the addition law $F_{m+n} = F_{m+1}F_n + F_m F_{n-1}$, one of the identities that Lucas studied in the 1870s. Dijkstra wrote the doubling method up as an algorithm in his note EWD654, "In honour of Fibonacci", in 1978. Takahashi in 2000 compared the operation counts of the doubling methods and gave a variant with Lucas numbers for very large $n$.

## References
