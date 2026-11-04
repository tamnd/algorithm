---
title: Splay tree operations take O(log n) amortized time
proves: [amortized-time]
status: full
---

**Setting.** Give each node weight 1. For a node $x$ let $s(x)$ be the number of nodes in its subtree and $r(x) = \lg s(x)$. The potential of a tree is $\Phi = \sum_x r(x)$, and of a collection of trees the sum over the trees. Each rank is between 0 and $\lg N$, where $N$ is the largest number of keys at any time. We count the cost of an operation as the number of nodes visited by its searches plus the number of rotations, plus $O(1)$; a search that visits $d + 1$ nodes is followed by a splay of a node at depth $d$, which makes $d$ rotations, so the search costs at most one more than the splay, and it is enough to count rotations plus $O(1)$.

**Access Lemma** (Sleator and Tarjan, Lemma 1; proved in [the complexity proof of splaying](/splaying/proofs/complexity.md)). The amortized number of rotations of a splay of $x$ in a tree with root $t$ is at most $3(r(t) - r(x)) + 1 \le 3 \lg N + 1$.

**Access.** One splay: at most $3 \lg N + 1$ amortized, plus $O(1)$.

**Join.** The splay of $m$ in $L$ costs at most $3 \lg N + 1$ amortized. Then $R$ is hung below $m$. This changes only the rank of $m$, which becomes $\lg(|L| + |R|) \le \lg N$, so the potential grows by at most $\lg N$. The total is $4 \lg N + O(1)$.

**Split.** One access, then one link is cut at the root. Cutting a subtree from the root only lowers the rank of the root, and no other rank changes, so the potential does not grow. The total is $3 \lg N + O(1)$.

**Insert.** One access, at most $3 \lg N + 1$. Then the new node $z$ becomes the root with the old root $r$ below it. The rank of $r$ does not grow (it loses a subtree), no other old rank changes, and $z$ adds $r(z) = \lg(n + 1) \le \lg N$. The total is $4 \lg N + O(1)$.

**Delete.** One access, at most $3 \lg N + 1$. Removing the root removes its rank, which only lowers $\Phi$. Then a join, at most $4 \lg N + O(1)$. The total is $7 \lg N + O(1)$.

**Sequences.** For a sequence of $m$ operations that starts from a tree with $n_0$ keys, the actual cost is the sum of the amortized costs plus $\Phi_0 - \Phi_{\text{end}}$. Since $\Phi \ge 0$ and $\Phi_0 \le n_0 \lg n_0$, the total actual cost is at most $m(7 \lg N + O(1)) + n_0 \lg n_0 = O((m + n_0) \log N)$. So each operation costs $O(\log N)$ amortized. $\blacksquare$

**Remark.** The constant 7 for delete is not tight; it comes from adding the bounds of the parts. Other weight choices in the Access Lemma give the static optimality, static finger and working set theorems.
