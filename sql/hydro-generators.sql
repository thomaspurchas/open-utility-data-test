-- The total number of hydro generator sites
SELECT count(meter_id) as hydro_count FROM export_meter WHERE generation_type = 'Hydro';
