---
title: Warrant proxy signatures verify exactly for messages the warrant allows
proves: [correctness]
status: full
---

**Setting.** $G = \langle g \rangle$ has prime order $q$. The original signer has $y_a = g^{x_a}$ and the proxy has $y_b = g^{x_b}$. A warrant $w$ names $y_a$, $y_b$, a scope and an expiry time, and $w$ allows a message $m$ at time $t$ if $m$ is in the scope and $t$ is not after the expiry. $H_1$ (delegation) and $H_2$ (proxy signing) map into $\mathbb{Z}_q$.

**Lemma 1 (the delegation checks).** If the original signer runs lines L1 and L2, then $g^{s_w} = y_a^{H_1(w, K)} K$, so the proxy's check at line L3 passes.

*Proof.* $s_w = x_a H_1(w, K) + k$ and $K = g^k$, so $g^{s_w} = (g^{x_a})^{H_1(w,K)} g^k = y_a^{H_1(w,K)} K$. $\square$

**Lemma 2 (the proxy key pair).** With $x_p = s_w + x_b$ (line L4) and $y_p = y_a^{H_1(w,K)} K y_b$ (line L9), $g^{x_p} = y_p$.

*Proof.* $g^{x_p} = g^{s_w} g^{x_b} = y_a^{H_1(w,K)} K \cdot y_b$ by Lemma 1. $\square$

The verifier computes $y_p$ from $y_a$, $w$ and $K$ alone, which are public, so it needs no secret of either party.

**Theorem 3 (correctness).** If $w$ allows $m$ at time $t$, the proxy's signature $(w, K, R, z)$ made at time $t$ is accepted by the verifier at time $t$.

*Proof.* Line L5 passes because $w$ allows $m$, and the verifier's line L8 passes for the same reason. Line L7 sets $z = r + e x_p$ with $R = g^r$ and $e = H_2(w, K, R, m)$. The verifier computes the same $e$ and, by Lemma 2, $g^z = g^r (g^{x_p})^e = R \cdot y_p^e$, so line L10 accepts. $\square$

**Theorem 4 (the warrant limits the proxy).** The verifier rejects every signature on a message that its warrant does not allow at the time of verification, whatever the proxy does. A signature made for warrant $w$ does not verify under a different warrant $w'$ unless the random oracle $H_2$ gives a matching value, which happens with probability $1/q$ per try.

*Proof.* The first part is line L8, which runs before any algebra and uses only public data. For the second part, the verifier hashes $w'$ into $e' = H_2(w', K, R, m)$ and computes $y_p' = y_a^{H_1(w', K)} K y_b'$. For a fixed $(K, R, z)$ the check $g^z = R \cdot y_p'^{e'}$ fixes $e'$ modulo $q$ unless $y_p' = 1$; since $e'$ is a fresh random oracle output for the new input, it equals the one value that passes with probability $1/q$. $\square$

The tests check Theorem 4 against a proxy that skips its own check at line L5, against a widened warrant, and at the expiry time.

**Unforgeability (note).** Correctness and Theorem 4 do not show that a forger without $s_w$ or $x_b$ fails. Boldyreva, Palacio and Warinschi define security for proxy signatures (an attacker may corrupt the original signer, or the proxy, but not both) and prove a Schnorr scheme of this kind, Triple Schnorr, secure in the random oracle model under the discrete logarithm assumption. Two points of their analysis are visible here: the original signer cannot sign alone because it does not know $x_b$, and the three uses of Schnorr (ordinary signing, delegation, proxy signing) must use separate hash functions so that a signature of one kind is not valid as another.
