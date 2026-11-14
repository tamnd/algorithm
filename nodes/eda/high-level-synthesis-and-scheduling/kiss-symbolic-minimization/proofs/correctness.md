---
title: Correctness of the KISS construction
proves: [correctness]
status: full
---

We use the notation of the page. The machine has inputs $x \in \{0, 1\}^m$, states $s_1, \ldots, s_n$, and a partial function that gives, for some pairs $(x, s)$, a next state $\delta(x, s)$ and an output vector whose entries are 0, 1 or don't care. The symbolic function has the variables $x$ and $S$, and the outputs $N_t$ for each state $t$ and $Z_j$ for each primary output. At a specified pair $(x, s)$, $N_t$ is 1 if $t = \delta(x, s)$ and 0 otherwise, and $Z_j$ is the specified output or don't care. At an unspecified pair every output is don't care.

A cube $c$ of the symbolic cover has an input part $I_c$, a group $G_c$ of states, and a set of asserted outputs. It contains $(x, s)$ when $x \in I_c$ and $s \in G_c$. The cover is correct: at every point and for every output, the output is 1 where the function is 1 and 0 where it is 0, where the value of the cover at a point is 1 if some cube that contains the point asserts the output.

## Lemma 1 (what one encoded point sees)

Let $\mathrm{enc}$ be injective and meet the face constraint of every group of the cover. For a symbolic cube $c$, let $\hat c$ be its encoded cube: input part $I_c$ and state part $\mathrm{face}(G_c)$. Then for every input $x$ and state $s$, $\hat c$ contains $(x, \mathrm{enc}(s))$ if and only if $c$ contains $(x, s)$.

*Proof.* The input parts are equal, so it is enough to show that $\mathrm{enc}(s) \in \mathrm{face}(G_c)$ exactly when $s \in G_c$. If $s \in G_c$, then $\mathrm{enc}(s)$ is in the face by its definition. Conversely, suppose $\mathrm{enc}(s)$ is in the face. If $1 < |G_c| < n$, the face constraint of $G_c$ says that the face holds no code of a state outside $G_c$, so $s \in G_c$. If $|G_c| = n$, every state is in $G_c$. If $G_c = \{t\}$, the face is the single point $\mathrm{enc}(t)$, so $\mathrm{enc}(s) = \mathrm{enc}(t)$, and $s = t$ since $\mathrm{enc}$ is injective. $\square$

## Theorem (the KISS bound)

Under the same assumption, the encoded cubes of line L7, with the cubes whose output part is empty removed, form a correct two-level cover of the encoded function. So the encoded function has a cover with at most as many cubes as the symbolic cover.

*Proof.* Recall that line L7 gives $\hat c$ the next-state bits $b$ with $\mathrm{enc}(t)_b = 1$ for each state $t$ that $c$ asserts, and the primary outputs that $c$ asserts. Points of the encoded function are $(x, y)$ with $y \in \{0, 1\}^k$. If $y$ is not a code, or $(x, y) = (x, \mathrm{enc}(s))$ with $(x, s)$ unspecified, every output is don't care there and nothing needs checking.

Take a specified pair $(x, s)$ with $t = \delta(x, s)$, and let $A$ be the set of symbolic cubes that contain $(x, s)$. By Lemma 1, the encoded cubes that contain $(x, \mathrm{enc}(s))$ are exactly $\hat c$ for $c \in A$.

*Next-state bits.* The symbolic cover is correct, so $N_t = 1$ at $(x, s)$ forces some $c \in A$ to assert $N_t$, and $N_u = 0$ for $u \ne t$ forces no $c \in A$ to assert $N_u$. So every cube of $A$ asserts either $N_t$ alone among the next-state outputs or none of them. The bits that the cubes $\hat c$, $c \in A$, set are therefore exactly the 1 bits of $\mathrm{enc}(t)$, since at least one of them asserts $t$. The value of next-state bit $b$ at $(x, \mathrm{enc}(s))$ is $\mathrm{enc}(t)_b$.

*Primary outputs.* $\hat c$ asserts $Z_j$ exactly when $c$ does. So the value of $Z_j$ in the encoded cover at $(x, \mathrm{enc}(s))$ equals its value in the symbolic cover at $(x, s)$, which is correct.

Removing a cube that asserts nothing does not change any value. So the cover is correct, and it has at most one cube per symbolic cube. $\blacksquare$

## Lemma 2 (termination of line L5)

The one-hot code $\mathrm{enc}(s_i) = e_i$ of $n$ bits meets every face constraint. So line L5 stops with $k \le n$.

*Proof.* The codes $e_i$, $i \in G$, agree on every bit outside $G$, where they are 0, and differ on each bit of $G$ when $|G| \ge 2$. So the face of $G$ is the set of vectors that are 0 outside $G$. A code $e_j$ with $j \notin G$ has a 1 at bit $j$, outside $G$, so it is not in the face. $\square$

The search of line L5 tries every injective code of each length, so it finds a code that meets every constraint at the least such length, and line L6 returns one.

## What is not proved

Nothing here says that the codes of line L6 make the final logic small. The theorem is an upper bound, and it holds for every code that meets the constraints. Codes that meet them can differ in cost, and codes that break them can be cheaper; the page gives a machine with both effects, found by exhaustive search over all codes of two bits.
