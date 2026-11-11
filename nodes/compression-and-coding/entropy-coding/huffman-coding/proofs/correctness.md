---
title: Huffman's algorithm builds an optimal prefix code, within one bit of the entropy
proves: [correctness]
status: full
---

**Setup.** The input is $n \ge 1$ symbols with weights $w_1, \ldots, w_n \ge 0$. A code tree $T$ is a binary tree whose leaves are the symbols. The depth $d_T(i)$ of leaf $i$ is the length of its codeword, and the cost of $T$ is $B(T) = \sum_i w_i\, d_T(i)$. Prefix codes and code trees are the same thing (see [prefix code](/prefix-code/)), so an optimal prefix code is a code tree of minimum cost. A tree is *full* if each inner node has two children. For $n \ge 2$, each instance has a full optimal tree: if an inner node has one child, replace the node by that child; no depth grows and the tree stays a code tree.

**Lemma 1 (greedy choice).** Let $n \ge 2$, and let $x$ and $y$ be two symbols with $w_x \le w_y \le w_i$ for each other symbol $i$. Then some optimal tree has $x$ and $y$ as sibling leaves at the largest depth of the tree.

*Proof.* Take a full optimal tree $T$ and let $D$ be its largest leaf depth. Let $u$ be a leaf at depth $D$. Its parent has a second child $v$. If $v$ were an inner node, $v$ would have a leaf below it at depth more than $D$, which is not possible. So $u$ and $v$ are two sibling leaves at depth $D$.

If two leaves of a tree swap their symbols, a symbol $s$ of weight $w_s$ moves from depth $d_s$ to depth $d_t$ and a symbol $t$ moves the other way. The cost changes by
$$ w_s d_t + w_t d_s - w_s d_s - w_t d_t = (w_s - w_t)(d_t - d_s). $$
This is at most $0$ when $w_s \le w_t$ and $d_t \ge d_s$: a swap that moves a lighter symbol deeper does not increase the cost.

Step 1. If $x$ is not at $u$, swap $x$ with the symbol $c$ at $u$. Here $w_x \le w_c$ and $D \ge d_T(x)$, so the cost does not grow. Step 2. Now $x$ is at $u$. If $y$ is not at $v$, swap $y$ with the symbol $c'$ at $v$. Here $c' \ne x$, so $w_y \le w_{c'}$, and $D \ge d(y)$, so the cost does not grow. The new tree has cost at most $B(T)$, so it is optimal, and $x$ and $y$ are siblings at depth $D$. $\square$

**Lemma 2 (merge).** Let $T$ be a code tree in which $x$ and $y$ are sibling leaves. Let $T'$ be the tree in which their parent is a leaf for a new symbol $z$ with $w_z = w_x + w_y$, and the other symbols are as before. Then $B(T) = B(T') + w_x + w_y$.

*Proof.* The other leaves have the same depth in both trees. In $T$, $d_T(x) = d_T(y) = d_{T'}(z) + 1$. So $w_x d_T(x) + w_y d_T(y) = (w_x + w_y)\, d_{T'}(z) + w_x + w_y = w_z d_{T'}(z) + w_x + w_y$. $\square$

**Theorem.** For every rule that breaks ties in the priority queue, HUFFMAN returns a code tree of minimum cost.

*Proof.* By induction on $n$. For $n = 1$, the loop of line L3 does not run and line L9 returns the single leaf. It is the only code tree, so it is optimal.

Let $n \ge 2$ and assume the theorem for $n - 1$ symbols. Lines L4 and L5 of the first iteration extract two items $x$ and $y$ of smallest weight, so $w_x \le w_y \le w_i$ for each other symbol $i$. After lines L6 to L8, the queue holds the $n - 2$ other symbols and the new item $z$ with weight $w_x + w_y$. From this point the algorithm does exactly what HUFFMAN does on the $n - 1$ symbols in the queue, with $z$ seen as one symbol. By the induction hypothesis, that run builds an optimal tree $T'$ for those $n - 1$ symbols, and the returned tree $T$ is $T'$ with the leaf $z$ replaced by the node with children $x$ and $y$. By Lemma 2, $B(T) = B(T') + w_x + w_y$.

Now let $S$ be an optimal tree for the $n$ symbols. By Lemma 1 we can take $S$ with $x$ and $y$ as siblings. Merge them as in Lemma 2, which gives a tree $S'$ for the $n - 1$ symbols with $B(S) = B(S') + w_x + w_y$. Since $T'$ is optimal, $B(S') \ge B(T')$. So $B(S) \ge B(T') + w_x + w_y = B(T)$, and $T$ is optimal. $\blacksquare$

**Theorem (entropy bounds).** Let $p_1, \ldots, p_n > 0$ with $\sum p_i = 1$, and let $L = \sum p_i l_i$ be the expected length of the Huffman code. Then $H \le L < H + 1$, where $H = -\sum p_i \log_2 p_i$.

*Proof.* Lower bound. The lengths of each prefix code satisfy the [Kraft inequality](/kraft-inequality/) $\sum 2^{-l_i} \le 1$. Since $\log_2$ is concave, Jensen's inequality gives
$$ H - L = \sum_i p_i \log_2 \frac{2^{-l_i}}{p_i} \le \log_2 \sum_i p_i \frac{2^{-l_i}}{p_i} = \log_2 \sum_i 2^{-l_i} \le 0. $$
Upper bound. Let $s_i = \lceil -\log_2 p_i \rceil$. Then $2^{-s_i} \le p_i$, so $\sum 2^{-s_i} \le 1$, and by the Kraft inequality a prefix code with lengths $s_i$ exists. Its expected length is $\sum p_i s_i < \sum p_i(-\log_2 p_i + 1) = H + 1$, because $\lceil t \rceil < t + 1$. The Huffman code is optimal by the first theorem, so $L \le \sum p_i s_i < H + 1$. $\blacksquare$
