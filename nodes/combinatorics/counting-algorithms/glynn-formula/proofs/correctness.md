---
title: GLYNN returns the permanent
proves: [correctness]
status: full
---

Notation: $A = (a_{ij})$ is an $n \times n$ matrix over a commutative ring $R$ in which $2^{n-1}$ is invertible, or over the integers with exact division. $[n] = \{1, \ldots, n\}$ and $\operatorname{per}(A) = \sum_{\pi \in S_n} \prod_{i=1}^{n} a_{i \pi(i)}$. Let $\Delta = \{ \delta \in \{\pm 1\}^n : \delta_1 = 1 \}$, so $|\Delta| = 2^{n-1}$. For $\delta \in \Delta$, let $\sigma(\delta) = \prod_{k=1}^{n} \delta_k$, $c_j(\delta) = \sum_{i=1}^{n} \delta_i a_{ij}$ and $T(\delta) = \sigma(\delta) \prod_{j=1}^{n} c_j(\delta)$. For $k \ge 1$, $\rho(k)$ is the number of trailing zero bits of $k$, and $g(k) = k \oplus \lfloor k/2 \rfloor$.

**Lemma 1 (Glynn's formula).** For $n \ge 1$, $\sum_{\delta \in \Delta} T(\delta) = 2^{n-1} \operatorname{per}(A)$.

*Proof.* Expanding the product of the $n$ sums by distributivity gives, for each $\delta$,

$$\prod_{j=1}^{n} c_j(\delta) = \sum_{f : [n] \to [n]} \prod_{j=1}^{n} \delta_{f(j)} a_{f(j) j},$$

one term for each choice of a row $f(j)$ for each column $j$. For such $f$, let $m_k = |f^{-1}(k)|$ for $k \in [n]$; then $\sum_k m_k = n$ and $\prod_j \delta_{f(j)} = \prod_k \delta_k^{m_k}$. So

$$\sum_{\delta \in \Delta} T(\delta) = \sum_{f : [n] \to [n]} w_f \prod_{j=1}^{n} a_{f(j) j}, \qquad w_f = \sum_{\delta \in \Delta} \prod_{k=1}^{n} \delta_k^{1 + m_k}.$$

The coordinates $\delta_2, \ldots, \delta_n$ range over $\{\pm 1\}$ independently and $\delta_1 = 1$, so the sum factors:

$$w_f = \prod_{k=2}^{n} \left( 1^{1 + m_k} + (-1)^{1 + m_k} \right),$$

and the factor for $k$ is 2 if $m_k$ is odd and 0 if $m_k$ is even. So $w_f = 2^{n-1}$ if $m_2, \ldots, m_n$ are all odd, and $w_f = 0$ otherwise.

*Claim.* $m_2, \ldots, m_n$ are all odd if and only if $f$ is a bijection.

If $f$ is a bijection, every $m_k = 1$, which is odd. Conversely, let $m_2, \ldots, m_n$ be odd. Then each is at least 1, so $\sum_{k=2}^{n} m_k \ge n - 1$ and $m_1 = n - \sum_{k \ge 2} m_k \le 1$. A sum of $n - 1$ odd numbers has the parity of $n - 1$, so $m_1 \equiv n - (n - 1) = 1 \pmod 2$, hence $m_1 = 1$. Then $\sum_{k=2}^{n} m_k = n - 1$ with each term at least 1, so each $m_k = 1$. All $m_k$ equal 1, so $f$ is a bijection. $\square$

A bijection $f$ of $[n]$ with $\prod_j a_{f(j) j}$ is $\pi = f^{-1}$ with $\prod_i a_{i \pi(i)}$, and $f \mapsto f^{-1}$ is a bijection of $S_n$. So the sum equals $2^{n-1} \sum_{\pi \in S_n} \prod_i a_{i \pi(i)} = 2^{n-1} \operatorname{per}(A)$. $\square$

**Lemma 2 (the Gray code).** For $k \ge 1$, $g(k) \oplus g(k - 1) = 2^{\rho(k)}$, and $g(0), g(1), \ldots, g(2^{n-1} - 1)$ are the integers $0, \ldots, 2^{n-1} - 1$, each once.

*Proof.* The map $x \mapsto \lfloor x/2 \rfloor$ acts on each bit position on its own, so $g(x \oplus y) = g(x) \oplus g(y)$. Since $k \oplus (k - 1) = 2^{\rho(k)+1} - 1$, we get $g(k) \oplus g(k - 1) = g(2^{\rho(k)+1} - 1) = (2^{\rho(k)+1} - 1) \oplus (2^{\rho(k)} - 1) = 2^{\rho(k)}$. If $g(x) = g(y)$, then $z = x \oplus y$ satisfies $z = \lfloor z/2 \rfloor$, so $z = 0$. The highest one bit of $g(x)$ is that of $x$, so $g$ maps $[0, 2^{n-1})$ into itself, one to one, hence onto. $\square$

For $0 \le x < 2^{n-1}$, let $\delta(x) \in \Delta$ have $\delta_1 = 1$ and, for $2 \le i \le n$, $\delta_i = -1$ exactly when bit $i - 2$ of $x$ is 1. This is a bijection from $[0, 2^{n-1})$ to $\Delta$.

**Lemma 3 (loop invariant).** For $n \ge 1$ and $0 \le k \le 2^{n-1} - 1$, after line L3 and $k$ passes of the loop of line L4:

1. $\delta = \delta(g(k))$ and $\sigma = \sigma(\delta)$;
2. $c[j] = c_j(\delta)$ for each $j \in [n]$;
3. $\text{total} = \sum_{t=0}^{k} T(\delta(g(t)))$.

*Proof.* By induction on $k$. For $k = 0$: line L2 sets all signs to $+1$, which is $\delta(0) = \delta(g(0))$, and $\sigma = 1$; it sets $c[j] = \sum_i a_{ij} = c_j(\delta(0))$; line L3 sets total $= \prod_j c_j(\delta(0)) = T(\delta(0))$.

Assume the claim after $k - 1$ passes, with $1 \le k \le 2^{n-1} - 1$. Then $\rho(k) \le n - 2$, so line L5 sets a row $i = \rho(k) + 2 \in \{2, \ldots, n\}$. By Lemma 2, $g(k)$ is $g(k - 1)$ with bit $\rho(k) = i - 2$ flipped, so $\delta(g(k))$ is $\delta(g(k - 1))$ with $\delta_i$ negated, which line L6 does; negating one factor negates $\sigma$, which line L6 also does. So (1) holds. Let $\delta_i'$ be the new sign, so the old sign was $-\delta_i'$. For each $j$, the new column sum is the old one minus $(-\delta_i') a_{ij}$ plus $\delta_i' a_{ij}$, that is, the old one plus $2 \delta_i' a_{ij}$, which is line L7. So (2) holds. Line L8 adds $\sigma \prod_j c[j] = T(\delta(g(k)))$, so (3) holds. $\square$

**Theorem.** GLYNN$(A)$ returns $\operatorname{per}(A)$.

*Proof.* If $n = 0$, line L1 returns 1, the permanent of the empty matrix. Let $n \ge 1$. After the last pass, $k = 2^{n-1} - 1$, Lemma 3 (3) gives total $= \sum_{t=0}^{2^{n-1}-1} T(\delta(g(t)))$. By Lemma 2 and the bijection $x \mapsto \delta(x)$, this is $\sum_{\delta \in \Delta} T(\delta)$, which equals $2^{n-1} \operatorname{per}(A)$ by Lemma 1. Over the integers this shows that the division of line L9 is exact. Line L9 returns $\operatorname{per}(A)$. $\blacksquare$
