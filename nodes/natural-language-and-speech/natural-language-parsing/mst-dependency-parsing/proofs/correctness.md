---
title: Chu-Liu-Edmonds returns a maximum spanning arborescence, and the parser returns a best dependency tree
proves: [correctness, termination]
status: full
---

Let $G$ be a directed graph with node set $V$, a root $\rho \in V$ and real arc scores $w(u, v)$, in which every node other than $\rho$ has at least one entering arc and no arc enters $\rho$. An **arborescence** of $G$ is a set $T$ of arcs that gives every $v \ne \rho$ exactly one entering arc, its head $h_T(v)$, such that the chain $v, h_T(v), h_T(h_T(v)), \ldots$ reaches $\rho$. Its score is $w(T) = \sum_{v \ne \rho} w(h_T(v), v)$. The claim is that $\mathrm{CLE}(V, \rho, w)$ returns an arborescence of largest score when one exists. For the parser, $V = \{0, \ldots, n\}$, $\rho = 0$, the graph is complete, and the arborescences are exactly the dependency trees.

**Lemma 1 (no cycle).** Let $B = \{best[v] \to v : v \ne \rho\}$ be the arcs of line L1. If $B$ has no cycle, $B$ is a maximum arborescence.

*Proof.* Each $v \ne \rho$ has one head in $B$. Follow the heads from $v$. The nodes are finite and no node repeats, because a repeat would be a cycle of $B$; the only node without a head is $\rho$, so the chain ends at $\rho$. So $B$ is an arborescence. Any arborescence $T$ has $w(h_T(v), v) \le w(best[v], v)$ for each $v$, so $w(T) \le w(B)$. $\square$

Now let $C$ be a cycle of $B$, found in line L2. Then $\rho \notin C$, because $\rho$ has no head in $B$. Write $S = \sum_{v \in C} w(best[v], v)$ and, for $v \in C$, $\delta(v) = S - w(best[v], v)$, the score of the arcs of $C$ other than the one into $v$.

**Lemma 2 (exchange).** Some maximum arborescence contains all the arcs of $C$ but one.

*Proof.* Let $T$ be a maximum arborescence. Let $v_0$ be a node of $C$ whose path in $T$ from $\rho$ contains no other node of $C$. Such a node exists: take any node of $C$, its path in $T$ from $\rho$, and the first node of $C$ on that path. Let $T'$ be $T$ with the head of every $v \in C$, $v \ne v_0$, changed to $best[v]$. Each node still has one head. Every node reaches $\rho$ in $T'$: the path from $\rho$ to $v_0$ in $T$ uses no node of $C$ other than $v_0$, so no head on it changed; each node of $C$ reaches $v_0$ along the cycle backwards, through heads $best[\cdot]$ that are in $T'$; and a node $x \notin C$ follows its chain in $T$, whose heads did not change until the chain meets $C$, if it does. So $T'$ is an arborescence. Each changed head became the best head of its node, so $w(T') \ge w(T)$, and $T'$ is maximum. $T'$ contains every arc of $C$ except possibly the one into $v_0$; it cannot contain that one too, since then $C$ would be a cycle in $T'$. $\square$

Let $\mathcal{A}_C$ be the set of arborescences of $G$ that contain all arcs of $C$ but one. Let $G'$ be the graph of line L5, on $V' = (V \setminus C) \cup \{c\}$, with the scores

$$w'(u, c) = \max_{v \in C} \big(w(u, v) + \delta(v)\big), \qquad w'(c, d) = \max_{v \in C} w(v, d), \qquad w'(u, d) = w(u, d)$$

for $u, d \notin C$, where a maximum is over the $v$ for which the arc exists. Note $w(u, v) - w(best[v], v) + S = w(u, v) + \delta(v)$. Every node of $V'$ other than $\rho$ has an entering arc in $G'$: a node $d \notin C$ keeps its entering arcs, with those from $C$ merged into one arc from $c$, and $c$ has an entering arc because some arc enters $C$ from outside (otherwise no node of $C$ could reach $\rho$ in $G$, and $G$ would have no arborescence; in the complete graph of the parser the root arcs always exist).

**Lemma 3 (contraction).** (a) Every $T \in \mathcal{A}_C$ maps to an arborescence $T'$ of $G'$ with $w'(T') \ge w(T)$. (b) Every arborescence $T'$ of $G'$ is mapped by lines L7 and L8 to some $T \in \mathcal{A}_C$ with $w(T) = w'(T')$.

*Proof.* (a) Let $T \in \mathcal{A}_C$ omit the arc of $C$ into $v_0$, and let $u = h_T(v_0)$. Then $u \notin C$: otherwise every node of $C$ would have its head in $C$, and the chains from the nodes of $C$ would never leave $C$ and never reach $\rho$. Replace the nodes of $C$ by $c$: the arc $u \to v_0$ becomes $u \to c$, each arc $v \to d$ with $v \in C$, $d \notin C$ becomes $c \to d$, and the arcs inside $C$ disappear. Every node of $V'$ other than $\rho$ gets one head, and chains to $\rho$ in $T$ map to chains in $T'$, so $T'$ is an arborescence. Its score is at least $w(u, v_0) + \delta(v_0) + \sum$ of the other arcs, because each $w'$ is a maximum over the choices that include the one $T$ made; and $w(T)$ is exactly $w(u, v_0) + \delta(v_0)$ plus the same other arcs. (b) Let $T'$ be an arborescence of $G'$ and let $u \to c$ be its arc into $c$. Line L7 replaces it by $u \to v_0$ for the $v_0 \in C$ that gave the maximum $w'(u, c)$, replaces each $c \to d$ by $v \to d$ for the $v$ that gave the maximum $w'(c, d)$, and keeps the other arcs. Line L8 gives every $v \in C \setminus \{v_0\}$ its head $best[v]$. Every node of $V$ other than $\rho$ now has one head. Every node reaches $\rho$: a node outside $C$ follows its chain in $T'$, reading $c$ as a passage through $C$, which works because each node of $C$ reaches $v_0$ along the cycle and $v_0$ goes to $u$. So $T$ is an arborescence in $\mathcal{A}_C$, and its score is $w(u, v_0) + \delta(v_0)$ plus the other arcs, which equals $w'(T')$ by the choice of the maximizers. $\square$

**Theorem 4.** $\mathrm{CLE}(V, \rho, w)$ returns a maximum arborescence of $G$.

*Proof.* By induction on $|V|$. If line L2 finds no cycle, Lemma 1 applies. Otherwise $|V'| = |V| - |C| + 1 < |V|$ because $|C| \ge 2$, so by induction line L6 returns a maximum arborescence $T'^\ast$ of $G'$. By Lemma 3(b) the returned $T$ is an arborescence with $w(T) = w'(T'^\ast)$. Let $T^\ast$ be a maximum arborescence of $G$ in $\mathcal{A}_C$, which exists by Lemma 2. By Lemma 3(a) it maps to an arborescence of $G'$ of score at least $w(T^\ast)$, so $w(T^\ast) \le w'(T'^\ast) = w(T)$. Hence $T$ is maximum. $\square$

**Termination.** Each call either returns at line L3 or makes one recursive call on a graph with fewer nodes, and every line does finite work. So there are at most $|V| - 1$ nested calls.

**Corollary 5 (the parser).** With $V = \{0, \ldots, n\}$, $\rho = 0$ and $w = s$ on all arcs $h \to d$, $d \ne 0$, $h \ne d$, CLE returns a highest scoring dependency tree. In the single-root version, run $m$ keeps only the root arc $0 \to m$; its arborescences are exactly the dependency trees whose only root child is $m$, every node still has an entering arc, and Theorem 4 gives the best of them. Every single-root tree is counted in exactly one run, so the best of the $n$ results is a best single-root tree. $\square$
