---
title: The deepest node with both marks spells a longest common substring
proves: [correctness]
status: full
---

Let $S = A \# B \$$ with $\#, \$ \notin \Sigma$ and $\# \ne \$$, and let $a = \lvert A \rvert$. The suffix of $S$ at position $p$ is an $A$-suffix if $p \le a$ and a $B$-suffix if $p > a$. We use these facts about the suffix tree of $S$: since $\$$ occurs only at the end, no suffix is a prefix of another, so each suffix is the path label of exactly one leaf; for each node $v$, the leaves below $v$ are the suffixes that have $label(v)$ as a prefix; and every string that is a prefix of some suffix ends either at a node or inside an edge, and in the second case the leaves below that point are those below the lower end of the edge.

**Lemma 1 (marks).** After line L5, $mark(v)$ is the set of kinds of the suffixes that have $label(v)$ as a prefix.

*Proof.* By induction in postorder. A leaf gets the kind of its own suffix at line L4. An inner node gets the union over its children, and the leaves below $v$ are the union of the leaves below its children. $\square$

**Lemma 2 (common prefixes stay inside the strings).** Let $X$ be a common prefix of an $A$-suffix $S[p ..]$ and a $B$-suffix $S[q ..]$, with $X \neq \varepsilon$. Then $p + \lvert X \rvert \le a$ and $X = A[p .. p + \lvert X \rvert - 1] = B[q - a - 1 .. q - a - 2 + \lvert X \rvert]$, so $X$ is a common substring of $A$ and $B$.

*Proof.* The $B$-suffix $S[q ..]$ contains no $\#$, and its only $\$$ is its last symbol. If $X$ contained $\#$, so would the $B$-suffix, which is impossible. If $X$ contained $\$$, then $\$$ would be the last symbol of the $B$-suffix's prefix $X$, so $X$ would be the whole $B$-suffix; but $X$ is also a prefix of the $A$-suffix, in which $\$$ occurs only at the end after a $\#$ (or, if $p = a$, the $A$-suffix starts with $\#$, and then the first symbols already differ, since $S[q] \ne \#$). In both cases $X$ would contain $\#$, which was excluded. So $X$ lies in $\Sigma^*$. Since the $A$-suffix has its first symbol outside $\Sigma$ at position $a$, the prefix $X$ ends before it: $p + \lvert X \rvert \le a$. Likewise, $X$ ends before the $\$$ of the $B$-suffix. $\square$

**Lemma 3 (every common substring is seen).** If $X \neq \varepsilon$ occurs in $A$ at $i$ and in $B$ at $j$, then there is a node $v$ with $mark(v) = \{A, B\}$ and $depth(v) \ge \lvert X \rvert$.

*Proof.* The $A$-suffix at $i$ and the $B$-suffix at $a + 1 + j$ both start with $X$. Let $v$ be the node where $X$ ends, or the lower end of the edge inside which $X$ ends. Its label has $X$ as a prefix, so $depth(v) \ge \lvert X \rvert$, and the leaves below $v$ are the suffixes that start with $label(v)$. Because $X$ ends at $v$ or inside the edge into $v$, every suffix that starts with $X$ continues along that edge and so starts with $label(v)$: both leaves are below $v$, and by Lemma 1, $mark(v) = \{A, B\}$. $\square$

**Theorem.** Line L7 returns $(\ell, i, j)$ where $\ell$ is the length of a longest common substring of $A$ and $B$, and $A[i .. i + \ell - 1] = B[j .. j + \ell - 1]$.

*Proof.* If $v \ne$ root has $mark(v) = \{A, B\}$, then $v$ is an inner node (a leaf has one kind), and by Lemma 1 some $A$-suffix $S[p ..]$ and some $B$-suffix $S[q ..]$ have $label(v)$ as a prefix. By Lemma 2, $label(v)$ is a common substring, found at $p$ in $A$ and at $q - a - 1$ in $B$; these are the positions that line L7 reports for $v^*$. So $best \le \ell^*$, the length of a longest common substring. If $\ell^* > 0$, Lemma 3 applied to a longest common substring gives a node with both marks and depth at least $\ell^*$, so $best \ge \ell^*$. Line L6 keeps the maximum of $depth$ over all such nodes, since the walk visits every node, so $best = \ell^*$. If $\ell^* = 0$, Lemma 2 shows that no node other than the root has both marks, because its label would be a nonempty common substring. The root has depth 0, and line L6 does not choose it since $best$ starts at 0, so line L7 returns $(0, 0, 0)$. $\blacksquare$
