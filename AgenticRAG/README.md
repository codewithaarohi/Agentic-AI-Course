
# Agentic RAG

## Video Tutorial (Hindi): https://youtu.be/PB9yf7E5YTw


### Environment setup: 
			pip install -U agno 
			pip install arxiv 
			
			Download postreSQL database:  https://www.postgresql.org
			
			Check version (Open Terminal / Command Prompt) - run this command: 
			
				psql --version
			
			Run this to enter the PostgreSQL shell using the default user (usually postgres):
				psql -U postgres
				If it asks for a password, enter the one you set during PostgreSQL installation.
			
			Inside the PostgreSQL shell, run:

				CREATE USER ai WITH PASSWORD 'ai';
				
				CREATE DATABASE ai;
				
				GRANT ALL PRIVILEGES ON DATABASE ai TO ai;

			pip install pgvector psycopg[binary]			
			
			pgvector — it lets your Python code talk to a pgvector-enabled PostgreSQL database.
			It does NOT install the vector extension into PostgreSQL itself. That extension must be installed at the PostgreSQL server level, not via pip.
			Lets install pgvector extension in our PostgreSQL.

				Open-  https://github.com/andreiramani/pgvector_pgsql_windows/releases
				
				Download vector.v0.8.0-pg17.3.zip
				
				Unzip it 

				vector.dll → C:\Program Files\PostgreSQL\17\lib
				
				vector.control, vector--*.sql → C:\Program Files\PostgreSQL\17\share\extension
				
				Restart PostgreSQL service. Make sure to run Command Prompt as Administrator:

				Then run this command again:
				
					net stop postgresql-x64-17   
				
				restart the PostgreSQL service:
				
					net start postgresql-x64-17   


