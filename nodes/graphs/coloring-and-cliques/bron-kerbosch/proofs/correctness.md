---
title: Bron-Kerbosch with pivot lists each maximal clique exactly once
proves: [correctness, termination]
status: full
---

Let $G = (V, E)$ be a simple undirected graph and $N(v)$ the set of neighbors of $v$. For a clique $R$ write $C(R) = \{ w \in V \setminus R : R \subseteq N(w) \}$, the vertices that extend $R$. For a call EXPAND$(R, P, X)$ let

$$\mathcal{M}(R, P, X) = \{ K : K \text{ is a maximal clique of } G,\ R \subseteq K \subseteq R \cup P \}.$$

**Precondition (Q).** $R$ is a clique, $P \cap X = \emptyset$, and $P \cup X = C(R)$.

**Claim.** If (Q) holds, EXPAND$(R, P, X)$ terminates and appends each clique of $\mathcal{M}(R, P, X)$ to out exactly once, and nothing else. The top call EXPAND$(\emptyset, V, \emptyset)$ satisfies (Q), since $C(\emptyset) = V$, and $\mathcal{M}(\emptyset, V, \emptyset)$ is the set of all maximal cliques, so BRON-KERBOSCH is correct.

*Proof.* Induction on $|P|$.

**Base: $P = \emptyset$.** Then $\mathcal{M}(R, \emptyset, X)$ is $\{R\}$ if $R$ is maximal and empty otherwise. $R$ is maximal exactly when $C(R) = \emptyset$, that is, when $X = \emptyset$. If $X = \emptyset$, line L4 appends $R$ and returns. If $X \ne \emptyset$, line L5 picks some $u$, the set $P \setminus N(u)$ is empty, and the call appends nothing. Both match $\mathcal{M}$.

**Step: $P \ne \emptyset$.** Line L4 does not fire. Let $u \in P \cup X$ be the pivot and $v_1, \ldots, v_s$ the vertices of $B = P \setminus N(u)$ in the order of the loop of line L6. Let $P_j$ and $X_j$ be the values of $P$ and $X$ before iteration $j$, so $P_1 = P$, $X_1 = X$, $P_{j+1} = P_j \setminus \{v_j\}$ and $X_{j+1} = X_j \cup \{v_j\}$. Then $P_j \cup X_j = P \cup X$ and $P_j \cap X_j = \emptyset$ for each $j$, and $v_j \in P_j$.

*The children satisfy (Q).* In iteration $j$ the child is EXPAND$(R', P', X')$ with $R' = R \cup \{v_j\}$, $P' = P_j \cap N(v_j)$, $X' = X_j \cap N(v_j)$. As $v_j \in C(R)$, $R'$ is a clique. The sets $P'$ and $X'$ are disjoint, and

$$P' \cup X' = (P \cup X) \cap N(v_j) = C(R) \cap N(v_j) = C(R'),$$

because a vertex $w \notin R'$ extends $R'$ exactly when it extends $R$ and is adjacent to $v_j$. Also $|P'| \le |P_j| - 1 < |P|$, since $v_j \notin N(v_j)$. By induction, the child terminates and appends exactly $\mathcal{M}(R', P', X')$, each once.

*Each clique of $\mathcal{M}(R, P, X)$ meets $B$.* Let $K \in \mathcal{M}(R, P, X)$ and suppose $K \cap B = \emptyset$. Then $K \setminus R \subseteq P \cap N(u)$, so $u$ is adjacent to every vertex of $K \setminus R$, and $u \in C(R)$ makes it adjacent to every vertex of $R$. Also $u \notin R$, and $u \notin K \setminus R$ because $u \notin N(u)$. So $K \cup \{u\}$ is a clique larger than $K$, which contradicts the maximality of $K$.

*The children list $\mathcal{M}(R, P, X)$, split by the first branch vertex.* For $K \in \mathcal{M}(R, P, X)$ let $j(K)$ be the smallest $j$ with $v_j \in K$, which exists by the previous paragraph. We show that $K \in \mathcal{M}(R', P', X')$ for iteration $j$ exactly when $j = j(K)$.

- If $j = j(K)$: $R' = R \cup \{v_j\} \subseteq K$. A vertex $w \in K \setminus R'$ lies in $P$ and is adjacent to $v_j$. It is not one of $v_1, \ldots, v_{j-1}$, by the choice of $j$, so $w \in P_j \cap N(v_j) = P'$. So $R' \subseteq K \subseteq R' \cup P'$.
- If $j < j(K)$: $v_j \notin K$, so $R' \not\subseteq K$.
- If $j > j(K)$: $v_{j(K)} \in K$ and $v_{j(K)} \in X_j$, so $v_{j(K)} \notin R' \cup P'$ (it is not $v_j$, and $P_j \cap X_j = \emptyset$), and $K \not\subseteq R' \cup P'$.

Conversely, every clique $K'$ of $\mathcal{M}(R', P', X')$ is maximal, contains $R$, and lies in $R \cup \{v_j\} \cup P \subseteq R \cup P$, so it is in $\mathcal{M}(R, P, X)$.

So the children together append each clique of $\mathcal{M}(R, P, X)$ exactly once, in iteration $j(K)$, and nothing else. The call itself appends nothing at line L4. The loop has $s \le |P|$ iterations, each child terminates, and so the call terminates. This completes the induction. $\blacksquare$
