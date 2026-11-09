---
title: Nested depth-first search reports a lasso iff an accepting cycle is reachable
proves: [correctness, complexity]
status: full
---

We use the pseudocode of the page. The graph is $G = (V, E)$ with initial states $I$ and accepting states $A$. A *DFS1 call* is a call of DFS1, and its state *finishes* when line L8 is reached for it. We write $d(u)$ for the time DFS1$(u)$ starts and $f(u)$ for the time $u$ finishes. Between $d(u)$ and $f(u)$, the state $u$ is *gray* (on the outer stack); after $f(u)$ it is *black*; before $d(u)$ it is *white*. We write $u \to^+ v$ when there is a path with at least one edge from $u$ to $v$, and $u \to^* v$ when there is a path with zero or more edges.

We use three standard facts of depth-first search (they hold for the forest that the loop of line L2 builds).

- **(P) Parenthesis.** For any two visited states $u, v$, the intervals $[d(u), f(u)]$ and $[d(v), f(v)]$ are either disjoint or nested. If $[d(v), f(v)] \subseteq [d(u), f(u)]$, then $v$ is a descendant of $u$ in the search forest, and so $u \to^* v$.
- **(B) Black states have no white successors.** When $u$ finishes, the loop of lines L6 and L7 has looked at each successor $t$ and called DFS1$(t)$ if $t$ was white. So at each time after $f(u)$, no successor of $u$ is white.
- **(G) The gray states are the stack.** At each time, the gray states are exactly the states on the outer stack, and they form a path of tree edges from a state of $I$ to the current state. Just after $u$ finishes, the gray states are exactly the proper ancestors of $u$.

**Soundness.** Suppose line L13 reports, with seed $s$. DFS2$(s)$ is called at line L10, before line L11 pops $s$, so by (G) the outer stack is a path $s_0 \ldots s_k$ of edges with $s_0 \in I$ and $s_k = s$. The inner searches use a stack in the same way: when line L13 runs in the call DFS2$(x)$, the inner stack is a path $s = x_0, x_1, \ldots, x_r = x$ of edges, and $(x, s) \in E$ by the test of line L13. Line L9 set $s$ only if $s \in A$. So $s_0 \ldots s_k$ followed by the cycle $x_0 \ldots x_r\, s$ is an accepting lasso. $\square$

**Lemma 1 (what one inner search reaches).** Let $D$ be the set of flagged states at the start of DFS2$(s)$. If DFS2$(s)$ does not report, then it flags each state $u$ for which there is a path $s = u_0, u_1, \ldots, u_r = u$ with $r \ge 1$ such that none of $u_1, \ldots, u_r$ is in $D$ or equal to $s$. Moreover, if there is such a path and $(u, s) \in E$, then DFS2$(s)$ reports.

*Proof.* By induction on $r$. For $r = 1$, line L12 in the call DFS2$(s)$ looks at the edge $(s, u_1)$. As $u_1 \neq s$ and $u_1 \notin D$, either $u_1$ was flagged earlier in this same search, or lines L14 and L15 flag it now. For $r > 1$, by induction $u_{r-1}$ is flagged in this search. A state is flagged in this search only at line L15, right before the call DFS2$(u_{r-1})$ of line L16, and that call looks at the edge $(u_{r-1}, u_r)$, so $u_r$ is flagged as in the base case. For the second claim, the call DFS2$(u)$ (or DFS2$(s)$ itself when $r = 0$) looks at the edge $(u, s)$, and line L13 reports, since the test for the seed comes before the test of line L14. $\square$

**Lemma 2 (the key lemma).** Assume that the run has not reported when DFS2$(s)$ starts, that $s \in A$, and that $s$ lies on a cycle. Assume also that no accepting state $s'$ with $f(s') < f(s)$ lies on a cycle. Then no state of a simple cycle $C$ through $s$ is flagged at the start of DFS2$(s)$.

*Proof.* Suppose that a state $t$ of $C$ is flagged. Flags are set only by inner searches, and the inner searches run in the order of line L10, so $t$ was flagged by DFS2$(s')$ for an accepting $s'$ with $f(s') < f(s)$. The call DFS2$(s')$ flags only states it reaches by edges from $s'$, so $s' \to^+ t$. As $t$ is on $C$, $t \to^* s$, hence $s' \to^+ s$. By (P), since $f(s') < f(s)$, either $d(s) < d(s') < f(s') < f(s)$ or $f(s') < d(s)$.

*Case (a): $d(s) < d(s')$.* Then $s'$ is a descendant of $s$ by (P), so $s \to^* s'$. With $s' \to^+ s$ this gives a cycle through $s'$.

*Case (b): $f(s') < d(s)$.* Look at the time just after $s'$ finishes. Then $s$ is white. Take a path $s' = p_0, p_1, \ldots, p_\ell = s$ with $\ell \ge 1$, and let $p_j$ be the first state on it that is white at this time. Then $j \ge 1$, and $p_{j-1}$ is not white. If $p_{j-1}$ were black, (B) would make its successor $p_j$ non-white. So $p_{j-1}$ is gray. Since $s'$ is black now, $p_{j-1} \neq s'$, so $j - 1 \ge 1$ and $s' \to^+ p_{j-1}$. By (G), $p_{j-1}$ is a proper ancestor of $s'$, so $p_{j-1} \to^+ s'$. This gives a cycle through $s'$.

In both cases $s'$ is an accepting state on a cycle with $f(s') < f(s)$, against the assumption. $\square$

**Completeness.** Suppose an accepting lasso exists. Then some accepting state that is reachable from $I$ lies on a cycle. If the run reports before such a state finishes, we are done by soundness. Otherwise the outer search visits every state that is reachable from $I$ (each call of line L3 visits all states reachable from its root that are still white, and the loop runs over all of $I$). Among the reachable accepting states on cycles, let $s$ be the one with the smallest $f(s)$. No report has happened when DFS2$(s)$ starts, so by Lemma 2 no state of a simple cycle $C = s\, c_1 \ldots c_r\, s$ is flagged at that time. The path $s, c_1, \ldots, c_r$ avoids the flagged states and $s$ itself, and $(c_r, s) \in E$ (for a self-loop, $r = 0$). By Lemma 1, DFS2$(s)$ reports. $\square$

So NESTED-DFS reports a lasso iff an accepting lasso exists, and each report is an accepting lasso.

**The early stop.** With the option of Holzmann, Peled and Yannakakis, the inner search also stops when it reaches a state $a$ on the outer stack. By (G), the outer stack holds a path from $a$ to the seed, so the inner path from the seed to a predecessor of $a$, then the edge to $a$, then the outer stack from $a$ to the seed, is a cycle through the seed. So each early report is sound. Up to its first early report, the run is the same as the plain run, so if an accepting lasso exists, the run reports (early or as before), and if none exists, it never reports.

**Cost.** DFS1 is called at most once per state, because line L7 calls it only on states not in *visited* and line L5 adds the state at once; each call scans the out-edges of its state once. DFS2 is called on a state $u$ either at line L10, at most once since $u$ finishes once, or at line L16, at most once since line L15 flags $u$ first and flags are never removed. Each call scans the out-edges of its state once. So the time is $O(n + m)$ with $n$ and $m$ the numbers of reachable states and edges, and the memory beyond the two stacks is two bits per state: one for *visited* and one for *flagged*. $\blacksquare$
