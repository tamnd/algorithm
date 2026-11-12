---
title: The parsimony ratchet ends and returns a TBR local optimum of the true length
proves: [correctness]
status: full
---

Let the taxa be $1, \ldots, n$ with $n \ge 4$ and let there be $m$ characters. For a weight vector $w$ with positive integer entries, write $L_w(T) = \sum_j w_j c_j(T)$, where $c_j(T)$ is the least number of changes of character $j$ on $T$. Write $N(T)$ for the set of TBR neighbors of $T$, and $\mathbf{1}$ for the vector of unit weights. A tree $T$ is a TBR local optimum of $L_w$ if $L_w(T') \ge L_w(T)$ for every $T' \in N(T)$.

**Lemma 1 (the search ends).** For every start tree $T_0$ and weights $w$, TBR-SEARCH$(T_0, w)$ ends after at most $L_w(T_0) + 1$ rounds, and it returns a pair $(T, L_w(T))$ where $T$ is a TBR local optimum of $L_w$ and $L_w(T) \le L_w(T_0)$.

*Proof.* Each round either finds a neighbor $T'$ with $L_w(T') < L_w(T)$ and moves to it, or finds none and returns. Every $L_w$ is a sum of products of nonnegative integers, so it is a nonnegative integer, and a move lowers it by at least 1. Starting from $L_w(T_0)$, at most $L_w(T_0)$ moves can happen, so the search returns after at most $L_w(T_0) + 1$ rounds. The search holds the length of its current tree, and it is set to $L_w$ of that tree on every move, so the returned number is $L_w(T)$. The search returns only in a round where no neighbor is shorter, so $T$ is a local optimum. The length never rises, which gives $L_w(T) \le L_w(T_0)$. $\square$

**Lemma 2 (the loop invariant).** Before each test of line L3, and at line L8: (a) $b = L_{\mathbf 1}(best)$; (b) $best$ is a TBR local optimum of $L_{\mathbf 1}$; (c) $b \le s_1$, where $s_1$ is the length returned on line L1.

*Proof.* By induction on the number of iterations. After line L2, $(best, b)$ is the pair from line L1, so (a) and (b) hold by Lemma 1 with $w = \mathbf 1$, and (c) holds with equality.

Suppose the claims hold before an iteration. Line L4 makes a vector $w'$ with entries in $\{1, 2\}$, which is a valid weight vector, so the search of line L5 ends by Lemma 1. Line L6 runs TBR-SEARCH under $\mathbf 1$, so by Lemma 1 it ends and returns $(T, s)$ with $s = L_{\mathbf 1}(T)$ and $T$ a TBR local optimum of $L_{\mathbf 1}$. If line L7 finds $s < b$, it sets $(best, b) \leftarrow (T, s)$, and (a) and (b) hold for the new pair; also the new $b$ is less than the old $b$, so (c) still holds. If $s \ge b$, nothing changes and the claims hold as before. $\square$

**Theorem.** PARSIMONY-RATCHET ends after $k$ iterations and returns a pair $(best, b)$ with $b = L_{\mathbf 1}(best)$, where $best$ is a TBR local optimum of the unit-weight length and $b$ is at most the length reached by a plain TBR search from the same start tree. If $T^*$ is a most parsimonious tree, then $L_{\mathbf 1}(T^*) \le b$.

*Proof.* The loop of line L3 runs exactly $k$ times, and each of its searches ends by Lemma 1, so the algorithm ends. The claims on $(best, b)$ are Lemma 2 at line L8, since the plain search from the start tree is exactly line L1. The last claim holds because $best$ is a tree on the $n$ taxa and $T^*$ minimizes $L_{\mathbf 1}$ over all such trees. $\blacksquare$

**Bound on the rounds.** A character has at most $n - 1$ changes on any tree: give every internal vertex the state that is most common among the leaves, and at most $n - 1$ edges to leaves change. So $L_{w'}(T) \le 2m(n-1)$ and $L_{\mathbf 1}(T) \le m(n-1)$ for every tree $T$, and by Lemma 1 each search makes at most $2m(n-1) + 1$ rounds. This is the count used on the main page for the worst-case time.
