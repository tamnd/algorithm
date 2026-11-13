---
title: Greedy best-first graph search returns a real path, stops on a finite graph, and fails only when no goal can be reached
proves: [correctness]
status: full
---

We use the graph search of the page: the pseudocode with lines L7 and L8. Each state has finitely many successors, each action cost $c(n, n')$ is a nonnegative number, and $h$ is any function from states to numbers. Nothing in this proof needs $h$ to be admissible or consistent.

**Fact 1 (each node holds a real path).** For each node in OPEN, following the parent pointers from it gives a path $s_0 = p_0, p_1, \ldots, p_k$ of the graph that ends at its state, and its value $g$ is $\sum_{i=1}^{k} c(p_{i-1}, p_i)$.

*Proof.* By induction on the number of nodes created. The node of $s_0$ at line L1 has the path $(s_0)$ and $g = 0$. A node made at line L9 for $n'$ has the parent $n$, where $(n', c)$ is a pair of SUCCESSORS$(n)$, so $n \to n'$ is an action of cost $c$. Its path is the path of $n$ followed by this action, and its value $g(n) + c$ is the cost of that path by the induction hypothesis. Nodes do not change after they are made. $\square$

**Theorem 1 (valid answer).** If the search returns at line L5, the path goes from $s_0$ to a goal along actions of the graph, and the returned number is its cost.

*Proof.* The node $n$ removed at line L4 was in OPEN, so Fact 1 applies to it, and IS-GOAL$(n)$ holds. $\square$

**Fact 2 (each state enters OPEN at most once).** Each state is put in OPEN at most one time over the whole run, and a state is in REACHED exactly when it was put in OPEN at some time.

*Proof.* The start is put in OPEN at line L2 and added to REACHED there. Another state $n'$ is put in OPEN only at line L9, which runs only when line L7 found $n' \notin$ REACHED, and line L8 then adds $n'$ to REACHED. States never leave REACHED. So after the first time, the test of line L7 fails for $n'$, and $s_0$ is in REACHED from the start. $\square$

**Theorem 2 (termination on a finite graph).** If $n$ states can be reached from $s_0$, the loop of line L3 runs at most $n$ times.

*Proof.* Each pass removes one node from OPEN at line L4. All states put in OPEN can be reached from $s_0$ by Fact 1, and by Fact 2 each one is put in OPEN at most once. So at most $n$ nodes are ever put in OPEN, and at most $n$ passes remove one. $\square$

**Theorem 3 (completeness on a finite graph).** On a finite graph the search returns failure only if no goal can be reached from $s_0$.

*Proof.* Suppose the search returns failure at line L10. Then OPEN is empty and no removed node was a goal. Every state $u$ in REACHED was put in OPEN (Fact 2) and is no longer there, so it was removed at line L4. It was not a goal, so the pass went on to lines L6 to L9 for $u$: for each successor $u'$ of $u$, line L7 found $u'$ in REACHED, or line L8 put it there. So REACHED is closed under SUCCESSORS. It contains $s_0$, so by induction on the length of a path it contains every state that can be reached from $s_0$. If one of them were a goal, it would have been removed at line L4 and returned at line L5. So no reachable state is a goal. $\square$

**Remark (what is not true).** The search is not optimal and has no bound on the ratio of its cost to $C^*$, even for a consistent $h$: on the edges S→X 1, S→Y 1, X→G $M$ and Y→G 1, with $h$ = 1, 0, 1, 0 on S, X, Y, G, it returns S-X-G of cost $M + 1$, while $C^* = 2$. The tree search form, without lines L7 and L8, does not have Fact 2, so the argument of Theorem 2 fails, and the loop example of the page shows that it can run forever on a finite graph. On an infinite graph the graph search can also run forever, so Theorem 2 needs finiteness.
