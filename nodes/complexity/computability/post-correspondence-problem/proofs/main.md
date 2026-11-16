---
title: Proof that the Post correspondence problem is undecidable
proves: [statement]
status: full
---

The proof reduces the [acceptance problem](/acceptance-problem/) $A_{\mathrm{TM}}$ to PCP in two many-one reductions. The first goes to a *modified* problem MPCP: does the list have a match that uses the first domino at the start and nowhere else? The second removes this condition. The construction follows Sipser, Section 5.2.

**Conventions.** A domino $[t / b]$ has a top word $t$ and a bottom word $b$, both nonempty. A *match* for a list $[t_1/b_1], \ldots, [t_k/b_k]$ is a nonempty index sequence $i_1, \ldots, i_m$ with $t_{i_1} \cdots t_{i_m} = b_{i_1} \cdots b_{i_m}$. Let $M = (Q, \Sigma, \Gamma, \delta, q_0, q_{\mathrm{acc}}, q_{\mathrm{rej}})$ be a single-tape [Turing machine](/turing-machine/) with blank symbol $\sqcup$. We may assume that $M$ never tries to move its head left from the leftmost cell, since any machine can be changed to mark the left end of its tape first. A configuration is written $u\,q\,v$: the tape holds $uv$ followed by blanks, the state is $q$, and the head is on the first symbol of $v$. The symbol $\#$ is not in $\Gamma \cup Q$.

## Step 1: from A_TM to MPCP

Given $\langle M, w \rangle$ with $w = w_1 \cdots w_n$, build the following dominoes over the alphabet $\Gamma \cup Q \cup \{\#\}$.

1. The first domino is $[\#\ /\ \#\, q_0 w_1 \cdots w_n \#]$.
2. For all $q \in Q \setminus \{q_{\mathrm{acc}}, q_{\mathrm{rej}}\}$ and $a \in \Gamma$ with $\delta(q, a) = (r, b, R)$: the domino $[q a\ /\ b r]$.
3. For all such $q, a$ with $\delta(q, a) = (r, b, L)$, and every $c \in \Gamma$: the domino $[c q a\ /\ r c b]$.
4. For every $a \in \Gamma$: the domino $[a / a]$.
5. The dominoes $[\# / \#]$ and $[\#\ /\ \sqcup \#]$.
6. For every $a \in \Gamma$: the dominoes $[a\, q_{\mathrm{acc}}\ /\ q_{\mathrm{acc}}]$ and $[q_{\mathrm{acc}}\, a\ /\ q_{\mathrm{acc}}]$.
7. The domino $[q_{\mathrm{acc}} \# \#\ /\ \#]$.

The list is computable from $\langle M, w \rangle$.

**Claim.** The list has a match that uses domino 1 at the start and nowhere else if and only if $M$ accepts $w$.

*If $M$ accepts $w$.* Let $C_1, \ldots, C_\ell$ be the accepting run, with $C_1 = q_0 w$ and $q_{\mathrm{acc}}$ in $C_\ell$. Start with domino 1. The bottom is then ahead of the top by the word $q_0 w \#$. In general, suppose the top reads $\# C_1 \# \cdots \# C_{j-1} \#$ and the bottom reads the same followed by $C_j \#$. Copy $C_j$ onto the top, one domino at a time, from left to right: use dominoes of type 4 for the cells away from the head, and the single domino of type 2 or 3 for the cells around the head. Each step puts the matching piece of $C_{j+1}$ on the bottom, because the type 2 and type 3 dominoes are exactly the local changes made by $\delta$. Finish with $[\#/\#]$, or with $[\# / \sqcup \#]$ if the head moves onto a blank beyond the written part. Now the top reads up to $C_j \#$ and the bottom is ahead by $C_{j+1} \#$. When $C_\ell$ is reached, the type 6 dominoes delete one tape symbol next to $q_{\mathrm{acc}}$ per configuration, until the bottom is ahead by $q_{\mathrm{acc}} \#$ only. Domino 7 then closes the match.

*If there is such a match.* Read the match from the left. After domino 1 the bottom is ahead by $q_0 w \#$. We show by induction that, as long as no $q_{\mathrm{acc}}$ has been used, whenever the top has just finished a block that ends in $\#$, the top reads $\# C_1 \# \cdots \# C_j \#$ and the bottom reads the same followed by $C_{j+1} \#$, where $C_1, \ldots, C_{j+1}$ is the start of the run of $M$ on $w$. To cover the next block $C_{j+1} \#$ of the bottom, the top must spell $C_{j+1} \#$, and the only dominoes whose tops fit are those of types 2 to 5. Each of them puts on the bottom the word that the step of $M$ produces in that place. The state symbol of $C_{j+1}$ must be covered by a domino of type 2 or 3, since types 4 and 5 have no state symbol on top. If the state of $C_{j+1}$ is $q_{\mathrm{rej}}$, no domino covers it, so the match cannot end. So the bottom grows by $C_{j+2} \#$, the next configuration of the run. In this phase the bottom stays strictly longer than the top, so the match cannot end there. The only dominoes with a top longer than their bottom are those of types 6 and 7, and they need $q_{\mathrm{acc}}$ on top. So the run of $M$ on $w$ reaches $q_{\mathrm{acc}}$, and $M$ accepts $w$. $\square$

## Step 2: from MPCP to PCP

For a word $u = u_1 \cdots u_n$, write
$$\star u = \star u_1 \star u_2 \cdots \star u_n, \qquad u \star = u_1 \star u_2 \star \cdots u_n \star, \qquad \star u \star = \star u_1 \star \cdots \star u_n \star,$$
where $\star$ and $\diamond$ are new symbols. From an MPCP list $[t_1/b_1], \ldots, [t_k/b_k]$, build the PCP list
$$[\star t_1\ /\ \star b_1 \star],\quad [\star t_i\ /\ b_i \star] \text{ for } 2 \le i \le k,\quad [\star \diamond\ /\ \diamond].$$

**Claim.** The new list has a match if and only if the MPCP list has a match that uses domino 1 at the start and nowhere else.

*If.* From an MPCP match $1, i_2, \ldots, i_m$ with every $i_j \ge 2$, use the first new domino, then $[\star t_{i_j} / b_{i_j} \star]$ for $j = 2, \ldots, m$, then $[\star\diamond / \diamond]$. The top reads $\star x_1 \star x_2 \cdots \star x_N \star \diamond$ and so does the bottom, where $x_1 \cdots x_N$ is the common word of the MPCP match.

*Only if.* A match must start with a domino whose top and bottom start with the same symbol. Every top starts with $\star$, and the only bottom that starts with $\star$ is that of the first new domino. A match must also end with a domino whose top and bottom end with the same symbol. Every bottom ends in $\star$ or $\diamond$, and every top except $\star\diamond$ ends in a symbol of the old alphabet, so the match uses $[\star\diamond/\diamond]$. The symbol $\diamond$ comes only from this domino, so the first $\diamond$ is at the same place in both rows, and the parts before it are equal. In that part the top has the form $\star x_1 \star x_2 \cdots \star x_N \star$, with no two $\star$ next to each other. Every bottom of the dominoes used before ends in $\star$, so a second use of the first new domino would put $\star\star$ in the bottom; hence it is used only at the start. Deleting every $\star$ from both rows of this part gives a match of the old list that uses domino 1 at the start and nowhere else. $\square$

## The theorem

**Theorem.** PCP is computably enumerable and complete for the c.e. sets under many-one reductions. In particular it is undecidable, and the set of lists that have no match is not c.e. The same holds over the alphabet $\{0, 1\}$.

*Proof.* Membership: list all nonempty index sequences in order of length and check each one; halt when one is a match. Hardness: the two steps give $A_{\mathrm{TM}} \le_m \mathrm{MPCP} \le_m \mathrm{PCP}$, and $A_{\mathrm{TM}}$ is complete for the c.e. sets. A complete c.e. set is undecidable, and its complement is not c.e., since a set that is c.e. and co-c.e. is decidable. For the binary alphabet, code the symbols of an alphabet of size $s$ as distinct binary blocks of the same length $\lceil \log_2 s \rceil$. A uniform block code $h$ is injective on words, so $h(x) = h(y)$ holds if and only if $x = y$, and the list $[h(t_i)/h(b_i)]$ has the same matches as $[t_i/b_i]$. $\blacksquare$
