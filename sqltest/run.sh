python3 generate.py
dropdb clothes
createdb clothes
psql clothes -af create.sql
psql clothes -af test-production.sql > test-production.out
