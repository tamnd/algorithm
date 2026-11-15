---
title: The layer method returns the models of p at minimum Hamming distance from the models of K
proves: [correctness, termination]
status: full
---

We use the pseudocode of the page. The input is a number $n \ge 0$ of atoms, the set $K$ of the models of the belief base and the set $P$ of the models of the new information $p$. Both are sets of worlds, and a world is a vector in $\{0,1\}^n$. Write $h(u, v)$ for the [Hamming distance](/hamming-distance/) between two worlds, the number of atoms on which they differ. For a nonempty set $K$, write

$$\mathrm{dist}(w, K) = \min_{u \in K} h(w, u).$$

Dalal's revision is $K \circ P = \{w \in P : \mathrm{dist}(w, K) = d^*\}$ with $d^* = \min_{w \in P} \mathrm{dist}(w, K)$ when $K$ and $P$ are nonempty, $K \circ P = P$ when $K$ is empty, and $K \circ P = \emptyset$ when $P$ is empty (Dalal 1988, with the empty base as in Eiter and Gottlob 1992).

Two worlds are neighbours when their distance is 1. Line L8 makes the neighbour of $w$ that differs from $w$ in atom $i$.

**Lemma 1 (one step).** Let $K$ be nonempty. If $u$ and $v$ are neighbours, then $|\mathrm{dist}(u, K) - \mathrm{dist}(v, K)| \le 1$. If $\mathrm{dist}(v, K) = j \ge 1$, then $v$ has a neighbour $u$ with $\mathrm{dist}(u, K) = j - 1$.

*Proof.* The Hamming distance is a metric, so $h(u, x) \le h(u, v) + h(v, x) = 1 + h(v, x)$ for each $x \in K$. Take the minimum over $x$ to get $\mathrm{dist}(u, K) \le 1 + \mathrm{dist}(v, K)$, and swap $u$ and $v$. For the second claim, take $x \in K$ with $h(v, x) = j \ge 1$, and let $u$ be $v$ with one of the atoms where $v$ and $x$ differ changed. Then $h(u, x) = j - 1$, so $\mathrm{dist}(u, K) \le j - 1$, and the first claim gives $\mathrm{dist}(u, K) \ge j - 1$. $\square$

**Lemma 2 (layers).** Let $K$ and $P$ be nonempty. Each time the test of line L4 runs, with the current value $d$,

> **(I1)** $L = \{w : \mathrm{dist}(w, K) = d\}$, and
>
> **(I2)** $S = \{w : \mathrm{dist}(w, K) \le d\}$.

*Proof.* By induction on the number of times the test has run. The first time, line L3 has set $L = S = K$ and $d = 0$, and $\mathrm{dist}(w, K) = 0$ holds exactly for $w \in K$.

Suppose the claims hold for $d$ and the body of the loop runs. Lines L5 to L9 put $v$ in $N$ exactly when $v$ is a neighbour of some $w \in L$ and $v \notin S$ at that moment. Since $S$ only grows by the worlds that are put in $N$, a world is put in $N$ at most once, and at the end

$$N = \{v : v \notin S_{\text{old}} \text{ and } v \text{ has a neighbour in } L\}.$$

Let $v \in N$. Then $\mathrm{dist}(v, K) > d$ by (I2), and $\mathrm{dist}(v, K) \le d + 1$ by Lemma 1, because a neighbour has distance $d$ by (I1). So $\mathrm{dist}(v, K) = d + 1$. Conversely let $\mathrm{dist}(v, K) = d + 1$. Then $v \notin S_{\text{old}}$ by (I2), and by Lemma 1 $v$ has a neighbour at distance $d$, which is in $L$ by (I1). So $v \in N$. This shows $N = \{w : \mathrm{dist}(w, K) = d + 1\}$, and $S_{\text{new}} = S_{\text{old}} \cup N = \{w : \mathrm{dist}(w, K) \le d + 1\}$. Line L10 sets $L \leftarrow N$ and $d \leftarrow d + 1$, so (I1) and (I2) hold for the new value of $d$. $\square$

**Lemma 3 (termination).** Let $K$ and $P$ be nonempty. The loop of lines L4 to L10 runs exactly $d^*$ times, and $d^* \le n$.

*Proof.* Each distance is at most $n$, so $d^* \le n$. By (I1), $L \cap P = \{w \in P : \mathrm{dist}(w, K) = d\}$ at the test of line L4. For $d < d^*$ this set is empty, by the definition of $d^*$, so the loop body runs. For $d = d^*$ the set holds a world of $P$ with the least distance, so the test fails and the loop stops. $\square$

**Theorem.** DALAL$(K, P, n)$ stops and returns $K \circ P$. When $K$ and $P$ are nonempty, the returned distance is $d^*$.

*Proof.* If $P$ is empty, line L1 returns $\emptyset$. If $K$ is empty, line L2 returns $P$. Otherwise, by Lemma 3 the loop stops with $d = d^*$, and by (I1) line L11 returns $L \cap P = \{w \in P : \mathrm{dist}(w, K) = d^*\}$, which is $K \circ P$. $\square$

**Cost.** By (I2) and the test of line L9, each world enters $S$ at most once, and each world of $L$ was put in $S$ when it entered $L$. So the layers are disjoint, the loop of line L6 meets each world at most once, and lines L7 to L9 run at most $n \cdot |S| \le n \cdot 2^n$ times in total. On the [word RAM](/word-ram/), with $K$, $P$ and $S$ stored as bit arrays of $2^n$ bits, each run of lines L8 and L9 takes $O(1)$ time, and the test of line L4 can be done when the members of $N$ are added. So the time is $O(n \cdot 2^n)$, plus $O(2^n)$ to set up the arrays. The bound is reached: for $K = \{0^n\}$ and $P = \{1^n\}$ we have $d^* = n$, every world enters $S$, and lines L7 to L9 run exactly $n \cdot 2^n$ times.

**The empty base.** The case of line L2 is a convention, not a consequence of the distance: with no model of $K$, no world of $P$ is closer than another, and Eiter and Gottlob (1992) take $\mathrm{Mod}(\psi \circ \mu) = \mathrm{Mod}(\mu)$ when $\psi$ is unsatisfiable. This choice is the flat preorder in which all worlds are equal, so the operator satisfies R1 to R6 also when $K$ is inconsistent.
