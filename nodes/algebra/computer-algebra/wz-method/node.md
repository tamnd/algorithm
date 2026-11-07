---
tag: A78177
kind: technique
slug: wz-method
name: WZ method
aliases: [WZ pairs, Wilf-Zeilberger method, WZ pair, WZ certificate, Wilf-Zeilberger pair]
area: algebra/computer-algebra
level: advanced
summary: Proves hypergeometric identities by finding a WZ pair whose certificate gives the identity.
prereqs: [hypergeometric-term, gosper-algorithm]
see_also: [zeilberger-algorithm, creative-telescoping, gosper-algorithm, indefinite-summation, holonomic-function, binomial-coefficient, telescoping-sum]
sources:
  - paper: doi:10.1090/S0894-0347-1990-1007910-7
    title: Herbert S. Wilf and Doron Zeilberger, Rational functions certify combinatorial identities, Journal of the American Mathematical Society 3(1), 1990
    locator: pp. 147 to 158
  - paper: doi:10.1007/BF02100618
    title: Herbert S. Wilf and Doron Zeilberger, An algorithmic proof theory for hypergeometric (ordinary and q) multisum/integral identities, Inventiones Mathematicae 108, 1992
    locator: pp. 575 to 633
  - book: isbn:9781568810638
    title: Marko Petkovšek, Herbert S. Wilf and Doron Zeilberger, A = B, A K Peters, 1996
    locator: Chapter 7, The WZ Phenomenon (with Chapter 5 on Gosper's algorithm and Chapter 6 on Zeilberger's algorithm)
  - paper: doi:10.1073/pnas.75.1.40
    title: R. William Gosper, Decision procedure for indefinite hypergeometric summation, Proceedings of the National Academy of Sciences 75(1), 1978
    locator: pp. 40 to 42
  - paper: doi:10.1016/0012-365X(90)90120-7
    title: Doron Zeilberger, A fast algorithm for proving terminating hypergeometric identities, Discrete Mathematics 80(2), 1990
    locator: pp. 207 to 211
  - paper: doi:10.37236/1318
    title: Tewodros Amdeberhan and Doron Zeilberger, Hypergeometric series acceleration via the WZ method, Electronic Journal of Combinatorics 4(2), 1997
    locator: fast series for zeta(3) and other constants from WZ pairs
---

## In plain words

Many identities say that a sum of products of binomial coefficients or factorials has a simple closed form. The WZ method proves such an identity by a single check that a computer can do.

First divide the summand by the claimed answer, so that the identity says "the sum is always 1". Then look for a companion expression such that the change of each summand from one value of the outer index to the next is a difference of two neighboring values of the companion. If such a companion exists, the changes cancel in pairs when summed, so the sum does not change from one index to the next, and it is enough to check one starting case. The companion is the summand times a rational function. That rational function is the certificate: anyone can check the proof with only algebra on fractions, without knowing how it was found.

## When it applies

**Setting.** $K$ is a field of characteristic $0$, usually $\mathbb{Q}$ or $\mathbb{Q}(a, b, \ldots)$ for identities with parameters. A function $F(n, k)$ is a *hypergeometric term* in both variables if $F(n + 1, k) / F(n, k)$ and $F(n, k + 1) / F(n, k)$ are rational functions of $n$ and $k$ over $K$. The target is an identity

$$\sum_k f(n, k) = r(n), \qquad n \ge 0,$$

with $f$ hypergeometric and $r(n)$ nonzero and hypergeometric in $n$, where $k$ runs over all integers and $f(n, \cdot)$ has finite support or decays fast enough.

**WZ pairs.** Put $F(n, k) = f(n, k) / r(n)$, so the identity is $\sum_k F(n, k) = 1$. A *WZ pair* is a pair $(F, G)$ with

$$F(n + 1, k) - F(n, k) = G(n, k + 1) - G(n, k).$$

If $G(n, k) \to 0$ as $k \to \pm\infty$ for each $n$ (in particular, if $G(n, \cdot)$ has finite support), summing over $k$ gives $\sum_k F(n + 1, k) = \sum_k F(n, k)$, so the sum is constant in $n$. Checking $\sum_k F(0, k) = 1$ ends the proof.

**The certificate.** In every case found by the method, $G(n, k) = R(n, k) F(n, k)$ for a rational function $R$, the *WZ certificate*. Dividing the WZ equation by $F(n, k)$ gives

$$\frac{F(n + 1, k)}{F(n, k)} - 1 = R(n, k + 1) \frac{F(n, k + 1)}{F(n, k)} - R(n, k),$$

an identity between rational functions of $n$ and $k$. So the proof is checked by clearing denominators and comparing two polynomials, which is exact and finite.

**Finding $G$.** For fixed $n$, the term $t_k = F(n + 1, k) - F(n, k)$ is hypergeometric in $k$ over $K(n)$, since it is $F(n, k)$ times a rational function. [Gosper's algorithm](/gosper-algorithm/) decides whether $t_k$ has a hypergeometric antidifference $G(n, k)$ with $G(n, k + 1) - G(n, k) = t_k$, and returns it as $R \cdot F$. If it fails, no WZ pair exists for this normalization, and [Zeilberger's algorithm](/zeilberger-algorithm/) gives a recurrence of higher order instead. This is the case of order one of [creative telescoping](/creative-telescoping/).

**Cost model.** The proof check is a fixed number of operations on rational functions in $K(n, k)$. Gosper's algorithm needs a dispersion computation (integer roots of a resultant) and the solution of a linear system for a polynomial of bounded degree; its cost in operations in $K$ is polynomial in the degrees of the numerator and denominator of $F(n, k + 1) / F(n, k)$ and in the largest integer root found, which can be exponential in the input size. These are proved bounds of the usual kind for Gosper's algorithm, and in practice the WZ step is fast for identities in textbooks.

## The template

```pseudo id=main
WZ-PROVE(f, r)                                ▷ claim: Σ_k f(n, k) = r(n) for n ≥ 0
L1  F(n, k) ← f(n, k) / r(n)                   ▷ ⟨normalization: r(n) ≠ 0 for all n⟩
L2  t(k) ← F(n + 1, k) − F(n, k), a term in k over K(n)
L3  G ← GOSPER(t, k)                           ▷ G(n, k + 1) − G(n, k) = t(k), or fail
L4  if G = fail then return ⟨fallback: Zeilberger's algorithm⟩
L5  R ← G / F, a rational function of n and k   ▷ the certificate
L6  check the WZ equation divided by F as an identity in K(n, k)
L7  check ⟨boundary: G(n, k) → 0 as k → ±∞, with G written without removable poles⟩
L8  check ⟨initial value: Σ_k F(0, k) = 1⟩
L9  return R                                   ▷ the proof is R, with L6, L7 and L8
```

The holes are:

- **Normalization** (L1). If $r(n)$ vanishes for some $n$, divide by another term, or prove a shifted identity.
- **Fallback** (L4). Zeilberger's algorithm, or a change of normalization, such as moving a factor from $f$ to $r$.
- **Boundary** (L7). For finite sums this is natural boundaries: $G(n, k) = 0$ outside the support. The formula $R \cdot F$ can have a pole exactly where $F$ vanishes, so $G$ must be written as a single hypergeometric expression that is defined there, as in the second example below.
- **Initial value** (L8). A finite sum at $n = 0$, or a limit for infinite sums.

## Classic examples

- **Sum of a row of [binomial coefficients](/binomial-coefficient/).** $\sum_k \binom{n}{k} = 2^n$. Here $F(n, k) = \binom{n}{k} 2^{-n}$, and $G(n, k) = -\binom{n}{k - 1} 2^{-n-1}$, so $R(n, k) = \frac{k}{2(k - n - 1)}$. Check: $F(n + 1, k) - F(n, k) = \left(\binom{n + 1}{k} - 2\binom{n}{k}\right) 2^{-n-1} = \left(\binom{n}{k - 1} - \binom{n}{k}\right) 2^{-n-1}$, and this is $G(n, k + 1) - G(n, k)$ by Pascal's rule. At $n = 0$ the sum is $1$.
- **Sum of squares.** $\sum_k \binom{n}{k}^2 = \binom{2n}{n}$. With $F(n, k) = \binom{n}{k}^2 / \binom{2n}{n}$ the certificate is
  $$R(n, k) = -\frac{k^2 (3n - 2k + 3)}{2 (2n + 1) (n - k + 1)^2}, \qquad G(n, k) = -\frac{(3n - 2k + 3) \binom{n}{k - 1}^2}{2 (2n + 1) \binom{2n}{n}}.$$
  The second form is defined at $k = n + 1$, where $R$ has a pole and $F$ vanishes. For example, at $n = 2$, $k = 1$: $F(2, 1) = 2/3$, $G(2, 1) = -7/60$ and $F(3, 1) = 9/20$. A script checked the WZ equation exactly for $0 \le n < 12$ and all $k$ from $-2$ to $n + 3$.
- **Vandermonde's identity.** $\sum_k \binom{a}{k}\binom{b}{n - k} = \binom{a + b}{n}$, with the WZ variable $n$ and integer parameters $a$, $b$. The certificate is $R(n, k) = -\frac{k (b - n + k)}{(n + 1 - k)(a + b - n)}$; a script confirmed it for several pairs $(a, b)$.
- **Series acceleration.** Amdeberhan and Zeilberger (1997) sum the WZ equation in both directions to turn a slowly converging series $\sum_n F(n, 0)$ into a fast one, and so obtain fast series for $\zeta(3)$ of the kind used in Apéry's proof.
- **Creative telescoping.** When no WZ pair exists, [creative telescoping](/creative-telescoping/) finds a recurrence $\sum_{i=0}^{J} a_i(n) F(n + i, k) = G(n, k + 1) - G(n, k)$ of order $J > 1$, and the WZ method is the case $J = 1$ with $a_0 = -1$, $a_1 = 1$.

## Variations

- **Companion identities.** Summing the WZ equation over $n$ instead of $k$ gives $F(N, k) - F(0, k) = \sum_{n=0}^{N-1} \left(G(n, k + 1) - G(n, k)\right)$, and with limits this gives new identities from old pairs.
- **Dual pairs.** A change of variables in a WZ pair gives a WZ pair for a different identity. Wilf and Zeilberger (1990) show how one pair gives a family of identities this way, which is the "WZ phenomenon" of A = B, Chapter 7.
- **q-analogues.** The same method with $q$-hypergeometric terms, where ratios are rational in $q^n$ and $q^k$, and with the $q$-version of Gosper's algorithm.
- **Multisums and integrals.** Wilf and Zeilberger (1992) extend the method to multiple sums and to integrals, with certificates for each summation variable, and with existence proved for proper hypergeometric terms.
- **WZ pairs for integrals.** For $\int F(n, x)\, dx$, the pair satisfies $F(n + 1, x) - F(n, x) = \partial_x G(n, x)$, with $G$ found by a continuous analogue of Gosper's algorithm.

## Pitfalls

- **Poles of the certificate.** $R$ can have poles at points where $F$ is zero, as in the sum of squares at $k = n + 1$. Using $G = R F$ literally there is wrong; write $G$ as a hypergeometric term in its own right, or check boundary terms with the limit.
- **Boundary terms.** For infinite sums, the WZ equation proves the identity only if $G(n, k) \to 0$ at both ends. Without this, the sum can change with $n$.
- **The normalization matters.** Gosper's algorithm can fail for $F = f / r$ and succeed for another split of the same identity. A failure in L3 proves that no WZ pair exists for this $F$, not that the identity is false.
- **Zero right side.** For $\sum_k (-1)^k \binom{n}{k} = 0$ for $n \ge 1$, $r(n)$ is $0$, and L1 is not possible. Such identities are better proved by indefinite summation or by a recurrence.
- **Parameters.** With symbolic parameters such as $a$ and $b$, the check is over $K(a, b)$, and the certificate can have poles at special values of the parameters, such as $a + b = n$ in the Vandermonde certificate. Those values need separate checks.

## Exercises

1. Check the certificate $R(n, k) = k / (2(k - n - 1))$ for $\sum_k \binom{n}{k} = 2^n$ by verifying the rational form of the WZ equation in L6.
2. Verify that the two forms of $G$ in the sum of squares example agree for $0 \le k \le n$.
3. Show that $f(n, k) = (-1)^k \binom{n}{k}$ is Gosper-summable in $k$, with $\sum_{k \le m} (-1)^k \binom{n}{k} = (-1)^m \binom{n - 1}{m}$ for $n \ge 1$, and explain why this proves the identity of the fourth pitfall without a WZ pair.
4. Run Gosper's algorithm by hand on $t_k = F(n + 1, k) - F(n, k)$ for the Vandermonde identity and recover the certificate given above.
5. Prove that if $(F, G)$ is a WZ pair, then so is $(F + c\, \Delta_k H, \; G + c\, \Delta_n H)$ for any function $H(n, k)$, where $\Delta_k H(n, k) = H(n, k + 1) - H(n, k)$, $\Delta_n H(n, k) = H(n + 1, k) - H(n, k)$ and $c$ is a constant.

## References
