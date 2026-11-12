---
tag: QPQHN8
kind: problem
slug: ellipse-rasterization
name: Ellipse rasterization
aliases:
- ellipse drawing
area: graphics-and-signals/rasterization
level: intro
summary: Choose the pixels that represent an axis-aligned ellipse outline, the nearest pixel per column where the curve is flat and per row where it is steep.
model: word-ram
complexity:
  vars: {a: the semi-axis along x, b: the semi-axis along y}
  time: {worst: Θ(a + b)}
prereqs: [circle-rasterization]
see_also: [midpoint-ellipse-algorithm, midpoint-circle-algorithm, line-rasterization, integer-square-root, bezier-curve, viewport-transform, antialiasing]
sources:
  - paper: doi:10.1145/130881.130892
    title: M. Douglas McIlroy, Getting raster ellipses right, ACM Transactions on Graphics 11(3), 259 to 275 (1992)
    locator: the whole paper (which pixels a raster ellipse should contain, and the cases near the change from flat to steep)
  - paper: doi:10.1109/MCG.1984.275994
    title: Jerry R. Van Aken, An efficient ellipse-drawing algorithm, IEEE Computer Graphics and Applications 4(9), 24 to 35 (1984)
    locator: the statement of the problem with two regions in each quadrant, split where the slope is -1
  - paper: "M. L. V. Pitteway, Algorithm for drawing ellipses or hyperbolae with a digital plotter, The Computer Journal 10(3), 282 to 289 (1967)"
    locator: conics in general position, given by a quadratic equation, on a plotter that moves in eight directions
  - book: isbn:9780201121100
    title: James D. Foley, Andries van Dam, Steven K. Feiner and John F. Hughes, Computer Graphics, Principles and Practice, second edition, Addison-Wesley, 1990
    locator: Chapter 3, Section 3.4, Scan Converting Ellipses (four-way symmetry and the two regions of a quadrant)
---

Ellipse rasterization asks for the set of pixels that represents an ellipse on a pixel grid. In the usual form the ellipse is axis-aligned, with an integer center and integer semi-axes $a$ and $b$, and the answer in each quadrant is the pixel nearest to the curve in each column where the curve is flat, and in each row where it is steep. The ellipse has only four-way symmetry, so a quadrant has two parts that change at the point where the slope is $-1$, and the choice of pixels near that point is the hard part of the definition. The [midpoint ellipse algorithm](/midpoint-ellipse-algorithm/) is the classic integer solution.

## In plain words

An ellipse is a stretched circle. To draw it on a grid of dots, you light the dots nearest to the curve, one in each column where the curve is flat and one in each row where it is steep.

A circle looks the same across a diagonal, but an ellipse does not, so you must work out a whole quarter and copy it to the other three quarters. The quarter has a flat part and a steep part, and where they meet you must take care that the dots still touch each other and the curve has no gap.

## Definition

The input is a center $(x_c, y_c)$ and semi-axes $a, b \ge 1$, all integers. As for the [circle](/circle-rasterization/), a pixel $(i, j)$ is the point sample $(i, j)$, the center is moved to the origin, and the answer is moved back at the end. The ellipse is

$$\frac{x^2}{a^2} + \frac{y^2}{b^2} = 1.$$

**Nearest pixels.** In the first quadrant, for a column $x$ with $0 \le x \le a$, let $\hat y(x)$ be the integer nearest to $\tfrac{b}{a}(a^2 - x^2)^{1/2}$, the height of the curve in that column; for a row $y$ with $0 \le y \le b$, let $\hat x(y)$ be the integer nearest to $\tfrac{a}{b}(b^2 - y^2)^{1/2}$. The slope of the curve is $-1$ at the point

$$(x^*, y^*) = \left(\frac{a^2}{(a^2 + b^2)^{1/2}},\ \frac{b^2}{(a^2 + b^2)^{1/2}}\right).$$

Region 1 is the arc from $(0, b)$ to $(x^*, y^*)$, where the slope is between 0 and $-1$, and region 2 is the arc from $(x^*, y^*)$ to $(a, 0)$. The answer for a quadrant is a chain of pixels from $(0, b)$ to $(a, 0)$ that has the pixel $(x, \hat y(x))$ in each column of region 1 and the pixel $(\hat x(y), y)$ in each row of region 2, and that is 8-connected. The output is the image of the quadrant under the four maps $(x, y) \mapsto (\pm x, \pm y)$.

**No ties.** A tie in column $x$ would need $4b^2(a^2 - x^2) = a^2 m^2$ for an odd $m$. Then $s = am/(2b)$ is an integer with $x^2 + s^2 = a^2$ and $s > 0$. In a Pythagorean triple the hypotenuse has at most as many factors 2 as each leg, but $2bs = am$ gives $s$ fewer factors 2 than $a$. So no tie occurs in a column, and in the same way none occurs in a row.

**The switch.** Near $(x^*, y^*)$ the rule above leaves a choice, because a column next to $x^*$ or a row next to $y^*$ can belong to either region. Two simple readings of the rule each leave gaps:

- *By the position on the curve:* use the columns $x \le x^*$ and the rows $y \le y^*$. For $a = b = 7$ this gives the columns 0 to 4 and the rows 0 to 4, and a gap between (4, 6) and (6, 4); the [circle](/circle-rasterization/) of radius 7 has the pixel (5, 5) there.
- *By the slope at the pixel:* keep $(x, \hat y(x))$ if $b^2 x \le a^2 \hat y(x)$ and $(\hat x(y), y)$ if $a^2 y \le b^2 \hat x(y)$. For $a = b$ this is the circle, but for $a = 1$, $b = 8$ the row pixel (0, 7) fails its test, and the chain jumps from (0, 8) to (1, 6).

A full definition therefore needs a rule for the pixels near the switch, for example the pixel that closes the gap, or the one nearest to the curve in the Euclidean sense. McIlroy's 1992 paper studies these choices.

The model is the [word RAM](/word-ram/) with integers of about $2\log_2 a + 2\log_2 b$ bits, the size of $a^2 b^2$.

## Variants

- **Rotated ellipses and general conics.** The curve is $A x^2 + B xy + C y^2 + D x + E y + F = 0$. For a rotated ellipse, the four points with a horizontal or a vertical tangent and the four points with a slope of $\pm 1$ are not on the coordinate axes through the center. They split the curve into eight arcs, each drawn per column or per row, and the symmetry is only the half turn about the center. Pitteway's 1967 method treats such conics, including hyperbolas.
- **An ellipse in a bounding box.** User interfaces often give an ellipse by the box of pixels that it fills. A box with an even width or height puts the center between pixels and makes the semi-axes half integers, and then ties can occur and need a rule.
- **Filled ellipses.** The output is the set of pixels with $b^2 x^2 + a^2 y^2 \le a^2 b^2$, or a set that ends at the outline pixels. It is a list of horizontal spans, one per row.
- **Arcs, thick ellipses and antialiased ellipses.** The output is a part of the curve between two angles, the pixels between two ellipses, or pixels with an intensity from the distance to the curve, as in [antialiasing](/antialiasing/).
- **Circles on non-square pixels.** With a pixel aspect ratio other than 1, or with different scales on the two axes in the [viewport transform](/viewport-transform/), a circle in the scene becomes an axis-aligned ellipse in pixels.

## Examples

For $a = 8$ and $b = 5$, the switch point is $(64/\sqrt{89}, 25/\sqrt{89}) \approx (6.78, 2.65)$. Region 1 has the columns 0 to 6, and region 2 the rows 0 to 2.

| part | heights or widths on the curve | pixels |
|---|---|---|
| columns 0 to 6 | 5, 4.96, 4.84, 4.64, 4.33, 3.90, 3.31 | (0, 5), (1, 5), (2, 5), (3, 5), (4, 4), (5, 4), (6, 3) |
| rows 2, 1, 0 | 7.33, 7.84, 8 | (7, 2), (8, 1), (8, 0) |

The quadrant has 10 pixels, and the ellipse has $4 \cdot 10 - 4 = 36$, because the four pixels on the axes are shared. Here both readings of the switch give the same pixels. For $a = b = 4$ they differ: the reading by the slope at the pixel gives the circle of radius 4, with the quadrant (0, 4), (1, 4), (2, 3), (3, 3), (3, 2), (4, 1), (4, 0) and 24 pixels in all, and the reading by the position on the curve drops (3, 3), which leaves 20 pixels in a chain that is still 8-connected.

## Known algorithms

- The [midpoint ellipse algorithm](/midpoint-ellipse-algorithm/) (Van Aken 1984, after Pitteway 1967) walks each region with an integer decision variable at the midpoints between candidate pixels, and changes region when the gradient of the curve at the midpoint passes the diagonal. Near the switch its pixels can differ from the nearest ones.
- McIlroy's 1992 programs are incremental integer methods whose pixels are the ones that his definition asks for, also near the switch.
- The direct method computes $\hat y(x)$ and $\hat x(y)$ with an [integer square root](/integer-square-root/) per column or row.
- A single loop that tests the step in $x$, the step in $y$ and the diagonal step at each pixel needs no switch test; Alois Zingl's 2012 report on the rasterization of curves gives this form.
- A polygon with many sides, drawn by [line rasterization](/line-rasterization/), approximates the curve, and a quarter of an ellipse is a rational quadratic [Bézier curve](/bezier-curve/), so curve renderers that flatten Bézier curves also draw ellipses.

## Bounds

The quadrant has about $x^* + y^* = (a^2 + b^2)^{1/2}$ pixels, so the ellipse has about $4(a^2 + b^2)^{1/2}$ pixels, which is $\Theta(a + b)$, and each algorithm that lists them takes $\Omega(a + b)$ time. The midpoint ellipse algorithm takes $\Theta(a + b)$ time with $O(1)$ operations per pixel and $O(1)$ extra space. A filled ellipse has $\Theta(ab)$ pixels in $2b + 1$ spans.

## Reductions

- **Symmetry.** The four maps $(x, y) \mapsto (\pm x, \pm y)$ reduce the ellipse to one quadrant. The exchange of $x$ and $y$ maps the ellipse with semi-axes $(a, b)$ to the one with $(b, a)$ and region 1 to region 2, so one method for region 1 serves for both.
- **Integer square roots.** The pixel in column $x$ has the row $\hat y(x) = \lfloor (\lfloor (4 b^2 (a^2 - x^2))^{1/2} \rfloor + a) / (2a) \rfloor$, so the direct method needs one [integer square root](/integer-square-root/) per column.
- **Circles.** With $a = b$ the problem is [circle rasterization](/circle-rasterization/). The ellipse is the image of a circle under a scale of one axis, but the pixels of the ellipse are not the scaled pixels of a circle.

## Applications

- User interfaces and drawing programs draw ellipses, ellipse tools and the quarter ellipses at the corners of rounded rectangles.
- Plotting libraries draw elliptical markers and confidence ellipses, and CAD programs show ellipses and elliptical arcs.
- Displays with non-square pixels draw circles as ellipses in pixel units.
- Pen plotters and machines with stepper motors trace ellipses and other conics with steps in eight directions, the use of Pitteway's 1967 method.

## References
