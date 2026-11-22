---
title: SYN cookies accept every recent real ACK and almost no forged one
proves: [correctness]
status: full
---

We use the names of the main block. A cookie is a 32-bit integer. The counter $t$ is a non-negative integer, $m \in \{0, \ldots, 7\}$, $0 \le A < 32$, and $h_K(c, t) = F_K(c, t) \bmod 2^{24}$.

**Lemma 1 (fields).** Let $y = $ MAKE-COOKIE$(K, c, t, m)$. Then $0 \le y < 2^{32}$, $\lfloor y / 2^{27} \rfloor = t \bmod 32$, $\lfloor y / 2^{24} \rfloor \bmod 8 = m$ and $y \bmod 2^{24} = h_K(c, t)$.

*Proof.* Line L2 returns $y = (t \bmod 32) \cdot 2^{27} + m \cdot 2^{24} + h$ with $0 \le t \bmod 32 \le 31$, $0 \le m \le 7$ and $0 \le h < 2^{24}$ by line L1. So $0 \le y \le 31 \cdot 2^{27} + 7 \cdot 2^{24} + 2^{24} - 1 = 2^{32} - 1$. Since $m \cdot 2^{24} + h < 8 \cdot 2^{24} = 2^{27}$, the quotient of $y$ by $2^{27}$ is $t \bmod 32$. Since $h < 2^{24}$, the quotient of $y$ by $2^{24}$ is $(t \bmod 32) \cdot 8 + m$, and its residue mod 8 is $m$. The residue of $y$ mod $2^{24}$ is $h$. $\square$

**Lemma 2 (the counter).** Let $t_5 \in \{0, \ldots, 31\}$ and let $t' = now - ((now - t_5) \bmod 32)$, as in line L5. Then $t' \equiv t_5 \pmod{32}$ and $now - 31 \le t' \le now$. It is the only integer with both properties.

*Proof.* Let $r = (now - t_5) \bmod 32$, so $0 \le r \le 31$ and $now - t_5 - r$ is a multiple of 32. Then $t' = now - r$ lies in $[now - 31, now]$, and $t' - t_5 = now - t_5 - r \equiv 0 \pmod{32}$. Two integers in an interval of 32 consecutive integers that are congruent mod 32 are equal, so $t'$ is unique. $\square$

**Theorem, part 1 (completeness).** If $0 \le now - t \le A$, then CHECK-COOKIE$(K, c, (y + 1) \bmod 2^{32}, now, A)$ with $y = $ MAKE-COOKIE$(K, c, t, m)$ returns ACCEPT with $T[m]$.

*Proof.* Line L3 computes $((y + 1) \bmod 2^{32} - 1) \bmod 2^{32} = y$, because $0 \le y < 2^{32}$ by Lemma 1. Line L4 then gives $t_5 = t \bmod 32$, the index $m$ and $h = h_K(c, t)$, by Lemma 1. The counter $t$ satisfies $t \equiv t_5 \pmod{32}$ and $now - 31 \le now - A \le t \le now$, because $A \le 31$. By Lemma 2, line L5 gives $t' = t$. Line L6 does not reject, because $now - t \le A$ and $t \ge 0$. Line L7 computes $h_K(c, t) = h$, so it does not reject. Line L8 returns $T[m]$. $\square$

**Theorem, part 2 (soundness against an off-path adversary).** Model $F_K$ as a function drawn uniformly at random from all functions from the inputs to $\{0, 1\}^{256}$. Fix $c$, $a$ and $now$, and let $t'$ be the value of line L5 for these inputs. Suppose the adversary chooses $a$ without having seen $F_K(c, t')$. Then CHECK-COOKIE accepts with probability at most $2^{-24}$. After $q$ such attempts, with any adaptive choice of the inputs, the probability that some attempt is accepted is at most $q \cdot 2^{-24}$.

*Proof.* Lines L3 to L5 are fixed functions of $a$ and $now$, so $t'$ and $h$ are fixed before $F_K(c, t')$ is drawn. If line L6 rejects, the claim holds. Otherwise acceptance needs $F_K(c, t') \bmod 2^{24} = h$. The value $F_K(c, t')$ is uniform on 256-bit strings and independent of what the adversary has seen, so its low 24 bits are uniform on $\{0, \ldots, 2^{24} - 1\}$, and the probability is exactly $2^{-24}$.

For $q$ attempts, consider the run until the first accepted attempt. Up to that moment every answer is REJECT, so the adversary's choices are a fixed function of its own coins and of the SYN-ACKs it saw, which by hypothesis do not hold the points it attacks. Fix the coins and this sequence of choices. Group the attempts by the point $(c, t')$ they use, and let attempt group $P$ use $q_P$ attempts with guesses in a set $H_P$ of at most $q_P$ values. Some attempt in group $P$ is accepted only if $F_K(P) \bmod 2^{24} \in H_P$, which has probability $|H_P| / 2^{24} \le q_P / 2^{24}$, since that value is uniform. By the [union bound](/union-bound/) over the groups, some attempt is accepted with probability at most $\sum_P q_P / 2^{24} = q \cdot 2^{-24}$. Averaging over the coins keeps the bound. $\square$

**Remark (a real PRF).** If $F_K$ is HMAC-SHA256 with a secret uniform key, replace the random function by $F_K$. Any adversary whose success probability differs from the bound above by more than $\varepsilon$ gives a distinguisher between $F_K$ and a random function with advantage $\varepsilon$, using one oracle query per SYN-ACK it sees and per check. So the forgery probability is at most $q \cdot 2^{-24} + \mathrm{Adv}^{\mathrm{prf}}_F$. The bound says nothing about an adversary that sees the SYN-ACK to $c$: it knows $F_K(c, t)$ and can complete the handshake. $\blacksquare$
