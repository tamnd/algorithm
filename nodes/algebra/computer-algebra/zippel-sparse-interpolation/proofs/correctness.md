---
title: Zippel's algorithm interpolates correctly with high probability
proves: [correctness]
status: full
---

**Setting.** $K = \mathbb{Z}/p\mathbb{Z}$ with $p$ prime. The polynomial $f \in K[x_1, \ldots, x_n]$ has $t$ terms and degree at most $d$ in each variable, with $d < p - 1$. For $1 \le i \le n$, write
$$f = \sum_{m \in M_i} c_{i,m}(x_{i+1}, \ldots, x_n)\, m,$$
where $M_i$ is the set of monomials $m$ in $x_1, \ldots, x_i$ with $c_{i,m} \ne 0$. So $M_n$ is the support of $f$, $|M_i| \le t$, and every $m \in M_{i+1}$ has the form $m' x_{i+1}^e$ with $m' \in M_i$. The anchor $a_2, \ldots, a_n$ is chosen uniformly from $\{1, \ldots, p - 1\}$.

Let $A$ be the event that $c_{i,m}(a_{i+1}, \ldots, a_n) \ne 0$ for all $1 \le i \le n - 1$ and all $m \in M_i$.

**Theorem.** (a) The algorithm makes at most $(d + 1)(1 + (n - 1) t)$ probes and stops with probability $1$. (b) If $A$ holds, the output is $f$. (c) $\Pr[A] \ge 1 - n(n - 1) d t / \bigl(2(p - 1)\bigr)$.

## Lemma 1 (dense interpolation and the Vandermonde solve)

A polynomial in one variable of degree at most $d$ is determined by its values at $d + 1$ distinct points, and `interp_dense` returns its coefficients. If $v_1, \ldots, v_T$ are distinct, the system $\sum_m c_m v_m^k = w_k$, $0 \le k < T$, has exactly one solution, and `solve_vandermonde` returns it.

*Proof.* The first claim is Newton interpolation: the divided differences give the Newton form, and Horner's rule converts it to the monomial form, all in the field $K$. For the second, the matrix $(v_m^k)$ is a Vandermonde matrix with distinct nodes, so it is invertible. Let $\Lambda(z) = \prod_m (z - v_m)$ and $\Lambda_m(z) = \Lambda(z) / (z - v_m) = \sum_k \lambda_{m,k} z^k$. Then $\sum_k \lambda_{m,k} w_k = \sum_{m'} c_{m'} \Lambda_m(v_{m'}) = c_m \Lambda_m(v_m)$, since $\Lambda_m(v_{m'}) = 0$ for $m' \ne m$, and $\Lambda_m(v_m) = \prod_{m' \ne m} (v_m - v_{m'}) \ne 0$. This is the formula in the code, with $\Lambda_m$ computed by synthetic division. $\square$

## Lemma 2 (one stage)

Let $1 \le i \le n - 1$, and suppose the skeleton before step L4 is $M_i$, with the coefficient of $m$ equal to $c_{i,m}(a_{i+1}, \ldots, a_n)$. Then after step L7 the skeleton is $\{ m \in M_{i+1} : c_{i+1,m}(a_{i+2}, \ldots, a_n) \ne 0 \}$, with these values as coefficients. (For $i + 1 = n$, read $c_{n,m}$ as the coefficients of $f$, which are nonzero.)

*Proof.* Fix one of the values $b$ of step L5. The polynomial $g_b = f(x_1, \ldots, x_i, b, a_{i+2}, \ldots, a_n)$ equals $\sum_{m \in M_i} c_{i,m}(b, a_{i+2}, \ldots, a_n)\, m$, so its support is contained in $M_i$. This holds for every $b$, with no condition on the random choices. With $v_m = m(r_1, \ldots, r_i)$, the probe at $(r_1^k, \ldots, r_i^k)$ is $\sum_m c_{i,m}(b, \ldots)\, v_m^k$. Step L4 ensures that the $v_m$ are distinct, so by Lemma 1, step L6 returns $c_{i,m}(b, a_{i+2}, \ldots, a_n)$ for every $m \in M_i$. As a polynomial in $x_{i+1}$, $c_{i,m}(x_{i+1}, a_{i+2}, \ldots, a_n)$ has degree at most $d$, and the $d + 1$ values $b$ are distinct, so by Lemma 1 step L7 recovers it. Its coefficient of $x_{i+1}^e$ is $c_{i+1, m x_{i+1}^e}(a_{i+2}, \ldots, a_n)$, and this is $0$ when $m x_{i+1}^e \notin M_{i+1}$. Every element of $M_{i+1}$ has this form for some $m \in M_i$. So the new skeleton is as claimed. $\square$

## Proof of the theorem

(a) Step L2 makes $d + 1$ probes. For $i \ge 1$, the stage that adds $x_{i+1}$ makes $(d + 1)$ times the size of the skeleton probes, and by Lemma 2 the skeleton is a subset of $M_i$, so it has at most $t$ elements. This gives the bound. Step L4 probes nothing. Each trial there fails only if $m(r) = m'(r)$ for some distinct $m, m'$ in the skeleton. The polynomial $m - m'$ is nonzero of total degree at most $i d$, so by the Schwartz-Zippel lemma a trial fails with probability at most $\binom{T}{2} i d / (p - 1)$. If this is below $1$, the number of trials is finite with probability $1$ (a geometric number of trials). Otherwise, when $p$ is very small, distinctness can be impossible. The code assumes $p$ is large compared with $t^2 n d$.

(b) By Lemma 1, step L2 returns $f(x_1, a_2, \ldots, a_n) = \sum_{m \in M_1} c_{1,m}(a_2, \ldots, a_n)\, m$, and under $A$ all these coefficients are nonzero. So the skeleton is $M_1$ with the values that Lemma 2 needs. By induction with Lemma 2, under $A$ the skeleton after the stage for $x_{i+1}$ is $M_{i+1}$ with coefficients $c_{i+1,m}(a_{i+2}, \ldots, a_n)$. After the last stage it is $M_n$ with the coefficients of $f$. The early return for an empty skeleton is correct under $A$: an empty $M_1$ means $f = 0$.

(c) For each $i \le n - 1$ and $m \in M_i$, $c_{i,m}$ is a nonzero polynomial in $x_{i+1}, \ldots, x_n$ of total degree at most $(n - i) d$. By the Schwartz-Zippel lemma, with the anchor uniform on a set of $p - 1$ elements, $\Pr[c_{i,m}(a) = 0] \le (n - i) d / (p - 1)$. A union bound over at most $t$ monomials for each $i$ gives
$$\Pr[\text{not } A] \le \sum_{i=1}^{n-1} \frac{t (n - i) d}{p - 1} = \frac{n (n - 1) d t}{2 (p - 1)}. \qquad \blacksquare$$

**Remark.** Without $A$, the algorithm can lose a term and return a wrong polynomial without an error. One extra probe at a random point detects this with probability at least $1 - n d / (p - 1)$, by the Schwartz-Zippel lemma applied to the difference.
