---
title: SLH-DSA signatures verify
proves: [correctness]
status: full
---

**Setting.** We use the functions of FIPS 205. Every call of $F$, $H$ and $T_\ell$ takes $PK.seed$ and a 32-byte address $ADRS$, and every PRF call takes $PK.seed$, $SK.seed$ and an address. The address of a call depends only on the position of the computed value in the key: layer, tree, type, key pair, chain or height, and hash index or node index. So each chain step, tree node, secret value and compression is a fixed function of its position. Signer and verifier set the same address words at each position (Algorithms 5 to 17), and we use this fact without repeating it.

**Lemma 1 (WOTS+).** Let $\sigma$ = wots_sign$(M, \ldots, ADRS)$. Then wots_pkFromSig$(\sigma, M, PK.seed, ADRS)$ = wots_pkGen$(SK.seed, PK.seed, ADRS)$.

*Proof.* Both functions compute the same digits $b_0, \ldots, b_{len-1}$ from $M$ (base_2b and the checksum). For chain $i$, $\sigma_i$ is the result of steps $0, \ldots, b_i - 1$ from the secret value; the verifier applies steps $b_i, \ldots, w - 2$. Each step $j$ is $F$ with hash address $j$, so the composition is the chain of $w - 1$ steps of wots_pkGen, and gives $tmp_i$. Both functions compress the same list $tmp$ with $T_{len}$ and the same WOTS_PK address. $\square$

**Lemma 2 (climbing a tree).** Let the nodes of a tree of height $z$ be defined by $v(0, i)$ for the leaves and $v(j, i) = H(PK.seed, ADRS_{j,i}, v(j-1, 2i) \| v(j-1, 2i+1))$, where $ADRS_{j,i}$ has height $j$ and index $i$ (plus a fixed offset of the index for the FORS trees). Given leaf $v(0, q)$ and the siblings $auth_j = v(j, \lfloor q/2^j \rfloor \oplus 1)$, the loop of Algorithm 11 (lines 6 to 18), or of Algorithm 17 (lines 8 to 18), returns $v(z, 0)$.

*Proof.* By induction on $j$: after round $j$, the current node is $v(j+1, \lfloor q/2^{j+1} \rfloor)$ and the tree index in $ADRS$ is $\lfloor q/2^{j+1} \rfloor$. The index starts at $q$ and is halved (after subtracting 1 for an odd value) in each round, which gives $\lfloor q/2^{j+1} \rfloor$. If $\lfloor q/2^j \rfloor$ is even, the current node is the left child and the sibling the right one; otherwise the order is swapped. In both cases the hash input and the address are those that define $v(j+1, \lfloor q/2^{j+1} \rfloor)$. For FORS tree $i$ the leaf index starts at $i \cdot 2^a + q$ and the same argument works with the offset, as $\lfloor (i 2^a + q)/2^{j} \rfloor = i 2^{a-j} + \lfloor q/2^j \rfloor$. $\square$

**Lemma 3 (XMSS).** For $\Sigma$ = xmss_sign$(M, SK.seed, idx, PK.seed, ADRS)$, xmss_pkFromSig$(idx, \Sigma, M, PK.seed, ADRS)$ = xmss_node$(SK.seed, 0, h', PK.seed, ADRS)$, the root of the XMSS tree at the layer and tree address of $ADRS$.

*Proof.* xmss_node defines the tree of Lemma 2 with the WOTS+ public keys as leaves. By Lemma 1 the first part of xmss_pkFromSig gives leaf $idx$. Line 2 of xmss_sign takes $auth_j$ = xmss_node$(\ldots, \lfloor idx/2^j \rfloor \oplus 1, j, \ldots)$, the sibling of Lemma 2. Lemma 2 gives the root. $\square$

**Lemma 4 (FORS).** For $\Sigma$ = fors_sign$(md, \ldots, ADRS)$, fors_pkFromSig$(\Sigma, md, PK.seed, ADRS)$ equals $T_k$ of the $k$ roots fors_node$(SK.seed, i, a, PK.seed, ADRS)$, $i = 0, \ldots, k-1$.

*Proof.* Both functions read the same indices $q_i$ from $md$ with base_2b. For tree $i$ the signature holds the secret value of leaf $i 2^a + q_i$ (line 4 of Algorithm 16), and the verifier hashes it with $F$ at height 0 and index $i 2^a + q_i$, which is the leaf fors_node computes. Line 7 of Algorithm 16 takes the siblings fors_node$(\ldots, i 2^{a-j} + (\lfloor q_i/2^j \rfloor \oplus 1), j, \ldots)$, so Lemma 2 gives the root of tree $i$. Both sides compress the $k$ roots with the same FORS_ROOTS address. $\square$

**Lemma 5 (hypertree).** For every $n$-byte $M$ and indices $idx_{tree} < 2^{h - h'}$, $idx_{leaf} < 2^{h'}$, ht_verify$(M$, ht_sign$(M, \ldots, idx_{tree}, idx_{leaf}), PK.seed, idx_{tree}, idx_{leaf}, PK.root)$ is true.

*Proof.* Signer and verifier compute the same sequence of (layer $j$, tree address, leaf index): both start with $(0, idx_{tree}, idx_{leaf})$ and both move from layer $j$ to $j+1$ by $idx_{leaf} \leftarrow idx_{tree} \bmod 2^{h'}$ and $idx_{tree} \leftarrow idx_{tree} \gg h'$. Let $r_j$ be the root of the tree used at layer $j$. The signer signs $M$ at layer 0 and $r_{j-1}$ at layer $j$, computing $r_{j-1}$ with xmss_pkFromSig, which by Lemma 3 is the true root. The verifier starts with $node = M$; by Lemma 3 and induction on $j$, after layer $j$ it holds $r_j$. After layer $d - 1$ the tree address is $idx_{tree} \gg (d-1)h' = 0$, as $idx_{tree} < 2^{(d-1)h'}$, so $r_{d-1}$ is xmss_node$(SK.seed, 0, h', \ldots)$ at layer $d - 1$ and tree 0, which is $PK.root$ by Algorithm 18. $\square$

**Theorem 6.** For every key pair from Algorithm 18, every message $M$ and context $ctx$ of at most 255 bytes, and both the hedged and the deterministic variant, slh_verify$(M$, slh_sign$(M, ctx, SK), ctx, PK)$ is true.

*Proof.* Both sides form $M' = 0 \| |ctx| \| ctx \| M$ (line L1). The signature has length $(1 + k(1+a) + h + d \cdot len) n$, so the length check passes. The verifier reads $R$ from the signature and computes the same digest $H_{msg}(R, PK.seed, PK.root, M')$ as line L3 of the signer, so it gets the same $md$, $idx_{tree}$ and $idx_{leaf}$. The randomness $opt\_rand$ only affects $R$, which the verifier reads. With the same FORS address, Lemma 4 gives the verifier the FORS public key $PK_{FORS}$ that the signer computed on line L6, and that the signer signed with ht_sign. Lemma 5 then shows that ht_verify accepts. $\square$

**Remarks on security.** The SPHINCS+ paper (CCS 2019) reduces security to multi-target properties of the tweakable hash functions $F$, $H$ and $T_\ell$, the pseudorandomness of PRF and $PRF_{msg}$, and the interleaved target subset resilience of $H_{msg}$ (the chance that the FORS leaves of a new digest are all already revealed). The "simple" form that FIPS 205 approves gets these properties when the hash is modelled as a random oracle. Kudinov, Kiktenko and Fedorov (2020) found a gap in the WOTS+ part of the tight proof, and Hülsing and Kudinov (Asiacrypt 2022) gave a corrected proof. The parameter sets of FIPS 205 are chosen for at most $2^{64}$ signatures per key pair, because each new signature reveals more FORS leaves.
