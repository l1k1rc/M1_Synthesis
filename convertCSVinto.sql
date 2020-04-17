--mysql -u l1k1 -D projetM1 -p 
--raccoon

CREATE TABLE csv_data (
    time DATETIME, 
    mac_address VARCHAR(100), 
    vendor VARCHAR(100), 
    ssid VARCHAR(100), 
    signal_strenght VARCHAR(100), 
    channel VARCHAR(100), 
    survey VARCHAR(100)
);

LOAD DATA LOCAL INFILE 'wifi_data.csv' 
    INTO TABLE csv_data FIELDS TERMINATED 
        BY ';' LINES TERMINATED 
        BY '\n' IGNORE 1 LINES;
