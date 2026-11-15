---
title: Logarithmic merging keeps all postings, follows a binary counter, and merges each posting at most log2(T/n) times
proves: [correctness, complexity]
status: full
---

Fix the capacity $n \ge 1$. Let $T$ be the number of postings added so far, all distinct, and let $X$ be the set of these postings. Write $T = qn + s$ with $0 \le s < n$, and let $q = \sum_i b_i 2^i$ be the binary form of $q$. An index is a sorted list of postings, and MERGE of two disjoint sorted lists returns the sorted list of their union. We show that after each call of LMERGE-ADD the following holds.

> **(I1)** $Z_0$ holds exactly $s$ postings.
>
> **(I2)** $I_i$ exists if and only if $b_i = 1$, and then $|I_i| = 2^i n$.
>
> **(I3)** $Z_0$ and the indexes $I_i$ that exist are pairwise disjoint, and their union is $X$.

1. **Base.** Before the first call, $T = 0$, $Z_0$ is empty and no $I_i$ exists. All three statements hold.

2. **A call that does not fill $Z_0$.** Suppose the statements hold before the call that adds posting $x$, with $T = qn + s$. Line L1 adds $x$ to $Z_0$. If $s + 1 < n$, the test of line L2 fails and nothing else changes. Now $T + 1 = qn + (s + 1)$, so (I1) holds with $s + 1$, (I2) is unchanged because $q$ is unchanged, and (I3) holds because $x$ is new and is now in $Z_0$.

3. **A call that fills $Z_0$.** Else $s + 1 = n$, so $T + 1 = (q + 1) n$. Let $c$ be the number of trailing 1 bits of $q$, so $b_0 = \cdots = b_{c-1} = 1$ and $b_c = 0$. By (I2), $I_0, \ldots, I_{c-1}$ exist and $I_c$ does not. The loop of lines L4 to L6 keeps the statement

    > **(L)** at the start of a step with index $i$, $|Z| = 2^i n$, the set $Z$ is the union of the old $Z_0$ with $x$ and of $I_0, \ldots, I_{i-1}$, and $I_0, \ldots, I_{i-1}$ no longer exist.

    It holds at $i = 0$ after line L3, since $|Z_0| = n$. If $I_i$ exists, line L5 merges it into $Z$, which gives $|Z| = 2^i n + 2^i n = 2^{i+1} n$, and deletes it. So (L) holds for $i + 1$. The loop runs for $i = 0, \ldots, c-1$ and stops at $i = c$, where $I_c$ does not exist. Line L7 stores $Z$ as $I_c$ with $|I_c| = 2^c n$, and empties $Z_0$. In binary, $q + 1$ has $b_0 = \cdots = b_{c-1} = 0$, $b_c = 1$, and the same higher bits as $q$. The indexes now present are exactly those of the bits of $q + 1$, with the sizes of (I2). $Z_0$ is empty, which is (I1) with $s = 0$. No posting was lost or copied: each merge moves the postings of $I_i$ into $Z$, and $Z$ becomes $I_c$. So (I3) holds.

4. **Queries.** By (I3), the posting list of a term $t$ in $X$ is the union of the lists of $t$ in $Z_0$ and in each $I_i$ that exists, and these lists are disjoint. Lines L8 and L9 return this union in document order, so the query is correct.

5. **Each merge doubles the index that holds a posting.** A posting $p$ starts in $Z_0$, which has $n$ postings when it is first merged. By step 3, $p$ takes part in a merge only at line L5, where it is in $Z$ or in $I_i$, both of size $2^i n$, and the result has size $2^{i+1} n$. After that merge, $p$ is in $Z$ for the rest of the loop and then in $I_c$, of size $2^c n$, and the next merge of $p$, in a later call, again starts from an index of the size that $p$ is in. So after $j$ merges, $p$ is in an index of $2^j n$ postings. That index is a subset of $X$, so $2^j n \le T$, which gives $j \le \log_2(T/n)$. Since $j$ is an integer, $j \le \lfloor \log_2(T/n) \rfloor$ when $T \ge n$, and $j = 0$ when $T < n$.

6. **Total merge work.** In the call that completes the $t$-th flush, $q = t - 1$ before the call, and the number $c$ of trailing 1 bits of $t - 1$ is the number of trailing 0 bits of $t$. The merges of that call write $\sum_{i=0}^{c-1} 2^{i+1} n = (2^{c+1} - 2) n$ postings. Summed over all postings, step 5 bounds the total by $T \lfloor \log_2(T/n) \rfloor$. When $T = 2^m n$, the sum of $(2^{c+1} - 2) n$ over $t = 1, \ldots, 2^m$ is exactly $m 2^m n = T \log_2(T/n)$: each of the $2^m n$ postings is merged exactly $m$ times, since all of them end in the single index $I_m$. $\blacksquare$
