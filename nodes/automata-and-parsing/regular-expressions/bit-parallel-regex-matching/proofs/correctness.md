---
title: The bit-parallel simulation accepts exactly the language of the expression
proves: [correctness, termination]
status: full
---

Let $G$ be the Glushkov automaton of $r$, with states $0, \ldots, k$, moves $(p, \mathrm{sym}(q), q)$ for $q \in \mathrm{Follow}(p)$, and accepting set $F$. By the correctness of the [Glushkov automaton](/glushkov-automaton/), $G$ accepts exactly $L(r)$. Identify a set $D \subseteq \{0, \ldots, k\}$ with the integer $\sum_{p \in D} 2^p$, so that $\mid$ is union, $\&$ is intersection, and bit $p$ of the integer is set if and only if $p \in D$. For a set $D$ write $\Phi(D) = \bigcup_{p \in D} \mathrm{Follow}(p)$, and for a symbol $c$ write $\delta(D, c) = \{q : (p, c, q) \text{ is a move of } G \text{ for some } p \in D\}$.

**Lemma 1 (homogeneity).** $\delta(D, c) = \Phi(D) \cap B[c]$, where $B[c] = \{q \ge 1 : \mathrm{sym}(q) = c\}$ is the set built at line L2.

*Proof.* A move $(p, c, q)$ exists if and only if $q \in \mathrm{Follow}(p)$ and $\mathrm{sym}(q) = c$. The positions in a Follow set are at least 1, and $\mathrm{sym}(q) = c$ for $q \ge 1$ means $q \in B[c]$. So $q \in \delta(D, c)$ if and only if $q \in \Phi(D)$ and $q \in B[c]$. $\square$

**Lemma 2 (tables).** After line L5, for each chunk $j$ and each $v$ with $0 \le v < 2^b$, $T_j[v] = \Phi(\{jb + i : \text{bit } i \text{ of } v \text{ is set}\})$, with $\mathrm{Follow}(p) = \emptyset$ for $p > k$.

*Proof.* By induction on $v$. For $v = 0$, $T_j[0] = 0 = \Phi(\emptyset)$. For $v > 0$, let $i$ be the index of the lowest set bit of $v$ and $v' = v - 2^i < v$. Line L5 sets $T_j[v] = T_j[v'] \mid \mathrm{Follow}(jb + i)$, where $\mathrm{Follow}(p) = \emptyset$ for $p > k$. By induction $T_j[v'] = \Phi(S')$ for the set $S'$ of $v'$, and the set of $v$ is $S' \cup \{jb + i\}$, so $T_j[v] = \Phi(S') \cup \mathrm{Follow}(jb + i) = \Phi(S' \cup \{jb + i\})$. $\square$

**Lemma 3 (one step).** For every $D \subseteq \{0, \ldots, k\}$ and symbol $c$, lines L8 and L9 compute $\delta(D, c)$.

*Proof.* For $j = 0, \ldots, g - 1$, the value $(D \gg jb) \mathbin{\&} (2^b - 1)$ is the integer $v_j$ whose bit $i$ is set if and only if $jb + i \in D$, so by Lemma 2, $T_j[v_j] = \Phi(D_j)$ with $D_j = D \cap \{jb, \ldots, jb + b - 1\}$. Since $g b \ge k + 1$, the sets $D_0, \ldots, D_{g-1}$ cover $D$, and $\Phi$ distributes over union, so $E = \Phi(D_0) \cup \cdots \cup \Phi(D_{g-1}) = \Phi(D)$ at line L8. Line L9 gives $E \cap B[c] = \delta(D, c)$ by Lemma 1. $\square$

**Invariant.** After line L9 in round $i$, $D = \delta^*(\{0\}, y_1 \cdots y_i)$, the set of states of $G$ that some run on $y_1 \cdots y_i$ from state 0 reaches.

*Proof.* Before the loop, $D = \{0\} = \delta^*(\{0\}, \varepsilon)$ by line L6. If $D = \delta^*(\{0\}, y_1 \cdots y_{i-1})$ before round $i$, Lemma 3 gives $\delta(D, y_i) = \delta^*(\{0\}, y_1 \cdots y_i)$ after line L9. $\square$

**Termination.** Line L5 runs $g(2^b - 1)$ rounds, the loop at line L7 at most $n$ rounds, and each round does $g$ lookups. So the algorithm stops.

**Theorem.** BITPARALLEL$(r, y, b)$ returns true if and only if $y \in L(r)$.

*Proof.* If line L10 returns false in round $i$, then $\delta^*(\{0\}, y_1 \cdots y_i) = \emptyset$ by the invariant; then $\delta^*(\{0\}, y) = \delta^*(\emptyset, y_{i+1} \cdots y_n) = \emptyset$ contains no accepting state, and $y \notin L(G) = L(r)$. Otherwise the loop ends with $D = \delta^*(\{0\}, y)$, and line L11 returns true if and only if this set meets $F$, that is, if and only if $G$ accepts $y$, that is, if and only if $y \in L(r)$. $\blacksquare$

**The search variant.** With $D \leftarrow \delta(D, y_i) \cup \{0\}$ in round $i$, and $D = \{0\}$ at the start, the same induction shows that after round $i$, $D = \bigcup_{s=0}^{i} \delta^*(\{0\}, y_{s+1} \cdots y_i)$: the runs that started before round $i$ are advanced by Lemma 3, and the added state 0 is the run of the empty suffix, with $s = i$. So $D$ meets $F$ after round $i$ if and only if some $y_{s+1} \cdots y_i$ with $0 \le s \le i$ is in $L(r)$.
