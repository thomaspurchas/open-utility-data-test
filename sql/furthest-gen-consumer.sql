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
