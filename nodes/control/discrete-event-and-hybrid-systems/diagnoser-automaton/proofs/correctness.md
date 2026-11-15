---
title: The diagnoser holds the exact state estimate, and the indeterminate cycle test decides diagnosability
proves: [correctness, termination]
status: full
---

**Setting.** The plant $G$ is a deterministic automaton with state set $X$, initial state $x_0$ and alphabet $\Sigma = \Sigma_o \cup \Sigma_{uo}$, where $\Sigma_o$ is the set of observable events. The fault events are unobservable, and each one has a fault type. The label $\ell(s)$ of a string $s$ is the set of fault types of the fault events in $s$. Labels only grow along a string. $P$ is the natural projection that erases the unobservable events. For a pair $p = (x, \ell)$ and $\sigma \in \Sigma_o$, MOVES$(p)[\sigma]$ is the set of pairs $(\delta(x, u\sigma), \ell \cup \ell(u\sigma))$ over all $u \in \Sigma_{uo}^*$ with $u\sigma$ defined at $x$. The function computes it by a search over pairs, so it stops even if $G$ has a cycle of unobservable events.

For $y \in \Sigma_o^*$ let

$$Q(y) = \{(\delta(x_0, s), \ell(s)) : s \in L(G),\ P(s) = y,\ s = \varepsilon \text{ or } s \text{ ends with an observable event}\}.$$

**Lemma 1 (meaning of a state).** For each $y \in \Sigma_o^*$: if $Q(y) \neq \emptyset$, the diagnoser reaches the state $Q(y)$ on $y$. If $Q(y) = \emptyset$, the diagnoser has no run on $y$.

*Proof.* By induction on $|y|$. For $y = \varepsilon$, only $s = \varepsilon$ qualifies, so $Q(\varepsilon) = \{(x_0, \emptyset)\}$, which is the state of line L1. Assume the claim for $y$, and let $\sigma \in \Sigma_o$. A string $s'$ that qualifies for $y\sigma$ ends with $\sigma$. Write $s' = s u \sigma$, where $s$ is the longest prefix of $s'$ before the last $\sigma$ that is empty or ends with an observable event. Then $s$ qualifies for $y$, $u \in \Sigma_{uo}^*$, and the pair of $s'$ is in MOVES$(p)[\sigma]$ for the pair $p$ of $s$. Conversely, each pair in MOVES$(p)[\sigma]$ for $p \in Q(y)$ is the pair of such a string $s u \sigma$. So $Q(y\sigma)$ is the union of MOVES$(p)[\sigma]$ over $p \in Q(y)$. This is the set that lines L6 and L7 build from the state $Q(y)$. Line L8 adds the transition exactly when the set is not empty. If $Q(y) = \emptyset$, then $Q(y\sigma) = \emptyset$ as well, and there is no run. $\blacksquare$

**Theorem (construction).** Lines L1 to L9 stop, and they return the part of the diagnoser that is reachable from $Q(\varepsilon)$.

*Proof.* A state is a set of pairs $(x, \ell)$ with $x \in X$ and $\ell$ a set of fault types. With $m$ fault types there are $|X| 2^m$ pairs, so at most $2^{|X| 2^m}$ states. Each state enters the queue once, so the loop of line L3 stops. By Lemma 1, each transition that line L8 adds is a transition of the diagnoser, and the search adds every transition from every reached state. $\blacksquare$

**The test.** Fix a fault type $F$. Lines L11 and L12 build the graph $T$. Its nodes are the triples $(q, a, b)$ with $q$ a reached diagnoser state, $a, b \in q$, $F$ in the label of $a$ and $F$ not in the label of $b$. There is an edge from $(q, a, b)$ to $(q', a', b')$ if $q' = \delta_d(q, \sigma)$, $a' \in$ MOVES$(a)[\sigma]$, $b' \in$ MOVES$(b)[\sigma]$ and $F$ is not in the label of $b'$, for some $\sigma \in \Sigma_o$. Then $a', b' \in q'$, and $F$ is in the label of $a'$, because labels only grow.

The type $F$ is diagnosable if there is an integer $N$ with this property: for every $s \in L(G)$ that ends with a fault event of type $F$ and every $t$ with $st \in L(G)$ and $|t| \ge N$, every $w \in L(G)$ with $P(w) = P(st)$ has a fault event of type $F$.

**Theorem (test).** Assume that $G$ has no cycle of unobservable events. Then $F$ is diagnosable if and only if $T$ has no cycle. Line L13 returns this answer.

*Proof that a cycle gives no diagnosability.* Let $(q, a, b)$ be a node on a cycle with the observable word $\sigma_1 \cdots \sigma_k$, $k \ge 1$. By Lemma 1 there is $y$ with $q = Q(y)$, a string $s_a$ for $a$ and a string $s_b$ for $b$, both with projection $y$. $s_a$ has a fault of type $F$, and $s_b$ has none. Each edge of the cycle extends the strings by $u\sigma_i$ and $v\sigma_i$ with $u, v \in \Sigma_{uo}^*$. One turn around the cycle brings $a = (x_a, \ell_a)$ back to itself, so it gives a string $c_a$ from $x_a$ to $x_a$ with $P(c_a) = \sigma_1 \cdots \sigma_k$ and $|c_a| \ge 1$. In the same way it gives $c_b$ from $x_b$ to $x_b$ with $P(c_b) = P(c_a)$, and $c_b$ has no fault of type $F$, because the label of $b$ does not get $F$. Let $s$ be the prefix of $s_a$ that ends with its first fault event of type $F$, and write $s_a = s r$. For every $N$, take $t = r c_a^N$ and $w = s_b c_b^N$. Then $st \in L(G)$, $|t| \ge N$, $w \in L(G)$, $P(w) = y\,P(c_a)^N = P(st)$, and $w$ has no fault of type $F$. So no $N$ works.

*Proof that no cycle gives diagnosability.* Let $M$ be the number of nodes of $T$, and $N = (M + 2)|X|$. Take $s$, $t$ and $w$ as in the definition, with $|t| \ge N$, and assume that $w$ has no fault of type $F$. Because $G$ has no cycle of unobservable events, a run of unobservable events visits each state at most once, so it has at most $|X| - 1$ events. So if $t$ has $j$ observable events, $|t| \le j + (j + 1)(|X| - 1)$, and $j \ge (|t| - |X| + 1)/|X| > M$. Let $y_0 = P(s)$, let $\sigma_1, \ldots, \sigma_j$ be the observable events of $t$, and let $y_i = y_0 \sigma_1 \cdots \sigma_i$. For $1 \le i \le j$, let $\alpha_i$ be the prefix of $st$ that ends with $\sigma_i$, and $\beta_i$ the prefix of $w$ that ends with its $(|y_0| + i)$-th observable event. Both qualify for $y_i$, so their pairs $a_i$ and $b_i$ are in $Q(y_i)$. $\alpha_i$ contains $s$, so $F$ is in the label of $a_i$, and $F$ is not in the label of $b_i$. So $(Q(y_i), a_i, b_i)$ is a node of $T$, and by the definition of MOVES there is an edge from node $i$ to node $i + 1$. This is a path with $j > M$ nodes in a graph with $M$ nodes, so a node repeats, and $T$ has a cycle. This contradicts the assumption, so every such $w$ has a fault of type $F$.

Line L13 runs Kahn's algorithm. It removes nodes of in-degree 0 until none is left, and it removes all nodes if and only if the graph has no cycle. $\blacksquare$

The first part of the proof does not use the assumption on unobservable cycles. The second part uses it to turn the length of $t$ into a number of observable events. Neither part uses the assumption of Sampath et al. that $L(G)$ is live.

**Cost.** $T$ has at most $D\,(|X| 2^m)^2$ nodes, where $D$ is the number of diagnoser states, and each node has at most $|\Sigma_o| (|X| 2^m)^2$ edges. So the test is polynomial in the size of the diagnoser, and the diagnoser can be exponential in $|X|$.
