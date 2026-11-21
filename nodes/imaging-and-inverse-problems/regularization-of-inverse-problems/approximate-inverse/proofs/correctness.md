---
title: Correctness of the approximate inverse
proves: [correctness, termination]
status: full
---

Exact arithmetic. $A$ is a real $m \times n$ matrix, $\langle \cdot, \cdot\rangle$ is the Euclidean inner product, $e_1, \dots, e_r \in \mathbb{R}^n$ are the mollifiers, and $\beta \ge 0$. Lines L2 and L3 define the kernels by
$$(A A^\top + \beta I)\,\psi_i = A e_i, \qquad i = 1, \dots, r, \tag{1}$$
whenever $A A^\top + \beta I$ is invertible, and line L6 returns $\hat x_i = \langle y, \psi_i\rangle$.

**Lemma 1 (the system of line L3).** If $\beta > 0$, or if $\beta = 0$ and $A$ has rank $m$, then $A A^\top + \beta I$ is symmetric positive definite, so (1) has exactly one solution.

*Proof.* For $z \ne 0$, $z^\top (A A^\top + \beta I) z = \|A^\top z\|^2 + \beta\|z\|^2$. If $\beta > 0$ this is at least $\beta \|z\|^2 > 0$. If $\beta = 0$ and $A$ has rank $m$, then $A^\top$ is injective, so $\|A^\top z\| > 0$. A symmetric positive definite matrix is invertible. $\square$

**Theorem 1 (the kernel minimizes the adjoint residual).** Under the hypothesis of Lemma 1, $\psi_i$ is the unique minimizer of
$$G(\psi) = \|A^\top \psi - e_i\|^2 + \beta\|\psi\|^2 .$$

*Proof.* For every $g$,
$$G(\psi_i + g) = G(\psi_i) + 2\big\langle (A A^\top + \beta I)\psi_i - A e_i,\ g\big\rangle + \|A^\top g\|^2 + \beta\|g\|^2 .$$
By (1) the middle term is zero, and by Lemma 1 the last two terms sum to $g^\top (A A^\top + \beta I) g > 0$ for $g \ne 0$. So $G(\psi_i + g) > G(\psi_i)$ for every $g \ne 0$. $\square$

**Theorem 2 (exact recovery of mollified values).** (a) If $A^\top \psi = e$, then $\langle A x, \psi\rangle = \langle x, e\rangle$ for every $x \in \mathbb{R}^n$.

(b) If $e_i$ is in the range of $A^\top$ and the hypothesis of Lemma 1 holds with $\beta = 0$, then $A^\top \psi_i = e_i$. In particular this holds when $A$ is square and nonsingular, and then $\psi_i = A^{-\top} e_i$.

(c) In the case of (b), for exact data $y = A x$, line L6 returns $\hat x_i = \langle x, e_i\rangle$, the mollified value.

*Proof.* (a) $\langle A x, \psi\rangle = (A x)^\top \psi = x^\top A^\top \psi = \langle x, e\rangle$.

(b) If $e_i = A^\top z$ for some $z$, then $G(z) = 0$ with $\beta = 0$, so the minimum of $G$ is $0$. By Theorem 1 the unique minimizer is $\psi_i$, so $G(\psi_i) = 0$, which means $A^\top \psi_i = e_i$. If $A$ is square and nonsingular, the range of $A^\top$ is $\mathbb{R}^n$ and $A$ has rank $m = n$; then $A^\top \psi_i = e_i$ gives $\psi_i = A^{-\top} e_i$.

(c) Apply (a) with $\psi = \psi_i$ and $e = e_i$. $\square$

**Theorem 3 (error with inexact kernels and noisy data).** Let $y = A x$ and $\|y^\delta - y\| \le \delta$. Then
$$\big|\langle y^\delta, \psi_i\rangle - \langle x, e_i\rangle\big| \le \delta\,\|\psi_i\| + \|x\|\,\|A^\top \psi_i - e_i\|,$$
and the bound $\delta\|\psi_i\|$ on the noise part is attained by the noise $y^\delta - y = \delta\,\psi_i/\|\psi_i\|$ if $\psi_i \ne 0$.

*Proof.* Write $\langle y^\delta, \psi_i\rangle - \langle x, e_i\rangle = \langle y^\delta - y, \psi_i\rangle + \langle x, A^\top \psi_i - e_i\rangle$, using $\langle A x, \psi_i\rangle = \langle x, A^\top \psi_i\rangle$. Apply the Cauchy-Schwarz inequality to each term. For the given noise vector, $\langle y^\delta - y, \psi_i\rangle = \delta\|\psi_i\|$. $\square$

**Theorem 4 (invariance).** Let $S$ be an orthogonal $n \times n$ matrix, let $A$ be $n \times n$ with $A S = S A$, and let the hypothesis of Lemma 1 hold. If $\psi$ is the kernel of the mollifier $e$, then $S\psi$ is the kernel of the mollifier $S e$.

*Proof.* From $A S = S A$ and $S^{-1} = S^\top$ we get $S^\top A = A S^\top$, and by transposition $A^\top S = S A^\top$. So $S$ commutes with $A A^\top + \beta I$, and
$$(A A^\top + \beta I)\, S\psi = S\,(A A^\top + \beta I)\,\psi = S A e = A S e .$$
So $S\psi$ solves (1) for the mollifier $S e$, and by Lemma 1 it is the only solution. $\square$

For a circulant matrix $A$ and the cyclic shift $S$, Theorem 4 says that the kernels of all shifted mollifiers are shifts of one kernel, which is what the shift invariance test checks.

**Theorem 5 (termination).** Under the hypothesis of Lemma 1, the algorithm performs $r$ matrix-vector products at line L2, one factorization with $r$ solves at line L3, and $r$ inner products per data set at line L6, and then stops. Each step is well defined by Lemma 1.

*Proof.* Lines L2, L3 and L6 are loops of fixed length $r$, line L5 runs once for each of the finitely many data sets, and there are no other loops. $\square$
