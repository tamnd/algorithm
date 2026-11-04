---
title: The sqrt tree stores the products it names and answers each query with at most two combines
proves: [correctness, termination]
status: full
---

Let $(S, \oplus)$ be a semigroup and $n \ge 1$. For $0 \le a \le b \le n - 1$ write $\Pi(a, b) = A[a] \oplus \cdots \oplus A[b]$. By associativity, for $a \le m < b$,

$$\Pi(a, b) = \Pi(a, m) \oplus \Pi(m + 1, b). \tag{1}$$

For a layer $j$ with block exponent $b_j$, the block of an index $i$ is $\beta_j(i) = \lfloor i / 2^{b_j} \rfloor$, and block $p$ is the range $[p 2^{b_j}, \min(n, (p + 1) 2^{b_j}) - 1]$. Write $\mathrm{st}_j(p)$ and $\mathrm{en}_j(p)$ for its first and last index.

**Termination.** Every loop of BUILD runs over a finite range that does not change in the loop, and the list of layers is finite because $k_{j+1} = \lceil k_j / 2 \rceil < k_j$ for $k_j \ge 2$. QUERY has no loop.

**Lemma 1 (the layer table).** For each $1 \le h < K$ there is exactly one layer $j$ with $b_j \le h < k_j$, and line L2 sets $\mathit{LAYER}[h]$ to it.

*Proof.* The intervals $[b_j, k_j) = [k_{j+1}, k_j)$ are consecutive pieces of $[k_t, k_0)$, where layer $t$ is the last one. They are disjoint, and their union is $[b_t, K)$. The last layer has $k_t \ge 2$ and $k_{t+1} = \lceil k_t / 2 \rceil < 2$, so $k_t = 2$, since $\lceil 3/2 \rceil = 2$, and $b_t = 1$. If $K < 2$, there is no layer and no $h$ with $1 \le h < K$. $\square$

**Lemma 2 (prefixes and suffixes).** After lines L3 and L4, $\mathit{PRE}_j[i] = \Pi(\mathrm{st}_j(\beta_j(i)), i)$ and $\mathit{SUF}_j[i] = \Pi(i, \mathrm{en}_j(\beta_j(i)))$ for each layer $j$ and each $0 \le i \le n - 1$.

*Proof.* Fix a block $[s, e]$. By induction on $i$ from $s$: $\mathit{PRE}_j[s] = A[s] = \Pi(s, s)$, and $\mathit{PRE}_j[i] = \Pi(s, i - 1) \oplus A[i] = \Pi(s, i)$ by (1). The suffixes are the mirror image, by induction on $i$ downward from $e$, with $A[i] \oplus \Pi(i + 1, e) = \Pi(i, e)$. The blocks of a layer are disjoint and cover $[0, n - 1]$, so every entry is set once. $\square$

**Lemma 3 (the between table).** After lines L5 and L6, for blocks $p \le q$ of the same segment of layer $j$, $\mathit{BTW}_j[p, q] = \Pi(\mathrm{st}_j(p), \mathrm{en}_j(q))$.

*Proof.* By Lemma 2, $\mathit{SUF}_j[\mathrm{st}_j(p)] = \Pi(\mathrm{st}_j(p), \mathrm{en}_j(p))$, the product of block $p$. By induction on $q$: $\mathit{BTW}_j[p, p]$ is this product, and $\mathit{BTW}_j[p, q] = \Pi(\mathrm{st}_j(p), \mathrm{en}_j(q - 1)) \oplus \Pi(\mathrm{st}_j(q), \mathrm{en}_j(q)) = \Pi(\mathrm{st}_j(p), \mathrm{en}_j(q))$ by (1), since $\mathrm{en}_j(q - 1) + 1 = \mathrm{st}_j(q)$. The loop of line L6 stops at the last block of the segment that exists, so every entry it writes names a range inside $[0, n - 1]$. $\square$

**Lemma 4 (the layer separates $l$ and $r$).** Let $0 \le l < r \le n - 1$, let $h \ge 1$ be the highest bit of $l$ xor $r$, and let $j = \mathit{LAYER}[h]$. Then $p = \beta_j(l)$ and $q = \beta_j(r)$ satisfy $p < q$, and $p$ and $q$ lie in the same segment of layer $j$.

*Proof.* Since $r \le n - 1 < 2^K$, the bits of $l$ and $r$ above $K - 1$ are 0, so $h < K$ and Lemma 1 applies: $b_j \le h < k_j$. The numbers $l$ and $r$ agree on all bits above $h$, so $\lfloor l / 2^{h+1} \rfloor = \lfloor r / 2^{h+1} \rfloor$, and since $h + 1 \le k_j$, also $\lfloor l / 2^{k_j} \rfloor = \lfloor r / 2^{k_j} \rfloor$: the same segment. They differ at bit $h \ge b_j$, so $\lfloor l / 2^{b_j} \rfloor \ne \lfloor r / 2^{b_j} \rfloor$, and $l < r$ gives $p < q$. A block lies inside one segment, because $2^{b_j}$ divides $2^{k_j}$. $\square$

**Lemma 5 (query).** For $0 \le l \le r \le n - 1$, QUERY$(l, r)$ returns $\Pi(l, r)$ and applies $\oplus$ at most twice.

*Proof.* If $l = r$, line L7 returns $A[l] = \Pi(l, l)$ with no combine. If $h = 0$, then $l$ and $r$ differ only in bit 0 and $l < r$, so $r = l + 1$ and line L8 returns $A[l] \oplus A[r] = \Pi(l, l + 1)$ with one combine. Otherwise $h \ge 1$, and by Lemma 4 the blocks $p < q$ are in one segment of layer $j$. By Lemma 2, $\mathit{SUF}_j[l] = \Pi(l, \mathrm{en}_j(p))$ and $\mathit{PRE}_j[r] = \Pi(\mathrm{st}_j(q), r)$; both blocks are whole blocks of $2^{b_j}$ indices except possibly block $q$, which may be clipped at $n - 1 \ge r$, so these ranges are as stated. If $q = p + 1$, then $\mathrm{en}_j(p) + 1 = \mathrm{st}_j(q)$, and line L10 returns $\Pi(l, r)$ by (1), with one combine. If $q > p + 1$, the blocks $p + 1$ and $q - 1$ lie in the same segment, between $p$ and $q$, and by Lemma 3 $\mathit{BTW}_j[p + 1, q - 1] = \Pi(\mathrm{st}_j(p + 1), \mathrm{en}_j(q - 1))$. The three ranges are consecutive and cover $[l, r]$ in order, so line L11 returns $\Pi(l, r)$ by (1) twice, with two combines. No step exchanges two factors, so commutativity is not used. $\square$

**Theorem.** After BUILD on $A[0 \ldots n - 1]$ over any semigroup, QUERY$(l, r)$ returns $A[l] \oplus \cdots \oplus A[r]$ with at most two applications of $\oplus$, for all $0 \le l \le r \le n - 1$, and all procedures end.

*Proof.* Lemmas 1 to 5 and the termination argument. $\blacksquare$
