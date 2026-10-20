HARBORFLOW PORT INTELLIGENCE CONSOLE - TEAM README

Run instructions
----------------
Command: python main.py (run from the project root, the folder that contains dataset/)
Python version tested: 3.11.9 (3.10 or newer is needed because of match/case)

Team members and concrete contributions
---------------------------------------
Name: Zaid
Contribution:
Task 0: A while loop shows the menu until the user picks 10. The input must be 1-10 and
match/case starts the chosen service.
Task 3: Finds a call's manifest, looks up each shipment and gives it the first category that
fits. Prints each one and the totals.
Task 5: Prints the port calls in the chosen month with the vessel name. Rows with an unknown
vessel are skipped.
Task 7: Goes through the event codes once and remembers where each was last seen. A repeat
moves the window start past the earlier one. The longest window wins, first on a tie.

Name: Edvin
Contribution:
data_access.py: Reads all JSON and CSV files, checks required fields and returns the valid
records and how many were skipped.
Task 1: Lists valid vessels sorted by name, ignoring case, and the number skipped.
Task 2: Finds the vessel's next call on or after a date, opens its manifest and looks up each
shipment. Missing ones show as MISSING RECORD.

Name: Isac
Contribution:
Task 4: Totals a customer's shipments and saves one row in exports/customer-profiles.csv,
replacing the row if the customer is already there.
Task 6: Uses re.sub to hide container IDs, seal numbers and emails and saves the text in
exports/sanitized. No file is made if nothing changed.

Name: Gustav
Contribution:
Task 8: Matches a vessel's upcoming calls to weather.csv by port and date and prints every
recommendation that fits.
Task 9: Not done yet. Plan: a word-to-incident index cached in dataset/incident-index.json.

Architecture
------------
main.py responsibilities: Menu loop and calling the services. Tasks 1, 2 and 7 live here.
data_access.py responsibilities: Reading and checking the JSON and CSV files.
operations.py responsibilities: Not used yet.
text_tools.py responsibilities: Not used yet.
Each of task_3, 4, 5, 6 and 8 .py holds one service and is called from main.py.

File and error-handling design
------------------------------
How paths are resolved: data_access.py builds paths from its own location, so none are absolute.
The task files use paths relative to the project root.
How malformed or missing input is handled: The loaders catch the expected file, JSON, CSV and
value errors, say which file or row failed and skip it. Menu, date and month input is asked
again when wrong.
How generated files are updated safely: Task 4 reads the old rows into a list and rewrites the
file, so other customers are kept. Task 6 only writes when something was changed.

Known limitations
-----------------
* Task 9 is not implemented.
* Tasks 3, 4, 5, 6 and 8 read files themselves and some prompts and messages differ from the
  assignment.
<<<<<<< HEAD
* Task 5 does not recognize out of bound dates like 02-30, where as it should report and skip it. 
=======
* Task 6 has no word boundaries for the regular expressions. F.e ABCD12345678 in an incident report would output [CONTAINER]8.
>>>>>>> 392041f2855230e35b78cf45888dfbab4b741644
