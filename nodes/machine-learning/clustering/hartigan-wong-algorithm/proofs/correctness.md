---
title: Hartigan's method lowers the cost at each move, stops, and returns a Lloyd fixed point
proves: [correctness]
status: full
---

For a finite non-empty set $Q$ of points let $\mu(Q)$ be its mean and $\mathrm{cost}(Q) = \sum_{y \in Q} \|y - \mu(Q)\|^2$. The cost of a partition is the sum of the costs of its clusters.

**Lemma 1 (adding a point).** Let $|Q| = m \ge 1$, $c = \mu(Q)$ and $x$ a point. Then $\mathrm{cost}(Q \cup \{x\}) = \mathrm{cost}(Q) + \frac{m}{m + 1}\|x - c\|^2$, and $\mu(Q \cup \{x\}) = (mc + x)/(m + 1)$. For $m = 0$ the cost of $\{x\}$ is $0 = \frac{0}{1}\|x - c\|^2$ for any $c$.

*Proof.* The new mean is $c' = c + \frac{x - c}{m + 1}$. By the centroid identity, $\sum_{y \in Q}\|y - c'\|^2 = \mathrm{cost}(Q) + m\|c - c'\|^2 = \mathrm{cost}(Q) + \frac{m}{(m+1)^2}\|x - c\|^2$. Also $x - c' = \frac{m}{m + 1}(x - c)$, so $\|x - c'\|^2 = \frac{m^2}{(m+1)^2}\|x - c\|^2$. The sum is $\mathrm{cost}(Q) + \frac{m + m^2}{(m+1)^2}\|x - c\|^2 = \mathrm{cost}(Q) + \frac{m}{m + 1}\|x - c\|^2$. $\square$

**Lemma 2 (removing a point).** Let $P$ contain $x$, $|P| = m \ge 2$ and $c = \mu(P)$. Then $\mathrm{cost}(P \setminus \{x\}) = \mathrm{cost}(P) - \frac{m}{m - 1}\|x - c\|^2$, and $\mu(P \setminus \{x\}) = (mc - x)/(m - 1)$.

*Proof.* Let $Q = P \setminus \{x\}$, with $|Q| = m - 1$ and mean $c' = (mc - x)/(m - 1)$. Then $x - c' = \frac{(m - 1)x - mc + x}{m - 1} = \frac{m}{m - 1}(x - c)$. By Lemma 1 applied to $Q$ and $x$, $\mathrm{cost}(P) = \mathrm{cost}(Q) + \frac{m - 1}{m}\|x - c'\|^2 = \mathrm{cost}(Q) + \frac{m - 1}{m} \cdot \frac{m^2}{(m - 1)^2}\|x - c\|^2 = \mathrm{cost}(Q) + \frac{m}{m - 1}\|x - c\|^2$. $\square$

**Invariant.** At the start of each step of line L4, $n_j$ is the size of cluster $j$, and $c_j$ is its mean when $n_j \ge 1$.

*Proof.* Line L1 makes it true. Lines L9 and L10 update the sizes and use the formulas for the means of Lemmas 2 and 1. No other line changes $a$, $n$ or $c$. $\square$

**Lemma 3 (each move).** A move of line L8 to L11 changes the cost by $\frac{n_q}{n_q + 1}\|x_i - c_q\|^2 - \frac{n_p}{n_p - 1}\|x_i - c_p\|^2 < 0$.

*Proof.* By the invariant, $n_p \ge 2$ is the size and $c_p$ the mean of cluster $p$, and the same for $q$. Only the clusters $p$ and $q$ change. By Lemma 2 the cost of $p$ falls by $r = \frac{n_p}{n_p - 1}\|x_i - c_p\|^2$, and by Lemma 1 the cost of $q$ rises by $\frac{n_q}{n_q + 1}\|x_i - c_q\|^2$. Line L8 moves only when the rise is less than $r$. $\square$

**Theorem.** The loop of lines L2 to L12 stops. At the end no single move of one point to another cluster lowers the cost (the partition is Hartigan stable), each point is at a nearest mean of the non-empty clusters, and the cost is at most the cost of the initial labels.

*Proof.* The cost is a function of the labels, and the labels take at most $k^n$ values. By Lemma 3 each move lowers the cost strictly, so no labeling occurs twice, and there are fewer than $k^n$ moves. Each pass of lines L4 to L11 that does not end the loop makes a move, so the loop ends.

The last pass made no move. During that pass nothing changed, so for each point $x_i$ with $n_p \ge 2$ and each cluster $j \ne p$, $\frac{n_j}{n_j + 1}\|x_i - c_j\|^2 \ge \frac{n_p}{n_p - 1}\|x_i - c_p\|^2$, because line L7 takes the least left side. By Lemmas 1 and 2 this says that no single move of $x_i$ lowers the cost. A point alone in its cluster cannot move without emptying it, which line L5 forbids.

Now let $x$ be in cluster $i$ and let $c_j$ be the mean of another non-empty cluster. If $n_i = 1$ then $x = c_i$ and $\|x - c_i\| = 0 \le \|x - c_j\|$. If $n_i \ge 2$, stability gives
$$\|x - c_j\|^2 \ge \frac{n_j}{n_j + 1}\|x - c_j\|^2 \ge \frac{n_i}{n_i - 1}\|x - c_i\|^2 \ge \|x - c_i\|^2 .$$
So each point is at a nearest mean, and each cluster has its mean as center: the partition is a fixed point of Lloyd's algorithm. The cost bound holds because each move lowers the cost. $\square$

**Remark (strictly fewer optima).** The converse fails. In the rectangle with corners $(0,0), (0,1), (2,0), (2,1)$, the partition bottom and top is a Lloyd fixed point of cost 4, but moving $(0,0)$ to the top cluster lowers the cost by $2 - \frac{4}{3} = \frac{2}{3}$.
