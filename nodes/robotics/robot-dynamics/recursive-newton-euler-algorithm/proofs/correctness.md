---
title: The recursive Newton-Euler algorithm returns the inverse dynamics
proves: [correctness]
status: full
---

We use the notation of the page. Body $i$ has the parent $\lambda(i) < i$, and $\lambda(i) = 0$ means the fixed base. The pose of frame $i$ in frame $\lambda(i)$ is $T_{\lambda(i),i}(q_i) = T^{\mathrm{tree}}_i e^{[S_i] q_i}$, where the screw axis $S_i$ is given in the coordinates of frame $i$. $X_i = \mathrm{Ad}(T_{\lambda(i),i}^{-1})$ maps motion vectors from the coordinates of $\lambda(i)$ to the coordinates of $i$, and $X_i^T$ maps force vectors from $i$ to $\lambda(i)$. Every vector of body $i$ is in the coordinates of frame $i$. The operators $\mathrm{crm}$ and $\mathrm{crf}$ are the spatial cross products, with $\mathrm{crf}(v) = -\mathrm{crm}(v)^T$ and $\mathrm{crm}(a) b = -\mathrm{crm}(b) a$.

**Lemma 1 (joint kinematics).** $T_{\lambda(i),i}^{-1} \tfrac{d}{dt} T_{\lambda(i),i} = [S_i]\dot q_i$, and $\tfrac{d}{dt} X_i = -\mathrm{crm}(S_i \dot q_i) X_i$.

*Proof.* Write $T = T^{\mathrm{tree}} E$ with $E = e^{[S_i] q_i}$. Then $\dot T = T^{\mathrm{tree}} E [S_i] \dot q_i$, because $[S_i]$ commutes with $E$, and so $T^{-1}\dot T = [S_i]\dot q_i$. For the second claim, $T(q_i + h)^{-1} = e^{-[S_i] h} T(q_i)^{-1}$. Since $\mathrm{Ad}$ is a group morphism, $X_i(q_i + h) = \mathrm{Ad}(e^{-[S_i] h}) X_i(q_i) = (1 - h\, \mathrm{crm}(S_i) + O(h^2)) X_i(q_i)$, because $\mathrm{crm}(S)$ is the matrix $\mathrm{ad}_S$ of the [Lie bracket](/lie-bracket/). Multiply by $\dot q_i$. $\square$

**Lemma 2 (velocities and accelerations).** Let $v_i$ be the twist of body $i$ and $a_i$ its spatial acceleration, both in frame $i$, and let the base have $v_0 = 0$ and $a_0 = 0$. Then $v_i = X_i v_{\lambda(i)} + S_i \dot q_i$ and $a_i = X_i a_{\lambda(i)} + S_i \ddot q_i + \mathrm{crm}(v_i) S_i \dot q_i$. These are lines L4 and L5.

*Proof.* With $T_{0,i} = T_{0,\lambda(i)} T_{\lambda(i),i}$, the body twist is
$[v_i] = T_{0,i}^{-1}\dot T_{0,i} = T_{\lambda(i),i}^{-1} [v_{\lambda(i)}] T_{\lambda(i),i} + T_{\lambda(i),i}^{-1}\dot T_{\lambda(i),i}$.
The first term is $[X_i v_{\lambda(i)}]$ by the definition of the adjoint map, and the second term is $[S_i]\dot q_i$ by Lemma 1. In body coordinates the components of the spatial acceleration are the time derivatives of the components of the twist, because the extra term of a moving frame is $\mathrm{crm}(v_i) v_i = 0$. So, by Lemma 1,
$a_i = \tfrac{d}{dt}(X_i v_{\lambda(i)}) + S_i \ddot q_i = X_i a_{\lambda(i)} - \mathrm{crm}(S_i \dot q_i) X_i v_{\lambda(i)} + S_i \ddot q_i$.
Now $-\mathrm{crm}(S_i\dot q_i) X_i v_{\lambda(i)} = \mathrm{crm}(X_i v_{\lambda(i)}) S_i \dot q_i = \mathrm{crm}(v_i - S_i\dot q_i) S_i \dot q_i = \mathrm{crm}(v_i) S_i \dot q_i$, since $\mathrm{crm}(S_i)S_i = 0$. $\square$

**Lemma 3 (gravity).** Start the recursion with $a_0 = -a_g$, where $a_g = (0, g)$ is the spatial acceleration of gravity in base coordinates (line L1). Then line L5 gives $a_i - X_{i,0}\,a_g$ in place of $a_i$, where $X_{i,0}$ is the motion transform from the base to frame $i$, and line L6 gives $f^B_i = I_i a_i + \mathrm{crf}(v_i) I_i v_i - I_i X_{i,0} a_g - f^{\mathrm{ext}}_i$.

*Proof.* Lines L4 and L5 are linear in $a_0$, and the term in $a_0$ reaches body $i$ as $X_{i,0} a_0$. The [spatial inertia](/spatial-inertia/) $I_i$ about the origin of frame $i$, applied to the uniform field $X_{i,0} a_g$, gives the wrench of gravity on body $i$: the force $m_i g$ at the center of mass. $\square$

**Lemma 4 (Newton-Euler equations).** The net wrench on body $i$, in frame $i$, is $I_i a_i + \mathrm{crf}(v_i) I_i v_i$. This is the spatial form of the [Newton-Euler equations](/newton-euler-equations/) (Featherstone 2008, Chapter 2).

**Theorem.** Assume ideal joints: the constraint wrench of joint $i$ does no work on the motion $S_i$. Let $f_i$ be the wrench that body $\lambda(i)$ applies to body $i$ through joint $i$, and let $\tau_i = S_i^T f_i$ be the joint force. Then line L10 returns these $\tau_i$, that is $\tau = M(q)\ddot q + C(q, \dot q)\dot q + g(q) - \sum_i J_i^T f^{\mathrm{ext}}_i$.

*Proof.* The forward loop (lines L2 to L6) computes $v_i$ and $a_i$ for $i = 1, \ldots, n$ in order. Every parent has a smaller index, so $v_{\lambda(i)}$ and $a_{\lambda(i)}$ are known when line L4 needs them. By Lemmas 2 and 3, $f^B_i$ after line L6 is the net wrench on body $i$ minus the wrenches of gravity and of the outside world. These are the wrenches that the joints must supply.

The wrenches that the joints apply to body $i$ are $f_i$ from its parent and $-X_c^T f_c$ from each child $c$, by Newton's third law, with $X_c^T$ to change the coordinates. So $f_i - \sum_{c:\, \lambda(c) = i} X_c^T f_c = f^B_i$, that is
$$f_i = f^B_i + \sum_{c:\, \lambda(c) = i} X_c^T f_c.$$
We show by backward induction on $i$ that, when the loop of line L7 reaches $i$, the variable $f_i$ holds this value. Every child $c$ of $i$ has $c > i$, so line L9 has added $X_c^T f_c$ for each child before the loop reaches $i$, and by the induction hypothesis each $f_c$ was complete at that time. Line L9 adds nothing else to $f_i$.

For an ideal joint, $f_i$ is the sum of a constraint wrench $f^c_i$ with $S_i^T f^c_i = 0$ and the wrench of the actuator, and the joint force $\tau_i$ is defined by the power of the actuator, $\tau_i \dot q_i = S_i^T f_i\, \dot q_i$. So line L8 returns the joint force. The map from $\ddot q$ to $\tau$ is affine with the matrix $M(q)$, the rest is $C(q,\dot q)\dot q + g(q)$, and $f^{\mathrm{ext}}$ enters through $J_i^T$, as in the [manipulator equation](/manipulator-equation/). $\blacksquare$

**Cost.** Each of the $n$ steps of each loop does a fixed number of $6 \times 6$ products, so the time is $\Theta(n)$. The extra space is the $n$ transforms and the $n$ vectors $v_i$, $a_i$ and $f_i$, which is $\Theta(n)$.
