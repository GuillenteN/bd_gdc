import json
import pandas as pd
import awswrangler as wr


# =========================================================
# CONFIGURACIÓN DE BUCKETS
# =========================================================

BUCKET_METEO_VACACIONES = "gdc-pi-meteo-y-vacaciones"
BUCKET_PLATA = "gdc-pi-plata"


# =========================================================
# LAMBDA HANDLER
# =========================================================

def lambda_handler(event, context):

    year = event.get("year", None)

    if not year:
        raise ValueError("No se ha especificado el año.")

    print(f"Iniciando proceso de compactación para el año: {year}")

    try:
        # Lectura de datos brutos en S3 (capa bronce)
        source_path = f"s3://{BUCKET_METEO_VACACIONES}/Aemet{year}/"
        df_anual = wr.s3.read_csv(path=source_path)

        # Validación básica
        if df_anual.empty:
            print("El dataset anual está vacío.")
            return

        # Ruta de salida en capa plata
        output_path = (
            f"s3://{BUCKET_PLATA}/"
            f"aemet_consolidada/year={year}/aemet_historico_{year}.parquet"
        )

        # Escritura en formato optimizado
        wr.s3.to_parquet(
            df=df_anual,
            path=output_path,
            index=False
        )

        print(f"Compactación completada correctamente para el año {year}")

    except Exception as e:
        print(f"ERROR durante la compactación: {e}")
        raise