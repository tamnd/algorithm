---
title: The Friedman statistic, its exact conditional p-value, and why both are valid
proves: [correctness]
status: full
---

We use the pseudocode of the page: $b$ blocks, $k$ treatments, midranks $r_{ij}$ within block $i$ (line L1), rank sums $R_j$ (line L2), and $\bar r = (k+1)/2$.

**Claim 1 (fixed quantities).** Given the tie pattern of every block, $\sum_j R_j = bk(k+1)/2$ and $A = \sum_{i,j} r_{ij}^2$ do not depend on how each block's values are assigned to the treatments.

*Proof.* Midranks keep the sum of the ranks $1, \ldots, k$ in each block, so each block contributes $k(k+1)/2$ to $\sum_j R_j$. A permutation of a block permutes its multiset of midranks, which keeps the sum of their squares. $\square$

**Claim 2 (the two forms of $Q$).** Without ties, $Q = \frac{12}{bk(k+1)} \sum_j R_j^2 - 3b(k+1)$.

*Proof.* Without ties each block contributes $\sum_{l=1}^{k} l^2 = k(k+1)(2k+1)/6$ to $A$, so $D = A - bk(k+1)^2/4 = bk(k+1)(k-1)/12$. Also $\sum_j (R_j - b\bar r)^2 = \sum_j R_j^2 - k b^2 \bar r^2$ by Claim 1. Then $Q = \frac{12}{bk(k+1)} \left(\sum_j R_j^2 - \frac{b^2 k (k+1)^2}{4}\right)$, which is the stated form. $\square$

**Claim 3 (the null law).** Under $H_0$, given the multiset of values in each block, the assignment of each block's values to the treatments is uniform over the $k!$ permutations of its positions, independently across blocks.

*Proof.* Within block $i$ the vector $(X_{i1}, \ldots, X_{ik})$ is exchangeable, so given its multiset of values every arrangement of these values over the treatments has the same conditional probability. The blocks are independent, so these conditional laws are independent. The midranks of a block depend only on its multiset of values and the arrangement, so the rank vector of block $i$ is a uniform random permutation of a fixed multiset of midranks. $\square$

**Claim 4 (the dynamic program).** After line L6 has processed blocks $1, \ldots, i$, the count stored for a vector $s = (s_1, \ldots, s_k)$ is the number of the $(k!)^i$ choices of one permutation for each of these blocks whose doubled column rank sums equal $s$.

*Proof.* Induction on $i$. With no blocks there is one choice, with all sums 0. Every choice for blocks $1, \ldots, i + 1$ is a choice for blocks $1, \ldots, i$ followed by one of the $k!$ permutations of block $i + 1$, which adds the permuted doubled ranks to the sums; the code makes exactly these $k!$ moves from each state and adds the counts. Permutations of the positions are used even when a block has ties, so tied values give repeated vectors, each counted once per permutation, matching the uniform law of Claim 3. $\square$

**Claim 5 (the ordering and validity).** Given the tie patterns, $Q$ is a nondecreasing function of $\sum_j R_j^2$, so line L7 returns $P(Q \ge Q_{obs})$ under the law of Claim 3, and $P_{H_0}(p \le \alpha) \le \alpha$ for every $\alpha$.

*Proof.* By Claim 1, the denominator $D$ is a fixed number and $\sum_j (R_j - b \bar r)^2 = \sum_j R_j^2 - k b^2 \bar r^2$ with a fixed subtracted term. If $D = 0$, every block is a single tie, $Q = 0$ for every outcome, and $p = 1$. Otherwise $Q$ is a positive multiple of $\sum_j R_j^2$ minus a constant, and comparing doubled sums compares $4\sum_j R_j^2$, so the comparison is exact. Validity follows as for any upper tail of a discrete law: the rejection set is empty or $\{Q \ge q^*\}$ with $P(Q \ge q^*) \le \alpha$, given the values, and averaging keeps the bound. $\square$

**Claim 6 (two treatments).** For $k = 2$ without ties, $Q = (2S - b)^2 / b$, where $S$ is the number of blocks with $X_{i2} > X_{i1}$, and the exact Friedman p-value equals the two-sided sign-test p-value.

*Proof.* Each block gives ranks $(1, 2)$ or $(2, 1)$, so $R_2 = b + S$ and $R_2 - 3b/2 = S - b/2 = -(R_1 - 3b/2)$. Claim 2 with $k = 2$ gives $Q = \frac{12}{6b} \cdot 2 (S - b/2)^2 = (2S - b)^2/b$. Under the law of Claim 3, $S$ is Binomial$(b, 1/2)$, and $Q \ge Q_{obs}$ exactly when $\lvert S - b/2 \rvert \ge \lvert S_{obs} - b/2 \rvert$. The binomial law is symmetric, so this probability is $\min\{1, 2 \min(P(S \le S_{obs}), P(S \ge S_{obs}))\}$, the two-sided sign test. $\square$

**The chi-square limit.** Without ties, the rank vectors $\rho_i = (r_{i1}, \ldots, r_{ik})$ are independent and identically distributed under $H_0$, each a uniform permutation of $1, \ldots, k$, with mean $\bar r \mathbf{1}$ and covariance $\Sigma = \frac{k(k+1)}{12}(I - \frac{1}{k} \mathbf{1}\mathbf{1}^{\top})$; the off-diagonal value $-(k+1)/12$ follows because each rank vector has a fixed sum. By the multivariate central limit theorem, $Z = b^{-1/2} \sum_i (\rho_i - \bar r \mathbf{1})$ converges in law to $N(0, \Sigma)$. Since $I - \frac{1}{k}\mathbf{1}\mathbf{1}^{\top}$ is a projection of rank $k - 1$, $\frac{12}{k(k+1)} \lVert Z \rVert^2$ converges to $\chi^2_{k-1}$, and $\frac{12}{k(k+1)} \lVert Z \rVert^2 = \frac{12}{bk(k+1)} \sum_j (R_j - b\bar r)^2 = Q$. With ties, the denominator $D/(b(k-1))$ is the average within-block variance of the midranks times $k/(k-1)$, and the same argument applies with $\Sigma$ scaled accordingly. This gives an approximation, and the page reports how close it is for small $b$.

**Cost.** Line L1 sorts $b$ blocks of size $k$, lines L2 to L4 scan the table once. In the exact branch every column sum lies in $[b, bk]$ and the sums add up to $bk(k+1)/2$, so at most $(bk + 1)^{k-1}$ states exist, and each block moves each state in $k!$ ways. $\square$
