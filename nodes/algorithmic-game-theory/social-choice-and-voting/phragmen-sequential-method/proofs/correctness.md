---
title: Sequential Phragmen is committee monotone, extends D'Hondt and satisfies proportional justified representation
proves: [correctness]
status: full
---

An approval profile has ballots $A_1, \ldots, A_n \subseteq \{0, \ldots, m - 1\}$, and $k$ is the committee size with $0 \le k \le m$. For a candidate $c$, $N(c) = \{i : c \in A_i\}$ is the set of its supporters. The method keeps a load $y_i$ for each voter, starting at $0$. In round $r$ it computes, for every candidate $c$ not yet elected with $N(c) \ne \emptyset$,

$$t_r(c) = \frac{1 + \sum_{i \in N(c)} y_i}{|N(c)|},$$

elects the candidate $c_r$ with the least $t_r(c)$ (ties to the smallest index), sets $t_r = t_r(c_r)$, and sets $y_i = t_r$ for every $i \in N(c_r)$. If no unelected candidate has a supporter, it elects the smallest unelected index, which changes no load.

## What the code computes

`seq_phragmen` keeps the list of supporters of each candidate, computes $t_r(c)$ by the formula with exact fractions, keeps the first candidate with the least value, and updates the loads of its supporters. So it computes the method as defined, with the stated tie-breaking.

## Loads and times

**Lemma 1.** Let $t_0 = 0$. After round $r$, every load is at most $t_r$, and $t_1 \le t_2 \le \cdots$ over the rounds that elect a supported candidate.

*Proof.* By induction on $r$. Before round $r$, every load is at most $t_{r-1}$ (the time of the last round with a supported candidate, or $0$). For a supporter $i$ of $c_r$ the new load is $t_r$. The other loads do not change.

To show $t_{r-1} \le t_r$, let round $r' < r$ be the last round before $r$ that elected a supported candidate, so $t_{r-1} = t_{r'}$. Loads only grow over time: a supporter $i$ of $c_{r'}$ had $y_i \le t_{r'-1} \le t_{r'}$ by induction, and its new load is $t_{r'}$. So for each candidate $c$ the value $t(c)$ does not decrease from round $r'$ to round $r$, and $c_r$ was a candidate in round $r'$ as well. Hence $t_r = t_r(c_r) \ge t_{r'}(c_r) \ge t_{r'}$. $\square$

**Lemma 2.** When $c_r$ is elected, its supporters pay $t_r - y_i \ge 0$ each, and these payments add up to $1$. So after the method ends, $\sum_i y_i$ equals the number of supported candidates elected, and $y_i$ is the total that voter $i$ paid.

*Proof.* By Lemma 1, $y_i \le t_r$ before round $r$. The payments add up to $|N(c_r)| \, t_r - \sum_{i \in N(c_r)} y_i = 1$ by the definition of $t_r$. $\square$

This is the continuous form of the method: each voter earns money at rate $1$, and $t_r(c)$ is the first time at which the supporters of $c$ have $1$ in total, counting what each has left after its earlier payments.

## Committee monotonicity

Rounds $1, \ldots, k$ do not depend on $k$. So the committee for $k + 1$ seats is the committee for $k$ seats plus one candidate.

## Proportional justified representation

A committee $W$ of size $k$ violates proportional justified representation (PJR) if there are an integer $\ell$ with $1 \le \ell \le k$ and a nonempty group $S$ of voters with $|S| \ge \ell n / k$ and $|\bigcap_{i \in S} A_i| \ge \ell$, such that $|W \cap \bigcup_{i \in S} A_i| < \ell$.

**Theorem.** The committee of sequential Phragmen satisfies PJR.

*Proof.* Suppose that $W$ violates PJR with $\ell$ and $S$, and let $s = |S| \ge 1$. The members of $W$ that some voter of $S$ approves are fewer than $\ell$. Each voter of $S$ pays only for members that it approves, and the total payment for one member is $1$. By Lemma 2, $\sum_{i \in S} y_i \le \ell - 1$ at every point of the method.

The common set $T = \bigcap_{i \in S} A_i$ has at least $\ell$ candidates, and at most $\ell - 1$ of them are in $W$. So some $c \in T$ is never elected, and $c$ is a candidate with $S \subseteq N(c)$ in every round. Let $t^* = \ell / s$, so $t^* \le k / n$.

We show by induction that $t_r \le t^*$ for every round $r$ that elects a supported candidate. Suppose all earlier times are at most $t^*$. By Lemma 1 every load is at most $t^*$, so

$$|N(c)| \, t^* - \sum_{i \in N(c)} y_i = \sum_{i \in N(c)} (t^* - y_i) \ge \sum_{i \in S} (t^* - y_i) \ge s t^* - (\ell - 1) = 1.$$

So $t_r(c) \le t^*$, and $t_r \le t_r(c) \le t^*$. Also $c$ always has a supporter, so every round elects a supported candidate.

At the end, all $k$ elected candidates are supported, every load is at most $t^*$, and by Lemma 2

$$k = \sum_{i \notin S} y_i + \sum_{i \in S} y_i \le (n - s) \, t^* + \ell - 1 = \frac{\ell n}{s} - 1 \le k - 1,$$

which is a contradiction. $\square$

PJR implies justified representation (the case $\ell = 1$). The method does not satisfy extended justified representation: Example 6 of Brill, Freeman, Janson and Lackner, which the tests check, has $n = 24$, $k = 12$ and four voters who approve $a$ and $b$ but get only one approved member each.

## Party lists

Let the voters split into parties, the $v_p$ voters of party $p$ all approve the same list of $k$ candidates, and the lists be disjoint. If party $p$ has $s_p$ elected members, its voters all have the load $s_p / v_p$, because each member costs $1$ and is shared equally by the same $v_p$ voters. So the next candidate of party $p$ has $t = (1 + s_p) / v_p$, and the method elects from the party with the largest $v_p / (s_p + 1)$. This is the D'Hondt rule of highest averages, with ties to the party whose candidates have smaller indices.

## Running time

Each round computes $t_r(c)$ for at most $m$ candidates, with $|N(c)|$ additions each, so a round takes $O(m + \sum_c |N(c)|) = O(mn)$ arithmetic operations, and the $k$ rounds take $O(kmn)$. The supporter lists take $O(mn)$ space.
