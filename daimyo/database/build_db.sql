-- The database layout for Daimyo
-- Chris Vantine

-- Keep track of arbitrary information sent up by the host
CREATE TABLE `keys_aws` (
  `name`      TEXT,
	`access`    TEXT,
	`private`   TEXT,
	`region`    TEXT
) ;

-- These are the IPs that we know about with last checkin time
CREATE TABLE `keys_vsphere` (
  `name`      TEXT,
	`ip`        TEXT,
	`username`  TEXT,
  `password`  TEXT
) ;