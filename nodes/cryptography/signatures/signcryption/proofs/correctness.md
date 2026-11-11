---
title: Zheng's signcryption returns the message to the intended recipient
proves: [correctness]
status: full
---

**Setting.** $G = \langle g \rangle$ has prime order $q$. Alice has $y_a = g^{x_a}$ and Bob has $y_b = g^{x_b}$. $H$ maps a group element to a key pair $(k_1, k_2)$, $E_{k_1}$ and $D_{k_1}$ are the encryption and decryption of a symmetric cipher with $D_{k_1}(E_{k_1}(m)) = m$, and $KH_{k_2}$ is a keyed hash into $\mathbb{Z}_q$. A signcryptext is $(c, r, s)$.

**Lemma 1 (the shared key).** Let $x \in \mathbb{Z}_q^*$ and $K = y_b^x$ (line L2).

- In SDSS1, with $s = x (r + x_a)^{-1} \bmod q$, it holds $(y_a g^r)^{s x_b} = K$.
- In SDSS2, with $s = x (1 + x_a r)^{-1} \bmod q$, it holds $(g\, y_a^r)^{s x_b} = K$.

*Proof.* SDSS1: $y_a g^r = g^{x_a + r}$, so $(y_a g^r)^{s x_b} = g^{(x_a + r) \cdot x (x_a + r)^{-1} \cdot x_b} = g^{x x_b} = (g^{x_b})^x = y_b^x$. The exponent arithmetic is modulo $q$, which is valid because $g$ has order $q$. SDSS2: $g\, y_a^r = g^{1 + x_a r}$, and the same computation gives $g^{x x_b}$. The inverses exist because line L5 retries when $r + x_a \equiv 0$ (SDSS1) or $1 + x_a r \equiv 0$ (SDSS2). $\square$

**Theorem 2 (correctness).** For every message $m$, unsigncrypt with $y_a$ and $x_b$ returns $m$ on the output of signcrypt by $x_a$ for $y_b$, in the same variant.

*Proof.* By Lemma 1, line L6 computes the same $K$ as line L2, so $H(K)$ gives the same $(k_1, k_2)$. Line L7 computes $D_{k_1}(E_{k_1}(m)) = m$; for the stream cipher in the code, $E = D$ is XOR with a key stream that depends only on $k_1$, and XOR twice with the same stream is the identity. Line L8 computes $KH_{k_2}(m)$, which is the $r$ of line L4, so it accepts and returns $m$. $\square$

**Proposition 3 (tag rejection).** Let $(c, r, s)$ be a valid signcryptext of $m$ and change it to $(c', r', s')$. Bob accepts only if $KH_{k_2'}(m') = r'$, where $K'$, $(k_1', k_2')$ and $m' = D_{k_1'}(c')$ are what he computes. If only $c$ changes, then $k_2' = k_2$ and $m' \ne m$, so acceptance needs a second message with the same tag under the secret key $k_2$. If only $s$ changes, then $K' \ne K$, because $s \mapsto b^{s x_b}$ is injective on $\mathbb{Z}_q$ for a base $b \ne 1$ of order $q$; acceptance then needs the tag $r$ under a key that is a fresh hash output. If $r$ changes, acceptance needs the new value $r'$ as the tag of $m'$.

*Proof.* Each case restates line L8 for the values Bob computes. If $H$ and $KH$ are modelled as random functions and the attacker does not know the keys involved, a fixed change is accepted with probability $1/q$. $\square$

With the toy $q = 1019$ that probability is about $10^{-3}$, so the tests use fixed seeds and check the specific changes listed above, Carol's key in place of Bob's or Alice's, and the other variant.

**Security (note).** Proposition 3 is not a proof of unforgeability: it does not handle an attacker who chooses $(r', s')$ to aim at a $K'$ it knows. Baek, Steinfeld and Zheng (Journal of Cryptology, 2007) prove that Zheng's scheme, with the identities of both parties and the public keys bound into the hash, gives confidentiality and unforgeability in a multi-user model under the gap Diffie-Hellman assumption in the random oracle model. Unsigncryption shows that Alice sent $m$ to Bob, but in Zheng's original form a third party cannot check this without Bob's secret key; non-repudiation needs an extra protocol or a variant that is publicly verifiable.
