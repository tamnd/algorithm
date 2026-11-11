---
title: The toy group signature verifies, and opening finds the signer with a checkable proof
proves: [correctness]
status: full
---

This proof is about the toy linear-size scheme in the code, not about BMW or BBS.

**Setting.** $G = \langle g \rangle$ has prime order $q$. Members have $y_j = g^{x_j}$ for $j = 0, \ldots, n-1$, all distinct, and the opener has $Y = g^{x_o}$. For a ciphertext $(C_1, C_2)$ and a triple $(c_j, u_j, v_j)$ write

$$T_j = \big(g^{u_j} y_j^{c_j},\ g^{v_j} C_1^{c_j},\ Y^{v_j} (C_2 / y_j)^{c_j}\big).$$

A signature $(C_1, C_2, (c_j, u_j, v_j)_j)$ is valid for $m$ if $\sum_j c_j \equiv H(L, Y, m, C_1, C_2, T_0, \ldots, T_{n-1}) \pmod q$ (lines L7 and L8).

**Theorem 1 (correctness of signing).** For every member $i$, every message and all coins, verify accepts the output of sign.

*Proof.* For $j \ne i$, the verifier's $T_j$ is computed from the same $(c_j, u_j, v_j)$ by the same formula as line L2. For $j = i$, with $C_1 = g^\rho$ and $C_2 / y_i = Y^\rho$ (line L1), and $u_i = a - c_i x_i$, $v_i = b - c_i \rho$ (line L5):

- $g^{u_i} y_i^{c_i} = g^{a - c_i x_i + c_i x_i} = g^a$,
- $g^{v_i} C_1^{c_i} = g^{b - c_i \rho + c_i \rho} = g^b$,
- $Y^{v_i} (C_2/y_i)^{c_i} = Y^{b - c_i \rho + c_i \rho} = Y^b$.

These are the values of line L3. So the verifier hashes the same tuple as line L4 and gets $c$, and line L4 chose $c_i$ so that $\sum_j c_j = c$. $\square$

**Theorem 2 (correctness of opening).** For a signature made by member $i$, line L9 gives $y = y_i$, so the opener returns index $i$, and the judge accepts the opening.

*Proof.* $C_2 / C_1^{x_o} = y_i Y^\rho / g^{\rho x_o} = y_i$, and since the keys are distinct, the index is $i$. For the Chaum-Pedersen proof, $A = g^w$, $B = C_1^w$ and $z = w + e x_o$, so $g^z = A Y^e$ and $C_1^z = B\, C_1^{x_o e} = B (C_2 / y_i)^e$. $\square$

**Theorem 3 (a false opening fails).** Suppose the judge accepts two openings $(y', A, B, z)$ and $(y', A, B, z')$ with the same $y'$, $A$, $B$ and different hash values $e \ne e'$. Then $y' = C_2 / C_1^{x_o}$.

*Proof.* Dividing the checks gives $g^{z - z'} = Y^{e - e'}$ and $C_1^{z - z'} = (C_2/y')^{e - e'}$. With $\delta = (z - z')(e - e')^{-1} \bmod q$ this says $Y = g^\delta$, so $\delta = x_o$, and $C_2 / y' = C_1^{x_o}$. $\square$

So an opener that names the wrong member must answer a hash value that it cannot control; in the random oracle model, by the forking lemma, it succeeds with negligible probability. The tests check that the judge rejects the four wrong indices and a changed response.

**Notes on security.** These are not proved here.

- *Traceability.* The same extraction applied to the OR proof gives, from two signatures with the same commitments and different hash values, an index $j$ with $c_j \ne c_j'$ and then $x_j$ and $\rho$ with $y_j = g^{x_j}$, $C_1 = g^\rho$ and $C_2 = y_j Y^\rho$. So a valid signature opens to a member, and its signer knew that member's key.
- *Anonymity.* The OR proof is perfectly witness indistinguishable, and ElGamal hides $y_i$ under the decisional Diffie-Hellman assumption. This gives anonymity against an attacker without $x_o$ that cannot ask for openings (CPA anonymity). Anonymity with an opening oracle, as in the BMW model, needs a CCA-secure encryption.
- *Non-frameability.* Members make their own keys, and the opener knows only $x_o$, so it cannot sign as a member.
