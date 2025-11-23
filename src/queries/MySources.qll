import cpp
import semmle.code.cpp.dataflow.DataFlow
import semmle.code.cpp.dataflow.ExternalFlow

module MySources {
  /**
   * User-controlled data entering the program via common C APIs.
   */
  predicate isGPTDetectedSource(DataFlow::Node source) {
    // scanf writes into pointer arguments starting at index 1.
    exists(FunctionCall call |
      call.getTarget().getName() = "scanf" |
      source.asExpr() = call.getArgument(1)
    )
    or
    exists(FunctionCall call |
      call.getTarget().getName() = "gets" |
      source.asExpr() = call.getArgument(0)
    )
    or
    exists(FunctionCall call |
      call.getTarget().getName() = "fgets" |
      source.asExpr() = call.getArgument(0)
    )
  }
}
