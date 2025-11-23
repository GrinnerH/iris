import cpp

from Function c
where
  c.fromSource() and
  c.getName() != ""
select
  c.getQualifiedName() as name,
  c.getFile().getRelativePath() as file_path,
  c.getLocation().getStartLine() as start_line,
  c.getLocation().getEndLine() as end_line
