---
title: The general simplex returns a model or a Farkas certificate, and CHECK terminates with Bland's rule
proves: [correctness, termination]
status: full
---

**Setting.** The original variables are $x_1, \ldots, x_n$. Each linear form $a_k \cdot x$ of an atom with two or more variables gets a slack variable $x_{n+k}$, $k = 1, \ldots, m$, with the definition $x_{n+k} = a_k \cdot x$. Write $N = n + m$ and $K$ for the set of vectors $v$ that satisfy all $m$ definitions. Values live in $\mathbb{Q}_\delta$, the pairs $(c, k)$ read as $c + k\delta$, ordered lexicographically, added componentwise and multiplied by rationals componentwise. $\mathbb{Q}_\delta$ is an ordered vector space over $\mathbb{Q}$: $u \le v$ implies $u + w \le v + w$, and $q u \le q v$ for each rational $q > 0$. A bound is $l_i \le x_i$ or $x_i \le u_i$ with $l_i, u_i \in \mathbb{Q}_\delta$; a missing bound is $-\infty$ or $+\infty$. A strict atom $x_i < c$ is the bound $u_i = (c, -1)$, and $x_i > c$ is $l_i = (c, 1)$.

At each moment the solver has a basis $B$ of $m$ variables, a tableau with one row $x_i = \sum_{j \notin B} a_{ij} x_j$ for each $i \in B$, and an assignment $\beta \in \mathbb{Q}_\delta^N$.

**Invariants.**

- **(T)** A vector satisfies the tableau rows if and only if it is in $K$.
- **(A)** $\beta$ satisfies the tableau rows, so $\beta \in K$.
- **(N)** Each nonbasic $x_j$ has $l_j \le \beta(x_j) \le u_j$, and each variable has $l_j \le u_j$.

**Lemma 1 (the invariants hold).** They hold at the start and after each operation.

*Proof.* At the start there are no slacks, all variables are nonbasic, the tableau is empty, $K$ is the whole space, $\beta = 0$, and there are no bounds. A new slack $x_{n+k} = a_k \cdot x$ becomes basic: its row is $a_k \cdot x$ with each basic $x_j$ replaced by its row, which is equivalent under (T), and its value is the value of that row at $\beta$, so (A) holds. Its bounds are missing, so (N) is not affected.

UPDATE$(x_j, v)$ (lines L17 and L18) adds $v - \beta(x_j)$ to $x_j$ and $a_{kj}(v - \beta(x_j))$ to each basic $x_k$, so each row still holds and (A) stays. ASSERT-UPPER calls it only with $v = c$ after line L13 checked $c \ge l_j$, and $c$ is the new $u_j$, so (N) stays. Line L13 also keeps $l_j \le u_j$, because a bound that breaks it is never stored. ASSERT-LOWER is the mirror image.

PIVOT-AND-UPDATE$(x_i, x_j, v)$ (lines L19 to L22) adds $\theta$ to $x_j$ and $a_{kj}\theta$ to each basic $x_k$, with $\theta = (v - \beta(x_i))/a_{ij}$. This is a move along the column of $x_j$, so the rows still hold, and $x_i$ gets the value $v$. Then PIVOT solves the row of $x_i$ for $x_j$ (possible since $a_{ij} \neq 0$) and puts the result into the other rows. Each step replaces a system by an equivalent one, so (T) stays, and (A) stays because (A) held before the pivot and the new system is equivalent. After the pivot, $x_i$ is nonbasic with value $v$, and $v$ is $l_i$ or $u_i$ (lines L7 and L11), so (N) holds for $x_i$. The other nonbasic variables keep their values and bounds.

POP restores bounds from the trail. Each entry of the trail holds the bound that was in force before a strictly tighter bound replaced it, so POP only makes bounds looser. Looser bounds keep (N). It does not change $\beta$ or the tableau. $\square$

**Lemma 2 (SAT is correct).** If CHECK returns SAT, then the rational vector of MODEL satisfies all asserted atoms.

*Proof.* Line L3 returns SAT only when no basic variable breaks a bound, and (N) covers the nonbasic variables, so $l_j \le \beta(x_j) \le u_j$ for each $j$. Write $\beta(x_j) = (c_j, k_j)$ and a bound as $(c', k')$. For a single true inequality $(c', k') \le (c_j, k_j)$: if $c' = c_j$ then $k' \le k_j$, and $c' + k'\delta \le c_j + k_j\delta$ for each $\delta > 0$; if $c' < c_j$ and $k' > k_j$, it holds for $0 < \delta \le (c_j - c')/(k' - k_j)$; in the other cases it holds for each $\delta > 0$. MODEL takes $\delta_0$ as the least of 1 and these quotients, so each bound holds for the rational values $c_j + k_j \delta_0$. A strict upper bound $u = (c, -1)$ then gives a value at most $c - \delta_0 < c$, and a strict lower bound gives a value more than $c$. By (A), $\beta \in K$; the definitions have rational coefficients and hold in each component, so they hold for $c + k\delta_0$ too. Each atom is a bound on an original variable or on a slack, so each atom holds. $\square$

**Lemma 3 (UNSAT is correct).** Each conflict is a Farkas certificate, so the asserted atoms have no real model.

*Proof.* A conflict at line L13 is the pair $x_i \le c$ and $l_i \le x_i$ with $c < l_i$: the sum $(x_i - c) + (l_i - x_i) = l_i - c > 0$ would be $\le 0$ in a model.

Take line L6. The row of the basic $x_i$ is $x_i = \sum_j a_{ij} x_j$, and $\beta(x_i) < l_i$. No candidate exists, so each $x_j$ with $a_{ij} > 0$ has $\beta(x_j) \ge u_j$, and by (N) $\beta(x_j) = u_j$. In the same way each $x_j$ with $a_{ij} < 0$ has $\beta(x_j) = l_j$. So, by (A),
$$\beta(x_i) = \sum_{a_{ij} > 0} a_{ij} u_j + \sum_{a_{ij} < 0} a_{ij} l_j < l_i.$$
Now take any vector $v \in K$ that meets the bounds in the conflict. By (T), $v$ meets the row. Each term below is at most 0:
$$(l_i - v_i) + \sum_{a_{ij} > 0} a_{ij}(v_j - u_j) + \sum_{a_{ij} < 0} (-a_{ij})(l_j - v_j).$$
The variable parts add up to $-v_i + \sum_j a_{ij} v_j = 0$, by the row. The constant parts add up to $l_i - \beta(x_i) > 0$. So the sum is a positive constant and also at most 0, a contradiction. The multipliers are $1$, $a_{ij}$ and $-a_{ij}$, all positive. Line L10 is the mirror image. The rows of the tableau are linear consequences of the definitions, so the same sum, with each slack replaced by its definition, has all coefficients 0 on the original variables; this is the form that the implementation returns, with each bound scaled back to its atom. In $\mathbb{Q}_\delta$, a positive constant $(c, k)$ means $c > 0$, or $c = 0$ and $k > 0$; the second case can only come from a strict bound with a positive multiplier, which then also excludes a real model. $\square$

**Lemma 4 (termination).** Each call of CHECK makes finitely many pivots.

*Proof.* Inside CHECK the bounds do not change, UPDATE is not called, and a nonbasic variable changes its value only when it enters the basis. Suppose that CHECK runs forever. Each round of the loop makes one pivot, which changes the status of two variables. There are finitely many variables, so some variables change status infinitely often; call them *fickle*. Pick a time $T$ after which no other variable changes status. Let $x_t$ be the fickle variable with the largest index. After $T$, $x_t$ leaves and enters infinitely often, so there is a pivot $E_1$ after $T$ at which $x_t$ leaves and a later pivot $E_2$ at which $x_t$ enters, with no pivot of $x_t$ in between.

At $E_1$, $x_t$ is the basic variable of least index that breaks a bound (line L2). Let $\varepsilon_t = +1$ if $\beta(x_t) < l_t$ and $-1$ if $\beta(x_t) > u_t$. After $E_1$, $x_t$ is nonbasic with value $b_t = l_t$ or $u_t$ (lines L7 and L11), and it keeps this value until $E_2$. Let $\beta_1$ be the assignment just before $E_1$ and $\beta_2$ the assignment just before $E_2$, and let $\Delta = \beta_2 - \beta_1$. Then $\varepsilon_t \Delta_t = \varepsilon_t (b_t - \beta_1(x_t)) > 0$.

At $E_2$, let $x_s$ be the basic variable that leaves, with basis $B'$ and row $x_s = \sum_{j \notin B'} a'_{sj} x_j$. Let $\varepsilon_s = +1$ if $\beta_2(x_s) < l_s$ and $-1$ if $\beta_2(x_s) > u_s$. $x_s$ is fickle and $s \neq t$, so $s < t$.

*The sign of $a'_{st}$.* $x_t$ can enter only if $l_t < u_t$, since a nonbasic variable with $l_t = u_t$ is never a candidate at line L5 or L9. If $\varepsilon_t = +1$, then $\beta_2(x_t) = l_t < u_t$, so $x_t$ can only go up, and lines L5 and L9 allow this exactly when $\varepsilon_s a'_{st} > 0$. If $\varepsilon_t = -1$, then $\beta_2(x_t) = u_t$, $x_t$ can only go down, and this needs $\varepsilon_s a'_{st} < 0$. In both cases $\varepsilon_s \varepsilon_t a'_{st} > 0$.

*The row identity.* Both $\beta_1$ and $\beta_2$ are in $K$ by (A), so $\Delta \in K$, and by (T) $\Delta$ meets the row of $x_s$ in $B'$:
$$\varepsilon_s \Delta_s = \sum_{j \notin B'} \varepsilon_s a'_{sj} \Delta_j. \tag{1}$$

*The left side is negative.* $\beta_2(x_s)$ breaks a bound of $x_s$ in the direction $\varepsilon_s$. Just before $E_1$, $x_s$ is either nonbasic, and then inside its bounds by (N), or basic with index $s < t$, and then inside its bounds because $x_t$ was the least-index violated basic variable. So $\varepsilon_s \Delta_s < 0$.

*The right side is positive.* Look at each $j \notin B'$ with $a'_{sj} \neq 0$.

- $j = t$: $\varepsilon_s a'_{st} \Delta_t$ has the sign of $\varepsilon_s \cdot \varepsilon_s \varepsilon_t \cdot \varepsilon_t = +1$, so it is positive.
- $x_j$ not fickle: $x_j$ is nonbasic during the whole time after $T$, so its value does not change, and $\Delta_j = 0$.
- $x_j$ fickle, $j \neq t$: then $j < t$, and $x_j$ was not chosen at $E_2$, so it is not a candidate. If $\varepsilon_s a'_{sj} > 0$, not being a candidate means $\beta_2(x_j) = u_j$. Just before $E_1$, $x_j$ was inside its bounds (nonbasic by (N), or basic with $j < t$ as above), so $\Delta_j = u_j - \beta_1(x_j) \ge 0$. If $\varepsilon_s a'_{sj} < 0$, then $\beta_2(x_j) = l_j$ and $\Delta_j \le 0$. In both cases $\varepsilon_s a'_{sj} \Delta_j \ge 0$.

So the right side of (1) is positive and the left side is negative, a contradiction. Hence CHECK stops.

*A bound on the number of pivots.* Inside CHECK each nonbasic variable has its value from the start of the call, or the value of one of its bounds, because a variable becomes nonbasic only by leaving at a bound. The basis and the nonbasic values fix the tableau and the basic values. So there are at most $\binom{N}{m} 3^{N} \le 6^N$ states. The step from one state to the next is deterministic, so a repeated state would make the run periodic and infinite, which we excluded. So CHECK makes fewer than $6^{n+m}$ pivots. $\square$

**Theorem.** Call an atom *active* if it was asserted and no POP has undone it. CHECK stops after finitely many pivots. It returns SAT with a rational model of all active atoms, or UNSAT with a Farkas certificate over a subset of the active atoms, and then the active atoms have no real model.

*Proof.* Lemmas 1 to 4. $\blacksquare$
