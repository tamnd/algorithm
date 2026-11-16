---
tag: SHJNS7
kind: problem
slug: multi-robot-slam
name: Multi-robot SLAM
aliases:
- collaborative SLAM
- cooperative SLAM
area: robotics/multi-robot-systems
level: advanced
summary: Several robots build one map together from their own data, which needs relative poses between robots and shared constraints.
prereqs: [slam-problem, pose-graph-optimization, multi-robot-system]
see_also: [graphslam, loop-closure-detection, data-association-slam, sparse-extended-information-filter, factor-graph, gaussian-belief-propagation, switchable-constraints, relative-pose-problem]
sources:
  - paper: doi:10.1177/0278364906072250
    title: Andrew Howard, Multi-robot simultaneous localization and mapping using particle filters, International Journal of Robotics Research 25(12), 2006
    locator: pages 1243 to 1256 (robots with unknown initial poses, mutual encounters, and the use of data from before the encounter)
  - paper: doi:10.1109/ROBOT.2010.5509154
    title: Been Kim and coauthors, Multiple relative pose graphs for robust cooperative mapping, IEEE International Conference on Robotics and Automation, 2010
    locator: pages 3185 to 3192 (one pose graph per robot with an anchor node, joined by encounters)
  - paper: doi:10.1002/rob.21620
    title: Sajad Saeedi, Michael Trentini, Mae Seto and Howard Li, Multiple-robot simultaneous localization and mapping, a review, Journal of Field Robotics 33(1), 2016
    locator: pages 3 to 46 (the problems of relative poses, map merging, data association and communication)
  - book: isbn:9780262201629
    title: Sebastian Thrun, Wolfram Burgard and Dieter Fox, Probabilistic Robotics, MIT Press, 2005
    locator: Chapter 12 (the sparse extended information filter, including the merging of maps of several robots)
---

Multi-robot SLAM asks several robots to build one consistent map of an unknown place and to locate themselves in it, each using its own sensors and sharing data over a limited network. The single-robot parts, the motion model, the measurements and the optimization, are the same as in the [SLAM problem](/slam-problem/), [pose graph optimization](/pose-graph-optimization/) and [GraphSLAM](/graphslam/). What is new with several robots is that their start poses relative to each other are unknown, that constraints between the maps of different robots must be found and checked, and that the data must travel over links that are slow, short and often broken.

## In plain words

Several people explore a cave, each with a notebook and a compass, and each draws a map from where they started. Later they want one map. But nobody wrote down where the others started, so the maps do not line up. They can fix this when two of them meet and see each other, or when two of them recognize the same rock. Each such match tells how one map sits relative to the other.

Robots do the same. The hard parts are finding true matches between maps, rejecting false ones, and sending the right data over a weak radio, without counting the same evidence twice and becoming too sure.

## Definition

There are $r$ robots. Robot $i$ has poses $x^i_0, x^i_1, \dots$ in its own frame, odometry between them, and measurements of landmarks or of the scene. Two kinds of data link the robots:

- **Encounters.** Robot $i$ at time $t$ measures robot $j$ at time $t'$: a relative pose between $x^i_t$ and $x^j_{t'}$ with an uncertainty.
- **Inter-robot loop closures.** Robots $i$ and $j$ observe the same place, possibly at different times, and a scan match or a visual match gives a relative pose, as in [loop closure detection](/loop-closure-detection/).

The unknowns are all robot poses and the map, plus one transform $T_i$ per robot from its frame to a common frame; one robot's frame can be fixed as the common frame. The goal is the most likely values given all data, as a [factor graph](/factor-graph/) or pose graph that joins the robots' graphs.

**Communication model.** The robots form a communication graph that changes as they move, with limited bandwidth and messages that may be delayed or lost; time is asynchronous. Either a server collects all data, or each robot keeps its own estimate and exchanges summaries with neighbors.

**Questions.** Estimate the common map and all trajectories; decide which inter-robot matches to accept; decide what to send, to whom and when.

## Variants

- **Known initial poses.** If the start poses are known, for example from a common start or a global positioning system, the problem is close to one SLAM problem with more data.
- **Unknown initial poses.** The usual case; the frames are tied only by encounters or shared places.
- **Centralized.** A server runs the joint optimization, which is simple but needs all data and a link to the server.
- **Distributed.** Each robot solves its own part and exchanges messages, for example with [Gaussian belief propagation](/gaussian-belief-propagation/) or by summarizing its graph to the variables it shares with others.
- **Map merging only.** Robots build separate maps, and only the final maps are aligned, by matching features or occupancy grids.
- **Filter-based.** Particle filters, as in Howard (2006), or information filters, as in the [sparse extended information filter](/sparse-extended-information-filter/), where merging two maps adds their information after alignment.

## Examples

**Aligning two frames from one encounter.** Robot $A$ uses its own frame. It sees robot $B$ at $(2, 0)$ m, and the two robots measure that $B$'s heading is $90°$ more than $A$'s. In its own frame, $B$ believes it is at $(1, 1)$ m with heading 0. The transform from $B$'s frame to $A$'s frame is a rotation by $90°$, $(x, y) \mapsto (-y, x)$, and a translation $t$ chosen so that $(1, 1)$ maps to $(2, 0)$: the rotation gives $(-1, 1)$, so $t = (3, -1)$ m. A landmark that $B$ mapped at $(3, 0)$ m in its frame lies at $(0, 3) + (3, -1) = (3, 2)$ m in $A$'s frame. In a real system this transform has an uncertainty, and it enters the joint graph as one more factor, not as a fixed value.

**Anchors.** Kim et al. (2010) give each robot's pose graph an *anchor* node, the unknown pose of its frame. Before an encounter, the graphs are independent, and each is solved alone. An encounter adds one factor between two graphs, through their anchors, and from then on one optimization fixes the relative frames and all poses at once.

**Double counting.** Robot $A$ sends its landmark estimate to $B$, $B$ fuses it and sends its result back, and $A$ fuses that too. Then $A$'s own evidence has been counted twice, and its covariance is too small. Systems avoid this by sending only new data, by keeping track of what each neighbor already has, or by fusing with rules that do not assume independence (heuristic design rules).

## Known algorithms

- **Centralized joint optimization.** Collect all pose graphs and inter-robot factors on one computer and solve with [pose graph optimization](/pose-graph-optimization/) or incremental methods such as [iSAM2](/isam2/).
- **Multiple relative pose graphs with anchors** (Kim et al. 2010), above.
- **Particle filters with encounters** (Howard 2006). When robots meet, the data of one robot from before the meeting is also used, by running its filter backward in time from the encounter.
- **Information filter merging** (Probabilistic Robotics, Chapter 12). Align the two maps, then add their information matrices and vectors.
- **Robust inter-robot loop closures.** Check groups of matches for mutual consistency, or use [switchable constraints](/switchable-constraints/) or [M-estimators](/m-estimator/) so that a false match can be switched off.
- **Distributed solvers.** Robots exchange only the variables they share, or run iterative message passing over the joint graph.

## Bounds

- **Same estimator, more data (theorem).** With Gaussian noise and all data in one place, the joint maximum likelihood estimate is the solution of one nonlinear least squares problem, as for one robot; the number of robots changes only the size, by adding $r - 1$ frame transforms.
- **Unobservable relative frames (theorem).** Without any encounter or shared place, the transform between two robots' frames is not determined by the data, so their maps cannot be merged.
- **Communication.** Sending all raw data costs bandwidth that grows with the length of the mission; sending summaries costs less but makes later relinearization hard (heuristic trade-off, discussed in the survey of Saeedi et al. 2016).
- **False matches.** One wrong inter-robot loop closure can bend both maps; robust methods reduce this risk but give no guarantee in general (heuristic).

## Reductions

- With $r = 1$ the problem is the [SLAM problem](/slam-problem/).
- With known relative frames, the problem is one large [full SLAM](/full-slam/) problem whose data come from several robots.
- Aligning two maps from shared features is a [relative pose problem](/relative-pose-problem/), solved with [RANSAC](/ransac/) when some matches are wrong.

## Applications

Teams of robots that explore caves, mines and collapsed buildings, fleets of self-driving cars that share maps, drone swarms that survey a site, and underwater vehicles that map the sea floor all need multi-robot SLAM. It also lets one robot reuse the maps of earlier robots in the same place.

## References
