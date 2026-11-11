---
title: Confirmation and disavowal of Chaum-van Antwerpen signatures are complete and sound
proves: [correctness]
status: full
---

**Setting.** $G = \langle g \rangle$ has prime order $q$, the signer's key is $a \in \mathbb{Z}_q^*$ with $y = g^a$, and a message is hashed to $h \in G \setminus \{1\}$. A claimed signature is any $s \in G$; it is valid if $s = h^a$. The verifier draws $e_1, e_2$ (and $f_1, f_2$) uniformly from $\mathbb{Z}_q^*$. The honest signer answers a challenge $c$ with $c^{a^{-1}}$, where $a^{-1}$ is taken modulo $q$. The signer in the soundness statements may be computationally unbounded and may answer with any function of what it has seen.

**Theorem 1 (confirmation is complete).** If $s = h^a$ and the signer is honest, the verifier accepts at line L5.

*Proof.* $d = (s^{e_1} y^{e_2})^{a^{-1}} = (h^{a e_1} g^{a e_2})^{a^{-1}} = h^{e_1} g^{e_2}$. $\square$

**Lemma 2.** Let $s = g^i$, $h = g^j$ and suppose $s \ne h^a$, that is $i \ne a j \pmod q$. For a fixed challenge $c = s^{e_1} y^{e_2}$, the pairs $(e_1, e_2) \in (\mathbb{Z}_q^*)^2$ that give $c$ number at least $q - 2$, and their expected answers $h^{e_1} g^{e_2}$ are pairwise distinct.

*Proof.* In exponents, $(e_1, e_2) \mapsto (i e_1 + a e_2,\ j e_1 + e_2)$ is the linear map with matrix $\begin{pmatrix} i & a \\ j & 1 \end{pmatrix}$, whose determinant $i - a j$ is not $0$ modulo $q$. So it is a bijection of $\mathbb{Z}_q^2$, and the pairs that give a fixed $c = g^\gamma$ get pairwise distinct expected answers. These pairs form the line $i e_1 + a e_2 = \gamma$. Since $a \ne 0$, each $e_1$ fixes one $e_2$, so the line has $q$ points, exactly one of them with $e_1 = 0$. If $i \ne 0$, at most one point has $e_2 = 0$. If $i = 0$, every point has $e_2 = \gamma / a$, and this is $0$ only if $c = 1$; but with $i = 0$ the challenge is $c = y^{e_2} \ne 1$ for $e_2 \ne 0$, so $c = 1$ is never sent. In all cases at least $q - 2$ points have both coordinates nonzero. $\square$

**Theorem 3 (confirmation is sound).** If $s \ne h^a$, the verifier accepts with probability at most $1/(q-2)$, whatever the signer does.

*Proof.* The signer sees only $c$. Given $c$, the pair $(e_1, e_2)$ is uniform among the at least $q - 2$ pairs of Lemma 2, whose expected answers are distinct. Any answer $d$ equals at most one of them. $\square$

**Theorem 4 (disavowal is complete).** If $s \ne h^a$ and the signer is honest, the verifier outputs "forgery".

*Proof.* The honest answer is $d = s^{e_1 a^{-1}} g^{e_2}$. It equals $h^{e_1} g^{e_2}$ only if $s^{e_1 a^{-1}} = h^{e_1}$, and since $e_1$ is invertible modulo $q$ this means $s = h^a$; so line L7 does not return, and line L9 does not return for the same reason. At line L10, $d g^{-e_2} = s^{e_1 a^{-1}}$ and $D g^{-f_2} = s^{f_1 a^{-1}}$, so both sides equal $s^{e_1 f_1 a^{-1}}$. $\square$

**Theorem 5 (disavowal is sound).** If $s = h^a$, the verifier outputs "forgery" with probability at most $1/(q-2)$, whatever the signer does.

*Proof.* Suppose the first answer $d$ fails line L7, so $d \ne h^{e_1} g^{e_2}$. Let $h_0 = (d g^{-e_2})^{e_1^{-1}}$, which is fixed after the first round; then $h_0 \ne h$. The verifier outputs "forgery" only if $(d g^{-e_2})^{f_1} = (D g^{-f_2})^{e_1}$, that is $h_0^{e_1 f_1} = (D g^{-f_2})^{e_1}$, that is $D = h_0^{f_1} g^{f_2}$. The second challenge is $C = s^{f_1} y^{f_2}$ with $s = h^a \ne h_0^a$. This is a confirmation challenge for the false claim "$s$ is the signature on $h_0$", and producing $D = h_0^{f_1} g^{f_2}$ is passing it; by Theorem 3, applied with $h_0$ in place of $h$ and fresh $f_1, f_2$, this happens with probability at most $1/(q-2)$. $\square$

With honest answers to a valid signature, the first round already returns "valid" at line L7 (Theorem 1). The tests check Theorems 1, 3, 4 and 5 on 20 messages, with false signatures made by another key, for another message and at random, and with cheating signers that answer at random or with the wrong key.

**What is not shown here.** The protocols as given are not zero knowledge against a dishonest verifier, who may choose $c$ without knowing $e_1, e_2$ and so learn $c^{a^{-1}}$. Chaum's zero-knowledge version (Eurocrypt 1990) makes the verifier commit to and later reveal its exponents. Unforgeability of $s = h^a$ rests on the computational Diffie-Hellman problem with $h$ a random oracle output, and invisibility (nobody can tell a valid $s$ from a random group element without the signer) on the decisional Diffie-Hellman problem.
