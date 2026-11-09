---
title: Binary search tree range search reports exactly the keys in the range, in order, and enters at most k + 2h nodes
proves: [correctness, termination, complexity]
status: full
---

**Setting.** $T$ is a binary search tree of height $h$ (the number of nodes on a longest root-to-leaf path) that holds a multiset $P$ of $n$ keys and obeys the order rule: for every node $x$, every key in the left subtree of $x$ is $< x.key$, and every key in the right subtree is $\ge x.key$. A query is a pair of keys $lo, hi$. Write $T_x$ for the subtree of $x$ and $\mathrm{ino}(T_x)$ for the in-order sequence of its keys.

**Claim.** RANGE-SEARCH$(\mathit{root}, lo, hi)$ terminates and outputs the subsequence of $\mathrm{ino}(T)$ formed by the keys $y$ with $lo \le y \le hi$. It enters at most $k + 2h$ nodes, where $k$ is the length of the output.

**Step 1 (each call outputs the filtered in-order sequence of its subtree).** We show by induction on the height of $T_x$ that RANGE-SEARCH$(x, lo, hi)$ outputs $F(T_x)$, the subsequence of $\mathrm{ino}(T_x)$ of keys in $[lo, hi]$.

If $x = \mathrm{nil}$, line L1 returns with no output, and $F$ of the empty tree is empty.

Otherwise $\mathrm{ino}(T_x) = \mathrm{ino}(T_{x.left}), x.key, \mathrm{ino}(T_{x.right})$, so $F(T_x) = F(T_{x.left}), [x.key \text{ if } lo \le x.key \le hi], F(T_{x.right})$.

- If $lo < x.key$, line L3 outputs $F(T_{x.left})$ by induction. If $lo \ge x.key$, every key $y$ of the left subtree has $y < x.key \le lo$, so $F(T_{x.left})$ is empty, and skipping it outputs the same thing.
- Lines L4 and L5 output $x.key$ exactly when $lo \le x.key \le hi$.
- If $x.key \le hi$, line L7 outputs $F(T_{x.right})$ by induction. If $x.key > hi$, every key $y$ of the right subtree has $y \ge x.key > hi$, so $F(T_{x.right})$ is empty.

The three parts come out in this order, so the call outputs $F(T_x)$. Applied to the root, the output is the keys of $P$ in $[lo, hi]$, in in-order, which is non-decreasing by the order rule, with each copy of a key once.

**Step 2 (termination).** Each call either returns at line L1 or makes at most two calls on children, whose subtrees are smaller. So the recursion is finite. The iterative code pushes each node at most once as a start frame and once as a resume frame, and each nil child once.

**Step 3 (entered nodes off the answer lie on two search paths).** Define the search path $\pi(lo)$ as the sequence of nodes from the root that goes to the left child at a node $y$ if $lo < y.key$ and to the right child otherwise, until it reaches nil. Define $\pi(hi)$ the same way with $hi$ in place of $lo$. Each path has at most $h$ nodes.

Let $x$ be a node that the search enters and does not report, so $x.key < lo$ or $x.key > hi$.

*Case $x.key < lo$.* Let $y$ be a proper ancestor of $x$; the search entered $y$ and then the child of $y$ toward $x$. If $x$ lies in the left subtree of $y$, line L2 was taken, so $lo < y.key$, and $\pi(lo)$ also goes left at $y$. If $x$ lies in the right subtree of $y$, then $y.key \le x.key < lo$, so $lo \not< y.key$ and $\pi(lo)$ also goes right at $y$. By induction from the root, $\pi(lo)$ follows the path from the root to $x$, so $x \in \pi(lo)$.

*Case $x.key > hi$.* If $x$ lies in the left subtree of an ancestor $y$, then $hi < x.key < y.key$, so $\pi(hi)$ goes left at $y$. If $x$ lies in the right subtree of $y$, line L6 was taken, so $y.key \le hi$, that is $hi \not< y.key$, and $\pi(hi)$ goes right at $y$. So $x \in \pi(hi)$.

**Step 4 (the count).** Every entered node is reported (at most $k$ such nodes, since each reported node is reported once) or lies on $\pi(lo) \cup \pi(hi)$ (at most $2h$ nodes). So at most $k + 2h$ nodes are entered. Each entered node makes at most two calls on children, so the number of calls, nil calls included, is at most $1 + 2(k + 2h)$, and each call does $O(1)$ work besides its children. The time is $O(h + k)$ and the stack depth is at most $h + 1$. $\blacksquare$
