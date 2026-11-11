---
title: Regev decryption returns the bit when the error sum is below q/4
proves: [correctness]
status: full
---

Fix $q \ge 4$, and write $a = \lfloor q/4 \rfloor$ and $h = \lfloor q/2 \rfloor$. Let $(A, b = A s + e \bmod q)$ be a public key from lines L1 to L4, let $x \in \{0,1\}^m$ be the coins of line L5, and let $E = x^\mathsf{T} e$, an integer.

**Lemma 1 (the decryption value).** For the ciphertext $(u, v)$ of lines L6 to L8, line L9 computes $d = (E + \mu h) \bmod q$.

*Proof.* Modulo $q$, $\langle u, s \rangle \equiv x^\mathsf{T} A s$ by line L6, and $v \equiv x^\mathsf{T} b + \mu h \equiv x^\mathsf{T} A s + x^\mathsf{T} e + \mu h$ by lines L3 and L7. So $v - \langle u, s \rangle \equiv E + \mu h \pmod q$, and line L9 takes the representative in $[0, q-1]$. $\square$

**Lemma 2 (two facts on the rounding).** $2a \le h$ and $h + 2a \le q$.

*Proof.* $2a = 2\lfloor q/4 \rfloor \le \lfloor 2 \cdot q/4 \rfloor = h$, because $2 \lfloor y \rfloor$ is an integer at most $2y$. Then $h + 2a \le 2h \le q$. $\square$

**Theorem.** If $|E| < a$, line L10 returns $\mu$.

*Proof.* Line L10 returns 1 exactly when $a < d < q - a$.

Case $\mu = 0$. If $0 \le E < a$, then $d = E < a$, so line L10 returns 0. If $-a < E < 0$, then $d = q + E$, and $q - a < d < q$, so line L10 returns 0.

Case $\mu = 1$. The integer $E + h$ satisfies $E + h > -a + h \ge -a + 2a = a$ by Lemma 2, so $E + h > a \ge 0$. It also satisfies $E + h < a + h \le q - a$ by Lemma 2. So $E + h$ lies in $[0, q-1]$, hence $d = E + h$, and $a < d < q - a$. Line L10 returns 1. $\blacksquare$

**When the condition holds.** $|E| \le \sum_i |e_i| \le m \max_i |e_i|$, so a deterministic sufficient condition is $m \max_i |e_i| < \lfloor q/4 \rfloor$. With the rounded Gaussian errors of the paper, the $e_i$ are independent with mean 0 and standard deviation about $\alpha q / \sqrt{2\pi}$, and $E$ is a sum of at most $m$ of them. A tail bound for this sum shows that $|E| < \lfloor q/4 \rfloor$ fails only with probability negligible in $n$ when $\alpha \sqrt{m} = o(1/\sqrt{\log n})$, which holds for $\alpha = 1/(\sqrt{n}\log^2 n)$ and $m = O(n \log n)$. This part is a probability statement on the key and the coins, and the paper proves it in its correctness lemma; the theorem above is the exact rounding step that it uses.
