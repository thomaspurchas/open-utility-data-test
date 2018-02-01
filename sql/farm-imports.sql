-- The total monthly estimated volumes of all import sites that are farms
SELECT SUM(monthy_estimate_volume) as total_farm_volume FROM import_meter WHERE consumer_type = 'Farm';
