---
title: The tables of the de Bruijn graph are correct, and walks spell exactly the strings whose K-mers are edges
proves: [correctness, termination]
status: full
---

**Notation.** $\Sigma$ is a finite alphabet, $K \ge 2$, and indices are 0-based. For a multiset $X$ of words of length $K$, $\#_X(x)$ is the number of copies of $x$ in $X$. The graph $G_K(X)$ has a vertex for each word $x[0..K-2]$ and $x[1..K-1]$ with $x \in X$, and an edge $x[0..K-2] \to x[1..K-1]$ labeled $x$ for each distinct $x \in X$, with multiplicity $\#_X(x)$. An absent key of a table counts as 0.

**Invariant.** After the calls ADD-KMER$(x_1), \ldots,$ ADD-KMER$(x_r)$, with $X = \{x_1, \ldots, x_r\}$ as a multiset:

- **(T1)** for every word $u$ of length $K - 1$ and letter $c$, $\mathrm{out}[u][c] = \#_X(u\,c)$;
- **(T2)** for every word $v$ of length $K - 1$ and letter $a$, $\mathrm{in}[v][a] = \#_X(a\,v)$;
- **(T3)** the keys of $\mathrm{out}$ and of $\mathrm{in}$ are both the vertex set of $G_K(X)$.

*Proof.* For $r = 0$ all tables are empty, $X$ is empty and $G_K(X)$ has no vertex. Suppose the invariant holds for $X$ and let $x$ be added, $X' = X + \{x\}$. Line L1 sets $u = x[0..K-2]$ and $v = x[1..K-1]$. Line L2 adds $u$ and $v$ as keys of both tables, which are the two vertices that $x$ adds to $G_K(X')$; no other key is added. Line L3 increases $\mathrm{out}[u][x[K-1]]$ by one, and $u\,x[K-1] = x$, so (T1) holds for the pair $(u, x[K-1])$; any other pair $(u', c)$ has $u'c \ne x$, so $\#_{X'}(u'c) = \#_X(u'c)$ and its entry is unchanged. Line L4 does the same for (T2), since $x[0]\,v = x$. $\square$

**ADD-READ.** Line L5 calls ADD-KMER on $r[i..i+K-1]$ for $0 \le i \le |r| - K$, which are the $K$-mers of $r$, each occurrence once. If $|r| < K$, the range is empty. So after adding a set of reads, $X$ is the multiset of all their $K$-mers.

**SUCCESSORS and PREDECESSORS.** An edge leaves $u$ exactly for the distinct $x \in X$ with $x[0..K-2] = u$, that is, $x = u\,c$ with $\#_X(u\,c) > 0$, and it goes to $x[1..K-1] = u[1..K-2]\,c$. By (T1), these letters $c$ are the keys of $\mathrm{out}[u]$ with positive count, which are all its keys, since counts only grow from 1. Line L6 returns these vertices. The same argument with (T2) gives line L7: an edge enters $v$ from $a\,v[0..K-3]$ exactly when $a\,v \in X$.

**Spelling lemma.** Let $v_0, \ldots, v_w$ be words of length $K - 1$ such that $v_t[0..K-3] = v_{t-1}[1..K-2]$ for $1 \le t \le w$, and let $s$ be the output of lines L8 to L10. Then

1. $|s| = K - 1 + w$ and $s[t..t+K-2] = v_t$ for $0 \le t \le w$;
2. for $1 \le t \le w$, the $K$-mer $s[t-1..t+K-2]$ is $v_{t-1}$ followed by the last letter of $v_t$, which is the label of an edge $v_{t-1} \to v_t$ if one exists.

*Proof.* Item 1 by induction on $t$. For $t = 0$, $s$ starts with $v_0$. Suppose $s[t-1..t+K-3] = v_{t-1}$. The letter appended for $t$ is at index $t + K - 2$ and equals $v_t[K-2]$. The letters at $t, \ldots, t + K - 3$ are $v_{t-1}[1..K-2] = v_t[0..K-3]$. So $s[t..t+K-2] = v_t$. Each step appends one letter, which gives the length. For item 2, $s[t-1..t+K-2]$ is $s[t-1..t+K-3] = v_{t-1}$ followed by $s[t+K-2] = v_t[K-2]$. An edge $v_{t-1} \to v_t$ has label $v_{t-1}\,c$ with $v_{t-1}[1..K-2]\,c = v_t$, so $c = v_t[K-2]$. $\square$

**Converse.** If $s$ is a string of length $L \ge K$ whose $K$-mers all lie in $X$, then $v_t = s[t..t+K-2]$ for $0 \le t \le L - K + 1$ is a walk, since $s[t-1..t+K-2]$ is an edge from $v_{t-1}$ to $v_t$, and SPELL returns $s$ by item 1 of the lemma.

**Consequence.** If a walk uses each edge of $G_K(X)$ exactly once, then by item 2 the $K$-mers of its spelled string are the labels of the edges in the order of the walk, so they are the distinct $K$-mers of $X$, each exactly once.

**Termination.** Each operation is straight-line code or a loop over a finite range: line L5 runs $\max(0, |r| - K + 1)$ times, lines L6 and L7 run once per key, at most $\sigma$ keys, and line L9 runs $w$ times. $\blacksquare$
