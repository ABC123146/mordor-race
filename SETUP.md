# Road to Mordor: phone setup

Live map: https://abc123146.github.io/mordor-race/
Open it in Safari, Share, Add to Home Screen.

All race data lives in this GitHub repo as JSON files (`logs/trev.json`, `logs/trem.json`). No other services.

## The race key (Trev does this once, takes 2 minutes)

1. Go to https://github.com/settings/personal-access-tokens/new (logged in as ABC123146).
2. Token name `mordor`, expiration Custom, 1 year out.
3. Repository access: Only select repositories, pick `mordor-race`.
4. Permissions, Repository permissions, Contents: Read and write. Nothing else.
5. Generate, copy the `github_pat_...` string. That string is the race key.

Text the key to Tremayne too. It can only touch this one repo, nothing else on the account.

## On each phone (both of you)

1. Open the live map. Under "Log a walk" there is a one time "race key" box. Paste the key, Save. Manual logging now works from the page on that device forever.
2. Auto logging from Apple Health, in the Shortcuts app, new shortcut named "Mordor Log" (swap `trev` for `trem` on Tremayne's phone):
   - **Find Health Samples**: Steps, Start of Today to Now, then **Calculate Statistics**, Sum.
   - **Format Date**: Current Date, custom format `yyyy-MM-dd`.
   - **Text**: `{"steps": <Statistics>}`
   - **Base64 Encode** the Text.
   - **Text**: `{"message":"auto log","branch":"main","content":"<Base64 Encoded>"}`
   - **Get Contents of URL**: `https://api.github.com/repos/ABC123146/mordor-race/contents/logs/auto/trev-<Formatted Date>-<Current Date formatted HHmmss>.json`
     Method PUT, Headers: `Authorization` = `Bearer <the race key>`, `Accept` = `application/vnd.github+json`. Request Body: the second Text.
3. Automation: Time of Day 9:15 PM daily, Run Immediately, run "Mordor Log".

A robot in the repo folds those auto files into the ledger within a minute. Re running a day just corrects it.
