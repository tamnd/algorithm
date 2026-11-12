---
title: DBSCAN labels core points by the components of the core graph and finds all noise
proves: [correctness]
status: full
---

We use the pseudocode of the page. Fix $\varepsilon > 0$ and an integer $\mathit{MinPts} \ge 1$. A point $p$ is *core* if $|N_\varepsilon(p)| \ge \mathit{MinPts}$, where $N_\varepsilon(p) = \{q \in D : \mathrm{dist}(p, q) \le \varepsilon\}$ holds $p$ itself. The *core graph* $G$ has the core points as vertices and an edge between two core points at distance at most $\varepsilon$. A non-core point is a *border point* if some core point lies in its $\varepsilon$-neighborhood, and *noise* otherwise.

**Claim.** When DBSCAN stops:

1. each point has exactly one label, which is NOISE or a cluster number;
2. two core points have the same label if and only if they lie in the same connected component of $G$, and the labels of the components are distinct;
3. a point has the label NOISE if and only if it is noise by the definition above;
4. a border point has the label of the component of some core point in its $\varepsilon$-neighborhood.

*Step 1: the labels change in one direction.* A label starts as UNDEFINED. Line L5 changes UNDEFINED to NOISE. Line L6 changes UNDEFINED to a cluster number. Line L14 changes NOISE to a cluster number, and line L15 changes UNDEFINED to a cluster number. No line changes a cluster number. So a cluster number, once given, is final, and a NOISE label can only become a cluster number.

*Step 2: each point is queried exactly once.* A point enters the queue only in line L15, when its label changes from UNDEFINED, so it enters at most once. A point is queried in line L4 if its label is UNDEFINED when the outer loop reaches it, and in line L10 if it leaves the queue. These two cases exclude each other. A point queried in line L4 gets a label in line L5 or L6 at once, so it is never UNDEFINED again and never enters the queue. A point that enters the queue was UNDEFINED, so the outer loop had not reached it yet; when the outer loop reaches it later, it has a cluster label, and line L3 skips it. Each point is queried in one of the two ways: if the outer loop finds it UNDEFINED, line L4 queries it; if not, its label was set earlier by line L6 (then it was queried in line L4), by line L15 (then it was in the queue, and the inner loop runs until the queue is empty, so it was queried in line L10), or by line L5 or L14 (then it was queried in line L4 when it became NOISE). Each query sees the fixed set $N_\varepsilon(p)$, so the test of line L5 or L11 is true exactly for the core points. Hence every core point is queried and found core, and line L7 or L12 then calls CLAIM on each point of its neighborhood.

*Step 3: the core points of one label lie in one component.* Consider the run of the outer loop that creates label $C$ at the point $i$. The point $i$ is core by line L5. During this run, a point gets the label $C$ only through CLAIM, called in line L7 or L12 on a point of $N_\varepsilon(c)$ where $c$ is a core point with label $C$ ($c = i$ in line L7, and $c = q$ in line L12 after the test of line L11). By induction on the order in which the points get the label $C$, each core point with label $C$ is joined to $i$ by a path in $G$: the new point $j$ is within $\varepsilon$ of the core point $c$, so $j$ and $c$ are adjacent in $G$ when $j$ is core, and $c$ is joined to $i$ by the induction hypothesis. Other runs never give the label $C$, because each run uses a new number.

*Step 4: a component gets one label.* Let $K$ be the component of $G$ that holds $i$. Assume that, when the run for $C$ ends, some core point of $K$ does not have the label $C$. Take a path in $G$ from $i$ to that point, and let $w$ be the first vertex on the path without the label $C$, with predecessor $v$. Then $v$ is core, has the label $C$, and was queried during this run (in line L4 if $v = i$, else in line L10 before the queue became empty). So CLAIM$(w)$ ran during this run. If $w$ was UNDEFINED or NOISE at that moment, it got the label $C$, which contradicts the choice of $w$. So $w$ already had a cluster label $C' \ne C$ from an earlier run. In that earlier run, $w$ got its label in line L6 or line L15, because line L14 only labels a point that line L5 found to be non-core, and $w$ is core. In both cases $w$ was queried in that earlier run (by Step 2) and found core, so CLAIM$(v)$ ran in the run for $C'$. At that moment $v$ was UNDEFINED or NOISE, because it later received the label $C$ and cluster labels are final. So $v$ got the label $C'$, a contradiction. Hence all of $K$ has the label $C$.

Steps 3 and 4 prove part 2: each label is the label of exactly the core points of one component, each run starts at an unlabeled core point, so it starts a component that has no label yet, and every core point is labeled by Step 2.

*Step 5: noise.* A point gets NOISE only in line L5, so it is not core. If a core point $c$ has $j \in N_\varepsilon(c)$, then by Step 2 the query of $c$ calls CLAIM$(j)$, which gives $j$ a cluster number unless it has one, and by Step 1 that number is final. So a point ends with NOISE if and only if it is not core and no core point has it in its neighborhood. Distance is symmetric, so this is the definition of noise. This proves part 3.

*Step 6: border points.* A border point $j$ ends with a cluster number by Step 5. That number came from CLAIM$(j)$, called on a point of $N_\varepsilon(c)$ for a core point $c$ that had that label at that moment, so $j$ is within $\varepsilon$ of a core point of that label. This proves part 4. Part 1 follows from Step 1 and Step 2. $\square$

**Termination and cost.** The outer loop runs $n$ times. Each point enters the queue at most once, so the inner loop runs at most $n$ times in total. So the algorithm makes exactly $n$ range queries, and CLAIM runs $\sum_p |N_\varepsilon(p)| \le n^2$ times over the core points. With brute force range queries, each query costs $\Theta(n d)$ in $\mathbb{R}^d$ with the Euclidean distance, and the total is $\Theta(n^2 d)$.

**What depends on the order.** Parts 2 and 3 do not mention the order of the input, so the core points, their partition into clusters and the noise are the same for each order. The number of a cluster and the cluster of a border point within $\varepsilon$ of two components can change with the order.
