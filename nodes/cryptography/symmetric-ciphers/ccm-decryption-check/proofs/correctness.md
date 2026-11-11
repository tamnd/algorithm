---
title: CCM decryption-verification accepts exactly the outputs of encryption and releases nothing else
proves: [correctness]
status: full
---

Fix a key $K$ and a tag length $\mathrm{Tlen}$. Write $\mathrm{GE}(N, A, P)$ for generation-encryption of SP 800-38C, Section 6.1: if $(N, A, P)$ is valid, let $B = \mathrm{format}(N, A, P)$, $T = \mathrm{MSB}_{\mathrm{Tlen}}(\mathrm{CBCMAC}_K(B))$, $S_0 = E_K(\mathrm{Ctr}_0)$, $S = E_K(\mathrm{Ctr}_1) \| \cdots \| E_K(\mathrm{Ctr}_m)$ with $m = \lceil \mathrm{Plen}/128 \rceil$, and return $C = (P \oplus \mathrm{MSB}_{\mathrm{Plen}}(S)) \| (T \oplus \mathrm{MSB}_{\mathrm{Tlen}}(S_0))$. Write $\mathrm{DV}(N, A, C)$ for the algorithm of the page, lines L1 to L11. The counter blocks depend only on $N$ and the index, so both procedures use the same $S_0$ and the same $S$ when the payload lengths match. All procedures are deterministic.

We assume $\mathrm{Plen} \ge 1$ in $\mathrm{GE}$, because Step 1 of Section 6.2 rejects $\mathrm{Clen} \le \mathrm{Tlen}$.

**Lemma 1 (completeness).** For every valid $(N, A, P)$ with $\mathrm{Plen} \ge 1$, $\mathrm{DV}(N, A, \mathrm{GE}(N, A, P)) = P$.

*Proof.* Let $C = \mathrm{GE}(N, A, P)$, so $\mathrm{Clen} = \mathrm{Plen} + \mathrm{Tlen} > \mathrm{Tlen}$ and L1 does not return. L2 computes $m = \lceil \mathrm{Plen}/128 \rceil$, the same $m$ as in $\mathrm{GE}$, so L3 and L4 compute the same $S_0$ and $S$. L5 computes $\mathrm{MSB}_{\mathrm{Plen}}(C) \oplus \mathrm{MSB}_{\mathrm{Plen}}(S) = P \oplus \mathrm{MSB}_{\mathrm{Plen}}(S) \oplus \mathrm{MSB}_{\mathrm{Plen}}(S) = P$. L6 computes $\mathrm{LSB}_{\mathrm{Tlen}}(C) \oplus \mathrm{MSB}_{\mathrm{Tlen}}(S_0) = T$. At L7 the triple $(N, A, P)$ is valid, so ok is true and the blocks are $\mathrm{format}(N, A, P)$, the same $B$ as in $\mathrm{GE}$. L8 then gives $Y = \mathrm{CBCMAC}_K(B)$ and $\mathrm{MSB}_{\mathrm{Tlen}}(Y) = T$. The comparison at L9 reads equal strings, so ok stays true, L10 does not return, and L11 returns $P$. $\square$

**Lemma 2 (canonical verification).** If $\mathrm{DV}(N, A, C)$ returns a string $P$, then $(N, A, P)$ is valid and $C = \mathrm{GE}(N, A, P)$.

*Proof.* The algorithm returns a string only at L11, so L1 did not return, ok was true after L7, and the tags were equal at L9. So $\mathrm{Clen} > \mathrm{Tlen}$, $(N, A, P)$ is valid, and $T = \mathrm{MSB}_{\mathrm{Tlen}}(\mathrm{CBCMAC}_K(\mathrm{format}(N, A, P)))$, where $P$ and $T$ are the values of L5 and L6. Then $\mathrm{Plen} = \mathrm{Clen} - \mathrm{Tlen}$, and $\mathrm{GE}(N, A, P)$ uses the same $m$, $S_0$ and $S$. Its first part is $P \oplus \mathrm{MSB}_{\mathrm{Plen}}(S) = \mathrm{MSB}_{\mathrm{Plen}}(C)$, by L5 and because XOR with a fixed string is its own inverse. Its tag is the same $T$ as above, so its second part is $T \oplus \mathrm{MSB}_{\mathrm{Tlen}}(S_0) = \mathrm{LSB}_{\mathrm{Tlen}}(C)$, by L6. The two parts together are $C$. $\square$

So decryption-verification accepts a triple $(N, A, C)$ if and only if $C$ is an output of encryption on $(N, A)$, and the accepted payload is then unique: it is the only $P$ with $\mathrm{GE}(N, A, P) = C$, because by Lemma 1 that $P$ is what $\mathrm{DV}$ returns. In particular, an accepted $C$ that the sender never produced for $(N, A)$ is a forgery against CCM in the sense of ciphertext integrity.

**Lemma 3 (no release on failure).** For every input on which $\mathrm{DV}$ does not return at L11, its output is the constant INVALID. So the output of $\mathrm{DV}$ is a function of the pair (accept bit, $\mathrm{GE}^{-1}$ on accepted inputs), and on rejected inputs it carries no information on $P$, $T$, $S_0$, $S$ or on which step failed.

*Proof.* There are exactly two return points other than L11, at L1 and at L10, and both return the same constant. The code joins the validity failure of Step 7 with the tag failure of Step 10 into the single flag ok, so a failure at Step 7 also reaches L10 and gives the same output. The values $P$ and $T$ are local and are not part of any output on these paths. $\square$

This lemma is about the output values. The timing of the code is a separate matter: the comparison at L9 has no early exit, and the dummy block at L7 makes the Step 7 failure run a CBC-MAC too, but the AES of the study code still uses table lookups, so the page claims no constant time.

**Corollary (the decryption oracle can be simulated).** Consider any adversary that asks the encryption oracle for $C_i = \mathrm{GE}(N_i, A_i, P_i)$ and the decryption oracle on triples $(N, A, C)$ that are not among the $(N_i, A_i, C_i)$. By Lemmas 2 and 3, until the first query on which $\mathrm{DV}$ accepts, every answer is INVALID, and the first accepted query is a forgery. So replacing $\mathrm{DV}$ by the oracle that always says INVALID changes the view of the adversary only on the event that it forges. This is the step in the proof that integrity of ciphertexts together with IND-CPA gives IND-CCA (see the page on authenticated encryption).

**Proposition 4 (early release decrypts every target).** Let $\mathrm{DV}'$ be the wrong decryptor that returns $\mathrm{MSB}_{\mathrm{Plen}}(C) \oplus \mathrm{MSB}_{\mathrm{Plen}}(S)$ whatever the result of the tag check. Then for every target $C^* = \mathrm{GE}(N, A, P^*)$ and every nonzero $\Delta$ of length $\mathrm{Plen}$, one query to $\mathrm{DV}'$ on the new triple $(N, A, (\mathrm{MSB}_{\mathrm{Plen}}(C^*) \oplus \Delta) \| \mathrm{LSB}_{\mathrm{Tlen}}(C^*))$ gives $P^*$.

*Proof.* The query is different from $C^*$ because $\Delta \ne 0$, so it is allowed in the IND-CCA game. Its first part has the same length as that of $C^*$, so $\mathrm{DV}'$ uses the same $m$ and $S$ and returns $\mathrm{MSB}_{\mathrm{Plen}}(C^*) \oplus \Delta \oplus \mathrm{MSB}_{\mathrm{Plen}}(S) = P^* \oplus \Delta$. The adversary XORs $\Delta$ to get $P^*$. $\square$

With $\Delta$ chosen at random, the same query sent to the correct $\mathrm{DV}$ is accepted only if it is a forgery, by Lemma 2, and otherwise it returns INVALID by Lemma 3. So the difference between the two decryptors is the difference between a forgery bound of about $q \cdot 2^{-\mathrm{Tlen}}$ plus the PRP advantage, and an advantage of 1 with one query. $\blacksquare$
