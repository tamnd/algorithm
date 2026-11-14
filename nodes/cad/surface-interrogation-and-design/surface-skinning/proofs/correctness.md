---
title: The skinned surface contains every section
proves: [correctness]
status: full
---

We use the pseudocode and the notation of the page. The sections $C_0, \dots, C_K$, $K \ge 1$, are clamped B-spline curves of one degree $p$ on one parameter interval, and the parameters $v_0 < \dots < v_K$ increase, whether they are given or come from line L2.

## Lemma 1 (common basis)

After line L1 there are control points $P_{k,i}$ with $C_k(u) = \sum_{i=0}^{n} N_i(u) P_{k,i}$ for every $k$ and every $u$, where $N_0, \dots, N_n$ are the B-spline basis functions of degree $p$ on the merged knot vector $U$.

*Proof.* The merged vector $U$ contains each knot vector of a section as a sub-multiset, because each knot value appears in $U$ with its largest multiplicity in any section. The end knots of all sections are the same, so every missing knot is an inner knot of $U$, and its multiplicity in $U$ is at most $p$ because it is at most $p$ in the section where it is largest. So the missing knots of $C_k$ can be inserted one at a time, and by the theorem on the [Boehm knot insertion](/boehm-knot-insertion/) page each insertion gives new control points on the larger knot vector that define the same curve. After the last insertion the knot vector is $U$ for every $k$. $\square$

## Lemma 2 (the interpolation in $v$)

Let $q' = \min(q, K)$, let $V$ be the averaged knot vector of degree $q'$ for $v_0, \dots, v_K$, with basis $M_0, \dots, M_K$, and let $A_{kl} = M_l(v_k)$. Then $A$ is nonsingular.

*Proof.* Number the knots of $V$ as $t_0, \dots, t_{K+q'+1}$. They are $t_0 = \dots = t_{q'} = v_0$, the inner knots $t_{j+q'} = (v_j + \dots + v_{j+q'-1})/q'$ for $j = 1, \dots, K - q'$, and $t_{K+1} = \dots = t_{K+q'+1} = v_K$. So there are $K + 1$ basis functions, one for each parameter, and $M_l$ is non zero only on $(t_l, t_{l+q'+1})$. Take $0 < l < K$. If $l \le q'$ then $t_l = v_0 < v_l$. If $l > q'$ then $t_l$ is the mean of $v_{l-q'}, \dots, v_{l-1}$, which are all less than $v_l$. If $l + 1 \le K - q'$ then $t_{l+q'+1}$ is the mean of $v_{l+1}, \dots, v_{l+q'}$, which are all greater than $v_l$, and otherwise $t_{l+q'+1} = v_K > v_l$. So $t_l < v_l < t_{l+q'+1}$ for $0 < l < K$, while $v_0$ and $v_K$ are the end knots, where $M_0(v_0) = M_K(v_K) = 1$. These are the conditions of the [Schoenberg-Whitney theorem](/schoenberg-whitney-theorem/), so $A$ is nonsingular. $\square$

## Theorem

The surface $S$ returned in line L5 satisfies $S(u, v_k) = C_k(u)$ for every $k = 0, \dots, K$ and every $u$.

*Proof.* By Lemma 2, line L3 has a unique solution: for each column $i$, the points $Q_{i,0}, \dots, Q_{i,K}$ with $\sum_l M_l(v_k) Q_{i,l} = P_{k,i}$ for all $k$. The system is solved for each coordinate of each column, and these are independent linear systems with the same matrix. The surface of line L5 is

$$S(u, v) = \sum_{i=0}^{n} \sum_{l=0}^{K} N_i(u) M_l(v) Q_{i,l}.$$

Fix $k$ and put $v = v_k$. Then

$$S(u, v_k) = \sum_i N_i(u) \Bigl(\sum_l M_l(v_k) Q_{i,l}\Bigr) = \sum_i N_i(u) P_{k,i} = C_k(u),$$

where the second equality is line L3 and the third is Lemma 1. $\square$

## Why the common knot vector is needed

The second equality holds for each $i$ separately: it says that the iso-curve of $S$ at $v_k$ has the control points $P_{k,0}, \dots, P_{k,n}$ on the knots $U$. The third equality needs that all sections use the same functions $N_i$. If the sections kept their own knot vectors, the column $i$ would collect control points that multiply different basis functions in different sections, and no single surface of the form above would reproduce them all: a tensor product surface has one basis in $u$ for all values of $v$.

## The parameters of line L2

The chord length parameters of one column are $0$, then the partial sums of the distances $|P_{k,i} - P_{k-1,i}|$ divided by their total, so they increase strictly when no two consecutive points of the column coincide, and they do not decrease in any case. Their average over the columns that are not a single point starts at $0$, ends at $1$, and increases strictly unless two consecutive sections have the same control points in every column, that is, unless two consecutive sections are the same curve. In that case the parameters are not increasing, line L3 has no solution, and the implementation reports it. Any other choice of increasing parameters also satisfies the theorem.
