CREATE TABLE barang (
	id_barang serial PRIMARY KEY,
	jenis CHAR (255),
	merek CHAR (255),
	nama CHAR (255),
	harga float8,
	id_tag CHAR (255)
);

CREATE TABLE pembelian (
	ID_pembelian serial PRIMARY KEY,
	ID_barang integer,
	Warna_barang CHAR(255),
	Merek CHAR (255),
	Jenis CHAR(255),
	Harga float8,
	Universal_size integer,
	Diskon integer,
	Rating float8
);