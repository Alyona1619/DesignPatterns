@echo off

:: Запрос для получения форматов отчетов
curl -X GET "http://localhost:8001/api/reports/formats"

:: Запрос для получения отчета по категории и формату
curl -X GET "http://localhost:8001/api/reports/nomenclature/JSON"

:: Запрос для фильтрации данных по категории
curl -X POST "http://localhost:8001/api/filter/nomenclature" -H "Content-Type: application/json" -d "{\"name\": \"ука\", \"id\": \"\", \"filter_option\": \"like\"}"

:: Запрос для получения периода блокировки
curl -X GET "http://localhost:8001/api/settings/block_period"

:: Запрос для установки нового периода блокировки
curl -X POST "http://localhost:8000/api/settings/new_block_period" -H "Content-Type: application/json" -d "{\"block_period\": \"23.11.2024\"}"

:: Запрос для получения оборотно-сальдовой ведомости по складу
curl -X GET "http://localhost:8001/api/tbs/2024-03-15/2024-11-23/WH_1"

:: Запрос для сохранения данных в файл
curl -X POST "http://localhost:8000/api/save_data"

:: Запрос для выгрузки данных из файла
curl -X POST "http://localhost:8000/api/load_data"

