---
title: The Land-Doig algorithm returns an optimal integer solution
proves: [correctness, termination]
status: full
---

We use the pseudocode of the page. Let $P = \{x \ge 0 : A x \le b\}$, which we assume bounded. For a set $F$ of fixings $x_j = k$ ($j \in I$, $k \in \mathbb{Z}$, each $j$ at most once), let $P(F) = P \cap \{x : x_j = k \text{ for } (x_j = k) \in F\}$ and $Z(F) = \{x \in P(F) : x_j \in \mathbb{Z} \text{ for } j \in I\}$. Let $v(F) = \max_{x \in P(F)} c^\top x$, or $-\infty$ if $P(F) = \emptyset$. Clearly $c^\top x \le v(F)$ for $x \in Z(F)$. Let $z^* = \max_{x \in Z(\emptyset)} c^\top x$, or $-\infty$ if $Z(\emptyset) = \emptyset$.

**Lemma 1 (values move down away from the LP optimum).** Let $P(F) \ne \emptyset$ with optimal solution $\bar{x}$, let $j \in I$ be free in $F$, and let $\varphi(t) = v(F \cup \{x_j = t\})$ for real $t$. Then $D = \{t : \varphi(t) > -\infty\}$ is an interval that contains $\bar{x}_j$, $\varphi$ is concave on $D$, and $\varphi(\bar{x}_j) = v(F)$. So for $t \le t' \le \bar{x}_j$ or $\bar{x}_j \le t' \le t$, we have $\varphi(t) \le \varphi(t')$; in particular, if $t \notin D$, then no $t$ further from $\bar{x}_j$ on the same side is in $D$.

*Proof.* $D$ is the projection of the convex set $P(F)$ on the coordinate $j$, so it is an interval, and $\bar{x}_j \in D$. If $y, y'$ are optimal for $t, t' \in D$ and $0 \le \lambda \le 1$, then $\lambda y + (1 - \lambda) y' \in P(F)$ has $x_j = \lambda t + (1 - \lambda) t'$, so $\varphi(\lambda t + (1-\lambda) t') \ge \lambda \varphi(t) + (1 - \lambda) \varphi(t')$. Also $\varphi(t) \le v(F) = c^\top \bar{x} = \varphi(\bar{x}_j)$. A concave function with its maximum at $\bar{x}_j$ does not increase as $t$ moves away from $\bar{x}_j$: if $\bar{x}_j \le t' \le t$, write $t' = \lambda t + (1 - \lambda) \bar{x}_j$ and get $\varphi(t') \ge \lambda \varphi(t) + (1 - \lambda) \varphi(\bar{x}_j) \ge \varphi(t)$. The other side is the same. $\square$

**Regions.** For a live node with fixings $F$ and note $sib$, its *region* is $Z(F)$ if $sib = \text{NIL}$, and $Z(F) \cup \bigcup_{t \ge 0} Z(F' \cup \{x_j = k + t s\})$ if $sib = (F', j, k, s)$. Every live node with $sib \ne \text{NIL}$ was made as $F = F' \cup \{x_j = k - s\}$, where $k - s$ is on the side $s$ of $\bar{x}_j(F')$ (with $\bar{x}_j(F')$ fractional), so by Lemma 1 each point of the region has value at most $v(F)$.

**Claim 2 (incumbent).** At each point, $best = \text{NIL}$ and $z = -\infty$, or $best \in Z(\emptyset)$ and $z = c^\top best$; so $z \le z^*$, and $z$ never decreases. *Proof.* Only line L9 changes them, to the LP solution of a node whose integer variables are all integers, which lies in $Z(F) \subseteq Z(\emptyset)$; and it does so only if $v > z$. $\square$

**Claim 3 (a skipped MAKE loses nothing).** Suppose MAKE$(G, sib)$ is called with $G = F' \cup \{x_j = k\}$ and $sib = (F', j, k + s, s)$, where $k$ is on the side $s$ of $\bar{x}_j(F')$, and it does not insert $G$. Then every point of $Z(G) \cup \bigcup_{t \ge 1} Z(F' \cup \{x_j = k + t s\})$ has value at most $z$, for the current and every later $z$. *Proof.* If $P(G) = \emptyset$, then $k \notin D$, and by Lemma 1 no further value is in $D$, so all these sets are empty. Otherwise $v(G) \le z$, and by Lemma 1 every further value has $\varphi \le v(G) \le z$. As $z$ never decreases, this stays true. $\square$

**Claim 4 (invariant).** At the start of each iteration of line L3, every $x \in Z(\emptyset)$ with $c^\top x > z$ lies in the region of some live node.

*Proof.* At the start, if MAKE$(\emptyset, \text{NIL})$ inserted the root, its region is $Z(\emptyset)$; if not, $P = \emptyset$ and there is no $x$. Suppose the claim holds at the start of an iteration that takes the node $N = (F, \bar{x}, v, sib)$ and does not break. Let $x \in Z(\emptyset)$ with $c^\top x > z$ at the end of the iteration; then $c^\top x > z$ held at the start too, so $x$ lies in the region of a node that was live. If that node is not $N$, it is still live. Suppose it is $N$.

- If $x$ is in the chain part of the region of $N$, then $x \in Z(F' \cup \{x_j = k + t s\})$ for some $t \ge 0$. Line L7 calls MAKE on $t = 0$ with the note for $t \ge 1$. If it inserts the node, $x$ is in its region; if not, Claim 3 gives $c^\top x \le z$, which is false.
- If $x \in Z(F)$ and $\bar{x}$ is integral on $I$, then line L9 makes $z \ge v \ge c^\top x$, which is false.
- If $x \in Z(F)$ and $\bar{x}_j$ is fractional for the $j$ of line L10, let $f = \lfloor \bar{x}_j \rfloor$. Since $x_j$ is an integer, either $x_j = f - t$ for some $t \ge 0$, so $x$ is in $Z(F \cup \{x_j = f\})$ or in the chain of the first MAKE of line L11, or $x_j = f + 1 + t$, and $x$ is in $Z(F \cup \{x_j = f + 1\})$ or the chain of the second. If the node is inserted, $x$ is in its region; if not, Claim 3 gives a contradiction.

So the claim holds at the start of the next iteration. $\square$

**Claim 5 (termination).** Each set of fixings is passed to MAKE at most once, and there are finitely many. *Proof.* $P$ is bounded, so each $x_j$ ranges in a bounded interval on $P$, and a fixing $x_j = k$ outside it gives an empty $P(F)$; such a node is never inserted, and its chain is not continued. A node $G = F' \cup \{x_j = k\}$ is made only by line L11 while $F'$ is split, or by line L7 while the node $F' \cup \{x_j = k - s\}$ is taken. By induction on $|G|$, $F'$ is inserted at most once, hence taken and split at most once, on a single $j$; the two chains $f, f - 1, \ldots$ and $f + 1, f + 2, \ldots$ each make every value at most once, and each chain stops at the first value that is not inserted. Sets of fixings have at most $|I|$ elements with values in bounded ranges, so there are finitely many, and the loop runs finitely often. $\square$

**Theorem.** LAND-DOIG returns $(z^*, best)$ with $best$ an optimal integer solution, or $(-\infty, \text{NIL})$ when there is none.

*Proof.* By Claim 5 the loop ends. If it ends because $H$ is empty, Claim 4 says no $x \in Z(\emptyset)$ has $c^\top x > z$. If it ends at line L5 with node $N$, every live node $M$ has $v(M) \le v(N) \le z$, so every point of every region has value at most $z$, and by Claim 4 (at the start of that iteration) no $x$ has $c^\top x > z$. So $z \ge z^*$, and by Claim 2 $z = z^*$, with $best$ optimal when $z^* > -\infty$. $\blacksquare$
