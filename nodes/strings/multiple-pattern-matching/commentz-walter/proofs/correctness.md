---
title: Commentz-Walter outputs exactly the occurrences of the patterns
proves: [correctness, termination]
status: full
---

**Claim.** For every text $T[0 \ldots n-1]$ and patterns $P_0, \ldots, P_{k-1}$, COMMENTZ-WALTER stops and outputs each pair $(s, j)$ with $0 \le s \le n - |P_j|$ and $T[s \ldots s + |P_j| - 1] = P_j$ exactly once, and no other pair.

**Notation.** A *pattern suffix* is a suffix of a nonempty pattern, the empty string included. Each node $v$ of the trie of line L3 stands for a pattern suffix $y(v)$: the labels on the path from the root to $v$ spell $y(v)$ backward, and $d(v) = |y(v)|$. A child $u$ of $v$ by the character $c$ has $y(u) = c\, y(v)$. The list $\mathrm{out}[v]$ holds the $j$ with $P_j = y(v)$, and $v$ is a *pattern node* if this list is not empty. The failure link $\mathrm{fail}(v)$, for $v \ne$ root, is the node of the longest proper prefix of $y(v)$ that is a pattern suffix; it is the Aho-Corasick failure link in the trie of the reversed patterns. The *chain* of $v'$ is the sequence $\mathrm{fail}(v'), \mathrm{fail}(\mathrm{fail}(v')), \ldots$, down to the root. A pattern $P$ *ends at* $e$ if it occurs at $e - |P| + 1$. Let $w$ be the shortest nonempty pattern length.

**Lemma 1 (the trie).** Every pattern suffix is $y(v)$ for exactly one node $v$, and every suffix of a pattern suffix is a pattern suffix.

*Proof.* The trie of the reversed nonempty patterns has one node for each prefix of a reversed pattern, that is, for each reversed pattern suffix. A suffix of a suffix of $P$ is a suffix of $P$. $\square$

**Lemma 2 (the reading).** Fix a window end $\mathrm{pos}$. Lines L9 to L12 visit the nodes $v_t$ with $y(v_t) = T[\mathrm{pos} - t + 1 \ldots \mathrm{pos}]$ for $t = 0, 1, \ldots, D$, where $D$ is the largest $t \le \mathrm{pos} + 1$ for which $T[\mathrm{pos} - t + 1 \ldots \mathrm{pos}]$ is a pattern suffix. They output $(\mathrm{pos} - |P_j| + 1, j)$ for exactly the nonempty patterns $P_j$ that end at $\mathrm{pos}$, each once.

*Proof.* By induction on $t$: at $t = 0$ the node is the root, with $y = \varepsilon$. If the node is $v_t$ and $i = \mathrm{pos} - t \ge 0$, then $v_t$ has a child for $T[i]$ if and only if $T[i]\, y(v_t) = T[i \ldots \mathrm{pos}]$ is a pattern suffix (Lemma 1), and that child is $v_{t+1}$. By Lemma 1 the strings $T[\mathrm{pos} - t + 1 \ldots \mathrm{pos}]$ that are pattern suffixes are exactly those with $t \le D$, so the loop visits $v_0, \ldots, v_D$ and stops. At $v_t$, $t \ge 1$, line L12 outputs $(i + 1, j) = (\mathrm{pos} - t + 1, j)$ for each $j$ with $P_j = T[\mathrm{pos} - t + 1 \ldots \mathrm{pos}]$. A nonempty $P_j$ ends at $\mathrm{pos}$ if and only if $|P_j| \le \mathrm{pos} + 1$ and $P_j = T[\mathrm{pos} - |P_j| + 1 \ldots \mathrm{pos}]$; then this string is a pattern suffix, so $|P_j| \le D$, and $P_j$ is reported at $t = |P_j|$, at that visit only. $\square$

**Lemma 3 (chains).** A node $v$ is on the chain of $v'$ if and only if $y(v)$ is a proper prefix of $y(v')$.

*Proof.* Each step of the chain goes to a proper prefix, and a proper prefix of a prefix is a prefix, so every chain node spells a proper prefix of $y(v')$. Conversely, let $x$ be a proper prefix of $y(v')$ that is a pattern suffix. We use induction on $d(v')$. By definition $|y(\mathrm{fail}(v'))| \ge |x|$. If they are equal, $x = y(\mathrm{fail}(v'))$. Otherwise $x$ is a proper prefix of $y(\mathrm{fail}(v'))$, because both are prefixes of $y(v')$, and by induction $x$ is spelled by a node on the chain of $\mathrm{fail}(v')$, which is part of the chain of $v'$. $\square$

So, for a node $v$, the nodes $v'$ whose chain contains $v$ are the pattern suffixes $y(v)\, x$ with $|x| = d(v') - d(v) \ge 1$.

**Lemma 4 (the tables).** After lines L4 to L6:

1. $\mathrm{char}(c) = \min(\{w + 1\} \cup \{1 + e : c = P_j[|P_j| - 1 - e] \text{ for some } j \text{ and } 0 \le e < |P_j|\})$.
2. $\mathrm{shift1}(v) = \min(\{w\} \cup \{|x| : |x| \ge 1 \text{ and } y(v)\, x \text{ is a pattern suffix}\})$.
3. $\mathrm{shift2}(v) = \min(\{w\} \cup \{|P_j| - i : 1 \le i < |P_j| \text{ and } P_j[0 \ldots i-1] \text{ is a suffix of } y(v)\})$.

*Proof.* (1) A node $u$ entered by $c$ has $y(u) = c\, y(\mathrm{parent}(u))$, so $c$ occurs in a pattern at distance $e = d(u) - 1$ from its end, and $d(u) = 1 + e$. Conversely, an occurrence of $c$ at distance $e$ from the end of $P_j$ gives the pattern suffix $c\, P_j[|P_j| - e \ldots |P_j| - 1]$, whose node is entered by $c$ and has depth $1 + e$.

(2) By Lemma 3 and the remark after it, the set in (2) is $\{d(v') - d(v) : v \text{ is on the chain of } v'\}$. Line L5 takes the minimum over the $v'$ with $\mathrm{fail}(v') = v$ only. This loses nothing: if $v$ is on the chain of $v'$, the chain node $u$ just before $v$ (or $u = v'$) has $\mathrm{fail}(u) = v$ and $d(u) \le d(v')$.

(3) Let $g(v)$ be the minimum of $d(v') - d(v)$ over the pattern nodes $v'$ whose chain contains $v$ ($\infty$ if none). By Lemma 3 this is the minimum of $|x| \ge 1$ such that $y(v)\, x$ is a pattern. The pass in decreasing depth computes it: for such a $v'$, let $u$ be the chain node just before $v$ (or $u = v'$), so $\mathrm{fail}(u) = v$. If $u = v'$, $u$ passes $d(u) - d(v)$, which is at most the value of $u$ as a pattern node. If $u \ne v'$, then $u$ is on the chain of $v'$, so $d(v') - d(u) \ge g(u)$, and $u$ passes at most $g(u) + d(u) - d(v) \le d(v') - d(v)$. Conversely each value passed is $d(v') - d(v)$ for some pattern node $v'$ whose chain contains $v$. Every node that passes to $u$ is deeper than $u$, so $g(u)$ is final when $u$ passes it on.

Now the set in (3) for the root has no element, since $i \ge 1$, so $\mathrm{shift2}(\mathrm{root}) = w$. For $v \ne$ root with parent $q$, $y(v) = c\, y(q)$. A suffix of $y(v)$ of length $i \ge 1$ is $y(v)$ itself or a suffix of $y(q)$. The terms with $i = d(v)$ are those with $P_j = y(v)\, x$, $|x| = |P_j| - i \ge 1$, whose minimum is $g(v)$. The terms with $i < d(v)$ form the set for $q$. So the minimum is $\min(\mathrm{shift2}(q), g(v))$, which line L6 computes from the root down. $\square$

**Lemma 5 (safe shift).** Let the reading at $\mathrm{pos}$ stop at $v$ with $i = \mathrm{pos} - d(v)$, and let $c$ be as in line L13. Then $\sigma = \min(\max(\mathrm{shift1}(v), \mathrm{char}(c) - d(v) - 1), \mathrm{shift2}(v)) \ge 1$, and no nonempty pattern ends at any $e$ with $\mathrm{pos} < e < \mathrm{pos} + \sigma$.

*Proof.* Each element of the sets in Lemma 4 (2) and (3) is at least 1, and $w \ge 1$, so $\mathrm{shift1}(v) \ge 1$ and $\mathrm{shift2}(v) \ge 1$, and $\sigma \ge 1$. Let a nonempty pattern $P$ end at $e = \mathrm{pos} + \delta$ with $\delta \ge 1$, and let $s = e - |P| + 1$ be its start. By Lemma 2, $y(v) = T[i + 1 \ldots \mathrm{pos}]$. We show $\delta \ge \sigma$.

*Case A: $s \le i$.* Then $i \ge s \ge 0$, and the reading stopped because $v$ has no child for $c = T[i]$. The occurrence contains $T[i \ldots e]$, so $y(v)\, x$ with $x = T[\mathrm{pos} + 1 \ldots e]$ is a suffix of $P$, and $|x| = \delta \ge 1$. By Lemma 4 (2), $\delta \ge \mathrm{shift1}(v)$. Also $c = T[i]$ occurs in $P$ at distance $e - i = \delta + d(v)$ from its end, so by Lemma 4 (1), $\mathrm{char}(c) \le 1 + \delta + d(v)$, that is, $\delta \ge \mathrm{char}(c) - d(v) - 1$. So $\delta \ge \max(\mathrm{shift1}(v), \mathrm{char}(c) - d(v) - 1) \ge \sigma$.

*Case B: $i < s \le \mathrm{pos}$.* Let $i' = \mathrm{pos} - s + 1$. Then $1 \le i' \le d(v)$, and $i' < |P|$ because $e > \mathrm{pos}$. The prefix $P[0 \ldots i' - 1] = T[s \ldots \mathrm{pos}]$ is a suffix of $y(v)$, and $|P| - i' = e - \mathrm{pos} = \delta$. By Lemma 4 (3), $\delta \ge \mathrm{shift2}(v) \ge \sigma$.

*Case C: $s > \mathrm{pos}$.* Then $\delta = e - \mathrm{pos} \ge e - s + 1 = |P| \ge w \ge \mathrm{shift2}(v) \ge \sigma$.

The cases cover all $s$. When $i < 0$, case A cannot occur because $s \ge 0$, so the value given to $c$ in line L13 does not matter. $\square$

**Theorem.** The claim holds.

*Proof.* Line L1 outputs the pairs of the empty patterns, each $(s, j)$ with $0 \le s \le n$ once, which are exactly their occurrences. If no pattern is nonempty, line L2 stops and the output is complete. Otherwise let $\mathrm{pos}_0 = w - 1 < \mathrm{pos}_1 < \cdots$ be the window ends of line L8; they increase by at least 1 (Lemma 5), so there are at most $n - w + 1$ of them, and each inner loop stops because $i$ decreases. So the algorithm stops. A nonempty pattern $P$ ends at some $e$ only if $w - 1 \le |P| - 1 \le e \le n - 1$. By Lemma 5, no end lies strictly between two consecutive window ends, and none lies between the last window end $\le n - 1$ and $n - 1$, because the next window end is above $n - 1$. So every $e$ at which a nonempty pattern ends is a window end, and by Lemma 2 the reading at $e$ outputs every pair $(s, j)$ with $P_j$ ending at $e$. Each window end is visited once and each reading outputs each such pair once, and no reading outputs anything else, so each pair is output exactly once and no other pair is output. $\blacksquare$
