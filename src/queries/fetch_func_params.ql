import cpp

bindingset[f]
string fullSignature(Function f) {
  result = f.getReturnType().toString() + " " + f.getName() + "(" +
    concat(Parameter p |
      p.getFunction() = f |
      p.getType().toString() + " " + p.getName(), ", " order by p.getIndex() asc) + ")"
}

bindingset[f]
string paramTypes(Function f) {
  result = concat(Parameter p |
    p.getFunction() = f |
    p.getType().toString(), ";" order by p.getIndex() asc)
}

bindingset[f]
string getDocString(Function f) { result = "" }

from
  Function method
where
  method.fromSource() and
  not method.hasNoParameters()
select
  method.getFile().getRelativePath() as package,
  "Global" as clazz,
  method.getName() as func,
  fullSignature(method) as full_signature,
  method.getSignature() as internal_signature,
  method.getLocation().toString() as location,
  paramTypes(method) as parameter_types,
  method.getReturnType().toString() as return_type,
  getDocString(method) as doc
