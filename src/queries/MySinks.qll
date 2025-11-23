import cpp
import semmle.code.cpp.dataflow.DataFlow
import semmle.code.cpp.dataflow.ExternalFlow

module MySinks {
  /**
   * Potentially unsafe buffer write targets.
   */
  predicate isGPTDetectedSink(DataFlow::Node sink) {
    exists(FunctionCall call |
      call.getTarget().getName() = "memcpy" or
      call.getTarget().getName() = "strcpy" or
      call.getTarget().getName() = "strncpy" or
      call.getTarget().getName() = "memmove" |
      sink.asExpr() = call.getArgument(0) or
      sink.asExpr() = call.getArgument(1)
    )
  }
}
