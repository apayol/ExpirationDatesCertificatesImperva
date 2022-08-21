# ExpirationDatesCertificatesImperva

## WAF TELEFÓNICA ##
Script: ExpirationDates.py
Versión: 4.0
Autor: Adrián Payol Montero
Fecha: 18/08/2022

---------------------------------------------------------------------------------
Descripción:
  Uso de API Imperva v.1 y v.3 para obtención de datos sobre estado de certificados (por dominio):
- Customizados
- Auto-generado por Imperva

----------------------------------------------------------------------------------
Formato de salida:
  Entity, Site, Custom Certificate, Expiration Date Custom Certificate, Scheduled Renewal Custom Certificate, Imperva Certificate, Status Imperva Certificate, Expiration Date GlobalSign Imperva Certificate, Host where TXT must be added, TXT Certificate Imperva, Expiration Date TXT

Actualmente no existen llamadas de API para la obtención de las fechas de caducidad de los registros TXT pendientes de añadir [Expiration Date TXT]
  En cambio es posible descargarlo en .csv desde la GUI de Imperva (SSL certificates...) y con un filtrado/buscarv en excel se completa

Para la [Scheduled Renewal Custom Certificate] acudimos a la herramienta de ticketing para la extracción de Números de cambio programados

-----------------------------------------------------------------------------------
 Objetivos:
 - Seguimiento semanal de certificados
 - Notificaciones a clientes
 
 ----------------------------------------------------------------------------------
 Sobre la ejecución del .py:
 - Introducir el conjunto Api-ID y Api-KEY manualmente en el script.
 - Ejecutarlo con los parámetros: --accountid <id_de_cuenta> , por ejemplo: --accountid 1372704 (pudiendo ser estas la cuenta general o sub-cuentas)
 - Salida por pantalla, con valores separados por comas, facilmente exportable a excel para separar por columnas y aplicar filtros y ordenación
  
 ----------------------------------------------------------------------------------
  A mejorar:
  - HECHO --> Salida [Imperva Certificate]: La llamada a response_dict["data"] en casos sin certificado devuelve el conjunto vacío "None".
  Equivale al estado "Not Active" y sus estados posteriores vacíos. En futuro mejorar esa salida desde el propio script. --> HECHO en el commit de hoy

