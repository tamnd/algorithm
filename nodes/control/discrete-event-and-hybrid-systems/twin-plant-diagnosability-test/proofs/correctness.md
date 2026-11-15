---
title: The verifier has a cycle of flagged states if and only if the fault is not diagnosable
proves: [correctness, termination]
status: full
---

**Setting.** The plant $G$ is a deterministic automaton with state set $X$, initial state $x_0$ and alphabet $\Sigma = \Sigma_o \cup \Sigma_{uo}$. $\Sigma_F \subseteq \Sigma_{uo}$ is the set of fault events of the type under test. $P$ erases the unobservable events. The fault type is diagnosable if there is an integer $N$ such that for every $s \in L(G)$ that ends with an event of $\Sigma_F$, every $t$ with $st \in L(G)$ and $|t| \ge N$, and every $w \in L(G)$ with $P(w) = P(st)$, the string $w$ has an event of $\Sigma_F$.

Lines L1 to L8 build the verifier $V$. Its states are triples $(x, f, y)$ with $x, y \in X$ and a flag $f$. Its edges are:

- L5: $(x, f, y) \to (x', f \lor [e \in \Sigma_F], y)$ for $e \in \Sigma_{uo}$ with $\delta(x, e) = x'$ (copy 1 moves alone);
- L6: $(x, f, y) \to (x, f, y')$ for $e \in \Sigma_{uo} \setminus \Sigma_F$ with $\delta(y, e) = y'$ (copy 2 moves alone);
- L7: $(x, f, y) \to (x', f, y')$ for $e \in \Sigma_o$ with $\delta(x, e) = x'$ and $\delta(y, e) = y'$ (both move).

Each edge carries the event of copy 1 (or nothing) and the event of copy 2 (or nothing). For a path $\pi$, let $s_1(\pi)$ and $s_2(\pi)$ be the two strings of these events.

**Lemma 1 (paths and string pairs).** (a) If $\pi$ is a path from $v_0 = (x_0, 0, x_0)$ to $(x, f, y)$, then $s_1 = s_1(\pi)$ and $s_2 = s_2(\pi)$ are in $L(G)$, $\delta(x_0, s_1) = x$, $\delta(x_0, s_2) = y$, $P(s_1) = P(s_2)$, $s_2$ has no event of $\Sigma_F$, and $f = 1$ if and only if $s_1$ has an event of $\Sigma_F$. (b) Conversely, for $s_1, s_2 \in L(G)$ with $P(s_1) = P(s_2)$ and no event of $\Sigma_F$ in $s_2$, there is a path $\pi$ from $v_0$ with $s_1(\pi) = s_1$ and $s_2(\pi) = s_2$.

*Proof.* (a) By induction on the length of $\pi$; each kind of edge keeps every claim true. (b) Write $s_1 = u_0 \sigma_1 u_1 \cdots \sigma_k u_k$ and $s_2 = u_0' \sigma_1 u_1' \cdots \sigma_k u_k'$ with $u_i, u_i' \in \Sigma_{uo}^*$. The path does $u_0$ with edges L5, then $u_0'$ with edges L6, then $\sigma_1$ with an edge L7, and so on. Each edge exists because the strings are in $L(G)$ and $u_i'$ has no event of $\Sigma_F$. $\blacksquare$

**Lemma 2.** The flag never goes from 1 to 0. So a cycle of $V$ through a flagged state has only flagged states.

*Proof.* The three kinds of edges keep the flag or set it. $\blacksquare$

**Theorem.** Assume that $G$ has no cycle of unobservable events. The fault type is diagnosable if and only if the flagged states $W$ (line L9) of $V$ contain no cycle. Line L10 returns this answer.

*Proof that a flagged cycle gives no diagnosability.* Let $\pi$ be a path from $v_0$ to a flagged state $v$, and $c$ a cycle from $v$ to $v$. If $s_1(c)$ were empty, every edge of $c$ would be of kind L6, and the states $y$ along $c$ would form a cycle of unobservable events in $G$. So $s_1(c) \neq \varepsilon$. For each $k$, the path $\pi c^k$ gives by Lemma 1 the strings $p_1 c_1^k$ and $p_2 c_2^k$, with $p_i = s_i(\pi)$ and $c_i = s_i(c)$. They are in $L(G)$ and have the same projection. The second one has no event of $\Sigma_F$, and the first one has one, because $v$ is flagged. Let $s$ be the prefix of $p_1$ that ends with its first event of $\Sigma_F$, and $p_1 = s r$. Then $t = r c_1^k$ has $|t| \ge k$, and $w = p_2 c_2^k$ breaks the condition. As $k$ is arbitrary, no $N$ works.

*Proof that no flagged cycle gives diagnosability.* Let $N = |W|$; note $|W| \le |X|^2$. Take $s$, $t$ and $w$ as in the definition with $|t| \ge N$, and assume that $w$ has no event of $\Sigma_F$. By Lemma 1(b), there is a path $\pi$ from $v_0$ with $s_1(\pi) = st$ and $s_2(\pi) = w$. Each event of $st$ is on its own edge of $\pi$. After the edge of the last event of $s$, the flag is 1, and by Lemma 2 it stays 1. The events of $t$ come after this edge, on $|t|$ more edges. So $\pi$ has a part of at least $|t| \ge |W|$ edges, that is at least $|W| + 1$ states, all in $W$. A state repeats, so $W$ contains a cycle. This contradicts the assumption. So every such $w$ has an event of $\Sigma_F$, and the fault type is diagnosable with the delay bound $N = |W| \le |X|^2$.

Line L10 runs Kahn's algorithm on the graph that $V$ induces on $W$. It removes all states of $W$ if and only if this graph has no cycle. $\blacksquare$

Only the first part uses the assumption on unobservable cycles. Without it, a cycle of kind L6 edges alone can make the test answer "not diagnosable" for a diagnosable plant.

**Termination and cost.** There are at most $2|X|^2$ triples, and the search of lines L3 to L8 puts each one in the queue once, so it stops. A state has at most $|\Sigma_{uo}|$ edges of kind L5, $|\Sigma_{uo}|$ of kind L6 and $|\Sigma_o|$ of kind L7, so at most $2|\Sigma|$ edges. The search and Kahn's algorithm each take $O(|X|^2 |\Sigma|)$ dict operations. $\blacksquare$
