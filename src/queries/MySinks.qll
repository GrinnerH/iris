import cpp
import semmle.code.cpp.dataflow.DataFlow
import semmle.code.cpp.dataflow.ExternalFlow

module MySinks {
  /**
   * Identifies data flow sinks such as dangerous memory copy functions.
   */
  predicate isGPTDetectedSink(DataFlow::Node sink) {
    exists(FunctionCall call |
      (
        call.getTarget().hasName("memcpy") or
        call.getTarget().hasName("strcpy") or
        call.getTarget().hasName("strncpy") or
        call.getTarget().hasName("memmove") or
        call.getTarget().hasName("sprintf") or
        call.getTarget().hasName("strcat")
      ) and
      sink = DataFlow::exprNode(call.getArgument(0))
    )
  }
}
