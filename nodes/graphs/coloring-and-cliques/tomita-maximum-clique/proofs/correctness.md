---
title: The coloring bound never cuts off a larger clique
proves: [correctness, termination]
status: full
---

Write $N(p)$ for the neighbors of $p$ and $\omega(H)$ for the clique number of a graph $H$, with $\omega$ of the empty graph equal to 0. For a call EXPAND$(Q, R)$ let $R_0$ be the list $R$ at its start.

**Invariant of a call.** At every call EXPAND$(Q, R)$:

(a) $Q$ is a clique, and every vertex of $R$ is adjacent to every vertex of $Q$; in particular $Q \cap R = \emptyset$.

This holds for the first call, with $Q = \emptyset$. If it holds for a call and $p \in R$, then $Q \cup \{p\}$ is a clique, and $R' = R \cap N(p)$ consists of vertices adjacent to all of $Q$ and to $p$; so it holds for the child call of line L10. The same argument shows that the set $Q \cup \{p\}$ stored at line L9 is a clique.

**Termination.** Each turn of the loop of lines L5 to L11 either returns or removes one vertex from $R$ at line L11, and a child call gets a list $R'$ that does not contain $p$, so $|R'| < |R|$. By induction on $|R|$ every call stops.

**Lemma (the bound).** After line L4, let $p$ be the last vertex of the current list $R$. Every clique contained in the current $R$ has at most $\mathrm{col}[p]$ vertices.

*Proof.* NUMBER-SORT puts a vertex into a class only if the class has no neighbor of it, so every class is an independent set. The list is sorted by class number, and the loop only removes vertices from the end, so every vertex left in $R$ has color at most $\mathrm{col}[p]$. A clique meets an independent set in at most one vertex, so a clique in $R$ has at most one vertex of each of the colors $1, \ldots, \mathrm{col}[p]$. $\square$

**Claim.** When EXPAND$(Q, R_0)$ returns, $|Q_{\max}| \ge |Q| + \omega(G[R_0])$, where $Q_{\max}$ is its value at that moment. Moreover, $Q_{\max}$ only grows and is always a clique.

*Proof.* By induction on $|R_0|$. If $R_0 = \emptyset$, this is the top call with $Q = \emptyset$, since line L10 calls EXPAND only with $R' \ne \emptyset$, and the claim $|Q_{\max}| \ge 0$ is trivial. So let $R_0 \ne \emptyset$, and let $K$ be a maximum clique of $G[R_0]$, so $K \ne \emptyset$.

Let $p^*$ be the vertex of $K$ that the loop reaches first, that is, the vertex of $K$ that comes last in the sorted list.

- If the call returns at line L7 at some turn with last vertex $p$ while all of $K$ is still in $R$, then by the lemma $|K| \le \mathrm{col}[p] \le |Q_{\max}| - |Q|$, which is the claim, since $Q_{\max}$ only grows afterwards.
- Otherwise the loop reaches the turn with $p = p^*$, with all of $K$ still in $R$, because line L11 has removed only vertices after $p^*$ in the list, none of them in $K$. Passing line L7, it computes $R' = R \cap N(p^*) \supseteq K \setminus \{p^*\}$. If $R' = \emptyset$, then $K = \{p^*\}$ and line L9 makes $|Q_{\max}| \ge |Q| + 1 = |Q| + |K|$. If $R' \neq \emptyset$, the child call EXPAND$(Q \cup \{p^*\}, R')$ has $|R'| < |R_0|$, and by induction, after it returns, $|Q_{\max}| \ge |Q| + 1 + \omega(G[R']) \ge |Q| + 1 + |K| - 1$.

In all cases $|Q_{\max}| \ge |Q| + |K|$ after the call. Every value stored in $Q_{\max}$ is a clique by invariant (a), and it is replaced only by a larger one. $\square$

**Conclusion.** The top call is EXPAND$(\emptyset, V)$, so at the end $|Q_{\max}| \ge \omega(G)$. As $Q_{\max}$ is a clique, $|Q_{\max}| = \omega(G)$, and line L3 returns a maximum clique. If $V = \emptyset$, the loop does not run and the empty clique is returned, which is correct. ∎
