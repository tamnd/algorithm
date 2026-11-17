---
title: ARACNE computes its pruned network, and recovers a tree from exact values
proves: [correctness]
status: full
---

**Setup.** Let $I$ be a symmetric $m \times m$ matrix of non-negative numbers, $I_0 \ge 0$ and $\tau \in [0, 1)$. Let $E = \{\{i, j\} : I_{ij} > I_0\}$, the set of line L3. A *triangle* of $E$ is a set $\{i, j, k\}$ of three genes whose three pairs are all in $E$. Call an edge $e$ of a triangle *weak in it* when $I(e) < (1 - \tau) I(f)$ for both other edges $f$ of the triangle. Define

$$A = \{\, e \in E : e \text{ is weak in no triangle of } E \,\}.$$

**Lemma 1.** ARACNE returns $A$.

*Proof.* Line L4 starts with $D = \emptyset$. Lines L5 to L7 visit every triangle of $E$, and line L7 adds to $D$ exactly the edges that are weak in the visited triangle. The loop does not change $E$ or $I$, so the triangles and the test of line L7 are the same whatever the order of the visits. After the loop, $D$ is the set of edges of $E$ that are weak in at least one triangle of $E$, and line L8 returns $E \setminus D = A$. $\square$

**Lemma 2 (data processing inequality).** If the random variables $X$, $Y$ and $Z$ satisfy that $X$ and $Z$ are independent given $Y$, then $I(X; Z) \le \min(I(X; Y), I(Y; Z))$.

*Proof.* By the chain rule of mutual information, $I(X; Y, Z) = I(X; Z) + I(X; Y \mid Z) = I(X; Y) + I(X; Z \mid Y)$. The term $I(X; Z \mid Y)$ is zero by the conditional independence, and $I(X; Y \mid Z) \ge 0$. So $I(X; Z) \le I(X; Y)$. The hypothesis is symmetric in $X$ and $Z$, so the same argument with $X$ and $Z$ exchanged gives $I(X; Z) \le I(Z; Y)$. This is Theorem 2.8.1 of Cover and Thomas. $\square$

Now let $T$ be a tree on the genes. Say that the law of $(X_1, \ldots, X_m)$ is *Markov on $T$* if $X_i$ and $X_k$ are independent given $X_j$ whenever $j$ is an inner node of the path from $i$ to $k$ in $T$. By Lemma 2, exact values then satisfy $I_{ik} \le \min(I_{ij}, I_{jk})$ for each such triple. The theorem needs a strict form with the tolerance.

**Theorem.** Let $I_{ij} = I(X_i; X_j)$ be exact, and assume:

1. $I_{ij} > I_0$ for every edge $\{i, j\}$ of $T$;
2. for any three distinct genes $i$, $j$, $k$ with $j$ an inner node of the path from $i$ to $k$ in $T$, $I_{ik} < (1 - \tau) \min(I_{ij}, I_{jk})$.

Then ARACNE returns the edge set of $T$.

*Proof.* By Lemma 1 it is enough to show that $A$ is the edge set of $T$.

*Step 1: every edge of $T$ is in $A$.* Let $\{i, j\}$ be an edge of $T$. By assumption 1 it is in $E$. Suppose it were weak in a triangle $\{i, j, k\}$ of $E$. Deleting the edge $\{i, j\}$ from $T$ splits the tree into two parts, one with $i$ and one with $j$. By the symmetry of the claim we may assume that $k$ is in the part of $i$. Then the path from $k$ to $j$ in $T$ goes through $i$, and $i$ is an inner node of it. Assumption 2 for the triple $(k, i, j)$ gives $I_{kj} < (1 - \tau) I_{ij} \le I_{ij}$. Weakness of $\{i, j\}$ needs $I_{ij} < (1 - \tau) I_{kj} \le I_{kj}$, which contradicts $I_{kj} < I_{ij}$. So $\{i, j\}$ is weak in no triangle, and it is in $A$.

*Step 2: no other pair is in $A$.* Let $\{i, k\}$ be a pair that is not an edge of $T$. If $\{i, k\} \notin E$, it is not in $A$. Otherwise, the path from $i$ to $k$ in $T$ has at least two edges. Let $j$ be the node after $i$ on it, so $\{i, j\}$ is an edge of $T$ and $j$ is an inner node of the path. By assumption 1, $\{i, j\} \in E$. By assumption 2, $I_{ik} < (1 - \tau) I_{jk}$, so $I_{jk} > I_{ik} / (1 - \tau) \ge I_{ik} > I_0$, and $\{j, k\} \in E$. So $\{i, j, k\}$ is a triangle of $E$, and assumption 2 says that $I_{ik} < (1 - \tau) I_{ij}$ and $I_{ik} < (1 - \tau) I_{jk}$. So $\{i, k\}$ is weak in it, and it is not in $A$.

Steps 1 and 2 show that $A$ is the edge set of $T$. $\blacksquare$

**The normal case.** Let the genes be jointly normal and Markov on $T$, with correlation $r_e$ on each edge $e$ of $T$, $0 < |r_e| < 1$. Then the correlation of genes $i$ and $k$ is the product of $r_e$ over the path between them, so $|\rho_{ik}| = |\rho_{ij}| \, |\rho_{jk}| < \min(|\rho_{ij}|, |\rho_{jk}|)$ when $j$ is an inner node of the path. The map $\rho \mapsto -\tfrac12 \ln(1 - \rho^2)$ is strictly increasing in $|\rho|$, so assumption 2 holds with $\tau = 0$, and assumption 1 holds with $I_0 = 0$. This is the case that the test checks on random trees.
