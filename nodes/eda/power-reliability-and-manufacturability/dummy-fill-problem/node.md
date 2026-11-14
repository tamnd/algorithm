---
tag: FGFG7V
kind: problem
slug: dummy-fill-problem
name: Dummy fill problem
aliases:
- metal fill
- layout density control
area: eda/power-reliability-and-manufacturability
level: core
summary: Add non-functional fill shapes to a layout so that metal density in every window lies within bounds for even chemical-mechanical polishing, with little extra coupling.
prereqs: [linear-programming-problem]
see_also: [lp-density-fill, critical-area, crosstalk-noise, binary-integer-programming, design-rule-checking, prefix-sums]
sources:
  - paper: doi:10.1145/274535.274549
    title: Andrew B. Kahng, Gabriel Robins, Anish Singh, Huijuan Wang and Alexander Zelikovsky, Filling and slotting, analysis and algorithms, Proceedings of the International Symposium on Physical Design (ISPD), 95 to 102, 1998
    locator: the Filling and Slotting Problem with area density bounds on every w by w window, the extremal-density window analysis (Theorem 1 on windows with a corner on the Hanan grid, and the prefix-sum and O(k^2) algorithms), and Theorem 8 on the error of fixed dissections
  - paper: "Andrew B. Kahng, Gabriel Robins, Anish Singh and Alexander Zelikovsky, Filling algorithms and analyses for layout density control, IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems 18(4), 445 to 462, April 1999"
    locator: the min-variation fill formulation with an upper density bound, the fixed r-dissection of the layout into tiles, and the slack of each tile
  - paper: "Brian E. Stine, Duane S. Boning, James E. Chung and others, The physical and electrical effects of metal-fill patterning practices for oxide chemical-mechanical polishing processes, IEEE Transactions on Electron Devices 45(3), 665 to 679, 1998"
    locator: the dependence of the dielectric thickness after polishing on the local pattern density, the reduction of that variation by metal fill, and the extra capacitance that fill adds
---

The dummy fill problem asks where to add electrically unused shapes to a layout layer so that the area density of the layer, measured in every window of a fixed size, lies between given bounds and varies as little as possible. Its purpose is chemical-mechanical polishing (CMP): the thickness left after polishing depends on the local pattern density, so a layer with dense and sparse regions ends with an uneven surface, which harms both the next lithography step and the wire resistance and capacitance. Fill may only go in the free space at a safe distance from the real wires, and each fill shape adds coupling capacitance, so the problem trades uniform density against [crosstalk](/crosstalk-noise/) and delay. Kahng, Robins, Singh, Wang and Zelikovsky gave the window formulation in 1998 and 1999 that this page uses.

## In plain words

Polishing a chip flat works like sanding a floor that has some tiles sticking up. Where there are many metal lines, the pad meets more metal and wears the surface more slowly, and where there are few, it wears faster. The result is a surface with hills and valleys.

The fix is to add small pieces of metal that carry no signal in the empty places, so that every patch of the chip of a given size has about the same amount of metal. The rules say how much metal each patch must have, at least and at most. The pieces must keep away from the real wires, and they should not add too much electrical coupling to them.

The task is to choose where the pieces go and how many, so that the emptiest patch is as full as it can be while no patch is too full.

## Definition

**Layout.** The layout region is the square $R = [0, n]^2$. The features $F \subset R$ are a finite union of rectangles on one layer. A buffer distance $B > 0$ defines the *slack region* $S = \{p \in R : \operatorname{dist}(p, F) \ge B\}$, minus any keep-out areas; fill may be placed only in $S$. A *fill* is a set $P \subseteq S$ that is a finite union of fill shapes obeying the fill design rules (shape size, spacing).

**Windows and density.** For a window size $w \le n$, a *window* is a square $Q = x + [0, w]^2 \subseteq R$. The density of $Q$ under fill $P$ is

$$ d_P(Q) = \frac{\operatorname{area}\big((F \cup P) \cap Q\big)}{w^2}. $$

Two families of windows are used. The *floating* family $\mathcal{W}$ contains all windows in $R$, a continuum. For an integer $r \ge 1$ such that $w/r$ divides $n$, the *fixed $r$-dissection* cuts $R$ into tiles of side $w/r$, and $\mathcal{W}_r$ contains the windows whose corners lie on the tile grid, each a block of $r \times r$ tiles.

**Min-variation fill (Min-Var).** Given an upper bound $U$, find a fill $P$ that

$$ \text{maximizes } \min_{Q \in \mathcal{W}} d_P(Q) \quad \text{subject to} \quad \max_{Q \in \mathcal{W}} d_P(Q) \le U. $$

The density variation $\max_Q d_P(Q) - \min_Q d_P(Q)$ is then at most $U - \min_Q d_P(Q)$, which is what the objective drives down.

**Feasibility version.** Given $L \le U$, find a fill with $L \le d_P(Q) \le U$ for every window, or report that none exists. This is the Filling and Slotting Problem of Kahng et al. (1998) for area density; slotting removes metal from inside wide wires to lower the density where it is above $U$.

## Variants

- **Window family.** The rules are stated for floating windows, but tools check and optimize a fixed $r$-dissection, which has $(r(n/w) - r + 1)^2$ windows. Larger $r$ is more accurate and more costly; the error is bounded below.
- **Min-Fill.** Given $L \le U$, minimize the fill area $\operatorname{area}(P)$ subject to $L \le d_P(Q) \le U$ for all windows. Less fill means less added capacitance and smaller mask data.
- **Continuous or discrete fill.** In the continuous variant each tile $T$ may receive any fill area between $0$ and its slack $\operatorname{slack}(T) = \operatorname{area}(S \cap T)$, because the slack is assumed to be fillable at any fraction. In the discrete variant fill is made of fixed squares on a grid, and each tile receives an integer number of them.
- **Performance-aware fill.** Minimize the extra coupling capacitance, or the extra delay on critical nets, subject to the density bounds. Grounded fill adds capacitance to ground, floating fill adds coupling between neighbor wires, and Stine et al. measured both effects.
- **Model-based fill.** Replace the window density by an *effective density*, the pattern density smoothed with a weighting function whose width is the planarization length of the CMP process, and bound the predicted thickness range instead of the density range.
- **Several layers.** Fill on one layer changes the capacitance of the layers above and below, and the thickness after CMP of one layer affects the next, so the layers interact.

## Examples

**Fixed windows can miss the worst window.** Let $n = 4$, $w = 2$ and let the only feature be the square $[1, 3]^2$ of area 4. With $r = 1$ the fixed windows are the four quadrants $[0, 2]^2$, $[2, 4] \times [0, 2]$, $[0, 2] \times [2, 4]$ and $[2, 4]^2$, and each contains a $1 \times 1$ corner of the feature, so every fixed window has density $\frac{1}{4}$. The floating window $[1, 3]^2$ has density $1$. A rule checked only on the fixed windows with $U = \frac{1}{4}$ passes this layout, while the true maximum density is four times higher. With $r = 2$ the tiles have side 1, the window $[1, 3]^2$ is in $\mathcal{W}_2$, and the error disappears for this layout.

**The lowest window decides the objective.** Let $n = 3$, $w = 1$, $r = 1$, so the nine unit tiles are the windows. Let the feature density of the tiles be $0.5$ in the middle tile and $0.1$ in the eight others, and let the slack of each outer tile be $0.3$, while the middle tile has slack $0.4$. With $U = 0.6$, the best Min-Var fill fills each outer tile completely, to $0.1 + 0.3 = 0.4$, and gives the middle tile any density in $[0.5, 0.6]$. The optimal minimum density is $0.4$, set by the slack of the outer tiles and not by $U$. Fill cannot lower the middle tile below its feature density $0.5$, so the best variation is $0.5 - 0.4 = 0.1$, attained when the middle tile gets no fill.

**An infeasible instance.** If any window already has feature density above $U$, no fill helps, since fill only adds area. The layout must be changed, or the wide wires slotted.

## Known algorithms

- **Density analysis.** Kahng et al. (1998) compute the extremal-density windows of a layout with $k$ rectangles in $O(n^2)$ time on an $n \times n$ grid with two-dimensional [prefix sums](/prefix-sums/), each window then costing four lookups, and in $O(k^2)$ time by sliding windows along rectangle sides. They also proved that some maximum-density window has a corner on the Hanan grid of the layout (their Theorem 1).
- **[Linear programming fill](/lp-density-fill/)** (Kahng, Robins, Singh and Zelikovsky 1999). Solve the continuous Min-Var problem on a fixed $r$-dissection exactly as a [linear program](/linear-programming-problem/) with one fill variable per tile, then place fill shapes in each tile to match the amounts.
- **Integer programming.** The discrete variant is an integer program with the same constraints; it is solved exactly for small instances or by rounding the LP solution.
- **Greedy and randomized fill.** Add fill one shape at a time in the tile that belongs to the window of least density, or choose tiles at random with probabilities weighted by need, until no window can be raised. These scale to full chips and give no optimality guarantee.
- **Row-based fill.** For wiring laid out in rows, where the spacing rules already keep the density below the upper bound, Kahng et al. (1998) sort the wires by row and by left end, then put fill in the gaps of each row from left to right. This takes $O(k \log k)$ time and targets only the lower bound.

## Bounds

- **Feasibility.** Fill only adds area, so a fill with all densities at most $U$ exists if and only if every window has feature density at most $U$ (the empty fill then works). And every fill satisfies $\min_Q d_P(Q) \le \min_Q \operatorname{area}((F \cup S) \cap Q)/w^2$, the density with all slack filled.
- **Fixed against floating windows.** If every window of $\mathcal{W}_r$ has density in $[L, U]$, then every floating window has density in $[L - \frac{1}{r} + \frac{1}{4r^2},\ U + \frac{1}{r} - \frac{1}{4r^2}]$, and the bounds are tight (Kahng et al. 1998, Theorem 8). For $r = 1$ the excess is $\frac{3}{4}$, which the first example attains: $\frac{1}{4} + \frac{3}{4} = 1$. For $r = 4$ it is $0.234$ and for $r = 16$ it is $0.061$. The proof is on the [LP fill](/lp-density-fill/) page.
- **Size of the fixed problem.** With $m = r n / w$ tiles on a side, the fixed problem has $m^2$ tile variables and $(m - r + 1)^2$ windows, so its size grows with the square of $r$.

## Reductions

- The continuous Min-Var and Min-Fill problems on a fixed dissection reduce to linear programs: the density of a window is a sum of tile densities, linear in the fill amounts, and the objectives are linear after adding one variable for the minimum. See [LP density fill](/lp-density-fill/).
- The discrete variant is a [0-1 or integer linear program](/binary-integer-programming/) over the fill sites.
- Density analysis on a grid is a two-dimensional range-sum problem, answered in constant time per window after building prefix sums.

## Applications

- **Oxide CMP.** The dielectric between metal layers is polished flat; its final thickness depends on the density of the metal below, and fill reduces the spread of that thickness, as Stine et al. measured.
- **Copper damascene CMP.** Copper wires are made by polishing away excess copper; wide wires dish and dense regions erode, and density rules with fill and slotting keep both within limits.
- **Foundry rules.** Foundries state minimum and maximum density rules per window for each layer; layouts are filled after routing so that [design rule checking](/design-rule-checking/) of these rules passes.
- **Yield interplay.** Fill changes the spaces between shapes, so it can change the [critical area](/critical-area/) for shorts if placed too close; the buffer $B$ limits that effect.

## References
