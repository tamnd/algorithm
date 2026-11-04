---
tag: 2Y3JCH
kind: concept
slug: arithmetic-series
name: Arithmetic series
aliases:
- arithmetic progression sum
area: foundations/asymptotic-analysis
level: intro
summary: The sum of an arithmetic progression, which equals n(a+l)/2 and gives quadratic bounds for nested loops.
prereqs: [asymptotic-notation]
see_also: [geometric-series, harmonic-series, integral-bounds-for-sums, quadratic-time, insertion-sort, selection-sort]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Appendix A, Summations
  - book: isbn:9780201558029
    title: Graham, Knuth and Patashnik, Concrete Mathematics, second edition
    locator: Chapter 2, Sums
  - book: isbn:9780201896831
    title: Donald E. Knuth, The Art of Computer Programming, Volume 1, third edition
    locator: Section 1.2.3, Sums and products
---

An arithmetic series is the sum of the terms of an arithmetic progression: a list $a, a+d, a+2d, \dots$ in which each term is the previous term plus a fixed difference $d$. The sum of $n$ terms with first term $a$ and last term $\ell$ is $n(a+\ell)/2$. In algorithm analysis the main case is $1 + 2 + \dots + n = n(n+1)/2$, which is $\Theta(n^2)$ in [asymptotic notation](/asymptotic-notation/) and is the exact cost of many nested loops.

## In plain words

Write the numbers from 1 to 100 in a row. Write them again below, in reverse order. Each column adds to 101, and there are 100 columns. The two rows together add to 10100, so one row adds to 5050. The same trick works for any list in which each step adds the same amount.

A loop in which the inner part does one more step in each round makes such a list. The work is 1 step, then 2 steps, then 3 steps, and so on. The total is about half of a square, so it grows like the square of the number of rounds. If the work in each round grows like the square of the round number, the total grows like the cube. In general the power goes up by one.

## The idea

**Closed form.** Let $n \ge 1$, let $a_i = a + id$ for $i = 0, \dots, n-1$, and let $\ell = a_{n-1}$ be the last term. Then

$$ S = \sum_{i=0}^{n-1} (a + id) = \frac{n(a + \ell)}{2} = na + d\,\frac{n(n-1)}{2}. $$

*Proof (Gauss pairing).* Write $S$ twice, once in the given order and once in the reverse order. The term $a_i$ meets the term $a_{n-1-i}$. Their sum is $a + id + a + (n-1-i)d = 2a + (n-1)d = a + \ell$, for each $i$. So $2S = n(a + \ell)$. Divide by 2. The second form follows from $\ell = a + (n-1)d$ and $\sum_{i=0}^{n-1} i = n(n-1)/2$, which is the case $a = 0$, $d = 1$. $\square$

*Proof by induction, for $T_n = 1 + 2 + \dots + n = n(n+1)/2$.* For $n = 0$ the sum is empty and the formula gives 0. Assume $T_n = n(n+1)/2$. Then $T_{n+1} = T_n + (n+1) = (n+1)(n/2 + 1) = (n+1)(n+2)/2$, which is the formula for $n+1$. $\square$

**Number of terms.** When the first term $a$, the last term $\ell$ and the difference $d \ne 0$ are given, the number of terms is $n = (\ell - a)/d + 1$, provided $\ell$ is a term of the progression, that is, $d$ divides $\ell - a$ and $(\ell - a)/d \ge 0$. If you forget the $+1$, you count $n - 1$ terms, and for $1 + \dots + n$ you get $(n-1)(n+1)/2$ in place of $n(n+1)/2$. A related off-by-one error is a wrong last term: $1 + \dots + (n-1) = n(n-1)/2$ is not $1 + \dots + n = n(n+1)/2$.

The numbers $T_n$ are the *triangular numbers*. They also count the pairs: $T_{n-1} = \binom{n}{2}$ is the number of pairs $i < j$ in $\{1, \dots, n\}$.

**Sum of squares.** For each integer $n \ge 0$,

$$ \sum_{j=1}^{n} j^2 = \frac{n(n+1)(2n+1)}{6}. $$

*Proof.* Induction on $n$. For $n = 0$ both sides are 0. Assume the formula for $n$. Then the sum for $n+1$ is $\frac{n(n+1)(2n+1)}{6} + (n+1)^2 = \frac{(n+1)\,(n(2n+1) + 6(n+1))}{6} = \frac{(n+1)(2n^2 + 7n + 6)}{6} = \frac{(n+1)(n+2)(2n+3)}{6}$. This is the formula for $n+1$. $\square$

**Sum of cubes.** For each integer $n \ge 0$, $\sum_{j=1}^{n} j^3 = \left(\frac{n(n+1)}{2}\right)^2 = T_n^2$.

*Proof.* Induction on $n$. For $n = 0$ both sides are 0. Assume the formula for $n$. Then the sum for $n+1$ is $\frac{n^2(n+1)^2}{4} + (n+1)^3 = \frac{(n+1)^2 (n^2 + 4n + 4)}{4} = \left(\frac{(n+1)(n+2)}{2}\right)^2$. $\square$

**Sum of $k$-th powers.** For each fixed real $k \ge 0$, $\sum_{j=1}^{n} j^k = \Theta(n^{k+1})$.

*Proof.* Upper bound: each of the $n$ terms is at most $n^k$, so the sum is at most $n^{k+1}$. Lower bound: let $m = \lceil n/2 \rceil$. The terms with $j = m, \dots, n$ number $n - m + 1 \ge (n+1)/2 \ge n/2$, and each is at least $m^k \ge (n/2)^k$. All terms are non-negative, so the sum is at least $(n/2)(n/2)^k = n^{k+1}/2^{k+1}$. Both bounds hold for each $n \ge 1$. $\square$

The constant is known: the sum is $\sim n^{k+1}/(k+1)$. This follows from the [integral bounds for sums](/integral-bounds-for-sums/): $\int_0^n x^k\,dx \le \sum_{j=1}^n j^k \le \int_1^{n+1} x^k\,dx$, because $x^k$ is non-decreasing. The sum of the first $n$ integers is not $\Theta(n)$, and the sum of the first $n$ squares is not $\Theta(n^2)$: the exponent grows by one.

## Examples

Exact values for $n = 10$: $\sum j = 55$, $\sum j^2 = 385$, $\sum j^3 = 3025$. The ratio $\sum_{j \le n} j^2 / n^3$ is 0.385 for $n = 10$, 0.33835 for $n = 100$ and 0.3338335 for $n = 1000$, and it tends to $1/3$.

**Selection sort.** [Selection sort](/selection-sort/) finds the minimum of $A[i..n]$ for $i = 1, \dots, n-1$. The search for round $i$ makes $n - i$ comparisons. So the total is $(n-1) + (n-2) + \dots + 1 = n(n-1)/2$ comparisons on each input of length $n$. For $n = 10$ this is 45.

**Insertion sort.** [Insertion sort](/insertion-sort/) inserts $A[i]$ into the sorted prefix $A[1..i-1]$ for $i = 2, \dots, n$. Count one comparison of the key with an element, and stop at the left end without a comparison. On a reverse-sorted array, the key of round $i$ is compared with all $i - 1$ elements before it. The total is $1 + 2 + \dots + (n-1) = n(n-1)/2$. For $[5,4,3,2,1]$ this is 10. On a sorted array each round makes one comparison, so the total is $n - 1$, which is 4 for $[1,2,3,4,5]$. In the worst case the time is $\Theta(n^2)$.

**A nested loop.** The loop `for i = 1 to n, for j = 1 to i` runs its body $n(n+1)/2$ times. The loop `for i = 1 to n, for j = i+1 to n` runs it $n(n-1)/2$ times, once for each pair $i < j$. Both are $\Theta(n^2)$, and both are about half of the $n^2$ steps of the loop with full ranges.

**Non-examples.**

- The sum $\sum_{j=1}^{n} 1/j$ is not an arithmetic series: its terms have no fixed difference. It is the [harmonic series](/harmonic-series/) and it is $\Theta(\log n)$.
- The sum $1 + 2 + 4 + \dots + 2^{n}$ is not arithmetic: each term is the previous term times 2. It is a [geometric series](/geometric-series/) and it is $\Theta(2^n)$.
- The sum $\sum_{j=1}^{n} j^j$ is not a power sum: the exponent depends on $j$.

## Where it is used

- **Quadratic sorts.** The comparison counts of [selection sort](/selection-sort/) and of the worst case of [insertion sort](/insertion-sort/) are $n(n-1)/2$. This sum is the most common source of [quadratic time](/quadratic-time/) bounds.
- **Nested loops.** A loop whose inner range is bounded by the outer index costs $\Theta(n^2)$, and, for a fixed $d$, the $d$ nested loops with $1 \le i_d \le \dots \le i_1 \le n$ run their body $\binom{n+d-1}{d} = \Theta(n^d)$ times. To get the order, apply the power sum once for each level, from the innermost loop out. A formal count turns the nest into a sum and uses the closed form.
- **Bounds with a constant.** The exact value $n(n-1)/2$ matters when you compare two algorithms with the same $\Theta$ bound. The [tilde notation](/tilde-notation/) keeps the leading term $n^2/2$.
- **Other sums.** The [integral bounds for sums](/integral-bounds-for-sums/) generalise the power-sum argument to other monotone terms, and the [harmonic series](/harmonic-series/) is the case $k = -1$, which the rule $\Theta(n^{k+1})$ does not cover.

## References
