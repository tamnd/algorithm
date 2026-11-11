---
title: Correctness of SRP-6a
proves: [correctness]
status: full
---

We prove that two honest parties agree on the premaster secret, that the aborts of lines L6 and L10 do not fire in an honest run except with negligible probability, and that a wrong password makes the key confirmation fail except with negligible probability. Notation is that of the page: $N = 2q + 1$ a safe prime with $q$ an odd prime, $g$ a generator of $\mathbb{Z}_N^*$, $k$, $x$, $v = g^x$, secrets $a, b \in [1, 2^{256})$, $A = g^a$, $B = (kv + g^b) \bmod N$ and $u = H(\mathrm{PAD}(A) \| \mathrm{PAD}(B))$ with $\ell$ output binary digits. All arithmetic is modulo $N$. For the groups of RFC 5054, $q > 2^{1000}$, so $2^{256} < q$ and $2^{\ell} < q$.

**Fact.** The order of an element of $\mathbb{Z}_N^*$ divides $N - 1 = 2q$, so it is 1, 2, $q$ or $2q$. The only element of order 2 is $-1$. Distinct exponents in $[0, q)$ give distinct powers of an element of order at least $q$.

**Lemma 1 (unblinding).** If the client uses the same $x$ as the one in $v$, then line L8 gives $\mathrm{base} = g^b \bmod N$.

*Proof.* By line L5, $B \equiv kv + g^b \pmod N$. Line L8 computes $B - k g^x \equiv kv + g^b - kv \equiv g^b \pmod N$, since $g^x \equiv v$. $\square$

**Lemma 2 (agreement).** In an honest run, both sides compute $S = g^{b(a + ux)} \bmod N$.

*Proof.* Both sides compute $u$ from the same $\mathrm{PAD}(A)$ and $\mathrm{PAD}(B)$ (lines L7 and L11), so they hold the same $u$. By Lemma 1, the client computes $S_c = (g^b)^{a + ux} = g^{b(a + ux)}$ in line L9. The server computes $A v^u = g^a g^{xu} = g^{a + ux}$, and line L12 gives $S_s = (g^{a + ux})^b = g^{b(a + ux)}$. Integer multiplication is commutative, so $S_c = S_s$. $\square$

**Lemma 3 (no false abort).** In an honest run, line L10 never aborts, and line L6 aborts with probability at most $2^{-256}$.

*Proof.* $N$ is prime and $g$ is a unit, so $A = g^a$ is a unit and $A \bmod N \ne 0$. $B \equiv 0$ means $g^b \equiv -kv$. Since $g$ has order $2q > 2^{256}$, distinct $b$ in the range give distinct $g^b$ (Fact), so at most one $b$ hits the value $-kv$, and a uniform $b$ does so with probability at most $2^{-256}$. $\square$

**Lemma 4 (equal keys give equal proofs).** If $S_c = S_s$, then $K_c = K_s$, the server accepts $M_1$, and the client accepts $M_2$.

*Proof.* $K = H(S)$ is a function of $S$, so $K_c = K_s$. $M_1$ and $M_2$ are functions of $(A, B, K)$ and $(A, M_1, K)$, and both sides hold the same $A$ and $B$ because the messages were delivered unchanged. So the value that each side recomputes in line L16 equals the value it receives. $\square$

**Lemma 5 (wrong password).** Model $H$ in lines L7 and L11 as a random oracle, so $u$ is uniform in $[0, 2^{\ell})$ and independent of $b$. If the client uses $x'$ with $g^{x'} \ne g^x$, then $S_c = S_s$ with probability at most $2^{-\ell} + 2^{-256}$.

*Proof.* Line L8 now gives $\mathrm{base} = g^b + \delta$ with $\delta = k(g^x - g^{x'}) \bmod N$. Here $\delta \ne 0$, because $g^x \ne g^{x'}$ and $0 < k < N$ for the groups of RFC 5054. Put $d = \mathrm{base} \cdot g^{-b}$ and $w = \mathrm{base}^{x'} g^{-bx}$; both depend on $b$ but not on $u$ or $a$. The client gets $S_c = \mathrm{base}^{a + ux'}$ and the server gets $S_s = g^{b(a + ux)}$, so $S_c = S_s$ if and only if $d^a = w^{-u}$.

Case $w \notin \{1, -1\}$. Then $w$ has order at least $q > 2^{\ell}$, so the values $w^{-u}$ for $u \in [0, 2^{\ell})$ are distinct, and at most one $u$ solves the equation. The probability over $u$ is at most $2^{-\ell}$.

Case $w \in \{1, -1\}$. Then the equation needs $d^a \in \{1, -1\}$. We have $d \ne 1$ since $\delta \ne 0$. $d = -1$ means $2 g^b \equiv -\delta$, which holds for at most one $b$, so with probability at most $2^{-256}$. Otherwise $d$ has order $q$ or $2q$. Then $d^a = 1$ needs the order to divide $a$, and $d^a = -1$ needs the order to be $2q$ and $a \equiv q \pmod{2q}$; both are impossible for $1 \le a < 2^{256} < q$.

Adding the two bounds gives the claim. $\square$

**Theorem.** In an honest run with the right password, SRP-6a terminates, except with probability at most $2^{-256}$, with both sides holding the same key $K = H(g^{b(a + ux)} \bmod N)$ and both proofs accepted. With a wrong password, the server rejects in line L16 except with probability at most $2^{-\ell} + 2^{-256}$ plus the probability of a collision of $H$ in lines L13 and L14.

*Proof.* Lemma 3 shows that the run reaches lines L9 and L12, Lemma 2 gives equal $S$, and Lemma 4 gives equal $K$ and accepted proofs. For a wrong password, Lemma 5 gives $S_c \ne S_s$ with the stated probability; then equal proofs need $H(S_c) = H(S_s)$ or a collision in line L14. $\blacksquare$

This is a correctness proof only. It says nothing about security against an active attacker: SRP has no reduction to a standard assumption, as the page explains.
