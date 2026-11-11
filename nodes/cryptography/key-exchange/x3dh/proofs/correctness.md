---
title: Correctness of X3DH
proves: [correctness]
status: full
---

We prove that when Bob's bundle is genuine and Alice's first message reaches Bob unchanged, Alice's check of line L3 passes, both parties compute the same $SK$, and Bob accepts in line L15. Notation is that of the page. Let $B$ be the base point of edwards25519, $\ell$ its prime order, and $u_0 = 9$ the base $u$-coordinate of Curve25519. We assume the AEAD is correct: $\mathrm{DEC}(k, \mathrm{ENC}(k, p, a), a) = p$.

**Lemma 1 (X25519 is symmetric).** For private keys $x$ and $y$ with public keys $X = \mathrm{X25519}(x, u_0)$ and $Y = \mathrm{X25519}(y, u_0)$, $\mathrm{X25519}(x, Y) = \mathrm{X25519}(y, X)$.

*Proof.* Let $c(\cdot)$ be the clamping of RFC 7748, Section 5, and $P_0$ the Curve25519 point with $u$-coordinate $u_0$. X25519$(k, u)$ is the $u$-coordinate of $c(k) \cdot Q$ for a point $Q$ with $u$-coordinate $u$, which does not depend on the sign of $Q$. So $\mathrm{X25519}(x, Y)$ is the $u$-coordinate of $c(x) c(y) \cdot P_0$, and so is $\mathrm{X25519}(y, X)$, because scalar multiplication on the group commutes. $\square$

**Lemma 2 (the four values agree).** The values $DH1, \ldots, DH4$ that Alice computes in lines L5 to L8 equal those that Bob computes in lines L11 and L12, and DH4 is present on one side exactly when it is present on the other.

*Proof.* Alice's $DH1 = \mathrm{X25519}(ik_A, SPK_B)$ and Bob's $DH1 = \mathrm{X25519}(spk_B, IK_A)$ are equal by Lemma 1, where lower case letters are the private keys. In the same way, $DH2$ uses the pair $(ek_A, ik_B)$, $DH3$ the pair $(ek_A, spk_B)$ and $DH4$ the pair $(ek_A, opk_B)$; Bob reads $IK_A$ and $EK_A$ from the unchanged message. Alice includes the one-time prekey id in line L10 exactly when the bundle had $OPK_B$ (line L8), and Bob computes $DH4$ exactly when the id is present (line L12). Since the server gave this $OPK_B$ to Alice only, Bob still holds its private key, so line L12 does not abort. $\square$

**Lemma 3 (the signature verifies).** An XEdDSA signature made in line L1 on $M = \mathrm{Encode}(SPK_B)$ passes the check of line L3 with $IK_B$.

*Proof.* In XEdDSA, calculate_key_pair takes $k = c(ik_B)$, forms $E = kB$, and sets $a = k$ if the sign bit of $E$ is 0, else $a = -k \bmod \ell$; so $A = aB$ is the point with $u$-coordinate equal to $IK_B$ and sign bit 0. The signer picks $r$, sets $R = rB$, $h = H(R \,\|\, A \,\|\, M) \bmod \ell$ and $s = r + ha \bmod \ell$. The verifier maps $IK_B$ to $y = (u - 1)/(u + 1)$ with sign bit 0, which is the encoding of the same point $A$ by the birational map between Curve25519 and edwards25519. It computes the same $h$ and checks $sB - hA = R$. Indeed $sB - hA = (r + ha)B - h(aB) = rB = R$. The range checks pass because $u < p$, the encoding of $R$ is canonical, and $s < \ell$. $\square$

**Lemma 4 (same KDF input and associated data).** Both parties compute $SK$ from the same byte string, and both use the same $AD$.

*Proof.* By Lemma 2, the concatenation $DH1 \,\|\, DH2 \,\|\, DH3 \,[\,\|\, DH4]$ is the same in lines L9 and L13, and both apply the same KDF with the same prefix, salt and info, which is a deterministic function. Lines L10 and L14 both form $\mathrm{Encode}(IK_A) \,\|\, \mathrm{Encode}(IK_B)$ from the same public keys. $\square$

**Theorem.** With a genuine bundle and an unchanged first message, Alice does not abort in line L3, Bob's $SK$ in line L16 equals Alice's $SK$ of line L9, and Bob's decryption in line L15 returns Alice's first plaintext.

*Proof.* By Lemma 3, line L3 passes. By Lemma 4, both get the same $SK$ and $AD$. The ciphertext is $\mathrm{ENC}(SK, p, AD)$, so by the correctness of the AEAD, line L15 returns $p$ and does not abort, and Bob returns $SK$ in line L16. $\blacksquare$

**Remarks.** If the message is changed, $IK_A$ or $EK_A$ differs, so $SK$ or $AD$ differs, and line L15 aborts unless the AEAD is forged. If the same message is delivered twice with a one-time prekey, the second delivery aborts in line L12 because the prekey was deleted; without a one-time prekey Bob computes the same $SK$ again, which is the replay behaviour described in Section 4 of the specification.
