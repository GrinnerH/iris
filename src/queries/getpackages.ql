import cpp
from File f
where f.isSourceFile()
select f, f.getRelativePath()
