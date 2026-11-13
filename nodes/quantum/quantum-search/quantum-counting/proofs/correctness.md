---
title: Quantum counting gives M within 2 pi sqrt(M(N-M))/P + pi^2 N/P^2 with probability at least 8/pi^2
proves: [correctness]
status: full
---

We use the pseudocode of the page. The search space is $\{0, 1, \ldots, N-1\}$, the set of marked items is $S$ with $|S| = M$, and $P = 2^t$. Let $\theta \in [0, \pi/2]$ be the angle with $\sin^2\theta = M/N$. The Grover iteration is $G = D\,O_f$, where $O_f|x\rangle = (-1)^{f(x)}|x\rangle$ and $D = 2|s\rangle\langle s| - I$ with $|s\rangle = N^{-1/2}\sum_x |x\rangle$. If the search register has more than $N$ basis states, the extra states start with amplitude 0, and $G$ keeps them at 0, so we work in the span of $|0\rangle, \ldots, |N-1\rangle$.

**Theorem.** QUANTUM-COUNTING makes $P - 1$ queries. With probability at least $8/\pi^2$ its output $\tilde M$ satisfies

$$|\tilde M - M| \le \frac{2\pi\sqrt{M(N-M)}}{P} + \frac{\pi^2 N}{P^2}.$$

If $M = 0$ or $M = N$, the output is $M$ with certainty.

**Claim 1 (queries).** Line L4 applies $G^{2^j}$, which makes $2^j$ queries, for $j = 0, \ldots, t-1$. The total is $\sum_{j=0}^{t-1} 2^j = 2^t - 1 = P - 1$. No other line makes a query.

**Claim 2 (the eigenvectors of G).** Let $0 < M < N$. Let $|\alpha\rangle$ be the uniform state on the unmarked items and $|\beta\rangle$ the uniform state on the marked items. Then $|s\rangle = \cos\theta\,|\alpha\rangle + \sin\theta\,|\beta\rangle$. On the plane spanned by $|\alpha\rangle$ and $|\beta\rangle$, $O_f$ is the reflection in $|\alpha\rangle$ and $D$ is the reflection in $|s\rangle$. The product of two reflections in lines at angle $\theta$ is the rotation by $2\theta$, so in the basis $(|\alpha\rangle, |\beta\rangle)$

$$G = \begin{pmatrix} \cos 2\theta & -\sin 2\theta \\ \sin 2\theta & \cos 2\theta \end{pmatrix}.$$

The vectors $|\psi_\pm\rangle = (|\alpha\rangle \mp i|\beta\rangle)/\sqrt{2}$ are orthonormal, and a direct product gives $G|\psi_\pm\rangle = e^{\pm 2i\theta}|\psi_\pm\rangle$. Also $\langle\psi_\pm|s\rangle = (\cos\theta \pm i\sin\theta)/\sqrt 2 = e^{\pm i\theta}/\sqrt 2$, so

$$|s\rangle = \frac{1}{\sqrt 2}\left(e^{i\theta}|\psi_+\rangle + e^{-i\theta}|\psi_-\rangle\right).$$

Write $e^{\pm 2i\theta} = e^{2\pi i\omega_\pm}$ with $\omega_+ = \theta/\pi$ and $\omega_- = 1 - \theta/\pi$, both in $[0, 1)$.

**Claim 3 (the state before the measurement).** Line L2 gives $P^{-1/2}\sum_{y=0}^{P-1}|y\rangle|s\rangle$. Let $y = \sum_j y_j 2^j$, where $y_j$ is the bit of counting qubit $j$. Line L4 for qubit $j$ applies $G^{2^j}$ to the search register when $y_j = 1$, so after line L3 the search register of the term $|y\rangle$ is $G^{y}|s\rangle$. For an eigenvector with $G|\psi\rangle = e^{2\pi i\omega}|\psi\rangle$, the state $P^{-1/2}\sum_y |y\rangle G^y|\psi\rangle$ is $\left(P^{-1/2}\sum_y e^{2\pi i\omega y}|y\rangle\right)|\psi\rangle$. The inverse Fourier transform maps $|y\rangle$ to $P^{-1/2}\sum_k e^{-2\pi i yk/P}|k\rangle$, so after line L5 this state is $\sum_k a_\omega(k)|k\rangle|\psi\rangle$ with

$$a_\omega(k) = \frac{1}{P}\sum_{y=0}^{P-1} e^{2\pi i y(\omega - k/P)}.$$

Let $\delta = P\omega - k$. If $\delta$ is an integer, $a_\omega(k)$ is 1 when $\delta \equiv 0 \pmod P$ and 0 otherwise. If not, the geometric sum gives

$$|a_\omega(k)|^2 = \frac{\sin^2(\pi\delta)}{P^2\sin^2(\pi\delta/P)}.$$

By Claim 2 and linearity, the state after line L5 is $2^{-1/2}\sum_k \left(e^{i\theta}a_{\omega_+}(k)|k\rangle|\psi_+\rangle + e^{-i\theta}a_{\omega_-}(k)|k\rangle|\psi_-\rangle\right)$. Because $|\psi_+\rangle$ and $|\psi_-\rangle$ are orthogonal, line L6 gives $y = k$ with probability

$$\Pr[y = k] = \tfrac{1}{2}|a_{\omega_+}(k)|^2 + \tfrac{1}{2}|a_{\omega_-}(k)|^2.$$

**Claim 4 (two nearest grid points).** Let $\omega \in [0, 1)$, let $k_0 = \lfloor P\omega \rfloor$ and $\delta = P\omega - k_0 \in [0, 1)$. Then $|a_\omega(k_0)|^2 + |a_\omega(k_0 + 1 \bmod P)|^2 \ge 8/\pi^2$.

*Proof.* If $\delta = 0$, then $|a_\omega(k_0)|^2 = 1$. Let $0 < \delta < 1$. For $k_0$ the offset is $\delta$, and for $k_0 + 1$ it is $\delta - 1$; the case $k_0 + 1 = P$ has the offset $\delta - 1 + P$, with the same value of $|a|^2$, because $\sin^2(\pi\cdot)$ has period 1 and $\sin^2(\pi\cdot/P)$ has period $P$. From $0 < \sin z \le z$ for $0 < z < \pi$,

$$|a_\omega(k_0)|^2 + |a_\omega(k_0+1)|^2 \ge \frac{\sin^2(\pi\delta)}{\pi^2}\left(\frac{1}{\delta^2} + \frac{1}{(1-\delta)^2}\right).$$

Let $A = \pi/2$ and $x = A - \pi\delta$, so $\pi\delta = A - x$, $\pi(1 - \delta) = A + x$ and $\sin(\pi\delta) = \cos x$. The right side is then

$$\cos^2 x\left(\frac{1}{(A-x)^2} + \frac{1}{(A+x)^2}\right) = \frac{2\cos^2 x\,(A^2 + x^2)}{(A^2 - x^2)^2}.$$

This is at least $8/\pi^2 = 2/A^2$ if and only if $\cos^2 x\,(1 + u) \ge (1 - u)^2$, where $u = x^2/A^2 \in [0, 1)$. The product formula $\cos x = \prod_{k \ge 1}\left(1 - u/(2k-1)^2\right)$ has all factors in $[0, 1]$, and $\prod (1 - a_k) \ge 1 - \sum a_k$ for $a_k \in [0, 1]$. So

$$\cos x \ge (1 - u)(1 - cu), \qquad c = \sum_{k \ge 2}\frac{1}{(2k-1)^2} = \frac{\pi^2}{8} - 1 < 0.234.$$

It is enough to show $(1 - cu)^2(1 + u) \ge 1$. Expand: $(1 - cu)^2(1 + u) - 1 = u\left(1 - 2c + (c^2 - 2c)u + c^2u^2\right)$. Since $c^2 - 2c < 0$ and $u < 1$, the bracket is more than $1 - 4c + c^2$, which is positive because $c < 2 - \sqrt 3$. $\square$

**Claim 5 (from the angle to the count).** Let $\tilde\theta$ be a real number and $\varepsilon = \tilde\theta - \theta$. Then $N|\sin^2\tilde\theta - \sin^2\theta| \le 2|\varepsilon|\sqrt{M(N-M)} + N\varepsilon^2$. The same bound holds when $\varepsilon = \pm\tilde\theta - \theta + m\pi$ for any integer $m$ and either sign, because $\sin^2$ is even and has period $\pi$.

*Proof.* $\sin^2(\theta + \varepsilon) - \sin^2\theta = \sin(2\theta + \varepsilon)\sin\varepsilon = \sin 2\theta\cos\varepsilon\sin\varepsilon + \cos 2\theta\sin^2\varepsilon$. Its absolute value is at most $\sin 2\theta\,|\varepsilon| + \varepsilon^2$. Multiply by $N$ and use $N\sin 2\theta = 2N\sin\theta\cos\theta = 2\sqrt{M(N-M)}$. $\square$

**Proof of the theorem.** Claim 1 gives the queries.

Let $M = 0$. Then $f$ is 0 everywhere, $O_f = I$ and $G|s\rangle = D|s\rangle = |s\rangle$. The state after line L3 is $P^{-1/2}\sum_y|y\rangle|s\rangle$, and line L5 maps it to $|0\rangle|s\rangle$. So $y = 0$ and $\tilde M = N\sin^2 0 = 0$ with certainty.

Let $M = N$. Then $O_f = -I$ and $G|s\rangle = -|s\rangle = e^{2\pi i/2}|s\rangle$. By Claim 3 with $\omega = 1/2$ and $\delta = 0$ at $k = P/2$, line L6 gives $y = P/2$ with certainty, and $\tilde M = N\sin^2(\pi/2) = N$.

Let $0 < M < N$. Let $K_+$ be the two grid points of Claim 4 for $\omega_+$ and $K_-$ those for $\omega_-$. Call an outcome $y$ good if $y \in K_+ \cup K_-$. By Claims 3 and 4,

$$\Pr[y \text{ good}] \ge \tfrac{1}{2}\sum_{k \in K_+}|a_{\omega_+}(k)|^2 + \tfrac{1}{2}\sum_{k \in K_-}|a_{\omega_-}(k)|^2 \ge \tfrac{1}{2}\cdot\tfrac{8}{\pi^2} + \tfrac{1}{2}\cdot\tfrac{8}{\pi^2} = \frac{8}{\pi^2}.$$

Let $y$ be good and $\tilde\theta = \pi y/P$ (line L7). If $y \in K_+$, then $y/P$ is within $1/P$ of $\omega_+ = \theta/\pi$ modulo 1, so $\tilde\theta - \theta + m\pi \in [-\pi/P, \pi/P]$ for an integer $m$. If $y \in K_-$, then $y/P$ is within $1/P$ of $1 - \theta/\pi$ modulo 1, so $-\tilde\theta - \theta + m\pi \in [-\pi/P, \pi/P]$ for an integer $m$. In both cases Claim 5 with $|\varepsilon| \le \pi/P$ gives, for $\tilde M = N\sin^2\tilde\theta$ (line L8),

$$|\tilde M - M| \le \frac{2\pi\sqrt{M(N-M)}}{P} + \frac{\pi^2 N}{P^2}.$$

So the bound holds with probability at least $8/\pi^2$. $\blacksquare$
