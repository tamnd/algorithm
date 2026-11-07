---
title: The Schur-Cohn test returns the exact number of zeros in the disc, or reports a singular step, after at most n passes
proves: [correctness, termination]
status: full
---

Write $\mathbb{D} = \{|z| < 1\}$, $\mathbb{T} = \{|z| = 1\}$, and $k(p)$ for the number of zeros of $p$ in $\mathbb{D}$, counted with multiplicity. For $p$ of exact degree $n$ with $a_n \ne 0$, let $p^*(z) = z^n\,\overline{p(1/\bar z)} = \sum_{i=0}^n \overline{a_{n-i}}\,z^i$ and $Tp = \overline{a_0}\,p - a_n\,p^*$. The arithmetic is exact.

## Lemma 1: the reciprocal polynomial

(a) $|p^*(z)| = |p(z)|$ for $z \in \mathbb{T}$. (b) $p^*(0) = \overline{a_n} \ne 0$, and for $z \ne 0$, $p^*(z) = 0$ if and only if $p(1/\bar z) = 0$, with the same multiplicity. (c) If $p$ has no zeros on $\mathbb{T}$, then $k(p^*) = n - k(p)$.

*Proof.* (a) On $\mathbb{T}$, $1/\bar z = z$ and $|z^n| = 1$. (b) The first claim is the constant coefficient. For $z \ne 0$, $z^n \ne 0$, and $w \mapsto 1/\bar w$ is an anti-holomorphic bijection of $\mathbb{C} \setminus \{0\}$; writing $p(w) = (w - \zeta)^m g(w)$ with $g(\zeta) \ne 0$ gives $p^*(z) = z^n\,\overline{(1/\bar z - \zeta)^m}\,\overline{g(1/\bar z)} = (1 - \bar\zeta z)^m z^{n-m}\,\overline{g(1/\bar z)}$, which has a zero of multiplicity exactly $m$ at $z = 1/\bar\zeta$. (c) By (b), the zeros of $p^*$ in $\mathbb{D}$ are the images under $w \mapsto 1/\bar w$ of the nonzero zeros of $p$ with $|w| > 1$. Since $p$ has no zeros on $\mathbb{T}$, those are all zeros of $p$ outside $\overline{\mathbb{D}}$, of total multiplicity $n - k(p)$ (zeros at $0$ are inside, and are not images of anything). $\square$

## Lemma 2: one transform

Let $p$ have exact degree $n \ge 1$ and no zeros on $\mathbb{T}$, and let $\delta = Tp(0) = |a_0|^2 - |a_n|^2$.

(a) $\deg Tp \le n - 1$.

(b) If $\delta \ne 0$, then $Tp$ has no zeros on $\mathbb{T}$, is not the zero polynomial, and $k(Tp) = k(p)$ if $\delta > 0$, $k(Tp) = n - k(p)$ if $\delta < 0$.

*Proof.* (a) The coefficient of $z^n$ in $Tp$ is $\overline{a_0}a_n - a_n\overline{a_0} = 0$. The constant term is $\overline{a_0}a_0 - a_n\overline{a_n} = \delta$.

(b) On $\mathbb{T}$, by Lemma 1(a), $|\overline{a_0}p(z)| = |a_0||p(z)|$ and $|a_n p^*(z)| = |a_n||p(z)|$, and $|p(z)| > 0$. If $\delta > 0$, then $|a_0| > |a_n|$, so $|a_n p^*| < |\overline{a_0} p|$ on $\mathbb{T}$. Hence $|Tp| \ge (|a_0| - |a_n|)|p| > 0$ on $\mathbb{T}$, and by Rouché's theorem $Tp$ and $\overline{a_0}p$ have the same number of zeros in $\mathbb{D}$, which is $k(p)$ since $a_0 \ne 0$. If $\delta < 0$, the roles swap: $|\overline{a_0}p| < |a_n p^*|$ on $\mathbb{T}$, $Tp$ has no zeros on $\mathbb{T}$, and $k(Tp) = k(-a_n p^*) = k(p^*) = n - k(p)$ by Lemma 1(c). $\square$

## Lemma 3: singular cases

If $p$ and $p^*$ have a common zero $\zeta$, then every polynomial $p_j$ computed by the algorithm vanishes at $\zeta$, and the algorithm returns "singular". This includes a zero $\zeta \in \mathbb{T}$, since then $p^*(\zeta) = \zeta^n\overline{p(\zeta)} = 0$, and a pair of zeros $\zeta$, $1/\bar\zeta$, by Lemma 1(b).

*Proof.* If $p(\zeta) = p^*(\zeta) = 0$, then $Tp(\zeta) = 0$, and if $\zeta \ne 0$ also $(Tp)^*(\zeta) = 0$: indeed $(Tp)^*$ is, up to a power of $z$ coming from the degree drop, $a_0\,p^* - \overline{a_n}\,p$, which vanishes at $\zeta$. (If $\zeta = 0$ then $p^*(0) = \overline{a_n} \ne 0$, so $\zeta \ne 0$.) Dividing by a positive rational in line L7 does not change zeros. By induction every $p_j$ and $p_j^*$ vanish at $\zeta$, as long as the algorithm runs. If no step were singular, the loop would end with a nonzero constant $p_J$, which does not vanish at $\zeta$: a contradiction. So some $\delta_{j+1}$ is $0$, or some $p_{j+1}$ is the zero polynomial, which also has $\delta_{j+1} = 0$, and line L6 returns "singular". $\square$

## Theorem

The algorithm stops after at most $n$ passes. If it returns $(k, \text{"count"})$, then $p$ has no zeros on $\mathbb{T}$ and $k(p) = k$.

*Proof.* Termination: by Lemma 2(a), $\deg p_{j+1} < \deg p_j$, and line L7 only removes leading zeros, so the loop runs at most $n$ times.

Correctness: suppose the algorithm returns a count, with polynomials $p_0, \ldots, p_J$, $p_J$ a nonzero constant and all $\delta_1, \ldots, \delta_J \ne 0$. If $p_0$ had a zero on $\mathbb{T}$, Lemma 3 would give "singular", so it has none. By Lemma 2(b) and induction on $j$, no $p_j$ has a zero on $\mathbb{T}$, and
$$k(p_j) = k(p_{j+1}) \text{ if } \delta_{j+1} > 0, \qquad k(p_j) = n_j - k(p_{j+1}) \text{ if } \delta_{j+1} < 0,$$
where the division in line L7 by a positive rational changes neither the zeros of $p_{j+1}$ nor the sign of $\delta_{j+2}$, since $\delta_{j+2}$ is homogeneous of degree 2 in the coefficients of $p_{j+1}$. Since $k(p_J) = 0$, line L9 computes exactly $k(p_{J-1}), \ldots, k(p_0)$ by this recursion. $\square$

## Disc of centre c and radius r

The map $w \mapsto c + rw$ is a bijection from $\mathbb{D}$ onto $\{|z - c| < r\}$ and from $\mathbb{T}$ onto the boundary circle, and it preserves multiplicities. So the zeros of $q(w) = p(c + rw)$ in $\mathbb{D}$ correspond one to one to the zeros of $p$ in the disc, and the theorem applies to $q$, which the implementation computes exactly by a Taylor shift and a scaling.
