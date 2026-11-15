---
title: Array dataflow analysis returns the exact last writer for static control programs
proves: [correctness]
status: full
---

**Setting.** We use the notation of the page. The program is a static control program with integer parameters $N$ that satisfy the context $K$. Statement $S$ has depth $d_S$, a domain $D_S$ that is a polyhedron and is bounded for each $N$, and writes $A[f_S(\vec{s})]$ with $f_S$ affine. The read is $A[g(\vec{t})]$ in $T$, with $\vec{t} \in D_T$. All counters and parameters are integers. For two statements, $c = c_{ST}$ is the number of common loops, and $\beta^S_k$ is the text position of $S$ (or of the loop that holds it) at depth $k$. The schedule of $S(\vec{s})$ is $\theta_S(\vec{s}) = (\beta^S_0, s_1, \beta^S_1, \dots, s_{d_S}, \beta^S_{d_S})$, and the program runs the instances in the lexicographic order of their schedules. Two different statements in a common loop have different text positions at the first depth where they are not in the same loop, so two different instances never have the same schedule.

**Claim.** For every $N$ in $K$ and every $\vec{t} \in D_T$, the quast $Q$ returned at line L7, evaluated at $(\vec{t}, N)$, gives the instance $S(\vec{s})$ with the lexicographically greatest schedule among the instances that write $A[g(\vec{t})]$ and have a schedule less than $\theta_T(\vec{t})$, or $\bot$ if there is no such instance.

### Step 1: the candidate sets cover the earlier writes, and are disjoint

For a statement $S$ that writes $A$ and a depth $l \in \{1, \dots, c\}$, let

$$C_{S,l}(\vec{t}) = \{\vec{s} \in D_S : f_S(\vec{s}) = g(\vec{t}),\ s_k = t_k \text{ for } k < l,\ s_l \le t_l - 1\},$$

and if $\beta^S_c < \beta^T_c$, let $C_{S,\mathrm{eq}}(\vec{t}) = \{\vec{s} \in D_S : f_S(\vec{s}) = g(\vec{t}),\ s_k = t_k \text{ for } k \le c\}$. These are the sets of line L4.

**Lemma 1.** $\theta_S(\vec{s}) <_{\mathrm{lex}} \theta_T(\vec{t})$ if and only if $\vec{s}$ satisfies the depth condition of exactly one of these sets.

*Proof.* The first $2c$ components of the two schedules are $(\beta_0, s_1, \beta_1, \dots, s_c)$ and $(\beta_0, t_1, \beta_1, \dots, t_c)$, with the same $\beta_0, \dots, \beta_{c-1}$, because the statements share the loops 1 to $c$. Let $l$ be the first $k \le c$ with $s_k \ne t_k$, if there is one. Then the schedules differ first at the component of $s_l$, and $\theta_S(\vec{s}) < \theta_T(\vec{t})$ exactly when $s_l < t_l$, that is, $s_l \le t_l - 1$ for integers. This is the condition of $C_{S,l}$. If there is no such $l$, the next component is $\beta^S_c$ against $\beta^T_c$. If $S = T$, then $\vec{s} = \vec{t}$ on all $d_S = c$ loops, the instance is $T(\vec{t})$ itself, and it is not earlier. Otherwise $\beta^S_c \ne \beta^T_c$, by the remark in the setting, and the order is decided there: $S(\vec{s})$ is earlier exactly when $\beta^S_c < \beta^T_c$. This is the set $C_{S,\mathrm{eq}}$, which line L3 builds only in that case. The first index $l$ is unique, so the cases are disjoint. $\square$

The access condition $f_S(\vec{s}) = g(\vec{t})$ selects the writes of the element that $T(\vec{t})$ reads. So the union over all $S$ and all depths of the candidate sets is exactly the set of earlier writes of $A[g(\vec{t})]$, and each such write is in exactly one set.

### Step 2: inside one candidate set, later means lexicographically greater

**Lemma 2.** For $\vec{s}, \vec{s}' \in D_S$, $\theta_S(\vec{s}) <_{\mathrm{lex}} \theta_S(\vec{s}')$ if and only if $\vec{s} <_{\mathrm{lex}} \vec{s}'$.

*Proof.* Both schedules have the same constants $\beta^S_k$ at the same positions, and the counters in between. The first difference is at the first counter where $\vec{s}$ and $\vec{s}'$ differ, with the same sign. $\square$

So the latest instance in a candidate set is its lexicographic maximum.

### Step 3: PIP returns the integer lexicographic optimum for every parameter value

PIP works on a tableau whose rows are $x_i = c_i(p) + \sum_j a_{ij} n_j$, where $p$ are the parameters (here $\vec{t}$, $N$ and the new parameters), the $n_j$ are the nonbasic variables, and every row must be $\ge 0$. The first $n$ rows are the unknowns. At the start the nonbasic variables are the unknowns themselves, so these rows form the identity matrix. We call this tableau *lex-positive* when every column $(a_{1j}, a_{2j}, \dots)$ is lexicographically positive.

The unknowns of line L5 are $x_k = M - s_k$, where $M$ is a symbolic parameter. For fixed $N$ and $\vec{t}$ the candidate set is bounded, so for $M$ large enough all $x_k$ are nonnegative and the lexicographic minimum of $\vec{x}$ is reached at the lexicographic maximum of $\vec{s}$. The sign of an affine form with a nonzero $M$ coefficient is the sign of that coefficient for $M$ large enough, so the sign tests are correct for all large $M$.

**Lemma 3 (invariant).** At every step, (a) the tableau is lex-positive, (b) every integer point of the current problem is also a point of the original problem and conversely, every integer point of the original problem with parameters in the current context satisfies all the rows, and (c) the context is a subset of the original context, and the new parameters satisfy their definitions $D q \le e \le D q + D - 1$.

*Proof.* At the start the tableau is the identity in the unknown rows, so it is lex-positive, and (b) and (c) hold. A pivot at line L9 on row $r$ with $c_r < 0$ uses the column $j$ with $a_{rj} > 0$ whose column divided by $a_{rj}$ is lexicographically least. A pivot is an invertible affine change of the nonbasic variables, so the $n$ unknown rows always form an invertible $n \times n$ matrix, and every column is nonzero in its first $n$ entries. Each new column $l \ne j$ is $\mathrm{col}_l - (a_{rl}/a_{rj}) \mathrm{col}_j$. If $a_{rl} \le 0$, it is $\mathrm{col}_l$ plus a nonnegative multiple of $\mathrm{col}_j$, so it is lex-positive. If $a_{rl} > 0$, it is $a_{rl}(\mathrm{col}_l / a_{rl} - \mathrm{col}_j / a_{rj})$, which is lexicographically nonnegative by the choice of $j$ and is not zero by the remark above, so it is lex-positive. The new column $j$ is $\mathrm{col}_j / a_{rj}$, which is lex-positive. A pivot only rewrites the same equations with another set of nonbasic variables, so (b) holds. A split at line L10 adds a constraint to the context and changes no row. A cut at line L13 or L14 adds a row at the bottom, and Lemma 4 shows that every integer point satisfies it. The sign of a column is decided in its first $n$ entries, so a new row at the bottom keeps (a). The new parameter of line L14 comes with its two defining constraints, which gives (c). $\square$

**Lemma 4 (cuts).** Let row $k$ be $x_k = c_k(p) + \sum_j a_{kj} n_j$, with $x_k$ and all $n_j$ integers. Then every integer point satisfies $\sum_j \mathrm{frac}(-a_{kj}) n_j \ge \mathrm{frac}(c_k(p))$. The new row has an integer value at every integer point.

*Proof.* Write $x_k - \sum_j a_{kj} n_j = c_k$ and split each number into its floor and its fractional part: $x_k + \sum_j \lfloor -a_{kj} \rfloor n_j - \lfloor c_k \rfloor = \mathrm{frac}(c_k) - \sum_j \mathrm{frac}(-a_{kj}) n_j$. The left side is an integer. The right side is less than 1, because $\mathrm{frac}(c_k) < 1$ and the sum is nonnegative. So it is at most 0, which is the cut. The slack of the cut is the negative of the left side, an integer. When $c_k(p)$ has parameter terms, the code first replaces every coefficient by its fractional part, which changes $c_k(p)$ by an integer for integer $p$; call the result $f(p)$. With $D$ the common denominator, $q = \lfloor D f(p) / D \rfloor$ is an integer and $\mathrm{frac}(c_k(p)) = f(p) - q$, which is affine in $p$ and $q$. So the row of line L14 is the same cut. $\square$

The nonbasic variables are always unknowns or slacks of rows with integer values: the unknowns, the slacks of the constraints, which have integer coefficients, and the slacks of earlier cuts, which are integers by Lemma 4. So Lemma 4 applies at every step.

**Lemma 5.** Each leaf of the quast that PIP returns is correct on its context: (i) if it is "no solution", no integer point of the problem has parameters in the context; (ii) if it is $(c_1(p), \dots, c_n(p))$, then for every integer $p$ in the context this point is the integer lexicographic minimum.

*Proof.* (i) Line L8 returns "no solution" only if the context has no rational point, so it has no integer point. Line L9 returns it for a row with $c_r(p) < 0$ on the whole context and all $a_{rj} \le 0$; then $x_r \le c_r(p) < 0$ for every $n \ge 0$, so no point satisfies the row, and by Lemma 3 (b) the problem has no integer point. (ii) At line L12, every row has $c_i(p) \ge 0$ on the context, because the sign tests of lines L9 and L10 found no negative and no mixed constant. Setting all $n_j = 0$ gives $x = c(p)$, which satisfies every row. Any other point of the current rational problem has some $n_j > 0$. Its unknowns are $c(p) + \sum_j n_j \bar{a}_j$, where $\bar{a}_j$ is the part of column $j$ in the first $n$ rows. Each $\bar{a}_j$ is lex-positive, so a nonnegative combination of them that is not all zero is lex-positive, and the point is lexicographically greater than $c(p)$. So $c(p)$ is the rational lexicographic minimum of the current problem. All its coordinates are integers, because line L11 found no row with a non-integral constant. The current problem contains every integer point of the original problem, by Lemma 3 (b), so $c(p)$ is the integer lexicographic minimum. $\square$

The split at line L10 adds $c_i \ge 0$ to one branch and $c_i \le -1$ to the other, where $c_i$ is scaled to integer coefficients, so for integer parameters the two branches cover the context. The implementation also proves a row integral when it finds a new parameter $q$ that is already defined with the same numerator and denominator and the context forces $D q = e$; then $c_k(p)$ equals an integer form on the context, which is a rewriting and changes no value. So the quast of PIP, evaluated at any integer $p$ in the context, follows one path to a correct leaf.

**Termination.** The lemmas above show partial correctness: whenever PIP returns, its answer is right. Termination rests on Gomory's argument for the lexicographic dual simplex with cuts, which Feautrier's method follows: the lexicographic minimum grows strictly with each cut and stays in a bounded set. The implementation adds a depth limit that raises an error, so it never returns a wrong answer silently.

### Step 4: the merge keeps the later source

**Lemma 6.** For every integer point of the context, the quast $\mathrm{MERGE}(Q_1, Q_2)$ gives the later of the two instances that $Q_1$ and $Q_2$ give at that point, where an instance is later than $\bot$.

*Proof.* Merge walks down $Q_1$ and then $Q_2$, adding to the context the test of each node it passes or its negation $e \le -1$. For integer points the two branches of a node cover its context, so every integer point reaches the pair of leaves that $Q_1$ and $Q_2$ give there. If one leaf is $\bot$, merge returns the other. Otherwise it compares $\theta_S(\vec{h})$ and $\theta_{S'}(\vec{h}')$ component by component: at component $k$ it splits the context into the difference $\ge 1$, $\le -1$ and $= 0$, which for integers covers all cases, and goes to component $k + 1$ only in the third case. The first nonzero difference decides the lexicographic order, which is the execution order. If one vector is a prefix of the other, the leaves are the same instance (two different instances have different schedules, and both are then the same statement and point), and either is correct. A branch whose context has no rational point has no integer point, so dropping it loses nothing. $\square$

The function simplify, used after each merge, only drops branches without rational points and replaces a node by one of its subtrees when it proves, with rational tests on integer-valued differences, that both give the same instance at every point of the node's context. It changes no value at an integer point.

### Conclusion

By Lemma 1, the earlier writes of the element are partitioned into the candidate sets. By Lemmas 2 and 5, the quast $K$ of line L5 gives the latest write in its set, or $\bot$ if the set is empty. By Lemma 6 and induction on the number of sets merged so far, after line L6 the quast $Q$ gives the latest instance among all sets seen so far. After the last set, it gives the latest of all earlier writes of $A[g(\vec{t})]$, or $\bot$ when there is none. This is the source. $\blacksquare$
