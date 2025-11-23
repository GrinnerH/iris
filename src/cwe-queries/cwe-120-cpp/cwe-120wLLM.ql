/**
 * @name Potential buffer copy without bounds check (C/C++)
 * @kind path-problem
 * @problem.severity error
 * @precision medium
 * @id cpp/my-buffer-overflow
 * @tags security
 *       external/cwe/cwe-120
 */

import cpp
import MyBufferOverflowFlow::PathGraph

from MyBufferOverflowFlow::PathNode source, MyBufferOverflowFlow::PathNode sink
where MyBufferOverflowFlow::flowPath(source, sink)
select
  sink.getNode(),
  source,
  sink,
  "Tainted length/index reaches buffer write without a guard.",
  source.getNode(),
  source.toString()
