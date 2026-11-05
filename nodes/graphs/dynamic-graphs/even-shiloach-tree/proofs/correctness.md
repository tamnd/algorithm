---
title: The levels of an Even-Shiloach tree are the capped distances from the source
proves: [correctness]
status: full
---

Let $G$ be the current graph, with positive integer weights, and let $d(v) = d(s, v)$ and $d_D(v)$ be as on the page. Write $\ell(v)$ for the level, with $\infty$ allowed. An edge $(u, v)$ **supports** $v$ if it is present and $\ell(u) + w(u, v) = \ell(v)$.

We prove that the following invariants hold before and after every iteration of the loop of line L4, and at the start and end of every deletion.

- **(A)** $\ell(s) = 0$, and $\ell(v) \le d_D(v)$ for every $v$.
- **(B)** For every present edge $(u, v)$ with $v \ne s$ and $\ell(v) < \infty$: $\ell(v) \le \ell(u) + w(u, v)$.
- **(C)** For every $v \ne s$ with $\ell(v) < \infty$, no edge before $p(v)$ in $\mathrm{in}(v)$ supports $v$.
- **(D)** Every $v \ne s$ with $\ell(v) < \infty$ that is not supported by the edge at $p(v)$ is in the queue $Q$.

**Initialization.** Line L1 sets $\ell = d_D$, so (A) holds. For a present edge $(u, v)$ with $d_D(v) < \infty$: if $d(u) = \infty$ or $d(u) + w > D$, the right side of (B) is $\infty$ or larger than $D \ge \ell(v)$; otherwise $d(v) \le d(u) + w$. So (B) holds. The pointer is set to the first supporting edge, which exists for a finite $v \ne s$ because the last edge of a shortest path supports it; so (C) holds and (D) holds with an empty queue.

**A deletion (lines L2 and L3).** Deleting an edge can only increase distances, so $d_D$ does not decrease and (A) still holds. (B) and (C) speak only about present edges or about edges that do not support, and a deleted edge supports nothing, so they still hold. The only vertex that may lose the support at its pointer is the head $v$ of the deleted edge, and line L3 puts it into $Q$, so (D) holds.

**An iteration of the loop.** Let $x$ be taken from $Q$. If $x = s$ or $\ell(x) = \infty$, nothing changes. Otherwise line L5 moves $p(x)$ forward over edges that do not support $x$, which keeps (C). If it stops at a supporting edge, $x$ leaves $Q$ and (D) holds for $x$.

Otherwise no edge of $\mathrm{in}(x)$ supports $x$: the edges before the old pointer by (C), and the others by the scan. Together with (B), every present edge $(u, x)$ has $\ell(u) + w(u, x) \ge \ell(x) + 1$, because levels and weights are integers. Line L6 sets $\ell(x)$ to $\ell(x) + 1$.

- (A) still holds for $x$. Suppose $d_D(x) = \ell(x)$ before the raise, so $d(x) = \ell(x) \le D$ is finite and $x \ne s$. Let $(u, x)$ be the last edge of a shortest path to $x$; then $d(u) = d(x) - w(u, x) \le D$, so $d_D(u) = d(u)$, and by (A) for $u$, $\ell(u) + w(u, x) \le d(u) + w(u, x) = \ell(x)$. This contradicts the inequality above. So $d_D(x) \ge \ell(x) + 1$. If the new level exceeds $D$, then $d_D(x) > D$, which means $d_D(x) = \infty$, and line L7 sets $\ell(x) = \infty$, still within (A).
- (B) holds for the edges into $x$, by the inequality above. For an edge $(x, y)$ out of $x$, raising $\ell(x)$ only increases the right side of (B) for $y$.
- (C) holds for $x$, since the pointer is reset to the first edge (or $x$ became $\infty$). For a vertex $y \ne x$, raising $\ell(x)$ can only make an edge $(x, y)$ stop supporting $y$, never start: if $(x, y)$ supported $y$ before, it does not after, and if it did not, then $\ell(x) + w > \ell(y)$ by (B), which stays true. So no edge before $p(y)$ starts to support $y$.
- (D): if $x$ is still finite, line L7 puts it back into $Q$. Line L8 puts every out-neighbor $y$ into $Q$, which covers every $y$ whose support at $p(y)$ was an edge from $x$. Every other vertex keeps the support it had.

**Termination.** Each raise increases a level, levels are bounded by $D + 1$ before they become $\infty$, and each queue entry that does not raise a vertex removes one entry. So the loop ends.

**Theorem.** After each deletion, $\ell(v) = d_D(v)$ for every vertex $v$.

*Proof.* When the queue is empty, by (D) every finite $v \ne s$ is supported by the edge $(u, v)$ at $p(v)$, so $\ell(u) = \ell(v) - w(u, v) < \ell(v)$ and $\ell(u)$ is finite. Following the supporting edges from $v$ backward visits vertices with strictly decreasing finite levels, so it ends, and it can only end at $s$, the one finite vertex that needs no support. This gives a path from $s$ to $v$ of length $\ell(v)$, so $d(v) \le \ell(v)$. By (A), $\ell(v) \le d_D(v)$, and $\ell(v)$ is finite, so $d_D(v) = d(v) \le \ell(v) \le d_D(v)$, and equality holds. If $\ell(v) = \infty$, then by (A) $d_D(v) = \infty$ as well. Line L9 returns $\ell(v)$. $\blacksquare$
