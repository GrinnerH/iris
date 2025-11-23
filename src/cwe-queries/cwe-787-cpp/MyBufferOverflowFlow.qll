/**
 * Dataflow config for C/C++ out-of-bounds access flows.
 */
import cpp
import semmle.code.cpp.dataflow.DataFlow
import semmle.code.cpp.dataflow.TaintTracking
private import semmle.code.cpp.dataflow.ExternalFlow

import MySources
import MySinks
import MySummaries

module MyBufferOverflowConfig implements TaintTracking::ConfigSig {
  predicate isSource(DataFlow::Node source) { isGPTDetectedSource(source) }
  predicate isSink(DataFlow::Node sink) { isGPTDetectedSink(sink) }
  predicate isAdditionalFlowStep(DataFlow::Node n1, DataFlow::Node n2) { isGPTDetectedStep(n1, n2) }
}

module MyBufferOverflowFlow = TaintTracking::Global<MyBufferOverflowConfig>;
module MyBufferOverflowPath = MyBufferOverflowFlow::PathGraph;
