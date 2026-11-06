---
title: The closure algorithm decides size-change termination
proves: [correctness]
status: full
---

We use the definitions and the pseudocode of the page. $\mathcal{G}$ is a finite set of size-change graphs, each graph $G : f \to g$ has at most one arc between each pair of parameters, and $G ; H$ is defined when $G : f \to g$ and $H : g \to h$. A **walk** is a nonempty sequence $w = H_1 \cdots H_n$ of graphs of $\mathcal{G}$ with $H_t : f_t \to f_{t+1}$, and $G_w = H_1 ; \cdots ; H_n : f_1 \to f_{n+1}$. A **path** through $w$ from $i$ to $j$ is a sequence of parameters $x_1 = i, x_2, \ldots, x_{n+1} = j$ with an arc $x_t \to x_{t+1}$ in $H_t$ for each $t$; it is strict if one of these arcs is strict.

**Lemma 1 (composition).** $G_w$ has an arc $i \to j$ iff there is a path through $w$ from $i$ to $j$, and the arc is strict iff some such path is strict. In particular composition is associative, and $G_{w} ; G_{v} = G_{wv}$ whenever $wv$ is a walk.

*Proof.* By induction on $n$. For $n = 1$ a path is one arc of $H_1$. For $n > 1$ write $w = w' H_n$. By definition $G_{w'} ; H_n$ has an arc $i \to j$ iff some $k$ has an arc $i \to k$ in $G_{w'}$ and $k \to j$ in $H_n$, which by induction holds iff there is a path through $w'$ from $i$ to $k$ followed by an arc $k \to j$ of $H_n$, that is, a path through $w$ from $i$ to $j$. The arc is strict iff for some such $k$ one of the two parts is strict, which by induction holds iff some path through $w$ from $i$ to $j$ is strict. Since paths through $wv$ are paths through $w$ followed by paths through $v$, the same description gives $G_w ; G_v = G_{wv}$, and associativity follows. $\square$

**Lemma 2 (the closure).** Lines L1 to L6 stop, and afterwards $S = \{G_w : w \text{ a walk}\}$.

*Proof.* A graph $f \to g$ is determined by its endpoints and by the state of each of the at most $p^2$ pairs of parameters: no arc, a non-strict arc or a strict arc. So there are at most $F^2 \cdot 3^{p^2}$ graphs. A graph enters $W$ only when it enters $S$, and never leaves $S$, so at most that many graphs enter $W$; each iteration of L2 removes one, so the loop stops.

Every graph put into $S$ is some $G_w$: this holds for the graphs of $\mathcal{G}$ at L1, and line L5 forms $G_w ; H = G_{wH}$ by Lemma 1, where $wH$ is a walk since $H$ starts at the end of $G_w$.

Conversely, let $w$ be a walk; we show $G_w \in S$ by induction on its length. Walks of length 1 are put into $S$ at L1. For $w = w' H$, by induction $G_{w'} \in S$. Every graph of $S$ entered $W$ when it entered $S$, and the loop runs until $W$ is empty, so $G_{w'}$ is removed at L3 at some time. Then L4 considers $H$, which starts where $G_{w'}$ ends, and L5 and L6 ensure $G_{w'} ; H = G_w \in S$. $\square$

**Lemma 3 (Ramsey).** If every idempotent $G : f \to f$ in $S$ has a strict arc $x \to x$, then every multipath has an infinitely descending thread.

*Proof.* Let $H_1 H_2 \cdots$ be a multipath, with $H_t : f_t \to f_{t+1}$. For times $s < t$ let $c(s, t) = G_{H_s \cdots H_{t-1}}$, a graph of $S$ by Lemma 2. This colors the pairs of positive integers with finitely many colors, so by the infinite Ramsey theorem there are times $t_0 < t_1 < t_2 < \cdots$ and a graph $G$ with $c(t_a, t_b) = G$ for all $a < b$. Then $G : f_{t_0} \to f_{t_1}$ and $G : f_{t_1} \to f_{t_2}$, so $f_{t_0} = f_{t_1}$ and $G : f \to f$ for $f = f_{t_0}$. By Lemma 1, $G ; G = c(t_0, t_1) ; c(t_1, t_2) = c(t_0, t_2) = G$, so $G$ is idempotent. By assumption it has a strict arc $x \to x$, and by Lemma 1, for each $a$ there is a strict path from $x$ to $x$ through $H_{t_a} \cdots H_{t_{a+1} - 1}$. These paths join into a thread from time $t_0$ that has a strict arc in each segment, so it is infinitely descending. $\square$

**Lemma 4 (the witness).** If $G = G_w : f \to f$ is idempotent and has no strict arc $x \to x$, then the multipath $w w w \cdots$ has no infinitely descending thread.

*Proof.* The multipath is well formed, since $w$ starts and ends at $f$. Suppose a thread from some time $s$ has infinitely many strict arcs. Let the period boundaries after $s$ be the times $b_0 < b_1 < \cdots$ at which a copy of $w$ starts, and let $y_m$ be the parameter of the thread at $b_m$. There are finitely many parameters and infinitely many strict arcs, so there are $m < m'$ with $y_m = y_{m'} = x$ and a strict arc of the thread between $b_m$ and $b_{m'}$. That part of the thread is a strict path from $x$ to $x$ through $w^{m' - m}$, so by Lemma 1 the graph $G_{w^{m'-m}} = G^{m'-m}$ has a strict arc $x \to x$. Since $G$ is idempotent, $G^{m'-m} = G$, which has no strict arc $x \to x$, a contradiction. $\square$

**Theorem.** SIZE-CHANGE-TERMINATES stops, and it returns "SCT" iff $\mathcal{G}$ is size-change terminating; when it returns "not SCT" with witness $G = G_w$, the multipath $w w w \cdots$ has no infinitely descending thread.

*Proof.* The closure stops by Lemma 2, and lines L7 to L9 make one finite pass over $S$. Line L8 tests $G ; G = G$ for graphs $f \to f$, that is, idempotence, and L9 tests for a strict self arc. If the algorithm returns "SCT" at L10, every idempotent $G : f \to f$ in $S$ has a strict self arc, so $\mathcal{G}$ is SCT by Lemma 3. If it returns "not SCT" at L9 with $G$, then $G = G_w$ for a walk $w$ by Lemma 2, recorded by the implementation, and by Lemma 4 the multipath $w w w \cdots$ has no infinitely descending thread, so $\mathcal{G}$ is not SCT. $\blacksquare$
