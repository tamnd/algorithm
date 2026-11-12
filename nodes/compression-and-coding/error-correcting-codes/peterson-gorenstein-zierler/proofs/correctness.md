---
title: The Peterson-Gorenstein-Zierler decoder corrects up to t errors
proves: [correctness, termination]
status: full
---

We use the pseudocode of the page. Let $F$ be a field and $\beta \in F$ an element of order at least $n$, so that $\beta^0, \beta^1, \ldots, \beta^{n-1}$ are distinct. The code is the set of words $c$ of length $n$ with $c(\beta^j) = 0$ for $b \le j \le b + 2t - 1$. The received word is $r = c + e$, where $e$ is nonzero exactly at the distinct positions $i_1, \ldots, i_\nu$ with $\nu \le t$. Put $X_k = \beta^{i_k}$ and $Y_k = e_{i_k} \ne 0$. The $X_k$ are distinct and nonzero.

**Syndromes.** Since $c(\beta^j) = 0$, $S_j = r(\beta^j) = e(\beta^j) = \sum_{k=1}^{\nu} Y_k X_k^{\,j}$ for $b \le j \le b + 2t - 1$.

**Lemma 1 (factorization).** For $1 \le \mu \le t$, $M_\mu = V_\mu D V_\mu^{\mathsf T}$, where $V_\mu$ is the $\mu \times \nu$ matrix with entries $X_k^{\,i}$ ($0 \le i < \mu$, $1 \le k \le \nu$) and $D = \mathrm{diag}(Y_1 X_1^{\,b}, \ldots, Y_\nu X_\nu^{\,b})$.

*Proof.* The entry $(i, j)$ of $V_\mu D V_\mu^{\mathsf T}$ is $\sum_k X_k^{\,i} \, Y_k X_k^{\,b} \, X_k^{\,j} = S_{b+i+j}$, which is the entry $(i, j)$ of $M_\mu$. All indices $b + i + j \le b + 2\mu - 2 \le b + 2t - 2$ are in range. $\square$

**Lemma 2 (the stopping point).** $M_\mu$ is singular for $\nu < \mu \le t$ and nonsingular for $\mu = \nu \ge 1$.

*Proof.* If $\mu > \nu$, then $\operatorname{rank} M_\mu \le \operatorname{rank} V_\mu \le \nu < \mu$, so $M_\mu$ is singular. If $\mu = \nu$, then $V_\nu$ is a square Vandermonde matrix with distinct nodes $X_k$, so $\det V_\nu = \prod_{k < l}(X_l - X_k) \ne 0$. Also $\det D = \prod_k Y_k X_k^{\,b} \ne 0$. So $\det M_\nu = (\det V_\nu)^2 \det D \ne 0$. $\square$

So line L2, which starts at $\nu' = t$ in line L1 and decreases by one, stops exactly at $\nu' = \nu$ when $\nu \ge 1$. If $\nu = 0$, every syndrome is 0, every $M_\mu$ is the zero matrix, the loop reaches 0, and line L3 returns no errors, which is correct.

**Lemma 3 (Newton identities).** Let $\Lambda(x) = \prod_{k=1}^{\nu}(1 - X_k x) = 1 + \Lambda_1 x + \cdots + \Lambda_\nu x^\nu$. For $0 \le i < \nu$, $\sum_{j=0}^{\nu} \Lambda_j S_{b+i+\nu-j} = 0$, with $\Lambda_0 = 1$.

*Proof.* By the syndrome formula,

$$\sum_{j=0}^{\nu} \Lambda_j S_{b+i+\nu-j} = \sum_{k=1}^{\nu} Y_k X_k^{\,b+i+\nu} \sum_{j=0}^{\nu} \Lambda_j X_k^{-j} = \sum_{k=1}^{\nu} Y_k X_k^{\,b+i+\nu} \Lambda(X_k^{-1}) = 0,$$

because $\Lambda(X_k^{-1})$ has the factor $1 - X_k X_k^{-1} = 0$. The indices $b+i+\nu-j$ lie between $b$ and $b + 2\nu - 1 \le b + 2t - 1$. $\square$

Moving the term $j = 0$ to the right side, Lemma 3 says $M_\nu (\Lambda_\nu, \ldots, \Lambda_1)^{\mathsf T} = -(S_{b+\nu}, \ldots, S_{b+2\nu-1})^{\mathsf T}$: row $i$ has the coefficient $S_{b+i+c}$ for the unknown $\Lambda_{\nu - c}$. By Lemma 2 this system has a unique solution, so line L4 computes the true locator $\Lambda$.

**Positions.** The roots of $\Lambda$ are exactly $X_1^{-1}, \ldots, X_\nu^{-1}$, and $X_k^{-1} = \beta^{-i_k}$. Since the points $\beta^{-i}$ for $0 \le i < n$ are distinct, line L5 finds exactly the set $P = \{i_1, \ldots, i_\nu\}$, with $\nu$ elements, and line L6 does not fail.

**Values.** The system of line L7 has the matrix $A$ with entries $X_k^{\,b+i}$, which is $V_\nu \, \mathrm{diag}(X_1^{\,b}, \ldots, X_\nu^{\,b})$. Both factors are nonsingular, so the system has a unique solution. The true values satisfy it by the syndrome formula, so line L7 returns $Y_1, \ldots, Y_\nu$, and $r - e$ is the codeword $c$.

**Termination.** Line L2 runs at most $t$ times, each with a finite elimination. Line L5 tests $n$ positions and line L7 is one finite elimination. $\blacksquare$
