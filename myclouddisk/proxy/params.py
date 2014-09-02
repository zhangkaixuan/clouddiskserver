# -*- coding: utf-8 -*-
'''
Created on 2013年11月28日

@author: adrian
'''

''' http status code  and its description'''

RESPONSE_REASONS = {
    100: ('Continue', ''),
    200: ('OK', ''),
    201: ('Created', ''),
    202: ('Accepted', 'The request is accepted for processing.'),
    204: ('No Content', ''),
    206: ('Partial Content', ''),
    301: ('Moved Permanently', 'The resource has moved permanently.'),
    302: ('Found', ''),
    304: ('Not Modified', ''),
    307: ('Temporary Redirect', 'The resource has moved temporarily.'),
    400: ('Bad Request', 'The server could not comply with the request since '
          'it is either malformed or otherwise incorrect.'),
    401: ('Unauthorized', 'This server could not verify that you are '
          'authorized to access the document you requested.'),
    402: ('Payment Required', 'Access was denied for financial reasons.'),
    403: ('Forbidden', 'Access was denied to this resource.'),
    404: ('Not Found', 'The resource could not be found.'),
    405: ('Method Not Allowed', 'The method is not allowed for this '
          'resource.'),
    406: ('Not Acceptable', 'The resource is not available in a format '
          'acceptable to your browser.'),
    408: ('Request Timeout', 'The server has waited too long for the request '
          'to be sent by the client.'),
    409: ('Conflict', 'There was a conflict when trying to complete '
          'your request.'),
    410: ('Gone', 'This resource is no longer available.'),
    411: ('Length Required', 'Content-Length header required.'),
    412: ('Precondition Failed', 'A precondition for this request was not '
          'met.'),
    413: ('Request Entity Too Large', 'The body of your request was too '
          'large for this server.'),
    414: ('Request URI Too Long', 'The request URI was too long for this '
          'server.'),
    415: ('Unsupported Media Type', 'The request media type is not '
          'supported by this server.'),
    416: ('Requested Range Not Satisfiable', 'The Range requested is not '
          'available.'),
    417: ('Expectation Failed', 'Expectation failed.'),
    422: ('Unprocessable Entity', 'Unable to process the contained '
          'instructions'),
    499: ('Client Disconnect', 'The client was disconnected during request.'),
    500: ('Internal Error', 'The server has either erred or is incapable of '
          'performing the requested operation.'),
    501: ('Not Implemented', 'The requested method is not implemented by '
          'this server.'),
    502: ('Bad Gateway', 'Bad gateway.'),
    503: ('Service Unavailable', 'The server is currently unavailable. '
          'Please try again at a later time.'),
    504: ('Gateway Timeout', 'A timeout has occurred speaking to a '
          'backend server.'),
    507: ('Insufficient Storage', 'There was not enough space to save the '
          'resource. Drive: %(drive)s'),
}
class StatusMap(object):
    """
    A dict-like object that returns HTTPException subclasses/factory functions
    where the given key is the status code.
    """
    def __getitem__(self, key):
        return str(key)+" "+RESPONSE_REASONS[key][0]
    
status_map = StatusMap()

#HTTP Status Code Definition
HTTPOk = status_map[200]
HTTPCreated = status_map[201]
HTTPAccepted = status_map[202]
HTTPNoContent = status_map[204]
HTTPMovedPermanently = status_map[301]
HTTPFound = status_map[302]
HTTPNotModified = status_map[304]
HTTPBadRequest = status_map[400]
HTTPUnauthorized = status_map[401]
HTTPForbidden = status_map[403]
HTTPMethodNotAllowed = status_map[405]
HTTPNotFound = status_map[404]
HTTPNotAcceptable = status_map[406]
HTTPRequestTimeout = status_map[408]
HTTPConflict = status_map[409]
HTTPLengthRequired = status_map[411]
HTTPPreconditionFailed = status_map[412]
HTTPRequestEntityTooLarge = status_map[413]
HTTPRequestedRangeNotSatisfiable = status_map[416]
HTTPUnprocessableEntity = status_map[422]
HTTPClientDisconnect = status_map[499]
HTTPServerError = status_map[500]
HTTPInternalServerError = status_map[500]
HTTPNotImplemented = status_map[501]
HTTPBadGateway = status_map[502]
HTTPServiceUnavailable = status_map[503]
HTTPInsufficientStorage = status_map[507]

#Log File Path
LogFilePath = '/var/log/myclouddisk/log.txt'
#LogFilePath = '/var/log/myclouddisk/log.txt'
#API Configuration File
APIConfigFile = '/root/myclouddisk/api/apiconfig.xml'

#Service Configuration File
# ServiceConfigFile = '/Users/adrian/Dropbox/workspace/EcustCloudStorage/services/backend/mq/services.xml'
#ServiceConfigFile = r'C:\Users\jipingzh\Dropbox\workspace\EcustCloudStorage\services\backend\mq\services.xml'

#Server Configuration File Path
proxy_server_config_file = '/root/myclouddisk/proxy/config.ini'
# pie_server_config_file = '/Users/adrian/Dropbox/workspace/EcustCloudStorageV2/services/backend/pie/config.ini'

