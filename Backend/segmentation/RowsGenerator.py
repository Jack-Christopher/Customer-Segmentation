import random

i = 10

correos = ["rsantisteban@unsa.edu.pe", "jhuaihuah@unsa.edu.pe", "lsantet@unsa.edu.pe"]
priority = ["0","1","2","3"]
stage_id = ["1","2","3","4"]
partner_id = ["7","3","8","9"]
partner_name = ["Ejemplo", "NULL", "Ejemplo2", "Propuestas"]
month = ["01","02","03","04","05","06","07","08","09","10","11","12"]
day = ["01","02","03","04","05","06","07","08","09","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","26","27","28"]

queries = ""


for i in range(i, 2000):

	id = str(i)
	correo = correos[random.randint(0,2)]
	nombre = "Oportunidad"+str(i)
	priority_chosen = priority[random.randint(0,3)]
	stage_id_chosen = stage_id[random.randint(0,3)]

	expected_revenue = str(random.randint(1000,40000)/10)
	probability = str(random.randint(800,980)/10)

	partner_index = random.randint(0,3)

	partner_id_chosen = partner_id[partner_index]
	partner_name_chosen = partner_name[partner_index]

	month_chosen = month[random.randint(0,11)]
	day_chosen = day[random.randint(0,27)]

	date1 = "2021-"+month_chosen+"-"+day_chosen+" 18:39:06"
	date2 = "2021-"+month_chosen+"-"+day_chosen+" 18:39:04.726888"

	queries += "INSERT INTO crm_lead(id,campaign_id, source_id, medium_id, message_main_attachment_id, phone_sanitized, email_normalized, message_bounce, email_cc, name , user_id , team_id , company_id , referred , description , active , type , priority , stage_id , color , expected_revenue , prorated_revenue , recurring_revenue , recurring_plan , recurring_revenue_monthly , recurring_revenue_monthly_prorated , date_closed , date_action_last , date_open , day_open , day_close , date_last_stage_update , date_conversion , date_deadline , partner_id , contact_name , partner_name , function , title , email_from , phone , mobile , phone_state , email_state , website , lang_id , street , street2 , zip , city , state_id , country_id , probability , automated_probability , lost_reason , create_uid , create_date , write_uid , write_date , reveal_id , iap_enrich_done , lead_mining_request_id)\n"
	queries += "VALUES ("+id+", NULL, NULL, NULL, NULL, NULL, '"+correo+"', 0, NULL, '"+nombre+"', 2, 1, 1, NULL, NULL, true, 'opportunity', "+priority_chosen+", "+stage_id_chosen+", 0, "+expected_revenue+", "+expected_revenue+", NULL, NULL, 0, 0, NULL, NULL, '"+date1+"', 0, 0, '"+date1+"', NULL, NULL, "+partner_id_chosen+", NULL, '"+partner_name_chosen+"', NULL, NULL, '"+correo+"', NULL, NULL, NULL, 'correct', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, "+probability+", "+probability+", NULL, 2, '"+date2+"', 2, '"+date2+"', NULL, NULL, NULL);"
	queries += "\n\n\n"

print(queries)

with open('queries.txt', 'w') as f:
    f.write(queries)