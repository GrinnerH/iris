import cpp

/**
 * Identify calls to external APIs in the C/C++ code base.
 * Java-specific reflection helpers have been removed in favor of C++ APIs.
 */
predicate isExternalCall(FunctionCall c) {
  // Skip obvious test helpers; keep libc-style memory operations.
  not c.getTarget().hasName("assert") and
  not c.getTarget().getQualifiedName().matches("testing::%")
}

/**
 * Build a readable signature for the target function.
 */
string fullSignature(Function f) {
  result = f.getType().toString() + " " + f.getQualifiedName() + "(" +
    concat(Parameter p |
      p.getFunction() = f |
      p.getType().toString() + " " + p.getName(), ", " order by p.getIndex() asc) + ")"
}

/**
 * Collect semicolon separated parameter type names.
 */
string paramTypes(Function f) {
  result = concat(Parameter p |
    p.getFunction() = f |
    p.getType().toString(), ";" order by p.getIndex() asc)
}

/**
 * Represent whether the function is static as a string.
 */
string isStaticAsString(Function f) {
  result = "true" and exists(MemberFunction m | m = f and m.isStatic()) or
  result = "false" and not exists(MemberFunction m | m = f and m.isStatic())
}

/**
 * Placeholder for a documentation string.
 */
string getDocString(Function f) { result = "" }

from
  FunctionCall api,
  Function target
where
  api.getTarget() = target and
  isExternalCall(api)
select
  api as callstr,
  api.getFile().getRelativePath() as file_path,
  fullSignature(target) as full_signature,
  target.getType().toString() as internal_signature,
  target as func,
  isStaticAsString(target) as is_static,
  api.getFile() as file,
  api.getLocation().toString() as location,
  paramTypes(target) as parameter_types,
  target.getType().toString() as return_type,
  getDocString(target) as doc
