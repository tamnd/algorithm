---
title: The q-digest has rank error at most L⌊n/k⌋ and at most 4k nodes after a compress
proves: [correctness]
status: full
---

We prove the error bound for Rank and Query, mergeability, termination of the compress, and the size bound for the digest of lines L1 to L11. The universe is $[0, U)$ with $U = 2^L$, a node $(j, i)$ is the dyadic interval $[i2^j, (i + 1)2^j - 1]$, and $c(v) = 0$ for nodes not in $Q$. Write $R(x)$ for the number of items at most $x$, with $R(-1) = 0$, and $\hat R(x)$ for the sum of $c(v)$ over the nodes $v$ whose right end is at most $x$.

**Lemma 1 (conservation).** At all times $\sum_v c(v) = n$, and each item is counted at a node whose interval contains it.

*Proof.* Line L1 counts the new item at its own leaf. Line L6 moves the counts of $v$ and its sibling to their parent, whose interval contains both. Line L10 adds two digests whose counts each satisfy the claim. $\square$

**Lemma 2 (Property 1).** At all times, $c(v) \le \lfloor n/k \rfloor$ for each node $v$ above level 0.

*Proof.* By induction. Line L1 changes only a leaf, and $n$ grows, so $\lfloor n/k \rfloor$ does not go down. Line L6 sets the count of the parent to a value that line L5 has checked to be at most $\lfloor n/k \rfloor$. Line L10 gives $c(v) = c_1(v) + c_2(v) \le \lfloor n_1/k \rfloor + \lfloor n_2/k \rfloor \le \lfloor (n_1 + n_2)/k \rfloor$. $\square$

**Theorem 1 (rank error).** For each $x \in [0, U)$, $0 \le R(x) - \hat R(x) \le L\lfloor n/k \rfloor$.

*Proof.* By Lemma 1, an item counted at a node whose right end is at most $x$ is itself at most $x$. So $\hat R(x)$ counts only items at most $x$, and $\hat R(x) \le R(x)$. Now take an item $y \le x$ that $\hat R(x)$ misses. It is counted at a node $v$ whose interval contains $y$ and whose right end is above $x$. The left end of $v$ is at most $y \le x$, so the interval of $v$ contains $x$. A dyadic interval that contains $x$ and does not end at $x$ is not the leaf of $x$, so it is one of the proper ancestors of the leaf $x$, of which there is one at each level 1 to $L$. By Lemma 2 each holds at most $\lfloor n/k \rfloor$ items, so at most $L\lfloor n/k \rfloor$ items are missed. $\square$

**Theorem 2 (quantile error).** For $1 \le r \le n$, Query($r$) returns $x$ with $R(x) \ge r$ and $R(x - 1) \le r - 1 + L\lfloor n/k \rfloor$.

*Proof.* Line L8 orders the nodes by right end, and line L9 stops at the first node at which the running sum reaches $r$. By Lemma 1 the total is $n \ge r$, so it stops. Let $x$ be the right end of that node. All nodes with right end below $x$ come before it, so the running sum just before the first node with right end $x$ is $\hat R(x - 1)$. This value is below $r$, since the loop did not stop earlier. After all nodes with right end $x$ the sum is $\hat R(x) \ge r$, as the loop stopped at one of them. Theorem 1 gives $R(x) \ge \hat R(x) \ge r$ and $R(x - 1) \le \hat R(x - 1) + L\lfloor n/k \rfloor \le r - 1 + L\lfloor n/k \rfloor$. $\square$

With $k \ge L/\varepsilon$, $L\lfloor n/k \rfloor \le \varepsilon n$, which gives the error $\varepsilon n$ of the abstract type. If $x$ occurs in the stream, its copies fill the positions $R(x - 1) + 1$ to $R(x)$, and this range meets $[r, r + \varepsilon n]$ because $R(x - 1) + 1 \le r + \varepsilon n$ and $R(x) \ge r$.

**Lemma 3 (termination).** The loop of lines L3 to L7 ends after at most $nL + 1$ passes.

*Proof.* Let $\Phi = \sum_v c(v)\,j(v)$, where $j(v)$ is the level of $v$. A merge at line L6 moves the positive amount $c(v) + c(\mathrm{sibling}(v))$ up one level, so $\Phi$ grows by at least 1. By Lemma 1, $\Phi \le nL$. Each pass except the last makes at least one merge. $\square$

**Theorem 3 (size).** When the loop of lines L3 to L7 ends, $c(v) + c(\mathrm{sibling}(v)) + c(\mathrm{parent}(v)) > \lfloor n/k \rfloor$ for each node $v \in Q$ below the root (Property 2), and $|Q| \le 4k$.

*Proof.* The last pass makes no merge, so line L5 fails for every node of $Q$ below the root, which is Property 2. Let $Q'$ be the nodes of $Q$ other than the root, so $|Q'| \ge |Q| - 1$. Sum Property 2 over $Q'$:
$$S = \sum_{v \in Q'} \big(c(v) + c(\mathrm{sibling}(v)) + c(\mathrm{parent}(v))\big).$$
Each term is an integer above $\lfloor n/k \rfloor$, so it is at least $\lfloor n/k \rfloor + 1 > n/k$, and $S > |Q'|\,n/k$. Now count how often a fixed count $c(u)$ appears in $S$: as the first term when $v = u$, as the sibling term when $v$ is the sibling of $u$, and as the parent term when $v$ is one of the two children of $u$. That is at most 4 times, so $S \le 4\sum_u c(u) = 4n$ by Lemma 1. So $|Q'|\,n/k < 4n$, which gives $|Q'| < 4k$. If the root is not in $Q$, then $|Q| = |Q'| \le 4k - 1$. If it is, $|Q| = |Q'| + 1 \le 4k$. $\square$

Between compresses, line L2 runs a compress as soon as $|Q| > 4k$, and line L1 adds at most one node, so $|Q| \le 4k + 1$ at all times.

**Theorem 4 (mergeability).** Lines L10 and L11 give a digest of the union of the two streams that satisfies Lemma 1, Lemma 2 and Theorem 3 with $n = n_1 + n_2$, so Theorems 1 and 2 hold for the union with error $L\lfloor (n_1 + n_2)/k \rfloor$.

*Proof.* Lemma 1 and Lemma 2 hold after line L10 by their proofs, and line L11 gives Theorem 3. Theorems 1 and 2 use only Lemmas 1 and 2. $\blacksquare$
