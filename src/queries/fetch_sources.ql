import cpp
import semmle.code.cpp.dataflow.DataFlow
private import semmle.code.cpp.dataflow.ExternalFlow

import MySources

from
  DataFlow::Node node
where
  isGPTDetectedSource(node)
select
  node.toString() as node_str,

   node.getLocation().toString() as location
