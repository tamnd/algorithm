---
title: PMVS keeps only accepted patches in their cells and ends after a finite number of steps
proves: [correctness]
status: full
---

We use the pseudocode of the page and the code that follows it. A cell is a pair (image $i$, index $C$); there are $M$ cells in total, a finite number. A patch $p$ is *registered* when it is in the list of patches and in the list of the cell of its projection in each image of $V^*(p)$. We write $\mathrm{cell}_i(X)$ for the cell of image $i$ that holds the projection of $X$, which is defined only when $X$ is in front of camera $i$ and projects inside the image.

**Lemma 1 (what ACCEPT guarantees).** If ACCEPT$(p)$ returns true, then at that time: $R(p) \in V(p)$, $\mathrm{cell}_i(c(p))$ is defined for every $i \in V(p)$, $R(p) \in V^*(p) \subseteq V(p)$, $h(p, I, R(p)) \le \alpha$ for every $I \in V^*(p) \setminus \{R(p)\}$, and $|V^*(p)| \ge \gamma$.

*Proof.* After refinement, ACCEPT computes $V(p)$ again. It puts an image $i$ into $V(p)$ only when $\mathrm{cell}_i(c(p))$ is defined, and it returns false when $R(p) \notin V(p)$. Then it sets $V^*(p)$ to the images of $V(p)$ that are $R(p)$ or have $h \le \alpha$; if the grid of $p$ does not project inside $R(p)$, it sets $V^*(p) = \emptyset$. In the other case $R(p) \in V^*(p)$ by the definition. ACCEPT returns true only when $|V^*(p)| \ge \gamma$, and $\gamma \ge 1$, so the empty case returns false. $\square$

**Lemma 2 (refinement does not make the score worse).** Let $S$ be the set $V^*(p)$ that ACCEPT computes before refinement. The value of $g^*$ over $S$ at the end of refinement is at most its value at the start.

*Proof.* The search keeps the current point $x$ and its cost $best = g^*$ over $S$. It replaces $x$ only by a point $y$ with a strictly smaller cost, and at the end it puts the patch at $x$. So the cost at the end is the least cost it has seen, which is at most the cost at the start. If the normal does not face the reference camera, refinement does nothing, and the claim is trivial. $\square$

The score that ACCEPT stores at the end is $g^*$ over the new $V^*(p)$, which can differ from $S$. Lemma 2 is about $S$ only.

**Lemma 3 (registration).** Every patch in the list after MATCH, after each EXPAND and after each FILTER is registered, with the values of $V(p)$ and $V^*(p)$ that ACCEPT gave it, and no list of a cell holds a patch that is not in the list of patches.

*Proof.* A patch enters the list only in lines L7 and L14, right after ACCEPT returned true, and the code does not change $c(p)$, $n(p)$, $V(p)$ or $V^*(p)$ after that. Register adds $p$ to the list of $\mathrm{cell}_i(c(p))$ for each $i \in V^*(p)$, and this cell is defined by Lemma 1, since $V^*(p) \subseteq V(p)$. FILTER removes a patch $p$ from the list and from the list of $\mathrm{cell}_i(c(p))$ for each $i \in V^*(p)$, which are exactly the cells where register put it. Nothing else changes the lists. $\square$

**Lemma 4 (one new patch per empty cell).** In EXPAND, each patch $q$ that line L14 registers was made for a target cell $(i, C)$ that held no patch at line L10, and after line L14 the cell $(i, C)$ holds $q$. EXPAND removes no patch.

*Proof.* Line L10 skips $(i, C)$ when its list is not empty. Line L13 requires $i \in V^*(q)$ and $\mathrm{cell}_i(c(q)) = C$, so register puts $q$ into the list of $(i, C)$ by Lemma 3. EXPAND has no step that removes a patch from a list. $\square$

**Lemma 5 (termination of EXPAND).** One call of EXPAND registers at most $M$ patches and ends.

*Proof.* By Lemma 4, every registered patch turns one empty cell into a non-empty one, and no cell becomes empty again during the call. There are at most $M$ empty cells at the start, so at most $M$ patches are registered. The queue starts with a finite list and grows only when a patch is registered, so it gets at most $M$ more entries. Each entry is processed once, with at most $4 N$ target cells and one ACCEPT for each. ACCEPT ends because the refinement stops after at most a fixed number of cost evaluations. So EXPAND ends. $\square$

**Lemma 6 (FILTER).** FILTER ends, removes only patches, and removes $p$ exactly when $p$ sees at least one other patch in the $3 \times 3$ cells around its own cell in the images of $V^*(p)$, and fewer than the fraction $f$ of these patches are neighbors of $p$.

*Proof.* Line L15 visits each patch once and looks at at most $9 N$ finite lists. The decision of line L16 uses only the patches present at the start of the pass, because the removals happen after the loop. So the result does not depend on the order of the patches. $\square$

**Theorem.** PMVS ends. Every patch $p$ in its output satisfies the conditions of Lemma 1 and is registered as Lemma 3 says. Every patch that expansion added fills a cell that was empty when it was made, and every patch that survived the last filter pass had, at that pass, no other patches in the cells around it or at least the fraction $f$ of them as neighbors.

*Proof.* MATCH loops over a finite set of features and a finite list of candidates, and each ACCEPT ends, so MATCH ends. The main loop runs $R$ rounds; each round ends by Lemmas 5 and 6. The output conditions follow from Lemmas 1, 3, 4 and 6, since the last step of each round is FILTER and a patch that FILTER keeps is not changed. $\blacksquare$

**The truth passes the test on exact data.** Suppose the images are exact images of a Lambertian textured surface, read with no error at any point, and $p$ lies on the surface with the true normal, small enough that the surface is flat over its grid. Each grid point is a point of the surface, so every image that sees it records the same value there. Then the samples of $p$ in $R(p)$ and in any image that sees the whole grid are equal, their NCC is 1 when the texture is not flat, and $h = 0 \le \alpha$. So the true patch has every such image in $V^*(p)$ and passes ACCEPT when at least $\gamma$ images see it at an angle below the limit. The code reads the images by bilinear interpolation of pixel values, so in the tests $h$ is small but not zero.

**What is not proved.** The theorem says nothing about how close the patches are to the true surface. Refinement is a local search, so it can stop at a wrong minimum of $g^*$, and a repeated texture or a flat region can give a wrong patch a low score. Matching and expansion can miss parts of the surface, for example where no feature is matched or where the expansion cannot reach. The filter of the code is one rule of the regularization kind, with a fraction chosen for the code, and the visibility filters of the paper are not implemented, so outliers that agree with their neighbors are not removed. The proof also does not cover the paper's refinement by the conjugate gradient method.
