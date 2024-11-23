from datetime import datetime

from src.core.abstract_logic import abstract_logic
from src.core.event_type import event_type
from src.core.logging_level import logging_level
from src.core.validator import validator, operation_exception
from src.logics.observe_service import observe_service
from src.settings_manager import settings_manager


class logging(abstract_logic):
    __settings_manager: settings_manager = None
    __log_file_path: str = "application.log"

    def __init__(self, manager: settings_manager):
        validator.validate(manager, settings_manager)

        observe_service.append(self)

        self.__settings_manager = manager
        self.current_logging_level = logging_level(self.__settings_manager.current_settings.logging_level)

    def set_exception(self, ex: Exception):  # pragma: no cover
        super().set_exception(ex)

    def handle_event(self, type: event_type, params):
        super().handle_event(type, params)

        if type in {event_type.LOG_INFO, event_type.LOG_ERROR, event_type.LOG_DEBUG}:
            self._log_event(type, params)

    def _log_event(self, type: event_type, params):
        """
        Логирует событие, если оно соответствует текущему уровню логирования
        """
        if self._should_log(type):
            log_message = self._format_log_message(type, params)
            self._write_log(log_message)

    def _should_log(self, type: event_type) -> bool:
        """
        Определяет, нужно ли логировать событие на основе текущего уровня логирования
        """
        if self.current_logging_level == logging_level.DEBUG:
            return type in {event_type.LOG_DEBUG, event_type.LOG_ERROR, event_type.LOG_INFO}
        elif self.current_logging_level == logging_level.ERROR:
            return type in {event_type.LOG_ERROR, event_type.LOG_INFO}
        elif self.current_logging_level == logging_level.INFO:
            return type == event_type.LOG_INFO
        return False

    @staticmethod
    def _format_log_message(type: event_type, params) -> str:
        """
        Форматирует сообщение для логирования
        """
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return f"{current_time} [{type.name}] {params}"

    def _write_log(self, message: str):
        """
        Записывает лог-сообщение в файл
        """
        try:
            with open(self.__log_file_path, 'a', encoding='utf-8') as log_file:
                log_file.write(message + "\n")
        except Exception as ex:
            raise operation_exception(f"Error writing to log file: {ex}")
        #print(message)
