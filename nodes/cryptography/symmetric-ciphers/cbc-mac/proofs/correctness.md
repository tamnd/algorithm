---
title: CBC-MAC is correct, equals the last CBC block, and admits the splice forgery
proves: [correctness]
status: full
---

Fix a block cipher $E_K$ with block length $n$. For a message $M = M_1 \cdots M_m$ of $m \ge 1$ blocks, let $Y_0 = 0^n$ and $Y_j = E_K(Y_{j-1} \oplus M_j)$ for $j = 1, \ldots, m$, as in lines L1 to L3. Write $\mathrm{T}(M) = Y_m$ for the output of line L4. More generally, for a start value $S$ let $\mathrm{chain}_S(M)$ be the value $Y_m$ of the same loop started from $Y_0 = S$, so $\mathrm{T}(M) = \mathrm{chain}_{0^n}(M)$.

**Lemma 1 (verification accepts honest tags).** For every $K$ and $M$, VERIFY$(K, M, \mathrm{T}(M))$ accepts.

*Proof.* The loop is deterministic, so line L5 computes the same value $\mathrm{T}(M)$ again, and every byte of the two equal strings matches, so the comparison returns true. $\square$

**Lemma 2 (CBC-MAC is the last CBC block).** Let $C_1, \ldots, C_m$ be the CBC encryption of $P_1, \ldots, P_m$ under $K$ with initialization vector $IV$, so $C_0 = IV$ and $C_j = E_K(C_{j-1} \oplus P_j)$. Then $C_m = \mathrm{T}(M)$ for the message $M = (P_1 \oplus IV) \, P_2 \cdots P_m$.

*Proof.* We show $Y_j = C_j$ for $j = 1, \ldots, m$ by induction. For $j = 1$: $Y_1 = E_K(0^n \oplus P_1 \oplus IV) = E_K(IV \oplus P_1) = C_1$. For $j \ge 2$, if $Y_{j-1} = C_{j-1}$, then $Y_j = E_K(Y_{j-1} \oplus P_j) = E_K(C_{j-1} \oplus P_j) = C_j$. So $\mathrm{T}(M) = Y_m = C_m$. $\square$

**Lemma 3 (the chain composes).** For messages $A$ and $B$ of whole blocks and any start value $S$, $\mathrm{chain}_S(A \,\|\, B) = \mathrm{chain}_{\mathrm{chain}_S(A)}(B)$.

*Proof.* The loop processes the blocks of $A$ first and reaches the value $\mathrm{chain}_S(A)$; the remaining iterations are the loop on $B$ started from that value. $\square$

**Lemma 4 (moving a start value into the first block).** For any start value $S$, any block $X$ and any message $R$ of whole blocks (possibly empty), $\mathrm{chain}_S(X \,\|\, R) = \mathrm{chain}_{0^n}((X \oplus S) \,\|\, R)$.

*Proof.* The first iteration from $S$ computes $E_K(S \oplus X)$. The first iteration from $0^n$ on the block $X \oplus S$ computes $E_K(0^n \oplus X \oplus S)$, the same value. After that both loops process $R$ from the same value. $\square$

**Theorem (the splice).** Let $M$ have tag $T = \mathrm{T}(M)$ and let $M' = M'_1 \, R$ with $M'_1$ one block, $R$ the remaining blocks, and tag $T' = \mathrm{T}(M')$. Then
$$\mathrm{T}\bigl(M \,\|\, (M'_1 \oplus T) \,\|\, R\bigr) = T'.$$

*Proof.* By Lemma 3 with $S = 0^n$, $\mathrm{T}(M \,\|\, (M'_1 \oplus T) \,\|\, R) = \mathrm{chain}_{T}((M'_1 \oplus T) \,\|\, R)$, since $\mathrm{chain}_{0^n}(M) = T$. By Lemma 4 with $S = T$ and $X = M'_1 \oplus T$, this equals $\mathrm{chain}_{0^n}((M'_1 \oplus T \oplus T) \,\|\, R) = \mathrm{chain}_{0^n}(M'_1 \,\|\, R) = \mathrm{T}(M') = T'$. $\blacksquare$

**Remark.** The spliced message has $|M| + |M'|$ blocks, so it is longer than both $M$ and $M'$, and $M$ is a prefix of it. On a message space with one fixed number of blocks, or more generally with no message a prefix of another, the splice gives no message of the space, which agrees with the security theorems of Bellare, Kilian and Rogaway and of Petrank and Rackoff. Lemma 4 with $S = IV$ is also the forgery against the random IV variant: replacing $(IV, M_1)$ by $(IV \oplus \Delta, M_1 \oplus \Delta)$ leaves $IV \oplus M_1$ and so the tag unchanged.
