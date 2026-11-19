---
title: Stochastic beam search returns an exact sample without replacement
proves: [correctness]
status: full
---

We use the notation of the page. Every output ends with "</s>" within $n$ tokens, so the tree of prefixes of positive probability is finite; its leaves are the outputs. For a node $y$, $\phi_y = \log p(y)$ is the log of the total probability of the outputs below it (for a prefix, the product of its token probabilities is the total probability of its completions, since the model ends within $n$ tokens). We work with exact real numbers and exact Gumbel draws. All logs are natural logs.

$\text{Gumbel}(\phi)$ has the distribution function $F_\phi(x) = \exp(-e^{\phi - x})$. The map $E = e^{-G}$ turns $G \sim \text{Gumbel}(\phi)$ into an exponential variable with rate $\lambda = e^{\phi}$, since $P(E > u) = P(G < -\log u) = e^{-\lambda u}$. It reverses the order: the largest $G$ is the smallest $E$.

**Lemma 1 (exponential races).** Let $E_1, \ldots, E_m$ be independent exponential variables with rates $\lambda_1, \ldots, \lambda_m$, and $\Lambda = \sum_i \lambda_i$. Then $M = \min_i E_i$ is exponential with rate $\Lambda$; the index $I$ of the minimum is $i$ with probability $\lambda_i / \Lambda$; $I$ and $M$ are independent; and given $I = i$ and $M$, the variables $E_j - M$ for $j \ne i$ are independent exponential with rates $\lambda_j$.

*Proof.* For $u \ge 0$ and $x_j \ge 0$, the joint density of $E_i = u$ with $E_j > u + x_j$ for all $j \ne i$ is $\lambda_i e^{-\lambda_i u} \prod_{j \ne i} e^{-\lambda_j (u + x_j)} = \frac{\lambda_i}{\Lambda} \cdot \Lambda e^{-\Lambda u} \cdot \prod_{j \ne i} e^{-\lambda_j x_j}$. The product form gives all four claims. $\square$

In Gumbel terms: $\max_i G_i \sim \text{Gumbel}(\log \sum_i e^{\phi_i})$, the argmax is $i$ with probability $p_i = e^{\phi_i} / \sum_j e^{\phi_j}$, and it is independent of the maximum.

**Theorem 2 (Gumbel-top-k).** Let $G_i \sim \text{Gumbel}(\phi_i)$ be independent for $i = 1, \ldots, m$. The indices $I_1, \ldots, I_k$ of the $k$ largest $G_i$, in decreasing order, have the law of a sample without replacement from $p$: $P(I_1 = i_1, \ldots, I_k = i_k) = \prod_{r=1}^{k} p_{i_r} / (1 - \sum_{s < r} p_{i_s})$.

*Proof.* Pass to $E_i = e^{-G_i}$. By Lemma 1, $I_1 = i_1$ with probability $p_{i_1}$, and given that and $M$, the others are $M$ plus independent exponentials with their own rates. The smallest of the others is therefore the first in a race among $\{E_j - M : j \ne i_1\}$, which by Lemma 1 again is $j$ with probability $\lambda_j / \sum_{l \ne i_1} \lambda_l = p_j / (1 - p_{i_1})$, and the remaining differences are again independent exponentials. Induction on $k$ gives the product. $\square$

**Lemma 3 (truncation).** Let $g_1, \ldots, g_m$ be independent with $g_i \sim \text{Gumbel}(\phi_i)$, and $Z = \max_i g_i$. For a fixed real $T$ let $\tilde g_i = -\log(e^{-T} - e^{-Z} + e^{-g_i})$. Then $(\tilde g_1, \ldots, \tilde g_m)$ has the law of $(g_1, \ldots, g_m)$ conditioned on $\max_i g_i = T$. Moreover $\max_i \tilde g_i = T$, attained at the same index as $Z$, and the map keeps the order of the $g_i$.

*Proof.* In the exponential form $E_i = e^{-g_i}$, $M = e^{-Z}$, $\tilde E_i = e^{-\tilde g_i} = e^{-T} + (E_i - M)$. The map adds the same constant to every $E_i$, so it keeps the order, and the argmin $I$ gets $\tilde E_I = e^{-T}$, that is $\tilde g_I = T$. By Lemma 1, $I$ has law $p$, and given $I$, the values $E_j - M$ are independent exponentials with rates $\lambda_j$, independent of $M$. So $(\tilde E_j)$ is: $\tilde E_I = e^{-T}$, and the others $e^{-T}$ plus independent exponentials. By Lemma 1 applied to the conditional law of $(E_j)$ given $M = e^{-T}$, this is exactly that conditional law. $\square$

The stable formula of the page is the same number: with $v = T - g + \log(1 - e^{g - Z})$, $e^{-T} - e^{-Z} + e^{-g} = e^{-T}(1 + e^{v})$, so $\tilde g = T - \log(1 + e^v)$, and $\log(1 + e^v) = \max(0, v) + \log(1 + e^{-|v|})$.

**Lemma 4 (top-down sampling).** Attach to every output $y$ an independent $G_y \sim \text{Gumbel}(\phi_y)$, and to every internal node $u$ the value $G_u = \max$ of $G_y$ over the outputs below $u$. Draw instead $\hat G_{\text{root}}$ from $\text{Gumbel}(\phi_{\text{root}}) = \text{Gumbel}(0)$, and for each node $u$, given $\hat G_u$, draw the values of its children by line L6 and line L7 with $T = \hat G_u$. Then the family $(\hat G_u)$ over all nodes has the same law as $(G_u)$.

*Proof.* The children of $u$ partition the outputs below $u$, so by Lemma 1, $G_{u w} \sim \text{Gumbel}(\phi_{uw})$ independently over the children, and $G_u = \max_w G_{uw}$. The subtrees are disjoint, so given the values of the children, the families below different children are independent, and the family below $uw$ depends on the rest only through $G_{uw}$. So the law of $(G_u)$ is fixed by the law of the root value, $\text{Gumbel}(\log \sum_y p(y)) = \text{Gumbel}(0)$, and the conditional law of the children values given the parent value, which is the law of independent $\text{Gumbel}(\phi_{uw})$ conditioned on their maximum. Lemma 3 says that line L7 draws exactly from that conditional law. Induction on the depth gives the claim. $\square$

The code sets the root value to 0 in place of a $\text{Gumbel}(0)$ draw. The proof of Lemma 4 then gives the law of $(G_u)$ conditioned on $G_{\text{root}} = 0$. The algorithm uses only the order of the values, and the order of the outputs' values is independent of their maximum: by Lemma 1 applied again and again, the first index, then the first of the remaining differences, and so on, are independent of $M$. So the conditioning does not change the law of the order, and the root value can be any constant.

**Lemma 5 (the beam keeps the top k).** In the algorithm, treat a finished node as its own only descendant at every later depth. Let $y_1, \ldots, y_k$ be the outputs with the $k$ largest values (all values are distinct with probability 1). Then after each step $t$, the beam holds, for each $y_r$, its ancestor at depth $t$ (or $y_r$ itself if it is shorter).

*Proof.* Suppose the ancestor $u$ of $y_r$ at depth $t$ is a candidate at step $t$ but is not kept. Then $k$ other candidates $v_1, \ldots, v_k$ have larger values. Each $v_s$ is the maximum over the outputs below it, so it has an output $x_s$ below it with value $\hat G_{v_s} > \hat G_u \ge \hat G_{y_r}$. The candidates at one depth have disjoint subtrees, so the $x_s$ are $k$ distinct outputs, none equal to $y_r$, with larger values than $y_r$. That contradicts that $y_r$ is among the $k$ largest. By induction on $t$, each kept ancestor produces the next ancestor as a candidate at step $t + 1$. $\square$

**Theorem 6 (correctness).** STOCHASTIC-BEAM-SEARCH returns the outputs with the $k$ largest perturbed values, in decreasing order, and these form an exact sample of $k$ outputs without replacement from the model (all outputs, in a random order, if there are fewer than $k$).

*Proof.* By Lemma 5, after the last step the beam holds $y_1, \ldots, y_k$, and since it holds at most $k$ nodes, it holds nothing else; line L10 returns them in the order of their values. By Lemma 4, the values have the law of independent $\text{Gumbel}(\log p(y))$ perturbations of the outputs, the setting of Theorem 2, with $p_y = p(y)$, since the outputs' probabilities sum to 1. $\square$
