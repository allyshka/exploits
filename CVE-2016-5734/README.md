# PhpMyAdmin 4.3.0—4.6.2 authorized user RCE:

## Overview

All 4.6.x versions (prior to 4.6.3), 4.3.x and 4.4.x versions (prior to 4.4.15.7) are affected if server running at PHP version 4.3.0-5.4.6.

Exploit is remote command execution for authorized users only.

The problem in table search and replace function because of unsafe handling of preg_replace parameters.

## Some details

Problem source code part in PMA 4.6.2:
- libraries/controllers/table/TableSearchController.php:708:
```php
708:    private function _getRegexReplaceRows(
...
727:        if (is_array($result)) {
728:            foreach ($result as $index=>$row) {
729:                $result[$index][1] = preg_replace(
730:                    "/" . $find . "/",
731:                    $replaceWith,
732:                    $row[0]
733:                );
734:            }
735:        }
```
Problem source code part in PMA 4.4.15.6:
- libraries/TableSearch.class.php:
```php
1388:    function _getRegexReplaceRows($columnIndex, $find, $replaceWith, $charSet)
..
1405:        if (is_array($result)) {
1406:            foreach ($result as $index=>$row) {
1407:                $result[$index][1] = preg_replace(
1408:                    "/" . $find . "/",
1409:                    $replaceWith,
1410:                    $row[0]
1411:                );
1412:            }
```
See also — https://www.phpmyadmin.net/security/PMASA-2016-27/
CVE-2016-5734

## Exploit
Working only on PHP 4.3.0—5.4.6 :-{

`python3 cve-2016-5734.py -u root --pwd="" http://localhost/pma -c "system('ls -lua')"`

## Fix
Upgrade to phpMyAdmin 4.6.3, 4.4.15.7 or newer and use PHP version 5.4.7 or newer.

4.4 — https://github.com/phpmyadmin/phpmyadmin/commit/33d1373ab645d61cca258fabb07b0c817f1d254c

4.6 — https://github.com/phpmyadmin/phpmyadmin/commit/4bcc606225f15bac0b07780e74f667f6ac283da7
