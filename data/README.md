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


-- This query pivots lab values taken in the first 24 hours of a patient's stay

-- Have already confirmed that the unit of measurement is always the same: null or the correct unit

SELECT
  pvt.subject_id, pvt.hadm_id, pvt.icustay_id --, hours_in, vfd.heartrate_mean
  , AVG (pvt.hours_in) AS hours_in
  , AVG(CASE WHEN label = 'ANION GAP' THEN valuenum ELSE NULL END) AS aniongap_AVG
  , AVG(CASE WHEN label = 'ALBUMIN' THEN valuenum ELSE NULL END) AS ALBUMIN_AVG
  , AVG(CASE WHEN label = 'BANDS' THEN valuenum ELSE NULL END) AS bands_AVG
  , AVG(CASE WHEN label = 'BICARBONATE' THEN valuenum ELSE NULL END) AS bicarbonate_AVG
  , AVG(CASE WHEN label = 'BILIRUBIN' THEN valuenum ELSE NULL END) AS bilirubin_AVG
  , AVG(CASE WHEN label = 'CREATININE' THEN valuenum ELSE NULL END) AS creatinine_AVG
  , AVG(CASE WHEN label = 'CHLORIDE' THEN valuenum ELSE NULL END) AS chloride_AVG
  , AVG(CASE WHEN label = 'GLUCOSE' THEN valuenum ELSE NULL END) AS glucose_AVG
  , AVG(CASE WHEN label = 'HEMATOCRIT' THEN valuenum ELSE NULL END) AS hematocrit_AVG
  , AVG(CASE WHEN label = 'HEMOGLOBIN' THEN valuenum ELSE NULL END) AS hemoglobin_AVG
  , AVG(CASE WHEN label = 'LACTATE' THEN valuenum ELSE NULL END) AS lactate_AVG
  , AVG(CASE WHEN label = 'PLATELET' THEN valuenum ELSE NULL END) AS platelet_AVG
  , AVG(CASE WHEN label = 'POTASSIUM' THEN valuenum ELSE NULL END) AS potassium_AVG
  , AVG(CASE WHEN label = 'PTT' THEN valuenum ELSE NULL END) AS ptt_AVG
  , AVG(CASE WHEN label = 'INR' THEN valuenum ELSE NULL END) AS inr_AVG
  , AVG(CASE WHEN label = 'PT' THEN valuenum ELSE NULL END) AS pt_AVG
  , AVG(CASE WHEN label = 'SODIUM' THEN valuenum ELSE NULL END) AS sodium_AVG
  , AVG(CASE WHEN label = 'BUN' THEN valuenum ELSE NULL END) AS bun_AVG
  , AVG(CASE WHEN label = 'WBC' THEN valuenum ELSE NULL END) AS wbc_AVG  
  , AVG (vfd.sysbp_mean) AS sysbp_mean
  , AVG (vfd.heartrate_mean) AS heartrate_mean
  , AVG (vfd.diasbp_mean) AS diasbp_mean
  , AVG (vfd.meanbp_mean) AS meanbp_mean
  , AVG (vfd.resprate_mean) AS resprate_mean
  , AVG (vfd.tempc_mean) AS tempc_mean
  , AVG (vfd.spo2_mean) AS spo2_mean
  , AVG (vfd.glucose_mean) AS glucose_mean
  , AVG (vfd.sysbp_mean) AS sysbp_mean
  , AVG (wfd.weight) AS weight

FROM
( -- begin query that extracts the data
  SELECT ie.subject_id, ie.hadm_id, ie.icustay_id,
		DATETIME_DIFF(ict.outtime_hr, ict.intime_hr, HOUR) AS hours_in
  -- here we assign labels to ITEMIDs
  -- this also fuses together multiple ITEMIDs containing the same data
  , CASE
        WHEN itemid = 50868 THEN 'ANION GAP'
        WHEN itemid = 50862 THEN 'ALBUMIN'
        WHEN itemid = 51144 THEN 'BANDS'
        WHEN itemid = 50882 THEN 'BICARBONATE'
        WHEN itemid = 50885 THEN 'BILIRUBIN'
        WHEN itemid = 50912 THEN 'CREATININE'
        WHEN itemid = 50806 THEN 'CHLORIDE'
        WHEN itemid = 50902 THEN 'CHLORIDE'
        WHEN itemid = 50809 THEN 'GLUCOSE'
        WHEN itemid = 50931 THEN 'GLUCOSE'
        WHEN itemid = 50810 THEN 'HEMATOCRIT'
        WHEN itemid = 51221 THEN 'HEMATOCRIT'
        WHEN itemid = 50811 THEN 'HEMOGLOBIN'
        WHEN itemid = 51222 THEN 'HEMOGLOBIN'
        WHEN itemid = 50813 THEN 'LACTATE'
        WHEN itemid = 51265 THEN 'PLATELET'
        WHEN itemid = 50822 THEN 'POTASSIUM'
        WHEN itemid = 50971 THEN 'POTASSIUM'
        WHEN itemid = 51275 THEN 'PTT'
        WHEN itemid = 51237 THEN 'INR'
        WHEN itemid = 51274 THEN 'PT'
        WHEN itemid = 50824 THEN 'SODIUM'
        WHEN itemid = 50983 THEN 'SODIUM'
        WHEN itemid = 51006 THEN 'BUN'
        WHEN itemid = 51300 THEN 'WBC'
        WHEN itemid = 51301 THEN 'WBC'
      ELSE null
    END as label
  , -- add in some sanity checks on the values
  -- the where clause below requires all valuenum to be > 0, so these are only upper limit checks
    CASE
      WHEN itemid = 50862 and valuenum >    10 THEN null -- g/dL 'ALBUMIN'
      WHEN itemid = 50868 and valuenum > 10000 THEN null -- mEq/L 'ANION GAP'
      WHEN itemid = 51144 and valuenum <     0 THEN null -- immature band forms, %
      WHEN itemid = 51144 and valuenum >   100 THEN null -- immature band forms, %
      WHEN itemid = 50882 and valuenum > 10000 THEN null -- mEq/L 'BICARBONATE'
      WHEN itemid = 50885 and valuenum >   150 THEN null -- mg/dL 'BILIRUBIN'
      WHEN itemid = 50806 and valuenum > 10000 THEN null -- mEq/L 'CHLORIDE'
      WHEN itemid = 50902 and valuenum > 10000 THEN null -- mEq/L 'CHLORIDE'
      WHEN itemid = 50912 and valuenum >   150 THEN null -- mg/dL 'CREATININE'
      WHEN itemid = 50809 and valuenum > 10000 THEN null -- mg/dL 'GLUCOSE'
      WHEN itemid = 50931 and valuenum > 10000 THEN null -- mg/dL 'GLUCOSE'
      WHEN itemid = 50810 and valuenum >   100 THEN null -- % 'HEMATOCRIT'
      WHEN itemid = 51221 and valuenum >   100 THEN null -- % 'HEMATOCRIT'
      WHEN itemid = 50811 and valuenum >    50 THEN null -- g/dL 'HEMOGLOBIN'
      WHEN itemid = 51222 and valuenum >    50 THEN null -- g/dL 'HEMOGLOBIN'
      WHEN itemid = 50813 and valuenum >    50 THEN null -- mmol/L 'LACTATE'
      WHEN itemid = 51265 and valuenum > 10000 THEN null -- K/uL 'PLATELET'
      WHEN itemid = 50822 and valuenum >    30 THEN null -- mEq/L 'POTASSIUM'
      WHEN itemid = 50971 and valuenum >    30 THEN null -- mEq/L 'POTASSIUM'
      WHEN itemid = 51275 and valuenum >   150 THEN null -- sec 'PTT'
      WHEN itemid = 51237 and valuenum >    50 THEN null -- 'INR'
      WHEN itemid = 51274 and valuenum >   150 THEN null -- sec 'PT'
      WHEN itemid = 50824 and valuenum >   200 THEN null -- mEq/L == mmol/L 'SODIUM'
      WHEN itemid = 50983 and valuenum >   200 THEN null -- mEq/L == mmol/L 'SODIUM'
      WHEN itemid = 51006 and valuenum >   300 THEN null -- 'BUN'
      WHEN itemid = 51300 and valuenum >  1000 THEN null -- 'WBC'
      WHEN itemid = 51301 and valuenum >  1000 THEN null -- 'WBC'
    ELSE le.valuenum
    END as valuenum

  FROM `physionet-data.mimiciii_clinical.icustays` ie

  LEFT JOIN `physionet-data.mimiciii_clinical.labevents` le
    ON le.subject_id = ie.subject_id AND le.hadm_id = ie.hadm_id
    AND le.charttime BETWEEN (DATETIME_SUB(ie.intime, INTERVAL '6' HOUR)) AND (DATETIME_ADD(ie.intime, INTERVAL '1' DAY))
    AND le.ITEMID in
    (
      -- comment is: LABEL | CATEGORY | FLUID | NUMBER OF ROWS IN LABEVENTS
      50868, -- ANION GAP | CHEMISTRY | BLOOD | 769895
      50862, -- ALBUMIN | CHEMISTRY | BLOOD | 146697
      51144, -- BANDS - hematology
      50882, -- BICARBONATE | CHEMISTRY | BLOOD | 780733
      50885, -- BILIRUBIN, TOTAL | CHEMISTRY | BLOOD | 238277
      50912, -- CREATININE | CHEMISTRY | BLOOD | 797476
      50902, -- CHLORIDE | CHEMISTRY | BLOOD | 795568
      50806, -- CHLORIDE, WHOLE BLOOD | BLOOD GAS | BLOOD | 48187
      50931, -- GLUCOSE | CHEMISTRY | BLOOD | 748981
      50809, -- GLUCOSE | BLOOD GAS | BLOOD | 196734
      51221, -- HEMATOCRIT | HEMATOLOGY | BLOOD | 881846
      50810, -- HEMATOCRIT, CALCULATED | BLOOD GAS | BLOOD | 89715
      51222, -- HEMOGLOBIN | HEMATOLOGY | BLOOD | 752523
      50811, -- HEMOGLOBIN | BLOOD GAS | BLOOD | 89712
      50813, -- LACTATE | BLOOD GAS | BLOOD | 187124
      51265, -- PLATELET COUNT | HEMATOLOGY | BLOOD | 778444
      50971, -- POTASSIUM | CHEMISTRY | BLOOD | 845825
      50822, -- POTASSIUM, WHOLE BLOOD | BLOOD GAS | BLOOD | 192946
      51275, -- PTT | HEMATOLOGY | BLOOD | 474937
      51237, -- INR(PT) | HEMATOLOGY | BLOOD | 471183
      51274, -- PT | HEMATOLOGY | BLOOD | 469090
      50983, -- SODIUM | CHEMISTRY | BLOOD | 808489
      50824, -- SODIUM, WHOLE BLOOD | BLOOD GAS | BLOOD | 71503
      51006, -- UREA NITROGEN | CHEMISTRY | BLOOD | 791925
      51301, -- WHITE BLOOD CELLS | HEMATOLOGY | BLOOD | 753301
      51300  -- WBC COUNT | HEMATOLOGY | BLOOD | 2371
    )
    AND valuenum IS NOT null AND valuenum > 0 -- lab values cannot be 0 and cannot be negative
  INNER JOIN 
    `physionet-data.mimiciii_derived.icustay_times` as ict
  ON
    ict.subject_id = ie.subject_id AND ict.hadm_id = ie.hadm_id AND ict.icustay_id = ie.icustay_id
) pvt

INNER JOIN 
    `physionet-data.mimiciii_derived.vitals_first_day` as vfd
  ON
    vfd.subject_id = pvt.subject_id AND vfd.hadm_id = pvt.hadm_id AND vfd.icustay_id = pvt.icustay_id
INNER JOIN 
    `physionet-data.mimiciii_derived.weight_first_day` as wfd
  ON
    wfd.icustay_id = pvt.icustay_id
GROUP BY pvt.subject_id, pvt.hadm_id, pvt.icustay_id--, pvt.hours_in, vfd.heartrate_mean
ORDER BY pvt.subject_id, pvt.hadm_id, pvt.icustay_id;
