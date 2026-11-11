---
title: The unblinded RSA signature verifies and the signer's view is independent of the message
proves: [correctness]
status: full
---

**Setting.** The public key is $(n, e)$ with $n = pq$ for distinct primes $p, q$, and the private exponent $d$ satisfies $ed \equiv 1 \pmod{\lambda(n)}$, where $\lambda(n) = \operatorname{lcm}(p-1, q-1)$. Let $k$ be the length of $n$ in bytes and $\text{emBits} = \lvert n \rvert - 1$. The client has the prepared message $M$ (line L1) and the salt $\text{salt}$ of length $sLen$. Write $EM = \text{EMSA-PSS-ENCODE}(M, \text{emBits}, \text{salt})$ and $m = \text{OS2IP}(EM)$ (line L2).

**Lemma 1 (RSA inverts).** For every integer $x$ with $0 \le x < n$, $(x^d)^e \equiv x \pmod n$ and $(x^e)^d \equiv x \pmod n$.

*Proof.* Write $ed = 1 + t\lambda(n)$. Modulo $p$: if $p \mid x$ both sides are $0$; otherwise $x^{p-1} \equiv 1$ by Fermat's little theorem, and $p - 1 \mid \lambda(n)$, so $x^{ed} = x \cdot (x^{p-1})^{t\lambda(n)/(p-1)} \equiv x$. The same holds modulo $q$, and the Chinese remainder theorem gives the congruence modulo $n$. $\square$

**Lemma 2 (the encoding is below $n$).** $m < 2^{\text{emBits}} \le n$, so $m$ is a valid RSA input.

*Proof.* EMSA-PSS-ENCODE clears the $8 \cdot \lceil \text{emBits}/8 \rceil - \text{emBits}$ leftmost bits of $EM$, so $m < 2^{\text{emBits}}$. Since $n$ has $\text{emBits} + 1$ bits, $n \ge 2^{\text{emBits}}$. $\square$

**Lemma 3 (the signer's answer).** Let $r$ be a unit modulo $n$ (line L4) and $z = m \cdot r^e \bmod n$ (line L5). Then the signer's answer $s' = z^d \bmod n$ (line L6) satisfies $s' \equiv m^d \cdot r \pmod n$, and the fault check of line L7 passes.

*Proof.* $z^d \equiv m^d \cdot r^{ed} \equiv m^d \cdot r$ by Lemma 1 applied to $r$. Lemma 1 applied to $z$ gives $(s')^e \equiv z$, so line L7 finds no fault. $\square$

**Theorem 4 (correctness).** With an honest signer, line L8 outputs $s = m^d \bmod n$, which is the RSASSA-PSS signature of $M$ with this salt, and lines L9 and L10 accept it.

*Proof.* Line L8 computes $s' \cdot r^{-1} \equiv m^d \cdot r \cdot r^{-1} = m^d \pmod n$ by Lemma 3. RSASSA-PSS-SIGN (RFC 8017, Section 8.1.1) with the same salt computes $EM$, then $m$, then $m^d \bmod n$: the same value. Verification computes $s^e \bmod n = m$ by Lemma 1, writes it as the $\lceil \text{emBits}/8 \rceil$-byte string $EM$, and EMSA-PSS-VERIFY undoes the mask: it computes $\text{dbMask} = \text{MGF}(H, \cdot)$ from the same $H$, recovers $DB = PS \Vert \texttt{01} \Vert \text{salt}$, and recomputes $H = \text{Hash}(\texttt{00}^8 \Vert \text{Hash}(M) \Vert \text{salt})$, which matches. So both checks accept. $\square$

**Theorem 5 (perfect blindness against the signer).** Assume $(n, e)$ is a valid RSA key, so $x \mapsto x^e$ is a permutation of the units modulo $n$, and $m$ is a unit (line L3). If $r$ is uniform over the units, then $z$ is uniform over the units, whatever $M$ is. Moreover, for any session view $(z, s')$ and any finished pair $(M^*, s^*)$ with $s^*$ a valid signature, there is exactly one unit $r^*$ with $z = m^* \cdot (r^*)^e$ and $s^* = s' \cdot (r^*)^{-1}$, namely $r^* = s' \cdot (s^*)^{-1}$.

*Proof.* For a fixed unit $m$, the map $r \mapsto m \cdot r^e$ is a bijection of the units, being the composition of a permutation and a multiplication by a unit. So a uniform $r$ gives a uniform $z$, independent of $m$, and $s' = z^d$ is a function of $z$ alone. For the second claim, $(s^*)^e \equiv m^*$, so $m^* \cdot (s' \cdot (s^*)^{-1})^e \equiv m^* \cdot z \cdot (m^*)^{-1} = z$; uniqueness follows because $x \mapsto x^e$ is injective on units. Every session is therefore equally consistent with every output signature, and the signer's view gives no information that links them. $\square$

The assumption on the key matters. If $\gcd(e, \lambda(n)) \ne 1$, then $r^e$ ranges over a subgroup and $z$ may leak which coset $m$ lies in; this is the attack on low-entropy messages under a malicious key in RFC 9474, Section 7.3, which the randomized preparation of line L1 defeats. A non-unit $m$ or $r$ reveals a factor of $n$ and happens with negligible probability for an honest key.

**Unforgeability.** Correctness does not show that the client cannot get more signatures than sessions. Bellare, Namprempre, Pointcheval and Semanko proved one-more unforgeability of Chaum's scheme with a full-domain hash in the random oracle model under the one-more RSA inversion assumption, and Lysyanskaya proved the same for the PSS variants of RFC 9474.
