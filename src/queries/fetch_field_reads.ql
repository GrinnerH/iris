import cpp

from VariableAccess va, Variable v
where
  va.getTarget() = v and
  v.fromSource()
select
  va as fieldread,
  v as field,
  "Global" as clazz,
  va.getFile().getRelativePath() as package,
  va.getFile() as file,
  va.getLocation().toString() as location

