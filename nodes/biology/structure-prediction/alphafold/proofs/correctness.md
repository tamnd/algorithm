---
title: Properties of lDDT and pLDDT as computed on the page
proves: [correctness]
status: full
---

We prove the properties of the main pseudocode, lines L1 to L9. The AlphaFold network itself has no correctness proof; its accuracy is an experimental result.

Let $x = (x_1, \ldots, x_n)$ be the model and $x^0$ the reference, points in $\mathbb{R}^3$, $R_0 > 0$, and $T$ a finite set of positive thresholds. Write $d_{ij} = \|x_i - x_j\|$, $d^0_{ij} = \|x^0_i - x^0_j\|$, $P_i = \{ j \ne i : d^0_{ij} < R_0 \}$, and let $k_i = \sum_{t \in T} |\{ j \in P_i : |d_{ij} - d^0_{ij}| < t \}|$ be the number of passed tests of residue $i$. Then $s_i = k_i / (|T| |P_i|)$ when $P_i \ne \emptyset$, and $S = \sum_i k_i / (|T| \sum_i |P_i|)$ when some $P_i \ne \emptyset$.

**Proposition 1 (range).** $0 \le s_i \le 1$ and $0 \le S \le 1$, and $S$ is the average of the $s_i$ weighted by $|P_i|$.

*Proof.* Each $j \in P_i$ passes at most $|T|$ tests, so $0 \le k_i \le |T| |P_i|$. Then $S = \sum_i |P_i| s_i / \sum_i |P_i|$, a weighted average of numbers in $[0, 1]$. $\square$

**Proposition 2 (rigid motions and mirror images).** Let $g$ be any isometry of $\mathbb{R}^3$, a rotation, a translation, a reflection or a composition of them. Then lDDT of $g(x)$ against $x^0$ equals lDDT of $x$ against $x^0$. In particular, if $x = g(x^0)$, every $s_i$ and $S$ equal 1.

*Proof.* An isometry keeps all distances, so $\|g(x_i) - g(x_j)\| = d_{ij}$. The sets $P_i$ depend only on $x^0$, and every test depends on $x$ only through the $d_{ij}$, so every $k_i$ is the same. If $x = g(x^0)$, then $d_{ij} = d^0_{ij}$, every deviation is $0 < t$ for all $t \in T$, so $k_i = |T| |P_i|$ and $s_i = 1$, and then $S = 1$ by Proposition 1. $\square$

The second statement includes reflections, so lDDT gives the full score to the mirror image of the reference. This is a limit of every score built from distances alone.

**Proposition 3 (the reference chooses the pairs).** lDDT is not symmetric in $x$ and $x^0$.

*Proof.* Take $n = 2$, $R_0 = 15$, $x^0_1 = x_1 = 0$, $x^0_2 = (14, 0, 0)$ and $x_2 = (20, 0, 0)$. Against $x^0$, the pair is scored and its deviation is 6, larger than every threshold in $T = \{0.5, 1, 2, 4\}$, so $S = 0$. With the roles exchanged, $d_{12} = 20 \ge R_0$ in the new reference, so no pair is scored and the score is not defined. $\square$

**Proposition 4 (pLDDT).** Let $z \in \mathbb{R}^b$ and $p = \mathrm{softmax}(z)$, so $p_k = e^{z_k} / \sum_l e^{z_l}$. Then $\mathrm{pLDDT} = 100 \sum_k p_k c_k$ with $c_k = (k + 1/2)/b$ is the expected value of $100 c_K$ for $K \sim p$. It lies in $[100 c_0, 100 c_{b-1}]$, which is $[1, 99]$ for $b = 50$. It does not change when the same constant is added to all $z_k$, and it is $50$ when all $z_k$ are equal.

*Proof.* The $p_k$ are positive and sum to 1, so $\sum_k p_k c_k$ is an expected value, and it lies between the least and the greatest $c_k$. Adding $a$ to every $z_k$ multiplies the numerator and the denominator of each $p_k$ by $e^a$. If all $z_k$ are equal, $p_k = 1/b$ and $\sum_k c_k / b = \frac{1}{b^2} \sum_{k=0}^{b-1} (k + 1/2) = \frac{1}{b^2} \cdot \frac{b^2}{2} = \frac{1}{2}$. $\square$

**Proposition 5 (the confidence loss).** For a true value $v \in [0, 1]$ with bin $\kappa = \min(b - 1, \lfloor b v \rfloor)$, the loss $-\log p_\kappa$ is positive for every finite $z$, and it tends to 0 along a sequence of logits if and only if $p_\kappa \to 1$.

*Proof.* Every $p_k$ is positive and the $b \ge 2$ probabilities sum to 1, so $0 < p_\kappa < 1$ and $-\log p_\kappa > 0$. The function $-\log$ is continuous and decreasing on $(0, 1]$ with value 0 only at 1. $\square$

The bin $\kappa$ contains $v$: for $v < 1$, $\kappa / b \le v < (\kappa + 1)/b$, and $v = 1$ falls in the last bin. So $|c_\kappa - v| \le 1/(2b)$, and $|c_k - v| \le 1 - 1/(2b)$ for every $k$. If the head puts mass $p_\kappa \ge 1 - \varepsilon$ on the true bin, then

$$|\mathrm{pLDDT} - 100 v| \le 100 \sum_k p_k |c_k - v| \le 100 \Big( \frac{1}{2b} + \varepsilon \Big(1 - \frac{1}{2b}\Big) \Big),$$

which for $b = 50$ is at most $1 + 99 \varepsilon$ points. A loss below $\varepsilon$ gives $p_\kappa > e^{-\varepsilon} \ge 1 - \varepsilon$, so a head with a low loss reports a pLDDT close to $100 v$. Whether the trained network reaches such a low loss on a new protein is an empirical question, which the AlphaFold paper answers by comparing pLDDT with the true lDDT on held-out structures.
