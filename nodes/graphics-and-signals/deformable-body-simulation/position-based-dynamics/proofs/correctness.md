---
title: The PBD projection is the smallest mass-weighted correction, keeps linear momentum and is torque-free, but the step does not keep angular momentum
proves: [correctness]
status: full
---

We use the notation of the page. There are $n$ particles with positions $\mathbf p_i \in \mathbb R^2$ and inverse masses $w_i = 1/m_i$; a pinned particle has $w_i = 0$ and is left out of all sums over masses. A constraint $C$ depends on a set $S$ of particles, and $\nabla_i C$ is its gradient with respect to $\mathbf p_i$. The projection of line L6 with the sweep stiffness $k'$ is

$$s = \frac{C(\mathbf p)}{\sum_{j \in S} w_j |\nabla_j C(\mathbf p)|^2}, \qquad \Delta \mathbf p_i = -k' s\, w_i \nabla_i C(\mathbf p) \quad (i \in S),$$

which is equations (8) and (9) of Müller et al. (2007) with the masses put in. An inequality constraint $C \ge 0$ is projected only when $C(\mathbf p) < 0$.

## The projection is a weighted least squares step

**Lemma 1.** Let $\nabla C(\mathbf p) \ne 0$ on the free particles. With $k' = 1$, the correction $\Delta \mathbf p$ is the unique minimizer of $\sum_{i \in S} m_i |\Delta \mathbf p_i|^2$ subject to the linearized constraint $C(\mathbf p) + \sum_{i \in S} \nabla_i C \cdot \Delta \mathbf p_i = 0$, where only free particles may move.

*Proof.* The objective is a strictly convex quadratic in the free unknowns, and the constraint is one affine equation that has a solution because some free $\nabla_i C$ is not zero. So the minimizer is unique, and it is the solution of the KKT system $m_i \Delta \mathbf p_i = \lambda \nabla_i C$ for free $i$, together with the constraint. Then $\Delta \mathbf p_i = \lambda w_i \nabla_i C$, and the constraint gives $C + \lambda \sum_j w_j |\nabla_j C|^2 = 0$, so $\lambda = -s$. This is the correction of line L6. $\square$

**Corollary 2 (equations (10) and (11) of the paper).** For $C = |\mathbf p_1 - \mathbf p_2| - d$, let $\mathbf n = (\mathbf p_1 - \mathbf p_2)/|\mathbf p_1 - \mathbf p_2|$. Then $\nabla_1 C = \mathbf n$, $\nabla_2 C = -\mathbf n$, $s = C/(w_1 + w_2)$, and $\Delta \mathbf p_1 = -\frac{w_1}{w_1 + w_2} (|\mathbf p_1 - \mathbf p_2| - d)\, \mathbf n$, $\Delta \mathbf p_2 = +\frac{w_2}{w_1 + w_2} (|\mathbf p_1 - \mathbf p_2| - d)\, \mathbf n$. After the correction, $\mathbf p_1 - \mathbf p_2$ keeps its direction and has the length $d$, so one projection satisfies a single distance constraint exactly. $\square$

## Momentum of one projection

**Lemma 3.** If $C$ does not change when all its particles move by the same vector, then $\sum_{i \in S} m_i \Delta \mathbf p_i = 0$, provided that all particles of $S$ are free.

*Proof.* Invariance under a translation by $t \mathbf e$ gives $0 = \frac{d}{dt} C(\mathbf p + t \mathbf e) = \sum_i \nabla_i C \cdot \mathbf e$ for every $\mathbf e$, so $\sum_i \nabla_i C = 0$. Then $\sum_i m_i \Delta \mathbf p_i = -k' s \sum_i m_i w_i \nabla_i C = -k' s \sum_i \nabla_i C = 0$. $\square$

**Lemma 4.** If $C$ does not change when all its particles turn by the same rotation about the origin, then $\sum_{i \in S} m_i\, \mathbf p_i \times \Delta \mathbf p_i = 0$, where $\mathbf a \times \mathbf b = a_x b_y - a_y b_x$ and $\mathbf p$ is the state before the projection. All particles of $S$ must be free.

*Proof.* Let $J$ be the rotation by $90°$. Invariance under the rotation by the angle $t$ gives $0 = \frac{d}{dt} C(R(t)\mathbf p)|_{t=0} = \sum_i \nabla_i C \cdot J \mathbf p_i$. Since $\mathbf g \cdot J \mathbf p = -\mathbf p \times \mathbf g$, this is $\sum_i \mathbf p_i \times \nabla_i C = 0$. Then $\sum_i m_i \mathbf p_i \times \Delta \mathbf p_i = -k' s \sum_i \mathbf p_i \times \nabla_i C = 0$. $\square$

Distance and area constraints satisfy both hypotheses. The ground constraint does not, because it fixes a line in space. These two lemmas are the conditions (1) and (2) of Section 3.3 of the paper.

## Momentum of one step

**Theorem 5 (linear momentum).** Let every constraint satisfy the hypothesis of Lemma 3, let no particle be pinned and let there be no ground. Then one call of the step, with any number of sweeps and any damping factor, gives $\sum_i m_i \mathbf v_i^{n+1} = \sum_i m_i \mathbf v_i^n + \Delta t \sum_i m_i \mathbf g$.

*Proof.* Line L1 adds $\Delta t \sum m_i \mathbf g$ to the momentum. The damping of line L2 replaces $\mathbf v_i$ by $\mathbf v_i + k_d (\mathbf v_{cm} + \omega J \mathbf r_i - \mathbf v_i)$; since $\sum m_i \mathbf r_i = 0$ and $\sum m_i \mathbf v_i = M_{\text{tot}} \mathbf v_{cm}$, the sum of $m_i$ times the change is zero. Lines L3 to L6 change $\mathbf p$ by a sum of corrections, each with $\sum m_i \Delta \mathbf p_i = 0$ by Lemma 3. So $\sum m_i \mathbf p_i = \sum m_i (\mathbf x_i + \Delta t \mathbf v_i)$ with the velocities after L2, and line L7 gives $\sum m_i \mathbf v_i^{n+1} = \sum m_i (\mathbf p_i - \mathbf x_i)/\Delta t = \sum m_i \mathbf v_i$. $\square$

**Lemma 6 (the damping keeps angular momentum).** The damping of line L2 does not change $\sum m_i \mathbf x_i \times \mathbf v_i$.

*Proof.* Write $\mathbf x_i = \mathbf x_{cm} + \mathbf r_i$. The change of velocity is $k_d \Delta \mathbf v_i$ with $\Delta \mathbf v_i = \mathbf v_{cm} + \omega J \mathbf r_i - \mathbf v_i$. Its linear part sums to zero, as in Theorem 5, so the angular momentum changes by $k_d \sum m_i \mathbf r_i \times \Delta \mathbf v_i$. Here $\sum m_i \mathbf r_i \times \mathbf v_{cm} = 0$, $\sum m_i \mathbf r_i \times \omega J \mathbf r_i = \omega I$ with $I = \sum m_i |\mathbf r_i|^2$, and $\sum m_i \mathbf r_i \times \mathbf v_i = L_{cm}$. With $\omega = L_{cm}/I$ the sum is zero. $\square$

**Theorem 7 (angular momentum changes).** With no external force, no damping and no pins, let $\Delta \mathbf p_i$ be the sum of all corrections that particle $i$ gets in lines L5 and L6. Then

$$L^{n+1} - L^n = \frac{1}{\Delta t} \sum_i m_i\, \mathbf x_i^n \times \Delta \mathbf p_i, \qquad L^n = \sum_i m_i \mathbf x_i^n \times \mathbf v_i^n .$$

This is not zero in general, even when every constraint satisfies the hypotheses of Lemmas 3 and 4.

*Proof.* Line L7 gives $\mathbf x^{n+1} = \mathbf x^n + \Delta t \mathbf v^{n+1}$, so $\mathbf x_i^{n+1} \times \mathbf v_i^{n+1} = \mathbf x_i^n \times \mathbf v_i^{n+1}$. Line L3 and the corrections give $\mathbf v_i^{n+1} = \mathbf v_i^n + \Delta \mathbf p_i / \Delta t$. Then $L^{n+1} = \sum m_i \mathbf x_i^n \times \mathbf v_i^{n+1} = L^n + \frac{1}{\Delta t} \sum m_i \mathbf x_i^n \times \Delta \mathbf p_i$. Lemma 4 makes each correction torque-free about the point where it acts, which is $\mathbf p$ and not $\mathbf x^n$.

For the counterexample, take two particles of mass 1 at $(\mp \tfrac12, 0)$ with one distance constraint of rest length 1, spinning at the rate $\omega$: $\mathbf v_{1,2} = (0, \mp \tfrac12 \omega)$ and $L^n = \tfrac12 \omega$. The prediction is $\mathbf p_{1,2} = \pm(\tfrac12, \tfrac12 \omega \Delta t)$ with the sign flipped for particle 1, at the distance $\ell = (1 + (\omega \Delta t)^2)^{1/2}$. By Corollary 2 with equal masses, the projection scales both points by $1/\ell$ about the origin, and later sweeps do nothing. So $\mathbf v_2^{n+1} = (\mathbf p_2/\ell - \mathbf x_2)/\Delta t$, and by symmetry $L^{n+1} = 2\, \mathbf x_2 \times \mathbf v_2^{n+1} = 2 \cdot \tfrac12 \cdot \tfrac12 \omega \Delta t / (\ell \Delta t) = \tfrac12 \omega / \ell$. Hence $L^{n+1}/L^n = (1 + (\omega \Delta t)^2)^{-1/2} < 1$. $\square$

If the gradients are taken at $\mathbf x^n$ instead of at the current $\mathbf p$, as in the SHAKE method of molecular dynamics, every correction is a multiple of $w_i \nabla_i C(\mathbf x^n)$, and the argument of Lemma 4 at $\mathbf x^n$ gives $\sum_i m_i \mathbf x_i^n \times \Delta \mathbf p_i = 0$, so Theorem 7 gives $L^{n+1} = L^n$.

## Stiffness per sweep

**Lemma 8.** Let one constraint have a gradient whose direction does not change under its own projection, for example a distance constraint between a pinned and a free particle. If it is projected $n_s$ times in a row with $k' = 1 - (1 - k)^{1/n_s}$, its value goes from $C_0$ to $(1 - k) C_0$.

*Proof.* By Corollary 2, one projection with $k'$ moves the free particle along the fixed direction by $k'$ times the full correction, so the value becomes $(1 - k') C$. After $n_s$ projections the value is $(1 - k')^{n_s} C_0 = (1 - k) C_0$. $\square$

With several coupled constraints the error after $n_s$ sweeps depends on the coupling, so the effective stiffness depends on the iteration count and on $\Delta t$ (Section 3.3 of the paper says this). This is the problem that XPBD addresses.

## Free motion

**Lemma 9.** With no constraints and no damping, one step is the symplectic Euler step $\mathbf v^{n+1} = \mathbf v^n + \Delta t \mathbf g$, $\mathbf x^{n+1} = \mathbf x^n + \Delta t \mathbf v^{n+1}$.

*Proof.* Lines L1 and L3 compute exactly these two updates, and line L7 gives back the same velocity, since $(\mathbf p - \mathbf x^n)/\Delta t = \mathbf v^n + \Delta t \mathbf g$. $\square$
