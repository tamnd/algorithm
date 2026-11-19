---
title: Without pruning, multi-stack decoding with recombination returns a best derivation
proves: [correctness]
status: full
---

The source is $f = f_1 \ldots f_m$, and the decoder translates it into a target sentence $e$. Spans are fencepost: $(s, t)$ covers $f_{s+1} \ldots f_t$. A *derivation* is a sequence of phrase translations $(s_1, t_1, \bar e_1), \ldots, (s_n, t_n, \bar e_n)$ whose source spans are disjoint and cover $1, \ldots, m$, where each $\bar e_k$ is a translation of $f_{s_k + 1} \ldots f_{t_k}$ in the phrase table and every jump $|s_k - t_{k-1}|$ (with $t_0 = 0$) is within the distortion limit, if there is one. Its score is

$$\sum_k \Bigl(\mathrm{tm}_k - \delta \, |s_k - t_{k-1}| + \omega \, |\bar e_k|\Bigr) + \mu \sum_{x=1}^{|e|+1} \ln p(e_x \mid e_{x-1}),$$

where $e = \bar e_1 \cdots \bar e_n$, $e_0 = $ `<s>`, $e_{|e|+1} = $ `</s>`, and $\delta, \omega, \mu$ are the weights. Logs are natural. The claim is about DECODE with no histogram limit and no threshold, so line L4 keeps every hypothesis.

A *partial derivation* is a prefix $(s_1, t_1, \bar e_1), \ldots, (s_r, t_r, \bar e_r)$ of a sequence with disjoint spans and allowed jumps. Its *state* is the triple (coverage $C$, last target word $w$, end $t_r$), with $w = $ `<s>` and end $0$ for the empty prefix, and its *partial score* is the score above with the sums cut after step $r$ and without the final `</s>` term.

**Lemma 1 (the rest of the score depends only on the state).** Let $d$ be a partial derivation with state $\sigma$ and let $x$ be a sequence of steps such that $d x$ is a derivation. Then the score of $d x$ is the partial score of $d$ plus a quantity $g(\sigma, x)$ that depends only on $\sigma$ and $x$. Whether $d x$ is a derivation also depends only on $\sigma$ and $x$.

*Proof.* The terms of the steps of $x$ are $\mathrm{tm}$, $\omega |\bar e|$, the jump $|s - t_{\mathrm{prev}}|$, and the bigrams inside $\bar e$ and between the last word before it and its first word. For the first step of $x$, the previous end and the previous word are the end and the word of $\sigma$. For later steps they are inside $x$. The final term $\ln p(\texttt{</s>} \mid \cdot)$ uses the last word of $d x$, which is the last word of $x$, or the word of $\sigma$ if $x$ is empty. Disjointness of $x$ from $d$ depends only on the coverage $C$, and the distortion test of the first step only on the end. $\square$

**Lemma 2 (invariant).** For each $c = 0, \ldots, m$, when the loop of line L3 reaches stack $c$ (and, for $c = m$, at line L11), stack $c$ holds, for every state $\sigma$ with $|C| = c$ that some partial derivation reaches, one hypothesis with state $\sigma$ whose score is the largest partial score over all partial derivations that reach $\sigma$. It holds nothing else.

*Proof.* By induction on $c$. Stack 0 holds the start hypothesis, the only state with $|C| = 0$, with score 0.

Let $c \ge 1$ and let $\sigma$ be a reachable state with $|C| = c$. Take a partial derivation $d$ with the best partial score $S^*$ for $\sigma$, and let its last step be $(s, t, \bar e)$ with $t - s = q$. Its prefix $d'$ has a state $\sigma'$ with $|C'| = c - q < c$. By Lemma 1 applied to partial scores (the same argument without the `</s>` term), the partial score of $d$ is the partial score of $d'$ plus a term that depends only on $\sigma'$ and the last step. By induction, stack $c - q$ holds a hypothesis $h'$ with state $\sigma'$ and score at least that of $d'$. When line L5 processes $h'$, line L6 tries the step $(s, t, \bar e)$. Line L7 accepts it, because it was allowed after $d'$ and the test depends only on $\sigma'$. Line L8 computes a score at least $S^*$ for a hypothesis with state $\sigma$, and puts it into stack $c$ under the key $\sigma$ (line L9). Line L10 keeps the higher score for each key, so the hypothesis kept for $\sigma$ has a score at least $S^*$. Every hypothesis in the stack is built from a hypothesis that corresponds to a partial derivation, by one allowed step, so its score is the partial score of a real partial derivation reaching $\sigma$, hence at most $S^*$. So it is exactly $S^*$.

All the steps into stack $c$ come from stacks $c' < c$, and the loop of line L3 handles the stacks in increasing order. So all of them are done before stack $c$ is read. $\square$

**Theorem.** If some derivation exists, DECODE with no pruning returns the largest derivation score, and the derivation it traces back at line L13 has this score. If none exists, it returns $-\infty$.

*Proof.* A complete derivation is a partial derivation with $|C| = m$ plus the `</s>` term, which depends only on the last word (Lemma 1). Line L12 adds this term to each hypothesis of stack $m$ and line L11 keeps the best. By Lemma 2, stack $m$ holds the best partial score of every reachable full state, so the maximum over it is the maximum over all derivations. The back pointers of a hypothesis lead through the hypotheses it was built from, so the traced steps form a derivation whose score is the stored score. If no derivation exists, stack $m$ is empty and line L11 finds nothing. $\square$

**With pruning.** Line L4 may drop the hypothesis that the best derivation passes through, because it ranks by score plus a future cost estimate that leaves out distortion and the language model context. Then the theorem fails. The test file has a two-word case in which a stack size of 1 returns a derivation with score $-6.1$ while the best has $-2.1$. Recombination alone never loses the best derivation, by Lemma 1.

**Cost.** Without a distortion limit there are up to $2^m$ coverage sets, so the number of states, and the time, can be exponential in $m$. With a stack size $k$, each of the $m$ stacks expands at most $k$ hypotheses, each with at most $|O|$ translation options, so the time is $O(m k |O|)$ for the expansions, plus the cost of ranking each stack.
