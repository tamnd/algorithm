---
title: The number of preferred path changes in a tango tree is the interleave bound
proves: [complexity, competitive-ratio]
status: full
---

Fix the reference tree $P$ and an access sequence $X = x_1, \ldots, x_m$. For a node $y$, list the accesses $x_i$ with $x_i \in I(y)$, the key interval of the subtree of $y$, and label each $L$ if $x_i \le y$ and $R$ otherwise. Let $\mathrm{ib}(y)$ be the number of changes of label along this list, and $\mathrm{IB}(X) = \sum_y \mathrm{ib}(y)$, the interleave bound.

**Lemma 1.** The preferred child of $y$ after access $i$ is left if the last access in $I(y)$ up to time $i$ is labelled $L$, right if it is labelled $R$, and none if there is none.

*Proof.* By [the correctness proof](correctness.md), access $i$ changes the preferred children exactly of the nodes on the root-to-$x_i$ path of $P$, which are the nodes $y$ with $x_i \in I(y)$, and sets them to the side of $x_i$: left for $x_i \le y$ (including $x_i = y$, by line L11), right for $x_i > y$. That is the label of $x_i$ at $y$. $\square$

**Theorem 1.** The number of L-R switches (changes of a preferred child from left to right or from right to left) over the whole sequence is exactly $\mathrm{IB}(X)$.

*Proof.* By Lemma 1, the preferred child of $y$ changes between left and right exactly when two consecutive accesses in $I(y)$ have different labels, which is one change counted in $\mathrm{ib}(y)$. Sum over $y$. $\square$

**Theorem 2.** Access $i$ visits at most $k_i + f_i + 1$ paths, where $k_i$ is its number of L-R switches and $f_i$ the number of nodes that get their first preferred child during access $i$. So the total number of paths visited is at most $\mathrm{IB}(X) + m + n$.

*Proof.* Each path visited after the first is entered from a pair $(u, c)$ of line L6, and $u$ then changes its preferred child: from the other side (an L-R switch) or from none (a first choice). Different pairs have different $u$. A node gets its first preferred child only once. Sum and use Theorem 1. $\square$

**Theorem 3 (cost).** If each auxiliary tree is a red-black tree with depth fields, so that a search, a cut and a join on a path of at most $\lg n + 1$ nodes take $O(\log \log n)$ time, then the total cost is $O((\mathrm{IB}(X) + m + n)(1 + \log \log n))$, and so $O((\mathrm{OPT}(X) + n)(1 + \log \log n))$.

*Proof.* Each visited path costs one search, and each pair $(u, c)$ and line L11 cost one cut and one join, all in trees of $O(\log n)$ nodes. By Theorem 2 the number of these is $O(\mathrm{IB}(X) + m + n)$. Wilber's first lower bound, in the form proved by Demaine, Harmon, Iacono and Pătraşcu, is $\mathrm{OPT}(X) \ge \mathrm{IB}(X)/2 - n$, and $\mathrm{OPT}(X) \ge m$ since each access touches a node. So $\mathrm{IB}(X) + m + n \le 2\,\mathrm{OPT}(X) + 2n + \mathrm{OPT}(X) + n = O(\mathrm{OPT}(X) + n)$. $\blacksquare$

The time bound of a search, cut and join in $O(\log \log n)$ is the part this page does not prove; it is the standard cost of split and concatenate of red-black trees of size $O(\log n)$, with the depth fields used to find the range to cut, as in the paper of Demaine, Harmon, Iacono and Pătraşcu. In the Python code, the search is a binary search on a sorted list, with at most $\lceil \lg(\lg n + 2) \rceil$ comparisons, and the tests check this count; the cut and the join are list slices.
