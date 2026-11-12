---
title: Chien search returns exactly the positions i with Lambda(alpha^(-i)) = 0
proves: [correctness, termination]
status: full
---

We use the pseudocode of the page. Let $\alpha$ be a primitive element of $\mathrm{GF}(q)$, so $\alpha$ has multiplicative order $q - 1$. Let $\Lambda(x) = \sum_{j=0}^{\nu} \Lambda_j x^j$ and $1 \le n \le q - 1$.

**Invariant.** At the test of line L4 in the step with index $i$ ($0 \le i < n$), $T_j = \Lambda_j \alpha^{-ij}$ for every $j$ with $0 \le j \le \nu$.

*Initialization.* Line L1 sets $T_j = \Lambda_j = \Lambda_j \alpha^{0}$, which is the claim for $i = 0$.

*Maintenance.* Assume the claim at step $i$. Line L4 does not change any $T_j$. Line L5 leaves $T_0$ unchanged, which is $\Lambda_0 \alpha^{-(i+1) \cdot 0}$, and for $1 \le j \le \nu$ sets $T_j = \Lambda_j \alpha^{-ij} \cdot \alpha^{-j} = \Lambda_j \alpha^{-(i+1)j}$. So the claim holds at step $i + 1$.

**The test.** By the invariant, at step $i$,

$$T_0 + T_1 + \cdots + T_\nu = \sum_{j=0}^{\nu} \Lambda_j \bigl(\alpha^{-i}\bigr)^{j} = \Lambda(\alpha^{-i}).$$

So line L4 appends $i$ exactly when $\Lambda(\alpha^{-i}) = 0$.

**Result.** The loop of line L3 takes each $i$ in $0, \ldots, n - 1$ once, in increasing order, and appends nothing else. So the returned list is the increasing list of all $i$ in $0 \le i < n$ with $\Lambda(\alpha^{-i}) = 0$. Since $n \le q - 1$ and $\alpha$ has order $q - 1$, the elements $\alpha^{-i}$ for these $i$ are distinct, so each root of $\Lambda$ of the form $\alpha^{-i}$ gives exactly one list entry.

**Use in decoding.** If $\Lambda(x) = \prod_{k=1}^{\nu} (1 - X_k x)$ with distinct $X_k = \alpha^{i_k}$ and $0 \le i_k < n$, then $\Lambda(\alpha^{-i}) = \prod_k (1 - \alpha^{i_k - i})$ is zero exactly when $i = i_k$ for some $k$, because $\alpha^{e} = 1$ only for $e \equiv 0 \pmod{q-1}$ and $|i_k - i| < q - 1$. So the search returns $\{i_1, \ldots, i_\nu\}$, which has $\nu = \deg \Lambda$ elements. Conversely, a polynomial of degree $\nu$ has at most $\nu$ roots, so if the search returns $\nu$ positions, $\Lambda = \Lambda_0 \prod_k (1 - \alpha^{i_k} x)$ for those positions.

**Termination.** The two loops have fixed bounds $n$ and $\nu$. $\blacksquare$
