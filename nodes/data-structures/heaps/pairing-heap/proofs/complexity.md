---
title: Amortized cost of the pairing heap
proves: [time.amortized]
status: full
---

We prove that each operation of the two-pass pairing heap takes $O(\log n)$ amortized time, where $n$ is the largest number of items in the heap during the sequence. The argument is the one of Fredman, Sedgewick, Sleator and Tarjan (1986), with the potential function of the splay tree.

**The potential.** View the tree in the child-sibling form: the left child of a node is its first child, and the right child is its next sibling. For a node $x$, let $s(x)$ be the number of nodes in the binary subtree of $x$ in this form. This is $x$ and its descendants, together with the right siblings of $x$ and their descendants. The root has no siblings, so $s(\mathrm{root})$ is the number of items. Let
$$\Phi = \sum_x \lg s(x).$$
Each term is at least $0$, and the empty heap has $\Phi = 0$. So for any sequence, the sum of the amortized costs, actual cost plus change of $\Phi$, is at least the sum of the actual costs. We count one unit of actual cost per link, plus one unit per operation.

**Lemma 1.** If $x, y > 0$ and $x + y \le 1$, then $\lg x + \lg y \le -2$.

*Proof.* For a fixed sum, the product $xy$ is largest when $x = y$, so $xy \le 1/4$. $\square$

So for positive $p$ and $q$, $\lg p + \lg q \le 2 \lg(p + q) - 2$, by Lemma 1 applied to $p/(p+q)$ and $q/(p+q)$.

**Lemma 2 (a link of two roots).** Let $a$ and $b$ be roots without siblings, of trees with $A$ and $B$ nodes, and let $A + B \le n$. Then $\mathrm{LINK}(a, b)$ raises $\Phi$ by at most $2 \lg n$.

*Proof.* Say $a$ wins. Before the link, $s(a) = A$ and $s(b) = B$. After it, $b$ is the first child of $a$ and its right sibling is the old first child of $a$, so $s(b) = B + A - 1$ and $s(a) = A + B$. The binary subtree of every other node is the same set as before. So the change is $\lg(A + B) + \lg(A + B - 1) - \lg A - \lg B \le 2 \lg n$. $\square$

**Insert and meld.** One link and $O(1)$ other work, so by Lemma 2 the amortized cost is at most $2 \lg n + O(1)$.

**Decrease-key.** Cut the subtree of $x$. After the cut, the binary subtree of $x$ loses the right siblings of $x$, and the binary subtree of each node that contained $x$ loses the nodes of the tree of $x$, or stays the same. No binary subtree grows, so $\Phi$ does not go up. The link with the root adds at most $2 \lg n$ by Lemma 2. The amortized cost is at most $2 \lg n + O(1)$.

**Delete-min.** Let the root $r$ have the children $x_1, \dots, x_k$, left to right, with trees of $t_1, \dots, t_k$ nodes. In the binary form they make a right chain, and $s(x_i) = t_i + t_{i+1} + \dots + t_k$. Write $S_i = s(x_i)$ and $S_{k+1} = 0$. The actual cost is $k + 1$ units at most.

*Removal of the root.* The term $\lg s(r) = \lg n$ goes away and no other binary subtree changes. The change is $-\lg n$.

*First pass.* Consider the link of $x_i$ with $x_{i+1}$ for an odd $i < k$. Let $a = t_i$, $b = t_{i+1}$ and $c = S_{i+2}$, so $S_i = a + b + c$. Before the link, $s(x_i) = a + b + c$ and $s(x_{i+1}) = b + c$. After it, the winner stays in the chain with $s = a + b + c$, and the loser becomes its first child, with the other children of the winner as its right siblings, so $s = a + b - 1$. Nothing else changes. The change is
$$\lg(a + b - 1) - \lg(b + c) \le \lg(a + b) - \lg(b + c).$$
If $c > 0$, then $\lg(b + c) \ge \lg c$, and by Lemma 1 $\lg(a + b) \le 2 \lg(a + b + c) - \lg c - 2$, so the change is at most $2 \lg S_i - 2 \lg S_{i+2} - 2$. If $c = 0$, which happens only for the last pair when $k$ is even, the change is at most $\lg(a + b) \le 2 \lg S_i$. A last tree without a partner does not change $\Phi$. Add over the $\lfloor k/2 \rfloor$ pairs: the terms telescope, and the sum is at most
$$2 \lg S_1 - 2 \lfloor k/2 \rfloor + 2 \le 2 \lg n - 2 \lfloor k/2 \rfloor + 2.$$

*Second pass.* Let the trees of the first pass be $y_1, \dots, y_m$, left to right, with $m = \lceil k/2 \rceil$. The pass keeps a tree $R$ at the right end of the chain and links the tree just to its left into it. Let that tree have $p$ nodes and let $R$ have $q$ nodes. Before the link, the left one has $s = p + q$ and the root of $R$ has $s = q$. After it, the winner has $s = p + q$ and the loser has $s = p + q - 1$. The binary subtrees of the trees further left hold the same nodes as before. The change is $\lg(p + q - 1) - \lg q \le \lg(p + q) - \lg q$. The new $R$ has $p + q$ nodes, so the changes telescope, and the sum over the pass is at most $\lg(n - 1) - \lg q_0 \le \lg n$, where $q_0 \ge 1$ is the size of $y_m$.

*Total.* The amortized cost of delete-min is at most
$$(k + 1) - \lg n + \left(2 \lg n - 2 \lfloor k/2 \rfloor + 2\right) + \lg n = 2 \lg n + k - 2 \lfloor k/2 \rfloor + 3 \le 2 \lg n + 4.$$

**Delete.** The cut does not raise $\Phi$, as for decrease-key. The removal of $x$ removes the term $\lg s(x) \ge 0$. The two passes on the children of $x$ raise $\Phi$ by at most $2 \lg n - 2 \lfloor k/2 \rfloor + 2 + \lg n$, and pay for their $k - 1$ links up to a constant, as above, with $3 \lg n$ in place of $2 \lg n$. The final link adds at most $2 \lg n$. So the amortized cost is $O(\log n)$.

**Conclusion.** Every operation takes $O(\log n)$ amortized time, and find-min takes $O(1)$. Since $\Phi \ge 0$ and $\Phi = 0$ at the start, any sequence of $m$ operations on an initially empty pairing heap takes $O(m \log n)$ time in total. $\blacksquare$
