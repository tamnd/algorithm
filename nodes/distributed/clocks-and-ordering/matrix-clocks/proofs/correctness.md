---
title: Each row of a matrix clock is the vector clock of a known event
proves: [correctness]
status: full
---

We use the model and the notation of the page: $n$ processes, asynchronous message passing, channels that need not be FIFO. $P_k$ is the set of events of $p_k$, $\to$ is [happened-before](/happened-before/), and $\downarrow e = \{g : g \to e\} \cup \{e\}$ is the causal past of $e$. $V(g)$ is the [vector clock](/vector-clocks/) of $g$, and $M(e)$ is the matrix that line L3 or line L8 returns at $e$. For an event $e$ and a process $p_j$, let $g_j(e)$ be the last event of $p_j$ in $\downarrow e$, and let $V(g_j(e))$ be the zero vector if $\downarrow e \cap P_j$ is empty.

We use three facts from the proof on the vector clocks page. (F1) If $g \to e$, then $g$ comes before $e$ in the run. (F2) $V(g)[k] = |\downarrow g \cap P_k|$, and for an event $e$ of $p_i$ with previous event $r$ on $p_i$ and, for a receive, matching send $s$, the vector clock rule gives $V(e) = \max(V(r), V(s)) + u_i$, where $u_i$ is the unit vector of entry $i$ and a missing event gives the zero vector. (F3) If $g$ comes before $h$ on one process, then $V(g) \le V(h)$.

**Theorem.** For each event $e$ of $p_i$ and each $j$, row $j$ of $M(e)$ is $V(g_j(e))$. In particular, row $i$ of $M(e)$ is $V(e)$.

*Proof.* By induction on the position of $e$ in the run. Let $r$ be the event before $e$ on $p_i$, if it exists, and let $s$, an event of $p_{j'}$ with $j' \ne i$, be the matching send if $e$ is a receive. As on the vector clocks page, $\downarrow e = \{e\} \cup \downarrow r \cup \downarrow s$, with the empty set for a missing event. Before the call for $e$, the matrix of $p_i$ is $M(r)$, or the zero matrix of line L1. By (F1) and line L4, the message carries $M(s)$, and the induction hypothesis holds for $r$ and $s$.

*Rows $j \ne i$.* For a local event or a send, $e$ changes only entry $(i, i)$ in line L2. Also $\downarrow e \cap P_j = \downarrow r \cap P_j$, so $g_j(e) = g_j(r)$ and the row is right. For a receive, lines L5 and L6 set row $j$ to $\max(V(g_j(r)), V(g_j(s)))$, and lines L7 and L8 do not change row $j$. Now $\downarrow e \cap P_j = (\downarrow r \cap P_j) \cup (\downarrow s \cap P_j)$, so $g_j(e)$ is the later of $g_j(r)$ and $g_j(s)$. By (F3), the maximum of the two vectors is the vector of the later event, which is $V(g_j(e))$.

*Row $i$.* The last event of $p_i$ in $\downarrow e$ is $e$, so we must show that row $i$ is $V(e)$. By the induction hypothesis, row $i$ of $M(r)$ is $V(r)$. For a local event or a send, line L2 gives $V(r) + u_i = V(e)$ by (F2). For a receive, row $j'$ of $M(s)$ is $V(s)$, since $s$ is an event of $p_{j'}$. Row $i$ of $M(s)$ is $V(h)$ for $h = g_i(s)$, or zero. If $h$ exists, it is an event of $p_i$ in $\downarrow s$, so it comes before $s$ and so before $e$ by (F1). So $h$ is $r$ or an earlier event of $p_i$, and (F3) gives $V(h) \le V(r)$. Lines L6 and L7 set row $i$ to $\max(V(r), V(h), V(s)) = \max(V(r), V(s))$, and line L8 adds $u_i$. By (F2) this is $V(e)$. $\blacksquare$

**Corollary (knowledge).** Let $e$ be an event of $p_i$ and $t = \min_k M(e)[k][l]$. Then for each process $p_k$, the first $t$ events of $p_l$ are in the causal past of $g_k(e)$, which is an event of $p_k$ in $\downarrow e$.

*Proof.* By the theorem and (F2), $M(e)[k][l] = V(g_k(e))[l] = |\downarrow g_k(e) \cap P_l|$, and this is at least $t$. The set $\downarrow g_k(e) \cap P_l$ is a prefix of the events of $p_l$, by Lemma 2 of the vector clocks proof, so it holds the first $t$ events of $p_l$. $\blacksquare$

So when the minimum of column $l$ reaches $t$ at $p_i$, each process has already seen the first $t$ events of $p_l$ in its causal past. A process that keeps a log of the events of $p_l$ only to forward them can drop the first $t$ entries. The value of the minimum never decreases at $p_i$, since every entry of $M_i$ only grows.
