---
title: Correctness of the companion matrix method
proves: [correctness, termination, convergence-rate]
status: full
---

Let $p(x) = a_0x^n + a_1x^{n-1} + \cdots + a_n$ with $a_0 \ne 0$ and $n \ge 1$, and let $C$ be its companion matrix, with first row $(-a_1/a_0, \dots, -a_n/a_0)$, ones on the subdiagonal and zeros elsewhere. Statements are in exact arithmetic unless they say otherwise.

## Lemma 1 (the characteristic polynomial)

$\det(zI - C) = p(z)/a_0$. Hence the eigenvalues of $C$, counted with algebraic multiplicity, are the roots of $p$ counted with multiplicity.

*Proof.* Write $c_j = a_j/a_0$ and $q_n(z) = \det(zI - C)$. Expand along the last column. The entry in position $(1, n)$ is $c_n$ and its minor is the determinant of an $(n-1) \times (n-1)$ upper triangular matrix with $-1$ on the diagonal, so it contributes $(-1)^{1+n}c_n(-1)^{n-1} = c_n$. The entry in position $(n, n)$ is $z$, and its minor is $\det(zI - C')$ where $C'$ is the companion matrix of $z^{n-1} + c_1z^{n-2} + \cdots + c_{n-1}$. So $q_n(z) = zq_{n-1}(z) + c_n$, with $q_1(z) = z + c_1$, and by induction $q_n(z) = z^n + c_1z^{n-1} + \cdots + c_n = p(z)/a_0$. $\square$

The vector $v(\lambda) = (\lambda^{n-1}, \dots, \lambda, 1)^T$ satisfies $Cv(\lambda) = \lambda v(\lambda)$ exactly when $p(\lambda) = 0$, which gives the geometric picture: every root has a one-dimensional eigenspace, so $C$ is nonderogatory and a multiple root is a single Jordan block.

## Lemma 2 (line L1)

If $a_n = \cdots = a_{n-t+1} = 0 \ne a_{n-t}$, then $p(x) = x^t\tilde p(x)$ with $\tilde p(0) = a_{n-t} \ne 0$. So recording $t$ roots at 0 and continuing with $\tilde p$ loses no root and adds none. Stripping leading zero coefficients only removes terms that are identically zero.

## Lemma 3 (similarities preserve the eigenvalues)

Line L3 replaces $C$ by $D^{-1}CD$ with $D$ diagonal and positive; each QR step of L8 replaces the active block $H$ by $RQ + \mu I = Q^*(H - \mu I)Q + \mu I = Q^*HQ$, where $Q$ is a product of Givens rotations and hence unitary. Similar matrices have the same characteristic polynomial, so neither step changes the eigenvalues. Both preserve the upper Hessenberg form: $D^{-1}CD$ has the same zero pattern as $C$, and for an upper Hessenberg $H - \mu I = QR$ computed by $n - 1$ Givens rotations on adjacent rows, $RQ$ is again upper Hessenberg.

In floating point, multiplying by powers of 2 is exact unless it overflows or underflows, so balancing introduces no rounding error. A QR step computed in floating point is the exact QR step of a matrix $H + E$ with $\|E\| \le c\,n\,u\|H\|$ for a modest constant $c$ (the backward stability of Givens rotations; Golub and Van Loan, Sections 5.1 and 7.4).

## Lemma 4 (deflation)

If $h_{l,l-1} = 0$ in an upper Hessenberg $H$, then $H$ is block upper triangular with diagonal blocks $H_{11}$ (rows and columns $1..l-1$) and $H_{22}$ (rows and columns $l..n$), and the eigenvalues of $H$ are those of $H_{11}$ together with those of $H_{22}$. When $H_{22}$ is $1 \times 1$ its entry is an eigenvalue, which is what L6 outputs.

*Proof.* $\det(zI - H) = \det(zI - H_{11})\det(zI - H_{22})$ for block triangular matrices. $\square$

Line L5 sets $h_{l,l-1}$ to zero when $|h_{l,l-1}| \le u(|h_{l-1,l-1}| + |h_{l,l}|)$. This is a perturbation of $H$ of norm at most $u\cdot 2\|H\|$, the same order as the rounding error of one QR step, so the computed eigenvalues are exact eigenvalues of a matrix within $O(u\|C\|)$ of the balanced companion matrix after all the steps (the errors add over the at most $nK$ steps, which gives the factor that the standard analysis bounds by a modest polynomial in $n$).

## Theorem 1 (correctness and termination)

Each pass of the loop L4 either outputs an eigenvalue and decreases $hi$ (L6), or performs one QR step and increases the step count of the current eigenvalue, returning "failed" at L9 once that count reaches $K$. So the loop stops after at most $n$ outputs and $nK$ QR steps. If it returns at L10, the $n$ outputs together with the zeros of L1 are, in exact arithmetic, exactly the eigenvalues of the deflated matrices, which by Lemmas 1 to 4 are the roots of $p$ with multiplicity whenever every deflated entry was exactly zero; in floating point they are the exact eigenvalues of a matrix $\tilde C$ with $\|\tilde C - D^{-1}CD\| = O(u\|D^{-1}CD\|)$. $\square$

## Convergence rate

The following local facts hold for the shifted QR iteration on an unreduced Hessenberg matrix (Golub and Van Loan, Section 7.5; Watkins, The Matrix Eigenvalue Problem, Chapter 4); they are cited, not proved here. If the shift $\mu_k$ approaches a simple eigenvalue $\lambda$ that is closer to it than all others, then $|h_{n,n-1}^{(k+1)}| = O(|h_{n,n-1}^{(k)}|^2)$, so the last subdiagonal entry tends to zero quadratically; with the Wilkinson shift on a symmetric matrix the rate is cubic. At an eigenvalue of multiplicity $m$, which for a companion matrix is a single Jordan block, convergence is only linear and the computed eigenvalues differ from the root by about $u^{1/m}\|C\|^{1/m}$, since a perturbation of size $\varepsilon$ of an $m \times m$ Jordan block moves its eigenvalue by about $\varepsilon^{1/m}$.

Global convergence of the QR iteration with Wilkinson shifts is not proved for general nonsymmetric matrices, and there are matrices on which unmodified shift strategies cycle. The exceptional shift every 10 steps is a heuristic that breaks such cycles in practice. So the statement made on the page is: termination is guaranteed by the cap, correctness of what is returned is guaranteed up to the backward error above, and the fact that the cap is essentially never reached is observed, in the tests on 500 random polynomials and on the special families, not proved.

## What is cited and not proved

The backward error bound of the computed QR steps, and the statement of Edelman and Murakami that the eigenvalue backward error of the balanced companion matrix corresponds to a small relative perturbation of the coefficients in most cases, are cited. The latter is not uniform: there are polynomials for which a backward stable eigenvalue computation on $C$ does not correspond to a small coefficientwise perturbation of $p$, and the page's statements about accuracy are made in terms of the matrix.
