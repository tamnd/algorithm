---
title: Backtracking for SAT returns the first model in lexicographic order, or UNSAT when there is none
proves: [correctness, termination]
status: full
---

We use the pseudocode of the page. $F$ is a CNF formula over $x_1, \ldots, x_n$, and each clause is a set of literals over these variables. We write an assignment as a word $a_1 a_2 \ldots a_n$ over $\{0, 1\}$, where $0$ is false and $1$ is true, and we order words lexicographically with $0 < 1$. A *prefix* is a word $p = a_1 \ldots a_i$ with $1 \le i \le n$, and its *block* is the set of full assignments that start with $p$. The blocks of the prefixes of one length $i$ split all $2^n$ assignments into $2^i$ intervals of the lexicographic order. For a clause $C$, let $\max(C)$ be the largest index of a variable in $C$. A clause with $\max(C) \le i$ has a value under every prefix of length at least $i$.

## The two easy lines

If $F$ has the empty clause, it has no model, and line L1 returns UNSAT. If $n = 0$ and $F$ has no empty clause, then $F$ has no clause at all, because every literal names one of $x_1, \ldots, x_n$. So the empty assignment is a model, and line L2 returns it. From now on $n \ge 1$ and every clause is nonempty, so $1 \le \max(C) \le n$.

## The invariant

Let $p = \alpha[1 \ldots i]$ be the current prefix each time line L5 runs.

> **(I)** (a) No assignment that comes before the block of $p$ in the lexicographic order is a model of $F$. (b) For each $j < i$, no clause $C$ with $\max(C) = j$ is false under $\alpha[1 \ldots j]$.

*Initialization.* Line L3 sets $p = 0$. The block of $0$ starts with $0^n$, the first assignment, so (a) holds. Part (b) has no case to check.

*Case 1: the test of line L5 passes and $i < n$.* Line L7 sets the new prefix $p0$. The block of $p0$ starts where the block of $p$ starts, so the assignments before it are the same, and (a) holds. The test that just passed is (b) for $j = i$, and the earlier cases of (b) do not change, because $\alpha[1 \ldots i]$ does not change.

*Case 2: the test fails.* Then some clause $C$ with $\max(C) = i$ is false under $p$. Every assignment in the block of $p$ agrees with $p$ on the variables of $C$, so none of them is a model. Line L9 removes the trailing ones: $p = q\,0\,1^r$ for some prefix $q$ of length $i' - 1$ and some $r \ge 0$, or $p = 1^i$.

- If $p = q\,0\,1^r$, line L11 makes the new prefix $q1$. The assignments before the block of $q1$ are those before the block of $q0$, and those in the block of $q0$. The block of $q0$ splits into the assignments before the block of $p$ and the block of $p$ itself, because every word in the block of $q0$ that is after the block of $p$ would have to be larger than $q\,0\,1^r$ at one of the positions $i' + 1, \ldots, i$, where $p$ has ones. So every assignment before the block of $q1$ is before the block of $p$, or in it, and none is a model. This is (a). Part (b) holds for $j < i'$ because $\alpha[1 \ldots j]$ did not change.
- If $p = 1^i$, every assignment is before the block of $p$ or in it, so $F$ has no model, and line L10 returns UNSAT correctly.

## Correctness

**Theorem.** The algorithm returns UNSAT if and only if $F$ has no model. When $F$ has a model, it returns the first model of $F$ in the lexicographic order.

*Proof.* Line L6 returns $\alpha$ when $i = n$ and the test of line L5 passes. By (I)(b) and this test, for each $j \le n$ no clause $C$ with $\max(C) = j$ is false under $\alpha[1 \ldots j]$. Every clause has some $\max(C) = j$ between 1 and $n$, and it is fully assigned by $\alpha[1 \ldots j]$, so it is true. So $\alpha$ is a model. The block of the full prefix $\alpha$ is $\{\alpha\}$, so by (I)(a) no earlier assignment is a model, and $\alpha$ is the first model. Case 2 shows that line L10 returns UNSAT only when $F$ has no model. By the termination argument below, the loop returns, so these are the only two outcomes. $\blacksquare$

## Termination and the count of tests

Each run of line L5 tests a prefix, which is a node of the full binary tree of depth $n$ without its root. Case 1 moves to the first child, and Case 2 moves to the next node after the whole subtree of an ancestor of $p$ in preorder. So the tested prefixes appear in strictly increasing preorder, no prefix is tested twice, and there are at most $2 + 4 + \cdots + 2^n = 2^{n+1} - 2$ tests. The bound is reached, for example, by $F = \{\{x_n\}, \{\neg x_n\}\}$, where every test at depth $n$ fails and every test above passes. $\blacksquare$
