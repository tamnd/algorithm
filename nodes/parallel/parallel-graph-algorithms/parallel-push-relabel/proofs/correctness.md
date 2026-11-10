---
title: Synchronous push-relabel computes a maximum flow in fewer than 4n^2 pulses
proves: [correctness, termination, complexity]
status: full
---

**Setting.** $G = (V, A)$ is a directed graph with $n$ vertices, $m$ arcs, integer capacities $c \ge 0$, a source $s$ and a sink $t \ne s$. Every arc $a = (u, v)$ has a reverse $\bar a = (v, u)$ in the residual graph; $r(a)$ is the residual capacity, and $r(a) + r(\bar a)$ stays equal to the capacity of the pair. A preflow $f$ gives each $v \ne s$ the excess $e(v) \ge 0$, its inflow minus its outflow. A vertex is active if $v \notin \{s, t\}$ and $e(v) > 0$. A labeling $d$ is valid if $d(s) = n$, $d(t) = 0$, and $d(v) \le d(w) + 1$ for every residual arc $(v, w)$, that is, every arc with $r > 0$. An arc $(v, w)$ is admissible for $d$ if $r(v, w) > 0$ and $d(v) = d(w) + 1$. In a pulse, $d_0$ and $e_0$ are the labels and excesses at its start.

**Lemma 1 (the pushes of a pulse do not interfere).** In a pulse, an arc and its reverse are never both admissible for $d_0$, so each residual capacity changes by the pushes of at most one vertex. The pushes give the same result in any order, and the excesses stay nonnegative.

*Proof.* If $(v, w)$ and $(w, v)$ were both admissible, then $d_0(v) = d_0(w) + 1$ and $d_0(w) = d_0(v) + 1$. A push on $(v, w)$ lowers $r(v, w)$ and raises $r(w, v)$; only $v$ pushes on $(v, w)$, and $w$ does not push on $(w, v)$ in this pulse, so the value of $r(v, w)$ that $v$ reads is the one at the start of the pulse. Each vertex $v$ sends at most $e_0(v)$, and the arriving amounts are added after the pushes. $\square$

**Lemma 2 (valid labels).** The labeling is valid after line L2 and after every pulse. Every relabel raises a label by at least 1.

*Proof.* After line L2, the arcs out of $s$ are saturated and their reverses carry no flow yet, so every residual arc out of $s$ is a loop at $s$. Every other residual arc starts at a vertex of label 0, so the condition holds. Assume $d_0$ is valid at the start of a pulse. After the pushes, $d_0$ is still valid: a push on $(v, w)$ can create the residual arc $(w, v)$, and $d_0(w) = d_0(v) - 1 \le d_0(v) + 1$. Now let $v$ be relabeled in line L9. It has excess, so it has a residual arc (the reverse of an arc on which flow came in), and the minimum is defined. For every residual arc $(v, w)$, $d_0(v) \le d_0(w) + 1$, and $d_0(v) \ne d_0(w) + 1$ since $v$ has no admissible arc, so $d_0(w) \ge d_0(v)$, and the new label $d(v) \ge d_0(v) + 1$.

Labels never go down, and $s$ and $t$ keep theirs. Take a residual arc $(v, w)$ after the pulse. If $v$ was relabeled, $d(v) \le 1 + d_0(w) \le 1 + d(w)$. If not, $d(v) = d_0(v) \le d_0(w) + 1 \le d(w) + 1$. $\square$

**Lemma 3 (label bound).** At all times, every vertex with $e(v) > 0$ has a residual path to $s$, and every label is at most $2n - 1$.

*Proof.* Decompose the preflow into paths from $s$ and cycles. Excess at $v$ comes from paths that start at $s$ and end at $v$, and the reverse of such a path is a residual path from $v$ to $s$. A label changes only when its vertex has excess, and right after the change, the valid labels along a simple residual path from $v$ to $s$, of at most $n - 1$ arcs, give $d(v) \le d(s) + n - 1 = 2n - 1$. $\square$

**Theorem 1 (correctness).** When no vertex is active, $f$ is a maximum flow.

*Proof.* With no active vertex, every $v \notin \{s, t\}$ has $e(v) = 0$, so $f$ is a flow. Suppose that the residual graph has a simple path from $s$ to $t$, with $k \le n - 1$ arcs. The labels are valid by Lemma 2, so $d(s) \le d(t) + k \le n - 1$, which contradicts $d(s) = n$. So the residual graph has no augmenting path, and $f$ is maximum by the max-flow min-cut theorem. $\blacksquare$

**Theorem 2 (termination).** The algorithm stops after fewer than $4n^2$ pulses.

*Proof.* By Lemma 3, each of the $n - 2$ vertices other than $s$ and $t$ gains at most $2n - 1$ in label, so the total label increase is $I < 2n^2$. A pulse with a relabel adds at least 1 to $I$ by Lemma 2, so there are fewer than $2n^2$ such pulses.

Let $\Phi$ be the largest label of an active vertex, or 0 if there is none; $\Phi = 0$ after line L2. Look at a pulse, and let $v$ be active at its end.

- If $v$ was not active at the start, it received flow in the pulse from an active vertex $u$ along an arc admissible for $d_0$, so $d_0(v) = d_0(u) - 1 \le \Phi - 1$.
- If $v$ was active at the start and keeps part of $e_0(v)$, then all its admissible arcs for $d_0$ are saturated. The arcs that became residual in the pulse go to vertices with a higher $d_0$, so $v$ has no admissible arc and it is relabeled.
- If $v$ was active at the start and sent all of $e_0(v)$, then its excess at the end came in during the pulse, and as in the first case, $d_0(v) \le \Phi - 1$.

So in a pulse with no relabel, every active vertex at the end has a label at most $\Phi - 1$, and $\Phi$ goes down by at least 1. In a pulse with relabels, every active vertex at the end has $d(v) \le \Phi + (d(v) - d_0(v))$, so $\Phi$ goes up by at most the label increase of that pulse. Since $\Phi$ starts at 0 and is never negative, the number of pulses with no relabel is at most $I < 2n^2$. In all, there are fewer than $4n^2$ pulses. $\blacksquare$

**Theorem 3 (cost).** In the work-span model with a fetch-and-add or a sum per target, the work is $O((n + m) n^2)$ and the span is $O(n^2 \log n)$.

*Proof.* A pulse reads each vertex and the arcs of the active and the relabeled vertices once, so it costs $O(n + m)$ work. Each vertex splits $e_0(v)$ over its admissible arcs in order with a prefix sum, the amounts that arrive at each vertex are added with a sum, and each relabel is a minimum over the arcs of one vertex; each of these steps has $O(\log n)$ span. Theorem 2 bounds the number of pulses by $4n^2$. $\blacksquare$
