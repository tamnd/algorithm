---
tag: 8RTNZC
kind: problem
slug: table-layout-problem
name: Table layout problem
aliases:
- automatic table layout
area: strings/text-processing-and-typesetting
level: advanced
summary: Choose a layout for each cell of a table, from its possible width and height pairs, to minimize the table height within a given width; NP-complete in this model.
prereqs: [np-complete, partition-problem, polynomial-time-reduction]
see_also: [page-breaking-problem, pagination-np-completeness, knuth-plass-line-breaking, greedy-line-breaking, text-shaping, bin-packing-np-hardness]
sources:
  - paper: doi:10.1145/304893.304937
    title: Richard J. Anderson and Sumeet Sobti, The table layout problem, Proceedings of the Fifteenth Annual Symposium on Computational Geometry, 1999, pages 115 to 123
    locator: the model of cells with minimal configurations, and the NP-completeness of the minimum height layout in a fixed width
  - url: https://drafts.csswg.org/css-tables-3/
    title: CSS Table Module Level 3, W3C
    locator: section 3.5.1, the table-layout property, and section 3.9, Available Width Distribution
---

The table layout problem asks how wide to make each column of a table, and so how to break the text in each cell, to make the table as short as possible within a given width. A cell of text can be set wide and short or narrow and tall, so each cell has a list of possible (width, height) pairs. The width of a column is the widest cell in it and the height of a row is the tallest cell in it, and this coupling of rows and columns makes the problem hard: it is NP-complete in the model of this page. Browsers do not solve it exactly; they use a fast rule that splits the free width among the columns.

## In plain words

A table has rows and columns of boxes with text in them. A box with a lot of text can be wide with few lines, or narrow with many lines.

Each column is as wide as its widest box, and each row is as tall as its tallest box. The whole table must fit in the width of the page, and we want it as short as possible.

Making one column narrower makes its boxes taller, which can make every row that crosses it taller. Because every choice affects both a row and a column, no fast method is known that always finds the best table.

## Definition

**Input.** A table of $r$ rows and $c$ columns. Each cell $(i, j)$ has a finite set $C_{ij}$ of **configurations**, pairs $(w, h)$ of a width and a height, all nonnegative integers. A width $W$.

**Output.** One configuration $(w_{ij}, h_{ij}) \in C_{ij}$ for each cell. The column widths are $c_j = \max_i w_{ij}$, the row heights are $r_i = \max_j h_{ij}$, the table width is $\sum_j c_j$ and the table height is $\sum_i r_i$.

**Objective.** Minimize the table height subject to a table width of at most $W$. The decision form asks, for a bound $H$, whether some choice has width at most $W$ and height at most $H$.

For a cell of text, the configurations come from the line breaks of the text: for each width, the least number of lines, times the height of a line. Only the **minimal** configurations matter, those for which no other configuration is at most as wide and at most as tall.

## Variants

- **Text cells.** The configurations are those of the text in the cell, which is the model of Anderson and Sobti.
- **Spanning cells.** A cell can span several columns or rows; its width must fit in the sum of the column widths it spans.
- **Minimize width or area.** The objective can be the width for a given height, or the area, or a weighted sum.
- **Fixed layout.** In CSS with `table-layout: fixed`, the column widths come from the first row alone, so the layout needs only one pass and no search.
- **Automatic layout in CSS.** With `table-layout: auto`, the initial value, each column gets a minimum width (its min-content width) and a preferred width (its max-content width), and the free width is shared among the columns by fixed rules. This is a heuristic: it is fast, but it does not minimize the height.

## Examples

A table of two rows and two columns with $W = 10$ and the configurations:

| cell | configurations $(w, h)$ |
|---|---|
| (1, 1) | (8, 1), (4, 2) |
| (1, 2) | (6, 1), (3, 2) |
| (2, 1) | (2, 1) |
| (2, 2) | (6, 1), (3, 2), (2, 3) |

The width of column 1 is at least 4, the narrowest choice of cell (1, 1), and the width of column 2 is at least 3. With column widths 4 and 6 (width 10), each cell takes its shortest configuration that fits: the rows have heights 2 and 1, so the table height is 3. With widths 4 and 3 (width 7), the heights are 2 and 2, for a height of 4. Widths 8 and 3 give width 11, which is too wide. So the optimum is height 3.

**The reduction from partition.** Given positive integers $a_1, \ldots, a_n$ with an even sum $S$, build an $n \times n$ table. Let $M = n + 1$. The diagonal cell $(j, j)$ has the two configurations $(M a_j, 1)$, "wide", and $(1, M a_j)$, "tall". Every other cell has the single configuration $(0, 0)$. Set $W = H = M S/2 + n$.

Column $j$ and row $j$ depend only on cell $(j, j)$. If $A$ is the set of the wide cells, the table width is $M \sum_{j \in A} a_j + (n - |A|)$ and the height is $M \sum_{j \notin A} a_j + |A|$.

- If $A$ is a half of a partition, with $\sum_{j \in A} a_j = S/2$, both are at most $M S/2 + n$.
- If the width is at most $MS/2 + n$, then $M \sum_{j \in A} a_j \le MS/2 + n < M (S/2 + 1)$, so $\sum_{j \in A} a_j \le S/2$, since both sides are integers. In the same way the height gives $\sum_{j \notin A} a_j \le S/2$. The two sums add up to $S$, so both are $S/2$.

The numbers have a partition exactly when the table fits in width $W$ and height $H$. The problem is in NP, since a choice of configurations is a certificate, so it is NP-complete. For example, $a = (1, 2, 3)$ gives $M = 4$ and $W = H = 15$: making only cell 3 wide gives width $12 + 2 = 14$ and height $12 + 1 = 13$, while making cells 1 and 3 wide gives width $16 + 1 = 17 > 15$.

## Known algorithms

- **Brute force over the column widths.** In an optimal layout each column width is the width of one of the configurations in that column. So try every vector of such widths with sum at most $W$; for each, give each cell its shortest configuration that fits in its column, and add up the row heights. This is exact, and it takes time about $\prod_j s_j$ times the number of configurations, where $s_j$ is the number of distinct widths in column $j$.
- **One row.** The table height is the tallest cell. For a bound $t$ on the height, each cell takes its narrowest configuration with height at most $t$, and the bound is feasible when these widths sum to at most $W$. A binary search over the candidate heights gives the optimum in $O(N \log N)$ time for $N$ configurations.
- **One column.** Each cell takes its shortest configuration of width at most $W$, in $O(N)$ time.
- **Heuristics.** The automatic layout of CSS shares the free width by the min-content and max-content widths of the columns. For small tables, an integer program with one 0-1 variable per configuration also gives the exact optimum.

## Bounds

- The decision problem is NP-complete in the model of this page, by the reduction above from [partition](/partition-problem/). The numbers of the reduction grow with the input numbers, so this proof gives NP-hardness in the weak sense only.
- Anderson and Sobti show that the minimum height layout within a fixed width is NP-complete for tables whose cells are given by their minimal configurations.
- For a fixed number of columns with few widths each, the brute force is polynomial.

## Reductions

- Partition reduces to table layout, as above, with one cell per number on the diagonal.
- Each cell of text is a small line breaking problem: its configurations come from breaking its text at each width, for example with [greedy line breaking](/greedy-line-breaking/) or [Knuth-Plass line breaking](/knuth-plass-line-breaking/), after [text shaping](/text-shaping/) has given the widths of the words.
- Like [pagination with figures](/pagination-np-completeness/), table layout is hard because it packs items with two coupled sizes, as in [bin packing](/bin-packing-np-hardness/).

## Applications

- Web browsers lay out HTML tables with the automatic layout of CSS.
- Word processors and typesetting systems set the column widths of tables, either from the author or by a heuristic.
- Spreadsheets and data viewers fit columns of data on a screen or a page.

## References
