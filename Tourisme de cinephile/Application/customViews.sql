-- VUES SUR LES TROIS TABLE
DROP VIEW IF EXISTS films_paris;
CREATE VIEW IF NOT EXISTS films_paris
  AS
    SELECT
      titre,
      realisateur,
      adresse,
      organisme_demandeur,
      type_de_tournage,
      ardt,
      substr(xy, 1, pos - 1) AS lattitude,
      substr(xy, pos + 1)    AS longitude
    FROM
      (SELECT
         *,
         instr(xy, ',') AS pos
       FROM tournagesdefilmsparis2011
       WHERE trim(xy) != '');

DROP VIEW IF EXISTS wifi_paris;
CREATE VIEW IF NOT EXISTS wifi_paris
  AS
    SELECT
      nom_site,
      adresse,
      code_site,
      arrondissement,
      substr(geo_point_2d, 1, pos - 1) AS lattitude,
      substr(geo_point_2d, pos + 1)    AS longitude
    FROM
      (SELECT
         *,
         instr(geo_point_2d, ',') AS pos
       FROM liste_des_sites_des_hotspots_paris_wifi
       WHERE trim(geo_point_2d) != '');

DROP VIEW IF EXISTS velib_paris;
CREATE VIEW IF NOT EXISTS velib_paris
  AS
    SELECT
      name,
      adresse,
      cp,
      substr(wgs84, 1, pos - 1) AS lattitude,
      substr(wgs84, pos + 1)    AS longitude
    FROM
      (SELECT
         *,
         instr(wgs84, ',') AS pos
       FROM velib_a_paris_et_communes_limitrophes
       WHERE trim(wgs84) != '');

-- VUE POUR SAVOIR - VELIB PROCHE DE LIEU DE TOURNAGE (ARRONDISSEMENTS, TITRE, REALISATEUR)
DROP VIEW IF EXISTS movies_velib;
CREATE VIEW IF NOT EXISTS movies_velib
  AS
    SELECT DISTINCT
      name                   AS Nom_de_la_station,
      velib.adresse          AS Adresse,
      lattitude,
      longitude,
      cp                     AS arrondissement,
      realisateur,
      films.type_de_tournage AS type_film
    FROM velib_a_paris_et_communes_limitrophes AS velib
      INNER JOIN tournagesdefilmsparis2011 AS films
        ON cp == films.ardt
    ORDER BY arrondissement;

-- VUE POUR SAVOIR - SPOT WIFI PROCHE DE LIEU DE TOURNAGE (ARRONDISSMENT, TITRE, REALISATEUR)
DROP VIEW IF EXISTS movies_wifi;
CREATE VIEW IF NOT EXISTS movies_wifi
  AS
    SELECT DISTINCT
      titre            AS nom_du_film,
      arrondissement,
      type_de_tournage AS type_film,
      realisateur,
      nom_site         AS borne_wifi,
      wifi.adresse     AS adresse_wifi,
      code_site        AS num_hotspot,
      geo_point_2d     AS coordonnees
    FROM liste_des_sites_des_hotspots_paris_wifi AS wifi
      INNER JOIN tournagesdefilmsparis2011 AS films
        ON arrondissement == ardt
    ORDER BY arrondissement;

-- VUE POUR SAVOIR - SPOT WIFI PROCHE DE STATION VELIB
CREATE VIEW IF NOT EXISTS velib_near_wifi
  AS
    SELECT DISTINCT
      velibs.cp,
      nom_site                                        AS nom_wifi,
      liste_des_sites_des_hotspots_paris_wifi.adresse AS adresse_wifi,
      velibs.name                                     AS velib_name,
      velibs.adresse                                  AS velib_adresse,
      velibs.wgs84                                    AS velib_geopos
    FROM liste_des_sites_des_hotspots_paris_wifi
      INNER JOIN velib_a_paris_et_communes_limitrophes AS velibs
        ON arrondissement == cp
    ORDER BY arrondissement;