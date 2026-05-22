import json
import urllib.parse
import boto3
import pandas as pd
import awswrangler as wr
import io


# =========================================================
# MAPEO DE COLUMNAS (INGLÉS → ESPAÑOL)
# =========================================================

TRANSLATION_ENTSOE = {
    "datetime": "fecha_hora",
    "Biomass": "biomasa_mwh",
    "Fossil Brown coal/Lignite": "carbon_marron_lignito_mwh",
    "Fossil Coal-derived gas": "gas_derivado_carbon_mwh",
    "Fossil Gas": "gas_natural_mwh",
    "Fossil Hard coal": "hulla_antracita_mwh",
    "Fossil Oil": "petroleo_mwh",
    "Fossil Oil shale": "esquisto_bituminoso_mwh",
    "Fossil Peat": "turba_mwh",
    "Geothermal": "geotermica_mwh",
    "Hydro Run-of-river and poundage": "hidraulica_fluyente_mwh",
    "Hydro Water Reservoir": "hidraulica_embalse_mwh",
    "Marine": "maritima_mwh",
    "Nuclear": "nuclear_mwh",
    "Other": "otras_tecnologias_mwh",
    "Other renewable": "otras_renovables_mwh",
    "Solar": "solar_fotovoltaica_mwh",
    "Waste": "residuos_mwh",
    "Wind Offshore": "eolica_marina_mwh",
    "Wind Onshore": "eolica_terrestre_mwh"
}

BUCKET_PLATA = "gdc-pi-plata"


# =========================================================
# LAMBDA HANDLER
# =========================================================

def lambda_handler(event, context):

    bucket_bronce = event["Records"][0]["s3"]["bucket"]["name"]

    key_bronce = urllib.parse.unquote_plus(
        event["Records"][0]["s3"]["object"]["key"],
        encoding="utf-8"
    )

    # Ejemplo de ruta: entsoe/year=2020/raw_data_2020.csv
    year = key_bronce.split("=")[1].split("/")[0]

    try:
        # Lectura desde S3 (capa bronce)
        df_raw = wr.s3.read_csv(
            path=f"s3://{bucket_bronce}/{key_bronce}"
        )

        # Conversión temporal
        df_raw["Datetime"] = pd.to_datetime(df_raw["Datetime"], utc=True)
        df_raw = df_raw.set_index("Datetime")

        # Filtrado y renombrado de columnas relevantes
        cols = [
            c for c in TRANSLATION_ENTSOE.keys()
            if c in df_raw.columns
        ]

        df_final = df_raw[cols].rename(columns=TRANSLATION_ENTSOE)

        # Agregación diaria
        df_daily = (
            df_final
            .resample("D")
            .sum()
            .reset_index()
        )

        df_daily["fecha"] = df_daily["Datetime"].dt.date
        df_daily.drop(columns=["Datetime"], inplace=True)

        # Escritura en capa plata (Parquet)
        output_path = (
            f"s3://{BUCKET_PLATA}/"
            f"energia_consolidada/year={year}/energia_{year}.parquet"
        )

        wr.s3.to_parquet(
            df=df_daily,
            path=output_path,
            index=False
        )

    except Exception as e:
        print(f"ERROR: {e}")