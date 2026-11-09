---
title: KARP-LUBY is an (ε, δ) approximation of the DNF count
proves: [correctness]
status: full
---

Notation: $F = C_1 \lor \cdots \lor C_m$ is a DNF over $x_1, \ldots, x_n$. An assignment is a vector $a \in \{0, 1\}^n$. $S_i$ is the set of assignments that satisfy $C_i$, and $S = S_1 \cup \cdots \cup S_m$ is the set of assignments that satisfy $F$. $|C_i|$ is the number of different literals of $C_i$. We take $0 < \varepsilon < 1$ and $0 < \delta < 1$.

We use one standard fact.

**Fact (Chernoff bound).** Let $s = X_1 + \cdots + X_N$, where the $X_t$ are independent 0-1 random variables with $\Pr[X_t = 1] = p$, and let $\mu = Np$. For $0 < \varepsilon < 1$,

$$\Pr[s \ge (1 + \varepsilon)\mu] \le e^{-\varepsilon^2 \mu / 3}, \qquad \Pr[s \le (1 - \varepsilon)\mu] \le e^{-\varepsilon^2 \mu / 2}.$$

This is Theorem 4.4 and Theorem 4.5 of Mitzenmacher and Upfal, Probability and Computing (Chapter 4).

**Lemma 1 (line L1).** A clause that contains a literal and its negation has $S_i = \emptyset$. A clause with no such pair has $|S_i| = 2^{n - |C_i|}$, and the assignments of $S_i$ are exactly those that make each literal of $C_i$ true, with the other $n - |C_i|$ variables free.

*Proof.* $C_i$ is true under $a$ if and only if every literal of $C_i$ is true under $a$. If $C_i$ has $x_v$ and $\lnot x_v$, no $a$ makes both true. Otherwise the literals of $C_i$ name $|C_i|$ different variables, each with one required value. These values are consistent, and $a$ satisfies $C_i$ if and only if it takes them; the other $n - |C_i|$ variables can take any of $2^{n - |C_i|}$ values. $\square$

So the clauses dropped by line L1 do not change $S$. From now on, $C_1, \ldots, C_m$ are the clauses that are left. If $m = 0$, then $S = \emptyset$ and line L1 returns $0 = |S|$, which is correct. Assume $m \ge 1$. By Lemma 1, line L2 sets $w_i = |S_i| \ge 1$ and $W = \sum_i |S_i|$.

Let $P = \{(i, a) : 1 \le i \le m, \ a \in S_i\}$, so $|P| = W$. A pair $(i, a) \in P$ is *first* if $a \notin S_j$ for every $j < i$.

**Lemma 2 (uniform pairs).** In each pass of the loop of line L4, the pair $(i, a)$ chosen by lines L5 and L6 is uniform on $P$: each pair in $P$ has probability $1/W$. The passes are independent.

*Proof.* Line L5 chooses $i$ with probability $w_i / W$. Given $i$, line L6 sets the literals of $C_i$ true and the other $n - |C_i|$ variables by independent fair coins, so by Lemma 1 it returns each $a \in S_i$ with probability $2^{-(n - |C_i|)} = 1/w_i$. So $\Pr[(i, a)] = (w_i / W)(1/w_i) = 1/W$ for each $(i, a) \in P$. Each pass uses fresh random choices, so the passes are independent. $\square$

**Lemma 3 (the success probability).** Exactly $|S|$ pairs of $P$ are first. So in each pass, line L7 adds 1 to $s$ with probability $p = |S|/W$, and $p \ge 1/m$.

*Proof.* Map each $a \in S$ to the pair $(i_a, a)$, where $i_a$ is the least index with $a \in S_{i_a}$. This pair is in $P$ and is first. Conversely, if $(i, a) \in P$ is first, then $a \in S_i \subseteq S$, and $a \notin S_j$ for $j < i$, so $i = i_a$. So the map is a bijection from $S$ onto the set of first pairs. Line L7 adds 1 exactly when the chosen pair is first, so by Lemma 2 the probability is $|S|/W$.

For the bound, each $a \in S$ lies in at most $m$ of the sets $S_i$, so $W = \sum_i |S_i| = \sum_{a \in S} |\{i : a \in S_i\}| \le m |S|$, and $p = |S|/W \ge 1/m$. $\square$

**Theorem.** KARP-LUBY returns $Y$ with $\mathbb{E}[Y] = |S|$ and

$$\Pr\big[(1 - \varepsilon)|S| \le Y \le (1 + \varepsilon)|S|\big] \ge 1 - \delta.$$

*Proof.* The case $m = 0$ is done above, with $Y = |S|$ always. Let $m \ge 1$. By Lemmas 2 and 3, $s = X_1 + \cdots + X_N$, where $X_t$ is 1 if pass $t$ adds 1 to $s$, and the $X_t$ are independent with $\Pr[X_t = 1] = p = |S|/W$. Line L8 returns $Y = W s / N$. Let $\mu = Np$; then $W \mu / N = Wp = |S|$, so $\mathbb{E}[Y] = W \mu / N = |S|$.

Line L3 sets $N \ge 3 m \ln(2/\delta)/\varepsilon^2$. By Lemma 3, $p \ge 1/m$, so

$$\mu = Np \ge \frac{N}{m} \ge \frac{3 \ln(2/\delta)}{\varepsilon^2}.$$

Since $p \ge 1/m > 0$, also $\mu > 0$ and $|S| > 0$. Multiplying by $W/N > 0$, the event $(1 - \varepsilon)|S| \le Y \le (1 + \varepsilon)|S|$ is the event $(1 - \varepsilon)\mu \le s \le (1 + \varepsilon)\mu$. By the Fact, the probability that it fails is at most

$$\Pr[s > (1 + \varepsilon)\mu] + \Pr[s < (1 - \varepsilon)\mu] \le e^{-\varepsilon^2 \mu / 3} + e^{-\varepsilon^2 \mu / 2} \le 2 e^{-\varepsilon^2 \mu / 3} \le 2 e^{-\ln(2/\delta)} = \delta.$$

So the event holds with probability at least $1 - \delta$. $\blacksquare$
