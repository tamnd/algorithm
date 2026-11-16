---
title: The articulated-body algorithm returns the forward dynamics
proves: [correctness]
status: full
---

We use the notation of the page and of the [recursive Newton-Euler algorithm](/recursive-newton-euler-algorithm/) (RNEA). Body $i$ has the parent $\lambda(i) < i$, and $\nu(i)$ is the set of $i$ and its descendants. For a given $(q, \dot q)$, every velocity $v_i$ is fixed by the first pass. For any vector $\ddot q$, let $a_i(\ddot q)$ be the accelerations of the RNEA with $a_0 = -a_g$, and let $f_i(\ddot q)$ be the wrench that joint $i$ transmits to body $i$, so that $\mathrm{RNEA}(q, \dot q, \ddot q)_i = S_i^T f_i(\ddot q)$. We assume that every body has a positive definite [spatial inertia](/spatial-inertia/) $I_i$.

**Lemma 1 (the transmitted inertia is positive semidefinite).** Let $I^A$ be symmetric positive definite, $U = I^A S$ and $D = S^T U > 0$. Then $I^a = I^A - U U^T / D$ is symmetric positive semidefinite and $I^a S = 0$.

*Proof.* For a vector $x$ and a number $t$, $(x + S t)^T I^A (x + S t) = x^T I^A x + 2 t\, U^T x + t^2 D$. The minimum over $t$ is at $t = -U^T x / D$ and its value is $x^T I^A x - (U^T x)^2/D = x^T I^a x$. A minimum of a nonnegative function is nonnegative. Finally $I^a S = U - U D / D = 0$. $\square$

**Lemma 2 (positive definite articulated inertias).** After the backward pass has finished body $i$, $I^A_i$ is symmetric positive definite, and so $D_i = S_i^T I^A_i S_i > 0$.

*Proof.* Line L5 sets $I^A_i = I_i$, and line L11 adds $X_c^T I^a_c X_c$ for each child $c$. Each child is finished first because $c > i$, so by induction and Lemma 1 each added term is positive semidefinite. A positive definite matrix plus positive semidefinite matrices is positive definite. $\square$

**Lemma 3 (the backward pass).** Fix $i$ and a vector $\ddot q$. Assume that $\tau_k = S_k^T f_k(\ddot q)$ for every $k \in \nu(i)$ with $k \ne i$. Then
$$f_i(\ddot q) = I^A_i\, a_i(\ddot q) + p^A_i ,$$
where $I^A_i$ and $p^A_i$ are the values after the backward pass has finished body $i$.

*Proof.* By backward induction on $i$. By the RNEA, $f_i = I_i a_i + \mathrm{crf}(v_i) I_i v_i - f^{\mathrm{ext}}_i + \sum_{c:\, \lambda(c) = i} X_c^T f_c$. Take a child $c$. The hypothesis holds for $c$ too, so by induction $f_c = I^A_c a_c + p^A_c$. By Lemma 2 of the RNEA proof, $a_c = a'_c + S_c \ddot q_c$ with $a'_c = X_c a_i + c_c$, where $c_c = \mathrm{crm}(v_c) S_c \dot q_c$ is line L4. The joint equation of $c$ is then
$$\tau_c = S_c^T \big(I^A_c (a'_c + S_c \ddot q_c) + p^A_c\big) = U_c^T a'_c + D_c \ddot q_c + S_c^T p^A_c ,$$
with $U_c = I^A_c S_c$ and $D_c = S_c^T U_c$, because $I^A_c$ is symmetric. $D_c > 0$ by Lemma 2, so
$$\ddot q_c = (u_c - U_c^T a'_c)/D_c, \qquad u_c = \tau_c - S_c^T p^A_c .$$
These are the quantities of line L7. Put this $\ddot q_c$ back into $f_c$:
$$f_c = I^A_c a'_c + U_c (u_c - U_c^T a'_c)/D_c + p^A_c = I^a_c a'_c + p^A_c + U_c u_c / D_c = I^a_c X_c a_i + p^a_c ,$$
with $I^a_c = I^A_c - U_c U_c^T / D_c$ (line L9) and $p^a_c = p^A_c + I^a_c c_c + U_c u_c / D_c$ (line L10). So $X_c^T f_c = X_c^T I^a_c X_c\, a_i + X_c^T p^a_c$. Summing over the children,
$$f_i = \Big(I_i + \sum_c X_c^T I^a_c X_c\Big) a_i + \Big(\mathrm{crf}(v_i) I_i v_i - f^{\mathrm{ext}}_i + \sum_c X_c^T p^a_c\Big).$$
Line L5 starts $I^A_i$ and $p^A_i$ at the first terms, and line L11 adds the sums. A leaf has no children, and the formula is line L5 alone. $\square$

**Theorem.** Line L17 returns the unique $\ddot q$ with $\mathrm{RNEA}(q, \dot q, \ddot q) = \tau$, that is $\ddot q = M(q)^{-1}\big(\tau - C(q,\dot q)\dot q - g(q) + \sum_i J_i^T f^{\mathrm{ext}}_i\big)$.

*Proof.* $M(q)$ is positive definite (see the proof of the [composite rigid body algorithm](/composite-rigid-body-algorithm/)), so there is exactly one solution $\ddot q^*$. For $\ddot q^*$, every joint equation holds, so Lemma 3 applies to every body, and the argument in its proof gives, for every $i$,
$$\ddot q^*_i = (u_i - U_i^T a'_i)/D_i, \qquad a'_i = X_i a_{\lambda(i)}(\ddot q^*) + c_i .$$
The right side uses only $\ddot q^*_k$ for the ancestors $k$ of $i$, through $a_{\lambda(i)}$. The forward pass of lines L12 to L16 evaluates the same formulas in the order $i = 1, \ldots, n$, starting from the same $a_0 = -a_g$. By induction on $i$, line L14 computes $a'_i$, line L15 computes $\ddot q_i = \ddot q^*_i$, and line L16 computes $a_i(\ddot q^*)$. $\blacksquare$

**Cost.** Every line does a fixed number of operations on $6 \times 6$ matrices and 6-vectors, and each pass visits each body once. The time is $\Theta(n)$, and the extra space is $\Theta(n)$ for $X_i$, $v_i$, $c_i$, $I^A_i$, $p^A_i$, $U_i$, $D_i$ and $u_i$.

**Massless bodies.** Lemma 2 needs a positive definite $I_i$. With a body of zero mass, such as an inner body of a floating base modelled by six joints, $D_i$ can still be positive through the inertia of the subtree. The implementation checks $D_i > 0$ and raises an error otherwise.
