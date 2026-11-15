---
title: The regulator equations decide the linear output regulation problem
proves: [statement]
status: full
---

This file proves the three parts of the statement: the full information case, the error feedback case, and the rank condition for solvability for all $P$ and $Q$. It uses only linear algebra and the solution formula of linear differential equations. The argument follows Francis (1977); the rank condition is proved here with a Schur form of $S$.

## Setting

The plant and the exosystem are

$$\dot x = A x + B u + P w, \qquad \dot w = S w, \qquad e = C x + Q w,$$

with $x \in \mathbb{R}^n$, $u \in \mathbb{R}^m$, $w \in \mathbb{R}^q$, $e \in \mathbb{R}^p$. The hypotheses are:

- (H1) every eigenvalue of $S$ has real part $\ge 0$;
- (H2) $(A, B)$ is stabilizable;
- (H3) the pair $(C_a, A_a)$ with $C_a = \begin{bmatrix} C & Q \end{bmatrix}$ and $A_a = \begin{bmatrix} A & P \\ 0 & S \end{bmatrix}$ is detectable.

The regulator equations are

$$\Pi S = A \Pi + B \Gamma + P, \qquad 0 = C \Pi + Q. \tag{RE}$$

## Two lemmas

**Lemma 1.** Let $S \in \mathbb{R}^{q \times q}$ satisfy (H1) and let $M$ be a complex matrix with $q$ columns. If $M e^{St} w_0 \to 0$ as $t \to \infty$ for every $w_0 \in \mathbb{R}^q$, then $M = 0$.

*Proof.* The limit is linear in $w_0$, so it holds for every complex $w_0$ too, because a complex vector is $a + ib$ with real $a$ and $b$. Let $\lambda$ be an eigenvalue of $S$ and let $v_1, \dots, v_k$ be a Jordan chain: $(S - \lambda I) v_1 = 0$ and $(S - \lambda I) v_j = v_{j-1}$ for $j \ge 2$. Then

$$e^{St} v_j = e^{\lambda t} \sum_{i=0}^{j-1} \frac{t^i}{i!} v_{j-i}.$$

We show $M v_j = 0$ by induction on $j$. If $M v_i = 0$ for all $i < j$, then $M e^{St} v_j = e^{\lambda t} M v_j$. Since $\operatorname{Re} \lambda \ge 0$, $|e^{\lambda t}| \ge 1$, so this tends to 0 only if $M v_j = 0$. The case $j = 1$ is the same argument with no earlier terms. The Jordan chains of all eigenvalues form a basis of $\mathbb{C}^q$, so $M = 0$. $\square$

**Lemma 2.** Let $A_c$ be Hurwitz and let $S$ satisfy (H1). Then for every matrix $R$ of the right size the equation $X S = A_c X + R$ has exactly one solution $X$.

*Proof.* The eigenvalues of $A_c$ have negative real part and those of $S$ have nonnegative real part, so the two spectra are disjoint. The Sylvester equation $A_c X - X S = -R$ then has a unique solution (see the Sylvester equation page: the map $X \mapsto A_c X - X S$ has eigenvalues $\alpha - \sigma$ for $\alpha \in \sigma(A_c)$, $\sigma \in \sigma(S)$, none of them zero). $\square$

## Part 1: full information

**Claim.** Under (H1) and (H2) there are $K$ and $L$ such that $A - BK$ is Hurwitz and $u = -Kx + Lw$ gives $e(t) \to 0$ for all initial states if and only if (RE) has a solution. If $(\Pi, \Gamma)$ solves (RE), then every $K$ with $A - BK$ Hurwitz and $L = \Gamma + K \Pi$ work.

*Sufficiency.* Let $(\Pi, \Gamma)$ solve (RE). By (H2) there is $K$ with $A - BK$ Hurwitz. Set $L = \Gamma + K\Pi$ and $z = x - \Pi w$. Then

$$\dot z = A x - BKx + B\Gamma w + BK\Pi w + P w - \Pi S w = (A - BK) x - (A - BK)\Pi w = (A - BK) z,$$

where the middle step uses $\Pi S = A\Pi + B\Gamma + P$. So $z(t) \to 0$. Also $e = C z + (C\Pi + Q) w = C z \to 0$.

*Necessity.* Let $K$, $L$ work and set $A_c = A - BK$, which is Hurwitz. The closed loop is $\dot x = A_c x + (BL + P) w$. By Lemma 2 there is $\Pi$ with $\Pi S = A_c \Pi + BL + P$. Let $\delta = x - \Pi w$. Then $\dot \delta = A_c x + (BL + P) w - \Pi S w = A_c \delta$, so $\delta \to 0$ for every initial state. Now $e = C\delta + (C\Pi + Q) e^{St} w(0)$, and $e \to 0$, so $(C\Pi + Q) e^{St} w(0) \to 0$ for every $w(0)$. By Lemma 1, $C \Pi + Q = 0$. Set $\Gamma = L - K\Pi$. Then $A\Pi + B\Gamma + P = A_c \Pi + BL + P = \Pi S$. So $(\Pi, \Gamma)$ solves (RE). $\square$

## Part 2: error feedback

**Claim.** Under (H1), (H2) and (H3) there is a controller $\dot\xi = F\xi + Ge$, $u = H\xi$ that makes $\begin{bmatrix} A & BH \\ GC & F \end{bmatrix}$ Hurwitz and gives $e(t) \to 0$ for all initial states if and only if (RE) has a solution.

*Sufficiency.* Let $(\Pi, \Gamma)$ solve (RE), and let $K$, $L$ be as in Part 1. By (H3) there is $G_a$ with $A_a - G_a C_a$ Hurwitz. Let $B_a = \begin{bmatrix} B \\ 0 \end{bmatrix}$ and use the observer

$$\dot \xi = A_a \xi + B_a u + G_a (e - C_a \xi), \qquad u = \begin{bmatrix} -K & L \end{bmatrix} \xi,$$

which has the required form with $F = A_a + B_a \begin{bmatrix} -K & L \end{bmatrix} - G_a C_a$, $G = G_a$ and $H = \begin{bmatrix} -K & L \end{bmatrix}$. Let $\varepsilon = (x, w) - \xi$. The plant and exosystem together satisfy $\frac{d}{dt}(x, w) = A_a (x, w) + B_a u$ and $e = C_a (x, w)$, so $\dot \varepsilon = (A_a - G_a C_a) \varepsilon$ and $\varepsilon \to 0$. The input is $u = -Kx + Lw + \begin{bmatrix} K & -L \end{bmatrix} \varepsilon$. With $z = x - \Pi w$ the computation of Part 1 gives $\dot z = (A - BK) z + B \begin{bmatrix} K & -L \end{bmatrix} \varepsilon$. This is a Hurwitz system driven by an input that decays exponentially, so $z \to 0$, and $e = C z \to 0$. For internal stability set $w = 0$. Then the map from $(x, \xi)$ to $(x, \varepsilon)$ is invertible, and in the new coordinates the closed-loop matrix is

$$\begin{bmatrix} A - BK & B \begin{bmatrix} K & -L \end{bmatrix} \\ 0 & A_a - G_a C_a \end{bmatrix},$$

which is block triangular with Hurwitz diagonal blocks. Similar matrices have the same eigenvalues, so the closed loop is internally stable.

*Necessity.* Let $(F, G, H)$ work, with $\xi \in \mathbb{R}^{k}$. Put $X = (x, \xi)$. The closed loop is $\dot X = A_{cl} X + P_{cl} w$ and $e = C_{cl} X + Q w$, with

$$A_{cl} = \begin{bmatrix} A & BH \\ GC & F \end{bmatrix}, \quad P_{cl} = \begin{bmatrix} P \\ GQ \end{bmatrix}, \quad C_{cl} = \begin{bmatrix} C & 0 \end{bmatrix}.$$

$A_{cl}$ is Hurwitz. By Lemma 2 there is $\Pi_{cl}$ with $\Pi_{cl} S = A_{cl} \Pi_{cl} + P_{cl}$. As in Part 1, $\delta = X - \Pi_{cl} w$ satisfies $\dot\delta = A_{cl}\delta$, and $e = C_{cl}\delta + (C_{cl}\Pi_{cl} + Q) w$, so Lemma 1 gives $C_{cl} \Pi_{cl} + Q = 0$. Write $\Pi_{cl} = \begin{bmatrix} \Pi \\ \Sigma \end{bmatrix}$ with $\Pi$ of size $n \times q$. The first block row of $\Pi_{cl} S = A_{cl}\Pi_{cl} + P_{cl}$ is $\Pi S = A\Pi + BH\Sigma + P$, and $C_{cl}\Pi_{cl} + Q = C\Pi + Q = 0$. So $(\Pi, H\Sigma)$ solves (RE). $\square$

The matrix $\Sigma$ is the steady state of the controller. The relation $\Gamma = H\Sigma$ says that the controller generates the steady-state input from its own state, which is the content of the internal model principle.

## Part 3: the rank condition

**Claim.** (RE) has a solution for every $P \in \mathbb{R}^{n \times q}$ and $Q \in \mathbb{R}^{p \times q}$ if and only if

$$\operatorname{rank} \begin{bmatrix} A - \lambda I & B \\ C & 0 \end{bmatrix} = n + p \quad \text{for every eigenvalue } \lambda \text{ of } S.$$

If moreover $m = p$, the solution is unique.

*Reformulation.* Put the unknowns in $X = \begin{bmatrix} \Pi \\ \Gamma \end{bmatrix} \in \mathbb{R}^{(n+m) \times q}$, and let

$$L = \begin{bmatrix} A & B \\ C & 0 \end{bmatrix}, \qquad E = \begin{bmatrix} I_n & 0 \\ 0 & 0 \end{bmatrix}, \qquad R = -\begin{bmatrix} P \\ Q \end{bmatrix},$$

with $L$ and $E$ of size $(n + p) \times (n + m)$. Then (RE) is $\mathcal{T}(X) = R$ for the linear map $\mathcal{T}(X) = L X - E X S$. The matrix $L - \lambda E$ is the matrix of the claim. Since $L$, $E$ and $S$ are real, $\mathcal{T}$ maps real matrices to real matrices, and $\mathcal{T}(\operatorname{Re} X) = \operatorname{Re} \mathcal{T}(X)$ for complex $X$. So $\mathcal{T}$ is onto the real matrices exactly when it is onto the complex ones.

*Necessity.* Suppose $L - \lambda E$ has rank below $n + p$ for an eigenvalue $\lambda$ of $S$. Take a nonzero row vector $y$ with $y (L - \lambda E) = 0$ and a nonzero column vector $v$ with $S v = \lambda v$. For every $X$,

$$y\, \mathcal{T}(X)\, v = y L X v - y E X S v = \lambda\, y E X v - \lambda\, y E X v = 0.$$

The matrix $Z = \bar y^T \bar v^T$ has $y Z v = |y|^2 |v|^2 \ne 0$, so $Z$ is not in the range of $\mathcal{T}$, and $\mathcal{T}$ is not onto. Some complex $R$ has no solution, and by the remark above some real pair $(P, Q)$ has no solution.

*Sufficiency.* Take a complex Schur form $S = U T U^\ast$ with $U$ unitary and $T$ upper triangular; the diagonal entries $t_{jj}$ are the eigenvalues of $S$. Put $Y = X U$ and $R' = R U$. The equation becomes $L Y - E Y T = R'$. Its column $j$ reads

$$(L - t_{jj} E)\, y_j = r'_j + E \sum_{i < j} t_{ij}\, y_i.$$

The matrix $L - t_{jj} E$ has full row rank $n + p$ by assumption, so this equation has a solution $y_j$ once $y_1, \dots, y_{j-1}$ are known. Solving for $j = 1, \dots, q$ in turn gives $Y$, and $X = Y U^\ast$ solves $\mathcal{T}(X) = R$. For real $R$, $\operatorname{Re} X$ is a real solution.

*Uniqueness.* If $m = p$, the map $\mathcal{T}$ goes between spaces of the same dimension $(n + m) q$. It is onto, so it is one to one. $\square$

The count of the reformulation also shows that the rank condition needs $m \ge p$: a matrix with $n + p$ rows and $n + m$ columns has rank at most $n + m$. $\blacksquare$
