#Query 1 
SELECT p.Name, p.Age , SUM(DISTINCT t.Cost) AS SumCost
FROM patient p , stay s , undergoes un, treatment t
WHERE p.Gender = "Male" AND p.Age>30 AND p.Age<40 AND 
	(SELECT COUNT(s.patient)
	 FROM stay s
	 WHERE s.patient = p.SSN) > 1
AND s.patient =p.SSN AND s.StayID = un.stay AND un.treatment = t.Code;

#Query 2 
SELECT distinct n.name
FROM on_call vardia, block b, nurse n
WHERE n.EmployeeID = vardia.Nurse 
AND vardia.OnCallStart >= '2008-04-20 23:22:00' AND vardia.OnCallEnd < '2009-06-04 11:00:00'
AND vardia.BlockFloor >= 4 and vardia.BlockFloor <= 7
GROUP BY b.Blockcode
HAVING (b.BlockCode) > 1;


#Query 3
SELECT DISTINCT p.name
FROM patient p , vaccination v , vaccines vacc
WHERE p.Gender = 'Female' AND p.Age > 40 
AND p.SSN = v.patient_SSN 
AND vacc.vax_name = v.vaccines_vax_name  
GROUP BY p.name , vacc.num_of_doses
HAVING count(v.vaccines_vax_name) = vacc.num_of_doses;


#Query 4
SELECT m.Name, m.Brand, count(*) AS Number_Of_Patients
FROM prescribes p, medication m, patient pa
WHERE p.medication = m.Code AND p.patient = pa.SSN 
GROUP BY p.Patient
HAVING count(*) > 1;


#Query 5 
SELECT p.name
FROM patient p , vaccination v , vaccines vacc 
WHERE  p.SSN = v.patient_SSN 
AND vacc.vax_name = v.vaccines_vax_name  
GROUP BY p.name , vacc.num_of_doses
HAVING count(v.vaccines_vax_name) = vacc.num_of_doses;
#until the part where patients have done all the vaccine doses 


#Query 6
(SELECT 'Yes' AS Answer
FROM stay s 
WHERE EXISTS (SELECT *
			  FROM room r, stay s 
			  WHERE s.room = r.RoomNumber 
		      AND s.StayStart >= '2013-01-01 00:00:00' 
              AND s.StayEnd < '2014-01-01 00:00:00'))
UNION 
(SELECT 'Yo'
WHERE NOT EXISTS (SELECT * 
				  FROM room r, stay s 
                  WHERE s.room = r.RoomNumber 
                  AND s.StayStart >= '2013-01-01 00:00:00' 
                  AND s.StayEnd < '2014-01-01 00:00:00'));


#Query 7
select p.name 
from physician p , trained_in t1 , treatment t2
where t1.Speciality = t2.Code
and t1.Physician = p.EmployeeID
and p.Position = 'PATHOLOGY';
#Doctors that have been trained in Pathology 


#Query 8
(SELECT p.name 
FROM patient p , vaccines vacc , vaccination v
WHERE p.SSN = v.patient_SSN 
AND vacc.vax_name = v.vaccines_vax_name  
GROUP BY p.name , vacc.num_of_doses
HAVING count(v.vaccines_vax_name) <> vacc.num_of_doses)
UNION 
(SELECT p.name
FROM patient p
WHERE p.SSN NOT IN (SELECT p2.SSN
			  FROM patient p2 , vaccination v2
			  WHERE p2.SSN = v2.patient_SSN ));  
 

#Query 9
SELECT v.vaccines_vax_name, count(v.vaccines_vax_name) AS Number_of_Vaccinations
FROM vaccination v , vaccines va
WHERE v.vaccines_vax_name = va.vax_name
GROUP BY v.vaccines_vax_name 
HAVING count(v.vaccines_vax_name)
ORDER BY count(v.vaccines_vax_name) DESC;
#Because we can't use LIMIT 1 I am displaying all the vaccines in descending order, the first one is the one that has being used the most for the vaccinations


#Query 10 
SELECT p.name
FROM physician p , trained_in t1 , treatment t2
WHERE t1.Speciality = t2.Code
AND t1.Physician = p.EmployeeID
AND t2.name = 'RADIATION ONCOLOGY'
GROUP BY p.name
HAVING count(p.name)>1;

