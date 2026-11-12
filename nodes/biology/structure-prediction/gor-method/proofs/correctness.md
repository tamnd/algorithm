---
title: GOR prediction computes the window sum of information, and is naive Bayes over the window
proves: [correctness]
status: full
---

We use the names and line numbers of the pseudocode on the page. The sequence is $x_0 \cdots x_{n-1}$, the half width is $h$, the set of states is $\mathcal{S}$, and $I(S; a, m)$ is any table of real numbers. The target score of state $S$ at position $j$ is

$$\mathrm{score}(j, S) = d(S) + \sum_{m \in M(j)} I(S; x_{j+m}, m), \qquad M(j) = \{ m : -h \le m \le h, \; 0 \le j + m < n \}.$$

**Lemma 1 (the scatter loop computes the window sum).** After lines L9 to L12, $\mathit{score}[j][S] = \mathrm{score}(j, S)$ for every $j$ and $S$.

*Proof.* Line L9 sets each entry to $d(S)$. Lines L10 to L12 run once for each pair $(i, m)$ with $0 \le i < n$, $-h \le m \le h$ and $0 \le i - m < n$, and add $I(S; x_i, m)$ to entry $(i - m, S)$. Map such a pair to $(j, m) = (i - m, m)$. Then $0 \le j < n$ and $0 \le j + m = i < n$, so $m \in M(j)$. The map is one to one, with inverse $(j, m) \mapsto (j + m, m)$, and it reaches every pair $(j, m)$ with $m \in M(j)$. So entry $(j, S)$ receives exactly one term $I(S; x_{j+m}, m)$ for each $m \in M(j)$, and no other term. $\square$

**Theorem 1.** GOR-PREDICT returns, at each position $j$, the first state in the order of $\mathcal{S}$ with the largest value of $\mathrm{score}(j, S)$.

*Proof.* By Lemma 1 the table holds the scores. Line L13 scans the states in order and replaces the current best only on a strictly larger score, so it keeps the first maximum. $\square$

**Theorem 2 (naive Bayes form).** Let a joint distribution on states $S$ and windows be given, with $P(S) > 0$ for each $S$, and suppose that the residues at the offsets of a window are independent given the central state: $P(x_{j+m}, m \in M(j) \mid S) = \prod_{m \in M(j)} P(x_{j+m} \text{ at } m \mid S)$. Let $I(S; a, m) = \ln \big( P(S \mid a \text{ at } m) / P(S) \big)$ and $d(S) = \ln P(S)$. Then for each $j$ the scores and the log posterior differ by a constant that does not depend on $S$:

$$\mathrm{score}(j, S) = \ln P\big(S \mid x_{j+m}, m \in M(j)\big) + C_j.$$

So the predicted state is a state of largest posterior probability given the window.

*Proof.* Write $R_m$ for the event that the residue $x_{j+m}$ is at offset $m$. By Bayes' theorem, $P(R_m \mid S) = P(S \mid R_m) P(R_m) / P(S)$. With the independence assumption,

$$P\big(S \mid R_m, m \in M(j)\big) = \frac{P(S) \prod_{m} P(R_m \mid S)}{Z_j} = \frac{P(S) \prod_{m} P(S \mid R_m) / P(S)}{Z_j} \prod_m P(R_m),$$

where $Z_j$ is the probability of the window and the products run over $m \in M(j)$. Take logarithms. The terms $\ln Z_j$ and $\sum_m \ln P(R_m)$ do not depend on $S$, and what remains is $\ln P(S) + \sum_m \ln \big( P(S \mid R_m)/P(S) \big) = d(S) + \sum_m I(S; x_{j+m}, m)$. $\square$

The training loop of lines L1 to L7 computes estimates of these probabilities from counts: it counts, for each state $S$, offset $m$ and residue $a$, the positions with state $S$ that have $a$ at offset $m$ (lines L4 and L5 visit each such triple once for each position $j$ and each $m \in M(j)$), and it adds a pseudocount $c$ to each count. With $c > 0$ the estimates are positive, so every logarithm of line L7 is defined. With $c = 0$ the estimates are the maximum likelihood estimates, and the theorem holds for the empirical distribution whenever all the counts are positive.

**Cost.** Training on a set of $N$ labelled residues costs $O(N(2h + 1))$ time for the counts and $O(K (2h + 1) A)$ time for the table, with $K$ states and $A$ amino acids. Prediction on $n$ residues costs $O(n (2h + 1) K)$ time, by the count of pairs in Lemma 1, and $O(nK)$ space for the scores.
