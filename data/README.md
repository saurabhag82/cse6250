BIGQuery SQL to get static.csv file

SELECT
  t1.icustay_id,
  t1.subject_id,
  t1.hadm_id,
  t1.gender,
  t1.admission_age,
  t1.ethnicity,
  t2.first_careunit,
  t1.dischtime,
  t1.dod as deathtime,
  t1.intime
FROM
  `physionet-data.mimiciii_derived.icustay_detail` AS t1
INNER JOIN
  `physionet-data.mimiciii_clinical.icustays` AS t2
ON
  t1.icustay_id = t2.icustay_id;


SELECT
  t1.icustay_id,
  t1.subject_id,
  t1.hadm_id,
  t1.gender,
  t1.admission_age,
  t1.ethnicity,
  t2.first_careunit,
  t1.dischtime,
  t1.dod AS deathtime,
  t1.intime,
  t3.charttime AS timecmo_nursingnote
FROM
  `physionet-data.mimiciii_derived.icustay_detail` AS t1
INNER JOIN
  `physionet-data.mimiciii_clinical.icustays` AS t2
ON
  t1.icustay_id = t2.icustay_id
INNER JOIN
  `physionet-data.mimiciii_notes.noteevents` AS t3
ON
  t1.hadm_id = t3.hadm_id
WHERE
  (t3.category LIKE '%Nursing%' or t3.category LIKE '%Nursing/other%')


SELECT
  t1.*,
  t3.charttime AS timecmo_nursingnote
FROM
  `physionet-data.mimiciii_derived.code_status` AS t1
INNER JOIN
  `physionet-data.mimiciii_notes.noteevents` AS t3
ON
  t1.hadm_id = t3.hadm_id
  AND t1.subject_id = t3.subject_id
WHERE
  (t3.category = "Nursing" OR t3.category = "Nursing/other")
