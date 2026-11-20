---
title: The Aziz-Mackenzie recursion is envy-free, and the toy for three agents is envy-free
proves: [correctness]
status: partial
---

**Setting.** The cake is $[0, 1]$. Agents $1, \dots, n$ have nonnegative, additive and nonatomic valuations $V_i$ with $V_i([0, 1]) = 1$. At each moment the pieces $X_1, \dots, X_n$ given out so far and the leftover $R$ are disjoint and cover the cake. Agent $i$ dominates agent $j$ if $V_i(X_i) - V_i(X_j) \ge V_i(R)$. We refer to the lines L1 to L7 of the page, and we assume only that each round of line L3 gives out a part of $R$ with no envy among the agents of $N$. This proof shows that the recursion is envy-free when it stops, and that the toy for three agents in `impl/python` is envy-free and stops. It does not prove that the loop of lines L2 to L6 ends within the bound of Aziz and Mackenzie; that is the theorem of their FOCS 2016 paper, and it is the reason for the status "partial".

**Lemma 1 (domination lasts).** If $i$ dominates $j$ before a round, it dominates $j$ after the round.

*Proof.* Let the round give the parts $P_k$ of a part $P$ of $R$ with $V_i(P_i) \ge V_i(P_j)$. Then $V_i(X_i \cup P_i) - V_i(X_j \cup P_j) \ge V_i(X_i) - V_i(X_j) \ge V_i(R) \ge V_i(R \setminus P)$. If $i$ is not in $N$, it gets no part and $j$ gets $P_j \subseteq R$; then $V_i(X_i) - V_i(X_j \cup P_j) \ge V_i(R) - V_i(P_j) \ge V_i(R \setminus P)$, since $P_j \subseteq P$. $\square$

**Lemma 2 (invariant).** At every call of AZIZ-MACKENZIE$(N, R)$, there is no envy on the pieces given out, and every agent outside $N$ dominates every agent in $N$.

*Proof.* At the first call, $N$ is all agents and nothing is given out. A round gives parts only to agents of $N$, with no envy among them, so it keeps the first part of the invariant for pairs inside $N$. An agent $k$ outside $N$ envies no one, because it dominates every agent of $N$ by Lemma 1, and $V_k(X_k) \ge V_k(X_j) + V_k(R) \ge V_k(X_j \cup P_j)$; pieces of other agents outside $N$ do not change. No agent of $N$ envies $k$, because $X_k$ does not change and the pieces of $N$ only grow. Line L7 is reached when $i$ dominates every other agent of $N$; then every agent outside $N \setminus \{i\}$ dominates every agent in $N \setminus \{i\}$, by the invariant and Lemma 1. $\square$

**Theorem 1.** If the recursion stops, the division is envy-free.

*Proof.* The recursion ends at line L1 with $N = \{k\}$. Before line L1 there is no envy, and every other agent $i$ dominates $k$, so $V_i(X_i) \ge V_i(X_k) + V_i(R) = V_i(X_k \cup R)$. Agent $k$ only gains. No other piece changes. $\square$

**The toy.** The toy has $n = 3$. With three agents in $N$, a round is stage one of the Selfridge-Conway procedure on $R$, with the cutter taking turns. With two agents, a round is divide and choose on $R$: one agent cuts $R$ into two parts of equal value to it, and the other picks the part it likes more. The toy checks for domination after each round.

**Lemma 3 (toy rounds).** Each toy round gives out a part of $R$ with no envy among the agents of $N$. After a three-agent round with cutter $c$, $c$ dominates the agent $T$ that took the trimmed piece. After a two-agent round, $R$ is empty.

*Proof.* In a three-agent round the chooser picks first; the trimmer values the trimmed piece and its second best piece equally and both at least as much as the third, and at most one of these two is taken before it; the cutter values the untrimmed pieces at $V_c(R)/3$ and the trimmed piece at $V_c(R)/3 - V_c(R')$, where $R'$ is the trimmings, and the trimmed piece is never left for it. So the round has no envy, and the gain of $c$ over $T$ in this round is $V_c(R')$. By induction over the earlier rounds, which have no envy, $V_c(X_c) - V_c(X_T) \ge V_c(R')$. In divide and choose the chooser picks the better part and the cutter values both parts equally, and the two parts make up all of $R$. $\square$

**Lemma 4 (the fallback).** Suppose $c$ dominates $T$ among three agents in $N$, and let $u$ be the third. If $u$ cuts $R$ into three parts of value $V_u(R)/3$ each, $T$ picks a best part, then $c$ picks a best remaining part, and $u$ takes the last, the final division is envy-free.

*Proof.* $T$ chooses first and $u$ values the parts equally, so neither envies another on $R$. Agent $c$ can envy only $T$ on $R$, and $V_c(X_c) - V_c(X_T) \ge V_c(R)$ covers all of $R$. $\square$

**Theorem 2.** The toy stops and returns an envy-free division of $[0, 1]$ among three agents.

*Proof.* With two agents, the first round leaves $R$ empty, and then each agent dominates the other, because the pieces have no envy and $V_i(\emptyset) = 0$. So the loop ends after one round. With three agents, each pass of the loop either runs a round and adds 1 to the round counter, or, when the counter has reached `max_rounds`, returns through the fallback. The condition `max_rounds >= 1` makes sure that at least one round ran, so the fallback has a cutter $c$ and a taker $T$, and $c$ still dominates $T$ by Lemma 1. So the toy stops, and the result is envy-free by Lemma 4 or by Theorem 1. Every interval of $R$ goes to some agent, so the pieces cover the cake. $\square$

The toy cannot force domination with three agents, which is why it needs the cap. The protocol of Aziz and Mackenzie forces domination with its core protocol and other sub-protocols, which this proof does not cover.
