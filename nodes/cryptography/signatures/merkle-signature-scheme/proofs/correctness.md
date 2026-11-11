---
title: Merkle signatures verify, and are unforgeable if the one-time scheme is
proves: [correctness]
status: full
---

**Setting.** The tree has height $h$. $L_q$ is leaf $q$, the hash of one-time public key $q$. Node $j$ of level $i$ is $N_{i,j}$, with $N_{0,j} = L_j$ and $N_{i,j} = P(N_{i-1,2j}, N_{i-1,2j+1})$ for the node hash $P$ (line L3). The root is $N_{h,0}$. For a leaf $q$, the node of level $i$ on its path is $N_{i, \lfloor q / 2^i \rfloor}$, and the authentication path is $a_i = N_{i, \lfloor q/2^i \rfloor \oplus 1}$ for $i = 0, \ldots, h-1$ (line L8).

**Lemma 1 (the path climbs to the root).** Let $v_0 = L_q$, and for $i = 0, \ldots, h-1$ let $v_{i+1} = P(v_i, a_i)$ if bit $i$ of $q$ is 0, and $v_{i+1} = P(a_i, v_i)$ otherwise (line L11). Then $v_i = N_{i, \lfloor q/2^i \rfloor}$ for every $i$, and in particular $v_h$ is the root.

*Proof.* By induction on $i$. For $i = 0$, $v_0 = L_q = N_{0,q}$. Assume $v_i = N_{i,t}$ with $t = \lfloor q / 2^i \rfloor$. Bit $i$ of $q$ is the last bit of $t$. If it is 0, $t = 2u$ with $u = \lfloor q/2^{i+1} \rfloor$, the sibling is $a_i = N_{i, 2u+1}$, and $v_{i+1} = P(N_{i,2u}, N_{i,2u+1}) = N_{i+1,u}$. If it is 1, $t = 2u + 1$, $a_i = N_{i,2u}$, and $v_{i+1} = P(N_{i,2u}, N_{i,2u+1}) = N_{i+1,u}$. $\square$

**Lemma 2 (an honest signature verifies).** If the signer signs $M$ with leaf $q$, then VERIFY accepts.

*Proof.* Line L7 makes a one-time signature with key $q$. The one-time scheme recomputes the one-time public key from a valid signature, so line L10 gives $L_q$. By Lemma 1, line L11 ends at the root, and line L12 accepts. $\square$

**Theorem 3 (many-time unforgeability).** Let $A$ make at most $2^h$ signing queries, run in time $t$, and output a forgery with chance $\varepsilon$. Then there is a forger $F$ against the one-time scheme (one query, EUF-1-CMA) and a collision finder $C$ for the hashes $P$ and the leaf hash, both of time about $t$ plus the work of key generation, with

$$\varepsilon \le 2^h \cdot \Pr[F \text{ wins}] + \Pr[C \text{ finds a collision}].$$

*Proof.* The signer uses each leaf at most once, because the index $q$ grows by one with each signature (line L6) and signing stops after $2^h$ signatures. Let $(M^*, \sigma^*)$ with $\sigma^* = (q^*, s^*, a^*)$ be a valid forgery for a message $M^*$ that $A$ did not ask for. Let $v^*_0, \ldots, v^*_h$ be the values of line L11 for it; $v^*_h$ is the root.

*Case 1: $v^*_0 \ne L_{q^*}$.* The honest path of leaf $q^*$ is $N_{0,q^*}, N_{1, \lfloor q^*/2 \rfloor}, \ldots$, which ends at the root too. Let $i$ be the largest level with $v^*_i \ne N_{i, \lfloor q^*/2^i \rfloor}$; then $i < h$ and $v^*_{i+1} = N_{i+1, \lfloor q^*/2^{i+1} \rfloor}$. The two values at level $i + 1$ are $P$ of two input pairs, and the pairs differ in the first or the second entry, because $v^*_i$ differs from the honest node. So the pairs are a collision of $P$. $C$ makes all keys itself, answers all queries, and finds this collision. Similarly, if $v^*_0 = L_{q^*}$ but the one-time public key computed in line L10 is not the one-time public key $q^*$, the two keys collide under the leaf hash.

*Case 2: the one-time public key computed in line L10 is key $q^*$.* Then $s^*$ is a valid one-time signature on $M^*$ under key $q^*$. $F$ gets a one-time public key $pk$ from its challenger, picks $q_0$ uniformly in $[0, 2^h)$, makes all other one-time keys itself, puts $pk$ at leaf $q_0$, and builds the tree. The public key has the same distribution as a real one. When $A$ asks for the signature with leaf $q_0$, $F$ asks its one signing query on that message. All other queries it answers itself. If $q^* = q_0$, $F$ outputs $(M^*, s^*)$. Leaf $q_0$ signed at most one message, which is not $M^*$, so this is a valid one-time forgery. The choice $q_0$ is hidden from $A$, so $q^* = q_0$ with chance $2^{-h}$, independent of the event of Case 2.

Adding the cases gives the bound. $\blacksquare$

**Remarks.** The factor $2^h$ is the loss of the reduction. If a signer reuses a leaf, Case 2 needs a one-time key that signed two messages, and the proof fails; for Winternitz and Lamport leaves that is a real attack. The same proof works with the hash of the message replaced by a randomized hash, and with collision resistance replaced by second preimage resistance if each node hash uses fresh bitmasks, as in XMSS.
