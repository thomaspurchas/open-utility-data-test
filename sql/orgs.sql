-- A list of distinct organisations by their names and IDs.
WITH all_orgs AS (
  SELECT org_id, org_name FROM export_meter
  UNION
  SELECT org_id, org_name FROM import_meter
)
SELECT DISTINCT org_id, org_name FROM all_orgs;
