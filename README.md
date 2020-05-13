# parse-SQL-requests
Sorts SQL request in reverse order by time  
  
**Run:**  
```
python parse_logs.py file_with_SQL_requests
```
**By default:**
Create 2 files: unsorted and sorted.

**Options:**  
`-c`, `--count` - write to file the total number of requests  
`-g`, `--group` - write to file group requests by first string(groupped_file)  
`-t`, `--time` - write the total time of requests  
