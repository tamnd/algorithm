---
title: Correctness of Bairstow's method
proves: [correctness, termination, convergence-rate]
status: full
---

Let $p(x) = \sum_{k=0}^n a_kx^{n-k}$ be real with $a_0 \ne 0$ and $n \ge 3$. For real $(u, v)$ let $D(x) = x^2 - ux - v$ and let $b_k$, $c_k$ be the sequences of lines L2 and L4, with $b_{-1} = b_{-2} = c_{-1} = c_{-2} = 0$. Write $F(u, v) = (b_{n-1}, b_n)$. Statements are in exact arithmetic unless said otherwise.

## Lemma 1 (division identity)

$p(x) = D(x)\,q(x) + b_{n-1}(x - u) + b_n$ with $q(x) = \sum_{k=0}^{n-2} b_kx^{n-2-k}$.

*Proof.* Compare coefficients. For $0 \le k \le n - 2$ the coefficient of $x^{n-k}$ on the right is $b_k - ub_{k-1} - vb_{k-2}$, which is $a_k$ by the recurrence. The coefficient of $x$ is $-ub_{n-2} - vb_{n-3} + b_{n-1} = a_{n-1}$, and the constant term is $-vb_{n-2} - ub_{n-1} + b_n = a_n$. $\square$

So $D$ divides $p$ if and only if the remainder $b_{n-1}(x - u) + b_n$ is the zero polynomial, that is, $F(u, v) = 0$. Then $q$ is the quotient, which line L12 keeps.

## Lemma 2 (the Jacobian)

$\partial b_k/\partial u = c_{k-1}$ and $\partial b_k/\partial v = c_{k-2}$ for all $k$, so the Newton system for $F$ is the one solved at L5 and L6.

*Proof.* Differentiate $b_k = a_k + ub_{k-1} + vb_{k-2}$. With $d_k = \partial b_k/\partial u$ we get $d_k = b_{k-1} + ud_{k-1} + vd_{k-2}$ with $d_0 = d_{-1} = 0$. The sequence $c_{k-1}$ satisfies the same recurrence, $c_{k-1} = b_{k-1} + uc_{k-2} + vc_{k-3}$, with the same initial values, so $d_k = c_{k-1}$. In the same way $\partial b_k/\partial v = b_{k-2} + u\,\partial b_{k-1}/\partial v + v\,\partial b_{k-2}/\partial v$, which is the recurrence of $c_{k-2}$. $\square$

The Jacobian matrix is $\begin{pmatrix} c_{n-2} & c_{n-3} \\ c_{n-1} & c_{n-2}\end{pmatrix}$ with determinant $J = c_{n-2}^2 - c_{n-1}c_{n-3}$, and Cramer's rule gives the formulas of L6.

## Lemma 3 (when the Jacobian is nonsingular)

Let $D^* = x^2 - u^*x - v^*$ divide $p$, with $p = D^*q^*$. Then the Jacobian of $F$ at $(u^*, v^*)$ is nonsingular if and only if $\gcd(D^*, q^*) = 1$.

*Proof.* For a direction $(\delta u, \delta v)$ let $\delta D = -(\delta u\,x + \delta v)$, the change of $D$ to first order. Differentiate the identity of Lemma 1 along the direction at $(u^*, v^*)$, where $p = D^*q^*$ and the remainder $\rho = b_{n-1}(x - u) + b_n$ vanishes: $0 = \delta D\,q^* + D^*\,\delta q + \delta\rho$, where $\delta q$ and $\delta\rho$ are the first order changes of the quotient and of the remainder, and $\deg \delta\rho \le 1$. So $\delta\rho$ is the remainder of $-\delta D\,q^*$ modulo $D^*$. The Jacobian is singular iff some nonzero $\delta D$ of degree at most 1 gives $\delta\rho = 0$, that is, $D^*$ divides $\delta D\,q^*$. If $\gcd(D^*, q^*) = 1$ this forces $D^* \mid \delta D$, impossible for a nonzero polynomial of degree at most 1. If $\gcd(D^*, q^*) = g$ has degree 1 or 2, take $\delta D = D^*/g$ when $\deg g = 1$, or any nonzero constant when $\deg g = 2$; then $D^* \mid \delta D\,q^*$. The map $(\delta u, \delta v) \mapsto \delta\rho$ is the Jacobian (written in the basis $x - u^*$, $1$ of the remainders), so this proves the claim. $\square$

The condition fails exactly when a root of $D^*$ is also a root of $q^*$, that is, when a root of $D^*$ has multiplicity in $p$ larger than its multiplicity in $D^*$. A factor $D^* = (x - r)^2$ with $r$ of multiplicity exactly 2 satisfies it.

## Theorem 1 (local quadratic convergence)

If $D^* \mid p$ and $\gcd(D^*, q^*) = 1$, there is $\rho > 0$ such that from every $(u_0, v_0)$ within distance $\rho$ of $(u^*, v^*)$ the steps of FACTOR are defined, converge to $(u^*, v^*)$, and satisfy $e_{k+1} \le Ce_k^2$ for some constant $C$.

*Proof.* By Lemmas 1 and 2, L5 to L7 are exactly Newton's method on $F : \mathbb{R}^2 \to \mathbb{R}^2$. The map $F$ is polynomial in $(u, v)$, so its Jacobian is Lipschitz on bounded sets, and by Lemma 3 it is nonsingular at the zero $(u^*, v^*)$. The standard local convergence theorem for Newton's method in $\mathbb{R}^n$ (for example Dennis and Schnabel, Theorem 5.2.1, or the statement on the page [Newton's method for systems](/newton-method-for-systems/)) then gives a ball of quadratic convergence. If some step lands exactly on the factor, L3 returns "exact". $\square$

All norms on $\mathbb{R}^2$ are equivalent, so the measure $e_k = |u_k - u^*| + |v_k - v^*|$ only changes $C$.

## Theorem 2 (termination and output)

FACTOR stops after at most $K$ steps and $K + 1$ divisions. ROOTS stops after at most $(R + 1)$ FACTOR runs per factor and $\lfloor (n - 1)/2 \rfloor$ factors, so after at most $(R + 1)K(n - 1)/2$ steps, with output either "failed" or $n$ roots.

*Proof.* Each pass of the loop L1 returns or increases $k$, so the loop ends by L9. In ROOTS each successful factor replaces $a$ by the quotient of degree $n - 2$ (Lemma 1), so the degree falls by 2 each pass of L10 and the loop ends once the degree is at most 2; each factor search is retried at most $R$ times before ROOTS returns "failed". Each factor adds two roots at L11 and L13 adds the rest, so a successful run returns $\deg p$ roots. In exact arithmetic, when a factor search ends "exact", the two roots of L11 are roots of $p$ and the quotient carries the rest, so by induction the output is the multiset of roots of $p$. $\square$

## What is not proved

There is no global convergence theorem: from a given start the iteration may cycle, diverge or hit $J = 0$, and the restarts are a heuristic with a cap, not a guarantee. When FACTOR stops on the step test or the rounding floor, the factor is accepted only approximately, and the quotient carries a perturbation into the later factors; the size of the resulting errors is observed in the tests, not proved. The rounding floor $\gamma\mu_k$ follows the pattern of the running error bound for Horner's rule but is used here as a stopping heuristic.
