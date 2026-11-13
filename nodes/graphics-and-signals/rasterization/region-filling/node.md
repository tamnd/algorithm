---
tag: TETMXJ
kind: problem
slug: region-filling
name: Region filling
area: graphics-and-signals/rasterization
level: intro
summary: Recolor the connected region of pixels that holds a seed pixel, where the region is given by its color or by a boundary color, under 4 or 8 connectivity.
model: word-ram
complexity:
  vars: {k: the number of pixels in the region}
  time: {worst: Θ(k)}
prereqs: [pixel, graph-reachability]
see_also: [flood-fill, connected-component-labeling, polygon-scan-conversion, scanline-polygon-fill, implicit-graph, depth-first-search, breadth-first-search, jordan-curve-theorem]
sources:
  - paper: doi:10.1145/800249.807456
    title: Alvy Ray Smith, Tint fill, Proceedings of the 6th Annual Conference on Computer Graphics and Interactive Techniques (SIGGRAPH 1979), 276 to 283
    locator: the whole paper (fill of a region of pixels from a seed, by horizontal spans)
  - paper: doi:10.1016/b978-0-08-050753-8.50058-9
    title: Paul S. Heckbert, A seed fill algorithm, in Graphics Gems, Academic Press (1990), 275 to 277
    locator: the whole article (a span seed fill with an explicit stack)
  - book: isbn:9780201121100
    title: James D. Foley, Andries van Dam, Steven K. Feiner and John F. Hughes, Computer Graphics, Principles and Practice, second edition, Addison-Wesley, 1990
    locator: Section 19.5, Filling Algorithms (boundary-defined and interior-defined regions, 4-connected and 8-connected fill)
  - paper: "Azriel Rosenfeld, Connectivity in digital pictures, Journal of the ACM 17(1), 1970"
    locator: the pairing of 4-connectivity with 8-connectivity for regions and their boundaries
---

Region filling asks to recolor a region of a raster image that is given by its pixels, not by a shape: the region is the set of pixels that are connected to a seed pixel and pass a color test. In the interior-defined form the region is the pixels with the color of the seed, and in the boundary-defined form it is the pixels that do not have a given boundary color. Connectivity is 4 (sides only) or 8 (sides and corners), and the choice changes which regions leak into each other. It is the problem of the paint bucket tool, and the main method is [flood fill](/flood-fill/) in its stack or span forms.

## In plain words

You have a picture made of colored squares and you click on one square. All squares of the same color that you can reach from it, step by step, get the new color. You stop at squares of other colors.

A step can go only up, down, left or right, or it can also go across a corner. With corner steps, the paint can slip through a thin diagonal line, so a closed outline must be thicker to hold it.

In a second form of the task you give the color of the outline. The paint spreads over every square that is not the outline color, whatever color it had, until it meets the outline.

## Definition

The image is a $W$ by $H$ array of colors $I(i, j)$, one for each pixel. Here a pixel is an element of the array, a cell of the grid, and the problem never looks at points inside a pixel. Two pixels are **4-adjacent** when they differ by one in one coordinate, and **8-adjacent** when they differ by at most one in each coordinate and are not equal. A set of pixels is **connected** under an adjacency when any two of its pixels are joined by a path of adjacent pixels in the set.

The input is the image, a seed pixel $s$, a new color $c$, a choice of adjacency, and a test:

- **Interior-defined (flood fill).** The candidates are the pixels with $I(p) = I(s)$.
- **Boundary-defined (boundary fill).** Given a boundary color $b$ with $I(s) \ne b$, the candidates are the pixels with $I(p) \ne b$.

The **region** $R$ is the connected component of $s$ in the set of candidates, under the chosen adjacency. The output is the image with $I(p) = c$ for each $p \in R$ and no other change. In words of graphs, $R$ is the set of vertices that are reachable from $s$ in the [implicit graph](/implicit-graph/) whose vertices are the candidate pixels and whose edges join adjacent candidates, so the problem is a case of [graph reachability](/graph-reachability/).

All tests are equality tests on stored colors, so the problem is exact and has no floating-point issue. A variant that accepts colors within a tolerance of the seed color needs a fixed distance, and its result depends on that distance.

## Variants

- **4 or 8 connectivity.** A 4-connected fill stops at a boundary that is only 8-connected, such as a line drawn with diagonal steps by the [Bresenham line algorithm](/bresenham-line-algorithm/). An 8-connected fill leaks through such a line, and it needs a 4-connected boundary. This pairing of the two adjacencies is the basis of the digital form of the [Jordan curve theorem](/jordan-curve-theorem/).
- **Interior or boundary.** A flood fill stops at every color that differs from the seed color. A boundary fill paints over all colors except the boundary color, so it also paints over text and small shapes inside the region.
- **Tolerance.** Paint programs often accept colors close to the seed color, with a tolerance that the user sets.
- **Soft fill.** The tint fill of Smith recolors a region drawn with antialiased edges, where pixels on the edge are a mix of the region color and the background, and it keeps the mix.
- **Labeling all regions.** [Connected component labeling](/connected-component-labeling/) gives a label to every region of the image at once, not only to the region of one seed.

## Examples

Take this 7 by 7 image, with `#` for the boundary color and `.` for the background, and the seed at the center pixel $(3, 3)$. The boundary is a diamond drawn with diagonal steps, so it is 8-connected and not 4-connected.

```text
...#...
..#.#..
.#...#.
#.....#
.#...#.
..#.#..
...#...
```

- A **4-connected** fill recolors the 13 pixels inside the diamond. A step from the inside to the outside would have to cross a corner between two `#` pixels.
- An **8-connected** fill leaks: from $(2, 2)$ it steps across the corner to $(1, 1)$, which is outside. It recolors all 37 background pixels of the image, inside and outside.
- With a red pixel at $(4, 4)$ inside the diamond, a 4-connected flood fill from $(3, 3)$ skips it, since its color differs from the seed, and recolors 12 pixels. A boundary fill with $b = \texttt{\#}$ paints it too and recolors 13.
- If the new color $c$ equals the seed color, the flood fill changes nothing. A boundary fill with $c = b$ makes the region part of the boundary.

## Known algorithms

- [Flood fill](/flood-fill/) visits the region by [depth-first search](/depth-first-search/) or [breadth-first search](/breadth-first-search/) on the grid, in $\Theta(k)$ time for a region of $k$ pixels. A version with an explicit stack or queue avoids the deep recursion of the simple recursive form, which can reach a depth of $k$.
- The span seed fill fills a whole horizontal run of the region at once and pushes one seed for each run above and below it that it has not yet filled. Smith described the method in 1979, and Heckbert gave a compact version with an explicit stack in 1990. It still takes $O(k)$ time, and on most images it keeps far fewer entries on the stack than the pixel by pixel fill.
- [Connected component labeling](/connected-component-labeling/) with a union-find pass labels all regions at once, after which any region can be recolored by its label.

These algorithms belong to the page of flood fill and to graph traversal. This page states only the problem and its forms.

## Bounds

Each pixel of the region must be written, so every algorithm needs $\Omega(k)$ time, and flood fill meets this bound with $O(k)$ time. The test of a pixel and its neighbors takes $O(1)$ time with 4 or 8 neighbors. The extra space of a stack or queue of pixels is $O(k)$ in the worst case. The span method stores runs in place of pixels, which is much less on most images but still grows with the region in the worst case.

## Reductions

- Region filling is single-source reachability in the implicit grid graph of the candidate pixels, so any graph search solves it.
- A boundary fill reduces to a flood fill on a mask: in a copy of the image, mark all pixels that are not of color $b$ with one temporary color, flood fill the copy from the seed, and give the new color in the image only to the pixels that this fill reached.
- It differs from [polygon scan conversion](/polygon-scan-conversion/): there the input is a geometric polygon and the result depends on a fill rule at pixel centers, and here the input is a set of pixels and the result depends on adjacency. A polygon drawn by its outline and then filled by region filling can differ from its scan conversion along thin parts and where the outline touches itself.
- It also differs from [point in polygon](/point-in-polygon/) in geometry, which tests one point against exact edges and knows nothing of pixels.

## Applications

- The paint bucket tool of image editors, and the coloring of drawn outlines in animation and comics.
- Selection by color ("magic wand"), the removal of a background, and the cleanup of scanned pages.
- Games: the reveal of empty cells in Minesweeper and the count of territory in Go.
- The labeling of cells, particles or rooms in binary images and maps.

## References
