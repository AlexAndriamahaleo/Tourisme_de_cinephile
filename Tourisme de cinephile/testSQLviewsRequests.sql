-- CLASSIC TU CONNAIS
SELECT *
FROM tournagesdefilmsparis2011;

SELECT *
FROM liste_des_sites_des_hotspots_paris_wifi;

SELECT *
FROM velib_a_paris_et_communes_limitrophes;

-- COUPLE LES VELIB ET LES LIEUX DE TOURNAGES EN FONCTION DE
-- LEUR ARRONDISSEMENTS
SELECT DISTINCT
  name                                          AS nom,
  titre                                         AS film_tourne,
  velib_a_paris_et_communes_limitrophes.adresse AS adresse,
  ardt                                          AS code_postal,
  lattitude,
  longitude
FROM velib_a_paris_et_communes_limitrophes
  INNER JOIN tournagesdefilmsparis2011 ON ardt = cp;

-- CONCAT() EN SQLITE
-- ICI CRÉE UNE COLONNE À PARTIR DE 2 COLONNES D'UNE MÊMME BASE
SELECT
  name,
  lattitude || ', ' || longitude    AS geo_point_velib,
  tournagesdefilmsparis2011.adresse AS film_adr,
  xy                                AS geo_point_tournages
FROM velib_a_paris_et_communes_limitrophes
  INNER JOIN tournagesdefilmsparis2011
    ON
      lattitude || ', ' || longitude > xy;

-- CAST(), SPLIT(), OMMIT EMPTY VALUES EN SQLITE
SELECT
  CAST(substr(xy, 1, pos - 1) AS FLOAT) AS lattitude,
  -- STRING TO FLOAT FOR GEO_POINT
  CAST(substr(xy, pos + 1) AS FLOAT)    AS longitude,
  -- STRING TO FLOAT FOR GEO_POINT
  *
FROM
  (SELECT
     *,
     instr(xy, ',') AS pos
   FROM tournagesdefilmsparis2011
   WHERE trim(xy) != '') -- DO NOT SELECT EMPTY VALUE
WHERE
  -- +/- 1 pour avoir une precision "proche" sur le lieu
  lattitude > 48.89
  AND lattitude < 48.90
  -- +/- 2 ou 3 pour avoir une precision "proche" sur le lieu
  AND longitude > 2.30
  AND longitude < 2.33
ORDER BY lattitude, longitude;