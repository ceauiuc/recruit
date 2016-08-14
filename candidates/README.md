how to run:
1. run python3 get_candidates.py
  * modify semesters list, output dir, and c value if necessary
2. compile the final candidate list based on the results (koreans.tsv, koreans_maybe.tsv, c-or-less.tsv)
  * needs to be done manually for now)
  * TODO: automate this somehow
3. run ./get_email.sh <listfile> <outfile> <memberlist> <cookiefile>
  * ex)./get_email.sh results/results-15fa_deans/full-list.tsv results/results-15fa_deans/email-list.txt data/members-email.txt data/cookies.txt"

* get_candidates.py - wrapper for find_koreans.py
  * can run on multiple semesters
  * can include korean last name list from previous semesters
* find_koreans.py - find korean students from given student list
  * list should be tab-delimited
  * non-data, such as header row, should be removed
  * following criteria is used to determine if student is korean:
    * originated from korea
    * same last name as other students from korea (should be double-checked manually)
    * last name length less than or equal to c value (default 6) (should be double-checked manually)
* get_email.sh - get email address (netid) from uiuc directory
  * requires authorized user's uiuc directory login cookie file
  * removes duplicates from current member list

