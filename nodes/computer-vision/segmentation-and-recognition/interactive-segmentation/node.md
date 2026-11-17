---
tag: H808XZ
kind: problem
slug: interactive-segmentation
name: Interactive segmentation
aliases:
- user-guided segmentation
area: computer-vision/segmentation-and-recognition
level: core
summary: "Cut an object out of an image from a few user inputs such as seeds, a box or boundary clicks, and update the result quickly each time the user corrects it."
model: real-ram
complexity:
  vars: {n: the number of pixels}
  time: {worst: O(n^3)}
prereqs: [image-segmentation, digital-image]
see_also: [boykov-jolly-graph-cuts, grabcut, intelligent-scissors, random-walker-segmentation, active-contours, watershed-segmentation, image-matting, semantic-segmentation]
sources:
  - paper: doi:10.1109/ICCV.2001.937505
    title: "Yuri Y. Boykov and Marie-Pierre Jolly, Interactive graph cuts for optimal boundary and region segmentation of objects in N-D images, ICCV 2001, vol. I, 105-112"
    locator: the user's seeds as hard constraints and the fast update after new seeds
  - paper: doi:10.1145/218380.218442
    title: "Eric N. Mortensen and William A. Barrett, Intelligent scissors for image composition, SIGGRAPH 1995, 191-198"
    locator: the boundary tracing interface and the live wire
  - paper: doi:10.1109/TPAMI.2006.233
    title: "Leo Grady, Random walks for image segmentation, IEEE TPAMI 28(11), 1768-1783, 2006"
    locator: "Section 3, seeds with K labels as boundary values of a Dirichlet problem"
  - book: isbn:978-1-84882-934-3
    title: "Richard Szeliski, Computer Vision: Algorithms and Applications, 1st edition, Springer, 2011"
    locator: "Chapter 5, Segmentation"
---

Interactive segmentation is the problem of cutting one object, or a few regions, out of an image with help from a user. The user gives a little input, such as seed strokes on the object and the background, a box around the object, a few clicks, or points on its boundary. The program returns a mask. The user then corrects the mask with more input, and the program updates it, again and again until the result is right. A good method needs little input, obeys the input, and answers fast enough for the user to keep working. The input turns the general [image segmentation](/image-segmentation/) problem, which has no single right answer, into a problem with a target that the user defines.

## In plain words

A program cannot know which object in a photo you care about, or where exactly it ends. So you help it. You draw a stroke on the object and one on the background, or a box around the object, or you click along its edge. The program uses these hints to cut out the object and shows you the result.

If part of the result is wrong, you add a hint there. The program fixes the result and shows it again. A good program needs only a few hints, never ignores one, and answers almost at once.

## Definition

The input is an image $I$ with $n$ pixels and a sequence of user inputs $u_1, u_2, \dots$. Common kinds of input are:

- **Seeds:** sets of pixels marked with labels, such as object and background.
- **A box:** a rectangle that contains the object; the pixels outside are background.
- **Boundary points:** points on the edge of the object, joined by the program into a closed curve.
- **Clicks:** single positive or negative points, often on the errors of the last result.

After the input $u_t$ the program returns a labeling $A_t$ of the pixels, usually object and background, or $K$ labels. Most methods treat the input as *constraints*: a pixel marked as object must be object in $A_t$. A method is judged on three things:

- **Effort:** how much input the user needs to reach a mask of a given quality. Benchmarks for click-based methods count the clicks needed to reach a given overlap (intersection over union) with a ground truth mask.
- **Control:** whether the result always obeys the input, and whether a local correction changes the result only near it.
- **Speed:** each update must take a fraction of a second, so the time per update matters more than the total time.

The output can also be soft, with a value in $[0, 1]$ per pixel. The soft version for hair and other thin structures is [image matting](/image-matting/).

## Variants

- **Seed-based, two labels.** The user marks object and background pixels. [Boykov-Jolly graph cuts](/boykov-jolly-graph-cuts/) solve it exactly for an energy with region and boundary terms.
- **Seed-based, $K$ labels.** Each seed has one of $K$ labels, as in the [random walker](/random-walker-segmentation/) or in seeded [watershed](/watershed-segmentation/).
- **Box-based.** The user gives only a box. [GrabCut](/grabcut/) learns color models from the box and refines them.
- **Boundary tracing.** The user follows the edge, and the program snaps the path to it, as in [intelligent scissors](/intelligent-scissors/) or [active contours](/active-contours/).
- **Click-based.** Deep networks take the image and a map of clicks as input. Each new click goes on an error of the last result.
- **Prompt-based.** Large models trained on huge mask data sets take points, boxes or a rough mask as a prompt, and return a mask in one pass.
- **3D and video.** The same inputs on a volume, such as a medical scan, or on a video, where the mask must also follow the object in time.

## Examples

**Seeds on a row of pixels.** Take the gray values $20, 40, 140, 200, 220$, a background seed at pixel 0 and an object seed at pixel 4. The jump from 40 to 140 is the strongest edge, so a good method puts the border there: labels $0, 0, 1, 1, 1$. The [Boykov-Jolly](/boykov-jolly-graph-cuts/) page works through this example. If the user then marks pixel 2 as background, the border moves to the next edge, between 140 and 200, and the labels become $0, 0, 0, 1, 1$.

**A correction that is local.** A good method changes the result only where the new seed has an effect. In the example above, pixels 0, 1, 3 and 4 keep their labels; only pixel 2 changes.

**Boundary points.** With [intelligent scissors](/intelligent-scissors/) the user clicks a start point on the edge and moves the mouse. The program shows the cheapest path to the mouse, and it follows the edge. The user clicks again to fix a part of the path.

## Known algorithms

| Method | Input | Output | Cost of one update | Kind of result |
|---|---|---|---|---|
| [Intelligent scissors](/intelligent-scissors/) (1995) | boundary points | closed curve | one shortest path tree, $O(n \log n)$ | exact for its path cost |
| [Active contours](/active-contours/) (1988) | initial curve | closed curve | iterative | local optimum |
| [Boykov-Jolly graph cuts](/boykov-jolly-graph-cuts/) (2001) | seeds, 2 labels | mask | one max flow, reused | exact for its energy |
| [GrabCut](/grabcut/) (2004) | box, then seeds | mask | a few max flows | local optimum of a joint energy |
| [Random walker](/random-walker-segmentation/) (2006) | seeds, $K$ labels | probabilities and labels | one sparse linear system per label | exact for its system |
| seeded [watershed](/watershed-segmentation/) | seeds, $K$ labels | labels | near linear | exact for its flooding rule |
| [Closed-form matting](/closed-form-matting/) (2006) | scribbles or trimap | soft matte | one sparse linear system | exact for its cost |
| deep click and prompt models (2016 on) | clicks, boxes | mask | one network pass | learned, no guarantee |

The years are of the main papers. "Exact" means that the method finds the global optimum of its own cost. It does not mean that the cost picks the object that the user wants.

## Bounds

All bounds here use the [real-RAM](/real-ram/) model with $n$ pixels and a bounded number of neighbors per pixel.

- **Lower bound.** Any method that reads the whole image needs $\Omega(n)$ time per first result. This is a theorem in the model, and it is trivial.
- **Two labels with seeds.** An energy with unary terms and nonnegative pairwise terms of the form $B_{pq} [A_p \ne A_q]$, with hard seeds, is minimized exactly by one minimum $s$-$t$ cut (Greig, Porteous and Seheult 1989; Boykov and Jolly 2001). So it is solvable in polynomial time, for example $O(n^3)$ with push-relabel on a graph with $O(n)$ edges. This is a theorem.
- **Three or more labels.** With the Potts pairwise term and seeds of $K \ge 3$ labels, the energy contains the multiway cut problem, which is NP-hard (Dahlhaus and others, 1994). This is a theorem, and it is why methods such as [alpha-expansion](/alpha-expansion/) give approximations. The [random walker](/random-walker-segmentation/) avoids it by solving a different, quadratic problem.
- **Boundary tracing.** A cheapest path on the pixel graph costs $O(n \log n)$ with a binary heap, or $O(n)$ with integer costs below a fixed bound and a bucket queue. This is a theorem.
- **Interactive speed.** Measured update times depend on the image, the hardware and the input, so they are benchmark results, not bounds.

## Reductions

- **Seeds to cuts.** Seeds become terminal arcs of capacity larger than any cut through the pixel, so a [minimum cut](/max-flow-min-cut-theorem/) obeys them. See [Boykov-Jolly graph cuts](/boykov-jolly-graph-cuts/).
- **Boundary to paths.** Tracing between two points is a [single source shortest path](/single-source-shortest-paths/) problem on the pixel graph, with low costs on edges. See [intelligent scissors](/intelligent-scissors/).
- **Seeds to a Dirichlet problem.** With seeds as fixed values, harmonic interpolation on the pixel graph is a linear system with the [Laplacian matrix](/laplacian-matrix/). See [random walker](/random-walker-segmentation/).
- **Box to seeds.** A box gives background seeds outside it and an initial color model inside, as in [GrabCut](/grabcut/).
- **Mask to matte.** A hard mask, eroded and dilated, gives a trimap for [image matting](/image-matting/).

## Applications

- **Photo editing.** Cutting out a person or an object to move it, to change the background, or to adjust only that part.
- **Medical imaging.** Outlining an organ or a tumor in a scan for measurement or planning, often in 3D.
- **Labeling data.** Making ground truth masks for [semantic segmentation](/semantic-segmentation/) and object detection data sets, where the time per mask is the main cost.
- **Video and film.** Rotoscoping, where a mask follows an object through many frames.

## References
