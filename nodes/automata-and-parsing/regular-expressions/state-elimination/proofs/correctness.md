---
title: State elimination returns an expression for the language of the automaton
proves: [correctness]
status: full
---

**Statement.** Let $N = (Q, \Sigma, \delta, q_0, F)$ be a finite automaton with $n$ states and $t$ moves, some of which may be $\varepsilon$-moves. For every order of removal, STATE-ELIMINATION$(N)$ returns a regular expression $r$ with $L(r) = L(N)$. With shared labels it runs in $O(n^3 + t)$ time.

**Setup.** Let $N'$ be $N$ with the two new states $s$ and $f$ and the moves $s \xrightarrow{\varepsilon} q_0$ and $q \xrightarrow{\varepsilon} f$ for $q \in F$ of line L1. A word $w$ is in $L(N)$ if and only if some path of $N'$ from $s$ to $f$ reads $w$: such a path is $s \to q_0$, then a path of $N$ from $q_0$ to some $q \in F$, then $q \to f$, and the two new moves read nothing. Let $E$ be the set of states eliminated so far, a subset of $Q$. For remaining states $p, q$ (in $Q \setminus E$ or in $\{s, f\}$), let $P_E(p, q)$ be the set of words read by paths of $N'$ from $p$ to $q$ that have at least one move and whose inner states, all states visited strictly between the first and the last, lie in $E$.

**Simplifications.** The constructors used in lines L2, L4 and L7 apply only the laws $\emptyset \mid r = r$, $r \mid r = r$ (when both sides are the same stored expression), $\emptyset r = r \emptyset = \emptyset$, $\varepsilon r = r \varepsilon = r$, $\emptyset^* = \varepsilon^* = \varepsilon$ and $(r^*)^* = r^*$. Each holds as an equality of languages, so we can reason about the languages of the labels and ignore the simplifications.

**Invariant.** Before each pass of line L3 and after the last one, $L(R[p][q]) = P_E(p, q)$ for all remaining $p, q$, where a missing label stands for $\emptyset$.

*Base.* Before the first pass, $E = \emptyset$, so a path counted by $P_\emptyset(p, q)$ has no inner state and is a single move from $p$ to $q$. Lines L1 and L2 set $R[p][q]$ to the union of the labels of these moves, which is exactly $P_\emptyset(p, q)$.

*Step.* Suppose the invariant holds for $E$, and the pass removes $k$; let $E' = E \cup \{k\}$. Take remaining states $p, q \neq k$; they may be equal. Consider a path $\pi$ from $p$ to $q$ with at least one move and inner states in $E'$.

- If $k$ is not an inner state of $\pi$, then $\pi$ is counted by $P_E(p, q)$.
- Otherwise, cut $\pi$ at each visit to $k$. The pieces are: a path from $p$ to $k$, then $j \ge 0$ paths from $k$ to $k$, then a path from $k$ to $q$. Each piece has at least one move, since it joins two distinct visits or a visit to an end point, and its inner states lie in $E$, since all visits to $k$ are cut points. So the word of $\pi$ is in $P_E(p, k) \, P_E(k, k)^j \, P_E(k, q)$.

Conversely, every word of $P_E(p, q)$ is read by a path with inner states in $E \subseteq E'$, and every word in $P_E(p, k) \, P_E(k, k)^j \, P_E(k, q)$ is read by the concatenation of the corresponding paths, which goes from $p$ to $q$, has at least one move, and has inner states in $E \cup \{k\} = E'$. Hence
$$P_{E'}(p, q) = P_E(p, q) \cup P_E(p, k)\, P_E(k, k)^*\, P_E(k, q).$$
By the invariant for $E$, the right side is $L(R[p][q] \mid R[p][k] \cdot (R[k][k])^* \cdot R[k][q])$. Line L4 sets $L$ to $(R[k][k])^*$, and line L7 assigns this expression to $R[p][q]$ for every $p$ with $R[p][k] \neq \emptyset$ and every $q$ with $R[k][q] \neq \emptyset$. For the other pairs the second term is $\emptyset$, and $R[p][q]$ correctly stays as it is. All updates in the pass read $R[p][k]$, $R[k][k]$ and $R[k][q]$, which the pass does not change, because $p, q \neq k$; so the order of the updates inside the pass does not matter. Line L8 removes $k$, which is no longer a remaining state. The invariant holds for $E'$.

**Conclusion.** After the last pass, $E = Q$ and the remaining states are $s$ and $f$. Every path of $N'$ from $s$ to $f$ has at least one move, since $s \neq f$, and its inner states are in $Q$, since $s$ has no incoming moves and $f$ has no outgoing moves. So $L(R[s][f]) = P_Q(s, f) = L(N)$, and line L9 returns a correct expression. $\square$

**Running time.** Lines L1 and L2 cost $O(n + t)$, building at most $|F| + t + 1$ labels with $O(1)$ work each. The pass that removes $k$ runs the inner loop for at most $\mathrm{in}(k) \cdot \mathrm{out}(k) \le (n + 1)^2$ pairs, and each update creates $O(1)$ new expression nodes that point to existing labels. Line L8 costs $O(\mathrm{in}(k) + \mathrm{out}(k))$. With the labels kept in hash tables per state, every operation is $O(1)$ expected, or $O(1)$ worst case with arrays of size $n + 2$ per state. So $n$ passes cost $O(n^3)$, and the total is $O(n^3 + t)$. $\square$
