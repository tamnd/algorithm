---
title: Iterative broadening is sound and complete on finite trees, with a bounded overhead in the worst case
proves: [correctness, termination, complexity]
status: full
---

We use the pseudocode of the page. The search tree from $s_0$ is finite, and $B$ is the largest number of children of a node, with $B = 0$ when $s_0$ has no child.

**Lemma 1 (soundness).** If BOUNDED$(s, c)$ returns a list, the list is a path of the tree from $s$ to a goal.

*Proof.* By induction on the height of $s$ in the finite tree. A list is returned at line L6, where it is $[s]$ and $s$ is a goal, or at line L11, where it is $[s]$ followed by the list of a call BOUNDED$(s', c)$ for a child $s'$ of $s$, which by induction is a path from $s'$ to a goal. $\square$

**Lemma 2 (a run without pruning is a full search).** If a run of BOUNDED$(s_0, c)$ returns failure and leaves *pruned* false, then no node of the tree is a goal.

*Proof.* We show by induction on the height of $s$: if BOUNDED$(s, c)$ returns failure and sets no flag, then no node of the subtree of $s$ is a goal. The call returned at line L12, so $s$ is not a goal by line L6. No flag was set at line L8, so $s$ has at most $c$ children and line L9 calls BOUNDED on each of them. Each of these calls returned failure, or line L11 would have returned, and none set the flag. By induction their subtrees hold no goal. $\square$

**Lemma 3 (each run stops).** Each call BOUNDED$(s_0, c)$ stops.

*Proof.* The calls follow the edges of a finite tree from the root, and each call makes at most one call per child. So the number of calls is at most the number of nodes. $\square$

**Theorem 4 (correctness and termination).** The search stops after at most $\max(1, B - 1)$ runs. It returns a path from $s_0$ to a goal if the tree has a goal, and failure otherwise.

*Proof.* In the run with $c \ge B$, no node has more than $c$ children, so line L8 never sets the flag. That run returns a path or, by line L5, failure. The first such run has $c = \max(2, B)$, which is run number $\max(2, B) - 1$. Each run stops by Lemma 3. A returned path is a path to a goal by Lemma 1. Failure is returned only by a run that left the flag false, and then the tree has no goal by Lemma 2. If the tree has a goal, the search therefore cannot return failure, so it returns a path. $\square$

**Theorem 5 (worst-case cost).** In the uniform tree of branching factor $b \ge 2$ and depth $d \ge 1$, the leaves visited by all runs together number less than $(1 + b/(d+1))\, b^d$.

*Proof.* The run with cutoff $c \le b$ visits at most the $c^d$ leaves of the tree cut to breadth $c$, and there are runs only for $c = 2, \ldots, b$. For $1 \le c \le b - 1$, the function $x^d$ is increasing on $[c, c+1]$, so $c^d \le \int_c^{c+1} x^d\,dx$. Hence
$$ \sum_{c=2}^{b} c^d \le b^d + \sum_{c=2}^{b-1} \int_c^{c+1} x^d\,dx \le b^d + \int_1^b x^d\,dx < b^d + \frac{b^{d+1}}{d+1}. $$
The internal nodes of the run with cutoff $c$ number $(c^d - 1)/(c - 1) < c^d$, so the total number of nodes is less than twice this bound. $\blacksquare$
