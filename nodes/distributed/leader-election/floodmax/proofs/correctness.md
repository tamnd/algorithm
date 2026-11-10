---
title: FloodMax elects the largest identifier in d rounds with exactly 2md messages
proves: [correctness, termination, complexity]
status: full
---

**Claim.** Run FLOODMAX on a connected undirected graph $G = (V, E)$ with $n$ processes, $m$ edges and distinct identifiers, in the synchronous model without failures, with a common bound $d \ge \mathrm{diam}(G)$. Then every process stops after round $d$, the process $v_{\max}$ with the largest identifier $u_{\max}$ outputs *leader*, every other process outputs *non-leader* and holds $u_{\max}$, and the run sends exactly $2md$ messages. The same outputs hold for OptFloodMax, which sends at most $2md$ messages.

**Notation.** Write $\mathit{max}_v^r$ for the value of $\mathit{max}$ at $v$ after round $r$, with $\mathit{max}_v^0 = u_v$. Write $B_r(v) = \{ w : \mathrm{dist}(v, w) \le r \}$ for the ball of radius $r$, and $N(v)$ for the set of neighbours of $v$.

**Lemma 1 (balls).** For $r \ge 1$, $B_r(v) = B_{r-1}(v) \cup \bigcup_{w \in N(v)} B_{r-1}(w)$.

*Proof.* If $\mathrm{dist}(v, x) = k \le r$, either $k \le r - 1$ and $x \in B_{r-1}(v)$, or $k = r \ge 1$ and the second process $w$ on a shortest path from $v$ to $x$ is a neighbour of $v$ with $\mathrm{dist}(w, x) = r - 1$. Conversely, $\mathrm{dist}(v, x) \le 1 + \mathrm{dist}(w, x) \le r$ for $x \in B_{r-1}(w)$ and $w \in N(v)$. $\square$

**Lemma 2 (invariant).** For every $r$ with $0 \le r \le d$ and every $v$, $\mathit{max}_v^r = \max \{ u_w : w \in B_r(v) \}$.

*Proof.* Induction on $r$. For $r = 0$, $B_0(v) = \{v\}$ and line L1 sets $\mathit{max}_v = u_v$. For $r \ge 1$, in round $r$ every $w \in N(v)$ sends $\mathit{max}_w^{r-1}$ to $v$ (line L3), and $v$ receives all of them in the same round. Lines L4 and L5 set $\mathit{max}_v^r = \max(\mathit{max}_v^{r-1}, \max_{w \in N(v)} \mathit{max}_w^{r-1})$. By the hypothesis and Lemma 1 this is the largest identifier in $B_r(v)$. $\square$

**Outputs.** $d \ge \mathrm{diam}(G)$ gives $B_d(v) = V$ for every $v$, so $\mathit{max}_v^d = u_{\max}$ by Lemma 2. Line L6 holds at $v$ exactly when $u_v = u_{\max}$, which is $v = v_{\max}$ alone because the identifiers are distinct. Every other process runs line L7 and holds $u_{\max}$.

**Termination.** The loop of line L2 has exactly $d$ iterations, so each process outputs after round $d$.

**Messages.** In each round each process $v$ sends exactly $\deg(v)$ messages (line L3). Over all processes this is $\sum_v \deg(v) = 2m$ per round, so $2md$ in total.

**OptFloodMax.** Let $v$ skip the send of round $r \ge 2$ when $\mathit{max}_v^{r-1} = \mathit{max}_v^{r-2}$. Then each neighbour $w$ received the same value from $v$ in an earlier round, and since $\mathit{max}$ never goes down at $w$, $\mathit{max}_w$ is already at least that value. So the maximum in lines L4 and L5 is the same as with the send, Lemma 2 still holds, and the outputs are the same. The process sends at most what FloodMax sends in every round, so at most $2md$ messages. $\blacksquare$
