---
title: FlowMap labels are the least LUT depths, and the mapping reaches them
proves: [correctness]
status: full
---

Let $N$ be a $K$-bounded network: a directed acyclic graph whose sources are the primary inputs (PIs), in which every gate has between 1 and $K$ fanins. For a node $t$, $N_t$ is the cone of $t$, the set of nodes from which $t$ can be reached, $t$ included. A cut of $t$ is a set of nodes that meets every path from a PI to $t$. Let $\mathcal{C}(t)$ be the set of cuts $C$ of $t$ with $|C| \le K$ and $t \notin C$. Define
$$d(t) = 0 \text{ for a PI}, \qquad d(t) = \min_{C \in \mathcal{C}(t)} h(C), \quad h(C) = 1 + \max_{u \in C} d(u),$$
for a gate. The set of fanins of a gate is in $\mathcal{C}(t)$, so the minimum exists.

**Lemma 1 (d is the least depth).** In every mapping, the LUT network has depth at least $d(t)$ at each LUT root $t$, and the mapping that uses at each needed gate a cut $C_t \in \mathcal{C}(t)$ with $h(C_t) = d(t)$ has depth exactly $d(t)$ at $t$.

*Proof.* The inputs of the LUT of $t$ are PIs or LUT roots, and the LUT computes $t$ from them for all inputs of the network, so they form a cut of $t$; the cut does not contain $t$ and has at most $K$ nodes, so it is in $\mathcal{C}(t)$. By induction on the topological order, each LUT input $u$ has depth at least $d(u)$, so $t$ has depth at least $h(C_t) \ge d(t)$. For the second claim, the same induction gives depth $1 + \max_{u \in C_t} d(u) = d(t)$. $\square$

**Lemma 2 (d is monotone).** If $u \in N_t$, then $d(u) \le d(t)$.

*Proof.* Induction on the topological order of $t$. For $t = u$, or for a PI $u$ with $d(u) = 0$, it is clear. Let $u \ne t$ be a gate, so $t$ is a gate too, and let $C \in \mathcal{C}(t)$ with $h(C) = d(t)$. There are two cases.

If some path $Q$ from $u$ to $t$ avoids $C$, then $C$ is a cut of $u$: a path $P$ from a PI to $u$, followed by $Q$, meets $C$, and not on $Q$, so $P$ meets $C$. Also $u \notin C$. So $C \in \mathcal{C}(u)$ and $d(u) \le h(C) = d(t)$.

Otherwise every path from $u$ to $t$ meets $C$. Take one, and let $w$ be its first node in $C$. Then $u \in N_w$, $w$ comes before $t$, and by induction $d(u) \le d(w) \le h(C) - 1 < d(t)$. $\square$

**Lemma 3 (two values).** Let $t$ be a gate and $p = \max d(u)$ over its fanins $u$. Then $p \le d(t) \le p + 1$. If $p = 0$, then $d(t) = 1$.

*Proof.* Each fanin is in $N_t$, so $p \le d(t)$ by Lemma 2. The fanin set is in $\mathcal{C}(t)$ and has $h = p + 1$. If $p = 0$, then $d(t) \ge 1$ because $h(C) \ge 1$ for every $C$. $\square$

So for $p \ge 1$, $d(t) = p$ exactly when some $C \in \mathcal{C}(t)$ has $d(u) \le p - 1$ for all $u \in C$. Let $H = \{t\} \cup \{w \in N_t \setminus \{t\} : d(w) = p\}$, the set merged at line L5. By Lemma 2, every $w \in N_t \setminus \{t\}$ has $d(w) \le p$, since $w$ is in the cone of some fanin of $t$.

**Lemma 4 (cuts of low label are the separators of H).** Let $p \ge 1$ and let $C$ be a set of nodes of $N_t \setminus H$. Then $C$ is a cut of $t$ if and only if $C$ meets every path in $N_t$ from a PI to a node of $H$.

*Proof.* If $C$ meets every path to a node of $H$, it meets every path to $t \in H$. Conversely, let $C$ be a cut of $t$ and $P$ a path from a PI to $w \in H$. Extend $P$ by a path from $w$ to $t$. The extended path meets $C$. Every node $x$ on the extension, after $w$, has $w \in N_x$, so $d(x) \ge d(w) = p$ by Lemma 2 (or $x = t$), so $x \in H$ and $x \notin C$. Hence $P$ meets $C$. $\square$

**Lemma 5 (the flow test).** Let $p \ge 1$ and let $F$ be the network of line L6. The max flow from $s$ to $t'$ is the least size of a set $C \subseteq N_t \setminus H$ that meets every path from a PI to $H$. If the flow is at most $K$, the set of line L8 is such a set of size equal to the flow.

*Proof.* A path from $s$ to $t'$ in $F$ is $s \to w^1_{in} \to w^1_{out} \to \cdots \to t'$, where $w^1$ is a PI and $w^1, w^2, \ldots$ is a path of $N_t$ to a node of $H$, and conversely. An $s$-$t'$ edge cut of finite capacity uses only split edges $w_{in} \to w_{out}$, which have capacity 1, and a set of split edges is an $s$-$t'$ cut exactly when the set of their nodes meets every path from a PI to $H$. So the least finite cut capacity is the least size of such a node set. A finite cut exists, for example the split edges of all PIs. By the [max-flow min-cut theorem](/max-flow-min-cut-theorem/), the max flow equals this least size.

For the second claim, let $R$ be the set of nodes of $F$ reachable from $s$ in the residual graph of a max flow. Then $t' \notin R$, and the edges from $R$ to the rest are saturated, and they form a min cut. An edge of capacity $\infty$ cannot be saturated by a finite flow, so every edge leaving $R$ is a split edge $w_{in} \to w_{out}$ with $w_{in} \in R$ and $w_{out} \notin R$. These $w$ are the nodes of line L8, and their number is the cut capacity, which equals the flow. The code stops after $K + 1$ augmenting paths: if the search finds no path before that, the flow is maximum, and if it finds $K + 1$, the max flow is more than $K$. $\square$

**Theorem.** FLOWMAP sets $\ell(t) = d(t)$ for every node, and every $C_t$ is in $\mathcal{C}(t)$ with $h(C_t) = d(t)$. The returned mapping has depth $\max_o d(o)$ over the outputs, the least depth of any mapping.

*Proof.* Induction on the topological order. For a PI, line L1 sets $\ell = 0 = d$. Let $t$ be a gate, and assume $\ell(u) = d(u)$ for all nodes before $t$. Then the value $p$ of line L3 is the $p$ of Lemma 3, and the merged set of line L5 is $H$.

If $p = 0$, line L4 sets $\ell(t) = 1 = d(t)$ by Lemma 3, and the fanin set has $h = 1$.

If $p \ge 1$ and the flow is at most $K$, Lemma 5 gives a set $C_t \subseteq N_t \setminus H$ of at most $K$ nodes that meets every path from a PI to $H$. By Lemma 4 it is a cut of $t$. It avoids $H$, so each of its nodes has $d \le p - 1$, and $t \notin C_t$. So $C_t \in \mathcal{C}(t)$ and $h(C_t) \le p$, and with Lemma 3, $d(t) = p = \ell(t)$ and $h(C_t) = p$.

If $p \ge 1$ and the flow is more than $K$, suppose $d(t) = p$. Then some $C \in \mathcal{C}(t)$ has only nodes of $d \le p - 1$. Remove from $C$ the nodes outside $N_t$; the rest is still a cut of $t$, it lies in $N_t \setminus H$, and by Lemma 4 it meets every path from a PI to $H$. By Lemma 5 the flow is at most $|C| \le K$, a contradiction. So $d(t) = p + 1$ by Lemma 3, which is the value of line L10, and the fanin set has $h = p + 1$.

For the mapping phase, line L13 makes a LUT for $t$ over $C_t$, which computes $t$ because a node is a function of each of its cuts. Every gate of $C_t$ gets a LUT in turn, so the LUT network is complete, and by the second part of Lemma 1 the depth at each LUT root $t$ is $h(C_t) = d(t)$. By the first part of Lemma 1, no mapping has smaller depth at any output. $\blacksquare$

**Running time.** At one gate, $F$ has $O(|N_t|)$ nodes and $O(m)$ edges, and each breadth-first augmenting path costs $O(m)$. Line L7 uses at most $K + 1$ paths, so the labeling costs $O(K m)$ per gate and $O(K m n)$ in all.
