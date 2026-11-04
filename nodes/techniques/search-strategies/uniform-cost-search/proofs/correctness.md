---
title: Uniform-cost search returns a cheapest path, and it stops when costs are bounded below
proves: [correctness, termination]
status: full
---

We use the pseudocode of the page. All action costs are non-negative. For a state $t$, $\delta(t)$ is the least cost of a path from $s_0$ to $t$, and $\delta(t) = \infty$ when $t$ cannot be reached. A pop is *live* if the node passes line L6, and a state is *expanded* when a live pop of one of its nodes reaches line L8. The cost of the path PATH$(n)$ is $n.g$, because line L11 sets $g$ of a child to $g$ of its parent plus the cost of the action. So $n.g \ge \delta(n.state)$ for each node.

**Facts about the table.** (R1) For each state $s$, the nodes stored as *reached*$[s]$, one after the other, have strictly decreasing values of $g$, by the strict test of line L10. Each of them was pushed when it was stored (lines L11 and L12), or it is the root (lines L2 and L3). (R2) A popped node $n$ is live if and only if it is the node stored in *reached*$[n.state]$ at the time of the pop. If it is, then $n.g = $ *reached*$[n.state].g$. If it is not, a later node with a smaller $g$ replaced it, and line L6 skips $n$. (R3) Each node is pushed once and popped at most once.

**Lemma 1.** At each live pop of a node $n$, $n.g \le \delta(t)$ for each state $t$ with $\delta(t) < \infty$ that was not expanded before this pop.

*Proof.* By induction on the live pops. Fix a live pop of $n$ and assume the lemma for all earlier live pops. Then each state $x$ expanded earlier was expanded at a live pop of a node $m$ with $m.g \le \delta(x)$, since $x$ was not expanded before that pop. With $m.g \ge \delta(x)$ we get $m.g = \delta(x)$.

Let $t$ be a state with $\delta(t) < \infty$ that was not expanded before the pop of $n$. Take a path $P = (x_0 = s_0, x_1, \ldots, x_k = t)$ of cost $\delta(t)$. Each prefix of $P$ is a cheapest path to its end, because a cheaper path to $x_j$ followed by the rest of $P$ would be cheaper than $\delta(t)$. So the prefix up to $x_j$ costs $\delta(x_j)$.

*Case 1: $s_0$ was not expanded before the pop of $n$.* Then this is the first live pop. Each node pushed so far is the root, because nodes are pushed only during expansions. So $n$ is the root, $n.g = 0 \le \delta(t)$.

*Case 2: $s_0$ was expanded.* The state $t = x_k$ was not. Let $j$ be the least index such that $x_j$ was not expanded before the pop of $n$. Then $j \ge 1$, and $x_{j-1}$ was expanded, at a live pop with $g = \delta(x_{j-1})$. During that expansion, line L9 computed $g' = \delta(x_{j-1}) + c(x_{j-1}, x_j) = \delta(x_j)$ for the child $x_j$. After lines L10 to L12, *reached*$[x_j].g \le \delta(x_j)$, and by (R1) it stays so. It cannot be less than $\delta(x_j)$, because it is the cost of a path. So at the pop of $n$, the node $r = $ *reached*$[x_j]$ has $r.g = \delta(x_j)$.

The node $r$ is still in the frontier just before the pop of $n$, or $r = n$. It was pushed, by (R1). If it had been popped earlier, it was the stored node at that time too, because a stored node is only replaced, never restored. So that pop was live by (R2), and $x_j$ would have been expanded, which is false. The node $n$ is popped as a minimum, so $n.g \le r.g = \delta(x_j) \le \delta(t)$, where the last step uses that the costs of $P$ after $x_j$ are non-negative. If $r = n$ itself, the same inequality holds. $\square$

**Corollary 2.** Each state is expanded at most once, and at each live pop, $n.g = \delta(n.state)$.

*Proof.* Let $m$ be the node of the first live pop for a state $s$. If $s$ was not expanded before, Lemma 1 with $t = s$ gives $m.g \le \delta(s)$, and $m.g \ge \delta(s)$ holds for each node, so $m.g = \delta(s)$. After this pop, no node can replace $m$ in *reached*$[s]$, because by (R1) it would need $g < \delta(s)$, and no path is that cheap. So $m$ stays the stored node. By (R3) $m$ is not popped again, and by (R2) a later pop of another node for $s$ is stale. So $s$ has exactly one live pop. $\square$

**Theorem 3 (soundness and optimality).** If the search returns PATH$(n)$ and $n.g$ at line L7, then PATH$(n)$ is a path from $s_0$ to a goal with cost $n.g = C^*$.

*Proof.* PATH$(n)$ follows parent pointers from $n$, and each parent link is an action of SUCCESSORS, so it is a path from $s_0$ to $n.state$, which is a goal by line L7, and its cost is $n.g$. Let $t$ be any goal with $\delta(t) < \infty$. If $t$ was expanded before this pop, line L7 would have returned at that earlier live pop, since $t$ is a goal. So $t$ was not expanded before, and Lemma 1 gives $n.g \le \delta(t)$. Hence $n.g \le C^*$. Since $n.g$ is the cost of a path to a goal, $n.g \ge C^*$. $\square$

**Theorem 4 (failure is correct).** If the search returns failure at line L13, no goal can be reached.

*Proof.* Suppose that a goal $t$ is reachable, and take a path $s_0 = x_0, \ldots, x_k = t$. The loop stops only when the frontier is empty. Then each node that was pushed was popped. For each state in *reached*, the node stored at the end was pushed by (R1) and popped, and at its pop it was the stored node, so the pop was live by (R2) and the state was expanded. The state $s_0$ is in *reached*. If $x_j$ is in *reached*, it was expanded, so $x_{j+1}$ was put in *reached* at that expansion (line L10 adds a state that is not in the table). By induction $t$ is in *reached* and was expanded. Line L7 runs before line L8, so the search returned at that live pop instead of failure. $\square$

**Theorem 5 (termination).**
(a) If the branching factor is finite, each action cost is at least $\epsilon > 0$, and a goal is reachable, the search stops after finitely many steps and returns a path of cost $C^*$.
(b) If the space of reachable states is finite, the search stops for all non-negative costs.

*Proof.* Each node that is pushed is a distinct path from $s_0$: a child is pushed only at the expansion of its parent node, a node is popped once, and so two pushed nodes with the same path would have two pushed parents with the same path, down to the root, which is pushed once.

(a) Let $t$ be a goal with $\delta(t) = C^*$; it exists by the fact that a finite branching factor and costs at least $\epsilon$ make the minimum attained (see [completeness and optimality of search](/completeness-and-optimality-of-search/), Fact 1). As long as no goal has been expanded, the proof of Lemma 1, case 2, gives a node in the frontier with $g \le \delta(t) = C^*$ (in case 1 the root has $g = 0$). So each pop, live or stale, before the search returns has $g \le C^*$. A path with $g \le C^*$ has at most $\lfloor C^*/\epsilon \rfloor$ actions, and with a finite branching factor there are finitely many such paths. So the number of pops before the return is finite, and each pop does finitely many steps. The loop cannot stop with failure, by Theorem 4. So it returns, and by Theorem 3 the cost is $C^*$.

(b) Suppose a pushed node has a path that visits a state $x$ twice, at positions $i < j$. When the prefix up to position $i$ was pushed or $x = s_0$ was stored, *reached*$[x].g$ became at most the cost of that prefix, and by (R1) it never increased. The prefix up to $j$ costs at least as much, because the costs between $i$ and $j$ are non-negative. So the strict test of line L10 refused the prefix up to $j$, and it was never pushed, a contradiction because each prefix of a pushed node was pushed. Hence each pushed node is a path without a repeated state. A finite space has finitely many such paths, so the loop runs finitely often. $\blacksquare$
