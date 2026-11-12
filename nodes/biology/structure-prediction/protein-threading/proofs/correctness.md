---
title: The threading dynamic program is optimal in the singleton case
proves: [correctness]
status: full
---

We use the model and the pseudocode of the page. The template has $K \ge 1$ core segments of lengths $c_k \ge 1$, offsets $o_k = c_1 + \cdots + c_{k-1}$, and minimum loop lengths $g_k \ge 0$. A threading of $a_1 \ldots a_n$ is a vector $t = (t_1, \ldots, t_K)$ with $t_1 \ge 1$, $t_{k+1} \ge t_k + c_k + g_k$ for $1 \le k < K$, and $t_K + c_K - 1 \le n$. There are no pair terms, so the energy is

$$E(t) = \sum_{k=1}^{K} S_k(t_k), \qquad S_k(s) = \sum_{l=1}^{c_k} \varepsilon(o_k + l, a_{s+l-1}).$$

For $1 \le k \le K$, a *partial threading* of length $k$ is a vector $(t_1, \ldots, t_k)$ that satisfies the constraints that involve only $t_1, \ldots, t_k$, together with $t_k + c_k - 1 \le n$. Its energy is $E_k(t_1, \ldots, t_k) = \sum_{j \le k} S_j(t_j)$. Let $T_k(s)$ be the set of partial threadings of length $k$ with $t_k = s$, and let $F^*_k(s) = \min \{E_k(t) : t \in T_k(s)\}$, with $F^*_k(s) = \infty$ when $T_k(s)$ is empty.

**Lemma 1 (decomposition).** For $k \ge 2$, $(t_1, \ldots, t_k) \in T_k(s)$ if and only if $(t_1, \ldots, t_{k-1}) \in T_{k-1}(q)$ for some $q$ with $q \le s - c_{k-1} - g_{k-1}$, $t_{k-1} = q$, and $s + c_k - 1 \le n$.

*Proof.* The constraints of a partial threading of length $k$ are those of length $k - 1$ except the end condition $t_{k-1} + c_{k-1} - 1 \le n$, plus $t_k \ge t_{k-1} + c_{k-1} + g_{k-1}$ and $t_k + c_k - 1 \le n$. The end condition of length $k - 1$ follows from the other two, since $t_{k-1} + c_{k-1} - 1 < t_k \le n$. So the two sets of constraints are the same. $\square$

**Lemma 2 (recurrence).** $F^*_1(s) = S_1(s)$ for $1 \le s \le n - c_1 + 1$, and for $k \ge 2$ and $1 \le s \le n - c_k + 1$,

$$F^*_k(s) = S_k(s) + \min_{1 \le q \le s - c_{k-1} - g_{k-1}} F^*_{k-1}(q),$$

with the minimum of an empty set equal to $\infty$.

*Proof.* For $k = 1$, $T_1(s) = \{(s)\}$. For $k \ge 2$, $E_k(t_1, \ldots, t_k) = E_{k-1}(t_1, \ldots, t_{k-1}) + S_k(s)$, because no term links $t_k$ to the earlier starts. By Lemma 1, $T_k(s)$ is the union over the allowed $q$ of the sets $T_{k-1}(q)$, each extended by $s$. The least energy over a union is the least of the minima over its parts, and adding the constant $S_k(s)$ does not change which part is least. $\square$

**Lemma 3 (the loop computes the recurrence).** After line L7 for a pair $(k, s)$, $F[k][s] = F^*_k(s)$, and if this value is finite then $B[k][s] = q$ for a $q \le s - c_{k-1} - g_{k-1}$ with $F[k-1][q] = \min_{q' \le s - c_{k-1} - g_{k-1}} F^*_{k-1}(q')$.

*Proof.* By induction on $k$. For $k = 1$, line L3 sets $F[1][s] = S_1(s) = F^*_1(s)$. For $k \ge 2$, assume the claim for $k - 1$. In the loop of line L5, the threshold $s - c_{k-1} - g_{k-1}$ grows by exactly one when $s$ grows by one. So, by a second induction on $s$, after line L6 the value $best$ is the minimum of $F[k-1][q]$ over $1 \le q \le s - c_{k-1} - g_{k-1}$, and $arg$ is a $q$ that reaches it: line L6 compares the one new candidate $q$ with the minimum of all earlier candidates. By the hypothesis $F[k-1][q] = F^*_{k-1}(q)$, so line L7 sets $F[k][s]$ to the right side of Lemma 2, which is $F^*_k(s)$. $\square$

**Theorem.** If some threading exists, THREAD returns the least energy $E^* = \min_t E(t)$ and a threading $t$ with $E(t) = E^*$.

*Proof.* A threading is a partial threading of length $K$, so $E^* = \min_s F^*_K(s)$, and by Lemma 3 line L8 picks $t_K$ with $F[K][t_K] = E^*$. We show by downward induction on $k$ that the vector $(t_1, \ldots, t_k)$ built by line L9 is a partial threading in $T_k(t_k)$ with energy $F^*_k(t_k)$, extended by $t_{k+1}, \ldots, t_K$ so that the whole sum is $E^*$. For $k = K$ this is the choice of $t_K$. For the step from $k$ to $k - 1$, line L9 sets $t_{k-1} = B[k][t_k]$. By Lemma 3, $t_{k-1} \le t_k - c_{k-1} - g_{k-1}$ and $F^*_{k-1}(t_{k-1}) = F^*_k(t_k) - S_k(t_k)$, which is finite. So the constraint between segments $k - 1$ and $k$ holds, and the energy of the first $k - 1$ segments is the remaining part of the optimum. At $k = 1$ we get a threading $t$ with $E(t) = \sum_k S_k(t_k) = F^*_K(t_K) = E^*$. $\square$

**Remark (why pair terms break the proof).** With a contact $(u, v)$ between a position $u$ of segment $j$ and a position $v$ of segment $k > j$, the energy of segment $k$ depends on $t_j$, so $E_k$ is no longer $E_{k-1} + S_k(t_k)$, and Lemma 2 fails for $j < k - 1$. The page gives an instance where the optimum with the pair term differs from the singleton optimum.
