1. backend/docker/local/postgres/Dockerfile
Purpose: This Dockerfile is used to create a custom PostgreSQL Docker image. It starts from the official PostgreSQL image and adds custom maintenance scripts for database management. The scripts are made executable and moved to a directory in the PATH for easy access.
2. backend/docker/local/postgres/maintenance/_sourced/constants.sh
Purpose: This script defines constants used by other maintenance scripts, such as the directory path for backups and the prefix for backup file names.
3. backend/docker/local/postgres/maintenance/_sourced/countdown.sh
Purpose: Provides a utility function to display a countdown timer. This can be used in scripts to wait for a specified amount of time, showing the remaining time in a countdown format.
4. backend/docker/local/postgres/maintenance/_sourced/messages.sh
Purpose: Contains functions for printing formatted messages to the console. These functions help standardize the output of scripts, making it easier to read and understand logs or console output.
5. backend/docker/local/postgres/maintenance/_sourced/yes_no.sh
Purpose: A script to prompt the user for a yes/no confirmation. It reads user input and exits with a status code based on the response, which can be used to control the flow of a script.
6. backend/docker/local/postgres/maintenance/backup
Purpose: This script is used to back up the PostgreSQL database. It uses pg_dump to create a backup, compresses it with gzip, and saves it to a specified directory. It includes checks to ensure the backup is not performed as the postgres user for security reasons.
7. backend/docker/local/postgres/maintenance/backups
Purpose: Lists all available backup files in the backup directory. This script helps users quickly see what backups are available for restoration or other purposes.
8. backend/docker/local/postgres/maintenance/restore
Purpose: Restores a PostgreSQL database from a specified backup file. It drops the existing database, creates a new one, and applies the backup. Like the backup script, it includes checks to prevent running as the postgres user.