---
title: The cut weight of the Schism graph is an upper bound on the number of distributed transactions
proves: [correctness, termination]
status: full
---

We use the line numbers of the pseudocode on the page. A workload is a list of transactions $x_1, \dots, x_m$. Transaction $x$ reads the set $R(x)$ and writes the set $W(x)$ of tuples, with $R(x) \cap W(x) = \emptyset$, and touches $T(x) = R(x) \cup W(x)$. A placement $P$ maps each tuple $t$ to a nonempty set $P(t)$ of parts. Transaction $x$ is *local* under $P$ if there is a part $p$ with $p \in P(t)$ for every $t \in T(x)$ and $P(t) = \{p\}$ for every $t \in W(x)$; otherwise $x$ is *distributed*. The definition says that a read can use any copy, and that a write must reach every copy.

For a partition $\pi$ of the nodes of a graph with edge weights $w$, the cut weight is $\mathrm{cut}(\pi) = \sum w(e)$ over the edges $e$ whose ends are in different parts. The statements below hold for every partition, so they hold for the partition of line L3 whatever partitioner computes it. They do not say that the partitioner finds a small cut: METIS, and the multilevel search of the implementation, are heuristics.

**The graph without replication (line L1).** It has a node for each touched tuple and, for two tuples $t \ne t'$, an edge of weight $w(t, t') = |\{x : t, t' \in T(x)\}|$. The placement of line L4 is $P(t) = \{\pi(t)\}$.

**Theorem 1.** For every partition $\pi$ of the graph of line L1, the number of distributed transactions under $P$ is at most $\mathrm{cut}(\pi)$. If every transaction touches at most two tuples, the two numbers are equal.

*Proof.* Every tuple has one copy, so $x$ is local exactly when all of $T(x)$ lies in one part. Let $x$ be distributed. Then $T(x)$ has two tuples in different parts, and we charge $x$ to the first such pair $\{t, t'\}$ in a fixed order. The edge $\{t, t'\}$ is cut. The transactions charged to it all touch both $t$ and $t'$, so there are at most $w(t, t')$ of them. Summing over the cut edges gives the bound. If every transaction touches at most two tuples, a cut edge $\{t, t'\}$ stands for exactly $w(t, t')$ transactions with $T(x) = \{t, t'\}$, and each of them is distributed; a transaction with one tuple adds no edge and is local. So each cut edge stands for exactly its weight in distributed transactions, and no distributed transaction is missed. $\square$

The bound can be loose: a transaction that touches $d$ tuples spread over two parts can cut up to $d^2/4$ of its own edges and still counts as one distributed transaction. This is why the cut is a proxy for the cost, and why line L6 counts the distributed transactions directly.

**The graph with replication (line L2).** Let $u(t) = |\{x : t \in W(x)\}|$, the number of transactions that write $t$. For each tuple $t$ there is a center $c_t$ and, for each transaction $x$ that touches $t$, a replica $r_{t,x}$. The star edge $\{c_t, r_{t,x}\}$ has weight $u(t)$, and it is left out when $u(t) = 0$. For each transaction $x$ and two tuples $t \ne t'$ in $T(x)$, the edge $\{r_{t,x}, r_{t',x}\}$ has weight 1. The placement of line L4 is $P(t) = \{\pi(c_t)\} \cup \{\pi(r_{t,x}) : t \in T(x)\}$, the parts of the star of $t$.

**Theorem 2.** For every partition $\pi$ of the graph of line L2, the number of distributed transactions under $P$ is at most $\mathrm{cut}(\pi)$.

*Proof.* First we show: if all replicas $r_{t,x}$ with $t \in T(x)$ lie in one part $p$, and for each $t \in W(x)$ the star of $t$ lies in one part, then $x$ is local. For $t \in T(x)$, $r_{t,x}$ is in $p$, so $p \in P(t)$. For $t \in W(x)$, the star of $t$ lies in one part, which holds $r_{t,x}$, so it is $p$, and $P(t) = \{p\}$.

So a distributed transaction $x$ has one of two defects. (a) Its replicas lie in at least two parts. The replicas of $x$ are joined by a complete graph of edges of weight 1 that belong to $x$ alone, so one of these edges is cut. Charge $x$ to it. (b) Its replicas lie in one part, but some $t \in W(x)$ has a star that lies in at least two parts. Then $u(t) \ge 1$, the star is connected, and one of its edges is cut. For each tuple $t$, fix one cut star edge $e_t$ if there is one, and charge $x$ to $e_{t}$ for the first such $t$. A weight 1 edge of (a) gets at most one charge. A star edge $e_t$ gets charges only from transactions that write $t$, so at most $u(t) = w(e_t)$ charges. Each distributed transaction is charged once, and only cut edges get charges, so the number of distributed transactions is at most $\mathrm{cut}(\pi)$. $\square$

A cut star edge also has a meaning of its own: if a replica of $t$ is in a different part from the center, the tuple has a second copy, and each of the $u(t)$ writes of $t$ must update it. A tuple that no transaction writes has no star edges, so its copies are free in the cut; this is why the partitioner can copy read-only tuples to every part that reads them.

**Corollary.** If $\mathrm{cut}(\pi) = 0$, every transaction of the workload is local under the placement of line L4. In particular, if the workload splits into $k$ groups of transactions that share no written tuple and touch only their own tuples apart from read-only ones, and a balanced partition with a zero cut exists, then a perfect partitioner gives a placement with no distributed transaction.

**The candidates of line L6.** Line L6 evaluates every candidate placement with the definition of a local transaction, and line L7 returns one with the fewest distributed transactions (the simplest one on a tie, in the order hash, replication, tree, lookup). So the chosen placement is never worse, on the training workload, than hash partitioning or full replication. Under full replication with $k \ge 2$ parts, a transaction is local exactly when it writes nothing, since a written tuple has $k \ge 2$ copies. On a different workload than the training one, these comparisons need not hold.

**The decision tree of line L5.** Each split has two nonempty sides, so the recursion ends after at most $n - 1$ splits for $n$ training tuples. An impure node is split whenever two of its rows differ in some attribute, so when the training rows are pairwise distinct every leaf is pure and the tree predicts the label of line L4 for every training tuple. With a depth limit, or with equal rows of different labels, the tree can differ from the lookup table; line L6 measures the effect.

**Termination.** The graphs are finite. The local search of the partitioner applies only steps that lower the cut, which is a non-negative integer, so it ends. Coarsening stops when a level removes fewer than a tenth of the nodes, so the number of levels is finite. The tree ends as shown above. $\square$
