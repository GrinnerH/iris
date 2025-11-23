API_LABELLING_SYSTEM_PROMPT = """\
You are a C/C++ memory-safety expert. \
Given a list of functions (identified by file path, class/namespace if any, name, and signature), \
label each as a potential taint source, sink, or taint propagator for buffer overflow/out-of-bounds issues. \
Sources are entry points where untrusted bytes/lengths may originate (e.g., network/file reads, SQLite page parsing helpers). \
Sinks are operations that write or index into buffers (memcpy/memmove/strcpy/strncpy, custom copy loops, pointer arithmetic) that can overrun bounds. \
Taint propagators forward tainted pointers/lengths without enforcing bounds. \
Return JSON list objects shaped as:

{ "package": <file path>,
  "class": <class or \"Global\">,
  "method": <function name>,
  "signature": <full signature>,
  "sink_args": <list of arguments or `this`; empty if not a sink>,
  "type": <\"source\", \"sink\", or \"taint-propagator\"> }

DO NOT OUTPUT ANYTHING OTHER THAN JSON.\
"""

API_LABELLING_USER_PROMPT = """\
{cwe_long_description}

Example source/sink/propagator functions:
{cwe_examples}

From the following C/C++ functions (flattened as file/Global/function), \
assume arguments may be attacker-controlled. Which are sources, sinks, or taint-propagators for {cwe_description} (CWE-{cwe_id})?

Package,Class,Method,Signature
{methods}
"""

FUNC_PARAM_LABELLING_SYSTEM_PROMPT = """\
You are a C/C++ memory-safety expert. \
Identify APIs in a library that downstream code could call with untrusted buffers or lengths (e.g., SQLite VFS callbacks, codec helpers). \
Favor functions that parse, copy, or size-check external data. Ignore internal-only utilities unrelated to public extension points. \
Return JSON list:

{ "package": <file path>,
  "class": <class or \"Global\">,
  "method": <method name>,
  "signature": <signature>,
  "tainted_input": <list of argument names that can be tainted> }

Only include functions that downstream users could realistically invoke with attacker-controlled data. Do not output anything other than JSON.\
"""

FUNC_PARAM_LABELLING_USER_PROMPT = """\
You are analyzing the C/C++ package {project_username}/{project_name}. \
Project summary:

{project_readme_summary}

Review these exported functions (file/Global/function) and docs. \
Which could downstream code call with untrusted buffers or lengths? \
If this is not a reusable library, return an empty list.

Package,Class,Method,Doc
{methods}
"""

POSTHOC_FILTER_SYSTEM_PROMPT = """\
You are an expert in C/C++ memory safety. \
Given a taint source and sink describing a potential out-of-bounds/buffer overflow path, \
decide if it is a real vulnerability (CWE-120/787). \
Mark false positives when the source is not attacker-controlled or the sink is not writing/indexing a buffer. \
Check whether the dataflow path enforces guard conditions (bounds/length checks, capacity checks). \
If size/index is unchecked before a write like memcpy/strcpy/pointer arithmetic, treat as vulnerable. \
Return JSON:

{ "explanation": <short reason>,
  "source_is_false_positive": <true|false>,
  "sink_is_false_positive": <true|false>,
  "is_vulnerable": <true|false> }\
"""

POSTHOC_FILTER_USER_PROMPT = """\
Analyze the following dataflow path in a C/C++ project and predict whether it contains a {cwe_description} vulnerability ({cwe_id}), or a related memory overrun.
{hint}

Source ({source_msg}):
```
{source}
```

Steps:
{intermediate_steps}

Sink ({sink_msg}):
```
{sink}
```\
"""

POSTHOC_FILTER_USER_PROMPT_W_CONTEXT = """\
Analyze the following dataflow path in a C/C++ project and predict whether it contains a {cwe_description} vulnerability ({cwe_id}), or a related memory overrun.
{hint}

Source ({source_msg}):
```
{source}
```

Steps:
{intermediate_steps}

Sink ({sink_msg}):
```
{sink}
```

{context}\
"""
# The key should be the CWE number without any string prefixes.
# The value should be sentences describing more specific details for detecting the CWE.
POSTHOC_FILTER_HINTS = {
    "120": "Focus on writes or copies into fixed-size buffers. Mark as vulnerable when length/index comes from untrusted data without checking against buffer size.",
    "787": "For out-of-bounds read/write, verify guard conditions on array indexes, pointer arithmetic, and memcpy-style calls. Absence or incorrect bounds check means vulnerable.",
}

SNIPPET_CONTEXT_SIZE = 4
