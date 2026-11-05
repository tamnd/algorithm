---
title: Set Horspool outputs exactly the occurrences of the patterns
proves: [correctness, termination]
status: full
---

**Claim.** For every text $T[0 \ldots n-1]$ and patterns $P_0, \ldots, P_{k-1}$, SET-HORSPOOL stops and outputs each pair $(s, j)$ with $0 \le s \le n - |P_j|$ and $T[s \ldots s + |P_j| - 1] = P_j$ exactly once, and no other pair.

**Notation.** For a string $x$, $x^R$ is its reverse. In the trie of line L3, each node $v$ spells a string $\mathrm{str}(v)$ (the labels read from the root), and $\mathrm{out}[v] = \{ j : P_j \ne \varepsilon,\ P_j^R = \mathrm{str}(v) \}$. A pattern $P_j$ *ends at* $e$ if it occurs at $e - |P_j| + 1$. For a position $e$, let $U_e = T[e]\, T[e-1] \cdots T[0]$ be the text read backward from $e$.

**Lemma 1 (the trie).** A string $u$ is $\mathrm{str}(v)$ for some node $v$ if and only if $u$ is a prefix of $P_j^R$ for some nonempty $P_j$. Each node has at most one child per character.

*Proof.* Line L3 inserts each $P_j^R$ from the root, creating a child only when none exists for the next character. So the nodes are exactly the prefixes of the inserted strings, and children are unique per character. $\square$

**Lemma 2 (one reading).** Fix $\mathrm{pos}$ with $0 \le \mathrm{pos} \le n - 1$. Lines L9 to L12 output exactly the pairs $(\mathrm{pos} - |P_j| + 1, j)$ for the nonempty $P_j$ that end at $\mathrm{pos}$, each once.

*Proof.* Let $g$ be the length of the longest prefix of $U_{\mathrm{pos}}$ that is a node. By Lemma 1 and induction on the iterations of line L10, after $t$ iterations $v$ is the node of $T[\mathrm{pos}] \cdots T[\mathrm{pos} - t + 1]$ and $i = \mathrm{pos} - t$; the loop continues as long as the next prefix is a node and $i \ge 0$, so it makes exactly $g$ iterations. The node reached after $t$ iterations has the string $T[\mathrm{pos} - t + 1 \ldots \mathrm{pos}]^R$, so line L12 outputs $(\mathrm{pos} - t + 1, j)$ for the $j$ with $P_j = T[\mathrm{pos} - t + 1 \ldots \mathrm{pos}]$, that is, the patterns of length $t$ that end at $\mathrm{pos}$.

Conversely, if a nonempty $P_j$ ends at $\mathrm{pos}$, then $P_j^R$ is the prefix of $U_{\mathrm{pos}}$ of length $|P_j|$, and every prefix of it is a node by Lemma 1, so $|P_j| \le g$ and the iteration $t = |P_j|$ outputs $(\mathrm{pos} - |P_j| + 1, j)$. Each $t$ is visited once and each $j$ is in one $\mathrm{out}$ list, so no pair is output twice. $\square$

**Lemma 3 (the table).** After line L6, for every character $c$,
$$d[c] = \min\Big(\{\ell\} \cup \{\delta : 1 \le \delta \le \ell - 1,\ \exists j: P_j \ne \varepsilon,\ P_j[|P_j| - 1 - \delta] = c\}\Big).$$
In particular $1 \le d[c] \le \ell$.

*Proof.* Line L5 sets every entry to $\ell$. Line L6 visits, for each nonempty $P_j$, the indices $i$ from $|P_j| - \ell$ to $|P_j| - 2$, which are exactly the indices $|P_j| - 1 - \delta$ for $\delta$ from $1$ to $\ell - 1$ (all valid, since $|P_j| \ge \ell$), and lowers $d[P_j[i]]$ to $\delta$ when that is smaller. So each entry ends as the minimum of $\ell$ and the distances found. $\square$

**Lemma 4 (safe shift).** For every $\mathrm{pos} \le n - 1$ and every $\delta$ with $1 \le \delta < d[T[\mathrm{pos}]]$, no nonempty pattern ends at $\mathrm{pos} + \delta$.

*Proof.* Suppose $P_j$ ends at $e = \mathrm{pos} + \delta$ with $1 \le \delta < d[T[\mathrm{pos}]]$. By Lemma 3, $\delta < d[T[\mathrm{pos}]] \le \ell \le |P_j|$, so the occurrence $T[e - |P_j| + 1 \ldots e]$ contains $\mathrm{pos}$, at the index $|P_j| - 1 - \delta$ of $P_j$. Hence $P_j[|P_j| - 1 - \delta] = T[\mathrm{pos}]$ with $1 \le \delta \le \ell - 1$, and Lemma 3 gives $d[T[\mathrm{pos}]] \le \delta$, a contradiction. $\square$

**Theorem.** The claim holds.

*Proof.* *Empty patterns.* Line L1 outputs $(s, j)$ for every $s \in \{0, \ldots, n\}$ and every empty $P_j$, which are exactly their occurrences, once each; no later line outputs an empty pattern, since the trie has none. If all patterns are empty, line L2 stops here.

*Termination.* By Lemma 3, each pass of line L13 increases $\mathrm{pos}$ by at least 1, and the inner loop of line L10 runs at most $\mathrm{pos} + 1$ times since $i$ decreases from $\mathrm{pos}$ and must stay $\ge 0$. So the loop of line L8 ends.

*Nonempty patterns.* Let $e_1 < e_2 < \cdots$ be the values of $\mathrm{pos}$ at line L9. A nonempty pattern ends at some $e \ge |P_j| - 1 \ge \ell - 1 = e_1$ with $e \le n - 1$. If $e$ is not one of the $e_t$, there is a $t$ with $e_t < e < e_{t+1} = e_t + d[T[e_t]]$, or $e$ is beyond the last visited value $e_t$, where $e_t + d[T[e_t]] > n - 1 \ge e$; in both cases Lemma 4 with $\mathrm{pos} = e_t$ and $\delta = e - e_t$ says that no pattern ends at $e$. So every end position of a nonempty pattern is visited, each exactly once, and by Lemma 2 the readings at the visited positions output exactly the occurrences that end there, each once. Two different end positions give different pairs, so no pair is output twice. $\blacksquare$
