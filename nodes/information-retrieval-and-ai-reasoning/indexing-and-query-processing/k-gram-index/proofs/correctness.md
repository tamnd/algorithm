---
title: The k-gram index with its postfilter returns exactly the terms that match a wildcard query
proves: [correctness]
status: full
---

Fix $k \ge 1$. A term is a nonempty string without the characters \$ and \*. For a string $s$, the $k$-grams of $s$ are its substrings of length $k$. The padded form of a term $t$ is $\$t\$$. A query $q$ is a string without \$, in which each \* stands for any string, also the empty one. Write $q = P_0 * P_1 * \cdots * P_r$, with pieces $P_i$ that contain no \*, and $r \ge 0$ the number of stars. A term $t$ *matches* $q$ if $t = P_0 S_1 P_1 S_2 \cdots S_r P_r$ for some strings $S_1, \ldots, S_r$. The answer to $q$ over a vocabulary $V$ is $A(q) = \{t \in V : t \text{ matches } q\}$.

**Invariant (I).** The array $terms$ is the vocabulary $V$ in increasing order without repeats, and for every string $g$: if $g$ is a $k$-gram of $\$t\$$ for some $t \in V$, then $postings[g]$ is the sorted list, without repeats, of all such $t$; otherwise $g$ has no list.

**Lemma 1.** The constructor makes (I) true, and INSERT and DELETE keep it.

*Proof.* The empty index has $V = \emptyset$, no terms and no lists, so (I) holds. INSERT of a term $t$ already in $V$ stops at line L8 and changes nothing. Otherwise line L9 puts $t$ at its sorted place in $terms$, and line L10 takes each distinct $k$-gram $g$ of $\$t\$$ once and inserts $t$ at its sorted place in the list of $g$, creating the list if needed. Since $t$ was not in $V$, it was in no list, so each of these lists stays sorted and without repeats and is now the list of all terms of $V \cup \{t\}$ whose padded form contains $g$. The lists of other grams do not change, and $t$ does not contain those grams. So (I) holds for $V \cup \{t\}$.

DELETE of a term not in $V$ does nothing. Otherwise it removes $t$ from $terms$ and, for each distinct $k$-gram $g$ of $\$t\$$, removes $t$ from the list of $g$, which contains $t$ by (I). A list that becomes empty is removed, because no term of $V \setminus \{t\}$ has that gram. Other lists do not contain $t$. So (I) holds for $V \setminus \{t\}$. $\square$

**Lemma 2 (the candidates contain the answer).** Let $G(q)$ be the set of $k$-grams of the strings $\$P_0, P_1, \ldots, P_{r-1}, P_r\$$ (for $r = 0$, the single string $\$P_0\$$), as line L1 computes it. If $t$ matches $q$, then every $g \in G(q)$ is a $k$-gram of $\$t\$$.

*Proof.* If $t = P_0 S_1 P_1 \cdots S_r P_r$, then $\$t\$ = \$P_0 \cdot S_1 \cdot P_1 \cdots S_r \cdot P_r\$$, so each of the strings $\$P_0$, $P_1$, ..., $P_r\$$ is a substring of $\$t\$$. A $k$-gram of a substring of $\$t\$$ is a $k$-gram of $\$t\$$. $\square$

By (I), a term is in the list of $g$ exactly when $g$ is a $k$-gram of its padded form. So after line L3, the candidate list $C$ is the sorted list of the terms $t \in V$ such that every gram of $G(q)$ is a gram of $\$t\$$: the merge of sorted lists keeps exactly the common elements, in order, and the order of the merges does not change the result. When $G(q)$ is empty, line L2 sets $C = V$. In both cases Lemma 2 gives $A(q) \subseteq C$.

The inclusion can be strict. For $k = 3$ and $q$ = red\*, the gram set is $\{\$re, red\}$, and the term retired contains both grams but does not start with red. So the postfilter of line L6 is needed.

**Lemma 3 (the postfilter).** MATCHES$(t, q)$ returns true if and only if $t$ matches $q$.

*Proof.* For $r = 0$ the term matches exactly when $t = P_0$, which is the test of the code. Let $r \ge 1$. If $t$ matches $q$, then $t$ starts with $P_0$, ends with $P_r$, and these two parts do not overlap, so $|P_0| + |P_r| \le |t|$; and the middle pieces $P_1, \ldots, P_{r-1}$ occur in this order, without overlap, inside the window $W = t[|P_0| .. |t| - |P_r|)$. The code tests the first three facts directly. It remains to show that the greedy search of the middle pieces succeeds exactly when such an occurrence in order exists.

If the greedy search succeeds, it has found $P_1, \ldots, P_{r-1}$ inside $W$, each one starting at or after the end of the one before. Let the strings $S_i$ be the gaps between consecutive pieces; then $t = P_0 S_1 P_1 \cdots S_r P_r$, so $t$ matches $q$.

Conversely, let the pieces occur in order in $W$ at the positions $a_1 \le \cdots$, with $a_{i+1} \ge a_i + |P_i|$. Let $g_i$ be the position where the greedy search finds $P_i$. We show $g_i \le a_i$ by induction on $i$. For $i = 1$, the search starts at the start of $W$, and $P_1$ occurs at $a_1$, so the leftmost occurrence is at $g_1 \le a_1$. If $g_i \le a_i$, the search for $P_{i+1}$ starts at $g_i + |P_i| \le a_i + |P_i| \le a_{i+1}$, and $P_{i+1}$ occurs at $a_{i+1}$ inside $W$, so the search finds an occurrence at $g_{i+1} \le a_{i+1}$. So the greedy search never fails, and the code returns true. $\square$

**Theorem.** If (I) holds, WILDCARD$(q)$ returns $A(q)$ in increasing order.

*Proof.* By Lemma 1 the index satisfies (I) after any sequence of operations. By Lemma 2 and the remark after it, the list $C$ of lines L2 and L3 is sorted and contains $A(q)$, and every element of $C$ is in $V$. Lines L4 to L6 keep, in the order of $C$, exactly the elements $t$ for which MATCHES$(t, q)$ is true, which by Lemma 3 are the elements of $C$ that match $q$. Since $A(q) \subseteq C \subseteq V$, these are exactly the elements of $A(q)$, in increasing order. $\blacksquare$
