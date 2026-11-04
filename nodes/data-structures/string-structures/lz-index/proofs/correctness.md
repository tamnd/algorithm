---
title: The LZ-index reports every occurrence once, by the number of phrases it touches
proves: [correctness]
status: full
---

We use the pseudocode, the notation and the invariant (Z1) to (Z3) of the page. Let $T' = T\$$, and for a position $q$ of $T'$, let $ph(q)$ be the phrase that contains it. An occurrence of $P$ at $s$ occupies $T'[s \ldots s + m - 1]$; since $P$ has no $\$$, it lies inside $T$. It *touches* the phrases $ph(s), \ldots, ph(s + m - 1)$. We show that the three parts of SEARCH report exactly the occurrences that touch one, two, and at least three phrases, each once, and nothing else.

**Lemma 1 (prefix closure).** Every prefix of a phrase is a phrase, and the LZTrie node of $B_k$ is an ancestor of the node of $B_j$ exactly when $B_k$ is a prefix of $B_j$.

*Proof.* By (Z1) each phrase is an earlier phrase plus one symbol, so by induction its prefixes are phrases. In a trie, the node of $u$ is an ancestor of the node of $w$ exactly when $u$ is a prefix of $w$. $\square$

**One phrase (line L3).** *Soundness.* Line L3 takes a phrase $B_k$ ending with $P$, which is what the RevTrie subtree of $P^r$ holds by (Z2), and a phrase $B_j$ with $B_k$ as a prefix, by Lemma 1. Then $B_j[\lvert B_k \rvert - m \ldots \lvert B_k \rvert - 1] = P$, so $P$ occurs at $start(j) + \lvert B_k \rvert - m$ by (Z3), inside $B_j$. *Completeness.* If $P$ occurs inside $B_j$, ending at offset $e$, then $B_j[0 \ldots e]$ is a phrase $B_k$ by Lemma 1, it ends with $P$, and it is a prefix of $B_j$, so line L3 reports the occurrence with $\lvert B_k \rvert = e + 1$. *Uniqueness.* For a fixed $j$, different $k$ are different prefixes of $B_j$, of different lengths, and give different positions.

**Two phrases (lines L4 and L5).** *Soundness.* For a cut $i$, a reported pair has $B_j$ ending with $P[0 \ldots i - 1]$ and $B_{j+1}$ starting with $P[i \ldots]$. Since $B_j$ ends at $start(j + 1) - 1$, the occurrence at $start(j + 1) - i$ touches exactly $B_j$ and $B_{j+1}$. *Completeness.* An occurrence at $s$ that touches exactly $B_j$ and $B_{j+1}$ has $i = start(j + 1) - s$ symbols in $B_j$, with $1 \le i \le m - 1$; then $B_j$ ends with $P[0 \ldots i - 1]$ and $B_{j+1}$ starts with $P[i \ldots]$, so the pair is reported for this $i$. *Uniqueness.* The cut $i$ is the distance from $s$ to the phrase boundary inside the occurrence, so it is determined by the occurrence.

**At least three phrases (lines L6 and L7).** Let an occurrence at $s$ touch $B_a, \ldots, B_b$ with $b \ge a + 2$. Then $B_{a+1}$ lies wholly inside it, starting at $i = start(a + 1) - s \ge 1$ and ending before the end of the occurrence, so $B_{a+1} = P[i \ldots d - 1]$ with $d < m$, and $i \le m - 2$. *Completeness.* For this $i$, the walk of line L6 along $P[i \ldots]$ meets the node of $B_{a+1}$ at depth $d - i$, since by Lemma 1 all its prefixes are nodes; with $k = a + 1$, $B_{k-1}$ ends with $P[0 \ldots i - 1]$ and the following phrases spell a string that starts with $P[d \ldots]$, so line L7 reports $start(k) - i = s$. *Soundness.* If line L7 reports $start(k) - i$, then $P[0 \ldots i - 1]$ is a suffix of $B_{k-1}$, $P[i \ldots d - 1] = B_k$, and $P[d \ldots]$ is a prefix of $B_{k+1} B_{k+2} \cdots$, so $P$ occurs there; it starts inside $B_{k-1}$ and ends after $B_k$, so it touches at least three phrases. *Uniqueness.* For a given occurrence, $B_{k}$ must be the first phrase that starts inside it after its first position, so $k = a + 1$ and $i$ are determined.

The three parts cover the occurrences that touch one, two, and at least three phrases, which are all the occurrences, and these classes are disjoint. So SEARCH reports each occurrence exactly once. $\blacksquare$
