---
title: EHH returns the fraction of carrier pairs identical from the core to each marker, and the trapezoid area of that curve
proves: [correctness]
status: full
---

**Setting.** Haplotypes $h_1, \ldots, h_n$ have $m$ markers each, at positions $x_1 < \cdots < x_m$. The core is $c$, the allele is $a$, the carriers are $C = \{i : h_i[c] = a\}$, and $k = |C| \ge 2$. For a marker $j$, let $I(j)$ be the set of markers between $c$ and $j$, with both ends included. Two carriers $i$ and $i'$ are $j$-equal when they have the same allele at every marker of $I(j)$. This is an equivalence relation on $C$, and $\mathrm{EHH}(j)$ is the number of unordered $j$-equal pairs over $\binom{k}{2}$.

**Lemma 1 (refinement).** Let $d$ be $+1$ or $-1$, let $j$ be the core or a marker between the core and $j + d$, and let $j' = j + d$ be a marker. Then $i$ and $i'$ are $j'$-equal exactly when they are $j$-equal and have the same allele at $j'$.

*Proof.* $I(j') = I(j) \cup \{j'\}$. $\square$

**Lemma 2 (the invariant).** On one side $d$, after line L7 has run for the marker $j$, the list of classes holds exactly the classes of the $j$-equal relation that have two or more members, each one once.

*Proof.* By induction over the markers of the side. Before the first pass, the list is $[C]$, which is right: all carriers have allele $a$ at the core, and $I(c) = \{c\}$, so $C$ is the only class, and it has $k \ge 2$ members.

Suppose the list holds the classes of the $j$-equal relation with two or more members, and line L6 runs for $j' = j + d$. By Lemma 1, every class of the $j'$-equal relation is the set of members of one class $K$ of the $j$-equal relation that share one allele at $j'$. A class of the $j'$-equal relation with two or more members is inside such a $K$, which then also has two or more members, so $K$ is in the list, and line L6 forms that part and keeps it. Every part that line L6 keeps has two or more members and is a class of the $j'$-equal relation. Parts of different classes $K$ are disjoint, so no class is listed twice. $\square$

**Lemma 3 (the value at the markers the walk reaches).** Line L2 gives $E[c] = 1 = \mathrm{EHH}(c)$, and line L7 sets $E[j] = \mathrm{EHH}(j)$ for every marker $j$ that the walk reaches.

*Proof.* At the core, all $\binom{k}{2}$ pairs are $c$-equal, so $\mathrm{EHH}(c) = 1$. For a marker $j$ of the walk, a $j$-equal pair lies in one class of the $j$-equal relation, and that class then has two or more members. A class of $s$ members holds $\binom{s}{2}$ pairs of its own members, and all of them are $j$-equal. So, by Lemma 2, the sum of $\binom{|K|}{2}$ over the list is the number of $j$-equal pairs, and line L7 divides it by $\binom{k}{2}$. $\square$

**Lemma 4 (the markers the walk does not reach).** If the walk on side $d$ stops at a marker $j$ because the list is empty, then $\mathrm{EHH}(t) = 0$ for every marker $t$ that is further from the core than $j - d$ on that side. This is the value that line L2 left there.

*Proof.* The list became empty when line L6 ran for $j - d$, so by Lemma 2 no pair is $(j-d)$-equal. For such a $t$, $I(j - d)$ is a subset of $I(t)$, so a $t$-equal pair would also be $(j-d)$-equal. There is none. $\square$

**Lemma 5 (the curve is monotone).** $\mathrm{EHH}(c) = 1$, and $\mathrm{EHH}$ does not increase as the marker moves away from the core on either side.

*Proof.* By Lemma 1, every $j'$-equal pair is also $j$-equal, so the numerator does not increase. $\square$

**Lemma 6 (the area).** On one side $d$, line L8 adds the term $(E[j] + E[j-d]) \cdot |x_j - x_{j-d}| / 2$ for the markers $j = c + d, c + 2d, \ldots$, in this order, and stops before the first marker with $E[j] < \epsilon$, or at the end of the marker list. The total is the integral, from $x_c$ to the position of the last marker it added, of the piecewise linear function that passes through the points $(x_t, E[t])$.

*Proof.* The loop of line L8 visits the markers of the side in order from the core and stops at the first $j$ with $E[j] < \epsilon$ without adding its term, so the markers it adds are exactly those listed. The term of $j$ is the area of the trapezoid with the parallel sides $E[j-d]$ and $E[j]$ and the width $|x_j - x_{j-d}|$, which is the integral of the linear piece between the two positions. The pieces are next to each other and cover the interval from $x_c$ to the last added position, so the sum is the integral over that interval. $\square$

**Theorem.** For input haplotypes of one length, a core marker $c$ and an allele $a$ with $k \ge 2$ carriers, EHH returns the array $E$ with $E[j] = \mathrm{EHH}(j)$ for every marker $j$, and the number iHH, which is the sum over the two sides of the integral of Lemma 6. The values are exact rational numbers, because every step uses only integer counts and one division by $\binom{k}{2}$.

*Proof.* Line L1 forms $C$ by one pass over the core column and rejects $k < 2$. Lines L3 to L7 run the walk on both sides, and each side sets the values of its own markers only. By Lemma 3 the markers that the walk reaches get $\mathrm{EHH}$, and by Lemma 4 the others already hold their correct value 0 from line L2. The core gets 1 at line L2 and no walk changes it, because each walk starts at $c + d$. So $E$ is the EHH curve. Line L8 then returns the area of Lemma 6 for each side, and iHH is their sum. The implementation keeps the counts as integers and the values as fractions, so no rounding takes place. $\square$

**The score.** For a core marker where both alleles have two or more carriers and both areas are positive, the score is $\ln(\mathrm{iHH}_0 / \mathrm{iHH}_1)$, from one call of EHH per allele. It is 0 when the two curves give equal areas, negative when the derived allele has the larger area, and positive when the ancestral allele does.

**A check of the scale.** Suppose the $n$ haplotypes are independent and every marker of every haplotype is 0 or 1 with probability one half each, independently. Fix the core allele of the carriers. Two carriers agree at a given marker away from the core with probability one half, independently over the markers, so each pair is $j$-equal with probability $2^{-|I(j)| + 1}$, that is $2^{-r}$ for a marker $r$ steps from the core. By linearity over the $\binom{k}{2}$ pairs, the mean of $\mathrm{EHH}$ at that marker is $2^{-r}$. The tests use this to check the curve against its exact mean.
