---
title: Bottom-up linked-list merge sort sorts the list stably and stops
proves: [correctness, termination]
status: full
---

Let the input list have $n \ge 1$ nodes. Write $x \prec y$ for "node $x$ came before node $y$ in the input". A sequence of nodes is *stably sorted* when its keys are non-decreasing and nodes with equal keys appear in the order $\prec$.

**Lemma 1 (one merge).** Let lines L6 to L11 start with $p$ at the first node of a stably sorted run $L$ of $a \ge 1$ nodes, followed in the list by a stably sorted run $R$ of $\min(w, r)$ nodes, where $r$ is the number of nodes after $L$, and let each node of $L$ come before each node of $R$ in $\prec$. Then the loop of line L8 appends the nodes of $L$ and $R$ to $tail$, each exactly once, as a stably sorted sequence, and ends with $q$ at the first node after $R$, or nil.

*Proof.* Line L6 walks $a$ nodes, so $q$ is the first node of $R$, and $a = \min(w, n_p)$ where $n_p$ is the number of nodes from $p$ on. Each step of the loop of line L8 takes the first remaining node of $L$ (line L10) or of $R$ (line L9) and appends it (line L11). The counters $a$ and $b$ count the remaining nodes of $L$ and the nodes of $R$ that may still be taken, and $q \ne nil$ says that $R$ has nodes left when $b > 0$. So the loop runs while either run has nodes left, and takes each node once. It takes from $R$ only when $L$ is empty or the head of $R$ has a strictly smaller key than the head of $L$. By induction on the steps, the appended sequence is the stable merge: the node appended is a minimum of the remaining keys, because the heads of the two sorted runs are their minima; and among equal keys a node of $L$ is taken before a node of $R$, which matches $\prec$, while the order inside each run is kept. When both runs are used up, $q$ is the node after $R$. $\square$

**Invariant (B).** At the test of line L2 for width $w$, the list from $head$ holds all $n$ input nodes, linked in a line that ends with nil, and for each $j \ge 0$ the block of nodes at the positions $jw, \ldots, \min((j+1)w, n) - 1$ is stably sorted, and every node of block $j$ comes before every node of block $j+1$ in $\prec$.

*Initialization.* For $w = 1$, each block has one node, and the list is the input list in input order.

*One pass.* The loop of line L4 starts with $p$ at block 0. By Lemma 1, the first merge appends blocks 0 and 1 as a stably sorted sequence, and leaves $q$ at the start of block 2, which line L12 copies to $p$. The next merge handles blocks 2 and 3, and so on, until $p$ is nil. The nodes of different pairs are appended in the order of the pairs, and by (B) all nodes of pair $t$ come before all nodes of pair $t + 1$ in $\prec$. Line L13 ends the new list. So after the pass the list holds all $n$ nodes, and its blocks of $2w$ nodes are the merged pairs, each stably sorted, in the order $\prec$ between blocks. Line L15 sets $w$ to $2w$, so (B) holds at the next test of line L2.

**Termination.** A pass with width $w$ makes $\lceil n / w \rceil / 2$ merges rounded up, that is $\lceil n / 2w \rceil$, because each merge consumes two blocks, or one at the end. This is at most 1 exactly when $n \le 2w$. Since $w$ doubles in each pass, a pass with $2w \ge n$ comes after at most $\lceil \lg n \rceil$ passes, or 1 pass when $n = 1$. Each inner loop stops: line L6 makes at most $w$ steps, the loop of line L8 appends one node per step and there are finitely many, and the loop of line L4 moves $p$ forward past at least one node per merge.

**Correctness at the end.** Line L14 returns after a pass with $merges \le 1$. As $n \ge 1$, it made exactly one merge, of block 0 and block 1 of width $w$, which together hold all $n$ nodes. By Lemma 1 the list from $D.next$ is all $n$ nodes, stably sorted, and line L13 ended it with nil. $\blacksquare$
