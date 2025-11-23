import cpp

/**
 * Report reads of class or struct fields in C++ code.
 */
from FieldAccess fa, ClassField f
where
  fa.getTarget() = f and
  f.fromSource()
select
  fa as fieldread,
  f as field,
  fa.getFile().getRelativePath() as file_path,
  fa.getFile() as file,
  fa.getLocation().toString() as location

