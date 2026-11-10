---
title: Two distinct keys collide under a random dot-product hash with probability exactly 1/p
proves: [correctness]
status: full
---

**Setting.** Let $p$ be a prime and $r \ge 1$. Keys are vectors $x = (x_0, \ldots, x_{r-1})$ in $\mathbb{Z}_p^r$, and all arithmetic is in the field $\mathbb{Z}_p$. For $a \in \mathbb{Z}_p^r$ let $h_a(x) = \sum_i a_i x_i$, and for $b \in \mathbb{Z}_p$ let $g_{a,b}(x) = h_a(x) + b$. The vector $a$ is uniform on $\mathbb{Z}_p^r$, and $b$ is uniform on $\mathbb{Z}_p$ and independent of $a$.

**Statement.**

1. For all keys $x \ne y$, $\Pr_a[h_a(x) = h_a(y)] = 1/p$. So $\{h_a\}$ is a universal family with $p$ slots.
2. For all keys $x \ne y$ and all slots $s, t \in \mathbb{Z}_p$, $\Pr_{a,b}[g_{a,b}(x) = s \text{ and } g_{a,b}(y) = t] = 1/p^2$. So $\{g_{a,b}\}$ is strongly universal (pairwise independent).
3. Lines L2 to L5 of the pseudocode compute $h_a(x)$.

**Lemma (one free coordinate).** Let $d \in \mathbb{Z}_p^r$ with $d \ne 0$, and let $c \in \mathbb{Z}_p$. Exactly $p^{r-1}$ vectors $a \in \mathbb{Z}_p^r$ satisfy $\sum_i a_i d_i = c$.

*Proof.* Pick $j$ with $d_j \ne 0$. Since $p$ is a prime, $d_j$ has an inverse $d_j^{-1}$ in $\mathbb{Z}_p$. Fix the $r - 1$ coordinates $a_i$ with $i \ne j$ in any of $p^{r-1}$ ways. The equation becomes $a_j d_j = c - \sum_{i \ne j} a_i d_i$, and it has exactly one solution $a_j = d_j^{-1}\big(c - \sum_{i \ne j} a_i d_i\big)$. So each choice of the other coordinates extends to exactly one solution. $\square$

**Proof of 1.** Put $d = x - y$, which is not $0$ because $x \ne y$. By linearity, $h_a(x) = h_a(y)$ exactly when $\sum_i a_i d_i = 0$. By the lemma with $c = 0$, this holds for $p^{r-1}$ of the $p^r$ equally likely vectors $a$, so the probability is $p^{r-1}/p^r = 1/p$.

**Proof of 2.** The two conditions $h_a(x) + b = s$ and $h_a(y) + b = t$ hold together exactly when $\sum_i a_i d_i = s - t$ with $d = x - y$, and $b = s - h_a(x)$. By the lemma with $c = s - t$, the first condition holds for $p^{r-1}$ vectors $a$, and for each of them exactly one $b$ satisfies the second. So $p^{r-1}$ of the $p^{r+1}$ equally likely pairs $(a, b)$ give the values $(s, t)$, and the probability is $1/p^2$.

**Proof of 3.** The loop keeps the invariant $s = \sum_{i' < i} a_{i'} x_{i'}$ in $\mathbb{Z}_p$ before the iteration for index $i$: it holds with $s = 0$ for $i = 0$, and line L4 adds the next term modulo $p$. After the last iteration $s = h_a(x)$, which line L5 returns. The loop runs $r$ times, so it ends. $\blacksquare$

**Remark (why the modulus must be a prime).** The lemma uses an inverse of $d_j$. Modulo a composite $q$ it can fail: for $q = 4$, $r = 1$ and the keys $0$ and $2$, the equation $2a \equiv 0 \pmod 4$ holds for $a \in \{0, 2\}$, so the keys collide with probability $1/2$, not $1/4$.
