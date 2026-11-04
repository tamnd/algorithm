---
tag: JB2BYD
kind: technique
slug: dsu-with-distances-to-representative
name: Union-find with distances to the representative
aliases:
- Support distances to the representative
area: data-structures/disjoint-sets
level: core
summary: Extends union-find to store each node's distance to its set representative, updated during path compression, to answer distance queries.
prereqs: [disjoint-set-forest, path-compression]
see_also: [weighted-union-find, dsu-with-parity, path-compression, path-halving, union-by-size, difference-constraints]
sources:
  - url: https://cp-algorithms.com/data_structures/disjoint_set_union.html
    title: cp-algorithms, Disjoint Set Union
    locator: the section Support distances up to representative, and the section Support the parity of the path length
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 19.3, Disjoint-set forests (the recursive FIND-SET with path compression that this technique extends)
---

Union-find with distances to the representative is a way to keep a number on each edge of a [disjoint-set forest](/disjoint-set-forest/), so that each element knows its *distance* to the root of its tree: the sum of the numbers on its path. A find returns the root and this distance. [Path compression](/path-compression/) still works if each new edge gets the sum of the edges it replaces, and the union sets the number on the new edge from the two distances that the union must respect. The cost stays that of the plain forest. The technique answers queries such as "how far is $x$ above the bottom of its stack" or "what is $x - y$", and the general form for any group is [weighted union-find](/weighted-union-find/).

## In plain words

Each item points to a boss, as in ordinary union-find, and it also writes down a number: how far it is from its boss. The distance from an item to the leader is the sum of the numbers along its chain of bosses.

When you find the leader of an item, you add up the numbers on the way. When you then make the item point straight at the leader, you write the whole sum as its new number, so nothing is lost.

When two groups join, one leader gets a boss. You choose its number so that every distance the problem promises is still true. After that, each item of the moved group gets the new number added to its distance without any extra work, because it reaches the old leader first.

## When it applies

- **Elements carry values relative to each other.** The facts are of the form "$x$ is $d$ above $y$", "$x - y = d$", or "stack $A$ goes on top of stack $B$". The queries ask for such a relation between two elements of one group.
- **The relation is additive along paths.** The value from $x$ to $z$ is the value from $x$ to $y$ plus the value from $y$ to $z$. Any group works in the same way; integers with addition and bits with exclusive or are the common cases.
- **Groups only merge.** Like plain union-find, the technique does not split groups.

## The template

Each element $x$ has a parent $x.p$ and a number $x.d$, the distance from $x$ to $x.p$. A root has $r.d = 0$, and $\mathrm{dist}(x)$ is the sum of $d$ along the path from $x$ to its root.

```pseudo id=main
FIND(x)                                   ▷ returns (root, dist(x)) and compresses
L1  if x.p = x then return (x, 0)
L2  (r, e) ← FIND(x.p)                    ▷ e = dist(x.p)
L3  x.d ← x.d + e                         ▷ x.d becomes dist(x)
L4  x.p ← r
L5  return (r, x.d)

UNION(a, b)                               ▷ make the promised relation between a and b true
L6  (ra, da) ← FIND(a); (rb, db) ← FIND(b)
L7  if ra = rb then return ⟨CHECK⟩(da, db) ▷ hole: is the promise consistent?
L8  ra.p ← rb
L9  ra.d ← ⟨LINK-VALUE⟩(da, db)           ▷ hole: the distance from ra to rb
```

Lines L1 to L5 are the recursive find of the [disjoint-set forest](/disjoint-set-forest/), with one more line. After the recursive call, $x.p$ points to the root with $x.p.d = e = \mathrm{dist}(x.p)$, so line L3 makes $x.d = \mathrm{dist}(x)$, and line L4 can point $x$ to the root without changing $\mathrm{dist}(x)$.

Line L8 links root $ra$ under root $rb$. Each element $z$ of the tree of $ra$ now has $\mathrm{dist}(z) = (\text{old dist}(z)) + ra.d$, so line L9 must choose $ra.d$ to make the promise true. For the promise "$\mathrm{dist}(a) - \mathrm{dist}(b) = w$", the new distances are $da + ra.d$ and $db$, so ⟨LINK-VALUE⟩ is $w + db - da$. The hole ⟨CHECK⟩ is used when $a$ and $b$ are already in one tree: then the promise holds exactly when $da - db = w$.

**Linking rule.** Line L8 can put either root under the other, with the opposite value $-ra.d$ in the other direction, so [union by size](/union-by-size/) or [by rank](/union-by-rank/) works. Some problems fix the direction, for example to keep the bottom of a stack as the root, and then only path compression applies.

**Cost.** Each find and union does $O(1)$ extra work per step of the plain operation. With union by rank or size and compression, $m$ operations take $O(m\,\alpha(n))$ time, and each find recurses to depth $O(\log n)$.

## Classic examples

### Stacks of cubes

Cubes $0$ to $5$ start as six stacks of one. The operation move$(x, y)$ puts the whole stack of $x$ on top of the whole stack of $y$, and below$(x)$ asks how many cubes are under $x$. Let the root of each tree be the bottom cube, let $\mathrm{dist}(x)$ be below$(x)$, and keep size$(r)$ at each root. A move links the root of $x$ under the root of $y$ with ⟨LINK-VALUE⟩ $=$ size of the stack of $y$, because each cube of the moved stack now has that many more cubes under it. The direction is fixed, so there is no linking rule.

| operation | change | parents of 0 to 4 | d of 0 to 4 | answer |
|---|---|---|---|---|
| move(0, 1) | 0.p ← 1, 0.d ← 1 | 1 1 2 3 4 | 1 0 0 0 0 | |
| move(2, 3) | 2.p ← 3, 2.d ← 1 | 1 1 3 3 4 | 1 0 1 0 0 | |
| move(0, 3) | 1.p ← 3, 1.d ← 2 | 1 3 3 3 4 | 1 2 1 0 0 | |
| below(0) | path 0, 1, 3; 0.d ← 1 + 2 | 3 3 3 3 4 | 3 2 1 0 0 | 3 |
| move(4, 0) | 4.p ← 3, 4.d ← 4 | 3 3 3 3 3 | 3 2 1 0 4 | |
| below(4) | | | | 4 |

The stack is now, from the bottom, $3, 2, 1, 0, 4$, and the distances are the positions.

### Where it is used

- **[Union-find with parity](/dsu-with-parity/).** The numbers are bits and the sum is exclusive or. It checks whether a graph is [bipartite](/bipartite-graph/) while edges arrive.
- **[Weighted union-find](/weighted-union-find/).** The numbers are elements of any group, for relations like $x - y = w$ or $x / y = w$.
- **Equations $x_a - x_b = w$.** The template with ⟨CHECK⟩ tests whether a list of such equations has a solution, and gives the value of each difference that the equations fix. With inequalities instead of equations, the problem is a system of [difference constraints](/difference-constraints/), which needs shortest paths.

## Variations

- **Iterative find.** The recursion of line L2 has depth at most $\lfloor \lg n \rfloor$ with a linking rule. Without one, use [path halving](/path-halving/) with the update $x.d \leftarrow x.d + x.p.d$ before each skip, or a loop that collects the path and then sets the distances from the top down.
- **The root keeps a value.** If the moved group needs a value that depends on the root, such as a size, keep it at the root and update it in the union, as the stack example does with size.
- **Other groups.** Replace $+$ by the group operation and $-$ by the inverse. The order of the operands matters when the group is not commutative.

## Pitfalls

- **Linking elements, not roots.** Line L8 must link the roots $ra$ and $rb$ that line L6 found, and line L9 must use $da$ and $db$. Setting $a.p \leftarrow b$ breaks the distances of the rest of the tree of $a$.
- **Compression that drops the sum.** Line L4 without line L3 points $x$ to the root but keeps the distance to the old parent, so later queries are wrong. Line L3 must run before line L4.
- **Using a stale distance.** The value $da$ of line L6 is the distance before the link. After line L8 the distances in the tree of $ra$ have changed; read them with a new find.
- **A non-zero root value.** The template assumes $r.d = 0$ at each root, so the root returned by line L1 contributes nothing. A union that writes $r.d$ must also make $r$ a non-root.

## Exercises

1. Write the iterative find with path halving for this template, and show that it computes the same distances.
2. Use the template to test whether the equations $x_0 - x_1 = 3$, $x_1 - x_2 = -1$, $x_2 - x_0 = -2$ and $x_3 - x_2 = 5$ have a solution, and give $x_3 - x_0$.
3. Change the stack example so that it can use union by size: the bottom of a stack is no longer the root.

## References
