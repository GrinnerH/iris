import cpp

/**
 * Capture functions that have parameters, recording their signature and parameter types.
 */
string fullSignature(Function f) {
  result = f.getType().toString() + " " + f.getQualifiedName() + "(" +
    concat(Parameter p |
      p.getFunction() = f |
      p.getType().toString() + " " + p.getName(), ", " order by p.getIndex() asc) + ")"
}

string paramTypes(Function f) {
  result = concat(Parameter p |
    p.getFunction() = f |
    p.getType().toString(), ";" order by p.getIndex() asc)
}

string getDocString(Function f) { result = "" }

from Function method
where
  method.fromSource() and
  method.getNumberOfParameters() > 0
select
  method.getFile().getRelativePath() as file_path,
  method.getName() as func,
  fullSignature(method) as full_signature,
  method.getType().toString() as internal_signature,
  method.getLocation().toString() as location,
  paramTypes(method) as parameter_types,
  method.getType().toString() as return_type,
  getDocString(method) as doc
