QUERIES = {
  "cwe-120wLLM-cpp": {
    "name": "cwe-120wLLM-cpp",
    "cwe_id": "120",
    "cwe_id_short": "120",
    "cwe_id_tag": "CWE-120",
    "type": "cwe-query",
    "desc": "Buffer copy without checking size (C/C++)",
    "queries": [
      "cwe-queries/cwe-120-cpp/cwe-120wLLM.ql",
      "cwe-queries/cwe-120-cpp/MyBufferOverflowFlow.qll",
    ],
    "prompts": {
      "cwe_id": "120",
      "desc": "Buffer copy without checking size",
      "long_desc": """\
Focus on C/C++ buffer copies where size/index is derived from untrusted data and used without bounds checks. \
Typical sinks include memcpy/memmove/strcpy/strncpy, manual loops writing into fixed buffers, and pointer arithmetic into arrays. \
Sources include file/socket reads, SQLite page parsing helpers, and any API returning externally supplied bytes or lengths. \
Guard conditions like length comparisons should downgrade risk; missing or incorrect guards indicate vulnerability.""",
      "examples": [
        {
          "package": "src/os_unix.c",
          "class": "Global",
          "method": "unixRead",
          "signature": "int unixRead(unixFile *id, void *pBuf, int iAmt)",
          "sink_args": ["pBuf"],
          "type": "source"
        },
        {
          "package": "src/util.c",
          "class": "Global",
          "method": "sqlite3_snprintf",
          "signature": "char *sqlite3_snprintf(int n, char *zBuf, const char *zFormat, ...)",
          "sink_args": ["zBuf"],
          "type": "sink"
        },
        {
          "package": "src/btree.c",
          "class": "Global",
          "method": "get2byte",
          "signature": "u16 get2byte(const u8 *p)",
          "sink_args": [],
          "type": "taint-propagator"
        }
      ]
    }
  },
  "cwe-787wLLM-cpp": {
    "name": "cwe-787wLLM-cpp",
    "cwe_id": "787",
    "cwe_id_short": "787",
    "cwe_id_tag": "CWE-787",
    "type": "cwe-query",
    "desc": "Out-of-bounds read/write (C/C++)",
    "queries": [
      "cwe-queries/cwe-787-cpp/cwe-787wLLM.ql",
      "cwe-queries/cwe-787-cpp/MyBufferOverflowFlow.qll",
    ],
    "prompts": {
      "cwe_id": "787",
      "desc": "Out-of-bounds read/write",
      "long_desc": """\
Detect flows where attacker-influenced indexes or lengths reach array access, pointer arithmetic, or memcpy-style operations without proper bounds checks. \
Consider stack/heap buffers, vector/data pointers, and macros that decode SQLite pages. \
Treat explicit guards (<= buffer size) as mitigation; missing or off-by-one guards indicate OOB risk.""",
      "examples": [
        {
          "package": "src/pager.c",
          "class": "Global",
          "method": "readDbPage",
          "signature": "int readDbPage(DbPage *pPg, Pgno pgno)",
          "sink_args": [],
          "type": "source"
        },
        {
          "package": "src/vdbeaux.c",
          "class": "Global",
          "method": "memcpy",
          "signature": "void *memcpy(void *dest, const void *src, size_t n)",
          "sink_args": ["dest"],
          "type": "sink"
        },
        {
          "package": "src/where.c",
          "class": "Global",
          "method": "sqlite3WhereFindTerm",
          "signature": "WhereTerm *sqlite3WhereFindTerm(WhereClause *pWC, int iCur, int iColumn, u32 op)",
          "sink_args": [],
          "type": "taint-propagator"
        }
      ]
    }
  },
  "fetch_class_locs": {
    "name": "fetch_class_locs",
    "type": "helper-query",
    "queries": [
      "queries/fetch_class_locs.ql"
    ]
  },
  "fetch_func_locs": {
    "name": "fetch_func_locs",
    "type": "helper-query",
    "queries": [
      "queries/fetch_func_locs.ql"
    ]
  },
  "fetch_sources": {
    "name": "fetch_sources",
    "type": "helper-query",
    "queries": [
      "queries/fetch_sources.ql"
    ]
  },
  "fetch_sinks": {
    "name": "fetch_sinks",
    "type": "helper-query",
    "queries": [
      "queries/fetch_sinks.ql"
    ]
  },
  "fetch_external_apis": {
    "name": "fetch_external_apis",
    "type": "helper-query",
    "queries": [
      "queries/fetch_external_apis.ql"
    ]
  },
  "fetch_func_params": {
    "name": "fetch_func_params",
    "type": "helper-query",
    "queries": [
      "queries/fetch_func_params.ql"
    ]
  },
  "fetch_field_reads": {
    "name": "fetch_field_reads",
    "type": "helper-query",
    "queries": [
      "queries/fetch_field_reads.ql"
    ]
  },
  "getpackages": {
    "name": "getpackages",
    "type": "helper-query",
    "queries": [
      "queries/getpackages.ql"
    ]
  }
}
