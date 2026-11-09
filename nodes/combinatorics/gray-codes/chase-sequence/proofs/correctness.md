---
title: The Chase walk visits every (s, t)-combination once by near-perfect steps
proves: [correctness]
status: full
---

Strings are written $a_{m} \ldots a_1 a_0$ with the leading bit first. An $(s, t)$-string has $s$ zeros and $t$ ones. A step from $u$ to $v$ is *near-perfect* when $v$ arises from $u$ by replacing $10$ with $01$ or $01$ with $10$ in two adjacent positions, or $100$ with $001$ or $001$ with $100$ in three adjacent positions. This relation is symmetric. For $s, t \ge 0$ the lists are $A_{00} = B_{00} = (\varepsilon)$, a list with a negative index is empty, and otherwise

$$A_{st} = 1B_{s(t-1)},\ 0A^R_{(s-1)t}, \qquad B_{st} = 1A_{s(t-1)},\ 0A_{(s-1)t}.$$

Write $q_A(s) = \min(s, 1)$ and $q_B(s) = \min(s, 2)$, and for $t \ge 1$ let $E_q(s, t) = 0^q 1^t 0^{s-q}$, the block $1^t 0^s$ moved $q$ places right.

**Lemma 1 (one string).** If $s = 0$ or $t = 0$, then $A_{st} = B_{st}$ is the single string $1^t 0^s$.

*Proof.* Induction on $s + t$. If $s = t = 0$ this is the definition. If $s = 0 < t$, the second parts have index $-1$ and are empty, and the first parts are $1$ followed by the single string $1^{t-1}$. If $t = 0 < s$, the first parts are empty, and the second parts are $0$ followed by the single string $0^{s-1}$; reversal does not change a list of one string. $\square$

**Lemma 2 (content).** $A_{st}$ and $B_{st}$ each contain every $(s, t)$-string exactly once.

*Proof.* Induction on $s + t$, with Lemma 1 for $s = 0$ or $t = 0$. For $s, t \ge 1$, the first part of each list is $1$ followed by every $(s, t-1)$-string once, which gives every $(s, t)$-string that starts with 1. The second part is $0$ followed by every $(s-1, t)$-string once, in some order, which gives every $(s, t)$-string that starts with 0. The two parts are disjoint. $\square$

**Lemma 3 (ends).** Both lists start at $1^t 0^s$. If $t \ge 1$, $A_{st}$ ends at $E_{q_A(s)}(s, t)$ and $B_{st}$ ends at $E_{q_B(s)}(s, t)$. If $t = 0$, both end at $0^s$.

*Proof.* Induction on $s + t$. Lemma 1 covers $s = 0$ or $t = 0$, since then $q = 0$ and $E_0(s, t) = 1^t 0^s$. Let $s, t \ge 1$. Each list starts with the first string of $1X_{s(t-1)}$ for some $X$, which is $1 \cdot 1^{t-1} 0^s = 1^t 0^s$ by induction.

- $A_{st}$ ends at $0$ followed by the first string of $A_{(s-1)t}$, which is $0\,1^t 0^{s-1} = E_1(s, t)$, and $q_A(s) = 1$.
- $B_{st}$ ends at $0$ followed by the last string of $A_{(s-1)t}$. If $s = 1$ this is $0\,1^t = E_1(1, t)$, and $q_B(1) = 1$. If $s \ge 2$ it is $0\,E_1(s-1, t) = 0\,0\,1^t 0^{s-2} = E_2(s, t)$, and $q_B(s) = 2$. $\square$

**Lemma 4 (junctions).** Let $s, t \ge 1$ and $m = s + t - 1$, the position of the leading bit.

- In $A_{st}$, the last string of the first part and the first string of the second part differ by moving the 1 at position $m$ to position $y = m - 2$ if $s \ge 2$ and $y = m - 1$ if $s = 1$, and the step is near-perfect.
- In $B_{st}$, they differ by moving the 1 at position $m$ to position $y = m - 1$, and the step is near-perfect.

*Proof.* For $A_{st}$ the first part ends at $1$ followed by the last string of $B_{s(t-1)}$, and the second part starts at $0$ followed by the last string of $A_{(s-1)t}$. If $s \ge 2$, Lemma 3 gives $1\,00\,1^{t-1} 0^{s-2}$ and $0\,01^t 0^{s-2}$ (for $t = 1$ the first one is $1\,0^s$, of the same form). They differ only at positions $m$ and $m - 2$, and the bit at $m - 1$ is 0 in both, so the step is $100 \to 001$. If $s = 1$, Lemma 3 gives $1\,0\,1^{t-1}$ and $0\,1^t$, which differ by $10 \to 01$ at positions $m$ and $m - 1$.

For $B_{st}$ the first part ends at $1$ followed by the last string of $A_{s(t-1)}$, which is $1\,0\,1^{t-1}0^{s-1}$ by Lemma 3, and the second part starts at $0$ followed by the first string of $A_{(s-1)t}$, which is $0\,1^t 0^{s-1}$. They differ by $10 \to 01$ at positions $m$ and $m - 1$. $\square$

**Lemma 5 (steps).** Consecutive strings of $A_{st}$ and of $B_{st}$ differ by a near-perfect step.

*Proof.* Induction on $s + t$. Lists of one string have no steps. For $s, t \ge 1$, steps inside a part are steps of a smaller list, possibly reversed, with the same bit in front, and the relation is symmetric and does not depend on a common prefix. The step between the parts is near-perfect by Lemma 4. $\square$

**Lemma 6 (the walk).** Let $X \in \{A, B\}$, and suppose WALK$(s, t, X, d)$ starts when $a_{s+t-1} \ldots a_0$ holds the first string of $X_{st}$ if $d$ is forward and the last one if $d$ is reverse. Then the call visits $X_{st}$ in order if $d$ is forward and in reverse order if not, never reads or writes positions above $s + t - 1$, and returns with $a_{s+t-1} \ldots a_0$ equal to the other end of $X_{st}$.

*Proof.* Induction on $s + t$. If $s = 0$ or $t = 0$, line L3 visits the only string, which is both ends by Lemma 1. Let $s, t \ge 1$. Line L4 sets $m = s + t - 1$ and the $y$ of Lemma 4, and line L5 sets $Y$ to the kind of the first part: $B$ if $X = A$ and $A$ if $X = B$. The second part is $0A^R_{(s-1)t}$ if $X = A$ and $0A_{(s-1)t}$ if $X = B$.

*Forward.* The first string of $X_{st}$ is $1$ followed by the first string of $Y_{s(t-1)}$. Line L7 visits $1Y_{s(t-1)}$ by induction, with $a_m = 1$ untouched, and ends at its last string. Line L8 makes the move of Lemma 4, which gives the first string of the second part. Line L9 visits $A_{(s-1)t}$ in reverse if $X = A$ and forward if $X = B$, with $a_m = 0$ untouched, which is the second part, and it ends at the last string of $X_{st}$.

*Reverse.* The reverse of $X_{st}$ is the reverse of the second part followed by $1Y^R_{s(t-1)}$. The call starts at the last string of $X_{st}$. Line L11 walks $A_{(s-1)t}$ forward if $X = A$ and in reverse if $X = B$, which is the second part reversed, and ends at its first string. Line L12 undoes the move of line L8, which by Lemma 4 gives the last string of the first part. Line L13 walks $Y_{s(t-1)}$ in reverse and ends at $1^t 0^s$, the first string of $X_{st}$.

The inner calls work on $s + t - 1 = m$ low positions, so by induction they stay below $m$, and lines L8 and L12 touch only $m$ and $y < m$. $\square$

**Theorem.** For $s, t \ge 0$, CHASE$(s, t)$ visits every $(s, t)$-string exactly once, in the order of $C_{st}$, which is $A_{st}$ for odd $s + t$ and $B_{st}$ for even $s + t$, and consecutive visits differ by a near-perfect step. The walk makes $2C(s + t, t) - 1$ calls of WALK.

*Proof.* Line L1 sets $a$ to $1^t 0^s$, the first string of both lists by Lemma 3. Line L2 calls WALK with the kind of $C_{st}$, forward, so by Lemma 6 it visits $C_{st}$ in order. Lemma 2 gives each string once, and Lemma 5 gives near-perfect steps. For the count: a call with $s, t \ge 1$ makes two calls, each for a list that is not empty, and a call with $s = 0$ or $t = 0$ makes none and visits once. So the calls form a tree in which each inner node has two children and the $C(s + t, t)$ leaves are the visits, and such a tree has $C(s + t, t) - 1$ inner nodes. $\blacksquare$
