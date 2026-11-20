---
title: The code computes the Talmud rule, which is consistent with the contested garment rule and equals the nucleolus
proves: [correctness]
status: full
---

A bankruptcy problem is a vector of claims $c = (c_1, \ldots, c_n) \ge 0$ and an estate $E$ with $0 \le E \le C = c_1 + \cdots + c_n$. An award vector $x$ has $\sum_i x_i = E$ and $0 \le x_i \le c_i$.

**Definitions.** For $d \ge 0$ and $0 \le A \le \sum_i d_i$, constrained equal awards is $\mathrm{CEA}(d, A)_i = \min(d_i, \lambda)$, where $\lambda$ solves $\sum_i \min(d_i, \lambda) = A$. Constrained equal losses is $\mathrm{CEL}(d, A)_i = \max(0, d_i - \mu)$, where $\mu$ solves $\sum_i \max(0, d_i - \mu) = A$. The Talmud rule is

$$T(c, E) = \begin{cases} \mathrm{CEA}(c/2, E) & \text{if } E \le C/2, \\ c/2 + \mathrm{CEL}(c/2, E - C/2) & \text{if } E \ge C/2. \end{cases}$$

**Lemma 1 (CEA is well defined).** The function $g(\lambda) = \sum_i \min(d_i, \lambda)$ is continuous and nondecreasing on $[0, \infty)$, with $g(0) = 0$ and $g(\lambda) = \sum_i d_i$ for $\lambda \ge \max_i d_i$. So some $\lambda$ solves $g(\lambda) = A$. If two values $\lambda < \lambda'$ both do, then $g$ is constant on $[\lambda, \lambda']$, so no $d_i$ is above $\lambda$, and $\min(d_i, \lambda) = d_i = \min(d_i, \lambda')$ for every $i$. So the vector $\mathrm{CEA}(d, A)$ does not depend on the choice of $\lambda$. $\square$

**Lemma 2 (lines L5 to L10 compute CEA).** Let the code sort $d$ as $d_{(1)} \le \cdots \le d_{(n)}$ (line L5), and let $\lambda^*$ be a solution of $g(\lambda) = A$. Before step $k$ of line L6 (counting from 1), the invariant is: the players $(1), \ldots, (k-1)$ have $x = d$ and $d_{(j)} \le \lambda^*$ for $j < k$, and $\mathit{rest} = A - \sum_{j < k} d_{(j)}$. Then $\sum_{j \ge k} \min(d_{(j)}, \lambda^*) = \mathit{rest}$.

- If $d_{(k)} \le \mathit{rest}/(n - k + 1)$ (line L8), then $d_{(k)} \le \lambda^*$. Otherwise $\lambda^* < d_{(k)} \le d_{(j)}$ for all $j \ge k$, so $\mathit{rest} = (n - k + 1)\lambda^*$, and $\lambda^* = \mathit{rest}/(n - k + 1) \ge d_{(k)}$, a contradiction. So paying $d_{(k)}$ in full is right, and the invariant holds for $k + 1$.
- If $d_{(k)} > \lambda = \mathit{rest}/(n - k + 1)$ (line L9), then $\lambda^* < d_{(k)}$: otherwise every $j \ge k$ has $\min(d_{(j)}, \lambda^*) \ge d_{(k)}$, and $\mathit{rest} \ge (n - k + 1) d_{(k)} > \mathit{rest}$. So every $j \ge k$ gets $\lambda^*$, and $(n - k + 1)\lambda^* = \mathit{rest}$ gives $\lambda^* = \lambda$. Line L9 gives exactly this.
- If line L8 succeeds for every $k$, the invariant gives $d_{(j)} \le \lambda^*$ for all $j$, so $A = g(\lambda^*) = \sum_j d_j$, and the output $x = d$ is right.

All divisions are exact fractions, so the output is exactly $\mathrm{CEA}(d, A)$. $\square$

**Lemma 3 (lines L1 to L4 compute $T$).** If $E \le C/2$, line L2 returns $\mathrm{CEA}(c/2, E)$. Otherwise lines L3 and L4 return $c - \mathrm{CEA}(c/2, C - E)$. For $d = c/2$ the losses of CEL are $d_i - \max(0, d_i - \mu) = \min(d_i, \mu)$, so $\mathrm{CEL}(d, B) = d - \mathrm{CEA}(d, \sum_i d_i - B)$. With $B = E - C/2$ this gives $c/2 + \mathrm{CEL}(c/2, E - C/2) = c/2 + c/2 - \mathrm{CEA}(c/2, C - E)$, which is what line L4 returns. At $E = C/2$ both branches give $c/2$. $\square$

**Lemma 4 (self-duality).** $T(c, C - E) = c - T(c, E)$. *Proof.* If $E < C/2$, then $C - E > C/2$, and by Lemma 3, $T(c, C - E) = c - \mathrm{CEA}(c/2, E) = c - T(c, E)$. The case $E > C/2$ is the same statement with $E$ and $C - E$ exchanged, and $E = C/2$ gives $c/2$ on both sides. $\square$

**The contested garment rule.** For two claimants with claims $c_i, c_j$ and an estate $e \le c_i + c_j$, let $a_i = \max(0, e - c_j)$, the part of $e$ that claimant $j$ does not claim, and $a_j = \max(0, e - c_i)$. The rule gives $\mathrm{CG}_i(e) = a_i + (e - a_i - a_j)/2 = (e + a_i - a_j)/2$, and the same for $j$. It is self-dual: $c_i - \mathrm{CG}_i(c_i + c_j - e) = \mathrm{CG}_i(e)$. To see this, write $p(z) = \max(0, z)$ and use $p(z) - p(-z) = z$. Then $c_i - \mathrm{CG}_i(c_i + c_j - e) = \tfrac12 (c_i - c_j + e - p(c_i - e) + p(c_j - e))$, and the difference from $\tfrac12 (e + p(e - c_j) - p(e - c_i))$ is $\tfrac12 (c_i - c_j + (c_j - e) + (e - c_i)) = 0$. Each $\mathrm{CG}_i(e)$ is nondecreasing in $e$, because $e + a_i - a_j$ has slope 0, 1 or 2 in $e$ on each piece.

**Theorem 1 (consistency).** Let $x = T(c, E)$. For every pair $i \ne j$, $(x_i, x_j) = \mathrm{CG}(x_i + x_j)$ with the claims $c_i, c_j$.

*Proof.* First let $E \le C/2$, so $x_k = \min(c_k/2, \lambda)$. Let $c_i \le c_j$ and $e = x_i + x_j$.
- If $x_i = x_j = \lambda$: then $\lambda \le c_i/2$ and $e = 2\lambda \le c_i \le c_j$, so $a_i = a_j = 0$ and CG splits $e$ equally.
- If $x_i = c_i/2 \le \lambda$ and $x_j = \lambda \le c_j/2$: then $e - c_j \le c_i/2 - c_j/2 \le 0$, so $a_i = 0$, and $a_j = \lambda - c_i/2 \ge 0$. CG gives $i$ the amount $(e - a_j)/2 = c_i/2$ and $j$ the rest, $\lambda$.
- If $x_i = c_i/2$ and $x_j = c_j/2$: then $a_i = 0$ and $a_j = (c_j - c_i)/2$, and CG gives $c_i/2$ and $c_j/2$.
- The case $x_j = c_j/2$ with $x_i = \lambda < c_i/2$ is impossible, because it gives $\lambda < c_i/2 \le c_j/2 \le \lambda$.

Now let $E > C/2$. By Lemma 4, $x = c - y$ with $y = T(c, C - E)$ and $C - E < C/2$, so the first part applies to $y$: $(y_i, y_j) = \mathrm{CG}(y_i + y_j)$. By the self-duality of CG, $(x_i, x_j) = (c_i - y_i, c_j - y_j) = \mathrm{CG}(c_i + c_j - y_i - y_j) = \mathrm{CG}(x_i + x_j)$. $\square$

**Theorem 2 (uniqueness).** At most one award vector for $(c, E)$ is consistent with CG in the sense of Theorem 1.

*Proof.* Let $x \ne y$ be two such vectors. Both sum to $E$, so there are $i$ with $x_i < y_i$ and $j$ with $x_j > y_j$. If $x_i + x_j \le y_i + y_j$, then by monotonicity $x_j = \mathrm{CG}_j(x_i + x_j) \le \mathrm{CG}_j(y_i + y_j) = y_j$, a contradiction. If $x_i + x_j > y_i + y_j$, then in the same way $x_i \ge y_i$, a contradiction. $\square$

**Theorem 3 (Aumann and Maschler 1985).** $T(c, E)$ is the nucleolus of the bankruptcy game $v(S) = \max(0, E - c(N \setminus S))$.

*Proof.* This proof uses one cited result: the prenucleolus has the reduced game property of Davis and Maschler (Sobolev 1975; Peleg and Sudholter 2007, Chapter 6). For a game $(N, v)$, a vector $x$ with $x(N) = v(N)$ and a pair $\{i, j\}$, the reduced game $w$ on $\{i, j\}$ has $w(\{i, j\}) = x_i + x_j$ and $w(\{i\}) = \max_{Q \subseteq N \setminus \{i, j\}} (v(\{i\} \cup Q) - x(Q))$. The property says: if $x$ is the prenucleolus of $v$, then $(x_i, x_j)$ is the prenucleolus of $w$.

Step 1: the prenucleolus $\nu$ of $v$ is an award vector. The game is convex (Curiel, Maschler and Tijs 1987), so its core is not empty, and the prenucleolus lies in the core; core points satisfy $x_i \ge v(\{i\}) \ge 0$ and $x(N \setminus \{i\}) \ge v(N \setminus \{i\}) \ge E - c_i$, that is, $x_i \le c_i$. The core is a subset of the imputations, so $\nu$ is also the nucleolus.

Step 2: the reduced game of a bankruptcy game at an award vector $x$ is a bankruptcy game. Take $Q \subseteq N \setminus \{i, j\}$ and let $R = N \setminus (\{i, j\} \cup Q)$. Since $E = x_i + x_j + x(Q) + x(R)$,

$$v(\{i\} \cup Q) - x(Q) = \max\big({-x(Q)},\ x_i + x_j - c_j - (c(R) - x(R))\big).$$

Both $x(Q)$ and $c(R) - x(R)$ are at least 0. The first term is largest, 0, at $Q = \emptyset$; the second is largest, $x_i + x_j - c_j$, at $R = \emptyset$. So $w(\{i\}) = \max(0, x_i + x_j - c_j)$, which is the bankruptcy game of two claimants with claims $c_i, c_j$ and estate $x_i + x_j$.

Step 3: for two players, the prenucleolus is $x_i = w(\{i\}) + (w(\{i, j\}) - w(\{i\}) - w(\{j\}))/2$. The excesses of $\{i\}$ and $\{j\}$ are $w(\{i\}) - x_i$ and $w(\{j\}) - x_j$; their sum is fixed by $x_i + x_j = w(\{i, j\})$, so the larger one is smallest when they are equal. With $w(\{i\}) = a_i$, this is the contested garment division $\mathrm{CG}(x_i + x_j)$.

So $\nu$ is consistent with CG. By Theorem 1 so is $T(c, E)$, and by Theorem 2 they are equal. $\square$

**Remark.** The tests in `impl/python/test_talmud_rule.py` check the Mishna values, Theorem 1 on 300 random problems, Lemma 4, a second implementation of CEA that tries every breakpoint, and Theorem 3 against a brute-force lexicographic minimum over a grid of imputations with step 1/6 for 2 and 3 claimants.
