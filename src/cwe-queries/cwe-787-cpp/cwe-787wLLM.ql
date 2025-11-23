/**
 * @name Potential out-of-bounds access (C/C++)
 * @kind path-problem
 * @problem.severity error
 * @precision medium
 * @id cpp/my-out-of-bounds
 * @tags security
 *       external/cwe/cwe-787
 */

import cpp
import MyBufferOverflowFlow::PathGraph

from MyBufferOverflowFlow::PathNode source, MyBufferOverflowFlow::PathNode sink
where MyBufferOverflowFlow::flowPath(source, sink)
select
  sink.getNode(),
  source,
  sink,
  "Tainted index/length reaches out-of-bounds access without sufficient guard.",
  source.getNode(),
  source.toString()
