---
title: XMSS signatures verify
proves: [correctness]
status: full
---

**Setting.** All hash calls are keyed and masked through the public seed $SEED$ and an address $ADRS$, and the address of a call is a function of its position only: the type (chain, L-tree or tree node), the leaf index, the chain and step numbers, or the height and index of a node. RAND_HASH$(L, R, ADRS)$ (lines L1 and L2) and the chain step $x \mapsto F(KEY, x \oplus BM)$ with $KEY$, $BM$ derived from $(SEED, ADRS)$ are therefore fixed functions of the position. Write $c^{j}_{q,i}(x)$ for $j$ chain steps of chain $i$ of leaf $q$ from position 0, and $c_{q,i}[a, b)(x)$ for steps $a$ to $b - 1$.

**Lemma 1 (WOTS+ public key from a signature).** Let $M'$ be a message digest and $b_0, \ldots, b_{len-1}$ its WOTS+ digits with checksum. If $\sigma_i = c^{b_i}_{q,i}(sk_i)$ for every $i$, then $c_{q,i}[b_i, w-1)(\sigma_i) = pk_i$, the public value of chain $i$.

*Proof.* The steps $0, \ldots, b_i - 1$ followed by the steps $b_i, \ldots, w-2$ are the steps $0, \ldots, w - 2$ in order. Each step depends only on its position $(q, i, j)$, through the address, and not on who computes it. So the composition equals $c^{w-1}_{q,i}(sk_i) = pk_i$. $\square$

**Lemma 2 (the L-tree is a function of the list).** The value of LTREE (lines L3 and L4) depends only on the list $pk_0, \ldots, pk_{len-1}$, the seed and the leaf index.

*Proof.* The loop runs while more than one value is left. In each round, values $2i$ and $2i+1$ are hashed with the address (L-tree $q$, height of the round, index $i$), and an odd last value moves up unchanged. The number of rounds and the addresses depend only on $len$, so equal lists give equal results. $\square$

**Lemma 3 (the path).** Let $v_0$ be leaf $q$ and, for $k = 0, \ldots, h - 1$, let $v_{k+1}$ = RAND_HASH$(v_k, auth_k)$ if bit $k$ of $q$ is 0 and RAND_HASH$(auth_k, v_k)$ otherwise, with the node address (height $k$, index $\lfloor q / 2^{k+1} \rfloor$), where $auth_k$ is the node of height $k$ with index $\lfloor q/2^k \rfloor \oplus 1$. Then $v_k$ is the node of height $k$ and index $\lfloor q / 2^k \rfloor$, and $v_h$ is the root.

*Proof.* By induction on $k$, as for the Merkle signature scheme. Let $t = \lfloor q / 2^k \rfloor$ and $u = \lfloor t/2 \rfloor$. The node of height $k + 1$ and index $u$ is, by key generation, RAND_HASH of the nodes $2u$ and $2u + 1$ of height $k$ with the address (height $k$, index $u$). If bit $k$ of $q$ is 0 then $t = 2u$ and $v_k$ is the left child; otherwise $t = 2u + 1$ and $v_k$ is the right child. The sibling $auth_k$ is the other child, so in both cases $v_{k+1}$ is node $u$ of height $k+1$. $\square$

**Theorem 4.** For every key pair and every message $M$, an honest signature made with index $idx < 2^h$ passes verification.

*Proof.* Signer and verifier compute the same $M' = H\_msg(r \| root \| idx, M)$ (lines L7 and L10), because $r$ and $idx$ are in the signature and $root$ is in the public key. Line L8 gives $\sigma_i = c^{b_i}_{idx,i}(sk_i)$ for the digits $b$ of $M'$. By Lemma 1 the verifier gets back the WOTS+ public key of leaf $idx$, by Lemma 2 line L11 gives the leaf, and by Lemma 3 line L12 ends at the root, so line L13 accepts. $\square$

**Remarks on security.** Section 9.1 of RFC 8391 refers to Hülsing, Rijneveld and Song (PKC 2016) for a proof: a forger must break the multi-function multi-target second preimage resistance of $F$ or $H$, the pseudorandomness of PRF, or the multi-target extended target collision resistance of $H\_msg$. Collision resistance is not needed. The proof uses the bitmasks in the same way as the WOTS+ proof: a reduction sets the bitmask of one hash call so that the honest input is its challenge. Like all Merkle schemes, the proof needs that no index is used twice.
