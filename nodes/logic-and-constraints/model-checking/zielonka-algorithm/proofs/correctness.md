---
title: Zielonka's algorithm returns the winning regions with positional winning strategies
proves: [correctness, termination]
status: full
---

**Setting.** A game is $G = (V, V_0, V_1, E, \Omega)$ with $V$ finite, $V = V_0 \sqcup V_1$, $E \subseteq V \times V$, and $\Omega : V \to \mathbb{N}$. Each vertex has at least one successor. A play is an infinite path, and player 0 wins it when the largest priority that occurs infinitely often on it is even. A positional strategy of player $j$ on a set $W$ is a map $\sigma_j$ from $W \cap V_j$ to successors. A play *follows* $\sigma_j$ when each move from a vertex $v \in W \cap V_j$ goes to $\sigma_j(v)$. For $j \in \{0, 1\}$ we write $\bar{j} = 1 - j$.

We say that $(W, \sigma_j)$ is a *dominion* of player $j$ in $G$ when: (D1) each vertex of $W \cap V_{\bar{j}}$ has all its successors in $W$, (D2) $\sigma_j(v) \in W$ for each $v \in W \cap V_j$, and (D3) each play that starts in $W$ and follows $\sigma_j$ is won by player $j$. By (D1) and (D2), a play that starts in $W$ and follows $\sigma_j$ never leaves $W$.

A set $T$ is a *trap for player $j$* when each vertex of $T \cap V_j$ has all its successors in $T$, and each vertex of $T \cap V_{\bar{j}}$ has at least one successor in $T$. Then each vertex of $T$ has a successor in $T$, so the restriction $G[T]$ is a game.

**Lemma 1 (prefix independence).** Two plays that differ only in a finite prefix have the same winner.

*Proof.* The set of priorities that occur infinitely often does not change when a finite prefix changes. $\square$

**Lemma 2 (attractor).** Let $A$ be the set that ATTR$_j(G, U)$ returns, and number the vertices of $A$ in the order in which they join $A$, the vertices of $U$ first. Then:

1. a vertex $v \in A \setminus U$ of player $j$ has $\sigma(v) \in A$ with a smaller number, and a vertex $v \in A \setminus U$ of player $\bar{j}$ has all its successors in $A$ with smaller numbers;
2. each play that starts in $A$ and follows $\sigma$ on $A \setminus U$ reaches $U$ within $|A|$ moves;
3. $V \setminus A$ is a trap for player $j$.

*Proof.* (1) A vertex $v$ of player $j$ joins $A$ at line L18 when a successor $w$ of $v$ leaves the queue, so $w$ joined earlier, and line L18 sets $\sigma(v) = w$. A vertex $v$ of player $\bar{j}$ joins $A$ at line L20 when its counter reaches 0. Line L14 sets the counter to the number of successors, and line L19 lowers it by one for each successor that leaves the queue, which is after that successor joined $A$. So all successors of $v$ joined $A$ before $v$.

(2) By (1), each move from a vertex of $A \setminus U$ that follows $\sigma$ goes to a vertex with a smaller number, whatever player $\bar{j}$ chooses. The numbers are distinct and there are $|A|$ of them, so after at most $|A|$ moves the play is in $U$.

(3) Each vertex of $A$ enters the queue when it joins $A$, and the loop of line L15 runs until the queue is empty, so each vertex of $A$ leaves the queue and its predecessors are scanned. Take $v \in V \setminus A$. If $v \in V_j$ and $v$ had a successor $w \in A$, then line L18 would add $v$ when $w$ leaves the queue. So all successors of $v$ are outside $A$. If $v \in V_{\bar{j}}$ and all its successors were in $A$, its counter would reach 0 and line L20 would add $v$. So $v$ has a successor outside $A$. $\square$

**Lemma 3 (traps keep dominions).** Let $T$ be a trap for player $j$ in $G$, and let $(W, \tau)$ be a dominion of player $\bar{j}$ in $G[T]$. Then $(W, \tau)$ is a dominion of player $\bar{j}$ in $G$.

*Proof.* (D2) holds because the successor $\tau(v)$ is in $W$. For (D1), take $v \in W \cap V_j$. Its successors in $G[T]$ are in $W$ by (D1) in $G[T]$, and all its successors in $G$ are in $T$ because $T$ is a trap for player $j$. So all its successors in $G$ are in $W$. Then a play in $G$ that starts in $W$ and follows $\tau$ stays in $W \subseteq T$, so it is a play of $G[T]$ that follows $\tau$, and player $\bar{j}$ wins it. This is (D3). $\square$

**The recursive form.** Define $R(G)$ by recursion on $|V|$. If $V = \emptyset$, $R(G) = (\emptyset, \emptyset)$. Else let $p$, $i$, $U$, $A$ be as in lines L3 to L5, and $(W'_0, W'_1) = R(G[V \setminus A])$. If $W'_{\bar{i}} = \emptyset$, then $R(G)$ gives $V$ to player $i$ and $\emptyset$ to player $\bar{i}$. Else let $B = \mathrm{Attr}_{\bar{i}}(G, W'_{\bar{i}})$, $(W''_0, W''_1) = R(G[V \setminus B])$, and $R(G)$ gives $W''_i$ to player $i$ and $W''_{\bar{i}} \cup B$ to player $\bar{i}$. The calls are on games with fewer vertices, because $A \supseteq U \neq \emptyset$ and $B \supseteq W'_{\bar{i}} \neq \emptyset$, and both sets $V \setminus A$ and $V \setminus B$ are traps by Lemma 2 (3), so both restrictions are games.

**Theorem.** For each game $G$, $R(G) = (W_0, W_1)$ is a partition of $V$, and with the strategies of the page, $(W_0, \sigma_0)$ is a dominion of player 0 and $(W_1, \sigma_1)$ is a dominion of player 1.

*Proof.* By strong induction on $|V|$. If $V = \emptyset$, there is nothing to prove. Let $|V| \ge 1$, and assume the theorem for all games with fewer vertices. By the induction hypothesis, $(W'_0, W'_1)$ is a partition of $V \setminus A$, with dominions $(W'_0, \sigma'_0)$ and $(W'_1, \sigma'_1)$ in $G[V \setminus A]$.

*Case 1: $W'_{\bar{i}} = \emptyset$.* Then $W'_i = V \setminus A$. Let $\sigma_i$ be $\sigma'_i$ on $W'_i \cap V_i$, the attractor strategy $\sigma$ on $(A \setminus U) \cap V_i$, and any successor on $U \cap V_i$. The pair $(V, \emptyset)$ is a partition, and (D1) and (D2) hold for $W = V$. For (D3), take a play $\pi$ that follows $\sigma_i$. If $\pi$ visits $A$ infinitely often, then by Lemma 2 (2) each visit to $A \setminus U$ is followed by a visit to $U$ within $|A|$ moves, so $\pi$ visits $U$ infinitely often. Then the priority $p$ occurs infinitely often, no priority above $p$ occurs at all, and $p \bmod 2 = i$, so player $i$ wins. If $\pi$ visits $A$ only finitely often, then from some position $k$ on it stays in $V \setminus A = W'_i$. The suffix from position $k$ is a play of $G[V \setminus A]$ that starts in $W'_i$ and follows $\sigma'_i$, so player $i$ wins it by the dominion property, and wins $\pi$ by Lemma 1.

*Case 2: $W'_{\bar{i}} \ne \emptyset$.* First, $(W'_{\bar{i}}, \sigma'_{\bar{i}})$ is a dominion of player $\bar{i}$ in $G$: the set $V \setminus A$ is a trap for player $i$ by Lemma 2 (3), so Lemma 3 applies with $j = i$. Let $\sigma_B$ be $\sigma'_{\bar{i}}$ on $W'_{\bar{i}} \cap V_{\bar{i}}$ and the attractor strategy of $\mathrm{Attr}_{\bar{i}}(G, W'_{\bar{i}})$ on the rest of $B \cap V_{\bar{i}}$. A play that starts in $B$ and follows $\sigma_B$ reaches $W'_{\bar{i}}$ in finitely many moves by Lemma 2 (2), stays there by (D1) and (D2), and is won by player $\bar{i}$ by (D3) and Lemma 1. Also, a vertex of $B \cap V_i$ outside $W'_{\bar{i}}$ has all successors in $B$ by Lemma 2 (1), and a vertex of $W'_{\bar{i}} \cap V_i$ has all successors in $W'_{\bar{i}}$. So $(B, \sigma_B)$ is a dominion of player $\bar{i}$ in $G$.

By the induction hypothesis on $G[V \setminus B]$, $(W''_0, W''_1)$ is a partition of $V \setminus B$ with dominions $(W''_0, \sigma''_0)$ and $(W''_1, \sigma''_1)$. So $(W''_i, W''_{\bar{i}} \cup B)$ is a partition of $V$. The set $V \setminus B$ is a trap for player $\bar{i}$ by Lemma 2 (3), so Lemma 3 with $j = \bar{i}$ shows that $(W''_i, \sigma''_i)$ is a dominion of player $i$ in $G$.

For player $\bar{i}$, let $\sigma_{\bar{i}}$ be $\sigma''_{\bar{i}}$ on $W''_{\bar{i}} \cap V_{\bar{i}}$ and $\sigma_B$ on $B \cap V_{\bar{i}}$, and let $W = W''_{\bar{i}} \cup B$. (D2) holds because both strategies choose inside $W$. For (D1), take $v \in W \cap V_i$. If $v \in B$, its successors are in $B$ as shown above. If $v \in W''_{\bar{i}}$, its successors in $V \setminus B$ are in $W''_{\bar{i}}$ by (D1) in $G[V \setminus B]$, and its other successors are in $B$. So all are in $W$. For (D3), take a play $\pi$ that starts in $W$ and follows $\sigma_{\bar{i}}$. If $\pi$ never enters $B$, it is a play of $G[V \setminus B]$ that starts in $W''_{\bar{i}}$ and follows $\sigma''_{\bar{i}}$, and player $\bar{i}$ wins it. If $\pi$ enters $B$ at some position, the suffix from there starts in $B$ and follows $\sigma_B$, so player $\bar{i}$ wins it, and wins $\pi$ by Lemma 1. $\square$

**The loop computes $R$.** Let $G_0$ be the input of a call of ZIELONKA, and let $(R_0(G), R_1(G)) = R(G)$. Consider the invariant

> **(L)** $R_j(G_0) = X_j \cup R_j(G)$ for $j = 0, 1$, where $G$ is the current game.

Line L1 makes (L) true with $G = G_0$. Line L6 computes $R(G \setminus A)$, by induction on the number of vertices, because $G \setminus A$ is smaller. If the test of line L7 holds, $R(G) = (V(G), \emptyset)$ with $V(G)$ on the side of player $i$, so by (L) line L8 returns $R(G_0)$. Else $R(G)$ is $R(G \setminus B)$ with $B$ added to the side of player $\bar{i}$, so after lines L10 and L11, (L) holds again for the new $G$. Each pass that does not return removes $B \ne \emptyset$, so the loop ends after at most $|V(G_0)|$ passes. If it ends at line L12, then $G$ is empty, $R(G) = (\emptyset, \emptyset)$, and (L) gives $(X_0, X_1) = R(G_0)$. The strategies of the page are the ones of the theorem, built in the same order.

**Corollary (positional determinacy).** In each finite game, the winning regions of the two players partition $V$, and each player has one positional strategy that wins from every vertex of her winning region, against all strategies of the opponent, positional or not.

*Proof.* By the theorem, player $j$ wins from each vertex of $W_j$ with $\sigma_j$, since (D3) speaks of all plays that follow $\sigma_j$, whatever the opponent does. A vertex cannot be won by both players: if $\tau_0$ and $\tau_1$ both won from $v$, the unique play from $v$ that follows both would be won by both players. So $W_j$ is exactly the winning region of player $j$. $\blacksquare$
