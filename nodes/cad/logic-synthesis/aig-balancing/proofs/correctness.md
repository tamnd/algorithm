---
title: Balancing keeps the functions and does not raise any level or the node count
proves: [correctness]
status: full
---

We use the notation of the and-inverter graph page: $f_\ell$ is the function of a literal $\ell$, and $\mathrm{lev}_G$ and $\mathrm{lev}_H$ are the levels in the old graph $G$ and the new graph $H$. Let $V$ be the set of AND nodes of $G$ that the outputs reach, with the fanout counts of the algorithm. For $v \in V$, the supergate of $v$ is the tree found by line L5. Its inner nodes are $v$ and the AND nodes that the walk goes into, and its leaf edges are the fanins where the walk stops. We write $p(v)$ for the number of leaf edges.

**Lemma 1 (the supergate is a tree).** Each node that the walk enters below $v$ is entered once, and $f_v$ is the AND of $f_\ell$ over the leaf literals $\ell$, with repeats. The supergate has $p(v) - 1$ inner nodes.

*Proof.* The walk enters a node $u$ only through a fanin edge of a node already in the supergate, and $u$ has exactly one fanout, so it is entered through that edge only, once. So the inner nodes and their fanin edges form a binary tree with root $v$ and $p(v)$ leaf edges, which has $p(v) - 1$ inner nodes. An inner node $u$ below $v$ is reached by an edge with no inverter, so the tree is a tree of ANDs, and $f_v$ is the AND of its leaf literals. $\square$

**Lemma 2 (functions).** BAL(v) returns a literal $r$ of $H$ with $f_r = f_v$.

*Proof.* By induction on the level of $v$ in $G$. For an input or the constant, line L3 is right. For an AND node, each leaf $\ell$ comes from a node of smaller level, so by induction BAL(node($\ell$)) has the function of node($\ell$), and the literal put into $S$ at line L6 has the function $f_\ell$. The AND of a collection of functions does not depend on repeats, and the constant 1 does not change it, so $f_v = \bigwedge_{x \in S} f_x$, with the empty AND equal to 1. If $S$ holds 0 or both $x$ and $\neg x$, this AND is 0, which line L7 returns. Otherwise lines L8 to L10 replace two literals of $Q$ by a literal of their AND, by the AND page, until one is left, so the AND of $Q$ stays $f_v$. The memo of line L4 returns a value that was right when it was stored. $\square$

For a finite list of integers $a_1, \ldots, a_m$ with $m \ge 1$, let $\Sigma = \sum_i 2^{a_i}$ and $T(a) = \lceil \log_2 \Sigma \rceil$.

**Lemma 3 (the lower bound).** In any binary tree whose leaves have the levels $a_1, \ldots, a_m$ and whose inner nodes have the level one more than the larger level of their two children, the root has a level of at least $T(a)$.

*Proof.* We show $2^{\mathrm{lev}(u)} \ge \Sigma(u)$ for every node $u$, where $\Sigma(u)$ is the sum of $2^{a_i}$ over the leaves below $u$. For a leaf it is an equality. For an inner node with children $y$ and $z$, $2^{\mathrm{lev}(u)} = 2 \cdot 2^{\max(\mathrm{lev}(y), \mathrm{lev}(z))} \ge 2^{\mathrm{lev}(y)} + 2^{\mathrm{lev}(z)} \ge \Sigma(y) + \Sigma(z) = \Sigma(u)$. At the root, $2^{\mathrm{lev}} \ge \Sigma$, so $\mathrm{lev} \ge T(a)$. $\square$

**Lemma 4 (the greedy).** Let line L9 start with a queue whose levels are $a_1, \ldots, a_m$. The last literal has a level of at most $T(a)$.

*Proof.* We show that one round of line L9 does not raise $T$ of the levels in the queue. Let the two lowest levels be $x \le y$, and let the AND have level $z$. The AND of the AIG page returns either a node of level $y + 1$, or, by a trivial rule, a literal of level at most $y$, so $z \le y + 1$. Let $\Sigma$ be the sum before the round and $\Sigma' = \Sigma - 2^x - 2^y + 2^z$ the sum after it. If $z \le y$, then $\Sigma' \le \Sigma$. If $z = y + 1$ and $x = y$, then $\Sigma' = \Sigma$. If $z = y + 1$ and $x < y$, all levels other than $x$ are at least $y$, so $\Sigma - 2^x$ is a multiple of $2^y$, say $k 2^y$ with $k \ge 1$, and $\Sigma' = (k + 1) 2^y$. Let $2^t$ be the least power of two with $2^t \ge \Sigma$. Then $2^t > k 2^y \ge 2^y$, so $2^t$ is a multiple of $2^y$ and larger than $k 2^y$, so $2^t \ge (k + 1) 2^y = \Sigma'$. In all cases $T$ does not grow. At the end the queue holds one literal of some level $c$, with $T = c$, so $c \le T(a)$. $\square$

**Lemma 5 (levels).** For every AND node $v \in V$, $\mathrm{lev}_H(\mathrm{BAL}(v)) \le \mathrm{lev}_G(v)$.

*Proof.* By induction on $\mathrm{lev}_G(v)$. Let the leaf edges of the supergate of $v$ be $\ell_1, \ldots, \ell_p$ with the old levels $b_j = \mathrm{lev}_G(\mathrm{node}(\ell_j))$. By Lemma 1 the supergate is a binary tree over these leaves, so by Lemma 3, $\mathrm{lev}_G(v) \ge T(b)$. By induction, the literal that line L6 makes from $\ell_j$ has a level of at most $b_j$, and $S$ keeps a sub-collection of these literals, one for each distinct value. So the sum $\sum_{x \in S} 2^{\mathrm{lev}_H(x)}$ is at most $\sum_j 2^{b_j}$, and $T$ of the levels of $S$ is at most $T(b)$. If line L7 returns 0 or line L10 returns 1, the level is 0. Otherwise Lemma 4 gives $\mathrm{lev}_H(r) \le T(\text{levels of } S) \le T(b) \le \mathrm{lev}_G(v)$. $\square$

**Lemma 6 (size).** The number of AND nodes of $H$ is at most $|V|$.

*Proof.* Call $v \in V$ a root if BAL is called on it. Line L5 enters a node $u$ only if $u$ has one fanout and is reached by a plain edge, and BAL is called on a node only as an output node or as a leaf, that is, a node reached by a complemented edge, or with two or more fanouts, or as an output. A node with one fanout is either entered through its one fanin edge, or is a leaf of that edge, not both, and an output counts as a fanout. So each node of $V$ is a root or an inner node of exactly one supergate, and the supergates of the roots partition $V$, with $\sum_{\text{roots}} (p(v) - 1) = |V|$ by Lemma 1. The memo of line L4 runs the body once per root, and lines L8 to L10 for a root with $|S| \le p(v)$ distinct leaves make at most $|S| - 1 \le p(v) - 1$ calls of AND, each of which adds at most one node. Only these calls add nodes to $H$. $\square$

**Theorem.** BALANCE returns an AIG $H$ with the same output functions as $G$, with $\mathrm{lev}_H$ of each new output at most $\mathrm{lev}_G$ of the old one, so no more depth, and with no more AND nodes than the part of $G$ that the outputs reach.

*Proof.* Lemma 2 for the functions, with the output phase put back at line L2, Lemma 5 for the levels and Lemma 6 for the size. $\blacksquare$
