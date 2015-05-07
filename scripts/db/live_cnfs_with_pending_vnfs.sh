#!/bin/bash -e

sqlite3 dmnes.sqlite 'SELECT DISTINCT cnf.nym FROM cnf INNER JOIN vnf_cnf ON cnf.id = vnf_cnf.cnf INNER JOIN vnf ON vnf.id = vnf_cnf.vnf WHERE cnf.live == 1 AND vnf.live = 0 ORDER BY cnf.nym;'
