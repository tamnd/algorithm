---
title: Yao's algorithm returns the minimum spanning forest in O(m log log n) time
proves: [correctness, termination, complexity]
status: full
---

**Claim.** Let $G = (V, E)$ be a finite undirected multigraph with $n$ vertices, $m$ edges and real weights; self-loops, parallel edges, ties and several components are allowed. Order the edges by the key $(w(e), \text{index of } e)$. Then YAO-MST stops and returns the unique minimum spanning forest $F^\ast$ for this order, which is a minimum spanning forest for $w$. It runs in $O(m \log \log n + n)$ time.

## Facts used

**Uniqueness.** All keys are distinct, so the minimum spanning forest for the keys is unique; call it $F^\ast$. A forest of least total key order is also of least total weight for $w$, because the weight order is a coarsening of the key order: Kruskal's algorithm with the key order is a valid run of Kruskal's algorithm for $w$.

**Cut property.** If $S$ is the vertex set of a component of a forest $F \subseteq F^\ast$, and $e$ is the edge of least key with exactly one end in $S$, then $e \in F^\ast$. *Proof.* If $e \notin F^\ast$, the path in $F^\ast$ between the ends of $e$ crosses from $S$ to $V \setminus S$ by some edge $f \ne e$, and $f$ has a larger key than $e$. Then $F^\ast - f + e$ is a spanning forest with the same components and a smaller key sum, which is impossible. $\square$

## Invariant

**Invariant I.** At the start of each phase of line L2 and of each pass of line L7, $F \subseteq F^\ast$, and the components of the disjoint-set structure are the components of $(V, F)$.

It holds at line L1, where $F = \emptyset$. In one phase, every chosen edge $e_C$ is the least key edge that leaves the component $C$; this is immediate in line L2, and in line L13 it is Lemma 1 below. By the cut property, every chosen edge is in $F^\ast$. So $F$ together with all chosen edges is a subset of the forest $F^\ast$, and adding them one by one never closes a cycle; line L13 skips an edge only when its ends are already merged, which happens only when two components chose the same edge. Merging along the added edges keeps the second part of the invariant.

## Lemma 1: line L11 finds the least leaving edge at v

**Lemma 1.** At line L11, if $v$ has an edge to another component, then $e_v$ exists and is the least key edge at $v$ that leaves the component of $v$. Otherwise $e_v$ does not exist.

*Proof.* Two facts hold for all $v$ at all times.

(a) Every edge that was removed from a group of $v$ had both ends in one component when it was removed, and components only merge, so it still has both ends in one component.

(b) The groups $L(v, 1), \ldots, L(v, c(v) - 1)$ hold no edge that leaves a component. Indeed, $c(v)$ grows only in line L10, after $L(v, c(v))$ became empty by removals, so every edge that was ever in these groups was removed, and by (a) it does not leave a component.

After line L10, either $L(v, c(v))$ is nonempty and holds only edges that leave the component of $v$ (the inner ones were just removed), or $c(v) = k$ and the group is empty. In the first case, let $e$ be the least key edge at $v$ that leaves the component. By (b), $e$ is not in a group before $c(v)$. Every key in $L(v, c(v))$ is below every key in later groups, by line L5, and $L(v, c(v))$ contains a leaving edge, so $e$ is not in a later group either. So $e \in L(v, c(v))$, and it is the least edge there. In the second case, all groups are empty or hold no leaving edge, by (b) and the emptiness of the last group, so $v$ has no leaving edge. $\square$

So $e_C$ in line L12, the least of $e_v$ over the vertices $v$ of $H$ inside $C$, is the least key edge that leaves $C$: every edge of $G$ that leaves $C$ is an edge of $H$ at some vertex of $H$ inside $C$, since $H$ keeps all edges between different components after line L2.

## Termination and the result

Each pass of lines L7 to L13 in which some component has a leaving edge adds at least one edge to $F$, and $F \subseteq F^\ast$ has at most $n - 1$ edges, so the loop stops. When it stops, no edge leaves any component. Then the components of $(V, F)$ are the components of $G$, so $F$ is a spanning forest with $n - c$ edges, where $c$ is the number of components of $G$. Also $F \subseteq F^\ast$ and $|F^\ast| = n - c$, so $F = F^\ast$.

## Running time

Let $p = \lceil \log_2 \log_2 n \rceil$. Each plain Borůvka phase costs $O(n + m)$. In each phase, each component that has a leaving edge merges with at least one other, so after $p$ phases each component with a leaving edge has at least $2^p \ge \log_2 n$ vertices, and $H$ has $n' \le n / \log_2 n$ vertices with edges. The cost of line L2 is $O((n + m) \log \log n)$.

Line L5 on a list of $d$ edges uses $\lceil \log_2 k \rceil$ levels of splitting, and each level selects one rank in each part and splits it, which costs $O(d)$ by linear-time selection. So lines L4 to L6 cost $O(m \log k) = O(m \log \log n)$, as $k \le \log_2 n + 1$. Each group has at most $\lceil d/k \rceil + 1$ edges.

In lines L7 to L13, each pass at least halves the number of components that have a leaving edge, so there are at most $\lfloor \log_2 n' \rfloor + 1$ passes. In one pass, vertex $v$ reads its current group and every group it empties. Each edge is removed from each of its two lists at most once, so removals cost $O(m)$ over the whole run. Reading the final current group costs $O(d(v)/k + 1)$, so a pass costs $O(m/k + n')$ apart from removals. Over all passes this is $O((m/k + n') \log n') = O(m + n)$, since $k \ge \log_2 n'$ and $n' \log_2 n' \le n$.

The total is $O(m \log \log n + n)$. $\blacksquare$
