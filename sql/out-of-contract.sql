-- All sites that will be out of contract by the 1st February 2018.
WITH all_sites AS (
  SELECT site_id, site_name, site_address, site_postcode, contract_end_date FROM export_meter
  UNION
  SELECT site_id, site_name, site_address, site_postcode, contract_end_date FROM import_meter
)
SELECT * FROM all_sites WHERE contract_end_date < '2018-02-01';
