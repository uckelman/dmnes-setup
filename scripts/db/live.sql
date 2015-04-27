DELETE FROM vnf_cnf WHERE vnf NOT IN (SELECT id FROM vnf WHERE live = 1) OR cnf NOT IN (SELECT id FROM cnf WHERE live = 1);
DELETE FROM vnf_authors WHERE ref NOT IN (SELECT id FROM vnf WHERE live = 1);
DELETE FROM cnf_authors WHERE ref NOT IN (SELECT id FROM cnf WHERE live = 1);
DELETE FROM vnf WHERE live = 0;
DELETE FROM cnf WHERE live = 0;
VACUUM;
