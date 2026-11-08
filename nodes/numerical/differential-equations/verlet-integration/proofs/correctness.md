---
title: Velocity Verlet is a symmetric, symplectic method of order 2
proves: [correctness, termination, convergence]
status: full
---

**Setting.** We integrate $q'' = a(q)$, $q \in \mathbb{R}^k$, written as the first-order system $y = (q, v) \in \mathbb{R}^{2k}$, $q' = v$, $v' = a(q)$, so $d = 2k$ in the page notation $y' = f(t, y)$. When $a = -\nabla V$ for a potential $V$, this is the Hamiltonian system with $H(q, v) = \frac12|v|^2 + V(q)$. We assume $a \in C^2$ and Lipschitz with constant $L_a$, and use the Euclidean norm. One step of size $\tau$ is the map $\Phi_\tau = K_{\tau/2} \circ D_\tau \circ K_{\tau/2}$ with the kick $K_s(q, v) = (q, v + s\,a(q))$ and the drift $D_s(q, v) = (q + s v, v)$, applied right to left. Lines L6 to L9 compute exactly this composition.

**Termination.** Line L1 gives a finite $N \ge 0$; the loop of line L4 runs $N$ times, each with one evaluation of $a$ at line L8. Line L5 makes the last step end exactly at $T$, so its length lies in $(0, h]$ (up to the slack $\delta$). With $T = t_0$ the loop does not run and the start values are returned after the single evaluation of line L3.

**Lemma 1 (one evaluation per step).** At the start of each pass, the variable $A$ equals $a(q)$ for the current $q$.

*Proof.* Line L3 sets it before the first pass. Line L7 is the only line that changes $q$, and line L8 immediately recomputes $A = a(q)$. $\square$

**Lemma 2 (symplectic).** If $a = -\nabla V$ with $V \in C^2$, then $\Phi_\tau$ is symplectic: its Jacobian $J$ satisfies $J^T \Omega J = \Omega$ with $\Omega = \begin{pmatrix} 0 & I \\ -I & 0 \end{pmatrix}$.

*Proof.* The Jacobian of $K_s$ is $\begin{pmatrix} I & 0 \\ -sS & I \end{pmatrix}$ with $S = \nabla^2 V(q)$ symmetric, and that of $D_s$ is $\begin{pmatrix} I & sI \\ 0 & I \end{pmatrix}$. For any matrix of the form $\begin{pmatrix} I & 0 \\ B & I \end{pmatrix}$ with $B$ symmetric, a direct multiplication gives $J^T \Omega J = \begin{pmatrix} B - B^T & I \\ -I & 0 \end{pmatrix} = \Omega$, and the same holds for $\begin{pmatrix} I & B \\ 0 & I \end{pmatrix}$. The chain rule makes the Jacobian of $\Phi_\tau$ a product of such matrices evaluated at the intermediate points, and a product of symplectic matrices is symplectic. $\square$

For $k = 1$ symplectic means $\det J = 1$: the map preserves area in the $(q, v)$ plane.

**Lemma 3 (symmetric, time-reversible).** $\Phi_{-\tau} \circ \Phi_\tau = \mathrm{id}$, and if $R(q, v) = (q, -v)$ then $R \circ \Phi_\tau \circ R = \Phi_{-\tau} = \Phi_\tau^{-1}$.

*Proof.* $K_s^{-1} = K_{-s}$ and $D_s^{-1} = D_{-s}$. So $\Phi_\tau^{-1} = K_{-\tau/2} \circ D_{-\tau} \circ K_{-\tau/2} = \Phi_{-\tau}$. For the second claim, $R K_s R = K_{-s}$ and $R D_s R = D_{-s}$. $\square$

**Lemma 4 (local error).** Let $(q(t), v(t))$ be the exact solution through $(q, v)$ at $t$. Then $\Phi_\tau(q, v) - (q(t + \tau), v(t + \tau)) = O(\tau^3)$, uniformly on bounded sets.

*Proof.* Write $a = a(q)$ and $a' = Da(q)$. The method gives $q_1 = q + \tau v + \frac{\tau^2}{2} a$ exactly, and $v_1 = v + \frac{\tau}{2}(a + a(q_1)) = v + \frac{\tau}{2}\big(2a + a'(\tau v) + O(\tau^2)\big) = v + \tau a + \frac{\tau^2}{2} a' v + O(\tau^3)$, using $a \in C^2$. By Taylor's theorem, $q(t + \tau) = q + \tau v + \frac{\tau^2}{2} a + O(\tau^3)$ and $v(t + \tau) = v + \tau a + \frac{\tau^2}{2} a' v + O(\tau^3)$, since $\frac{d}{dt} a(q(t)) = a' v$. The terms agree up to $O(\tau^3)$. $\square$

**Theorem (global error, proved).** Under the assumptions above, on $[t_0, T]$ the computed values satisfy $\|y(t_n) - y_n\| \le C h^2$, with $C$ depending on $T - t_0$, $L_a$ and the bounds of Lemma 4.

*Proof.* Each of $K_s$ and $D_s$ is Lipschitz with constant at most $1 + |s|\max(1, L_a)$, so $\Phi_\tau$ is Lipschitz with constant $1 + \Lambda\tau$ for $\tau \le h$, with $\Lambda = 2\max(1, L_a)(1 + h\max(1, L_a))^2$. Let $e_n = y(t_n) - y_n$. Then $\|e_{n+1}\| \le \|y(t_{n+1}) - \Phi_{\tau_n}(y(t_n))\| + \|\Phi_{\tau_n}(y(t_n)) - \Phi_{\tau_n}(y_n)\| \le c\tau_n^3 + (1 + \Lambda\tau_n)\|e_n\|$ by Lemma 4. With $e_0 = 0$ and $\tau_n \le h$, induction gives $\|e_n\| \le c h^2 \sum_m \tau_m e^{\Lambda(t_n - t_{m+1})} \le c h^2 (T - t_0) e^{\Lambda (T - t_0)}$. $\square$

**Harmonic oscillator.** For $a(q) = -\omega^2 q$ and $z = h\omega$, the step matrix is
$$M = \begin{pmatrix} 1 - z^2/2 & h \\ -h\omega^2(1 - z^2/4) & 1 - z^2/2 \end{pmatrix}, \qquad \det M = 1, \qquad \operatorname{tr} M = 2 - z^2.$$
With $c = 1 - z^2/2$ and $\alpha = \omega^2(1 - z^2/4)$, one checks $M^T G M = G$ for $G = \operatorname{diag}(\alpha, 1)$, because $c^2 + h^2\alpha = 1$. So the modified energy $\tilde H = v^2 + \omega^2(1 - z^2/4) q^2$ is conserved exactly. For $0 < z < 2$ this form is positive definite, so all iterates stay on a fixed ellipse: the method is stable. At $z = 2$, $M = \begin{pmatrix} -1 & h \\ 0 & -1 \end{pmatrix}$ is a Jordan block and $v_0 \ne 0$ gives linear growth. For $z > 2$, $|\operatorname{tr} M| > 2$, so $M$ has a real eigenvalue of modulus greater than 1 and the iterates grow exponentially.

**Long times (cited, asymptotic).** For analytic $H$ and $h$ small, backward error analysis shows that the method is the exact flow of a modified Hamiltonian $\tilde H = H + h^2 H_2 + \cdots$ up to an error $O(e^{-c/h})$, so $|H(y_n) - H(y_0)| = O(h^2)$ for $nh \le e^{c/(2h)}$ (Hairer, Lubich and Wanner 2006, Sections IX.3 and IX.8). We state this as a known result; the tests check the absence of drift numerically.
