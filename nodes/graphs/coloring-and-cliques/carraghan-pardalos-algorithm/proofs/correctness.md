---
title: The Carraghan-Pardalos algorithm returns a maximum clique
proves: [correctness, termination]
status: full
---

Let $G = (V, E)$ be a finite simple undirected graph and $N(v)$ the set of neighbors of $v$. The variable best holds a vertex list; we write $|{\rm best}|$ for its length and treat it as a set. For a call EXPAND$(C, P)$, where $P$ is a list of distinct vertices, let

$$\mu(C, P) = \max \{ |K| : K \text{ is a clique of } G,\ C \subseteq K \subseteq C \cup P \}.$$

**Precondition (Q).** $C$ is a clique, $P \cap C = \emptyset$, and every vertex of $P$ is adjacent to every vertex of $C$.

**Invariant (B).** best is a clique of $G$. It holds at line L2, since $\emptyset$ is a clique. Line L9 is the only place that changes best, and it sets best to $C \cup \{v\}$ with $v$ taken from $P$ under (Q), which is a clique. The value $|{\rm best}|$ never decreases, since line L9 changes best only to a longer list.

**Claim.** Assume (Q), and that $P \ne \emptyset$ or $C = \emptyset$. Then EXPAND$(C, P)$ terminates, all its recursive calls satisfy (Q), and when it returns, $|{\rm best}| \ge \mu(C, P)$.

*Proof.* Induction on $|P|$.

If $P$ is empty, then $C = \emptyset$ and $\mu = 0 \le |{\rm best}|$. The loop does not run.

Let $P = (p_1, \ldots, p_s)$ with $s \ge 1$. The loop of line L5 removes the first element of the list at each pass of line L7, so it makes at most $s$ passes. Before pass $j$ the list is $P_j = (p_j, \ldots, p_s)$. Split the cliques $K$ with $C \subseteq K \subseteq C \cup P$ into $K = C$ and, for each $j$, the cliques whose element of $K \setminus C$ with the smallest position in $P$ is $p_j$. Call the second group $\mathcal{K}_j$. A clique in $\mathcal{K}_j$ lies in $C \cup P_j$.

We show: when pass $j$ ends without a return, $|{\rm best}| \ge |K|$ for every $K \in \mathcal{K}_j$; and when the call returns at line L6 before pass $j$ starts, $|{\rm best}| \ge |K|$ for every $K \in \mathcal{K}_i$ with $i \ge j$.

- *Pass $j$ ends.* Line L7 takes $v = p_j$, and line L8 forms $Q = (p_{j+1}, \ldots, p_s) \cap N(v)$ in list order. Each $K \in \mathcal{K}_j$ satisfies $K \subseteq C \cup \{v\} \cup Q$, since its other vertices outside $C$ come after $p_j$ and are adjacent to $v$. If $Q$ is empty, $K = C \cup \{v\}$, and line L9 ensures $|{\rm best}| \ge |C| + 1 = |K|$. If $Q$ is not empty, line L10 calls EXPAND$(C \cup \{v\}, Q)$. This call satisfies (Q): $C \cup \{v\}$ is a clique because $v$ is adjacent to all of $C$, and every vertex of $Q$ is in $P$, so adjacent to all of $C$, and is in $N(v)$. Also $|Q| \le s - 1 < |P|$. By induction, after it returns, $|{\rm best}| \ge \mu(C \cup \{v\}, Q) \ge |K|$.
- *Return at line L6 before pass $j$.* Then $|C| + |P_j| \le |{\rm best}|$. Every $K \in \mathcal{K}_i$ with $i \ge j$ lies in $C \cup P_j$, so $|K| \le |C| + |P_j| \le |{\rm best}|$.

Since $|{\rm best}|$ never decreases, at the return of the call every $K$ in some $\mathcal{K}_j$ has $|K| \le |{\rm best}|$: either pass $j$ ended, or the call returned at line L6 at or before pass $j$.

It remains to treat $K = C$. If the first pass returns at line L6, then $|C| \le |C| + |P| \le |{\rm best}|$. Otherwise the first pass ends, and it leaves $|{\rm best}| \ge |C| + 1$: either line L9 ran with $|C| + 1$, or the recursive call EXPAND$(C \cup \{p_1\}, Q)$ returned with $|{\rm best}| \ge \mu(C \cup \{p_1\}, Q) \ge |C| + 1$, since $C \cup \{p_1\}$ is itself a clique counted by $\mu$.

So $|{\rm best}| \ge \mu(C, P)$ when the call returns. The call terminates, because the loop has at most $s$ passes and each recursive call terminates by induction. $\square$

**Theorem.** CARRAGHAN-PARDALOS$(G)$ terminates and returns a maximum clique of $G$.

*Proof.* Line L3 calls EXPAND$(\emptyset, (v_1, \ldots, v_n))$ with the list of line L1. The precondition (Q) holds trivially, and $C = \emptyset$. By the claim, the call terminates with $|{\rm best}| \ge \mu(\emptyset, V) = \omega(G)$. By (B), best is a clique, so $|{\rm best}| \le \omega(G)$. So best is a clique of size $\omega(G)$, and line L4 returns it, sorted. The order of line L1 is not used in the proof, so the result is correct for every order. $\blacksquare$
