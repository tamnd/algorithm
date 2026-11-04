---
tag: Q3W4HY
kind: technique
slug: linear-recurrences-with-constant-coefficients
name: Linear recurrences with constant coefficients
aliases:
- characteristic equation method
- linear recurrence solution
area: foundations/recurrences
level: core
summary: Solve a linear recurrence through its characteristic polynomial, where repeated roots contribute polynomial factors.
prereqs: [recurrence-relation, generating-functions, partial-fraction-decomposition, fundamental-theorem-of-algebra]
see_also: [binet-formula, fibonacci-numbers, matrix-exponentiation, linear-recurrence-nth-term, jordan-normal-form, berlekamp-massey, closed-form-solution, change-of-variables]
sources:
  - book: isbn:9780201558029
    title: Graham, Knuth and Patashnik, Concrete Mathematics, second edition
    locator: Section 7.3, Solving Recurrences (rational generating functions and their partial fractions)
  - book: isbn:9780321905758
    title: Robert Sedgewick and Philippe Flajolet, An Introduction to the Analysis of Algorithms, second edition
    locator: Section 2.4, Higher-Order Recurrences
  - book: isbn:9781568812793
    title: Herbert S. Wilf, generatingfunctionology, third edition
    locator: Chapter 1, Introductory ideas and examples
---

A linear recurrence with constant coefficients is a [recurrence relation](/recurrence-relation/) $a_n = c_1 a_{n-1} + c_2 a_{n-2} + \cdots + c_d a_{n-d}$ with fixed numbers $c_1, \ldots, c_d$, and the characteristic-polynomial method solves it exactly. Each root $r$ of $x^d - c_1 x^{d-1} - \cdots - c_d$ with multiplicity $m$ contributes $P(n)\, r^n$ with a polynomial $P$ of degree less than $m$, and the $d$ unknown coefficients are fixed by the $d$ initial values. The [Fibonacci numbers](/fibonacci-numbers/) and [Binet's formula](/binet-formula/) are the standard example; the same method handles a non-homogeneous term of the form polynomial times exponential.

## In plain words

In this kind of recurrence, each new term is a fixed mix of the few terms just before it. Such sequences behave like sums of a few basic sequences, each of which grows or shrinks by a fixed factor at every step.

To find the factors, look for a sequence that is multiplied by the same number at each step and still follows the rule. This gives an equation for that number, and its solutions are the factors. The answer is then a mix of these basic sequences, and the first few terms tell you how much of each to take.

Two cases need care. If a factor appears twice as a solution, the basic sequence must also be multiplied by a counter that grows by one per step. If a factor is complex, two complex sequences combine into a real one that oscillates.

## When it applies

- The recurrence is linear in the earlier terms, with coefficients that do not depend on $n$: $a_n = \sum_{i=1}^{d} c_i a_{n-i}$ for $n \ge d$.
- The last coefficient is non-zero, $c_d \ne 0$, so that the order is really $d$. If $c_d = 0$, lower $d$ first (see Pitfalls).
- A non-homogeneous term is allowed when it is a sum of terms $q(n)s^n$ with $q$ a polynomial: $a_n = \sum_i c_i a_{n-i} + q(n)s^n$.
- It does not apply to coefficients that depend on $n$, as in $a_n = n a_{n-1}$, to nonlinear recurrences, or to divide-and-conquer recurrences $T(n/2)$, unless a [change of variables](/change-of-variables/) first brings them into this form.

## The template

1. **Write the characteristic polynomial** $\chi(x) = x^d - c_1 x^{d-1} - \cdots - c_{d-1}x - c_d$. It comes from the trial solution $a_n = x^n$: substituting and dividing by $x^{n-d}$ gives $\chi(x) = 0$.
2. **Find its roots with multiplicities**: $\chi(x) = \prod_{j=1}^{s}(x - r_j)^{m_j}$, with distinct $r_j$ and $\sum_j m_j = d$. Since $c_d \ne 0$, no root is 0.
3. **Write the general solution**
$$a_n = \sum_{j=1}^{s} \big(\beta_{j,0} + \beta_{j,1} n + \cdots + \beta_{j,m_j - 1} n^{m_j - 1}\big)\, r_j^n.$$
4. **Fit the initial values.** The $d$ equations for $n = 0, \ldots, d-1$ have exactly one solution $(\beta_{j,t})$.
5. **Check** a few later terms against the recurrence.

### Why it works

*Every solution has this form.* Let $A(z) = \sum_{n \ge 0} a_n z^n$ be the [generating function](/generating-functions/) and $Q(z) = 1 - c_1 z - \cdots - c_d z^d$. The coefficient of $z^n$ in $Q(z)A(z)$ is $a_n - \sum_{i=1}^{d} c_i a_{n-i}$ for $n \ge d$, which is 0. So $Q(z)A(z) = P(z)$, a polynomial of degree less than $d$. Since $Q(z) = z^d\chi(1/z)$,

$$Q(z) = \prod_{j=1}^{s}(1 - r_j z)^{m_j},$$

of degree exactly $d$ because $c_d \ne 0$. By [partial fractions](/partial-fraction-decomposition/), since $\deg P < \deg Q$,

$$A(z) = \frac{P(z)}{Q(z)} = \sum_{j=1}^{s}\sum_{t=1}^{m_j} \frac{\gamma_{j,t}}{(1 - r_j z)^t}.$$

The binomial series gives $[z^n](1 - rz)^{-t} = \binom{n + t - 1}{t - 1} r^n$, and $\binom{n+t-1}{t-1}$ is a polynomial in $n$ of degree $t - 1$. Collecting terms, $a_n = \sum_j P_j(n) r_j^n$ with $\deg P_j \le m_j - 1$.

*Each such term is a solution.* Let $E$ be the shift, $(Ea)_n = a_{n+1}$. The recurrence says $\chi(E)a = 0$ (applied at each index $n - d$). For a polynomial $q$, $(E - r)(q(n) r^n) = (q(n+1) - q(n))r^{n+1}$, and $q(n+1) - q(n)$ has degree one less than $q$. So $(E - r_j)^{m_j}$ kills $n^t r_j^n$ for $t < m_j$. The operators $(E - r_i)^{m_i}$ commute, so $\chi(E) = \prod_i (E - r_i)^{m_i}$ also kills it.

*The fit is unique.* The solutions form a vector space, and the map from a solution to its first $d$ values is a bijection onto $\mathbb{C}^d$, because the recurrence computes the rest. So the space has dimension $d$. The $d$ sequences $n^t r_j^n$ ($t < m_j$) span it by the first part, so they are a basis, and the system of step 4 has exactly one solution. $\square$

### Non-homogeneous terms

For $a_n = \sum_i c_i a_{n-i} + q(n)s^n$ with $\deg q = e$, apply $(E - s)^{e+1}$, which kills $q(n)s^n$ by the argument above. Then $a$ satisfies the homogeneous recurrence with characteristic polynomial $\chi(x)(x - s)^{e+1}$, of order $d + e + 1$. If $s$ is a root of $\chi$ of multiplicity $m$, the term $s^n$ gets a polynomial factor of degree up to $m + e$; this is *resonance*. In practice, try a particular solution $n^m R(n) s^n$ with $\deg R = e$, and add the general homogeneous solution.

### Growth

If one root $r$ has the largest modulus, has multiplicity $m$, and its polynomial has a non-zero leading coefficient $\beta$, then $a_n \sim \beta\, n^{m-1} r^n$. The leading coefficient can vanish for special initial values; see Pitfalls.

## Classic examples

### Fibonacci

$F_n = F_{n-1} + F_{n-2}$, $F_0 = 0$, $F_1 = 1$: $\chi(x) = x^2 - x - 1$ with roots $\varphi = \frac{1+\sqrt5}2$ and $\psi = \frac{1-\sqrt5}2$. Fitting gives $F_n = (\varphi^n - \psi^n)/\sqrt5$, which is [Binet's formula](/binet-formula/).

### A double root

$a_n = 4a_{n-1} - 4a_{n-2}$, $a_0 = 1$, $a_1 = 4$: $\chi(x) = (x - 2)^2$, so $a_n = (\beta_0 + \beta_1 n)2^n$. From $a_0 = 1$, $\beta_0 = 1$; from $a_1 = 4$, $2(1 + \beta_1) = 4$, so $\beta_1 = 1$. Hence $a_n = (n + 1)2^n$: $1, 4, 12, 32, 80, \ldots$

### A triple root

$a_n = 6a_{n-1} - 12a_{n-2} + 8a_{n-3}$, $a_0 = 1$, $a_1 = 2$, $a_2 = 12$: $\chi(x) = (x - 2)^3$, so $a_n = (\beta_0 + \beta_1 n + \beta_2 n^2)2^n$. The equations $\beta_0 = 1$, $2(\beta_0 + \beta_1 + \beta_2) = 2$, $4(\beta_0 + 2\beta_1 + 4\beta_2) = 12$ give $\beta_1 = -1$, $\beta_2 = 1$, so $a_n = (n^2 - n + 1)2^n$.

### Three distinct roots

$a_n = 2a_{n-1} + a_{n-2} - 2a_{n-3}$, $a_0 = 3$, $a_1 = 2$, $a_2 = 6$: $\chi(x) = x^3 - 2x^2 - x + 2 = (x - 1)(x + 1)(x - 2)$. Fitting gives $a_n = 1 + (-1)^n + 2^n$.

### Complex roots

$a_n = 2a_{n-1} - 2a_{n-2}$, $a_0 = 0$, $a_1 = 1$: the roots are $1 \pm i = \sqrt2\, e^{\pm i\pi/4}$. The conjugate terms combine into $a_n = 2^{n/2}\sin(n\pi/4)$: $0, 1, 2, 2, 0, -4, -8, -8, 0, 16, \ldots$

$a_n = a_{n-1} - a_{n-2}$, $a_0 = 0$, $a_1 = 1$: the roots $e^{\pm i\pi/3}$ are sixth roots of unity, and $a_n = \frac{2}{\sqrt3}\sin(n\pi/3)$, which has period 6: $0, 1, 1, 0, -1, -1, \ldots$

### Non-homogeneous terms

- $a_n = 2a_{n-1} + 1$, $a_0 = 0$ (the [Tower of Hanoi](/tower-of-hanoi/)): the term $1 = 1^n$ adds the root 1, and $a_n = 2^n - 1$.
- $a_n = 2a_{n-1} + n$, $a_0 = 0$: the term $n \cdot 1^n$ adds $(x - 1)^2$, and $a_n = 2^{n+1} - n - 2$.
- $a_n = 2a_{n-1} + 2^n$, $a_0 = 0$: here $s = 2$ is already a root, so it resonates, and $a_n = n2^n$.

## Variations

- **Matrix form.** The vector $(a_n, \ldots, a_{n-d+1})$ is multiplied by the companion matrix of $\chi$ at each step. Its eigenvalues are the roots of $\chi$, and repeated roots give Jordan blocks of size $m_j$, which is where the factors $n^t$ come from; see [Jordan normal form](/jordan-normal-form/). With [matrix exponentiation](/matrix-exponentiation/), $a_n$ takes $O(d^3\log n)$ arithmetic operations, and polynomial arithmetic modulo $\chi$ reduces this further; see [the $n$-th term of a linear recurrence](/linear-recurrence-nth-term/).
- **Exact integer computation.** For integer coefficients, the matrix or polynomial method gives exact integers, while the closed form with irrational roots needs high precision.
- **Finding the recurrence.** From the first $2d$ terms of a sequence that satisfies an unknown recurrence of order at most $d$, the [Berlekamp-Massey](/berlekamp-massey/) algorithm finds the recurrence.
- **Generating functions directly.** Instead of roots, compute $P(z)/Q(z)$ and expand. This is also the route for systems of several linear recurrences.

## Pitfalls

- **Forgetting the factor $n$ for repeated roots.** For $\chi(x) = (x - 2)^2$, the trial solution $\beta_0 2^n + \beta_1 2^n$ has only one free constant and cannot fit two initial values.
- **A zero last coefficient.** For $a_n = 2a_{n-1} + 0 \cdot a_{n-2}$ with $a_0 = 5$, $a_1 = 1$, the values are $5, 1, 2, 4, 8, \ldots$. The characteristic polynomial $x^2 - 2x = x(x - 2)$ has the root 0, and the formula $a_n = \beta 2^n$ holds only from $n = 1$. Remove the zero coefficients and treat the first terms separately.
- **Assuming the dominant root shows.** $a_n = 3a_{n-1} - 2a_{n-2}$ with $a_0 = a_1 = 1$ is the constant 1, not $\Theta(2^n)$: the coefficient of $2^n$ is 0 for these initial values.
- **Applying the method to variable coefficients.** $a_n = n a_{n-1}$ is not covered; its solution $n!\,a_0$ is not of the form polynomial times exponential.
- **Floating point.** Evaluating $\varphi^n/\sqrt5$ in double precision gives wrong Fibonacci numbers from $n = 71$ on. Use integer methods for exact values.

## Exercises

1. Solve $a_n = 5a_{n-1} - 6a_{n-2}$, $a_0 = 0$, $a_1 = 1$. (Answer: $3^n - 2^n$.)
2. Solve $a_n = 2a_{n-1} - a_{n-2}$ with $a_0 = 3$, $a_1 = 5$. (Answer: $2n + 3$.)
3. Show that the number of tilings of a $2 \times n$ board by dominoes satisfies $t_n = t_{n-1} + t_{n-2}$, and that $t_n = F_{n+1}$.
4. Solve $a_n = 3a_{n-1} + 3^n$, $a_0 = 1$. (Answer: $(n + 1)3^n$.)
5. Prove that $\binom{n+t-1}{t-1}$ is a polynomial in $n$ of degree exactly $t - 1$, and use it to show that the basis sequences $n^t r^n$ may be replaced by $\binom{n+t}{t} r^n$.

## References
