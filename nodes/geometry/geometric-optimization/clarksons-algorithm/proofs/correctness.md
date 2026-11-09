---
title: Clarkson's algorithm returns the optimum, and its loops have O(δ) and O(δ log n) expected rounds
proves: [correctness, termination, time.expected]
status: full
---

**Setting.** $(H, w)$ is an LP-type problem: $H$ is a finite set, $w$ maps subsets of $H$ to a totally ordered set with least element $-\infty$, and for all $F \subseteq G \subseteq H$ and $h \in H$:

- monotonicity: $w(F) \le w(G)$;
- locality: if $-\infty < w(F) = w(G)$ and $w(G \cup \{h\}) > w(G)$, then $w(F \cup \{h\}) > w(F)$.

We assume $w(G) > -\infty$ for every nonempty $G$, which holds for the smallest disk and for linear programming after the box constraints are added. A constraint $h$ *violates* $G$ if $w(G \cup \{h\}) > w(G)$; no element of $G$ violates $G$. A *basis* of $G$ is a subset $B \subseteq G$ with $w(B) = w(G)$ and $w(B') < w(B)$ for every proper subset $B'$ of $B$; every $G$ has one (take a subset of $G$ with value $w(G)$ of least size). The combinatorial dimension $\delta$ is the largest size of a basis. BASE returns the optimum of its input, and the violation test is exact. We write $n = |H|$ and $C = 9\delta^2$.

**Lemma 1 (certificate).** Let $\emptyset \ne R \subseteq G$. If no element of $G$ violates $R$, then $w(R) = w(G)$.

*Proof.* Let $G \setminus R = \{h_1, \dots, h_k\}$ and $G_j = R \cup \{h_1, \dots, h_j\}$. We show $w(G_j) = w(R)$ by induction on $j$; $j = 0$ is clear. Suppose $w(G_{j-1}) = w(R)$, which is $> -\infty$ since $R \ne \emptyset$. If $h_j$ violated $G_{j-1}$, then locality with $F = R \subseteq G_{j-1}$ would give that $h_j$ violates $R$, which is false. So $w(G_j) = w(G_{j-1}) = w(R)$. For $j = k$ this is $w(G) = w(R)$. $\square$

**Lemma 2 (violators meet every basis).** Let $\emptyset \ne R \subseteq G$ and let $B$ be a basis of $G$. If some $h \in G$ violates $R$, then some element of $B$ violates $R$.

*Proof.* Suppose no element of $B$ violates $R$. Lemma 1 applied to $R \subseteq R \cup B$ gives $w(R \cup B) = w(R)$. By monotonicity, $w(G) = w(B) \le w(R \cup B) = w(R) \le w(G)$, so $w(R) = w(G)$. Then $w(R \cup \{h\}) \le w(G) = w(R)$ by monotonicity, so $h$ does not violate $R$, a contradiction. $\square$

**Lemma 3 (extreme elements).** Call $h \in S$ extreme in $S$ if $w(S \setminus \{h\}) < w(S)$. Every set $S$ has at most $\delta$ extreme elements.

*Proof.* Let $B$ be a basis of $S$ and $h$ extreme in $S$. If $h \notin B$, then $B \subseteq S \setminus \{h\}$ and $w(S) = w(B) \le w(S \setminus \{h\}) < w(S)$, which is impossible. So every extreme element lies in $B$, and $|B| \le \delta$. $\square$

**Lemma 4 (sampling lemma).** Let $A \subseteq H$ be a fixed set and let $M$ be a list of $N$ entries, each a constraint of $H \setminus A$, with repetitions allowed. For a set $X$ of positions of $M$, let $c(X)$ be the set of constraints at these positions. Let $X$ be a uniformly random set of $r$ positions, $0 \le r \le N$, and let $Z$ be the number of positions $p \notin X$ whose constraint violates $c(X) \cup A$. Then $\mathbb{E}\,Z \le \delta (N - r)/(r + 1)$.

*Proof.* If $r = N$ then $Z = 0$. Otherwise consider a pair $(X, p)$ with $|X| = r$, $p \notin X$, whose constraint $h$ violates $S' = c(X) \cup A$. Then $h \notin S'$, since no element of a set violates it. Put $Q = X \cup \{p\}$ and $S = c(Q) \cup A = S' \cup \{h\}$. Then $S \setminus \{h\} = S'$ and $w(S') < w(S)$, so $h$ is extreme in $S$. Also $p$ is the only position of $Q$ with constraint $h$, because $h \notin c(X)$. So for a fixed $(r + 1)$-set $Q$, the pairs $(Q \setminus \{p\}, p)$ that we count have distinct extreme constraints of $c(Q) \cup A$, and by Lemma 3 there are at most $\delta$ of them. The number of counted pairs is at most $\delta \binom{N}{r+1}$, and

$$\mathbb{E}\,Z \le \frac{\delta \binom{N}{r+1}}{\binom{N}{r}} = \frac{\delta (N - r)}{r + 1}. \qquad \square$$

**Lemma 5 (ITERATIVE).** Let $G$ be nonempty with $m = |G|$. ITERATIVE$(G)$ returns $w(G)$, and its expected number of rounds is at most $2(2.3\,\delta \ln m + 1)$.

*Proof.* If $m \le C$ the base solver returns $w(G)$. Let $m > C$, so $C \ge 1$ draws are made and $R \ne \emptyset$.

*Correctness.* The loop returns $x = w(R)$ only when no element of $G$ violates $R$, and then $x = w(G)$ by Lemma 1.

*Success probability.* Fix the weights at the start of a round and let $W = \mu(G) \ge m > C$ be their sum, where $\mu(h)$ is the weight of $h$ and $\mu(V) = \sum_{h \in V} \mu(h)$. Let $M$ be the list in which each $h \in G$ appears $\mu(h)$ times; the $C$ draws pick a uniform set $X$ of $C$ positions, and $R = c(X)$. A constraint $h \in R$ does not violate $R$, and a constraint $h \in G \setminus R$ that violates $R$ has all its $\mu(h)$ positions outside $X$. So $\mu(V) = Z$ in Lemma 4 with $A = \emptyset$, $N = W$ and $r = C$, and

$$\mathbb{E}\,\mu(V) \le \frac{\delta (W - C)}{C + 1} < \frac{\delta W}{C + 1}.$$

By Markov's inequality, the test on L16 fails with probability at most $\mathbb{E}\,\mu(V) \cdot (C - \delta)/(2 \delta W) < (C - \delta)/(2(C + 1)) < 1/2$. A round is *successful* if $V = \emptyset$ or the test on L16 holds; so each round is successful with probability more than $1/2$, whatever happened before.

*Number of successful rounds.* Fix a basis $B$ of $G$; $1 \le |B| \le \delta$. Consider $k$ successful rounds that do not return. In each, $V \ne \emptyset$, so by Lemma 2 $V$ contains an element of $B$, whose weight doubles. If the elements of $B$ were doubled $k_h$ times, then $\sum_{h \in B} k_h \ge k$, so some $k_h \ge k/|B| \ge k/\delta$, and $\mu(B) \ge 2^{k/\delta}$. Each such round adds $\mu(V) \le 2\delta W/(C - \delta)$ to the total, and failed rounds change nothing, so after these $k$ rounds the total is at most $m (1 + 2\delta/(C - \delta))^k \le m\, e^{2\delta k/(C - \delta)}$. As $\mu(B)$ is at most the total,

$$\frac{k \ln 2}{\delta} \le \ln m + \frac{2 \delta k}{C - \delta}, \qquad\text{so}\qquad k \Bigl(\frac{\ln 2}{\delta} - \frac{2\delta}{C - \delta}\Bigr) \le \ln m.$$

With $C = 9\delta^2$ we have $2\delta/(C - \delta) = 2/(9\delta - 1) \le 1/(4\delta)$, and $\ln 2 - 1/4 > 0.44$, so $k \le \delta \ln m / 0.44 < 2.3\,\delta \ln m$. Hence at most $s = \lfloor 2.3\,\delta \ln m \rfloor + 1$ successful rounds occur, the last of which returns.

*Expected rounds.* Each round is successful with conditional probability at least $1/2$ given the past, so the expected number of rounds until the $s$-th success is at most $2s$. (The waiting time for each success is dominated by a geometric variable with mean 2.) The loop therefore ends with probability 1, after at most $2(2.3\,\delta \ln m + 1)$ rounds in expectation. $\square$

**Theorem.** CLARKSON$(H)$ returns $w(H)$ with probability 1 for nonempty $H$. The expected number of rounds of the outer loop is at most $2(\delta + 1)$, each subproblem passed to ITERATIVE has at most $3\delta\sqrt{n} + 1$ constraints, and the expected numbers of violation tests and BASE calls are $O(\delta n + \delta^3 \sqrt{n} \log n)$ and $O(\delta^2 \log n)$.

*Proof.* If $n \le C$, Lemma 5 applies directly. Let $n > C$; then $r = \lceil \delta\sqrt{n} \rceil \ge 1$.

*Correctness.* Each call on L5 returns $x = w(R \cup V^*)$ by Lemma 5, and $R \cup V^* \ne \emptyset$. The loop returns only when no constraint of $H$ violates $R \cup V^*$, and then $x = w(H)$ by Lemma 1.

*Violators are new.* No element of $R \cup V^*$ violates $R \cup V^*$, so $V \cap V^* = \emptyset$.

*Success probability.* Fix $V^*$ at the start of a round and let $N = n - |V^*|$. If $r \ge N$, then $R \cup V^* = H$ and $V = \emptyset$. Otherwise apply Lemma 4 with $A = V^*$ and $M$ the list of the constraints of $H \setminus V^*$, each once: $|V| = Z$, and

$$\mathbb{E}\,|V| \le \frac{\delta (N - r)}{r + 1} < \frac{\delta n}{r} \le \sqrt{n}.$$

By Markov's inequality $\Pr[|V| > 2\sqrt{n}] < 1/2$. Call a round successful if $V = \emptyset$ or $|V| \le 2\sqrt{n}$; each round is successful with conditional probability more than $1/2$.

*Number of successful rounds.* Fix a basis $B$ of $H$. In a successful round that does not return, $V \ne \emptyset$, and by Lemma 2 $V$ contains an element of $B$, which is not in $V^*$ and is added to $V^*$. So after at most $|B| \le \delta$ such rounds, $B \subseteq V^*$. In any round with $B \subseteq V^*$, monotonicity gives $w(H) = w(B) \le w(R \cup V^*) \le w(H)$, so no $h$ violates $R \cup V^*$ (that would need $w(R \cup V^* \cup \{h\}) > w(H)$), and the round returns. So there are at most $\delta + 1$ successful rounds, and as in Lemma 5 at most $2(\delta + 1)$ rounds in expectation. In particular the algorithm ends with probability 1.

*Size of the subproblems.* $V^*$ is the union of at most $\delta$ sets of size at most $2\sqrt{n}$, so $|R \cup V^*| \le \lceil \delta\sqrt{n} \rceil + 2\delta\sqrt{n} \le 3\delta\sqrt{n} + 1$.

*Cost.* A round of the outer loop makes $n$ violation tests on L6 and one call of ITERATIVE on $m \le 3\delta\sqrt{n} + 1$ constraints. Given the past, by Lemma 5 that call has at most $2(2.3\,\delta \ln m + 1) = O(\delta \log n)$ expected rounds, each with $m$ violation tests and one BASE call. So the expected cost of each outer round, given the past, is at most $K = n + O(\delta \log n) \cdot O(\delta\sqrt{n})$ violation tests and $O(\delta \log n)$ BASE calls. The number of outer rounds $T$ is a stopping time with $\mathbb{E}\,T \le 2(\delta + 1)$, so by Wald's identity the expected totals are at most $\mathbb{E}\,T$ times these bounds: $O(\delta n + \delta^3 \sqrt{n} \log n)$ violation tests and $O(\delta^2 \log n)$ BASE calls. $\blacksquare$
