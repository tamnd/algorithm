---
title: The MVV algorithm returns only perfect matchings and finds one with probability at least 1/2 per trial
proves: [correctness, termination]
status: full
---

Let $G = (V, E)$ be a general graph with $V = \{1, \ldots, n\}$ and $m = |E|$. For weights $w : E \to \{1, 2, \ldots\}$, let $B$ be the skew-symmetric matrix with $B_{ij} = 2^{w(ij)}$ and $B_{ji} = -2^{w(ij)}$ for each edge $ij$ with $i < j$, and 0 elsewhere. For a perfect matching $M$ write $w(M) = \sum_{e \in M} w(e)$. For a nonzero integer $D$, $\nu_2(D)$ is the exponent of 2 in $D$.

**Termination.** Line L1 runs at most $k$ trials, and each trial does a bounded amount of exact arithmetic. So the algorithm stops. $\square$

**Lemma 1 (only checked output).** If the algorithm returns a set $M$, then $M$ is a perfect matching of $G$. If $G$ has no perfect matching, the algorithm returns "none".

*Proof.* Line L8 returns $M$ only after it checks that $M \subseteq E$ and that every vertex is on exactly one edge of $M$. If $G$ has no perfect matching, no set passes this check, so line L9 is reached. $\square$

**Lemma 2 (isolation lemma).** Let $\mathcal F$ be a nonempty family of subsets of a finite set $S$ with $|S| = m$. Choose $w(e)$ uniformly and independently from $\{1, \ldots, N\}$ for each $e \in S$. Then the probability that two different sets of $\mathcal F$ both have the least weight is at most $m / N$.

*Proof.* Call $e \in S$ *ambiguous* if some set of least weight contains $e$ and some set of least weight does not. If two different sets of least weight exist, some element is in one and not in the other, and it is ambiguous. So it is enough to show $\Pr[e \text{ is ambiguous}] \le 1/N$ for each $e$, and then take the union over the $m$ elements.

Fix $e$ and fix the weights of all other elements. Let $a$ be the least weight of a set of $\mathcal F$ that does not contain $e$ ($a = \infty$ if there is none), and let $b$ be the least value of $w(F) - w(e)$ over sets $F \in \mathcal F$ that contain $e$ ($b = \infty$ if there is none). Neither $a$ nor $b$ depends on $w(e)$. The least weight of a set containing $e$ is $b + w(e)$. If $b + w(e) < a$, every set of least weight contains $e$; if $b + w(e) > a$, none does. So $e$ is ambiguous only if $w(e) = a - b$, which has probability at most $1/N$ over the choice of $w(e)$. Averaging over the other weights gives the bound. $\square$

**Lemma 3 (Pfaffian).** For a skew-symmetric matrix $B$ of even order $n$, $\det B = \operatorname{Pf}(B)^2$, where
$$\operatorname{Pf}(B) = \sum_{M} \operatorname{sgn}(M) \prod_{\{i < j\} \in M} B_{ij},$$
the sum over all perfect matchings $M$ of the complete graph on $V$, with a sign $\operatorname{sgn}(M) \in \{\pm 1\}$ that depends only on $M$. For odd $n$, $\det B = 0$. Also, for $i \ne j$ the cofactor of $B$ at $(i, j)$ is $\pm \operatorname{Pf}(B) \cdot \operatorname{Pf}(B^{ij})$, where $B^{ij}$ is $B$ with rows and columns $i$ and $j$ removed. Finally, the expansion of the Pfaffian along row $i$ gives $\operatorname{Pf}(B) = \sum_{j \ne i} \pm B_{ij} \operatorname{Pf}(B^{ij})$.

These are standard facts about Pfaffians (see Lovász and Plummer, *Matching Theory*, Chapter 8, and Motwani and Raghavan, *Randomized Algorithms*, Chapter 12). For odd $n$, $\det B = \det B^{T} = \det(-B) = (-1)^n \det B = -\det B$. $\square$

In our $B$, a product $\prod B_{ij}$ is nonzero only when every pair of $M$ is an edge of $G$, so
$$\operatorname{Pf}(B) = \sum_{M \text{ perfect matching of } G} \pm 2^{w(M)}. \tag{1}$$
In the same way, $\operatorname{Pf}(B^{ij}) = \sum_{M'} \pm 2^{w(M')}$ over perfect matchings $M'$ of $G - i - j$. For an edge $ij$, the sets $M' \cup \{ij\}$ are exactly the perfect matchings of $G$ that contain $ij$, so
$$2^{w(ij)} \operatorname{Pf}(B^{ij}) = \sum_{M \ni ij} \pm 2^{w(M)}. \tag{2}$$

**Lemma 4 (one isolated matching is read correctly).** Suppose $G$ has a perfect matching and exactly one perfect matching $M_0$ has the least weight $W$. Then the trial does not stop at lines L4 and L5, $\nu_2(\det B) = 2W$, and line L7 computes $M = M_0$.

*Proof.* Every term of (1) other than the term of $M_0$ is $\pm 2^{w(M)}$ with $w(M) \ge W + 1$, so it is divisible by $2^{W+1}$. So $\operatorname{Pf}(B) = 2^W (\pm 1 + 2t)$ for an integer $t$, which is $2^W$ times an odd number and is not 0. By Lemma 3, $\det B = \operatorname{Pf}(B)^2 = 2^{2W} \cdot (\text{odd})$, so $\det B \ne 0$ and $\nu_2(\det B) = 2W$, which is even. Lines L4 and L5 pass, with $W_2 = 2W$.

The adjugate entry $A_{ji}$ is the cofactor of $B$ at $(i, j)$, so by Lemma 3 and (2),
$$|A_{ji}| \cdot 2^{w(ij)} = |\operatorname{Pf}(B)| \cdot \Bigl| \sum_{M \ni ij} \pm 2^{w(M)} \Bigr| = 2^W \cdot (\text{odd}) \cdot \Bigl| \sum_{M \ni ij} \pm 2^{w(M)} \Bigr|.$$
If $ij \in M_0$, the sum contains the term of $M_0$ and all other terms are divisible by $2^{W+1}$, so the sum is $2^W \cdot (\text{odd})$, and the whole product is $2^{2W} \cdot (\text{odd})$. Divided by $2^{W_2} = 2^{2W}$, it is an odd integer, and line L7 puts $ij$ in $M$. If $ij \notin M_0$, every perfect matching that contains $ij$ has weight at least $W + 1$, so the sum is divisible by $2^{W+1}$ (it may be 0). The product is divisible by $2^{2W+1}$, and divided by $2^{2W}$ it is an even integer, so line L7 does not put $ij$ in $M$. So $M = M_0$. $\square$

**Theorem.** A set returned by the algorithm is a perfect matching of $G$, and "none" is returned whenever $G$ has no perfect matching. If $G$ has a perfect matching, each trial returns one with probability at least $1/2$, so the algorithm returns "none" with probability at most $2^{-k}$.

*Proof.* The first two claims are Lemma 1. Suppose $G$ has a perfect matching, so $m \ge 1$ or $n = 0$. If $n = 0$, the empty matching passes line L8 in the first trial, as $\det$ of the empty matrix is 1 and $\nu_2(1) = 0$. Otherwise apply Lemma 2 to $S = E$, $\mathcal F$ the perfect matchings of $G$, and $N = 2m$: with probability at least $1 - m/(2m) = 1/2$ the least-weight perfect matching $M_0$ is unique. Then by Lemma 4 line L7 computes $M_0$, which passes line L8. The trials use independent weights, so all $k$ fail with probability at most $2^{-k}$. $\blacksquare$
