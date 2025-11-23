import cpp

/**
 * Collect locations of classes/structs/unions defined in source code.
 * Uses qualified names so results remain clear inside namespaces.
 */
from Class c
where c.fromSource()
select
  c.getQualifiedName() as name,
  c.getLocation().getFile().getRelativePath() as file_path,
  c.getLocation().getStartLine() as start_line,
  c.getLocation().getEndLine() as end_line
