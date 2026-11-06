---
tag: 61JQEE
kind: theorem
slug: lames-theorem
name: Lamé's theorem
aliases:
- Lamé's theorem on Euclid's algorithm
area: number-theory/divisibility-and-gcd
level: advanced
summary: Euclid's algorithm on inputs with d digits takes O(d) division steps, bounded via Fibonacci numbers.
prereqs: [euclidean-algorithm, fibonacci-numbers, gcd-recursion-theorem]
see_also: [gcd-of-two-integers, extended-euclidean-algorithm, continued-fraction, binary-gcd, lehmers-gcd, gcd-of-array, linear-diophantine-solution, stern-brocot-tree]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 31.2, Greatest common divisor (the running time of Euclid's algorithm, the Fibonacci lemma and Lamé's theorem)
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, third edition
    locator: Section 4.5.3, Analysis of Euclid's Algorithm (the worst case and Lamé's theorem, and the average number of division steps)
  - book: isbn:9780199219865
    title: G. H. Hardy and E. M. Wright, An Introduction to the Theory of Numbers, sixth edition
    locator: Section 10.14, The series of Fibonacci and Lucas
  - paper: "J. Shallit, Origins of the analysis of the Euclidean algorithm, Historia Mathematica 21 (1994)"
    locator: pages 401 to 419 (Lamé's 1844 note and the earlier bounds)
---

Lamé's theorem bounds the number of division steps of the [Euclidean algorithm](/euclidean-algorithm/). If the algorithm on $a > b \ge 1$ performs $k$ divisions, then $b \ge F_{k+1}$ and $a \ge F_{k+2}$, where $F_j$ are the [Fibonacci numbers](/fibonacci-numbers/). Since $F_{k+1} \ge \varphi^{k-1}$ with $\varphi = (1 + \sqrt 5)/2$, the number of steps is at most $1 + \log_\varphi b$, and at most five times the number of decimal digits of $b$. Consecutive Fibonacci numbers reach the bound exactly, so it cannot be improved. The theorem makes the gcd a logarithmic-time operation on the [word RAM](/word-ram/), and it is one of the oldest results in the analysis of algorithms.

## Statement

For $a > b \ge 1$, let $r_0 = a$, $r_1 = b$, and $r_{i+1} = r_{i-1} \bmod r_i$ while $r_i \ne 0$. The **number of division steps** is the $k \ge 1$ with $r_k \ne 0$ and $r_{k+1} = 0$; then $r_k = \gcd(a, b)$. Let $F_0 = 0$, $F_1 = 1$ and $F_{j+2} = F_{j+1} + F_j$.

**Theorem (Lamé).** If the Euclidean algorithm on $a > b \ge 1$ performs $k$ division steps, then

$$a \ge F_{k+2} \quad \text{and} \quad b \ge F_{k+1}.$$

**Corollary.** For $a > b \ge 1$, the number of division steps $k$ satisfies

$$k \le 1 + \log_\varphi b \qquad \text{and} \qquad k \le 5 d,$$

where $d$ is the number of decimal digits of $b$.

**Tightness.** For every $k \ge 1$, the pair $(F_{k+2}, F_{k+1})$ takes exactly $k$ steps. So it is the pair with the smallest $a$, and with the smallest $b$, among those that take $k$ steps.

If $a < b$, the first step only swaps the two numbers, so the bound grows by 1; if $a = b$, there is one step.

## In plain words

Each step of Euclid's method replaces the larger of two numbers by the remainder after dividing it by the smaller one. Look at the steps backward from the end. The last nonzero remainder is at least one. The number before it is at least two. Every earlier number is at least the sum of the two numbers that come after it. This is the rule that makes the Fibonacci numbers, so the starting numbers are at least as big as Fibonacci numbers, and Fibonacci numbers grow by a fixed factor at each step. So the number of steps grows only with the number of digits of the inputs, and adding one decimal digit adds at most five steps.

## Proof

**The theorem.** Let $k$ be the number of steps, so $r_1 > r_2 > \cdots > r_k \ge 1$ and $r_{k+1} = 0$, and also $r_0 = a > b = r_1$. For $1 \le i \le k$, write $r_{i-1} = q_i r_i + r_{i+1}$ with $q_i = \lfloor r_{i-1} / r_i \rfloor$.

1. Because $r_{i-1} > r_i$ for every $i \le k$, each quotient satisfies $q_i \ge 1$.
2. In the last step $r_{k+1} = 0$, so $r_{k-1} = q_k r_k$ with $r_{k-1} > r_k$; hence $q_k \ge 2$.

We show $r_i \ge F_{k+2-i}$ for $i = k, k-1, \ldots, 0$ by downward induction.

- $i = k$: $r_k \ge 1 = F_2$.
- $i = k - 1$: $r_{k-1} = q_k r_k \ge 2 = F_3$.
- $i \le k - 2$: $r_i = q_{i+1} r_{i+1} + r_{i+2} \ge r_{i+1} + r_{i+2} \ge F_{k+1-i} + F_{k-i} = F_{k+2-i}$, using step 1 and the induction hypothesis for $i + 1$ and $i + 2$.

With $i = 1$ and $i = 0$ this gives $b \ge F_{k+1}$ and $a \ge F_{k+2}$. $\square$

**The corollary.** By induction, $F_{j} \ge \varphi^{j-2}$ for $j \ge 1$: it holds for $j = 1$ and $j = 2$, and $\varphi^{j-1} + \varphi^{j-2} = \varphi^{j-2}(\varphi + 1) = \varphi^{j}$ because $\varphi^2 = \varphi + 1$. So $b \ge F_{k+1} \ge \varphi^{k-1}$ and $k \le 1 + \log_\varphi b$. For the decimal form, $\varphi^5 \approx 11.09 > 10$. If $b$ has $d$ digits and $k \ge 5d + 1$, then $b \ge \varphi^{k-1} \ge \varphi^{5d} > 10^d$, which contradicts $b < 10^d$. So $k \le 5d$. $\square$

**Tightness.** For $k = 1$, $(F_3, F_2) = (2, 1)$ takes one step. For $k \ge 2$, $F_{k+2} = 1 \cdot F_{k+1} + F_k$ with $0 < F_k < F_{k+1}$, so the first step maps $(F_{k+2}, F_{k+1})$ to $(F_{k+1}, F_k)$, which takes $k - 1$ steps by induction. If another pair $(a, b)$ takes $k$ steps, the theorem gives $a \ge F_{k+2}$ and $b \ge F_{k+1}$. $\blacksquare$

## Consequences

**Examples.**

| $(a, b)$ | steps | bound $1 + \log_\varphi b$ | bound $5d$ |
| --- | --- | --- | --- |
| $(1071, 462)$ | 3 | 13.8 | 15 |
| $(13, 8) = (F_7, F_6)$ | 5 | 5.3 | 5 |
| $(89, 55) = (F_{11}, F_{10})$ | 9 | 9.3 | 10 |
| $(1346269, 832040) = (F_{31}, F_{30})$ | 29 | 29.3 | 30 |

The pair $(13, 8)$ shows that the bound $5d$ is reached for $d = 1$: a one-digit $b$ can need 5 steps. The same holds for $d = 2$ with $(F_{12}, F_{11}) = (144, 89)$ and $d = 3$ with $(F_{17}, F_{16}) = (1597, 987)$, which take 10 and 15 steps.

- **Gcd in logarithmic time.** On the [word RAM](/word-ram/), the Euclidean algorithm and the [extended Euclidean algorithm](/extended-euclidean-algorithm/) take $O(1 + \log \min(a, b))$ operations. This is the bound used for [linear Diophantine equations](/linear-diophantine-solution/), modular inverses and the [GCD of two integers](/gcd-of-two-integers/).
- **Bit complexity.** For $n$-bit inputs there are $O(n)$ steps, so the naive bound is $O(n^3)$ bit operations; a finer count, using that the sum of the logarithms of the quotients is at most $\log a$, gives $O(n^2)$.
- **Continued fractions.** The number of partial quotients of the [continued fraction](/continued-fraction/) of $a/b$ is the number of steps, so it is at most $1 + \log_\varphi b$; the slowest case is $F_{k+2}/F_{k+1}$, whose partial quotients are all 1, and which approaches $\varphi$.
- **Telescoping.** The steps on $(a, b)$ are the same as on $(a/g, b/g)$ with $g = \gcd(a, b)$, so the count is at most $1 + \log_\varphi(b/g)$. Summed over a fold of gcds, this gives the $O(k + \log \max)$ bound for the [GCD of an array](/gcd-of-array/).
- **Average case.** For a fixed $b$ and $a$ uniform in $[1, b]$, the average number of steps is asymptotic to $(12 \ln 2 / \pi^2) \ln b \approx 0.843 \ln b$, against the worst case $\log_\varphi b \approx 2.078 \ln b$; Knuth derives this in Section 4.5.3.

## Tightness

The constant $\varphi$ cannot be lowered: the Fibonacci pairs take $k = \log_\varphi b + O(1)$ steps. Other remainder rules change it. With the least absolute remainder, where each step may round the quotient up, the worst case has fewer steps, and the [binary GCD](/binary-gcd/) is measured in shifts and subtractions instead of divisions. The bound $5d$ for decimal digits is exact for $d \le 3$ but not for every $d$: for $d = 4$, the largest $k$ with $F_{k+1} < 10^4$ is 19, not 20.

## History

Gabriel Lamé published the theorem in 1844 in a note in the Comptes Rendus of the Paris Academy, with the bound of five times the number of decimal digits. Shallit's survey in Historia Mathematica (1994) traces earlier bounds on the number of steps, including a logarithmic bound by Finck in 1841. Knuth gives the theorem and its history in Section 4.5.3, and CLRS proves it in Section 31.2 through the lemma $a \ge F_{k+2}$, $b \ge F_{k+1}$.

## References
