---
title: Lamport clocks satisfy the clock condition and give a total order
proves: [correctness]
status: full
---

We use the model of the page: $n$ processes $p_1, \ldots, p_n$, asynchronous message passing, and channels that deliver each message at most once and not always in FIFO order. No process fails during the part of the run that we look at. An event is a local step, a send or a receive, as in lines L2, L4 and L7. We write $C(e)$ for the value that line L3, L6 or L8 returns at event $e$. The relation $\to$ is [happened-before](/happened-before/): the smallest transitive relation with $a \to b$ when $a$ comes before $b$ on the same process, and $a \to b$ when $a$ sends a message and $b$ receives it.

**Lemma 1 (local growth).** If $a$ and $b$ are events of the same process and $a$ comes before $b$, then $C(a) < C(b)$.

*Proof.* Only lines L2, L4 and L7 change $C_i$. Line L2 and line L4 add 1. Line L7 sets $C_i$ to $\max(C_i, T_m) + 1 \ge C_i + 1$. So each event makes $C_i$ larger by at least 1, and no other step changes it. The value that an event returns is the value of $C_i$ just after that event. Let $a = e_1, e_2, \ldots, e_k = b$ be the events of the process from $a$ to $b$, with $k \ge 2$. Then $C(e_{s+1}) \ge C(e_s) + 1$ for each $s$, so $C(b) \ge C(a) + k - 1 > C(a)$. $\square$

**Lemma 2 (messages).** If $a$ sends a message $m$ and $b$ receives $m$, then $C(a) < C(b)$.

*Proof.* At $a$, line L4 sets $C_i$, line L5 attaches $T_m = C_i$ to $m$, and line L6 returns the same value. So $T_m = C(a)$. The message is not changed in transit. At $b$, line L7 sets $C_j = \max(C_j, T_m) + 1 \ge T_m + 1$, and line L8 returns this value. So $C(b) \ge C(a) + 1$. $\square$

**Theorem 1 (clock condition).** For all events $a$ and $b$, if $a \to b$ then $C(a) < C(b)$.

*Proof.* By the definition of $\to$, $a \to b$ holds if and only if there is a chain $a = e_0, e_1, \ldots, e_k = b$ with $k \ge 1$, where each pair $(e_{s-1}, e_s)$ is a pair of the same process in order, or a send and its receive. We use induction on $k$. For $k = 1$, Lemma 1 or Lemma 2 gives $C(e_0) < C(e_1)$. For $k \ge 2$, the induction hypothesis gives $C(e_0) < C(e_{k-1})$, and Lemma 1 or Lemma 2 gives $C(e_{k-1}) < C(e_k)$. The order $<$ on integers is transitive, so $C(a) < C(b)$. $\blacksquare$

**Theorem 2 (total order).** Define $a \Rightarrow b$ if and only if $(C(a), i) < (C(b), j)$ in lexicographic order, where $a$ is an event of $p_i$ and $b$ is an event of $p_j$. Then $\Rightarrow$ is a strict total order on the events, and $a \to b$ implies $a \Rightarrow b$.

*Proof.* Lexicographic order on pairs of integers is a strict total order. So $\Rightarrow$ is a strict total order on events if the map $e \mapsto (C(e), i)$ is injective. Take two different events $a$ and $b$. If they are on different processes, the second parts differ. If they are on the same process, one of them comes first, and Lemma 1 gives $C(a) \ne C(b)$. So the map is injective. If $a \to b$, Theorem 1 gives $C(a) < C(b)$, so the first parts already decide, and $a \Rightarrow b$. $\blacksquare$

**Theorem 3 (the value is the depth).** For each event $e$, $C(e)$ is the number of events in a longest chain $e_1 \to e_2 \to \cdots \to e_k = e$ that ends at $e$.

*Proof.* Call this number $h(e)$. The immediate predecessors of $e$ are the event just before $e$ on its process, if there is one, and the matching send, if $e$ is a receive. Lines L2, L4 and L7 give $C(e) = 1 + \max$ of $C$ over the immediate predecessors, with $\max \emptyset = 0$: the value $C_i$ before $e$ is $C$ of the previous event on the process (or 0 by line L1), and $T_m$ is $C$ of the send by Lemma 2. We show $h(e) = 1 + \max h$ over the immediate predecessors, with the same convention. A longest chain to $e$ with $k \ge 2$ events has a last step $e_{k-1} \to e$. By the definition of $\to$, either $e_{k-1}$ is an immediate predecessor $g$, or $e_{k-1} \to g$ for an immediate predecessor $g$. In both cases a chain of $k - 1$ events ends at or before $g$, so $h(g) \ge k - 1$. Conversely, a longest chain to an immediate predecessor $g$, followed by $e$, is a chain of $h(g) + 1$ events. So both $C$ and $h$ satisfy the same recursion. The events in the order of the run form a topological order of the immediate-predecessor graph, so induction along this order gives $C(e) = h(e)$ for each $e$. $\blacksquare$
