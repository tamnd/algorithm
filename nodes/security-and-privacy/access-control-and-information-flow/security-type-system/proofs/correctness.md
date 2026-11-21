---
title: The checker decides typability, and typable programs are termination-insensitive noninterferent
proves: [correctness]
status: full
---

We use the language, the rules and the pseudocode of the page. Levels are in a finite lattice $(\mathcal{L}, \le, \sqcup, \sqcap)$ with least element $\bot$. For an expression $e$, $\mathrm{label}(e)$ is the join of $\Gamma(y)$ over the variables $y$ of $e$, and $\bot$ if $e$ has no variable. The typing judgment $p \vdash c$ is defined by these rules, one for each form of $c$:

- $p \vdash \mathtt{skip}$.
- $p \vdash x := e$ if $\mathrm{label}(e) \sqcup p \le \Gamma(x)$.
- $p \vdash c_1; c_2$ if $p \vdash c_1$ and $p \vdash c_2$.
- $p \vdash \mathtt{if}\ e\ \mathtt{then}\ c_1\ \mathtt{else}\ c_2$ if $q \vdash c_1$ and $q \vdash c_2$, where $q = p \sqcup \mathrm{label}(e)$.
- $p \vdash \mathtt{while}\ e\ \mathtt{do}\ c_1$ if $p \sqcup \mathrm{label}(e) \vdash c_1$.

The rule for a variable in the original system allows any type above $\Gamma(y)$; the least one is $\mathrm{label}(e)$, and a larger type only makes the side conditions harder. So these rules accept the same programs as the rules with subsumption.

## Part 1. TYPECHECK$(c, \Gamma, pc)$ returns true if and only if $pc \vdash c$

**Invariant.** At the test of line L2, $pc \vdash c$ holds if and only if $p \vdash d$ holds for every pair $(d, p)$ on the stack $S$.

*Initialization.* Line L1 puts the single pair $(c, pc)$ on $S$, so the two sides are the same statement.

*Maintenance.* Let line L3 pop $(d, p)$. The rules are syntax directed: for each form of $d$ there is exactly one rule, and $p \vdash d$ holds if and only if the side condition of that rule holds and each premise holds.

- If $d$ is skip, $p \vdash d$ holds with no premise. Removing the pair keeps the invariant.
- If $d$ is $x := e$ and the side condition holds, $p \vdash d$ holds and the pair is removed. If the side condition fails, line L6 returns false. Then $p \vdash d$ is false, and by the invariant $pc \vdash c$ is false, so the answer is right.
- If $d$ is $d_1; d_2$, line L7 replaces the pair by $(d_1, p)$ and $(d_2, p)$, which are exactly the premises of the rule.
- If $d$ is an if statement, lines L8 and L9 replace the pair by $(d_1, q)$ and $(d_2, q)$ with $q = p \sqcup \mathrm{label}(e)$, the premises of the rule.
- If $d$ is a while loop, line L10 replaces the pair by $(d_1, p \sqcup \mathrm{label}(e))$, the premise of the rule.

In each case the conjunction over the stack changes from "$p \vdash d$ and the rest" to "the premises of $d$ and the rest", which is equivalent.

*Termination.* Each step removes one pair and adds pairs for proper subterms of its command only. So each node of the syntax tree of $c$ is popped at most once, and the loop stops after at most $n$ steps for a program of $n$ command nodes. When it stops without line L6, the stack is empty, the conjunction over it is true, and by the invariant $pc \vdash c$ holds. Line L11 returns true.

## Part 2. If $\bot \vdash c$, then $c$ is TINI for every observer level

**Semantics.** A store $s$ maps the variables to integers. We write $\langle c, s \rangle \Downarrow t$ when the run of $c$ from $s$ ends in the store $t$, with the usual big-step rules; a while loop with a true condition runs the body and then the loop again. For an observer level $\ell$, two stores are $\ell$-equivalent, $s_1 =_\ell s_2$, if $s_1(x) = s_2(x)$ for every $x$ with $\Gamma(x) \le \ell$. For the two-point lattice and $\ell = L$ this is $s_1 =_L s_2$.

**Claim.** If $\bot \vdash c$, $s_1 =_\ell s_2$, $\langle c, s_1 \rangle \Downarrow t_1$ and $\langle c, s_2 \rangle \Downarrow t_2$, then $t_1 =_\ell t_2$.

**Lemma 1 (simple security).** If $\mathrm{label}(e) \le \ell$ and $s_1 =_\ell s_2$, then $e$ has the same value in $s_1$ and in $s_2$.

*Proof.* Each variable $y$ of $e$ has $\Gamma(y) \le \mathrm{label}(e) \le \ell$, so $s_1(y) = s_2(y)$. The value of $e$ depends only on these values.

**Lemma 2 (weakening).** If $p \vdash c$ and $p' \le p$, then $p' \vdash c$.

*Proof.* By induction on $c$. Each side condition has the form $\mathrm{label}(e) \sqcup p \le \Gamma(x)$, and $\mathrm{label}(e) \sqcup p' \le \mathrm{label}(e) \sqcup p$. The premises use $p \sqcup \mathrm{label}(e)$, which also decreases when $p$ decreases.

**Lemma 3 (confinement).** If $p \vdash c$ and $\langle c, s \rangle \Downarrow t$, then $t(x) = s(x)$ for every $x$ with $p \not\le \Gamma(x)$.

*Proof.* By induction on the derivation of $\langle c, s \rangle \Downarrow t$. For skip, $t = s$. For $x := e$, the rule gives $p \le \mathrm{label}(e) \sqcup p \le \Gamma(x)$, so the only changed variable has $p \le \Gamma(x)$. For a sequence, both parts are typed at $p$, and the induction hypothesis applies to each part. For an if statement or a while loop, the parts run are typed at $q = p \sqcup \mathrm{label}(e) \ge p$; if $p \not\le \Gamma(x)$ then $q \not\le \Gamma(x)$, so the induction hypothesis for the body (at $q$) and for the next round of the loop (at $p$) leaves $x$ unchanged.

**Proof of the claim.** We prove the stronger statement for every $p$: if $p \vdash c$, $s_1 =_\ell s_2$, $\langle c, s_1 \rangle \Downarrow t_1$ and $\langle c, s_2 \rangle \Downarrow t_2$, then $t_1 =_\ell t_2$. The induction is on the sum of the sizes of the two derivations.

1. *skip.* $t_i = s_i$.
2. *$x := e$.* If $\Gamma(x) \le \ell$, then $\mathrm{label}(e) \le \Gamma(x) \le \ell$, and by Lemma 1 both runs store the same value in $x$. If $\Gamma(x) \not\le \ell$, the change of $x$ is not seen at $\ell$. The other variables do not change.
3. *$c_1; c_2$.* The runs pass through stores $u_1$ and $u_2$. By the hypothesis for $c_1$, $u_1 =_\ell u_2$, and then by the hypothesis for $c_2$, $t_1 =_\ell t_2$.
4. *if $e$ then $c_1$ else $c_2$, with $\mathrm{label}(e) \le \ell$.* By Lemma 1 both runs take the same branch, which is typed at $q$, and the hypothesis for that branch gives the result.
5. *while $e$ do $c_1$, with $\mathrm{label}(e) \le \ell$.* By Lemma 1 the condition has the same value in both runs. If it is false, $t_i = s_i$. If it is true, each run is the body from $s_i$ to $u_i$, then the loop from $u_i$ to $t_i$. The hypothesis for the body (typed at $p \sqcup \mathrm{label}(e)$) gives $u_1 =_\ell u_2$, and the hypothesis for the loop (a smaller derivation, typed at $p$) gives $t_1 =_\ell t_2$.
6. *An if statement or a while loop with $\mathrm{label}(e) \not\le \ell$.* Then $q = p \sqcup \mathrm{label}(e) \not\le \ell$. If the loop condition is false in run $i$, then $t_i = s_i$. In every other case the run of the statement from $s_i$ is a run of a command typed at $q$ (a branch, or the body followed by the loop, which is also typed at $q$ by Lemma 2 and the loop rule, since $q \sqcup \mathrm{label}(e) = q$). Take $x$ with $\Gamma(x) \le \ell$. Then $q \not\le \Gamma(x)$, since otherwise $q \le \Gamma(x) \le \ell$. By Lemma 3, $t_i(x) = s_i(x)$. So $t_1(x) = s_1(x) = s_2(x) = t_2(x)$.

The claim is the case $p = \bot$. The statement needs both runs to end: case 6 uses the final stores, and the type system allows a loop on a high condition, so a typable program can stop on some secrets and run forever on others. So the result is termination-insensitive noninterference, and it says nothing about time. $\blacksquare$
