import hashlib
import logging

from django.http import HttpResponse
from django.shortcuts import render
from django.urls import resolve
from django.utils.deprecation import MiddlewareMixin


class LogMiddleware(MiddlewareMixin):

    def process_request(self, request):
        # процесинг запроса
        resolved_path_info = resolve(request.path_info)
        logging.info(
            'Request {} View name {} route {}'
            .format(request, resolved_path_info.view_name, resolved_path_info.route))

    def process_response(self, request, response):
        # процесинг ответа
        logging.info('For request {} response {}'.format(request, response))
        return response

# def process_view(self, request, view_func, view_args, view_kwargs):
    #
    #     print('proccess {}'.format(view_func))
    #     return view_func(request, *view_args, **view_kwargs)

class RawDataMiddleware(MiddlewareMixin):

    def process_request(self, request):
        hashing = hashlib.sha256(str(request).encode()).hexdigest()
        request.META['hash'] = hashing
        logging.info('  request.META with hash: {}'.format(request.META['hash']))

class IdentifyResponseMiddleware(MiddlewareMixin):

    def process_response(self, request, response):
        hash_value = request.META.get('hash', '')
        response['hash-value'] = hash_value
        logging.info('  response with hash: {}'.format(response['hash-value']))
        return response