---
title: Correctness of Williams' p+1 algorithm
proves: [correctness, termination]
status: full
---

Fix an integer $A$. The Lucas sequence is $V_0 = 2$, $V_1 = A$, $V_{j+1} = A V_j - V_{j-1}$, and we write $V_j(A)$ for its terms. Work in the ring $R = \mathbb Z[t]/(t^2 - At + 1)$, a free $\mathbb Z$-module with basis $1, t$, so that $\mathbb Z$ is a subring of $R$. Put $\tau = t$ and $\sigma = A - t$. Then $\tau + \sigma = A$ and $\tau\sigma = At - t^2 = 1$.

**Lemma 1.** $V_j(A) = \tau^j + \sigma^j$ in $R$ for all $j \ge 0$.

*Proof.* Both $\tau$ and $\sigma$ are roots of $X^2 - AX + 1$ (for $\sigma$: $\sigma^2 - A\sigma + 1 = \sigma(\sigma - A) + 1 = -\sigma\tau + 1 = 0$). So $W_j = \tau^j + \sigma^j$ satisfies $W_{j+1} = A W_j - W_{j-1}$, and $W_0 = 2$, $W_1 = A$. By induction $W_j = V_j(A)$. $\square$

**Lemma 2 (doubling rules).** For $j \ge 1$: $V_{2j} = V_j^2 - 2$ and $V_{2j+1} = V_j V_{j+1} - A$.

*Proof.* By Lemma 1 and $\tau\sigma = 1$: $(\tau^j + \sigma^j)^2 = \tau^{2j} + \sigma^{2j} + 2$, and $(\tau^j + \sigma^j)(\tau^{j+1} + \sigma^{j+1}) = \tau^{2j+1} + \sigma^{2j+1} + \tau^j\sigma^j(\sigma + \tau) = V_{2j+1} + A$. $\square$

**Lemma 3 (composition).** For $k, m \ge 1$: $V_m(V_k(A)) = V_{mk}(A)$.

*Proof.* Let $w = V_k(A) = \tau^k + \sigma^k$. The elements $\tau^k, \sigma^k$ satisfy $\tau^k\sigma^k = 1$ and $\tau^k + \sigma^k = w$, so both are roots of $X^2 - wX + 1$. As in Lemma 1, $\tau^{kj} + \sigma^{kj}$ satisfies the recurrence of the Lucas sequence with seed $w$ and the same first two terms $2, w$; so it equals $V_j(w)$. With $j = m$ and Lemma 1, $V_m(w) = \tau^{km} + \sigma^{km} = V_{km}(A)$. $\square$

All these are identities between integers built from $A$ by sums and products, so they also hold modulo $N$, with $A$ replaced by any integer congruent to it.

**Lemma 4 (LUCAS-V).** LUCAS-V$(v, m, N)$ returns $V_m(v) \bmod N$ for $m \ge 1$.

*Proof.* Write $m$ in binary with leading digit $1$, and let $j$ be the number formed by the digits read so far, so $j = 1$ before the loop of line K2. The invariant is $x \equiv V_j(v)$ and $y \equiv V_{j+1}(v) \pmod N$. It holds after line K1, since $V_2 = v^2 - 2$. If the next digit is $1$, the new $j$ is $2j + 1$, and line K3 sets $x$ to $V_j V_{j+1} - v = V_{2j+1}$ and $y$ to $V_{j+1}^2 - 2 = V_{2j+2}$, by Lemma 2 (for $y$, applied to $j + 1$), both from the old values. If the digit is $0$, the new $j$ is $2j$, and line K4 sets $x$ to $V_j^2 - 2 = V_{2j}$ and $y$ to $V_j V_{j+1} - v = V_{2j+1}$. After all digits, $j = m$, and line K5 returns $V_m(v) \bmod N$. The loop has one pass per digit, so it ends. $\square$

**Lemma 5 (the main loop).** After line L4 has run for the primes $q_1 < \dots < q_i$, with powers $Q_1, \dots, Q_i$, $v \equiv V_{Q_1 \cdots Q_i}(A) \pmod N$. At the end, $v \equiv V_M(A)$.

*Proof.* Before the loop, $v = A = V_1(A)$. If $v \equiv V_k(A)$, then line L4 makes $v \equiv V_{Q}(V_k(A)) = V_{Qk}(A)$ by Lemmas 4 and 3. Induction on $i$ gives the claim, and the product of all $Q$ is $M$. The loop is over the finitely many primes up to $B$, so it ends. $\square$

**Lemma 6 (the key congruence).** Let $p$ be an odd prime that does not divide $D = A^2 - 4$, and let $\varepsilon = (D/p)$. Then $V_j(A) \equiv 2 \pmod p$ for every multiple $j$ of $p - \varepsilon$.

*Proof.* Let $f = X^2 - AX + 1$ over $\mathbb F_p$. Its discriminant is $D \not\equiv 0$.

If $\varepsilon = 1$, then $D \equiv s^2$ for some $s \not\equiv 0$, and $f$ has the roots $\alpha = (A + s)/2$ and $\beta = (A - s)/2$ in $\mathbb F_p$ (here $p$ is odd, so $2$ is invertible). They satisfy $\alpha\beta = (A^2 - s^2)/4 = 1$, so both are nonzero, and by [Fermat's little theorem](/fermat-little-theorem/) $\alpha^{p-1} = \beta^{p-1} = 1$.

If $\varepsilon = -1$, then $f$ has no root in $\mathbb F_p$, so it is irreducible and $K = \mathbb F_p[X]/(f)$ is a field with $p^2$ elements. Let $\alpha$ be the class of $X$ and $\beta = A - \alpha$; then $\alpha\beta = 1$. The map $z \mapsto z^p$ is a ring homomorphism of $K$ that fixes $\mathbb F_p$, so $f(\alpha^p) = f(\alpha)^p = 0$, and $\alpha^p$ is a root of $f$. The roots of $f$ in the field $K$ are $\alpha$ and $\beta$. If $\alpha^p = \alpha$, then $\alpha$ would be a root of $Z^p - Z$, whose $p$ roots in $K$ are the elements of $\mathbb F_p$, and $\alpha \notin \mathbb F_p$. So $\alpha^p = \beta$ and $\alpha^{p+1} = \alpha\beta = 1$, and also $\beta^{p+1} = (\alpha^{-1})^{p+1} = 1$.

In both cases there is a ring homomorphism from $R$ to a field of characteristic $p$ that sends $t$ to $\alpha$ (since $f(\alpha) = 0$), and so $\sigma = A - t$ to $\beta$. By Lemma 1, $V_j(A) \bmod p$ is $\alpha^j + \beta^j$. With $\alpha^{p-\varepsilon} = \beta^{p-\varepsilon} = 1$, every multiple $j$ of $p - \varepsilon$ gives $\alpha^j + \beta^j = 2$. $\square$

**Theorem.** WILLIAMS-P-PLUS-1$(N, B, A)$ ends and returns a divisor $g$ of $N$. If an odd prime $p \mid N$ does not divide $A^2 - 4$ and $p - (D/p)$ divides $M$, then $p \mid g$. If moreover some prime power $r^f$ that divides $N$ has $V_M(A) \not\equiv 2 \pmod{r^f}$, then $1 < g < N$.

*Proof.* The loops end by Lemmas 4 and 5. The value $g = \gcd(v - 2, N)$ divides $N$. By Lemma 5, $v \equiv V_M(A) \pmod N$, so $v - 2 \equiv V_M(A) - 2 \pmod p$ for every $p \mid N$. Under the hypothesis on $p$, Lemma 6 with $j = M$ gives $p \mid v - 2$, so $p \mid g$ and $g > 1$. If $r^f \mid N$ and $r^f \nmid V_M(A) - 2$, then $r^f \nmid v - 2$, so $r^f \nmid g$ and $g \ne N$. $\blacksquare$
