---
title: The invariant subspace algorithm stops after at most dim K + 1 steps and returns the largest (A, B)-invariant subspace in K
proves: [correctness]
status: full
---

Let $A \in \mathbb{R}^{n \times n}$, $B \in \mathbb{R}^{n \times m}$ and let $\mathcal{K} \subseteq \mathbb{R}^n$ be a subspace. Write $\mathcal{B} = \operatorname{im} B$. A subspace $\mathcal{V}$ is $(A, B)$-invariant when $A \mathcal{V} \subseteq \mathcal{V} + \mathcal{B}$. For a subspace $\mathcal{W}$, the preimage is $A^{-1} \mathcal{W} = \{x : A x \in \mathcal{W}\}$; it is a subspace even when $A$ is singular. The algorithm computes

$$\mathcal{V}_0 = \mathcal{K}, \qquad \mathcal{V}_{k+1} = \mathcal{K} \cap A^{-1}(\mathcal{V}_k + \mathcal{B}),$$

and stops at the first $k$ with $\dim \mathcal{V}_{k+1} = \dim \mathcal{V}_k$. It returns $\mathcal{V}_{k+1}$. All operations are exact (rational arithmetic in the implementation), so every dimension is computed without error.

## Lemma 1: the sequence is nonincreasing

For every $k$, $\mathcal{V}_{k+1} \subseteq \mathcal{V}_k$.

*Proof.* By induction on $k$. For $k = 0$, $\mathcal{V}_1 = \mathcal{K} \cap A^{-1}(\cdot) \subseteq \mathcal{K} = \mathcal{V}_0$. Assume $\mathcal{V}_{k} \subseteq \mathcal{V}_{k-1}$. Then $\mathcal{V}_k + \mathcal{B} \subseteq \mathcal{V}_{k-1} + \mathcal{B}$, and the preimage keeps inclusions, so $A^{-1}(\mathcal{V}_k + \mathcal{B}) \subseteq A^{-1}(\mathcal{V}_{k-1} + \mathcal{B})$. Intersect both sides with $\mathcal{K}$ to get $\mathcal{V}_{k+1} \subseteq \mathcal{V}_k$. $\square$

## Lemma 2: equal dimension means a fixed point

If $\dim \mathcal{V}_{k+1} = \dim \mathcal{V}_k$, then $\mathcal{V}_{j} = \mathcal{V}_k$ for every $j \ge k$.

*Proof.* By Lemma 1, $\mathcal{V}_{k+1} \subseteq \mathcal{V}_k$. A subspace of a finite-dimensional space with the same dimension is the whole space, so $\mathcal{V}_{k+1} = \mathcal{V}_k$. The map $\mathcal{V} \mapsto \mathcal{K} \cap A^{-1}(\mathcal{V} + \mathcal{B})$ depends only on its argument, so it maps $\mathcal{V}_{k+1} = \mathcal{V}_k$ to $\mathcal{V}_{k+2} = \mathcal{V}_{k+1}$, and so on. $\square$

## Lemma 3: termination

The loop stops after at most $\dim \mathcal{K} + 1$ evaluations of the update.

*Proof.* While the loop runs, each step lowers the dimension by at least 1 (Lemma 1 and the stop test). The dimension starts at $\dim \mathcal{K}$ and cannot go below 0. So at most $\dim \mathcal{K}$ steps lower it, and the next step finds an equal dimension. $\square$

## Lemma 4: the result is an (A, B)-invariant subspace in K

Let $\mathcal{V}^\ast$ be the returned subspace. Then $\mathcal{V}^\ast \subseteq \mathcal{K}$ and $A \mathcal{V}^\ast \subseteq \mathcal{V}^\ast + \mathcal{B}$.

*Proof.* Every $\mathcal{V}_{k}$ with $k \ge 1$ is an intersection with $\mathcal{K}$, and $\mathcal{V}_0 = \mathcal{K}$, so $\mathcal{V}^\ast \subseteq \mathcal{K}$. By Lemma 2, $\mathcal{V}^\ast = \mathcal{K} \cap A^{-1}(\mathcal{V}^\ast + \mathcal{B})$. So each $x \in \mathcal{V}^\ast$ is in $A^{-1}(\mathcal{V}^\ast + \mathcal{B})$, that is, $A x \in \mathcal{V}^\ast + \mathcal{B}$. $\square$

## Lemma 5: the result contains every (A, B)-invariant subspace in K

Let $\mathcal{V} \subseteq \mathcal{K}$ with $A \mathcal{V} \subseteq \mathcal{V} + \mathcal{B}$. Then $\mathcal{V} \subseteq \mathcal{V}_k$ for every $k$.

*Proof.* By induction on $k$. For $k = 0$, $\mathcal{V} \subseteq \mathcal{K} = \mathcal{V}_0$. Assume $\mathcal{V} \subseteq \mathcal{V}_k$ and let $x \in \mathcal{V}$. Then $A x \in \mathcal{V} + \mathcal{B} \subseteq \mathcal{V}_k + \mathcal{B}$, so $x \in A^{-1}(\mathcal{V}_k + \mathcal{B})$. Also $x \in \mathcal{K}$. So $x \in \mathcal{V}_{k+1}$. $\square$

## Theorem

The algorithm stops after at most $\dim \mathcal{K} + 1$ updates, and the returned subspace $\mathcal{V}^\ast$ is the largest $(A, B)$-invariant subspace contained in $\mathcal{K}$: it is one of them, and it contains each of them.

*Proof.* Lemma 3 gives termination. Lemma 4 shows that $\mathcal{V}^\ast$ is in the family. Lemma 5, applied at the final index, shows that each member of the family is in $\mathcal{V}^\ast$. A member of a family that contains every member is unique, so the largest element exists and the algorithm returns it. $\square$

## Lemma 6: the friend computed by the implementation

Let $\mathcal{V}$ be $(A, B)$-invariant with basis $v_1, \dots, v_q$. Complete it to a basis $v_1, \dots, v_n$ of $\mathbb{R}^n$. For each $i \le q$ choose $w_i$ and $u_i$ with $A v_i = \sum_j (w_i)_j v_j + B u_i$, where the sum runs over $j \le q$. Define $K$ by $K v_i = u_i$ for $i \le q$ and $K v_i = 0$ for $i > q$. Then $(A - B K) \mathcal{V} \subseteq \mathcal{V}$.

*Proof.* The choice of $w_i$ and $u_i$ exists because $A v_i \in \mathcal{V} + \mathcal{B}$. The matrix $K$ exists and is unique because $v_1, \dots, v_n$ is a basis: $K = U T^{-1}$ with $T = [v_1, \dots, v_n]$ and $U = [u_1, \dots, u_q, 0, \dots, 0]$. For $i \le q$, $(A - BK) v_i = A v_i - B u_i = \sum_j (w_i)_j v_j \in \mathcal{V}$. A linear map that sends a basis of $\mathcal{V}$ into $\mathcal{V}$ sends all of $\mathcal{V}$ into $\mathcal{V}$. $\square$

The implementation returns `None` for the disturbance decoupling problem exactly when $\operatorname{im} E \not\subseteq \mathcal{V}^\ast$ with $\mathcal{K} = \ker C$. When $\operatorname{im} E \subseteq \mathcal{V}^\ast$, Lemma 6 gives $K$ with $(A - BK) \mathcal{V}^\ast \subseteq \mathcal{V}^\ast$, so $(A - BK)^j E$ has its columns in $\mathcal{V}^\ast \subseteq \ker C$ for every $j \ge 0$, and the transfer function $C (sI - A + BK)^{-1} E$ is zero. The converse (no $K$ works when $\operatorname{im} E \not\subseteq \mathcal{V}^\ast$) is proved on the [disturbance decoupling problem](/disturbance-decoupling-problem/) page: for any $K$, the smallest $(A - BK)$-invariant subspace that contains $\operatorname{im} E$ is $(A, B)$-invariant and lies in $\ker C$ when the output is decoupled, so it is in $\mathcal{V}^\ast$ by Lemma 5.
