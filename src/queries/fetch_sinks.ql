import cpp
import semmle.code.cpp.dataflow.DataFlow
private import semmle.code.cpp.dataflow.ExternalFlow

import MySinks

from
  DataFlow::Node node
where
  isGPTDetectedSink(node)
select
  node.toString() as node_str,
  node.getLocation() as loc
