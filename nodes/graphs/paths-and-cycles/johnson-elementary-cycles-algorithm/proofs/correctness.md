---
title: Johnson's algorithm lists every elementary cycle exactly once
proves: [correctness, termination]
status: full
---

Let $G$ be a directed graph on $\{0, \ldots, n - 1\}$ with parallel arcs merged, so that $A(v)$ lists each successor once; a self-loop at $v$ puts $v$ in $A(v)$. For $s \in V$ let $G_s = G[\{s, \ldots, n - 1\}]$. A cycle is identified by its vertex sequence starting at its least vertex.

## The outer loop

**Lemma 1.** Let line L3 run with the current value $s_0$ of $s$, and let $K$ be the component it finds, with least vertex $s$. (a) No vertex $t$ with $s_0 \le t < s$ is the least vertex of a cycle. (b) The cycles of $G$ whose least vertex is $s$ are exactly the cycles of $G[K]$ through $s$. (c) If no component is found, no vertex $t \ge s_0$ is the least vertex of a cycle.

*Proof.* A cycle with least vertex $t \ge s_0$ lies in $G_{s_0}$, and its vertices are strongly connected, so it lies in one strong component $K'$ of $G_{s_0}$, which has two or more vertices or a self-loop. This gives (c). Also $\min K \le \min K' \le t$, which gives (a). For (b), a cycle of $G[K]$ through $s$ has least vertex $s$, since $K \subseteq \{s, \ldots\}$. Conversely, a cycle with least vertex $s$ lies in the component $K'$ of $G_{s_0}$ that contains $s$, and that is $K$. $\square$

So, if each call CIRCUIT$(s)$ outputs exactly the cycles of $G[K]$ through $s$, each once, then JOHNSON outputs every cycle of $G$ exactly once, grouped by least vertex. The loop ends, because $s$ grows at every round. The rest of the proof fixes one phase, with $s$ and $K$, and writes $A(v)$ for $A_K(v)$.

## One phase: definitions

A *call* is one execution of CIRCUIT$(v)$; it *succeeds* if it returns true and *fails* otherwise. Calls nest: a call that starts after a call $X$ starts and before $X$ ends also ends before $X$ ends. The stack holds the vertices of the calls that have started and not ended, in the order of their starts. A vertex is set blocked only at line L9, when it is pushed, and set unblocked only by UNBLOCK.

**Fact 2 (failed calls).** During a failed call, UNBLOCK never runs, and when it ends, every $w \in A(v)$ is blocked and $s \notin A(v)$.

*Proof.* By induction on the nesting depth. A failed call of $v$ has $f = $ false at the end, so line L11 never ran ($s \notin A(v)$), every call it made at line L12 failed (so by induction no UNBLOCK ran inside them), and line L13 did not run UNBLOCK. So during the call no vertex was unblocked. Each $w \in A(v)$ was either blocked when scanned, or was pushed at line L12, which blocks it. $\square$

**Fact 3 ($B$-lists).** If $B[u]$ is not empty, then $u$ is blocked. Every entry of $B[u]$ was added after the last time $u$ was unblocked (or after line L6, if it never was).

*Proof.* Line L14 adds $v$ to $B[w]$ at the end of a failed call of $v$, when $w$ is blocked by Fact 2. UNBLOCK$(u)$ empties $B[u]$ when it unblocks $u$. $\square$

## The stack is a simple path

**Lemma 4.** Let $v$ be on top of the stack at line L13, and suppose UNBLOCK$(v)$ runs. Every vertex $x \ne v$ that it unblocks has the property that its last call started after $v$ was pushed and has ended. In particular, $x$ is not on the stack.

*Proof.* Say that a vertex $y$ is *late* if it is blocked, its last call started after the push of $v$, and that call has ended. UNBLOCK$(v)$ unblocks $x$ only if $x$ is blocked and $x \in B[y]$ for $y = v$ or for a vertex $y$ that it unblocked before. It suffices to show: if $y = v$ or $y$ is late, then every blocked $x \in B[y]$ is late.

Since $y$ is blocked, it has been blocked without a break since its last push $P_y$; for $y = v$ this is the push of $v$, and for a late $y$ it is after the push of $v$. Before $P_y$, $y$ was unblocked, so by Fact 3 every entry $x$ of $B[y]$ was added after $P_y$, by a failed call $X$ of $x$ that ended after $P_y$, hence after the push of $v$. If $X$ had started before the push of $v$, then $X$ would contain the call of $v$ and could end only after it; but $v$ is still on the stack. So $X$ started after the push of $v$. If $x$ was pushed again after $X$, that call started after the push of $v$; it cannot still be running, because then $x$ would be on the stack above $v$, and $v$ is the top. So the last call of $x$ started after the push of $v$ and has ended, and $x$ is blocked, so $x$ is late. $\square$

**Corollary 5.** A vertex on the stack stays blocked until it is popped. So the stack never holds a vertex twice: line L12 pushes $w$ only if $w$ is unblocked, hence not on the stack. The stack is always a simple path $s = x_0 \to x_1 \to \cdots \to x_k$ in $G[K]$, since each $x_{i+1} \in A(x_i)$.

## Soundness and no repetition

Line L11 outputs the stack $x_0, \ldots, x_k$ when $s \in A(x_k)$. By Corollary 5 this is a simple path from $s$ in $G[K]$ followed by the arc $x_k \to s$, so it is an elementary cycle of $G[K]$ through $s$; when $k = 0$, it is the self-loop at $s$.

Two different calls have different stacks. By induction on the start time: two calls with the same stack $x_0, \ldots, x_k$, $k \ge 1$, are made at line L12 by calls with the stack $x_0, \ldots, x_{k-1}$, which are the same call by induction, and one call scans each $w \in A(x_{k-1})$ once. The phase has exactly one call with stack $x_0 = s$. Each call outputs at most once, at the single entry $s$ of $A(x_k)$. So no cycle is output twice.

## Completeness

**Lemma 6 (blocked vertices).** At every moment, if $y$ is blocked and not on the stack, then $s \notin A(y)$, every $w \in A(y)$ is blocked, and $y \in B[w]$.

*Proof.* $y$ is blocked and off the stack, so its last call has ended and did not unblock it at line L13, so it failed. At its end, Fact 2 gives $s \notin A(y)$ and every $w \in A(y)$ blocked, and line L14 puts $y$ in $B[w]$. Afterwards, $w$ can be unblocked only by UNBLOCK$(w)$, which then finds $y \in B[w]$, blocked, and unblocks $y$ too. And $y$ leaves $B[w]$ only in that same UNBLOCK$(w)$. So while $y$ stays blocked, the claim holds. $\square$

**Lemma 7 (paths from blocked vertices).** At every moment, if $y$ is blocked and not on the stack, every path $y = p_0, p_1, \ldots, p_r = s$ in $G[K]$ contains a vertex of the stack among $p_1, \ldots, p_{r-1}$.

*Proof.* Let $p_i$ be the first vertex of the path that is on the stack or equal to $s$; it exists because $p_r = s$. All $p_j$ with $j < i$ are off the stack, and by Lemma 6 and induction on $j$, all of them are blocked: $p_0 = y$ is, and if $p_j$ is blocked and off the stack, then $p_{j+1} \in A(p_j)$ is blocked. If $p_i = s$, then $p_{i-1}$ is blocked, off the stack, and $s \in A(p_{i-1})$, which contradicts Lemma 6. So $p_i \ne s$ is on the stack, and $1 \le i \le r - 1$. $\square$

**Theorem.** CIRCUIT$(s)$ outputs every elementary cycle of $G[K]$ through $s$.

*Proof.* Let $C = (s, c_1, \ldots, c_{k-1})$ be such a cycle. We show by induction on $i$, for $0 \le i \le k - 1$, that some call has the stack $s, c_1, \ldots, c_i$. For $i = 0$ this is CIRCUIT$(s)$. Let a call $X$ have the stack $s, c_1, \ldots, c_i$. While $X$ scans its list, $c_i$ is the top, because all calls made by $X$ have ended.

If $i = k - 1$, then $s \in A(c_{k-1})$, and line L11 outputs $C$ when $X$ scans $s$. Otherwise $X$ scans $c_{i+1} \ne s$. If $c_{i+1}$ is blocked at that moment, it is not on the stack, since $C$ is simple, and Lemma 7 applies to the path $c_{i+1}, c_{i+2}, \ldots, c_{k-1}, s$: one of $c_{i+2}, \ldots, c_{k-1}$, or $c_{i+1}$ itself, would have to be on the stack $s, c_1, \ldots, c_i$, which is impossible because $C$ is simple. So $c_{i+1}$ is unblocked, and line L12 calls CIRCUIT$(c_{i+1})$ with the stack $s, c_1, \ldots, c_{i+1}$. $\square$

## Termination

Each call scans a finite list and makes at most one call per entry, and by Corollary 5 the stack has at most $|K|$ vertices, so the tree of calls is finite. UNBLOCK unblocks a vertex at each recursive step and recurses only on blocked vertices, so it makes at most $|K|$ steps. The outer loop increases $s$ each round. $\blacksquare$
