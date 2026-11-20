---
title: Round-robin allocation is EF1 for additive valuations
proves: [correctness]
status: full
---

**Setting.** There are $n \ge 1$ agents $1, \dots, n$ and a finite set $M$ of $m$ goods. Agent $i$ has an additive valuation with $v_i(g) \ge 0$ for each good $g$. We refer to the lines L1 to L8 of the page. A *turn* is one run of lines L4 to L7, and the turns are numbered $t = 0, 1, \dots$ as in the algorithm. Agent $i$ picks at the turns $t$ with $t \bmod n = i - 1$.

**Lemma 1 (termination and output).** The loop of line L3 runs exactly $m$ turns, and the output is an allocation: the bundles are disjoint and their union is $M$.

*Proof.* At the start of a turn $R \ne \emptyset$. Every good not in $R$ belongs to exactly one bundle and every good of $R$ belongs to none: this holds after line L2, where $R = M$ and all bundles are empty, and line L6 moves one good from $R$ to one bundle. Line L5 finds a good, because $L_i$ lists all of $M$ and $R \ne \emptyset$. So each turn removes exactly one good from $R$, and the loop stops after $m$ turns with $R = \emptyset$, when every good lies in exactly one bundle. $\square$

**Lemma 2 (each pick is a best free good).** The good $g$ chosen in line L5 at a turn of agent $i$ satisfies $v_i(g) \ge v_i(h)$ for every good $h$ in $R$ at that moment.

*Proof.* $L_i$ is sorted by $v_i$ in decreasing order, and $g$ is the first good of $L_i$ that lies in $R$. Any $h \in R$ appears at or after $g$ in $L_i$, so $v_i(h) \le v_i(g)$. $\square$

**Lemma 3 (phases).** Fix two different agents $i$ and $j$. Let $t_1 < t_2 < \dots < t_k$ be the turns of agent $i$, and set $t_{k+1} = m$. For $1 \le r \le k$, the phase $r$ is the set of turns $t$ with $t_r \le t < t_{r+1}$. Then each phase contains at most one turn of $j$, and if $j$ picks the good $h$ at a turn in phase $r$, the good $g_r$ that $i$ picks at $t_r$ has $v_i(g_r) \ge v_i(h)$.

*Proof.* The turns of $i$ are $n$ apart, so $t_{r+1} = t_r + n$ for $r < k$, and $m - t_k \le n$, since otherwise $t_k + n < m$ would be another turn of $i$. So each phase has at most $n$ consecutive turns, and $j$, whose turns are also $n$ apart, has at most one of them. If $j$ picks $h$ at a turn in phase $r$, that turn is after $t_r$, so $h$ was in $R$ at turn $t_r$. Lemma 2 gives $v_i(g_r) \ge v_i(h)$. $\square$

**Lemma 4 (turns before the first phase).** The turns $t < t_1$ contain at most one turn of $j$, and none if $j > i$.

*Proof.* Agent $i$ has its first turn at $t_1 = i - 1$, if $m \ge i$. The turns $0, \dots, i - 2$ belong to agents $1, \dots, i - 1$, one each. So $j$ has at most one turn before $t_1$, and none if $j > i$. If $m < i$, agent $i$ never picks, all $m$ turns go to distinct agents $1, \dots, m$, and $j$ has at most one turn; it has none if $j > i > m$. $\square$

**Theorem (EF1).** For all agents $i \ne j$: if $j > i$ then $v_i(A_i) \ge v_i(A_j)$; if $j < i$ and $A_j \ne \emptyset$, then $v_i(A_i) \ge v_i(A_j \setminus \{h_1\})$, where $h_1$ is the first good picked by $j$. Hence the output is EF1.

*Proof.* By Lemma 1 every pick of $j$ is at some turn, either before $t_1$ or in one of the phases. By Lemma 3, the picks of $j$ inside phases are distinct goods $h$ paired with distinct goods $g_r$ of $A_i$ (one per phase) with $v_i(g_r) \ge v_i(h)$. Summing over these pairs and using $v_i \ge 0$ for the goods of $A_i$ left unpaired,

$$v_i(A_i) \ge \sum_{h \text{ picked by } j \text{ in a phase}} v_i(h).$$

By Lemma 4, the picks of $j$ outside the phases are none if $j > i$, and at most the single good $h_1$ if $j < i$; if $i$ has no turn at all, there are no phases and $A_j \subseteq \{h_1\}$. In the first case the right side is $v_i(A_j)$. In the second case it is $v_i(A_j \setminus \{h_1\})$, by additivity. For the EF1 condition, take $g = h_1$ if $j < i$, and any good of $A_j$ if $j > i$, using $v_i(A_j \setminus \{g\}) \le v_i(A_j)$ since values are nonnegative. $\blacksquare$
