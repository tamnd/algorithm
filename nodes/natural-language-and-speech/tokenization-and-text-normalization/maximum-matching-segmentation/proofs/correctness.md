---
title: Forward maximum matching cuts the string into longest matches and stops
proves: [correctness, termination]
status: full
---

Let $s = s[0 \ldots n)$ be a string and $D$ a finite set of nonempty strings, stored in a trie $T$: each node of $T$ is a string, the root is the empty string, the child of node $u$ for the character $c$ is $uc$, and a node is marked as a word end exactly when it is in $D$. The trie holds every prefix of every word of $D$ and nothing else. For $0 \le i < n$ let $M(i) = \max\{ j : i < j \le n,\ s[i \ldots j) \in D \}$ if this set is not empty, and $M(i) = i + 1$ otherwise. The span $s[i \ldots j)$ covers the characters $i+1$ to $j$ in 1-based counting.

The claim is that MAX-MATCH returns the list $w_1, \ldots, w_r$ defined by $p_0 = 0$, $p_t = M(p_{t-1})$ and $w_t = s[p_{t-1} \ldots p_t)$, where $r$ is the first index with $p_r = n$.

**Lemma 1.** Each run of lines L3 to L6 with $0 \le i < n$ ends with $j = M(i)$.

*Proof.* We show this invariant at the test of line L4: $v$ is the trie node $s[i \ldots k)$, and $j = \max(\{ i + 1 \} \cup \{ k' : i < k' \le k,\ s[i \ldots k') \in D \})$. At line L3, $k = i$ and $v$ is the root, the empty string $s[i \ldots i)$, and the set of $k'$ is empty, so $j = i + 1$. If the test succeeds, then $v$ has a child for $s[k]$, so $s[i \ldots k+1)$ is a node, and line L5 moves $v$ to it and adds 1 to $k$. Line L6 sets $j \leftarrow k$ exactly when the new node is in $D$. The new $k$ is at least $i + 1$ and larger than every older $k'$, so the maximum is right again. The loop stops when $k = n$ or when $s[i \ldots k+1)$ is not a node. In the second case, no word of $D$ has the prefix $s[i \ldots k+1)$, so no $s[i \ldots k')$ with $k' > k$ is in $D$. In both cases the set of $k'$ in the invariant is the full set $\{ k' : i < k' \le n,\ s[i \ldots k') \in D \}$. If this set is empty, $j = i + 1 = M(i)$. If it is not empty, its maximum is at least $i + 1$, so $j$ is this maximum, which is $M(i)$. $\square$

**Lemma 2 (invariant of the outer loop).** At each test of line L2, the list $W$ is $w_1, \ldots, w_t$ and $i = p_t$ for some $t \ge 0$, and the concatenation of $W$ is $s[0 \ldots i)$.

*Proof.* At line L1, $t = 0$, $W$ is empty, $i = 0 = p_0$, and $s[0 \ldots 0)$ is empty. If the test passes, then $i = p_t < n$, and by Lemma 1, $j = M(p_t) = p_{t+1}$. Line L7 appends $s[p_t \ldots p_{t+1}) = w_{t+1}$, and line L8 sets $i = p_{t+1}$. The concatenation grows from $s[0 \ldots p_t)$ to $s[0 \ldots p_{t+1})$. $\square$

**Termination.** $M(i) \ge i + 1$, so $i$ grows by at least 1 in each pass of the outer loop, and $i \le n$ because $M(i) \le n$. The outer loop runs at most $n$ times. The inner loop runs at most $n - i$ times, because $k$ grows by 1 in each pass and stops at $n$.

**Theorem.** MAX-MATCH$(s, T)$ stops and returns $w_1, \ldots, w_r$. Their concatenation is $s$, each $w_t$ is the longest word of $D$ that starts at $p_{t-1}$, and $w_t$ is one character only when $D$ has no word that starts at $p_{t-1}$ or when the longest such word has one character.

*Proof.* By termination the loop ends, and then $i = n$, because $i < n$ keeps the loop going and $i \le n$. By Lemma 2 with $i = p_t = n$, $t = r$, the output is $w_1, \ldots, w_r$ and its concatenation is $s[0 \ldots n) = s$. The statement about each $w_t$ is the definition of $M$. $\blacksquare$

**Remark.** The theorem says that each word is a longest match at its own start, not that the list has the fewest words or the highest probability. For $D = \{a, ab, bcd, c, d\}$ and $s = abcd$, the algorithm returns $ab, c, d$, but $a, bcd$ has two words. The dynamic program over positions on the word-segmentation page finds a segmentation with the fewest words, or with the highest unigram probability.
