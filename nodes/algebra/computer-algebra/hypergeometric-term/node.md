---
tag: A5C9M5
kind: definition
slug: hypergeometric-term
name: Hypergeometric term
aliases:
- hypergeometric sequence
- closed-form term
area: algebra/computer-algebra
level: advanced
summary: A sequence whose consecutive ratio is a rational function of the index.
prereqs: [recurrence-relation, factorial]
see_also: [gosper-algorithm, petkovsek-hyper-algorithm, zeilberger-algorithm, indefinite-summation, definite-summation, holonomic-function, creative-telescoping, ore-algebra]
sources:
  - book: isbn:9781568810638
    title: Marko Petkovšek, Herbert S. Wilf and Doron Zeilberger, A = B, A K Peters, 1996
    locator: Chapter 3, The hypergeometric database (hypergeometric series and terms, and how to recognize them), Chapter 5 (Gosper's algorithm and the normal form of the ratio) and Chapter 8 (Hyper, hypergeometric solutions of recurrences)
  - book: isbn:9781107039032
    title: Joachim von zur Gathen and Jürgen Gerhard, Modern Computer Algebra, third edition, Cambridge University Press, 2013
    locator: Chapter 23, Symbolic summation (hypergeometric terms and Gosper's algorithm)
  - book: isbn:9780201558029
    title: Ronald L. Graham, Donald E. Knuth and Oren Patashnik, Concrete Mathematics, second edition, Addison-Wesley, 1994
    locator: Section 5.5, Hypergeometric functions, and Section 5.7, Partial hypergeometric sums
---

## Definition

Let $K$ be a field of characteristic $0$ and $k$ an integer variable. A sequence $t \colon \mathbb{N} \to K$ is a **hypergeometric term** if there is a rational function $r \in K(k)$ such that

$$t(k + 1) = r(k)\, t(k) \quad \text{for all } k \ge k_0,$$

for some $k_0$, and $t$ is not eventually zero. Clearing denominators, this says that $t$ satisfies a first-order linear recurrence with polynomial coefficients, $p(k)\, t(k + 1) = q(k)\, t(k)$ with $p, q \in K[k]$ nonzero. The rational function $r = q/p$ is the *ratio* of $t$. It is unique, because two ratios agree at infinitely many $k$.

Two hypergeometric terms $t_1, t_2$ are *similar* if $t_1/t_2$ is a rational function of $k$. A sum of similar terms is again hypergeometric, or zero. A sum of terms that are not similar is not, in general.

A function $F(n, k)$ of two integer variables is a *bivariate hypergeometric term* if both $F(n + 1, k)/F(n, k)$ and $F(n, k + 1)/F(n, k)$ are rational in $n$ and $k$. This is the setting of [definite summation](/definite-summation/) and [Zeilberger's algorithm](/zeilberger-algorithm/).

**Normal form of the ratio.** Every nonzero $r \in K(k)$ can be written as

$$r(k) = Z \, \frac{a(k)}{b(k)} \, \frac{c(k + 1)}{c(k)},$$

with $Z \in K$, monic $a, b, c \in K[k]$, $\gcd(a(k), b(k + h)) = 1$ for every integer $h \ge 0$, $\gcd(a(k), c(k)) = 1$ and $\gcd(b(k), c(k + 1)) = 1$. This is the Gosper-Petkovšek form (A = B, Chapter 5). The factor $c(k + 1)/c(k)$ is the ratio of the polynomial term $c(k)$, so the form separates a polynomial part of $t$ from its "factorial" part $a/b$. [Gosper's algorithm](/gosper-algorithm/) and [Hyper](/petkovsek-hyper-algorithm/) both start from it.

## Examples and non-examples

**Examples.** Each line gives $t(k)$ and its ratio $r(k)$.

| $t(k)$ | $r(k) = t(k + 1)/t(k)$ |
|---|---|
| $c^k$, for $c \ne 0$ | $c$ |
| $k!$ | $k + 1$ |
| $(-1)^k$ | $-1$ |
| a nonzero polynomial or rational function $s(k)$ | $s(k + 1)/s(k)$ |
| $\binom{n}{k}$, as a function of $k$ for fixed $n$ | $(n - k)/(k + 1)$ |
| Catalan numbers $C_k = \frac{1}{k + 1} \binom{2k}{k}$ | $2(2k + 1)/(k + 2)$ |
| $\Gamma(k + \alpha)$, for $\alpha \in K$ not a nonpositive integer | $k + \alpha$ |
| the terms of ${}_pF_q(a_1, \ldots, a_p; b_1, \ldots, b_q; x)$ | $\dfrac{(k + a_1) \cdots (k + a_p)}{(k + b_1) \cdots (k + b_q)} \dfrac{x}{k + 1}$ |

The last line explains the name: a hypergeometric series is a power series whose coefficient sequence is a hypergeometric term. Every hypergeometric term is, up to a constant and finitely many initial values, a product of terms of the forms $c^k$, $\Gamma(k + \alpha)$ and $1/\Gamma(k + \beta)$ over a splitting field of the numerator and denominator of $r$.

Products, quotients and shifts $t(k + m)$ of hypergeometric terms are hypergeometric. So is $t(mk)$ for an integer $m \ge 1$.

**Non-examples.**

- **Fibonacci numbers.** $F_{k+1}/F_k = \varphi + O\bigl((\psi/\varphi)^k\bigr)$, where $\varphi = (1 + \sqrt{5})/2$ and $\psi = (1 - \sqrt{5})/2$. A rational function that is not constant differs from its limit by a quantity of order $1/k^m$ for some $m \ge 1$, never by an exponentially small one. And the ratio is not the constant $\varphi$, since $F_2 / F_1 = 1$. So the Fibonacci sequence is not hypergeometric over any field. It satisfies a second-order recurrence, so it is [holonomic](/holonomic-function/).
- **Harmonic numbers.** $H_{k+1}/H_k = 1 + \frac{1}{(k + 1) H_k}$. If this were rational in $k$, then $H_k$ would be rational in $k$, which it is not ([indefinite summation](/indefinite-summation/) gives the proof).
- **$2^{k^2}$.** Its ratio $2^{2k + 1}$ is not a rational function of $k$.
- **$2^k + 1$.** Its ratio $(2^{k+1} + 1)/(2^k + 1)$ tends to $2$ exponentially fast and is not constant, so by the argument for Fibonacci it is not rational. This sum of the dissimilar terms $2^k$ and $1$ is not hypergeometric.
- **$\sin k$** or $\cos k$, viewed as sequences over $\mathbb{C}$, are sums of the dissimilar terms $e^{\pm ik}$ and are not hypergeometric, though they are holonomic.

## Related definitions

- **Holonomic (P-recursive) sequence.** A sequence that satisfies a linear recurrence of some order $r$ with polynomial coefficients. Hypergeometric terms are exactly the holonomic sequences of order $1$. See [holonomic function](/holonomic-function/).
- **Hypergeometric solutions of recurrences.** [Petkovšek's algorithm Hyper](/petkovsek-hyper-algorithm/) finds all hypergeometric terms that satisfy a given linear recurrence with polynomial coefficients. In operator language, these are the right factors of order $1$ of a recurrence operator in an [Ore algebra](/ore-algebra/).
- **Gosper-summable term.** A hypergeometric term $t$ whose [indefinite sum](/indefinite-summation/) is again hypergeometric, $\Delta T = t$. Then $T = R\, t$ for a rational $R$, and [Gosper's algorithm](/gosper-algorithm/) decides whether such an $R$ exists.
- **Proper hypergeometric term.** A bivariate term of the form $P(n, k) \, \frac{\prod_i (a_i n + b_i k + c_i)!}{\prod_j (u_j n + v_j k + w_j)!} x^k$ with a polynomial $P$ and integers $a_i, b_i, u_j, v_j$. For these, [creative telescoping](/creative-telescoping/) is guaranteed to find a recurrence for the definite sum (A = B, Chapter 4).
- **q-hypergeometric term.** The ratio is a rational function of $q^k$ instead of $k$.

## References
