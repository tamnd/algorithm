---
title: Pose space deformation reproduces its examples, reduces to plain skinning without sculpts, and moves corrections with the bones
proves: [correctness]
status: full
---

We use the notation of the page.
The example poses $p_1, \ldots, p_m \in \mathbb{R}^d$ are distinct, every blended matrix $A_i(p_e)$ is invertible, and $\varphi(r) = \exp(-r^2/(2\sigma^2))$ with $\sigma > 0$.
For a vertex $i$, the interpolated correction at a pose $p$ is $c_i(p) = \sum_e C_{e,i}\, \varphi(\lVert p - p_e \rVert)$, and the output of line L7 is $v_i'(p) = A_i(p)(v_i + c_i(p))$.
The arithmetic is exact.

## The interpolation system

**Lemma 1.** $\Phi$ is symmetric positive definite, so line L3 has exactly one solution.

*Proof.*
$\Phi$ is symmetric because the distance is symmetric.
The Gaussian $x \mapsto \exp(-\lVert x \rVert^2/(2\sigma^2))$ is the Fourier transform of a positive Gaussian, so by Bochner's theorem it is a positive definite function on $\mathbb{R}^d$, and since its Fourier transform is positive everywhere, the quadratic form $\sum_{e,f} a_e a_f \varphi(\lVert p_e - p_f \rVert)$ is positive for distinct points and $a \ne 0$.
In detail: with $\hat g > 0$ the Fourier transform of the kernel, $\sum_{e,f} a_e a_f g(p_e - p_f) = (2\pi)^{-d} \int \hat g(\omega) \lvert \sum_e a_e e^{i \omega \cdot p_e} \rvert^2 d\omega$.
The integrand is nonnegative, and it is zero almost everywhere only if the exponential sum vanishes on an open set, which for distinct $p_e$ forces $a = 0$, because exponentials with distinct frequencies are linearly independent. $\square$

## Reproduction and the plain case

**Theorem 1.** For every example $e$ and vertex $i$, $v_i'(p_e) = s_{e,i}$.

*Proof.*
Line L3 makes $\sum_f C_{f,i} \Phi_{e f} = d_{e,i}$, and $\Phi_{e f} = \varphi(\lVert p_e - p_f \rVert)$, so $c_i(p_e) = d_{e,i}$.
By line L1, $v_i + d_{e,i} = A_i(p_e)^{-1} s_{e,i}$.
So $v_i'(p_e) = A_i(p_e) A_i(p_e)^{-1} s_{e,i} = s_{e,i}$. $\square$

**Theorem 2.** If $s_{e,i} = A_i(p_e) v_i$ for every $e$ and $i$, then $v_i'(p) = A_i(p) v_i$ for every pose $p$.

*Proof.*
Line L1 gives $d_{e,i} = A_i(p_e)^{-1} A_i(p_e) v_i - v_i = 0$.
By Lemma 1 the only solution of $\Phi C = 0$ is $C = 0$, so $c_i(p) = 0$ for every $p$. $\square$

**Theorem 3.** $\lvert c_i(p) \rvert \le \bigl(\sum_e \lvert C_{e,i} \rvert\bigr) \exp(-\delta^2/(2\sigma^2))$, where $\delta$ is the distance from $p$ to the nearest example pose.
So the correction tends to 0, and $v_i'(p) - A_i(p) v_i \to 0$ when the blended matrices stay bounded, as $p$ moves away from all examples.

*Proof.*
Each $\varphi(\lVert p - p_e \rVert) \le \varphi(\delta)$, because $\varphi$ decreases in $r$. Apply the triangle inequality to the sum. $\square$

## Corrections move with the bones

**Theorem 4.** Let $G$ be a rigid motion, and let a pose $p'$ give the joint transforms $G M_j(p)$ for every joint, with the same pose distances to the examples as $p$.
Then $v_i'(p') = G\, v_i'(p)$.

*Proof.*
$A_i(p') = \sum_j w_{ij} G M_j(p) B_j^{-1} = G A_i(p)$.
The correction depends on $p$ only through the distances to the examples, so $c_i(p') = c_i(p)$.
So $v_i'(p') = G A_i(p)(v_i + c_i(p)) = G v_i'(p)$. $\square$

In the test, the pose $(\tau, \pi/2)$ turns the root by $\tau$, which multiplies every joint transform by the rotation $G$, and the example is placed at that same pose so that the distance is 0 in both cases.
If instead the correction were added after skinning, as $A_i(p) v_i + c_i(p)$, the result at $p'$ would be $G A_i(p) v_i + c_i(p)$, which differs from $G(A_i(p) v_i + c_i(p))$ unless $G$ fixes $c_i(p)$.

## The check value

For one scalar correction with $\theta_1 = 0$, $\theta_2 = \pi/2$, values $0$ and $0.1$, and $q = \varphi(\pi/2)$, the system is $\begin{pmatrix} 1 & q \\ q & 1 \end{pmatrix} C = \begin{pmatrix} 0 \\ 0.1 \end{pmatrix}$, so $C = (-0.1 q, 0.1)/(1 - q^2)$.
At $\theta = \pi/4$ both kernel values equal $r = \varphi(\pi/4)$, so the correction is $r (C_1 + C_2) = 0.1 r (1 - q)/(1 - q^2) = 0.1 r/(1 + q)$.
