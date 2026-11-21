---
title: Secure multi-execution is termination-sensitive noninterferent and precise
proves: [correctness]
status: full
---

We use the language and the pseudocode of the page. Levels are in a finite lattice $(\mathcal{L}, \le, \sqcup, \sqcap)$, and $\Gamma(x)$ is the level of variable $x$. The plain semantics is deterministic: $[\![c]\!](s)$ is the final store of the run of $c$ from $s$, or $\bot$ if the run does not end. For a store $s$ and a level $k$, let $s_k$ be the store of line L3: $s_k(y) = s(y)$ if $\Gamma(y) \le k$, and $s_k(y) = d$ otherwise, with $d$ the fixed default value. Let $\mathrm{SME}(s)$ be the result of the page, with $\mathrm{SME}(s)(x) = \bot$ when the copy for $x$ does not end.

**What the observer sees.** An observer at level $\ell$ sees the output $\mathrm{SME}(s)(x)$ for each $x$ with $\Gamma(x) \le \ell$; the value $\bot$ is the observation "no output". Two stores are $\ell$-equivalent, $s =_\ell s'$, if they agree on each $y$ with $\Gamma(y) \le \ell$. For final results, $\bot =_\ell \bot$, and $\bot$ is not $\ell$-equivalent to a store.

**The code computes this result.** Line L1 lists each level that occurs as $\Gamma(x)$. The loop of lines L2 to L4 runs $c$ once from $s_k$ for each such level, and stores $t_k = [\![c]\!](s_k)$. The loop of lines L5 to L7 sets $\mathrm{out}(x)$ to $t_{\Gamma(x)}(x)$, or to $\bot$ when $t_{\Gamma(x)} = \bot$. The level $\Gamma(x)$ is in the list of line L1, so $t_{\Gamma(x)}$ is defined. So $\mathrm{SME}(s)(x) = [\![c]\!](s_{\Gamma(x)})(x)$, read as $\bot$ when the run does not end.

**Lemma 1.** If $k \le \ell$ and $s =_\ell s'$, then $s_k = s'_k$.

*Proof.* Take a variable $y$. If $\Gamma(y) \le k$, then $\Gamma(y) \le \ell$, so $s_k(y) = s(y) = s'(y) = s'_k(y)$. Otherwise both values are $d$.

**Theorem 1 (soundness).** For every program $c$, every level $\ell$ and every two stores $s =_\ell s'$: for each $x$ with $\Gamma(x) \le \ell$, $\mathrm{SME}(s)(x) = \mathrm{SME}(s')(x)$. So the observer at $\ell$ sees the same outputs, and in particular sees "no output" in one run exactly when it does in the other. SME is termination-sensitive noninterferent.

*Proof.* Let $k = \Gamma(x) \le \ell$. By Lemma 1, $s_k = s'_k$. The plain semantics is deterministic, so $[\![c]\!](s_k) = [\![c]\!](s'_k)$: both are $\bot$, or both are the same store. In both cases $\mathrm{SME}(s)(x) = \mathrm{SME}(s')(x)$.

**Theorem 2 (precision).** Let $c$ be termination-sensitive noninterferent for each level: for each $k$ and each two stores $s =_k s'$, $[\![c]\!](s) =_k [\![c]\!](s')$. Then for every store $s$ with $[\![c]\!](s) = t \ne \bot$, $\mathrm{SME}(s) = t$.

*Proof.* Take a variable $x$ and let $k = \Gamma(x)$. The stores $s$ and $s_k$ agree on each $y$ with $\Gamma(y) \le k$, so $s =_k s_k$. By the hypothesis, $[\![c]\!](s_k) =_k t$. Since $t \ne \bot$, also $[\![c]\!](s_k) \ne \bot$, and the two final stores agree on $x$, because $\Gamma(x) = k \le k$. So $\mathrm{SME}(s)(x) = [\![c]\!](s_k)(x) = t(x)$.

If $[\![c]\!](s) = \bot$ and $c$ is as in Theorem 2, the same argument shows that each copy does not end, so $\mathrm{SME}(s)(x) = \bot$ for every $x$, as for the plain run.

**The bound on steps.** The code replaces "does not end" by "does not end within the fuel bound". Theorem 1 holds for this semantics with the same proof, because a run with a step bound is still deterministic. Theorem 2 holds for it when $c$ is termination-sensitive noninterferent for the semantics with the step bound.

**The hypothesis of Theorem 2 is needed.** The program "while $h = 0$ do skip; $l := 1$" is termination-insensitive noninterferent but not termination-sensitive. From $h = 1$ the plain run ends with $l = 1$, but the public copy sees $h = d = 0$ and does not end, so $\mathrm{SME}(s)(l) = \bot$. $\blacksquare$
