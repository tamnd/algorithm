---
title: T-VPack returns legal clusters that partition the netlist, each closed cluster is full or admits no further BLE, and the unit-delay criticalities are exact
proves: [correctness]
status: full
---

We use the notation of the page. The netlist is a list of $n$ BLEs. BLE $b$ has a set of input nets of size at most $K$, one output net, and a flag that says whether its flip-flop is used. For a set $C$ of BLEs, $\mathrm{ext}(C)$ is the set of nets that some member of $C$ reads and that no member of $C$ drives. A cluster $C$ is *legal* when $|C| \le N$ and $|\mathrm{ext}(C)| \le I$, which is the legality rule of a [logic cluster](/fpga-logic-cluster/) with a full crossbar. We assume $K \le I$, which the implementation checks.

**Lemma 1 (a single BLE is legal).** For every BLE $b$, $\{b\}$ is legal.

*Proof.* $|\{b\}| = 1 \le N$, and $\mathrm{ext}(\{b\})$ is a subset of the inputs of $b$, so $|\mathrm{ext}(\{b\})| \le K \le I$. $\square$

**Theorem 2 (legality and partition).** T-VPack stops, and its output is a list of legal clusters in which every BLE is in exactly one cluster.

*Proof.* Let $U$ be the set of unclustered BLEs and $C$ the open cluster. We show that the following invariant holds at line L3 each time it is tested: $C$ is legal, $C \cap U = \emptyset$, and $U$, $C$ and the clusters already output are pairwise disjoint with union the whole netlist.

At line L2 the seed is removed from $U$ and becomes $C$, so the sets stay disjoint with the same union, and $C$ is legal by Lemma 1. In the loop, line L5 keeps only BLEs $b \in U$ with $|\mathrm{ext}(C \cup \{b\})| \le I$. Line L8 runs only when line L3 has found $|C| < N$, so after it $|C \cup \{b\}| \le N$. So $C \cup \{b\}$ is legal, and moving $b$ from $U$ to $C$ keeps the sets disjoint with the same union. Line L9 outputs $C$, which is legal, and the next cluster starts with a new seed from $U$.

Each pass of the inner loop either adds a BLE (line L8) or leaves it (line L7), and $|C|$ grows by one per addition, so the inner loop ends after at most $N - 1$ additions. Each pass of the outer loop removes at least the seed from $U$, so the outer loop ends after at most $n$ passes. When it ends, $U = \emptyset$, so by the invariant the output clusters are disjoint and cover all BLEs. $\square$

**Theorem 3 (closed clusters are maximal).** When line L9 outputs $C$, either $|C| = N$, or for every BLE $b$ that is still unclustered at that time, $|\mathrm{ext}(C \cup \{b\})| > I$.

*Proof.* The inner loop ends in one of two ways. Line L3 fails, which means $|C| = N$. Or line L7 finds no kept BLE, which means that line L5 skipped every $b \in U$, that is, $|\mathrm{ext}(C \cup \{b\})| > I$ for each of them. $\square$

The set of BLEs that are unclustered when $C$ is closed is exactly the set of BLEs that later clusters hold, so Theorem 3 says that no BLE of a later cluster could have joined $C$. It does not say that the number of clusters is least: the page gives a netlist on which T-VPack uses 3 clusters and 2 suffice.

**Unit-delay criticality.** Call BLE $u$ *combinational* if its flip-flop is not used. A *connection* is a pair $(u, v)$ where $v$ reads the output net of $u$. A *timing path* is a sequence $v_1, \ldots, v_r$ of BLEs with $r \ge 1$ in which each $(v_j, v_{j+1})$ is a connection and $v_1, \ldots, v_{r-1}$ are combinational. It starts at a primary input or at a flip-flop and passes through the LUTs of $v_1, \ldots, v_r$. Its delay is $r$, one unit per LUT. We assume that the combinational connections form a directed acyclic graph $H$, which is the usual condition that every cycle passes through a flip-flop. Let $D$ be the largest delay of a timing path. For a connection $(u, v)$, let $\ell(u, v)$ be the largest delay of a timing path that uses it.

Define $\mathrm{to}(v)$ as the largest $r$ of a timing path that ends at $v$, and $\mathrm{from}(v)$ as the largest number of BLEs of a timing path that starts with the LUT of $v$; so $\mathrm{from}(v) = 1$ if $v$ is registered, and otherwise $1$ plus the largest $\mathrm{from}(w)$ over connections $(v, w)$, or $1$ if there is none.

**Lemma 4.** The arrays of the implementation satisfy $\mathrm{arrival}[v] = \mathrm{to}(v)$, $D = \max_v \mathrm{arrival}[v]$, and $\mathrm{required}[v] = D - \mathrm{from}(v) + 1$.

*Proof.* The depth-first search follows only edges from combinational BLEs, which are the edges of $H$, and appends a node after all its predecessors in $H$, so the order is a [topological order](/topological-sort/) of $H$. A timing path that ends at $v$ is either $v$ alone or a timing path that ends at a combinational predecessor $u$ followed by $v$. So $\mathrm{to}(v) = 1 + \max \mathrm{to}(u)$ over the combinational $u$ with $(u, v)$ a connection, or $1$ if there is none. The code computes exactly this recurrence in topological order, so $\mathrm{arrival}[v] = \mathrm{to}(v)$ by induction along the order. Every timing path has its delay as the $\mathrm{to}$ of its last BLE, so $D = \max_v \mathrm{to}(v)$.

For the required times, the code sets $\mathrm{required}[u] = D$ and lowers it to $\mathrm{required}[v] - 1$ for each combinational connection $(u, v)$, in reverse topological order. When $u$ is combinational, its readers $v$ come after it in the order, so by induction $\mathrm{required}[u] = \min(D, \min_v (D - \mathrm{from}(v)))$ over the connections $(u, v)$. This is $D - \max_v \mathrm{from}(v)$ if $u$ has a reader and $D$ if not, which in both cases is $D - (\mathrm{from}(u) - 1)$. A registered $u$ has no outgoing edge in $H$, so $\mathrm{required}[u] = D = D - \mathrm{from}(u) + 1$. $\square$

**Theorem 5 (criticality).** For every connection $(u, v)$, the implementation returns $\mathrm{crit}(u, v) = \ell(u, v) / D$. So $0 < \mathrm{crit}(u, v) \le 1$, with $\mathrm{crit}(u, v) = 1$ if and only if the connection is on a timing path of delay $D$.

*Proof.* A timing path through $(u, v)$ is a part that ends at $u$ and a part that starts with $v$. If $u$ is combinational, the first part is a timing path that ends at $u$, so $\ell(u, v) = \mathrm{to}(u) + \mathrm{from}(v)$. If $u$ is registered, the path through $(u, v)$ starts at the flip-flop of $u$, so $\ell(u, v) = \mathrm{from}(v)$. The code sets $\mathrm{start} = \mathrm{arrival}[u]$ in the first case and $0$ in the second, and

$$\mathrm{slack} = \mathrm{required}[v] - 1 - \mathrm{start} = D - \mathrm{from}(v) - \mathrm{start} = D - \ell(u, v)$$

by Lemma 4. So $1 - \mathrm{slack} / D = \ell(u, v) / D$. Since $1 \le \ell(u, v) \le D$, the value lies in $(0, 1]$. $\blacksquare$
