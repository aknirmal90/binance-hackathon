import sqlalchemy as sa
import pandas as pd
import json
import urllib.request
import random
from urllib.error import HTTPError

engine = sa.create_engine('clickhouse://safu_hackathon:SatisfactionGuaranteed@data.bloxy.info:8123/production?readonly=true')
conn = engine.connect()

# Extracting aggregates for user addresses by given address(es)
# In: array of addresses 
# Out: dictionary by address of aggregated values about address, 
#      sending/receiving to/from source address
def user_data_for_addresses(address_array):
    address_list = ', '.join(list(map(lambda x: 'unhex(\''+x[2:]+'\')', address_array)))
    query_agggegates = """SELECT * FROM (
  SELECT
    concat('0x',lower(hex(transfer_to_bin))) address,
    concat('0x',lower(hex(transfer_from_bin))) user_address,
    count(*) ether_in_count,
    sum(value)/1e18 ether_in_amount
  FROM production.transfers_to
  WHERE currency_id=1 AND
    transfer_to_bin IN ({})
  GROUP BY transfer_to_bin,transfer_from_bin
) ANY LEFT JOIN (
  SELECT
    concat('0x',lower(hex(transfer_from_bin))) address,
    concat('0x',lower(hex(transfer_to_bin))) user_address,
    count(*) ether_out_count,
    sum(value)/1e18 ether_out_amount
  FROM production.transfers_from
  WHERE currency_id=1 AND
    transfer_from_bin IN ({})
  GROUP BY transfer_from_bin,transfer_to_bin
) USING address,user_address"""

    rows = conn.execute(query_agggegates.format(address_list,address_list))
    dataFrame = pd.DataFrame([{key: value for (key, value) in row.items()} for row in rows])
    return dataFrame.set_index('address')
