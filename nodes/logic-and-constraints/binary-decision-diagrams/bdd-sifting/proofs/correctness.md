---
title: The in-place swap is correct, and sifting keeps the functions and never increases the size
proves: [correctness]
status: full
---

The store is a shared BDD with the variables on levels $0, \ldots, n - 1$, and two sinks below all levels. A node $u$ tests the variable $\mathrm{var}(u)$ and has a low child and a high child; $f_u$ is its function. The store is *ordered* if each child is on a lower level than its parent. It is *reduced* if no node has two equal children, and no two nodes test the same variable and have the same pair of children. The unique table of a variable $v$ maps each pair of children to the node of $v$ with these children. The size is the number of nodes that some root reaches, with the sinks.

We use two standard facts about ordered and reduced stores. They are proved on the pages [BDD canonicity](/bdd-canonicity/) and [reduced ordered BDD](/reduced-ordered-bdd/).

- **(C1)** In an ordered and reduced store, distinct nodes have distinct functions, and the function of a node depends on the variable that it tests.
- **(C2)** For a fixed order and a fixed list of root functions, the reduced diagram is unique up to the names of the nodes. In particular, the size depends only on the order and the root functions.

**Lemma 1 (the swap).** Let the store be ordered and reduced, with $x$ on level $k$ and $y$ on level $k + 1$. After SWAP$(k)$ and the garbage collection, the store is ordered and reduced for the order with $x$ and $y$ exchanged, every node that is still present has the same function as before, and the roots have the same ids.

*Proof.* Let $u$ be a node of $x$ with children $l$ and $h$. Both children are on levels larger than $k$.

*Case 1: neither child tests $y$.* Then both children are on levels larger than $k + 1$, so they do not depend on $x$ or $y$. The node $u$ stays unchanged. In the new order, $x$ is on level $k + 1$, and the children are below it, so $u$ is ordered.

*Case 2: some child tests $y$.* Put $f_{a0}, f_{a1}$ equal to the low and the high child of the child $c_a$ ($c_0 = l$, $c_1 = h$) if $c_a$ tests $y$, and both equal to $c_a$ otherwise. Then $f_{ab}$ is the function $f_u$ with $x = a$ and $y = b$, and its node is on a level larger than $k + 1$. The swap sets $u$ to test $y$ with the low child $p = \mathrm{MK}(x, f_{00}, f_{10})$ and the high child $q = \mathrm{MK}(x, f_{01}, f_{11})$. MK$(x, a, b)$ returns $a$ if $a = b$, and a node of $x$ with the function $\neg x \, f_a \vee x \, f_b$ otherwise. So $f_p = f_u|_{y=0}$ and $f_q = f_u|_{y=1}$, and the new function of $u$ is

$$\neg y \, f_u|_{y = 0} \vee y \, f_u|_{y = 1} = f_u .$$

So every node keeps its function. Nodes on the other levels are not touched, and the nodes on level $k + 1$ (the old $y$-nodes) keep their children.

*Ordered.* A rewritten $u$ tests $y$, now on level $k$, and its children are $x$-nodes on level $k + 1$ or nodes on levels larger than $k + 1$. A new $x$-node has children $f_{ab}$ on levels larger than $k + 1$. Old $y$-nodes now sit on level $k$ and their children are on levels larger than $k + 1$. Nodes above level $k$ point to nodes on levels at least $k$. So the store is ordered.

*No equal children.* A new $x$-node is made by MK only when its two children differ. For a rewritten $u$: some child $c_a$ of $u$ tests $y$, so by (C1) $f_{c_a}$ depends on $y$, and so does $f_u = \neg x \, f_l \vee x \, f_h$. Then $f_u|_{y=0} \ne f_u|_{y=1}$, so $f_p \ne f_q$ and $p \ne q$.

*No two nodes with the same key.* We check the unique tables while the loop runs. A new $x$-node has children $f_{ab}$, which do not test $y$. An $x$-node that is still waiting for its rewrite has a child that tests $y$. So MK never returns such a waiting node, and it never makes a node whose key is already used. A rewritten node $u$ is removed from the table of $x$ before MK runs, and it is entered into the table of $y$ with the key $(p, q)$. Since $u$ depends on $x$ (by (C1), as it tested $x$), $p$ and $q$ cannot both be nodes that do not test $x$: if they were, $f_{00} = f_{10}$ and $f_{01} = f_{11}$, so $f_u$ would not depend on $x$. So one of $p$ and $q$ is an $x$-node on level $k + 1$. An old $y$-node has both children on levels larger than $k + 1$, so its key differs from $(p, q)$. Two rewritten nodes $u \ne u'$ have different functions by (C1) before the swap, and they keep them, so their keys differ.

So the store is ordered and reduced. The garbage collection only deletes nodes that no root reaches, so it keeps these properties and does not change the roots. $\square$

**Lemma 2 (only the two levels change).** In the situation of Lemma 1, the number of reached nodes on each level other than $k$ and $k + 1$ is the same before and after the swap.

*Proof.* By (C2), the reached nodes on a level $j$ are the distinct functions $F|_\alpha$ that depend on the variable of level $j$, where $F$ is a root function and $\alpha$ is an assignment to the variables above level $j$. For $j < k$, the variables above $j$ and the variable on $j$ do not change. For $j > k + 1$, the set of variables above $j$ does not change, only their order, and the set of functions $F|_\alpha$ does not depend on that order. $\square$

**Theorem (sifting).** Let SIFT$(B, g)$ start on an ordered and reduced store $B$ of size $s_0$. Then it terminates; at the end the store is ordered and reduced, the roots have the same ids and functions, and the size is at most $s_0$. Moreover, after the step for each variable $v$, the size is the minimum of the sizes recorded at lines L2 and L7 during that step.

*Proof.* Each loop at line L5 moves $v$ one level in a fixed direction and stops at the end of the order, so each step makes at most $3n$ swaps, and there are $n$ steps. So SIFT terminates.

By Lemma 1, each swap keeps the store ordered and reduced and keeps the root ids and functions. So this holds at the end.

Fix the step for a variable $v$. Each swap at line L6 or line L9 exchanges $v$ with a neighbour, so the order of the other variables among themselves never changes in this step. An order in this step is therefore fixed by the level of $v$. At line L2 and at each execution of line L7, `best` is the minimum of the sizes recorded so far in this step, and `best_pos` is a level of $v$ at which that size was recorded. Line L9 moves $v$ to `best_pos`, so the order is the one for which `best` was recorded. By (C2) the size is `best` again. Since `best` starts at the size at line L2 and only decreases, the size after the step is at most the size before the step.

The size before the first step is $s_0$, and each step does not increase it, so the final size is at most $s_0$. Line L10 returns it. $\blacksquare$

**Remark (no guarantee of optimality).** The theorem shows only that each step reaches the best level for $v$ among the levels visited, with the other variables fixed. It says nothing about the distance to the optimum order. By the theorems of Bollig and Wegener and of Sieling on the page [NP-completeness of OBDD variable ordering](/variable-ordering-np-hardness/), no polynomial-time method can give a constant-factor guarantee unless P = NP.
