---
tag: 8X0XMB
kind: definition
slug: continued-fraction-convergents
name: Convergents of a continued fraction
aliases:
- Convergents
area: number-theory/divisibility-and-gcd
level: core
summary: The rational fractions obtained by truncating a continued fraction, which give best rational approximations of the number.
prereqs: [continued-fraction, coprime-integers]
see_also: [rational-approximation, farey-sequence, stern-brocot-tree, pell-equation, extended-euclidean-algorithm, wiener-attack, fibonacci-numbers, continued-fraction-post-processing]
sources:
  - book: isbn:9780199219865
    title: G. H. Hardy and E. M. Wright, An Introduction to the Theory of Numbers, sixth edition
    locator: Chapter 10, Continued fractions (convergents, their recurrence and the determinant formula), and Chapter 11, Approximation of irrationals by rationals (Hurwitz's theorem)
  - book: isbn:9780486696300
    title: A. Ya. Khinchin, Continued Fractions, Dover edition
    locator: Chapter I (convergents and their properties) and Chapter II (best approximations and Legendre's criterion)
  - book: isbn:9780201558029
    title: Ronald L. Graham, Donald E. Knuth and Oren Patashnik, Concrete Mathematics, second edition
    locator: Section 6.7, Continuants
---

The convergents of a [continued fraction](/continued-fraction/) $x = [a_0; a_1, a_2, \ldots]$ are the fractions $p_n / q_n = [a_0; a_1, \ldots, a_n]$ obtained by cutting the expansion after $n + 1$ terms. They are always in lowest terms, they lie alternately below and above $x$, and their errors shrink like $1/q_n^2$. They are the best approximations of $x$: no fraction with a smaller denominator is as close in the sense $|qx - p|$, and every fraction closer than $1/(2q^2)$ to $x$ is a convergent. Computing them takes two multiply-adds per term, and it is the standard way to find a good fraction with a bounded denominator.

## Definition

Let $x = [a_0; a_1, a_2, \ldots]$ be a finite or infinite simple continued fraction, with $a_0 \in \mathbb{Z}$ and $a_i \ge 1$ for $i \ge 1$. The **$n$-th convergent** of $x$ is

$$c_n = [a_0; a_1, \ldots, a_n] = a_0 + \cfrac{1}{a_1 + \cfrac{1}{\ddots + \cfrac{1}{a_n}}},$$

for each $n \ge 0$ up to the length of the expansion. Its numerator and denominator are defined by the recurrence

$$p_n = a_n p_{n-1} + p_{n-2}, \qquad q_n = a_n q_{n-1} + q_{n-2}, \qquad n \ge 0,$$

with $p_{-2} = 0$, $p_{-1} = 1$, $q_{-2} = 1$, $q_{-1} = 0$. So $p_0 = a_0$, $q_0 = 1$, $p_1 = a_1 a_0 + 1$, $q_1 = a_1$. The following facts hold for every $n$ in range; they justify writing $c_n = p_n / q_n$.

**1. The recurrence gives the convergent.** For any real $t > 0$, $[a_0; a_1, \ldots, a_{n-1}, t] = (t p_{n-1} + p_{n-2}) / (t q_{n-1} + q_{n-2})$. *Proof.* By induction on $n$; for $n = 0$ it reads $t = t$. For the step, $[a_0; \ldots, a_n, t] = [a_0; \ldots, a_{n-1}, a_n + 1/t]$, and by the hypothesis this is $((a_n + 1/t) p_{n-1} + p_{n-2}) / ((a_n + 1/t) q_{n-1} + q_{n-2}) = (p_n + p_{n-1}/t)/(q_n + q_{n-1}/t)$, which is $(t p_n + p_{n-1})/(t q_n + q_{n-1})$. With $t = a_n$ this gives $c_n = p_n / q_n$. $\square$

**2. The determinant formula.** $p_n q_{n-1} - p_{n-1} q_n = (-1)^{n+1}$ for $n \ge -1$. *Proof.* For $n = -1$: $1 \cdot 1 - 0 \cdot 0 = 1$. Then $p_n q_{n-1} - p_{n-1} q_n = (a_n p_{n-1} + p_{n-2}) q_{n-1} - p_{n-1}(a_n q_{n-1} + q_{n-2}) = -(p_{n-1} q_{n-2} - p_{n-2} q_{n-1})$. $\square$ Consequences: $\gcd(p_n, q_n) = 1$, so each convergent is in lowest terms ([coprime integers](/coprime-integers/)), and $c_n - c_{n-1} = (-1)^{n+1} / (q_n q_{n-1})$ for $n \ge 1$.

**3. Order.** $c_0 < c_2 < c_4 < \cdots \le x \le \cdots < c_5 < c_3 < c_1$: the even convergents increase toward $x$ and the odd ones decrease toward it. This follows from $c_n - c_{n-2} = (-1)^n a_n / (q_n q_{n-2})$, a consequence of fact 2, and from fact 4.

**4. The error.** Let $x_{n+1} = [a_{n+1}; a_{n+2}, \ldots]$ be the complete quotient, so $x = [a_0; \ldots, a_n, x_{n+1}]$. By fact 1 and fact 2,

$$x - \frac{p_n}{q_n} = \frac{(-1)^n}{q_n (x_{n+1} q_n + q_{n-1})}.$$

Since $a_{n+1} \le x_{n+1} < a_{n+1} + 1$, this gives

$$\frac{1}{q_n (q_{n+1} + q_n)} < \left| x - \frac{p_n}{q_n} \right| \le \frac{1}{q_n q_{n+1}} \le \frac{1}{a_{n+1} q_n^2},$$

for each $n$ such that $a_{n+1}$ exists. The middle inequality is an equality only when $x$ is rational and $c_{n+1}$ is its last convergent. A large partial quotient $a_{n+1}$ means that $p_n / q_n$ is unusually good.

**5. Growth.** $q_n \ge F_{n+1}$, the Fibonacci number, because $q_n \ge q_{n-1} + q_{n-2}$ for $n \ge 1$. So $q_n \ge \varphi^{n-1}$, and the denominators grow at least exponentially. A convergent with denominator up to $Q$ is reached in $O(\log Q)$ terms.

**6. Best approximation (Lagrange).** If $p, q$ are integers with $0 < q < q_{n+1}$, then $|q x - p| \ge |q_n x - p_n|$. Call $p/q$ a *best approximation of the second kind* if every $p'/q' \ne p/q$ with $0 < q' \le q$ has $|q'x - p'| > |qx - p|$. Then every best approximation of the second kind is a convergent, and every convergent $p_n/q_n$ with $n \ge 1$ is one; the only exception at $n = 0$ is $x = a_0 + 1/2$, where $a_0$ and $a_0 + 1$ are equally close.

**7. Legendre's criterion.** If $q \ge 1$ and $|x - p/q| < 1/(2q^2)$, then $p/q$ is a convergent of $x$. Of two consecutive convergents at least one satisfies this inequality (Vahlen), and of three consecutive ones at least one satisfies $|x - p/q| < 1/(\sqrt 5 q^2)$ (Borel). So for irrational $x$ there are infinitely many fractions with $|x - p/q| < 1/(\sqrt 5 q^2)$; this is Hurwitz's theorem, and the constant $\sqrt 5$ cannot be raised, because of the golden ratio.

## Examples and non-examples

**$\pi$.** With $\pi = [3; 7, 15, 1, 292, 1, \ldots]$:

| $n$ | $a_n$ | $p_n / q_n$ | $|\pi - p_n/q_n|$ | $1/(2q_n^2)$ |
|---|---|---|---|---|
| 0 | 3 | $3/1$ | $1.4 \cdot 10^{-1}$ | $5.0 \cdot 10^{-1}$ |
| 1 | 7 | $22/7$ | $1.3 \cdot 10^{-3}$ | $1.0 \cdot 10^{-2}$ |
| 2 | 15 | $333/106$ | $8.3 \cdot 10^{-5}$ | $4.5 \cdot 10^{-5}$ |
| 3 | 1 | $355/113$ | $2.7 \cdot 10^{-7}$ | $3.9 \cdot 10^{-5}$ |
| 4 | 292 | $103993/33102$ | $5.8 \cdot 10^{-10}$ | $4.6 \cdot 10^{-10}$ |

The recurrence: $p_3 = 1 \cdot 333 + 22 = 355$, $q_3 = 1 \cdot 106 + 7 = 113$. The determinant formula: $355 \cdot 106 - 333 \cdot 113 = 37630 - 37629 = 1$. The fraction $355/113$ is within $3 \cdot 10^{-7}$ of $\pi$ because the next partial quotient is $292$. The convergents $333/106$ and $103993/33102$ are not within $1/(2q^2)$, so the converse of Legendre's criterion fails; their neighbours are, as Vahlen's result says.

**$\sqrt 2$.** With $\sqrt 2 = [1; 2, 2, \ldots]$, the convergents are $1/1, 3/2, 7/5, 17/12, 41/29, 99/70, \ldots$, and $p_n^2 - 2 q_n^2 = (-1)^{n+1}$: $3^2 - 2 \cdot 2^2 = 1$ and $7^2 - 2 \cdot 5^2 = -1$. These are the solutions of the [Pell equation](/pell-equation/) $x^2 - 2y^2 = \pm 1$.

**The golden ratio.** For $\varphi = [1; 1, 1, \ldots]$ the convergents are $F_{n+2}/F_{n+1}$, ratios of consecutive [Fibonacci numbers](/fibonacci-numbers/): $1, 2, 3/2, 5/3, 8/5, \ldots$. All partial quotients are $1$, the smallest possible, so the error $q_n^2 |\varphi - p_n/q_n|$ tends to $1/\sqrt 5$, the largest possible limit. This is why $\sqrt 5$ is the best constant in Hurwitz's theorem.

**A rational number.** $415/93 = [4; 2, 6, 7]$ has convergents $4/1$, $9/2$, $58/13$ and $415/93$. The last convergent is the number itself, and $415 \cdot 13 - 58 \cdot 93 = 5395 - 5394 = 1$.

**Non-example: a semiconvergent.** Fractions of the form $(p_{n-1} + k p_n)/(q_{n-1} + k q_n)$ with $0 < k < a_{n+1}$ lie between two convergents but are not convergents. For $\pi$, with $n = 1$ and $a_2 = 15$, these are $25/8, 47/15, \ldots, 311/99$. Some of them are closer to $\pi$ than every fraction with a smaller denominator, the *best approximations of the first kind*: $179/57$, $201/64$ and so on up to $311/99$ (those with $k \ge 8$), as well as $13/4$, $16/5$ and $19/6$ between $3/1$ and $22/7$. But none of them is a best approximation in the sense $|qx - p|$, which singles out the convergents.

**Non-example: a close fraction that is not a convergent.** $311/99$ is the fraction closest to $\pi$ among all fractions with denominator at most $105$, with error about $1.8 \cdot 10^{-4}$. It is not a convergent, so by Legendre's criterion its error must be at least $1/(2 \cdot 99^2) \approx 5.1 \cdot 10^{-5}$, and it is. Its value of $|99\pi - 311| \approx 0.0177$ is larger than $|7\pi - 22| \approx 0.0089$, so in the sense $|qx - p|$ it loses to the convergent $22/7$, whose denominator is smaller.

## Related definitions

- **Partial quotients and complete quotients.** The integers $a_n$, and the real numbers $x_n = [a_n; a_{n+1}, \ldots]$ with $x = [a_0; \ldots, a_{n-1}, x_n]$. See [continued fraction](/continued-fraction/).
- **Semiconvergent (intermediate fraction).** $(p_{n-1} + k p_n) / (q_{n-1} + k q_n)$ for $1 \le k \le a_{n+1}$; the case $k = a_{n+1}$ is the convergent $c_{n+1}$. The best approximations of the first kind are the convergents and some semiconvergents, those with $k > a_{n+1}/2$ and sometimes $k = a_{n+1}/2$.
- **Best approximations.** First kind: $|x - p/q|$ is smaller than for each fraction with a smaller denominator. Second kind: the same for $|qx - p|$. The second kind are exactly the convergents. See [rational approximation](/rational-approximation/).
- **Continuants.** The polynomials $K_n(a_0, \ldots, a_n)$ defined by the same recurrence, so that $p_n = K_{n+1}(a_0, \ldots, a_n)$ and $q_n = K_n(a_1, \ldots, a_n)$. They are sums over ways of deleting pairs of adjacent terms (Euler's rule).
- **Farey neighbours.** Fractions $a/b < c/d$ with $bc - ad = 1$. By the determinant formula, consecutive convergents are Farey neighbours, and each convergent appears in the [Farey sequence](/farey-sequence/) of its denominator next to the previous one. In the [Stern-Brocot tree](/stern-brocot-tree/), the nodes on the path from the root to $x$ are its convergents and semiconvergents.
- **Bézout coefficients.** For $x = a/b$, the convergents are the ratios $-t_i / s_i$ of the coefficients produced by the [extended Euclidean algorithm](/extended-euclidean-algorithm/).

## References
