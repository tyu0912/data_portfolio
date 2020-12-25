move /Y "C:\Users\tyu\Downloads\DKSalaries.csv" "C:\Users\tyu\Google_Drive\Data Development\nhl_dk\DK_Input"
cd "Active Roster Scrape"
python scrape.py
cd ..
cd "DK_Input"
python DK_cleanup.py
cd ..
REM cd "OOP player data pull - Dev"
REM python new_data_pull.py
REM cd ..
cd "Rotogrind_Scrape"
python lineup_scrape.py
cd ..
TIMEOUT /T 5
python 1_DataGathering.py
TIMEOUT /T 5
python 2_DataLearning.py
TIMEOUT /T 5
python 4_MappingExtraDetails.py
TIMEOUT /T 5
cd "Final Results"
python optimizer2.py
cmd