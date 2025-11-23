import cpp

from FieldAccess fa, ClassField f
where
  fa.getTarget() = f and
  f.fromSource()
select
  fa as fieldread,
  f as field,
  fa.getFile().getRelativePath() as file_path,
  fa.getLocation().toString() as location
