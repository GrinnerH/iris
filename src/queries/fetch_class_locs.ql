import cpp

from
  File f
where
  f.isSourceFile()
select
  "Global" as name,
  f.getRelativePath() as file,
  1 as start_line,
  f.getNumberOfLines() as end_line
