---
title: NEXT-Z lists all t-ary trees in lexicographic order, in constant amortized time
proves: [correctness]
status: full
---

Fix $t \ge 2$ and $n \ge 0$. Let $b_i = t(i - 1) + 1$ for $i \ge 1$, and let $Z_n$ be the set of integer sequences $z = (z_1, \ldots, z_n)$ with $z_1 < z_2 < \cdots < z_n$, $z_1 \ge 1$ and $z_i \le b_i$ for all $i$. Let $F_n = |Z_n|$.

A *preorder word* is the word over $\{1, 0\}$ obtained from an extended $t$-ary tree by writing $1$ for each internal node and $0$ for each leaf, in preorder. For a word $w = w_1 \cdots w_m$ let $c_0 = 1$ and $c_k = c_{k-1} + (t - 1)$ if $w_k = 1$ and $c_k = c_{k-1} - 1$ if $w_k = 0$.

**Lemma 1 (preorder words).** A word $w$ of length $m \ge 1$ is a preorder word if and only if $c_k \ge 1$ for $0 \le k < m$ and $c_m = 0$.

*Proof.* By induction on $m$. If $w_1 = 0$, then $c_1 = 0$, so the condition holds only for $w = 0$, which is the preorder word of the tree that is a single leaf. If $w_1 = 1$, then $c_1 = t$. Suppose $w$ satisfies the condition. The counter moves down by $1$ at a time, so for $s = 1, \ldots, t$ there is a first index $k_s$ with $c_{k_s} = t - s$, and $1 = k_0 < k_1 < \cdots < k_t = m$. Between $k_{s-1}$ and $k_s$ the counter stays at least $t - s + 1$, so the piece $w_{k_{s-1}+1} \cdots w_{k_s}$, with its own counter started at $1$, satisfies the condition. By induction each piece is a preorder word, and $w$ is the preorder word of the tree whose root has these $t$ subtrees. Conversely, if $w = 1\, u_1 \cdots u_t$ for preorder words $u_s$, then by induction the counter falls from $t - s + 1$ to $t - s$ across $u_s$ and stays at least $t - s + 1$ before the end of $u_s$; so it is at least $1$ before the end of $w$ and $0$ at the end. $\square$

For a tree with $n$ internal nodes, the counter ends at $0 = 1 + (t - 1)n - \ell$, so the tree has $\ell = (t - 1)n + 1$ leaves and $tn + 1$ nodes. The *z-sequence* of the tree is the list of the positions of the $1$s in its preorder word, in increasing order.

**Lemma 2 (valid sequences).** A sequence of $n$ distinct positions in $\{1, \ldots, tn + 1\}$, in increasing order, is the z-sequence of a $t$-ary tree if and only if it lies in $Z_n$. So the z-sequence is a bijection from the $t$-ary trees with $n$ internal nodes to $Z_n$.

*Proof.* Let $w$ be the word of length $tn + 1$ with $1$s exactly at $z_1, \ldots, z_n$. It has $n$ ones and $(t-1)n + 1$ zeros, so $c_{tn+1} = 0$. The counter only falls at a $0$, so over $0 \le k < tn + 1$ it takes its smallest values at the indices $k = z_i - 1$, just before a $1$, and at $k = tn$, the last index before the end. At $k = tn$ the next symbol is the last one, and since $c_{tn+1} = 0$ the counter is $1$ if that symbol is $0$. If the last symbol is $1$, then $z_n = tn + 1 > b_n$ and also $c_{tn} = -(t-1) < 1$, so both sides of the claim fail. Otherwise, before the $i$-th $1$ the prefix has $i - 1$ ones and $z_i - i$ zeros, so $c_{z_i - 1} = 1 + (t-1)(i-1) - (z_i - i) = b_i + 1 - z_i$, and $c_{z_i - 1} \ge 1$ if and only if $z_i \le b_i$. By Lemma 1, $w$ is a preorder word if and only if $z \in Z_n$. The preorder word determines the tree, so the map is one to one. $\square$

In particular $z_1 = 1$ for every $z \in Z_n$ with $n \ge 1$, the smallest element of $Z_n$ in lexicographic order is $\alpha = (1, 2, \ldots, n)$, since $z_i \ge i$ for every increasing sequence of positive integers and $i \le b_i$, and the largest is $\omega = (b_1, \ldots, b_n)$.

**Lemma 3 (successor).** Let $z \in Z_n$. If $z = \omega$, NEXT-Z returns LAST and does not change $z$. Otherwise it changes $z$ into the smallest element of $Z_n$ that is larger than $z$ in lexicographic order.

*Proof.* Lines L1 and L2 stop with $j = \max\{i : z_i \ne b_i\}$, or $j = 0$ if there is no such $i$, that is, if $z = \omega$; then line L3 returns LAST. Let $j \ge 1$. Since $z_i \le b_i$, we have $z_j < b_j$, and $z_i = b_i$ for $i > j$. Let $z'$ be the sequence after lines L4 and L5: $z'_i = z_i$ for $i < j$, $z'_j = z_j + 1$, and $z'_i = z'_j + (i - j)$ for $i > j$.

*$z' \in Z_n$.* It is increasing, $z'_1 \ge 1$, $z'_j \le b_j$, and for $i > j$, $z'_i \le b_j + (i - j) \le b_j + t(i - j) = b_i$.

*$z'$ is the successor.* Clearly $z' > z$. Let $y \in Z_n$ with $y > z$, and let $k$ be the first index with $y_k \ne z_k$, so $y_k > z_k$. If $k > j$, then $y_k > z_k = b_k$, which is impossible. If $k < j$, then $y$ and $z'$ agree before $k$ and $y_k > z_k = z'_k$, so $y > z'$. If $k = j$, then $y_j \ge z_j + 1 = z'_j$. If $y_j > z'_j$ then $y > z'$. If $y_j = z'_j$, then for $i > j$, by induction, $y_i \ge y_{i-1} + 1 \ge z'_{i-1} + 1 = z'_i$, so $y \ge z'$. In all cases $y \ge z'$. $\square$

**Lemma 4 (the order of the words).** For $y, z \in Z_n$ with $z < y$ in lexicographic order, the preorder word of $z$ is smaller than the preorder word of $y$ in the lexicographic order in which $1$ comes before $0$.

*Proof.* Let $k$ be the first index with $z_k \ne y_k$, so $z_k < y_k$. Both words have $1$s at $z_1, \ldots, z_{k-1}$, and no other $1$ before $z_k$, because the other entries of $z$ are at least $z_k$ and those of $y$ are at least $y_k > z_k$. At position $z_k$ the word of $z$ has $1$ and the word of $y$ has $0$. $\square$

For $t = 2$, dropping the last symbol, which is always $0$, and writing $\texttt{(}$ for $1$ and $\texttt{)}$ for $0$ gives the Dyck word, so the trees come in the lexicographic order of their Dyck words with $\texttt{(} < \texttt{)}$.

**Lemma 5 (amortized cost).** For $z \in Z_n$ let $r(z) = n - j$, the number of entries that line L2 skips. Then $\sum_{z \in Z_n} r(z) \le F_n$ for $n \ge 1$.

*Proof.* For $1 \le k \le n$, $r(z) \ge k$ means $z_i = b_i$ for $i > n - k$. The prefix $(z_1, \ldots, z_{n-k})$ then lies in $Z_{n-k}$, and conversely every $u \in Z_{n-k}$ followed by $b_{n-k+1}, \ldots, b_n$ lies in $Z_n$, since $u_{n-k} \le b_{n-k} < b_{n-k+1}$. So $\#\{z : r(z) \ge k\} = F_{n-k}$, and
$$\sum_{z \in Z_n} r(z) = \sum_{k=1}^{n} F_{n-k} = F_0 + F_1 + \cdots + F_{n-1}.$$
Next, $F_{m+1} \ge 2F_m$ for $m \ge 1$: each $u \in Z_m$ extends to $(u, u_m + 1)$ and to $(u, b_{m+1})$, both in $Z_{m+1}$, and they are different because $u_m + 1 \le b_m + 1 = tm - t + 2 < tm + 1 = b_{m+1}$. Different $u$ give different extensions. Now $F_0 = 1 = F_1$, and if $F_0 + \cdots + F_{m-1} \le F_m$ for some $m \ge 1$, then $F_0 + \cdots + F_m \le 2F_m \le F_{m+1}$. By induction the claim holds for all $n \ge 1$. $\square$

**Theorem.** Starting from $\alpha = (1, \ldots, n)$ and calling NEXT-Z until it returns LAST visits every $t$-ary tree with $n$ internal nodes exactly once, in lexicographic order of the z-sequences, which for $t = 2$ is the lexicographic order of the Dyck words with $\texttt{(} < \texttt{)}$. The total time is $O(F_n)$, so the time per tree is $O(1)$ amortized.

*Proof.* By Lemma 3, each call moves from an element of $Z_n$ to its successor, starting at the smallest element $\alpha$, and the loop stops after visiting the largest element $\omega$. So every element of $Z_n$ is visited once, in increasing order, and by Lemma 2 these are the z-sequences of all trees, each once. Lemma 4 gives the order of the words. A call on $z$ does $r(z) + 1$ tests in line L2 and $r(z)$ writes in line L5, plus $O(1)$ other work, so all $F_n$ calls take $O\big(F_n + \sum_z r(z)\big) = O(F_n)$ time by Lemma 5. For $n = 0$, the list is the single empty sequence and the first call returns LAST. $\blacksquare$
