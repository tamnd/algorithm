---
title: The degree dynamic program is optimal, and a graph that Supergraph returns adds the fewest edges
proves: [correctness]
status: full
---

Let $d(1) \ge \cdots \ge d(n)$ be the sorted degrees of a simple graph $G$ and let $1 \le k \le n$. A vector is k-anonymous if each of its values occurs at least $k$ times. Let $OPT$ be the least $L_1(\hat d - d) = \sum_i (\hat d(i) - d(i))$ over all k-anonymous $\hat d$ with $\hat d \ge d$. Write $I(a, b) = \sum_{\ell = a}^{b} (d(a) - d(\ell))$.

**Claim 1 (runs).** Some optimal $\hat d$ cuts the positions $1, \ldots, n$ into runs $(t_0, t_1], (t_1, t_2], \ldots$ of consecutive positions, each of length at least $k$ and at most $2k - 1$ (or a single run when $n < 2k$), and sets every position of a run $(t, i]$ to $d(t + 1)$. Its cost is the sum of $I(t + 1, i)$ over the runs.

*Proof.* Take any k-anonymous $\hat d \ge d$ and group the positions by the value of $\hat d$. Each group has at least $k$ positions. Replacing the value of a group by the largest $d$ in it keeps $\hat d \ge d$, keeps the groups, and does not raise the cost, so assume this. Now sort the groups by value. If a group with value $x$ holds a position $j$ and a group with a smaller value $y$ holds a position $j' < j$, then $d(j') \ge d(j)$, and $y \ge d(j') \ge d(j)$. Swap the two positions between the groups: position $j'$ now gets $x \ge y \ge d(j')$ and $j$ gets $y \ge d(j)$, so $\hat d \ge d$ still holds, the group sizes do not change, and the cost changes by $(x - d(j')) + (y - d(j)) - (x - d(j)) - (y - d(j')) = 0$. Repeat until each group holds consecutive positions; each swap moves a position of a larger value to the left, so this ends. Each group is then a run $(t, i]$, and after the replacement above its value is $d(t + 1)$, its largest degree.

A run $(t, i]$ with $i - t \ge 2k$ splits into $(t, t + k]$ and $(t + k, i]$, both of length at least $k$. The second part gets the value $d(t + k + 1) \le d(t + 1)$, which still is at least each $d(\ell)$ in it and costs no more. So some optimal $\hat d$ has all runs shorter than $2k$, except a single run when $n < 2k$ makes two runs impossible. $\square$

**Claim 2 (the recursion).** After line L4 for position $i \ge k$, $DA(i)$ is the least cost of cutting $1, \ldots, i$ into runs as in Claim 1.

*Proof.* By induction on $i$. If $k \le i < 2k$, the prefix cannot hold two runs of at least $k$, so the only cut is one run, of cost $I(1, i)$, which line L3 sets. If $i \ge 2k$, the last run $(t, i]$ has $k \le i - t \le 2k - 1$, so $i - 2k + 1 \le t \le i - k$; it is not the only run, since a single run would be $2k$ or longer, so the runs before it cover $1, \ldots, t$ with $t \ge k$. Their least cost is $DA(t)$ by induction. Line L4 takes the minimum of $DA(t) + I(t + 1, i)$ over exactly these $t$. $\square$

By Claims 1 and 2, $DA(n) = OPT$, and line L5 follows the stored cuts to build a $\hat d$ of cost $DA(n)$: each run $(t, i]$ is set to $d(t + 1)$, so $\hat d \ge d$, and each run has at least $k$ positions, so $\hat d$ is k-anonymous. (Runs next to each other may end with the same value, which only makes the groups larger.)

**Claim 3 (the lower bound).** Every k-degree anonymous simple graph $\hat G \supseteq G$ on the same vertices adds at least $OPT / 2$ edges.

*Proof.* The degree of each vertex can only grow, so the degree sequence of $\hat G$, listed in the order of $d$, is a k-anonymous vector at least $d$. By the handshake lemma, the number of added edges is half the total growth of the degrees, which is at least $OPT / 2$. $\square$

**Claim 4 (Supergraph).** If lines L6 to L14 return a set of edges, adding it to $G$ gives a simple graph with degree sequence $\hat d$ and exactly $OPT / 2$ added edges, which is the least possible.

*Proof.* Keep the invariant: the current graph $H$ is a simple supergraph of $G$, and for every vertex $u$, $\deg_H(u) + a(u) = \hat d(u)$ with $a(u) \ge 0$. Line L6 makes it true with $H = G$. In one pass, line L10 picks only vertices $w \ne v$ that are not adjacent to $v$ in $H$ and have $a(w) > 0$, so the new edges are new, have two distinct ends, and are distinct from each other. Line L12 adds 1 to $\deg_H(w)$ and takes 1 from $a(w) \ge 1$ for each of them, and $v$ gains $a(v)$ edges, after which line L13 sets $a(v) = 0$. So the invariant holds after the pass. Each pass makes $a(v)$ zero for a vertex with $a(v) > 0$ and never raises any $a$, so the loop ends. If it ends at line L14, every $a(u) = 0$, so $\deg_H = \hat d$. The number of added edges is $\tfrac12 \sum_u (\hat d(u) - d(u)) = OPT / 2$, which by Claim 3 is the least possible. $\blacksquare$

**UNKNOWN is not a proof of impossibility.** For $G$ with one edge on three vertices and $k = 2$, the only least-cost $\hat d$ is $(1, 1, 1)$, whose sum is odd, so line L7 answers UNKNOWN, while the triangle is a 2-degree anonymous supergraph with two added edges.

**Cost.** Sorting takes $O(n \log n)$ time and the prefix sums $O(n)$, after which each $I(t + 1, i) = (i - t) d(t + 1) - (P(i) - P(t))$ takes $O(1)$ time. Line L4 tries at most $k$ values of $t$, so the DP takes $O(n k)$ time and $O(n)$ space. Line L5 takes $O(n)$ time. In the code each pass of the construction scans and sorts $O(n)$ candidates and there are at most $n$ passes, for $O(n^2 \log n)$ time.
