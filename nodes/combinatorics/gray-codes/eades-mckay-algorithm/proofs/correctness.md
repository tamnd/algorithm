---
title: The Eades-McKay walk visits every (s, t)-combination once by homogeneous steps
proves: [correctness]
status: full
---

Strings are written $a_m \ldots a_1 a_0$ with the leading bit first. An $(s, t)$-string has $s$ zeros and $t$ ones. A step from $u$ to $v$ is *homogeneous* when $v$ arises from $u$ by exchanging a 1 and a 0 such that every bit strictly between them is 0. This relation is symmetric, and it is kept when the same prefix is put in front of both strings. The lists are $K_{s0} = (0^s)$ for $s \ge 0$, $K_{0t} = (1^t)$ for $t \ge 0$, $K_{st}$ empty if $s$ or $t$ is negative, and for $s, t \ge 1$

$$K_{st} = 0K_{(s-1)t},\ \ 10K^R_{(s-1)(t-1)},\ \ 11K_{s(t-2)}.$$

The third part is empty when $t = 1$. All three parts are nonempty otherwise, since their indices are not negative.

**Lemma 1 (content).** $K_{st}$ contains every $(s, t)$-string exactly once.

*Proof.* Induction on $s + t$. For $s = 0$ or $t = 0$ there is one such string. For $s, t \ge 1$, an $(s, t)$-string starts with 0, with 10, or with 11. Those that start with 0 are $0$ followed by an $(s-1, t)$-string, those that start with 10 are $10$ followed by an $(s-1, t-1)$-string, and those that start with 11 are $11$ followed by an $(s, t-2)$-string, of which there are none when $t = 1$. By induction each part holds its class once, and reversal does not change the content. $\square$

**Lemma 2 (ends).** $K_{st}$ starts at $0^s1^t$ and ends at $1^t0^s$.

*Proof.* Induction on $s + t$. Both claims hold for one-string lists. Let $s, t \ge 1$. The list starts at $0$ followed by the first string of $K_{(s-1)t}$, which is $0 \cdot 0^{s-1}1^t = 0^s1^t$. If $t \ge 2$ it ends at $11$ followed by the last string of $K_{s(t-2)}$, which is $11 \cdot 1^{t-2}0^s = 1^t0^s$. If $t = 1$ it ends at $10$ followed by the first string of $K_{(s-1)0}$, which is $10 \cdot 0^{s-1} = 10^s = 1^t0^s$. $\square$

**Lemma 3 (seams).** Let $s, t \ge 1$ and $m = s + t - 1$.

- The last string of $0K_{(s-1)t}$ and the first string of $10K^R_{(s-1)(t-1)}$ differ by moving the 1 at position $m - 1$ to position $m$, a homogeneous step.
- If $t \ge 2$, the last string of $10K^R_{(s-1)(t-1)}$ and the first string of $11K_{s(t-2)}$ differ by moving the 1 at position $t - 2$ to position $m - 1$, and the bits between are 0, so the step is homogeneous.

*Proof.* By Lemma 2 the first string is $0\,1^t0^{s-1}$. The first string of a reversed list is the last string of the list, so the second is $10\,1^{t-1}0^{s-1}$. They agree except at positions $m$ and $m - 1$, which are neighbors.

For the second seam, the last string of the reversed list is the first string of $K_{(s-1)(t-1)}$, so the first string is $10\,0^{s-1}1^{t-1}$, with ones at positions $m$ and $t - 2, \ldots, 0$. The second is $11\,0^s1^{t-2}$, with ones at positions $m$, $m - 1$ and $t - 3, \ldots, 0$. They agree except at positions $m - 1$ and $t - 2$, and in the first string the positions $t - 1, \ldots, m - 2$ between them hold the $s - 1$ zeros of $0^{s-1}$. $\square$

**Lemma 4 (steps).** Consecutive strings of $K_{st}$ differ by a homogeneous step.

*Proof.* Induction on $s + t$. Lists of one string have no steps. For $s, t \ge 1$, steps inside a part are steps of a smaller list, possibly reversed, with the same prefix in front, so they are homogeneous by induction and symmetry. The steps between parts are homogeneous by Lemma 3. $\square$

**Lemma 5 (the walk).** Suppose WALK$(s, t, d)$ starts when $a_{s+t-1} \ldots a_0$ holds the first string of $K_{st}$ if $d$ is forward and the last one if $d$ is reverse. Then the call visits $K_{st}$ in order if $d$ is forward and in reverse order if not, never reads or writes positions above $s + t - 1$, and returns with $a_{s+t-1} \ldots a_0$ equal to the other end of $K_{st}$.

*Proof.* Induction on $s + t$. If $s = 0$ or $t = 0$, line L3 visits the only string, which is both ends. Let $s, t \ge 1$ and $m = s + t - 1$ from line L4.

*Forward.* The array holds $0^s1^t$, which is $0$ followed by the first string of $K_{(s-1)t}$. Line L6 visits $0K_{(s-1)t}$ by induction, with $a_m = 0$ untouched, and ends at its last string. Line L7 makes the first move of Lemma 3, which gives $10$ followed by the last string of $K_{(s-1)(t-1)}$. Line L8 walks $K_{(s-1)(t-1)}$ in reverse on positions $m - 2, \ldots, 0$, with $a_m a_{m-1} = 10$ untouched, so it visits the second part and ends at $10$ followed by the first string of $K_{(s-1)(t-1)}$. If $t = 1$ this is the last string of $K_{st}$ and the call returns. If $t \ge 2$, line L10 makes the second move of Lemma 3, and line L11 visits $11K_{s(t-2)}$ forward, with $a_m a_{m-1} = 11$ untouched, and ends at the last string of $K_{st}$.

*Reverse.* The reverse of $K_{st}$ is $11K^R_{s(t-2)},\ 10K_{(s-1)(t-1)},\ 0K^R_{(s-1)t}$. If $t \ge 2$, line L14 walks $K_{s(t-2)}$ in reverse from the last string of $K_{st}$ and ends at the first string of the third part, and line L15 undoes the move of line L10, which by Lemma 3 gives the last string of the second part. If $t = 1$ the array already holds that string, since the second part is the end of the list. Line L16 walks $K_{(s-1)(t-1)}$ forward, which visits the second part in reverse order, and ends at its first string. Line L17 undoes the move of line L7, which gives the last string of the first part. Line L18 walks $K_{(s-1)t}$ in reverse and ends at $0^s1^t$.

The inner calls work on at most $m$ low positions, so by induction they stay below $m$, and lines L7, L10, L15 and L17 touch only $m$, $m - 1$ and $t - 2 < m$. $\square$

**Theorem.** For $s, t \ge 0$, EADES-MCKAY$(s, t)$ visits every $(s, t)$-string exactly once, in the order $K_{st}$, and consecutive visits differ by a homogeneous step. The walk makes at most $2C(s + t, t) - 1$ calls of WALK.

*Proof.* Line L1 sets $a$ to $0^s1^t$, the first string of $K_{st}$ by Lemma 2. By Lemma 5 line L2 visits $K_{st}$ in order. Lemma 1 gives each string once and Lemma 4 gives homogeneous steps. For the count: a call with $s, t \ge 1$ makes two or three calls, each for a nonempty list, and a call with $s = 0$ or $t = 0$ makes none and visits once. A tree with $L$ leaves in which every inner node has at least two children has at most $L - 1$ inner nodes, so there are at most $2C(s + t, t) - 1$ calls. $\blacksquare$
