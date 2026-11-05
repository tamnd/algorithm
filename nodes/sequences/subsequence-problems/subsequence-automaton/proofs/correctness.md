---
title: The subsequence automaton accepts exactly the subsequences of the text
proves: [correctness]
status: full
---

We use the pseudocode of the page. Let $T = t_1 \cdots t_n$. For $0 \le i \le n$ write $T_{>i} = t_{i+1} \cdots t_n$. For a word $P$ and $0 \le q \le n$, write $P \preceq_q T$ if $P$ is a subsequence of $t_1 \cdots t_q$. Let $\mathrm{first}(P)$ be the least $q$ with $P \preceq_q T$, or NIL if $P \not\preceq T$; then $\mathrm{first}(\varepsilon) = 0$.

**Lemma 1 (the table).** After BUILD, for all $0 \le i \le n$ and all letters $c$, $\mathrm{nxt}[i][c] = \min\{ j : i < j \le n,\ t_j = c \}$, or NIL if the set is empty.

*Proof.* Induction on $i$ from $n$ down. For $i = n$ the set is empty, and line L1 sets NIL. Let $i \le n$ and assume the claim for row $i$. Lines L3 and L4 make row $i - 1$ equal to row $i$ except at $t_i$, where the entry is $i$. For $c = t_i$, the least $j > i - 1$ with $t_j = c$ is $i$. For $c \ne t_i$, a $j > i - 1$ with $t_j = c$ has $j \ne i$, so $j > i$, and the least one is $\mathrm{nxt}[i][c]$ by the hypothesis. $\square$

**Lemma 2 (greedy step).** Let $P$ be a word with $q = \mathrm{first}(P) \ne$ NIL, and let $c$ be a letter. Then $\mathrm{first}(Pc) = \mathrm{nxt}[q][c]$, where NIL on the right means that $Pc \not\preceq T$.

*Proof.* If $j = \mathrm{nxt}[q][c] \ne$ NIL, then $P \preceq_q T$ and $t_j = c$ with $j > q$, so $Pc \preceq_j T$ and $\mathrm{first}(Pc) \le j$. Conversely, let $Pc \preceq_{j'} T$ with an embedding whose last position is $j' $ and holds $c$. The other positions embed $P$ in $t_1 \cdots t_{j' - 1}$, so $q = \mathrm{first}(P) \le j' - 1$, that is, $j' > q$, and $t_{j'} = c$. By Lemma 1, $\mathrm{nxt}[q][c]$ is defined and at most $j'$. So $\mathrm{first}(Pc) \ge j$ when $j$ is defined, and if $\mathrm{nxt}[q][c] = $ NIL, no such $j'$ exists and $Pc \not\preceq T$. $\square$

**Theorem 1.** CONTAINS($P$) returns true if and only if $P \preceq T$. Each time line L8 completes with $q \ne$ NIL after the letters $p_1 \cdots p_r$, $q = \mathrm{first}(p_1 \cdots p_r)$.

*Proof.* Induction on $r$. For $r = 0$, line L6 sets $q = 0 = \mathrm{first}(\varepsilon)$. The step from $r$ to $r + 1$ is Lemma 2. If line L9 returns false after $p_1 \cdots p_{r+1}$, then this prefix is not a subsequence of $T$ by Lemma 2, and so neither is $P$. If the loop ends, $\mathrm{first}(P) \ne$ NIL, so $P \preceq T$, and line L10 returns true. $\square$

**Lemma 3 (the words read from a state).** For each state $i$, the words $w$ that the automaton can read from state $i$ without a NIL move are exactly the subsequences of $T_{>i}$, and each such word has exactly one path.

*Proof.* The automaton is deterministic, so each word has at most one path from $i$. A path from $i$ that reads $c_1 \cdots c_r$ visits states $i < j_1 < \cdots < j_r$ with $t_{j_s} = c_s$ by Lemma 1, so the word is a subsequence of $T_{>i}$. Conversely, Lemma 2 applied to the text $T$, with the start state $i$ in place of 0 (the proof is the same, with positions restricted to $(i, n]$), shows that a subsequence of $T_{>i}$ is read from $i$ without a NIL move. $\square$

**Theorem 2.** COUNT-DISTINCT returns the number of distinct subsequences of $T$, the empty one included.

*Proof.* Let $N(i)$ be the number of distinct subsequences of $T_{>i}$, the empty one included. By Lemma 3, $N(i)$ is the number of paths that start at $i$ (the path of length 0 reads $\varepsilon$). Each non-empty path starts with a move to some $\mathrm{nxt}[i][c] \ne$ NIL and continues with a path from there, and the first letter $c$ and the rest of the path determine it. So $N(i) = 1 + \sum_{c} N(\mathrm{nxt}[i][c])$ over the letters with a move. All moves go to larger states, so line L11, which runs from $n$ down to 0, uses only values already computed; $\mathrm{cnt}[n] = 1 = N(n)$. By induction $\mathrm{cnt}[i] = N(i)$, and line L12 returns $N(0)$. $\square$

**Theorem 3 (minimality).** Every deterministic automaton, with partial or total transitions, that accepts exactly the subsequences of $T$ has at least $n + 1$ states that are not dead, so the subsequence automaton has the least number of states.

*Proof.* By Lemma 3, the language accepted from state $i$ is $L_i = \{ w : w \preceq T_{>i} \}$. For $i < i'$, $T_{>i}$ itself is in $L_i$ and has length $n - i > n - i'$, while every word of $L_{i'}$ has length at most $n - i'$. So the $n + 1$ languages $L_0, \ldots, L_n$ are distinct and non-empty. The words $t_1 \cdots t_i$, for $0 \le i \le n$, lead state 0 of our automaton to state $i$, by Theorem 1 (the leftmost embedding of a prefix of $T$ is the prefix itself). In any deterministic automaton for the same language, the states reached by two of these words must accept different languages: for $i < i'$, the word $T_{>i}$ is accepted after $t_1 \cdots t_i$, but $t_1 \cdots t_{i'} T_{>i}$ has length $n + i' - i > n$ and is not a subsequence of $T$. So these $n + 1$ words reach $n + 1$ different states, and none of them is dead. $\square$

**Cost.** BUILD copies $n$ rows of $\sigma$ entries: $\Theta(n \sigma)$. CONTAINS does at most $k$ iterations with one lookup each. COUNT-DISTINCT reads each of the $(n + 1) \sigma$ entries once.
