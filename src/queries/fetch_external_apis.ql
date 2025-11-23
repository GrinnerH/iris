import cpp

predicate isExternalCall(FunctionCall c) {
  // Skip obvious test helpers; keep libc-style memory operations.
  not c.getTarget().hasName("assert") and
  not c.getTarget().getQualifiedName().matches("testing::%")
}

bindingset[f]
string fullSignature(Function f) { result = f.getType().toString() }

bindingset[f]
string paramTypes(Function f) {
  result = concat(Parameter p |
    p.getFunction() = f |
    p.getType().toString(), ";" order by p.getIndex() asc)
}

string isStaticAsString(Function f) { result = "false" }

bindingset[f]
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
