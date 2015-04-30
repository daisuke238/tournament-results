Tournament Results

Steps to run the program (assumes Git Bash/Vagrant/VirtualBox installed):

1. Place following files in the same folder:
   "tournament.sql"
   "tournament.py"
   "tournament_test.py"
2. Run Git Bash (as admin if necessary)
3. Navigate to folder in #1
4. Run "vagrant up" command (to launch virtual machine)
5. Run "vagrant ssh" command (to login to virtual machine)
6. Navigate to folder in #1
7. Run "psql" command (to login into psql)
8. Run "\i tournament.sql" command (to create the tournament DB and it's contents)
9. Run "\q" to exit psql
10. Run "python tournament_test.py"

