QL_SOURCE_PREDICATE = """\
import cpp
import semmle.code.cpp.dataflow.DataFlow
private import semmle.code.cpp.dataflow.ExternalFlow

predicate isGPTDetectedSource(DataFlow::Node src) {{
{body}
}}

{additional}
"""

QL_SINK_PREDICATE = """\
import cpp
import semmle.code.cpp.dataflow.DataFlow
private import semmle.code.cpp.dataflow.ExternalFlow

predicate isGPTDetectedSink(DataFlow::Node snk) {{
{body}
}}

{additional}
"""

QL_SUBSET_PREDICATE = """\
predicate isGPTDetected{kind}Part{part_id}(DataFlow::Node {node}) {{
{body}
}}
"""

CALL_QL_SUBSET_PREDICATE = "    isGPTDetected{kind}Part{part_id}({node})"

QL_STEP_PREDICATE = """\
import cpp
import semmle.code.cpp.dataflow.DataFlow
private import semmle.code.cpp.dataflow.ExternalFlow

predicate isGPTDetectedStep(DataFlow::Node prev, DataFlow::Node next) {{
{body}
}}
"""

QL_METHOD_CALL_SOURCE_BODY_ENTRY = """\
    exists(FunctionCall fc |
        src.asExpr() = fc and
        fc.getTarget().hasName("{method}") and
        fc.getFile().getRelativePath() = "{package}"
    )\
"""

QL_FUNC_PARAM_SOURCE_ENTRY = """\
    exists(Parameter p |
        src.asParameter() = p and
        p.getFunction().hasName("{method}") and
        p.getFunction().getFile().getRelativePath() = "{package}" and
        ({params})
    )\
"""

QL_FUNC_PARAM_NAME_ENTRY = """ p.getName() = "{arg_name}" """

QL_SUMMARY_BODY_ENTRY = """\
    exists(FunctionCall c |
        (c.getArgument(_) = prev.asExpr()) and
        c.getTarget().hasName("{method}") and
        c.getFile().getRelativePath() = "{package}" and
        c = next.asExpr()
    )\
"""

QL_SINK_BODY_ENTRY = """\
    exists(FunctionCall c |
        c.getTarget().hasName("{method}") and
        c.getFile().getRelativePath() = "{package}" and
        ({args})
    )\
"""

QL_SINK_ARG_NAME_ENTRY = """ c.getArgument({arg_id}) = snk.asExpr() """

QL_SINK_ARG_THIS_ENTRY = """ c.getArgument(0) = snk.asExpr() """

QL_BODY_OR_SEPARATOR = "\n    or\n"

EXTENSION_YML_TEMPLATE = """\
extensions:
  - addsTo:
      pack: codeql/cpp-all
      extensible: sinkModel
    data:
{sinks}
  - addsTo:
      pack: codeql/cpp-all
      extensible: sourceModel
    data:
{sources}
"""

EXTENSION_SRC_SINK_YML_ENTRY = """\
      - ["{package}", "{clazz}", True, "{method}", "", "", "{access}", "{tag}", "manual"]\
"""

EXTENSION_SUMMARY_YML_ENTRY = """\
      - ["{package}", "{clazz}", True, "{method}", "", "", "{access_in}", "{access_out}", "{tag}", "manual"]\
"""
