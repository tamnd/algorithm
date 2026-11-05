---
title: Warshall's algorithm computes the transitive closure
proves: [correctness, termination]
status: full
---

Let $G = (V, E)$ be a directed graph with $V = \{0, \ldots, n-1\}$, where parallel arcs and loops are allowed. A *walk* from $i$ to $j$ of length $\ell \ge 1$ is a sequence $i = x_0, x_1, \ldots, x_\ell = j$ with $(x_{t-1}, x_t) \in E$ for each $t$; its *inner vertices* are $x_1, \ldots, x_{\ell-1}$. For $0 \le k \le n$, let

$$P_k = \{(i, j) : \text{some walk of length at least 1 from } i \text{ to } j \text{ has all its inner vertices in } \{0, \ldots, k - 1\}\}.$$

We view $R$ as a set of pairs: $(i, j) \in R$ when $R[i][j] = 1$. Write $R_k$ for the value of $R$ just before round $k$ of line L2, so that $R_n$ is the value returned by line L6.

**Lemma 1.** $P_0 = E$, as a set of pairs, and $P_n$ is the transitive closure $E^+$.

*Proof.* A walk with no inner vertex has length 1 and is an arc, and an arc is such a walk. Every inner vertex is in $V = \{0, \ldots, n - 1\}$, so $P_n$ contains every pair joined by a walk of length at least 1. $\square$

**Lemma 2.** $P_k \subseteq P_{k+1}$, and if $(i, k) \in P_k$ and $(k, j) \in P_k$, then $(i, j) \in P_{k+1}$.

*Proof.* The first claim is clear. For the second, join a walk from $i$ to $k$ and a walk from $k$ to $j$, both with inner vertices below $k$. The result is a walk of length at least 2 from $i$ to $j$ whose inner vertices are those of the two walks and $k$, all in $\{0, \ldots, k\}$. $\square$

**Lemma 3.** If $(i, j) \in P_{k+1}$, then $(i, j) \in P_k$, or both $(i, k) \in P_k$ and $(k, j) \in P_k$.

*Proof.* Take a walk $i = x_0, \ldots, x_\ell = j$ with inner vertices in $\{0, \ldots, k\}$. If $k$ is not an inner vertex, $(i, j) \in P_k$. Else let $x_a$ be the first inner vertex equal to $k$ and $x_b$ the last, with $0 < a \le b < \ell$. The walk $x_0, \ldots, x_a$ goes from $i$ to $k$, has length $a \ge 1$, and its inner vertices $x_1, \ldots, x_{a-1}$ are inner vertices of the whole walk other than $k$, so they are below $k$. So $(i, k) \in P_k$. In the same way $x_b, \ldots, x_\ell$ shows $(k, j) \in P_k$. $\square$

**Lemma 4 (one round).** If $R_k = P_k$, then $R_{k+1} = P_{k+1}$.

*Proof.* During round $k$, line L5 adds to row $i$ the pairs $(i, j)$ with $(k, j)$ in the current row $k$, for those $i$ with $(i, k)$ in the current $R$. We first show that row $k$ does not change in round $k$. A change of row $k$ can only happen when line L5 runs with $i = k$, and it then takes the OR of row $k$ with itself. So throughout round $k$, row $k$ equals row $k$ of $R_k = P_k$.

*$R_{k+1} \subseteq P_{k+1}$.* We show that $R \subseteq P_{k+1}$ holds throughout round $k$. It holds at the start, as $R_k = P_k \subseteq P_{k+1}$. Suppose it holds before some run of line L5 with row $i$, where $(i, k) \in R$. Each pair it adds is $(i, j)$ with $(k, j)$ in row $k$, so $(k, j) \in P_k$. Also $(i, k) \in R \subseteq P_{k+1}$, and by Lemma 3 applied with $j = k$, either $(i, k) \in P_k$, or $(k, k) \in P_k$ and $(i, k) \in P_k$; in both cases $(i, k) \in P_k$. Lemma 2 gives $(i, j) \in P_{k+1}$.

*$P_{k+1} \subseteq R_{k+1}$.* Let $(i, j) \in P_{k+1}$. Entries never change from 1 to 0, so if $(i, j) \in P_k = R_k$ it is in $R_{k+1}$. Else, by Lemma 3, $(i, k) \in P_k$ and $(k, j) \in P_k$. When line L3 reaches row $i$ in round $k$, $(i, k)$ is still in $R$, so line L4 succeeds, and $(k, j)$ is in row $k$, which has not changed. So line L5 sets $R[i][j] = 1$. $\square$

**Theorem.** WARSHALL stops, after $n$ rounds of $n$ steps each, and returns $R$ with $R[i][j] = 1$ exactly when $G$ has a walk of length at least 1 from $i$ to $j$.

*Proof.* The loops of lines L2 and L3 have $n$ steps each, and line L5 is a finite row operation, so the algorithm stops. Line L1 sets $R_0 = E = P_0$ by Lemma 1, as parallel arcs set the same entry. By Lemma 4 and induction on $k$, $R_n = P_n$, which is $E^+$ by Lemma 1. $\blacksquare$

**Remark on the implementation.** The Python code reads row $k$ once, as `rk`, before the loop over $i$. This is the same as reading it at each step, because, as shown in Lemma 4, row $k$ does not change in round $k$.
