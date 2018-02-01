-- The average installed capacity of solar generator sites
SELECT AVG(installed_capacity) as avg_solar_capacity FROM export_meter WHERE generation_type = 'Solar';
