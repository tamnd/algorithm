---
title: Beam search returns real paths and stops on finite graphs, and with no width limit it is breadth-first search
proves: [correctness]
status: full
---

We use the pseudocode of the page. The graph is directed, each state has finitely many successors, and each action cost is a nonnegative number. A finite width $k$ gives no promise of a path or of a cheapest path, and the example on the page shows both failures. So the claims below are the ones that do hold: the answer is valid, the search stops, and with no limit it is complete.

**Fact 1 (parents and costs).** At each visit of line L3, each state $u$ of LAYER has a value $g[u]$ and a parent pointer, and following the pointers from $u$ gives a path from $s_0$ to $u$ of cost $g[u]$. Each state of LAYER at depth $i$ (the $i$-th visit of line L3, counting from 0) reaches $s_0$ in exactly $i$ pointer steps.

*Proof.* By induction on $i$. For $i = 0$, LAYER is $[s_0]$ with $g[s_0] = 0$ and no parent. Line L6 records each candidate $m$ with a parent $n$ in the current LAYER and the cost $g[n] + c$, where $(m, c)$ is a pair of SUCCESSORS$(n)$. So the path to $n$ followed by the action to $m$ costs $g[n] + c$ and has $i + 1$ steps. Line L8 keeps a subset of the candidates with these values. The values of states in earlier layers never change, because line L5 skips the states in SEEN, so the pointers of the path to $n$ still hold. $\square$

**Theorem 2 (a valid answer).** If line L1 or line L7 returns a path, it is a path from $s_0$ to a goal state, and its cost is the returned value.

*Proof.* Line L1 returns $(s_0)$ only if $s_0$ is a goal. Line L7 returns the path to a goal candidate $m$, which by the argument of Fact 1 is the path to its parent in LAYER followed by the action to $m$, of cost equal to the value recorded for $m$. $\square$

**Theorem 3 (termination).** If finitely many states, say $N$, can be reached from $s_0$, the search stops after at most $N$ visits of line L3.

*Proof.* Each candidate is a state that is not in SEEN, by line L5. So each nonempty LAYER built at line L8 consists of states that are not in SEEN, and line L9 adds at least one new state to SEEN. SEEN holds only reachable states, so at most $N - 1$ nonempty layers follow the first one. After that LAYER is empty, the loop of line L3 ends, and line L10 returns failure, unless line L7 returned before. $\square$

**Theorem 4 (no width limit).** If line L8 keeps all candidates, LAYER at depth $i$ is the set of states whose least number of actions from $s_0$ is $i$. So the search returns a path when a goal is reachable on a finite graph, and if each action costs 1, the path is a cheapest one.

*Proof.* Write $\delta(u)$ for the least number of actions from $s_0$ to $u$. By induction on $i$, assume that the layers at depths $0, \ldots, i$ are the sets $\{u : \delta(u) = j\}$ for $j \le i$, so that SEEN is $\{u : \delta(u) \le i\}$. A candidate at depth $i + 1$ is a successor of a state with $\delta = i$ that is not in SEEN, so its $\delta$ is $i + 1$. Conversely, a state with $\delta = i + 1$ has a predecessor with $\delta = i$, is not in SEEN, and is a candidate. With no limit, line L8 keeps all of them.

If a goal is reachable, let $t$ be a goal of least $\delta(t) = D$. If $D = 0$, line L1 returns. Otherwise no goal is a candidate at depths below $D$, and at depth $D$ the goal $t$ is a candidate, so line L7 returns a path to some goal with $D$ actions. When each action costs 1, its cost is $D$, and no path to a goal is shorter. $\square$

**Remark.** With general costs, even the version with no limit does not return a cheapest path in general: it returns a path with the fewest actions, like breadth-first search. With a finite width, Theorems 2 and 3 still hold, but Theorem 4 fails, because line L8 can drop each candidate that lies on a path to a goal.
