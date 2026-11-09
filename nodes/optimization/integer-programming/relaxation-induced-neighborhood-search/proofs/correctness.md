---
title: RINS returns a better feasible point and solves its neighborhood
proves: [correctness]
status: full
---

**Statement.** Let $P = \{x \ge 0 : A x \le b\}$ be bounded, let $\bar{x}$ be a feasible point of $\min\{c^\top x : x \in P,\ x_j \in \mathbb{Z}\ (j \in I)\}$, and let $Q$ be the program of line L3. Then RINS solves at most $M + 1$ linear programs and returns a feasible point $x$ with $c^\top x \le c^\top \bar{x}$. If the loop ends with an empty stack, $x$ is an optimal solution of $Q$.

For a node $N$ of the search, let $P_N$ be the polyhedron of its LP relaxation (the constraints of $Q$ and the bound changes on the path to $N$) and let $S_N = \{x \in P_N : x_j \in \mathbb{Z}\ (j \in I)\}$.

**Lemma 1.** Let $N$ be a node whose LP solution has a value $t = x_j \notin \mathbb{Z}$ for some $j \in I$. Then the two children $N^-$ (with $x_j \le \lfloor t \rfloor$) and $N^+$ (with $x_j \ge \lceil t \rceil$) satisfy $S_N = S_{N^-} \cup S_{N^+}$.

*Proof.* Each child adds a constraint to $P_N$, so $S_{N^-} \cup S_{N^+} \subseteq S_N$. Let $z \in S_N$. Then $z_j$ is an integer. Since $t$ is not an integer, $\lceil t \rceil = \lfloor t \rfloor + 1$, so no integer lies strictly between $\lfloor t \rfloor$ and $\lceil t \rceil$. Hence $z_j \le \lfloor t \rfloor$ or $z_j \ge \lceil t \rceil$, and $z$ lies in $S_{N^-}$ or in $S_{N^+}$. $\square$

**Proof of the statement.**

*Number of linear programs.* Line L1 solves one. Each pass through the loop increases `count` by 1 and solves one, and the loop runs only while `count` $< M$. So there are at most $M + 1$ linear programs. Each of them is either infeasible or has an optimum, because its feasible set lies in the bounded set $P$.

*Feasibility and value.* At line L4, `best` $= \bar{x}$, which is feasible. Line L8 changes `best` only to an optimal $x$ of a node LP whose integer variables are integer. Such an $x$ lies in $P_N \subseteq P$ and is integer on $I$, so it is feasible for the original program. Line L8 is reached only when line L7 did not continue, so $v = c^\top x < c^\top \mathrm{best}$. Hence $c^\top \mathrm{best}$ never increases, and the returned point has $c^\top x \le c^\top \bar{x}$.

*Optimality when the stack empties.* Let $S_Q$ be the feasible set of $Q$ and let $\beta$ denote the current value $c^\top \mathrm{best}$. We show that the following invariant holds each time line L5 tests the loop condition:

> every $z \in S_Q$ with $c^\top z < \beta$ lies in $S_N$ for some node $N$ on the stack.

At the first test, the stack holds only the root, and $S_{\mathrm{root}} = S_Q$. Now consider one pass, which pops a node $N$ with LP solution $x$ and value $v$. Take $z \in S_Q$ with $c^\top z < \beta'$, where $\beta' \le \beta$ is the value after the pass. Then $c^\top z < \beta$ too, so before the pass $z$ was in $S_{N'}$ for a node $N'$ on the stack. If $N' \ne N$, the node $N'$ is still on the stack. If $N' = N$, there are three cases.

1. Line L7 continues. If the LP of $N$ is infeasible, $S_N$ is empty, which contradicts $z \in S_N$. Otherwise $c^\top z \ge v \ge \beta$, because $z \in P_N$ and $v$ is the minimum over $P_N$; this contradicts $c^\top z < \beta$. So this case does not happen.
2. Line L8 runs. Then $\beta' = v \le c^\top z$, because $z \in P_N$. This contradicts $c^\top z < \beta'$. So this case does not happen either.
3. Line L9 runs. By Lemma 1, $z$ lies in $S_{N^-}$ or in $S_{N^+}$, and both children are now on the stack.

So the invariant holds after the pass. If the loop ends with an empty stack, no $z \in S_Q$ has $c^\top z < \beta$. The point `best` lies in $S_Q$: the incumbent $\bar{x}$ meets the fixings $x_j = \bar{x}_j$ ($j \in F$) by the definition of $F$, and each later value of `best` is in some $S_N \subseteq S_Q$. So `best` is an optimal solution of $Q$. $\blacksquare$

**What is not claimed.** The optimum of $Q$ is in general not the optimum of the original program, because the fixings of line L3 can remove every optimal point. If the loop ends because of the node limit, the returned point need not be optimal for $Q$ either.
