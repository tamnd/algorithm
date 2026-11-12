---
title: Bayes-Ball marks on the bottom exactly the nodes that an active trail reaches
proves: [correctness]
status: full
---

We use the pseudocode of the page. The DAG is $G = (V, E)$, the query set is $J$, the evidence set is $K$, and $J \cap K = \emptyset$. There are no functional nodes. A *visit* is a pair $(v, \uparrow)$ (the ball comes to $v$ from a child) or $(v, \downarrow)$ (from a parent). An *active trail given $K$* is defined on the [d-separation query](/d-separation-query/) page, and $\mathrm{An}(K)$ is $K$ with all ancestors of nodes of $K$.

**Claim.** A node $y \notin K$ is marked on the bottom if and only if $y \in J$ or an active trail given $K$ joins a node of $J$ to $y$. So $Y \cap \text{bottom} = \emptyset$ exactly when $J$ and $Y$ are d-separated given $K$.

*Step 1: the ball explores a fixed state graph.* Let $H$ be the directed graph on the visits with these arcs:

- from $(v, \uparrow)$ with $v \notin K$: to $(p, \uparrow)$ for each $p \in \mathrm{Pa}(v)$, and to $(c, \downarrow)$ for each $c \in \mathrm{Ch}(v)$;
- from $(v, \downarrow)$ with $v \in K$: to $(p, \uparrow)$ for each $p \in \mathrm{Pa}(v)$;
- from $(v, \downarrow)$ with $v \notin K$: to $(c, \downarrow)$ for each $c \in \mathrm{Ch}(v)$;
- no arc leaves $(v, \uparrow)$ with $v \in K$.

The top mark of $v$ is set at the first visit that sends the ball to all parents (line L5 for $v \notin K$, line L8 for $v \in K$), and the bottom mark of $v \notin K$ is set at the first visit that sends it to all children (lines L6 and L9). A later visit that would send the same set of balls finds the mark set and sends nothing. So every arc of $H$ out of a visit that occurs is followed once, and the visits that occur are exactly the visits reachable in $H$ from the start visits $(j, \uparrow)$, $j \in J$. A node $v \notin K$ is marked on the bottom exactly when some visit to $v$ occurs, since each visit of either kind to $v \notin K$ reaches line L6 or line L9.

*Step 2: comparison with the reachable set algorithm.* Let $H'$ be the state graph of REACHABLE on the [d-separation query](/d-separation-query/) page: it has the same arcs as $H$, except that from $(v, \downarrow)$ it goes to $(p, \uparrow)$ for $p \in \mathrm{Pa}(v)$ whenever $v \in \mathrm{An}(K)$, and from $(v, \uparrow)$ with $v \in K$ it has no arc. Koller and Friedman (Section 3.3.3) prove that the nodes $y \notin K$ reached in $H'$ from the visits $(j, \uparrow)$ are exactly $J$ and the nodes joined to $J$ by an active trail. We show that $H$ and $H'$ reach the same nodes outside $K$.

*$H'$ reaches everything $H$ reaches.* We prove by induction on the length of a walk in $H$ from a start visit that each visit $(v, d)$ on it satisfies (P): $H'$ reaches $(v, d)$, or $d = {\uparrow}$, $v \in \mathrm{An}(K)$ and $H'$ reaches $(v, \downarrow)$. A start visit is reached in $H'$. Take an arc of $H$ out of a visit that satisfies (P).

- Out of $(v, \uparrow)$, $v \notin K$. If $H'$ reaches $(v, \uparrow)$, it has the same arcs. Otherwise $v \in \mathrm{An}(K)$ and $H'$ reaches $(v, \downarrow)$; there $H'$ has the arcs to $(c, \downarrow)$ because $v \notin K$, and the arcs to $(p, \uparrow)$ because $v \in \mathrm{An}(K)$.
- Out of $(v, \downarrow)$, $v \in K$. By (P), $H'$ reaches $(v, \downarrow)$, and $v \in K \subseteq \mathrm{An}(K)$ gives the same arcs to the parents.
- Out of $(v, \downarrow)$, $v \notin K$. $H'$ reaches $(v, \downarrow)$ and has the same arcs to the children.

In each case the new visit satisfies (P). A visit that satisfies (P) has its node reached in $H'$.

*$H$ reaches everything $H'$ reaches.* We show by induction on walks in $H'$ that $H$ reaches each visit that $H'$ reaches. The start visits agree. The arcs of $H'$ out of $(v, \uparrow)$ with $v \notin K$, out of $(v, \downarrow)$ to the children, and out of $(v, \downarrow)$ with $v \in K$ to the parents are also arcs of $H$. The one remaining arc goes from $(v, \downarrow)$ with $v \in \mathrm{An}(K) \setminus K$ to $(p, \uparrow)$. Then a directed path $v = w_0 \to w_1 \to \cdots \to w_m$ with $w_m \in K$ exists; cut it at its first node in $K$, so $w_0, \ldots, w_{m-1} \notin K$ and $m \ge 1$. In $H$ the ball goes $(w_0, \downarrow) \to (w_1, \downarrow) \to \cdots \to (w_m, \downarrow)$ through nodes outside $K$, then from $(w_m, \downarrow)$ with $w_m \in K$ up to $(w_{m-1}, \uparrow)$, then up through $(w_{m-2}, \uparrow), \ldots, (w_0, \uparrow)$, since each $w_t \notin K$ passes the ball to its parents. From $(v, \uparrow) = (w_0, \uparrow)$ with $v \notin K$, $H$ has the arc to $(p, \uparrow)$.

So $H$ and $H'$ reach the same nodes, and the claim follows from Step 1 and the theorem of Koller and Friedman. $\square$

**Cost.** Each node gets its top mark at most once and its bottom mark at most once. Setting the top mark of $v$ schedules $|\mathrm{Pa}(v)|$ visits and setting the bottom mark schedules $|\mathrm{Ch}(v)|$ visits. So the number of visits is at most $|J| + \sum_v |\mathrm{Pa}(v)| + \sum_v |\mathrm{Ch}(v)| = |J| + 2|E|$, and each visit takes $O(1)$ time besides the visits it schedules. With adjacency lists, the run takes $O(|V| + |E|)$ time and $O(|V| + |E|)$ memory for the queue and the marks. $\square$
