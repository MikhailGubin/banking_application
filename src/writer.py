from pandas import DataFrame


def writing_dataframe_to_dict(df_excel_file: DataFrame) -> list[dict]:
    """
    Считывает финансовые операций из Excel-файла,
    выдаёт объект DataFrame список словарей с транзакциями
    """
    try:
        transactions_dict = df_excel_file.to_dict(orient="records")
    except Exception as error_message:
        print(f"\nВозникла ошибка при записи содержимого Excel-файла в словарь. Текст ошибки: \n{error_message}")
        return [{}]
    if not transactions_dict:
        print("\nВ Excel-файле нет данных")
        return [{}]
    return transactions_dict
