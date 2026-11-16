---
tag: JHT4AA
kind: technique
slug: depth-map-fusion
name: Depth map fusion
aliases:
- depth map merging
area: computer-vision/stereo-and-dense-reconstruction
level: advanced
summary: Combine depth maps from many views into one consistent model, by voting, visibility reasoning or a volumetric function, removing outliers.
prereqs: [multi-view-stereo, pinhole-camera-model, z-buffer]
see_also: [tsdf-fusion, plane-sweep-stereo, patchmatch-stereo, left-right-consistency-check, signed-distance-function, marching-cubes, poisson-surface-reconstruction, point-cloud]
sources:
  - paper: doi:10.1109/ICCV.2007.4408984
    title: Paul Merrell, Amir Akbarzadeh, Liang Wang, Philippos Mordohai, Jan-Michael Frahm, Ruigang Yang, David Nistér and Marc Pollefeys, Real-time visibility-based fusion of depth maps, IEEE International Conference on Computer Vision 2007
    locator: the free-space violations and occlusions of a depth hypothesis, the stability-based fusion, the confidence measure, and the confidence-based fusion of Algorithm 2
  - paper: doi:10.1145/237170.237269
    title: Brian Curless and Marc Levoy, A volumetric method for building complex models from range images, SIGGRAPH 1996, pages 303 to 312
    locator: the cumulative weighted signed distance function and its running update, and the surface as its zero set
  - paper: doi:10.1561/0600000052
    title: "Yasutaka Furukawa and Carlos Hernández, Multi-view stereo: a tutorial, Foundations and Trends in Computer Graphics and Vision 9(1-2), pages 1 to 148, 2015"
    locator: the chapter on multi-view stereo algorithms (depth map reconstruction and the merging of depth maps)
  - book: isbn:9783030343712
    title: Richard Szeliski, Computer Vision, Algorithms and Applications, second edition, Springer, 2022
    locator: Chapter 12, Depth estimation (multi-view stereo and the merging of depth maps)
---

Depth map fusion is the step that turns many depth maps, one per view, into one model of the scene. A depth map from [plane sweep](/plane-sweep-stereo/) or [PatchMatch stereo](/patchmatch-stereo/) has errors: wrong depths on weak texture, noise, and holes. Different views make different errors, so a depth that several views confirm is more likely to be right, and a depth that blocks what other views see is likely to be wrong. Fusion uses this to remove outliers and average the rest. This page is the general technique, with its point-based and visibility-based forms. [TSDF fusion](/tsdf-fusion/) is one algorithm of the volumetric form, which averages truncated signed distances on a grid; it has its own page. Fusion is the second half of the depth map approach to [multi-view stereo](/multi-view-stereo/).

## In plain words

Ask ten people to measure the distance to a wall, each from a slightly different place. Most say about 2 meters, one says 3 meters, and one says 1 meter. The 1 meter answer would put a wall right where the other people can see through to the real wall, so it must be wrong. The 3 meter answer is hidden behind the real wall and agrees with nobody. You throw away the two odd answers and average the others. Depth map fusion does this for every pixel of every view, and then puts all the good points into one model.

## When it applies

- You have depth maps $Z_1, \dots, Z_N$ with known cameras $(K_i, R_i, t_i)$, and the views overlap, so most surface points are seen in several maps.
- The errors of different maps are not the same: an outlier in one map is not repeated at the same 3D place in the others. Errors that all views share, such as a bias from a wrong calibration, cannot be found this way.
- The scene is static, and the depths are in the same scale and the same world frame.

A depth map gives the point $X = R_i^{\mathsf T} (Z_i(p) K_i^{-1} \tilde p - t_i)$ for a pixel $p$ of view $i$, where $\tilde p = (u, v, 1)^{\mathsf T}$. Rendering the depths of view $j$ into view $i$ is a [z-buffer](/z-buffer/) pass: project each point of view $j$ into view $i$ and keep the nearest depth per pixel.

## The template

```pseudo id=main
FUSE(depth maps Z_1 ... Z_N, cameras, tolerance τ, least support m)
L1  for each reference view r do
L2      render each other depth map Z_j into view r, keeping the nearest depth per pixel
L3      for each pixel p of r with candidate depths z from Z_r and the rendered maps do
L4          for each candidate z: count the views that support it (depth within τ of z),
L5              the views whose surface lies in front of it (occlusions) and
L6              the views that see through its point to a farther surface (free-space violations)
L7          pick one candidate by a rule on these counts; drop p if its support is below m
L8          average the supporting depths, and mark the supporting pixels in the other views as used
L9  collect the kept 3D points of all views into one model
L10 build a surface from the model, for example by Poisson reconstruction or by marching cubes on a volume
```

Lines L2 to L6 compare one view with the others by projection. A point of view $j$ that agrees with the candidate within $\tau$ supports it. A point that lies in front of the candidate along the ray of $p$ occludes it, which does not prove it wrong. A candidate that lies in front of the surface that view $j$ sees, along the ray of view $j$, is in space that view $j$ saw as empty: that is a free-space violation, and it is evidence that the candidate is wrong. Line L7 is where the methods differ. Line L8 keeps each surface point once, so that the model is not dense where many views overlap. The tolerance $\tau$ is usually relative to the depth, since depth error grows with distance.

## Classic examples

- **Stability-based fusion (Merrell et al. 2007).** The stability of a depth hypothesis is its number of occlusions minus its number of free-space violations. For each pixel the method takes the closest hypothesis whose stability is not negative. A depth that floats in front of the surface has many free-space violations and fails; the true surface has none. The paper also has a confidence-based fusion (its Algorithm 2), which weights each depth with a confidence from the matching cost, $C(x) = \big(\sum_{d \ne d_0} e^{-(c(x, d) - c(x, d_0))^2 / \sigma^2}\big)^{-1}$, where $d_0$ is the best depth. Both run in real time on the GPU for video from a moving vehicle. Each reference view renders the other maps, so the work is $O(N^2)$ renderings for $N$ views when every view is a reference.
- **Volumetric fusion (Curless and Levoy 1996).** Each depth map gives a signed distance along the line of sight, near the surface. A grid stores a weighted average $D(x) = \sum_i w_i(x) d_i(x) / \sum_i w_i(x)$ with a weight sum $W(x)$, updated per map by $D \leftarrow (W D + w d) / (W + w)$ and $W \leftarrow W + w$. The surface is the zero set of $D$, found by [marching cubes](/marching-cubes/). [TSDF fusion](/tsdf-fusion/) is this method with truncated distances, as used in real-time depth camera systems.
- **Consistency checks for point clouds.** Many multi-view stereo systems keep a pixel only if its 3D point reprojects into at least $m$ other views with a depth within $\tau$ and, where normals exist, a normal within an angle. The kept points are merged and meshed with [Poisson surface reconstruction](/poisson-surface-reconstruction/). This is the depth map form of the [left-right consistency check](/left-right-consistency-check/) of two-view stereo.
- **Median fusion.** Rendering all maps into a reference view and taking the median of the candidate depths per pixel removes isolated outliers. It is simple but ignores visibility, so it fails at depth edges.

## Variations

- **Output.** A point cloud with normals, a volume with a signed distance, or a fused depth map for each reference view.
- **Weights.** Weight each depth by its matching cost, by the angle between the ray and the surface normal, or by the depth, since far points are less certain.
- **Normals.** Methods that compute a normal per pixel, such as PatchMatch stereo, can check that the normals agree, not only the depths.
- **Visibility in the volume.** Volumetric methods can mark the space between each camera and its surface as empty, which removes floating outliers and helps to fill holes. Curless and Levoy describe such a carving of empty space.
- **Graph cut fusion.** The depth labels of a reference view can be chosen by an energy with a visibility term and a smoothness term, solved with graph cuts.

## Pitfalls

- **Tolerance in pixels or meters.** A fixed tolerance in meters is too strict for far points and too loose for near ones. Use a tolerance relative to the depth or to the size of one pixel at that depth.
- **Counting the same view twice.** After a pixel supports one fused point, mark it as used. If not, the same depth gives support many times and the model has duplicate points.
- **Occlusion is not conflict.** A depth of another view that lies in front of the candidate may just be an object in front. Only free-space violations are evidence against the candidate.
- **Thin structures.** A thin object seen in few views gets little support and can be removed by a high $m$.
- **Grid size.** A volumetric method with a coarse grid loses detail, and a fine grid needs much memory. Use a sparse grid, a hash of blocks, or an octree.
- **Shared errors.** If the calibration is wrong, all views agree on a wrong surface. Fusion does not correct this; fix the cameras with bundle adjustment first.

## Exercises

1. Show that the running update $D \leftarrow (W D + w d) / (W + w)$, $W \leftarrow W + w$ gives after all maps the same value as the batch weighted average, in any order of the maps.
2. A pixel has the matching costs 1 at its best depth $d_0$ and 2 and 3 at two other depths. Compute the confidence $C$ of Merrell et al. with $\sigma = 1$, and say how it changes when the second cost drops to 1.1.
3. Along the ray of a reference pixel there are three candidates at depths 1.2, 2.0 and 3.1. The candidate at 1.2 lies in front of the surfaces that three other views see, and the candidate at 2.0 is behind the candidate at 1.2 and has no free-space violation. Give the stability of each of the two near candidates and the depth that stability-based fusion picks.
4. Two depth maps of a plane at depth 2 m come from cameras 0.5 m apart. One has an outlier pixel with depth 1 m. Show that the outlier point lies in the free space of the other view if the other view sees the plane behind it.
5. Explain why taking the median of the rendered depths per pixel can remove the front surface at a depth edge.

## References
