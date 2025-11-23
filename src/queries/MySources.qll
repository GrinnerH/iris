import cpp
import semmle.code.cpp.dataflow.DataFlow
import semmle.code.cpp.dataflow.ExternalFlow

module MySources {
  /**
   * Identifies data flow sources such as user input functions.
   */
  predicate isGPTDetectedSource(DataFlow::Node source) {
    exists(FunctionCall call |
      call.getTarget().hasName("scanf") or
      call.getTarget().hasName("gets") or
      call.getTarget().hasName("fgets") or
      call.getTarget().hasName("std::getline") or
      call.getTarget().hasName("getline") |
      source = DataFlow::exprNode(call.getArgument(0))
    )
  }
}
