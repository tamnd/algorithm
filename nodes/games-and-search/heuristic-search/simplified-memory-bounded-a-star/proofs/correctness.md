---
title: SMA* stays within its memory, and a path it returns is cheapest among the paths that fit
proves: [correctness]
status: partial
---

We use the pseudocode of the page. The graph is finite, each action cost is positive, $M \ge 2$, and $h$ is admissible: $0 \le h(u) \le h^*(u)$, where $h^*(u)$ is the cost of a cheapest path from $u$ to a goal, so $h = 0$ at goals. Each node $x$ stands for a simple path from $s_0$, the path from the root to $x$. Its depth is the number of actions on that path and $g(x)$ is their cost. The slots of a node that is not a goal are the successors of its state that are not on its path. A goal node has no slots. A *leaf* of MEM is a node with no stored child.

For a node $x$, let $L(x)$ be the least cost of a simple path from $s_0$ to a goal that has the path of $x$ as a prefix and has at most $M - 1$ actions, or $\infty$ if there is none. For a slot of $x$ with state $m$, let $L$ of the slot be $L$ of the child with state $m$. Let $C_M = L(\text{root})$, the least cost of a goal path with at most $M - 1$ actions. A cheapest such path repeats no state, since costs are positive, so it is simple. We use three facts about $L$. First, $g(x) + h(x) \le L(x)$, since the rest of a goal path from the state of $x$ costs at least $h^*$. Second, if $x$ is not a goal, $L(x)$ is the least $L$ over its slots, since a simple goal path through $x$ goes on to a state that is not on the path of $x$. Third, if $x$ is not a goal and has depth at least $M - 1$, or has no slots, then $L(x) = \infty$.

**Lemma 1 (stored nodes form a tree).** At each step, the root is in MEM, and the parent of each other node of MEM is in MEM. So a node at depth $t$ in MEM has its $t$ proper ancestors in MEM too.

*Proof.* A new node is added at line L11 as a child of $n$, which is in MEM. Line L10 deletes only a leaf, so no stored node loses its parent, and line L9 never picks the root. $\square$

**Lemma 2 (memory).** At line L9 a leaf other than the root and $n$ exists, and MEM never holds more than $M$ nodes. So by Lemma 1, each node of MEM has depth at most $M - 1$.

*Proof.* MEM grows by one node only at line L11, after line L10 has deleted a node whenever MEM held $M$ nodes. So it is enough to show that line L9 finds a leaf. At line L9, MEM holds $M \ge 2$ nodes, and by Lemma 1 they form a tree with the root, so the tree has a leaf other than the root. Suppose that $n$ is its only leaf other than the root. Then the tree is a single path from the root to $n$ with $M$ nodes, so $n$ has depth $M - 1$. Line L5 did not return, so $n$ is not a goal, and line L7 set its value to $\infty$ when $n$ was made. Values never fall, as line L12 only raises them, so $f(n) = \infty$, and line L4 would have returned. So a leaf other than the root and $n$ exists. $\square$

**Lemma 3 (lower bounds).** At each step, $f(x) \le L(x)$ for each node $x$ of MEM, and the value in each forgotten slot is at most the $L$ of that slot.

*Proof.* By induction on the steps. The root starts with $f = h(s_0) \le L(\text{root})$ by the first fact, or with $\infty$ only when the third fact gives $L = \infty$. At line L7, if $s$ gets $\infty$, the third fact gives $L(s) = \infty$. Otherwise its value is the larger of $g(s) + h(s) \le L(s)$ and the floor. The floor is $f(n)$ or the value of the forgotten slot $i$. By induction $f(n) \le L(n)$, and $L(n) \le L(s)$ by the second fact, since $n$ is not a goal. The value of slot $i$ is at most $L(s)$ by induction. So $f(s) \le L(s)$. At line L10, the value stored in the slot of $z$ is $f(z) \le L(z)$. At line L12, a node $x$ gets the least value over its slots, with each slot full or forgotten. Each of these values is at most the $L$ of its slot, by induction, so their least is at most the least $L$ over the slots, which is $L(x)$ by the second fact. Line L12 works only on $n$ and its ancestors, which are not goals. $\square$

**Lemma 4 (a good node is in Q).** If $C_M < \infty$, then at each visit of line L2 some node $x$ of Q has $f(x) \le C_M$.

*Proof.* Let $P = (p_0, \ldots, p_k)$ be a goal path with at most $M - 1$ actions and cost $C_M$. It is simple, so $p_{j+1}$ is not on $(p_0, \ldots, p_j)$. No $p_j$ with $j < k$ is a goal, since that would give a cheaper goal path. So for each $j < k$, the node for $(p_0, \ldots, p_j)$, when it is stored, has a slot for $p_{j+1}$. The root is the node for $(p_0)$ and is in MEM. Let $j$ be the largest index such that the nodes for $(p_0), \ldots, (p_0, \ldots, p_j)$ are all in MEM, each a stored child of the one before. If $j = k$, this node is a goal, so it is in Q. If $j < k$, the slot for $p_{j+1}$ of this node holds no stored child, so the node is in Q. In both cases the node $x$ lies on $P$, so $L(x) = C_M$, and $f(x) \le C_M$ by Lemma 3. $\square$

**Theorem 5 (the answer).** If SMA* returns a path, the path leads from $s_0$ to a goal, has at most $M - 1$ actions, and costs $C_M$. If SMA* returns failure, no goal path has at most $M - 1$ actions.

*Proof.* A path returned at line L5 is the path from the root to a goal node $n$ of MEM. Each node is made from a successor of its parent at line L7, so the path is a real path of cost $g(n)$, and by Lemma 2 it has at most $M - 1$ actions. So $g(n) \ge C_M$. By Lemma 3 and the first fact, $g(n) = g(n) + h(n) \le f(n)$, and $n$ has the least $f$ in Q, so by Lemma 4, $f(n) \le C_M$. So $g(n) = C_M$.

If $C_M < \infty$, Lemma 4 says that Q is not empty and holds a node with $f \le C_M < \infty$. So the node $n$ of line L3 has $f(n) < \infty$, and neither line L2 nor line L4 returns failure. So failure is returned only when $C_M = \infty$. $\square$

**What is not proved here.** The theorem says what SMA* returns if it stops. It does not show that it stops. Russell states that SMA* is complete when memory holds a shallowest solution path, which needs termination. The implementation guards the loop with a step limit. A full proof of termination for this version, with one value per slot, is missing, so the status of this page is partial.
