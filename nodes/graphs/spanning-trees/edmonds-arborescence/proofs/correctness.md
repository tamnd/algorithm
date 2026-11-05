---
title: Edmonds' algorithm returns a minimum arborescence, or NONE exactly when no arborescence exists
proves: [correctness, termination]
status: full
---

Let $G = (V, A)$ be a finite directed graph with $n$ vertices, a root $r \in V$ and a real cost $c(a)$ on each arc. Parallel arcs, self-loops and negative costs are allowed, and costs may tie. An *arborescence* (rooted at $r$, spanning) is a set $T \subseteq A$ in which each vertex $v \ne r$ has exactly one entering arc, no arc enters $r$, and each vertex is reachable from $r$ along arcs of $T$. Such a $T$ has $n - 1$ arcs and no cycle.

We prove that EDMONDS (lines L1 to L10 of the page) stops, returns NONE exactly when $G$ has no arborescence, and otherwise returns an arborescence of least cost.

## Facts used

**Fact 1 (a test for arborescences).** A set $T$ in which each $v \ne r$ has exactly one entering arc and no arc enters $r$ is an arborescence if and only if $T$ has no cycle. Indeed, follow the entering arcs backwards from any $v$: the walk either reaches $r$, where it stops, or repeats a vertex, which gives a cycle. If $T$ has no cycle, every walk reaches $r$, so $v$ is reachable. If $T$ has a cycle $C$, no vertex of $C$ is reachable from $r$, because the only arc of $T$ into a vertex of $C$ is the arc of $C$, so a path from $r$ into $C$ would have to start inside $C$.

**Fact 2 (shifting the costs into one vertex).** For a vertex $v \ne r$ and a number $y$, replace $c(a)$ by $c(a) - y$ for each arc $a$ entering $v$. Each arborescence has exactly one arc entering $v$, so the cost of every arborescence drops by exactly $y$, and the set of optimal arborescences does not change.

## The cycle lemma

Fix one level of the recursion. For each $v \ne r$ let $\mathrm{in}[v]$ be the arc chosen at line L2: an arc of least cost among the arcs $(u, v)$ with $u \ne v$. Let $C$ be a cycle formed by these arcs, with vertex set $V_C$; $r \notin V_C$ since no chosen arc enters $r$.

**Lemma 1.** If $G$ has an arborescence, then it has an optimal arborescence $T^*$ with exactly one arc entering $V_C$ from outside, and $T^*$ contains $\mathrm{in}[w]$ for each $w \in V_C$ except the head of that arc.

*Proof.* By Fact 2, applied with $y = c(\mathrm{in}[v])$ at each $v \ne r$, we may assume that each chosen arc has cost 0 and every arc that is not a self-loop and does not enter $r$ has cost at least 0 (self-loops and arcs into $r$ are in no arborescence); the optimal arborescences are the same. Let $T$ be an optimal arborescence. In $T$, take a shortest path from $r$ to a vertex of $V_C$; its last arc is $(a, b)$ with $a \notin V_C$ and $b \in V_C$, and the path from $r$ to $a$ uses no vertex of $V_C$. Let

$$T^* = \bigl(T \setminus \{\text{arcs of } T \text{ entering } V_C\}\bigr) \cup \{(a, b)\} \cup \{\mathrm{in}[w] : w \in V_C, w \ne b\}.$$

Each $v \ne r$ has exactly one entering arc in $T^*$: for $v \notin V_C$ it is the arc of $T$; for $v = b$ it is $(a, b)$; for the other $w \in V_C$ it is $\mathrm{in}[w]$. Each vertex is reachable from $r$ in $T^*$. The path of $T$ from $r$ to $a$ enters only vertices outside $V_C$, so it is in $T^*$; then $(a, b)$ reaches $b$, and the arcs of $C$ other than $\mathrm{in}[b]$ form a path from $b$ through all of $V_C$. For $v \notin V_C$, take the path from $r$ to $v$ in $T$. If it meets $V_C$, let $z$ be its last vertex in $V_C$; the part after $z$ enters only vertices outside $V_C$, so it lies in $T^*$, and $z$ is reachable. If it does not meet $V_C$, the whole path lies in $T^*$. So $T^*$ is an arborescence. The arcs added have cost 0, and the arcs removed have cost at least 0, so $c(T^*) \le c(T)$ and $T^*$ is optimal. $\square$

## The contraction

Line L6 builds $G'$: the vertices of $V_C$ become one vertex $x$, arcs with both ends in $V_C$ are dropped, an arc $(u, v)$ with $v \in V_C$ and $u \notin V_C$ becomes $(u, x)$ of cost $c'(u, x) = c(u, v) - c(\mathrm{in}[v])$, and every other arc keeps its ends (with $x$ for an end in $V_C$) and its cost. The root of $G'$ is $r$. Each arc of $G'$ remembers the arc of $G$ it came from.

Call an arborescence $T$ of $G$ *$C$-shaped* when it has exactly one arc $(u, v)$ entering $V_C$ from outside and contains $\mathrm{in}[w]$ for each $w \in V_C \setminus \{v\}$.

**Lemma 2.** The map $\phi$ that sends a $C$-shaped arborescence $T$ of $G$ to the images in $G'$ of its arcs that do not have both ends in $V_C$ is a bijection onto the arborescences of $G'$, and

$$c(T) = c'(\phi(T)) + \sum_{w \in V_C} c(\mathrm{in}[w]).$$

*Proof.* Let $T$ be $C$-shaped with entering arc $(u, v)$. The arcs of $T$ inside $V_C$ are exactly the $|V_C| - 1$ arcs $\mathrm{in}[w]$, $w \ne v$, since each $w \in V_C$ has one entering arc and only $v$ gets it from outside. So $\phi(T)$ has $(n - 1) - (|V_C| - 1) = n' - 1$ arcs, where $n' = n - |V_C| + 1$. Each vertex of $G'$ other than $r$ has exactly one entering arc in $\phi(T)$: $x$ has the image of $(u, v)$, and other vertices keep their arc. Contracting a set of vertices maps a path of $T$ to a walk of $\phi(T)$, so every vertex of $G'$ is reachable from $r$, and $\phi(T)$ is an arborescence.

Conversely, let $T'$ be an arborescence of $G'$. Its arc into $x$ comes from an arc $(u, v)$ of $G$ with $v \in V_C$; let $\psi(T')$ be the set of the original arcs of $T'$ together with $\mathrm{in}[w]$ for $w \in V_C \setminus \{v\}$. Each $v' \ne r$ of $G$ has exactly one entering arc in $\psi(T')$. A path from $r$ to a vertex in $T'$ lifts to $G$: each time it passes through $x$ it enters $V_C$ at $v$ and can leave from any vertex of $V_C$, all of which $v$ reaches along $C \setminus \{\mathrm{in}[v]\}$. So $\psi(T')$ is a $C$-shaped arborescence, and $\phi$ and $\psi$ are inverse to each other.

For the costs: arcs not entering $V_C$ keep their cost, the arc $(u, v)$ has $c(u, v) = c'(u, x) + c(\mathrm{in}[v])$, and the arcs inside $V_C$ cost $\sum_{w \ne v} c(\mathrm{in}[w])$. Adding these gives the formula. $\square$

**Lemma 3.** $G$ has an arborescence if and only if $G'$ has one, and if $T'$ is an optimal arborescence of $G'$, then $\psi(T')$ is an optimal arborescence of $G$.

*Proof.* If $G$ has an arborescence, Lemma 1 gives a $C$-shaped one, and $\phi$ maps it to an arborescence of $G'$. If $G'$ has one, $\psi$ maps it to an arborescence of $G$. Now let $T'$ be optimal for $G'$ and let $T^*$ be the $C$-shaped optimal arborescence of Lemma 1. By Lemma 2, with $K = \sum_{w \in V_C} c(\mathrm{in}[w])$,

$$c(\psi(T')) = c'(T') + K \le c'(\phi(T^*)) + K = c(T^*),$$

so $\psi(T')$ is optimal. $\square$

## The theorem

**Theorem.** On every input, EDMONDS stops. It returns NONE if and only if $G$ has no arborescence rooted at $r$, and otherwise it returns a minimum-cost arborescence.

*Proof.* By induction on $n$. Each call either returns at line L3 or L4, or recurses on $G'$, which has $n - |V_C| + 1 \le n - 1$ vertices, because a cycle of chosen arcs has at least two vertices (self-loops are never chosen). So there are at most $n$ nested calls, and the algorithm stops.

*Return at line L3.* Some $v \ne r$ has no entering arc other than self-loops. Then no arborescence exists, and NONE is correct.

*Return at line L4.* Each $v \ne r$ has exactly one chosen arc, no chosen arc enters $r$, and the chosen arcs form no cycle, so by Fact 1 they form an arborescence $B$. Every arborescence $T$ has one arc into each $v \ne r$, which costs at least $c(\mathrm{in}[v])$, so $c(T) \ge c(B)$, and $B$ is optimal.

*Recursion at lines L5 to L10.* By the induction hypothesis the recursive call returns NONE exactly when $G'$ has no arborescence, which by Lemma 3 is exactly when $G$ has none; line L8 then returns NONE correctly. Otherwise it returns an optimal arborescence $T'$ of $G'$. Lines L9 and L10 find the arc $(u, v)$ of $G$ behind the arc of $T'$ into $x$ and return the arcs behind $T'$ together with $C \setminus \{\mathrm{in}[v]\}$, which is $\psi(T')$. By Lemma 3 it is an optimal arborescence of $G$. $\blacksquare$

**Ties.** Nothing above uses distinct costs: Lemma 1 works with any choice of cheapest arcs at line L2, so breaking ties by index is correct. With ties the optimum need not be unique, and the algorithm returns one optimum.
