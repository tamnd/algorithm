---
title: Correctness of the Double Ratchet
proves: [correctness]
status: full
---

We prove that two honest parties who run the Double Ratchet from the same $SK$ decrypt every delivered message to its plaintext, when messages are delivered at most once, unchanged and in any order, and each call of line L19 passes. Notation is that of the page. We also assume that all ratchet public keys generated in the run are distinct (this fails only with negligible probability) and that the encryption is correct: $\mathrm{DECRYPT}(mk, \mathrm{ENCRYPT}(mk, p, a), a) = p$.

**Chains.** Let $P_0$ be Bob's initial ratchet public key, $P_1$ Alice's key from line L1, and $P_{j+1}$ the key that a party creates in line L26 when it ratchets on $P_j$. Define $RK_0 = SK$ and $(RK_j, CK_j) = \mathrm{KDF\_RK}(RK_{j-1}, \mathrm{DH}(P_j, P_{j-1}))$ for $j \ge 1$, where $\mathrm{DH}(P_j, P_{j-1})$ is the X25519 value of the two key pairs, which either owner can compute. Chain $j$ is the sequence of messages whose header carries $dh = P_j$. Odd chains are sent by Alice and even chains by Bob. Write $(c_{j,0}, mk_{j,0}) = (CK_j, \cdot)$ and $(c_{j,i+1}, mk_{j,i}) = \mathrm{KDF\_CK}(c_{j,i})$, so $mk_{j,i}$ is the key for message $i$ of chain $j$.

**Lemma 1 (DH symmetry).** If one party holds the private key of $P_j$ and the other the private key of $P_{j-1}$, both compute the same $\mathrm{DH}$ value, so both get the same $(RK_j, CK_j)$ from the same $RK_{j-1}$.

*Proof.* X25519 is commutative: $\mathrm{X25519}(a, \mathrm{X25519}(b, 9)) = \mathrm{X25519}(b, \mathrm{X25519}(a, 9))$, since both are the $u$-coordinate of $ab$ times the base point (RFC 7748, Section 6.1). KDF_RK is a deterministic function of its two inputs. $\square$

**Lemma 2 (keys of each chain).** Every message number $i$ of chain $j$ is encrypted under $mk_{j,i}$, and the header carries $pn$ equal to the length of chain $j - 2$ (or 0 for $j \le 2$).

*Proof.* The sender of chain $j$ sets $CK_s$ in line L2 (for $j = 1$, with $RK_0 = SK$ and $\mathrm{DH}(P_1, P_0)$) or in line L27 (for $j \ge 2$, with the root key $RK_{j-1}$ that it got in line L25 and $\mathrm{DH}(P_j, P_{j-1})$). By the definition this is $CK_j$, and the root key becomes $RK_j$. Line L23 sets $N_s = 0$, and each call of lines L4 to L6 uses $\mathrm{KDF\_CK}$ once and increments $N_s$, so message $i$ gets $mk_{j,i}$. Line L23 also sets $PN$ to the number of messages sent in the sender's previous chain, $j - 2$; after line L27 the sender never uses that chain again, so this number is its final length. $\square$

**Lemma 3 (order of ratchet keys).** While a party's own current key is $P_{k}$, every message it receives carries $dh = P_m$ with $m \le k + 1$ and $m \equiv k + 1 \pmod 2$. When its receiving key $DH_r$ is $P_{k-1}$ (with $P_{-1}$ the empty value, for Bob before his first message), a header with $dh \ne DH_r$ either carries $P_{k+1}$ or belongs to a chain $m < k - 1$.

*Proof.* The peer creates $P_{k+2}$ only in line L26 after it received a message with $P_{k+1}$, and $P_{k+1}$ is created by our party only after it moves on from $P_k$. So while our key is $P_k$, the peer's keys are at most $P_{k+1}$, and the peer's keys have the other parity. The last part follows, since $P_{k-1} = DH_r$. $\square$

**Invariant.** For a party whose receiving key is $DH_r = P_r$ with counter $N_r$:

1. $RK$ is $RK_{r+1}$ and, if $r \ge 1$, $CK_r$ in the state equals $c_{r, N_r}$ (the receiving chain key after $N_r$ steps);
2. for each $i < N_r$, message $i$ of chain $r$ was already decrypted, or $\mathrm{MKSKIPPED}[(P_r, i)] = mk_{r,i}$;
3. for each earlier chain $m < r$ of the peer and each $i$ less than its length, message $i$ of chain $m$ was already decrypted, or $\mathrm{MKSKIPPED}[(P_m, i)] = mk_{m,i}$;
4. every entry of MKSKIPPED has this form, and no entry belongs to a message that was already decrypted.

In every state the party's own key pair is $P_{r+1}$. For Bob after line L3, we write $P_{-1}$ for the empty value of $DH_r$, so $r = -1$, his own key is $P_0$, $RK = SK = RK_0$, and MKSKIPPED is empty. For Alice after lines L1 and L2, $r = 0$, her own key is $P_1$, $RK = RK_1$, and she has received nothing. So the invariant holds after initialization.

**Lemma 4 (skipping keeps the invariant).** A call $\mathrm{SkipMessageKeys}(u)$ that passes line L19 leaves the invariant true, with $N_r = \max(N_r, u)$.

*Proof.* If $CK_r$ is none there is no receiving chain and nothing changes. Else each pass of lines L21 and L22 replaces $c_{r,N_r}$ by $c_{r,N_r+1}$, stores $mk_{r,N_r}$ under $(P_r, N_r)$ and increments $N_r$. Message $N_r$ was not yet decrypted, because it was not stored and its index is not below $N_r$; so items 2 and 4 hold. $\square$

**Lemma 5 (one honest message).** Let a message with header $(P_m, pn, n)$ and ciphertext for $mk_{m,n}$ arrive, not delivered before. If the invariant holds, RatchetDecrypt returns the plaintext and the invariant holds after.

*Proof.* There are three cases.

Case A: $(P_m, n)$ is in MKSKIPPED. By item 4 the stored key is $mk_{m,n}$, so line L17 decrypts correctly, and line L18 deletes the entry, which keeps item 4 because the message is now decrypted.

Case B: not stored and $m = r$. By item 2 and delivery at most once, $n \ge N_r$. Line L12 makes $N_r = n$ by Lemma 4, line L13 gives $mk_{r,n}$ and line L14 makes $N_r = n + 1$, so items 1 and 2 hold and line L15 decrypts correctly.

Case C: not stored and $m \ne r$. If $m < r$, then $m$ is an earlier chain, and by item 3 and delivery at most once the key would be stored, which contradicts the case. So by Lemma 3, with $k = r + 1$, $m = r + 2$ (for Bob's first message, $r = -1$ and $m = 1$). By Lemma 2 the header has $pn$ equal to the length of chain $r$. Line L10 stores all remaining keys of chain $r$ (Lemma 4), so item 3 now holds for chain $r$ as well. In line L11, lines L23 and L24 set $N_r = 0$ and $DH_r = P_m$. The party holds the private key of $P_{r+1}$ and $RK = RK_{r+1}$, so by Lemma 1 line L25 yields $RK_{r+2}$ and $CK_r$ becomes $CK_{r+2} = c_{m,0}$. Line L26 creates $P_{m+1}$, and line L27 gives $RK_{m+1}$ and the sending chain $CK_{m+1}$, as in Lemma 2. Item 1 holds with $r$ replaced by $m$. Case B then applies to lines L12 to L15.

In each case decryption succeeds, so line L16 does not run. $\square$

**Theorem.** Under the assumptions stated above, every message delivered to an honest party decrypts to the plaintext that the peer encrypted, and the two parties' sending and receiving chains of each index $j$ are equal.

*Proof.* The invariant holds after initialization. By Lemma 2, each message of chain $j$ is encrypted under $mk_{j,i}$ with $dh = P_j$. By Lemma 5 and induction on the number of delivered messages, each delivered message decrypts correctly and the invariant is kept. Lemma 1 shows that both parties compute the same $(RK_j, CK_j)$ for each $j$. $\blacksquare$

**Remarks.** If a header asks to skip more than MAX_SKIP keys, line L19 raises, line L16 restores the state, and the invariant is unchanged; that message cannot be read, but later messages can. A replayed message is not in MKSKIPPED, and its index is below $N_r$ or its chain is old, so it is decrypted with the wrong key or no key, and the authentication of ENCRYPT rejects it; line L16 then restores the state.
