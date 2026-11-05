---
title: FNV computes its recurrence, and its steps are bijections of the state
proves: [correctness, termination]
status: full
---

**Notation.** Fix a width $w$ and write $N = 2^w$, $P = P_w$ and $O = O_w$. All states are in $\{0, \ldots, N - 1\}$. For a byte $\beta \in \{0, \ldots, 255\}$, let $f_\beta(x) = ((x \oplus \beta) \cdot P) \bmod N$ be one step of FNV-1a and $g_\beta(x) = ((x \cdot P) \bmod N) \oplus \beta$ one step of FNV-1. For a byte string $z = z_0 \cdots z_{k-1}$, let $F_z = f_{z_{k-1}} \circ \cdots \circ f_{z_0}$, with $F_\varepsilon$ the identity, so that the FNV-1a hash of $z$ is $F_z(O)$. The XOR of a state with a byte stays below $N$ because $N \ge 256$.

**Lemma 1 (the procedure computes the recurrence).** FNV-1A stops after $n$ passes of its loop and returns $F_b(O)$.

*Proof.* The loop at line L2 runs for $i = 0, \ldots, n - 1$, so it makes $n$ passes and stops. Let $h_i$ be the value of $h$ after $i$ passes. Then $h_0 = O$ by line L1. Lines L3 and L4 replace $h_i$ by $((h_i \oplus b[i]) \cdot P) \bmod N = f_{b[i]}(h_i)$, so $h_{i+1} = f_{b[i]}(h_i)$. By induction on $i$, $h_i = F_{b[0] \cdots b[i-1]}(O)$, and line L5 returns $h_n = F_b(O)$. $\square$

**Lemma 2 (each step is a bijection).** For every byte $\beta$, $f_\beta$ and $g_\beta$ are bijections of $\{0, \ldots, N - 1\}$.

*Proof.* The map $x \mapsto x \oplus \beta$ is its own inverse on $\{0, \ldots, N - 1\}$, so it is a bijection. $P$ is odd and $N$ is a power of 2, so $\gcd(P, N) = 1$ and $P$ has an inverse $P^{-1}$ modulo $N$; the map $x \mapsto (x P) \bmod N$ has the inverse $y \mapsto (y P^{-1}) \bmod N$. A composition of bijections is a bijection. $\square$

**Lemma 3 (suffix extension).** For all byte strings $u, v, z$, the FNV-1a hashes satisfy $h(uz) = h(vz)$ if and only if $h(u) = h(v)$. The same holds for FNV-1.

*Proof.* By Lemma 1, $h(uz) = F_z(F_u(O)) = F_z(h(u))$, and likewise $h(vz) = F_z(h(v))$. By Lemma 2, $F_z$ is a composition of bijections, so it is injective, and $F_z(h(u)) = F_z(h(v))$ holds exactly when $h(u) = h(v)$. For FNV-1, use $g$ in place of $f$. $\square$

**Lemma 4 (one changed byte).** If $x$ and $y$ have the same length and differ in exactly one position, then $h(x) \ne h(y)$, for FNV-1a and for FNV-1.

*Proof.* Write $x = u \alpha z$ and $y = u \beta z$ with bytes $\alpha \ne \beta$. The state after $u$ is the same value $s$ for both. For FNV-1a, $s \oplus \alpha \ne s \oplus \beta$, and multiplication by $P$ modulo $N$ is injective (Lemma 2), so $f_\alpha(s) \ne f_\beta(s)$. For FNV-1, $(sP \bmod N) \oplus \alpha \ne (sP \bmod N) \oplus \beta$, so $g_\alpha(s) \ne g_\beta(s)$. The remaining steps for $z$ form an injective map by Lemma 2, so the final states differ. $\square$

**Lemma 5 (low bits).** For $1 \le k \le w$, $h(b) \bmod 2^k$ depends only on $O \bmod 2^k$ and on the values $b[i] \bmod 2^k$. Bit 0 of $h(b)$ equals bit 0 of $O$ XOR the parity of the number of indices $i$ with $b[i]$ odd.

*Proof.* Bit $j$ of $x \oplus \beta$ is bit $j$ of $x$ XOR bit $j$ of $\beta$, so $(x \oplus \beta) \bmod 2^k = (x \bmod 2^k) \oplus (\beta \bmod 2^k)$. Since $2^k$ divides $N$, $(xP \bmod N) \bmod 2^k = xP \bmod 2^k = ((x \bmod 2^k)(P \bmod 2^k)) \bmod 2^k$. So $f_\beta(x) \bmod 2^k$ is a function of $x \bmod 2^k$ and $\beta \bmod 2^k$. By induction on the steps, as in Lemma 1, the state after $i$ bytes modulo $2^k$ is a function of $O \bmod 2^k$ and $b[0] \bmod 2^k, \ldots, b[i-1] \bmod 2^k$. For $k = 1$: $P$ is odd, so multiplication by $P$ keeps bit 0, and the XOR with $b[i]$ flips bit 0 exactly when $b[i]$ is odd. So bit 0 of the final state is bit 0 of $O$, flipped once for each odd byte. $\square$

**Theorem.** FNV-1A stops on every input and returns the FNV-1a hash $F_b(O)$ defined by the recurrence. The hash satisfies the suffix extension property, never maps two strings of one length that differ in one byte to one value, and has the low-bit property of Lemma 5.

*Proof.* Termination and the returned value are Lemma 1. The other claims are Lemmas 3, 4 and 5. $\blacksquare$

**Remark (what is not proved).** No statement here bounds the number or the probability of collisions. FNV has no random parameter, and Lemma 3 shows that a single collision, which exists by the pigeonhole principle among any $N + 1$ inputs, extends to infinitely many.
