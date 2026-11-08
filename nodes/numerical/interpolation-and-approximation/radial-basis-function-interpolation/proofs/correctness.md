---
title: The RBF system is nonsingular for conditionally positive definite kernels, and its solution interpolates and reproduces the tail
proves: [correctness, termination]
status: full
---

**Setting.** Distinct sites $x_1, \ldots, x_N \in \mathbb{R}^d$, values $y \in \mathbb{R}^N$, a radial function $\phi$, and a basis $p_1, \ldots, p_M$ of $\Pi_{m-1}$, the polynomials of total degree at most $m - 1$ on $\mathbb{R}^d$ ($M = 0$ when $m = 0$). $A_{ij} = \phi(\|x_i - x_j\|)$, $P_{ik} = p_k(x_i)$, and
$$K = \begin{pmatrix} A & P \\ P^T & 0 \end{pmatrix}.$$

**Definition.** $\phi$ is **conditionally positive definite of order $m$** on $\mathbb{R}^d$ if for every $N$, every set of distinct sites and every nonzero $c \in \mathbb{R}^N$ with $P^T c = 0$ (that is, $\sum_j c_j q(x_j) = 0$ for all $q \in \Pi_{m-1}$), the quadratic form $c^T A c$ is positive. Order 0 means positive definite with no side condition. The sites are **$\Pi_{m-1}$-unisolvent** if the only $q \in \Pi_{m-1}$ vanishing at all sites is $q = 0$, that is, $P$ has full column rank $M$.

**Facts used (cited, not proved here).** The Gaussian and the inverse multiquadric are positive definite on every $\mathbb{R}^d$ (Bochner's theorem, since their Fourier transforms are positive; Schoenberg 1938 for completely monotone functions of $r^2$). The multiquadric and $r$ are conditionally positive definite of order 1, and $r^2 \log r$ and $r^3$ of order 2, on every $\mathbb{R}^d$ (Micchelli 1986; Wendland 2005, Chapter 8). With the sign convention used by some authors, $-\phi$ is the conditionally positive definite function; the argument below is unchanged if $c^T A c$ is negative instead of positive for all admissible nonzero $c$.

**Lemma 1 (nonsingularity).** If $\phi$ is conditionally positive definite of order $m$ (or the negative of one) and the sites are distinct and $\Pi_{m-1}$-unisolvent, then $K$ is nonsingular.

*Proof.* Suppose $K (c, d) = 0$, that is, $Ac + Pd = 0$ and $P^T c = 0$. Multiply the first equation by $c^T$: $c^T A c + (P^T c)^T d = c^T A c = 0$. Since $P^T c = 0$, conditional definiteness forces $c = 0$. Then $Pd = 0$, and since $P$ has full column rank, $d = 0$. A square matrix with trivial kernel is nonsingular. $\square$

**Lemma 2 (interpolation).** If $(c, d)$ solves $K (c, d) = (y, 0)$, then $s(x) = \sum_j c_j \phi(\|x - x_j\|) + \sum_k d_k p_k(x)$ satisfies $s(x_i) = y_i$ for all $i$.

*Proof.* Row $i$ of the first block reads $\sum_j A_{ij} c_j + \sum_k P_{ik} d_k = y_i$, and the left side is $s(x_i)$. $\square$

**Lemma 3 (reproduction of the tail).** If $y_i = q(x_i)$ for some $q \in \Pi_{m-1}$, then $s = q$.

*Proof.* Write $q = \sum_k e_k p_k$. Then $(c, d) = (0, e)$ satisfies $A \cdot 0 + P e = y$ and $P^T \cdot 0 = 0$. By Lemma 1 the solution is unique, so the computed $(c, d)$ is $(0, e)$ and $s = q$. $\square$

**Theorem (correctness).** Under the hypotheses of Lemma 1, RBF-FIT returns the unique coefficients $(c, d)$ of an interpolant of the stated form with $P^T c = 0$, and RBF-EVAL returns its value; polynomials of degree at most $m - 1$ are reproduced exactly. If the hypotheses fail (repeated sites, or sites not unisolvent for the tail), $K$ may be singular, and the implementation reports this rather than returning a solution.

*Proof.* Lines L1 and L2 build $A$ and $P$ as defined, line L3 solves the nonsingular system (Lemma 1) by Gaussian elimination with partial pivoting, which in exact arithmetic finds the unique solution, and line L5 evaluates $s$. Lemmas 2 and 3 give interpolation and reproduction. The implementation rejects repeated sites before line L1 and raises an error if elimination meets a zero pivot column. $\square$

**Termination.** Lines L1 and L2 fill $N^2 + NM$ entries; Gaussian elimination on the $(N + M)$-square system performs $N + M$ pivot steps of finitely many operations and back substitution; line L5 is a single sum of $N + M$ terms. There are no loops with data-dependent bounds and no recursion. $\square$
