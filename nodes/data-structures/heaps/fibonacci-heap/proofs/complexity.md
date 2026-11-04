---
title: Amortized bounds of the Fibonacci heap and the degree bound
proves: [time.amortized, space]
status: full
---

We use the invariants (S), (O), (M) and (L) of [the correctness proof](correctness.md). Let $F_0 = 0$, $F_1 = 1$ and $F_j = F_{j-1} + F_{j-2}$, and let $\varphi = (1 + \sqrt 5)/2$, so that $\varphi^2 = \varphi + 1$.

## The degree bound

**Lemma 1.** Let $x$ be a node, and let $y_1, \ldots, y_k$ be the children of $x$ in the order in which they were linked to $x$, from the earliest. Then $y_1.degree \ge 0$ and $y_i.degree \ge i - 2$ for $2 \le i \le k$.

*Proof.* The first claim is clear. Let $i \ge 2$. When LINK made $y_i$ a child of $x$, the nodes $y_1, \ldots, y_{i-1}$ were already children of $x$, so $x.degree \ge i - 1$. LINK is called only on two roots of the same degree (line L20 of CONSOLIDATE), so then $y_i.degree \ge i - 1$. Since that link, $y_i$ has stayed a child of $x$, and by (L) it has lost at most one child. A node gains children only by LINK, and only while it is a root, so $y_i$ has gained none. So $y_i.degree \ge i - 2$. $\square$

**Lemma 2.** $F_{k+2} = 1 + \sum_{i=0}^{k} F_i$ and $F_{k+2} \ge \varphi^k$ for each $k \ge 0$.

*Proof.* Both by induction on $k$. For $k = 0$: $F_2 = 1 = 1 + F_0$ and $F_2 = 1 = \varphi^0$. For $k = 1$, $F_3 = 2 \ge \varphi$. For the step, $F_{k+3} = F_{k+2} + F_{k+1} = 1 + \sum_{i=0}^{k} F_i + F_{k+1}$, and $F_{k+3} = F_{k+2} + F_{k+1} \ge \varphi^k + \varphi^{k-1} = \varphi^{k-1}(\varphi + 1) = \varphi^{k+1}$. $\square$

**Lemma 3.** A node of degree $k$ has at least $F_{k+2} \ge \varphi^k$ nodes in its subtree.

*Proof.* We show $\mathrm{size}(x) \ge F_{x.degree + 2}$ for each node $x$, by induction on the height of $x$. A leaf has degree 0 and size $1 = F_2$. Let $x$ have degree $k \ge 1$ and the children $y_1, \ldots, y_k$ as in Lemma 1. Each child has a smaller height than $x$, so the claim holds for it. By this and Lemma 1, the subtree of $y_i$ has at least $F_{y_i.degree + 2} \ge F_i$ nodes for $i \ge 2$, since the Fibonacci numbers do not decrease, and $y_1$ adds at least 1 node. Counting $x$ too,

$$\mathrm{size}(x) \ge 2 + \sum_{i=2}^{k} F_i = 1 + \sum_{i=0}^{k} F_i = F_{k+2},$$

using $F_0 = 0$, $F_1 = 1$ and Lemma 2. The second inequality of the claim is Lemma 2. $\square$

**Corollary.** In a heap of $n \ge 1$ nodes, each degree is at most $D(n) = \lfloor \log_\varphi n \rfloor$.

*Proof.* A node of degree $k$ has $n \ge \varphi^k$ by Lemma 3, so $k \le \log_\varphi n$. $\square$

## The amortized costs

Let $t(H)$ be the number of roots and $m(H)$ the number of marked nodes, and let

$$\Phi(H) = t(H) + 2\,m(H) \ge 0,$$

with $\Phi = 0$ for the empty heap. Scale the unit of work so that each line of the main block that is not a loop, and each iteration of a loop, costs at most 1 unit, and scale $\Phi$ by the same constant $c$. Then for each sequence of operations from the empty heap, the total actual cost is at most the sum of the amortized costs $\hat c = c_{\text{actual}} + \Delta \Phi$, because $\Phi$ starts at 0 and stays non-negative.

**Insert.** $O(1)$ actual work, $\Delta t = 1$, $\Delta m = 0$. So $\hat c = O(1)$.

**Union.** $O(1)$ actual work. The potential of the union is the sum of the two potentials, so $\Delta \Phi = 0$, and $\hat c = O(1)$.

**Find-min.** $O(1)$, with no change.

**Extract-min.** Let $t = t(H)$ before the call. Line L11 adds at most $D(n)$ roots, the children of $z$, and line L12 removes $z$. So CONSOLIDATE starts with at most $t + D(n) - 1$ roots. Each iteration of the loop of line L18 costs $O(1)$ plus $O(1)$ for each LINK, and each LINK removes one root, so there are fewer links than roots. Lines L26 to L30 go over at most $D(n) + 1$ entries of $T$, by the corollary. The actual cost is $O(t + D(n))$. At the end, the roots have pairwise different degrees in $\{0, \ldots, D(n)\}$, so $t(H) \le D(n) + 1$, and no mark is set. So

$$\hat c \le c_1 (t + D(n)) + c\,(D(n) + 1 - t) = O(D(n))$$

when $c \ge c_1$.

**Decrease-key.** Let the call do $q \ge 0$ cuts in total, counting the cut of line L37 and the cuts of line L45. The actual cost is $O(q + 1)$. The $q$ cuts add $q$ roots. Each cut of line L45 removes the mark of a marked node, by line L41, and there are at least $q - 1$ such cuts when $q \ge 1$. At most one mark is set, at line L44. So

$$\Delta \Phi \le c\,\bigl(q + 2\,(1 - (q - 1))\bigr) = c\,(4 - q),$$

and $\hat c \le c_1(q + 1) + c(4 - q) = O(1)$ when $c \ge c_1$. If $q = 0$, the change is 0 and the cost is $O(1)$.

**Delete.** One decrease-key and one extract-min, so $\hat c = O(1) + O(D(n)) = O(D(n))$.

**Theorem.** For each sequence of operations on Fibonacci heaps that starts from empty heaps, the total time is at most $O(1)$ for each insert, find-min, union and decrease-key, plus $O(\log n)$ for each extract-min and delete, where $n$ is the size of the heap at that time. The space is $O(n)$.

*Proof.* By the cases above, the amortized costs are $O(1)$ and $O(D(n))$, and $D(n) \le \log_\varphi n = O(\log n)$ by the corollary. Each node has a fixed number of fields, and the table $T$ has at most $D(n) + 1$ entries. $\blacksquare$
