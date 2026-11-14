---
tag: BMEE6J
kind: theorem
slug: grashof-condition
name: Grashof condition
aliases:
- Grashof criterion
- Grashof's law
area: cad/mechanism-and-assembly-design
level: intro
summary: In a four-bar linkage with shortest link s, longest l and others p and q, some link turns fully relative to another if and only if s + l <= p + q.
prereqs: [four-bar-linkage]
see_also: [transmission-angle, vector-loop-closure, slider-crank-mechanism, kinematic-chain, freudenstein-equation, roberts-chebyshev-theorem, kinematic-synthesis, coupler-curve]
sources:
  - book: "Franz Grashof, Theoretische Maschinenlehre, Volume 2, Theorie der Getriebe und der mechanischen Messinstrumente, Leopold Voss, Leipzig, 1883"
    locator: the part on the kinematics of linkages (general locator; no page number confirmed)
  - book: isbn:9781260113310
    title: Robert L. Norton, Design of Machinery, 6th edition, McGraw-Hill, 2019
    locator: Section 2.13 (p. 55, the Grashof condition, with the classification of the fourbar on p. 60) and Section 2.12 (p. 53, inversion)
  - book: isbn:9780190264482
    title: John J. Uicker, Gordon R. Pennock and Joseph E. Shigley, Theory of Machines and Mechanisms, 5th edition, Oxford University Press, 2017
    locator: Section 1.9, Grashof's law
  - book: doi:10.1007/978-1-4419-7892-9
    title: J. Michael McCarthy and Gim Song Soh, Geometric Design of Linkages, 2nd edition, Springer, 2011
    locator: Chapter 2 (pp. 15 to 53), the range of movement of the planar 4R linkage
  - book: isbn:0130408727
    title: Arthur G. Erdman, George N. Sandor and Sridhar Kota, Mechanism Design, Analysis and Synthesis, Volume 1, 4th edition, Prentice Hall, 2001
    locator: the chapter on the fundamentals of linkages, the Grashof criterion
---

The Grashof condition decides, from the four link lengths alone, whether any link of a [four-bar linkage](/four-bar-linkage/) can turn through a full revolution relative to another. With $s$ the shortest length, $l$ the longest and $p$, $q$ the other two, some joint turns fully exactly when $s + l \le p + q$. When the inequality is strict, the joints that turn fully are exactly the two joints on the shortest link. Equality gives a change point linkage, which can lie flat and change its assembly there.

This page is about which joints can turn fully. The [transmission angle](/transmission-angle/) page is about the same linkage at each position, and how well it passes force from the coupler to the output.

## Statement

A four-bar chain is four rigid links of positive lengths, joined in a cycle by four revolute joints and moving in the plane. It can be assembled exactly when $l \le s + p + q$, and this is assumed. Sort the lengths as $s \le p \le q \le l$. A joint *turns fully* when the angle between its two links takes every value in $[0, 2\pi)$ in some assembly.

**Theorem (Grashof).**

1. *Joint test.* Let a joint join the links of lengths $x$ and $y$, and let $u$ and $v$ be the other two lengths. The joint turns fully if and only if $x + y \le u + v$ and $|x - y| \ge |u - v|$.
2. *The condition.* Some joint turns fully if and only if $s + l \le p + q$. More exactly, a joint turns fully if and only if $s + l \le p + q$ and one of its two links is a shortest link.
3. *Strict case.* If $s + l < p + q$, the shortest link is unique, the two joints on it turn fully, the other two joints do not, and each full turn is a continuous motion that never passes a position where the two assemblies meet.
4. *Change point.* If $s + l = p + q$, the linkage has a configuration with all four links on one line, and in it the two assemblies of every joint meet.

The theorem does not depend on which link is the ground, so it holds for all four inversions of a chain.

## In plain words

Take four sticks and pin them into a loop. Can one stick spin all the way round against its neighbour? Add the shortest and the longest stick, and add the other two. If the first sum is not larger, yes, and the stick that spins round is the shortest one. If the first sum is larger, no stick can spin round, and every joint only swings back and forth.

When the two sums are equal, the loop can be folded flat onto one line. At that moment it can go on in two different ways, so a real machine of this kind can jump from one way of moving to the other.

## Proof

**Step 1, the joint test.** Let $\varphi$ be the angle at a joint $J$ between the links $x$ and $y$, and let $\delta$ be the distance between their far ends. By the law of cosines, $\delta^2 = x^2 + y^2 - 2xy\cos\varphi$. The other two links $u$ and $v$ join the two far ends through one more joint, so an assembly with angle $\varphi$ exists exactly when two circles of radii $u$ and $v$, with centers $\delta$ apart, meet. That is, exactly when $|u - v| \le \delta \le u + v$. As $\varphi$ goes from $0$ to $\pi$, $\delta$ grows continuously from $|x - y|$ to $x + y$, and the angles in $[\pi, 2\pi)$ give the same values again. So every $\varphi$ is feasible exactly when $[|x - y|, x + y] \subseteq [|u - v|, u + v]$, which is the pair of inequalities of part 1.

**Step 2, the joint test in terms of $s$ and $l$.** Name the lengths so that $x \le y$ and $u \le v$. The joint test is then $x + y \le u + v$ (i) and $y - x \ge v - u$ (ii).

*If the joint turns.* Add (i) and the inequality $x - y \le u - v$ from (ii): $2x \le 2u$. So $x \le u \le v$ and $x \le y$, and $x$ is a shortest link, $x = s$. If $l = y$, then (i) is $s + l \le p + q$. If $l = v$, then (ii) reads $x + v \le y + u$, which is again $s + l \le p + q$.

*If $s + l \le p + q$ and $x = s$.* If $l = y$, then $\{u, v\} = \{p, q\}$, so (i) is $s + l \le p + q$, and (ii) holds because $y = l \ge v$ and $x = s \le u$. If $l = v$, then (i) holds because $x \le u$ and $y \le v$, and (ii) is $x + v \le y + u$, which is $s + l \le p + q$.

This proves the second sentence of part 2. Each link has two joints, so a joint on a shortest link exists, and the first sentence follows.

**Step 3, the strict case.** If $s = p$, then $s + l < p + q$ gives $l < q$, which is false. So $s < p$, the shortest link is unique, and by step 2 exactly the two joints on it turn fully. In step 1 the two assemblies at an angle $\varphi$ meet only when $\delta$ equals $u + v$ or $|u - v|$. For a joint that turns, $\delta$ stays in $[|x - y|, x + y]$, so they could meet only if $x + y = u + v$ or $|x - y| = |u - v|$, that is, only if some split of the four lengths into two pairs has equal sums. The split $\{s, l\}, \{p, q\}$ has unequal sums by hypothesis. The split $\{l, q\}, \{s, p\}$ has $l + q > s + p$ because $p > s$, and the split $\{l, p\}, \{s, q\}$ has $l + p > s + q$ for the same reason with $l \ge q$. So the two assemblies never meet. They are mirror images in the diagonal, and the side of the diagonal on which the far joint lies cannot change without a meeting, so following one of them as $\varphi$ grows is a continuous full turn that comes back to the start.

**Step 4, the change point.** If $s + l = p + q$, put the four links on the $x$ axis in their cyclic order, with the links $s$ and $l$ pointing in the $+x$ direction and $p$ and $q$ in the $-x$ direction. The signed lengths add to $s + l - p - q = 0$, so the chain closes, and every joint angle is $0$ or $\pi$. For each joint the two other links $u$ and $v$ lie on one line with the diagonal, so $\delta = u + v$ or $\delta = |u - v|$, and by step 1 the two assemblies at that angle coincide. $\blacksquare$

## Consequences

- **The classification of four-bars.** With $s + l < p + q$, the position of the shortest link decides the type: on the ground, a double-crank; the input, a crank-rocker; the output, a rocker-crank; the coupler, a Grashof double-rocker, in which only the coupler turns fully. With $s + l > p + q$ the linkage is a triple-rocker. The table is on the [four-bar linkage](/four-bar-linkage/) page, which also uses the same split argument to count the circuits: two for $s + l < p + q$, one for $s + l > p + q$.
- **Design of cranks.** A motor needs a crank that turns fully, so a crank-rocker design starts with the input shortest and $s + l < p + q$. The [Freudenstein equation](/freudenstein-equation/) and other [kinematic synthesis](/kinematic-synthesis/) methods give lengths that must be checked against this condition.
- **The slider-crank limit.** Letting one link and the ground grow without bound turns the four-bar into the [slider-crank mechanism](/slider-crank-mechanism/), and the condition becomes $b \ge a + |e|$ for crank length $a$, rod length $b$ and offset $e$.
- **Cognates.** By the [Roberts-Chebyshev theorem](/roberts-chebyshev-theorem/), a crank-rocker has one crank-rocker cognate and one Grashof double-rocker cognate, and a double-crank has two double-crank cognates. The three cognates are all Grashof or all not.
- **Tests by a sweep.** The [vector loop closure](/vector-loop-closure/) page solves the position at each input angle. The tests there sweep every joint of 500 random integer linkages and agree with the joint test and the class in every case.

## Tightness

The inequality cannot be weakened. For every $\varepsilon > 0$, the lengths $2, 4, 4, 6 + \varepsilon$ have $s + l = p + q + \varepsilon$, and no joint turns fully. With $\varepsilon = 0$, the change point linkage $2, 4, 4, 6$ (ground $6$, input $2$, coupler $4$, output $4$) has a crank that turns fully, and at $\theta_2 = \pi$ all four links lie on the ground line: the crank pin is at $(-2, 0)$, the coupler runs from there to $(2, 0)$, and the output folds back from $(2, 0)$ to $(6, 0)$. So the boundary case belongs to the side where a joint turns, and it is the only case where the two assemblies meet during a full turn.

Part 3 also needs the strict inequality. In a parallelogram $a, b, a, b$, $s + l = p + q$ and all four joints turn fully, not only two. At the flat positions the parallelogram can switch to the antiparallelogram (crossed) motion.

## History

Franz Grashof stated the condition in Volume 2 of his Theoretische Maschinenlehre (1883). Textbooks call it the Grashof condition, the Grashof criterion or Grashof's law, and give the classification of the four inversions by the position of the shortest link. Later work classified all four-bars, including the non-Grashof and change point cases, by the same sums.

## References
