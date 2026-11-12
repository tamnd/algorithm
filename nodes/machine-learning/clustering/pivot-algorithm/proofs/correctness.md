---
title: KwikCluster has expected cost at most 3 times the optimum
proves: [correctness]
status: full
---

We use the pseudocode of the page. The input is a complete graph on $V$, $|V| = n$, with each pair labeled $+$ or $-$. A partition pays 1 for each $+$ pair it splits and each $-$ pair it joins; $\mathrm{OPT}$ is the least cost. A *bad triangle* is a set of three vertices with exactly two $+$ pairs. The argument is the one of Ailon, Charikar and Newman (2008).

**Lemma 1 (the output is a partition).** KWIKCLUSTER stops after at most $n$ rounds, and its clusters partition $V$.

*Proof.* Invariant: the clusters output so far and $R$ partition $V$. It holds at the start, with no cluster and $R = V$. Line L4 takes $C \subseteq R$ with $p \in C$, so $C \ne \emptyset$, and line L6 moves exactly $C$ from $R$ to the output. So the invariant holds after each round, and $|R|$ drops by at least 1 per round. $\square$

**Lemma 2 (each lower bound by bad triangles).** Let $\mathcal{T}$ be the set of bad triangles and let $\beta_T \ge 0$ for $T \in \mathcal{T}$ satisfy $\sum_{T \ni e} \beta_T \le 1$ for each pair $e$. Then $\mathrm{OPT} \ge \sum_T \beta_T$.

*Proof.* Let $\mathcal{C}$ be any partition and $x_e = 1$ if $\mathcal{C}$ makes a mistake on $e$, else 0. Let $T = \{u, v, w\}$ with $uv$ and $uw$ positive and $vw$ negative. If $\mathcal{C}$ makes no mistake on $uv$ and $uw$, then $u \sim v$ and $u \sim w$, so $v \sim w$, a mistake on $vw$. So $\sum_{e \subset T} x_e \ge 1$. Then

$$\mathrm{cost}(\mathcal{C}) = \sum_e x_e \ge \sum_e x_e \sum_{T \ni e} \beta_T = \sum_T \beta_T \sum_{e \subset T} x_e \ge \sum_T \beta_T. \qquad \square$$

Fix a run. Say that a bad triangle $T$ is *hit by $x$* if, in some round, all three vertices of $T$ are in $R$ and the pivot is $x \in T$. At most one round can hit $T$: after the round in which the pivot is in $T$, that pivot is no longer in $R$.

**Lemma 3 (cost equals hits).** In each run, the cost of the output equals the number of hit bad triangles. More precisely, if $T = \{x, u, v\}$ is hit by $x$, the pair $uv$ is a mistake and is decided in that round, and each mistake arises in this way from exactly one hit triangle.

*Proof.* Look at one round with pivot $p$ and the set $R$ before it. A pair is *decided* in the round in which the first of its two vertices leaves $R$; from then on its status (joined or split) is fixed, because later clusters do not contain that vertex.

Pairs $pv$ with $v \in R$: if $pv$ is $+$, $v \in C$ and the pair is joined; if $-$, $v \notin C$ and the pair is split. No mistake.

Pairs $uv$ with $u, v \in R \setminus \{p\}$:

- both $pu$ and $pv$ are $+$: both join $C$, so $uv$ is joined. It is a mistake exactly when $uv$ is $-$, that is, when $\{p, u, v\}$ is a bad triangle;
- exactly one of them, say $pu$, is $+$: $u \in C$, $v \notin C$, so $uv$ is split. It is a mistake exactly when $uv$ is $+$, that is, when $\{p, u, v\}$ has the two $+$ pairs $pu$ and $uv$, a bad triangle;
- both are $-$: neither joins $C$, and $uv$ is not decided in this round. The triple $\{p, u, v\}$ has at most one $+$ pair, so it is not bad.

So the mistakes decided in this round are exactly the pairs $uv$ opposite to $p$ in the bad triangles $\{p, u, v\} \subseteq R$, that is, in the triangles hit by $p$, and each such triangle gives one mistake. Different triangles hit by $p$ have different opposite pairs. A pair is decided in only one round, so it is never counted twice. Summing over the rounds, the cost equals the number of hit bad triangles. $\square$

Now let the pivots be random, as in line L3. For $T \in \mathcal{T}$ let $p_T$ be the probability that $T$ is hit, and let $A_T(x)$ be the event that $T$ is hit by $x$.

**Lemma 4 (symmetry).** For each $T \in \mathcal{T}$ and each $x \in T$, $\Pr[A_T(x)] = p_T/3$.

*Proof.* Let $R_t$ be the set $R$ before round $t$ (empty after the end). Since at most one round hits $T$,

$$\Pr[A_T(x)] = \sum_t \Pr[T \subseteq R_t \text{ and the pivot of round } t \text{ is } x] = \sum_t \mathbb{E}\Bigl[\mathbb{1}[T \subseteq R_t] \cdot \frac{1}{|R_t|}\Bigr],$$

because given the history up to round $t$, the pivot is uniform on $R_t$. The right side does not depend on $x \in T$. The three events $A_T(x)$, $x \in T$, are disjoint and their union is "$T$ is hit", so each has probability $p_T/3$. $\square$

**Lemma 5 (a fractional packing).** For each pair $e$, $\sum_{T \in \mathcal{T},\, T \ni e} p_T/3 \le 1$.

*Proof.* For $T \ni e$ let $x_T$ be the vertex of $T$ that is not in $e$. By Lemma 3, the event $A_T(x_T)$ decides $e$ in that round, as a mistake. The pair $e$ is decided in exactly one round, by one pivot, so at most one of the events $A_T(x_T)$, $T \ni e$, happens; they are disjoint. Hence $\sum_{T \ni e} \Pr[A_T(x_T)] \le 1$, and by Lemma 4 each term is $p_T/3$. $\square$

**Theorem.** $\mathbb{E}[\mathrm{cost}(\text{KWIKCLUSTER})] \le 3 \cdot \mathrm{OPT}$.

*Proof.* By Lemma 3 and linearity of expectation, $\mathbb{E}[\mathrm{cost}] = \sum_T \Pr[T \text{ is hit}] = \sum_T p_T$. By Lemma 5 the weights $\beta_T = p_T/3$ satisfy the condition of Lemma 2, so $\mathrm{OPT} \ge \sum_T p_T/3 = \mathbb{E}[\mathrm{cost}]/3$. $\square$

**Remarks.** If there is no bad triangle, Lemma 3 gives cost 0 in every run, so the algorithm is exact on consistent input. The bound is on the mean only; the cost of one run can be larger. The proof uses that every pair is labeled (a mistake on a pair needs a label), so it does not apply to general graphs with missing pairs.
