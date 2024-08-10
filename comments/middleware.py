
import logging
from django.urls import resolve
from django.utils.deprecation import MiddlewareMixin

# Промежуточное ПО для логирования входящих запросов и исходящих ответов
class LogMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # Логирование информации о входящем запросе
        resolved_path_info = resolve(request.path_info)
        logging.info(
            f"Request received: {request} View name: {resolved_path_info.view_name} Route: {resolved_path_info.route}"
        )

    def process_response(self, request, response):
        # Логирование информации о сформированном ответе
        logging.info(f"Response generated for request: {request} Response: {response}")
        return response
