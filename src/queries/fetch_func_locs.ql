import cpp

/**
 * Emit the location of each function defined in source code using qualified names.
 */
from Function c
where
  c.fromSource() and
  c.getName() != ""
select
  c.getQualifiedName() as name,
  c.getFile().getRelativePath() as file_path,
  c.getLocation().getStartLine() as start_line,
  c.getLocation().getEndLine() as end_line
