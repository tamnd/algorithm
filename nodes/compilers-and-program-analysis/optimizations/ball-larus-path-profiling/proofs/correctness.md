---
title: Ball-Larus path numbers are a bijection, and the chord placement keeps them
proves: [correctness]
status: full
---

**Setting.** $G = (V, E)$ is a finite directed acyclic multigraph with two nodes ENTRY and EXIT. EXIT has no out-edges, ENTRY reaches every node, and every node reaches EXIT. A *path from $v$* is a directed path from $v$ to EXIT, given as a list of edges. $P(v)$ is the set of paths from $v$, and $\mathrm{num}(v)$ and $\mathrm{Val}(e)$ are computed by lines L1 to L7 of the algorithm. For a path $p$, $\mathrm{Val}(p) = \sum_{e \in p} \mathrm{Val}(e)$.

**Lemma 1.** For every node $v$, $\mathrm{num}(v) = |P(v)| \ge 1$, and the map $p \mapsto \mathrm{Val}(p)$ is a bijection from $P(v)$ onto $\{0, 1, \ldots, \mathrm{num}(v) - 1\}$.

*Proof.* Induction along the reverse topological order used in L1. When $v$ is processed, every successor $w$ of $v$ has been processed, because $v$ comes before $w$ in the topological order.

For $v = \mathrm{EXIT}$, $P(v)$ holds only the empty path, whose sum is 0, and $\mathrm{num}(v) = 1$.

Let $v \ne \mathrm{EXIT}$ with out-edges $e_1 = v \to w_1, \ldots, e_k = v \to w_k$ in the order of L5. Since $v$ reaches EXIT, $k \ge 1$. By L6 and L7, $\mathrm{Val}(e_i) = s_i$ with $s_1 = 0$ and $s_{i+1} = s_i + \mathrm{num}(w_i)$, and $\mathrm{num}(v) = s_{k+1} = \sum_i \mathrm{num}(w_i)$. Every path from $v$ is $e_i$ followed by a path $q$ from $w_i$, for exactly one $i$ and one $q$, so $|P(v)| = \sum_i |P(w_i)| = \mathrm{num}(v)$ by induction. For such a path, $\mathrm{Val}(e_i q) = s_i + \mathrm{Val}(q)$. By induction $\mathrm{Val}(q)$ ranges bijectively over $\{0, \ldots, \mathrm{num}(w_i) - 1\}$, so the paths through $e_i$ map bijectively onto the block $B_i = \{s_i, \ldots, s_{i+1} - 1\}$. The blocks $B_1, \ldots, B_k$ are disjoint and their union is $\{0, \ldots, s_{k+1} - 1\}$, since each starts where the previous one ends. Hence the map is a bijection from $P(v)$ onto $\{0, \ldots, \mathrm{num}(v) - 1\}$. Each $\mathrm{num}(w_i) \ge 1$, so $\mathrm{num}(v) \ge 1$. $\square$

With $v = \mathrm{ENTRY}$: the $N = \mathrm{num}(\mathrm{ENTRY})$ paths of $G$ get the numbers $0, \ldots, N - 1$, each exactly once.

**Lemma 2 (regeneration).** For $0 \le r < \mathrm{num}(\mathrm{ENTRY})$, REGENERATE$(r)$ returns the unique path $p$ with $\mathrm{Val}(p) = r$.

*Proof.* Invariant at the top of L17: the edges in `path` form a path from ENTRY to $v$ whose sum is the original $r$ minus the current $r$, and $0 \le r < \mathrm{num}(v)$. It holds at the start. If $v \ne \mathrm{EXIT}$, the blocks $B_i$ of Lemma 1 partition $\{0, \ldots, \mathrm{num}(v) - 1\}$, so L18 finds exactly one edge $e_i$ with $r \in B_i$. After L19, the new $r$ is $r - s_i \in \{0, \ldots, \mathrm{num}(w_i) - 1\}$, so the invariant holds at $w_i$. Each step moves forward in a finite DAG, so the loop ends, at $v = \mathrm{EXIT}$ where $\mathrm{num}(v) = 1$ forces $r = 0$. Then the sum of `path` is the original $r$. By Lemma 1 there is exactly one such path. $\square$

**Lemma 3 (placement).** Let $H$ be the undirected multigraph with the edges of $G$ and one extra edge $x$ joining EXIT and ENTRY, and give $x$ the value $\mathrm{Val}(x) = 0$, read in the direction EXIT $\to$ ENTRY. Let $T$ be any spanning tree of $H$ that contains $x$. There is a function $\phi$ on the nodes with $\phi(\mathrm{ENTRY}) = 0$ and $\phi(v) = \phi(u) + \mathrm{Val}(u \to v)$ for every edge $u \to v$ of $T$ (including $x$). With $\mathrm{Inc}(u \to v) = \mathrm{Val}(u \to v) + \phi(u) - \phi(v)$:

1. $\mathrm{Inc}(e) = 0$ for every edge $e$ of $G$ in $T$;
2. $\sum_{e \in p} \mathrm{Inc}(e) = \mathrm{Val}(p)$ for every path $p$ from ENTRY to EXIT.

*Proof.* $H$ is connected, because every node is joined to ENTRY by a directed path of $G$. So $T$ exists. Define $\phi(v)$ by walking the unique tree path from ENTRY to $v$ and adding $\mathrm{Val}(e)$ for each edge crossed along its direction and subtracting it for each edge crossed against its direction. This is what L10 to L12 compute, and because the tree path is unique, $\phi$ is well defined. For a tree edge $u \to v$, the tree path to one endpoint is the tree path to the other plus this edge, so $\phi(v) = \phi(u) + \mathrm{Val}(u \to v)$ in both cases. For $x$ this gives $\phi(\mathrm{ENTRY}) = \phi(\mathrm{EXIT}) + 0$, so $\phi(\mathrm{EXIT}) = 0$.

Part 1 is the rule for tree edges: $\mathrm{Inc}(u \to v) = \mathrm{Val}(u \to v) + \phi(u) - \phi(v) = 0$.

Part 2: let $p$ be $v_0 \to v_1 \to \cdots \to v_m$ with $v_0 = \mathrm{ENTRY}$ and $v_m = \mathrm{EXIT}$. Then

$$\sum_{j=1}^{m} \mathrm{Inc}(v_{j-1} \to v_j) = \mathrm{Val}(p) + \sum_{j=1}^{m} (\phi(v_{j-1}) - \phi(v_j)) = \mathrm{Val}(p) + \phi(\mathrm{ENTRY}) - \phi(\mathrm{EXIT}) = \mathrm{Val}(p).$$

$\square$

So the chord placement assigns the same number to every path as Val does, and needs code only on chords, the edges of $G$ outside $T$. There are $|E| + 1 - (|V| - 1) = |E| - |V| + 2$ chords, none of them $x$. The choice of a maximum spanning tree for the edge frequencies is a cost choice: among all spanning trees that contain $x$, it is one whose chords have the least total frequency. It does not affect correctness.

**Lemma 4 (programs with loops).** Let the DAG come from a program as described on the page: back edges $b \to h$ of a depth-first search from the entry block are removed, and replaced by a start edge ENTRY $\to h$ and a stop edge $b \to$ EXIT. Then every finite run that ends in a `ret` splits in exactly one way into a sequence of DAG paths, and the instrumented program counts exactly the numbers of these paths, in order.

*Proof.* Removing all DFS back edges leaves a DAG, because in a DFS every cycle contains a back edge (an edge to a node on the stack). The run is a walk $c_0, c_1, \ldots, c_t$ in the CFG from the entry block to a `ret` block. Cut it at every step $c_{j} \to c_{j+1}$ that is a back edge. Each piece is a walk that uses only DAG edges. The first piece starts at the entry block, so prefixing ENTRY $\to$ entry gives a DAG path start. A later piece starts at the header $h$ of the back edge just crossed, so its DAG path starts with the start edge ENTRY $\to h$. A piece that ends before a back edge $b \to h$ ends at $b$ and is closed by the stop edge $b \to$ EXIT, and the last piece ends at a `ret` block and is closed by its edge to EXIT. Each piece is thus a path from ENTRY to EXIT. The cut points are fixed by the run, so the split is unique.

Now the register. Claim: while the run is inside a piece, $r$ equals the sum of Inc over the DAG edges of the current piece crossed so far, starting with its first edge from ENTRY. At the start of the run, $r$ is set to $\mathrm{Inc}(\mathrm{ENTRY} \to \text{entry})$. Crossing a DAG edge $e$ inside a piece adds $\mathrm{Inc}(e)$ (no code is the same as adding 0). At a `ret` block $b$ the count uses $r + \mathrm{Inc}(b \to \mathrm{EXIT})$, which is the sum over the whole piece. At a back edge $b \to h$, the count uses $r + \mathrm{Inc}(\text{stop edge of } b)$, again the sum over the whole piece, and then $r$ is set to $\mathrm{Inc}(\mathrm{ENTRY} \to h)$, the first edge of the next piece. By Lemma 3 each counted value is the Val sum of the piece, and by Lemma 1 it is the number of that DAG path. $\square$

A run that traps or does not end also has its completed pieces counted correctly; only the last, incomplete piece is not counted.

**Theorem.** The Ball-Larus numbering gives the $N$ paths of the DAG the numbers $0, \ldots, N - 1$ bijectively, REGENERATE inverts it, the increments placed on the chords of any spanning tree of $H$ that contains EXIT -- ENTRY give every path the same sum, and the instrumented program counts each path of each run under its number. This is Lemmas 1 to 4. $\square$
