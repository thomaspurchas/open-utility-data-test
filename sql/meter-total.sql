-- The total number of meters (meter IDs)
WITH all_meters AS (
  SELECT meter_id FROM export_meter
  UNION
  SELECT meter_id FROM import_meter
)
SELECT count(meter_id) as total_meters from all_meters;
