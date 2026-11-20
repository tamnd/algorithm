---
title: The Brams-Taylor procedure is envy-free when it stops, and the toy for three agents is envy-free
proves: [correctness]
status: partial
---

**Setting.** The cake is $[0, 1]$. Agents $1, \dots, n$ have nonnegative, additive and nonatomic valuations $V_i$ with $V_i([0, 1]) = 1$. At each moment the pieces $X_1, \dots, X_n$ given out so far and the leftover $R$ are disjoint and cover the cake. Agent $i$ has an irrevocable advantage over agent $j$ if $V_i(X_i) - V_i(X_j) \ge V_i(R)$. We refer to the lines L1 to L9 of the page. This proof shows that the protocol is envy-free when it stops, and that the toy for three agents in `impl/python` is envy-free and stops. It does not prove that each while loop of the protocol for $n$ agents ends; that is the theorem of Brams and Taylor (1995), and it is the reason for the status "partial".

**Lemma 1 (advantages last).** If $i$ has an irrevocable advantage over $j$ before a round of lines L4 to L7, it has one after the round.

*Proof.* The round gives parts $P_1, \dots, P_n$ of a part $P$ of $R$ with no envy, so $V_i(P_i) \ge V_i(P_j)$. After the round, $V_i(X_i \cup P_i) - V_i(X_j \cup P_j) \ge V_i(X_i) - V_i(X_j) \ge V_i(R) \ge V_i(R \setminus P)$, because $V_i$ is additive and nonnegative. $\square$

**Lemma 2 (no envy at the end).** If the loop of lines L2 to L7 ends, the division of line L9 is envy-free.

*Proof.* The loop for the pair $(i, j)$ ends only when $i$ has an irrevocable advantage over $j$. By Lemma 1 the advantage holds until the end of the loop, so at line L8 every agent has an irrevocable advantage over every other agent. Line L8 gives $R$ to an agent $k$. For $i \ne k$, $V_i(X_i) \ge V_i(X_k) + V_i(R) = V_i(X_k \cup R)$. For $i$ and $j$ that are both different from $k$, nothing changes, and $V_i(X_i) - V_i(X_j) \ge V_i(R) \ge 0$. Agent $k$ only gains. So no agent envies another. $\square$

**The toy.** The toy has $n = 3$. Each round is stage one of the Selfridge-Conway procedure on $R$, with $i$ as the cutter, $c$: the cutter cuts $R$ into three pieces of value $V_c(R)/3$ each; the trimmer $t$ trims its best piece, if it is strictly best, to the value of its second best piece, and the trimmings are the new leftover $R'$; the chooser picks a best piece; the trimmer takes the trimmed piece if it is still there, and otherwise a best remaining piece; the cutter takes the last piece.

**Lemma 3 (a toy round).** A toy round divides $R \setminus R'$ with no envy. If $T$ is the agent that takes the trimmed piece, then $V_c(P_c) - V_c(P_T) = V_c(R')$.

*Proof.* The chooser picks first, so it envies no one. The trimmer values the trimmed piece and its second best piece equally and both at least as much as the third piece. At most one of these two is taken by the chooser, so the trimmer gets a piece of the largest value among the three pieces as they are after the trim. The cutter values each untrimmed piece at $V_c(R)/3$ and the trimmed piece at $V_c(R)/3 - V_c(R')$. The trimmed piece is never left for the cutter, so the cutter gets an untrimmed piece and envies no one. Its gain over $T$ is $V_c(R)/3 - (V_c(R)/3 - V_c(R')) = V_c(R')$. If there is no trim, $R' = \emptyset$ and the gain is $0 = V_c(R')$. $\square$

By Lemma 3 and induction over the earlier rounds, each of which is envy-free, after a toy round with cutter $c$ the agent $c$ has an irrevocable advantage over $T$.

**Lemma 4 (the fallback).** Suppose $c$ has an irrevocable advantage over $T$, and let $u$ be the third agent. If $u$ cuts $R$ into three pieces of value $V_u(R)/3$ each, then $T$ picks a best piece, then $c$ picks a best remaining piece, and $u$ takes the last piece, the final division is envy-free.

*Proof.* Before the fallback there is no envy on the pieces given out, by Lemma 3. $T$ picks first, so it envies no one on $R$. Agent $c$ envies no one on $R$ except possibly $T$, and $V_c(X_c) - V_c(X_T) \ge V_c(R)$ covers any part of $R$ that $T$ gets. Agent $u$ values the three parts of $R$ equally. Adding an envy-free division of $R$ to an envy-free division of the rest, with the one exception covered by the advantage, gives an envy-free division. $\square$

**Theorem.** The toy stops after at most `max_rounds` rounds and returns an envy-free division of $[0, 1]$ among three agents.

*Proof.* Each pass through the while loop either returns through the fallback, when the round counter has reached `max_rounds`, or runs one round and adds 1 to the counter. So there are at most `max_rounds` rounds. If the toy returns through the fallback, the last round had a cutter $c$ and a taker $T$, and $c$ still has an irrevocable advantage over $T$ by Lemma 1, so the result is envy-free by Lemma 4. The condition `max_rounds >= 1` makes sure that there was a last round. If the loops over all ordered pairs end, the result is envy-free by Lemma 2. In both cases every interval of $R$ goes to some agent, so the pieces cover the cake. $\square$

The toy chooses which agent takes the trimmed piece only through the order of the roles, so it can fail to make an advantage of $i$ over $j$ in a round. This is why it needs the cap. The protocol of Brams and Taylor uses a different round for $n$ agents, which this proof does not cover.
