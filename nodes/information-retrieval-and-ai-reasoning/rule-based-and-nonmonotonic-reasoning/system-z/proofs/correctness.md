---
title: System Z gives the least admissible ranking and decides rational closure
proves: [correctness]
status: full
---

Let $R$ be a finite set of conditionals $\alpha \to \beta$ over a finite set of atoms, where $\alpha$ and $\beta$ are propositional formulas. A *world* is a truth assignment to the atoms. A world *verifies* the rule $\alpha \to \beta$ if it satisfies $\alpha \wedge \beta$, and *falsifies* it if it satisfies $\alpha \wedge \neg\beta$. For a set $S$ of rules, $M(S)$ is the conjunction of the material implications $\alpha \supset \beta$ for the rules of $S$, so a world satisfies $M(S)$ exactly when it falsifies no rule of $S$. A rule $r$ is *tolerated* by $S$ if some world verifies $r$ and falsifies no rule of $S$, that is, if $\alpha_r \wedge \beta_r \wedge M(S)$ is satisfiable.

## The partition and the ranking

Lines L1 to L7 compute $R_{\ge 0} = R$ and, for $i = 0, 1, \ldots$, the layer $R_i$ of the rules of $R_{\ge i}$ that $R_{\ge i}$ tolerates, with $R_{\ge i+1} = R_{\ge i} \setminus R_i$. The loop stops at the first $k$ where $R_{\ge k}$ is empty or tolerates none of its rules. Write $R_\infty = R_{\ge k}$. Each round removes at least one rule, so $k \le |R|$. The *Z-rank* of a rule $r \in R_i$ is $Z(r) = i$. The set $R$ is *consistent* if $R_\infty = \emptyset$. Note that $R_{\ge i} = R_i \cup \cdots \cup R_{k-1} \cup R_\infty$ for $0 \le i \le k$.

The rank of a world $w$ is

$$\kappa(w) = \begin{cases} \infty & \text{if } w \text{ falsifies a rule of } R_\infty, \\ 0 & \text{if } w \text{ falsifies no rule}, \\ 1 + \max\{Z(r) : w \text{ falsifies } r\} & \text{otherwise}, \end{cases}$$

and the rank of a formula is $\kappa(\varphi) = \min\{\kappa(w) : w \models \varphi\}$, with $\min \emptyset = \infty$. System Z accepts $\alpha \mathrel{|\!\sim} \beta$ when $\kappa(\alpha \wedge \beta) < \kappa(\alpha \wedge \neg\beta)$ or $\kappa(\alpha \wedge \neg\beta) = \infty$ (line L16).

## The rank of a formula with a satisfiability oracle

**Lemma 1.** For $0 \le i \le k$ and every world $w$: $\kappa(w) \le i$ if and only if $w \models M(R_{\ge i})$. Also, $\kappa(w) < \infty$ if and only if $w \models M(R_{\ge k})$.

*Proof.* For $i = 0$: $\kappa(w) = 0$ exactly when $w$ falsifies no rule, that is, $w \models M(R)$. For $1 \le i \le k$: $\kappa(w) \le i$ exactly when $w$ falsifies no rule of $R_\infty$ and every rule that it falsifies has $Z(r) \le i - 1$. These are the conditions that $w$ falsifies no rule of $R_i, \ldots, R_{k-1}, R_\infty$, which is $w \models M(R_{\ge i})$. For the last claim, $\kappa(w) < \infty$ exactly when $w$ falsifies no rule of $R_\infty = R_{\ge k}$, and then $\kappa(w) \le k$ because every Z-rank is at most $k - 1$. $\square$

**Corollary 2.** $\kappa(\varphi) \le i$ if and only if $\varphi \wedge M(R_{\ge i})$ is satisfiable, for $0 \le i \le k$, and $\kappa(\varphi) = \infty$ if and only if $\varphi \wedge M(R_{\ge k})$ is unsatisfiable.

So the predicate "$\varphi \wedge M(R_{\ge i})$ is satisfiable" is false and then true as $i$ goes from $0$ to $k$. Line L8 handles the case $\kappa(\varphi) = \infty$, and lines L9 to L13 find the least $i$ for which the predicate is true by binary search. That value is $\kappa(\varphi)$.

## The ranking is admissible and least

A *ranking* is a function $\kappa'$ from worlds to $\{0, 1, 2, \ldots\} \cup \{\infty\}$, extended to formulas by the minimum as above. It *admits* the rule $\alpha \to \beta$ if $\kappa'(\alpha \wedge \beta) < \kappa'(\alpha \wedge \neg\beta)$. It is *admissible* for $R$ if it admits every rule of $R$ and gives some world rank $0$.

**Lemma 3.** $\kappa$ admits every rule that has a Z-rank. If $R$ is consistent, $\kappa$ is admissible for $R$.

*Proof.* Let $r \in R_i$. Since $R_{\ge i}$ tolerates $r$, some world $w$ verifies $r$ and falsifies no rule of $R_{\ge i}$. By Lemma 1, $\kappa(w) \le i$, so $\kappa(\alpha_r \wedge \beta_r) \le i$. Every world that falsifies $r$ has rank at least $1 + i$. So $\kappa(\alpha_r \wedge \beta_r) \le i < i + 1 \le \kappa(\alpha_r \wedge \neg\beta_r)$. If $R$ is consistent, every rule has a Z-rank. If $R$ is empty, every world has rank $0$. Otherwise $R_0$ is not empty, so some world verifies a rule of $R_0$ and falsifies no rule of $R$, and it has rank $0$. $\square$

**Lemma 4.** Let $\kappa'$ be a ranking that admits every rule of $R$. Then for each $i \le k$ and each rule $r \in R_{\ge i}$, $\kappa'(\alpha_r \wedge \beta_r) \ge i$.

*Proof.* By induction on $i$. The case $i = 0$ is clear. Assume the claim for $i < k$, and let $r \in R_{\ge i+1}$. Then $r \notin R_i$, so $R_{\ge i}$ does not tolerate $r$: every world $w$ that verifies $r$ falsifies some rule $s \in R_{\ge i}$. Then $\kappa'(w) \ge \kappa'(\alpha_s \wedge \neg\beta_s) > \kappa'(\alpha_s \wedge \beta_s) \ge i$, using that $\kappa'$ admits $s$ and the induction hypothesis. So $\kappa'(w) \ge i + 1$ for every such $w$, and $\kappa'(\alpha_r \wedge \beta_r) \ge i + 1$. $\square$

**Theorem 5 (least admissible ranking).** If $R$ is consistent and $\kappa'$ is admissible for $R$, then $\kappa(w) \le \kappa'(w)$ for every world $w$. If $R$ is not consistent, no ranking admits every rule of $R$.

*Proof.* Let $R$ be consistent. If $w$ falsifies no rule, $\kappa(w) = 0 \le \kappa'(w)$. Otherwise let $r$ be a rule that $w$ falsifies with the largest Z-rank $i$. By Lemma 4, $\kappa'(\alpha_r \wedge \beta_r) \ge i$. Since $\kappa'$ admits $r$, $\kappa'(w) \ge \kappa'(\alpha_r \wedge \neg\beta_r) \ge i + 1 = \kappa(w)$.

Now let $R_\infty \ne \emptyset$, and suppose that $\kappa'$ admits every rule. The set $R_\infty$ tolerates none of its rules. The argument of Lemma 4, applied inside $R_\infty$, shows by induction on $j$ that $\kappa'(\alpha_r \wedge \beta_r) \ge j$ for every $r \in R_\infty$ and every $j$: each world that verifies $r$ falsifies some $s \in R_\infty$ and so has rank above $\kappa'(\alpha_s \wedge \beta_s) \ge j$. So $\kappa'(\alpha_r \wedge \beta_r) = \infty$, and $\kappa'$ cannot admit $r$, because $\infty < \kappa'(\alpha_r \wedge \neg\beta_r)$ is false. $\square$

So, for a consistent set, $\kappa$ is the least admissible ranking, and the set has an admissible ranking exactly when it is consistent.

## System Z is rational closure

We use the decision procedure of Lehmann and Magidor (1992, Section 5.8). For a finite set $C$ of conditionals, a formula $\alpha$ is *exceptional* for $C$ if $C$ preferentially entails $\top \mathrel{|\!\sim} \neg\alpha$, and by their Lemma 33 and Corollary 6 this holds exactly when $M(C) \models \neg\alpha$. Let $E(C)$ be the set of the rules of $C$ whose antecedent is exceptional for $C$. Their procedure decides whether $\alpha \mathrel{|\!\sim} \beta$ is in the rational closure of $R$:

1. $C \leftarrow R$.
2. While $\alpha$ is exceptional for $C$ and $E(C) \ne C$, set $C \leftarrow E(C)$.
3. Answer yes if $\alpha \wedge \neg\beta$ is exceptional for $C$, and no otherwise.

**Lemma 6.** For every finite $C$, a rule $r \in C$ is tolerated by $C$ if and only if $\alpha_r$ is not exceptional for $C$. So $E(C)$ is the set of the rules of $C$ that $C$ does not tolerate, and the sequence $C_0 = R$, $C_{i+1} = E(C_i)$ is $C_i = R_{\ge i}$ for $i \le k$ and $C_i = R_\infty$ for $i \ge k$.

*Proof.* Since $r \in C$, $M(C)$ contains $\alpha_r \supset \beta_r$, so $\alpha_r \wedge M(C)$ is satisfiable exactly when $\alpha_r \wedge \beta_r \wedge M(C)$ is. The first is "not exceptional", the second is "tolerated". So $E(C_i) = C_i \setminus \{\text{tolerated rules}\}$. For $i < k$ this is $R_{\ge i} \setminus R_i = R_{\ge i+1}$. For $C = R_\infty$ no rule is tolerated, so $E(R_\infty) = R_\infty$. $\square$

**Theorem 7.** For all formulas $\alpha$ and $\beta$, System Z accepts $\alpha \mathrel{|\!\sim} \beta$ if and only if the procedure of Lehmann and Magidor answers yes, that is, if and only if $\alpha \mathrel{|\!\sim} \beta$ is in the rational closure of $R$.

*Proof.* By Lemma 6, the procedure walks through $R_{\ge 0}, R_{\ge 1}, \ldots$. It stops at the first $i \le k$ where $\alpha$ is not exceptional for $R_{\ge i}$, or at the fixed point $R_{\ge k}$.

Case $\kappa(\alpha) < \infty$. By Corollary 2, $\alpha$ is not exceptional for $R_{\ge i}$ exactly when $\kappa(\alpha) \le i$, so the procedure stops at $i = \kappa(\alpha)$. It answers yes exactly when $\alpha \wedge \neg\beta \wedge M(R_{\ge i})$ is unsatisfiable, which by Corollary 2 means $\kappa(\alpha \wedge \neg\beta) > i = \kappa(\alpha)$. Since $\kappa(\alpha) = \min(\kappa(\alpha \wedge \beta), \kappa(\alpha \wedge \neg\beta))$, this holds exactly when $\kappa(\alpha \wedge \beta) < \kappa(\alpha \wedge \neg\beta)$. That is the test at line L16.

Case $\kappa(\alpha) = \infty$. Then $\alpha$ is exceptional for every $R_{\ge i}$, and the procedure stops at the fixed point $C = R_{\ge k}$ with $M(C) \models \neg\alpha$. So $M(C) \models \neg(\alpha \wedge \neg\beta)$ and it answers yes. System Z also answers yes, because $\kappa(\alpha \wedge \neg\beta) \ge \kappa(\alpha) = \infty$. $\blacksquare$

Goldszmidt and Pearl (1990) proved that System Z and rational closure agree. The argument above reaches the same result through the decision procedure of Lehmann and Magidor, and it also covers sets that are not consistent: there, every formula whose rank is $\infty$ entails every formula, as in rational closure.

## Cost

The partition makes at most $|R|$ rounds, and round $i$ makes one satisfiability test for each rule of $R_{\ge i}$, so there are at most $|R|(|R| + 1)/2$ tests. Each rank $\kappa(\varphi)$ needs one test at line L8 and at most $\lceil \log_2(k + 1) \rceil$ tests in the binary search. One query $\alpha \mathrel{|\!\sim} \beta$ after the partition needs two ranks, so $O(\log |R|)$ tests, each on a formula of size $O(|R| \cdot \ell + |\alpha| + |\beta|)$, where $\ell$ is the largest size of a rule.
