---
title: With a beam that keeps every prefix, CTC prefix beam search returns the most probable labeling
proves: [correctness]
status: full
---

We use the notation of the page. The frames are $t = 1, \ldots, T$, the blank is $\varnothing$, and $y_t(k)$ is the output of frame $t$. The map $\mathcal{B}$ merges runs of equal symbols and then deletes blanks. The proofs work with probabilities; the code stores natural logs, and log_add in log space is $+$ on probabilities. For a prefix $\ell = \ell_1 \ldots \ell_n$ write $\ell_{\mathrm{end}} = \ell_n$, write $\ell^-$ for $\ell$ without its last label, and let

$$\Lambda(\ell) = \prod_{i=1}^{n} \lambda(\ell_1 \ldots \ell_{i-1}, \ell_i)$$

be the product of the language model weights $\lambda = e^{\mathrm{lm}}$ along $\ell$, with $\Lambda(\varepsilon) = 1$ for the empty prefix $\varepsilon$. Without a language model, $\lambda = 1$ and $\Lambda = 1$.

For $t \ge 1$, let $P_t(\ell)$ be the set of paths $\pi_1 \ldots \pi_t$ with $\mathcal{B}(\pi_1 \ldots \pi_t) = \ell$. Split it into $P^{b}_t(\ell)$, the paths with $\pi_t = \varnothing$, and $P^{nb}_t(\ell)$, the paths with $\pi_t \neq \varnothing$. A path in $P^{nb}_t(\ell)$ has $\ell \neq \varepsilon$ and $\pi_t = \ell_{\mathrm{end}}$, because the last symbol of a path that is not a blank is the last label of its collapse. Define

$$b_t^*(\ell) = \Lambda(\ell) \sum_{\pi \in P^b_t(\ell)} \prod_{\tau=1}^{t} y_\tau(\pi_\tau), \qquad nb_t^*(\ell) = \Lambda(\ell) \sum_{\pi \in P^{nb}_t(\ell)} \prod_{\tau=1}^{t} y_\tau(\pi_\tau).$$

At $t = T$, $b_T^*(\ell) + nb_T^*(\ell) = \Lambda(\ell)\, p(\ell \mid x)$.

**Lemma 1 (one frame).** For $t \ge 2$, every path in $P_t(\ell)$ is a path $\pi_1 \ldots \pi_{t-1}$ followed by one symbol, in exactly one of these four ways:

1. $\pi_t = \varnothing$ and $\pi_1 \ldots \pi_{t-1} \in P_{t-1}(\ell)$;
2. $\pi_t = \ell_{\mathrm{end}}$ and $\pi_1 \ldots \pi_{t-1} \in P^{nb}_{t-1}(\ell)$ (the run of the last label goes on);
3. $\pi_t = \ell_{\mathrm{end}}$ and $\pi_1 \ldots \pi_{t-1} \in P^{b}_{t-1}(\ell^-)$ (a new run after a blank);
4. $\pi_t = \ell_{\mathrm{end}}$, $\ell^- \neq \varepsilon$, $\ell_{\mathrm{end}} \neq \ell^-_{\mathrm{end}}$ and $\pi_1 \ldots \pi_{t-1} \in P^{nb}_{t-1}(\ell^-)$ (a new run right after a different label).

For $t = 1$ the same holds with $P_0(\varepsilon) = P_0^b(\varepsilon)$ holding only the empty path, and $P_0$ empty for every other prefix.

*Proof.* If $\pi_t = \varnothing$, deleting it does not change the collapse, which gives case 1. Otherwise $\pi_t = \ell_{\mathrm{end}}$. If $\pi_{t-1} = \pi_t$, the last symbol joins the run before it, so the shorter path also collapses to $\ell$ and ends in a label: case 2. If $\pi_{t-1} = \varnothing$, the last symbol starts a new run, and the shorter path collapses to $\ell^-$ and ends in a blank: case 3. If $\pi_{t-1}$ is a label different from $\pi_t$, the last symbol starts a new run after a label run, the shorter path collapses to $\ell^-$, ends in a label, and that label is $\ell^-_{\mathrm{end}} = \pi_{t-1} \neq \ell_{\mathrm{end}}$: case 4. The cases are disjoint because they differ in $\pi_t$ or in $\pi_{t-1}$. Conversely, each construction gives a path in $P_t(\ell)$, by the same reading of the runs. $\square$

**Theorem.** If the beam width $W$ is at least the number of prefixes scored at every frame (for example $W \ge \sum_{n=0}^{T} (K-1)^n$), then after frame $t$, for every prefix $\ell$ that has a path, the code holds $b(\ell) = b_t^*(\ell)$ and $nb(\ell) = nb_t^*(\ell)$. So line L11 returns a labeling $\ell$ that maximizes $\Lambda(\ell)\, p(\ell \mid x)$, and the returned score is its exact value.

*Proof.* By induction on $t$. Before the first frame, line L1 sets $b(\varepsilon) = 1$ and $nb(\varepsilon) = 0$, which matches $P_0$. Assume the claim after frame $t - 1$. No prefix is pruned, so the map $A$ holds every prefix that has a path of length $t-1$, and every other prefix has $b^* = nb^* = 0$ at $t - 1$. Lines L4 to L9 add, for every $\ell$ in $A$:

- to $b(\ell)$ the term $y_t(\varnothing)(b(\ell) + nb(\ell))$, which is case 1 (line L5);
- to $nb(\ell)$ the term $y_t(\ell_{\mathrm{end}})\, nb(\ell)$, which is case 2 (line L6);
- to $nb(\ell c)$ for every label $c$ the term $y_t(c)\, s\, \lambda(\ell, c)$, with $s = b(\ell)$ if $c = \ell_{\mathrm{end}}$ and $s = b(\ell) + nb(\ell)$ otherwise (lines L8 and L9). For the prefix $\ell c$, whose $\ell c^-$ is $\ell$, this is case 3 plus, when $c \neq \ell_{\mathrm{end}}$, case 4.

Each case of Lemma 1 for each prefix of frame $t$ is added exactly once, from the unique prefix it names. Cases 1 and 2 keep the prefix, so the factor $\Lambda(\ell)$ carries over. Cases 3 and 4 extend $\ell^-$ by $\ell_{\mathrm{end}}$ and multiply by $\lambda(\ell^-, \ell_{\mathrm{end}})$, and $\Lambda(\ell^-)\lambda(\ell^-, \ell_{\mathrm{end}}) = \Lambda(\ell)$. By Lemma 1 and the induction hypothesis the sums are $b_t^*(\ell)$ and $nb_t^*(\ell)$. The step of the option recover adds nothing here, because it acts only on prefixes that were pruned. At $t = T$, line L11 picks the largest $b + nb = \Lambda(\ell)\, p(\ell \mid x)$. $\square$

**Proposition (a narrow beam gives a lower bound).** For any beam width, every value $b(\ell)$ and $nb(\ell)$ that the code holds after frame $t$ is at most $b_t^*(\ell)$ and $nb_t^*(\ell)$. In particular, the returned score is at most $\Lambda(\ell)\, p(\ell \mid x)$ of the returned $\ell$, which is at most the optimum.

*Proof.* By induction on $t$, the stored values are sums over subsets of the four cases of Lemma 1: pruning removes whole prefixes from $A$, which removes the terms that come from them, and adds nothing. The recover step adds, for a pruned prefix $\ell^+$ that is made again from its parent, the terms of cases 1 and 2 of $\ell^+$ computed from its values at frame $t - 1$, which by induction are at most the true values. These cases are not added anywhere else in that frame, because $\ell^+$ is not in $A$. All terms are non-negative, so a subset gives a smaller or equal sum. $\square$

The proposition says nothing about which labeling a narrow beam returns, and no such guarantee holds: the page and the tests give an example where a beam of 3 returns the wrong labeling while beams of 2 and 4 return the right one.
