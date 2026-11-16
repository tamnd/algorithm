---
title: The differentiated Newton-Euler recursion returns the partial derivatives of the dynamics
proves: [correctness]
status: full
---

We use the notation of the page and of the [recursive Newton-Euler algorithm](/recursive-newton-euler-algorithm/) (RNEA). Body $i$ has the parent $\lambda(i) < i$. $\mathrm{anc}(i)$ is the set of $i$ and its ancestors, and $\nu(i)$ is the set of $i$ and its descendants. We write $\partial_k$ for the partial derivative by one coordinate $u_k$, where $u$ is $q$, $\dot q$ or $\ddot q$. The operators satisfy $\mathrm{crm}(a) b = -\mathrm{crm}(b) a$ and $\mathrm{crf}(a) = -\mathrm{crm}(a)^T$.

**Lemma 1 (the two identities).** For a motion vector $m$ and a force vector $f$ that do not depend on $q_i$,
$$\frac{\partial (X_i m)}{\partial q_i} = \mathrm{crm}(X_i m)\, S_i, \qquad \frac{\partial (X_i^T f)}{\partial q_i} = X_i^T\, \mathrm{crf}(S_i)\, f .$$

*Proof.* The joint pose is $T(q_i) = T^{\mathrm{tree}}_i e^{[S_i] q_i}$, so $T(q_i + h)^{-1} = e^{-[S_i] h} T(q_i)^{-1}$ and $X_i(q_i + h) = \mathrm{Ad}(e^{-[S_i]h}) X_i(q_i)$. The derivative at $h = 0$ is $\partial X_i / \partial q_i = -\mathrm{crm}(S_i) X_i$. Then $\partial(X_i m)/\partial q_i = -\mathrm{crm}(S_i) X_i m = \mathrm{crm}(X_i m) S_i$. For the second identity, $\partial X_i^T / \partial q_i = -X_i^T \mathrm{crm}(S_i)^T = X_i^T \mathrm{crf}(S_i)$. $\square$

**Lemma 2 (dependence).** $v_i$ and $a_i$ depend only on $q_k$, $\dot q_k$ and $\ddot q_k$ with $k \in \mathrm{anc}(i)$. The joint wrench $f_i$ and $\tau_i$ depend only on the coordinates of joints $k$ with $k \in \mathrm{anc}(i)$ or $k \in \nu(i)$.

*Proof.* Lines L4 and L5 of the RNEA use only the parent, so the first claim follows by induction on $i$. The body wrench $f^B_l$ depends on the coordinates of $\mathrm{anc}(l)$, and $f_i$ adds the $f^B_l$ of $l \in \nu(i)$ through transforms of joints in $\nu(i)$. A joint $k$ in $\mathrm{anc}(l)$ for some $l \in \nu(i)$ is in $\mathrm{anc}(i)$ or in $\nu(i)$. $\square$

So every derivative that the algorithm does not store in a dict is 0.

**Lemma 3 (the forward pass).** After line L7 for body $i$, the dicts hold, for every $k \in \mathrm{anc}(i)$, the derivatives $\partial_k v_i$, $\partial_k a_i$ and $\partial_k f^B_i$ by $q_k$, by $\dot q_k$ and by $\ddot q_k$.

*Proof.* By induction on $i$. Differentiate the RNEA lines $v_i = X_i v_{\lambda} + S_i \dot q_i$, $a_i = X_i a_{\lambda} + S_i \ddot q_i + \mathrm{crm}(v_i) S_i \dot q_i$ and $f^B_i = I_i a_i + \mathrm{crf}(v_i) I_i v_i$, where $\lambda = \lambda(i)$.

- For $k \in \mathrm{anc}(\lambda)$, $X_i$, $q_i$ and $\dot q_i$ do not change with $u_k$, so $\partial_k (X_i v_\lambda) = X_i\, \partial_k v_\lambda$ and the same for $a$. This is line L3, with the dicts of the parent from the induction hypothesis.
- For $k = i$ and $u = q$: $v_\lambda$ and $a_\lambda$ do not depend on $q_i$, so Lemma 1 gives $\partial_i (X_i v_\lambda) = \mathrm{crm}(X_i v_\lambda) S_i$ and $\partial_i (X_i a_\lambda) = \mathrm{crm}(X_i a_\lambda) S_i$. This is line L4.
- For $k = i$ and $u = \dot q$: $\partial_i v_i = S_i$, and the last term of $a_i$ gives $\mathrm{crm}(v_i) S_i$ from the factor $\dot q_i$. This is line L5. For $u = \ddot q$: $\partial_i a_i = S_i$.
- For every $k$ and $u \in \{q, \dot q\}$, the last term of $a_i$ also gives $\mathrm{crm}(\partial_k v_i) S_i \dot q_i$. This is line L6. For $k = i$ and $u = \dot q$ this term is $\mathrm{crm}(S_i) S_i \dot q_i = 0$, so it does no harm.
- The product rule on $f^B_i$ gives $\partial_k f^B_i = I_i\, \partial_k a_i + \mathrm{crf}(\partial_k v_i) I_i v_i + \mathrm{crf}(v_i) I_i\, \partial_k v_i$. This is line L7. For $u = \ddot q$ the velocities do not change, and only $I_i\, \partial_k a_i$ is left. $\square$

**Theorem.** Line L14 returns $\tau = \mathrm{RNEA}(q, \dot q, \ddot q)$, $\partial \tau / \partial q$, $\partial \tau / \partial \dot q$ and $\partial \tau / \partial \ddot q = M(q)$.

*Proof.* The value $\tau$ is the RNEA (its correctness proof applies line by line). The backward pass of the RNEA computes $f_i = f^B_i + \sum_{c:\, \lambda(c) = i} X_c^T f_c$ and $\tau_i = S_i^T f_i$. Differentiate:
$$\partial_k f_i = \partial_k f^B_i + \sum_c \Big( X_c^T\, \partial_k f_c + [k = c]\,[u = q]\; X_c^T\, \mathrm{crf}(S_c) f_c \Big),$$
by the product rule and Lemma 1, because $X_c$ depends on $q_c$ only. We show by backward induction on $i$ that, when the loop of line L8 reaches $i$, the dicts of $f_i$ hold $\partial_k f_i$ for every $k$ allowed by Lemma 2, and $f_i$ is complete. The dicts start with $\partial_k f^B_i$ by Lemma 3. Each child $c > i$ was handled before $i$; at that time $f_c$ and its dicts were complete by the induction hypothesis, and lines L11 to L13 added the three terms of the sum. Nothing else changes these values.

Then $\partial_k \tau_i = S_i^T\, \partial_k f_i$ because $S_i$ is constant, which is line L9. Every entry that the dicts do not hold is 0 by Lemma 2, and the output matrices start at 0. Since $\tau$ is affine in $\ddot q$ with the matrix $M(q)$, $\partial\tau/\partial\ddot q = M(q)$. $\blacksquare$

**Corollary (forward dynamics).** Let $\mathrm{FD}(q, \dot q, \tau)$ be the solution $\ddot q$ of $\mathrm{RNEA}(q, \dot q, \ddot q) = \tau$. Then, at $\ddot q = \mathrm{FD}(q, \dot q, \tau)$,
$$\frac{\partial \mathrm{FD}}{\partial q} = -M^{-1} \frac{\partial \mathrm{RNEA}}{\partial q}, \qquad \frac{\partial \mathrm{FD}}{\partial \dot q} = -M^{-1} \frac{\partial \mathrm{RNEA}}{\partial \dot q}, \qquad \frac{\partial \mathrm{FD}}{\partial \tau} = M^{-1}.$$

*Proof.* The identity $\mathrm{RNEA}(q, \dot q, \mathrm{FD}(q, \dot q, \tau)) = \tau$ holds for all arguments. Differentiate it by $q$ with the chain rule: $\partial \mathrm{RNEA}/\partial q + M\, \partial \mathrm{FD}/\partial q = 0$. The same holds for $\dot q$. By $\tau$: $M\, \partial \mathrm{FD}/\partial \tau = 1$. $M$ is invertible because it is positive definite. $\blacksquare$

**Cost.** For body $i$ the dicts of the forward pass have $\mathrm{depth}(i)$ entries, and each entry costs a fixed number of $6 \times 6$ products. In the backward pass, the dict of $f_i$ holds the joints of $\mathrm{anc}(i)$ and $\nu(i)$, and each entry is moved once to the parent. The sum over all bodies of these sizes is the number of pairs $(i, k)$ on a common path, which is at most $2 \sum_i \mathrm{depth}(i)$. So the time is $O(n d)$ for a tree of depth $d$ and $\Theta(n^2)$ for a serial chain.
