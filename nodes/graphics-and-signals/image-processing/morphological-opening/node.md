---
tag: 97EJK2
kind: algorithm
slug: morphological-opening
name: Morphological opening
aliases:
- opening
area: graphics-and-signals/image-processing
level: intro
summary: Erosion followed by dilation with the same element. It removes the foreground parts where the element does not fit and keeps the rest unchanged.
solves: [morphological-filtering]
model: word-ram
complexity:
  vars: {W: image width in pixels, H: image height in pixels, k: the number of offsets in the structuring element}
  time: {worst: Θ(W H k)}
  space: {extra: Θ(W H)}
properties: {deterministic: true, recursive: false, in_place: false, exact: true, linear: false, idempotent: true}
prereqs: [morphological-erosion, morphological-dilation, structuring-element]
see_also: [morphological-closing, morphological-filtering, mathematical-morphology, image-noise, median-filter, image-thresholding, connected-component-labeling]
sources:
  - book: isbn:9783540429883
    title: Pierre Soille, Morphological Image Analysis, Principles and Applications, second edition, Springer, 2003
    locator: Chapter 4, Opening and Closing (the definitions, the algebraic properties, the top-hats and the granulometries)
  - book: isbn:9780126372403
    title: Jean Serra, Image Analysis and Mathematical Morphology, Academic Press, 1982
    locator: Chapter II, The hit or miss transformation, erosion and opening
  - book: isbn:9780133356724
    title: Rafael C. Gonzalez and Richard E. Woods, Digital Image Processing, fourth edition, Pearson, 2018
    locator: Chapter 9, Morphological Image Processing (the section on opening and closing, and the gray scale section with the top-hat)
  - paper: doi:10.1109/TPAMI.1987.4767941
    title: Robert M. Haralick, Stanley R. Sternberg and Xinhua Zhuang, Image analysis using mathematical morphology, IEEE Transactions on Pattern Analysis and Machine Intelligence 9(4), 532 to 550, 1987
    locator: the sections on opening and closing
---

Morphological opening is [erosion](/morphological-erosion/) followed by [dilation](/morphological-dilation/) with the same [structuring element](/structuring-element/) $B$: $X \circ B = (X \ominus B) \oplus B$. For a binary image it is the union of all the translates of $B$ that fit inside the foreground, so it removes the parts where $B$ does not fit (specks, thin bridges, sharp corners) and keeps the rest exactly. On a gray image it cuts down bright peaks narrower than $B$. Opening is increasing, anti-extensive and idempotent, which makes it the basic morphological filter. The cost is that of the two steps, $\Theta(WHk)$ for a $W \times H$ image and $k$ offsets by the direct method.

## In plain words

Take a stamp, for example a small disk. Slide it everywhere inside the white part of a black and white picture, without letting it touch black. Keep white every pixel that the stamp can cover, and make black every white pixel that the stamp can never reach.

White dots smaller than the stamp vanish, thin white lines vanish, and narrow necks between white regions break. Large white regions keep their size, but their sharp corners get rounded to the shape of the stamp. If you do it a second time, nothing more changes.

On a gray picture, bright details narrower than the stamp are cut down to the level around them. Dark details stay.

## The problem

The input is an image $f$ with $W$ columns and $H$ rows of integer values in $\{0, \dots, \top\}$, pixel centers at the integer points, binary or gray, and a finite structuring element $B \subset \mathbb{Z}^2$ of offsets. The output is

$$\gamma_B(f) = (f \ominus B) \oplus B, \qquad (f \ominus B)(z) = \min_{b \in B} f(z + b), \quad (g \oplus B)(p) = \max_{b \in B} g(p - b),$$

where both steps ignore the pixels outside the image (the minimum over an empty set is $\top$ and the maximum is 0). For a binary image with foreground $X$,

$$X \circ B = \bigcup \{B_z : B_z \subseteq X\},$$

the union of the translates $B_z = \{z + b : b \in B\}$ that fit inside $X$. On a finite image, with the outside ignored, the translates are cut to the image and $z$ runs over the pixels. On a gray image $\gamma_B(f)(p)$ is the largest value $t$ such that some translate of $B$ that covers $p$ has $f \ge t$ on all of it. This is the "rolling ball" picture: push a flat stamp up under the graph of $f$ as far as it goes, and keep the highest level that the stamp reaches at each pixel.

## The algorithm

```pseudo id=main
OPEN(f, W, H, B)                         ▷ both steps ignore the outside
L1  set e[p] ← ⊤ for every pixel p
L2  for each offset b in B do
L3      for each pixel p with p + b in the image do e[p] ← min(e[p], f[p + b])
L4  set g[p] ← 0 for every pixel p
L5  for each offset b in B do
L6      for each pixel p with p − b in the image do g[p] ← max(g[p], e[p − b])
L7  return g
```

Lines L1 to L3 are the erosion: $e(z)$ is the minimum of $f$ over the translate $B_z$, so $e(z) = 1$ on a binary image when $B_z$ fits. Lines L4 to L6 are the dilation: the pixel $p$ takes the largest $e(z)$ over the translates $B_z$ that cover it, since $p - b = z$ means $p = z + b \in B_z$. The two steps must use the same element and must not be fused into one pass, because $g$ at $p$ needs $e$ at every $z$ with $p \in B_z$.

## Example

Take the 8 by 5 image $X$ of the [erosion](/morphological-erosion/) page: a 4 by 3 block with a bump at $(5, 2)$ and an isolated pixel at $(7, 2)$.

```text
X                   X opened by the square     X opened by the cross
. . . . . . . .     . . . . . . . .            . . . . . . . .
. # # # # . . .     . # # # # . . .            . . # # # . . .
. # # # # # . #     . # # # # . . .            . # # # # # . .
. # # # # . . .     . # # # # . . .            . . # # # . . .
. . . . . . . .     . . . . . . . .            . . . . . . . .
```

The 3 by 3 square fits at the two centers $(2, 2)$ and $(3, 2)$, and their two translates cover the whole block, so the opening gives back the 12 pixels of the block exactly. The bump and the isolated pixel go, since no square that holds them fits. With the 5-pixel cross the erosion keeps $(2, 2)$, $(3, 2)$ and $(4, 2)$. The three crosses cover 11 pixels. They keep the bump, which the cross centered at $(4, 2)$ reaches. They lose the two left corners $(1, 1)$ and $(1, 3)$ of the block, which no cross inside $X$ reaches; the cross at $(4, 2)$ reaches the right corners.

On a gray row with the segment $\{-1, 0, 1\}$:

| $x$ | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|---|---|---|---|---|---|---|---|---|---|
| $f$ | 5 | 3 | 8 | 8 | 2 | 7 | 7 | 7 | 6 |
| erosion | 3 | 3 | 3 | 2 | 2 | 2 | 7 | 6 | 6 |
| opening | 3 | 3 | 3 | 3 | 2 | 7 | 7 | 7 | 6 |

The plateau 8, 8 is two pixels wide, narrower than the segment, and it is cut down to 3. The plateau 7, 7, 7 is three pixels wide and stays. The peak 5 at the left end goes to 3. Dark values never rise: the opening is below $f$ at every pixel.

## Correctness

The proof below shows that OPEN returns, at each pixel $p$, the maximum over the cut translates $T$ of $B$ that hold $p$ of the minimum of $f$ on $T$. From that form alone the three properties follow. It is increasing, because each minimum grows with $f$. It is anti-extensive, because a minimum over a set that holds $p$ is at most $f(p)$. It is idempotent: if $T$ gives the value $g(p)$, then every pixel of $T$ is at least $g(p)$ in the output, so $T$ gives the same value again in a second opening. The proof does not need the origin in $B$.

## Complexity

- **Time.** Two passes of $k$ offsets over $WH$ pixels: $\Theta(WHk)$ in the word-RAM model, in every case.
- **Space.** The intermediate erosion $e$ and the output $g$: $\Theta(WH)$ extra.
- **Fast elements.** Every speedup of erosion and dilation applies to both steps. For a rectangle, two passes of a constant time moving minimum and two of a moving maximum, as on the page [sliding window maximum](/sliding-window-maximum/), give $\Theta(WH)$ for any size. For a binary disk, threshold the Euclidean [distance transform](/distance-transform/) of the background to get the erosion, then threshold the distance transform of the eroded set to get the dilation: $\Theta(WH)$ for any radius.
- **Packed bits.** On a binary image with $w$ pixels in a word, $O(WHk/w)$ word operations.

## Properties

- **Idempotent.** $\gamma_B(\gamma_B(f)) = \gamma_B(f)$.
- **Anti-extensive.** $\gamma_B(f) \le f$, for every $B$.
- **Increasing.** $f_1 \le f_2$ implies $\gamma_B(f_1) \le \gamma_B(f_2)$. An operator with these three properties is an algebraic opening.
- **Duality.** $\gamma_B(f)$ is the complement of the [closing](/morphological-closing/) of the complement by the reflected element: $(X \circ B)^c = X^c \bullet \check B$.
- **Independent of the origin of $B$.** On the whole plane $X \circ B_z = X \circ B$ for every $z$: the opening depends on the shape of $B$, not on where its origin is. The erosion and the dilation each shift, and the two shifts cancel.
- **Sieving.** On the whole plane, if $B = A \oplus C$ (for example a 5 by 5 square and a 3 by 3 square), then $X \circ B \subseteq X \circ A$ and $(X \circ A) \circ B = (X \circ B) \circ A = X \circ B$. A family of openings by growing elements is a granulometry: the area that each size removes measures the size distribution of the objects.
- **Fixed points.** The opening keeps a set exactly if and only if the set is a union of translates of $B$. A square region is kept by a square element, but a disk loses pixels at the rim under a square element.

## Variants and improvements

- **Top-hat.** The white top-hat $f - \gamma_B(f)$ keeps the bright details narrower than $B$ and removes the slowly varying background. It is the standard step before [thresholding](/image-thresholding/) an image with uneven lighting.
- **Opening by reconstruction.** Erode, then rebuild by repeated dilation under the mask $f$ until nothing changes. Every connected component of the foreground that holds a translate of $B$ comes back whole, with its corners, and the others vanish. It is on the page [morphological filtering](/morphological-filtering/).
- **Area opening.** Remove the connected components with fewer than $a$ pixels, with no element at all. For a binary image this is a [connected component labeling](/connected-component-labeling/) followed by a size test. It is also idempotent, increasing and anti-extensive.
- **Union of openings.** The maximum of openings by several elements, for example line segments in several directions, is again an algebraic opening. It keeps thin structures in any of the directions.
- **Alternating filters.** An opening followed by a closing, or a sequence of them with growing elements, removes both bright and dark noise. They are on the page [morphological filtering](/morphological-filtering/).

## When to use it

Use opening to remove salt [noise](/image-noise/) and small foreground specks from a binary mask, to break thin bridges between objects before you count them, and to estimate a background for top-hat correction. Use it when the objects you keep must keep their size and position; erosion alone shrinks them. Use the [closing](/morphological-closing/) for the opposite job of filling small holes and gaps. A [median filter](/median-filter/) removes both bright and dark specks in one step, but it is not idempotent and it moves the edges of large thin shapes.

## Pitfalls

- **Different border rules in the two steps.** If line L3 counts the outside as background, a translate that crosses the border never fits, and objects that touch the border lose the parts within the reach of $B$. This can be the intent, but then the dilation must still ignore the outside, or the border grows foreground.
- **The wrong order.** Dilation followed by erosion is the closing, which fills holes instead of removing specks.
- **Reflecting only one step.** If the code of one step uses $p + b$ and the other also uses $p + b$, the result is $(X \ominus B) \oplus \check B$, which is not an opening for an element that is not symmetric: it can move the result by the size of $B$ and is not anti-extensive.
- **Expecting the shape to be kept.** The opening rounds convex corners to the shape of $B$ and removes thin parts. An object that must keep its outline exactly needs an opening by reconstruction.
- **Gray opening is not a smoothing of dark noise.** A flat opening never raises a value, so dark specks stay. Use a closing, or an alternating filter.

## Implementations

## History

Opening comes from the work of Matheron and Serra on porous media and random sets at the École des Mines de Paris in the 1960s. Matheron introduced the granulometries, the families of openings by growing elements, to measure the size distribution of grains, and he described the openings by the three algebraic properties of this page. Serra (1982) gives the theory for sets and functions. Haralick, Sternberg and Zhuang (1987) made the gray scale opening and closing common in computer vision.

## References
