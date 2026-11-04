---
title: Held-Karp returns a shortest tour
proves: [correctness, termination]
status: full
---

We use the pseudocode of the page, with cities $0, \ldots, n-1$, $V = \{1, \ldots, n-1\}$ and distances $d(i, j)$, which are real numbers. For a nonempty $S \subseteq V$ and $j \in S$, an *$(S, j)$-path* is a sequence $0 = u_0, u_1, \ldots, u_k = j$ with $k = |S|$ and $\{u_1, \ldots, u_k\} = S$. So it starts at 0, visits each city of $S$ exactly once, visits no other city, and ends at $j$. Its length is $\sum_{t=1}^{k} d(u_{t-1}, u_t)$. Let $\mathrm{OPT}(S, j)$ be the least length of an $(S, j)$-path. It exists, because $S \setminus \{j\}$ has finitely many orders and each order gives exactly one $(S, j)$-path.

**Lemma 1.** After lines L2 to L6, for each nonempty $S \subseteq V$ and $j \in S$: (a) $C[S, j] = \mathrm{OPT}(S, j)$; (b) if $|S| = 1$ then $P[S, j] = 0$, and if $|S| \ge 2$ then $i = P[S, j]$ lies in $S \setminus \{j\}$ and $C[S, j] = C[S \setminus \{j\}, i] + d(i, j)$.

*Proof.* First, each entry is written once and only after the entries it reads. Line L2 writes the sets of size 1. Line L5 for $S$ reads $C[S \setminus \{j\}, i]$. If $|S| = 2$, the set $S \setminus \{j\}$ has size 1 and was written by line L2. If $|S| \ge 3$, the mask of $S \setminus \{j\}$ is the mask of $S$ minus the positive number $2^{j-1}$, so it is smaller, and line L3 handled it in an earlier pass. So line L5 reads only final values.

We prove (a) by induction on $|S|$.

*Base, $|S| = 1$.* Then $S = \{j\}$, and the only $(S, j)$-path is $0, j$, with length $d(0, j)$. Line L2 sets $C[\{j\}, j] = d(0, j)$ and $P[\{j\}, j] = 0$.

*Step, $|S| \ge 2$.* Assume (a) for all sets of size $|S| - 1$. Let $R = S \setminus \{j\}$, which is nonempty.

- *Each value of line L5 is the length of a path.* Take $i \in R$. By the hypothesis, some $(R, i)$-path $p$ has length $C[R, i]$. Append $j$ to $p$. Since $j \notin R$, the result visits exactly the cities of $R \cup \{j\} = S$, once each, and ends at $j$. So it is an $(S, j)$-path of length $C[R, i] + d(i, j)$. Hence the minimum of line L5 is at least $\mathrm{OPT}(S, j)$.
- *An optimal path gives one of the values.* Let $q = u_0, \ldots, u_k$ be an $(S, j)$-path of length $\mathrm{OPT}(S, j)$, with $k = |S| \ge 2$. Let $i = u_{k-1}$. Then $i \ne 0$ because $k - 1 \ge 1$, and $i \in R$. The prefix $u_0, \ldots, u_{k-1}$ is an $(R, i)$-path, so its length is at least $\mathrm{OPT}(R, i) = C[R, i]$ by the hypothesis. So $\mathrm{OPT}(S, j) \ge C[R, i] + d(i, j)$, which is at least the minimum of line L5.

The two bounds give $C[S, j] = \mathrm{OPT}(S, j)$. Line L6 picks an $i \in R$ that attains the minimum, which is (b). $\square$

**Lemma 2.** The least length of a tour is $\min_{j \in V} (\mathrm{OPT}(V, j) + d(j, 0))$ for $n \ge 2$.

*Proof.* A tour $0 = v_0, v_1, \ldots, v_{n-1}$ is exactly a $(V, v_{n-1})$-path followed by the edge back to 0, and its length is the length of the path plus $d(v_{n-1}, 0)$. Conversely, each $(V, j)$-path followed by the edge $(j, 0)$ is a tour. So the set of tour lengths is the set of values (length of a $(V, j)$-path) $+\ d(j, 0)$ over all $j$ and all such paths, and its minimum is the stated one. $\square$

**Lemma 3 (the rebuild).** Lines L8 to L11 stop, and they produce a tour of length $C[V, last] + d(last, 0)$.

*Proof.* Each pass of line L11 with $j \ne 0$ removes $j$ from $S$, so $|S|$ drops by exactly 1. While $|S| \ge 2$, Lemma 1(b) gives a new $j \in S$, which is not 0. When $|S| = 1$, line L11 sets $j = P[\{j\}, j] = 0$ and the loop stops. So the loop runs exactly $|V| = n - 1$ times.

We claim that before each test of line L9 with $j \ne 0$: $j \in S$, the list $tour$ followed by nothing is a sequence $w$ of the cities of $V \setminus S$, and $C[S, j] + (\text{length of the walk } j, w)$ $= C[V, last]$, where the length of the walk $j, w$ is the sum of $d$ over its consecutive pairs. At the start, $S = V$, $j = last$, $w$ is empty, and the claim holds. In a pass with $|S| \ge 2$, let $i = P[S, j]$. By Lemma 1(b), $C[S, j] = C[S \setminus \{j\}, i] + d(i, j)$. After the pass, $S' = S \setminus \{j\}$, the new list is $j, w$, and the new walk is $i, j, w$, whose length is $d(i, j)$ plus the old one. So the sum is unchanged. In the last pass, $|S| = 1$, so $S = \{j\}$ and $C[S, j] = d(0, j)$. After it, the list is a sequence of all of $V$, and $0$ followed by the list is a walk of length $C[V, last]$ that visits each city of $V$ once. Line L12 returns it, and the edge from $last$ back to 0 closes it into a tour of length $C[V, last] + d(last, 0)$. $\square$

**Theorem.** HELD-KARP$(d, n)$ stops and returns the least length of a tour and a tour of that length.

*Proof.* For $n = 1$, line L1 returns the only tour, of length 0. For $n \ge 2$, all loops of lines L2 to L6 run over finite sets, and the loop of line L9 stops by Lemma 3. By Lemma 1(a), line L7 computes $\min_j (\mathrm{OPT}(V, j) + d(j, 0))$, which is the least tour length by Lemma 2. By Lemma 3 the returned tour has length $C[V, last] + d(last, 0) = best$. $\blacksquare$
