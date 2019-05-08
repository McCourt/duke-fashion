CREATE TABLE Person
(uid INTEGER NOT NULL PRIMARY KEY,
 collegeid INTEGER NOT NULL,
 username VARCHAR(256) NOT NULL,
 phone DECIMAL(10, 0),
 email VARCHAR(256) UNIQUE NOT NULL,
 SHApassword VARCHAR(256) NOT NULL);

CREATE TABLE Seller (
  uid INTEGER NOT NULL PRIMARY KEY REFERENCES Person(uid),
  numtrade INTEGER NOT NULL CHECK (numtrade >= 0)
);

CREATE TABLE Clothes (
  cid INTEGER NOT NULL PRIMARY KEY,
  sellerid INTEGER NOT NULL REFERENCES Seller(uid),
  orginalprice DECIMAL(10,2),
  sellprice DECIMAL(10,2) NOT NULL,
  condition VARCHAR(20) NOT NULL CHECK (
    condition = 'new' OR
    condition = 'nearly new' OR
    condition = 'used' OR
    condition = 'damaged' OR
    condition = 'usable'
  ),
  size VARCHAR(3) NOT NULL CHECK (
    size = 'xs' OR
    size = 's' OR
    size = 'm' OR
    size = 'l' OR
    size = 'xl'
  ),
  color VARCHAR(256),
  brand VARCHAR(256),
  ctype VARCHAR(256),
  description VARCHAR(256),
  closed BOOLEAN NOT NULL,
  imgpath VARCHAR(256)
);

CREATE TABLE Bidding (
  uid INTEGER NOT NULL REFERENCES Person(uid),
  cid INTEGER NOT NULL PRIMARY KEY REFERENCES Clothes(cid),
  biddingprice DECIMAL(10, 2) NOT NULL,
  closed BOOLEAN NOT NULL DEFAULT FALSE,
  openuntil TIMESTAMP NOT NULL
);

CREATE FUNCTION Post_Bidding() RETURNS TRIGGER AS $$
BEGIN
  INSERT INTO Bidding VALUES(
    NEW.sellerid,
    NEW.cid,
    NEW.sellprice,
    FALSE,
    CURRENT_TIMESTAMP + INTERVAL '7' DAY
  );
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER Post_Bidding
  AFTER INSERT ON Clothes
  FOR EACH ROW
  EXECUTE PROCEDURE Post_Bidding();

CREATE FUNCTION Bidding_Update() RETURNS TRIGGER AS $$
BEGIN
  IF (TG_OP = 'DELETE') THEN
    RAISE EXCEPTION 'Illegal Operation';
  END IF;
  IF EXISTS(SELECT * FROM Bidding AS b WHERE b.cid = NEW.cid AND b.openuntil < CURRENT_TIMESTAMP) THEN
    RAISE EXCEPTION 'Illegal time';
  END IF;
  IF EXISTS(SELECT * FROM Bidding AS b WHERE b.cid = NEW.cid AND b.biddingprice >= NEW.biddingprice) THEN
    RAISE EXCEPTION 'Illegal Bidding';
  END IF;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER Bidding_Update
  BEFORE UPDATE OR DELETE OR INSERT ON Bidding
  FOR EACH ROW
  EXECUTE PROCEDURE Bidding_Update();