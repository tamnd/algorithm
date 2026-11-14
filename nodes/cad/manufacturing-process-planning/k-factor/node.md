---
tag: 1D12MX
kind: definition
slug: k-factor
name: K-factor
aliases:
- neutral axis factor
area: cad/manufacturing-process-planning
level: intro
summary: The distance from the inner surface of a bend to its neutral axis divided by the sheet thickness, a measured value of about 0.3 to 0.5 that sets the bend allowance.
see_also: [bend-allowance, flat-pattern-development, springback-compensation]
sources:
  - book: isbn:9780133128741
    title: Serope Kalpakjian and Steven R. Schmid, Manufacturing Engineering and Technology, 7th edition, Pearson, 2014
    locator: Chapter 16 (sheet-metal forming), the part on bending of sheets and plates, where k is about 0.33 for R < 2T and 0.5 for R > 2T (general locator; the section number is not confirmed)
  - title: DIN 6935, Kaltbiegen von Flacherzeugnissen aus Stahl (cold bending of flat rolled steel products), Beuth, 2011
    locator: the correction factor k = 0.65 + 0.5 log10(r/s) for the position of the neutral line, with k = 1 for r/s > 5
---

The K-factor of a sheet metal bend is the position of the neutral axis in the thickness of the sheet, as a fraction of the thickness from the inside face. It is the one material and process parameter in the [bend allowance](/bend-allowance/) formula $\mathrm{BA} = \theta (R + K t)$. It is not computed from geometry. Shops measure it from test bends, or take it from a table or a standard.

## Definition

**K-factor.** Let a sheet of thickness $t$ be bent with inside radius $R$. In the bend zone, the outer fibres get longer and the inner fibres get shorter. The *neutral axis* is the fibre whose length does not change. If it is at the distance $\delta$ from the inside face, the K-factor is

$$K = \frac{\delta}{t}, \qquad 0 \le K \le 1,$$

and the neutral axis has radius $R + K t$. The bounds are exact, because the neutral axis is inside the material. Within the bounds, $K$ is an empirical value. Kalpakjian and Schmid give about 0.33 for $R < 2t$ and 0.5 for $R > 2t$. A thin sheet on a large radius bends almost elastically, and its neutral axis is near the mid-plane, $K = 0.5$. A tight bend moves the neutral axis toward the inside, so $K$ gets smaller. Tables for air bending seldom give a value of $K$ above 0.5.

**$K$ from a test bend.** Bend a strip with flat flange lengths $a$ and $b$ through the angle $\theta$ (in radians), or cut a strip of known length $L$ and measure the flanges after the bend. The bend allowance is $\mathrm{BA} = L - a - b$, and since $\mathrm{BA} = \theta (R + K t)$,

$$K = \frac{1}{t}\left(\frac{L - a - b}{\theta} - R\right).$$

The error in $K$ is the measurement error in $L - a - b$ times $1/(\theta t)$. So a test bend with a large angle on a thick sheet gives the most exact $K$.

**$K$ from DIN 6935.** The German standard DIN 6935 gives a correction factor $k = 0.65 + 0.5 \log_{10}(r/s)$ for inside radius $r$ and thickness $s$, with $k = 1$ for $r/s > 5$. It puts the neutral axis at the radius $r + (s/2) k$, so $K = k/2$. This is an empirical fit for steel, not a law.

**What $K$ ignores.** One number for $K$ ignores that the neutral axis of strain and the neutral axis of stress are not the same fibre, that the sheet gets thinner in the bend, and that the value changes with the material, the grain direction, the tool (air bending, bottoming or coining) and the die opening. For this reason the same $K$ is good only for the material, thickness, radius and tool of the test bend.

## Examples and non-examples

**A test bend.** A steel strip with $t = 2$ mm is bent through $\theta = \pi/2$ on a tool with $R = 3$ mm. The flat flanges after the bend are $a = 45$ mm and $b = 25$ mm, and the blank was $L = 75.8$ mm.

| step | formula | value |
|---|---|---|
| bend allowance | $L - a - b$ | 5.8 mm |
| neutral radius | $\mathrm{BA} / \theta$ | 3.6924 mm |
| distance $\delta$ | $\mathrm{BA}/\theta - R$ | 0.6924 mm |
| K-factor | $\delta / t$ | 0.3462 |

The value is in the range of Kalpakjian and Schmid for $R < 2t$. An error of 0.1 mm in $L - a - b$ changes $K$ by $0.1/(\theta t) = 0.0318$: a blank of 75.7 mm gives $K = 0.3144$ and one of 75.9 mm gives $K = 0.3780$. So a test bend must be measured to a few hundredths of a millimetre to give $K$ to two decimal places.

**The same bend from DIN 6935.** With $r/s = 1.5$, $k = 0.65 + 0.5 \log_{10} 1.5 = 0.7380$, so $K = 0.3690$, the neutral radius is 3.7380 mm and the blank is 75.8717 mm. The table value and the measured value are different by 0.07 mm in the blank. This is typical: a table is a start value, and a test bend sets the value for production.

**Non-examples.**

- The bend allowance is not a K-factor. In the example $\mathrm{BA} = 5.8$ mm is a length, and $K = 0.3462$ is a ratio without unit.
- The ratio $R/t$ is not a K-factor, although tables give $K$ as a function of it.
- The DIN factor $k$ is not the K-factor of this page. It is measured from the inside face in units of $s/2$, so $K = k/2$. A $k$ of 0.738 means $K = 0.369$.

## Related definitions

- [Bend allowance](/bend-allowance/): the bend allowance is the length of the neutral axis through one bend, which is computed from the K-factor, while the K-factor is only the position of that axis in the thickness.
- [Flat pattern development](/flat-pattern-development/): the blank of a part, with one bend allowance per bend, so one $K$ per material, thickness and tool.
- [Springback compensation](/springback-compensation/): the elastic opening of the bend after release, a different effect that $K$ does not include.

## References
