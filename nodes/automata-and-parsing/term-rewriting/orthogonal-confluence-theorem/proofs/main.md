---
title: Proof that orthogonal systems are confluent, by multi-step reduction
proves: [statement]
status: full
---

Let $R$ be an orthogonal term rewriting system: every left side is linear and not a variable, and no two rules overlap. $R$ may be infinite, and it need not terminate. We use the notation of the term rewriting pages: terms $T(\Sigma, V)$, positions as sequences of positive integers, $t|_p$, substitutions $\sigma$ applied as $t\sigma$, rules $l \to r$ with $\mathrm{Var}(r) \subseteq \mathrm{Var}(l)$, and $\to^*$ for the reflexive transitive closure of $\to_R$. $\mathrm{Pos}_\Sigma(l)$ is the set of non-variable positions of $l$.

## Multi-step reduction

Define the relation $\Rightarrow$ on terms inductively by three rules.

- (V) $x \Rightarrow x$ for every variable $x$.
- (F) If $s_i \Rightarrow t_i$ for $i = 1, \ldots, n$, then $f(s_1, \ldots, s_n) \Rightarrow f(t_1, \ldots, t_n)$.
- (R) If $l \to r \in R$ and $x\sigma \Rightarrow x\tau$ for every $x \in \mathrm{Var}(l)$, then $l\sigma \Rightarrow r\tau$.

So $s \Rightarrow t$ contracts a set of redexes of $s$, possibly nested, from the inside out.

**Lemma 1 (reflexivity).** $u \Rightarrow u$ for every term $u$.

*Proof.* Induction on $u$, with (V) for variables and (F) otherwise. $\blacksquare$

**Lemma 2 (sandwich).** ${\to_R} \subseteq {\Rightarrow} \subseteq {\to^*}$.

*Proof.* Let $s \to_R t$ by the rule $l \to r$ at position $p$, so $s|_p = l\sigma$ and $t = s[r\sigma]_p$. Induction on $p$. If $p = \varepsilon$, then $l\sigma \Rightarrow r\sigma$ by (R), since $x\sigma \Rightarrow x\sigma$ by Lemma 1. If $p = i.q$, then $s = f(s_1, \ldots, s_n)$, $t$ differs from $s$ only in argument $i$, $s_i \Rightarrow t_i$ by induction, and (F) with Lemma 1 for the other arguments gives $s \Rightarrow t$.

For the second inclusion, use induction on the derivation of $s \Rightarrow t$. Case (V) is trivial. In case (F), rewrite the arguments one after the other. In case (R), rewrite each occurrence of each $x$ in $l\sigma$ from $x\sigma$ to $x\tau$, which gives $l\sigma \to^* l\tau$, and then $l\tau \to_R r\tau$. $\blacksquare$

**Lemma 3 (substitution).** If $x\tau \Rightarrow x\tau'$ for every $x \in \mathrm{Var}(r)$, then $r\tau \Rightarrow r\tau'$.

*Proof.* Induction on $r$. For a variable this is the hypothesis. For $r = f(r_1, \ldots, r_n)$ use the induction hypothesis on each $r_i$ and (F). $\blacksquare$

## The complete development

**Lemma 4 (at most one root redex).** If $s = l_1\sigma_1 = l_2\sigma_2$ for rules $l_1 \to r_1$ and $l_2 \to r_2$ of $R$, then the two rules are the same and $\sigma_1$, $\sigma_2$ agree on $\mathrm{Var}(l_1)$.

*Proof.* Rename the second rule apart from the first. The substitution that acts as $\sigma_1$ on the variables of $l_1$ and as $\sigma_2$ on those of $l_2$ unifies $l_1$ and $l_2$, an overlap at $\varepsilon$. Orthogonality only allows this when the two rules are the same. Then $l_1\sigma_1 = l_1\sigma_2$ forces $x\sigma_1 = x\sigma_2$ for every $x \in \mathrm{Var}(l_1)$. $\blacksquare$

Define the **complete development** $s^*$ by induction on $s$:

- $x^* = x$;
- if $s = l\sigma$ for a rule $l \to r$, then $s^* = r\sigma^*$, where $x\sigma^* = (x\sigma)^*$ for $x \in \mathrm{Var}(l)$;
- otherwise $f(s_1, \ldots, s_n)^* = f(s_1^*, \ldots, s_n^*)$.

By Lemma 4 the second clause does not depend on a choice. Each $x\sigma$ is a proper subterm of $s$, because $l$ is not a variable, so the definition is well-founded. $s^*$ contracts all redexes of $s$, from the inside out.

**Lemma 5 (redex survives).** Let $s = l\sigma$ for a rule $l \to r$, and let $s \Rightarrow t$ by a derivation whose last rule is (F). Then $t = l\tau$ for a substitution $\tau$ such that $x\sigma \Rightarrow x\tau$ by a sub-derivation, for every $x \in \mathrm{Var}(l)$.

*Proof.* We show by induction on the length of $q$: for every position $q$ of $l$, the derivation contains a sub-derivation of $(l|_q)\sigma \Rightarrow t|_q$, and if $q \in \mathrm{Pos}_\Sigma(l)$, the last rule of that sub-derivation is (F). For $q = \varepsilon$ this is the hypothesis. Let $q \in \mathrm{Pos}_\Sigma(l)$ with last rule (F); then $(l|_q)\sigma$ and $t|_q$ have the same root, and for each argument position $q.i$ of $l$ the derivation contains $(l|_{q.i})\sigma \Rightarrow t|_{q.i}$. If $q.i \in \mathrm{Pos}_\Sigma(l)$, the last rule of this sub-derivation is not (V), since $(l|_{q.i})\sigma$ is not a variable. It is not (R) either: otherwise $(l|_{q.i})\sigma = l'\rho$ for a rule $l' \to r'$, and $l|_{q.i}$, a non-variable subterm of $l$ at a position other than $\varepsilon$, unifies with a renamed copy of $l'$. That is an overlap, which orthogonality forbids, also when $l' \to r'$ is the rule $l \to r$ itself. So it is (F).

Hence $t$ agrees with $l$ at every position of $\mathrm{Pos}_\Sigma(l)$, and at the position $q_x$ of a variable $x$ of $l$ there is a sub-derivation $x\sigma \Rightarrow t|_{q_x}$. Since $l$ is linear, each variable $x$ has exactly one position $q_x$, so $x\tau = t|_{q_x}$ defines a substitution with $t = l\tau$. $\blacksquare$

Without linearity, two occurrences of $x$ could be rewritten to different terms and $\tau$ would not exist; without the overlap condition, a step inside the pattern of $l$ could destroy the redex. These are exactly the two hypotheses of the theorem.

**Lemma 6 (triangle).** If $s \Rightarrow t$, then $t \Rightarrow s^*$.

*Proof.* Induction on the size of $s$, with a case analysis on the last rule of the derivation of $s \Rightarrow t$.

- (V): $s = t = x$ and $s^* = x$, so $t \Rightarrow s^*$ by (V).
- (R): $s = l\sigma$, $t = r\tau$ and $x\sigma \Rightarrow x\tau$ for $x \in \mathrm{Var}(l)$. By Lemma 4, $s^* = r\sigma^*$ with this rule and this $\sigma$. Each $x\sigma$ is smaller than $s$, so by induction $x\tau \Rightarrow (x\sigma)^* = x\sigma^*$. By Lemma 3, since $\mathrm{Var}(r) \subseteq \mathrm{Var}(l)$, $t = r\tau \Rightarrow r\sigma^* = s^*$.
- (F), and $s$ is not of the form $l\sigma$: $s = f(s_1, \ldots, s_n)$, $t = f(t_1, \ldots, t_n)$ with $s_i \Rightarrow t_i$, and $s^* = f(s_1^*, \ldots, s_n^*)$. By induction $t_i \Rightarrow s_i^*$, and (F) gives $t \Rightarrow s^*$.
- (F), and $s = l\sigma$ for a rule $l \to r$: by Lemma 5, $t = l\tau$ with $x\sigma \Rightarrow x\tau$ for each $x \in \mathrm{Var}(l)$. By induction $x\tau \Rightarrow x\sigma^*$. Then (R) gives $t = l\tau \Rightarrow r\sigma^* = s^*$. $\blacksquare$

## Confluence

**Lemma 7 (diamond).** If $s \Rightarrow t_1$ and $s \Rightarrow t_2$, then $t_1 \Rightarrow s^*$ and $t_2 \Rightarrow s^*$. This is Lemma 6 applied twice. $\blacksquare$

**Lemma 8 (tiling).** If a relation $\Rightarrow$ has the diamond property, then so does $\Rightarrow^*$.

*Proof.* First, if $a \Rightarrow b$ and $a \Rightarrow^n c$, there is $d$ with $b \Rightarrow^n d$ and $c \Rightarrow d$. For $n = 0$ take $d = b$. For $a \Rightarrow c_1 \Rightarrow^{n-1} c$, the diamond gives $e$ with $b \Rightarrow e$ and $c_1 \Rightarrow e$, and induction applied to $c_1 \Rightarrow e$ and $c_1 \Rightarrow^{n-1} c$ gives $d$ with $e \Rightarrow^{n-1} d$ and $c \Rightarrow d$; then $b \Rightarrow^n d$. Second, if $a \Rightarrow^m b$ and $a \Rightarrow^n c$, use induction on $m$: for $a \Rightarrow b_1 \Rightarrow^{m-1} b$, the first part gives $e$ with $b_1 \Rightarrow^n e$ and $c \Rightarrow e$, and induction on $b_1$ gives $d$ with $b \Rightarrow^* d$ and $e \Rightarrow^* d$, so $c \Rightarrow^* d$. $\blacksquare$

**Theorem.** $\to_R$ is confluent.

*Proof.* By Lemma 2, $\to^* \subseteq \Rightarrow^* \subseteq (\to^*)^* = \to^*$, so $\Rightarrow^* = \to^*$. By Lemmas 7 and 8, $\Rightarrow^*$ has the diamond property, which for a reflexive transitive relation is confluence. So $\to^*$ has the diamond property, that is, $\to_R$ is confluent. $\blacksquare$

No step used termination or finiteness of $R$, and the proof gives more: from any term $s$, every multi-step reduct of $s$ reaches $s^*$ in one multi-step.
