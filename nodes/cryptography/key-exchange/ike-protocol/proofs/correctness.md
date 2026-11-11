---
title: Honest IKEv2 parties accept each other and derive the same keys
proves: [correctness]
status: full
---

We use the notation of the page, with signature authentication. The building blocks satisfy these correctness properties.

- **(S)** For every signature key pair $(sk, pk)$ and message $m$, VERIFY$(pk, m, \mathrm{SIG}(sk, m))$ succeeds.
- **(E)** For every pair of keys $(k_e, k_a)$ and string $w$, opening $\mathrm{SK}_{k_e, k_a}\{w\}$ with the same keys gives $w$.
- **(C)** The encoding of a tuple can be decoded: the receiver gets back each part.

prf and prf+ are deterministic functions. Each directory maps the name of each honest party to its true public key.

**Lemma 1.** If $1 \le i, r \le q - 1$, then $\mathrm{KE}_i = g^i$ and $\mathrm{KE}_r = g^r$ lie in $G \setminus \{1\}$, and $\mathrm{KE}_r^{\,i} = \mathrm{KE}_i^{\,r}$.

*Proof.* Both are powers of $g$, and they differ from 1 because $g$ has prime order $q$ and $q$ does not divide $i$ or $r$. Since $G$ is commutative, $(g^r)^i = g^{ir} = (g^i)^r$. $\blacksquare$

**Theorem.** Suppose $I$ and $R$ are honest, every message arrives unchanged, and, if $R$ asks for a cookie at line L2, $I$ repeats message 1 with that cookie. Then $I$ accepts $R$'s identity at line L8, $R$ accepts $I$'s identity at line L7, and both compute the same KEYMAT at line L9.

*Proof.* *Lines L1 to L3.* If $R$ asks for a cookie, it computes it as a deterministic function of (Ni, IP of $I$, SPIi, secret); the repeated message 1 has the same Ni, address and SPIi, so $R$ computes the same value and the check passes. By Lemma 1, the KE values pass the group checks. Let message 1 be the request that $R$ answered and message 2 its response; both parties hold both byte strings.

*Lines L4 and L5.* By Lemma 1, both hold the same $g^{ir}$. Both know Ni, Nr, SPIi and SPIr from messages 1 and 2. So both compute the same SKEYSEED and the same seven keys.

*Line L6 and the check at line L7.* $I$ sends $\mathrm{SK}\{\mathrm{IDi}, \mathrm{AUTHi}\}$ under SK_ei and SK_ai. $R$ opens it with the same keys, and by (E) and (C) it gets IDi and AUTHi. $R$ rebuilds message 1 $\mid$ Nr $\mid$ prf(SK_pi, IDi) from the same bytes and the same SK_pi, which is the string that $I$ signed. Its directory gives $I$'s true public key, so by (S) the check passes and $R$ accepts IDi.

*Line L7 (the reply) and line L8.* In the same way, $I$ opens $\mathrm{SK}\{\mathrm{IDr}, \mathrm{AUTHr}\}$ under SK_er and SK_ar, rebuilds message 2 $\mid$ Ni $\mid$ prf(SK_pr, IDr), and by (S) the check passes; $I$ accepts IDr.

*Line L9.* Both apply prf+ to the same SK_d and the same Ni $\mid$ Nr, so both get the same KEYMAT. $\blacksquare$
