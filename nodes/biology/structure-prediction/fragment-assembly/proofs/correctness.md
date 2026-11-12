---
title: Fragment assembly keeps a valid chain, returns the best state it visited, and samples the Boltzmann distribution with a full library at a fixed temperature
proves: [correctness]
status: full
---

We use the pseudocode of the page and the lattice model of its implementation. Let $W = \{L, S, R\}^{n-2}$, let $V \subseteq W$ be the set of self-avoiding words, and let $E(w)$ be the HP energy of $w \in V$, with $E(w) = +\infty$ for $w \notin V$. We write $w_t$ and $E_t$ for the values of $w$ and $E$ after the $t$-th step over all stages, and $w_0$, $E_0$ for the values after line L2.

**Claim 0 (the score is exact).** SCORE$(s, w)$ returns $+\infty$ exactly when $w \notin V$, and $E(w)$ otherwise.

*Proof.* SCORE places the residues one at a time and stores each site in a hash table. A site is stored twice exactly when two residues share it, and then SCORE returns $+\infty$. Otherwise the map from sites to residues is injective, and for each H residue $i$ SCORE looks up the 4 lattice neighbours of $x_i$ and counts a residue $j$ there when $j > i + 1$ and $s_j = H$. A contact $\{i, j\}$ with $i + 2 \le j$ is counted when the loop is at $i$, at the vector $x_j - x_i$, and not when the loop is at $j$, because then the partner $i$ fails the test $i > j + 1$. A pair with $|i - j| = 1$ is never counted. So the count is the number of H-H contacts, and SCORE returns minus that number, which is $E(w)$. $\square$

**Claim 1 (every state is valid).** For every $t$, $w_t \in V$ and $E_t = E(w_t)$.

*Proof.* By induction on $t$. The word $S^{n-2}$ of line L1 is a straight line, so its sites $(0, 0), (1, 0), \ldots, (n - 1, 0)$ are distinct, and $w_0 \in V$. Line L2 sets $E_0 = E(w_0)$ by Claim 0. Assume the claim for $t - 1$. If line L10 rejects, nothing changes. If it accepts, then either $E' \le E_{t-1} < +\infty$, or $\text{random}() < e^{-(E' - E_{t-1})/T}$, which is false when $E' = +\infty$ because the right side is $0$. So an accepted $w'$ has $E' < +\infty$, hence $w' \in V$ by Claim 0, and line L11 sets $E_t = E' = E(w_t)$. $\square$

**Claim 2 (the returned pair).** After step $t$, $E^* = \min\{E_0, \ldots, E_t\}$ and $w^*$ is one of $w_0, \ldots, w_t$ with $E(w^*) = E^*$. So line L14 returns a valid word and its exact energy, and no visited word has a lower energy.

*Proof.* By induction on $t$. Line L2 gives the claim for $t = 0$. Assume it for $t - 1$. If step $t$ rejects, $E_t = E_{t-1}$, the minimum does not change, and lines L12 and L13 do not run. If it accepts, line L12 compares $E_t$ with $E^* = \min\{E_0, \ldots, E_{t-1}\}$, and line L13 replaces the pair by $(E_t, w_t)$ exactly when $E_t$ is smaller. In both cases the new $E^*$ is $\min\{E_0, \ldots, E_t\}$, and by Claim 1 the stored word has this energy. The loops of lines L3 and L4 are finite, so line L14 is reached. $\square$

**Claim 3 (detailed balance with a full library).** Fix a stage with fragment length $k$, and assume that $T$ is constant and that $F_j = \{L, S, R\}^k$ for each of the $m = n - 1 - k$ windows. Let $\pi(w) = e^{-E(w)/T} / Z$ for $w \in V$, with $Z = \sum_{v \in V} e^{-E(v)/T}$. Then the transition probabilities $P$ of one step satisfy $\pi(w) P(w, w') = \pi(w') P(w', w)$ for all $w, w' \in V$, and $\pi$ is a stationary distribution of the chain on $V$.

*Proof.* Lines L6 to L8 propose $w'$ from $w$ with probability
$$R(w, w') = \frac{1}{m \, 3^k} \bigl|\{j : w \text{ and } w' \text{ agree outside } j, \ldots, j + k - 1\}\bigr|,$$
because each window has probability $1/m$ and, given the window, each of the $3^k$ fragments has probability $3^{-k}$ and gives exactly one word. The set in the formula does not change when $w$ and $w'$ are swapped, so $R(w, w') = R(w', w)$. For $w' \ne w$ with $w' \in V$, line L10 accepts with probability $\min(1, e^{-(E(w') - E(w))/T})$: with probability 1 when $E(w') \le E(w)$, and otherwise when a fresh uniform number is below $e^{-(E(w') - E(w))/T} < 1$. So
$$P(w, w') = R(w, w') \min\bigl(1, e^{-(E(w') - E(w))/T}\bigr), \qquad w \ne w',\ w, w' \in V.$$
A proposal outside $V$ is rejected by Claim 1, so it adds to $P(w, w)$, and the chain stays in $V$. Let $a = E(w) \le b = E(w')$, without loss of generality. Then $Z \pi(w) P(w, w') = e^{-a/T} R(w, w') e^{-(b - a)/T} = R(w, w') e^{-b/T}$ and $Z \pi(w') P(w', w) = e^{-b/T} R(w', w)$. These are equal because $R$ is symmetric. For $w = w'$ the equation is trivial. Summing it over $w \in V$ gives $\sum_{w} \pi(w) P(w, w') = \pi(w') \sum_{w} P(w', w) = \pi(w')$, since each row of $P$ sums to 1 on $V$. $\square$

If in addition the graph on $V$ with an edge where $R(w, w') > 0$ is connected, the chain is irreducible, and the argument of the [simulated annealing](/simulated-annealing/) page shows that the distribution of $w_t$ converges to $\pi$ when $E$ is not constant on $V$. For $k = n - 2$ the graph is complete, because the single window covers the whole word. For smaller $k$ connectivity is a property of the lattice and of $n$, and the proof above does not use it.

**What is not claimed.** The geometric schedule of line L5 and the finite number of steps give no bound on $E^* - \min_{w \in V} E(w)$. The problem is [NP-hard](/hp-folding-np-completeness/), and the only general guarantee for annealing is asymptotic, under a logarithmic schedule, see [convergence of simulated annealing](/simulated-annealing-convergence/). A library picked from known structures has $F_j$ smaller than $\{L, S, R\}^k$, and then $R$ need not be symmetric and some words of $V$ need not be reachable, as the example of the page shows.
