---
tag: 7M87RK
kind: definition
slug: assortativity
name: Assortativity
aliases:
- degree assortativity
- assortative mixing
area: graphs/network-analysis
level: advanced
summary: Tendency of nodes to connect to nodes with similar degree.
prereqs: [degree, degree-distribution, variance]
see_also: [degree-distribution, homophily, modularity, rich-club-coefficient, configuration-model, scale-free-network, core-periphery-structure, degree]
sources:
  - paper: doi:10.1103/PhysRevLett.89.208701
    title: M. E. J. Newman, Assortative mixing in networks, Physical Review Letters 89(20), 208701 (2002)
    locator: the whole paper (the coefficient r as the Pearson correlation of the remaining degrees at the two ends of an edge, the edge-sum formula, and the signs of r for social, technological and biological networks)
  - paper: doi:10.1103/PhysRevE.67.026126
    title: M. E. J. Newman, Mixing patterns in networks, Physical Review E 67(2), 026126 (2003)
    locator: Section II (assortative mixing by a discrete attribute, the matrix e and the coefficient r) and Section IV (mixing by a scalar attribute, and the directed case)
  - book: isbn:9780199206650
    title: M. E. J. Newman, Networks, An Introduction, Oxford University Press, 2010
    locator: Chapter 7, Section 7.13 (homophily and assortative mixing, for enumerative and scalar characteristics, and by degree)
  - paper: doi:10.1103/PhysRevE.87.022801
    title: Nelly Litvak and Remco van der Hofstad, Uncovering disassortativity in large scale-free networks, Physical Review E 87(2), 022801 (2013)
    locator: the whole paper (the behaviour of r for heavy-tailed degrees as the graph grows, and a rank correlation as a replacement)
---

**Assortativity** is the tendency of the [vertices](/vertex/) of a network to be joined to vertices that are like them. By [degree](/degree/), a network is assortative when high-degree vertices tend to link to high-degree vertices, and disassortative when hubs tend to link to low-degree vertices. Newman measured it in 2002 by the assortativity coefficient $r$, the correlation between the degrees at the two ends of an edge. Social networks usually have $r > 0$, while technological and biological networks, such as the Internet and protein interaction networks, usually have $r < 0$. The [degree distribution](/degree-distribution/) alone does not determine $r$.

## Definition

Let $G = (V, E)$ be an undirected simple graph with $M \ge 1$ edges, and let $\deg(x)$ be the degree of $x$. Write the edges as $\{x_i, y_i\}$ for $i = 1, \ldots, M$, and let $j_i = \deg(x_i)$, $k_i = \deg(y_i)$. The **degree assortativity coefficient** is

$$r = \frac{\frac{1}{M} \sum_i j_i k_i - \Bigl(\frac{1}{M} \sum_i \tfrac12 (j_i + k_i)\Bigr)^2}{\frac{1}{M} \sum_i \tfrac12 (j_i^2 + k_i^2) - \Bigl(\frac{1}{M} \sum_i \tfrac12 (j_i + k_i)\Bigr)^2}.$$

Equivalently, list each edge in both directions, which gives $2M$ ordered pairs $(x, y)$, and take the Pearson correlation of $\deg(x)$ and $\deg(y)$ over these pairs. The two coordinates have the same distribution, so the numerator is their covariance and the denominator their common [variance](/variance/). So $-1 \le r \le 1$. The network is called **assortative** if $r > 0$, **disassortative** if $r < 0$, and **neutral** if $r = 0$.

Some points of the definition:

- **Remaining degree.** Newman uses the remaining degree $\deg(x) - 1$, the number of other edges at an end. Subtracting 1 from every value does not change a correlation, so $r$ is the same.
- **Undefined case.** The denominator is 0 exactly when all ends of all edges have the same degree, that is, when all non-isolated vertices have one common degree, as in a regular graph. Then $r$ is not defined.
- **Disconnected graphs.** The sums run over all edges of all components, and isolated vertices do not contribute. So $r$ of a disjoint union is not an average of the values of the parts; it can be large even if each part has $r$ undefined.
- **Directed graphs.** For an arc $(x, y)$, correlate the out-degree of $x$ with the in-degree of $y$ over the $M$ arcs; the two variances in the denominator now differ, and the denominator is the product of the two standard deviations. The other three pairings (in-in, out-out, in-out) are also used.
- **Weights.** The standard coefficient ignores weights. A weighted version counts each edge with its weight in all the averages.

**Mixing by an attribute.** If each vertex has a type from a finite set, let $e_{ab}$ be the fraction of the $2M$ ordered pairs whose ends have the types $a$ and $b$, and $a_a = \sum_b e_{ab}$. Newman's coefficient for this case is

$$r = \frac{\sum_a e_{aa} - \sum_a a_a^2}{1 - \sum_a a_a^2},$$

which is 1 when all edges join vertices of the same type and 0 when the types of the two ends are independent. Its numerator is the [modularity](/modularity/) of the partition by type, so $r$ is the modularity divided by its largest possible value for these $a_a$.

## Examples and non-examples

Let $G_7$ be the graph with the vertices 0 to 6 and the edges $\{0,1\}$, $\{0,2\}$, $\{1,2\}$, $\{1,3\}$, $\{2,3\}$, $\{3,4\}$, $\{4,5\}$, $\{4,6\}$, $\{5,6\}$, with the degrees $2, 3, 3, 3, 3, 2, 2$. The degree pairs of the 9 edges are $(2,3), (2,3), (3,3), (3,3), (3,3), (3,3), (3,2), (3,2), (2,2)$. Then $\frac1M \sum j_i k_i = 64/9$, the mean end degree is $\frac{1}{18} \cdot 48 = 8/3$, and its square is also $64/9$. So $r = 0$: $G_7$ is exactly neutral, although its degrees vary.

- **Star.** In the star with one centre and 4 leaves, every edge joins degree 4 to degree 1. The mean end degree is $5/2$, $\frac1M \sum j_i k_i = 4$ and $\frac1M \sum \frac12(j_i^2 + k_i^2) = 17/2$, so $r = (4 - 25/4)/(17/2 - 25/4) = -1$. Every star is perfectly disassortative.
- **Paths.** The path with 4 vertices has $r = -1/2$, and the path with 5 vertices has $r = -1/3$; the two ends of degree 1 attach to vertices of degree 2.
- **Two hubs.** Two vertices of degree 4 joined by an edge, each with 3 leaves, give $r = -3/4$: the one edge between the hubs is not enough to offset the six edges from hub to leaf.
- **A disjoint union.** The union of $K_4$ and a single edge $K_2$ has $r = 1$: every edge joins equal degrees, 3 with 3 or 1 with 1, and the degrees do vary. Each part alone is regular, with $r$ undefined.
- **A tail.** $K_4$ on $\{0, 1, 2, 3\}$ with the path $3, 4, 5, 6$ attached has $r = 17/53 \approx 0.32$.
- **Not defined.** A cycle, a complete graph, or any other regular graph has all end degrees equal, so the denominator is 0 and $r$ is not defined.
- **Attribute mixing.** In $G_7$ with the types $A$ for $\{0, 1, 2, 3\}$ and $B$ for $\{4, 5, 6\}$, the edge fractions are $e_{AA} = 5/9$, $e_{BB} = 3/9$ and $e_{AB} = e_{BA} = 1/18$, so $a_A = 11/18$, $a_B = 7/18$, and $r = (16/18 - 170/324)/(1 - 170/324) = 59/77 \approx 0.77$. The numerator $59/162$ is the modularity of this partition.

Assortativity is not a property of the degree sequence: the same degrees can be wired with different $r$. Rewiring two edges $\{a, b\}$, $\{c, d\}$ into $\{a, c\}$, $\{b, d\}$ keeps every degree, and choosing which swaps to accept moves $r$ up or down. The [configuration model](/configuration-model/) gives $r$ close to 0 for large graphs with light-tailed degrees, which is why $r$ is compared with that null model.

## Related definitions

- [Homophily](/homophily/): the social tendency to link with similar people, of which assortative mixing by an attribute is the measured form.
- [Modularity](/modularity/): the numerator of the attribute coefficient, used to score partitions into communities.
- [Rich-club coefficient](/rich-club-coefficient/): the density among the vertices of highest degree, a different view of how hubs connect to each other.
- [Core-periphery structure](/core-periphery-structure/): a dense core joined to a sparse periphery; its effect on $r$ depends on whether the high-degree vertices link mostly to each other or mostly to the periphery.
- Rank versions: for heavy-tailed degrees, Litvak and van der Hofstad show that $r$ of large disassortative networks is pulled towards 0, and suggest a rank correlation, as with Spearman's coefficient, in its place.

## References
