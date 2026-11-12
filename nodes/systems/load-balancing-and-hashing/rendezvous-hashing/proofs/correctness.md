---
title: Rendezvous hashing agrees across clients, moves only the necessary keys, and gives weighted shares exactly
proves: [correctness]
status: full
---

We use the pseudocode of the page. A *score function* $h$ maps each pair (key, server) to a value in a totally ordered set. Ties are broken by a fixed total order on the server names, so we can treat the pair $(h(k, s), s)$ as the score, and two different servers never have equal scores. For a finite nonempty set $S$ of servers, write $f_S(k) = \arg\max_{s \in S} (h(k, s), s)$.

**Lemma 1 (the procedure computes the argmax).** HRW$(k, S)$ returns $f_S(k)$.

*Proof.* The loop of line L2 keeps this invariant: after the servers $s_1, \ldots, s_j$ are seen, $best$ is the server with the largest score among them, and $bestScore$ is its score. Before the loop no server is seen and $bestScore = -\infty$. In the step for $s_{j+1}$, line L4 compares the new score with the largest of the first $j$ scores, and line L5 replaces $best$ if and only if the new score is larger. So the invariant holds after the step. When the loop ends, all of $S$ is seen. $\square$

**Lemma 2 (agreement).** The result depends only on $k$ and on the set $S$, not on the order in which the loop sees the servers and not on earlier calls.

*Proof.* The argmax of a set of distinct values does not depend on the order of the set. The procedure keeps no state between calls. $\square$

So two clients that know the same server set send a key to the same server without any communication. This is the property that Thaler and Ravishankar needed for a group of clients in front of a group of caches.

**Theorem 1 (removal).** Let $r \in S$ and $|S| \ge 2$. For each key $k$ with $f_S(k) \ne r$, $f_{S \setminus \{r\}}(k) = f_S(k)$.

*Proof.* Let $s^* = f_S(k)$. The score of $s^*$ is larger than the score of each server of $S$, and $S \setminus \{r\} \subseteq S$ contains $s^*$. So $s^*$ is also the largest in $S \setminus \{r\}$. $\square$

**Theorem 2 (addition).** Let $t \notin S$. For each key $k$, $f_{S \cup \{t\}}(k) \in \{f_S(k), t\}$.

*Proof.* Apply Theorem 1 to the set $S \cup \{t\}$ with $r = t$. If the winner over $S \cup \{t\}$ is not $t$, it is the winner over $S$. $\square$

Theorem 2 is the [monotonicity property](/monotonicity-property/) of Karger et al.: when a server is added, a key moves only to the new server.

**Theorem 3 (balance in the random oracle model).** Assume that the scores $h(k, s)$ are independent and uniform on $[0, 1)$ (a continuous model, so ties have probability 0). Then for each key and each $s \in S$, $\Pr[f_S(k) = s] = 1/|S|$. With $m$ keys, the expected number of keys on each server is $m/|S|$. When a server $t$ is added, the expected number of keys that move is $m/(|S| + 1)$.

*Proof.* The scores of one key on the $n = |S|$ servers are independent and identically distributed, so each permutation of the servers is equally likely to be their order by score, and each server is first with probability $1/n$. Linearity of expectation gives $m/n$. By Theorem 2 a key moves on the addition of $t$ if and only if $t$ wins over $S \cup \{t\}$, which has probability $1/(n+1)$. $\square$

With the 64-bit scores of the implementation, a tie on one key has probability at most $\binom{n}{2} 2^{-64}$, and the name order then decides, so the bounds hold up to this term. The loads are not exactly equal: the load of one server is a binomial variable with $m$ trials and success probability $1/n$, and its spread is the subject of [balls into bins](/balls-into-bins-max-load/).

**Theorem 4 (weighted shares).** Let server $i$ have weight $w_i > 0$, let $W = \sum_i w_i$, and let $U_1, \ldots, U_n$ be independent and uniform on $(0, 1)$. Then

$$\Pr\left[\arg\max_i \frac{-w_i}{\ln U_i} = j\right] = \frac{w_j}{W}.$$

*Proof.* Let $E_i = -\ln U_i$. Then $\Pr[E_i > x] = \Pr[U_i < e^{-x}] = e^{-x}$ for $x \ge 0$, so $E_i$ is exponential with rate 1, and the $E_i$ are independent. The score is $w_i / E_i$, which is positive, so the largest score belongs to the smallest $T_i = E_i / w_i$. Here $\Pr[T_i > t] = \Pr[E_i > w_i t] = e^{-w_i t}$, so $T_i$ is exponential with rate $w_i$, with density $w_i e^{-w_i t}$. Then

$$\Pr[T_j < \min_{i \ne j} T_i] = \int_0^\infty w_j e^{-w_j t} \prod_{i \ne j} e^{-w_i t} \, dt = \int_0^\infty w_j e^{-W t} \, dt = \frac{w_j}{W}.$$

Ties have probability 0 because the $T_i$ have densities. $\square$

**Theorem 5 (weighted changes).** In weighted HRW the score of server $i$ depends only on the key, on the name of $i$ and on $w_i$. So Theorems 1 and 2 hold for weighted HRW without change. If only $w_r$ grows, a key can only move to $r$. If only $w_r$ falls, only keys on $r$ can move.

*Proof.* The first part is the proof of Theorems 1 and 2, which used only that each score does not depend on the other servers. If $w_r$ grows, the score of $r$ grows and the other scores stay. A key whose winner changes must now have $r$ as its winner. If $w_r$ falls, the score of $r$ falls and the other scores stay. A key whose winner was not $r$ keeps a winner whose score is still larger than every other score. $\blacksquare$
