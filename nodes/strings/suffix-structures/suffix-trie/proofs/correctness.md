---
title: The suffix trie holds exactly the substrings, with their counts and ends
proves: [correctness]
status: full
---

Let $S = S[0 \ldots n-1]$, and write $S_i = S[i \ldots n-1]$. For a node $x$, $str(x)$ is the string spelled by the path from the root to $x$. Edges out of a node carry distinct symbols, because line L5 creates a child for $c$ only when none exists. So for each string $w$ there is at most one node $x$ with $str(x) = w$.

**Lemma (build).** For $0 \le k \le n$, after the passes $i = 0, \ldots, k-1$ of line L2:

1. the strings $str(x)$, over all nodes $x$, are exactly the distinct prefixes of $S_0, \ldots, S_{k-1}$, together with $\varepsilon$;
2. for each node $x \ne root$, $x.count = |\{\, i < k : str(x) \text{ is a prefix of } S_i \,\}|$;
3. for each node $x$, $x.ends$ is the list, in increasing order, of the $i < k$ with $S_i = str(x)$.

*Proof.* By induction on $k$. For $k = 0$, line L1 makes only the root, $str(root) = \varepsilon$, and the claims hold.

Step from $k$ to $k + 1$. The pass $i = k$ starts at the root (line L3). We show by induction on $j$ that before the iteration $j$ of line L4, $x$ is the node of $S[k \ldots j-1]$. This holds for $j = k$. In the iteration $j$, line L5 makes sure that a child for $S[j]$ exists, creating it if the string $S[k \ldots j]$ had no node, and line L6 moves to it, so $x$ becomes the node of $S[k \ldots j]$. Hence the pass visits the nodes of the nonempty prefixes $S[k \ldots j]$, $k \le j \le n-1$, each one time, and adds 1 to each of their counts. The only new nodes are those of prefixes of $S_k$ that were missing, which proves claim 1 for $k + 1$. A node $x \ne root$ gets $+1$ exactly when $str(x)$ is a nonempty prefix of $S_k$, which proves claim 2. After the loop, $x$ is the node of $S_k$ (the root if $S_k$ were empty, which does not happen since $k \le n - 1$), and line L7 appends $k$ to its list. Since $k$ is larger than all earlier positions, the list stays increasing, which proves claim 3. $\square$

**Theorem.** After SUFFIX-TRIE-BUILD$(S)$, the invariants (ST1), (ST2) and (ST3) of the page hold. For each string $P$, FIND$(P)$ returns the node of $P$ if $P$ is a substring of $S$, and NIL otherwise. For a nonempty $P$, the count of that node is the number of occurrences of $P$, and the union of the end lists in its subtree is the set of positions where $P$ occurs.

*Proof.* Apply the lemma with $k = n$.

(ST1). A string $w$ is a substring of $S$ if and only if $w = S[i \ldots j-1]$ for some $0 \le i \le j \le n$. If $i < n$, this is a prefix of $S_i$ with $i \le n-1$. If $i = n$, then $w = \varepsilon$. So the substrings of $S$ are exactly $\varepsilon$ and the prefixes of $S_0, \ldots, S_{n-1}$, and claim 1 says that these are exactly the strings $str(x)$. With the uniqueness shown at the start, $x \mapsto str(x)$ is a bijection.

(ST2). For a nonempty $w$, "$w$ is a prefix of $S_i$" holds if and only if $i + |w| \le n$ and $S[i \ldots i + |w| - 1] = w$, that is, if and only if $w$ occurs at $i$. With claim 2 this gives (ST2).

(ST3). This is claim 3. Each $i < n$ is appended exactly once, in pass $i$.

FIND. The loop of lines L9 to L11 keeps the statement "$x$ is the node of the prefix of $P$ read so far". This holds at line L8, since the root is the node of $\varepsilon$. If the node of the prefix $Pc$ exists, it is the child of $x$ for $c$, because $str(x.next[c]) = str(x)\,c$ and nodes are unique. If no such node exists, then $Pc$ is not a substring by (ST1), so $P$ is not one either (a substring of $S$ has all its prefixes as substrings), and line L11 returns NIL correctly. If the loop ends, line L12 returns the node of $P$.

Occurrences. Let $x$ be the node of a nonempty $P$. A node $y$ is in the subtree of $x$ if and only if $str(x)$ is a prefix of $str(y)$. By (ST3), position $i$ is in the list of the node $y$ with $str(y) = S_i$, so $i$ is collected if and only if $P$ is a prefix of $S_i$, that is, if and only if $P$ occurs at $i$. Each position is in one list, so no position is reported twice. $\blacksquare$
