-- The total number of meters (meter IDs)
WITH all_meters AS (
  SELECT meter_id FROM export_meter
  UNION
  SELECT meter_id FROM import_meter
)
SELECT count(meter_id) as total_meters from all_meters;

-- The total number of hydro generator sites
SELECT count(meter_id) as hydro_count FROM export_meter WHERE generation_type = 'Hydro';

-- The average installed capacity of solar generator sites
SELECT AVG(installed_capacity) as avg_solar_capacity FROM export_meter WHERE generation_type = 'Solar';

-- A list of the different generation types
SELECT DISTINCT generation_type FROM export_meter;

-- A list of distinct organisations by their names and IDs.
WITH all_orgs AS (
  SELECT org_id, org_name FROM export_meter
  UNION
  SELECT org_id, org_name FROM import_meter
)
SELECT DISTINCT org_id, org_name FROM all_orgs;

-- All sites that will be out of contract by the 1st February 2018.
WITH all_sites AS (
  SELECT site_id, site_name, site_address, site_postcode, contract_end_date FROM export_meter
  UNION
  SELECT site_id, site_name, site_address, site_postcode, contract_end_date FROM import_meter
)
SELECT * FROM all_sites WHERE contract_end_date < '2018-02-01';

-- The total monthly estimated volumes of all import sites that are farms
SELECT SUM(monthy_estimate_volume) as total_farm_volume FROM import_meter WHERE consumer_type = 'Farm';

-- The distance between the furthest generator and consumer
WITH generator_locations AS (
  SELECT DISTINCT site_id, site_name, site_address, site_postcode, easting, northing FROM export_meter
    JOIN postcode ON postcode.postcode = site_postcode
), consumer_locations AS (
  SELECT DISTINCT site_id, site_name, site_address, site_postcode, easting, northing FROM import_meter
    JOIN postcode ON postcode.postcode = site_postcode
)
SELECT
  g.site_id as gen_site_id
  ,g.site_name as gen_site_name
  ,g.site_postcode as gen_site_postcode
  ,c.site_id as con_site_id
  ,c.site_name as con_site_name
  ,c.site_postcode as con_site_postcode
  ,(((g.easting - c.easting) * (g.easting - c.easting)) + ((g.northing - c.northing) * (g.northing - c.northing))) as dist
FROM generator_locations g CROSS JOIN consumer_locations c 
ORDER BY dist DESC
LIMIT 1;

