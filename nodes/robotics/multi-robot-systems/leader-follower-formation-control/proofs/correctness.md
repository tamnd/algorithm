---
title: The separation-bearing law makes the separation and bearing errors of each follower decay exponentially, and the heading error decays behind a straight leader
proves: [correctness]
status: full
---

Each robot is a unicycle with state $(x, y, \theta)$ and inputs $(v, \omega)$: $\dot x = v \cos\theta$, $\dot y = v \sin\theta$, $\dot\theta = \omega$. A follower $F$ with leader $L$ controls its point $P_F = (x_F + d \cos\theta_F, y_F + d \sin\theta_F)$ with $d > 0$. The separation $l > 0$ and the bearing $\psi$ are defined by $P_F - (x_L, y_L) = l\,(\cos(\theta_L + \psi), \sin(\theta_L + \psi))$, and $\gamma = \theta_L + \psi - \theta_F$. The follower knows $v_L$ and $\omega_L$. Line numbers refer to the pseudocode on the [leader-follower formation control](/leader-follower-formation-control/) page.

**Lemma 1 (kinematics of the separation and bearing).**

$$\dot l = v_F \cos\gamma + d \omega_F \sin\gamma - v_L \cos\psi, \qquad \dot\psi = \frac{v_L \sin\psi - v_F \sin\gamma + d \omega_F \cos\gamma}{l} - \omega_L.$$

*Proof.* Let $\phi = \theta_L + \psi$ and $w = P_F - p_L = l (\cos\phi, \sin\phi)$. Then $\dot w = \dot l (\cos\phi, \sin\phi) + l \dot\phi (-\sin\phi, \cos\phi)$, so $\dot l = \dot w \cdot (\cos\phi, \sin\phi)$ and $l \dot\phi = \dot w \cdot (-\sin\phi, \cos\phi)$. Also $\dot P_F = v_F (\cos\theta_F, \sin\theta_F) + d \omega_F (-\sin\theta_F, \cos\theta_F)$ and $\dot p_L = v_L (\cos\theta_L, \sin\theta_L)$. With $\phi - \theta_F = \gamma$ and $\phi - \theta_L = \psi$, the dot products are $(\cos\theta_F, \sin\theta_F) \cdot (\cos\phi, \sin\phi) = \cos\gamma$, $(-\sin\theta_F, \cos\theta_F) \cdot (\cos\phi, \sin\phi) = \sin\gamma$, $(\cos\theta_L, \sin\theta_L) \cdot (\cos\phi, \sin\phi) = \cos\psi$, and in the normal direction $-\sin\gamma$, $\cos\gamma$ and $-\sin\psi$. So $\dot l = v_F \cos\gamma + d \omega_F \sin\gamma - v_L \cos\psi$ and $l \dot\phi = -v_F \sin\gamma + d \omega_F \cos\gamma + v_L \sin\psi$. Finally $\dot\psi = \dot\phi - \omega_L$. $\square$

**Lemma 2 (the inputs invert the kinematics).** With $a$ and $b$ from lines L4 and L5, the inputs of lines L6 and L7 give $v_F \cos\gamma + d \omega_F \sin\gamma = a$ and $-v_F \sin\gamma + d \omega_F \cos\gamma = b$.

*Proof.* Line L6 gives $v_F = a \cos\gamma - b \sin\gamma$, and line L7 gives $d \omega_F = a \sin\gamma + b \cos\gamma$. This is the rotation of $(a, b)$ by $-\gamma$, so its inverse rotation gives back $(a, b)$: $v_F \cos\gamma + d\omega_F \sin\gamma = a (\cos^2\gamma + \sin^2\gamma) = a$, and $-v_F \sin\gamma + d \omega_F \cos\gamma = b$. The map from $(v_F, \omega_F)$ to $(\dot l, \dot\psi)$ has the matrix $\begin{pmatrix} \cos\gamma & d \sin\gamma \\ -\sin\gamma / l & d \cos\gamma / l \end{pmatrix}$, whose determinant is $d / l > 0$, so the inversion is possible exactly because $d > 0$ and $l > 0$. $\square$

**Theorem 1 (exponential decay of the output errors).** Let $l(0) > 0$, $l_d > 0$, $\alpha_1, \alpha_2 > 0$, and $|\psi(0) - \psi_d| < \pi$. For any leader inputs, the closed loop gives

$$l(t) = l_d + (l(0) - l_d) e^{-\alpha_1 t}, \qquad \psi(t) - \psi_d = (\psi(0) - \psi_d) e^{-\alpha_2 t}.$$

*Proof.* By Lemmas 1 and 2, $\dot l = a - v_L \cos\psi = \alpha_1 (l_d - l)$ and $\dot\psi = (v_L \sin\psi + b)/l - \omega_L = \alpha_2 (\psi_d - \psi)$, as long as $l > 0$. These are linear equations with the stated solutions. The solution for $l$ is a convex combination of $l(0)$ and $l_d$ for every $t$, so it stays positive, and the formulas hold for all $t \ge 0$. The bearing error keeps its sign and shrinks, so it stays in $(-\pi, \pi)$ and the wrapping of angles in line L5 never changes it. $\square$

**Theorem 2 (trees of followers).** Let the robots form a directed tree in which each follower has one leader, and let each follower run the law with the actual inputs of its leader. Then the separation and bearing errors of every edge decay as in Theorem 1, whatever the root does.

*Proof.* Theorem 1 holds for any leader inputs, so it applies to each edge on its own, whether the leader is the root or another follower. $\square$

**Lemma 3 (zero dynamics behind a straight leader).** Let the leader move straight, with constant $v_L > 0$ and $\omega_L = 0$, and let the follower start with $l = l_d$ and $\psi = \psi_d$. Then the heading error $e = \theta_L - \theta_F$ satisfies $\dot e = -(v_L / d) \sin e$, and $\tan(e(t)/2) = \tan(e(0)/2)\, e^{-v_L t / d}$. So $e(t) \to 0$ for every $|e(0)| < \pi$, and the follower ends with the heading of the leader.

*Proof.* By Theorem 1, $l = l_d$ and $\psi = \psi_d$ for all $t$. Then lines L4 and L5 give $a = v_L \cos\psi$ and $b = -v_L \sin\psi$, and line L7 gives $d \omega_F = v_L (\cos\psi \sin\gamma - \sin\psi \cos\gamma) = v_L \sin(\gamma - \psi) = v_L \sin e$, since $\gamma - \psi = \theta_L - \theta_F$. So $\dot e = \dot\theta_L - \dot\theta_F = -(v_L/d) \sin e$. For $e \in (-\pi, \pi)$ with $e \ne 0$, $\frac{d}{dt} \ln |\tan(e/2)| = \dot e / \sin e = -v_L / d$, which gives the formula, and the case $e = 0$ is an equilibrium. $\blacksquare$

**What is not proved here.** Lemma 3 is the motion on the set where the outputs are already at their targets, the [zero dynamics](/zero-dynamics/). When the outputs start away from their targets, the heading error is driven also by terms that decay exponentially, and the stability of that cascade for a leader that moves straight, or with bounded turning, is the subject of the analysis of Desai, Ostrowski and Kumar (2001). That analysis, and the case of a leader that moves backward ($v_L < 0$), where the heading error grows, are not proved here.
