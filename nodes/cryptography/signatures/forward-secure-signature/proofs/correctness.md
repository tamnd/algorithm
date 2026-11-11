---
title: The tree-based forward-secure signature verifies and keeps the past safe
proves: [correctness]
status: full
---

**Setting.** There are $T = 2^h$ periods. The seeds are $s_0$ (random) and $s_{t+1} = G(s_t)$. Period $t$ has $2^b$ Winternitz one-time keys; key $j$ has the secret values $x_{t,j,i} = H(\text{secret}, s_t, j, i)$, and its leaf $\lambda_{t,j}$ is the hash of the chain ends. The period tree of $t$ has the leaves $\lambda_{t,0}, \ldots, \lambda_{t,2^b-1}$ and root $\rho_t$; the top tree has the leaves $\rho_0, \ldots, \rho_{T-1}$ and root $PK$. Every hash call takes its position (period, key, chain, step, or tree tag, height and index) as input, so all chain steps and nodes are fixed functions of their positions.

**Lemma 1 (the key of period $t$ holds $s_t$).** After $t$ updates the signer holds $s_t$.

*Proof.* Key generation keeps $s_0$ (line L1). Each update replaces $s_u$ with $G(s_u) = s_{u+1}$ (lines L4 and L5). By induction, after $t$ updates the stored seed is $s_t$. $\square$

**Lemma 2 (one-time signatures).** If $\sigma_i$ is chain $i$ of key $(t, j)$ applied $d_i$ times to $x_{t,j,i}$, where $d_0, \ldots, d_{66}$ are the digits and checksum digits of $D = H(\text{msg}, M)$, then the verifier's chain ends equal the true chain ends, and it computes $\lambda_{t,j}$.

*Proof.* The verifier computes the same digits from $M$. Steps $0, \ldots, d_i - 1$ followed by steps $d_i, \ldots, w - 2$ are the $w - 1$ steps of key generation, and each step depends only on its position. The leaf hash takes the same position and the same ends. $\square$

**Lemma 3 (paths).** For a tree with leaves $v_0, \ldots, v_{2^z - 1}$ built by `build`, climbing from $v_q$ with the siblings $\text{path}(q)$ gives the root.

*Proof.* As for the Merkle signature scheme: by induction on $k$, after $k$ steps the value is the node of height $k$ and index $\lfloor q / 2^k \rfloor$. Bit $k$ of $q$ says whether this node is a left or a right child, and the parent hash has the same tag, height $k$ and index $\lfloor q/2^{k+1} \rfloor$ in both computations. $\square$

**Theorem 4 (correctness).** In every period $t$, each of the first $2^b$ signatures verifies under $PK$, also after later updates.

*Proof.* By Lemma 1 the signer signs with $s_t$, so line L7 makes the values of Lemma 2 for key $(t, j)$, and the verifier computes $\lambda_{t,j}$. The period tree of $t$ that the signer builds in `_enter` from $s_t$ is the tree whose root $\rho_t$ key generation put in the top tree, because both use $s_t$ and the same positions. By Lemma 3, line L9 gives $\rho_t$ and line L10 gives $PK$. The signature holds all values that verification needs, so later updates do not change the result. $\square$

**Theorem 5 (forward security, sketch).** Model $H$ and $G$ as random oracles. Let an attacker get signatures of its choice in periods $0, \ldots, \beta - 1$ and the full secret key of period $\beta$. Its chance to output a valid signature for a period $t < \beta$ on a message that was not signed in period $t$ is at most about $q_H \cdot \beta / 2^{256} + T \cdot 2^b \cdot \varepsilon_{OTS} + \varepsilon_{CR}$, where $q_H$ is its number of oracle queries, $\varepsilon_{OTS}$ bounds a forgery of one Winternitz key after one signature, and $\varepsilon_{CR}$ bounds a collision in the tree hashes.

*Proof sketch.* The secret key of period $\beta$ is $(\beta, s_\beta, \text{public nodes})$. In the random oracle model, $s_0, \ldots, s_{\beta - 1}$ are uniform values whose only link to the attacker's view is $s_\beta = G^{\beta - t}(s_t)$ and the signatures; the attacker learns an earlier seed only by querying $G$ or $H$ at it, which happens with chance at most $q_H/2^{256}$ per seed. Without the seed of period $t$, the secret values $x_{t,j,i}$ that the signer did not reveal are uniform. A valid signature for period $t$ then either climbs to $PK$ through a different leaf or path, which gives a collision in the tree hash, or reaches $\lambda_{t,j}$ for a key $(t, j)$ through a forged one-time signature, which the Winternitz checksum allows only with chance $\varepsilon_{OTS}$ (a guess over the $T \cdot 2^b$ keys costs the factor). $\square$

The same argument fails for the scheme in which every seed is $H(\text{master}, t)$: the master seed is in every period's secret key, so a key leaked in period $\beta$ gives $s_0$ directly. The tests show this back-dating attack.
