import json
import urllib.parse
import boto3
import pandas as pd
import holidays
from datetime import datetime
import io

s3_client = boto3.client("s3") # lo creo fuera del handler para poder reutilizar la conexión

PROVINCIAS_CCAA = {
    # Andalucía (AN)
    "ALMERÍA": "AN", "CÁDIZ": "AN", "CÓRDOBA": "AN", "GRANADA": "AN", 
    "HUELVA": "AN", "JAÉN": "AN", "MÁLAGA": "AN", "SEVILLA": "AN",
    # Aragón (AR)
    "HUESCA": "AR", "TERUEL": "AR", "ZARAGOZA": "AR",
    # Principado de Asturias (AS)
    "ASTURIAS": "AS",
    # Canarias (CN)
    "LAS PALMAS": "CN", "SANTA CRUZ DE TENERIFE": "CN",
    # Cantabria (CB)
    "CANTABRIA": "CB",
    # Castilla y León (CL)
    "ÁVILA": "CL", "BURGOS": "CL", "LEÓN": "CL", "PALENCIA": "CL", 
    "SALAMANCA": "CL", "SEGOVIA": "CL", "SORIA": "CL", "VALLADOLID": "CL", "ZAMORA": "CL",
    # Castilla-La Mancha (CM)
    "ALBACETE": "CM", "CIUDAD REAL": "CM", "CUENCA": "CM", "GUADALAJARA": "CM", "TOLEDO": "CM",
    # Cataluña (CT)
    "BARCELONA": "CT", "GIRONA": "CT", "GERONA": "CT", "LLEIDA": "CT", "LÉRIDA": "CT", "TARRAGONA": "CT",
    # Extremadura (EX)
    "BADAJOZ": "EX", "CÁCERES": "EX",
    # Galicia (GA)
    "A CORUÑA": "GA", "LA CORUÑA": "GA", "LUGO": "GA", "OURENSE": "GA", "ORENSE": "GA", "PONTEVEDRA": "GA",
    # Illes Balears (IB)
    "BALEARES": "IB", "ILLES BALEARS": "IB", "ISLAS BALEARES": "IB",
    # La Rioja (RI)
    "LA RIOJA": "RI",
    # Comunidad de Madrid (MD)
    "MADRID": "MD",
    # Región de Murcia (MC)
    "MURCIA": "MC",
    # Comunidad Foral de Navarra (NC)
    "NAVARRA": "NC",
    # País Vasco (PV)
    "ÁLAVA": "PV", "ARABA": "PV", "GUIPÚZCOA": "PV", "GIPUZKOA": "PV", "VIZCAYA": "PV", "BIZKAIA": "PV",
    # Comunidad Valenciana (VC)
    "ALICANTE": "VC", "ALACANT": "VC", "CASTELLÓN": "VC", "CASTELLÓ": "VC", "VALENCIA": "VC", "VALÈNCIA": "VC",
    # Ciudades Autónomas
    "CEUTA": "CE",
    "MELILLA": "ML"
}

BUCKET_DESTINO = "gdc-pi-meteo-y-vacaciones"

def lambda_handler(event, context):
    bucket = event["Records"][0]["s3"]["bucket"]["name"]
    key = urllib.parse.unquote_plus(event["Records"][0]["s3"]["object"]["key"], encoding="utf-8")

    print(f"Procesando: {key} de {bucket}")

    try:
        response = s3_client.get_object(Bucket = bucket, Key = key)
        path_splitted = key.split("/")

        year = int(path_splitted[0].replace("Aemet", ""))
        month = int(path_splitted[1])
        day = int(path_splitted[2].replace(".csv", ""))

        if year < 2020:
            print("ERROR: El fichero era anterior a 2020.")
            return
        
        df = pd.read_csv(io.BytesIO(response["Body"].read()))

        # Si no pongo la fecha en formato de pandas da errores
        current_date = pd.to_datetime(f"{year}-{month}-{day}")
        df["fecha"] = current_date

        # Separa la provincia en 2 partes (Alacant/Alicante) para quedarse con la última
        df["Provincia_Limpia"] = df["Provincia"].str.split("/").str[-1]
        df["ccaa_codigo"] = df["Provincia_Limpia"].str.strip().str.upper().map(PROVINCIAS_CCAA)
        
        df["es_festivo"] = 0

        # Es posible que deje algunas sin mapear sin darme cuenta, así que me dejo de problemas con esto
        ccaa_dataset = df["ccaa_codigo"].dropna().unique()

        for ccaa in ccaa_dataset:
            # Obtiene festivos para la comunidad autónoma específica
            country_holidays = holidays.ES(subdiv = ccaa, years = year)

            if current_date in country_holidays:
                df.loc[df["ccaa_codigo"] == ccaa, "es_festivo"] = 1
        
        s3_client.put_object(
            Bucket = BUCKET_DESTINO,
            Key = f"{key}",
            Body = df.to_csv(index = False),
            ContentType = "text/csv"
        )
        print(f"Fichero procesado y almacenado en: {BUCKET_DESTINO}/{key}")
    except Exception as e:
        print(e)
        raise e