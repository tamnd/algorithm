---
title: The loop shaping code computes gamma_min and a controller that meets the level
proves: [correctness]
status: full
---

Notation is that of the page. The theorem of Glover and McFarlane (1989) is cited, not proved here: for the stabilizing solutions $X \ge 0$ and $Z \ge 0$ of the two Riccati equations, $\gamma_{\min} = \sqrt{1 + \rho(XZ)}$ is the smallest achievable value of $\gamma(G_s, K_s)$, and for every $\gamma > \gamma_{\min}$ the central controller of the source reaches $\gamma(G_s, K_s) \le \gamma$ with an internally stable loop. What we prove is that the code computes the objects in that theorem and wires the result correctly.

## Claim 1: the Riccati step returns the stabilizing solutions

*Line L3 returns the unique symmetric $X$ with $A^T X + X A - X B B^T X + C^T C = 0$ and $A - B B^T X$ Hurwitz. Line L2 returns the unique symmetric $Z$ with $A Z + Z A^T - Z C^T C Z + B B^T = 0$ and $A - Z C^T C$ Hurwitz.*

*Proof.* The routine `riccati(a, r, q)` is the same as on the two-Riccati synthesis page, where Claims 3 and 4 of its proof show that it returns the stabilizing solution of $a^T X + X a + X r X + q = 0$, or nothing. Line L3 calls it with $a = A$, $r = -B B^T$, $q = C^T C$, which is the control equation, and the routine checks that $A - B B^T X$ is Hurwitz. Line L2 calls it with $a = A^T$, $r = -C^T C$, $q = B B^T$. Then $a^T Z + Z a + Z r Z + q = A Z + Z A^T - Z C^T C Z + B B^T$, and the routine checks that $A^T - C^T C Z$ is Hurwitz, which holds if and only if its transpose $A - Z C^T C$ is Hurwitz. Stabilizability of $(A, B)$ and detectability of $(C, A)$ give existence and $X, Z \ge 0$ (the [stabilizing Riccati solution theorem](/stabilizing-riccati-solution-theorem/)). $\square$

Line L4 then evaluates the formula of the theorem. $XZ = (X Z^{1/2}) Z^{1/2}$ has the same eigenvalues as $Z^{1/2} X Z^{1/2} \ge 0$, so its eigenvalues are real and nonnegative and $\rho(XZ)$ is its largest eigenvalue.

## Claim 2: the sign change gives the same loop and the same margin

*Let $K_+ = (A_K, B_K, B^T X, 0)$ be the controller of the source for positive feedback $u = K_+ y$. The code returns $K = (A_K, B_K, -B^T X, 0)$ for $u = -K y$. The two loops are the same, and $\gamma(G_s, K)$ equals the robustness level of the source for $K_+$.*

*Proof.* The transfer matrix of $K$ is $-K_+$, so $-K y = K_+ y$ and the two loops have the same equations. The source states the level for $K_+$ as $\| [K_+; I](I - G_s K_+)^{-1} M^{-1} \|_\infty$. Put $K_+ = -K$:

$$\begin{bmatrix} -K \\ I \end{bmatrix} (I + G_s K)^{-1} M^{-1} = \begin{bmatrix} -I & 0 \\ 0 & I \end{bmatrix} \begin{bmatrix} K \\ I \end{bmatrix} (I + G_s K)^{-1} M^{-1}.$$

The left factor is a constant orthogonal matrix, so it does not change the largest singular value. Next, $M^{-1} \begin{bmatrix} N & M \end{bmatrix} = \begin{bmatrix} G_s & I \end{bmatrix}$, and the normalized factors satisfy $\begin{bmatrix} N & M \end{bmatrix} \begin{bmatrix} N & M \end{bmatrix}^* = I$ on the imaginary axis. For any matrix $T$ and any $V$ with $V V^* = I$, $(T V)(T V)^* = T T^*$, so $T V$ and $T$ have the same largest singular value. With $T = [K; I](I + G_s K)^{-1} M^{-1}$ and $V = [N\ M]$, the norm in the source equals the norm of $[K; I](I + G_s K)^{-1}[G_s\ I]$ at every frequency. Swapping the two block columns does not change the singular values, which gives $\gamma(G_s, K)$ as defined on the page. $\square$

## Claim 3: the final loop has the same closed loop matrix as the shaped loop

*Let $G_s$ = `series(series(W1, G), W2)` and $K$ = `series(series(W2, Ks), W1)`. Then the closed loop state matrix of $G$ with $u = -K y$ is equal, up to a permutation of the states, to the closed loop state matrix of $G_s$ with $u_s = -K_s y_s$. So the first loop is internally stable if and only if the second is.*

*Proof.* `series(s1, s2)` builds the state $(x_1, x_2)$ with $\dot x_1 = A_1 x_1 + B_1 v$, $r = C_1 x_1 + D_1 v$, $\dot x_2 = A_2 x_2 + B_2 r$ and output $C_2 x_2 + D_2 r$. This is the realization of $s_2 s_1$ whose state is the union of the two states, and the empty-state cases in the code are the same formulas with one part removed. So $G_s$ is the chain $W_1 \to G \to W_2$ and $K$ is the chain $W_2 \to K_s \to W_1$, each with the states of its parts. Both closed loops are the ring $W_1 \to G \to W_2 \to K_s \to (-1) \to W_1$ with the same four realizations. The closed loop equations list the same state equations in a different order, so the closed loop matrices are equal up to a permutation of the states. $\square$

The level $\gamma$ is a property of the shaped loop $(G_s, K_s)$, not of $(G, K)$. The page and the tests state it only for the shaped loop.

## Claim 4: closed forms for first-order shaped plants

*For $G_s = 1/(s - a)$, that is $A = a$ and $B = C = 1$, $X = Z = a + \sqrt{a^2 + 1}$ and $\gamma_{\min}^2 = 1 + (a + \sqrt{a^2 + 1})^2$. For $a = 0$, $\gamma_{\min} = \sqrt 2$. For $a = -1$, $\gamma_{\min} = \sqrt{4 - 2\sqrt 2}$ and $1/\gamma_{\min} = \cos(\pi/8)$.*

*Proof.* Both equations become $-X^2 + 2 a X + 1 = 0$. The roots are $a \pm \sqrt{a^2 + 1}$, and $a - X = -\sqrt{a^2 + 1} < 0$ only for the plus sign, so that is the stabilizing root. Then $\rho(XZ) = X^2$. For $a = 0$, $X = 1$. For $a = -1$, $X = \sqrt 2 - 1$ and $X^2 = 3 - 2\sqrt 2$, so $\gamma_{\min}^2 = 4 - 2\sqrt 2$. Finally $\cos^2(\pi/8) = (1 + \cos(\pi/4))/2 = (2 + \sqrt 2)/4$ and $(4 - 2\sqrt 2)(2 + \sqrt 2) = 8 - 4 = 4$, so $\gamma_{\min}^{-2} = \cos^2(\pi/8)$. $\square$

## Claim 5: for 1/s the unity gain is optimal

*For $G_s = 1/s$ and $K_s = 1$, $\gamma(G_s, K_s) = \sqrt 2 = \gamma_{\min}$.*

*Proof.* The loop $1/s$ with unity negative feedback has the pole $-1$, so it is internally stable. At $s = j\omega$ with $\omega \ne 0$, $(1 + 1/s)^{-1} = s/(s + 1)$ and the map is $\frac{s}{s + 1} \begin{bmatrix} 1 \\ 1 \end{bmatrix} \begin{bmatrix} 1 & 1/s \end{bmatrix}$. This has rank one, so its largest singular value is $\left| \frac{s}{s + 1} \right| \sqrt 2 \sqrt{1 + 1/\omega^2} = \sqrt 2$ for every $\omega$. By Claim 4 this equals $\gamma_{\min}$. $\square$

The test checks this value with the code's frequency sweep, which tests the sweep and the definition of $b$ against a value known in closed form.

## What the tests check

- The values of Claim 4, and the Riccati residuals, positive semidefiniteness and Hurwitz checks of Claim 1 on four plants, one of them open loop unstable and two with a pole at 0.
- $\gamma_{\min}$ against an independent route: $1 - \|[N\ M]\|_H^2 = \gamma_{\min}^{-2}$, with the Hankel norm from the controllability and observability gramians of the realization $(A - Z C^T C, [B, -Z C^T], C, [0, I])$, each from a Kronecker form Lyapunov solve.
- For each plant and $\gamma = 1.05, 1.1, 1.5$ times $\gamma_{\min}$: the closed loop is Hurwitz and the swept margin is between $1/\gamma$ and $\varepsilon_{\max}$.
- Brute force: random static and first-order controllers for two plants. Every one that stabilizes has a swept margin at most $\varepsilon_{\max}$. The sweep uses a coarse grid, which can only miss the peak and so overstate the margin; the check is therefore on the safe side.
- A full design with $W_1 = (s + 2)/s$: the final controller contains the integrator and the loop with the plant is Hurwitz.
