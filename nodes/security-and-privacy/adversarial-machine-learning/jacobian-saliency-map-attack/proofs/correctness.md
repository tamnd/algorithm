---
title: JSMA changes only the chosen features, stays in the box and in the budget, and stops
proves: [correctness]
status: full
---

Let $x \in [0,1]^d$, $\theta > 0$, target class $t$ and $\Gamma = \lfloor \gamma d \rfloor$ the budget of line L2, where $\gamma$ is `max_distortion`. Let $D_0 = \{i : x_i < 1\}$ be the first search domain (line L1). The list $C$ is `changed`.

**Lemma 1 (the pair rule).** `saliency_pair` returns a pair $(p, q)$ of distinct indices of the domain with $\alpha_{pq} > 0$, $\beta_{pq} < 0$ and the largest value of $-\alpha_{pq}\beta_{pq}$, where $\alpha_{pq} = \partial_p z_t + \partial_q z_t$ and $\beta_{pq} = \sum_{j \ne t} (\partial_p z_j + \partial_q z_j)$. Ties go to the first such pair in the order of the domain. If no pair has $\alpha > 0$ and $\beta < 0$, it returns `None`.

*Proof.* The double loop visits each unordered pair of distinct positions $u < v$ of the domain once, in order. It replaces the best pair only when the pair is allowed and its value is strictly larger than the best so far, which starts at $0$. An allowed pair has $-\alpha\beta > 0$, so the first allowed pair is always taken, and a later pair replaces it only with a strictly larger value. $\square$

**Lemma 2 (the loop invariant).** Each time line L3 is checked, these hold:

1. $C$ has no repeated index, $|C|$ is even and $|C| \le \Gamma$.
2. The domain is $D_0 \setminus C$, in the order of the indices.
3. $x^a_i = x_i$ for $i \notin C$, and $x^a_i = \min(x_i + \theta, 1)$ for $i \in C$.
4. $x^a \in [0,1]^d$, and $x^a_i \ne x_i$ exactly when $i \in C$.

*Proof.* At the first check, $C$ is empty, the domain is $D_0$ and $x^a = x$, so the claims hold. Suppose they hold at one check and the loop body runs to line L7. Then line L3 gave $|C| + 2 \le \Gamma$. Line L5 returned two distinct indices $p, q$ of the domain, so by part 2 they are in $D_0$ and not in $C$. Line L7 sets $x^a_p = \min(x_p + \theta, 1)$ and the same for $q$ (part 3 says these two coordinates still had their start values), removes both from the domain and appends both to $C$. So $C$ gets two new distinct indices and its size stays even and at most $\Gamma$, and parts 2 and 3 hold again. For part 4, $x_i < 1$ for $i \in D_0$ and $\theta > 0$, so $x_i < \min(x_i + \theta, 1) \le 1$, and $x_i \ge 0$. If the body leaves at line L6, nothing changes. $\square$

**Theorem 1 (the output).** The attack stops after at most $\lfloor \Gamma / 2 \rfloor$ passes of the loop. It returns $(x^a, s, C)$ with $x^a \in [0,1]^d$, $\lVert x^a - x \rVert_0 = |C| \le \Gamma$, $x^a \ge x$ in every coordinate, and $s$ true exactly when $\arg\max_k z_k(x^a) = t$.

*Proof.* Each full pass adds two indices to $C$, and line L3 needs $|C| + 2 \le \Gamma$ before a pass. So there are at most $\lfloor \Gamma / 2 \rfloor$ full passes, and at most one more pass that leaves at line L6. The properties of $x^a$ and $C$ are Lemma 2 at the last check, together with $\min(x_i + \theta, 1) \ge x_i$. Line L8 computes $s$ from the label of $x^a$. $\blacksquare$

**Corollary (success means a valid targeted adversarial input).** If $s$ is true, then $x^a$ is in the box, has the label $t$, and differs from $x$ in at most $\Gamma$ features. So every reported success is a real one for the given model.

**What is not claimed.** JSMA is greedy. It does not find the smallest set of features. On the 500 random affine models of the seeded test, JSMA succeeds in 94 cases, and in 82 of them an exhaustive search over feature sets set to 1 finds a smaller successful set. In 64 of the cases where JSMA fails, such a set exists (a measurement, partly because JSMA changes features in pairs). A failure of JSMA ($s$ false) does not prove that no change of $\Gamma$ features reaches $t$.
