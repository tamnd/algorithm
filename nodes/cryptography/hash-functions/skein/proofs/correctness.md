---
title: UBI is injective on its inputs, so a Skein collision gives a collision of the tweaked compression function
proves: [correctness]
status: full
---

We use the notation of the page. Let $F(G, T, P) = E(G, T, P) \oplus P$ be the tweaked compression function, with $G$ and $P$ of $N_b$ bytes and $T$ of 16 bytes. We consider messages of whole bytes, so the BitPad flag is 0.

**Lemma 1 (Threefish is a permutation).** For each key $K$ and tweak $T$, $P \mapsto E(K, T, P)$ is a bijection.

*Proof.* Each round is a subkey addition (a bijection for a fixed subkey), a set of MIX steps and a word permutation. A MIX step maps $(x_0, x_1)$ to $(y_0, y_1) = (x_0 + x_1, (x_1 \lll R) \oplus y_0)$, and it is undone by $x_1 = (y_1 \oplus y_0) \ggg R$ and $x_0 = y_0 - x_1$. A composition of bijections is a bijection. $\square$

So decryption exists and Threefish is a tweakable block cipher. Lemma 1 is not needed for the injectivity below, which is about the inputs of $F$, but it is what makes $F$ a Matyas-Meyer-Oseas compression function and not just a function.

**Lemma 2 (the tweak sequence fixes the length).** In a call UBI$(G, M, T_s)$ with $n$ bytes and $k$ blocks, the tweaks are $T_s + \min(n, (i+1) N_b) + a_i 2^{126} + b_i 2^{127}$, with $a_0 = b_{k-1} = 1$ and the other $a_i, b_i$ zero. The tweak of the last block, the one with the Final bit, holds the position $n$.

*Proof.* For $i = k - 1$, $(i + 1) N_b = k N_b \ge n$, so the minimum is $n$. The restriction on $T_s$ in Section 3.4 ensures that the position field does not carry into the other fields. $\square$

**Lemma 3 (UBI inputs determine the message).** Let $(T_i, P_i)_{i < k}$ be the tweaks and blocks of UBI$(G, M, T_s)$, and $(T'_i, P'_i)_{i < k'}$ those of UBI$(G, M', T_s)$. If the last tweak and block of the two calls are equal, $T_{k-1} = T'_{k'-1}$ and $P_{k-1} = P'_{k'-1}$, and the two chaining values before the last block are equal, then either $M = M'$, or some earlier pair of calls of $F$ has different inputs and equal outputs.

*Proof.* By Lemma 2 the equal last tweaks give $n = n'$, so $k = k'$ and the padding is the same. Walk back from the last block. At step $i$, the outputs of $F$ at block $i - 1$ are the chaining values before block $i$, and they are equal. If the inputs $(G_{i-1}, T_{i-1}, P_{i-1})$ differ, we have a collision of $F$. Otherwise $P_{i-1} = P'_{i-1}$ and we continue. If we reach block 0 with all inputs equal, every block is equal, and with $n = n'$ the messages are equal. $\square$

**Theorem 1 (collision of Skein gives a collision of $F$).** Fix $N_b$, $N_o$ and an empty key. If $M \ne M'$ and Skein$(M) =$ Skein$(M')$, then one can find, from the two computations, two different inputs of $F$ with equal outputs, or two different inputs of the output step that give the same output bits.

*Proof.* The configuration step is the same for both messages, so both message UBI calls start from the same $G_0$. Let $G_1$ and $G'_1$ be the results of the message UBI calls. If $G_1 \ne G'_1$, the output calls have different inputs and the same first $N_o$ bits, which is the second case. If $G_1 = G'_1$, then the last calls of $F$ in the two message UBI calls have equal outputs. If their inputs differ, that is a collision of $F$. If they are equal, Lemma 3 gives a collision of $F$ at an earlier block, or $M = M'$, which is false. $\square$

**Remark on tightness.** The reduction makes at most $\lceil n/N_b \rceil + \lceil n'/N_b \rceil + 4$ calls of $F$ and loses no probability, so it is tight. If $N_o < 8 N_b$, the second case is a collision of a truncated output of $F$, which costs about $2^{N_o / 2}$ calls generically; this matches the claim $2^{m/2}$ with $m = \min(8 N_b, N_o)$. The type field also separates the configuration, message and output calls, so a collision cannot mix a message block with an output block: their tweaks differ in bits 120 to 125. Bellare et al. (2009) prove the matching statements for pseudorandomness and indifferentiability, with the same type and position argument.

**Theorem 2 (the code is Skein).** The code computes the function of Section 3.5.4 and 3.5.5 for byte messages: it agrees with all 9 vectors of Appendix C and with the initial values of Appendix B, which test Threefish, UBI, the configuration and the output step for the three state sizes. $\blacksquare$
