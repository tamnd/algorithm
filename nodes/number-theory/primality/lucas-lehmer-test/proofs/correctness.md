---
title: The Lucas-Lehmer test returns true exactly when 2^p - 1 is prime
proves: [correctness, termination]
status: full
---

We use the pseudocode LUCAS-LEHMER$(p)$ of the page, for an integer $p \ge 2$, with $M_p = 2^p - 1$. Define the integers $s_0 = 4$ and $s_{i+1} = s_i^2 - 2$.

**Termination.** The loop of line L4 runs $p - 2$ times, and each pass does one squaring and one reduction. So the call ends.

**Lemma 1 (the loop computes $s_{p-2}$).** For $p \ge 3$, after the $i$-th pass of line L5, $s \equiv s_i \pmod{M_p}$. So line L6 returns true if and only if $M_p \mid s_{p-2}$.

*Proof.* Before the loop $s = 4 = s_0$, and $4 < M_p$ as $p \ge 3$. If $s \equiv s_i$, then $s^2 - 2 \equiv s_i^2 - 2 = s_{i+1}$, and line L5 keeps the residue. After $p - 2$ passes, $s$ is the residue of $s_{p-2}$ in $[0, M_p)$, which is 0 if and only if $M_p \mid s_{p-2}$. $\square$

**The ring.** For an odd prime $q$, let $R_q = \mathbb{Z}_q[x]/(x^2 - 3)$, and write $\sqrt 3$ for the class of $x$. Its elements are $a + b\sqrt 3$ with $a, b \in \mathbb{Z}_q$, so $|R_q| = q^2$, and the units of $R_q$ number at most $q^2 - 1$, since 0 is not a unit. Put $\omega = 2 + \sqrt 3$ and $\bar\omega = 2 - \sqrt 3$. Then $\omega \bar\omega = 4 - 3 = 1$, so both are units and $\bar\omega = \omega^{-1}$.

**Lemma 2 (closed form).** In $R_q$, the image of $s_i$ is $\omega^{2^i} + \bar\omega^{2^i}$ for each $i \ge 0$.

*Proof.* For $i = 0$, $\omega + \bar\omega = 4$. If the claim holds for $i$, then $s_{i+1} = s_i^2 - 2 = \omega^{2^{i+1}} + 2(\omega\bar\omega)^{2^i} + \bar\omega^{2^{i+1}} - 2 = \omega^{2^{i+1}} + \bar\omega^{2^{i+1}}$. $\square$

**Lemma 3 (if $M_p \mid s_{p-2}$, then $M_p$ is prime).** Let $p \ge 3$ and $M_p \mid s_{p-2}$. Then $M_p$ is prime.

*Proof.* Suppose $M_p$ is composite, and let $q$ be its smallest prime factor. Then $q^2 \le M_p$, and $q$ is odd since $M_p$ is odd. As $q \mid s_{p-2}$, Lemma 2 gives $\omega^{2^{p-2}} + \bar\omega^{2^{p-2}} = 0$ in $R_q$. Multiplying by $\omega^{2^{p-2}}$ and using $\omega\bar\omega = 1$ gives $\omega^{2^{p-1}} + 1 = 0$, so $\omega^{2^{p-1}} = -1$ and $\omega^{2^p} = 1$. Since $q$ is odd, $-1 \ne 1$ in $R_q$, so the order of $\omega$ in the unit group divides $2^p$ but not $2^{p-1}$, and it is $2^p$. The order of an element is at most the size of the group, so $2^p \le q^2 - 1 \le M_p - 1 = 2^p - 2$, which is false. $\square$

**Lemma 4 (residue facts).** Let $p \ge 3$ and let $q = M_p$ be prime. Then $p$ is odd, $q \equiv 7 \pmod 8$ and $q \equiv 1 \pmod 3$. Hence 2 is a quadratic residue modulo $q$ and 3 is not.

*Proof.* If $p$ were even, $3 = 2^2 - 1$ would divide $2^p - 1$, and $q > 3$; so $p$ is odd. As $p \ge 3$, $2^p \equiv 0 \pmod 8$, so $q \equiv -1 \equiv 7 \pmod 8$. As $p$ is odd, $2^p \equiv (-1)^p = -1 \equiv 2 \pmod 3$, so $q \equiv 1 \pmod 3$. By the second supplement of quadratic reciprocity, 2 is a residue modulo $q$ because $q \equiv \pm 1 \pmod 8$. Since $q \equiv 3 \pmod 4$ and $3 \equiv 3 \pmod 4$, quadratic reciprocity gives $\left(\frac{3}{q}\right) = -\left(\frac{q}{3}\right) = -\left(\frac{1}{3}\right) = -1$. $\square$

**Lemma 5 (if $M_p$ is prime, then $M_p \mid s_{p-2}$).** Let $p \ge 3$ and let $q = M_p$ be prime. Then $q \mid s_{p-2}$.

*Proof.* By Lemma 4, $x^2 - 3$ has no root modulo $q$, so it is irreducible over $\mathbb{Z}_q$ and $R_q$ is a field with $q^2$ elements. In it, $u \mapsto u^q$ is a ring homomorphism (the binomial coefficients $\binom{q}{j}$ with $0 < j < q$ vanish), it fixes $\mathbb{Z}_q$ by Fermat's little theorem, and $(\sqrt 3)^q = 3^{(q-1)/2} \sqrt 3 = -\sqrt 3$ by Euler's criterion and Lemma 4. So $(a + b\sqrt 3)^q = a - b\sqrt 3$.

Let $\tau = 1 + \sqrt 3$. Then $\tau^2 = 4 + 2\sqrt 3 = 2\omega$, and $\tau^{q+1} = \tau \cdot \tau^q = (1 + \sqrt 3)(1 - \sqrt 3) = -2$. On the other hand, $\tau^{q+1} = (\tau^2)^{(q+1)/2} = 2^{(q+1)/2} \omega^{(q+1)/2}$, and $2^{(q+1)/2} = 2 \cdot 2^{(q-1)/2} = 2$ by Euler's criterion, since 2 is a residue. Hence $2\omega^{(q+1)/2} = -2$, and as $2$ is invertible, $\omega^{(q+1)/2} = -1$. Here $(q + 1)/2 = 2^{p-1}$. So $\omega^{2^{p-1}} = -1$, and

$$s_{p-2} = \omega^{2^{p-2}} + \bar\omega^{2^{p-2}} = \bar\omega^{2^{p-2}} \left(\omega^{2^{p-1}} + 1\right) = 0$$

in $R_q$, using $\omega^{2^{p-2}} = \bar\omega^{2^{p-2}} \omega^{2^{p-1}}$. As $s_{p-2}$ is an integer whose image in $R_q$ is 0, $q \mid s_{p-2}$. $\square$

**Theorem.** For each integer $p \ge 2$, LUCAS-LEHMER$(p)$ returns true if and only if $M_p$ is prime.

*Proof.* For $p = 2$, line L1 returns true, and $M_2 = 3$ is prime. For $p \ge 3$, by Lemma 1 the call returns true if and only if $M_p \mid s_{p-2}$. By Lemma 3 this implies that $M_p$ is prime, and by Lemma 5 it follows from it. $\blacksquare$

**Remark.** Lemma 3 does not use that $p$ is prime. So for a composite $p \ge 4$ the test returns false, which is right because $M_p$ is then composite.
