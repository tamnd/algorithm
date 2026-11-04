---
title: Depth-limited search stops, and its answer of path, cutoff or failure is exact
proves: [correctness, termination]
status: full
---

We use the pseudocode of the page with the check for cycles. Without the check, read "path" below as "path that may repeat states" and treat *onpath* as always empty; each step of the proof stays the same. Let $T$ be the tree of paths from $s_0$ that repeat no state. A call DLS$(s, k)$ is made for a node $\pi$ of $T$ that ends at $s$, and $\pi$ has depth $\ell - k$.

**Invariant 1.** When DLS$(s, k)$ is called for the path $\pi$, the set *onpath* is exactly the set of states of $\pi$, and each call leaves *onpath* as it found it.

*Proof.* At line L2 the path is $(s_0)$ and *onpath* $= \{s_0\}$ by line L1. A call adds $s'$ at line L9 before the recursive call for the path $\pi$ followed by $s'$, and removes it at line L11 after the call returns, and $s'$ was not in *onpath* by the test of line L8. The call returns at lines L3, L5, L6, L12 or L14, and each recursive call that it made has already undone its own addition. $\square$

**Theorem 1 (termination).** If each state has finitely many successors, the search stops after at most $N = \sum_{i=0}^{\ell} b^i$ calls, where $b$ is the largest number of successors.

*Proof.* Each call with $k > 0$ makes at most $b$ calls with $k - 1$, and a call with $k = 0$ makes none. By induction on $k$, a call with budget $k$ makes at most $\sum_{i=0}^{k} b^i$ calls in total, itself included. Each call does finitely many other steps. $\square$

**Lemma 2 (meaning of a returned path).** If DLS$(s, k)$ returns a list $r$ for the path $\pi$, then $r$ starts at $s$, follows SUCCESSORS, ends at a goal state, has at most $k$ actions, and $\pi$ followed by $r$ without its first state repeats no state.

*Proof.* By induction on $k$. A list is returned at line L3, where $r = [s]$ and $s$ is a goal, or at line L12, where $r = [s]$ followed by the list $r'$ of a call DLS$(s', k-1)$ for a successor $s'$ of $s$ not on $\pi$. By induction, $r'$ is a path from $s'$ to a goal with at most $k - 1$ actions that avoids the states of $\pi$ followed by $s'$, apart from $s'$ itself. So $r$ has at most $k$ actions and the claim holds. $\square$

Applied to the first call, Lemma 2 shows that a returned path goes from $s_0$ to a goal with at most $\ell$ actions and repeats no state.

**Lemma 3 (completeness within the budget).** Let DLS$(s, k)$ be called for the path $\pi$. If some goal state can be reached from $s$ by a path of at most $k$ actions that avoids the states of $\pi$ other than $s$, then the call returns a path.

*Proof.* By induction on $k$. If $s$ is a goal, line L3 returns. Otherwise the path to a goal has at least one action, so $k \ge 1$, and its second state $s'$ is a successor of $s$ that is not on $\pi$. So line L8 tries $s'$, unless an earlier child already returned a path at line L12. By Invariant 1 the call DLS$(s', k-1)$ is made for $\pi$ followed by $s'$, and the rest of the path to the goal has at most $k - 1$ actions and avoids that path. By induction it returns a path, and line L12 returns. $\square$

A path to a goal of at most $\ell$ actions can be shortened to one that repeats no state, by cutting out each cycle. So by Lemma 3 with $\pi = (s_0)$ and $k = \ell$, the search returns a path when some goal is within $\ell$ actions of $s_0$.

**Lemma 4 (meaning of failure).** If DLS$(s, k)$ for the path $\pi$ returns failure, then no path from $s$ that avoids the states of $\pi$ other than $s$ has more than $k$ actions, and none of them ends at a goal.

*Proof.* By induction on $k$. For $k = 0$, failure comes from line L6: $s$ is not a goal and each successor of $s$ is on $\pi$, so each path that avoids $\pi$ has 0 actions. For $k \ge 1$, failure comes from line L14 with *cut* false: $s$ is not a goal, no child returned a path, and no child returned cutoff, so each child $s'$ not on $\pi$ returned failure. A path from $s$ that avoids $\pi$ and has at least one action starts with such an $s'$, and by induction its remainder has at most $k - 1$ actions and does not end at a goal. $\square$

**Theorem 5 (the answer is exact).**

1. The search returns a path if and only if some goal has a path of at most $\ell$ actions from $s_0$, and the path is such a path.
2. If it returns failure, no goal can be reached from $s_0$.
3. If it returns cutoff, no goal has a path of at most $\ell$ actions, and some path from $s_0$ that repeats no state has more than $\ell$ actions.

*Proof.* Part 1 is Lemma 2 and Lemma 3 for the first call. For part 2, Lemma 4 for the first call says that each path from $s_0$ that repeats no state has at most $\ell$ actions and does not end at a goal. Each reachable goal has a path that repeats no state, so no goal is reachable. For part 3, the first half is part 1. For the second half, follow the chain of calls that returned cutoff, from the first call down. A call returns cutoff at line L14 only if one of its children returned cutoff, and at line L5 only if $k = 0$ and $s$ has a successor not on the path. So the chain ends at a call with $k = 0$, for a path of $\ell$ actions, which extends to a path of $\ell + 1$ actions that repeats no state. $\blacksquare$
