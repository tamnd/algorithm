---
title: What each ePIE step guarantees
proves: [correctness]
status: partial
---

ePIE has no proof of global convergence; the problem it solves is not convex. This page proves what holds for each step: the modulus replacement is a nearest-point projection, the object and probe updates are gradient steps that do not increase the residual at the current position, a pair that fits all the data is a fixed point, and the data cannot tell apart the pairs of a few known families.

**Notation.** The object $O$ is an $n_1 \times n_2$ complex image and the probe $P$ an $m_1 \times m_2$ complex image, with $N = m_1 m_2$ pixels. For a position $j$, $O_j$ is the window of $O$ under the probe, and $\psi_j = P \odot O_j$ is the exit wave, where $\odot$ is the pixelwise product. $F$ is the unnormalized 2D DFT, so $F/\sqrt{N}$ is unitary and $\|F x\| = \sqrt{N}\, \|x\|$. The data are the amplitudes $a_j \ge 0$. The *modulus set* of position $j$ is

$$M_j = \{\psi : |F\psi| = a_j \text{ entry by entry}\}.$$

For a complex image $x$ let $\pi_j(x)$ be the output of lines L4 and L5: $\pi_j(x) = F^{-1} R_j(F x)$, where $R_j(Y)$ is $a_j Y/|Y|$ at entries with $Y \ne 0$ and $a_j$ at entries with $Y = 0$.

**Lemma 1 (modulus replacement is a projection).** For every $x$, $\pi_j(x) \in M_j$ and $\|x - \pi_j(x)\| = \min_{\psi \in M_j} \|x - \psi\|$.

*Proof.* Put $Y = F x$. For one entry, a complex number $z$ with $|z| = a$ obeys $|Y - z| \ge \big||Y| - a\big|$ by the triangle inequality, with equality at $z = a Y/|Y|$ if $Y \ne 0$ and at every such $z$ if $Y = 0$. So $R_j(Y)$ is a nearest point to $Y$ in the set $\{Z : |Z| = a_j\}$, entry by entry, hence in the product set. Since $\|F x - F\psi\| = \sqrt{N} \|x - \psi\|$, a nearest point to $Y$ among the $F\psi$ with $\psi \in M_j$ gives a nearest point to $x$ in $M_j$. $\square$

The set $M_j$ is not convex, and the nearest point is not unique where $Y$ has a zero entry with $a_j > 0$. Lemma 1 also gives the identity $\big\| |F x| - a_j \big\| = \sqrt{N}\, \|x - \pi_j(x)\|$, so the data error at one position is a distance to $M_j$.

**Lemma 2 (the object step).** Fix the probe and a position $j$. Let $\psi = P \odot O_j$ and $\psi' = \pi_j(\psi)$ (lines L3 to L5), and let $p = \max |P|^2 > 0$. Line L7 sets

$$O_j^{\text{new}} = O_j + \frac{\alpha}{p}\, \overline{P} \odot (\psi' - \psi).$$

(a) This is a step of size $\alpha/p$ along the negative gradient, in the Wirtinger sense, of $f(O_j) = \|P \odot O_j - \psi'\|^2$ with respect to $\overline{O_j}$, with $\psi'$ held fixed.

(b) At each pixel, $P\, O_j^{\text{new}} - \psi' = \big(1 - \alpha |P|^2/p\big)(\psi - \psi')$.

(c) For $0 < \alpha \le 2$, the factor in (b) lies in $[-1, 1]$, so $|P\, O_j^{\text{new}} - \psi'| \le |\psi - \psi'|$ at every pixel.

*Proof.* (a) $f = \sum |P O - \psi'|^2$ over the pixels, and $\partial f/\partial \overline{O} = \overline{P}(P O - \psi') = -\overline{P}(\psi' - \psi)$ at each pixel. (b) Multiply the update by $P$ and subtract $\psi'$: $P O_j + (\alpha/p)|P|^2 (\psi' - \psi) - \psi' = (1 - \alpha |P|^2/p)(\psi - \psi')$. (c) $0 \le |P|^2/p \le 1$, so the factor lies in $[1 - \alpha, 1] \subset [-1, 1]$. $\square$

The division by the maximum of $|P|^2$, not by $|P|^2$ at each pixel, is what keeps the step stable: where the probe is weak, the factor is close to $1$ and the object barely changes, so noise in dark parts of the probe is not amplified.

**Corollary 1 (the data error at the current position does not grow).** With a fixed probe and $0 < \alpha \le 2$, the object step does not increase the distance of the exit wave at position $j$ to $M_j$:

$$\operatorname{dist}(P \odot O_j^{\text{new}}, M_j) \le \|P \odot O_j^{\text{new}} - \psi'\| \le \|\psi - \psi'\| = \operatorname{dist}(\psi, M_j).$$

*Proof.* The first inequality holds because $\psi' \in M_j$. The second is Lemma 2(c) summed over the pixels. The equality is Lemma 1. $\square$

By the identity after Lemma 1, the data error $\big\||F(P \odot O_j)| - a_j\big\|$ at position $j$ does not grow either. The step changes the pixels that position $j$ shares with other positions, so the total error over all positions can grow in one step. This is why the corollary is not a convergence proof.

**Lemma 3 (the probe step).** Fix the object and let $o = \max |O_j|^2 > 0$. Line L8 sets $P^{\text{new}} = P + (\beta/o)\, \overline{O_j} \odot (\psi' - \psi)$. With $O_j$ fixed, the statements of Lemma 2 and Corollary 1 hold with the roles of $P$ and $O_j$ exchanged and $\alpha$ replaced by $\beta$.

*Proof.* The exit wave $P \odot O_j$ is symmetric in $P$ and $O_j$, and the proofs use nothing else. $\square$

ePIE applies both steps from the same old pair (the code computes the probe step from the old window $O_j$). The new exit wave is then

$$P^{\text{new}} O_j^{\text{new}} - \psi' = \Big(1 - \frac{\alpha |P|^2}{p} - \frac{\beta |O_j|^2}{o}\Big)(\psi - \psi') + \frac{\alpha\beta}{p\, o}\, \overline{P}\, \overline{O_j}\, (\psi' - \psi)^2,$$

which follows by multiplying out the two updates. The first factor can leave $[-1, 1]$ for $\alpha = \beta = 1$, and the second term is of second order in the residual. So the joint step is not covered by Lemma 2, and no monotone decrease is claimed for it. For small residuals the joint step behaves like a gradient step on both factors, which is a heuristic, not a theorem.

**Lemma 4 (fixed points).** If a pair $(O, P)$ fits all the data, that is $|F(P \odot O_j)| = a_j$ for every $j$, then ePIE started at $(O, P)$ returns $(O, P)$ unchanged, for every order of the positions and all $\alpha$ and $\beta$.

*Proof.* At each step $\psi \in M_j$. Where $F\psi \ne 0$, $R_j$ returns $a_j F\psi/|F\psi| = F\psi$; where $F\psi = 0$, $a_j = 0$ and $R_j$ returns $0$. So $\psi' = \psi$, line L6 gives $\psi' - \psi = 0$, and lines L7 and L8 change nothing. By induction over the steps, the pair never changes. $\square$

**Lemma 5 (ambiguities).** The data error is the same for $(O, P)$ and for each of these pairs:

1. $(c\, O, P/c)$ for a complex $c \ne 0$, which includes a global phase factor $c = e^{i\theta}$ on the object alone with $e^{-i\theta}$ on the probe, and a global phase of both;
2. $(O e^{i k \cdot r}, P e^{-i k \cdot r})$ for a real vector $k$, where $r$ is the pixel position in the object and in the probe frame;
3. $(e^{i\theta} O, P)$ and $(O, e^{i\theta} P)$ for real $\theta$.

*Proof.* In case 1 the exit wave does not change. In case 2 the exit wave at the window offset $R_j$ is $P(r') O(R_j + r') e^{i k \cdot R_j}$, the old exit wave times a constant of modulus 1, and $|F|$ ignores a constant phase factor. Case 3 is a constant phase factor on every exit wave. $\square$

So ePIE can at best recover the object up to these changes. With a known, fixed probe, cases 1 and 2 cannot occur, and the global phase of case 3 remains. Whether the data fix the object up to that phase alone is a question of uniqueness, which depends on the overlap of the windows; this proof does not cover it.

**What is not proved.** There is no proof that ePIE converges to a pair that fits the data, or to the true pair up to Lemma 5, from a general start. The tests on the page are measurements on small synthetic cases. The analysis of ePIE and related methods as stochastic or alternating minimization schemes is the subject of later work and is outside this proof.
