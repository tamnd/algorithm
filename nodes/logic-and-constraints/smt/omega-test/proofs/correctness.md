---
title: The omega test decides integer feasibility of linear constraints and always stops
proves: [correctness, termination]
status: full
---

**Setting.** A constraint is $\sum_i a_i x_i + c \ge 0$ (an inequality) or $\sum_i a_i x_i + c = 0$ (an equality), with integer $a_i$ and $c$ and integer variables. For a system $S$ over variables $V$, write $\mathrm{Sol}(S) \subseteq \mathbb{Z}^V$ for its integer solutions. For a variable $z$, the *integer projection* is $\pi_z(S) = \{ y : (y, z) \in \mathrm{Sol}(S) \text{ for some } z \in \mathbb{Z} \}$. The symmetric residue is $a \operatorname{\widehat{mod}} m = a - m \lfloor a/m + 1/2 \rfloor$, for $m \ge 2$. It satisfies $a \equiv a \operatorname{\widehat{mod}} m \pmod m$ and $-m/2 \le a \operatorname{\widehat{mod}} m < m/2$.

Fix $z$. Write each inequality that contains $z$ as a lower bound $b z \ge \beta$ with $b > 0$, or an upper bound $a z \le \alpha$ with $a > 0$, where $\beta$ and $\alpha$ are linear expressions in the other variables. For a point $y$ of the other variables, $\beta(y)$ and $\alpha(y)$ are integers. Let $a_{\max}$ be the largest coefficient $a$ of an upper bound. The *real shadow* $R_z(S)$ is the set of constraints without $z$ plus $b\alpha - a\beta \ge 0$ for each pair of a lower and an upper bound. The *dark shadow* $D_z(S)$ is the same with $b\alpha - a\beta \ge (a - 1)(b - 1)$. The *splinters* of $S$ are the systems $S \cup \{b z = \beta + i\}$ for each lower bound and each $0 \le i \le \lfloor (a_{\max} b - a_{\max} - b)/a_{\max} \rfloor$.

**Lemma 1 (normalization).** Let $g \ge 1$ be the gcd of the coefficients of a constraint. An equality $\sum a_i x_i + c = 0$ has no integer solution if $g \nmid c$, and otherwise it has the same integer solutions as $\sum (a_i/g) x_i + c/g = 0$. An inequality $\sum a_i x_i + c \ge 0$ has the same integer solutions as $\sum (a_i/g) x_i + \lfloor c/g \rfloor \ge 0$.

*Proof.* For integer $x$, $\sum a_i x_i$ is a multiple of $g$. If $g \nmid c$ the sum cannot equal $-c$. For the inequality, $t = \sum (a_i/g) x_i$ is an integer, and $t \ge -c/g$ holds if and only if $t \ge \lceil -c/g \rceil = -\lfloor c/g \rfloor$. $\square$

**Lemma 2 (one equality step).** Let $e$ be the equality $\sum_i a_i x_i + c = 0$ after normalization, and let $k$ be a variable whose coefficient has the least absolute value.

(a) If $|a_k| = 1$, then $x_k = -a_k(\sum_{i \ne k} a_i x_i + c)$ on $\mathrm{Sol}(e)$, and substituting this value in the rest of the system gives a system whose integer solutions, extended by this value of $x_k$, are exactly the integer solutions of the old system.

(b) If $|a_k| \ge 2$, let $s = \operatorname{sign}(a_k)$, $m = |a_k| + 1$, $\sigma$ a new variable, and
$$x_k = -s m \sigma + s \sum_{i \ne k} (a_i \operatorname{\widehat{mod}} m) x_i + s (c \operatorname{\widehat{mod}} m). \tag{1}$$
The integer solutions of $S$ are exactly the restrictions to $V$ of the integer solutions of $S[x_k := (1)]$, extended by (1). After the substitution and normalization, $e$ has the coefficient $-|a_k|$ on $\sigma$, and each other coefficient $a_i'$ has $|a_i'| < |a_i|$.

*Proof.* (a) is solving a linear equation with a unit coefficient: the value is an integer for each integer point.

(b) First, $a_k \operatorname{\widehat{mod}} m = -s$. Indeed, for $a_k > 0$, $a_k/m + 1/2 \in [1, 3/2)$, so the floor is 1 and the residue is $a_k - m = -1$; the case $a_k < 0$ is the mirror image. Take an integer solution $x$ of $S$. Then $T = \sum_i (a_i \operatorname{\widehat{mod}} m) x_i + (c \operatorname{\widehat{mod}} m) \equiv \sum_i a_i x_i + c = 0 \pmod m$, so $\sigma = T/m$ is an integer. The term of $x_k$ in $T$ is $-s x_k$, so $m\sigma = -s x_k + \sum_{i \ne k} (a_i \operatorname{\widehat{mod}} m) x_i + (c \operatorname{\widehat{mod}} m)$, and multiplying by $-s$ gives (1). So $x$ with this $\sigma$ solves $S[x_k := (1)]$. Conversely, for each integer solution of $S[x_k := (1)]$, the value (1) is an integer, and the constraints of $S$ hold for it because they hold after the substitution.

Now the coefficients. Write $a_i = m q_i + r_i$ with $q_i = \lfloor a_i/m + 1/2 \rfloor$ and $r_i = a_i \operatorname{\widehat{mod}} m$. After the substitution, $e$ has coefficient $a_k \cdot (-s m) = -|a_k| m$ on $\sigma$ and $a_i + |a_k| r_i = m q_i + r_i + (m - 1) r_i = m(q_i + r_i)$ on $x_i$, and the constant is a multiple of $m$ in the same way. Dividing by $m$ (normalization divides by a multiple of $m$) gives $-|a_k|$ on $\sigma$ and $a_i' = q_i + r_i = a_i - (m - 1) q_i$, possibly divided further. For $i \ne k$, $|a_i| \ge |a_k| = m - 1 \ge 2$ by the choice of $k$. If $a_i > 0$ then $a_i/m + 1/2 \ge (m-1)/m + 1/2 \ge 1$, so $q_i \ge 1$, and $q_i \le a_i/m + 1/2$ gives $(m - 1) q_i \le a_i (m-1)/m + (m-1)/2 < a_i + a_i/2$. So $0 < (m - 1) q_i < 2 a_i$, and $|a_i - (m-1) q_i| < a_i$. The case $a_i < 0$ is the mirror image. $\square$

**Lemma 3 (the shadows).** For each system $S$ and variable $z$:
$$\mathrm{Sol}(D_z(S)) \subseteq \pi_z(S) \subseteq \mathrm{Sol}(R_z(S)).$$
If every lower bound has $b = 1$, or every upper bound has $a = 1$, then $\pi_z(S) = \mathrm{Sol}(R_z(S))$. If $z$ has no lower bound or no upper bound, then $\pi_z(S)$ is the solution set of the constraints without $z$.

*Proof.* Fix $y$, and write $\beta, \alpha$ for the integer values $\beta(y), \alpha(y)$. An integer $z$ fits all bounds if and only if $L = \max \lceil \beta/b \rceil \le U = \min \lfloor \alpha/a \rfloor$, and this holds if and only if $\lceil \beta/b \rceil \le \lfloor \alpha/a \rfloor$ for each pair. If $z$ has no lower or no upper bound, one side is missing and a $z$ always exists.

Right inclusion: if $\beta \le b z$ and $a z \le \alpha$ then $a \beta \le a b z \le b \alpha$.

Exact case, with all $a = 1$: from $b \alpha - \beta \ge 0$ we get $\alpha \ge \beta/b$, and $\alpha$ is an integer, so $\alpha \ge \lceil \beta/b \rceil$. The case with all $b = 1$ is the mirror image.

Left inclusion: suppose a pair has $\lfloor \alpha/a \rfloor < \lceil \beta/b \rceil = t$. Then $\beta > b(t-1)$, so $\beta \ge b(t - 1) + 1$, and $\alpha < a t$, so $\alpha \le a t - 1$. Hence $b\alpha - a\beta \le b(at - 1) - a(bt - b + 1) = ab - a - b = (a-1)(b-1) - 1$, and $y$ is not in the dark shadow. $\square$

**Lemma 4 (the splinters).** Each integer solution $(y, z)$ of $S$ with $y \notin \mathrm{Sol}(D_z(S))$ is a solution of some splinter of $S$.

*Proof.* Write $X_b = (a_{\max} b - a_{\max} - b)/a_{\max}$. Suppose that for each lower bound, $b z - \beta > \lfloor X_b \rfloor$. Both sides are integers, so $b z - \beta \ge \lfloor X_b \rfloor + 1 > X_b$. Take any pair. Then $\alpha - a z \ge 0$ and $a \le a_{\max}$, so
$$b\alpha - a\beta = b(\alpha - a z) + a(b z - \beta) > a X_b = ab - a - \frac{ab}{a_{\max}} \ge ab - a - b = (a-1)(b-1) - 1.$$
The left side is an integer, so it is at least $(a-1)(b-1)$, for each pair: $y$ is in the dark shadow, a contradiction. So some lower bound has $0 \le b z - \beta \le \lfloor X_b \rfloor$, and $(y, z)$ solves the splinter with $i = b z - \beta$. $\square$

**Lemma 5 (termination).** Each call of OMEGA stops.

*Proof.* *The equality phase stops.* Let $E$ be the number of equalities and $W$ the sum of the absolute values of the coefficients of the equality in work. A step of Lemma 2(a), or a step that finds $g \nmid c$, removes one equality. A step of Lemma 2(b) keeps $E$ and decreases $W$ by at least 1, since the coefficient of $\sigma$ is $|a_k|$ again and each other coefficient shrinks; there is another coefficient because a normalized equality with one variable has coefficient $\pm 1$. So the pair $(E, W)$ decreases in the lexicographic order. Step (b) also keeps the number of variables in the system, since $\sigma$ replaces $x_k$, and step (a) decreases it by at least one.

*The whole procedure stops.* Let $N$ be the number of variables in the system when the equality phase ends. We show by induction on $N$ that the call stops. If no constraint has a variable, the call stops at line L6 or L7. Otherwise each recursive call is one of these. (i) A call on the constraints without $z$, on a real shadow or on a dark shadow: it has no equality and at most $N - 1$ variables. (ii) A call on a splinter: it has one equality, which contains $z$, over at most $N$ variables. Its equality phase stops by the first part. Each step (b) keeps the number of variables and the final step (a) removes one, so this call has at most $N - 1$ variables when its equality phase ends. There are finitely many splinters. By the induction hypothesis, each recursive call stops. $\square$

**Theorem.** For each finite system $S$ of linear equalities and inequalities with integer coefficients, OMEGA$(S)$ stops. It returns SAT if and only if $S$ has an integer solution, and the model that the implementation builds is an integer solution.

*Proof.* Termination is Lemma 5. Correctness by induction along the calls, which is well founded by Lemma 5. The equality phase keeps the set of integer solutions, up to the new variables $\sigma$ and the solved variables (Lemmas 1 and 2). Line L6 keeps it too (Lemma 1), and it returns UNSAT only for a constant constraint $c \ge 0$ with $c < 0$, which has no solution. Line L7: a system with no variables and no false constant constraint is true. Line L9 and line L10 return the answer for $\pi_z(S)$ by Lemma 3, and $\pi_z(S) \neq \emptyset$ if and only if $\mathrm{Sol}(S) \neq \emptyset$. Line L11: if the dark shadow has an integer solution, then by Lemma 3 so does $S$. Lines L12 and L13: each splinter adds a constraint, so a solution of a splinter solves $S$. Line L14: if the dark shadow and all splinters have no solution, then $S$ has none, because by Lemma 4 each solution of $S$ lies in the dark shadow or in a splinter.

The model: after a recursive call returns a solution $y$ of the shadow, the implementation sets $z = L = \max \lceil \beta(y)/b \rceil$ (or $U$, or 0 if $z$ has no bounds), and $L \le U$ by the first paragraph of the proof of Lemma 3 and the inclusions there. After an equality step, it computes $x_k$ from (a) or (1), which is an integer. Variables that occur in no constraint get the value 0, the same value in each place where they are read. $\blacksquare$
