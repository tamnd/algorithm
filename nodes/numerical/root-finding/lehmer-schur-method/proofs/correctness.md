---
title: The Lehmer-Schur method keeps a disc that contains a zero and shrinks it by at least 33/64 per pass
proves: [correctness, termination, global-convergence]
status: full
---

Write $D(c, r)$ for the open disc, $\rho = \frac{13}{16}$, $\beta = \frac{7}{16}$, $\omega_j$ for the eight directions of the implementation, and $F = \{1, \frac{33}{32}, \frac{31}{32}, \frac{65}{64}, \frac{63}{64}\}$ for the radius factors tried by COUNT. All factors lie in $[\frac{31}{32}, \frac{33}{32}]$. The Schur-Cohn test is exact: when it returns a number, that number is the count of zeros in the open disc (see the [Schur-Cohn correctness proof](/schur-cohn-test/)).

## Lemma 1: the starting disc

Let $M = \max_{i < n} |a_i/a_n|$. Every zero $z$ of $p$ satisfies $|z| < 1 + M \le B$, so $D(0, B)$ contains all $n$ zeros.

*Proof.* If $|z| \ge 1 + M$, then $|z| > 1$ and
$$\Bigl|\frac{p(z)}{a_n z^n}\Bigr| \ge 1 - \sum_{i<n} M|z|^{i-n} > 1 - \frac{M}{|z| - 1} \ge 0,$$
so $p(z) \ne 0$. The implementation uses $|\operatorname{Re} x| + |\operatorname{Im} x| \ge |x|$ for $x = a_i/a_n$, so its $B$ is at least $1 + M$. $\square$

## Lemma 2: the covering

Let $z$ satisfy $\frac{31}{64}r \le |z - c| < r$. Then for some $j$, and for every $f \in [\frac{31}{32}, \frac{33}{32}]$, $|z - (c + \rho r\omega_j)| < \beta f r$.

*Proof.* Scale so that $c = 0$ and $r = 1$, and write $z = s e^{i\theta}$ with $\frac{31}{64} \le s < 1$. The directions have arguments exactly $k\pi/4$, because the diagonal ones have equal parts $\pm\frac{181}{256}$; their moduli are $1$ or $\frac{181}{256}\sqrt2 \in [0.99989, 1]$, so the centres $\rho\omega_j$ have modulus $\rho_j \in [0.8124, 0.8125]$. Choose $j$ with $|\theta - j\pi/4| \le \pi/8$. Then
$$|z - \rho_j e^{ij\pi/4}|^2 = s^2 + \rho_j^2 - 2s\rho_j\cos(\theta - j\pi/4) \le g(s) := s^2 + 0.8125^2 - 2s \cdot 0.8124 \cdot 0.9238,$$
using $\cos(\pi/8) > 0.9238$. The function $g$ is convex, so on $[\frac{31}{64}, 1]$ it is at most $\max(g(\frac{31}{64}), g(1)) < \max(0.16774, 0.1592) = 0.16774$. On the other hand $(\beta f)^2 \ge (\frac{7}{16} \cdot \frac{31}{32})^2 > 0.1796$. Hence $|z - \rho_j e^{ij\pi/4}| < \beta f$. $\square$

## Lemma 3: one pass keeps the invariant

Suppose that at the start of a pass $D(c, r)$ contains at least one zero and $\mathrm{count}$ is the number of zeros in it. If the pass does not return, the same holds at its end, with the new radius at most $\frac{33}{64}$ times the old one.

*Proof.* Line L4 tests $D(c, fr/2)$ for $f \in F$ in turn. If all are singular the pass returns. Otherwise let $r' = fr/2$ be the radius of the first regular test and $m$ its count.

If $m \ge 1$, the new disc $D(c, r')$ contains $m \ge 1$ zeros, exactly, and $r' \le \frac{33}{64}r$.

If $m = 0$, no zero lies in $D(c, r')$, and $r' \ge \frac{31}{64}r$. By the invariant some zero $z$ lies in $D(c, r)$, so $\frac{31}{64}r \le r' \le |z - c| < r$. By Lemma 2 there is a $j$ such that $z \in D(c_j, \beta f r)$ for every $f \in F$. Lines L5 and L6 test the discs in order. If one of them, possibly before reaching $j$, returns a regular count $m \ge 1$, the new disc contains exactly $m$ zeros and has radius $\beta f r \le \frac{7}{16} \cdot \frac{33}{32} r = \frac{231}{512} r < \frac{33}{64} r$. If none does, then in particular the disc $j$ gave no regular count with $m \ge 1$; since it contains $z$, a regular test there would have returned $m \ge 1$, so all five of its tests were singular, and the pass returns "failure" at L7. $\square$

## Theorem

(a) If the method returns "converged", then $D(c, r)$ with $r \le \delta$ contains exactly $\mathrm{count} \ge 1$ zeros of $p$; in particular some zero $z$ has $|z - c| < r \le \delta$.

(b) The method returns after at most $k_{\max}$ passes, and it returns "converged" after at most $\lceil \log(B/\delta)/\log(64/33) \rceil$ passes unless some test is singular for all five radii.

(c) "Failure" and "singular" are returned only when some test is singular for all five radii.

*Proof.* By Lemma 1 the invariant holds at the first pass, with $\mathrm{count} = n$. By Lemma 3 and induction it holds at the start of every pass, which gives (a) at line L3. After $k$ passes that do not return, $r \le B(33/64)^k$, which is at most $\delta$ once $k \ge \log(B/\delta)/\log(64/33)$; then line L3 returns, which gives (b) together with the bound $k_{\max}$ on the loop. Lemma 3 shows (c). $\square$

## Remark on the singular case

A test on $D(c', r'')$ is singular when $p(c' + r'' w)$ and its reciprocal have a common zero, for example a zero of $p$ on the circle, or when a constant term vanishes by accident. Five radii are tried; for all five to fail the polynomial must meet one of these conditions five times, which never happened in the tests. The proof does not rule it out, and the method then reports it instead of returning a wrong disc.
