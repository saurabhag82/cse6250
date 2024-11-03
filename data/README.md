BIGQuery SQL to get static.csv file

SELECT
  t1.icustay_id,
  t1.subject_id,
  t1.hadm_id,
  t1.gender,
  t1.admission_age,
  t1.ethnicity,
  t2.first_careunit
FROM
  `physionet-data.mimiciii_derived.icustay_detail` AS t1
INNER JOIN
  `physionet-data.mimiciii_clinical.icustays` AS t2
ON
  t1.icustay_id = t2.icustay_id;
