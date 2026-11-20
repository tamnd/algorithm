---
title: The table counts the swings of each size, and the indices follow from these counts
proves: [correctness]
status: full
---

The game is $[q; w_1, \ldots, w_n]$ with nonnegative integer weights and an integer quota $1 \le q \le w(N)$. A coalition $S$ wins if $w(S) \ge q$. Fix the player $i$ and let $J$ be the set of the players $j \ne i$ that the loop of line L2 has handled so far.

**Lemma (table).** After the loop of line L2 has handled the players in $J$, for each $0 \le s \le n-1$ and $0 \le k \le q-1$, the entry $C[s][k]$ is the number of sets $S \subseteq J$ with $|S| = s$ and $w(S) = k$.

*Proof.* By induction on $|J|$. Line L1 sets $C[0][0] = 1$ and every other entry to 0. For $J = \emptyset$ the only subset is $\emptyset$, with size 0 and weight 0, so the claim is true.

Assume that the claim is true for $J$ and that line L2 now handles the player $j$. Write $C$ for the table before this step and $C'$ for the table after it. A set $S' \subseteq J \cup \{j\}$ with $|S'| = s + 1$ and $w(S') = k'$ either does not contain $j$, and then it is a subset of $J$ of the same size and weight, or it contains $j$, and then $S' \setminus \{j\}$ is a subset of $J$ with size $s$ and weight $k' - w_j$. So the correct new value is $C'[s+1][k'] = C[s+1][k'] + C[s][k' - w_j]$, where the second term is 0 if $k' < w_j$. The entries of row 0 do not change, which is correct, because the only set of size 0 is $\emptyset$.

We show that lines L3 to L5 compute exactly this. Line L5 at the step $(s, k)$ reads $C[s][k]$ and adds it to $C[s+1][k+w_j]$. The loop of line L3 goes down from $s = n-2$ to $s = 0$. At the step $s$, row $s+1$ is written. Row $s+1$ was read only at the earlier step $s+1$, and row $s$ is written only at the later step $s-1$. So every read of row $s$ sees the value from before the handling of $j$, even when $w_j = 0$, because the read and the write are always in different rows. Inside one step $s$ the reads are in row $s$ and the writes in row $s+1$, so the order of $k$ does not matter.

Line L4 takes each $k$ with $0 \le k$ and $k + w_j \le q-1$, so line L5 adds $C[s][k'-w_j]$ to each entry $C[s+1][k']$ with $w_j \le k' \le q-1$, and to no other entry. For $k' < w_j$ the correct second term is 0, and the entry does not change. So $C' = $ the correct table on the range $0 \le k' \le q-1$. The loop of line L3 covers the rows $s + 1$ from $1$ to $n-1$, and a subset of $J$ has at most $n-1$ players, so no size is missed.

One more point needs care: line L5 drops each set of weight $q$ or more. This is safe, because a set of weight at least $q$ only grows in weight when the later steps add players to it, since the weights are nonnegative. So no entry with $k \le q-1$ ever needs a count of a set of weight $q$ or more. $\square$

**Lemma (swings).** After the loop of line L2 ends, line L6 sets $c_s$ to the number of swings of $i$ of size $s$: sets $S \subseteq N \setminus \{i\}$ with $|S| = s$, $w(S) \le q-1$ and $w(S) + w_i \ge q$.

*Proof.* At the end, $J = N \setminus \{i\}$. A set $S \subseteq J$ is a swing if and only if $q - w_i \le w(S) \le q-1$, which is $\max(0, q - w_i) \le w(S) \le q-1$ since weights are nonnegative. Line L6 adds the entries $C[s][k]$ for exactly these $k$, and by the table lemma each entry counts the sets of size $s$ and weight $k$. $\square$

**Theorem.** Line L7 returns the raw Banzhaf index $\beta_i$ of $i$, and line L8 returns the Shapley-Shubik index $\varphi_i$ of $i$.

*Proof.* The game is monotone: if $S \subseteq T$ then $w(S) \le w(T)$, so $v(S) \le v(T)$. Hence the marginal contribution $v(S \cup \{i\}) - v(S)$ of $i$ to a set $S \not\ni i$ is 0 or 1, and it is 1 exactly when $S$ is a swing of $i$.

The raw Banzhaf index is the mean of the marginal contribution over the $2^{n-1}$ sets $S \subseteq N \setminus \{i\}$, so it is the number of swings divided by $2^{n-1}$. By the swings lemma, this number is $\sum_s c_s$, which line L7 uses.

The Shapley-Shubik index is the Shapley value of the simple game. By the subset formula,
$$\varphi_i = \sum_{S \subseteq N \setminus \{i\}} \frac{|S|!\,(n-|S|-1)!}{n!} \big(v(S \cup \{i\}) - v(S)\big).$$
The weight depends only on $|S|$, and the bracket is 1 for the swings and 0 for the other sets. If we group the sets by size, the sum is $\sum_{s=0}^{n-1} \frac{s!\,(n-1-s)!}{n!} c_s$, which is line L8. $\blacksquare$

**Normalized index.** The normalized Banzhaf index divides the swings of $i$ by the sum of the swings of all players. This sum is positive: in each order of the players, the first player whose arrival takes the weight to $q$ or more is a swing for the set of the players before it, and such a player exists because $w(N) \ge q$ and $w(\emptyset) = 0 < q$.
