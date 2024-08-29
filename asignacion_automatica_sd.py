import json
import requests
import datetime
import warnings

warnings.filterwarnings("ignore")
fecha_hora_actual = datetime.datetime.now()
 
url = "https://kionetworks.n.technology/api/v3/requests"
headers ={"authtoken":"F763657A-5B93-4B47-BE23-48A2102D4EDD"}
input_data = '''{
    "list_info": {
        "sort_order": "asc",
        "row_count": 100,
        "start_index": 1,
        "get_total_count": "true",
        "fields_required": [
            "account",
            "id",
            "status",
            "group",
            "technician",
            requester,
        ],
        "search_criteria": [
            {
                "field": "group.name",
                "condition": "is",
                "values": [
                    "IT - Bsa"
                ],
                "logical_operator": "AND"
            },
            {
                "field": "status.name",
                "condition": "is",
                "values": [
                    "Asignado"
                ],
                "logical_operator": "AND"
            }
        ]
    }
}'''
params = {'input_data': input_data}
response = requests.get(url,headers=headers,params=params,verify=False)
data = json.loads(response.text)


fecha_ejecucion = f"\n\nEjecucion: {fecha_hora_actual}"
with open("log_asignacion_sd.txt", "a") as archivo:
	archivo.write(fecha_ejecucion)

for request in data['requests']:

	nticket = request.get('id')
	technician = request.get('technician')
	url = f"https://kionetworks.n.technology/api/v3/requests/{nticket}"
	solicitante = request.get('requester')
	solicitante = solicitante["name"]
    

	if technician is not None:

		tecnico = technician["name"]
		
		if solicitante != "Site24x7":

			input_data_curso = '''{
		        "request": {
		            "status": {
		                "name": "En curso"
		            },
		        "note_comments": {
		            "description": "En curso",
		            	"mark_first_response": true,
		           }
		        }
		    }'''


			data = {'input_data': input_data_curso}
			response = requests.put(url,headers=headers,data=data,verify=False)
			data_curso = json.loads(response.text)
			status = data_curso["response_status"]["status"]
			resultado = f"El ticket {nticket} ha sido actualizado al estado 'En curso' con exito: {status}"
			with open("log_asignacion_sd.txt", "a") as archivo:
				archivo.write(resultado)

			input_data = '''{
		        "request": {
		            "status": {
		                "name": "Pendiente por usuario"
		            },
		            "note_comments": {
		                    "description": "En proceso de atención",
		                    "mark_first_response": true,
		           }
		        }
		    }'''

			data = {'input_data': input_data}
			response = requests.put(url,headers=headers,data=data,verify=False)
			data = json.loads(response.text)
			status = data["response_status"]["status"]
			resultado = f"El ticket {nticket} ha sido actualizado al estado 'Pendiente por usuario' con exito: {status}"
			with open("log_asignacion_sd.txt", "a") as archivo:
				archivo.write(resultado)

	else:

		if solicitante != "Site24x7":
                        # asignar a email_id: site24x7@kio.tech o al id: 21603
			input_data_curso = '''{
	        	"request": {
	            	"technician": {
	                	"id": "21603"
	            	},
	            	"note_comments": {
		            	"description": "En curso",
		            	"mark_first_response": true,
		           },
	            	"status": {
	                	"name": "En curso"
	            	}
	        	}
	    	}'''

			data = {'input_data': input_data_curso}
			response = requests.put(url,headers=headers,data=data,verify=False)
			data_curso = json.loads(response.text)
			status = data_curso["response_status"]["status"]
			resultado = f"El ticket {nticket} ha sido actualizado al estado 'En curso' con exito: {status}"
			with open("log_asignacion_sd.txt", "a") as archivo:
				archivo.write(resultado)

			input_data = '''{
		        "request": {
		            "status": {
		                "name": "Pendiente por usuario"
		            },
		            "note_comments": {
		            	"description": "En proceso de atención",
		            	"mark_first_response": true,
		           }
		        }
		    }'''

			data = {'input_data': input_data}
			response = requests.put(url,headers=headers,data=data,verify=False)
			data = json.loads(response.text)
			status = data["response_status"]["status"]
			resultado = f"El ticket {nticket} ha sido actualizado al estado 'Pendiente por usuario' con exito: {status}"
			with open("/opt/AsignacionAutomaticaTicketsBsa/log_asignacion_sd.txt", "a") as archivo:
				archivo.write(resultado)
