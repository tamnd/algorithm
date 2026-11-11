---
title: Columnar transposition decrypts correctly, keeps the letters, and multiple anagramming returns one chain
proves: [correctness]
status: full
---

Let the plaintext be $t_0 \cdots t_{n-1}$ and let $\pi = (\pi_0, \ldots, \pi_{k-1})$ be the column order of line L1, a permutation of $\{0, \ldots, k-1\}$ with $k \ge 1$. Column $c$ is the sequence $t_c, t_{c+k}, t_{c+2k}, \ldots$ of the positions $i < n$ with $i \equiv c \pmod k$.

**Claim 1.** Column $c$ has $\ell_c = \lfloor n/k \rfloor + [c < n \bmod k]$ letters.

*Proof.* Write $n = qk + s$ with $0 \le s < k$. The positions $c, c + k, \ldots, c + (q-1)k$ are all less than $qk \le n$, which gives $q$ letters. The next position $c + qk$ is less than $n$ exactly when $c < s$, and the position after it is at least $c + (q+1)k \ge n$. $\square$

**Claim 2.** Encryption is a bijection from the plaintext positions to the ciphertext positions. So the ciphertext has the letter counts of the plaintext.

*Proof.* The columns partition $\{0, \ldots, n-1\}$ by the residue modulo $k$, and lines L2 and L3 output each column once, because $\pi$ lists each column once. So each position is output exactly once, and the ciphertext has $\sum_c \ell_c = n$ letters. A bijection of positions keeps the multiset of letters. $\square$

**Claim 3.** Decryption with the same key returns the plaintext.

*Proof.* By Claim 2 the ciphertext is the concatenation of column $\pi_0$, column $\pi_1$, and so on, with column $\pi_j$ of length $\ell_{\pi_j}$. Decryption knows $n$ and $\pi$, so by Claim 1 it knows each $\ell_{\pi_j}$, and it cuts the ciphertext at the offsets $\sum_{j' < j} \ell_{\pi_{j'}}$. The piece number $j$ is then exactly column $\pi_j$, in its order from top to bottom, and decryption stores it as column $\pi_j$. Position $i$ of the plaintext is entry $\lfloor i/k \rfloor$ of column $i \bmod k$, and decryption reads exactly this entry for each $i$ from $0$ to $n - 1$. Double transposition applies two such bijections, and decryption inverts the second one and then the first one. $\square$

**Claim 4.** BREAK-COLUMNAR returns an order $\pi$ whose decryption has the largest score among all $k!$ orders.

*Proof.* Lines L6 to L8 visit every permutation of $k$ elements once, and line L8 keeps the best one seen so far. After the loop, the kept order has a score at least that of every visited order. $\square$

This claim is about the search only. Whether the best order is the true key depends on the score and the length of the text, not on the search.

**Claim 5.** MULTIPLE-ANAGRAM returns a list in which each of the $n$ positions appears exactly once.

*Proof.* Call the kept links the edges of a directed graph on $\{0, \ldots, n-1\}$. Line L12 keeps a link $i \to j$ only when $i$ has no outgoing edge and $j$ has no incoming edge, so every node has at most one outgoing and at most one incoming edge. It also rejects a link that closes a cycle. A graph with these two properties is a disjoint union of directed paths, and each node is on exactly one path (a path may be a single node). This holds after every step.

Suppose the loop ends with $p \ge 2$ paths. Take two of them, $A$ with first node $a$ and last node $x$, and $B$ with first node $b$ and last node $y$. The link $x \to b$ is one of the pairs of line L11, since $x \ne b$. When the loop reached it, $x$ had no outgoing edge and $b$ had no incoming edge, because edges are never removed and they still have none at the end. Also $x$ and $b$ were on different paths, because they are at the end, and paths only merge. So $x \to b$ closed no cycle and line L12 kept it, which contradicts that $x$ has no outgoing edge at the end. So the loop ends with one path, which has $n$ nodes and $n - 1$ edges.

Line L13 starts at the only node with no incoming edge, which is the first node of this path, and follows the edges to its end, so it lists all $n$ positions, each one once. $\square$

Claims 1 to 3 prove that the cipher is correct and keeps the letter counts, Claim 4 that the search is exhaustive, and Claim 5 that multiple anagramming always returns an arrangement of all the positions. $\blacksquare$
