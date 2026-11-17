---
title: One stable pass per site gives the prefix and divergence arrays, and the block and scan rules list exactly the long and set-maximal matches
proves: [correctness]
status: full
---

**Setting.** Haplotypes $x_0, \ldots, x_{M-1} \in \{0, 1\}^N$. For $0 \le k \le N$, let $\rho_k(i)$ be the reversed prefix $x_i[k - 1], \ldots, x_i[0]$, a string of length $k$. Then $a_k$ sorts the indices by the key $(\rho_k(i), i)$ in lexicographic order. For $u \ne v$, let $\sigma_k(u, v)$ be the smallest $s$ with $x_u[s, k) = x_v[s, k)$, so the common suffix of $x_u[0, k)$ and $x_v[0, k)$ has length $k - \sigma_k(u, v)$. Then $d_k[r] = \sigma_k(a_k[r - 1], a_k[r])$ for $r \ge 1$, and $d_k[0] = k$.

**Lemma 1 (range minimum of common prefixes).** For rows $r' < r$ of $a_k$, $\sigma_k(a_k[r'], a_k[r]) = \max(d_k[r' + 1], \ldots, d_k[r])$.

*Proof.* The length of the common prefix of $\rho_k(u)$ and $\rho_k(v)$ is $k - \sigma_k(u, v)$. In a list of strings in lexicographic order, the common prefix of two entries is the shortest common prefix of the adjacent pairs between them. If the strings $w_{r'}, \ldots, w_r$ are sorted and all adjacent pairs share the first $\ell$ symbols, then all of them share the first $\ell$ symbols, so the common prefix of $w_{r'}$ and $w_r$ has length at least $\ell$. Conversely, suppose $w_{r'}$ and $w_r$ share the first $\ell + 1$ symbols. Every $w_t$ with $r' \le t \le r$ lies between them in lexicographic order, so it also has those $\ell + 1$ symbols, and every adjacent pair between them shares at least $\ell + 1$ symbols. So the two lengths are equal, and the claim follows by taking $k$ minus each side. Ties in the key, which are equal strings, have common prefix $k$ and fit the same argument. $\square$

**Lemma 2 (the order).** The list of zeros followed by the list of ones at line L8 is $a_{k+1}$.

*Proof.* $\rho_{k+1}(i)$ is $x_i[k]$ followed by $\rho_k(i)$. If $x_u[k] < x_v[k]$, then $u$ comes before $v$ in $a_{k+1}$ by the first symbol, and the pass puts $u$ in the zero list and $v$ in the one list, which comes later. If $x_u[k] = x_v[k]$, the keys $(\rho_{k+1}(u), u)$ and $(\rho_{k+1}(v), v)$ compare as $(\rho_k(u), u)$ and $(\rho_k(v), v)$, that is, in the order of $a_k$. The pass visits the rows in the order $a_k$ and appends to each list at the end, so the relative order in each list is that of $a_k$. $\square$

**Lemma 3 (the divergence).** The value appended with each index at lines L6 and L7 is its entry of $d_{k+1}$.

*Proof.* Take the zero list; the ones are the same with $q$ in place of $p$. Let row $r$ of $a_k$ have $x_{a_k[r]}[k] = 0$.

Case 1: some earlier row has value 0, and $r'$ is the last such row. Then $a_k[r']$ is the neighbor above $a_k[r]$ in $a_{k+1}$, by Lemma 2. Line L6 set $p = 0$ after row $r'$, and lines L5 at rows $r' + 1, \ldots, r$ raised it to $\max(d_k[r' + 1], \ldots, d_k[r])$, since all these values are at least 0. By Lemma 1 this is $\sigma_k(a_k[r'], a_k[r])$. Both haplotypes have 0 at site $k$, so the common suffix grows by one site and the start does not change: $\sigma_{k+1} = \sigma_k$. This is the correct entry of $d_{k+1}$.

Case 2: row $r$ is the first with value 0. The zero list comes first, so $a_k[r]$ is row 0 of $a_{k+1}$, whose entry is $k + 1$ by convention. The value of $p$ is $\max(k + 1, d_k[0], \ldots, d_k[r])$, and every $d_k[t] \le k$, so $p = k + 1$.

For the first row of the one list, the row above it in $a_{k+1}$ is the last row of the zero list. The two differ at site $k$, so the correct entry is $k + 1$. The value of $q$ is $\max(k + 1, \ldots) = k + 1$ for the same reason as in Case 2. For later rows of the one list, Case 1 applies. $\square$

**Theorem 1 (the arrays).** build returns $a_k$ and $d_k$ for all $k = 0, \ldots, N$.

*Proof.* Line L1 gives $a_0 = (0, \ldots, M - 1)$, which sorts the empty prefixes by index, and $d_0 = (0, \ldots, 0)$, which is correct since every $\sigma_0 = 0$ and $d_0[0] = 0 = k$. By induction on $k$, Lemmas 2 and 3 give $a_{k+1}$ and $d_{k+1}$ from $a_k$ and $d_k$. $\square$

**Lemma 4 (ranges).** For a row $r$ of $a_k$ and $s \le k$, the rows $t$ with $\sigma_k(a_k[r], a_k[t]) \le s$ form a contiguous range of rows that contains $r$.

*Proof.* By Lemma 1, for $t > r$ the condition is $\max(d_k[r + 1], \ldots, d_k[t]) \le s$, which holds for $t = r + 1, \ldots$ up to the first row with $d_k > s$ and fails beyond it. The same holds for $t < r$ going up. $\square$

**Theorem 2 (long matches).** long_matches returns the pairs $i < j$ and intervals $[s, e)$ that are maximal matches with $e - s \ge L$.

*Proof.* A maximal match of $x_i$ and $x_j$ on $[s, e)$ ends at $e$, and at site $k = e$ it is the common suffix of $x_i[0, k)$ and $x_j[0, k)$, so $s = \sigma_k(i, j)$, and maximality at the right end means $k = N$ or $x_i[k] \ne x_j[k]$. Maximality at the left end holds for $s = \sigma_k(i, j)$ by the definition of $\sigma$. So the maximal matches ending at $k$ are the pairs with $k = N$ or $x_i[k] \ne x_j[k]$, with $s = \sigma_k(i, j)$. The code cuts $a_k$ into blocks at the rows with $d_k[r] > k - L$. By Lemma 1, two rows are in the same block exactly when $\sigma_k \le k - L$, that is, when the match ending at $k$ has length at least $L$. Within each block the code tests every pair for the right end and computes $s$ with Lemma 1. Every maximal match has one end $e$, so each is found once, at $k = e$. $\square$

**Theorem 3 (set-maximal matches).** set_maximal_matches returns exactly the set-maximal matches.

*Proof.* Fix $k$ and row $r$, with $i = a_k[r]$. The code sets the sentinels $d[0] = d[M] = k + 1$, so the scans stop at the ends. By Lemma 1, the longest common suffix of $x_i[0, k)$ with any other haplotype has start $s^* = \min(d_k[r], d_k[r + 1])$, reached by the row above if $d_k[r] = s^*$ and by the row below if $d_k[r + 1] = s^*$. If $s^* \ge k$, no match of positive length ends at $k$ for $x_i$, and the code skips the row.

A set-maximal match of $x_i$ that ends at $k$ must be a longest match of $x_i$ ending at $k$: if a match $[s, k)$ of $x_i$ to $x_j$ is maximal but some match of $x_i$ ending at $k$ starts before $s$, that match covers $[s, k)$ and is longer. So it starts at $s^*$. By Lemma 4, the haplotypes $j$ with $\sigma_k(i, j) = s^*$ are the rows of a contiguous range around $r$, and the scans find this range: up while $d \le d_k[r] = s^*$ and down while $d \le d_k[r + 1] = s^*$, each scan done only on the side that reaches $s^*$.

Now the match $[s^*, k)$ of $x_i$ to such a $j$ is maximal if and only if $k = N$ or $x_i[k] \ne x_j[k]$. If some $j$ in the range has $x_j[k] = x_i[k]$, then $x_i$ has a match to $j$ on $[s^*, k + 1)$ or longer, which covers $[s^*, k)$ for every $j'$ in the range and is longer, so none of them is set-maximal. The code then reports nothing. If no $j$ in the range has $x_j[k] = x_i[k]$, then each match $[s^*, k)$ is maximal. No match of $x_i$ covers $[s^*, k)$ and is longer: such a match would start at or before $s^*$ and end after $k$, or start before $s^*$ and end at $k$. The second kind does not exist by the choice of $s^*$. The first kind would be to some $j$ with $\sigma_k(i, j) \le s^*$, so $\sigma_k(i, j) = s^*$ and $j$ is in the range, with $x_j[k] = x_i[k]$, which we excluded. So the code reports exactly the set-maximal matches of $x_i$ ending at $k$, and taking all $k$ and $r$ gives all of them. $\square$

**Complexity.** Each call of step visits the $M$ rows once with $O(1)$ work, so build costs $O(NM)$. In set_maximal_matches, each scan step either stops or adds a reported pair, except for at most two steps per row, so the cost is $O(NM)$ plus the number of reported pairs. The reference functions sort, compare and test all pairs, and serve only to check these results.
