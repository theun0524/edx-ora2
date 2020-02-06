import json
import logging
import os

from django.conf import settings
from django.http import HttpResponseNotFound
from django.shortcuts import Http404, HttpResponse, redirect
from django.utils import timezone
from django.views.decorators.http import require_http_methods

from . import exceptions
from .backends.base import BaseBackend, Settings
from .backends.s3 import _connect_to_s3

logger = logging.getLogger("openassessment.fileupload.api")


@require_http_methods(["GET"])
def s3_storage(request, key):
    """
    Uploading and download files to the local filesystem backend.
    """
    bucket_name = Settings.get_bucket_name()
    path, num = key.rsplit('/', 1)
    try:
        conn = _connect_to_s3()
        bucket = conn.get_bucket(bucket_name)
        s3_key = bucket.get_key(key)
        meta_key = bucket.get_key(path + '/metadata.json')
        if meta_key:
            metadata = json.loads(meta_key.get_contents_as_string())
            file_name = metadata[int(num)]
        else:
            logger.exception(
                u"meta_key does not exist."
            )
            raise
        logger.info(
            u"filename={file_name}".format(file_name=file_name)
        )
        response_headers = {
          'response-content-type': 'application/force-download',
          'response-content-disposition':'attachment;filename="%s"' % file_name
        }
        response = redirect(s3_key.generate_url(
            expires_in=BaseBackend.DOWNLOAD_URL_TIMEOUT,
            response_headers=response_headers
        ))
        return response
    except Exception as ex:
        return HttpResponseNotFound()
